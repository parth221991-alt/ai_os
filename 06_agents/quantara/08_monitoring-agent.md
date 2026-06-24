# Monitoring Agent Specification

**Agent ID:** `monitoring`  
**Status:** PARTIALLY IMPLEMENTED — `app/api/status_writer.py` writes JSON every 5s. `app/logging_engine/trade_logger.py` logs events. No active alerting, no anomaly detection, no feed health escalation.  
**Priority:** High — without monitoring, system failures are silent until a subscriber asks why signals stopped  
**Activation:** Always — from startup to shutdown, including pre-market and post-market

---

## Mission

Observe all other agents, the data feed, and system performance. Emit structured alerts when something is wrong. Write the status JSON that external dashboards consume. Detect anomalies that individual agents cannot see because each agent only observes its own scope.

The Monitoring Agent is the only agent that has a global view. It reads from every other agent's Redis state and the agent decision bus. It does not make trading decisions — it makes operational decisions (escalate, alert, degrade gracefully).

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| All agent decisions | Redis bus `quantara:bus:agent_decisions` | `AgentDecision[]` | Per bar |
| Feed health | `app/ingestion/processing/feed_health.py` | `FeedHealth` | Every tick |
| Trade state | Execution Agent | `TradeState` | Per bar (open positions) |
| Kill switch state | Risk Agent | `KillSwitchState` | Per trade event |
| Portfolio state | Portfolio Agent | `PortfolioState` | Per trade event |
| Signal decisions | Signal Agent | `SignalDecision \| NoTradeResult` | Per bar |
| Debate verdicts | Debate Agent | `DebateVerdict` | Per signal |
| System config | `configs/system.yaml` | `execution_enabled`, `app_env` | On startup |
| StatusWriter | `app/api/status_writer.py` | Current status JSON | Every 5s |
| Log events | `app/logging_engine/` | All log event types | Streaming |

---

## Outputs

### `SystemAlert`
```python
@dataclass(frozen=True)
class SystemAlert:
    alert_id: str           # Format: "ALERT-{YYYYMMDD}-{HHMMSS}-{code}"
    timestamp: datetime
    severity: str           # CRITICAL | HIGH | MEDIUM | LOW | INFO
    category: str           # FEED | EXECUTION | RISK | REGIME | AGENT | PERFORMANCE
    code: str               # Unique alert code (see catalog below)
    message: str            # Human-readable
    context: Dict[str, Any] # Relevant data for diagnosis
    resolved: bool          # False until resolution confirmed
    resolution_note: str
```

### `SystemStatus` (written to disk every 5s by StatusWriter)
```python
@dataclass
class SystemStatus:
    timestamp: datetime
    app_env: str
    execution_enabled: bool
    
    # Feed
    feed_status: str          # GOOD | WARNING | CRITICAL | SAFE_MODE
    feed_latency_ms: float
    last_tick_age_seconds: float
    
    # Agents
    agents_healthy: Dict[str, bool]   # All 8 agent health flags
    
    # Regime
    vol_regime: str
    market_regime: str
    session_bucket: str
    is_signal_allowed: bool
    
    # Signal
    current_state: str        # SignalState
    signals_today: int
    no_trades_today: int
    
    # Risk
    kill_switch_active: bool
    consecutive_losses: int
    daily_pnl_r: float
    
    # Portfolio
    open_positions: int
    daily_trades: int
    
    # Performance
    today_win_rate: Optional[float]
    today_profit_factor: Optional[float]
    debate_override_count: int  # How many signals Debate Agent blocked today
    
    # Alerts
    active_alerts: List[str]  # Alert IDs with severity >= HIGH
```

---

## Alert Catalog

All alerts are classified by severity and category. Complete catalog:

### CRITICAL — Requires immediate human action
| Code | Trigger | Message |
|---|---|---|
| `FEED_DEAD` | `FeedHealth.status == CRITICAL` for > 30s | "WebSocket feed dead. Trading suspended." |
| `KILL_SWITCH_ACTIVE` | `KillSwitchState.kill_switch_active = True` | "Kill switch triggered: {reason}. Manual reset required." |
| `EOD_SQUAREOFF_FAILED` | Open position after 15:25 IST | "EOD square-off failed for trade {trade_id}. Manual close required." |
| `LIVE_ORDER_IN_PAPER_MODE` | `execution_enabled=False` but order attempt detected | "CRITICAL: Live order attempted in paper mode. Immediate investigation required." |
| `REPLAY_PARITY_FAILURE` | `ReplayParityError` | "Replay hash mismatch on {trade_id}. Determinism compromised." |
| `POSITION_DESYNC` | Kite positions vs internal state mismatch | "Position desync detected. Kite: {kite_qty}, internal: {tracked_qty}." |

### HIGH — Investigate within the hour
| Code | Trigger | Message |
|---|---|---|
| `FEED_WARNING` | `FeedHealth.status == WARNING` for > 60s | "Feed degraded: {latency_ms}ms latency, {missing_ticks} missing ticks." |
| `TOKEN_EXPIRY_APPROACHING` | Zerodha token age > 22 hours | "Access token expires soon. Prepare daily re-auth." |
| `CONSECUTIVE_LOSSES_4` | `consecutive_losses >= 4` | "4 consecutive losses. Kill switch triggers at 5. Review strategy." |
| `DAILY_LOSS_1_5_PCT` | `daily_loss_pct >= 1.5%` | "Daily loss at 1.5% of equity. Kill switch triggers at 2.5%." |
| `DEBATE_OVERRIDE_RATE_HIGH` | Debate Agent OVERRIDE_BLOCK > 30% of today's signals | "Debate Agent blocking unusually high proportion of signals. Review debate transcripts." |
| `MACRO_EVENT_NOT_CONFIGURED` | `events.yaml` last_modified > 30 days | "Event calendar is stale. Update configs/events.yaml for current month." |

### MEDIUM — Review end of day
| Code | Trigger | Message |
|---|---|---|
| `CLAUDE_API_UNAVAILABLE` | Debate Agent bypassed > 3 times due to Claude unavailability | "Debate Agent running without Claude for {count} signals today." |
| `HIGH_NO_TRADE_RATE` | > 80% of setups rejected in last 2 hours | "High no-trade rate: potential overfiltering. Check regime or news agent." |
| `OVERFILTER_DETECTED` | NoTradeLog.would_have_won > 40% of today's SKIPs | "Possible overfiltering: {pct:.0f}% of skipped setups would have won." |
| `SIGNAL_DRY_SPELL` | No Tier A+ or A signals in 3+ hours during valid session | "No qualifying signals in {hours:.1f} hours. Market in CHOP?" |
| `EXPIRY_DAY_SIZE_REDUCTION` | DTE = 0 detected | "Expiry day active: position sizes reduced to 60%." |
| `DRAWDOWN_5PCT` | `drawdown_pct >= 5%` | "Drawdown at 5%. Size reduction to 75% active." |

### LOW — Informational
| Code | Trigger | Message |
|---|---|---|
| `SESSION_STARTED` | `DailyRunner.run_day()` begins | "Trading session started. App env: {app_env}." |
| `SESSION_ENDED` | EOD cleanup complete | "Session complete. Signals: {signals}, P&L: {pnl_r:.2f}R." |
| `MACRO_EVENT_TODAY` | News Agent finds HIGH/CRITICAL event | "Macro event today: {event_type} at {time_ist}. Blackout: {start}–{end}." |
| `KILL_SWITCH_MANUAL_RESET` | Manual reset performed | "Kill switch manually reset by {authorized_by}: {reason}." |
| `DEBATE_DOWNGRADE` | Debate Agent downgrades A+ to A | "Signal {signal_id} downgraded A+→A by Debate Agent: {reason}." |

---

## Anomaly Detection

The Monitoring Agent performs three anomaly checks that individual agents cannot:

### 1. Overfilter Detection
Every `NoTradeResult` logs `would_have_won` (populated 7 bars after the skipped signal). The Monitoring Agent aggregates:
```python
skip_win_rate = count(no_trade_logs where would_have_won=True) / count(all_no_trades)
if skip_win_rate > 0.40:  # Skipped setups winning > 40%
    emit OVERFILTER_DETECTED
```
Source: `app/discovery/signal_logger.py` — already logs this. Need to aggregate.

### 2. Regime Drift Detection
Compare current session's `RegimeContext.regime_fit` distribution vs 30-day baseline:
```python
chop_pct_today = count(regime_fit == BAD) / total_bars
chop_pct_30d = historical_baseline.chop_pct
if chop_pct_today > chop_pct_30d * 2.0:  # 2x historical CHOP rate
    emit REGIME_DRIFT (MEDIUM)
```

### 3. Debate Agent Coherence Check
```python
# If Debate Agent OVERRIDE_BLOCK rate > 30%: something is wrong with Claude prompt or input
override_rate = count(verdicts.verdict == OVERRIDE_BLOCK) / count(all_verdicts)
if override_rate > 0.30:
    emit DEBATE_OVERRIDE_RATE_HIGH (HIGH)
```

---

## Confidence Scoring

The Monitoring Agent does not produce confidence scores. It produces `SystemAlert` objects with deterministic severity classification.

Feed health scoring (for `feed_status` in StatusJSON):
```
feed_latency_ms < 100 AND missing_ticks == 0 AND stale_seconds < 5  → GOOD
latency 100-500 OR 1-3 missing_ticks OR stale 5-30s               → WARNING
latency > 500 OR > 3 missing_ticks OR stale > 30s                 → CRITICAL
SAFE_MODE active                                                    → SAFE_MODE
```

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| Monitoring Agent itself crashes | External watchdog process (systemd or pm2) | Restart automatically. First action on restart: emit `MONITORING_RESTARTED` alert to Telegram. |
| Redis unavailable (cannot read other agents' state) | Connection error | Switch to polling PostgreSQL for critical state. Emit `REDIS_UNAVAILABLE` (HIGH). |
| Telegram delivery failure | Retry logic in `app/telegram/sender.py` | After 3 failures: write alert to local file `logs/pending_alerts.jsonl` for manual review. |
| StatusWriter falls behind (> 10s latency) | Timestamp check on status file | Emit `STATUS_WRITER_LAG` (MEDIUM). |
| Log file growing too large (> 500MB) | File size check on startup | Emit `LOG_ROTATION_NEEDED` (LOW). Do not delete or truncate — these are append-only. |

---

## Tool Requirements

- `app/api/status_writer.py` — already exists, extend with additional fields
- `app/telegram/sender.py` — already exists, for alert delivery
- `app/ingestion/processing/feed_health.py` — already exists, `FeedHealth`
- `app/logging_engine/trade_logger.py` — streaming access to log events
- **Redis**: read access to all `quantara:*` key namespaces
- **Redis**: write to `quantara:alerts:{session_id}` — sorted set of active alerts
- **PostgreSQL**: read `no_trade_events`, `signal_decisions`, `trade_outcomes` for anomaly detection
- **New**: `system_alerts` PostgreSQL table — persists all alerts with resolution tracking
- **New**: `configs/monitoring.yaml` — alert thresholds (all magic numbers externalized)

### `configs/monitoring.yaml` (to be created)
```yaml
feed:
  warning_latency_ms: 100
  critical_latency_ms: 500
  warning_stale_seconds: 5
  critical_stale_seconds: 30

performance:
  overfilter_threshold: 0.40         # Skip win rate > 40% = overfiltering
  debate_override_threshold: 0.30    # Override rate > 30% = coherence issue
  signal_dry_spell_hours: 3.0

risk:
  consecutive_losses_alert: 4        # Alert at 4 (kill at 5)
  daily_loss_alert_pct: 1.5          # Alert at 1.5% (kill at 2.5%)

alerts:
  telegram_enabled: true
  log_to_file: true
  status_write_interval_seconds: 5
```

---

## Interface Contract

```python
class MonitoringAgent:
    async def start(self) -> None:
        """Start monitoring loops. Runs continuously."""
    
    async def on_agent_decision(self, decision: AgentDecision) -> None:
        """Process every AgentDecision from the bus."""
    
    async def on_feed_health(self, health: FeedHealth) -> Optional[SystemAlert]:
        """Check feed health. Emit alert if degraded."""
    
    async def on_trade_event(
        self,
        event_type: str,  # ENTRY | EXIT | SL_HIT | TP1_HIT | KILL_SWITCH
        data: Dict,
    ) -> None:
        """Process trade lifecycle events."""
    
    async def emit_alert(self, alert: SystemAlert) -> None:
        """
        Write alert to: Redis, PostgreSQL, Telegram (if severity >= HIGH),
        and logs/pending_alerts.jsonl (backup).
        """
    
    async def get_status(self) -> SystemStatus:
        """Build current SystemStatus from all agent states."""
    
    async def run_anomaly_checks(self) -> List[SystemAlert]:
        """
        Run overfilter detection, regime drift, debate coherence.
        Called every 15 minutes during trading hours.
        """
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Alert latency** | CRITICAL alerts delivered within 30s | Timestamp between event occurrence vs Telegram delivery |
| **False alert rate** | < 5% (alerts that resolve without intervention) | Count of resolved alerts with `resolution_note = "false alarm"` |
| **Feed health detection accuracy** | 100% of feed degradations detected | Compare FEED_WARNING/CRITICAL alerts vs actual feed events in logs |
| **Overfilter detection accuracy** | Triggers when skip win rate > threshold | Back-test on historical `no_trade_events` data |
| **Status freshness** | Status JSON updated within 10s | File modification time vs `now()` |
| **Monitoring uptime** | > 99.9% during market hours | Count of session minutes without a status write |
