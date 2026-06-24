# News Agent Specification

**Agent ID:** `news`  
**Status:** NOT IMPLEMENTED  
**Priority:** High — `NoTradeReason.MACRO_EVENT` exists in enums but no module generates it  
**Activation:** 08:00 IST daily (pre-market), Redis cache valid for the trading day

---

## Mission

Prevent trades from firing into known high-impact macro events (RBI policy, Union Budget, SEBI announcements, FOMC, NFP, F&O expiry surprises).

The existing system has `NoTradeReason.MACRO_EVENT` wired into the validator and `NoTradeReason` enum, but nothing populates it. Trades can currently execute on RBI announcement day without any suppression. This agent closes that gap.

The News Agent does NOT predict market direction from news. It identifies calendar-based event risk and injects structured no-trade windows. Claude assists in classifying event severity from a pre-fetched event description — it does not scrape or interpret live news.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| Macro event calendar | Pre-loaded from `configs/events.yaml` (to be created) | `MacroEventCalendar` | Daily at 08:00 |
| Claude event classification | Anthropic API (haiku) | Structured JSON | Once per event, cached |
| Current IST timestamp | `app/common/time_utils.now_ist()` | `datetime` | Per-bar |
| DTE | `app/market/expiry_calendar.py` | `int` | Per-bar |
| Existing `NoTradeReason` codes | `app/common/enums.py` | `NoTradeReason` | Read-only |

### `MacroEventCalendar` Schema (proposed)
```python
@dataclass(frozen=True)
class MacroEvent:
    event_id: str
    event_type: str          # RBI_POLICY | UNION_BUDGET | SEBI_CIRCULAR | 
                             # FOMC | NFP | FO_EXPIRY_SPECIAL | CORPORATE_RESULT
    date: date               # IST date of event
    time_ist: Optional[time] # Announcement time if known
    window_before_mins: int  # Suppress trading N minutes before
    window_after_mins: int   # Suppress trading N minutes after
    severity: str            # CRITICAL | HIGH | MEDIUM
    description: str         # Human-readable

@dataclass(frozen=True)
class MacroEventCalendar:
    date: date
    events: List[MacroEvent]
    trading_day_valid: bool  # False = NSE holiday
    high_impact_today: bool  # Any CRITICAL/HIGH severity event
```

---

## Outputs

### `NewsAgentDecision` (extends `AgentDecision`)
```python
@dataclass(frozen=True)
class NewsAgentDecision:
    agent_id: str = "news"
    trace_id: UUID
    timestamp: datetime
    verdict: str             # "PROCEED" | "BLOCK" | "WARN"
    confidence: float        # 1.0 for calendar-based blocks (deterministic)
    reasons: List[str]
    blocking_reasons: List[str]
    
    # News-specific
    active_events: List[MacroEvent]
    in_blackout_window: bool
    blackout_start: Optional[datetime]
    blackout_end: Optional[datetime]
    no_trade_reason: Optional[NoTradeReason]  # Always MACRO_EVENT if blocking
    severity: Optional[str]                   # CRITICAL | HIGH | MEDIUM
```

**Verdict rules:**
- `BLOCK` — any CRITICAL severity event, or HIGH severity with known announcement time and current time within `window_before_mins` + `window_after_mins`
- `WARN` — MEDIUM severity events or HIGH severity without known time (all-day caution)
- `PROCEED` — no events today, or only LOW severity

---

## Confidence Scoring

The News Agent does not use probabilistic confidence. Its verdicts are deterministic:
- Calendar-based BLOCK: confidence = 1.0 (certain — the event is scheduled)
- Claude-classified WARN: confidence = 0.70 (AI classification of an unknown event)
- PROCEED: confidence = 1.0

If Claude is unavailable, the News Agent defaults to WARN (not BLOCK) for any unclassified events and logs the degradation. A Claude failure never causes a false PROCEED on a known high-impact day.

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| `events.yaml` missing or malformed | `ConfigValidationError` on startup | Agent enters WARN state for full day — downstream receives WARN not BLOCK |
| Claude API unavailable | `httpx.TimeoutError` or Anthropic SDK error | Fall back to `events.yaml` calendar only; log Claude unavailability to `agent_decisions` |
| NSE holiday not detected | Calendar gap | Default to normal trading; post-hoc review catches this |
| Event calendar not updated for month | Staleness check: if `events.yaml` last_modified > 30 days, emit WARN in monitoring | Monitoring Agent alerts; human must update calendar |
| Unknown event type appears | Claude returns unrecognized classification | Log as MEDIUM severity, emit WARN |

---

## Tool Requirements

- **`configs/events.yaml`** (to be created): annual calendar of macro events with severity classification
- **`app/market/expiry_calendar.py`**: already exists — DTE and expiry date calculation
- **`app/common/time_utils.py`**: already exists — `now_ist()`, `is_in_window()`
- **Anthropic SDK** (haiku): optional enhancement for classifying unscheduled events found in pre-market headlines
- **Redis**: key `quantara:news:{YYYY-MM-DD}` → `MacroEventCalendar` JSON, TTL = 86400s

### `configs/events.yaml` structure (to be created)
```yaml
events_version: "2026"
events:
  - event_id: "RBI_2026_01"
    event_type: RBI_POLICY
    date: "2026-02-06"
    time_ist: "10:00"
    window_before_mins: 60
    window_after_mins: 90
    severity: CRITICAL
    description: "RBI MPC Policy Announcement"
  
  - event_id: "BUDGET_2026"
    event_type: UNION_BUDGET
    date: "2026-02-01"
    time_ist: "11:00"
    window_before_mins: 120
    window_after_mins: 180
    severity: CRITICAL
    description: "Union Budget 2026-27"
```

---

## Interface Contract

```python
class NewsAgent:
    async def initialize(self, date: date) -> MacroEventCalendar:
        """Load event calendar for the trading day. Called at 08:00 IST."""
    
    async def evaluate(self, ts: datetime) -> NewsAgentDecision:
        """
        Called before every Signal Agent evaluation.
        Returns BLOCK if current time falls in a blackout window.
        O(1) lookup — calendar is pre-loaded at initialize().
        """
    
    async def get_calendar(self) -> MacroEventCalendar:
        """Return current day's calendar. Used by Monitoring Agent."""
    
    def is_blackout(self, ts: datetime) -> bool:
        """Quick boolean check. Used by Signal Agent pre-filter."""
```

**Redis contract:**
- Write: `quantara:news:{YYYY-MM-DD}` → serialized `MacroEventCalendar`
- Read: any agent can read this key to inspect today's event risk
- TTL: 86400s (expires at midnight, refreshed next morning)

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Miss rate** | 0 (zero missed CRITICAL events) | Count of CRITICAL events that fired a trade instead of BLOCK |
| **False positive rate** | < 5% of trading days blocked with no event impact | Count of BLOCK days where market moved normally |
| **Latency** | < 10ms per `evaluate()` call | Timing instrumentation in agent |
| **Calendar freshness** | Updated within 7 days of use | `events.yaml` file modification timestamp vs current date |
| **Claude classification accuracy** | > 90% on known event types | Compare Claude classification vs manual labels on historical events |

---

## Implementation Notes

The minimum viable News Agent is purely calendar-based — no Claude required. Just load `events.yaml`, check if current time falls in a blackout window, return BLOCK/PROCEED. This is one day's work to implement.

Claude enhancement (phase 2): add a pre-market step where Claude reviews the event description and classifies any unrecognized event types from an external economic calendar API (e.g., Investing.com API). System prompt is large and static → cache it.

The `NoTradeReason.MACRO_EVENT` code is already wired into the validator at step 8. The News Agent output plugs directly into that slot.
