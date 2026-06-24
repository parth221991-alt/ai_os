# Architecture Decisions

Tags: #decisions #architecture

A living log of non-obvious architectural choices. Full ADRs live in `D:\AI_OS\09_docs\`.

## Decision Framework (evaluate in order)
1. **Correctness** — edge cases including market microstructure (gaps, reconnects, partial fills)
2. **Safety** — risk of unintended live trades, data loss, security exposure
3. **Auditability** — can a human trace every decision through logs 6 months later?
4. **Cost** — Claude vs Ollama, unnecessary broker API calls
5. **Simplicity** — composing simple things produces complex behavior safely
6. **Reusability** — does this belong in AI_SNIPP or templates?
7. **Performance** — only after correctness is proven and bottleneck is measured

## Standing Decisions

### MongoDB for OptionHABot
Per-user dynamic collections require document model. Deliberate, not tech debt.

### SQLite for TradingBotA
Local-only tool. Acceptable. Production services → PostgreSQL always.

### Groq in TradeCopilot
Tech debt. New features → Anthropic Claude. Migration is medium-priority backlog.

### Paper Gate (8 weeks minimum)
No system goes live without verified paper trading. Applies regardless of backtest performance.

### State Machines for Complex Flows
Any process with 3+ states uses explicit FSM. Prevents undefined transitions, enables replay.

### Append-Only Trade Logs
Trade outcomes and signal decisions are facts. Never update, only append. SHA-256 replay in Quantara.

### LIMIT→MARKET Fallback
LIMIT at LTP+2, wait 10s, convert to MARKET only if slippage < 4pts, else cancel. Identical in TradingBotA and TradingBotwithAIAnalyzer — extract to shared module.

## Patterns To Extract (backlog)
- [ ] Zerodha WebSocket client (identical in 3 projects)
- [ ] LIMIT→MARKET fallback order logic
- [ ] Kill switch / daily loss limiter (port from Quantara)
- [ ] Heikin Ashi candle builder
- [ ] 2-lot multi-exit risk model

## Related
- [[Quantara]] (reference architecture for all decisions)
- [[Canonical Tech Stack]]
