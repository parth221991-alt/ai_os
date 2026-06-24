# QUANTARA OS — TIER-1 ALPHA EXPANSION PACK
## Extension Architecture v1.1 (companion to MASTER v3.1 and Institutional Extension v1.0)

**Status:** Proposal — requires architectural review before adoption
**Scope discipline:** Unchanged. Tier 0, kill switches, database split, engineering rules, and anti-patterns are untouched. Every new alpha source enters execution only through the existing Weighted Signal Engine → Probability Engine → Pre-Submission Guard path. No module gets a private road to the broker.
**New discipline added:** every module below carries a **Feasibility Grade** against the realities of a retail-API, single-VPS operation:

| Grade | Meaning |
|-------|---------|
| F-A | Fully buildable today with Zerodha KiteConnect + free public data |
| F-B | Buildable with one paid/scraped data source (NSE data products, vendor chain data, filings feeds) |
| F-C | Requires institutional infrastructure (colocation, full order book, tick-by-tick TBT feed) — design the interface now, defer the implementation |

A world-class system is honest about its data perimeter. Pretending to have institutional order flow while running on a 5-level retail depth feed is how systems lie to themselves — and anti-pattern #4's spirit (no masked conflicts) applies to capability claims too.

---

# PART 1 — RECONCILIATION AGAINST EXISTING ARCHITECTURE

| Requested module | Already covered? | Verdict |
|------------------|------------------|---------|
| Market microstructure modeling | Largely — Microstructure Agent (dealer gamma, flip levels, walls, OI anomalies, max pain, liquidity pools) | EXTEND, don't rebuild |
| Execution optimization / slippage | Partially — Execution Engine has limit management, "never chase," slippage estimate (guard check #10), staggered exits | EXTEND with pre-trade cost model + post-trade TCA |
| Order flow inference | Thin — tick validity checks exist, no flow analytics | NEW |
| Options volatility surface | Thin — IV validity checks, IV percentile no-trade filter | NEW |
| Cross-asset arbitrage | Absent | NEW |
| Statistical arbitrage | Absent | NEW (new strategy module, Swing book) |
| Smart money tracking | Partial — FII/DII analytics in Extension v1.0 | EXTEND into composite engine |
| Insider pattern detection | Absent | NEW — **reframed, see Part 2.6** |

---

# PART 2 — MODULE ARCHITECTURES

## 2.1 Cross-Asset Arbitrage Detection — Grade F-A/F-B

**Honest framing first:** classical risk-free arbitrage in Indian markets is mostly dead at retail cost structures — STT, stamp duty, brokerage, and impact consume the basis. The institutional move is to use arbitrage *dislocations as information*, and execute only the rare dislocations that clear the full cost stack.

**Sub-detectors (all computed, no AI):**

| Detector | Definition | Primary use |
|----------|-----------|-------------|
| Cash–futures basis monitor | (Fut − Spot − fair carry) per index and liquid stock futures, annualized | Basis z-score as sentiment input (steep contango = leveraged长 positioning; backwardation = hedging demand). Execution only if net-of-cost edge > threshold |
| Calendar spread monitor | Near vs far futures vs fair roll | Roll timing for the Swing/Investment hedges; anomaly = event repricing signal |
| Put–call parity scanner | C − P vs S − K·e^(−rT) per liquid strike | Violations beyond cost stack = data error (feed validity check) or genuine dislocation; either way, flag before trading that strike |
| Box spread monitor | Synthetic lending rate from boxes vs repo | Funding stress indicator feeding the Liquidity Cycle Detector |
| NSE–BSE dual-listing spread | Same-ISIN price gap | Mostly an execution-venue signal (route to cheaper venue), rarely a trade |
| ETF–iNAV monitor | Liquid ETFs vs indicative NAV | Dislocation = market stress signal; occasionally tradable in size constraints |

**Cost gate (hard, named constants):** no arb execution unless `edge_after_costs > 2 × estimated_total_cost` where the cost model includes STT, stamp, brokerage, GST, and the impact estimate from 2.8. Below that, the dislocation is *published as a signal* to the intelligence feed, not traded.

**Output contract:** `arb_state` object per market, cached 60s, consumed by Regime Engine (funding/positioning context) and by the Pre-Submission Guard as a new data-sanity input (a PCP-violating strike is suspect data until proven otherwise).

## 2.2 Statistical Arbitrage Module — Grade F-A (research-gated)

A genuine new **strategy module** (per anti-pattern #6: a module with the standard strategy interface, not a feature flag), homed in the **Swing book** (2–30 day horizon matches mean-reversion half-lives in Indian large caps).

**Pipeline:**

```
Universe: NIFTY 100 ∩ (market cap > ₹5,000 Cr) ∩ (ADV > liquidity floor)
  → Pair candidates: same sector/sub-industry, correlation pre-filter > 0.7
  → Cointegration test: Engle–Granger + Johansen agreement required (both or no trade)
  → Half-life filter: OU half-life ∈ [3, 25] days (must fit Swing book horizon)
  → Stability check: cointegration must hold in 3 of 3 rolling sub-windows
  → Live monitoring: spread z-score on the validated hedge ratio
Entry:  |z| > 2.0 (configurable Layer 3)        Exit: z crosses 0 or ±0.5
Stop:   |z| > 3.5 (relationship-break stop) OR half-life × 2 elapsed (time stop)
Kill:   cointegration p-value degrades past threshold → force exit, retire pair
```

**Risk specifics:** pairs are two-legged — leg risk is real. Entry only via the Execution Engine's paired-order mode (new): second leg must fill within T seconds or first leg is closed at market (named constant, small size). Sector-neutral by construction; net exposure of the stat-arb sleeve capped at a Layer-3 constant.

**Governance:** the module ships **disabled**. It activates only after Research Lab walk-forward validation (Extension v1.0 Part 8 gates: out-of-sample distribution, regime-tagged results, cost-realistic). Stat arb without rigorous validation is the most seductive way to lose money slowly — the lab gate is non-negotiable.

**Signals integrate normally:** stat-arb confidence feeds the standard explainability contract; "Mean Reversion" already has a row in the regime weights table (0.00 trending / 0.10 range) — the module's signals are naturally suppressed in trending regimes by frozen design.

## 2.3 Options Volatility Surface Modeling — Grade F-A

**Inputs:** validated option chains (existing Data Validity Engine — IV sanity, parity checks, partial-chain flags already enforced).

**Surface construction (per underlying, per refresh):**

1. Clean mid-IVs per strike/expiry (reject quotes failing existing validity checks; require ≥80% strike coverage — the PARTIAL flag rule already exists)
2. Fit per-expiry smile: **SVI parameterization** (5 params: a, b, ρ, m, σ) with no-arbitrage constraints (butterfly: density ≥ 0; calendar: total variance monotone in T)
3. Stitch term structure; emit fitted surface + residuals

**Derived analytics (the actual alpha inputs):**

| Metric | Use |
|--------|-----|
| ATM IV term structure slope | Event pricing detection (kink at event expiry = market pricing the event) |
| 25Δ risk-reversal analog (skew) | Directional fear/greed; skew percentile vs 1-year history |
| Butterfly (smile curvature) | Tail demand; crash-hedge bid detection |
| IV rank/percentile by moneyness bucket | Replaces the single scalar IV-percentile no-trade filter with a surface-aware version |
| Fit residual outliers | Per-strike rich/cheap flags → strike selection input for 2.8 |
| Surface arbitrage violations | Data quality alarm first, opportunity second |
| Realized vs implied spread (per tenor) | Vol risk premium state → volatility breakout framework input (Extension v1.0) |

**Refresh cadence:** every 5 minutes during market hours (aligned with Microstructure Agent), full-day archive to MongoDB `options_data` for surface-history analytics. Response budget: 300ms per underlying fit (Rule 7 compliant — and it's off the execution path regardless).

**Consumers:** Intraday SMC+F&O Agent (richer no-trade filters, strike selection), expiry-day playbook (gamma + skew context), Black Swan detection (ATM spread trigger already exists; add skew-explosion trigger: 25Δ skew percentile > 98 intraday).

## 2.4 Order Flow Inference Layer — Grade F-A core / F-C ceiling

**Data perimeter, stated plainly:** KiteConnect provides tick LTP, cumulative volume, last-trade quantity, OI, and **5-level depth**. It does not provide full order book, order-level events, or trader categories. True order flow toxicity models (VPIN on order-level data, queue position) are F-C. What follows is the maximum honest extraction from the retail feed:

| Feature | Method | Grade |
|---------|--------|-------|
| Aggressor classification | Tick rule + quote rule hybrid (trade at/above ask = buyer-initiated) | F-A |
| Cumulative Volume Delta (CVD) | Running Σ(signed volume), per instrument, session-anchored | F-A |
| Order book imbalance | (ΣbidQty − ΣaskQty)/(Σboth) over 5 levels, EMA-smoothed; level-1 vs level-5 divergence | F-A |
| Large-print detection | Trade size > k·σ of rolling trade-size distribution → block flag | F-A |
| Absorption detection | High signed volume + price stasis at a level (iceberg/passive absorption footprint) | F-A |
| Sweep detection | Multi-level depth consumption within n ticks | F-A (5-level limited) |
| Price impact coefficient | Kyle-λ estimate: regression of Δprice on signed volume, rolling | F-A |
| Quote-fade / spoof flags | Depth appears and cancels without trades, repeatedly | F-B (depth snapshot frequency limits) |
| Full VPIN / queue models | Requires NSE TBT feed + colo | F-C — interface defined, implementation deferred with ADR |

**Output:** `flow_state` per tracked instrument every 1 minute: `{cvd_trend, imbalance, absorption_zones[], large_print_bias, lambda, flow_confidence}`. Feeds the Weighted Signal Engine under the existing Volume/VWAP row (15–20% regime weight — enriched input, frozen weight structure unchanged). Absorption zones feed SMC liquidity-pool confluence.

## 2.5 Smart Money Tracking Engine — Grade F-B

Composite of **public, disclosed** institutional and insider activity. Extends the FII/DII analytics from Extension v1.0 into a per-stock engine:

| Source | Signal extracted | Cadence |
|--------|------------------|---------|
| Bulk & block deal disclosures (NSE/BSE) | Named-entity accumulation/distribution; repeat-buyer detection across sessions | Daily |
| Delivery percentage | Delivery % z-score vs 60-day baseline; rising delivery + rising price = conviction buying | Daily |
| SAST disclosures (>5% holders, ±2% changes) | Stake-building footprints | Event-driven |
| PIT disclosures (promoter/insider trades —公开 filings) | Promoter buying clusters (historically one of the strongest Indian signals); pledging changes as risk flag | Event-driven |
| Quarterly shareholding patterns | FII/DII/MF holding deltas per stock | Quarterly |
| MF monthly portfolio disclosures | Aggregate fund accumulation breadth per stock | Monthly |
| FII derivatives positioning (Extension v1.0) | Index-level smart-money stance | Daily |

**Composite:** `smart_money_score ∈ [−1, +1]` per stock with **evidence list attached** (explainability rule applies to features, not just trades — a score with no cited disclosures is invalid, anti-pattern #14). Consumed by: Investment Alpha momentum factor (institutional accumulation component already in its 20% weight — this makes it rigorous), Swing agent confirmation, and the Earnings Momentum Engine (accumulation before results = informational prior).

## 2.6 Informed-Flow Anomaly Detection — Grade F-A/F-B
### (the "insider pattern detection" request, reframed)

**The reframe, stated explicitly:** Quantara trades exclusively on public data. This module does not seek or use material non-public information — doing so is illegal under SEBI PIT regulations. What it does is what exchange surveillance and institutional desks legitimately do: **detect the public footprints of potentially informed activity** and use them defensively and as event-anticipation context.

**Detectors (all on public market data):**

| Pattern | Definition |
|---------|-----------|
| Pre-event OI anomaly | OI buildup z > 3 in specific strikes within 5 days of a known event (results calendar), without proportional underlying move |
| IV firming without news | IV percentile rising > 20 points over 3 sessions, news feed silent (Haiku news cache as the "no news" check) |
| Volume–delivery spike | Volume z > 3 with delivery % z > 2, no disclosed reason |
| Directional options skew shift | Single-name skew inverting ahead of events |
| Price drift pre-announcement | Abnormal return (vs sector) accumulating in the 5 sessions before scheduled announcements |

**Uses — strictly two, both defensive/contextual:**
1. **Risk avoidance:** an active anomaly flag on an instrument raises the entry confidence threshold (+0.10) or blocks new positions in it (Layer 3 config) — don't be the liquidity for someone who knows something.
2. **Event-anticipation context:** anomaly flags feed the event-day playbook and the scenario engine as a "market may be pre-positioned" prior.

**It never:** generates standalone buy signals from anomaly flags alone, infers *what* the information is, or claims certainty. Flags carry the standard confidence + evidence contract.

## 2.7 Market Microstructure Modeling — Grade F-A (extension of existing agent)

The frozen Microstructure Agent keeps everything it has. Additions:

| Addition | Detail |
|----------|--------|
| Intraday liquidity profile | Per-instrument U-curve of spread/depth/volume by 15-min bucket, 20-day rolling — feeds execution scheduling (2.8) |
| Spread dynamics model | Spread regime per instrument (tight/normal/stressed) with transition alerts; stressed spread = execution size haircut |
| Trade-size distribution tracking | Retail vs block mix shift detection (distribution percentile drift) |
| Realized impact curves | From Quantara's own fills: realized slippage vs (order size / depth) — the only ground-truth impact data available at retail, and it's proprietary |
| Gamma profile integration | Existing dealer-gamma output cross-referenced with flow_state: long-gamma zone + absorption = mean-reversion microcontext; short-gamma + sweeps = expansion microcontext. Published as `micro_regime` |

## 2.8 Execution Optimization Layer — Grade F-A

Extends the frozen Execution Engine (which keeps its state machine, idempotency, and "never chase" doctrine). Three additions:

**Pre-trade cost model (runs inside guard check #10, making it rigorous):**
```
expected_cost = half_spread
             + impact(order_qty / visible_depth, λ from 2.4, liquidity bucket from 2.7)
             + timing_risk(volatility state, urgency)
Output: expected_slippage_bps + max_advisable_size for this instrument right now
```
If signal size > max_advisable_size → size down (never up) or slice.

**Order placement policy (computed decision, no AI, <100ms):**

| Condition | Tactic |
|-----------|--------|
| Urgency high (stop-out, black swan Phase 3C) | Marketable limit at touch + buffer; existing staggering rules apply |
| Normal entry, size ≤ depth at touch | Limit at LTP ± improvement (current frozen behavior) |
| Size > 3× depth at touch | Slice: child orders ≤ depth fraction, randomized 5–20s intervals, participation cap 10% of rolling volume, abandon-remainder rule if price drifts past tolerance (a partially-filled good entry beats a fully-filled bad one) |
| Options entry | Strike substitution: if target strike spread > 2% of mid (existing block), evaluate adjacent strike with better liquidity and ≥90% of the Greeks profile before rejecting the trade entirely |

**Post-trade TCA loop (Tier 4 food):**
Every fill writes implementation shortfall vs three benchmarks (decision price, arrival price, interval VWAP) into the explainability post-trade block (v1.1 fields: `slippage_bps`, `benchmark_deltas`, `tactic_used`). Weekly learning synthesis now includes execution quality; tactic parameters are learnable **within bounds** through the standard governance protocol. Realized slippage continuously recalibrates the pre-trade model — the loop closes.

---

# PART 3 — INTEGRATION MAP

```
                          ┌─────────────────────────────┐
  NEW DATA INGESTION      │   DATA VALIDITY ENGINE       │   (new staleness types:
  filings, deals, depth ─▶│   (all new data graded here) │    depth 2s, deals 24h,
                          └──────────┬──────────────────┘    filings event-driven)
                                     ▼
   ┌──────────────┬──────────────┬──────────────┬───────────────┐
   │ Vol Surface  │ Order Flow   │ Smart Money  │ Arb Monitors  │   5-min / 1-min /
   │ (2.3)        │ (2.4)        │ (2.5)        │ (2.1)         │   daily cadences
   └──────┬───────┴──────┬───────┴──────┬───────┴──────┬────────┘
          ▼              ▼              ▼              ▼
   ┌──────────────────────────────────────────────────────────┐
   │ Microstructure Agent (extended, 2.7) → micro_regime       │
   │ Informed-Flow Anomaly Detector (2.6) → anomaly flags      │
   └──────────────────────┬───────────────────────────────────┘
                          ▼
   Weighted Signal Engine (frozen weights; richer inputs)
   Stat-Arb Strategy Module (2.2) ──┐ (standard strategy interface)
                          ▼         ▼
   Probability Engine → Pre-Submission Guard (13 checks, #10 upgraded)
                          ▼
   Execution Engine + Optimization Layer (2.8)
                          ▼
   Zerodha — single path, unchanged
```

Anomaly flags (2.6) additionally publish to `quantara:stream:alerts` and raise per-instrument thresholds in Layer-3 config. Nothing publishes orders directly.

---

# PART 4 — API ADDITIONS

```
GET /api/v1/vol/surface/{underlying}          fitted surface + analytics
GET /api/v1/vol/skew-history/{underlying}     skew/butterfly percentiles
GET /api/v1/flow/{instrument}                 flow_state (CVD, imbalance, λ)
GET /api/v1/micro/{instrument}                micro_regime + liquidity profile
GET /api/v1/arb/dislocations                  current cross-asset dislocations
GET /api/v1/smartmoney/{symbol}               composite score + evidence list
GET /api/v1/anomalies                         active informed-flow flags
GET /api/v1/statarb/pairs                     validated pairs + live z-scores
GET /api/v1/execution/tca                     TCA summaries per period/tactic
GET /api/v1/execution/pretrade-estimate       POST {instrument, qty} → cost est
```

All read-only on production. Stat-arb pair validation runs in the Research Lab service.

---

# PART 5 — ROADMAP PLACEMENT & SEQUENCING

Ordered by (alpha per engineering hour × data availability), respecting frozen phases:

| Order | Module | Phase home | Why this order |
|-------|--------|-----------|----------------|
| 1 | Execution Optimization (2.8) | Phase 2 tail / Phase 3 | Improves every strategy's realized edge; uses only existing data; TCA data compounds from day one |
| 2 | Vol Surface (2.3) | Phase 3 | Direct upgrade to the F&O desk's core filters; chain data already flowing |
| 3 | Order Flow (2.4) + Micro extensions (2.7) | Phase 3 | Same tick/depth feed, shared infrastructure |
| 4 | Smart Money (2.5) + Anomaly Detection (2.6) | Phase 4 | Needs filings ingestion (new data work); pairs naturally with Investment Book build |
| 5 | Cross-Asset Arb monitors (2.1) | Phase 4 | Mostly signal value; low urgency |
| 6 | Stat Arb (2.2) | Phase 4–5, lab-gated | Highest validation burden; do not rush a strategy that needs 2 legs and a cointegration thesis |

**Defer-with-ADR list (F-C):** NSE tick-by-tick feed integration, colocation execution, full VPIN — each gets an ADR with a trigger condition (e.g., "capital > ₹2 Cr in intraday book AND realized slippage > X bps justifies TBT feed cost").

---

# PART 6 — NEW OPEN QUESTIONS

1. Depth snapshot frequency achievable from KiteConnect WebSocket under current subscription limits — empirical test needed before committing to imbalance feature cadence.
2. Filings ingestion source for SAST/PIT/bulk deals: scrape exchange pages (fragile) or vendor feed (cost)? Affects Smart Money data grading.
3. SVI fit failure policy on illiquid weekly strikes: fall back to simple polynomial smile, or mark surface PARTIAL and suppress derived analytics for that expiry? (Proposal: PARTIAL flag, consistent with chain-coverage rule.)
4. Stat-arb sleeve capital cap at activation: proposal 5% of Swing book, expandable via capital-graduation logic.
5. Anomaly-flag threshold action default: +0.10 confidence requirement or full block? (Proposal: +0.10 default, full block on instruments within 48h of scheduled results.)
6. Does the paired-order execution mode (stat arb) need its own failure-mode analysis appended to the five Zerodha failure modes? (Almost certainly yes — leg-out risk is failure mode F.)

---

*Extension v1.1 — additive. Frozen decisions untouched. World-class means honest about the data perimeter, gated by validation, and slippage-aware before it is alpha-hungry.*
