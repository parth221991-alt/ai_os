---
role: ai-os-orchestrator
version: 1.0
scope: workspace
projects: ALL
---

# AI_OS Master Orchestrator

## Purpose

This is the primary entry point for all work inside `D:\AI_OS`. Every task — regardless of project, domain, or complexity — begins here.

The orchestrator does not perform work itself. It determines what the task is, which project it belongs to, what context is required, and which skills to activate. It then hands off to the appropriate execution layer with the correct context pre-loaded.

**Read this file first. Then load what it tells you to load. Then act.**

---

## Orchestration Flow

Every task passes through five stages in sequence:

```
[1] Intent Detection
        ↓
[2] Project Identification
        ↓
[3] Context Loading (memory + docs + skills)
        ↓
[4] Execution
        ↓
[5] Artifact Routing (output → correct AI_OS folder)
```

Never skip a stage. A task started without identified intent and project produces incorrect context loading, which produces incorrect output.

---

## Stage 1 — Intent Detection Rules

Map the user's request to one of six intent categories:

| Intent Code | Description | Signal Phrases |
|---|---|---|
| `STRATEGY` | Signal logic, entry/exit rules, backtest review | "signal", "setup", "entry", "exit", "backtest", "win rate", "pattern", "candle", "Heikin Ashi", "NIFTY", "option" |
| `EXECUTION` | Order placement, broker integration, kill switch, position tracking | "order", "Zerodha", "fill", "slippage", "kill switch", "live", "paper", "session", "EOD" |
| `INFRASTRUCTURE` | FastAPI routes, database schema, logging, deployment, CI/CD | "route", "endpoint", "schema", "migration", "Docker", "deploy", "CI", "log" |
| `FRONTEND` | React components, UI layout, charts, subscriptions, dashboards | "component", "UI", "chart", "dashboard", "Tailwind", "Radix", "Recharts", "TypeScript", "hook" |
| `AI_INTEGRATION` | Claude/Ollama integration, prompt design, caching, agent logic | "Claude", "Ollama", "prompt", "agent", "cache", "LLM", "model", "embedding", "batch" |
| `ORCHESTRATION` | Cross-project workflows, shared module extraction, AI_OS structure | "extract", "share", "reuse", "AI_OS", "skill", "memory", "template", "orchestrat" |

**Rule:** If multiple intent codes match, load the primary intent skill first, then the supporting skill. If intent is genuinely ambiguous, ask one clarifying question before loading context.

---

## Stage 2 — Project Identification Rules

Apply the following rules in order. Stop at the first match.

### Explicit identification (highest confidence)
- User names a project directly → use that project.
- User references a file path under a known project directory → use that project.
- User references a concept unique to one project (e.g., "7-point ratchet" → OptionHABot, "pre-market package" → Quantara, "Razorpay subscription" → TradeCopilot) → use that project.

### Signal-based identification
| Signal | Project |
|---|---|
| NIFTY weekly options, FSM states (IDLE/WATCHING/CANDIDATE/SIGNAL_READY), four-tier architecture, CIO allocation, three capital books | Quantara |
| Telegram signals, subscriber delivery, weekly options signal engine (intraday) | Quantara |
| Heikin Ashi Doji, "C-2 + C-1", ratchet trailing stop, 7-point step, MongoDB per-user collections | OptionHABot |
| "C1+C2 momentum", 1-min HA candles, 2-lot multi-exit, SQLite, port 8765 | TradingBotA |
| Supabase, Razorpay, tradecopilot.in, Groq migration, React trading dashboard, rule engine | TradeCopilot |
| AI_SNIPP, content business, snippet library, creator tools, prompt library | AI_SNIPP |

### Workspace-level tasks (no single project)
Tasks touching `01_memory/`, `02_skills/`, `03_prompts/`, `06_agents/`, `07_templates/`, `08_mcp/`, or `09_docs/` are `AI_OS` tasks. Load the orchestration context defined in the Cross-Project Workflows section.

### Ambiguity handling
If no project is identifiable after the above rules, ask: "Which project does this relate to?" with the full project list as options. Do not guess.

---

## Stage 3 — Context Loading Rules

### Load order (mandatory sequence)
1. **Project memory file** — provides project state, open questions, architecture decisions
2. **CLAUDE.md** — provides workspace standards, canonical stack, operating rules
3. **Primary skill file** — matched from intent detection
4. **Supporting skill file** — if task spans two domains
5. **Project-specific docs** — if the task touches a documented subsystem

### Loading is not optional
Do not begin execution without loading the context files mapped to the project and intent. Partial context produces partial solutions that violate standards already decided.

### What "loading" means
Read each context file and internalize: constraints, prior decisions, standards, and open questions. Before writing code, check:
- Is there an equivalent pattern already solved in Quantara?
- Does a standard in CLAUDE.md prescribe this exact choice?
- Is there an open question in the memory file that this task would answer?

---

## Project Definitions

---

### AI_SNIPP

**Primary Objective:** Build and maintain the AI content business — reusable prompt templates, agent definitions, Claude snippets, tooling libraries, and creator content. Route extracted patterns from trading projects here.

**Location:** `D:\AI_OS\05_content\`

**Required Memory:** `D:\AI_OS\01_memory\ai_snipp_memory.md`

**Required Skills:**
- Primary: `ai-integration-engineer.md`
- Supporting: `python-backend-architect.md` (if building tooling)

**Required Context Files:**
- `D:\AI_OS\CLAUDE.md` § 6 (AI Agent Philosophy), § 10 (Reusability Standards)
- `D:\AI_OS\03_prompts\` — scan for existing templates before creating new ones
- `D:\AI_OS\06_agents\` — scan for existing agent definitions

**Output Expectations:**
- Prompt templates → `D:\AI_OS\03_prompts\` as `.md` files with metadata frontmatter
- Agent definitions → `D:\AI_OS\06_agents\` as `.md` files
- Reusable Python utilities → `D:\AI_OS\05_content\` as annotated `.py` files with usage examples
- Never create standalone AI_SNIPP deliverables that duplicate existing project code — extract and generalize

---

### Quantara

**Primary Objective:** Deterministic NIFTY weekly options signal engine operating as a Personal Hedge Fund OS. Three capital books (Investment, Swing, Intraday/F&O). Architecture frozen at v3.1. Phase 1 (Tier 0 survivability foundation) is the current implementation target.

**Location:** `D:\AI_OS\04_projects\Quantara` and `D:\AI_OS\06_agents\quantara\`

**Required Memory:** `D:\AI_OS\01_memory\quantara_memory.md`

**Required Skills:**
- `STRATEGY` tasks: `quantitative-analyst.md` + `python-backend-architect.md`
- `EXECUTION` tasks: `trading-systems-engineer.md` + `python-backend-architect.md`
- `INFRASTRUCTURE` tasks: `python-backend-architect.md` + `data-architect.md`
- `AI_INTEGRATION` tasks: `ai-integration-engineer.md` + `python-backend-architect.md`

**Required Context Files:**
- `D:\AI_OS\06_agents\quantara\QUANTARA_OS_MASTER.md` — frozen v3.1 spec, authoritative
- `D:\AI_OS\06_agents\quantara\05_risk-agent.md` — for any risk or kill switch work
- `D:\AI_OS\06_agents\quantara\00_system-overview.md` — for agent topology and event bus
- Relevant tier agent doc (04, 06, 07, 08, 09, 10, 11, 12) based on task
- `D:\AI_OS\CLAUDE.md` § 4 (Technical Standards), § 5 (Architectural Principles)

**Output Expectations:**
- All thresholds and parameters in YAML config. Zero magic numbers.
- All monetary values as integer paise. Float arithmetic on money = hard rejection.
- Append-only writes to: `order_state_transitions`, `audit_trail`, `alert_log`, `kill_switch_log`.
- All 13 pre-submission checks must remain intact on any execution path change.
- Claude never on the execution critical path (Engineering Rule 6 — pre-cache all AI context).
- Emergency Flatten Service (`port 8001`) must remain zero-dependency from main backend.
- Any new capability → confirm which tier it belongs to before writing code.

---

### TradeCopilot

**Primary Objective:** SaaS trading dashboard and rule engine live at tradecopilot.in. React 19 + TypeScript frontend, Supabase backend, Razorpay subscriptions, real paying users.

**Location:** `D:\AI_OS\04_projects\TradingCopilot` / `D:\tradecopilot`

**Required Memory:** `D:\AI_OS\01_memory\tradecopilot_memory.md`

**Required Skills:**
- `FRONTEND` tasks: `react-typescript-engineer.md` + `ai-integration-engineer.md`
- `INFRASTRUCTURE` tasks: `python-backend-architect.md` + `data-architect.md`
- `AI_INTEGRATION` tasks: `ai-integration-engineer.md` + `react-typescript-engineer.md`

**Required Context Files:**
- `D:\TradingBotwithAIAnalyzer\design_guidelines.json` — canonical design system, always load for any frontend work
- `D:\AI_OS\CLAUDE.md` § 4 TypeScript/React Standards
- Supabase schema files in the project — load before any schema change

**Output Expectations:**
- `"strict": true` in tsconfig. No `any`. Functional components only.
- Design system: dark mode, Tailwind, Radix UI. Typography: Chivo / IBM Plex Sans / JetBrains Mono.
- Palette: Emerald-500 (profit) · Red-500 (loss) · Indigo-600 (primary). No shadows.
- Server state: React Query. No global state libraries without justification.
- New AI features use Anthropic Claude, not Groq. Groq migration is active tech debt.
- Razorpay and Supabase keys are live. Any schema migration requires a versioned migration file.
- Regressions affecting paying users are P0 — fix before any new feature work.

---

### OptionHABot

**Primary Objective:** Multi-user Heikin Ashi Doji + Confirmation automated trading bot. Per-user session isolation, MongoDB per-user trade collections, 7-point ratchet trailing stop.

**Location:** `D:\AI_OS\04_projects\OptionHABot` / `D:\OptionHABot`

**Required Memory:** `D:\AI_OS\01_memory\optionhabot_memory.md`

**Required Skills:**
- `STRATEGY` tasks: `quantitative-analyst.md` + `trading-systems-engineer.md`
- `EXECUTION` tasks: `trading-systems-engineer.md` + `python-backend-architect.md`
- `INFRASTRUCTURE` tasks: `python-backend-architect.md` + `data-architect.md`

**Required Context Files:**
- `D:\AI_OS\CLAUDE.md` § 4 Python Standards, § 5 Multi-user isolation principle
- `D:\AI_OS\01_memory\optionhabot_memory.md` — session model, kill switch state

**Output Expectations:**
- Strategy: Doji (C-2 body ≤ 30% of range) + Bull Confirmation (C-1 bullish, closes > Doji high) → MARKET entry.
- Entry: LIMIT at LTP-1, 5s fill window, MARKET fallback if slippage < 3pts, cancel otherwise.
- Trailing stop: ratchet at 7-point steps. SL never moves backward. Hard SL cap: `MAX_SL_PTS = 7`.
- All risk state (kill switch, consecutive losses, daily P&L) is per-user. No shared state across users.
- MongoDB is the correct database for this project — do not suggest replacing it.
- `market_protection=-1` on every MARKET order. Non-negotiable.
- EOD square-off at 15:20 IST. No new signals after 14:00 IST.

---

### TradingBotA

**Primary Objective:** C1+C2 momentum strategy on 1-min Heikin Ashi option candles. 2-lot multi-exit model. SQLite persistence. Port 8765.

**Location:** `D:\AI_OS\04_projects\TradingBotA` / `D:\Trading_bot_a`

**Required Memory:** `D:\AI_OS\01_memory\tradingbota_memory.md`

**Required Skills:**
- `STRATEGY` tasks: `quantitative-analyst.md` + `trading-systems-engineer.md`
- `EXECUTION` tasks: `trading-systems-engineer.md` + `python-backend-architect.md`
- `INFRASTRUCTURE` tasks: `python-backend-architect.md`

**Required Context Files:**
- `D:\AI_OS\CLAUDE.md` § 4 Python Standards
- `D:\AI_OS\01_memory\tradingbota_memory.md` — backtest results, known state

**Output Expectations:**
- Strategy: C1 body ≥ threshold% of LTP + C2 breaks C1 high on 1-min HA candles. ATM-50/ATM/ATM+50.
- 2-lot exit model: Lot 1 exits at +30pts SL -15pts. Lot 2 SL → breakeven after Lot 1 exit, then trails.
- SQLite via `aiosqlite` — acceptable for this project's local-only scope. Do not propose PostgreSQL migration without business justification.
- Kill switch: 2 consecutive losses → size reduction, 5 consecutive → pause for day.
- `market_protection=-1` on every MARKET order.
- EOD square-off required. Hard cutoff for new signals at 15:15 IST.
- Backtest WR ~90% over 60 days. Any strategy change requires re-verification before live.

---

## Stage 4 — Execution Rules

### Before writing any code
1. Confirm which project and which intent are active.
2. Verify the relevant context files have been loaded.
3. Check: does Quantara already solve this? If yes — port the pattern.
4. Check: does CLAUDE.md prescribe this exact technical choice? If yes — follow it without deviation.
5. State what the change affects in the signal or execution flow before writing a single line.

### While writing code
- No hardcoded thresholds or time windows. Add to YAML config.
- No `any` in TypeScript. No untyped functions in Python.
- No blocking calls in async handlers.
- No silent failures. Every execution path logs its outcome to JSONL.
- No live orders without explicit `TRADING_MODE=live` and kill switch clear.
- No Claude API call without prompt caching on the system prompt block.
- No new dependency without checking if an existing one covers the need.

### Quality gate before completing a task
- Trading strategy change: state what fires differently and under what conditions.
- Execution change: verify `market_protection=-1` is present on all MARKET orders.
- Schema change: confirm a migration file was created.
- New Claude API call: confirm `cache_control: ephemeral` is applied to system prompt.
- Frontend change: confirm dark mode, correct typography, correct palette.
- Any live trading system change: confirm paper mode is the default and is verified.

---

## Stage 5 — Artifact Routing Rules

Every output produced by a task should be routed to its correct permanent home:

| Output Type | Target Location |
|---|---|
| Reusable prompt template | `D:\AI_OS\03_prompts\` |
| Agent definition or spec | `D:\AI_OS\06_agents\` |
| Reusable Python utility / snippet | `D:\AI_OS\05_content\` |
| Project scaffolding template | `D:\AI_OS\07_templates\` |
| MCP server config | `D:\AI_OS\08_mcp\` |
| Architecture decision | `D:\AI_OS\09_docs\` as `ADR-NNN.md` |
| Session context / learned state | `D:\AI_OS\01_memory\` |
| Project-specific code | Inside the project directory — do not pollute other projects |

**Extraction trigger:** If a pattern appears in two or more projects unchanged (e.g., Zerodha WebSocket client, LIMIT→MARKET fallback, Heikin Ashi candle builder), route to `05_content/` as a shared module and update all projects to import from it.

---

## Cross-Project Workflows

### AI_SNIPP ↔ Quantara

**Flow: Quantara → AI_SNIPP (extraction)**
Trigger: A Quantara component is general enough to be useful outside trading (e.g., YAML config loader, JSONL logger, kill switch pattern, FSM base class).
Steps:
1. Identify the component's interface — what it takes, what it returns, what it requires.
2. Strip all Quantara-specific business logic. The extracted module should have zero knowledge of NIFTY, Zerodha, or options.
3. Write to `D:\AI_OS\05_content\` with a header comment stating the origin and extraction date.
4. Update Quantara to import from the shared location.
5. Update `D:\AI_OS\01_memory\ai_snipp_memory.md` with the new artifact.

**Flow: AI_SNIPP → Quantara (prompt injection)**
Trigger: Quantara needs a new Claude prompt (e.g., new agent, new analysis type).
Steps:
1. Draft the prompt template in `D:\AI_OS\03_prompts\` first.
2. Test the prompt in isolation against representative inputs.
3. Wire into Quantara's AI cache layer (Redis hot → MongoDB warm → Claude API miss).
4. Add `cache_control: ephemeral` to the system prompt block.
5. Record the prompt key, TTL, and model selection in Quantara's agent doc.

---

### AI_SNIPP ↔ TradeCopilot

**Flow: TradeCopilot → AI_SNIPP (UI pattern extraction)**
Trigger: A TradeCopilot React component, hook, or design pattern is reusable across frontends.
Steps:
1. Identify the component — does it contain business logic or only presentation logic?
2. Extract presentation-only components to `D:\AI_OS\05_content\ui_components\`.
3. Document props, variants, and design tokens used.
4. Reference `D:\TradingBotwithAIAnalyzer\design_guidelines.json` — confirm extracted pattern is consistent with the canonical design system.

**Flow: AI_SNIPP → TradeCopilot (Claude migration)**
Trigger: A TradeCopilot feature currently using Groq needs to migrate to Claude.
Steps:
1. Load the existing Groq call — identify: prompt, expected output schema, call frequency.
2. Design the Claude equivalent using `tool_use` for structured output (not free text).
3. Add `cache_control: ephemeral` to the system prompt.
4. Determine model: Haiku for high-frequency, Sonnet for reasoning. Never Sonnet for Haiku-capable tasks.
5. Test the new call produces equivalent structured output before removing the Groq call.
6. Log Claude model, token count, and cache hit rate per call type.

---

### Quantara ↔ TradeCopilot

**Flow: Quantara → TradeCopilot (signal surface)**
Trigger: Quantara generates signals that should be visible in TradeCopilot's dashboard.
Steps:
1. Define the signal schema as a shared Pydantic model (Quantara side) / TypeScript type (TradeCopilot side).
2. Quantara writes signals to a shared PostgreSQL schema or Supabase table.
3. TradeCopilot reads via React Query with real-time subscription if latency-sensitive.
4. Signal data is read-only from TradeCopilot's perspective — no writes back to Quantara state.
5. Schema changes require a versioned migration on both sides simultaneously.

**Flow: TradeCopilot → Quantara (subscriber config)**
Trigger: A TradeCopilot subscriber sets trading preferences that Quantara should respect.
Steps:
1. Preferences live in TradeCopilot's Supabase database — Quantara reads, never writes.
2. Quantara fetches subscriber config at session start, not at signal time (avoid latency on critical path).
3. Config changes during an active session take effect at the next session start, not mid-session.
4. Validate config against Quantara's YAML bounds before applying — subscriber cannot override hard limits.

---

## Failure Handling Rules

### Ambiguous intent
- Do not guess. Ask one direct question: "Is this a strategy question, an execution question, or an infrastructure question?"
- Do not ask multiple clarifying questions at once. One question per turn.

### Ambiguous project
- Do not guess. List the five projects as options and ask which one.
- If the task genuinely spans multiple projects, identify the primary project (where the change lives) and list the secondary projects (where the impact lands).

### Missing context file
- If a required memory or docs file does not exist yet, state that explicitly before proceeding.
- Do not substitute with assumptions. Ask what the current state is, or inspect the live code to derive it.

### Conflicting standards
- CLAUDE.md takes precedence over a project's local convention.
- Quantara's implementation takes precedence over a general pattern when both exist.
- If two standards genuinely conflict, surface the conflict explicitly before choosing — do not resolve silently.

### Live trading system risk
- Any task that touches order placement, kill switch logic, position tracking, or EOD square-off is P0.
- State the exact code path that will change and what the failure mode is before writing code.
- Confirm paper mode is the test path. Never test execution logic against live Zerodha endpoints.

### Scope creep detection
- If completing the assigned task would require changing more than two files outside the stated scope, stop and confirm the expanded scope with the user before proceeding.
- Do not refactor surrounding code incidentally. A bug fix is not a refactoring opportunity.

---

## Priority Override Rules

These override all other routing and execution decisions:

1. **Open live position in any bot** → all other work stops until position is closed or incident resolved.
2. **TradeCopilot regression affecting paying subscribers** → P0. Fix before any feature work.
3. **Kill switch failure in any trading system** → P0. Trace and restore before resuming.
4. **Paper trading gate** → No system goes live without the minimum verified paper period. Requests to skip this gate are refused.
5. **Destructive git operations** → Require explicit confirmation every time, regardless of prior approvals.

---

## Quick-Reference Skill Matrix

| Task type | Primary skill | Supporting skill |
|---|---|---|
| Quantara signal logic or setup | `quantitative-analyst` | `python-backend-architect` |
| Quantara execution / order / kill switch | `trading-systems-engineer` | `python-backend-architect` |
| Quantara agent design or AI caching | `ai-integration-engineer` | `python-backend-architect` |
| Quantara database schema or migration | `data-architect` | `python-backend-architect` |
| OptionHABot / TradingBotA strategy | `quantitative-analyst` | `trading-systems-engineer` |
| OptionHABot / TradingBotA execution | `trading-systems-engineer` | `python-backend-architect` |
| TradeCopilot UI component or hook | `react-typescript-engineer` | `ai-integration-engineer` |
| TradeCopilot schema or Supabase | `data-architect` | `react-typescript-engineer` |
| TradeCopilot Claude / Groq migration | `ai-integration-engineer` | `react-typescript-engineer` |
| AI_SNIPP prompt or agent definition | `ai-integration-engineer` | — |
| AI_SNIPP utility extraction | `python-backend-architect` | `ai-integration-engineer` |
| Cross-project shared module | `python-backend-architect` | relevant project skill |
| AI_OS structure, memory, docs | orchestrator (this file) | — |
