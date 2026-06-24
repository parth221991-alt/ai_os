# Lessons Learned — AI_OS Institutional Memory

**Last Updated:** 2026-06-08  
**Purpose:** Cross-project learnings that should inform every future decision in this ecosystem.

---

## Technical Learnings

### T1: Float Arithmetic on Money Is a Bug Category
Integer paise arithmetic eliminates an entire class of rounding errors. `₹1,234.56 = 123456 paise`. The display layer converts. Every arithmetic operation stays in integer domain.

**Evidence:** Quantara's QUANTARA_OS_MASTER.md mandates this as an immutable rule. The risk: float rounding on a position size calculation could result in ordering 0 lots or fractional lots — both fatal.

**Apply to:** Every new trading system. Even when it feels unnecessary for small amounts.

---

### T2: API Keys in Frontend `.env` Are Public Keys
`REACT_APP_*` variables in a Create React App / Vite project are bundled into the JavaScript that ships to the browser. Any user can read them in the browser's network tab or by inspecting the bundle.

**Evidence:** TradeCopilot's `REACT_APP_GROQ_API_KEY` is exposed to every browser load. The Razorpay live key is in `.env` and may be in git history.

**Apply to:** Never put secrets in frontend `.env`. Use server-side Edge Functions or backend proxies. Audit every `REACT_APP_*` variable before deployment.

---

### T3: Unused Dependencies Are Silent Debt
`anthropic==0.28.0` in OptionHABot's requirements.txt adds install cost, update burden, and reader confusion — with zero benefit. Speculative dependencies installed "for later" become permanent fixtures.

**Apply to:** Only add a dependency when it is wired and used. Remove it immediately if the feature is deferred.

---

### T4: Lot Sizes Change Without Notice
Broker-specific constants (lot sizes, tick sizes, margin requirements) change periodically. Hardcoding `NIFTY_LOT_SIZE=65` when the actual current size is 75 is a 15% error in all position sizing calculations.

**Apply to:** Never hardcode instrument-level constants. Fetch from the broker's instruments API at startup and validate. Store in YAML config at minimum, with a startup validation step.

---

### T5: WebSocket Reconnect Logic Is Non-Negotiable
Kite Connect WebSocket connections drop. Without a reconnect handler with exponential backoff, a bot runs headlessly on stale data — placing orders based on prices that are minutes old.

**Apply to:** Every bot using Zerodha WebSocket must have: connection monitoring, reconnect with backoff, staleness detection (if no tick in N seconds → data is stale → halt trading).

---

### T6: SQLite WAL Mode for Async Writes
When using SQLite with `aiosqlite` in FastAPI, concurrent reads from the dashboard and writes from the trading engine can cause lock contention. WAL (Write-Ahead Logging) mode allows concurrent reads without blocking writes.

**Apply to:** Any SQLite usage in an async FastAPI application. Enable with `PRAGMA journal_mode=WAL`.

---

### T7: Append-Only Logs Are the Correct Audit Model
Financial event logs (orders, signals, no-trade decisions) should never be updated or deleted. Every event is a fact that happened. Append-only design makes replay, audit, and debugging dramatically simpler.

**Evidence:** Quantara's `order_state_transitions`, `audit_trail`, `kill_switch_log` are INSERT-only. The SHA-256 hash chain in Quantara's JSONL logging enables cryptographic replay verification.

**Apply to:** Every trading-related event store. Resist the urge to UPDATE when state changes — instead, INSERT a new transition record.

---

### T8: State Machines Prevent Undefined Transitions
Any process with >3 states benefits from an explicit FSM. Without it, states like "order sent but fill not confirmed" have undefined behavior.

**Evidence:** Quantara's FSM (IDLE → WATCHING → CANDIDATE → VALIDATING → SIGNAL_READY → IN_TRADE → EXITING → EXITED) prevents the bot from placing a second order while one is already in flight.

**Apply to:** Order management, session management, kill switch state, circuit breakers.

---

### T9: Local Pre-Filters Before AI Calls
Before calling Claude to analyze a setup, verify with deterministic logic that it passes hard gates. A setup that fails a simple confidence floor check (< 0.50) should never reach Claude — it wastes tokens and latency.

**Apply to:** Every AI call with a deterministic pre-condition. Gate first, call second.

---

### T10: Prompt Caching Is Not Optional at Scale
A system prompt sent 100 times without `cache_control: ephemeral` is 100× the input token cost. For trading systems that generate multiple signals per day, uncached system prompts become a material operating cost.

**Apply to:** Every Claude API call with a static system prompt. Add `cache_control` from day one — retrofitting is error-prone.

---

## Trading Learnings

### TR1: Black Swan Protocol — Do NOT Auto-Flatten Into a Black Swan
The instinct during a flash crash or circuit breaker event is to flatten immediately. This is wrong. Auto-flattening into a black swan locks in losses at the worst possible price. The correct response is stop-widening — let positions breathe through the shock, then reassess.

**Evidence:** Quantara's Black Swan Protocol explicitly specifies stop-widening as Phase 2, not immediate closure. Manual intervention is required for Phase 3 decisions.

**Apply to:** Every bot with stop management. Never fire a market flatten order in response to a volatility spike — check if it's a black swan first.

---

### TR2: Backtest Win Rate Is a Hypothesis
A 90% backtest WR over 60 days is statistically meaningful but not a live performance guarantee. Slippage, spread costs, market impact, execution delays, and regime changes degrade real performance by 10–30%.

**Evidence:** TradingBotA's documented ~90% WR is unverified in live trading.

**Apply to:** Never size up based on backtest performance. Trade minimum size until live P&L matches backtest expectations over ≥40 trading days.

---

### TR3: Candle Close Entries Reduce Whipsaw
Entering on candle close (not intrabar) eliminates entries based on wicks that never close at the entry price. Every bot in the portfolio that uses HA candles should enter on close, not on tick.

**Evidence:** Quantara's non-negotiable rule — no intrabar entries.

**Apply to:** All candle-based strategies.

---

### TR4: EOD Square-Off Is a Non-Negotiable for Options
Options held overnight (for a day-trading strategy) carry gap risk, theta decay, and margin changes. The 15:25 IST square-off is a hard risk limit, not a preference.

**Apply to:** All intraday options strategies.

---

### TR5: Consecutive Losses Signal Regime Change, Not Just Bad Luck
3+ consecutive losses in 60 minutes often indicates a regime shift (trending → choppy, or vice versa) that the strategy is not designed for. Automatic size reduction and halting prevents the most damaging drawdowns.

**Evidence:** Quantara's consecutive loss governor: 2 losses=−25% size, 3=−50%+alert, 4=pause 2h, 5=halt for day.

**Apply to:** Every automated trading bot. Port the governor from Quantara.

---

### TR6: Paper Trading Minimum Is 40 Trading Days
"It looks good on paper" after 2 weeks is insufficient. Statistical significance for a trading strategy requires ≥40 trading days (≥200 signals for a 5-min strategy) with measured Sharpe, win rate, and Brier score for confidence calibration.

**Apply to:** Every strategy before live deployment.

---

### TR7: Market Regime Determines Strategy Validity
A momentum strategy that works brilliantly in trending markets will lose consistently in range-bound markets. Regime detection is not optional — it determines which signals to listen to and which to ignore.

**Evidence:** Quantara's regime engine (ADX, ATR, A/D ratio, VWAP, VIX) feeds regime-adaptive signal weights. The same setup gets different weights in different regimes.

---

## Product Learnings

### P1: Security Cannot Be Retrofitted
TradeCopilot's Groq key exposure happened because the AI integration was added quickly. Moving it server-side requires refactoring the entire AI call path. Security must be designed in from the start.

---

### P2: SaaS Dependencies on Single Services Are Fragile
TradeCopilot is 100% dependent on Groq. If Groq goes down, all AI features fail with no fallback. Building against Claude from the start would give access to Anthropic's uptime SLA and the ability to switch models.

---

### P3: Staging Environment Is Not Optional for Live SaaS
TradeCopilot has paying subscribers. Schema changes tested directly on the production Supabase project are high-risk. A staging Supabase project should have been provisioned from day one.

---

### P4: pg_cron Is Powerful but Hard to Debug
pg_cron jobs run inside the database with no console output. Failures are silent unless explicitly logged to a table. Always add a `cron_log` table and log every job execution result.

---

### P5: Supabase Edge Functions Are the Right Abstraction for Solo SaaS
No server management, no auth middleware, no deployment pipeline. For a solo founder, the productivity gain is worth the lock-in. The edge function pattern should be the default for any serverless AI calls.

---

## AI Learnings

### AI1: Model Selection Matters More Than Optimization
Using Sonnet where Haiku suffices is a 5–10× cost multiplier. Using Haiku where Sonnet is needed produces worse-than-rule-based outputs. The decision rule: Haiku for classification and summarization, Sonnet for multi-step reasoning and synthesis.

---

### AI2: Structured Output Over Free Text
When the downstream consumer is code, use JSON mode or tool_use. Free text responses require parsing that breaks on edge cases. Structured outputs are type-safe and predictable.

---

### AI3: Cache First, Call Second
The cache-before-call protocol (Redis hot → MongoDB warm → Claude API) is the correct production pattern. Every Claude response that is deterministic given the same inputs should be cached. Most are.

---

### AI4: Claude on the Critical Path Is an Architecture Mistake
A 0.5–3s Claude call at signal evaluation time introduces unacceptable latency and availability risk for intraday trading. The pre-cached scenario approach (Quantara's pre-market batch) delivers the same adversarial quality without the execution dependency.

**The rule:** Claude assists, it does not gate. Failure of Claude must degrade gracefully, never block execution.

---

### AI5: Batch Operations Save 10–20× on Cost
20 news headlines → 1 Claude call with structured JSON output is 20× cheaper than 20 separate calls. Batching is always the correct pattern for high-volume AI tasks.

---

### AI6: Ollama for Local Classification
Pattern matching, candle regime classification, and embedding generation do not require frontier model capability. Running `mistral` or `llama3.2` locally via Ollama eliminates API cost for these tasks and removes the latency of a network call.

---

## Content Learnings

### C1: Extraction Must Be Deliberate
Reusable patterns do not automatically migrate to `05_content/`. Every time a pattern is copied from one project to another, it should instead be extracted to `05_content/` as the canonical version.

---

### C2: The Design System Is an Asset
`TradingBotwithAIAnalyzer`'s `design_guidelines.json` codifies typography, palette, spacing, and component patterns. This document should be the canonical reference for all new frontend development — not recreated per project.

---

## Mistakes to Avoid

1. **Groq key in frontend `.env`** — Never put API keys in React environment variables. They become public.
2. **Float arithmetic on monetary values** — Always use integer paise. No exceptions.
3. **Hardcoding lot sizes** — Fetch from broker instruments API and validate at startup.
4. **Installing unused dependencies** — Wire it or remove it. Never install speculatively.
5. **Skipping paper trading gate** — 40 trading days minimum. No shortcuts.
6. **Real-time Claude calls at execution** — Pre-cache everything that can be pre-cached.
7. **No kill switch on trading bots** — Every bot needs a daily loss limit and consecutive loss governor.
8. **No reconnect handler on WebSocket** — Kite Connect drops. Handle it or the bot runs on stale data.
9. **No staging environment for live SaaS** — Schema changes on production without staging are reckless.
10. **Auto-flattening into a black swan** — Stop-widening first, assess second, decide third.
11. **Treating backtest WR as live performance** — They are different things. Trade minimum size until live data validates.
12. **Silent cron job failures** — Every pg_cron job must log its result to a table. Silent failures are invisible failures.
