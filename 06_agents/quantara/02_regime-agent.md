# Regime Agent Specification

**Agent ID:** `regime`  
**Status:** PARTIALLY IMPLEMENTED — scattered across `market/`, `no_trade/`, `confidence/scoring.py`  
**Priority:** High — regime_fit is the 6th confidence component (0.07 weight) but uses only `VolatilityRegime`. `MarketRegime` enum exists but is not fully populated in the pipeline.  
**Activation:** 09:14 IST (one bar before signal_start), updates every bar close

---

## Mission

Synthesize all market context signals into a single authoritative `RegimeContext` that every downstream agent consumes. Eliminate the current pattern where regime information is scattered across three modules and inconsistently applied.

The existing system has:
- `VolatilityTracker` in `market/volatility_regime.py` — ATR-based, `LOW/NORMAL/HIGH`
- `MarketRegime` enum in `common/enums.py` — `TREND/RANGE/CHOP/EXPANSION`
- `SessionClock` in `market/session_clock.py` — `OPEN/MIDDAY/POWER_HOUR` buckets
- `IVRegime` in `common/enums.py` — `LOW/NORMAL/HIGH/DISTORTED`
- Lunch chop detection in `no_trade/rejection_engine.py`

None of these are unified. The Regime Agent merges them into `RegimeContext` and publishes it once per bar.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| HTF candles (1h, 4h) | `app/ingestion/` | `CandleHTF` | Per bar close |
| LTF feature vector | `app/features/feature_pipeline.py` | `FeatureVector` | Per bar close |
| Current IST timestamp | `app/common/time_utils.py` | `datetime` | Per bar close |
| ATR history (rolling 14-bar) | `VolatilityTracker` | `float[]` | Per bar close |
| IV regime | `FeatureVector.iv_regime` | `IVRegime` | Per bar close |
| DTE / expiry flag | `app/market/expiry_calendar.py` | `int`, `bool` | Per bar close |
| Option chain PCR | Kite REST (cached 15 min) | `float` | Intraday |
| VIX (from Kite or NSE) | External feed | `float` | Per bar close |

---

## Outputs

### `RegimeContext` (new contract, to be added to `app/market/schemas.py`)
```python
@dataclass(frozen=True)
class RegimeContext:
    schema_version: str
    trace_id: UUID
    timestamp: datetime
    
    # Volatility
    vol_regime: VolatilityRegime       # LOW | NORMAL | HIGH
    iv_regime: IVRegime                # LOW | NORMAL | HIGH | DISTORTED
    vix: Optional[float]
    atr_14: float
    atr_percentile: float              # 0-100
    
    # Market structure
    market_regime: MarketRegime        # TREND | RANGE | CHOP | EXPANSION
    trend_strength: float              # 0.0 to 1.0
    trend_direction: Optional[str]     # BULLISH | BEARISH | NEUTRAL
    
    # Session
    session_bucket: str                # OPEN | MIDDAY | POWER_HOUR
    is_lunch_chop: bool                # 11:45-13:15 IST
    is_signal_allowed: bool            # After 09:45, before 15:00
    is_power_hour: bool                # After 14:00
    
    # Options context
    pcr: Optional[float]               # Put-Call Ratio
    pcr_regime: Optional[str]          # BULLISH (<0.7) | NEUTRAL | BEARISH (>1.2)
    
    # Expiry
    dte: int
    is_expiry_day: bool
    is_one_before_expiry: bool
    
    # Composite
    regime_fit: str                    # GOOD | NEUTRAL | BAD (for confidence component)
    regime_score: float                # Maps to: GOOD=0.07, NEUTRAL=0.0, BAD=-0.05
    trade_suppressed: bool             # True = lunch chop / CHOP regime / MACRO
    suppression_reason: Optional[str]
```

### `RegimeAgentDecision` (extends `AgentDecision`)
```python
verdict logic:
    BLOCK → trade_suppressed == True (lunch chop, CHOP regime, IV distorted)
    WARN  → vol_regime == HIGH or is_expiry_day
    PROCEED → all clear
```

---

## Confidence Scoring

The Regime Agent directly produces `regime_score` which feeds the 6th component of Quantara's confidence scoring (weight: 0.07).

Regime score mapping (from `configs/confidence.yaml`):
```
regime_fit == GOOD    → +0.07 (TREND regime, normal IV, no suppression)
regime_fit == NEUTRAL → 0.00  (RANGE or EXPANSION regime)
regime_fit == BAD     → -0.05 (CHOP regime, HIGH IV, lunch chop window)
```

Additional penalties the Regime Agent can trigger (applied in confidence scoring):
- `high_iv: -0.05` — when `iv_regime == DISTORTED`
- `lunch_chop: -0.08` — when `is_lunch_chop == True`

The Regime Agent computes `regime_score` deterministically. No probabilistic model.

---

## Market Regime Classification Logic

```python
def classify_market_regime(htf_candles_1h: List[CandleHTF]) -> MarketRegime:
    """
    Based on last 20 bars of 1h candles:
    
    EXPANSION: ATR percentile > 80 AND directional bars > 70%
    TREND:     ATR percentile 40-80 AND directional bars > 60% AND
               close > EMA20 (bull) or close < EMA20 (bear)
    RANGE:     ATR percentile 20-60 AND directional bars 40-60%
    CHOP:      ATR percentile < 30 AND directional bars < 40%
    """

def classify_pcr_regime(pcr: float) -> str:
    if pcr < 0.70:   return "BULLISH"   # Calls dominate
    if pcr > 1.20:   return "BEARISH"   # Puts dominate
    return "NEUTRAL"

def calc_regime_fit(market_regime, iv_regime, is_lunch_chop, session_bucket) -> tuple[str, float]:
    if is_lunch_chop:
        return "BAD", -0.05
    if market_regime == CHOP:
        return "BAD", -0.05
    if iv_regime == DISTORTED:
        return "BAD", -0.05
    if market_regime == TREND and iv_regime in (LOW, NORMAL) and session_bucket != MIDDAY:
        return "GOOD", 0.07
    return "NEUTRAL", 0.0
```

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| VIX feed unavailable | `None` returned from Kite | Set `vix=None`, `iv_regime` derived from option chain spread only |
| PCR feed unavailable | Kite option chain timeout | Set `pcr=None`, `pcr_regime=None`, use last known PCR from Redis |
| Insufficient HTF candles (< 20 bars) | Length check | Default to `NEUTRAL` regime, emit WARN in `trade_suppressed=False` |
| ATR = 0 (first bar) | Division guard | Return `atr_percentile=50.0` (neutral) |
| IV regime DISTORTED at market open | Valid condition | Emit BLOCK, log `VEGA_DISTORTION` as suppression reason |
| All feeds healthy but regime changes mid-session | Valid condition | Re-evaluate every bar; regime can flip from GOOD to BAD intraday |

---

## Tool Requirements

- `app/market/volatility_regime.py` — already exists, `VolatilityTracker.update()`
- `app/market/session_clock.py` — already exists, `SessionClock.session_bucket()`
- `app/market/expiry_calendar.py` — already exists, DTE and expiry detection
- `app/features/schemas.py` — `FeatureVector.iv_regime`, `FeatureVector.vol_regime`
- `app/ingestion/` — `CandleHTF` for 1h/4h candles
- **Redis** — key `quantara:regime:{session_id}`, TTL = 5 minutes (bar lifetime), updated every bar
- **New**: `app/market/schemas.py` — add `RegimeContext` dataclass
- **New**: `app/market/pcr_tracker.py` — PCR fetch and cache (optional enhancement)

---

## Interface Contract

```python
class RegimeAgent:
    async def initialize(self, session_id: str) -> None:
        """Load initial HTF candles at session start."""
    
    async def on_bar_close(
        self,
        features: FeatureVector,
        htf_candles: Dict[str, List[CandleHTF]],
        ts: datetime,
        dte: int,
        is_expiry_day: bool,
    ) -> RegimeContext:
        """
        Called on every bar close (every 5 minutes during trading).
        Publishes RegimeContext to Redis and to agent bus.
        Returns RegimeContext for synchronous callers.
        """
    
    async def get_current(self) -> Optional[RegimeContext]:
        """Return last published RegimeContext from Redis. None if not initialized."""
    
    def evaluate(self, ctx: RegimeContext) -> RegimeAgentDecision:
        """Convert RegimeContext to AgentDecision for agent bus."""
```

**Redis contract:**
- Write: `quantara:regime:{session_id}` → serialized `RegimeContext` JSON
- TTL: 360s (one bar, refreshed every bar close)
- Read: Signal Agent reads this before scoring; Monitoring Agent reads for dashboard

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Regime accuracy** | > 75% correct on backtested regimes | Compare classified regime vs manual market type labels on historical data |
| **CHOP detection precision** | > 80% (blocks in CHOP are justified) | Count BLOCK-in-CHOP days where premium movement was < 0.5R |
| **Suppression false positive rate** | < 10% | Count suppressed sessions where a valid setup would have won |
| **Latency** | < 50ms per `on_bar_close()` | ATR + EMA computation is O(N); profile on 20-bar window |
| **Regime transition accuracy** | Stable transitions (not flickering) | Count same-bar regime flip-flops (target: < 2% of bars) |

---

## Relationship to Existing Code

The Regime Agent is a refactoring and extension, not a rewrite. The implementation path:
1. Create `RegimeContext` dataclass in `app/market/schemas.py`.
2. Create `RegimeAgent` class that wraps `VolatilityTracker` + `SessionClock` + new regime classifier.
3. Add `classify_market_regime()` function to `app/market/volatility_regime.py`.
4. Wire `RegimeAgent.on_bar_close()` into `DailyRunner._run_session()` before `TierEngine`.
5. Replace scattered regime lookups in `confidence/scoring.py` with `RegimeContext.regime_score`.
6. Replace scattered lunch chop checks with `RegimeContext.is_lunch_chop`.
