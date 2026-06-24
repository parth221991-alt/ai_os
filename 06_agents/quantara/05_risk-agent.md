# Risk Agent Specification (Tier 0)

**Agent ID:** `risk`  
**Status:** IMPLEMENTED — upgrade required to 3-level kill switch, drawdown-adjusted sizing, Black Swan Protocol, and full Tier 0 hard limits  
**Priority:** Critical — supreme authority. No other agent can override.  
**Activation:** At system startup — Tier 0 is verified before all other tiers  
**Tier:** 0 — Survivability Foundation

---

## Mission

Be the supreme authority over all capital risk. Nothing bypasses this agent.

The Tier 0 Risk Engine operates independently of all strategy logic. It owns: 3-level kill switch hierarchy, drawdown-adjusted position sizing, per-order hard limit checks, Black Swan Protocol, capital preservation mode, consecutive loss governor, and the settlement-aware margin model.

Unlike advisory agents, the Risk Engine enforces absolutely. Its BLOCK verdicts terminate the order flow immediately and are logged to the audit trail before any downstream notification.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| Trade outcomes | `app/logging_engine/` | `TradeExitLog` | Per trade close |
| Signal decision | Signal Agent | `SignalDecision` | Per signal |
| Regime context | Regime Agent | `RegimeContext` | Per bar |
| Account equity | Zerodha `kite.margins()` (paper: config) | `float` | Daily + on trade close |
| DTE, expiry flag | `app/market/expiry_calendar.py` | `int`, `bool` | Per bar |
| Kill switch state | Redis `quantara:ks:{session_id}` | `KillSwitchState` | Continuous |

---

## Outputs

### `KillSwitchState` (3-level)
```python
@dataclass
class KillSwitchState:
    level: int                     # 0=none, 1=new entries blocked, 2=all blocked, 3=emergency flatten
    reason: Optional[str]
    activated_at: Optional[datetime]
    reset_code_hash: Optional[str] # Generated at activation. Wrong code = rejected.
    # Level 3 can ONLY be reset by manual system restart — no API reset.
```

### `RiskAgentDecision` (extends `AgentDecision`)
```python
@dataclass(frozen=True)
class RiskAgentDecision:
    agent_id: str = "risk"
    trace_id: UUID
    timestamp: datetime
    verdict: str                   # "PROCEED" | "BLOCK" | "WARN"
    confidence: float              # 1.0 (deterministic)
    reasons: List[str]
    blocking_reasons: List[str]

    # Kill switch
    kill_switch_level: int         # 0 / 1 / 2 / 3
    black_swan_active: bool
    capital_preservation_mode: bool

    # Sizing (populated on PROCEED)
    approved_quantity: Optional[int]
    approved_risk_amount_paise: Optional[int]  # integer paise
    drawdown_size_mult: float      # 1.0 / 0.75 / 0.50 / 0.25 / 0.00
    consecutive_loss_mult: float   # per time-windowed governor
    
    # State
    daily_loss_pct: float
    weekly_loss_pct: float
    drawdown_pct: float
    consecutive_losses_60min: int
```

### `SizingResult`
```python
@dataclass(frozen=True)
class SizingResult:
    base_risk_paise: int           # 1.0% of equity in paise
    confidence_mult: float         # A=1.0, B=0.80, C=0.65
    setup_mult: float              # SFR=1.5, PES=1.0, OPA=0.75
    drawdown_mult: float           # see drawdown table
    consecutive_loss_mult: float   # per governor
    dte_mult: float                # 0.60 to 1.0
    vol_mult: float                # 0.80 (elevated) or 1.0
    final_risk_paise: int          # min(all_mults * base, 2% equity cap)
    quantity: int                  # floor(final_risk / sl_distance), never 0
```

---

## Tier 0 Hard Limit Checks (8 Checks — All Must Pass)

Applied to every order BEFORE business logic. Checked in order. First failure short-circuits.

```python
HARD_LIMIT_CHECKS = [
    check_kill_switch_level,          # Level 1+ = no new entries, Level 2+ = all blocked
    check_black_swan_protocol,        # Active = no new entries
    check_daily_loss_limit,           # Absolute paise figure from config
    check_drawdown_halt_threshold,    # >20% drawdown = HALT
    check_capital_preservation_mode,  # Active = no new entries
    check_margin_utilization,         # Post-trade utilization ≤ 70%
    check_confidence_floor,           # Signal confidence ≥ 0.50 (LAYER 1 CONSTANT)
    check_rr_floor,                   # Signal RR ≥ 2.0 (LAYER 1 CONSTANT)
]
```

Every rejection produces a specific, auditable reason code. Every rejection is logged to `audit_trail` in PostgreSQL.

---

## Kill Switch Hierarchy

| Level | Trigger | Effect | Reset Method |
|---|---|---|---|
| 0 | None | Normal operation | N/A |
| 1 | New entries blocked | Stop new trades, existing managed normally | Authorization code via API |
| 2 | All trading blocked | Stop all + cancel pending + pause all strategies | Authorization code via API |
| 3 | Emergency flatten | Trigger EmergencyFlattenService immediately | Manual system restart ONLY |

**Automatic cascade triggers:**
- Daily loss limit breached → Level 2
- Drawdown halt threshold (>20%) → Level 2
- Black swan protocol active → Level 1 (human decides Level 3)
- WebSocket reconnection failed after backoff → Level 2
- Reconciliation DISCREPANCY → Level 2

**Reset codes:** Generated at activation time. Wrong code = rejected. No bypass possible.

**Level 3:** Written to `kill_switch_log` in PostgreSQL. Sends EMERGENCY alert (Telegram + Twilio voice). Cannot be reset via API — requires manual system restart after investigation.

---

## Drawdown-Adjusted Sizing

| Drawdown | Size Multiplier | State |
|---|---|---|
| 0–5% | 1.00× | Normal |
| 5–10% | 0.75× | Size reduced |
| 10–15% | 0.50× | Size heavily reduced |
| 15–20% | 0.25× | Near-halt |
| >20% | 0.00× | HALT — Level 2 kill switch triggered |

---

## Consecutive Loss Governor (Time-Windowed, Per Cross-Strategy)

| Condition | Action |
|---|---|
| 2 losses in 60 min | Reduce size 25% |
| 3 losses in 60 min | Reduce size 50% + Level 1 alert |
| 4 losses in 60 min | Pause strategy 2 hours |
| 5 losses in session | Halt strategy for day |

Governor applies to each book separately AND to combined portfolio losses.

---

## Capital Preservation Mode

- **Trigger:** Daily loss reaches 50% of max daily loss limit
- **Effect:** No new entries. All existing stops tightened to 50% of normal ATR level.
- **Alert:** CRITICAL (Level 2) dispatched immediately via Telegram.
- **Exit:** Manual authorization OR end of trading day.

---

## Settlement-Aware Margin Model

```python
def calc_available_capital(account: CapitalAccount) -> int:  # returns paise
    return (
        account.equity_delivery_settled
        + account.fo_daily_settled
        + int(account.fo_mtm_unrealized * 0.80)  # 80% haircut on unrealized
        - account.margin_blocked_span
        - account.margin_blocked_exposure
        - account.cash_reserve_mandatory
    )
```

This calculation runs before every order. At ₹5 crore, a wrong capital figure = margin call risk.

---

## Black Swan Protocol

**Triggers (any one sufficient):**
- VIX intraday change > 30% in either direction
- NIFTY move > 4% from previous close by 10 AM
- 40%+ of NIFTY 50 stocks at circuit filters
- ATM options spread > ₹100
- NSE circuit breaker L1 or above triggered
- 3+ position stop losses hit within 5 minutes

**Phase 1 — Immediate (within 30 seconds):**
- Level 1 kill switch
- Cancel all pending limit orders
- EMERGENCY alert with: trigger reason, current positions, P&L, margin utilization

**Phase 2 — Assessment (30s to 5min):**
- Do NOT autonomously flatten — worst prices guaranteed in black swan
- Widen all stops to 2× normal ATR (prevent stop hunting)
- Calculate max loss if all positions hit widened stops
- If max loss < 5% portfolio: HOLD, wait for human
- If max loss > 5%: URGENT alert, 3-minute human response window

**Phase 3 — Resolution (human required):**
- Option A: Resume at reduced size after human confirms stability
- Option B: Human orders flatten, system executes at human-approved timing
- Option C: No human response in 10 minutes → attempt orderly limit-order exit

---

## Confidence Scoring

All verdicts are deterministic (confidence = 1.0 always):
- Kill switch Level 2+ → BLOCK
- Black swan active → BLOCK
- Daily loss limit breached → BLOCK
- Drawdown > 20% → BLOCK
- Capital preservation mode → BLOCK (new entries)
- Drawdown 5–20% → WARN + size reduction
- Consecutive loss governor triggered → WARN + size reduction
- All clear → PROCEED

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| Redis unavailable | `redis.ConnectionError` | Reconstruct state from PostgreSQL `risk_state`. If reconstruction fails: default kill switch Level 1 (conservative). |
| PostgreSQL unavailable | `asyncpg.ConnectionError` | Cannot determine capital or positions → Level 2 kill switch. No trading without DB. |
| Account equity unavailable (Kite API) | `KiteConnectError` on margins | Use last known equity from PostgreSQL `capital_accounts`. Log degradation. |
| Reconciliation DISCREPANCY | Reconciliation engine | Automatic Level 2 kill switch. Requires human sign-off to resume. |
| Black swan protocol already active + new trigger | Multiple triggers | Each trigger logged independently. Protocol stays active until human explicitly clears it. |

---

## Tool Requirements

- `app/risk/kill_switch.py` — upgrade to 3-level hierarchy
- `app/risk/sizing.py` — add drawdown-adjusted sizing table
- `app/risk/risk_engine.py` — add 8 hard limit checks, capital preservation mode
- `app/risk/black_swan.py` — NEW: black swan detection and protocol
- `app/risk/margin_model.py` — NEW: settlement-aware margin calculation
- `configs/risk.yaml` — add: drawdown thresholds, consecutive loss governor params, margin ceiling
- **PostgreSQL**: `risk_state` (daily), `kill_switch_log` (all activations), `audit_trail` (BEFORE actions)
- **Redis**: `quantara:state:risk:daily` — no TTL; `quantara:state:kill_switch` — no TTL

---

## Interface Contract

```python
class Tier0RiskEngine:
    async def initialize(self) -> KillSwitchState:
        """Reconstruct state from PostgreSQL risk_state. Never trust Redis alone."""
    
    async def check_hard_limits(
        self,
        signal: Union[SignalDecision, SwingSignal, InvestmentSignal],
        execution_plan: ExecutionPlan,
    ) -> RiskAgentDecision:
        """8 hard limit checks. All must pass. First failure = BLOCK immediately."""
    
    async def on_trade_close(
        self,
        book: str,            # "intraday" | "swing" | "investment"
        trade_id: UUID,
        outcome: str,         # "WIN" | "LOSS"
        pnl_paise: int,
        pnl_pct: float,
    ) -> KillSwitchState:
        """Update loss counters. Trigger kill switch if thresholds crossed."""
    
    async def trigger_kill_switch(
        self,
        level: int,           # 1, 2, or 3
        reason: str,
    ) -> KillSwitchState:
        """Write to audit_trail FIRST, then to kill_switch_log, then execute effect."""
    
    async def reset_kill_switch(
        self,
        reset_code: str,
        authorized_by: str,
    ) -> bool:
        """Validate reset_code against hash. Level 3 always returns False."""
    
    def is_trading_permitted(self, order_type: str = "new") -> bool:
        """True only if kill_switch.level == 0 and no preservation mode active."""
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Kill switch trigger accuracy** | 100% (never misses a trigger) | Verify every session has kill switch correctly active on day with 5 losses |
| **Size reduction accuracy** | 100% (correct multiplier on every trade) | Compare `trade_executions.quantity` vs `sizing.calc_final_quantity()` on replay |
| **State reconstruction accuracy** | 100% (Redis vs DB reconstructed state match) | Daily reconciliation on session start |
| **Manual reset audit coverage** | 100% (every reset logged with reason) | `agent_decisions` table: count manual resets vs logged resets |
| **Sizing cap enforcement** | 100% (no trade > 2% equity) | `trade_executions.risk_amount / account_equity <= 0.02` |
