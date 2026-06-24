# Market Microstructure Agent Specification (Tier 1)

**Agent ID:** `microstructure`  
**Status:** NOT IMPLEMENTED  
**Priority:** High — options intelligence is a core component of the intraday signal weight (0.20 in Trending regime, 0.45 on Expiry)  
**Activation:** 09:15 IST, updates every 5 minutes during market hours  
**Tier:** 1 — Alpha Generation Engine  
**Claude dependency:** None — entirely quantitative. No AI.

---

## Mission

Compute dealer gamma exposure, liquidity pool locations, max pain, and OI-based structural signals from the live options chain. Publish this as structured context consumed by the Intraday SMC+F&O Agent.

This agent operates purely through quantitative analysis. It is one of the few Tier 1 agents with no Claude dependency — its outputs are computed deterministically from options chain data every 5 minutes.

The Intraday SMC+F&O Agent cannot operate without this agent's output. If this agent is stale by more than one candle, the F&O component of signal confidence is set to zero.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| Options chain (live) | Zerodha KiteConnect API | `OptionChain` | Every 5 minutes |
| Spot price | Zerodha WebSocket | `MarketTick` | Every tick |
| Previous session OI | MongoDB `options_data` | `OISnapshot` | At session start |
| VIX | NSE / Zerodha | `float` | Every 5 minutes |
| ATR (NIFTY 50) | Feature pipeline | `float` | Per bar close |
| Data validity flags | Market Data Validity Engine | `ValidityState` | Continuous |

**Data validity gate:** If options chain fails validation (partial chain, stale > 60s, Greeks sign error): set all microstructure outputs to `INVALID`. Intraday agent receives zero weight for options intelligence.

---

## Outputs

### `MicrostructureSnapshot`
```python
@dataclass(frozen=True)
class MicrostructureSnapshot:
    timestamp: datetime
    underlying: str           # "NIFTY"
    expiry: date
    
    # Dealer gamma exposure
    net_dealer_gamma: float   # Positive = long gamma (stabilizing), Negative = short gamma (amplifying)
    gamma_flip_level: int     # Price level in paise where dealer gamma switches sign
    gamma_wall_above: int     # paise — nearest strong resistance from gamma
    gamma_wall_below: int     # paise — nearest strong support from gamma
    
    # Liquidity pools
    buy_pools: List[int]      # paise — strikes with significant buy-side OI concentration
    sell_pools: List[int]     # paise — strikes with significant sell-side OI concentration
    
    # Max pain
    max_pain_level: int       # paise
    max_pain_proximity_pct: float  # How close spot is to max pain as % of spot
    
    # OI dynamics
    oi_buildup_direction: str     # "bullish" | "bearish" | "neutral" | "mixed"
    ce_oi_change: int             # CE OI change from previous session
    pe_oi_change: int             # PE OI change from previous session
    oi_price_divergence: bool     # Price rising but OI declining (warning)
    oi_buildup_anomaly: bool      # OI change > 2σ from session baseline
    
    # Structural context
    iv_percentile: float          # 0–100
    put_call_ratio: float         # PCR by OI
    atm_iv: float
    iv_skew: float                # Call IV vs Put IV differential
    
    # Data quality
    chain_completeness_pct: float  # % of expected strikes received
    data_age_seconds: float
    is_valid: bool                 # False if chain failed validation
```

---

## Computation Methods

### Dealer Gamma Exposure
```python
def compute_dealer_gamma(chain: OptionChain, spot: int) -> float:
    """
    Dealer net gamma = sum over all strikes of:
    - Call: dealer sold calls to retail → dealer is SHORT gamma
    - Put: dealer bought puts from retail → dealer is LONG gamma
    
    Net dealer gamma per strike = (OI_CE × GEX_CE) - (OI_PE × GEX_PE)
    
    Positive net: long gamma → dealer buying dips, selling rallies → stabilizing
    Negative net: short gamma → dealer buys rallies, sells dips → amplifying
    """

def find_gamma_flip(dealer_gamma_by_strike: Dict[int, float]) -> int:
    """
    Strike where cumulative dealer gamma switches from positive to negative.
    Price below flip = short gamma zone (volatile, amplified moves)
    Price above flip = long gamma zone (range compression, mean reversion)
    """
```

### Liquidity Pool Detection
```python
def find_oi_pools(chain: OptionChain, sigma_threshold: float = 2.0) -> Tuple[List[int], List[int]]:
    """
    Buy pools: strikes where PE OI concentration significantly exceeds baseline
    Sell pools: strikes where CE OI concentration significantly exceeds baseline
    Uses z-score of OI per strike vs session rolling mean.
    Returns (buy_pools, sell_pools) sorted by significance.
    """
```

### Max Pain
```python
def compute_max_pain(chain: OptionChain) -> int:
    """
    Strike where combined dollar value of in-the-money options is minimized.
    Computed as: for each strike price S, sum(max(0, S - strike) × OI for all calls) + sum(max(0, strike - S) × OI for all puts)
    Returns strike with minimum total value (paise).
    """
```

### OI Divergence
```python
def detect_oi_divergence(
    current_price: int,
    prev_price: int,
    current_oi: int,
    prev_oi: int,
) -> bool:
    """
    Bearish divergence: price UP but OI DOWN (positions closing, no conviction)
    Bullish divergence: price DOWN but OI UP (shorts building, potential squeeze)
    """
```

---

## Signal Output for Intraday Agent

The microstructure snapshot is consumed by the Intraday SMC+F&O Agent as part of its options intelligence component. Key signals:

| Microstructure Signal | Intraday Implication |
|---|---|
| `net_dealer_gamma < 0` (short gamma zone) | Larger moves expected. Widen stop estimates. Momentum trades more favored. |
| `spot near gamma_wall` | Expect resistance/support. Conservative targets. |
| `oi_buildup_direction == "bullish"` | Confirms long CE positions. Adds to call buyer confidence. |
| `oi_price_divergence == True` | Caution — current trend may lack conviction. Reduce confidence. |
| `max_pain_proximity_pct < 2%` | Near max pain on expiry day → mean reversion risk. |
| `iv_percentile < 15` | Cheap options, but signals may be unreliable. Hard block in intraday agent. |
| `atm_spread_pct > 2%` | Liquidity insufficient. Hard block in intraday agent. |

---

## Expiry Day Specifics

On expiry day (`dte == 0`), microstructure weights change dramatically:

- Options Intelligence weight rises to **0.45** (vs 0.20 in trending regime)
- Gamma dynamics are most extreme
- Max pain calculation is highest-impact
- IV crush post-expiry affects exit pricing

The microstructure agent emits an explicit `expiry_mode: true` flag. The Intraday agent uses the expiry playbook when this flag is set.

---

## Partial Chain Protocol

If chain completeness < 80% of expected strikes:
1. Set `is_valid = False` on all microstructure outputs
2. Do NOT compute max pain or dealer positioning on partial data
3. Emit `PARTIAL_CHAIN` alert (Level 1 WARNING)
4. Intraday agent receives: options intelligence component = 0 weight until chain recovers

---

## Cache Architecture

Microstructure snapshots are high-frequency. Redis is the primary store.

```
quantara:cache:microstructure:{underlying}   TTL: 6 minutes
```

If Redis read fails: use previous snapshot if age < 7 minutes. If > 7 minutes: set `is_valid = False`.

Full snapshots written to MongoDB `microstructure_analysis` for post-session analysis (one document per 5-minute interval per underlying).

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| Options chain older than 60s | `data_age_seconds > 60` | Set `is_valid = False`. Alert Level 1. Intraday agent zeroes options component. |
| Partial chain (< 80% strikes) | `chain_completeness_pct < 0.80` | Set `is_valid = False`. No max pain or GEX computation. |
| IV calculation error (zero division, negative IV) | `iv <= 0 or iv > 500%` | Reject that strike. If > 30% of strikes affected: full `is_valid = False`. |
| OI counter goes negative (data error) | `oi_change > previous_oi` | Reject OI change for that strike. Alert `OI_DATA_ANOMALY`. |
| Network error on chain fetch | Zerodha API timeout | Use previous snapshot if < 6 minutes old. Alert on 3 consecutive failures. |

---

## Tool Requirements

- `app/market/microstructure.py` — NEW: GEX computation, max pain, OI analysis
- `app/market/options_chain.py` — NEW: chain fetcher + validation
- `configs/microstructure.yaml` — NEW: OI anomaly sigma thresholds, gamma zone params
- **Redis**: `quantara:cache:microstructure:{underlying}`, TTL=6min
- **MongoDB**: `options_data` (chain snapshots), `microstructure_analysis` (computed output)
- **PostgreSQL**: none — microstructure is analytical, not financial state

---

## Interface Contract

```python
class MarketMicrostructureAgent:
    async def update(self, spot: int) -> MicrostructureSnapshot:
        """
        Fetch options chain. Validate. Compute all microstructure metrics.
        Write to Redis and MongoDB. Returns snapshot.
        Called every 5 minutes.
        """
    
    async def get_current(self) -> MicrostructureSnapshot:
        """
        Read from Redis cache. If stale: trigger update.
        Called by Intraday SMC+F&O Agent before every signal evaluation.
        """
    
    def get_signal_weight(self, regime: RegimeContext) -> float:
        """
        Returns the options intelligence signal weight for current regime.
        Trending=0.20, Range=0.15, Expiry=0.45, Event=0.35.
        Returns 0.0 if snapshot is_valid=False.
        """
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Data freshness** | Age < 6 min, 99%+ of bars during market hours | `data_age_seconds` distribution |
| **Chain completeness** | > 95% of bars with completeness > 80% | `chain_completeness_pct` histogram |
| **GEX flip predictive power** | Price reversal rate > 55% within 30 min of entering short gamma zone | Back-test `net_dealer_gamma < 0` vs subsequent NIFTY moves |
| **Max pain attraction** | On expiry: NIFTY closes within 1% of max pain > 60% of expiry sessions | Historical expiry closes vs max pain |
| **OI buildup accuracy** | OI direction matches next-session price move > 55% | `oi_buildup_direction` vs next-day close |
