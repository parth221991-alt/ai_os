# AI_OS Project Templates

Project scaffolding templates for new builds. All templates follow AI_OS technical standards from CLAUDE.md.

## Available Templates

| Template | Description | Stack |
|---|---|---|
| `python-trading-bot/` | Async trading bot scaffold | Python 3.12 · FastAPI · asyncpg · YAML config · kill switch |
| `react-saas/` | SaaS dashboard scaffold | React 19 · TypeScript · Tailwind · Radix UI · Supabase |
| `shared-modules/` | Reusable patterns extracted from existing projects | Python utilities |

## Usage

Copy the relevant template to `D:\AI_OS\04_projects\<ProjectName>` and replace all `{{PLACEHOLDER}}` values.

## Patterns Pending Extraction

The following patterns exist in production projects and should be extracted here (see CLAUDE.md §10):

- **Zerodha WebSocket client** — identical in OptionHABot, TradingBotA, TradingBotwithAIAnalyzer → `shared-modules/zerodha_ws.py`
- **LIMIT→MARKET fallback order** — TradingBotA + TradingBotwithAIAnalyzer → `shared-modules/order_utils.py`
- **Kill switch / daily loss limiter** — Quantara is most robust → `shared-modules/kill_switch.py`
- **Heikin Ashi candle builder** — OptionHABot, TradingBotA, TradingBotwithAIAnalyzer → `shared-modules/ha_candles.py`
- **2-lot multi-exit risk model** — TradingBotA → `shared-modules/multi_exit.py`

Extraction is a Content Director + Engineering Director joint task (see backlog in 00_dashboard tasks.db).
