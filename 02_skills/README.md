# Skills Framework

Seven expert roles covering 100% of work across the AI_OS portfolio.
Each file is an implementation-ready context document — load the relevant one before starting work in that domain.

**Start here:** `ai_os_orchestrator.md` is the primary entry point for all work. It detects intent, identifies the project, loads the correct context, and tells you which skill(s) to activate.

| Skill | File | Projects |
|---|---|---|
| **AI_OS Orchestrator** | `ai_os_orchestrator.md` | ALL — load this first |
| Python Backend Architect | `python-backend-architect.md` | All Python projects |
| Trading Systems Engineer | `trading-systems-engineer.md` | All trading bots |
| Quantitative Analyst | `quantitative-analyst.md` | Quantara (primary), all bots |
| React / TypeScript Engineer | `react-typescript-engineer.md` | TradeCopilot, TradingBotwithAIAnalyzer |
| AI Integration Engineer | `ai-integration-engineer.md` | All (AI OS goal) |
| Data Architect | `data-architect.md` | All (different DB per project) |

## How to use

1. Load `ai_os_orchestrator.md` first — it maps the task to the correct project and skills.
2. Load the primary skill identified by the orchestrator.
3. Load the supporting skill if the task spans two domains.

Most tasks require 2 skills: one for the domain (Quant Analyst, Trading Systems) and one for the craft (Python Backend, React).

## Coverage map

| Task type | Primary skill | Supporting skill |
|---|---|---|
| New FastAPI route in any Python project | python-backend-architect | trading-systems-engineer (if execution-related) |
| New trading strategy or signal | quantitative-analyst | python-backend-architect |
| Zerodha order execution change | trading-systems-engineer | python-backend-architect |
| React component or hook | react-typescript-engineer | ai-integration-engineer (if AI-connected) |
| Supabase schema change | data-architect | react-typescript-engineer |
| Claude/Ollama integration | ai-integration-engineer | python-backend-architect or react-typescript-engineer |
| Database schema design | data-architect | python-backend-architect |
| Kill switch or risk rule | trading-systems-engineer | quantitative-analyst |
