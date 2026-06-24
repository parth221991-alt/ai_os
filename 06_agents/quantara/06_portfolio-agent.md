# Portfolio State Manager Specification (Tier 2)

**Agent ID:** `portfolio`  
**Status:** NOT IMPLEMENTED — Three-book CIO allocation system. No portfolio-level state exists.  
**Priority:** High — required for multi-book operation. Without this, cross-book concentration and capital allocation cannot be enforced.  
**Activation:** At system startup, before any book begins trading  
**Tier:** 2 — CIO Allocation System

---

## Mission

Be the authoritative capital accounting and cross-book risk manager.

The Portfolio State Manager owns: authoritative capital allocation per book, real-time P&L per position and book, cross-book sector concentration enforcement, rebalancing signals when allocation drifts from targets, and the `StrategyStats` context for the investment and learning agents.

This is not a single-position heat tracker. It is a three-book CIO allocation system that must detect dangerous concentrations that individual books cannot see — HDFC (Investment) + ICICI (Swing) + BANKNIFTY (Intraday) = 3× banking exposure.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| Trade outcomes | `app/logging_engine/` | `TradeExitLog` | Per trade close |
| Open positions | `ExecutionAgent.get_open_positions()` | `List[TradeState]` | Per bar |
| Account equity | Kite margins (paper: config) | `float` | Daily + on trade close |
| Signal decision | Signal Agent | `SignalDecision` | Per signal (pre-trade) |
| Risk agent state | Risk Agent | `KillSwitchState` | Per bar |
| Historical trade outcomes | PostgreSQL `trade_outcomes` | `TradeExitLog[]` | Daily on startup |

---

## Outputs

### `PortfolioState`
```python
@dataclass
class PortfolioState:
    session_id: str
    timestamp: datetime
    
    # Capital per book (in paise — integer)
    investment_capital_paise: int
    swing_capital_paise: int
    intraday_capital_paise: int
    cash_reserve_paise: int
    total_equity_paise: int
    
    # Allocation vs targets (drift detection)
    investment_alloc_pct: float     # Target: 40–60%
    swing_alloc_pct: float          # Target: 15–30%
    intraday_alloc_pct: float       # Target: 10–30%
    allocation_drift_alert: bool    # True if any book >5% outside target range
    
    # Cross-book open exposure
    total_open_positions: int
    total_open_heat_pct: float      # Combined heat across all books
    
    # Per-book P&L (paise)
    investment_pnl_paise: int
    swing_pnl_paise: int
    intraday_pnl_paise: int
    
    # Equity curve
    peak_equity_paise: int
    current_drawdown_pct: float
    
    # Cross-book concentration
    sector_exposure: Dict[str, float]          # sector → % of total portfolio
    max_sector_pct: float                      # Alert if > 40%
    max_single_stock_pct: float                # Alert if > 15%
    concentration_alert: bool
    
    # Limits
    heat_limit_breached: bool
    max_simultaneous_positions: int            # Stage 1: 1; Stage 2: 3
```

### `PortfolioDecision` (extends `AgentDecision`)
```python
verdict logic:
    BLOCK  → heat_limit_breached == True
    BLOCK  → daily_trades >= max_daily_trades per book
    BLOCK  → single sector > 40% post-trade
    BLOCK  → single stock > 15% post-trade
    WARN   → allocation drift > 5% from target range
    WARN   → concentration approaching limits
    PROCEED → all clear
```

### `StrategyStats` (consumed by Investment Agent + Learning Agent)
```python
@dataclass(frozen=True)
class StrategyStats:
    book: str                     # "intraday" | "swing" | "investment"
    strategy_type: str            # "OPA" | "PES" | "SFR" | "momentum_breakout" | etc.
    win_rate_30d: float
    profit_factor_30d: float
    expectancy_30d: float         # in R
    recent_losses: int
    last_trade_outcome: str       # WIN | LOSS | PENDING
    avg_confidence_score: float
    sample_count_30d: int
    computed_at: datetime
```

---

## Three-Book Capital Allocation

### Allocation Targets and Limits

| Book | Target | Minimum | Maximum |
|---|---|---|---|
| Investment | 50% | 40% | 60% |
| Swing | 22.5% | 15% | 30% |
| Intraday / F&O | 17.5% | 10% | 30% |
| Cash Reserve | 10% | 10% | — |

Drift > 5% outside target range triggers rebalancing signal (advisory, not automatic).

### Cross-Book Concentration Rules

- Single sector > 40% of total portfolio → ALERT + BLOCK new positions in that sector
- Single stock > 15% of total portfolio → ALERT + BLOCK new positions in that stock
- Example: HDFC Bank (Investment long) + ICICI Bank (Swing long) + BANKNIFTY CE (Intraday) = 3× banking concentration — counted together.

### Adaptive Correlation Model

Three lookback windows blended by regime:

| Regime | Blend |
|---|---|
| Normal | 40% × 20-day + 40% × 60-day + 20% × 5-day |
| Elevated volatility | 50% × 5-day + 30% × stress + 20% × 20-day |
| Crisis | 70% × stress + 30% × 5-day |

Stress correlations computed from 2020 and 2022 Indian market crisis periods.

Concentration thresholds by regime:

| Regime | Correlation Threshold |
|---|---|
| Normal | > 0.70 triggers review |
| Elevated volatility | > 0.50 triggers review |
| Crisis | > 0.30 triggers review |

---

## Confidence Scoring

All verdicts are deterministic (confidence = 1.0 always):
- Heat limit breached → BLOCK
- Daily trade limit reached → BLOCK
- Sector/stock concentration exceeds limit → BLOCK
- Approaching limits → WARN
- All clear → PROCEED

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| PostgreSQL unavailable | `asyncpg.ConnectionError` | Use Redis-cached portfolio state. No new trades until DB is back — positions cannot be accurately tracked. |
| Kite margin API fails | `KiteConnectError` | Use last known capital from PostgreSQL `capital_accounts`. Log degradation. |
| Sector data unavailable (for concentration check) | External data error | Use last known sector mapping. Flag concentration check as DEGRADED, apply stricter single-stock limits as proxy. |
| No historical trades for stats | Empty DB | Return `StrategyStats` with nulls. Learning agent notes "insufficient history." |

---

## Tool Requirements

- **PostgreSQL**: `capital_accounts`, `positions`, `orders` — authoritative capital state
- **PostgreSQL**: `portfolio_snapshots` (NEW) — daily equity curve snapshots
- **MongoDB**: `learning_metrics` — strategy stats aggregation
- **Redis**: `quantara:cache:portfolio:{session_id}` — `PortfolioState` JSON, TTL=300s
- **Redis**: `quantara:cache:portfolio:stats:{book}:{strategy}` — `StrategyStats` JSON, TTL=3600s
- **Redis**: `quantara:cache:sector:exposure:{session_id}` — cross-book sector map, TTL=600s
- `configs/portfolio.yaml` — NEW: allocation targets, concentration limits, correlation params

---

## Interface Contract

```python
class PortfolioStateManager:
    async def initialize(self, session_id: str) -> PortfolioState:
        """
        Session start. Fetch capital from PostgreSQL capital_accounts.
        Load open positions. Compute sector exposure. Compute stats.
        Never use Redis as source of truth for capital figures.
        """
    
    async def evaluate_pre_trade(
        self,
        book: str,
        signal: Union[SignalDecision, SwingSignal, InvestmentSignal],
        execution_plan: ExecutionPlan,
    ) -> PortfolioDecision:
        """
        Check: heat limits, sector concentration, stock concentration,
        daily trade limits. BLOCK or PROCEED.
        """
    
    async def on_position_open(
        self,
        book: str,
        trade_id: UUID,
        symbol: str,
        sector: str,
        risk_paise: int,
    ) -> PortfolioState:
        """Update capital allocation and concentration tracker."""
    
    async def on_position_close(
        self,
        book: str,
        trade_id: UUID,
        pnl_paise: int,
    ) -> PortfolioState:
        """Update P&L, equity curve, drawdown. Recompute concentration."""
    
    async def get_strategy_stats(
        self,
        book: str,
        strategy_type: str,
    ) -> StrategyStats:
        """Returns cached stats for Investment and Learning agents."""
    
    async def check_rebalance_needed(self) -> Optional[RebalanceSignal]:
        """
        Compare current allocation vs targets.
        Returns advisory signal if drift > 5%. Human reviews and approves.
        """
    
    def get_state(self) -> PortfolioState:
        """Return current portfolio state. Reads Redis cache."""
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Equity curve accuracy** | 100% match vs PostgreSQL trade_outcomes | Daily reconciliation: reconstructed equity vs actual |
| **Heat tracking accuracy** | 100% (open_heat_r matches actual open positions) | Cross-check `open_heat_r` vs sum of `trade_executions.risk_amount` for open trades |
| **Stats freshness** | Updated within 5 minutes of trade close | Timestamp on `StrategyStats.computed_at` |
| **Daily trade limit enforcement** | 100% (no 4th trade when limit=3) | Count days with >3 trades |
| **Debate Agent context quality** | Debate Agent receives non-null stats > 90% of signals | Count `StrategyStats.win_rate == null` / total Debate calls |
