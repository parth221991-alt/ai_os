# Execution Agent Specification

**Agent ID:** `execution`  
**Status:** PARTIALLY IMPLEMENTED — `PaperRunner` exists in `app/paper/paper_runner.py`. Live execution is scaffolded in `app/execution/` schemas but not wired into a live order placement module.  
**Priority:** Critical — owns the trade lifecycle from entry to exit  
**Activation:** On demand — only when all upstream agents (Signal, Debate, Risk, Portfolio) issue PROCEED

---

## Mission

Execute `ExecutionPlan` objects faithfully in paper or live mode. Manage the full trade lifecycle: entry, TP1 partial exit, TP2 activation, adaptive trailing stop, time stop, and EOD square-off.

The Execution Agent is the only agent that interacts with the broker. All other agents reason about trades in the abstract. This agent touches real or simulated money.

**Paper mode is the default and safe state.** `execution_enabled = False` in `configs/system.yaml`. The Execution Agent must check this flag on every entry before placing any order.

---

## Inputs

| Input | Source | Schema | When |
|---|---|---|---|
| Execution plan | Signal Agent + Risk Agent | `ExecutionPlan` | On entry |
| Debate verdict | Debate Agent | `DebateVerdict` | On entry (final confidence) |
| Market ticks | `app/ingestion/broker/zerodha_feed.py` | `MarketTick` | Continuous |
| Bar close events | `app/ingestion/` | `CandleHTF` | Per bar close |
| Feature vector | Signal Agent | `FeatureVector` | Per bar close (for trailing) |
| Liquidity context | Signal Agent | `LiquidityContext` | Per bar close (runner target) |
| Kill switch state | Risk Agent | `KillSwitchState` | Continuous |
| System config | `configs/system.yaml` | `execution_enabled` flag | On startup |

---

## Outputs

### `TradeEntryLog` (to `app/logging_engine/trade_logger.py`)
```python
TradeEntryLog(
    trade_id,
    signal_id,
    execution_mode,      # "paper" | "live" | "backtest"
    strike, option_type,
    entry_price,         # Plan price
    fill_price,          # Actual fill (paper: entry_price, live: actual fill)
    sl_price, tp1_price, tp2_price,
    spread_pct, slippage_pct, latency_seconds,
    quantity, risk_amount,
    missed_fill,         # True if fill rejected (slippage > threshold)
)
```

### `TradeState` (continuous, in-memory + Redis)
```python
TradeState(
    trade_id,
    sub_state,           # ACTIVE | TP1_HIT | TP2_HIT | RUNNER
    entry_price,
    current_price,
    sl_price,            # Updated by trailing stop
    tp1_price, tp2_price,
    time_stop_candles,
    candles_elapsed,
    MFE, MAE,            # Updated every tick
    tp1_hit, tp2_hit,
    exit_reason,         # None while open
)
```

### `TradeExitLog` (to `app/logging_engine/trade_logger.py` on close)
```python
TradeExitLog(
    trade_id,
    exit_reason,         # TP1 | TP2 | STOP_LOSS | TIME_STOP | INVALIDATION_EXIT | MANUAL_KILL
    gross_pnl,           # Before brokerage
    net_pnl,             # After brokerage + slippage
    MFE, MAE,
    outcome_label,       # WIN | LOSS | BREAKEVEN
    failure_labels,      # e.g., ["EARLY_STOP", "LATE_TP1"]
    quality_labels,      # e.g., ["CLEAN_TP2", "TEXTBOOK_RUNNER"]
)
```

---

## Trade Lifecycle State Machine

```
AWAITING_ENTRY
    ↓ (entry order placed/filled)
ACTIVE (initial SL active, monitoring TP1)
    ↓ (TP1 hit: tp1_price reached)
TP1_HIT (Lot 1 exited, Lot 2 SL moves to entry = breakeven)
    ↓ (TP2 hit: tp2_price reached)
TP2_HIT (Lot 2 exits at TP2, runner logic activates)
    ↓ (runner: trailing SL from tp2_price)
RUNNER (adaptive trailing, target = opposing liquidity)
    ↓ (SL hit, time stop, or EOD)
EXITED
```

Alternate exit paths from any state:
- SL hit → `EXITED` (ExitReason.STOP_LOSS)
- Time stop exceeded → `EXITED` (ExitReason.TIME_STOP)
- 15:20 IST → `EXITED` (ExitReason.INVALIDATION_EXIT — EOD)
- Manual kill switch → `EXITED` (ExitReason.MANUAL_KILL)

---

## Execution Logic (exact from `app/execution/`)

### Entry
```python
def calc_fill_price(entry_price, vol_regime, is_expiry_distortion) -> float:
    slippage_pct = {
        LOW: 0.10, NORMAL: 0.20, HIGH: 0.40,
    }[vol_regime]
    if is_expiry_distortion: slippage_pct = 0.60
    return apply_slippage(entry_price, slippage_pct, direction)

def check_missed_fill(signal_price, next_open, sl_distance) -> bool:
    # Reject if premium gapped > 0.75R before entry
    return abs(next_open - signal_price) > 0.75 * sl_distance
```

### SL Calculation
```python
def calc_sl(direction, entry_price, structural_sl, setup) -> float:
    # Tighter of structural SL vs premium max loss
    premium_max_loss = {OPA: 0.40, PES: 0.35, SFR: 0.35}
    premium_sl = entry_price * (1 - premium_max_loss[setup])
    if LONG: return max(structural_sl, premium_sl)  # Higher = tighter
    else:    return min(structural_sl, premium_sl)  # Lower = tighter
```

### TP Levels
```python
TP1 = entry + (sl_distance × 1.0)  # 1R → move SL to breakeven
TP2 = entry + (sl_distance × 2.0)  # 2R → activate runner
```

### Adaptive Trailing Stop
```python
def get_trail_lookback(momentum_decay: float) -> int:
    if decay >= 0.85: return 3    # Normal: use 3-bar low/high
    elif decay >= 0.70: return 2  # Tighter
    else: return 1                # Tightest (decay deteriorating)

def update_trail(direction, current_trail, candles, momentum_decay) -> float:
    lb = get_trail_lookback(momentum_decay)
    if LONG:
        new_trail = min(candle.low for candle in candles[-lb:])
        return max(new_trail, current_trail)  # Never moves backward
    else:
        new_trail = max(candle.high for candle in candles[-lb:])
        return min(new_trail, current_trail)
```

### Runner Target Priority
```python
def init_runner_target(direction, entry, sl, opposing_liquidity, vwap) -> float:
    sl_dist = abs(entry - sl)
    if opposing_liquidity:  return opposing_liquidity  # PDH/PDL
    elif vwap:              return vwap
    else:                   return entry + sl_dist * 3  # 3R fallback
```

### Time Stop
```python
TIME_STOPS = {
    "5m": 12,   # 12 × 5m = 60 minutes
    "15m": 8,   # 8 × 15m = 120 minutes
}
```

---

## Paper vs Live Execution

| Aspect | Paper Mode | Live Mode |
|---|---|---|
| Entry fill | `fill_price = entry_price + slippage_model()` (simulated) | `kite.place_order()` → poll fill |
| SL/TP monitoring | In-memory price comparison every bar | Real-time tick monitoring |
| Exit | Simulated at modeled price | `kite.place_order()` with `market_protection=-1` |
| Brokerage | Not deducted | Deducted from P&L |
| P&L tracking | Modeled | Real |
| Gate | `execution_enabled = False` in system.yaml | `execution_enabled = True` (manual flip) |

**SEBI compliance (live mode):** All MARKET orders include `market_protection=-1`. Never place a MARKET order without this flag.

**Live mode prerequisite:** 8 verified paper weeks with documented results. The gate is in `configs/system.yaml` (`execution_enabled: false`). Flipping it requires human action — it will never be changed by code.

---

## Confidence Scoring

The Execution Agent does not produce confidence scores. It executes deterministically given a valid `ExecutionPlan`. It does produce `quality_labels` on exit:

```python
quality_labels = []
if tp2_hit and runner_exited_at_target:
    quality_labels.append("CLEAN_TP2")
if mfe > tp2_price and exit_at_sl:
    failure_labels.append("GAVE_BACK_PROFIT")  # Runner deteriorated
if sl_distance > avg_sl_distance * 1.3:
    failure_labels.append("WIDE_SL")
if momentum_decay_at_exit < 0.5:
    failure_labels.append("DECAY_STOP")
```

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| `execution_enabled = False` but live order attempted | Code gate before `kite.place_order()` | Raise `HardGateViolationError("execution_enabled is False")`. Never proceed. |
| Missed fill (premium gapped > 0.75R) | `check_missed_fill()` returns True | Log `missed_fill=True`, `MissedFillError`. Do NOT force entry at worse price. |
| Kite API error on entry (live) | `KiteConnectError` | Retry once after 200ms. If still failing: log, emit alert, state → IDLE. |
| SL hit before first bar close | Live tick monitoring | Execute SL immediately at market. No waiting for bar close. |
| EOD square-off fails (live) | Kite API error at 15:20 | Retry 3 times at 30s intervals. If all fail: alert Monitoring Agent immediately. |
| Position desync (live reported vs tracked) | Compare Kite positions vs internal state | On every bar: reconcile. If mismatch: log `DESYNC`, alert, force manual review. |
| Time stop not triggered (bug) | Paper: compare candles_elapsed vs time_stop_candles | Add assertion: if `candles_elapsed > time_stop_candles + 2`: force time stop, log `TIME_STOP_OVERRUN` |

---

## Tool Requirements

- `app/paper/paper_runner.py` — already exists, paper mode lifecycle
- `app/execution/tp_sl.py` — already exists, TP/SL calculation
- `app/execution/trailing.py` — already exists, adaptive trailing
- `app/execution/slippage.py` — already exists, slippage model
- `app/execution/schemas.py` — `ExecutionPlan`, `TradeState`
- `app/logging_engine/trade_logger.py` — `TradeEntryLog`, `TradeExitLog`
- `app/ingestion/broker/zerodha_feed.py` — live ticks for SL monitoring
- `configs/system.yaml` — `execution_enabled` flag (must be checked on every entry)
- **Redis**: `quantara:trade:{trade_id}` → `TradeState` JSON, no TTL (until trade closes)
- **PostgreSQL**: `trade_executions` + `trade_outcomes` — persistent record

---

## Interface Contract

```python
class ExecutionAgent:
    async def enter_trade(
        self,
        plan: ExecutionPlan,
        debate_verdict: DebateVerdict,
    ) -> Union[TradeState, None]:
        """
        Execute entry. Returns TradeState if filled, None if missed fill.
        Checks execution_enabled FIRST. Never bypasses this gate.
        """
    
    async def on_bar_close(
        self,
        current_prices: Dict[int, float],  # {instrument_token: ltp}
        features: FeatureVector,
        liquidity: LiquidityContext,
        ts: datetime,
    ) -> Optional[TradeState]:
        """
        Update SL/TP/trailing on every bar close.
        Returns updated TradeState or None if no open position.
        """
    
    async def on_tick(self, tick: MarketTick) -> Optional[str]:
        """
        Real-time SL monitoring. Returns exit_reason if SL/TP hit intrabar.
        Paper mode: only checks at bar close.
        Live mode: monitors every tick.
        """
    
    async def eod_square_off(self, ts: datetime) -> Optional[TradeExitLog]:
        """Force-close all positions at 15:20 IST. Must always succeed."""
    
    def get_open_positions(self) -> List[TradeState]:
        """Return all open TradeState objects. Used by Portfolio Agent."""
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Missed fill rate** | < 5% of entries | `trade_executions.missed_fill == True` / total entries |
| **Slippage accuracy** | Model within 10% of actual (live) | Compare `slippage_pct` vs actual `fill_price - entry_price` |
| **SL hit accuracy** | 100% (never hold through SL in live) | `trade_outcomes` where `exit_price < sl_price` for LONG (0 allowed) |
| **EOD square-off rate** | 100% | Count of open positions after 15:20 IST (target: 0) |
| **Time stop accuracy** | 100% (closes at time_stop_candles exactly) | Compare `candles_elapsed` vs `time_stop_candles` at time stop exits |
| **MFE/MAE tracking accuracy** | Within 0.1pt (paper) | Compare tracked MFE/MAE vs post-hoc computed from raw candles |
| **Paper P&L integrity** | Paper P&L reconstructible from logs | Replay `trade_executions` + `trade_outcomes` vs paper account balance |
