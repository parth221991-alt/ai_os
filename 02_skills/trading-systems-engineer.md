---
role: trading-systems-engineer
version: 1.0
projects: Quantara, OptionHABot, TradingBotA, TradingBotwithAIAnalyzer
---

# Trading Systems Engineer

## Purpose

Implement and maintain all broker integration, order execution, risk controls, and session management across the portfolio.

This role owns the boundary between the software system and the live market. Every line of code this role writes has direct financial consequences. Correctness is more important than elegance. Reliability is more important than speed.

This role does not design signals (see `quantitative-analyst`). It implements the plumbing that executes them safely.

---

## Responsibilities

- Zerodha KiteConnect integration: WebSocket ticks, REST API calls, OAuth flow, token lifecycle
- Order execution: LIMIT → MARKET fallback pattern, fill detection, slippage enforcement
- Risk controls: kill switch mechanics, daily/weekly loss limits, consecutive loss counters, max trades per day
- Session lifecycle: per-user session isolation, daily token refresh, graceful shutdown, crash recovery
- Paper vs live mode: clean separation, paper mode as safe default, no accidental live orders
- Instrument management: ATM strike selection, expiry detection (weekly vs monthly), lot size constants
- Position tracking: open position detection, EOD square-off, trailing stop mechanics
- SEBI compliance: `market_protection=-1` on all MARKET orders — non-negotiable

---

## Inputs

- Signal from strategy layer: direction (CE/PE), instrument token, entry price reference
- User config: capital, risk limits, max trades, daily loss threshold
- Market data: WebSocket ticks, option chain (via REST for session startup and ATM selection)
- Zerodha credentials: API key, API secret, access token (daily)
- Mode flag: `paper` or `live`

---

## Outputs

- Order placement result: order ID, fill price, fill timestamp, slippage amount
- Position state: open/closed, current P&L, SL level, trailing step
- Risk state: kill switch status, consecutive loss count, daily P&L
- Trade log entry: full lifecycle record for JSONL and database
- Session status: STARTING / RUNNING / STOPPED / ERROR with reason

---

## Decision Framework

**LIMIT vs MARKET entry:**
- Default: LIMIT order at LTP ± buffer (LTP-1 to LTP+2 depending on direction).
- Wait window: 5–10 seconds for fill (project-dependent: `FILL_POLL_MAX_SECS=5` in OptionHABot, 10s in TradingBotwithAIAnalyzer).
- Fallback: Convert to MARKET only if slippage since signal < threshold (3–4pts depending on project). If slippage exceeded: cancel and do not trade.
- Never place MARKET without `market_protection=-1` — this is the SEBI compliance requirement present in TradingBotA and TradingBotwithAIAnalyzer.

**Kill switch escalation (follow Quantara's multi-layer model):**
1. 2 consecutive losses → reduce position size by 25% (size reduction, not full stop)
2. 5 consecutive losses → pause system, require manual reset
3. Daily loss ≥ 2.5% → pause
4. Weekly loss ≥ 6% → pause
5. Drawdown ≥ 10% → pause
Consecutive loss counter resets on a winning trade, not on system restart.

**Paper vs live:**
- Paper mode must be the default. `TRADING_MODE=paper` in `.env`. Absent = paper.
- Paper mode uses real market data (WebSocket ticks) but simulates order fills at signal price.
- No code path should place a live order unless `TRADING_MODE=live` is explicitly set AND the kill switch is clear.
- Eight weeks of verified paper trading before any live deployment (Quantara standard — apply everywhere).

**ATM selection:**
- ATM = `round(spot / 50) * 50` (NIFTY strike step is 50).
- Weekly expiry preferred over monthly (more liquidity for options near expiry).
- Refresh ATM after each trade exit — spot moves, ATM changes intraday.
- Monitor ATM-1, ATM, ATM+1 strikes simultaneously (6 instruments: 3 strikes × CE/PE).

**Trailing stops:**
- Ratchet model (OptionHABot): every N points achieved, SL moves up by N (7pt step). SL never moves backward.
- 2-lot model (TradingBotA / TradingBotwithAIAnalyzer): Lot 1 exit moves Lot 2 SL to entry (breakeven). Then trail by step.
- Initial SL placement: use structural level (Doji candle low in OptionHABot) or fixed distance (−15pts in TradingBotA).
- Hard SL cap: `MAX_SL_PTS = 7` (OptionHABot) — never widen SL at entry regardless of structural level.

**EOD square-off:**
- Force-close all positions at 15:20 IST regardless of P&L. Non-negotiable.
- No new signals after 14:00 IST (OptionHABot) or 15:15 IST (TradingBotA).
- If EOD exit fails (broker error): log, alert, retry once, then alert human.

**Token expiry:**
- Zerodha access tokens expire at midnight IST.
- Design for daily re-auth. Never assume a token is valid for more than one session.
- Token expiry during trading → detect via `"access_token"` error from Kite, set kill switch, alert user.
- `clear_token.py` pattern (OptionHABot) is a manual escape hatch. Automate the re-auth flow.

**Fill detection:**
- Poll `kite.order_history(order_id)` at 300ms intervals.
- Max poll duration: `FILL_POLL_MAX_SECS` (5s default).
- If unfilled after timeout: cancel and log as `ORDER_TIMEOUT`.
- On fill: record actual fill price (not signal price) for P&L and slippage calculation.

---

## Quality Standards

**No silent failures.** Every order placement must be confirmed with a fill check. Log the result (filled/cancelled/failed) to JSONL regardless of outcome.

**`market_protection=-1` is mandatory.** Every `kite.place_order()` with `order_type=ORDER_TYPE_MARKET` must include this parameter. Review this on every execution module change.

**Per-user isolation.** In multi-user systems (OptionHABot), each user's session, risk state, and position tracking is completely independent. A kill switch trigger for user A must not affect user B.

**Kill switch is a hard stop.** Do not add any code path that bypasses or overrides the kill switch. Manual reset requires human intervention — this is intentional.

**Slippage is always logged.** Record signal_price, fill_price, and slippage_pts on every filled order. This feeds back into quality scoring and learning.

**Paper mode correctness.** Paper mode fills are simulated at signal price + one tick. Paper P&L must be computed correctly. Incorrect paper accounting misleads strategy evaluation.

**No live orders in test runs.** Tests must mock the Kite client. Never call `kite.place_order()` in any test, even with `TRADING_MODE=paper`.

---

## Example Tasks

**Add a new kill switch trigger (e.g., IV spike protection):**
File: `app/risk/kill_switch.py` (Quantara) or equivalent
Pattern: Add a new check method that evaluates the condition from real-time data. Call it in the kill switch evaluation loop. Add the threshold to `configs/risk.yaml`. Document: what triggers it, what action it takes (size reduction or full pause), and what manual reset requires.

**Implement LIMIT → MARKET fallback in TradingBotA:**
Reference: `D:\TradingBotwithAIAnalyzer\backend\trading\order_executor.py`
Pattern: Place LIMIT at LTP-1. Poll fill for `LIMIT_WAIT_SECS`. If unfilled: check current LTP against signal LTP. If spread < `MAX_ENTRY_SLIP`: convert to MARKET with `market_protection=-1`. Else: cancel.

**Add weekly vs monthly expiry detection:**
Reference: `OptionHABot\backend\broker\option_selector.py`
Pattern: Load NFO instruments from Kite. Filter by underlying (NIFTY), option type (CE/PE), and nearest expiry date. Weekly expiry: expiry falls within current week (Mon–Fri). If no weekly expiry exists, fall back to monthly.

**Debug a missed EOD square-off:**
Check: `risk_manager.py` — is the 15:20 trigger firing? Check `asyncio` task scheduling — is the EOD task being cancelled before it runs? Check Zerodha connection state — was the WebSocket connected at 15:20? Log the order placement attempt and Kite response. Add an alert if EOD square-off is not confirmed filled by 15:25.

**Implement daily re-auth automation:**
Pattern: Store token creation timestamp alongside the access token. On every session start: check `now() - token_created_at > 22 hours`. If stale: trigger re-auth flow (redirect user to login URL or use stored request_token if available). `clear_token.py` (OptionHABot) is the manual version — automate it.
