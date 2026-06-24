# AI_OS — Company Operating System

This is the company operating system for a solo founder running a portfolio of quantitative trading and AI products. AI_OS is not a collection of projects — it is a structured company with departments, workflows, reporting, and an executive AI layer.

**Read this file in full before taking any action. Every decision should be traceable back to a principle here.**

---

## 0. Company OS Structure

AI_OS is organized as a company, not a project folder:

```
Founder → Chief of Staff → Department Directors → Projects → Workflows → Reports → Dashboard
```

**Key directories:**
- `00_dashboard/` — Executive and product dashboards (specs)
- `01_memory/` — Company knowledge: decisions, opportunities, competitors, history
- `06_agents/company/` — Company-level AI agents (Chief of Staff + 5 Directors)
- `06_agents/quantara/` — Quantara-internal trading agents (do NOT modify without Founder approval)
- `09_docs/COMPANY_OS_ARCHITECTURE.md` — Full architecture design document
- `09_docs/roadmaps/COMPANY_OS_90DAY_ROADMAP.md` — Implementation roadmap
- `10_workflows/` — Daily, weekly, and monthly workflow definitions
- `11_reports/` — Report templates and archive

**When asked to run a workflow:** Read the relevant file in `10_workflows/`, use the prompt from `03_prompts/`, and output using the template from `11_reports/templates/`.

**When asked to act as a department director:** Read the relevant agent definition in `06_agents/company/`.

**Current phase:** Phase 1 — Manual execution via Claude. All workflows triggered by Founder on demand.

---

## 1. Business Context

This workspace is operated by a solo founder building an AI-first software stack around Claude Pro.
The work spans live trading systems, subscriber-facing signal platforms, and an AI content business.

**Primary Revenue Streams:**
- Quantara: subscriber signal delivery (Telegram) for NIFTY weekly options
- TradeCopilot: SaaS dashboard for traders (Razorpay subscriptions at tradecopilot.in)
- OptionHABot / TradingBotA: proprietary automated trading bots

**Business Constraint:** Solo operation. Every architectural decision has a maintenance cost.
Complexity not justified by real need is a liability, not an asset.

**AI Philosophy:** Claude is the primary reasoning layer for this entire operation — not just a code assistant.
The goal is to build a Claude-centric operating system where prompts, agents, memory, and tools are first-class assets.

---

## 2. Project Portfolio

### Quantara (Flagship — highest priority)
**Location:** `D:\AI_OS\04_projects\Quantara`  
**Purpose:** Deterministic NIFTY weekly options signal engine. Probability engine, not a prediction engine.  
**Stack:** Python 3.12 · FastAPI · PostgreSQL 16 · asyncpg · Redis · Zerodha Kite Connect · Telegram Bot API · Docker  
**Architecture:** 12+ modular subsystems with a finite state machine (IDLE → WATCHING → CANDIDATE → VALIDATING → SIGNAL_READY → IN_TRADE → EXITING → EXITED)  
**Key standards already present:** 10 YAML config files (no hardcoded thresholds), 37 pytest files, GitHub Actions CI, 11-layer immutable JSONL logging, SHA-256 replay verification, paper trading gate (8 weeks minimum before live)  
**Status:** Production-ready. This is the gold standard for all other projects.

### TradeCopilot
**Location:** `D:\AI_OS\04_projects\TradingCopilot` / `D:\tradecopilot`  
**Purpose:** SaaS trading rule engine and dashboard with AI analysis. Live at tradecopilot.in.  
**Stack:** React 19 · TypeScript · Tailwind CSS · Radix UI · Supabase (PostgreSQL + Auth) · Recharts · Groq API  
**Note:** Uses Groq, not Anthropic. This is a tech debt item — the AI layer should converge on Claude.  
**Status:** Active. Has Razorpay live keys, production Supabase project, real subscribers.

### OptionHABot
**Location:** `D:\AI_OS\04_projects\OptionHABot` / `D:\OptionHABot`  
**Purpose:** Heikin Ashi Doji + Confirmation pattern on 5-min ATM option candles. Multi-user, per-session isolation.  
**Stack:** Python 3.11 · FastAPI · MongoDB (Motor) · Zerodha Kite Connect · HTML/JS frontend  
**Strategy:** Doji (C-2) + Bull Confirmation (C-1) → MARKET entry. 7-point ratchet trailing stop (breakeven at +7, lock-in at +14, +21 etc.)  
**Status:** Active. Has multi-user architecture. MongoDB is a deliberate choice for per-user trade collections.

### TradingBotA
**Location:** `D:\AI_OS\04_projects\TradingBotA` / `D:\Trading_bot_a`  
**Purpose:** C1+C2 momentum strategy on 1-min Heikin Ashi option candles. 2-lot multi-exit.  
**Stack:** Python 3.12 · FastAPI · SQLite (aiosqlite) · Zerodha Kite Connect · HTML dashboard (port 8765)  
**Strategy:** ATM-50/ATM/ATM+50 CE/PE. C1 body ≥ threshold% of LTP + C2 breaks C1 high. Lot 1: TP +30pts / SL -15pts. Lot 2: TP +15pts / SL → breakeven after Lot 1 exit.  
**Status:** Active with documented backtest WR ~90% over 60 days. Lacks CI/CD.

### AI_SNIPP (Content Business)
**Location:** `D:\AI_OS\05_content`  
**Purpose:** AI-powered content and tooling library. Currently empty — this is the intended home for reusable snippets, prompts, and creator content.  
**Status:** Scaffolded, not yet populated. Treat as a parallel investment — route reusable artifacts here.

### Supporting Infrastructure (D:\ root)
- `D:\TradingBotwithAIAnalyzer` — Most mature frontend design system (design_guidelines.json, Anthropic integrated, shadcn/ui, dark-mode-only). Reference this for frontend decisions.
- `D:\ai_sql_assistant` — Claude API proof of concept for NLP → SQL. Prototype only.
- `D:\DharmaAI`, `D:\SocietyOS`, `D:\vedaverse` — Other ventures. Not primary focus.

---

## 3. AI_OS Workspace Structure

```
D:\AI_OS\
├── 01_memory/      # Knowledge base, context documents, session summaries
├── 02_skills/      # Claude skill definitions, agent capabilities
├── 03_prompts/     # Prompt templates (system prompts, task prompts, chains)
├── 04_projects/    # Active project codebases
├── 05_content/     # AI_SNIPP: reusable snippets, creator content, tools
├── 06_agents/      # Agent configurations, multi-agent orchestration
├── 07_templates/   # Project scaffolding templates
├── 08_mcp/         # MCP server configs and custom server implementations
├── 09_docs/        # Architecture decisions, runbooks, API specs
└── CLAUDE.md       # This file
```

Currently only `04_projects/` is populated. Populating the other directories is a primary objective.

---

## 4. Technical Standards

### Canonical Stack

| Layer | Standard | Notes |
|---|---|---|
| Backend | Python 3.12+ · FastAPI · asyncio | Quantara pattern |
| Frontend | React 19 · TypeScript · Tailwind CSS · Radix UI | TradingBotwithAIAnalyzer design system |
| Database (primary) | PostgreSQL via asyncpg or Supabase | Quantara / TradeCopilot |
| Database (document) | MongoDB via Motor | OptionHABot only — justified by per-user dynamic collections |
| Cache | Redis | Quantara pattern — add to others when needed |
| Broker | Zerodha Kite Connect 5.x | Universal across all trading projects |
| AI (primary) | Anthropic Claude API | claude-sonnet-4-6 for reasoning; claude-haiku-4-5 for throughput |
| AI (local) | Ollama | Classification, embedding, summarization, background jobs |
| Config | YAML files (not hardcoded, not .env-only) | Quantara is the model |
| Linting | ruff (Python) · ESLint + Prettier (TS) | |
| Testing | pytest (Python) · vitest or jest (TS) | Minimum 60% coverage on business logic |
| Logging | Append-only JSONL | Quantara's 11-layer system is the reference |

### Python Standards
- Python 3.12+ minimum across all projects.
- Type annotations on all function signatures. Run `mypy` or `pyright`.
- `pydantic` for all external data validation (API inputs, config parsing, broker responses).
- `asyncio` + `asyncpg` / `Motor` / `aiosqlite` for all I/O. No blocking calls in async handlers.
- `black` formatting + `ruff` linting (line-length 100, matching Quantara CI config).
- All thresholds, windows, and parameters externalized to YAML. No magic numbers.
- Kill switch logic is non-negotiable in every trading bot (2/5 consecutive loss limits, daily/weekly drawdown gates matching Quantara's risk.yaml pattern).

### TypeScript / React Standards
- `"strict": true` in tsconfig. No `any`.
- Functional components only. Custom hooks for non-trivial logic.
- Server state: React Query. Local state: `useState` / `useReducer`. No global state libraries without justification.
- Design system: dark mode, Tailwind CSS, Radix UI primitives (shadcn/ui pattern). Reference `D:\TradingBotwithAIAnalyzer\design_guidelines.json`.
- Typography: Chivo (headings) · IBM Plex Sans (body) · JetBrains Mono (all numerics). Right-align numeric columns.
- Palette: Emerald-500 (profit) · Red-500 (loss) · Indigo-600 (primary).
- No shadows. Flat solid backgrounds with 1px borders. Minimal motion.

### Database Standards
- Every table: `id UUID PRIMARY KEY`, `created_at TIMESTAMPTZ DEFAULT NOW()`, `updated_at TIMESTAMPTZ`.
- Append-only writes preferred for audit trails (signal_decisions, trade_executions, no_trade_events).
- Schema lives in version-controlled migrations. No schema changes without a migration file.
- No raw SQL in application code — use SQLAlchemy async or typed query builders.
- SQLite is acceptable only for local-only tools (TradingBotA pattern). Production services use PostgreSQL.

### Broker Integration (Zerodha)
- All MARKET orders must include `market_protection=-1` (SEBI compliance — present in TradingBotA, TradingBotwithAIAnalyzer).
- LIMIT → MARKET fallback: LIMIT at LTP+2, wait 10 seconds, convert to MARKET only if slippage < 4pts, else cancel.
- WebSocket ticks are the authoritative data source for live trading. REST fallback for reconnections.
- No intrabar entries. All entries on candle close only (Quantara non-negotiable rule).

---

## 5. Architectural Principles

**Quantara is the reference architecture.** When designing any component of any project, ask: does Quantara already solve this? If yes, port the pattern. If not, design to that standard.

**Determinism over prediction.** Quantara's core insight — probability engines beat prediction engines for trust, auditability, and compounding learning. Apply this to all signal logic: if a human cannot trace exactly why a signal fired by reading the logs, the system is wrong.

**State machines for complex flows.** Any process with more than 3 states should use an explicit state machine. Quantara's FSM (IDLE → WATCHING → ... → EXITED) prevents undefined state transitions and makes replay verification possible.

**Hard gates before soft gates.** Always apply hard rejection criteria (data quality, IV distortion, spread limits, HTF conflict) before running soft confidence scoring. This prevents the confidence engine from laundering bad setups.

**Append-only logs as the source of truth.** Trade outcomes, signal decisions, and no-trade events are facts that happened. They are never updated, only appended. Replay verification (SHA-256 hashing in Quantara) ensures reproducibility.

**Config externalizes everything.** Strategy parameters, thresholds, time windows, and risk limits live in YAML, not in code. Changing a threshold should never require a code deployment.

**Multi-user isolation is a first-class concern.** OptionHABot's per-user session model (isolated TradingSession, per-user MongoDB collections, per-user risk limits) is the correct pattern when building multi-tenant trading tools.

**Paper before live.** No system goes live without 8+ weeks of verified paper trading (Quantara rule). This applies to all trading projects regardless of backtest performance.

---

## 6. AI Agent Philosophy

### Claude Usage Guidelines

**Use Claude for:**
- Reasoning about strategy logic, edge cases, and tradeoffs
- Code generation requiring contextual understanding of the codebase
- Reviewing signal logic and architecture decisions
- Writing prompts, templates, and agent definitions for `03_prompts/` and `06_agents/`
- Analyzing trade performance data and surfacing non-obvious patterns
- Any task requiring judgment, not just pattern matching

**Do not use Claude for:**
- Classifying trade patterns where a local model suffices
- Generating embeddings — use Ollama or a dedicated embedding model
- Batch operations that can run offline without real-time reasoning
- Repeating the same prompt at high frequency — cache system prompts aggressively

**Model selection:**
- `claude-sonnet-4-6` (this model): default for all reasoning, code, and architecture work
- `claude-haiku-4-5-20251001`: high-throughput classification, short summaries, real-time UI feedback
- `claude-opus-4-7`: only for the most complex reasoning tasks with explicit justification

**Prompt caching is mandatory** on any system prompt or large static context. The Anthropic SDK supports `cache_control: ephemeral` on content blocks — use it. A system prompt sent 100 times without caching is 100x the cost.

**Structured outputs over free text** wherever the downstream consumer is code. Use `tool_use` / JSON mode to get predictable, parseable responses.

### Ollama Usage Guidelines

**Use Ollama for:**
- Embedding generation for semantic search (trade journals, documentation, memory retrieval)
- Classifying candle regimes, volatility states, day types (not worth Claude API cost)
- Summarizing long trade logs before passing to Claude for insight generation
- Background jobs: overnight report generation, weekly clustering (Quantara learning module)
- Any task that runs more than 10 times per minute in production

**Model recommendations:**
- `nomic-embed-text` or `mxbai-embed-large`: embeddings
- `mistral` or `llama3.2`: classification and summarization
- `deepseek-coder-v2`: code-related local inference

**The decision rule:** If the task does not require world knowledge, nuanced reasoning, or frontier capability — run it locally.

### Groq Note
TradeCopilot currently uses Groq (`gsk_oMdKaBJ...`). This is a tech debt item. New AI features in TradeCopilot should use Anthropic. Migration of existing Groq calls to Claude is a backlog item with medium priority.

---

## 7. Cost Optimization Strategy

**Billing awareness:** Claude Pro is the primary intelligence layer. API spend must be treated as a real operating cost, not a sunk cost.

1. **Prompt cache all static context.** System prompts for trading bots, strategy descriptions, and schema definitions are good cache candidates. Use Anthropic SDK `cache_control`.
2. **Preprocess with Ollama before Claude.** Summarize 500-line trade logs to 50 lines locally, then send the summary to Claude.
3. **Batch non-urgent Claude calls.** Daily report generation, weekly clustering analysis, and content drafts do not need real-time Claude. Queue them and batch via the Anthropic Batch API.
4. **Gate Claude calls behind local pre-filters.** Before calling Claude to analyze a setup, verify with local logic that it passes hard gates. Don't pay for Claude to reject a setup a simple rule could reject.
5. **Cache Claude responses where deterministic.** If the same data produces the same prompt, cache the output. Volatility classifications for standard market regimes do not need a fresh Claude call every 5 minutes.
6. **Haiku for high-frequency, Sonnet for reasoning.** Never use Sonnet for tasks Haiku handles correctly. Audit any production Claude call that runs more than once per minute.
7. **Track spend per project.** Tag API calls with a project identifier so cost is attributable. Use Anthropic usage logs.

---

## 8. Documentation Standards

**What must exist in every project:**
- `README.md`: what it is, how to run locally, required env vars, how to deploy
- `.env.example`: all required keys listed with descriptions, no real values
- `09_docs/` at workspace root: architecture decision records for non-obvious choices

**ADR format** (for `D:\AI_OS\09_docs\`):
```
# ADR-NNN: Title
Date: YYYY-MM-DD
Status: Accepted | Superseded | Deprecated
Context: why this decision was needed
Decision: what was decided
Consequences: what this enables and what it forecloses
```

**Comments in code:** Only when the WHY is non-obvious. Quantara's hard gates, kill switch rules, and SEBI compliance notes are good examples of comments worth writing. Do not comment what the code does.

**No generated documentation files** unless explicitly requested. No README created speculatively.

---

## 9. Decision-Making Framework

When facing a decision with competing options, evaluate in this order:

1. **Correctness** — Does it handle all edge cases, including market microstructure edge cases (data gaps, WebSocket reconnections, partial fills, broker API errors)?
2. **Safety** — Does it introduce risk of unintended live trades, data loss, or security exposure? Trading systems have real financial consequences.
3. **Auditability** — Can a human trace every decision through the logs 6 months later? If not, the design is wrong.
4. **Cost** — Does it use Claude where Ollama suffices? Does it make unnecessary broker API calls?
5. **Simplicity** — Is there a simpler path? Quantara's hard gate chain (12 gates checked in sequence) is simple because each gate is simple. Composing simple things produces complex behavior safely.
6. **Reusability** — Does this belong in `05_content/` (AI_SNIPP) or `07_templates/`?
7. **Performance** — Optimize only after correctness is proven and a bottleneck is measured.

**When the decision is irreversible** (live trading logic, database schema, API contracts): slow down, paper-test, get the design right before shipping.

**When in doubt about strategy logic:** defer to Quantara's design philosophy. It is the most battle-tested codebase in this portfolio.

---

## 10. Reusability Standards

The goal is to extract patterns from individual projects into shared assets. Route the following to the appropriate `AI_OS` folders:

| Artifact | Target Location |
|---|---|
| Reusable prompt templates | `D:\AI_OS\03_prompts\` |
| Claude agent definitions | `D:\AI_OS\06_agents\` |
| Code snippets and utilities | `D:\AI_OS\05_content\` (AI_SNIPP) |
| Project scaffolding | `D:\AI_OS\07_templates\` |
| MCP server configs | `D:\AI_OS\08_mcp\` |
| Architecture decisions | `D:\AI_OS\09_docs\` |
| Session context and memory | `D:\AI_OS\01_memory\` |

**Patterns already worth extracting:**
- Zerodha WebSocket client (identical in 3 projects — extract to shared module)
- LIMIT → MARKET fallback order logic (identical in TradingBotA, TradingBotwithAIAnalyzer)
- Kill switch / daily loss limiter (Quantara's is most robust — port it)
- Heikin Ashi candle builder (OptionHABot, TradingBotA, TradingBotwithAIAnalyzer)
- `design_guidelines.json` pattern (TradingBotwithAIAnalyzer) — promote to `07_templates/`
- 2-lot multi-exit risk model (TradingBotA / TradingBotwithAIAnalyzer)

---

## 11. Project Prioritization

Default priority when work spans multiple products:

1. **Quantara** — Flagship, subscriber-facing, revenue-critical. Stability and feature work here first.
2. **TradeCopilot** — Live SaaS with paying users. Fix regressions immediately. New features after Quantara is stable.
3. **OptionHABot** — Active bot. Bugs that affect trading sessions are P1.
4. **TradingBotA** — Active bot. Lower subscriber exposure than OptionHABot.
5. **AI_SNIPP / AI_OS Infrastructure** — Parallel investment. Route reusable artifacts here continuously — not last.

**Override rule:** Any live trading system with an open position takes priority over all other work until the position is closed or the incident is resolved.

---

## 12. Environment and Secrets

- **OS:** Windows 11 Home · PowerShell primary shell · Bash available
- **Working directory:** `D:\AI_OS`
- **Python environments:** `.venv` per project (already present in Quantara, OptionHABot)
- **Secrets:** All secrets via `.env` files. Never commit real values. Always maintain `.env.example`.
- **Port assignments (conflict-free — all projects can run simultaneously):**
  - Quantara: 8000 (API) · 8001 (Emergency Flatten) · 8002 (Zerodha OAuth callback)
  - TradingBotwithAIAnalyzer: 8003 (backend) · 3002 (frontend)
  - OptionHABot: 8004 (backend) · 3001 (frontend)
  - TradingBotA: 8765
  - TradeCopilot: 3000 (frontend, Supabase cloud backend)
  - CareerPilot: 8005 (backend) · 3003 (frontend)

**Known secrets in the clear (action required):**
- `D:\AI_OS\04_projects\TradingCopilot\.env` contains a live Groq API key and Razorpay live key. These must be rotated if the file has ever been committed to git.

---

## Operating Rules for Claude

- Do not hardcode any threshold, time window, or parameter. Add it to the project's YAML config.
- Do not generate `.md` documentation files unless explicitly requested.
- Do not introduce a new dependency without checking if an existing one covers the need.
- Do not skip the paper trading gate. If asked to wire live trading, confirm paper mode is verified first.
- Do not run destructive git operations (reset --hard, force push) without explicit confirmation.
- When modifying any trading strategy file, state what the change affects in the signal flow before writing code.
- When adding a Claude API call to any project, add prompt caching to the system prompt block.
- When a task touches live trading systems, treat it as P0. Correctness over speed.
