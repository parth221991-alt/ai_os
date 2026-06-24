# TradingBotA — Project Memory

**Last Updated:** 2026-06-08  
**Status:** Active — single-user automated trading bot  
**Port:** 8765  
**GitHub:** niftybot_alpesh (implied from codebase)

---

## Project Overview

TradingBotA is a single-user automated trading bot implementing a C1+C2 momentum strategy on 1-minute Heikin Ashi option candles. It uses a 2-lot multi-exit model (different TP/SL for each lot). It is the simplest and most focused bot in the portfolio — single user, SQLite database, minimal dependencies.

**Stack:** Python 3.12 · FastAPI · SQLite (aiosqlite) · Zerodha Kite Connect · HTML dashboard  
**Location:** `D:\AI_OS\04_projects\TradingBotA` / `D:\Trading_bot_a`  
**Start command:** `run.bat` (Windows batch file)

---

## Business Context

- Single-user operation (not multi-tenant)
- Documented backtest win rate of ~90% over 60 days — **this figure is unverified for live trading**
- Lower subscriber exposure than OptionHABot — likely personal or for a small group
- Revenue model: [PLACEHOLDER — personal use or small group? Unclear]

---

## Current State

- **Python version:** 3.12 ✓ (aligned with AI_OS standard)
- **Database:** SQLite via aiosqlite — appropriate for single-user local tool
- **Frontend:** HTML dashboard on port 8765
- **CI/CD:** None — manual deployment
- **Test suite:** None documented
- **Anthropic/AI integration:** None

---

## Trading Strategy

### C1+C2 Momentum Pattern (1-minute Heikin Ashi)
- **C1:** Heikin Ashi candle with body ≥ 0.5% of LTP (`body ≥ 0.005 × LTP`)
- **C2:** Next candle closes above C1 high — confirms the momentum direction
- **Entry:** MARKET order at C2 close on ATM-50 / ATM / ATM+50 CE or PE

### 2-Lot Multi-Exit Model
| Lot | Take Profit | Stop Loss | Notes |
|---|---|---|---|
| Lot 1 | +30 points | −15 points | Exits fully at TP or SL |
| Lot 2 | +15 points (after Lot 1 TP) | Moves to breakeven after Lot 1 TP; then trails +10pts | Stays open after Lot 1 closes |

**Lot 2 logic detail:**
1. Open both lots simultaneously at C2 close
2. When Lot 1 hits TP (+30pts): move Lot 2 SL to entry (breakeven)
3. Lot 2 then trails: every +10pts of additional move, ratchet SL up by +10pts
4. Lot 2 SL is -15pts from entry until Lot 1 TP fires

### Strike Selection
- ATM-50, ATM, ATM+50 CE/PE — standard near-the-money options
- [PLACEHOLDER — verify exact strike selection logic and which strikes get which lot allocation]

---

## Architecture

### Database Design
- **SQLite via aiosqlite**: Correct choice for single-user local tool. No PostgreSQL overhead.
- **Note:** If this bot ever becomes multi-user or moves to a VPS, SQLite must be replaced with PostgreSQL.

### Process Model
- Single Python process
- FastAPI serves the HTML dashboard
- Zerodha WebSocket connection for 1-min candle data
- Single user, single session — no isolation complexity

---

## Important Constraints

1. **Unverified live performance**: The ~90% backtest WR over 60 days is documented but has not been formally verified against live trading results. Do not assume live performance matches backtest.
2. **No CI/CD**: Manual deployment via `run.bat`. Any change requires manual restart.
3. **No test suite**: No pytest files documented. Behavioral validation is manual.
4. **SQLite is local-only**: Not suitable for VPS deployment without migration to PostgreSQL.
5. **No kill switch**: No documented daily loss limit or kill switch mechanism. This is a gap — port Quantara's risk model.
6. **1-minute candles**: Higher signal frequency than Quantara's 5-minute — more noise, requires lower C1 threshold (`0.005` vs Quantara's stricter gates).
7. **`run.bat`**: Windows-specific. VPS deployment requires Linux equivalent.

---

## Architectural Decisions

- **SQLite over PostgreSQL**: Single user, local operation, no concurrent writes. SQLite is the right choice — aligns with AI_OS guideline "SQLite acceptable for local-only tools."
- **Python 3.12**: Correct version — aligned with AI_OS standard.
- **HTML dashboard**: Acceptable for single-user internal tool. Not subscriber-facing.
- **No AI integration**: Momentum strategy is fully deterministic — Claude would add cost without benefit for this use case.
- **2-lot exit model**: Captures initial momentum (Lot 1) while running the winner (Lot 2). Common pattern in professional prop trading.

---

## Known Risks

1. **Backtest vs live gap**: 90% WR is a backtest figure. Market microstructure (slippage, spread, partial fills) typically degrades live performance by 10–20%. Live P&L must be tracked separately.
2. **No kill switch**: If the bot enters a losing streak, there is no automatic halt. The operator must manually intervene.
3. **SQLite concurrency**: If the HTML dashboard and the trading engine write to SQLite simultaneously, there can be lock contention. Verify WAL mode is enabled.
4. **1-minute frequency risk**: Higher candle frequency means more trades per day — overtrading risk if market conditions deteriorate.
5. **No WebSocket reconnect verification**: Kite Connect drops. Verify reconnect handler is implemented and tested.
6. **SEBI compliance**: Verify `market_protection=-1` is on all MARKET orders.

---

## Future Opportunities

1. **Port Quantara kill switch**: Add daily loss limit (₹X max) and consecutive loss governor.
2. **Add pytest suite**: Cover C1/C2 detection, 2-lot exit logic, and order flow.
3. **Paper trading mode**: Add a paper fill simulator so new strategy variants can be tested without capital risk.
4. **Extract shared patterns**: C1+C2 detection, HA candle builder, and 2-lot model are reusable — route to `D:\AI_OS\05_content\`.
5. **Performance attribution**: Track live vs backtest performance with a simple dashboard widget.

---

## Open Questions

1. What is the exact strike selection logic? (ATM-50/ATM/ATM+50 — which gets which allocation?)
2. Is there a daily trade limit? Is it enforced?
3. Is `market_protection=-1` on all MARKET orders?
4. Is SQLite WAL mode enabled to prevent lock contention?
5. Has live performance data been collected and compared to the 90% backtest WR?
6. Where is `run.bat` meant to be executed — local Windows machine or VPS?

---

## Important Learnings

- **Backtest WR is a hypothesis, not a fact**: A ~90% WR on 60 days of backtesting is promising but must be validated in live trading. Slippage, spread costs, and market impact are invisible in backtests but very real in execution.
- **2-lot exits are operationally complex**: The conditional SL-to-breakeven on Lot 2 requires careful state management. A bug here (moving SL too early, not moving it at all) has direct financial consequences.
- **SQLite is good until it isn't**: For single-user local tools it's excellent. The moment concurrency or remote access is needed, migrate early — retrofitting is painful.
- **Simple strategies need kill switches too**: Even a high-WR strategy can have a drawdown streak. Without an automatic halt, a bad day can erase weeks of gains.
