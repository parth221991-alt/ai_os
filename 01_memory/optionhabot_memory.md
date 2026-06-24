# OptionHABot — Project Memory

**Last Updated:** 2026-06-08  
**Status:** Active — live multi-user trading bot  
**Port:** 8002

---

## Project Overview

OptionHABot is a multi-user automated trading bot based on the Heikin Ashi Doji + Confirmation pattern on 5-minute ATM option candles. It is the most architecturally mature of the smaller bots, featuring per-user session isolation and MongoDB-based trade storage.

**Stack:** Python 3.11 · FastAPI · MongoDB (Motor) 8.2 · Zerodha Kite Connect · HTML/JS frontend  
**Location:** `D:\AI_OS\04_projects\OptionHABot`  
**Start command:** `start.ps1` (PowerShell)

---

## Business Context

- Multi-user system — multiple traders can run sessions simultaneously without interference
- Each user gets isolated: trading session, position tracking, risk limits, trade history
- Not a subscriber SaaS — appears to be for a controlled group of users (not public)
- Revenue model: [PLACEHOLDER — direct use or subscription? Unclear from codebase]

---

## Current State

- **Python version:** 3.11 (oldest in the portfolio — upgrade path to 3.12 is a backlog item)
- **MongoDB version:** 8.2 (Motor async driver)
- **Auth:** JWT-based user authentication
- **Frontend:** Plain HTML/JS (not React)
- **CI/CD:** None — manual deployment
- **Test suite:** None — no pytest files found
- **Anthropic package:** `anthropic==0.28.0` installed in requirements.txt but **not wired to any agent**

---

## Trading Strategy

### Entry Signal
- **C-2 candle:** Heikin Ashi Doji (body ≤ `DOJI_BODY_MAX_PCT`% of range, configurable; currently 40%)
- **C-1 candle:** Bull confirmation candle — breaks above C-2 high
- **Entry:** MARKET order at C-1 close on 5-min ATM options

### 7-Point Ratchet Trailing Stop
| Price Move | Action |
|---|---|
| +7 points from entry | Move SL to breakeven (entry price) |
| +14 points | Lock in +7 points (SL = entry +7) |
| +21 points | Lock in +14 points (SL = entry +14) |
| +N points | Lock in +(N-7) points |

This ratchet continues indefinitely — the stop only moves up, never down.

### Risk Parameters
| Parameter | Value | Notes |
|---|---|---|
| `DOJI_BODY_MAX_PCT` | 40% | Max body as % of candle range to qualify as Doji |
| `TRAIL_STEP_PTS` | 7 | Points per ratchet step |
| `MAX_TRADES_PER_DAY` | 6 | Per-user daily trade limit |
| `DEFAULT_MAX_DAILY_LOSS_RS` | ₹20,000 | Per-user daily loss limit |
| `NIFTY_LOT_SIZE` | 65 | **May be outdated** — NIFTY lot size changed to 75 |

---

## Architecture

### Per-User Isolation (Key Design Decision)
Each user gets their own MongoDB collections:
- `trades_{user_id}` — trade history
- `positions_{user_id}` — open positions

This is why MongoDB was chosen over PostgreSQL for this project: dynamic collection creation per user is idiomatic in MongoDB and would be awkward in a relational schema.

### Multi-User Session Management
- Each user runs an isolated `TradingSession` object
- Per-user risk limits applied independently
- One user hitting their loss limit does not affect other users
- JWT auth ensures session isolation at the API layer

### Data Flow
```
Zerodha WebSocket → HA Candle Builder → Signal Detector → Risk Check → Order → MongoDB
```

---

## Important Constraints

1. **NIFTY lot size must be verified**: `NIFTY_LOT_SIZE=65` may be wrong. Current NIFTY lot size is 75. This affects position sizing and P&L calculations — **verify before next session**.
2. **No test suite**: Any code change is untested. Adding pytest is a Phase 1 priority.
3. **Python 3.11**: One minor version behind the AI_OS standard (3.12). Not urgent but should be tracked.
4. **Anthropic installed but unused**: `anthropic==0.28.0` adds a dependency with no benefit. Either wire it to an agent or remove it from requirements.txt.
5. **No CI/CD**: Deployment is manual. If the server crashes, recovery is manual.
6. **HTML/JS frontend**: Not aligned with canonical React 19 + TypeScript stack. Acceptable for an internal tool — not acceptable if it becomes subscriber-facing.
7. **`start.ps1`**: Windows-specific startup. VPS deployment would require a Linux equivalent.

---

## Architectural Decisions

- **MongoDB over PostgreSQL**: Per-user dynamic collections are idiomatic in MongoDB. Creating 100 PostgreSQL tables (one per user) would be an antipattern. This is a justified deviation from the AI_OS default.
- **Motor (async)**: Correct choice for FastAPI async context.
- **Plain HTML/JS frontend**: Acceptable for internal multi-user tool. If subscriber-facing, migrate to React.
- **JWT auth**: Standard for multi-user API. Correct choice.
- **Anthropic package (unused)**: Likely installed speculatively for future AI features. Should be removed or wired up.

---

## Known Risks

1. **NIFTY lot size discrepancy**: If `NIFTY_LOT_SIZE=65` but actual lot size is 75, all position sizing and P&L calculations are wrong by ~15%.
2. **No kill switch**: Unlike Quantara, there's no documented kill switch or daily loss halt mechanism beyond `DEFAULT_MAX_DAILY_LOSS_RS`. Verify this limit is actually enforced in code.
3. **No test suite**: Behavioral changes cannot be validated automatically. Any code change could introduce silent bugs.
4. **No CI/CD**: Version control exists (implied) but deployments are manual — risky for a live trading bot.
5. **WebSocket reconnection**: Kite Connect WebSocket drops are common. Verify reconnect logic is implemented.
6. **Market SEBI compliance**: Verify `market_protection=-1` is present on all MARKET orders.

---

## Future Opportunities

1. **Wire Anthropic package**: Add signal quality analysis or session summaries using Claude Haiku.
2. **Add pytest suite**: Cover signal detection, risk limits, and order flow.
3. **Add CI/CD**: GitHub Actions for automatic testing on push.
4. **Port kill switch from Quantara**: Add the 2/5 consecutive loss governor and daily drawdown halt.
5. **Upgrade to Python 3.12**: Align with AI_OS standard.
6. **Extract Heikin Ashi builder to shared module**: Same logic exists in TradingBotA and TradingBotwithAIAnalyzer.

---

## Open Questions

1. Is `NIFTY_LOT_SIZE=65` still correct? NIFTY lot size changed to 75 — verify in Zerodha instruments API.
2. What is the exact user base? How many concurrent users are expected?
3. Is `market_protection=-1` present on MARKET orders? (Required for SEBI compliance)
4. What happens when a user's daily loss limit is hit? Is trading halted automatically?
5. Where is the deployment hosted? Windows server or VPS?
6. Is there a reconnect handler for Zerodha WebSocket disconnections?

---

## Important Learnings

- **MongoDB's per-user collection pattern works well**: For multi-user trading tools where each user has a different trade history, MongoDB's dynamic collection creation is a genuine architectural advantage over relational schemas.
- **Unused dependencies are debt**: `anthropic==0.28.0` in requirements.txt with no usage means an install cost, a dependency update burden, and confusion. Wire it or remove it.
- **Lot size validation must be hardcoded**: Never hardcode broker-specific lot sizes without a validation check against the live instruments API. They change without notice.
