# QUANTARA OS — INSTITUTIONAL INTELLIGENCE EXTENSION
## Extension Architecture v1.0 (companion to QUANTARA_OS_MASTER.md v3.1)

**Status:** Proposal — requires architectural review before adoption (per frozen doc closing rule)
**Scope discipline:** Nothing here modifies Tier 0, the kill switch hierarchy, the database split, monetary integer rule, the 14 engineering rules, or the 12 anti-patterns. All new modules attach to Tiers 2, 3, and 4, or run as offline tooling.
**Naming:** "Quantara OS" remains the trading system. This extension adds the institutional CIO intelligence the new brief requests.

---

# PART 1 — RECONCILIATION MATRIX

Every module requested in the institutional brief, mapped against the frozen architecture. Three verdicts: **COVERED** (frozen, do not redesign), **PARTIAL** (exists, needs extension), **NEW** (architected in this document).

## 1.1 Market Regime Engine

| Requested | Verdict | Frozen location / gap |
|-----------|---------|----------------------|
| Regime detection (trend/vol/breadth) | COVERED | Tier 1 Context/Regime Engine — 5-min updates, STALE protection |
| Liquidity cycle detector | **NEW** | No system-level liquidity cycle model exists |
| RBI policy interpretation | **NEW** | Event flag exists; no policy analysis module |
| Inflation & rate sensitivity modeling | **NEW** | Not present |
| USDINR & global risk integration | PARTIAL | Pre-market package collects USDINR/global at 8:30 AM; no continuous signal model |
| FII/DII flow tracker | PARTIAL | Collected pre-market; no flow analytics, trend scoring, or divergence detection |

## 1.2 Equity Intelligence Engine

| Requested | Verdict | Frozen location / gap |
|-----------|---------|----------------------|
| Balance sheet strength ranking | COVERED | Investment Alpha Agent quality factor (ROE, ROCE, D/E, interest coverage) |
| Earnings momentum detection | PARTIAL | Momentum factor includes earnings revision; no standalone surprise/revision-breadth engine |
| Sector rotation scoring | PARTIAL | Sector strength ranked daily at 8:50; no rotation *transition* model |
| Valuation dispersion analysis | **NEW** | Per-stock value factor exists; cross-sectional dispersion does not |
| Relative strength model | COVERED | Momentum factor + swing sector-strength requirement |

## 1.3 Derivatives & Positioning Engine

| Requested | Verdict | Frozen location / gap |
|-----------|---------|----------------------|
| OI analysis, max pain, gamma positioning | COVERED | Market Microstructure Agent — dealer gamma by strike, flip level, walls, pools, OI anomalies |
| PCR & volatility regime | COVERED | Regime engine (VIX state) + microstructure |
| Institutional positioning inference | PARTIAL | OI-based inference exists; FII derivatives data (index futures/options long-short) not integrated |

## 1.4 Capital Allocation Engine

| Requested | Verdict | Frozen location / gap |
|-----------|---------|----------------------|
| Drawdown containment | COVERED | Tier 0 drawdown-adjusted sizing table (1.00x → 0.00x), capital preservation mode |
| Conviction-weighted allocation | COVERED | Confidence-based sizing (0.82 threshold for max size) |
| Kelly-adjusted position sizing | **NEW** | Current sizing is threshold-banded, not Kelly-derived |
| Risk parity overlay | **NEW** | Book allocation is range-based (40–60% etc.), not risk-balanced |

## 1.5 Risk Management Layer

| Requested | Verdict | Frozen location / gap |
|-----------|---------|----------------------|
| Correlation breakdown monitor | COVERED | Adaptive Correlation Engine (3 windows, regime-blended, crisis thresholds) |
| Stop-loss discipline framework | COVERED | Tier 0 + SL verification (failure mode D) + position aging |
| Black swan handling | COVERED | Black Swan Protocol (3 phases) |
| Portfolio VaR modeling | **NEW** | No VaR computation exists |
| Tail risk simulation (Monte Carlo) | **NEW** | Black swan sim test exists for Phase-1 gating; no ongoing portfolio MC |
| Liquidity stress modeling | **NEW** | Per-trade liquidity checks exist (check #9); portfolio-level liquidation cost does not |

## 1.6 Strategy Research Lab

| Requested | Verdict | Frozen location / gap |
|-----------|---------|----------------------|
| Backtest framework | PARTIAL | vectorbt chosen in stack; no formal lab structure, no walk-forward protocol doc |
| Regime-based strategy switching | COVERED | Regime-adaptive signal weights table |
| Factor model testing | **NEW** | Not present |
| Alpha decay monitor | **NEW** | Anti-drift protections exist (paralysis spiral, directional bias) but not per-strategy alpha decay curves |

## 1.7 Institutional Reporting Engine

| Requested | Verdict | Frozen location / gap |
|-----------|---------|----------------------|
| CIO daily note | COVERED | Tier 3 Claude routing: CIO daily briefing (Haiku, 24h cache) |
| Trade thesis documentation | COVERED | Explainability contract (Rule 13) is stronger than the brief's ask |
| Confidence scoring | COVERED | Numeric confidence (superior to High/Med/Low — do not regress to labels) |
| Weekly macro brief | **NEW** | Weekly learning synthesis exists; macro brief does not |
| Sector heatmap | PARTIAL | Sector ranking computed; no rendered heatmap artifact |
| Risk disclosure section | **NEW** | Add as a templated section in all reports |

**The 12-field trade idea output format requested in the brief is already exceeded by the frozen explainability contract.** Mapping: thesis → `why_trade`; macro alignment → `regime_context`; positioning → microstructure inputs in `confidence_breakdown`; entry/SL/targets → order spec; RR → enforced floor 2.0; probability → `confidence`; invalidation → `counter_argument` + scenario bear case; allocation % → sizing engine output. One genuine addition: an explicit `invalidation_condition` field (price/structure level that kills the thesis) should be added to explainability v1.1 — currently implicit in SL, but thesis invalidation ≠ stop loss.

---

# PART 2 — EXTENSION ARCHITECTURE (NEW MODULES ONLY)

```
                    EXISTING (FROZEN)                      NEW (THIS DOC)
┌─────────────────────────────────────────┐   ┌────────────────────────────────┐
│ TIER 0 — Survivability      [UNTOUCHED] │   │                                │
├─────────────────────────────────────────┤   │  MACRO INTELLIGENCE ENGINE     │
│ TIER 1 — Alpha Generation               │◀──│  · Liquidity Cycle Detector    │
│   Regime Engine ◀───── macro_state feed │   │  · RBI Policy Interpreter      │
│   Weighted Signals (macro weight row    │   │  · Rate Sensitivity Model      │
│   already exists — richer input only)   │   │  · FII/DII Flow Analytics      │
├─────────────────────────────────────────┤   │  · Global Risk Composite       │
│ TIER 2 — CIO Allocation                 │◀──│                                │
│   Portfolio State Mgr ◀── VaR, Kelly,   │   │  PORTFOLIO ANALYTICS ENGINE    │
│   Investment Alpha     risk parity      │   │  · Portfolio VaR (3 methods)   │
│   Correlation Engine ◀── tail sim       │   │  · Tail Risk Monte Carlo       │
├─────────────────────────────────────────┤   │  · Liquidity Stress Model      │
│ TIER 3 — AI Intelligence                │◀──│  · Kelly / Risk Parity Overlay │
│   Pre-market package ◀── macro brief,   │   │                                │
│   Claude routing       sector heatmap,  │   │  EQUITY INTELLIGENCE EXT.      │
│   (new rows, same      reports          │   │  · Earnings Momentum Engine    │
│    batching/cache                       │   │  · Sector Rotation Transition  │
│    protocols)                           │   │  · Valuation Dispersion        │
├─────────────────────────────────────────┤   │                                │
│ TIER 4 — Learning                       │◀──│  STRATEGY RESEARCH LAB         │
│   Governance protocol  ◀── alpha decay, │   │  (OFFLINE — separate process,  │
│   (unchanged: recs         factor tests │   │   never touches live system;   │
│    only, human approve)    feed recs    │   │   reads replicas only)         │
└─────────────────────────────────────────┘   └────────────────────────────────┘
```

**Placement rule:** all new engines are Tier 2/3-class — pre-computed, cached, non-blocking. None sits on the execution path. Engineering Rule 6 extends naturally: *no new module is ever on the critical path for intraday execution.*

## 2.1 Macro Intelligence Engine (Tier 3-class, runs 24/7 off-hours + pre-market)

### Liquidity Cycle Detector

Composite of weekly-updated inputs, each normalized to a 10-year z-score:

| Input | Source | Weight |
|-------|--------|--------|
| RBI system liquidity (LAF net position) | RBI DBIE | 0.25 |
| M3 growth vs trend | RBI | 0.15 |
| Credit growth vs deposit growth spread | RBI | 0.15 |
| G-sec 10Y yield trend + curve slope (10Y–1Y) | CCIL/NSE | 0.15 |
| FII net flows (20-day cumulative, equity + debt) | NSDL | 0.20 |
| USDINR trend + RBI intervention proxy (reserves delta) | RBI | 0.10 |

Output state machine: `EXPANSION → PEAK → CONTRACTION → TROUGH` with confidence and a regime-change probability. Feeds the Regime Engine as one additional input (the macro/breadth signal row already carries 0.10–0.25 weight — this enriches it without changing the frozen weights table).

### RBI Policy Interpreter

- Calendar-driven: MPC meeting dates pre-loaded yearly (event flag already exists for these days).
- Post-announcement pipeline: statement text → Haiku batch extraction (stance shift, vote split, inflation/GDP projection changes, liquidity guidance) → computed scoring vs previous statement → `policy_delta` object cached 30 days.
- Pre-meeting: scenario engine generates 3 outcomes (hold/hike/cut × stance) with playbooks — the existing event-day playbook pattern, specialized.

### Rate Sensitivity Model

Per portfolio holding: empirical beta to 10Y yield moves (rolling 250-day regression, computed, no AI). Aggregated to a portfolio rate-DV01 analog. Surfaces: "a 25bps repo surprise propagates to portfolio P&L of approximately X" — feeding the stress library (2.2).

### FII/DII Flow Analytics

Daily NSDL/exchange data: 5/20/60-day cumulative flows, flow z-scores, equity vs derivatives divergence (FII index futures long-short ratio vs cash flows — the institutional positioning inference the brief requests), and flow-vs-price divergence flags (price up on FII selling = DII-supported rally, fragility note). Cached daily; consumed by pre-market package at 8:30 AM slot (already scheduled — this deepens what that slot produces).

### Global Risk Composite

Continuous (overnight-updated) composite: US 10Y, DXY, Brent, SGX/GIFT Nifty gap, US VIX, Asia session breadth. Output: `global_risk_state ∈ {supportive, neutral, hostile}` + gap-day probability estimate feeding the existing gap-day playbook selection.

## 2.2 Portfolio Analytics Engine (Tier 2-class, post-market batch + on-demand)

### Portfolio VaR (three methods, computed nightly)

| Method | Use |
|--------|-----|
| Parametric (variance-covariance, using the Adaptive Correlation Engine's regime-blended matrix — reuse, don't recompute) | Fast daily headline |
| Historical simulation (500-day window, including 2020/2022 stress periods already curated for stress correlations) | Fat-tail honesty |
| Monte Carlo (correlated draws via Cholesky on the regime-blended matrix, 50k paths) | Tail risk + option nonlinearity via full reval on strike grid |

Outputs: 1-day and 5-day VaR at 95/99, Expected Shortfall (ES99 is the binding metric — VaR alone understates tails), per-book and per-factor attribution. **Display only + alerting; the Tier 0 hard limits remain the supreme authority — VaR informs the human and the CIO layer, it does not gate orders.** If nightly ES99 exceeds a configured fraction of the daily loss limit, raise a WARNING alert recommending size reduction next session.

### Tail Risk / Black Swan Stress Library

Extends the black swan *simulation test* (Phase 1 gate) into a standing nightly battery:

| Scenario | Shock definition |
|----------|------------------|
| RBI surprise hike | +50bps repo, +8 VIX, banking −3%, rate-sensitivity propagation via 2.1 model |
| Geopolitical event | NIFTY gap −4%, VIX +60%, INR −1.5%, spreads ×3 |
| Global risk-off | DXY +2%, FII outflow 3σ, IT/metals −4% |
| Budget shock | Sector-specific ±5% (capital goods, PSU, consumption) |
| Election surprise | Gap ±5%, VIX 30+, circuit proximity logic |
| Liquidity freeze | Spreads ×5, fill assumption 50% at touch |

Each run answers: P&L impact, margin utilization after shock (settlement-aware margin model reused), which kill-switch level would trigger, and time-to-flatten estimate under stressed liquidity. Report attached to pre-market package.

### Liquidity Stress Model

Per position: participation-rate model (max 10% of ADV per session) → days-to-liquidate; stressed variant at 3× spread and 50% volume. Portfolio metric: % liquidatable in 1 session without exceeding impact budget. Alert if < 70% (configurable Layer 3).

### Kelly / Risk Parity Allocation Overlay

Two computed advisories layered on top of (never replacing) frozen sizing:

- **Fractional Kelly:** per setup-type, using realized win rate and payoff from the explainability post-trade writebacks (the data already exists). Quarter-Kelly cap. Output is a *suggested size multiplier within the existing drawdown-adjusted band* — and it can only reduce, never exceed, the Tier 0-permitted size.
- **Risk parity (book level):** computes risk contribution per book from the correlation engine; flags when the Intraday/F&O book consumes risk disproportionate to its 10–30% capital range. Advisory to the human; capital range targets are frozen and learning cannot touch them (already enforced).

## 2.3 Equity Intelligence Extensions (Tier 2-class, daily batch)

| Module | Design |
|--------|--------|
| Earnings Momentum Engine | Per stock: standardized earnings surprise (SUE), revision breadth (analyst up/down ratio where available, else guidance-delta from concall Haiku extractions — already cached 24h), post-earnings drift window flag. Feeds the Investment Alpha momentum factor (within its frozen 20% weight) and the swing agent's no-earnings-in-hold-period check |
| Sector Rotation Transition Detector | Daily sector RS ranks already computed at 8:50. New: rank-velocity (Δrank over 5/20 days), leadership persistence score, and a transition alert when a top-3 sector's rank velocity turns negative for 5 consecutive days while a bottom-half sector posts +3 rank improvement — the "sector leadership transition detection" feature, computed, zero AI |
| Valuation Dispersion Analyzer | Cross-sectional: sector PE/PB z-score dispersion; intra-sector spread between cheapest and richest quintile. High dispersion + improving sector phase = stock-picker regime flag for the Investment Alpha Agent; compressed dispersion = beta regime, favor index instruments |

## 2.4 Strategy Research Lab (OFFLINE — hard isolation)

Separate repo/process. Reads from a nightly PostgreSQL replica + MongoDB export. **Zero write access to any production database. Zero imports from production code except shared Pydantic contracts.** The lab is to strategy what the Emergency Flatten Service is to execution: isolated by construction.

Components:

1. **Backtest framework** — vectorbt (frozen stack choice) wrapped with: mandatory walk-forward protocol (train/validate/test splits, no full-sample optimization), realistic cost model (Zerodha brokerage + STT + impact estimate from the liquidity model), and regime-tagged results (performance reported per regime, never blended — anti-pattern #4 applied to research).
2. **Factor model testing** — Investment Alpha factor weights (30/25/25/20) tested via cross-sectional regressions; decile spread analysis; results become *learning recommendations*, entering production only through the frozen Tier 4 governance protocol (shadow mode → human approval → 5-day staging).
3. **Alpha decay monitor** — per strategy/setup-type: rolling 60-trade Sharpe, hit rate, and profit factor with CUSUM change-point detection. Decay flag → recommendation to reduce that setup's weight (within the ±20% learning bound). Complements existing paralysis-spiral and directional-bias detectors.
4. **Regime strategy matrix maintenance** — periodic re-validation that the frozen regime-weight table still ranks correctly; proposed adjustments flow through governance, bounded ±20%.

## 2.5 Institutional Reporting Engine (Tier 3-class)

Adds rows to the existing Claude routing table — same batching, cache-before-call, and Haiku-default protocols:

| Report | Model | Schedule | Cache |
|--------|-------|----------|-------|
| Weekly macro brief (liquidity cycle, flows, RBI stance, global composite) | Haiku | Sunday 18:00 | 7 days |
| Sector heatmap narrative (rendered grid is computed; Haiku writes 5-line commentary) | Haiku | Daily 8:52 | 24h |
| Monthly CIO letter (performance attribution, calibration review, regime recap) | Sonnet | Month-end | Permanent |
| Stress test summary | Haiku | Daily post-batch | 24h |

Every report template ends with a standing **Risk Disclosure** section (system limitations, data staleness states at generation time, active governance flags) — generated from system state, not boilerplate. Narrative engines may only cite fields present in the underlying computed objects (no new claims in prose).

---

# PART 3 — DATA FLOW (EXTENSION OVERLAY)

```
NIGHT (post-market)
  exchange/NSDL/RBI data pulls → Data Validity Engine (staleness types added:
  flows 24h, macro series 7d, RBI series per-release)
    → FII/DII analytics → MongoDB intelligence_feed
    → VaR batch (parametric + historical + MC) → MongoDB learning_metrics
    → Stress library run → report cache
    → Equity intelligence batch (earnings momentum, dispersion, rotation)
    → Liquidity cycle weekly update (Sundays)

8:30–9:10 PRE-MARKET (existing schedule, enriched — no new time slots)
  8:30 macro collection now includes: liquidity cycle state, flow analytics,
       global risk composite, rate-sensitivity snapshot
  8:50 sector ranking now also emits rotation-transition flags + heatmap
  8:55 regime preliminary assessment consumes macro_state (richer input,
       same output contract)
  9:10 package READY — now includes stress summary + VaR headline

INTRADAY
  No new intraday consumers. Extension modules are read-only context.
  (Engineering Rule 6 preserved: nothing new on the execution path.)

WEEKLY / RESEARCH
  Replica snapshot → Research Lab → recommendations → Tier 4 governance
  → human approval → staging → production (frozen protocol, unchanged)
```

---

# PART 4 — API STRUCTURE DRAFT (ADDITIVE ENDPOINTS)

```
GET  /api/v1/macro/liquidity-cycle           current state + history
GET  /api/v1/macro/flows                     FII/DII analytics
GET  /api/v1/macro/rbi/latest                policy_delta object
GET  /api/v1/macro/global-risk               composite state
GET  /api/v1/portfolio/var                   latest VaR/ES + attribution
GET  /api/v1/portfolio/stress                stress library results
GET  /api/v1/portfolio/liquidity             liquidation profile
GET  /api/v1/allocation/kelly                advisory multipliers per setup
GET  /api/v1/allocation/risk-parity          book risk contributions
GET  /api/v1/equity/rotation                 sector transition flags
GET  /api/v1/equity/dispersion               valuation dispersion state
GET  /api/v1/equity/earnings-momentum/{sym}  SUE / revision data
GET  /api/v1/reports/{type}/{date}           rendered reports
POST /api/v1/research/backtest               lab-only (separate service/auth)
GET  /api/v1/research/alpha-decay            decay monitor states
```

All read-only on the production service except research endpoints, which live on the lab service with separate credentials. No new mutating endpoints touch trading state.

---

# PART 5 — ROADMAP ALIGNMENT (NOT A NEW ROADMAP)

The frozen build phases stand. Extension modules slot in where their dependencies exist:

| Frozen Phase | Extension work added |
|--------------|---------------------|
| Phase 2 (Tier 1 pipeline, 40 paper days) | None — do not dilute the paper-trading gate |
| Phase 3 (Tier 2+3 Intelligence) | Macro Intelligence Engine, FII/DII analytics, reporting rows (natural fit: this phase already builds the pre-market package consumers) |
| Phase 4 (Investment Book + Learning) | Equity Intelligence extensions, Kelly/risk-parity advisories, Research Lab v1 (factor tests, alpha decay) |
| Phase 5 (Observability + Dashboard) | VaR/stress dashboards, sector heatmap UI, report archive |

v1→v5 institutional platform framing maps to: v1 = Phases 1–2 (survivable trading), v2 = Phase 3 (+macro intelligence), v3 = Phase 4 (+research lab and full CIO analytics), v4 = Phase 5 (+institutional reporting surface), v5 = multi-agent operation (Part 6) — gated, as everything is, by the capital graduation protocol.

---

# PART 6 — MULTI-AGENT UPGRADE PATH

The frozen architecture is already implicitly multi-agent (Intraday SMC+F&O Agent, Swing Alpha Agent, Investment Alpha Agent, Microstructure Agent). The upgrade path formalizes coordination without violating anti-pattern #9 (no shared mutable state) or #7 (no god orchestrator):

| Stage | Addition | Constraint |
|-------|----------|-----------|
| M1 | Macro Strategist agent (owns Macro Intelligence outputs) + Risk Officer agent (owns VaR/stress narration) | Both publish to streams/cache only; no order authority |
| M2 | CIO Debate protocol: before Investment INITIATE decisions, structured Sonnet debate — Alpha agent thesis vs Risk Officer counter vs Macro context — three cached artifacts, computed reconciliation, human-visible | Uses existing "conflicting signal reasoning" Sonnet routing row; conflicts surfaced, never averaged |
| M3 | Agent scorecards: per-agent calibration (Brier) computed from explainability writebacks; chronically miscalibrated agent → weight-reduction recommendation via Tier 4 governance | Learning bounds (±20%) apply |
| M4 | Capability-token execution agents (post Stage-2 capital graduation) | Tier 0 + pre-submission guard remain the only path to the broker |

Communication remains database/stream-mediated. Agents never call each other directly.

---

# PART 7 — INSTITUTIONAL COMPLIANCE FRAMEWORK

Current legal posture: an individual trading proprietary capital through a registered broker. The compliance framework has two horizons:

**Horizon 1 — proprietary operation (now):**
- Complete audit trail (already frozen: append-only, written before action) — retain ≥ 8 years
- Order/trade records reconcilable against broker contract notes (reconciliation engine already does the position side; add monthly contract-note checksum job)
- Algo trading via broker APIs: stay within Zerodha/exchange API terms; SEBI's retail algo framework (exchange-approved algos via brokers) is evolving — track circulars; the kill-switch + audit design positions the system well for any registration regime
- Tax discipline: F&O = business income; the audit trail should emit a yearly P&L export suitable for ITR-3 filing

**Horizon 2 — if Quantara ever serves others (signals, capital, or SaaS):**
- Selling research/signals to Indian clients → SEBI Research Analyst (RA) registration territory
- Advising individuals → Investment Adviser (RIA) regulations
- Managing third-party capital → PMS license (₹5 Cr net-worth requirement) or AIF route
- A signals SaaS (the Quantara Signals product line) must be structured carefully against the RA boundary — generic tools vs personalized recommendations is the operative distinction

This section is a planning framework, not legal advice — a securities lawyer should review before any client-facing launch.

**System-level compliance controls (build now, cheap):** immutable report archive, model-change log (governance protocol already produces this), data-source license registry, and a kill-switch activation register (exists: `kill_switch_log`).

---

# PART 8 — BACKTESTING INTEGRATION PLAN

1. **Data foundation:** nightly replica of PostgreSQL + MongoDB market_data/options_data export to the lab environment. Historical 1-min data via Kite historical API (the NiftyBot backtester rebuild pattern reuses directly).
2. **Contract sharing:** lab imports only the Pydantic signal/order/explainability contracts — strategies under test produce the same explainability objects as production, so backtest results and live results are directly comparable rows in the same analytical schema.
3. **Cost realism:** brokerage + STT + stamp + SEBI charges + slippage model calibrated from actual fill data (production fills vs LTP-at-signal already capturable from order records).
4. **Walk-forward protocol (mandatory):** rolling 6-month train / 1-month test; report distribution of out-of-sample results, never the best run. Regime-tagged reporting per the regime engine's historical states.
5. **Promotion path:** lab result → learning recommendation → human approval → shadow mode 5 trading days → staged production. Identical to the frozen Tier 4 protocol — research has no privileged path to production.
6. **Statistical gates:** any "ready" claim requires the same rigor as the capital graduation protocol — minimum sample sizes, significance tests on win rate vs random, and Brier calibration on predicted confidences. "It looks good" is not a gate (frozen doc, Part 7, verbatim spirit).

---

# PART 9 — OPEN QUESTIONS ADDED BY THIS EXTENSION

1. FII/DII and derivatives positioning data source: scrape NSDL/exchange dailies, or paid vendor? (Affects data validity grading.)
2. Fundamental data source for the Equity Intelligence extensions: screener-class API, exchange filings parsing, or vendor? Quality factor inputs need a graded source.
3. VaR alerting threshold: what fraction of the daily loss limit should nightly ES99 trigger a WARNING at? (Proposal: 80%.)
4. Should the stress library run pre-market (adds time pressure to the 8:30–9:10 window) or remain nightly-only? (Proposal: nightly, with pre-market consuming cached results.)
5. Kelly advisory visibility: dashboard-only, or annotated on each signal's explainability block? (Proposal: explainability v1.1 field `kelly_advisory`, display-only.)
6. Research Lab compute: same VPS (risk: resource contention with live system) or separate box? (Proposal: separate — Tier 0 isolation philosophy.)

---

*Extension v1.0 — additive to QUANTARA_OS_MASTER.md v3.1. No frozen decision is modified.*
*Adoption requires explicit architectural review per the master document's change rule.*
