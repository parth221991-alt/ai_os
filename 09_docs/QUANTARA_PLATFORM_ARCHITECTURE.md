# QUANTARA — Decision Intelligence Platform
## Master Architecture Document v1.0

**Status:** Draft for review — designed to sit alongside QUANTARA_OS_MASTER.md v3.1
**Positioning:** Quantara is the general-purpose decision intelligence kernel. Quantara OS (the autonomous hedge fund system) is its first vertical "desk." Every battle-tested pattern from Quantara OS — probabilistic contracts, governance gates, explainability, degradation contracts — is generalized here from *trade decisions* to *strategic decisions*.
**Stack lineage:** Python 3.12 / FastAPI / PostgreSQL / Redis / Claude API — deliberately consistent with Quantara OS so modules, infra knowledge, and ops runbooks transfer.

---

# PART 0 — PRODUCT IDENTITY

## What Quantara Is

A multi-layered decision intelligence system for strategic thinking, financial intelligence, business analysis, decision modeling, risk analysis, knowledge synthesis, predictive reasoning, and autonomous task assistance.

The unit of value is not "an answer." It is a **Decision Object** — a structured, auditable, probabilistic artifact:

```json
{
  "decision_id": "dec_20260611_a3f7",
  "question": "Should TradeCopilot expand to a Telegram-first tier?",
  "recommendation": "proceed_phased",
  "confidence": 0.71,
  "expected_value": {"upside": "₹18L ARR in 12m", "downside": "₹2.5L sunk + 6 wks"},
  "risk_level": "medium",
  "time_horizon": "2 quarters",
  "assumptions": ["Telegram CAC < ₹150", "churn parity with web tier"],
  "verified_facts": ["current MRR", "current churn", "build cost estimate"],
  "alternatives": ["do_nothing", "whatsapp_first", "full_mobile_app"],
  "reasoning_path_ref": "rp_88412",
  "kill_criteria": ["CAC > ₹400 after 500 signups", "activation < 20%"],
  "review_date": "2026-09-15"
}
```

This is the same philosophy as Quantara OS Rule #1 (every decision probabilistic, never binary) — applied to business strategy instead of order flow.

## The Three Inherited Laws (from Quantara OS)

1. **No naked conclusions.** Every output carries direction, confidence, risk, expected value, horizon, and reasoning. A recommendation without a confidence score is a bug.
2. **Assumptions are quarantined from facts.** Verified data and assumptions live in separate fields, always. Mixing them is the strategic equivalent of optimistic caching of monetary state (banned anti-pattern #1).
3. **Learning recommends; humans ratify.** The feedback loop can never silently rewrite the system's own decision parameters (anti-pattern #12 generalized). All self-modification flows through a governance gate.

## Desks (Role-Based Verticals)

| Desk | User Mode | Primary Decision Types | First Implementation |
|------|-----------|------------------------|---------------------|
| Trading Desk | Trader | Position, allocation, risk | **Quantara OS (already frozen, in build)** |
| Founder Desk | Founder Mode | Build/kill, pricing, GTM, hiring, runway | v1 of this platform |
| Analyst Desk | Analyst Mode | Market sizing, competitor analysis, forecasting | v1–v2 |
| Investor Desk | Investor Mode | Capital allocation, portfolio thesis, due diligence | v2–v3 |

A "desk" = a configuration bundle: prompt frameworks + data connectors + decision templates + governance thresholds. The kernel is identical underneath.

---

# PART 1 — FULL SYSTEM ARCHITECTURE (Text Diagram)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 1 — INTERFACE                                                     │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Conversational│  │  Dashboard   │  │   Command    │  │  Role Views │ │
│  │ UI (chat +   │  │  (decision   │  │   Palette    │  │ Founder /   │ │
│  │ threads)     │  │  board, KPI) │  │  (/commands) │  │ Analyst /   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │ Investor    │ │
│         └─────────────────┴────────┬────────┘          └──────┬──────┘ │
└────────────────────────────────────┼──────────────────────────┼────────┘
                                     ▼  (REST + WebSocket)      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ API GATEWAY — FastAPI :8000                                             │
│  AuthN/AuthZ (JWT, role claims) · Rate limiting · Request audit log     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 2 — COGNITIVE ENGINE                                              │
│                                                                         │
│  ┌─────────────────────────┐   ┌──────────────────────────────────┐    │
│  │ CONTEXT & MEMORY        │   │ REASONING ORCHESTRATOR           │    │
│  │ · Working memory (Redis)│──▶│ · Step-decomposed reasoning      │    │
│  │ · Episodic (PG+pgvector)│   │ · Reasoning Path recorder        │    │
│  │ · Strategic memory      │   │ · Confidence scorer (sequential  │    │
│  │   (decisions, theses,   │   │   modifiers, Quantara OS style)  │    │
│  │   postmortems)          │   │ · Assumption/Fact separator      │    │
│  └─────────────────────────┘   └───────────┬──────────────────────┘    │
│                                            ▼                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │ Scenario     │ │ SWOT         │ │ Risk-Weighted│ │ Monte Carlo   │  │
│  │ Modeling     │ │ Automation   │ │ Decision     │ │ Simulation    │  │
│  │ Engine       │ │ Engine       │ │ Matrix       │ │ Framework     │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼ (reads via Data Contract API only)
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3 — DATA & INTELLIGENCE                                           │
│                                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │ Financial    │ │ Market       │ │ Competitor   │ │ Economic      │  │
│  │ Modeling     │ │ Research     │ │ Analysis     │ │ Signal        │  │
│  │ Module       │ │ Synthesis    │ │ Engine       │ │ Monitor       │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────────────┘  │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────────────────────────┐   │
│  │ KPI Tracking │ │ Forecasting  │ │ DATA VALIDITY ENGINE          │   │
│  │ System       │ │ Logic        │ │ (all data passes through —    │   │
│  └──────────────┘ └──────────────┘ │  staleness, source grading,   │   │
│                                    │  contradiction detection)     │   │
│                                    └───────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 4 — STRATEGIC AUTOMATION                                          │
│                                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │ Goal         │ │ Action Plan  │ │ Opportunity  │ │ Resource      │  │
│  │ Decomposition│ │ Generator    │ │ Scoring      │ │ Allocation    │  │
│  │ Engine       │ │              │ │ System       │ │ Optimizer     │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ FEEDBACK LEARNING LOOP                                           │  │
│  │ outcomes → calibration metrics (Brier) → recommendations table   │  │
│  │ ⚠ writes ONLY to learning_recommendations — never to live params │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼ (every action passes the gate)
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 5 — GOVERNANCE & SAFETY  (supreme authority — nothing bypasses)   │
│                                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │ Bias         │ │ Risk         │ │ Ethical /    │ │ STRATEGIC     │  │
│  │ Detection    │ │ Containment  │ │ Compliance   │ │ OVERRIDE      │  │
│  │ (8 named     │ │ Guardrails   │ │ Review       │ │ (3-level kill │  │
│  │  biases)     │ │ (hard limits)│ │ Framework    │ │  switch)      │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────────────┘  │
│            All verdicts written to audit_trail BEFORE action            │
└─────────────────────────────────────────────────────────────────────────┘
         │                              │                       │
         ▼                              ▼                       ▼
┌──────────────┐            ┌──────────────────┐      ┌─────────────────┐
│ PostgreSQL   │            │ MongoDB / pgvector│     │ Redis           │
│ (decision    │            │ (intelligence,    │     │ (working memory,│
│  state, audit│            │  research corpus, │     │  cache, streams)│
│  money-class)│            │  embeddings)      │     └─────────────────┘
└──────────────┘            └──────────────────┘
```

**Topology rule (inherited):** anything that affects state-of-record (decisions, capital figures, approved plans, audit) lives in PostgreSQL. Intelligence, research artifacts, embeddings, and LLM cache live in the document/vector store. Redis is display/working-memory only — never authoritative.

---

# PART 2 — MODULAR COMPONENT BREAKDOWN

## Layer 1 — Interface

| Module | Responsibility | Key Detail |
|--------|----------------|------------|
| `chat_service` | Conversational UI backend; threads, streaming responses | Each thread bound to a Decision Object or exploration session |
| `dashboard_service` | Decision Board, KPI panels, risk matrix renders | Read-only projections; never originates state changes |
| `command_engine` | `/commands` (e.g., `/simulate`, `/swot`, `/stress`, `/decide`) | Commands are typed, validated, and map 1:1 to kernel APIs |
| `role_manager` | Founder / Analyst / Investor modes | A role = prompt pack + visible modules + governance thresholds + output templates |

Role modes are **configuration, not code branches** (anti-pattern #6 generalized: no `if FOUNDER_MODE:` flags scattered through logic — each role is a declarative profile).

## Layer 2 — Cognitive Engine

### 2.1 Memory System (three tiers)

| Tier | Store | Contents | Retention |
|------|-------|----------|-----------|
| Working memory | Redis | Current session context, active scenario state | TTL hours |
| Episodic memory | PostgreSQL + pgvector | Conversation summaries, research sessions, embeddings for retrieval | Months, compacted |
| Strategic memory | PostgreSQL (relational, first-class schema) | Decision Objects, theses, assumptions registry, postmortems, kill criteria, calibration history | Permanent, append-only |

Strategic memory is the platform's moat-in-data: every decision, its predicted confidence, and its eventual outcome. This enables **calibration scoring** (Brier score per decision category — directly reusing the Quantara OS Phase 2 gate concept).

### 2.2 Reasoning Orchestrator

The orchestrator routes; it contains no business logic (anti-pattern #7). Pipeline per query:

```
classify intent → load relevant memory → select reasoning template
→ decompose into steps → execute steps (LLM + computed modules)
→ separate assumptions/facts → score confidence → governance gate
→ emit Decision Object or Analysis Object → persist reasoning path
```

**Confidence scorer** — sequential modifiers, same mechanic as the Quantara OS Probability Engine:

```
base        = evidence-weighted score from module outputs
+0.05         multiple independent sources agree (>0.80 agreement)
−0.10         critical source conflict (e.g., financial model vs market signal)
−0.05         key data older than freshness threshold for its type
−0.15         core assumption unverifiable
−0.20         data validity warnings active on any input used
+0.03         historical calibration for this decision category > 0.75
Floor: outputs below 0.50 confidence are never presented as recommendations —
       they are presented as "insufficient basis," with the missing data named.
```

### 2.3 Scenario Modeling Engine

Generates 3–5 structured futures per question: base / bull / bear / tail. Each scenario carries probability mass (must sum to 1.0 ± 0.02), key drivers, leading indicators to watch, and a playbook. This is the generalization of the Quantara OS pre-market debate: scenarios are **pre-computed and cached**, then live events are matched against them rather than re-reasoned from scratch.

### 2.4 SWOT Automation Engine

Not a static 4-box. Pipeline: entity profile → evidence retrieval (Layer 3) → claim extraction with source grading → SWOT placement with confidence per cell → cross-cell tension detection (a "strength" contradicted by a "threat" gets flagged, not averaged away — anti-pattern #4: confidence averaging that masks conflicts is banned here too).

### 2.5 Risk-Weighted Decision Matrix

For N options × M criteria: weights elicited or defaulted per role profile, scores from modules, then risk adjustment = score × (1 − risk_penalty) where risk_penalty derives from downside severity × probability × reversibility. Output includes the **sensitivity row**: which single weight change flips the ranking.

### 2.6 Monte Carlo Simulation Framework (Advanced Feature)

```
inputs:  variable definitions {name, distribution, params, correlations}
engine:  numpy vectorized; 10k–100k paths; correlated draws via Cholesky
outputs: P5/P25/P50/P75/P95 bands, probability of ruin / target,
         tornado chart data (variance attribution per input)
```

Used by: runway modeling, market-entry probability, capital allocation, stress testing. Deterministic seed stored with every run (reproducibility = auditability).

## Layer 3 — Data & Intelligence

| Module | Function | Computed vs LLM |
|--------|----------|-----------------|
| `financial_modeling` | 3-statement lite models, unit economics, runway, cohort math. All money as integer paise. | 100% computed. LLM never does arithmetic. |
| `market_research_synthesis` | Ingest reports/URLs/notes → graded claims with citations | LLM extraction + computed dedup/grading |
| `competitor_analysis` | Competitor profiles, feature matrices, positioning deltas, change detection | Hybrid |
| `economic_signal_monitor` | Rates, inflation, FX, sector indices; threshold alerts | Computed |
| `kpi_tracking` | User-defined KPI registry, targets, variance, anomaly flags | Computed |
| `forecasting` | Baseline stats (ETS/ARIMA-class) + scenario adjustments; forecasts always emitted as intervals, never points | Computed; LLM only narrates |

### Data Validity Engine (the non-negotiable one)

Direct port of Quantara OS 0.4 to knowledge work. Every datum entering Layer 2 carries:

```json
{"value": ..., "source": "...", "source_grade": "A|B|C|D",
 "as_of": "timestamp", "staleness_state": "FRESH|AGING|STALE",
 "verification": "verified|reported|assumed|model_output"}
```

Staleness thresholds per type (market prices: minutes; competitor pricing: 30 days; market-size reports: 12 months; user-entered financials: until superseded). Contradiction detection: two A-grade sources disagreeing > tolerance → both flagged, surfaced to user, **never silently averaged**.

## Layer 4 — Strategic Automation

| Module | Behavior |
|--------|----------|
| Goal Decomposition Engine | Goal → outcome tree → workstreams → tasks, each with owner-type, effort band, dependency edges, and a measurable definition-of-done |
| Action Plan Generator | Topologically sorted plan from the tree; critical path marked; every task carries its kill criterion |
| Opportunity Scoring System | Standardized 0–100 score: market (30) + fit/moat (25) + economics (25) + timing (10) + risk inverse (10). Grade A/B/C/D exactly like Quantara OS trade grades — Grade D opportunities are logged for learning, never recommended |
| Resource Allocation Optimizer | Constrained optimization (linear/greedy v1, OR-Tools later) over money/time/people against scored opportunities; respects hard reserves (the "10% cash reserve, never tradeable" rule generalized: always hold a configured slack reserve of time and capital) |
| Feedback Learning Loop | Decision outcomes → calibration metrics → parameter recommendations. **Writes only to `learning_recommendations`. A human approves promotion to live parameters via the governance UI. The learning service's DB user lacks write permission on live config tables — enforced at the database, not in code.** |

## Layer 5 — Governance & Safety

### Bias Detection (named, checkable biases — not vibes)

Eight checks run on every Decision Object before release:

1. Confirmation bias — were disconfirming sources retrieved at all?
2. Sunk cost — does reasoning reference prior investment as a *forward* justification?
3. Anchoring — does the recommendation cluster suspiciously near the user's stated prior?
4. Survivorship — does evidence sample only winners?
5. Recency overweight — is >60% of evidence weight from the last 10% of the time window?
6. Optimism drift — compare predicted vs realized outcomes per category (calibration data)
7. Authority substitution — claims graded high solely on source prestige without corroboration
8. Narrative coherence trap — confidence boosted by story-quality rather than evidence count

Each fires a flag with severity; CRITICAL bias flags block release until acknowledged.

### Risk Containment Guardrails (hard limits, Tier-0 style)

| # | Guardrail |
|---|-----------|
| 1 | No recommendation above the user's declared risk mandate (set per role profile) |
| 2 | Irreversible + high-stakes decisions always require explicit human confirmation, regardless of confidence |
| 3 | Confidence floor 0.50 for any "recommend" verb (Layer-1 constant, no exceptions) |
| 4 | Financial figures must originate from `financial_modeling` (computed), never from LLM free text |
| 5 | Any output relying on STALE critical data is auto-downgraded to "analysis," never "recommendation" |
| 6 | Autonomous task execution capped by spend/scope budget per session |

### Ethical Review Framework

Rule-tier (computed: legality flags, counterparty harm categories, regulatory domains like SEBI/RBI/GDPR-adjacent topics) + judgment-tier (LLM structured review against a checklist) → verdict ∈ {clear, clear_with_notes, escalate_human, blocked}. Verdicts are audit-logged before the output ships.

### Strategic Override System (kill switch hierarchy, generalized)

| Level | Effect | Reset |
|-------|--------|-------|
| 1 | Block new autonomous actions; analysis continues | Auth code via API |
| 2 | Freeze all automation incl. scheduled jobs; read-only mode | Auth code via API |
| 3 | Hard halt: revoke task-runner credentials, snapshot state, require restart | Manual restart only |

Automatic cascade triggers: calibration collapse (Brier degradation > threshold), repeated CRITICAL bias flags in one session, data-validity failure storm, or user-declared crisis mode.

---

# PART 3 — DATA FLOW

## Canonical flow: a strategic question enters the system

```
1. INGRESS      User asks (chat / command / API). Gateway authenticates,
                attaches role profile, writes request to audit log.

2. CONTEXT      Memory system assembles: working context (Redis),
                relevant episodic retrievals (vector), and strategic
                memory hits (prior decisions on this entity/topic).

3. CLASSIFY     Orchestrator classifies: question type (explore / analyze
                / decide / simulate / execute) → selects reasoning template
                and required Layer-3 modules.

4. GATHER       Layer 3 modules pull data through the Data Validity Engine.
                Every datum tagged: source grade, freshness, verification.
                Missing critical data → clarification question generated
                instead of fabricated input (hard rule).

5. REASON       Stepwise execution. Computed modules do math; the LLM does
                synthesis, hypothesis generation, and narrative. Each step
                appended to the Reasoning Path record.

6. QUANTIFY     Scenario engine / Monte Carlo / decision matrix run as the
                template requires. Confidence scorer applies sequential
                modifiers. Assumptions and facts written to separate fields.

7. GOVERN       Layer 5 gate: bias checks → guardrails → ethical review.
                Verdict + flags written to audit_trail BEFORE release.

8. EMIT         Decision/Analysis Object persisted to PostgreSQL,
                rendered to UI (tables, trees, matrices per template),
                reasoning path available on demand ("show reasoning").

9. LEARN        Review date scheduled. When outcome lands, the learning
                loop scores the prediction, updates calibration, and may
                write a recommendation — which a human ratifies or rejects.
```

## Event backbone

Redis Streams, same convention as Quantara OS:

```
quantara:stream:queries        — inbound requests
quantara:stream:decisions      — emitted Decision Objects
quantara:stream:alerts         — KPI / signal / governance alerts
quantara:stream:tasks          — autonomous task lifecycle events
quantara:stream:learning       — outcome and calibration events
```

Key convention: `quantara:{category}:{subcategory}:{id}` — identical scheme, zero relearning.

---

# PART 4 — EXAMPLE USE CASE WALKTHROUGH

**Scenario:** Founder Mode. "Should I take TradeCopilot from ₹199/month to ₹299/month?"

1. **Context load.** Strategic memory surfaces: launch decision object (Razorpay ₹49 intro + ₹199 autopay), churn KPI series, prior pricing thesis.
2. **Classification.** `decide` type → Pricing Decision template → requires `financial_modeling`, `kpi_tracking`, `competitor_analysis`, scenario engine, Monte Carlo.
3. **Gather.** KPI module returns MRR, churn, ARPU (verified, FRESH). Competitor engine returns Sensibull/Opstra tier pricing (B-grade, 19 days old → FRESH for its type). Price elasticity is **unknown** → system asks one clarification: "Any signal from the ₹49→₹199 step-up cohort? Conversion % at autopay?" User supplies 38%.
4. **Reason + quantify.** Computed model builds revenue under elasticity assumptions ε ∈ {−0.5, −1.0, −1.8}. Monte Carlo (20k paths, elasticity and churn as distributions): P50 net MRR +22% at ₹299; P(net MRR decline) = 0.18. Scenario engine emits base/bull/bear with leading indicators (week-2 churn delta, support ticket sentiment).
5. **Govern.** Anchoring check notes the user proposed ₹299 — system independently evaluates ₹249 and ₹349 as alternatives (₹249 dominates on risk-adjusted basis in bear scenario). Sunk-cost: clear. Guardrail 2: reversible decision → no forced confirmation.
6. **Emit.** Decision Object: `recommend ₹299 for new users, grandfather existing for 90 days; confidence 0.68; kill criterion: 30-day churn delta > +2.5pp → revert; review date +45 days; alternative ranked #2: ₹249 flat`. Assumptions (elasticity band, cohort transfer) listed separately from verified facts (current MRR, churn, conversion).
7. **Learn.** At +45 days, actual churn delta and MRR land; Brier score updates the "pricing decisions" calibration curve; if the system was overconfident, the learning loop *recommends* a confidence-modifier change — Parth approves or rejects it in the governance UI.

---

# PART 5 — SUGGESTED TECH STACK

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language / API | Python 3.12 + FastAPI | Continuity with every existing system you run |
| State DB | PostgreSQL 15 + pgvector | Decisions/audit/calibration relational; embeddings co-located — one fewer DB than Quantara OS for v1 |
| Intelligence store | MongoDB 6 (defer to v2 if pgvector + JSONB suffices) | Research corpus at scale |
| Cache / events | Redis 7 (streams + cache) | Identical conventions to Quantara OS |
| LLM | Anthropic API — Haiku for extraction/classification, Sonnet for synthesis, Opus-class only for high-stakes Decision Objects | Cost-tiered, mirrors Quantara OS Haiku-default policy |
| Math | numpy/pandas; OR-Tools deferred; statsmodels for forecasting | Computed-first doctrine |
| Frontend | React SPA (Next.js when multi-tenant SaaS, v3) | Familiar |
| Auth | JWT + role claims; Supabase Auth acceptable for v1 speed | You've shipped this twice |
| Jobs | APScheduler v1 → BullMQ-equivalent (arq/Celery) at v3 | Defer complexity |
| Payments (SaaS phase) | Razorpay | Already integrated patterns from TradeCopilot |
| Infra | AWS Lightsail Mumbai → ECS/EKS at v4 | Same ops surface as Quantara OS |
| Observability | Loguru JSON + /metrics v1; Prometheus+Grafana v3 | Same deferral logic |

**Deferred (explicitly):** Kafka, Airflow, dedicated vector DB (Qdrant/Weaviate), Kubernetes, fine-tuned models. Each gets an ADR with a trigger condition, not a date.

---

# PART 6 — SCALABILITY ROADMAP (v1 → v5)

| Version | Name | Scope | Gate to next version |
|---------|------|-------|---------------------|
| **v1** | Personal Strategist | Single user (Parth). Layers 1–2–5 minimal + financial modeling + KPI tracking. Chat + command palette, no dashboard. Decision Objects, strategic memory, governance gate, manual data entry + URL ingestion. | 50 real Decision Objects logged; calibration pipeline computing Brier on ≥20 resolved decisions; zero governance bypasses in audit |
| **v2** | Analyst Workbench | Full Layer 3 (competitor engine, research synthesis, economic signals, forecasting). Scenario + Monte Carlo + SWOT engines. Dashboard v1. | Research synthesis precision ≥ spot-check threshold; forecast intervals empirically calibrated (80% interval ≈ 80% hit rate) |
| **v3** | Strategic Automation | Layer 4 complete: goal decomposition, action plans, opportunity scoring, resource optimizer, learning loop with governance UI. Multi-user, role profiles live, Razorpay billing. **First external desk: Founder Desk SaaS for Indian solo founders.** | 10 paying users; learning recommendations reviewed weekly; override system fire-drilled |
| **v4** | Autonomous Desk | Bounded autonomous task execution (research tasks, monitoring tasks, draft generation) under spend/scope budgets and Level 1–3 override. Quantara OS integrated as the Trading Desk via API federation. | 30 days autonomous task operation, zero guardrail breaches; cross-desk strategic memory functioning |
| **v5** | Venture Platform | Multi-tenant, desk marketplace (third-party desk configs), org-level memory, API platform for embedding Quantara decisions in other products. Kubernetes, Kafka if event volume demands. | SOC2-track controls; per-tenant governance isolation proven |

Capital-graduation thinking applies: autonomy expands only after each stage proves itself, exactly like Paper → ₹2L → ₹25L → ₹5Cr.

---

# PART 7 — API STRUCTURE DRAFT

```
POST   /api/v1/sessions                      open reasoning session (role, desk)
POST   /api/v1/query                         general question → Analysis Object
POST   /api/v1/decide                        full pipeline → Decision Object
GET    /api/v1/decisions/{id}                fetch Decision Object
GET    /api/v1/decisions/{id}/reasoning      full reasoning path
POST   /api/v1/decisions/{id}/outcome        record real-world outcome (feeds learning)

POST   /api/v1/simulate/montecarlo           variables+distributions → bands, tornado
POST   /api/v1/simulate/scenarios            entity/question → 3–5 scenarios
POST   /api/v1/analyze/swot                  entity → evidence-graded SWOT
POST   /api/v1/analyze/matrix                options×criteria → risk-weighted ranking
POST   /api/v1/analyze/stress                plan/model → stress test report
POST   /api/v1/score/opportunity             opportunity → 0–100 + grade

POST   /api/v1/goals                         goal → decomposition tree
POST   /api/v1/goals/{id}/plan               tree → action plan
POST   /api/v1/allocate                      resources+opportunities → allocation

GET    /api/v1/kpis            POST /api/v1/kpis          KPI registry
GET    /api/v1/signals                        economic signal states
POST   /api/v1/research/ingest                URL/doc → graded claims

GET    /api/v1/governance/flags               open bias/risk flags
POST   /api/v1/governance/override            {level, reason} → activate
POST   /api/v1/governance/override/reset      {level, auth_code}
GET    /api/v1/learning/recommendations       pending parameter recommendations
POST   /api/v1/learning/recommendations/{id}/approve | /reject

GET    /api/v1/health | /health/detailed      same contract as Quantara OS
WS     /api/v1/stream                         decisions, alerts, task events
```

Every mutating endpoint: idempotency key required (same `{context}_{action}_{µs-timestamp}_{rand4}` format), audit-before-action, and a typed Pydantic v2 contract.

---

# PART 8 — PROMPT FRAMEWORK FOR INTERNAL REASONING

Reasoning templates are versioned YAML, stored in PG, hot-loadable. Skeleton:

```yaml
template: pricing_decision_v3
model_tier: sonnet            # haiku | sonnet | opus per step, overridable
steps:
  - id: frame
    instruction: >
      Restate the decision as a falsifiable question. List what would
      have to be true for each answer. Do NOT recommend yet.
  - id: evidence
    instruction: >
      For each retrieved datum (provided with source_grade, as_of,
      verification): classify as FACT (verified) or ASSUMPTION.
      Never upgrade an assumption. Flag contradictions explicitly.
  - id: hypotheses
    instruction: >
      Generate ≥3 materially different options including do-nothing.
      For each: mechanism, upside, downside, reversibility.
  - id: red_team
    instruction: >
      Argue the strongest case AGAINST the currently leading option.
      Cite which evidence it relies on. (Feeds bias detector #1.)
  - id: quantify
    handoff: computed            # Monte Carlo / matrix — NOT the LLM
  - id: synthesize
    instruction: >
      Emit Decision Object JSON only. confidence must reflect the
      sequential modifier table provided. assumptions[] and
      verified_facts[] must be disjoint. Include kill_criteria and
      review_date. No prose outside JSON.
output_contract: decision_object_v1   # Pydantic-validated; retry on violation
```

Standing rules injected into every template (the system's own constitution):

1. Think stepwise; conclusions only in the final step.
2. Show reasoning when asked — the Reasoning Path record is the source, not a post-hoc rationalization.
3. Every numeric claim either comes from a computed module or is labeled ASSUMPTION.
4. If critical data is missing, output a `clarification_request`, never a guess.
5. Always present ≥1 alternative and the conditions under which it would win.
6. Confidence below 0.50 → "insufficient basis," name the missing evidence.

LLM outputs are Pydantic-validated; contract violations trigger one structured retry then hard-fail to human review — never silent acceptance.

---

# PART 9 — UI DASHBOARD LAYOUT

```
┌──────────────────────────────────────────────────────────────────────┐
│ TOP BAR   Quantara ▾ [Desk: Founder]  [Override: ●OFF]  [Alerts: 2]  │
├────────────┬─────────────────────────────────────────┬───────────────┤
│ LEFT NAV   │  CENTER — DECISION BOARD                │ RIGHT RAIL    │
│            │                                         │               │
│ ◉ Decisions│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │ GOVERNANCE    │
│ ○ Chat     │  │ OPEN (4) │ │ WATCH(6) │ │RESOLVED │ │ · Bias flags  │
│ ○ Goals    │  │ pricing  │ │ churn    │ │ Brier:  │ │ · Pending     │
│ ○ KPIs     │  │ ₹299 ?   │ │ review   │ │  0.19   │ │   learning    │
│ ○ Research │  │ conf .68 │ │ +45d     │ │ calib ▲ │ │   recs (1)    │
│ ○ Scenarios│  └──────────┘ └──────────┘ └─────────┘ │ · Override    │
│ ○ Simulate │                                         │   controls    │
│ ○ Competi- │  KPI STRIP                              │               │
│   tors     │  MRR ₹— ▲   Churn —% ▼   Runway —mo    │ ASSUMPTIONS   │
│ ○ Signals  │                                         │ REGISTRY      │
│ ○ Governance│ RISK MATRIX        SCENARIO TILES      │ · 3 unverified│
│            │  (impact ×          base .55 │ bull .25 │ · 1 expiring  │
│            │   likelihood        bear .15 │ tail .05 │               │
│            │   heatmap)                              │               │
├────────────┴─────────────────────────────────────────┴───────────────┤
│ COMMAND PALETTE (⌘K): /decide /simulate /swot /stress /override ...   │
└──────────────────────────────────────────────────────────────────────┘
```

Principles: the Decision Board (not chat) is the home screen — chat is an input method, decisions are the product. Every card shows confidence + review date. Governance is permanently visible, never buried in settings. Role switch re-skins modules, templates, and thresholds in one action.

---

# PART 10 — ADVANCED FEATURE SPECIFICATIONS

| Feature | Design essence |
|---------|----------------|
| **Monte Carlo framework** | Part 2.6. Shared service; every consumer (runway, market entry, allocation) calls the same engine with stored seeds |
| **Strategic stress testing** | Take any plan/model; apply shock library (demand −40%, CAC ×2, key-person loss, regulatory shock, funding winter, platform-dependency cutoff). Output: survival verdict per shock, first breaking point, cheapest pre-emptive hedge. The Black Swan Protocol's *assessment* phase, applied to strategy |
| **Capital allocation optimizer** | Opportunities (scored) + constraints (capital, time, mandatory reserve) → frontier of allocations; presents 3 points (conservative/balanced/aggressive), never a single "optimal" |
| **Founder decision sandbox** | Fork current strategic memory into a sandbox; play decisions forward against scenario engine; nothing in sandbox touches real state (separate schema, big red banner). Diff view: sandbox future vs current trajectory |
| **Market-entry probability model** | Structured factor model (market timing, distribution access, moat potential, capital adequacy, regulatory friction) → Monte Carlo over factor uncertainty → P(traction milestones) with tornado attribution |
| **Competitive positioning heatmap** | Axes chosen by variance analysis of feature/price matrices (not hardcoded); entities plotted with confidence halos; white-space cells scored as opportunities |
| **Moat detection algorithm** | Scores 7 moat types (network effects, switching costs, scale economics, brand, regulatory, data, counter-positioning) from evidence claims; each score carries evidence count + grade — a moat claim with 1 C-grade source renders visibly weak |
| **Narrative synthesis engine** | Final-mile renderer: Decision/Analysis Objects → board memo, investor update, or one-pager. Templates per audience. **Narrative can only cite fields that exist in the object — it cannot introduce new claims** (enforced by citation check against the object schema) |

---

# PART 11 — EXPANSION INTO AUTONOMOUS AGENT SYSTEM (v4+)

Autonomy expands along the proven graduation curve:

| Stage | Autonomy granted | Bound by |
|-------|------------------|----------|
| A0 | Suggest only (v1–v3 default) | — |
| A1 | Autonomous research & monitoring tasks (gather, watch, summarize) | Scope whitelist, spend budget, Level-1 override |
| A2 | Autonomous drafting & scheduling (reports, alerts, calendar of reviews) | Output quarantine until human release |
| A3 | Bounded external actions (publish report, send update, place paper trade via Trading Desk) | Per-action governance gate + idempotency + full audit |
| A4 | Closed-loop desk operation (Quantara OS already defines this for trading) | Capital/scope graduation protocol per desk |

Architecture: each agent is a worker consuming `quantara:stream:tasks`, holding a **capability token** (scoped credentials, TTL, spend ceiling) issued by Layer 5. Revoking tokens is the Level-3 override mechanism. Agents share state only via the database (anti-pattern #9: no shared mutable memory between agents).

The endgame loop:

```
Founder Desk decides → Action plans execute (A2/A3) → KPIs measure →
Learning loop calibrates → Investor Desk reallocates → Trading Desk
(Quantara OS) compounds the capital → back to Founder Desk
```

One kernel, four desks, every decision auditable, every confidence score eventually graded against reality.

---

# PART 12 — ANTI-PATTERNS (BANNED, inherited and extended)

| # | Anti-pattern | Generalized form |
|---|--------------|------------------|
| 1 | Optimistic cache for monetary state | Redis is never authoritative for decisions, capital figures, or audit |
| 2 | `except Exception: pass` | Unchanged. Banned. |
| 3 | Status inferred from absence | A decision without an outcome record is OPEN, not "fine" |
| 4 | Confidence averaging masking conflicts | Contradictory evidence is surfaced, never blended |
| 5 | Time-dependent tests | FrozenClock everywhere |
| 6 | Feature flags as architecture | Roles and desks are declarative profiles, not if-branches |
| 7 | God orchestrator | Orchestrator routes; modules reason |
| 8 | Synchronous LLM calls in hot request paths | Tiered models, caching, pre-computation |
| 9 | Shared mutable state between agents | DB-mediated only |
| 10 | Magic numbers in governance logic | Every threshold a named constant with derivation comment |
| 11 | Deployment without rollback | <5-minute rollback documented per release |
| 12 | Learning autonomy creep | Learning DB user has no write permission on live parameters |
| 13 | **LLM-originated arithmetic** (new) | All numbers from computed modules; LLM narrates, never calculates |
| 14 | **Unsourced confidence** (new) | A confidence score with no modifier trace is invalid |

---

*Quantara v1.0 — designed as the generalization of Quantara OS v3.1.*
*Frozen decisions in Quantara OS remain frozen; this document governs the platform layer only.*
