# Quantara OS — Implementation Roadmap

**Version:** 3.1 (aligned with QUANTARA_OS_MASTER.md)  
**Status:** Architecture frozen. This roadmap reflects the build sequence for the frozen design.  
**Capital target:** ₹5 crore autonomous operation across three books.

---

## Capital Graduation Protocol

| Stage | Capital | Books Active | Max Positions | Gate Criteria |
|---|---|---|---|---|
| **0 — Paper** | ₹0 | All (simulated) | Unlimited | 40 trading days, ≥60% intraday win rate, no system errors 5 consecutive days, reconciliation + kill switches verified |
| **1 — Minimum** | ₹2–5L | Intraday F&O only | 1 | 4 weeks, drawdown <10%, no system errors, emergency flatten tested |
| **2 — Expanded** | ₹10–25L | Intraday + Swing | 3 max | 8 weeks, Sharpe >1.0, drawdown <15%, correlation engine tested |
| **3 — Multi-crore** | ₹5 Cr | All three books | Per book limits | Continuous monitoring, learning governance active |

**Paper trading minimum is 40 trading days with statistical significance testing — not "it looks good."**

---

## Build Phases

### Phase 1 — Tier 0 Survivability Foundation
**Capital:** Paper only  
**Goal:** A system that cannot lose money due to software failure

**Components to build:**
- [ ] PostgreSQL schema: `capital_accounts`, `positions`, `orders`, `order_state_transitions`, `risk_state`, `strategy_states`, `strategy_parameters`, `learning_recommendations`, `reconciliation_log`, `system_checkpoints`, `audit_trail`, `alert_log`, `kill_switch_log`
- [ ] MongoDB schema: `market_data`, `options_data`, `microstructure_analysis`, `signals`, `intelligence_feed`, `premarket_packages`, `learning_metrics`, `ai_cache`, `system_logs`
- [ ] Zerodha Session Manager (state machine, heartbeat, 5 failure modes, reconnect backoff)
- [ ] Position Reconciliation Engine (cold start, warm start, continuous, post-execution)
- [ ] Order Idempotency Engine (key generation, PostgreSQL-first, near-duplicate suppression)
- [ ] Market Data Validity Engine (OHLC, tick, options chain, circuit breaker, timezone)
- [ ] Tier 0 Risk Engine (8 hard limit checks, kill switch Level 1/2, drawdown-adjusted sizing)
- [ ] 3-Level Kill Switch (state machine, reset codes, cascade triggers)
- [ ] Black Swan Protocol (6 triggers, 3 phases, stop-widening, human response window)
- [ ] Capital Preservation Mode
- [ ] Settlement-Aware Margin Model (paise arithmetic only)
- [ ] Emergency Flatten Service (standalone process, port 8001, zero backend imports)
- [ ] 4-Level Alert System (Telegram + Twilio voice for Level 2+)
- [ ] Health endpoints: `/api/v1/health`, `/api/v1/health/ready`, `/api/v1/health/detailed`
- [ ] System checkpoints written every 5 minutes
- [ ] systemd service files (backend + flatten, with correct dependency order)
- [ ] UptimeRobot external monitoring config

**Phase 1 Definition of Done (ALL required before Phase 2):**
- [ ] All unit tests passing (validity_engine: 95%+, kill_switches: 95%+)
- [ ] Integration tests: all 5 Zerodha failure modes handled correctly
- [ ] Emergency flatten: tested independently with main backend stopped
- [ ] 72-hour continuous run on VPS: zero unhandled exceptions, zero silent failures
- [ ] Kill switch cascade: Level 1 → 2 → 3 correct behavior verified
- [ ] Black swan simulation test passes
- [ ] Reconciliation: handles clean state, discrepancy, warm start correctly
- [ ] CRITICAL alert unacknowledged → escalation fires correctly
- [ ] Health endpoint correctly reflects component failures
- [ ] All 12 anti-patterns verified absent via code review
- [ ] Runbooks written: emergency flatten, token refresh failure, reconciliation discrepancy, warm start
- [ ] VPS backup scripts tested and verified (pg_dump + mongodump to S3)

---

### Phase 2 — Tier 1 Core Trading Pipeline (Intraday)
**Capital:** Paper → Stage 1 (₹2–5L, intraday only)  
**Gate:** Phase 1 Definition of Done completely satisfied

**Components to build:**
- [ ] Context/Regime Engine (ADX, ATR, A/D ratio, VWAP, VIX, regime output)
- [ ] Intraday SMC+F&O Agent (upgrade from existing OPA/PES/SFR pipeline to new architecture)
- [ ] Market Microstructure Agent (GEX, max pain, OI dynamics, liquidity pools)
- [ ] 13-Check Pre-Submission Guard (complete all 13 checks)
- [ ] Weighted Signal Engine (regime-adaptive weights table)
- [ ] Probability Engine (confidence scoring with all adjustments)
- [ ] Pre-Market Scenario Engine (Haiku batch: 3–5 intraday scenarios, cached by 9:10 AM)
- [ ] Execution Engine (order submission flow, limit order management, fill monitoring)
- [ ] Rule 13 Explainability Block (all fields populated by the correct component)
- [ ] Pre-market Intelligence Package schedule (8:30–9:10 AM)
- [ ] Paper trading runner (full pipeline, paper fills, P&L tracking)
- [ ] Intraday position management (trail stop, time stop, EOD square-off at 15:25)
- [ ] Learning metrics collection (signal quality, win rate, regime performance)

**Phase 2 Definition of Done:**
- [ ] 40 paper trading days completed
- [ ] Brier score computed for confidence calibration
- [ ] Black swan simulation passes with live intraday positions
- [ ] Claude unavailability scenario tested (pre-cached scenarios still work)
- [ ] Pre-market package 100% reliable (completes before 9:10 AM every day)
- [ ] All 13 pre-submission checks tested with failure injections

---

### Phase 3 — Tier 2 + Tier 3 Intelligence
**Capital:** Stage 1 → Stage 2 (₹10–25L, add Swing book)  
**Gate:** Phase 2 Definition of Done + Stage 1 capital criteria met

**Components to build:**
- [ ] Swing Alpha Agent (overnight screener, pre-market batch debate, entry/exit management)
- [ ] Portfolio State Manager (3-book capital accounting, sector concentration, correlation)
- [ ] Adaptive Correlation Engine (3 lookback windows, regime-blended)
- [ ] Sector Ranking Engine (3× daily updates, outperformance vs NIFTY)
- [ ] Intelligence/News Agent (news batch, Haiku summarization, event calendar)
- [ ] Enhanced pre-market package (swing setups, sector rankings, macro events)
- [ ] Cross-book risk governor (correlated loss detection, sector concentration)
- [ ] Capital allocation rebalancing signals

**Phase 3 Definition of Done:**
- [ ] Swing book paper trading: 20 days minimum before live
- [ ] Portfolio concentration limits tested with scenarios (3× sector concentration)
- [ ] Correlation engine tested across market regimes
- [ ] Full pre-market package tested for all components completing before 9:10 AM

---

### Phase 4 — Investment Book + Learning Governance
**Capital:** Stage 2 → Stage 3 (₹5 Cr target, all books)  
**Gate:** Phase 3 Definition of Done + Stage 2 criteria met

**Components to build:**
- [ ] Investment Alpha Agent (stock scoring, Sonnet thesis generation, hold management)
- [ ] Investment screening pipeline (fundamental data ingestion, scoring model)
- [ ] Thesis break detection (automated fundamental monitoring)
- [ ] Learning Agent (weekly analysis, parameter recommendations, shadow mode testing)
- [ ] Learning governance workflow (human review → staging → production promotion)
- [ ] Anti-drift protections (regime balance check, directional bias detection, paralysis spiral)
- [ ] Learning service DB permissions (write access only to `learning_recommendations`)
- [ ] Weekly learning synthesis (Sonnet postmortem batches)

**Phase 4 Definition of Done:**
- [ ] Learning governance workflow end-to-end tested (recommendation → review → staging → promote)
- [ ] Investment thesis quality reviewed by human (first 5 INITIATE decisions)
- [ ] Staging environment running 5 days before any parameter promotion

---

### Phase 5 — Observability + Production Dashboard
**Capital:** Stage 3 (ongoing)

**Components to build:**
- [ ] React dashboard (full SPA: capital allocation, P&L per book, active positions, alerts, regime display)
- [ ] Prometheus metrics endpoints (`/api/v1/metrics`)
- [ ] Grafana dashboards (system health, P&L, signal quality, Claude cost)
- [ ] Enhanced alert dashboard (acknowledgment workflow, alert history)
- [ ] Mobile-responsive Telegram bot commands (`/status`, `/positions`, `/ack {code}`, `/flatten`)
- [ ] Historical performance analytics (equity curves, drawdown charts, win rate by regime)

---

## Open Questions (Pre-Stage 1 Answers Required)

These 8 questions must be resolved before any real capital deploys:

| # | Question | Required by |
|---|---|---|
| 1 | Zerodha token refresh — fully automated TOTP or semi-manual 8 AM alert? | Phase 2 |
| 2 | Order fill timeout (45s, ambiguous status) — wait or cancel? | Phase 2 |
| 3 | Emergency flatten access when software crashed — HTTP port 8001 or physical kill? | Phase 1 |
| 4 | Maximum daily loss in absolute rupees for Stage 1 (hardcode this number) | Phase 2 |
| 5 | Maximum simultaneous positions — Stage 1: 1. Stage 2: 3. Confirm. | Phase 2 |
| 6 | Primary options chain data source — Zerodha sufficient or external vendor? | Phase 2 |
| 7 | Paper trading statistical success criteria — exact Sharpe, win rate, sample size? | Before Stage 1 |
| 8 | Learning reviewer — who reviews and approves parameter recommendations? | Phase 4 |

---

## Infrastructure Timeline

| Task | Phase |
|---|---|
| AWS Lightsail Mumbai provisioning (4GB, 2vCPU, Ubuntu 22.04) | Phase 1 |
| PostgreSQL 15 + MongoDB 6 + Redis 7 installation + systemd | Phase 1 |
| Nginx + SSL certificate | Phase 1 |
| VPS backup automation (pg_dump + mongodump → S3) | Phase 1 |
| UptimeRobot external monitoring | Phase 1 |
| S3 bucket for backups | Phase 1 |
| Twilio account for voice alerts | Phase 1 |

---

## Deferred Technology

Introduce only when the criteria below are met:

| Tool | Deferred Until |
|---|---|
| Celery | Background job complexity justifies it (Phase 4+) |
| Prometheus + Grafana | Metrics volume justifies it (Phase 5) |
| Next.js / SSR | Dashboard needs routing/SSR (Phase 5) |
| Polars | Data volume exceeds pandas threshold (measure first) |
| TimescaleDB | OHLC/IV query performance degrades (ADR-002 required) |

---

## Key Non-Negotiables (Carry Through Every Phase)

- Audit trail written BEFORE every action that affects money
- PostgreSQL is the only source of truth for capital state
- All monetary values in integer paise — no floats
- Emergency Flatten Service: zero imports from main backend
- Learning service: zero database permission to write `strategy_parameters`
- No Claude on the critical path for intraday/swing execution
- Kill switch Level 3 requires manual system restart — no API reset
- 13-check pre-submission guard: all 13 must pass, no exceptions
