# Swing Alpha Agent Specification (Tier 1)

**Agent ID:** `swing_alpha`  
**Status:** NOT IMPLEMENTED  
**Priority:** High — required for Swing Book operation (Phase 3)  
**Activation:** 09:30 IST, monitors watchlist continuously during market hours  
**Tier:** 1 — Alpha Generation Engine  
**Claude dependency:** YES — claude-haiku-4-5-20251001 for pre-market batch debate. No live Claude calls during execution.

---

## Mission

Identify and manage 2–30 day momentum and breakout setups in individual equities.

The Swing Book targets 15–30% of total capital. Swing positions bridge the gap between intraday noise and long-term conviction — they capture multi-day trend moves, sector rotation, and earnings-driven breakouts.

**Key constraint:** No live Claude calls at execution time. All debate and scenario analysis is pre-computed in the pre-market batch (9:00–9:10 AM). The swing agent at entry time matches against cached scenarios — it does not generate new analysis.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| Daily OHLCV | MongoDB `market_data` | `DailyCandle` | Daily (post-close) |
| Weekly OHLCV | MongoDB `market_data` | `WeeklyCandle` | Weekly |
| Volume data | Market data feed | `VolumeProfile` | Daily |
| Sector rankings | Intelligence Agent | `SectorRanking` | 3× daily |
| Pre-market swing scenarios | Intelligence Agent cache | `SwingScenario[]` | Daily at 9:10 AM |
| Portfolio state | Portfolio State Manager | `PortfolioState` | Per signal |
| Regime context | Context/Regime Engine | `RegimeContext` | Per bar |

---

## Outputs

### `SwingSignal`
```python
@dataclass(frozen=True)
class SwingSignal:
    agent_id: str = "swing_alpha"
    trace_id: UUID
    timestamp: datetime
    
    symbol: str
    direction: str          # "long" | "short"
    confidence: float       # 0.0 to 1.0
    
    # Entry
    entry_zone_low: int     # paise
    entry_zone_high: int    # paise
    entry_trigger: str      # "breakout" | "pullback" | "reversal"
    
    # Exit plan
    stop_loss_paise: int
    target_1_paise: int
    target_2_paise: Optional[int]
    hold_days_max: int      # Max hold period (2–30 days)
    no_earnings_within_days: bool  # Must be True for INITIATE
    
    # RR and sizing
    rr_ratio: float         # Must be ≥ 2.5
    position_size_pct: float  # % of swing book capital
    
    # Context
    sector: str
    sector_strength: str    # STRONG | IMPROVING | NEUTRAL | WEAK
    volume_expansion: float # vs 20-day average at breakout
    
    # Explainability
    scenario_match: Optional[SwingScenarioMatch]
    explainability: ExplainabilityBlock
```

---

## Entry Requirements (All Mandatory)

| Requirement | Threshold |
|---|---|
| Daily trend alignment | Bullish (or bearish for short) |
| Weekly trend alignment | Must agree with daily |
| Volume expansion on breakout | > 1.5× 20-day average volume |
| Sector strength | STRONG or IMPROVING (must outperform NIFTY) |
| Market regime | TRENDING or BREAKOUT (not RANGE) |
| Risk:Reward | ≥ 2.5 |
| Confidence | ≥ 0.70 |
| Earnings proximity | No major earnings within hold period |
| Portfolio concentration | No sector breach post-trade |
| Regime | Not event day (or with event-specific playbook) |

Any one failure = NO_TRADE.

---

## Pre-Market Debate (Claude Haiku — Batch)

**When:** Daily, 9:00–9:10 AM, as part of pre-market intelligence package.

**Protocol:**
1. Overnight screener identifies up to 5 highest-scoring swing setups from watchlist
2. One Haiku call with all 5 setups (mandatory batching — never 5 separate calls)
3. Output: per-setup bull case, bear case, key risk, probability estimate, playbook
4. Cached to Redis `quantara:cache:scenarios:swing:{date}` with 24-hour TTL
5. At execution time: match signal against cached scenario. No live Claude call.

**Batch prompt structure:**
```
SWING SETUPS FOR REVIEW — {date}
[Regime: {trend_state}, {volatility_state}, Sector leaders: ...]

SETUP 1: {symbol} | {entry_zone} | SL: {sl} | Target: {target} | RR: {rr}
Evidence: {volume_expansion}× volume, {sector} outperforming, {pattern} pattern
[Fundamental context: sector growth, recent earnings quality]

SETUP 2: ...
...

For each setup (max 4 bullet points each):
1. Bull case
2. Bear case  
3. Key risk to monitor
4. Probability estimate (0.0–1.0)
5. Any novel risk not covered by the technical setup?
```

**If novel setup not in pre-market cache:** Reduce confidence by 0.15. Require confidence ≥ 0.82 (instead of 0.70) to proceed.

---

## Setup Types

### Momentum Breakout
- Price breaks above resistance (daily/weekly) with volume > 1.5×
- Sector in STRONG or IMPROVING phase
- Entry: breakout candle close or next-day open
- Stop: below breakout level

### Trend Pullback
- Strong trend (ADX > 25)
- Pullback to 20-day EMA or key support (Fibonacci 38.2/50%)
- Volume dries up on pullback (< 0.7× avg)
- Entry: at support, stop below support

### Sector Rotation Play
- Sector transitioning from NEUTRAL → IMPROVING → STRONG
- Leading stocks in sector showing first-mover breakout
- Entry: on confirmation of sector leadership

---

## Position Management

**Trail stop after Trend Pulls reach Target 1 (50% size exit):**
- Remaining 50%: trail using 10-day EMA or recent swing low
- Exit remaining: if price closes below 10-day EMA for 2 consecutive days
- Hard time stop: exit at max hold day regardless of P&L

**Forced exits:**
- Earnings announcement within next 5 days: reduce to 50% size or exit entirely
- Sector transitions to WEAK: tighten stop to recent swing low (48 hours)
- Market regime shifts to RANGE or EVENT: tighten all swing stops to 50% of normal ATR

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| Pre-market batch missed (Claude unavailable) | Empty swing cache at 9:10 AM | Proceed with confidence threshold raised to +0.10. Use only highest-conviction setups. Log as SWING_DEGRADED. |
| Earnings date data unavailable | External data error | Do NOT initiate new swing positions until earnings calendar is verified. Log EARNINGS_DATA_MISSING. |
| Sector ranking stale (> 2 hours) | Redis cache TTL | Do not use stale sector ranking as confirming signal. Revert to neutral sector assumption. |
| Position hits time stop | `candles_held >= max_hold_days` | Force exit regardless of P&L. Log TIME_STOP. |

---

## Tool Requirements

- **MongoDB**: `market_data` (daily/weekly OHLCV), `signals` (swing signals)
- **Redis**: `quantara:cache:scenarios:swing:{date}` — batch debate results, TTL=24h
- **Redis**: `quantara:cache:sector:rankings:{date}` — sector strength, TTL=2h
- **PostgreSQL**: `positions` (swing positions), `orders`, `audit_trail`
- **New**: `configs/swing.yaml` — entry thresholds, hold day limits, volume multiplier

---

## Interface Contract

```python
class SwingAlphaAgent:
    async def run_overnight_screen(self) -> List[SwingCandidate]:
        """
        Post-close (after 3:30 PM): screen watchlist for qualifying setups.
        Pure computation — no Claude. Produces candidates for pre-market debate.
        """
    
    async def get_premarket_scenarios(
        self,
        candidates: List[SwingCandidate],
    ) -> Dict[str, SwingScenario]:
        """
        Retrieve or populate pre-market scenario cache.
        Called during pre-market package generation (9:00 AM).
        One Claude Haiku call for up to 5 candidates. Writes to Redis cache.
        """
    
    async def evaluate_entry(
        self,
        symbol: str,
        regime: RegimeContext,
        portfolio: PortfolioState,
    ) -> Optional[SwingSignal]:
        """
        Called intraday when price approaches entry zone.
        Checks all entry requirements. Matches against cached scenarios.
        Never calls Claude directly.
        """
    
    async def on_bar_close(
        self,
        open_positions: List[Position],
        daily_closes: Dict[str, int],  # paise
    ) -> List[Tuple[Position, Optional[str]]]:
        """
        Daily position review. Returns (position, exit_reason or None).
        exit_reason: TIME_STOP | TRAIL_STOP | EARNINGS_PROXIMITY | SECTOR_DETERIORATION
        """
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Entry requirements compliance** | 100% (no entry misses a mandatory gate) | Audit all `swing_signals` for requirement flags |
| **Win rate** | > 55% | `trade_outcomes` for swing book |
| **Average RR on wins** | > 2.5 | `trade_outcomes.actual_return / trade_outcomes.risk` |
| **Pre-market cache hit rate** | > 90% | Entries that matched a cached scenario |
| **Time stop rate** | < 20% | Positions closed by TIME_STOP / total |
| **Earnings proximity violation** | 0% | Positions with earnings within hold period |
