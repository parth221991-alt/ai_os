# QUANTARA SIGNALS
## Master Implementation Document — v1.0
### NIFTY Weekly Options Signal Engine

*Status: Implementation-ready. Every section is automation-ready. No vague language.*

---

## 1. EXECUTIVE SUMMARY

Quantara Signals is a NIFTY weekly options signal engine with two concurrent purposes: personal alpha generation and a subscription-grade signal delivery business. The system is built around **option premium behaviour** as the primary signal source — spot price is a validation layer, not a trigger.

The philosophy is simple: options markets price in information before spot moves. CE/PE premium asymmetry, premium divergence from spot, and premium flow acceleration are the lead indicators. Spot structure, OI context, and regime filters are supporting validators. Nothing triggers a trade without option confirmation.

**Design constraints that shaped everything:**
- ₹20k starting capital. ₹20L scale target. No gambler math.
- 25–40 paper trades/month for fast learning. Not 8–12.
- Subscription-grade = "no signal today" is as valuable as "A+ signal today."
- Telegram-first V1. No dashboards. No React. No UI.
- Fastest path to truth: signal validation first, broker last.

**What this is not:** a trend-following bot, a scalping engine, a sentiment aggregator, or an SMC setup generator. SMC concepts (sweep, MSS, FVG) exist only as confidence modifiers — never triggers.

---

## 2. FINAL ARCHITECTURE

```
DATA LAYER
  └── Zerodha KiteConnect WebSocket (OHLCV + OI, 5-min bars)
  └── Kite REST (OI snapshots, token resolution)
  └── NSE option chain (backup, 5-min pull)

FEATURE ENGINE
  └── Premium Flow Features (PM_CE, PM_PE, P_DIV, PMP, etc.)
  └── RS_spread (CE/PE Relative Strength Engine)
  └── OI Engine (context only)
  └── Spot Validation Engine

SIGNAL ENGINE
  └── Setup Classifiers (OPA / PES / SFR)
  └── Hard Gate Checker
  └── Confidence Engine (composite score → A+/A/SKIP)
  └── No-Trade Engine

RISK ENGINE
  └── Position Sizer
  └── Daily/Weekly Stop Manager
  └── Kill Switch

EXECUTION LAYER (paper first)
  └── Paper Trade Engine
  └── Broker Bridge (Zerodha Kite, wired later)

LEARNING LOOP
  └── Signal Logger (all evaluated signals, not just taken)
  └── Trade Logger (entry, exit, MFE, MAE)
  └── Meta Learning Engine (monthly clustering)

DELIVERY LAYER
  └── Telegram Bot
  └── Signal Formatter
  └── Subscriber Manager

STORAGE
  └── PostgreSQL (primary — all logs, signals, trades)
  └── Redis (intraday state, kill switch, rate limiting)
```

**Technology stack:** Python 3.12, FastAPI, PostgreSQL, Redis, python-telegram-bot, Zerodha KiteConnect SDK, scikit-learn (meta learning), pandas, numpy.

**Deployment:** AWS Lightsail Mumbai (single instance, same server as NiftyBot for now). systemd service. Nginx reverse proxy.

---

## 3. FEATURE ENGINE

### Classification

| Category | Features |
|---|---|
| PRIMARY SIGNALS | PM_CE, PM_PE, P_DIV, RS_spread, PMP |
| SECONDARY CONFIRMATIONS | SPT_ROC, PE_ratio, Premium Acceleration, Momentum Decay |
| CONTEXT ONLY | OI regime, VWAP position, spot structure, session sweep grade |

---

### A. PREMIUM FLOW FEATURES

#### PM_CE — Call Option Premium Momentum

**Formula:**
```
PM_CE(t) = (CE_close(t) - CE_close(t-3)) / CE_close(t-3)
```
3-bar lookback (15 minutes at 5-min bars). Captures momentum, not tick noise.

**Expected predictive power:** High for directional bias detection. CE_premium rising with healthy spread = bullish pressure. Rising CE with PE also rising = IV expansion noise.

**Weakness:** IV spikes post-event distort. Single-leg signal insufficient.

**Confidence level:** 0.7 standalone. Combined with RS_spread: 0.85.

**Why included:** Lead indicator. Options price in expectation before spot moves.

---

#### PM_PE — Put Option Premium Momentum

**Formula:**
```
PM_PE(t) = (PE_close(t) - PE_close(t-3)) / PE_close(t-3)
```
Same lookback as PM_CE for comparability.

**Expected predictive power:** Mirror of PM_CE. Bearish signal when PE rising + CE flat/falling.

**Weakness:** Same as PM_CE. Must always pair with PM_CE for context.

**Confidence level:** 0.7 standalone. Combined: 0.85.

**Why included:** You cannot read premium asymmetry without both legs.

---

#### P_DIV — Premium Divergence

**Formula:**
```
P_DIV = PM_CE - PM_PE
```
Positive = bullish premium bias. Negative = bearish premium bias.

**Expected predictive power:** High. P_DIV cleanly separates direction from IV.

**Weakness:** Does not distinguish IV-driven vs direction-driven moves in isolation. RS_spread corrects for this.

**Confidence level:** 0.75.

**Why included:** Single number summarising asymmetry. Core signal input.

**Threshold:**
- `P_DIV > 0.05` = bullish lean
- `P_DIV < -0.05` = bearish lean
- `-0.05 ≤ P_DIV ≤ 0.05` = neutral/no-trade zone

---

#### PMP — Premium Momentum Persistence

**Formula:**
```
PMP_CE = count of last 5 bars where PM_CE > 0 / 5
PMP_PE = count of last 5 bars where PM_PE > 0 / 5
PMP = PMP_CE - PMP_PE
```
Range: -1.0 to +1.0. Measures sustained directional pressure, not a single spike.

**Expected predictive power:** Medium-high. High PMP = trend conviction. Low PMP = chop.

**Weakness:** Lags on reversals.

**Confidence level:** 0.65.

**Why included:** Filters impulse spikes from sustained flows.

---

#### PE_ratio — Premium Elasticity

**Formula:**
```
PE_ratio = abs(PM_CE) / max(abs(SPT_ROC), 0.0001)
```
Where SPT_ROC is spot rate of change over same 3-bar window.

**Interpretation:**
- `PE_ratio > 2.0`: premium moving faster than spot — options are pricing in more than spot shows. High signal quality.
- `PE_ratio < 0.5`: spot moving faster than premium — spot-led, not option-led. Lower quality.
- `PE_ratio > 5.0`: suspect. Possibly low spot volume or IV event distortion. Apply penalty.

**Expected predictive power:** High for signal quality gating.

**Why included:** Confirms options are leading, not lagging.

---

#### SPT_ROC — Spot Rate of Change

**Formula:**
```
SPT_ROC = (NIFTY_close(t) - NIFTY_close(t-3)) / NIFTY_close(t-3)
```
**Purpose:** Context only. Confirms direction, vetos divergence. If SPT_ROC and P_DIV disagree sharply, reduce confidence.

**Confidence contribution:** ±0.05

---

#### Premium Acceleration

**Formula:**
```
PA_CE = PM_CE(t) - PM_CE(t-1)
PA_PE = PM_PE(t) - PM_PE(t-1)
```
Rate of change of rate of change. Measures momentum building.

**Expected predictive power:** Medium. Accelerating CE premium = conviction building. Useful as secondary confirmation.

**Threshold:** `PA_CE > 0.02` = accelerating. `PA_CE < -0.02` = decelerating.

---

#### Momentum Decay

**Formula:**
```
MD_CE = PM_CE(t-1) - PM_CE(t)
MD_PE = PM_PE(t-1) - PM_PE(t)
```
Positive = momentum fading. Used in No-Trade Engine and exit logic.

---

### B. CE/PE RELATIVE STRENGTH ENGINE

**This is PRIMARY SIGNAL.**

**RS_spread formula:**
```python
def compute_rs_spread(pm_ce_series: pd.Series, pm_pe_series: pd.Series, window: int = 20) -> float:
    z_ce = (pm_ce_series.iloc[-1] - pm_ce_series.rolling(window).mean().iloc[-1]) / \
           (pm_ce_series.rolling(window).std().iloc[-1] + 1e-8)
    z_pe = (pm_pe_series.iloc[-1] - pm_pe_series.rolling(window).mean().iloc[-1]) / \
           (pm_pe_series.rolling(window).std().iloc[-1] + 1e-8)
    return z_ce - z_pe
```

**Purpose:** Distinguish true directional asymmetry from IV expansion.

**Critical distinction:**
```
CE +12%, PE +9% → IV expansion. Not a clean directional signal.
CE +12%, PE -3% → True directional asymmetry. High quality signal.
```

P_DIV alone cannot make this distinction. RS_spread can.

**Classification:** PRIMARY. Log from day 1. This is non-negotiable.

**Thresholds:**
- `RS_spread > 1.0` → bullish directional asymmetry confirmed
- `RS_spread < -1.0` → bearish directional asymmetry confirmed
- `-1.0 ≤ RS_spread ≤ 1.0` → ambiguous, apply confidence penalty of -0.10

**Confidence contribution:**
- `abs(RS_spread) > 1.5` → +0.15
- `1.0 < abs(RS_spread) ≤ 1.5` → +0.08
- `abs(RS_spread) ≤ 1.0` → -0.10

---

### C. OI ENGINE — CONTEXT ONLY

**Hard rule:** OI contributes maximum ±0.03 to confidence. It is context. Not a trigger.

**Lag assumption:** 5-minute lag minimum. Do not use OI for intraday precision.

**Price/OI Matrix:**

| Price | OI | Interpretation | Action |
|---|---|---|---|
| ↑ | ↑ | New longs adding. Bullish conviction | Context: supports bull signal |
| ↓ | ↑ | New shorts adding. Bearish conviction | Context: supports bear signal |
| ↑ | ↓ | Short covering rally. Weaker conviction | Context: confidence penalty -0.02 |
| ↓ | ↓ | Long unwinding. Weaker conviction | Context: confidence penalty -0.02 |

**What survives intraday:**
- Price↑ OI↑ and Price↓ OI↑ are relatively reliable intraday.
- Price↑ OI↓ and Price↓ OI↓ often false signals intraday due to delay in OI reporting.
- Do not make decisions based on OI↓ patterns within first 30 minutes of session.

**OI Regime:**
```python
def get_oi_regime(ce_oi: float, pe_oi: float) -> str:
    ratio = pe_oi / max(ce_oi, 1)
    if ratio > 1.3:
        return "PUT_HEAVY"   # support below
    elif ratio < 0.7:
        return "CALL_HEAVY"  # resistance above
    else:
        return "NEUTRAL"
```

**OI context confidence adjustment:**
```python
OI_ADJUSTMENT = {
    ("bullish_signal", "PUT_HEAVY"): +0.02,   # puts signal support below = good for calls
    ("bullish_signal", "CALL_HEAVY"): -0.02,  # call wall above = resistance
    ("bearish_signal", "CALL_HEAVY"): +0.02,
    ("bearish_signal", "PUT_HEAVY"): -0.02,
    ("any", "NEUTRAL"): 0.00,
}
```

---

### D. SPOT VALIDATION ENGINE

**Core rule:** Spot can VETO or BOOST CONFIDENCE. It cannot trigger a trade alone.

#### Liquidity Sweep Detection

```python
def detect_liquidity_sweep(highs: list, lows: list, close: float, window: int = 20) -> dict:
    prev_high = max(highs[-window:-1])
    prev_low = min(lows[-window:-1])
    swept_high = highs[-1] > prev_high and close < prev_high  # sweep and reject
    swept_low = lows[-1] < prev_low and close > prev_low      # sweep and reject
    return {
        "swept_high": swept_high,
        "swept_low": swept_low,
        "sweep_direction": "bearish" if swept_high else ("bullish" if swept_low else None)
    }
```

#### ORBF — Opening Range Breakout/Failure

```python
ORBF_WINDOW = slice("09:15", "09:45")  # 30-min opening range

def compute_orbf(bars: pd.DataFrame) -> dict:
    or_bars = bars[ORBF_WINDOW]
    or_high = or_bars['high'].max()
    or_low = or_bars['low'].min()
    current = bars.iloc[-1]['close']
    return {
        "or_high": or_high,
        "or_low": or_low,
        "above_orh": current > or_high,
        "below_orl": current < or_low,
        "inside_or": or_low <= current <= or_high,
        "or_width_pct": (or_high - or_low) / or_low * 100
    }
```

#### VWAP Reclaim

```python
def vwap_status(bars: pd.DataFrame) -> str:
    bars['vwap'] = (bars['close'] * bars['volume']).cumsum() / bars['volume'].cumsum()
    current_close = bars.iloc[-1]['close']
    current_vwap = bars.iloc[-1]['vwap']
    prev_close = bars.iloc[-2]['close']
    prev_vwap = bars.iloc[-2]['vwap']
    if prev_close < prev_vwap and current_close > current_vwap:
        return "RECLAIM_BULLISH"
    elif prev_close > prev_vwap and current_close < current_vwap:
        return "RECLAIM_BEARISH"
    elif current_close > current_vwap:
        return "ABOVE_VWAP"
    else:
        return "BELOW_VWAP"
```

**Spot confidence modifiers:**

```python
SPOT_MODIFIERS = {
    "bullish_signal": {
        "ABOVE_VWAP":         +0.05,
        "RECLAIM_BULLISH":    +0.08,
        "BELOW_VWAP":         -0.05,
        "above_orh":          +0.05,
        "inside_or":          -0.03,
        "swept_low":          +0.10,   # SFR setup enhancer
        "swept_high":         -0.05,
    },
    "bearish_signal": {
        "BELOW_VWAP":         +0.05,
        "RECLAIM_BEARISH":    +0.08,
        "ABOVE_VWAP":         -0.05,
        "below_orl":          +0.05,
        "inside_or":          -0.03,
        "swept_high":         +0.10,
        "swept_low":          -0.05,
    }
}
```

**VETO conditions (hard block from spot engine):**
- Both price and premium showing opposite directions simultaneously for 3+ bars
- Invalid structure: current bar closes outside 3-sigma of session VWAP (likely bad data)

---

## 4. SIGNAL ENGINE

### Core pipeline (runs every 5 minutes on new bar close):

```python
def evaluate_signal(state: MarketState) -> SignalResult:
    # 1. Compute all features
    features = compute_feature_vector(state)

    # 2. Hard gate check — fail fast
    gate_result = hard_gate_check(features, state)
    if gate_result.blocked:
        return SignalResult(action="BLOCKED", reason=gate_result.reason)

    # 3. No-trade engine
    no_trade = check_no_trade_conditions(features)
    if no_trade.triggered:
        log_signal(features, action="NO_TRADE", reason=no_trade.reason)
        return SignalResult(action="NO_TRADE", reason=no_trade.reason)

    # 4. Setup classification
    setup = classify_setup(features, state)
    if setup is None:
        log_signal(features, action="NO_SETUP")
        return SignalResult(action="NO_SETUP")

    # 5. Confidence engine
    confidence = compute_confidence(features, setup)

    # 6. Grading
    if confidence.score >= 0.72:
        grade = "A+"
    elif confidence.score >= 0.58:
        grade = "A"
    else:
        log_signal(features, action="SKIP", confidence=confidence)
        return SignalResult(action="SKIP", confidence=confidence)

    # 7. Risk engine
    sizing = compute_position_size(confidence.score, state.account)

    # 8. Build signal
    signal = build_signal(setup, confidence, sizing, features)
    log_signal(features, action="SIGNAL", signal=signal)
    return SignalResult(action="SIGNAL", signal=signal, grade=grade)
```

**Feature vector (logged on every bar, not just signals):**
```python
@dataclass
class FeatureVector:
    timestamp: datetime
    bar_index: int
    pm_ce: float
    pm_pe: float
    p_div: float
    pmp: float
    pe_ratio: float
    spt_roc: float
    pa_ce: float           # premium acceleration CE
    pa_pe: float           # premium acceleration PE
    md_ce: float           # momentum decay CE
    md_pe: float           # momentum decay PE
    rs_spread: float
    oi_regime: str
    ce_oi_change_pct: float
    pe_oi_change_pct: float
    vwap_status: str
    orbf: dict
    sweep: dict
    iv_ce_approx: float
    iv_pe_approx: float
    iv_skew: float         # iv_ce - iv_pe
    spread_pct: float      # option bid-ask spread as % of mid
    session_time_bucket: str  # "09:15-09:45", "09:45-10:20", etc.
    regime: str
    day_of_week: int
    dte: int               # days to expiry
```

---

## 5. FINAL SETUPS

### SETUP 1 — OPA (Opening Premium Asymmetry)

**Concept:** In the first 60–65 minutes of session, institutional order flow creates asymmetric premium pressure. CE or PE premium rises significantly while the other leg is flat or falling. This is non-random directional expectation.

**Time windows:**
```python
OPA_WINDOWS = {
    "primary":  ("09:45", "10:00"),  # full confidence
    "extended": ("10:00", "10:20"),  # confidence penalty: -0.07
}
```

**Hard trigger conditions (ALL must pass):**
```python
def is_opa_trigger(features: FeatureVector) -> bool:
    return all([
        abs(features.p_div) > 0.05,           # meaningful premium asymmetry
        abs(features.rs_spread) > 0.8,        # directional vs IV (lowered from 1.0 for OPA)
        abs(features.pmp) > 0.3,              # sustained, not spike
        features.pe_ratio > 1.2,              # options leading spot
        features.spread_pct < 3.0,            # spread quality gate
    ])
```

**Direction:**
```python
def opa_direction(features: FeatureVector) -> str:
    return "BULLISH" if features.p_div > 0 else "BEARISH"
```

**Strike selection:**
```python
def select_opa_strike(direction: str, spot: float, dte: int) -> int:
    # ATM + 1 OTM for buying
    # ATM for selling (if doing spreads later)
    step = 50  # NIFTY strike step
    atm = round(spot / step) * step
    if direction == "BULLISH":
        return atm + step  # 1 OTM CE
    else:
        return atm - step  # 1 OTM PE
```

**Entry logic:**
- Enter on bar close confirming trigger.
- Use LIMIT order at mid + 0.5% buffer. Max wait: 2 bars (10 min). If not filled, cancel.

**Stop logic:**
```python
def opa_stop(entry_premium: float) -> float:
    return entry_premium * 0.70  # 30% of premium as stop
```

**Exit logic:**
- Target: entry_premium * 1.60 (60% profit)
- Time stop: 11:00 AM hard exit if neither target nor stop hit
- Extended window entry: time stop is 11:15 AM

**Failure modes:**
- OPA triggered at 09:47 but IV expansion causes both legs to rise → RS_spread catches this (low RS_spread = penalty). Log as IV_FALSE.
- OPA triggered with poor spread → spread gate catches this.
- Spot trapped in opening range with P_DIV signal → inside_or penalty reduces confidence below SKIP threshold.

**Confidence modifiers specific to OPA:**
```python
OPA_MODIFIERS = {
    "time_primary":     0.00,
    "time_extended":   -0.07,
    "pe_ratio_high":   +0.05,   # PE_ratio > 2.5
    "pe_ratio_low":    -0.05,   # PE_ratio < 1.2 (still passed but marginal)
    "pmp_strong":      +0.05,   # abs(PMP) > 0.6
    "prev_day_trend_aligned": +0.04,
    "doji_at_trigger": -0.06,   # indecision candle
}
```

---

### SETUP 2 — PES (Premium Expansion Setup)

**Concept:** Sustained premium dominance over multiple bars indicates strong directional intent. One leg consistently dominates without mean-reversion. This is mid-session conviction.

**Active window:** 10:00–13:30

**Adaptive dominance window:**

Rather than hardcoding 20 bars, use adaptive logic:
```python
def compute_pes_dominance(pm_series: pd.Series, direction: str) -> dict:
    """
    Tests dominance at 15, 20, and 25 bar windows.
    Returns the window with highest dominance score.
    """
    results = {}
    for window in [15, 20, 25]:
        recent = pm_series.iloc[-window:]
        if direction == "BULLISH":
            dominant_bars = (recent > 0.01).sum()
        else:
            dominant_bars = (recent < -0.01).sum()
        score = dominant_bars / window
        results[window] = score

    best_window = max(results, key=results.get)
    return {
        "best_window": best_window,
        "dominance_score": results[best_window],
        "all_scores": results
    }
```

**Trigger conditions:**
```python
def is_pes_trigger(features: FeatureVector) -> bool:
    direction = "BULLISH" if features.p_div > 0 else "BEARISH"
    pm_series = get_pm_series(direction)  # PM_CE or PM_PE history
    dominance = compute_pes_dominance(pm_series, direction)

    return all([
        dominance["dominance_score"] > 0.65,  # 65% of bars showing direction
        abs(features.rs_spread) > 1.0,        # asymmetry confirmed
        abs(features.p_div) > 0.04,
        features.spread_pct < 3.5,
        not momentum_decay_severe(features),  # MD not collapsing
    ])
```

**Momentum decay gate:**
```python
def momentum_decay_severe(features: FeatureVector) -> bool:
    # If the dominant leg's momentum is falling for 3 consecutive bars, reject
    return features.md_ce < -0.03 or features.md_pe < -0.03
```

**Strike selection:** ATM strike. PES signals sustained flow, not a breakout, so ATM captures better.

**Stop:** 25% of premium. Wider than OPA because PES allows more time.

**Target:** 50% of premium. More conservative because entry is later in move.

**Time stop:** 14:00 hard exit.

**Confidence modifiers:**
```python
PES_MODIFIERS = {
    "dominance_score_above_80": +0.08,
    "dominance_score_65_80":    +0.04,
    "best_window_15":           -0.03,  # fast window = less reliable
    "best_window_25":           +0.04,  # slow window = more reliable
    "rs_spread_above_1.5":      +0.06,
    "vwap_aligned":             +0.05,
    "prior_failed_attempt":     -0.08,  # PES setup broke and restarted
}
```

---

### SETUP 3 — SFR (Sweep + Flow Reversal)

**Concept:** Liquidity sweep in spot (stop hunt) followed by premium reversal in options. Smart money clears weak hands, then repositions. Highest quality setup.

**Requirement:** Spot event (sweep) AND option confirmation. Both mandatory.

**External vs Session sweep grading:**

```python
def grade_sweep(sweep_type: str, sweep_data: dict) -> dict:
    """
    External sweep = beyond previous day's high/low.
    Session sweep = beyond session high/low only.
    """
    if sweep_type == "external":
        return {"grade": "A", "confidence_bonus": +0.12}
    elif sweep_type == "session":
        return {"grade": "B", "confidence_bonus": +0.06}
    else:
        return {"grade": "C", "confidence_bonus": 0.00}

def classify_sweep_type(sweep_data: dict, prev_day_high: float, prev_day_low: float) -> str:
    if sweep_data["swept_high"] and sweep_data["sweep_price"] > prev_day_high:
        return "external"
    elif sweep_data["swept_low"] and sweep_data["sweep_price"] < prev_day_low:
        return "external"
    elif sweep_data["swept_high"] or sweep_data["swept_low"]:
        return "session"
    return "none"
```

**Trigger conditions:**
```python
def is_sfr_trigger(features: FeatureVector, sweep_data: dict) -> bool:
    sweep_present = sweep_data.get("swept_high") or sweep_data.get("swept_low")
    if not sweep_present:
        return False

    # After sweep, premium must confirm reversal
    reversal_direction = "BULLISH" if sweep_data.get("swept_low") else "BEARISH"

    if reversal_direction == "BULLISH":
        premium_confirms = features.p_div > 0.04 and features.rs_spread > 0.7
    else:
        premium_confirms = features.p_div < -0.04 and features.rs_spread < -0.7

    return all([
        sweep_present,
        premium_confirms,
        features.spread_pct < 3.0,
        features.pe_ratio > 1.0,
    ])
```

**Timing:** Sweep can occur any time 09:15–13:00. Signal valid within 3 bars of sweep (15 min window). After 15 min, sweep is stale.

**Strike:** ATM or 1 OTM in reversal direction.

**Stop:** 35% of premium. Wider because entries are against local momentum.

**Target:** 80% of premium. SFR has highest expectancy when clean.

**Confidence modifiers:**
```python
SFR_MODIFIERS = {
    "external_sweep":       +0.12,
    "session_sweep":        +0.06,
    "rs_spread_confirmed":  +0.08,
    "vwap_in_reversal_dir": +0.06,
    "oi_supports_reversal": +0.03,
    "spread_excellent":     +0.04,  # spread_pct < 1.5
    "late_sweep_13plus":    -0.08,  # sweeps after 13:00 are weak
    "multiple_sweeps":      -0.05,  # choppy, not clean
}
```

---

## 6. HARD GATES vs SOFT PENALTIES

### Hard Gates (BLOCKED — no trade, no log to learning queue)

Only 6. Everything else is a soft penalty.

```python
HARD_GATES = [
    {
        "name": "spread_quality",
        "condition": "spread_pct > 5.0",
        "reason": "Option spread too wide. Execution cost exceeds signal value."
    },
    {
        "name": "kill_switch",
        "condition": "kill_switch_active == True",
        "reason": "Kill switch engaged. All signals blocked."
    },
    {
        "name": "data_integrity",
        "condition": "any(price <= 0 for price in [ce_bid, ce_ask, pe_bid, pe_ask])",
        "reason": "Data integrity failure. Zero or negative prices detected."
    },
    {
        "name": "extreme_iv_distortion",
        "condition": "iv_skew > 30 or iv_ce > 80 or iv_pe > 80",
        "reason": "IV in extreme distortion range. Premium signals unreliable."
    },
    {
        "name": "expired_time_window",
        "condition": "current_time > 14:30 or current_time < 09:20",
        "reason": "Outside valid trading hours."
    },
    {
        "name": "expiry_day_filter",
        "condition": "dte == 0 and current_time > 13:00",
        "reason": "Expiry day afternoon. Gamma risk too high for system."
    }
]
```

**Everything else is a soft penalty.** This means:
- High IV but not extreme → confidence -0.08
- Spot trapped in OR → confidence -0.03
- Both legs rising (IV noise) → confidence -0.10 via RS_spread
- Extended time window → confidence -0.07 (OPA only)
- Poor OI regime → confidence -0.02
- Low PE_ratio → confidence -0.05
- Missing VWAP alignment → confidence -0.05

The system takes more trades. The system learns faster. Edge is discovered in the data.

---

## 7. NO-TRADE ENGINE

**Purpose:** Explicitly identify and log "chop" conditions. "No signal" is a signal. Subscriber trust depends on this.

```python
@dataclass
class NoTradeResult:
    triggered: bool
    reason: str
    regime: str
    confidence_in_no_trade: float

def check_no_trade_conditions(features: FeatureVector) -> NoTradeResult:
    conditions = []

    # VEGA NOISE: both legs rising simultaneously
    if features.pm_ce > 0.03 and features.pm_pe > 0.03:
        conditions.append("VEGA_NOISE: both premiums rising")

    # TRAPPED SPOT: spot inside opening range + weak P_DIV
    if features.orbf["inside_or"] and abs(features.p_div) < 0.04:
        conditions.append("TRAPPED_SPOT: inside OR + weak P_DIV")

    # DECAY CHOP: premiums were strong, now decaying, no clean direction
    if abs(features.md_ce) > 0.03 and abs(features.md_pe) > 0.03:
        conditions.append("BILATERAL_DECAY: both premiums decaying")

    # SPT RISING AGAINST SIGNAL: spot ROC contradicts premium direction
    if features.p_div > 0.05 and features.spt_roc < -0.002:
        conditions.append("SPT_CONFLICT: bullish premium but spot falling")
    elif features.p_div < -0.05 and features.spt_roc > 0.002:
        conditions.append("SPT_CONFLICT: bearish premium but spot rising")

    # RS_SPREAD COLLAPSE: was strong, now neutral for 5+ bars
    if abs(features.rs_spread) < 0.3 and features.pmp_abs < 0.2:
        conditions.append("RS_COLLAPSE: no directional conviction")

    # POST-EVENT IV SPIKE: IV jumped > 15% in 3 bars — noise regime
    if features.iv_ce_approx > 35 or features.iv_pe_approx > 35:
        conditions.append("IV_SPIKE_REGIME: IV too high for clean signals")

    triggered = len(conditions) >= 1
    regime = "CHOP" if triggered else "NORMAL"

    return NoTradeResult(
        triggered=triggered,
        reason=" | ".join(conditions) if conditions else "None",
        regime=regime,
        confidence_in_no_trade=min(len(conditions) * 0.25, 1.0)
    )
```

**Telegram output for no-trade:**
```
🔕 QUANTARA — NO SIGNAL
Session: 10:15 | Regime: CHOP
Reason: VEGA_NOISE + TRAPPED_SPOT
Interpretation: Both legs rising. IV expansion, not directional.
Next evaluation: 10:30
```

This gets sent to subscribers. Transparency builds trust.

---

## 8. CONFIDENCE ENGINE

### Architecture

Move beyond `score += points`. The confidence engine is a weighted composition with human-readable decomposition.

```python
@dataclass
class ConfidenceResult:
    score: float               # 0.0 to 1.0
    grade: str                 # "A+", "A", "SKIP"
    components: dict           # each contributor + value
    explanation: list[str]     # human-readable bullets
    warnings: list[str]        # risk flags

def compute_confidence(features: FeatureVector, setup: Setup) -> ConfidenceResult:
    base = 0.50  # start neutral

    components = {}
    explanation = []
    warnings = []

    # --- PRIMARY SIGNALS ---
    # RS_spread (PRIMARY)
    rs_adj = _rs_adjustment(features.rs_spread)
    components["rs_spread"] = rs_adj
    if rs_adj > 0:
        explanation.append(f"+ strong CE/PE asymmetry (RS={features.rs_spread:.2f})")
    else:
        warnings.append(f"- RS_spread weak ({features.rs_spread:.2f}), possible IV noise")

    # P_DIV
    pdiv_adj = min(abs(features.p_div) * 1.5, 0.12) * (1 if features.p_div > 0 else 1)
    components["p_div"] = pdiv_adj
    explanation.append(f"+ premium asymmetry P_DIV={features.p_div:.3f}")

    # PE_ratio
    if features.pe_ratio > 2.0:
        components["pe_ratio"] = +0.06
        explanation.append(f"+ options leading spot (PE_ratio={features.pe_ratio:.1f})")
    elif features.pe_ratio < 1.0:
        components["pe_ratio"] = -0.05
        warnings.append(f"- spot moving faster than options (PE_ratio={features.pe_ratio:.1f})")
    else:
        components["pe_ratio"] = 0.00

    # --- SECONDARY CONFIRMATIONS ---
    # Spot alignment
    spot_adj = _spot_adjustment(features, setup.direction)
    components["spot"] = spot_adj
    if spot_adj > 0:
        explanation.append(f"+ spot aligned ({features.vwap_status})")
    elif spot_adj < 0:
        warnings.append(f"- spot misaligned ({features.vwap_status})")

    # PMP
    pmp_adj = abs(features.pmp) * 0.10 if abs(features.pmp) > 0.4 else 0
    components["pmp"] = pmp_adj

    # OI context
    oi_adj = _oi_adjustment(features.oi_regime, setup.direction)
    components["oi"] = oi_adj

    # --- SETUP-SPECIFIC MODIFIERS ---
    setup_adj = _setup_modifiers(features, setup)
    components["setup_specific"] = sum(setup_adj.values())

    # --- IV RISK ---
    if features.iv_skew > 10:
        iv_penalty = -0.05
        components["iv_risk"] = iv_penalty
        warnings.append(f"- mild IV skew ({features.iv_skew:.1f})")
    else:
        components["iv_risk"] = 0.00

    # --- SPREAD QUALITY ---
    if features.spread_pct < 1.5:
        components["spread"] = +0.04
        explanation.append("+ excellent spread quality")
    elif features.spread_pct > 3.0:
        components["spread"] = -0.05
        warnings.append(f"- wide spread ({features.spread_pct:.1f}%)")
    else:
        components["spread"] = 0.00

    # Final score
    total_adj = sum(components.values())
    final_score = max(0.0, min(1.0, base + total_adj))

    # Grade
    if final_score >= 0.72:
        grade = "A+"
    elif final_score >= 0.58:
        grade = "A"
    else:
        grade = "SKIP"

    return ConfidenceResult(
        score=final_score,
        grade=grade,
        components=components,
        explanation=explanation,
        warnings=warnings
    )
```

**Paper phase override:** During paper trading phase, emit signals for SKIP grades too (with SKIP label). Do not execute paper trades on SKIP, but log them. This is how we learn what was being filtered out.

**Human-readable Telegram signal:**
```
📊 QUANTARA SIGNAL
━━━━━━━━━━━━━━━━
Setup: OPA (Opening Premium Asymmetry)
Direction: BULLISH
Grade: A+ (78% confidence)
Strike: 24150 CE
Entry: ₹85–92 (LIMIT)
Stop: ₹60 (-30%)
Target: ₹138 (+60%)
Time stop: 11:00 AM
━━━━━━━━━━━━━━━━
WHY:
+ strong CE/PE asymmetry (RS=1.82)
+ premium asymmetry P_DIV=0.087
+ options leading spot (PE_ratio=2.4)
+ spot reclaimed VWAP
+ excellent spread quality
⚠ mild IV skew (11.2)
━━━━━━━━━━━━━━━━
DTE: 3 | OI: PUT_HEAVY | VWAP: RECLAIM_BULLISH
```

---

## 9. RISK ENGINE

### Core parameters

```python
RISK_CONFIG = {
    "risk_per_trade_pct": 0.015,     # 1.5% of capital per trade
    "daily_stop_pct": 0.045,         # 4.5% of capital max loss/day
    "weekly_stop_pct": 0.10,         # 10% of capital max loss/week
    "max_concurrent_trades": 2,      # V1 limit
    "kill_switch_trigger": 0.10,     # 10% drawdown triggers kill switch
    "recovery_wait_days": 1,         # days before kill switch resets
}
```

### Position Sizer

```python
def compute_position_size(
    confidence: float,
    account_capital: float,
    entry_premium: float,
    dte: int,
    config: dict = RISK_CONFIG
) -> dict:
    # Base risk
    base_risk_inr = account_capital * config["risk_per_trade_pct"]

    # Confidence scaling: 0.58–0.72 → 0.7x, 0.72–0.85 → 1.0x, >0.85 → 1.2x
    if confidence >= 0.85:
        conf_multiplier = 1.20
    elif confidence >= 0.72:
        conf_multiplier = 1.00
    else:
        conf_multiplier = 0.70

    # DTE scaling: higher DTE = slightly larger size (more time to be right)
    if dte >= 4:
        dte_multiplier = 1.10
    elif dte == 3:
        dte_multiplier = 1.00
    elif dte == 2:
        dte_multiplier = 0.85
    elif dte == 1:
        dte_multiplier = 0.60
    else:  # DTE 0
        dte_multiplier = 0.30

    adjusted_risk_inr = base_risk_inr * conf_multiplier * dte_multiplier

    # Stop is 30% of premium for OPA, compute lots
    # Stop amount per lot = entry_premium * stop_pct * lot_size
    lot_size = 75  # NIFTY lot size (verify current)
    stop_pct = 0.30  # default stop
    risk_per_lot = entry_premium * stop_pct * lot_size
    lots = max(1, int(adjusted_risk_inr / risk_per_lot))

    # Cap at ₹20k for paper phase
    max_premium_exposure = min(account_capital * 0.15, 20000)
    lots = min(lots, int(max_premium_exposure / (entry_premium * lot_size)))

    return {
        "lots": lots,
        "capital_at_risk_inr": risk_per_lot * lots,
        "max_premium_exposure_inr": entry_premium * lots * lot_size,
        "confidence_multiplier": conf_multiplier,
        "dte_multiplier": dte_multiplier,
    }
```

### Daily Stop Manager

```python
class DailyStopManager:
    def __init__(self, account_capital: float, config: dict):
        self.daily_limit = account_capital * config["daily_stop_pct"]
        self.weekly_limit = account_capital * config["weekly_stop_pct"]
        self.daily_loss = 0.0
        self.weekly_loss = 0.0
        self.kill_switch_active = False

    def record_loss(self, loss_inr: float):
        self.daily_loss += loss_inr
        self.weekly_loss += loss_inr
        if self.daily_loss >= self.daily_limit:
            self.engage_kill_switch("DAILY_STOP_HIT")
        if self.weekly_loss >= self.weekly_limit:
            self.engage_kill_switch("WEEKLY_STOP_HIT")

    def engage_kill_switch(self, reason: str):
        self.kill_switch_active = True
        redis.set("kill_switch", "1", ex=86400)  # 24-hour TTL
        send_telegram_admin(f"🛑 KILL SWITCH: {reason}")

    def reset_daily(self):
        self.daily_loss = 0.0  # called at 15:30 each day

    def reset_weekly(self):
        self.weekly_loss = 0.0  # called Monday 09:00
```

### Streak Protocol

```python
STREAK_PROTOCOL = {
    "3_consecutive_losses": {"action": "reduce_size_50pct", "duration": "day"},
    "5_consecutive_losses": {"action": "paper_mode_only",    "duration": "week"},
    "win_streak_3":         {"action": "increase_size_10pct_cap_120pct"},
}
```

---

## 10. LEARNING LOOP

**Non-negotiable rule:** Every evaluated signal is logged. Every skipped setup is logged. Not just taken trades.

### Signal Log Schema (PostgreSQL)

```sql
CREATE TABLE signal_log (
    id              BIGSERIAL PRIMARY KEY,
    session_date    DATE NOT NULL,
    evaluated_at    TIMESTAMPTZ NOT NULL,
    signal_id       UUID NOT NULL DEFAULT gen_random_uuid(),

    -- Setup identification
    setup_type      VARCHAR(10),    -- OPA, PES, SFR, NO_TRADE, SKIP, BLOCKED
    direction       VARCHAR(10),    -- BULLISH, BEARISH, NULL
    grade           VARCHAR(5),     -- A+, A, SKIP, NULL

    -- Core features (full feature vector as JSONB)
    features        JSONB NOT NULL,

    -- Key signal values (indexed separately for fast querying)
    p_div           NUMERIC(8,4),
    rs_spread       NUMERIC(8,4),
    pe_ratio        NUMERIC(8,4),
    pmp             NUMERIC(8,4),
    oi_regime       VARCHAR(20),
    vwap_status     VARCHAR(30),
    spread_pct      NUMERIC(6,2),
    iv_skew         NUMERIC(6,2),

    -- Confidence
    confidence_score    NUMERIC(4,3),
    confidence_components JSONB,
    confidence_explanation TEXT[],
    warnings            TEXT[],

    -- Sizing (if signal issued)
    lots            INT,
    entry_strike    INT,
    entry_premium   NUMERIC(8,2),
    stop_premium    NUMERIC(8,2),
    target_premium  NUMERIC(8,2),

    -- Outcome (filled after trade closes)
    outcome         VARCHAR(10),    -- WIN, LOSS, TIME_STOP, NOT_TAKEN
    exit_premium    NUMERIC(8,2),
    pnl_inr         NUMERIC(10,2),
    mfe             NUMERIC(8,2),   -- max favourable excursion
    mae             NUMERIC(8,2),   -- max adverse excursion
    time_to_move    INT,            -- bars to first meaningful move
    time_to_failure INT,            -- bars to stop if stopped

    -- Context
    dte             INT,
    session_high    NUMERIC(10,2),
    session_low     NUMERIC(10,2),
    prev_day_high   NUMERIC(10,2),
    prev_day_low    NUMERIC(10,2),
    nifty_spot      NUMERIC(10,2),
    regime          VARCHAR(20),
    day_of_week     INT,
    session_bucket  VARCHAR(20),    -- "09:45-10:20", etc.
    veto_reasons    TEXT[],
    no_trade_reasons TEXT[],

    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_signal_log_date ON signal_log(session_date);
CREATE INDEX idx_signal_log_setup ON signal_log(setup_type, grade);
CREATE INDEX idx_signal_log_outcome ON signal_log(outcome);
CREATE INDEX idx_signal_log_confidence ON signal_log(confidence_score);
```

### MFE/MAE Tracker

After entry, every bar until close:
```python
def update_mfe_mae(signal_id: str, current_premium: float, entry_premium: float):
    pnl_pct = (current_premium - entry_premium) / entry_premium
    redis.execute_command(
        "ZADD", f"mfe_tracker:{signal_id}", pnl_pct, f"{datetime.now().isoformat()}:{current_premium}"
    )
```

---

## 11. META LEARNING ENGINE

**This is the hidden moat. Builds over time. Cannot be reverse-engineered quickly.**

### Monthly Cluster Analysis

```python
def run_monthly_clustering(month: date) -> ClusterReport:
    """Runs last day of each month. Discovers winning feature combinations."""

    # 1. Pull all signals with outcomes from the month
    signals = db.query("""
        SELECT features, confidence_score, outcome, pnl_inr,
               p_div, rs_spread, pe_ratio, pmp, oi_regime,
               setup_type, grade, session_bucket, day_of_week, dte
        FROM signal_log
        WHERE session_date BETWEEN %s AND %s
          AND setup_type IN ('OPA', 'PES', 'SFR')
    """, month_start, month_end)

    df = pd.DataFrame(signals)

    # 2. Feature matrix for clustering
    feature_cols = ['p_div', 'rs_spread', 'pe_ratio', 'pmp',
                    'confidence_score', 'dte', 'day_of_week']
    X = df[feature_cols].fillna(0)

    # Encode categoricals
    X['oi_regime_enc'] = df['oi_regime'].map({"PUT_HEAVY": 1, "NEUTRAL": 0, "CALL_HEAVY": -1})
    X['session_bucket_enc'] = df['session_bucket'].map(SESSION_BUCKET_MAP)

    # 3. Cluster
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # 4. Analyse each cluster
    cluster_stats = df.groupby('cluster').agg(
        count=('outcome', 'count'),
        win_rate=('outcome', lambda x: (x == 'WIN').mean()),
        avg_pnl=('pnl_inr', 'mean'),
        avg_confidence=('confidence_score', 'mean'),
        avg_rs_spread=('rs_spread', 'mean'),
        avg_pe_ratio=('pe_ratio', 'mean'),
    ).reset_index()

    # 5. Tag clusters
    for _, row in cluster_stats.iterrows():
        if row['win_rate'] > 0.65 and row['count'] >= 5:
            tag = "ALPHA_CLUSTER"
        elif row['win_rate'] < 0.40:
            tag = "AVOID_CLUSTER"
        else:
            tag = "NEUTRAL_CLUSTER"
        cluster_stats.loc[cluster_stats['cluster'] == row['cluster'], 'tag'] = tag

    # 6. Save cluster centroids as confidence adjustors for next month
    save_cluster_adjustors(kmeans.cluster_centers_, scaler, cluster_stats)

    return ClusterReport(
        month=month,
        clusters=cluster_stats.to_dict('records'),
        alpha_clusters=[r for r in cluster_stats.to_dict('records') if r['tag'] == 'ALPHA_CLUSTER'],
        avoid_clusters=[r for r in cluster_stats.to_dict('records') if r['tag'] == 'AVOID_CLUSTER']
    )
```

### Confidence Adjustor (next month application)

```python
def apply_cluster_adjustor(features: FeatureVector, adjustors: list) -> float:
    """After month-1 clustering, this nudges confidence for month-2 signals."""
    feature_vec = extract_cluster_features(features)
    distances = [euclidean(feature_vec, adj['centroid']) for adj in adjustors]
    nearest_idx = np.argmin(distances)
    nearest = adjustors[nearest_idx]

    if nearest['distance'] < nearest['threshold'] and nearest['tag'] == 'ALPHA_CLUSTER':
        return +0.05
    elif nearest['tag'] == 'AVOID_CLUSTER':
        return -0.08
    return 0.00
```

### Questions the meta-learning engine answers over time:

- Does OPA + high RS_spread + external sweep outperform OPA alone? By how much?
- Does PES work better on Tuesday (closer to expiry) vs Monday?
- Is there a "golden DTE window" (DTE=3 outperforming DTE=1)?
- What regime + setup combinations have >65% WR?
- When does the system's own confidence score predict outcomes? At what threshold?

---

## 12. SAAS ARCHITECTURE

### V1 Architecture (Telegram-first, no dashboard)

```
Signal Engine (FastAPI service, runs continuously)
    ↓
Telegram Bot (python-telegram-bot)
    ↓
Subscriber Manager (PostgreSQL)
    ↓
Subscribers receive formatted signal messages
```

### Subscriber Manager

```sql
CREATE TABLE subscribers (
    id              BIGSERIAL PRIMARY KEY,
    telegram_id     BIGINT UNIQUE NOT NULL,
    telegram_handle VARCHAR(100),
    plan            VARCHAR(20) DEFAULT 'trial',  -- trial, basic, premium
    status          VARCHAR(20) DEFAULT 'active', -- active, suspended, cancelled
    trial_ends_at   TIMESTAMPTZ,
    subscription_ends_at TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    last_active_at  TIMESTAMPTZ
);

CREATE TABLE subscription_events (
    id              BIGSERIAL PRIMARY KEY,
    subscriber_id   BIGINT REFERENCES subscribers(id),
    event_type      VARCHAR(30),  -- signup, payment, cancel, upgrade
    plan            VARCHAR(20),
    amount_inr      NUMERIC(8,2),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Telegram Bot Commands

```python
COMMANDS = {
    "/start":     "Register as subscriber",
    "/status":    "Your subscription status",
    "/signals":   "Today's signals so far",
    "/stats":     "Week's performance summary",
    "/explain":   "Explain last signal",
    "/pause":     "Pause notifications",
    "/resume":    "Resume notifications",
}
```

### Delivery Rules

```python
DELIVERY_CONFIG = {
    "max_signals_per_day": 4,        # hard cap on subscriber signals
    "no_trade_notification": True,   # subscribers get NO_TRADE messages
    "min_grade_to_deliver": "A",     # A+ and A delivered, SKIP never delivered
    "delivery_delay_ms": 500,        # stagger delivery to avoid rate limits
    "broadcast_batch_size": 50,      # deliver to 50 subscribers at a time
}
```

### Scaling path

- 1–100 subscribers: single Telegram bot, single server
- 100–1000 subscribers: connection pool, Redis pub/sub for delivery queue
- 1000+: separate delivery microservice, Celery workers

---

## 13. DATABASE SCHEMA

```sql
-- Core tables

CREATE TABLE sessions (
    id          BIGSERIAL PRIMARY KEY,
    session_date DATE UNIQUE NOT NULL,
    nifty_open  NUMERIC(10,2),
    nifty_close NUMERIC(10,2),
    or_high     NUMERIC(10,2),
    or_low      NUMERIC(10,2),
    vix_open    NUMERIC(6,2),
    regime      VARCHAR(20),
    expiry_this_week DATE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- signal_log defined in Section 10

CREATE TABLE paper_trades (
    id              BIGSERIAL PRIMARY KEY,
    signal_id       UUID REFERENCES signal_log(signal_id),
    session_date    DATE NOT NULL,
    setup_type      VARCHAR(10),
    direction       VARCHAR(10),
    entry_strike    INT,
    entry_premium   NUMERIC(8,2),
    lots            INT,
    stop_premium    NUMERIC(8,2),
    target_premium  NUMERIC(8,2),
    entry_time      TIMESTAMPTZ,
    exit_time       TIMESTAMPTZ,
    exit_reason     VARCHAR(30),  -- TARGET, STOP, TIME_STOP, MANUAL
    exit_premium    NUMERIC(8,2),
    pnl_points      NUMERIC(8,2),
    pnl_inr         NUMERIC(10,2),
    mfe             NUMERIC(8,2),
    mae             NUMERIC(8,2),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE bar_data (
    id          BIGSERIAL PRIMARY KEY,
    instrument  VARCHAR(30) NOT NULL,  -- NIFTY50, NFO:NIFTY24...CE, etc.
    bar_time    TIMESTAMPTZ NOT NULL,
    open        NUMERIC(10,4),
    high        NUMERIC(10,4),
    low         NUMERIC(10,4),
    close       NUMERIC(10,4),
    volume      BIGINT,
    oi          BIGINT,
    UNIQUE(instrument, bar_time)
);

CREATE TABLE feature_log (
    id          BIGSERIAL PRIMARY KEY,
    bar_time    TIMESTAMPTZ NOT NULL,
    features    JSONB NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE cluster_results (
    id          BIGSERIAL PRIMARY KEY,
    run_date    DATE NOT NULL,
    month       DATE NOT NULL,
    clusters    JSONB NOT NULL,
    adjustors   JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 14. REPLAY ENGINE

**Purpose:** Replay any past session using logged feature vectors and bar data. Validate new confidence logic without waiting for live sessions.

```python
class ReplayEngine:
    def __init__(self, session_date: date, new_signal_engine: SignalEngine):
        self.session_date = session_date
        self.engine = new_signal_engine

    def replay_session(self) -> ReplayReport:
        # Load bar data for this session
        bars = db.query("""
            SELECT * FROM bar_data
            WHERE DATE(bar_time) = %s
            ORDER BY bar_time
        """, self.session_date)

        # Replay bar by bar
        results = []
        for i, bar in enumerate(bars):
            if i < 20:  # need warmup
                continue
            state = build_market_state(bars[:i+1])
            result = self.engine.evaluate_signal(state)
            results.append({
                "bar_time": bar.bar_time,
                "result": result,
                "original_result": get_original_signal(self.session_date, bar.bar_time)
            })

        return ReplayReport(
            session_date=self.session_date,
            results=results,
            comparison=self._compare_with_original(results)
        )

    def _compare_with_original(self, results: list) -> dict:
        """Compares new engine output vs what was logged originally."""
        original_signals = db.query("SELECT * FROM signal_log WHERE session_date = %s", self.session_date)
        # ... comparison logic
```

**Use cases:**
- Testing a confidence threshold change before deploying live
- Backtesting a new feature addition on past 30 days
- Validating that a bug fix didn't alter signal output

---

## 15. PAPER TRADE FRAMEWORK

```python
class PaperTradeEngine:
    def __init__(self):
        self.open_trades = {}  # signal_id → PaperTrade
        self.closed_trades = []

    def open_trade(self, signal: Signal, current_bar: Bar):
        trade = PaperTrade(
            signal_id=signal.signal_id,
            entry_premium=current_bar.ce_close if signal.direction == "BULLISH" else current_bar.pe_close,
            entry_time=current_bar.bar_time,
            lots=signal.sizing.lots,
            stop_premium=signal.stop_premium,
            target_premium=signal.target_premium,
            time_stop=signal.time_stop,
        )
        self.open_trades[signal.signal_id] = trade
        db.insert_paper_trade(trade)

    def update_trades(self, current_bar: Bar):
        for signal_id, trade in list(self.open_trades.items()):
            current_premium = self._get_current_premium(trade, current_bar)

            # Update MFE/MAE
            pnl_pct = (current_premium - trade.entry_premium) / trade.entry_premium
            trade.mfe = max(trade.mfe, pnl_pct)
            trade.mae = min(trade.mae, pnl_pct)

            # Check exits
            if current_premium >= trade.target_premium:
                self._close_trade(signal_id, current_premium, "TARGET", current_bar.bar_time)
            elif current_premium <= trade.stop_premium:
                self._close_trade(signal_id, current_premium, "STOP", current_bar.bar_time)
            elif current_bar.bar_time >= trade.time_stop:
                self._close_trade(signal_id, current_premium, "TIME_STOP", current_bar.bar_time)

    def _close_trade(self, signal_id: str, exit_premium: float, reason: str, exit_time):
        trade = self.open_trades.pop(signal_id)
        pnl_points = exit_premium - trade.entry_premium
        pnl_inr = pnl_points * trade.lots * 75  # NIFTY lot size

        trade.exit_premium = exit_premium
        trade.exit_reason = reason
        trade.exit_time = exit_time
        trade.pnl_inr = pnl_inr

        db.update_paper_trade(trade)
        db.update_signal_outcome(signal_id, "WIN" if pnl_inr > 0 else "LOSS", pnl_inr, trade.mfe, trade.mae)

        send_telegram_admin(
            f"📋 PAPER TRADE CLOSED\n"
            f"Signal: {signal_id[:8]}\n"
            f"Exit: {reason} | P&L: ₹{pnl_inr:+.0f}\n"
            f"MFE: {trade.mfe*100:.1f}% | MAE: {trade.mae*100:.1f}%"
        )
```

### Paper trade performance dashboard (weekly Telegram summary)

```python
def send_weekly_paper_summary():
    stats = db.query("""
        SELECT
            COUNT(*) as total_trades,
            COUNT(CASE WHEN pnl_inr > 0 THEN 1 END) as wins,
            SUM(pnl_inr) as total_pnl,
            AVG(pnl_inr) as avg_pnl,
            MAX(pnl_inr) as best_trade,
            MIN(pnl_inr) as worst_trade
        FROM paper_trades
        WHERE session_date >= NOW() - INTERVAL '7 days'
    """)
    # format and send
```

---

## 16. BUILD ORDER

**Principle: Fastest path to truth. Validate signal quality before anything else.**

### Phase 1 — Signal Truth (Weeks 1–2)

Build in this exact order:
1. KiteConnect WebSocket data pipeline → bar data storage
2. Feature engine (all formulas) → feature_log table
3. Signal classifier (OPA, PES, SFR) → manual review output
4. Confidence engine → score output
5. No-trade engine → no-trade output
6. Basic PostgreSQL schema (signal_log, bar_data, feature_log)
7. Manual paper trading (no automation)

**Deliverable:** You can run the engine on live market data and read signal output in a terminal. You manually track paper trades in a spreadsheet.

---

### Phase 2 — Paper Automation (Weeks 3–4)

1. Paper trade engine (automated open/close tracking)
2. Signal logging (full feature vector, outcome tracking)
3. Hard gate checker + kill switch
4. Telegram admin notifications (your personal alerts only, no subscribers yet)
5. Risk engine (position sizer, daily/weekly stop)
6. Replay engine (replay last 5 sessions to validate)

**Deliverable:** System runs unattended. You receive Telegram alerts. Paper trade P&L is tracked automatically.

---

### Phase 3 — Subscriber V1 (Weeks 5–6)

1. Subscriber manager (PostgreSQL + Telegram bot)
2. Signal delivery (broadcast to subscribers)
3. No-trade notifications to subscribers
4. /start, /status, /signals, /stats commands
5. Trial + basic plan gating

**Deliverable:** 5–10 beta subscribers receiving real-time signals.

---

### Phase 4 — Learning Infrastructure (Month 2)

1. Full feature vector logging on every bar (not just signals)
2. MFE/MAE tracking
3. Weekly performance report generation
4. Monthly clustering (first run after 4 weeks of data)

**Deliverable:** First cluster report. Discover first hidden alpha.

---

### Phase 5 — Live Trading (Month 3+)

1. Broker bridge (Zerodha Kite order execution)
2. Live trade tracking
3. Kill switch → live order cancellation
4. Advanced sizing

**Deliverable:** First live trade.

---

### What gets SKIPPED in V1

- Dashboard / React UI → not needed
- BANKNIFTY → V2
- Multi-leg strategies (spreads, iron condors) → V2 after proven edge
- ML-based signal generation → meta-learning is advisory only in V1
- API for subscribers → Telegram is sufficient

---

## 17. FAILURE MODES

| Mode | Cause | Detection | Recovery |
|---|---|---|---|
| IV_FALSE | Both legs rising (IV event), system sees as directional | RS_spread < 0.5 but P_DIV > 0.05 | Logged as IV_FALSE. RS_spread threshold catches most. |
| DATA_STALE | WebSocket disconnect. Using old premium data | Bar timestamp check. Alert if last bar > 6 min old | Reconnect handler. Halt signals until fresh data. |
| SPREAD_BLOWOUT | Option spread widens suddenly (news, halt) | spread_pct > 5.0 hard gate | Hard blocked. Not traded. |
| SIGNAL_FLOOD | System fires 6+ signals in one session | Daily signal count check | Hard cap at 4 signals/session. |
| OVERFIT_CREEP | Confidence thresholds tuned to historical data | Monthly out-of-sample hold | Reserve last 20% of each month as OOS test before threshold changes. |
| STRIKE_MISMATCH | Selected strike has zero volume | Pre-entry volume check | Reject strike. Select adjacent. |
| KILL_SWITCH_STUCK | Redis TTL mismatch or server restart | Admin `/ks_status` command | Manual reset via admin command. |
| TIME_DRIFT | Server clock not synced to IST | NTP sync check on startup | systemd NTP dependency. Alert if drift > 2 sec. |
| CLUSTERING_NOISE | Too few trades for meaningful clusters | Require minimum 15 closed trades | Skip clustering if count < 15. Wait for next month. |
| EXPIRY_CONFUSION | System uses wrong expiry week | Explicit expiry date validation on startup | Pull expiry calendar from NSE on every restart. |

---

## 18. SELF CRITIQUE

### Weakest assumptions, ranked by severity

**1. Premium elasticity (PE_ratio) assumes spot data is clean.**
If spot data has 1-tick lag while option data is real-time, PE_ratio will be systematically wrong. In practice, KiteConnect spot WebSocket and NFO WebSocket are on the same feed — but verify. Incorrect PE_ratio makes it harder to distinguish option-led vs spot-led moves.

**2. IV approximation will be poor.**
The system approximates IV from premium movement, not from actual Black-Scholes inversion. This means IV_skew and iv_ce_approx are directional indicators, not precise IV values. This is acceptable for V1 filtering but will miss IV events that don't move premium dramatically.

**3. 5-minute bars are the data granularity — this limits what SFR can detect.**
A sweep can happen and recover within 2–3 minutes. At 5-minute bars, it may not be visible. A 1-minute bar feed would catch SFR setups much more cleanly. This is a real limitation. Consider 1-min bars for SFR detection specifically.

**4. RS_spread window (20 bars) is not validated.**
The 20-bar zscore window for RS_spread is chosen reasonably but untested. Too short = too noisy. Too long = too slow to react. This must be the first thing varied in backtesting.

**5. The OI lag problem is worse than stated.**
NSE OI data has been known to update unreliably intraday. "5-minute lag" is optimistic. Some sessions show no meaningful OI update until 30+ minutes have passed. This is why OI is limited to ±0.03 confidence contribution — it's near-noise intraday. Do not increase this contribution without evidence.

**6. The clustering approach will overfit on small sample sizes.**
After month 1, you may have 30–60 closed trades. KMeans with 6 clusters on 30 samples is statistically nonsense. Run clustering only after 60+ trades. Use 3 clusters, not 6, in early months.

**7. Strike selection logic is simplistic.**
ATM + 1 OTM is reasonable, but optimal strike selection should account for skew, DTE, and maximum gamma exposure. This is a V2 problem but acknowledge it now.

**8. The system has not been backtested yet.**
Every threshold in this document is based on logic and market intuition, not statistical validation. Treat all thresholds as hypotheses to test, not established rules. The build order deliberately puts paper trading before any parameter locking.

**9. Subscriber trust depends on signal quality, which is unknown.**
If the system has 40% win rate in the first month, subscribers leave. There is no guarantee of edge. The system is designed to discover edge, not to assert it. Be transparent with beta subscribers: this is a learning phase.

**10. Telegram delivery is a single point of failure.**
If Telegram is down or the bot is rate-limited, subscribers get nothing. For V1 this is acceptable. For V2, add a secondary delivery channel (WhatsApp or email).

### What likely overfits

- Specific confidence thresholds (0.72, 0.58) — these will need recalibration after 60+ trades.
- OPA time windows (09:45–10:00 vs 10:00–10:20) — the -0.07 penalty is arbitrary. Backtest it.
- PES dominance threshold (65%) — may need to be 55% or 75% depending on regime.

### What must be validated first (in order)

1. Does RS_spread actually distinguish directional vs IV moves in NIFTY options? (Day 1 logging)
2. Does PE_ratio > 2.0 correlate with better outcomes? (Week 2 analysis)
3. Is the OPA window (09:45–10:20) better than alternatives? (Month 1 replay analysis)
4. What is the actual no-trade regime frequency? Is the no-trade engine too aggressive? (Week 3)
5. Do external sweeps produce better SFR outcomes than session sweeps? (Month 2)

---

## 19. FINAL IMPLEMENTATION PLAN

### Repository structure

```
quantara/
├── config/
│   ├── settings.py          # all constants, thresholds
│   └── logging_config.py
├── data/
│   ├── kite_stream.py       # WebSocket feed
│   ├── bar_builder.py       # OHLCV bar construction
│   └── data_store.py        # PostgreSQL writes
├── features/
│   ├── premium_features.py  # PM_CE, PM_PE, P_DIV, PMP, PE_ratio, etc.
│   ├── rs_engine.py         # RS_spread computation
│   ├── oi_engine.py         # OI regime + adjustments
│   └── spot_engine.py       # VWAP, ORBF, sweep detection
├── signals/
│   ├── signal_engine.py     # main evaluate_signal() pipeline
│   ├── setups/
│   │   ├── opa.py
│   │   ├── pes.py
│   │   └── sfr.py
│   ├── hard_gates.py
│   ├── no_trade_engine.py
│   └── confidence_engine.py
├── risk/
│   ├── position_sizer.py
│   ├── daily_stop.py
│   └── kill_switch.py
├── paper/
│   ├── paper_engine.py
│   └── performance.py
├── learning/
│   ├── signal_logger.py
│   ├── outcome_tracker.py   # MFE, MAE, outcome writing
│   └── meta_learning.py     # monthly clustering
├── delivery/
│   ├── telegram_bot.py
│   ├── signal_formatter.py
│   └── subscriber_manager.py
├── replay/
│   └── replay_engine.py
├── db/
│   └── schema.sql
├── main.py                  # FastAPI app + scheduler
└── scripts/
    ├── backfill_bars.py
    └── run_clustering.py
```

### Environment variables

```
KITE_API_KEY=
KITE_API_SECRET=
KITE_ACCESS_TOKEN=          # refreshed daily
TELEGRAM_BOT_TOKEN=
TELEGRAM_ADMIN_CHAT_ID=
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
ENVIRONMENT=paper           # paper | live
LOG_LEVEL=INFO
```

### Scheduler (APScheduler)

```python
scheduler.add_job(refresh_access_token,     "cron", hour=8, minute=30)
scheduler.add_job(start_data_stream,         "cron", hour=9, minute=14)
scheduler.add_job(run_signal_evaluation,     "cron", minute="*/5", hour="9-14")
scheduler.add_job(daily_stop_reset,          "cron", hour=15, minute=30)
scheduler.add_job(weekly_stop_reset,         "cron", day_of_week="mon", hour=9)
scheduler.add_job(send_weekly_paper_summary, "cron", day_of_week="fri", hour=16)
scheduler.add_job(run_monthly_clustering,    "cron", day="last", hour=18)
scheduler.add_job(stop_data_stream,          "cron", hour=15, minute=35)
```

---

## APPENDIX: KEY METRICS TO TRACK FROM DAY 1

| Metric | Target | Alert if |
|---|---|---|
| Signals/month | 25–40 | < 15 or > 55 |
| No-trade days | < 30% of sessions | > 50% |
| A+ signal rate | 15–25% of evaluations | < 8% |
| Win rate (paper) | > 50% before going live | < 40% for 3+ weeks |
| Average MFE/MAE ratio | > 2.0 | < 1.5 |
| RS_spread on wins vs losses | Wins should show higher RS | No difference = RS not useful |
| Confidence score calibration | A+ wins should > A wins | A+ underperforms A = recalibrate |
| OPA vs PES vs SFR WR | SFR should be best | SFR worst = sweep detection broken |

---

*Document version 1.0. Review after 60 closed paper trades.*
*All thresholds are hypotheses. Validate, do not worship.*
