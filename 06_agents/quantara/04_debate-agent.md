# Pre-Market Scenario & Debate Agent Specification (Tier 3)

**Agent ID:** `debate`  
**Status:** NOT IMPLEMENTED  
**Priority:** High  
**Activation:** Pre-market batch (9:00 AM daily). NOT activated per-signal during market hours.  
**Tier:** 3 — AI Intelligence Layer  
**Claude dependency:** YES — claude-haiku-4-5-20251001 for pre-market scenarios (intraday/swing). claude-sonnet-4-6 for investment thesis only.

---

## Architecture Change vs Original Design

**Original design:** Per-signal real-time Claude call during market hours.

**Revised design (from master doc):** Pre-market batch at 9:00 AM. All Claude reasoning is completed before the market opens and cached to Redis. At signal entry time, the intraday/swing agents match their signal against the cached scenario. No live Claude call during execution.

**Why:** Claude is never on the critical path for intraday or swing execution (Engineering Rule 6). A 0.5–3s Claude call at signal time introduces unacceptable latency and availability risk. The pre-cached playbook approach delivers the same adversarial quality without the execution dependency.

---

## Mission

Generate adversarial scenario playbooks before market open that intraday and swing agents consult at entry time.

For intraday: 3–5 market scenarios (trend day, expiry day, gap day, event day, range day) with bull case, bear case, and confidence penalty if signal doesn't match a cached scenario.

For swing: up to 5 setups pre-analyzed with full bull/bear framework and risk assessment.

For investment: full Sonnet thesis per INITIATE decision (see `09_investment-alpha-agent.md` — that agent owns its own Claude calls).

---

## Inputs

| Input | Source | Schema | When |
|---|---|---|---|
| Candidate signal | Signal Agent | `SignalDecision` | On A+ or A signal |
| Full feature vector | `app/features/schemas.py` | `FeatureVector` | Same bar |
| Liquidity context | `app/liquidity/schemas.py` | `LiquidityContext` | Same bar |
| Regime context | Regime Agent | `RegimeContext` | Same bar |
| Setup candidate | `app/setups/schemas.py` | `SetupCandidate` | Same bar |
| Execution plan (draft) | Execution Agent (pre-debate) | `ExecutionPlan` | Pre-computed |
| Historical performance | `app/learning/` | `StrategyStats` | Cached daily |
| Prompt context | `D:\AI_OS\03_prompts\quantara-debate.md` | System prompt | Cached per session |

### Historical Performance Context (passed to Claude)
```python
@dataclass
class StrategyStats:
    # Passed to Claude for "is this a typical A+ setup?" context
    setup_type: SetupType
    win_rate_30d: float
    profit_factor_30d: float
    expectancy_30d: float
    recent_losses: int           # Consecutive losses (kill switch awareness)
    last_signal_outcome: str     # WIN | LOSS | PENDING
    avg_confidence_score: float  # Historical mean for this setup type
    similar_setup_count: int     # How many comparable setups in last 30 days
```

---

## Outputs

### `DebateVerdict`
```python
@dataclass(frozen=True)
class DebateVerdict:
    agent_id: str = "debate"
    trace_id: UUID
    timestamp: datetime
    signal_id: str               # Links to SignalDecision.signal_id
    
    # Verdict
    verdict: str                 # "CONFIRM" | "DOWNGRADE" | "OVERRIDE_BLOCK"
    final_confidence: ConfidenceClass  # After debate adjustment
    confidence_adjustment: float # Positive (upgrade) or negative (downgrade)
    
    # Arguments
    bull_case: List[str]         # Arguments FOR the trade
    bear_case: List[str]         # Arguments AGAINST the trade
    key_risk: str                # The single most important risk to monitor
    
    # Claude metadata
    model_used: str              # "claude-sonnet-4-6"
    input_tokens: int
    output_tokens: int
    cache_hit: bool
    latency_ms: int
    
    # Reasoning
    reasoning_summary: str       # 2-3 sentence synthesis
    override_reason: Optional[str]  # If OVERRIDE_BLOCK, why
```

**Verdict definitions:**
- `CONFIRM` — debate supports the signal. No change to confidence class. Execution proceeds.
- `DOWNGRADE` — debate finds material weakness. If A+ → downgrade to A (or A → SKIP). Execution proceeds at lower size.
- `OVERRIDE_BLOCK` — debate finds a disqualifying condition not caught by deterministic gates. Signal blocked. This is rare and requires a specific, articulable reason.

---

## Confidence Scoring

The Debate Agent applies a confidence **adjustment** to the Signal Agent's confidence score. It does not replace the score.

**Adjustment bounds:** ±0.10 maximum (prevents Claude from overriding the deterministic pipeline)

**Adjustment rules:**
```
bull_case strength: 3+ strong arguments AND bear_case < 2 → adjustment = +0.04 to +0.08
neutral:            balanced bull/bear → adjustment = 0.0
bear_case strength: 3+ material risks AND bull_case < 2 → adjustment = -0.05 to -0.10
OVERRIDE_BLOCK:     explicit disqualifying condition → blocks regardless of score
```

**Classification after adjustment:**
```
adjusted_score = original_confidence_score + adjustment
if adjusted_score >= 0.72: A+
elif adjusted_score >= 0.58: A  
else: SKIP
```

If Signal Agent returned A+ (score = 0.80) and debate adjusts by -0.08 → score = 0.72 → still A+.
If Signal Agent returned A (score = 0.61) and debate adjusts by -0.06 → score = 0.55 → SKIP.

---

## Claude Prompt Architecture

### System Prompt (large, static → cached)
Stored at: `D:\AI_OS\03_prompts\quantara-debate-system.md`

Contents:
1. Quantara's strategy identity (NIFTY weekly options, buying only, three setups)
2. The 7 confidence components with weights and thresholds
3. The 19 `NoTradeReason` codes with definitions
4. The three setup types (OPA/PES/SFR) with their structural requirements
5. Historical performance context template
6. Output format specification (JSON)
7. Constraints: no signals, no price predictions, no inventing statistics

### User Message (per-signal, NOT cached)
```
SIGNAL UNDER REVIEW
Setup: {setup_type} | Direction: {direction} | Confidence: {confidence_score:.3f} ({confidence_class})
Signal ID: {signal_id}

FEATURE EVIDENCE
P_DIV: {p_div:.3f} | RS_spread: {rs_spread:.3f} | PMP: {pmp:.3f}
RVI: {rvi_regime} | Momentum decay: {momentum_decay:.3f}
Spread: {spread_pct:.2f}% ({spread_quality}) | IV regime: {iv_regime}
VWAP relation: {vwap_relation} | SPT_ROC: {spt_roc:.4f}

STRUCTURE EVIDENCE
Sweep: {sweep.detected} ({sweep.type}, {sweep.grade}) | Reclaim: {reclaim_detected}
MSS: {mss_detected} | BOS: {bos_detected} | FVG: {fvg.valid} (retested: {fvg.retested})
HTF alignment: {htf_alignment} (conflict: {structure_conflict})
Market regime: {market_regime} | Vol regime: {vol_regime} | Session: {session_bucket}

EXECUTION PLAN
Entry: {entry_price:.2f} | SL: {sl_price:.2f} ({sl_distance:.2f}pt) | TP1: {tp1_price:.2f} | TP2: {tp2_price:.2f}
Strike: {strike} {option_type} | DTE: {dte} (expiry day: {is_expiry_day})
Size: {quantity} qty | Risk: ₹{risk_amount:.0f}

RECENT PERFORMANCE ({setup_type})
Win rate (30d): {win_rate:.1%} | Profit factor: {profit_factor:.2f} | Expectancy: {expectancy:+.2f}R
Consecutive losses: {recent_losses} | Last signal: {last_signal_outcome}

DEBATE TASK
1. State the bull case (max 4 points): why should this trade fire?
2. State the bear case (max 4 points): what could go wrong?
3. Identify the single key risk to monitor during the trade.
4. Issue your verdict: CONFIRM | DOWNGRADE | OVERRIDE_BLOCK
5. If DOWNGRADE or OVERRIDE_BLOCK: state the specific reason.

Return JSON matching the DebateVerdict schema.
```

### Output Format (JSON, not free text)
```json
{
  "verdict": "CONFIRM",
  "confidence_adjustment": 0.04,
  "bull_case": ["External sweep with strong reclaim", "P_DIV 1.52 exceeds strong threshold", ...],
  "bear_case": ["Lunch chop penalty active", "HTF neutral, not full alignment"],
  "key_risk": "Exit before 13:15 if price stalls at VWAP",
  "reasoning_summary": "Strong structural evidence with measurable premium asymmetry. Lunch proximity is the primary risk — tight time management required.",
  "override_reason": null
}
```

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| Claude API timeout (> 3s) | `asyncio.wait_for` with 3s timeout | Issue `CONFIRM` with `confidence_adjustment = 0.0`. Log timeout. Never BLOCK due to Claude unavailability — Claude is enhancement, not gate. |
| Claude returns malformed JSON | `json.JSONDecodeError` | Retry once. If still malformed: `CONFIRM, adjustment = 0.0`. |
| Claude returns OVERRIDE_BLOCK with no reason | Validation on `override_reason` field | Treat as `CONFIRM`. Block without reasoning is inadmissible. |
| Claude exceeds token limit | Response truncation | Parse what exists. If `verdict` field missing: `CONFIRM, adjustment = 0.0`. |
| Anthropic API down | SDK connection error | Bypass Debate Agent entirely. Signal proceeds as if `CONFIRM`. Monitoring Agent notified. |
| Cache miss on system prompt | Cold start (first call of session) | Accept 3–5x latency for the first call. Subsequent calls use cache. |

**Core principle:** Claude failure = signal proceeds. Claude assists, it does not gate. A trade should never be blocked because Claude was unavailable.

---

## Tool Requirements

- **Anthropic SDK** (`anthropic` Python package)
- **Model**: `claude-sonnet-4-6` — required for multi-perspective reasoning
- **Prompt file**: `D:\AI_OS\03_prompts\quantara-debate-system.md` — must be kept in sync with strategy changes
- **Prompt caching**: `cache_control: {type: "ephemeral"}` on system prompt block
- **Redis**: `quantara:debate:{signal_id}` → `DebateVerdict` JSON. TTL = 3600s (one session). Prevents redundant Claude calls on replay.
- **`app/learning/clustering.py`**: `StrategyStats` calculation for historical context
- **New table**: `debate_transcripts` in PostgreSQL — full debate record for audit

### Latency Budget
- Target end-to-end Debate Agent latency: < 2.5 seconds
- Claude API call with prompt cache hit: ~0.5–1.0s
- Claude API call with cache miss: ~2.0–3.0s
- This is acceptable because the signal fires on NEXT candle open (5 minutes away), not immediately

---

## Interface Contract

```python
class DebateAgent:
    async def evaluate(
        self,
        signal: SignalDecision,
        features: FeatureVector,
        liquidity: LiquidityContext,
        regime: RegimeContext,
        setup: SetupCandidate,
        execution_plan: ExecutionPlan,
        stats: StrategyStats,
    ) -> DebateVerdict:
        """
        Submit a signal for adversarial review.
        Returns within 3 seconds (timeout = CONFIRM with 0.0 adjustment).
        Writes DebateVerdict to Redis and debate_transcripts table.
        """
    
    async def get_verdict(self, signal_id: str) -> Optional[DebateVerdict]:
        """Retrieve a cached verdict by signal_id. Used by Monitoring Agent."""
    
    def is_available(self) -> bool:
        """Check if Anthropic API is reachable. Used for health checks."""
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **OVERRIDE_BLOCK precision** | > 80% (blocked trades would have lost) | `debate_transcripts` where `verdict == OVERRIDE_BLOCK` joined with simulated outcomes |
| **DOWNGRADE accuracy** | Downgraded signals have lower win rate than non-downgraded | Compare `trade_outcomes` for DOWNGRADE vs CONFIRM signals |
| **False block rate** | < 3% (OVERRIDE_BLOCK on winning trades) | Count OVERRIDE_BLOCK where simulated outcome was WIN |
| **Latency p95** | < 2.5s | Timing logs on `evaluate()` calls |
| **Cache hit rate** | > 90% (same session) | `cache_hit` field in `DebateVerdict` |
| **API cost per signal** | < $0.003 USD | Input/output token tracking per signal |
| **Availability** | > 99% (graceful degradation on failure) | Count of bypassed evaluations (Claude unavailable) |

---

## Important Constraints

1. **Replay determinism.** A Debate verdict stored in `debate_transcripts` must be replayable. When replaying a session, the Debate Agent reads from `debate_transcripts` instead of calling Claude. This preserves the SHA-256 hash chain.

2. **No signal invention.** The Claude prompt explicitly forbids generating entry/exit prices, strike recommendations, or market predictions. Claude's role is adversarial review of a pre-formed plan, not plan creation.

3. **Confidence adjustment cap.** ±0.10 maximum. Claude cannot reclassify a SKIP into an A+ or an A+ into a SKIP in a single step. This prevents extreme behavior.

4. **OVERRIDE_BLOCK requires evidence.** A null or empty `override_reason` is treated as `CONFIRM`. Claude must cite a specific articulable condition from the 19 `NoTradeReason` codes.
