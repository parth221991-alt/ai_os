# QUANTARA OS — MASTER ARCHITECTURE DOCUMENT
## Version 3.1 — Frozen for Implementation

**Status:** Architecture frozen. All decisions below are final.
**System:** Personal Hedge Fund Operating System — Indian Markets (Zerodha / NSE / BSE)
**Capital Target:** ₹5 Crore autonomous operation
**Stack:** Python 3.12 / FastAPI / PostgreSQL 15 / MongoDB 6 / Redis 7 / AWS Lightsail Mumbai

---

# PART 1 — PRODUCT IDENTITY

## What Quantara OS Is

A fully autonomous Personal Hedge Fund Operating System that manages:

- **Investment Book** — 3 months to multi-year. Quality Indian equities. Institutional CIO style.
- **Swing Book** — 2 to 30 days. Momentum, breakouts, sector rotation.
- **Intraday / F&O Desk** — Minutes to intraday. Index options, stock options, futures. SMC + F&O Intelligence.

Human role is limited to:
1. Defining capital
2. Setting risk mandates
3. Governance controls
4. Emergency intervention

Everything else is autonomous.

## Core Operating Philosophy

Every decision must be **probabilistic**, not binary.

Wrong: `BUY / SELL`
Correct: `Probability + Confidence + Expected Value + Risk`

Every output must contain: Direction, Confidence, Risk, Expected reward, Time horizon, Reasoning.

```json
{
  "direction": "long",
  "confidence": 0.78,
  "expected_reward": 2.4,
  "risk_level": "medium",
  "time_horizon": "intraday",
  "reasoning": ["bullish BOS", "banking sector strength", "positive OI buildup"]
}
```

## Capital Architecture

| Book | Allocation | Timeframe | Style |
|------|-----------|-----------|-------|
| Investment | 40–60% | 3 months → multi-year | Institutional CIO |
| Swing | 15–30% | 2–30 days | Momentum / breakout |
| Intraday / F&O | 10–30% | Minutes → intraday | SMC + F&O Intelligence |
| Cash Reserve | 10% min | Always | Never tradeable |

---

# PART 2 — SYSTEM ARCHITECTURE

## System Topology

```
Frontend (React SPA)
        ↓
Nginx (SSL reverse proxy)
        ↓
FastAPI Backend (port 8000)
        ↓
┌────────────────────────────────────────────┐
│  Tier 0: Survivability Foundation          │
│  Tier 1: Alpha Generation Engine           │
│  Tier 2: CIO Allocation System             │
│  Tier 3: AI Intelligence Layer             │
│  Tier 4: Learning and Adaptation           │
└────────────────────────────────────────────┘
        ↓
Emergency Flatten Service (port 8001 — SEPARATE PROCESS)
        ↓
Zerodha KiteConnect (broker)
```

## Service Boundaries

| Service | Process | Port | Dependencies |
|---------|---------|------|-------------|
| Quantara Backend | systemd | 8000 (internal) | PostgreSQL, MongoDB, Redis |
| Emergency Flatten | systemd (separate) | 8001 (internal) | PostgreSQL only, Zerodha direct |
| PostgreSQL | system | 5432 | — |
| MongoDB | system | 27017 | — |
| Redis | system | 6379 | — |
| Nginx | system | 80/443 | Backend |

**Critical rule:** Emergency Flatten Service has ZERO imports from the main backend. It operates independently. If the main backend is what crashed, flatten must still work.

## Database Split — Definitive Rule

**PostgreSQL owns all state that affects money:**

```
capital_accounts          — settlement-aware capital per book
positions                 — source of truth for all open positions
orders                    — full order lifecycle with idempotency keys
order_state_transitions   — immutable append-only state history
risk_state                — daily risk metrics, P&L, drawdown
strategy_states           — state machine per strategy
strategy_parameters       — layer 1/2/3 config (learning cannot write here)
learning_recommendations  — learning writes ONLY here
reconciliation_log        — every reconciliation run
system_checkpoints        — warm-start support (written every 5 min)
audit_trail               — immutable append-only, BEFORE every action
alert_log                 — all alerts with acknowledgment tracking
kill_switch_log           — all kill switch activations and resets
```

**MongoDB owns all intelligence and analytical data:**

```
market_data               — OHLC, tick, volume history
options_data              — option chains, IV, OI, Greeks snapshots
microstructure_analysis   — computed dealer positioning
signals                   — every generated signal with explainability
intelligence_feed         — news, macro, sentiment outputs
premarket_packages        — daily pre-market intelligence
learning_metrics          — performance analytics, signal quality
ai_cache                  — Claude output cache with TTL
system_logs               — operational logs (not financial audit)
```

**Rule:** If a service needs current position data, available capital, or risk state → it reads PostgreSQL. Period. Redis-cached versions are for display only, never for execution decisions.

## Monetary Values

All monetary values stored as **INTEGER in paise** (1 INR = 100 paise).
₹1,234.56 = stored as `123456`.
Floating point arithmetic on monetary values is banned.
Display layer converts to rupees. All arithmetic uses integer paise.

---

# PART 3 — TIER ARCHITECTURE

## TIER 0 — Survivability Foundation

*Nothing in any other tier runs until Tier 0 is healthy.*

### 0.1 Zerodha Session Manager

**State machine:** `UNINITIALIZED → AUTHENTICATING → ACTIVE → DEGRADED → FAILED → HALTED`

Every state transition logged to PostgreSQL audit_trail.

**Heartbeat:** Every 10 seconds. No tick for 30 seconds → DEGRADED.

**Reconnection backoff:** 1s, 2s, 4s, 8s, 16s, 30s. After 3 failures → HALTED state + EMERGENCY alert.

**Five failure modes — all handled explicitly:**

| Mode | Scenario | Handler |
|------|---------|---------|
| A | Order acknowledged, exchange cancels | Never retry automatically. Mark EXCHANGE_REJECTED. Alert. |
| B | Wrong instrument on WebSocket | Validate received_token == subscribed_token every tick. Counter → alert at 3 mismatches. |
| C | Stale position API | Dual-fetch 5 seconds apart. If different: take recent, flag POSSIBLY_STALE. |
| D | Silent SL modification failure | Verify after every modification. If mismatch: cancel and replace. |
| E | Rate limit cascade | Redis sliding window. Queue max 8 orders/second. Queue depth > 5: alert. Above 10: reject new, never queue indefinitely. |

**Additional operational rules:**
- Market open (9:15–9:30): read-only, no orders
- Market close (15:25–15:30): no new positions, manage exits only
- Post-15:25: force-close all intraday positions. Zerodha auto-squares at 15:30 at worst price — prevent this.
- Token refresh: attempt at 8:00 AM. Alert if fails. Manual intervention required by 8:45 AM or abort trading day.

### 0.2 Position Reconciliation Engine

**Cold start (pre-market, 9:00 AM):**
1. Fetch positions from Zerodha twice with 5-second gap
2. Compare with PostgreSQL positions
3. If CLEAN: log, continue
4. If DISCREPANCY: CRITICAL alert, await human sign-off before any trading

**Warm start (unplanned restart during market hours):**
1. Check if today's checkpoint exists in PostgreSQL
2. If yes: load checkpoint, run immediate reconciliation vs Zerodha
3. If match: resume trading
4. If mismatch: HALT, require human sign-off
5. If no checkpoint: treat as cold start

**Continuous:** Every 15 minutes during market hours. Any deviation → immediate full reconciliation.

**Post-execution:** After every fill confirmation. Verify internal state matches Zerodha.

**Position aging enforcement:**
- Every position has: strategy_type, expected_exit_time, max_hold_until
- Intraday position alive after 15:20: escalate to force-exit regardless of P&L
- Swing positions past hold period: flag for human review (do not auto-exit)

### 0.3 Order Idempotency Engine

**Key format:** `{strategy_id}_{instrument}_{direction}_{timestamp_microseconds}_{random_4char}`

Example: `intraday_smc_NIFTY_long_20240315_093247_847291_a3f7`

Microsecond timestamp + random suffix eliminates same-second collisions.

**Before any order submission:**
1. Generate key
2. Check PostgreSQL orders table for this key
3. If FILLED: do not resubmit, return existing fill
4. If PENDING: check Zerodha status, do not resubmit
5. If FAILED: only resubmit if retry policy allows, increment attempt_number
6. If not found: proceed, create record immediately (before API call)

**Near-duplicate suppression (Redis, TTL 60 seconds):**
Same instrument + direction + strategy within 30 seconds → suppress second signal.

### 0.4 Market Data Validity Engine

All data passes through this engine. No component receives unvalidated data.

**OHLC:** High ≥ Low always. High ≥ Open, Close. Low ≤ Open, Close. Volume > 0 during market hours.

**Tick data:** Not zero. Not older than 5 seconds during market hours. No duplicates. Price continuity (reject >5% move from last tick).

**Options chain:** IV positive. IV < 500%. Put-call parity sanity check. OI change cannot exceed previous OI. Greeks sign consistency (call delta positive, put delta negative). Bid-ask spread < 5% of mid. Chain age < 60 seconds during market hours.

**Additional detection (stress-tested):**

*Systematic bias:* Corporate action calendar checked before processing. If split/bonus detected but adjustment unclear: suspend instrument, alert.

*Timezone integrity:* All timestamps validated as IST explicitly. Drift > 60 seconds from system clock: flag source as degraded.

*Partial options chain:* If received strikes < 80% of expected → PARTIAL flag. Do NOT compute max pain or dealer positioning on partial data. Reduce F&O signal weight by 50%.

*Circuit breaker awareness:* Monitor NSE L1/L2/L3 circuit breaker status. If active: HALT all trading. Post-circuit-breaker: 10-minute mandatory observation before new entries.

*Breadth completeness:* Stocks at circuit disappear from feeds. If advance-decline count < 80% of normal universe: flag INCOMPLETE, do not use breadth as confirming signal.

**On validation failure:**
- Log failure with full data payload to MongoDB
- Increment failure counter per data type
- If failure rate > threshold in 5-minute window: disable trading for affected instrument class + alert

### 0.5 Tier 0 Risk Engine (Hard Limits)

Supreme authority. Nothing bypasses this. Operates independently of all strategy logic.

**Hard limit checks (in order):**

1. Kill switch level (0 = none, 1/2/3 = active)
2. Black swan protocol active flag
3. Daily loss limit (absolute paise figure from config)
4. Drawdown halt threshold
5. Capital preservation mode active
6. Margin utilization ceiling (70% hard max, 30% buffer always maintained)
7. Confidence absolute floor (0.50 — Layer 1 constant, no exceptions)
8. Risk:reward floor (2.0 — Layer 1 constant, no exceptions)

All checks return specific, auditable rejection reasons. Every rejection is logged.

**Drawdown-adjusted sizing:**

| Drawdown | Size Multiplier |
|---------|----------------|
| 0–5% | 1.00x (full size) |
| 5–10% | 0.75x |
| 10–15% | 0.50x |
| 15–20% | 0.25x |
| >20% | 0.00x — HALT, human review required |

**Capital preservation mode:**
- Trigger: daily loss reaches 50% of max daily limit
- Effect: no new entries, tighten all stops to 50% of normal ATR
- Alert: CRITICAL dispatched immediately

**Consecutive loss governor (time-windowed, per cross-strategy governor):**

| Condition | Action |
|-----------|--------|
| 2 losses in 60 min | Reduce size 25% |
| 3 losses in 60 min | Reduce size 50% + alert |
| 4 losses in 60 min | Pause strategy 2 hours |
| 5 losses in session | Halt strategy for day |

**Settlement-aware margin model:**
```
Available capital =
  equity_delivery_settled
  + fo_daily_settled
  + fo_mtm_unrealized (at 80% haircut)
  - margin_blocked_span
  - margin_blocked_exposure
  - cash_reserve_mandatory
```
This calculation runs before every order. Wrong capital figure at ₹5 crore = margin call risk.

### 0.6 Kill Switch Hierarchy

Three levels. Every activation written to audit_trail BEFORE action executes.

| Level | Trigger | Effect | Reset |
|-------|---------|--------|-------|
| 1 | New entries only blocked | Stop new trades, existing positions managed | Authorization code via API |
| 2 | All trading blocked | Stop all + cancel pending orders + pause strategies | Authorization code via API |
| 3 | Emergency flatten | Trigger EmergencyFlattenService | Manual system restart only — no API reset |

Reset codes generated at activation time. Wrong code = rejected. No bypass.

**Kill switch cascade triggers (automatic):**
- Daily loss limit breached → Level 2
- Drawdown halt threshold → Level 2
- Black swan protocol → Level 1 (human decides Level 3)
- WebSocket reconnection failed → Level 2
- Reconciliation DISCREPANCY > threshold → Level 2

### 0.7 Black Swan Protocol

**Detection triggers (any one sufficient):**
- VIX intraday change > 30% in either direction
- NIFTY move > 4% from previous close by 10 AM
- More than 40% of NIFTY 50 stocks at circuit filters
- ATM options spread > ₹100
- NSE circuit breaker L1 or above triggered
- 3 or more position stop losses hit within 5 minutes

**Phase 1 — Immediate (within 30 seconds):**
- Halt all new entries (Level 1 kill switch)
- Cancel all pending limit orders
- EMERGENCY alert with: trigger reason, current positions, P&L, margin utilization

**Phase 2 — Assessment (30 seconds to 5 minutes):**
- Do NOT autonomously flatten (autonomous flatten into black swan = worst prices)
- Widen all stops to 2× normal ATR-based levels (prevent stop hunting)
- Calculate maximum loss if all positions hit widened stops
- If max loss scenario < 5% of portfolio: HOLD, wait for human
- If max loss > 5%: URGENT alert, 3-minute human response window

**Phase 3 — Resolution (human decision required):**
- Option A: Resume with reduced size after human confirms stability
- Option B: Human orders flatten, system executes at human-approved timing
- Option C: No human response in 10 minutes → attempt orderly limit-order exit (no market orders unless deeply underwater)

**Post-black-swan:** Mandatory system audit before resuming autonomous trading. Paper trading for 3 days before live resumption (configurable).

### 0.8 Emergency Flatten Service

Standalone process. Independent of main backend. Zero shared imports.

**Triggers:**
1. Manual command: `POST /flatten` with authorization_code
2. Level 3 kill switch from main backend
3. System health check failure (system cannot verify its own state)

**Behavior:**
1. Disable all other services (prevent new orders during flatten)
2. Fetch positions directly from Zerodha (bypass internal state)
3. Place market orders for all open positions (staggered 0.5s gap)
4. Wait for fills (max 2 minutes)
5. Write to PostgreSQL audit_trail
6. Send complete flatten report via Telegram
7. Set system state to HALTED

### 0.9 Tiered Alert System

| Level | Severity | Channels | Acknowledgment | Auto-action |
|-------|---------|---------|----------------|------------|
| 0 (INFO) | — | Dashboard log | Not required | None |
| 1 (WARNING) | Low | Telegram | Not required (tracked) | None |
| 2 (CRITICAL) | High | Telegram + Twilio voice | Required within 10 min | Trading paused |
| 3 (EMERGENCY) | Critical | Telegram + voice + SMS simultaneously | Required within 5 min | Level 1 kill switch |

Unacknowledged CRITICAL: repeat every 3 minutes.
Unacknowledged EMERGENCY: escalates to Emergency Flatten after 5 minutes.
Acknowledgment via Telegram bot command: `/ack {code}`

### 0.10 System Health Monitor

**Health states:**
- `HEALTHY`: All Tier 0 components operational
- `WARNING`: One non-critical service degraded, trading continues with raised thresholds
- `CRITICAL`: Critical service down, trading halted, alert sent
- `OFFLINE`: System cannot determine its own state, Emergency Flatten triggered

**Endpoints:**
```
GET /api/v1/health          — overall state (UptimeRobot monitors this)
GET /api/v1/health/ready    — trading readiness (can we trade right now?)
GET /api/v1/health/detailed — per-component breakdown
GET /api/v1/ready           — Kubernetes probe, simple 200/503
```

**External monitoring:** UptimeRobot (free) pings /health every 5 minutes. Telegram + email alert on downtime.

**Startup sequence (systemd enforced):**
PostgreSQL → MongoDB → Redis → Backend. Backend /health returns 503 until all Tier 0 components verified.

### 0.11 Cross-Strategy Risk Governor

Monitors portfolio-level risk across all books simultaneously.

**Correlated loss detection:**
- Portfolio P&L drops > 1.5% in 30 minutes → PORTFOLIO_STRESS state
- Portfolio P&L drops > 2.5% in 60 minutes → PORTFOLIO_CRISIS state

**Shared factor exposure (computed every 30 minutes):**
- INR sensitivity, Banking sector beta, Global market beta, VIX sensitivity
- If any single factor > 40% of portfolio risk: alert

**Simultaneous exit coordination:**
- Multiple positions needing simultaneous exit: stagger 30 seconds apart
- Largest position exits first
- Reduce order size 30% for simultaneous exits (accept worse price, reduce market impact)

---

## TIER 1 — Alpha Generation Engine

*Runs only when Tier 0 is HEALTHY or WARNING.*

### Context / Regime Engine

Updates every 5-minute candle. If not updated within 7 minutes: state = STALE, downstream agents raise thresholds.

**Inputs (all computed code, no AI):**
- ADX + directional movement → trend strength
- ATR relative to 20-day average → volatility regime
- Advance-Decline ratio → breadth
- NIFTY vs VWAP → intraday bias
- India VIX level + change rate → volatility state
- Time-to-expiry → expiry proximity flag
- Pre-identified event schedule → event day flag

**Output:**
```json
{
  "trend_state": "trending_bullish | trending_bearish | range | breakout",
  "volatility_state": "low | normal | elevated | extreme",
  "market_bias": "bullish | bearish | neutral",
  "breadth_state": "strong | weak | diverging",
  "expiry_proximity": true,
  "event_flag": false,
  "regime_confidence": 0.82,
  "valid_until": "timestamp"
}
```

### Weighted Signal Engine

Signal weights are regime-adaptive, not static:

| Signal Category | Trending | Range | Expiry | Event |
|----------------|---------|-------|--------|-------|
| SMC Structure | 0.30 | 0.10 | 0.05 | 0.05 |
| Options Intelligence | 0.20 | 0.15 | 0.45 | 0.35 |
| Market Structure | 0.20 | 0.20 | 0.10 | 0.10 |
| Volume / VWAP | 0.15 | 0.20 | 0.15 | 0.15 |
| Macro / Breadth | 0.10 | 0.15 | 0.10 | 0.25 |
| Sentiment / News | 0.05 | 0.10 | 0.10 | 0.10 |
| Mean Reversion | 0.00 | 0.10 | 0.05 | 0.00 |

### Probability Engine

**Confidence scoring (applied sequentially):**
- Base: weighted average of signal scores
- +0.05 if cross-agent agreement > 0.80
- −0.10 if critical signal conflicts (SMC long + options bearish)
- −0.05 if regime confidence < 0.65
- −0.08 if expiry day without options confirmation
- −0.15 if event flag active
- +0.03 if historical pattern reliability > 0.75 for this setup type
- −0.20 if data validity warnings active for relevant data type

**Thresholds:**
- Minimum for trade entry: 0.65 (configurable Layer 3)
- Minimum for maximum sizing: 0.82
- Below 0.50: always reject (Layer 1 constant)

### Trade Grade

Computed deterministically. No AI involvement.

| Grade | Criteria |
|-------|---------|
| A | Confidence ≥ 0.82, RR ≥ 2.5, no conflicts, scenario matched |
| B | Confidence ≥ 0.72, RR ≥ 2.0, minor conflicts acceptable |
| C | Confidence ≥ 0.65, RR ≥ 2.0 (minimum viable trade) |
| D | Below threshold — blocked at execution, logged for learning only |

### Pre-Submission Guard (13 Checks)

All 13 must pass. One failure = rejected. No exceptions.

| # | Check | Fails if |
|---|-------|---------|
| 1 | No-trade window | Current time 9:15–9:30 or 15:25–15:30 |
| 2 | Zerodha session | Session state ≠ ACTIVE |
| 3 | Reconciliation status | Status = DISCREPANCY or HALTED |
| 4 | Margin utilization | Post-trade utilization > 70% |
| 5 | Daily loss limit | Daily loss ≥ configured limit |
| 6 | Strategy state | State not in {LIVE, LIVE_RESTRICTED, PAPER} |
| 7 | Idempotency | Key already exists in orders table |
| 8 | Data validity | Required data types INVALID or STALE |
| 9 | Liquidity | OI below minimum, spread above maximum |
| 10 | Slippage estimate | Estimated slippage > maximum acceptable |
| 11 | Rate limit | Zerodha API rate limit headroom insufficient |
| 12 | Kill switch / Black swan | Kill switch active OR black swan protocol active |
| 13 | Explainability (Rule 13) | Signal explainability block missing or incomplete |

The `why_not_rejected` list from passing checks feeds directly into the signal's explainability block.

### Intraday SMC + F&O Agent

Unified agent. Cannot operate without both SMC and options intelligence.

**No-trade conditions (hard blocks beyond the guard):**
- First 15 minutes (9:15–9:30): no execution — unreliable IV, wide spreads, erratic OI
- Last 5 minutes (15:25–15:30): no new positions
- VIX > 25 without volatility playbook active
- Options chain older than 60 seconds
- IV percentile < 15
- Bid-ask spread on target strike > 2% of mid
- Regime = RANGE when strategy requires TRENDING

**Pre-market debate (NOT live Claude at entry):**
- 9:00 AM: Claude Haiku generates 3–5 intraday scenarios with playbooks — cached to Redis
- At entry time: signal matched against cached scenarios
- If matches: proceed with cached bull/bear framework (no Claude call, no latency)
- If novel setup not in cache: reduce confidence by 0.15, require higher threshold

**Playbooks (pre-computed):**
- Trend day (ADX > 25, directional)
- Expiry day (gamma, IV crush, max pain)
- Gap day (overnight gap, first-hour behavior)
- Event day (reduced size, wider stops)
- Range day (mean reversion only)

### Market Microstructure Agent

Computed quantitative analysis. No AI. Updates every 5 minutes.

**Responsibilities:**
- Dealer gamma exposure by strike (net dealer gamma, long/short gamma zones)
- Gamma flip level, gamma wall above/below
- Liquidity pool identification (buy/sell pools from OI)
- Max pain calculation and proximity analysis
- Dealer hedging zone mapping
- OI buildup anomaly detection (sigma-based)
- OI vs price divergence signals

### Execution Engine

**Order submission flow:**
1. Create order record in PostgreSQL (CREATED)
2. Generate idempotency key
3. Submit to Zerodha API
4. Update to SUBMITTED
5. Wait for acknowledgment (max 10 seconds)
6. On acknowledgment: ACKNOWLEDGED
7. On fill: FILLED, create position record
8. On partial fill: PARTIALLY_FILLED, decision logic
9. On rejection: REJECTED, log reason, trigger signal feedback
10. On timeout (30 seconds, no status): query Zerodha directly

**Limit order management:**
- Enter at LTP or slight improvement
- If not filled in X seconds: assess slippage tolerance
- If within tolerance: adjust limit
- If market moved beyond tolerance: cancel, mark MISSED
- Never chase. A missed entry is better than a bad fill.

### Explicit Degradation Contracts

Every component has defined behavior under failure. No improvisation.

**Claude API unavailable:**

| Function | Without Claude | Behavior |
|---------|---------------|---------|
| Pre-market scenarios | Use yesterday's cached | DEGRADED |
| News summarization | Skip, no news signal | DEGRADED |
| Swing setup debate | Skip, raise threshold +0.10 | DEGRADED |
| Intraday decision | Pre-cached, no change | FULL |
| Investment new position | Block initiation | HALTED (investment only) |
| Investment existing mgmt | Rule-based management | DEGRADED |
| Weekly learning | Defer to next week | Postponed |

**Rule: Claude unavailability NEVER halts intraday or swing operations.**

---

## TIER 2 — CIO Allocation System

### Portfolio State Manager

- Authoritative capital allocation per book (PostgreSQL)
- Real-time P&L per position, book, strategy
- Cross-book exposure aggregation
- Rebalancing signals when allocation drifts from targets

**Cross-book sector exposure:**
If Investment long HDFC (banking) + Swing long ICICI (banking) + Intraday long BANKNIFTY = 3× banking concentration.
Alert if single sector > 40% of total portfolio. Alert if single stock > 15% of total portfolio.

### Investment Alpha Agent

**Stock scoring model:**

| Factor | Weight | Components |
|--------|--------|-----------|
| Quality | 30% | ROE, ROCE, debt/equity, interest coverage, promoter holding, governance |
| Growth | 25% | Revenue growth 3yr, earnings growth 3yr, margin expansion, guidance quality |
| Value | 25% | PE vs sector, PB ratio, EV/EBITDA, FCF yield, margin of safety |
| Momentum | 20% | Price momentum 12m, earnings revision, institutional accumulation |

**Minimum thresholds for consideration:**
- Quality score > 0.65
- Sector in improving or strong phase
- Margin of safety > 15%
- Market cap > ₹5,000 Cr (liquidity requirement)

**Decision types:** INITIATE (full Claude Sonnet analysis), ADD (lighter analysis), REDUCE (valuation or fundamentals trigger), EXIT (thesis break only, not temporary price), HOLD (documented reason required, not default state).

### Swing Alpha Agent

**Entry requirements (all mandatory):**
- Trend alignment: daily + weekly timeframe
- Volume expansion: >1.5× average on breakout
- Sector strength: outperforming NIFTY
- Market regime: TRENDING or BREAKOUT (not RANGE)
- Minimum RR: 2.5:1
- Minimum confidence: 0.70
- No major earnings within hold period

**Swing debate:** Daily pre-market batch. Claude Haiku analyzes up to 5 setups in one call, cached, referenced at entry time.

### Adaptive Correlation Engine

Three lookback windows computed simultaneously, blended by regime:

| Regime | Blend |
|--------|-------|
| Normal | 40% × 20-day + 40% × 60-day + 20% × 5-day |
| Elevated volatility | 50% × 5-day + 30% × stress + 20% × 20-day |
| Crisis | 70% × stress + 30% × 5-day |

Stress correlation computed from 2020 and 2022 crisis periods.

**Concentration thresholds:**
- Normal: > 0.70 triggers review
- Elevated volatility: > 0.50 triggers review
- Crisis: > 0.30 triggers review (everything correlates in crisis)

---

## TIER 3 — AI Intelligence Layer

*Runs 24/7. Non-blocking. Intelligence enriches decisions, never gates real-time execution.*

**Critical rule: Intelligence is always pre-computed and cached. No Tier 1 execution component ever waits for a live Claude call.**

### Claude Model Routing

| Task | Model | Frequency | Cache TTL |
|------|-------|-----------|----------|
| News headline summarization | Haiku | Per batch | 4 hours |
| Event extraction | Haiku | Per batch | 4 hours |
| Earnings summarization | Haiku | Per results | 24 hours |
| Concall key points | Haiku | Per event | 24 hours |
| Pre-market synthesis | Haiku | Daily | 24 hours |
| CIO daily briefing | Haiku | Daily | 24 hours |
| Sector analysis | Haiku | 3× daily | 2 hours |
| Swing setup scenarios | Haiku | Pre-market batch | 24 hours |
| Investment thesis | Sonnet | Per new position | 48 hours |
| Conflicting signal reasoning | Sonnet | Per occurrence | No cache |
| High-capital decision | Sonnet | Per occurrence | No cache |
| Post-trade postmortem | Sonnet | Batch of 3 | Permanent |
| Weekly learning synthesis | Sonnet | Weekly | Permanent |

**Target usage:** 90–95% Haiku, 5–10% Sonnet.

**Soft limits (log only, do not block):**
- Daily Haiku: 500 calls
- Daily Sonnet: 30 calls

### Mandatory Batching Protocol

Any task processing multiple items of the same type must batch:

```
Correct:   20 headlines → 1 Claude call → 20 outputs
Incorrect: 20 headlines → 20 Claude calls (BANNED)
```

**Batch size limits:**
- News summarization: max 20 per batch
- Earnings summaries: max 5 per batch
- Swing setups: max 5 per batch
- Postmortems: max 3 per batch

### Cache-Before-Call Protocol

```
1. Generate cache_key (deterministic hash of: prompt_type + input_hash + date)
2. Check Redis hot cache
3. If hit: return cached result
4. If miss: check MongoDB warm cache
5. If hit: promote to Redis, return
6. If miss: call Claude API
7. On response: write to MongoDB + Redis simultaneously
8. Log: model_used, tokens_used, cost_usd, cache_hit=false
```

### Pre-Market Intelligence Package

Runs 8:30 AM – 9:10 AM every trading day:

```
8:30 AM — Macro data collection (VIX, global markets, USDINR, FII/DII)
8:40 AM — News batch + Haiku summarization
8:45 AM — Options chain pre-open analysis
8:50 AM — Sector strength ranking computation
8:55 AM — Regime preliminary assessment
9:00 AM — Intraday scenario analysis (Haiku: 3–5 scenarios with playbooks)
9:05 AM — Risk limit refresh, drawdown state updated
9:08 AM — Swing position review
9:10 AM — Package cached to Redis. System declared READY.
```

If package fails to complete by 9:10 AM: system enters CAUTIOUS mode, confidence thresholds raised +0.10, no new positions until package completes or human override.

---

## TIER 4 — Learning and Adaptation

### Learning Governance Protocol

Learning system writes recommendations only. Humans approve. Parameters updated only after human sign-off.

**Process:**
1. Weekly: learning agent analyzes past week's signals and trades
2. Generates: parameter change recommendations with rationale
3. Shadow mode comparison: new params vs current on past data
4. Recommendation report produced (NOT automatic deployment)
5. Human reviews and approves/rejects each recommendation
6. Approved → staging environment for 5 trading days in shadow mode
7. If staging matches expectation → promote to production
8. Any approved change can be reverted in < 5 minutes

**What learning can change (bounded):**
- Signal weights (within ±20% of baseline)
- Confidence thresholds (within defined range)
- Sizing multipliers (within ±10% of baseline)
- No-trade filter parameters (within defined range)

**What learning cannot change:**
- Core strategy logic
- Hard risk limits
- Order execution logic
- Any Tier 0 component
- Capital allocation targets

**Database permissions enforce this:** Learning service user has write access ONLY to `learning_recommendations` table. It has no UPDATE permission on `strategy_parameters`. This is a database-level rule, not an application-level convention.

### Anti-Drift Protections

**Regime-balanced learning:** Training window must contain minimum 20% bullish + 20% bearish regimes. If >80% single regime: recommendations marked REGIME_BIASED, require explicit human approval.

**Directional bias detection:** Track win rate separately for longs vs shorts. If long win rate exceeds short by > 20%: flag potential bullish bias.

**Degradation spiral detection:** If trades_per_day declining > 30% over 4 weeks without regime change → flag POSSIBLE_PARALYSIS_SPIRAL, alert human to review threshold changes.

---

# PART 4 — FORMAL EXPLAINABILITY CONTRACT

*Rule 13: Every signal and execution must be explainable. No black-box confidence scores.*

Every signal object must persist:

```json
{
  "why_trade": ["Bullish BOS on 15-min structure", "Positive OI buildup CE side"],
  "why_not_rejected": ["Session ACTIVE", "Margin 45% within 70% ceiling", "..."],
  "counter_argument": ["Macro bearish divergence possible", "Banking IV elevated"],
  "risk_factors": ["Expiry day gamma risk", "VIX elevated at 18"],
  "confidence_breakdown": {
    "smc": 0.82,
    "options": 0.75,
    "volume_vwap": 0.68,
    "macro": 0.61,
    "historical_reliability": 0.74
  },
  "regime_context": {
    "trend_state": "trending_bullish",
    "volatility_state": "normal",
    "expiry_proximity": false,
    "regime_confidence": 0.81,
    "weights_applied": {}
  },
  "scenario_match": {
    "matched": true,
    "scenario_name": "TREND_CONTINUATION",
    "scenario_probability": 0.68,
    "confidence_penalty_applied": 0
  },
  "conflict_resolution": {
    "conflicts_detected": false,
    "conflict_description": null,
    "penalty_applied": 0
  },
  "trade_grade": "A",
  "generated_by": "intraday_smc_fo",
  "explainability_version": "1.0"
}
```

**Post-trade writeback (on trade closure):**
```json
{
  "post_trade": {
    "actual_outcome": "WIN | LOSS | SCRATCH",
    "actual_return_pct": 1.4,
    "confidence_was_accurate": true,
    "primary_failure_reason": null,
    "learning_flags": []
  }
}
```

**Who populates each field:**
- `why_trade`: WeightedSignalEngine
- `why_not_rejected`: PreSubmissionGuard (after all 13 checks pass)
- `counter_argument`: ProbabilityEngine from conflict resolution + cached scenario bear case
- `risk_factors`: RiskEngine during approval
- `confidence_breakdown`: WeightedSignalEngine (raw per-component before weighting)
- `regime_context`: RegimeEngine snapshot at signal generation time
- `scenario_match`: PremarketPackage cache lookup
- `trade_grade`: ProbabilityEngine (computed last)
- `post_trade`: Written back on position close

---

# PART 5 — ENGINEERING RULES

All 14 rules are frozen. Non-negotiable during implementation.

| # | Rule |
|---|------|
| 1 | PostgreSQL is the only source of truth for anything that affects money |
| 2 | Every order submission is preceded by a pre-submission checklist that must fully pass |
| 3 | The system never assumes it knows the state of the broker — always fetch for consequential decisions |
| 4 | Silent failures are the worst possible outcome — every failure must be loud |
| 5 | No business logic in the execution layer — it receives fully formed, validated order specs only |
| 6 | Claude is never on the critical path for intraday execution |
| 7 | Every component has an explicit maximum response time budget |
| 8 | Audit trail is append-only and written BEFORE the action executes |
| 9 | Configuration is layered (Layer 1: immutable code, Layer 2: env, Layer 3: runtime via API) |
| 10 | Every background job has a completion deadline — timeouts enforced, incomplete jobs logged as failures |
| 11 | Regime data and correlation data are never stale by more than one candle |
| 12 | No money moves without reconciliation status = CLEAN or HUMAN_OVERRIDE (logged, authenticated) |
| 13 | Every signal and execution must be explainable — no black-box confidence scores |
| 14 | No module exceeds ~1500 LOC — split before complexity, never after |

### Response Time Budgets (Rule 7)

| Component | Budget |
|-----------|--------|
| Data validity check | 50ms |
| Pre-submission checklist | 100ms |
| Risk engine approval | 200ms |
| Order submission to Zerodha | 500ms |
| Regime engine update | 300ms |

---

# PART 6 — ANTI-PATTERNS (BANNED)

All 12 anti-patterns are banned during development. No exceptions.

| # | Anti-pattern | Why |
|---|-------------|-----|
| 1 | Optimistic cache for monetary state | Redis position cache diverges from PostgreSQL silently |
| 2 | Catch-all exception suppression (`except Exception: pass`) | Silent failures in production |
| 3 | Status inferred from absence | Absence of FILLED record ≠ not filled. State must be explicitly stored. |
| 4 | Confidence averaging that masks conflicts | 0.20 options score averaged away in expiry regime is a dangerous lie |
| 5 | Time-dependent test code | Tests must use FrozenClock and work at any time of day |
| 6 | Feature flags as permanent architecture | Each book is a module with an interface, not an `if SWING_ENABLED:` flag |
| 7 | God orchestrator with business logic | Orchestrator routes events, never contains business logic |
| 8 | Synchronous Claude calls in market-hours request handlers | Claude must be async, pre-computed, or cached |
| 9 | Shared mutable state between strategies | Strategies share data only via database, never via shared memory objects |
| 10 | Magic numbers in risk logic | Every threshold is a named constant with a comment explaining its derivation |
| 11 | Deployment without rollback plan | Every production deployment has a documented <5-minute rollback procedure |
| 12 | Learning system autonomy creep | Learning service user has NO database permission to write strategy_parameters |

---

# PART 7 — IMPLEMENTATION ROADMAP

## Capital Graduation Protocol

| Stage | Capital | Scope | Success Criteria |
|-------|---------|-------|-----------------|
| 0 — Paper | ₹0 | Full system, zero real capital | ≥60% win rate, no system errors for 5 consecutive days, reconciliation and kill switches verified |
| 1 — Minimum | ₹2–5L | Intraday F&O only, max 1 position | 4 weeks without system errors, drawdown <10% |
| 2 — Expanded | ₹10–25L | Intraday + Swing activated, max 3 positions | 8 weeks, Sharpe >1.0, drawdown <15% |
| 3 — Multi-crore | ₹5 Cr target | All three books active | Continuous monitoring |

**Paper trading minimum: 40 trading days with statistical significance testing. Not 5 days. Not "it looks good." 40 days.**

## Build Phases

| Phase | Scope | Capital | Gate |
|-------|-------|---------|------|
| 1 | Tier 0 Survivability | Paper only | All unit + integration tests passing, 72-hour continuous VPS run, zero silent failures |
| 2 | Tier 1 Core Trading Pipeline | Paper → Stage 1 | 40 paper trading days, Brier score computed, black swan simulation passes |
| 3 | Tier 2 + Tier 3 Intelligence | Stage 1 → Stage 2 | Claude unavailability tested, pre-market package 100% reliable |
| 4 | Investment Book + Learning | Stage 2 → Stage 3 | Learning governance workflow end-to-end tested |
| 5 | Observability + Dashboard | Stage 3 | Prometheus, Grafana, full React dashboard |

## Phase 1 Definition of Done

Before Phase 2 begins, ALL of the following must be true:

- [ ] All unit tests passing with required coverage (validity_engine 95%+, kill_switches 95%+)
- [ ] All integration tests passing including 5 Zerodha failure modes
- [ ] Emergency flatten tested: closes simulated positions correctly
- [ ] 72-hour continuous run on VPS: no unhandled exceptions, no silent failures
- [ ] Kill switch cascade tested: Level 1 → 2 → 3 correct behavior
- [ ] Black swan simulation test passes
- [ ] Reconciliation handles: clean state, discrepancy, warm start correctly
- [ ] CRITICAL alert unacknowledged → escalation fires correctly
- [ ] Health endpoint correctly reflects component failures (manual kill test)
- [ ] All 12 anti-patterns verified absent via code review
- [ ] Runbooks written for: emergency flatten, token refresh failure, reconciliation discrepancy, warm start
- [ ] VPS backup scripts tested and verified

---

# PART 8 — TECH STACK DECISIONS

## Confirmed Stack (Frozen)

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Primary DB | PostgreSQL 15 | ACID for financial state |
| Intelligence DB | MongoDB 6 | Schema-flexible, analytics-friendly |
| Cache / Queue | Redis 7 | Streams for events, cache for intelligence |
| API Framework | FastAPI | Async, production-ready |
| Task Scheduling | APScheduler | Sufficient for V1 (not Celery) |
| Frontend | React (single page) | No SSR needed, familiar |
| Process Management | systemd | Native, reliable |
| Reverse Proxy | Nginx | SSL, already proven |
| Indicators | TA-Lib + pandas | Proven, sufficient |
| Backtesting | vectorbt | Fast, when needed |
| Validation | Pydantic v2 | Already in use |
| Logging | Loguru → JSON | Structured, searchable |
| Monitoring | FastAPI /metrics | Simple, no Grafana overhead in V1 |
| Broker | KiteConnect | Only option, isolated service |
| AI | Anthropic API | Haiku default, Sonnet selective |
| Alerts | Telegram Bot + Twilio | Free, reliable, instant |

## Explicitly Deferred

| Tool | When to Introduce |
|------|------------------|
| Celery | When background job complexity justifies it (Phase 4+) |
| Prometheus + Grafana | When metrics volume justifies it (Phase 5) |
| Next.js | When dashboard needs routing or SSR (Phase 5) |
| Polars | When data volume exceeds pandas threshold |
| TimescaleDB | When OHLC/IV query performance degrades (ADR-002 documented) |

---

# PART 9 — INFRASTRUCTURE

## VPS Specification

- AWS Lightsail Mumbai (minimize Zerodha API latency)
- 4GB RAM, 2 vCPU minimum, 50GB SSD
- Ubuntu 22.04 LTS
- 99.9% uptime SLA minimum

## Systemd Service Dependency Order

```
postgresql.service
  → mongod.service
    → redis-server.service
      → quantara-backend.service
quantara-flatten.service (independent, only requires postgresql.service)
```

## Backup Strategy

- PostgreSQL: daily `pg_dump` to S3 (automated)
- MongoDB: daily `mongodump` to S3 (automated)
- Config: stored in git (no secrets in git)
- Secrets: environment variables in systemd service files

## Redis Key Conventions

All keys: `quantara:{category}:{subcategory}:{identifier}`

**State keys (no TTL, explicit management):**
```
quantara:state:session:zerodha
quantara:state:health:system
quantara:state:risk:daily
quantara:state:circuit_breakers:{service}
quantara:state:data_validity:{data_type}
```

**Cache keys (TTL-based):**
```
quantara:cache:regime:current              TTL: 7 minutes
quantara:cache:premarket:{date}            TTL: 24 hours
quantara:cache:options:chain:{underlying}  TTL: 90 seconds
quantara:cache:microstructure:{underlying} TTL: 6 minutes
quantara:cache:ai:{cache_key}              TTL: per prompt type
```

**Streams (event bus):**
```
quantara:stream:market_events
quantara:stream:signals
quantara:stream:orders
quantara:stream:alerts
```

---

# PART 10 — OPEN QUESTIONS (MUST ANSWER BEFORE LIVE CAPITAL)

These must be answered before Stage 1 live capital deployment:

1. **Zerodha token refresh strategy** — fully automated TOTP via Playwright, or semi-manual with 8:00 AM alert?
2. **Order fill timeout behavior** — if no fill confirmation in 45 seconds and Zerodha query returns ambiguous status: wait or cancel?
3. **Emergency flatten trigger access** — if software has crashed, how does human trigger flatten? Direct HTTP to port 8001 or separate physical kill mechanism?
4. **Maximum capital at risk per day in absolute rupees** — this number must be hardcoded, not computed. What is it for Stage 1?
5. **Maximum simultaneous open positions** — Stage 1 answer: 1. Stage 2 answer: 3. Confirm.
6. **Primary options chain data source** — Zerodha's own API sufficient, or external vendor (Sensibull, Opstra, etc.)?
7. **Data staleness thresholds per type** — tick: 5s (confirmed), options chain: 60s (confirmed), macro: ? minutes
8. **Paper trading success criteria** — what statistical tests define "ready for live capital"? Sharpe threshold? Win rate threshold? Minimum sample size?
9. **Learning system reviewer** — who reviews and approves parameter change recommendations? What is the review process?
10. **NSE holiday calendar integration** — where does the system get the official holiday list to skip trading days?

---

*Document compiled from architecture versions v1, v2, v3, v3.1*
*All decisions above are frozen for implementation*
*Any change to frozen decisions requires explicit architectural review, not code-level improvisation*
