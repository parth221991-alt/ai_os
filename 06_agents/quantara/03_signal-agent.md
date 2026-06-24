# Signal Agent Specification

**Agent ID:** `signal`  
**Status:** IMPLEMENTED — formalization of `TierEngine` + `DiscoveryDispatcher` + `StateMachineEngine` + `ConfidenceScoring`  
**Priority:** Core — the central agent in the pipeline  
**Activation:** 09:44 IST (one bar before `signal_start: 09:45`), per-bar thereafter

---

## Mission

Own the complete signal lifecycle from raw `FeatureVector` to a typed `SignalDecision` or `NoTradeResult`. 

The Signal Agent is the formalization of four existing subsystems that currently run as a sequential pipeline inside `DailyRunner._run_session()`:
1. `TierEngine` (classification)
2. `StateMachineEngine` (state transitions)
3. Hard gates + `Validator` (10-step validation)
4. `ConfidenceScoring` (7-component scoring)

As an agent, it consumes `AgentDecision` verdicts from News, Regime, Risk, and Portfolio agents before committing to a `SignalDecision`. It respects their BLOCK verdicts as hard gates equivalent to the existing hard gate system.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| Feature vector | `app/features/feature_pipeline.py` | `FeatureVector` | Per bar close |
| Liquidity context | `app/liquidity/liquidity_engine.py` | `LiquidityContext` | Per bar close |
| Regime context | Regime Agent | `RegimeContext` | Per bar close |
| Setup candidate | `app/setups/setup_registry.py` | `SetupCandidate` | On setup trigger |
| News decision | News Agent | `NewsAgentDecision` | Per bar (cached) |
| Risk decision | Risk Agent | `RiskAgentDecision` | Per bar |
| Portfolio decision | Portfolio Agent | `PortfolioAgentDecision` | Per bar |
| Feed health | `app/ingestion/processing/feed_health.py` | `FeedHealth` | Continuous |
| Current state | `StateMachineEngine` | `SignalState` | Continuous |
| DTE, expiry flag | `app/market/expiry_calendar.py` | `int`, `bool` | Per bar |

---

## Outputs

### On signal approval:
```python
SignalDecision(
    signal_id,       # Format: "QNT-{YYYYMMDD}-{HHMM}"
    trace_id,
    timestamp,
    setup,           # OPA | PES | SFR
    direction,       # LONG | SHORT
    confidence,      # A+ | A
    confidence_score,
    reasons,         # List of human-readable evidence strings
    penalties,       # Soft penalties that reduced score
    entry_type,      # Always "NEXT_CANDLE_OPEN"
    status,          # Always "APPROVED"
)
```

### On rejection:
```python
NoTradeResult(
    trace_id,
    timestamp,
    decision,        # Always "NO_TRADE"
    reason_codes,    # List[NoTradeReason] — 19 possible codes from enums.py
    reasons,         # Human-readable
    setup,           # What setup was being evaluated (if applicable)
    is_hard_gate,    # True = hard gate, False = soft/confidence/agent-block
)
```

### State transitions (published to agent bus):
```python
StateTransitionLog(
    from_state,
    to_state,
    reason,
    trace_id,
)
```

---

## Confidence Scoring

The Signal Agent applies the existing 7-component scoring system from `app/confidence/scoring.py`.

**Component weights (from `configs/confidence.yaml`):**

| Component | Weight | Source |
|---|---|---|
| `setup_quality` | 0.30 | Setup type + completeness (SFR_A+ = 0.30, OPA_primary = 0.18) |
| `premium_quality` | 0.25 | P_DIV × RS_spread × PMP combination |
| `liquidity_quality` | 0.15 | Sweep grade (external = 0.15, internal = 0.07) |
| `structure_quality` | 0.10 | Reclaim + MSS + FVG completeness |
| `htf_alignment` | 0.10 | `LiquidityContext.htf_alignment` |
| `regime_fit` | 0.07 | `RegimeContext.regime_score` (from Regime Agent) |
| `execution_quality` | 0.03 | Reserved for future live execution data |

**Classification thresholds:**
- A+ ≥ 0.72: full size (1.0× risk)
- A ≥ 0.58: reduced size (0.70× risk)
- SKIP < 0.58: paper-only, no Telegram

**Active soft penalties (from `configs/confidence.yaml`):**
- `weak_reclaim: -0.05`
- `secondary_opa_window: -0.04`
- `high_iv: -0.05`
- `lunch_chop: -0.08`
- `minor_htf_conflict: -0.06`
- `weak_bos: -0.03`
- `htf_neutral: -0.03`

---

## Validation Order (NEVER reorder — replay determinism)

The existing 10-step validator from `app/signal_engine/validator.py` applies in this exact order:

```
1. Data integrity         — feed healthy + timestamp drift < 2.0s
2. Spread quality         — spread > 1.2% = SPREAD_FAILURE
3. IV distortion          — PM_CE_z > 1.5 AND PM_PE_z > 1.5 AND |P_DIV| < 0.70
4. Setup logic validity   — not expired, not invalidated
5. Feature thresholds     — premium asymmetry soft penalty if spot conflict
6. HTF alignment          — SEVERE_CONFLICT = HTF_CONFLICT (SFR exception: |P_DIV| > 1.8)
7. Spot validation        — VWAP mismatch penalizes confidence
8. No Trade Engine        — regime, lunch, structural (from Regime + News agents)
9. Confidence score       — < 0.58 = LOW_CONFIDENCE
10. Risk eligibility      — kill switch, daily/weekly limits (from Risk Agent)
```

**Agent BLOCK injection (new — not currently implemented):**
Between steps 8 and 9, check all agent decisions:
```python
for agent_decision in [news_decision, regime_decision, risk_decision, portfolio_decision]:
    if agent_decision.verdict == "BLOCK":
        return NoTradeResult(
            reason_codes=[agent_decision.no_trade_reason],
            is_hard_gate=True
        )
```

---

## Tier Classification (from `TierEngine`)

The Signal Agent classifies every bar into a tier for the discovery/paper system:

| Tier | Condition | Action |
|---|---|---|
| **B** | `|P_DIV| >= 0.04` | Log only — no trade, no Telegram |
| **A** | `|P_DIV| >= 0.07` AND VWAP aligned AND persistence ≥ 2 bars AND momentum_decay ≥ 0.50 | Paper trade at 70% size + Telegram [A] |
| **A+** | `|P_DIV| >= 0.14` AND persistence ≥ 2 bars | Paper trade at 100% size + Telegram [A+] |

Hard gates for tier (only 2 — designed for high-volume statistical learning):
1. `spread_reject=True` → skip tier (cost destroys edge)
2. `feed_stale=True` → skip tier (bad data)

**Target volume:** 120–250 signals/month (8–15/day) for statistical learning.

---

## State Machine

Existing implementation in `app/state_machine/engine.py`. Transitions:

| From | To | Trigger |
|---|---|---|
| `IDLE` | `WATCHING` | Tier A+ or A signal detected |
| `WATCHING` | `CANDIDATE` | Setup conditions met |
| `WATCHING` | `IDLE` | Timeout (20 candles) |
| `CANDIDATE` | `VALIDATING` | Setup ready for full validation |
| `CANDIDATE` | `WATCHING` | Timeout (5 candles) or invalidation |
| `VALIDATING` | `SIGNAL_READY` | All 10 validation steps pass |
| `VALIDATING` | `WATCHING` | Any hard gate fires |
| `SIGNAL_READY` | `IN_TRADE` | Execution Agent confirms entry |
| `SIGNAL_READY` | `WATCHING` | Timeout (1 candle — missed entry) |
| `IN_TRADE` | `EXITING` | SL / TP / time stop / manual kill |
| `EXITING` | `EXITED` | Exit confirmed |
| `EXITED` | `IDLE` | Reset |

SAFE_MODE override: any state → `IDLE` (bypasses all validation).

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| `FeatureVector` missing a field | Pydantic validation on consumption | `NoTradeResult(DATA_FAILURE)`, state → IDLE |
| State machine invalid transition | `InvalidStateTransitionError` | Log, force IDLE, emit alert |
| All agent inputs return WARN | Sum of warnings | Proceed with lower confidence (penalties applied) |
| Any agent input returns BLOCK | `AgentDecision.verdict == "BLOCK"` | `NoTradeResult(MACRO_EVENT or regime code)`, state → IDLE |
| Confidence scoring returns NaN | Arithmetic guard in scoring.py | `NoTradeResult(LOW_CONFIDENCE)` |
| Setup times out | `STATE_TIMEOUTS` exceeded | State regresses: CANDIDATE → WATCHING, WATCHING → IDLE |
| Replay parity failure | `ReplayParityError` | Emergency IDLE, alert Monitoring Agent |

---

## Tool Requirements

- `app/signal_engine/validator.py` — already exists, 10-step validation
- `app/signal_engine/hard_gates.py` — already exists, binary gate checks
- `app/signal_engine/signal_builder.py` — already exists, assembles `SignalDecision`
- `app/confidence/scoring.py` — already exists, 7-component scoring
- `app/state_machine/engine.py` — already exists, FSM
- `app/discovery/tier_engine.py` — already exists, tier classification
- `app/features/schemas.py` — `FeatureVector` definition
- `app/liquidity/schemas.py` — `LiquidityContext` definition
- **New**: `app/market/schemas.py` — `RegimeContext` definition (Regime Agent output)
- **Redis**: `quantara:sm:{session_id}` → current `SignalState` string
- **Redis**: `quantara:features:{session_id}:cache` → latest `FeatureVector`, TTL=600s

---

## Interface Contract

```python
class SignalAgent:
    async def on_bar_close(
        self,
        features: FeatureVector,
        liquidity: LiquidityContext,
        regime: RegimeContext,
        agent_decisions: Dict[str, AgentDecision],  # news, risk, portfolio
        ts: datetime,
    ) -> Union[SignalDecision, NoTradeResult]:
        """
        Core per-bar evaluation. Called every 5 minutes during trading hours.
        Returns SignalDecision if a valid signal exists, NoTradeResult otherwise.
        All NoTradeResults are logged via TradeLogger.
        """
    
    async def on_trade_exit(self, trade_id: UUID, exit_reason: ExitReason) -> None:
        """Notified when execution agent closes a trade. Transitions state EXITED → IDLE."""
    
    def get_state(self) -> SignalState:
        """Return current FSM state."""
    
    async def force_idle(self, reason: str) -> None:
        """Emergency reset. Used by kill switch and SAFE_MODE."""
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Signal quality rate** | > 60% of emitted signals become A or A+ | `signal_decisions` table: count approved vs total evaluated |
| **Hard gate accuracy** | < 5% false positive blocks | `no_trade_events` table: would_have_won on hard-gated setups |
| **State machine stability** | < 1% invalid transition attempts | `state_transitions` table: count `InvalidStateTransitionError` |
| **Confidence calibration** | A+ win rate > 65%, A win rate > 55% | `trade_outcomes` joined with `signal_decisions` |
| **Replay parity** | 100% | `replay_engine.py` parity verification on monthly replay |
| **No-trade analysis** | < 25% overfilter rate | `no_trade_events` where `would_have_won == True` / total no-trades |
