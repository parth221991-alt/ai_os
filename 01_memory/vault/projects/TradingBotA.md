# TradingBotA

Tags: #project #trading #python #sqlite

**Status:** Active — backtest WR ~90% over 60 days, lacks CI/CD
**Priority:** P4
**Location:** `D:\AI_OS\04_projects\TradingBotA` / `D:\Trading_bot_a`

## What It Is
C1+C2 momentum strategy on 1-min Heikin Ashi option candles. 2-lot multi-exit.

## Strategy
- Instruments: ATM-50 / ATM / ATM+50 CE/PE
- Entry: C1 body ≥ threshold% of LTP + C2 breaks C1 high
- Lot 1: TP +30pts / SL -15pts
- Lot 2: TP +15pts / SL → breakeven after Lot 1 exit

## Stack
Python 3.12 · FastAPI · SQLite (aiosqlite) · Zerodha Kite Connect · HTML dashboard
Port: 8765

## Notes
SQLite is acceptable here — local-only tool. Production → PostgreSQL.

## Related
- [[Quantara]] (reference for kill switch, kill switch should be ported from here)
- [[OptionHABot]]
