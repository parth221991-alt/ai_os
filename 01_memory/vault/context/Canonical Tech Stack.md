# Canonical Tech Stack

Tags: #context #standards #architecture

## Backend
- Python 3.12+ · FastAPI · asyncio
- Type annotations on all signatures (mypy/pyright)
- Pydantic for all external data validation
- black + ruff (line-length 100)

## Frontend
- React 19 · TypeScript · Tailwind CSS · Radix UI (shadcn/ui pattern)
- Design reference: `D:\TradingBotwithAIAnalyzer\design_guidelines.json`
- Dark mode only. No shadows. Flat solid backgrounds with 1px borders.
- Typography: Chivo (headings) · IBM Plex Sans (body) · JetBrains Mono (numerics)
- Palette: Emerald-500 (profit) · Red-500 (loss) · Indigo-600 (primary)

## Databases
- PostgreSQL via asyncpg or Supabase (primary)
- MongoDB via Motor (OptionHABot only — per-user dynamic collections)
- SQLite/aiosqlite (local-only tools like TradingBotA only)
- Every table: `id UUID PK`, `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`

## AI Models
- `claude-sonnet-4-6` — default reasoning, code, architecture
- `claude-haiku-4-5` — high-throughput classification, real-time UI
- `claude-opus-4-7` — most complex reasoning only, explicit justification required
- Ollama local — embeddings, classification, batch jobs

## Broker
- Zerodha Kite Connect 5.x
- All MARKET orders: `market_protection=-1` (SEBI compliance)
- LIMIT → MARKET fallback: LIMIT at LTP+2, wait 10s, convert if slippage < 4pts

## Config Standard
- All thresholds in YAML files. Zero hardcoded parameters.
- [[Quantara]] is the reference implementation.

## Port Assignments
| Project | Ports |
|---|---|
| Quantara | 8000, 8001, 8002 |
| TradingBotwithAIAnalyzer | 8003, 3002 |
| OptionHABot | 8004, 3001 |
| TradingBotA | 8765 |
| TradeCopilot | 3000 |
| CareerPilot | 8005, 3003 |

## Related
- [[AI Agent Philosophy]]
- [[Quantara]]
