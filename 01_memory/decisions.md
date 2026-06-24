# Architecture Decision Records — AI_OS

**Format:** ADR (Architecture Decision Record)  
**Last Updated:** 2026-06-08  
**Purpose:** Document non-obvious decisions with context, so future work can understand WHY, not just WHAT.

---

## ADR-001: PostgreSQL for Financial State, MongoDB for Intelligence (Quantara)

**Date:** 2026-06-08 (documented; decision made during v3.1 architecture design)  
**Status:** Accepted — frozen in QUANTARA_OS_MASTER.md v3.1

**Context:**  
Quantara needs to store two fundamentally different types of data: financial state (positions, orders, capital, audit trails) that requires ACID guarantees and zero tolerance for eventual consistency, and intelligence/analytical data (signals, scenarios, microstructure snapshots, AI cache) that has flexible schema and benefits from document-oriented access patterns.

**Decision:**  
Split databases by data category:
- **PostgreSQL 15**: ALL financial state — positions, orders, capital accounts, risk_state, audit_trail, kill_switch_log, reconciliation_log, strategy_parameters, learning_recommendations
- **MongoDB 6**: Intelligence and analytical — market_data, options_data, microstructure_analysis, signals, intelligence_feed, premarket_packages, ai_cache, learning_metrics, system_logs
- **Redis 7**: Ephemeral hot cache and event bus only — never authoritative for execution decisions

**Alternatives Considered:**
- Single PostgreSQL: Schema migrations for signal documents are painful; JSON columns lose query efficiency
- Single MongoDB: Cannot guarantee ACID semantics for financial transactions; append-only audit tables need relational integrity
- TimescaleDB: Considered for OHLC/IV time series; deferred until query performance degrades (ADR-002 required to revisit)

**Rationale:**  
PostgreSQL ACID guarantees are non-negotiable for money. MongoDB flexible schemas are a genuine advantage for signals and AI cache (different agents write different fields to the same signal document over time).

**Consequences:**  
Two database systems to operate, backup, and monitor. Offset by: cleaner data models, no compromise on financial integrity, no awkward JSON in relational tables for analytical data.

---

## ADR-002: Integer Paise for All Monetary Values (Quantara)

**Date:** 2026-06-08 (documented; decision made during v3.1 design)  
**Status:** Accepted — Layer 1 immutable constant

**Context:**  
Trading systems perform arithmetic on monetary values (position sizing, P&L, margin calculations). Floating-point arithmetic introduces rounding errors that compound over time and can produce nonsensical results (e.g., sizing calculation producing 1.9999 lots which rounds to 1, not 2).

**Decision:**  
ALL monetary values are stored and computed as INTEGER in paise. `₹1,234.56 = 123456`. Display layer converts. Float arithmetic on money is BANNED throughout the codebase.

**Alternatives Considered:**
- Python `Decimal`: Correct but slower and more verbose than integer arithmetic. Rejected.
- Float with rounding: Error-prone. Two floats added can produce results that don't match integer arithmetic.
- Integer rupees (not paise): Loses sub-rupee precision on options premium tracking.

**Rationale:**  
Integer arithmetic is exact. Paise precision (2 decimal places) covers all Indian market instruments. The display layer is a thin conversion — the complexity stays in one place.

**Consequences:**  
All new code interacting with monetary values must accept and return integers. Any agent that receives a float monetary value must reject it or convert with explicit logging.

---

## ADR-003: Claude Is Never on the Critical Path for Intraday Execution (Quantara)

**Date:** 2026-06-08 (documented; Engineering Rule 6 in QUANTARA_OS_MASTER.md v3.1)  
**Status:** Accepted — non-negotiable architectural rule

**Context:**  
The original Debate Agent design called Claude per-signal in real-time during market hours. A Claude API call takes 0.5–3 seconds. For a 5-minute candle strategy, the signal fires on candle close and must execute before the next candle opens. A 3-second Claude call introduces unacceptable latency AND creates a hard dependency on Anthropic API availability.

**Decision:**  
All Claude reasoning is completed BEFORE market open and cached to Redis. The Pre-Market Scenario Agent runs at 9:00 AM and generates 3–5 intraday scenarios cached with 24h TTL. At signal time, the agent matches against cached scenarios. No live Claude call during execution.

**Alternatives Considered:**
- Async Claude call (fire and continue): Signal could execute before debate result arrives — makes debate useless
- Claude with 1s hard timeout: Too unreliable; p99 Claude latency exceeds 1s during peak load
- Skip debate entirely: Loses adversarial quality that pre-cached scenarios provide

**Rationale:**  
Claude assists, it does not gate. Pre-caching delivers the same adversarial quality without execution dependency. The pre-market window (8:30–9:10 AM) is the correct time for AI reasoning.

**Consequences:**  
Pre-market package must complete reliably by 9:10 AM every day. Claude unavailability during market hours has zero impact on execution. Claude unavailability at 9:00 AM triggers fallback (yesterday's cached scenarios).

---

## ADR-004: Emergency Flatten Service as Standalone Process (Quantara)

**Date:** 2026-06-08 (documented; Emergency Flatten spec in 12_emergency-flatten-service.md)  
**Status:** Accepted — Tier 0 architectural requirement

**Context:**  
If the main backend crashes, deadlocks, or enters an unrecoverable state, open positions must still be closeable. The main backend cannot be the recovery mechanism for its own failure.

**Decision:**  
Emergency Flatten Service is a completely standalone Python process:
- ZERO imports from the main quantara backend
- Own requirements.txt (fastapi, uvicorn, asyncpg, kiteconnect, pydantic, python-dotenv only)
- Own systemd service (`quantara-flatten.service`) that `Requires: postgresql.service` only
- Port 8001, bound to 127.0.0.1 (internal only)
- Reads positions DIRECTLY from Zerodha (not from internal state)

**Alternatives Considered:**
- Flatten logic in the main backend: Circular dependency — if the main backend is down, flatten is inaccessible
- Separate Docker container: More complex than a separate Python process; adds Docker failure mode
- Physical kill switch (broker app): Available as last resort but requires human with phone access

**Rationale:**  
Independence is the entire value. Any shared code is a shared failure mode. The standalone process survives main backend crashes, Redis failures, and MongoDB failures — it only needs PostgreSQL and Zerodha.

**Consequences:**  
Two Python services to maintain, deploy, and monitor. The flatten service must be tested monthly to verify independence. The isolation constraint is a permanent maintenance discipline.

---

## ADR-005: 3-Level Kill Switch Hierarchy (Quantara)

**Date:** 2026-06-08 (documented; Tier 0 Risk Engine spec in 05_risk-agent.md)  
**Status:** Accepted — non-negotiable

**Context:**  
A single kill switch is binary. In practice, there are situations that warrant different responses: no new entries (Level 1), complete trading halt (Level 2), and emergency position closure (Level 3). These require different reset paths to prevent accidental activation and to match response to severity.

**Decision:**
- Level 1: No new entries, existing positions managed normally → API reset (authenticated)
- Level 2: All trading blocked, monitoring active → API reset + two-factor
- Level 3: Emergency flatten triggered → **Manual system restart ONLY, no API reset**

**Rationale:**  
Level 3 is the most dangerous state. The requirement for manual restart prevents an automated process from accidentally re-enabling trading after a critical event. The human must explicitly restart, observe the system, and confirm it is safe.

**Consequences:**  
Level 3 activation requires physical access (or SSH) to the VPS. This is intentional. The reset procedure must be documented in a runbook.

---

## ADR-006: 40 Trading Days Paper Minimum Before Live Capital (Quantara)

**Date:** 2026-06-08 (documented; ROADMAP.md Stage 0 criteria)  
**Status:** Accepted — non-negotiable gate

**Context:**  
An arbitrary "looks good" paper trading window leads to premature live deployment. Statistical significance for a trading strategy requires enough samples to measure win rate, Sharpe ratio, and Brier score with confidence.

**Decision:**  
Minimum 40 TRADING DAYS of paper trading with ALL of:
- ≥60% intraday win rate
- No system errors on 5 consecutive days
- Reconciliation and kill switches verified in simulation
- Brier score computed for confidence calibration

**Alternatives Considered:**
- 8 calendar weeks: Too short if markets are closed; trading days are the correct unit
- 20 trading days: Statistically insufficient for a low-frequency strategy
- "Until it looks good": Subjective and dangerous

**Rationale:**  
40 trading days ≈ 2 calendar months of trading. It covers multiple market regimes (trending, range, event days). Statistical significance requires sample size proportional to signal frequency.

**Consequences:**  
Stage 1 live deployment cannot happen before approximately 2 calendar months after paper trading begins. This is the correct constraint.

---

## ADR-007: Learning Service Cannot Write strategy_parameters (Quantara)

**Date:** 2026-06-08 (documented; KNOWLEDGE_ARCHITECTURE.md learning governance)  
**Status:** Accepted — enforced at database permission level

**Context:**  
An automated learning system that can directly modify its own trading parameters creates a feedback loop that can compound errors. A bad week of performance could cause the system to adjust parameters in ways that worsen the next week.

**Decision:**  
The learning service database user has READ-ONLY access to `strategy_parameters`. It can only write to `learning_recommendations`. Parameter changes require: human review → approval → staging deployment (5 days) → production promotion.

**Alternatives Considered:**
- Learning writes directly: Too dangerous; removes human oversight from parameter changes
- Learning writes with automatic rollback: Rollback is triggered by detection — detection can lag by hours or days
- No learning system: Leaves performance insights unused; misses compounding improvement opportunity

**Rationale:**  
Database-level permissions enforce this constraint at the infrastructure layer — it cannot be bypassed by a code bug. Human approval is required for the governance step that matters most.

**Consequences:**  
Parameter improvements take 5+ trading days to reach production. This lag is the correct tradeoff for safety.

---

## ADR-008: MongoDB for OptionHABot (Per-User Dynamic Collections)

**Date:** 2026-06-08 (documented from codebase analysis)  
**Status:** Accepted

**Context:**  
OptionHABot is a multi-user trading bot where each user has their own isolated trade history and positions. A relational approach would require creating new tables per user (antipattern) or using a discriminator column that makes per-user queries slower.

**Decision:**  
MongoDB with per-user collections: `trades_{user_id}`, `positions_{user_id}`. Dynamic collection creation is idiomatic in MongoDB.

**Alternatives Considered:**
- PostgreSQL with user_id discriminator: Correct approach, but per-user queries are less clean and collection-level isolation is weaker
- PostgreSQL with schemas per user: Creates 100+ schemas in the same database; harder to maintain

**Rationale:**  
This is the one justified deviation from the AI_OS PostgreSQL-first standard. The per-user dynamic collection pattern is a genuine MongoDB strength. For a 3-month trading history with <100 users, MongoDB's query patterns (find by user_id, sort by timestamp) are perfectly adequate.

**Consequences:**  
Two different database paradigms in the portfolio. If OptionHABot ever scales to thousands of users, revisit the collection-per-user pattern (MongoDB recommends against creating unlimited collections).

---

## ADR-009: SQLite for TradingBotA (Single-User Local Tool)

**Date:** 2026-06-08 (documented from codebase analysis)  
**Status:** Accepted

**Context:**  
TradingBotA is a single-user, locally-run bot. It doesn't need concurrent writes from multiple users, doesn't need backup replication, and doesn't need network access to the database.

**Decision:**  
SQLite via `aiosqlite` for all persistence.

**Rationale:**  
Zero operational overhead. No database server to manage. Correct for a single-user local tool. Aligns with AI_OS guideline: "SQLite is acceptable only for local-only tools."

**Consequences:**  
Cannot be deployed as a multi-user service without a database migration. If TradingBotA ever becomes multi-user or VPS-hosted, migrate to PostgreSQL.

---

## ADR-010: Groq in TradeCopilot (Tech Debt Acknowledged)

**Date:** 2026-06-08 (documented from codebase analysis)  
**Status:** Deprecated — new AI features must use Claude

**Context:**  
TradeCopilot integrated Groq (llama-3.3-70b-versatile) as the AI backend, likely during early prototyping when Groq's speed advantages were a deciding factor.

**Decision (original):**  
Use Groq for AI analysis generation.

**Why This Is Now Tech Debt:**
1. Key ended up in frontend `.env` (security vulnerability — see ADR-011)
2. Creates a second AI provider dependency (vs. Claude everywhere else in AI_OS)
3. Groq's API surface differs from Anthropic's — migration cost grows over time

**Migration path:**
1. Move Groq API call server-side (Supabase Edge Function) — immediate priority for security
2. Replace Groq model with `claude-haiku-4-5-20251001` for analysis generation
3. Deprecate `REACT_APP_GROQ_API_KEY` entirely

**Consequences:**  
Groq calls that exist today can remain until migrated. No NEW Groq integrations. All new AI features in TradeCopilot use Claude.

---

## ADR-011: market_protection=-1 on All MARKET Orders (Universal)

**Date:** 2026-06-08 (documented from codebase analysis; SEBI compliance requirement)  
**Status:** Accepted — non-negotiable for SEBI compliance

**Context:**  
SEBI regulations require that algorithmic MARKET orders include a market protection parameter. Zerodha's API enforces this with `market_protection=-1`. Orders placed without this parameter may be rejected by the exchange.

**Decision:**  
All MARKET orders across ALL projects must include `market_protection=-1`. This is a non-negotiable compliance requirement, not a preference.

**Apply to:** Quantara, OptionHABot, TradingBotA, TradingBotwithAIAnalyzer, and any future project that places orders on Indian exchanges through Zerodha.

**Consequences:**  
Any code review that finds a MARKET order without `market_protection=-1` is a P0 bug. Any extracted snippet in `05_content/` that involves MARKET orders must include this parameter and document why.

---

## ADR-012: systemd Over Docker for Quantara Production

**Date:** 2026-06-08 (documented; QUANTARA_OS_MASTER.md v3.1 production spec)  
**Status:** Accepted

**Context:**  
Quantara needs reliable production deployment on AWS Lightsail (single VPS). Two main options: Docker Compose (container orchestration) or systemd (native Linux process management).

**Decision:**  
systemd for production services (quantara-backend.service, quantara-flatten.service). Docker Compose for local development only.

**Rationale:**
- systemd restart semantics are simpler for two processes with a dependency (flatten requires PostgreSQL, not the main backend)
- systemd integrates natively with VPS monitoring tools (journald, systemctl status)
- Docker adds an abstraction layer that can hide real system resource issues
- For two Python processes on a dedicated VPS, Docker's benefits (environment isolation, portability) are less valuable than systemd's operational simplicity

**Consequences:**  
systemd unit files must be version-controlled and deployed manually. Environment files live at `/etc/quantara-backend/env` and `/etc/quantara-flatten/env` with mode 600. Containerization remains available if the architecture scales to multiple VPS nodes.

---

## ADR-013: Pre-Market Intelligence Window 8:30–9:10 AM (Quantara)

**Date:** 2026-06-08 (documented; QUANTARA_OS_MASTER.md schedule)  
**Status:** Accepted

**Context:**  
Quantara's AI-generated context (scenarios, swing debates, sector analysis, CIO briefing) must be available before the market opens at 9:15 AM. The pre-market window must be reliable — if it fails, the first signals of the day have no scenario context.

**Decision:**  
Pre-market intelligence package runs 8:30–9:10 AM:
- 8:30: News batch (Intelligence Agent → Haiku)
- 8:45: Sector rankings update
- 9:00: Intraday scenario generation (Debate Agent → Haiku batch)
- 9:05: Swing setup batch (Swing Alpha Agent → Haiku, up to 5 setups)
- 9:10: CIO briefing compiled → Redis cache ready

**Fallback if package fails:**
- News: skip news signal component
- Scenarios: use yesterday's cached scenarios
- Swing debate: raise confidence threshold by +0.10, proceed
- Investment thesis: no impact (runs weekly)

**Consequences:**  
The pre-market window is a daily critical path. Monitoring must alert if any component fails to complete by 9:10 AM. The 9:15 market open is a hard deadline — anything not cached by then is a miss.
