# AI_OS — Company Operating System Architecture

**Version:** 1.0  
**Date:** 2026-06-21  
**Status:** Design Approved — Phase 1 Active  
**Author:** Founder + Chief Architect (Claude Sonnet 4.6)

---

## 1. Mission Statement

AI_OS is not a collection of agents. It is a complete company operating system where:
- The **Founder** acts as capital allocator and strategic decision-maker
- The **Executive Layer** (AI agents) manages all operational work
- **Projects** are business units that report upward through the org
- Every recurring task has a workflow. Every workflow produces a report. Reports surface only exceptions to the Founder.

**Design principle:** The Founder's attention is the scarcest resource. AI_OS maximizes leverage by handling the predictable and surfacing only the irreversible.

---

## 2. Current State Audit (2026-06-21)

### What Exists
| Folder | Status | Notes |
|---|---|---|
| `01_memory/` | Partial | 7 project memory files. No company-level memory. |
| `02_skills/` | Good | 6 engineer persona skills for code generation. Keep. |
| `03_prompts/` | Empty | Needs population. |
| `04_projects/` | Active | All project codebases. Keep. |
| `05_content/AI_SNIPP/` | Partial | Content pipeline partially scaffolded. |
| `06_agents/quantara/` | Good | 15 Quantara-internal agent definitions. Keep as-is. No company-level agents exist. |
| `07_templates/` | Empty | Needs population. |
| `08_mcp/` | Empty | MCP configs TBD. |
| `09_docs/` | Quantara-only | 13 ADRs + architecture docs, all Quantara-specific. |

### What Is Missing
- `00_dashboard/` — does not exist
- `10_workflows/` — does not exist
- `11_reports/` — does not exist
- `06_agents/company/` — no company-level agents
- `01_memory/` company categories: opportunities, competitors, founder_preferences, company_history
- Company structure definition document

### What Should Be Relocated
- `architecture_inventory.md` at root → `09_docs/`
- `my-video/`, `voice.py`, `t01_voice.mp3` → not AI_OS structure (stray artifacts)

---

## 3. Company Structure

```
┌─────────────────────────────────────────────┐
│               FOUNDER                        │
│   Capital Allocator · Strategic Decisions    │
│   Approves: gates, spend, pivots, launches   │
└──────────────────┬──────────────────────────┘
                   │ reads: Daily Brief
                   │ approves: gate decisions
                   ▼
┌─────────────────────────────────────────────┐
│           CHIEF OF STAFF [AI]                │
│   Orchestration · Daily Brief · Exception    │
│   Routing · Cross-department coordination    │
└──┬──────┬────────┬──────────┬───────────────┘
   │      │        │          │         │
   ▼      ▼        ▼          ▼         ▼
 ENG    GROWTH  RESEARCH  CONTENT    OPS
DIRECTOR DIRECTOR DIRECTOR DIRECTOR MANAGER
 [AI]    [AI]     [AI]     [AI]     [AI]
```

### Reporting Flow
```
Projects → Department Directors → Chief of Staff → Founder
         (daily health)        (synthesis)     (exceptions only)
```

---

## 4. Department Definitions

### 4.1 Chief of Staff
**Role:** Orchestrator of the executive layer. The single interface between the Founder and all departments.

**Responsibilities:**
- Compile and deliver the Daily Founder Brief by 9:00 AM
- Route exceptions from any department to the Founder with context
- Track open decisions and follow through to closure
- Coordinate cross-department work (e.g., content about Quantara requires both Content and Research input)
- Own the Weekly Company Review and Monthly Executive Summary
- Maintain company memory (opportunities, competitor moves, open decisions)

**Does NOT own:** Any individual project. Does NOT duplicate Engineering, Growth, or Research work.

**Escalation trigger:** Any exception from any department that requires Founder decision within 24 hours.

---

### 4.2 Engineering Director
**Role:** Code health, technical delivery, and quality across all projects.

**Responsibilities:**
- Daily engineering health check: CI status, test coverage, open PRs, critical bugs
- Prioritize technical debt items from the backlog
- Review and approve architectural decisions for non-Quantara projects
- Ensure all new projects meet AI_OS technical standards (Python 3.12+, typed, tested, YAML config)
- Track port assignments and prevent conflicts
- Maintain the dependency matrix in `architecture_inventory.md`

**Projects owned:**
- Quantara (code health only — strategy is Research Director's domain)
- TradeCopilot (code + architecture)
- OptionHABot (code + bugs)
- TradingBotA (code + bugs)
- Future SaaS (bootstrap standards)

**Escalation triggers:** P0 bugs in live trading systems, security vulnerabilities, CI failures blocking production.

---

### 4.3 Growth Director
**Role:** SaaS metrics, user acquisition, and revenue growth for subscriber-facing products.

**Responsibilities:**
- Daily growth metrics pull: TradeCopilot signups, MRR, churn, Razorpay collections
- Weekly growth analysis: conversion funnel, feature adoption, user feedback themes
- Monthly growth report: MRR trend, cohort retention, CAC vs LTV
- Identify and prioritize growth levers (feature, pricing, channel, messaging)
- Draft marketing copy, landing page copy, email campaigns for Founder approval
- Track competitor SaaS products in the trading tools space

**Projects owned:**
- TradeCopilot (primary)
- Future SaaS products (intake + launch playbook)

**Escalation triggers:** MRR drops >10% week-over-week, churn spike, critical user complaint pattern.

---

### 4.4 Research Director
**Role:** Market intelligence, strategy R&D, and investment thesis development.

**Responsibilities:**
- Daily research brief: macro conditions, market regime, NSE/NIFTY developments
- Weekly strategy review: Quantara signal performance (at the business level — not duplicating internal agents)
- Identify new alpha sources and strategy ideas for Quantara roadmap
- Competitive intelligence on quantitative trading tools and strategies
- Research notes on emerging AI capabilities relevant to the portfolio
- Produce research memos for Founder review on major market events

**Projects owned:**
- Quantara (strategy direction — NOT internal execution logic)
- All projects (AI capability research)

**Does NOT:** Interfere with Quantara's internal agent logic. AI_OS monitors Quantara as a business; Quantara's agents manage the trading.

**Escalation triggers:** Significant market regime shift, new regulatory development affecting trading operations.

---

### 4.5 Content Director
**Role:** AI_SNIPP content pipeline — research, production, publishing, and distribution.

**Responsibilities:**
- Daily content pipeline: topic selection, script generation, reel production via Flow
- Maintain the content calendar and reel registry
- Ensure consistent brand voice across all platforms
- Track content performance metrics (views, engagement, followers)
- Identify high-performing content patterns and replicate
- Develop new content formats as the AI_SNIPP brand grows

**Projects owned:**
- AI_SNIPP (all content operations)

**Escalation triggers:** Viral content opportunity requiring rapid response, platform policy changes, collaboration requests.

---

### 4.6 Operations Manager
**Role:** System uptime, monitoring, incident response, and infrastructure costs.

**Responsibilities:**
- Daily ops check: all live trading systems healthy, no open incidents
- Monitor Quantara (as external monitor — NOT duplicating internal monitoring agent)
- Monitor OptionHABot session health during market hours
- Track AWS Lightsail, Supabase, Railway, and other infra costs
- Maintain incident log and post-mortems
- Ensure all secrets are current and not expired
- Port conflict monitoring
- Broker API status (Zerodha uptime, token refresh)

**Projects owned:**
- OptionHABot (daily operational oversight)
- TradingBotA (daily operational oversight)
- Quantara (external health monitoring)
- Infrastructure (all shared services)

**Escalation triggers:** Live trading system down during market hours (P0), API token expired, AWS cost spike >20%, incident not resolving within 30 minutes.

---

## 5. Project Ownership Matrix

| Project | Primary Owner | Secondary | Escalation | Priority |
|---|---|---|---|---|
| Quantara | Research Director | Engineering Director | Founder | P1 |
| TradeCopilot | Growth Director | Engineering Director | Founder | P2 |
| OptionHABot | Operations Manager | Engineering Director | Founder | P3 |
| TradingBotA | Operations Manager | Engineering Director | Founder | P4 |
| AI_SNIPP | Content Director | Chief of Staff | Founder | P5 parallel |
| Future SaaS | Chief of Staff (intake) | Growth Director | Founder | P6 |

**Override rule:** Any live trading system with an open position escalates to P0 immediately, overriding all other priorities.

---

## 6. Folder Structure (Complete)

```
D:\AI_OS\
├── 00_dashboard/          Executive and project dashboards (architecture)
│   ├── README.md
│   ├── executive_dashboard.md
│   ├── quantara_dashboard.md
│   ├── tradecopilot_dashboard.md
│   ├── ai_snipp_dashboard.md
│   └── company_health_dashboard.md
│
├── 01_memory/             Persistent company knowledge
│   ├── decisions.md       (exists — AI_OS-level decisions)
│   ├── lessons_learned.md (exists — cross-project learnings)
│   ├── quantara_memory.md (exists)
│   ├── tradecopilot_memory.md (exists)
│   ├── optionhabot_memory.md (exists)
│   ├── tradingbota_memory.md (exists)
│   ├── ai_snipp_memory.md (exists)
│   ├── founder_preferences.md  NEW — Founder working style, preferences
│   ├── company_history.md      NEW — Key milestones, pivots, launches
│   ├── opportunities/          NEW — Market opportunities being tracked
│   │   └── README.md
│   ├── competitors/            NEW — Competitor intelligence
│   │   └── README.md
│   └── project_history/        NEW — Per-project decision history
│       └── README.md
│
├── 02_skills/             Engineer persona skills (keep as-is)
│
├── 03_prompts/            Prompt templates for all workflows
│   ├── daily/
│   │   ├── founder_brief.md
│   │   ├── research_brief.md
│   │   ├── content_brief.md
│   │   ├── engineering_review.md
│   │   ├── growth_review.md
│   │   └── ops_health_check.md
│   ├── weekly/
│   │   └── company_review.md
│   └── monthly/
│       └── executive_summary.md
│
├── 04_projects/           Active project codebases (keep as-is)
│
├── 05_content/AI_SNIPP/   Content pipeline (keep as-is)
│
├── 06_agents/             Agent definitions
│   ├── company/           NEW — Company-level agents
│   │   ├── README.md
│   │   ├── chief_of_staff.md
│   │   ├── engineering_director.md
│   │   ├── growth_director.md
│   │   ├── research_lead.md
│   │   ├── content_director.md
│   │   └── operations_manager.md
│   └── quantara/          KEEP — Quantara-internal agents (untouched)
│
├── 07_templates/          Project scaffolding templates
│
├── 08_mcp/                MCP server configurations
│
├── 09_docs/               Architecture decisions + company docs
│   ├── COMPANY_OS_ARCHITECTURE.md  (this file)
│   ├── COMPANY_STRUCTURE.md
│   ├── decisions/         (ADR files — existing)
│   └── roadmaps/
│       └── COMPANY_OS_90DAY_ROADMAP.md
│
├── 10_workflows/          NEW — Workflow definitions
│   ├── README.md
│   ├── daily/
│   │   ├── 01_founder_brief.md
│   │   ├── 02_research_cycle.md
│   │   ├── 03_content_cycle.md
│   │   ├── 04_engineering_review.md
│   │   ├── 05_growth_review.md
│   │   └── 06_project_health_check.md
│   ├── weekly/
│   │   └── 01_weekly_review.md
│   └── monthly/
│       └── 01_monthly_review.md
│
└── 11_reports/            NEW — Report templates and archive
    ├── README.md
    ├── templates/
    │   ├── founder_brief.md
    │   ├── eod_report.md
    │   ├── weekly_company_review.md
    │   └── monthly_executive_summary.md
    └── archive/            Generated reports stored here by date
```

---

## 7. Automation Phases

### Phase 1: Manual Execution via Claude (Current)
- All workflows executed on-demand by invoking Claude
- Founder triggers workflows by asking Claude directly
- Claude populates report templates with available data
- Duration: Now through Day 30

### Phase 2: Scheduled Execution (Day 31–60)
- Daily brief auto-generated via Claude Code scheduled task
- Weekly review triggered automatically on Sunday evening
- Operations health check runs before market open (9:00 AM)
- Founder receives brief without having to ask

### Phase 3: Autonomous Execution with Exception Alerts (Day 61–90)
- Departments operate independently
- Only exceptions surface to Founder
- Push notification on P0 events
- Founder interacts with briefings, not with individual agents

### Phase 4: Dashboard-Driven Operation (Day 90+)
- Web dashboard renders live company health
- Founder approves/rejects queued decisions from the dashboard
- All departments report in real time
- New projects plug in via standard template

---

## 8. Key Constraints

1. **No AI on the critical path for live trading.** AI_OS monitors Quantara, OptionHABot, and TradingBotA. It does not intervene in execution.
2. **Quantara's internal agents are untouched.** `06_agents/quantara/` is Quantara's internal intelligence. AI_OS wraps it externally.
3. **Founder approval required for:** capital deployment, pricing changes, new product launches, live trading parameter changes, any spend >₹10,000/month new line item.
4. **Solo operation constraint.** Every agent definition must work with Claude Pro + Claude Code. No separate infrastructure required for Phase 1.
5. **Cost discipline.** Company-level agent calls use Claude Haiku (summaries, status checks). Claude Sonnet only for strategic reasoning, architecture decisions, and complex analysis.
