# Quantara Stage 1 — Design Decision Memo
**Date:** 2026-06-22
**Author:** Research Lead (AI_OS)
**Status:** Awaiting Founder Approval
**Blocking:** Stage 1 Live Capital Deployment (₹2–5L, Intraday F&O only)

---

## Research Basis

All recommendations below are grounded in:
- `QUANTARA_OS_MASTER.md` v3.1 (frozen architecture)
- `06_agents/quantara/12_emergency-flatten-service.md`
- `06_agents/quantara/07_execution-agent.md`
- `01_memory/quantara_memory.md`
- `06_agents/quantara/ROADMAP.md`
- CLAUDE.md technical standards and broker integration rules

Source code in `app/` is scaffolded (modules exist as `__init__.py` stubs and partial implementations). Key paths confirmed: `app/api/routes/emergency.py` exists but is read-restricted; the Flatten Service spec in `12_emergency-flatten-service.md` is the authoritative design.

---

## DQ-001: Zerodha TOTP Token Refresh

**Recommendation:** Semi-manual with automated 7:55 AM Telegram alert and a one-command token refresh script. Do NOT use fully automated Playwright for Stage 1.

**Rationale:**
The QUANTARA_OS_MASTER.md (Section 0.1) already specifies the exact policy: "Token refresh: attempt at 8:00 AM. Alert if fails. Manual intervention required by 8:45 AM or abort trading day." This is an established decision in the architecture. Fully automated TOTP via Playwright is fragile — Zerodha's 2FA page changes periodically, and a broken Playwright script at 8 AM with no fallback is worse than a manual step. For a solo founder, a 2-minute manual login at 7:55 AM is a low-cost, high-reliability solution. The risk of Playwright breakage during a live trading day is unacceptable at Stage 1.

The correct implementation is:
1. A Telegram bot alert fires at 7:55 AM: "QUANTARA: Token refresh required. Run /refresh before 8:45 AM."
2. A single CLI command (`python scripts/refresh_token.py`) that opens the Zerodha login flow, accepts TOTP input from terminal, retrieves the access token, and writes it to PostgreSQL (`zerodha_sessions` table) and the flatten service's env/PostgreSQL store.
3. The Zerodha Session Manager checks for a valid token at startup. If none by 8:45 AM, it alerts CRITICAL and sets state to FAILED — no trading that day.

**Implementation note:** Build `scripts/refresh_token.py` as a standalone script (not part of main backend) during Phase 1. It needs: `kiteconnect`, `asyncpg`, `python-dotenv`. Write the access token to PostgreSQL `system_checkpoints` table (or a dedicated `zerodha_sessions` table). The flatten service reads this token from PostgreSQL on startup (already specified in `12_emergency-flatten-service.md`, `get_access_token()` function).

**Founder action required:** YES — Confirm you accept a daily 2-minute manual login step as the Stage 1 operating procedure. Playwright automation can be added in Phase 3 if daily friction becomes a problem; for Stage 1, reliability > convenience.

---

## DQ-002: Fill Timeout at 45s — Convert to MARKET or Cancel?

**Recommendation:** Cancel the order, mark as MISSED, and do not resubmit. No automatic conversion to MARKET.

**Rationale:**
The architecture's Execution Engine section (QUANTARA_OS_MASTER.md) is explicit: "Never chase. A missed entry is better than a bad fill." The `07_execution-agent.md` confirms: if premium gapped >0.75R before entry, the trade is marked `missed_fill=True` and abandoned. The 45-second LIMIT timeout scenario is equivalent — if the market has not taken your limit price in 45 seconds, the setup has likely evolved.

More critically: converting a stale LIMIT to MARKET on an ambiguous status creates double-fill risk. The idempotency engine exists precisely to prevent this, but the safest protocol is: on ambiguous status at 45s, query Zerodha directly first. If the query confirms PENDING, cancel. If it confirms FILLED, accept the fill. If the status is still ambiguous after the query, cancel and mark MANUAL_REQUIRED. Never blindly convert to MARKET on ambiguity.

SEBI compliance (`market_protection=-1`) applies to any MARKET order placed, but placing a MARKET order without knowing if the LIMIT order already filled is a duplicate-order risk that no compliance flag can fix.

The existing architecture (MASTER.md Execution Engine, timeout at 30s in some specs, 45s in the question): the canonical behavior is query → if still pending → cancel → MISSED. No auto-MARKET conversion.

**Implementation note:** In `app/execution/order_manager.py` (to be built): implement `handle_fill_timeout()` as: (1) query Zerodha order status directly, (2) if PENDING: cancel via Kite API, record MISSED in `orders` table, (3) if FILLED: accept fill, update PostgreSQL, (4) if CANCELLED/REJECTED: record, do not retry, (5) if ambiguous: cancel, flag MANUAL_REQUIRED, alert Level 2 CRITICAL. Add this to the fill timeout YAML config parameter (`execution.fill_timeout_seconds: 45`).

**Founder action required:** YES — Confirm that you accept missed entries over ambiguous MARKET conversions. This is the conservative choice; it means the system will occasionally miss setups that would have worked. The alternative (auto-MARKET on timeout) has lower trade count but higher fill certainty at the cost of accepting any market price.

---

## DQ-003: NSE Holiday Calendar — Official Data Source

**Recommendation:** Use Zerodha's `kite.holidays(exchange="NSE", year=YYYY)` as the primary source, with a local YAML fallback file updated annually.

**Rationale:**
Zerodha's KiteConnect API provides a `holidays()` endpoint that returns the official NSE trading holiday list for a given year. This is the most operationally clean solution: (1) it uses the same API already integrated, (2) Zerodha's list matches NSE exactly (Zerodha is an NSE member and cannot afford to trade on a holiday), (3) no additional dependency or web scraping needed.

NSE's own website publishes the holiday calendar but requires scraping, which is brittle. The `exchange_holidays` Python package exists but is community-maintained and has had lag on announcements. The Zerodha API is authoritative for Quantara's purposes.

The YAML fallback is important: fetch and cache the holiday list at system startup each year, write to `configs/market_calendar.yaml`. If the API call fails, use the cached YAML. The system already has `configs/market_calendar.yaml` in its config set.

**Implementation note:**
```python
# In app/market/expiry_calendar.py (or session_clock.py)
# At startup:
holidays = kite.holidays(exchange="NSE", year=datetime.now().year)
# Cache to configs/market_calendar.yaml and Redis:
# quantara:cache:nse_holidays:{year}  TTL: 30 days
```
Refresh the cache on January 1 each year and on any trading-day anomaly detected (e.g., Zerodha WebSocket not available when expected to be).

**Founder action required:** NO — This is implementable directly. No Founder decision required. Confirm before Phase 2 build that the `kite.holidays()` API call is part of the startup sequence.

---

## DQ-004: Primary Options Chain Data Source

**Recommendation:** Zerodha WebSocket (KiteConnect) as the sole primary source for Stage 1. No external vendor required at Stage 1.

**Rationale:**
The QUANTARA_OS_MASTER.md Data Validity Engine already specifies options chain freshness requirements (<60s during market hours) and validates IV, OI, Greeks, and bid-ask spread. Zerodha's WebSocket provides full options chain data via instrument token subscriptions. For NIFTY weekly options (the only book active at Stage 1), this is sufficient.

External providers (Sensibull, Opstra) add cost (~₹2,000–5,000/month each) and an additional failure mode. At Stage 1 (1 position, intraday only), the complexity cost is not justified. Zerodha's feed has known limitations: OI data is delayed ~3–5 minutes at open, and the chain depth is shallower than Opstra. These are acceptable constraints at Stage 1 given the 60-second staleness threshold and the partial chain flag (if <80% of expected strikes received, the system already reduces F&O signal weight by 50%).

External supplemental data (Sensibull/Opstra) becomes justified at Stage 2 when the Swing book activates and multi-position IV surface analysis is required.

**Implementation note:** Subscribe to NIFTY option chain instruments via `kite.subscribe()` on WebSocket. The `app/ingestion/processing/chain_selector.py` file already exists — ensure it handles the partial chain scenario (PARTIAL flag, weight reduction) as specified in the Data Validity Engine. For the pre-market options chain analysis (8:45 AM step in the intelligence package), use Zerodha's REST API to fetch the full chain snapshot before WebSocket subscription.

**Founder action required:** NO — Implementable directly. Flag for review at Stage 2 planning whether Opstra or Sensibull should be added.

---

## DQ-005: Paper Trading Success Criteria

**Recommendation:** The following criteria must ALL be met before Stage 1 live capital:

| Criterion | Threshold | Rationale |
|---|---|---|
| Minimum trading days | 40 trading days | Already established in MASTER.md — non-negotiable |
| Minimum trade count | ≥ 60 completed trades | Statistical significance for a strategy with ~30–40% signal days |
| Win rate (intraday) | ≥ 60% | Already specified in ROADMAP Stage 0 criteria |
| Sharpe ratio (annualized, paper P&L) | ≥ 0.80 | Threshold for Stage 2 is >1.0; Stage 1 entry bar is lower |
| Maximum drawdown (paper) | < 15% of paper capital | Paper drawdown ceiling — tighter than Stage 1 live limit (10%) |
| No system errors for 5 consecutive trading days | Verified | Already in ROADMAP Stage 0 criteria |
| Reconciliation verified clean | ≥ 10 paper sessions | Confirm reconciliation engine works in paper simulation |
| Kill switch cascade tested | All 3 levels | Phase 1 Definition of Done requirement |
| Brier score | < 0.25 | Confidence calibration — confidence scores are probabilistically accurate |
| Maximum consecutive losses | ≤ 6 in any 10-trade window | Robustness check — not a random fluke |

**Sharpe calculation methodology:** Annualized Sharpe = (mean daily P&L / std daily P&L) × √250. Use paper P&L net of simulated slippage (the slippage model in `app/execution/slippage.py` must be applied to paper fills). Do not use gross P&L — it flatters the metric.

**Statistical note:** 60 trades at ~30% signal frequency over 40 days is achievable (approximately 1.5 trades/day average). The Sharpe of 0.80 at Stage 1 is a floor — it is below the Stage 2 requirement of >1.0 because Stage 1 capital (₹2–5L, 1 position) is a live testing phase, not a performance phase. The system should generate positive risk-adjusted returns, not necessarily optimal ones.

**Founder action required:** YES — Confirm the exact Sharpe threshold (0.80 recommended) and the minimum trade count (60 recommended). The win rate floor of 60% is already documented in the architecture. The Brier score threshold requires confirmation.

---

## DQ-006: Learning Reviewer Identity and Approval Process

**Recommendation:** Solo Founder weekly self-review, structured as a mandatory protocol with minimum evidence thresholds before any recommendation is eligible for review.

**Rationale:**
Since this is a solo founder operation, the "reviewer" is the Founder. The risk is not accountability (there is only one person) — it is cognitive bias, anchoring on recent performance, and approving changes during a drawdown when emotions are elevated. The protocol must protect against this.

**Recommended protocol:**

**Step 1 — Eligibility gate (automated, learning agent):**
A parameter recommendation is not surfaced for review until:
- Minimum 4 weeks of data post last parameter change (no reactive adjustments)
- Training window contains ≥20% bullish + ≥20% bearish regime days (anti-drift protection, already in MASTER.md)
- Shadow mode comparison has run for at least 5 trading days
- Recommendation is not triggered by a single extreme week (outlier filter)

**Step 2 — Weekly learning review (every Sunday, ~30 minutes):**
The learning agent produces a structured report (not raw data) containing:
1. The specific parameter(s) to change and the magnitude
2. Shadow mode: proposed vs. current performance over 5 days (Sharpe, win rate, trade count)
3. A counter-argument: what regime conditions would make the new params worse
4. The learning agent's confidence in the recommendation (0–1 scale)

**Step 3 — Founder decision criteria:**
- Approve only if shadow mode shows improvement AND the counter-argument has been considered
- Never approve during or immediately after (within 3 trading days of) a drawdown event
- Never approve more than 2 parameter changes per review cycle
- Document the reason for approval or rejection in `learning_recommendations` table

**Step 4 — Staging (5 trading days):**
Approved parameters run in shadow mode for 5 additional trading days before promotion to production. If staging diverges from expectation, reject and revert. As per MASTER.md, any approved change can be reverted in <5 minutes.

**Step 5 — Database enforcement:**
The learning service user has `WRITE` access to `learning_recommendations` only. It has no `UPDATE` permission on `strategy_parameters`. Promotion requires a separate authenticated API call (human-only endpoint, not automated). This is already specified in MASTER.md and is a database-level rule.

**Implementation note:** The weekly review report should be generated by the Learning Agent as a Telegram message or dashboard item, not an email. The Founder sees it on the same Telegram channel as alerts. The report template should be defined in `11_reports/templates/` as `weekly_learning_review.md`.

**Founder action required:** YES — Confirm Sunday as the review cadence and confirm you accept the "no approval during/after drawdown" rule as a self-imposed constraint.

---

## DQ-007: Max Capital at Risk Per Day — Stage 1 (Absolute Rupees)

**Recommendation:** ₹5,000 per day maximum daily loss limit for Stage 1 (₹2–5L capital base).

**Context for the Founder:**

For Stage 1 (₹2–5L capital, 1 NIFTY weekly option position at a time):

- **NIFTY lot size:** 75 units
- **Typical ATM NIFTY option premium at entry:** ₹150–400
- **Cost per lot:** ₹11,250–₹30,000 at entry
- **Max loss per position (per architecture):** 35–40% of premium (from `calc_sl()` in execution agent). At ₹200 premium, SL at ₹120 → max loss ₹6,000 per lot. At ₹150 premium, SL at ₹90 → max loss ₹4,500 per lot.

**Recommended daily loss limit: ₹5,000**

This means: if the day's P&L reaches -₹5,000, the system halts all trading for that day (Level 2 kill switch automatic trigger). At Stage 1 with 1 position and typical SL design, this is approximately 1 losing trade. The Consecutive Loss Governor (5 losses halts for the day) provides additional protection but the daily paise limit is the hard ceiling.

**Calibration:**
- On a ₹2L capital base: ₹5,000 daily limit = 2.5% of capital. Standard quant Stage 1 daily loss limit is 1–3% of capital.
- On a ₹5L capital base: ₹5,000 = 1% of capital. Conservative and appropriate.
- The Stage 1 success criterion requires drawdown <10% over 4 weeks (~20 trading days). At ₹5,000/day limit with ₹2L capital, 10% drawdown = ₹20,000, requiring 4 full loss-limit days out of 20. This is a realistic worst-case scenario for a system with ≥60% win rate.

**This number must be hardcoded in paise in `configs/risk.yaml`:**
```yaml
stage1:
  max_daily_loss_paise: 500000  # ₹5,000 in paise
```

**Founder action required:** YES — This is the Founder's decision. The ₹5,000 recommendation is a starting point. The Founder must confirm the exact number before any live capital is deployed. If starting with ₹2L, ₹5,000 is appropriate. If starting with ₹5L, consider ₹7,500 (1.5% of capital). Write the confirmed number in paise to `configs/risk.yaml` before enabling `execution_enabled: true`.

---

## DQ-008: Emergency Flatten Access If Main Backend Crashes

**Recommendation:** The Emergency Flatten Service (port 8001, standalone process) is the correct mechanism and is already fully specified. It must be supplemented with a Telegram bot command as a human-accessible trigger.

**What already exists (per `12_emergency-flatten-service.md`):**
The Emergency Flatten Service is a standalone Python process that:
- Runs on port 8001, bound to `127.0.0.1` (internal only)
- Has ZERO imports from the main backend
- Depends only on `postgresql.service` via systemd
- Accepts `POST /flatten` with an authorization code
- Reads positions directly from Zerodha (bypasses internal state)
- Places MARKET orders with `market_protection=-1`
- The spec is fully written; the service is NOT YET IMPLEMENTED

**The gap — human access when backend is crashed:**
Port 8001 is bound to `127.0.0.1` — it is not accessible from outside the VPS. If the main backend crashes, the Founder cannot reach port 8001 from a phone browser. There must be a human-accessible trigger that does not require SSH to the VPS.

**Recommended access mechanism:**

1. **Primary: Telegram bot command** — `/flatten {auth_code}` sent to the Quantara Telegram bot. The Telegram bot runs as a separate lightweight process (already in the stack — `app/telegram/` exists). When it receives `/flatten`, it calls `POST http://127.0.0.1:8001/flatten` internally. The Telegram bot process only needs to be running (not the main backend) — it can survive a backend crash if it is a separate systemd service.

2. **Secondary: Direct SSH command** — As a fallback, document the command in the runbook: `curl -X POST http://127.0.0.1:8001/flatten -H "Content-Type: application/json" -d '{"authorization_code":"XXXX"}'`. Founder must have SSH key access to the VPS at all times.

3. **Auth code access** — The authorization code is generated at Level 3 kill switch activation (per MASTER.md) and stored in `kill_switch_log`. Founders must also have a pre-generated emergency code stored securely (e.g., in a password manager or notes app on phone) for the scenario where the system itself generated Level 3. A static "break-glass" code, different from the dynamic kill-switch code, should be configured in the flatten service env file for manual human use.

**systemd dependency clarification:**
```
quantara-flatten.service
  Requires: postgresql.service
  Does NOT require: quantara-backend.service, mongod, redis-server
```
This means: if only the main backend crashes, the flatten service continues running independently. This is the correct design.

**Implementation note:**
- Phase 1 deliverable: Implement the standalone flatten service per the existing spec.
- Add a dedicated `quantara-telegram-alerts.service` (lightweight, separate from main backend) that handles `/flatten`, `/status`, and `/ack` commands.
- The "break-glass" static auth code must be set in `/etc/quantara-flatten/env` (mode 600) during VPS provisioning.
- Runbook must be written before Phase 1 is complete (already a Phase 1 DoD requirement).

**Founder action required:** YES — Confirm the Telegram bot command approach is acceptable. Confirm you have a mechanism (SSH keys, VPS access on phone) to reach the VPS directly if Telegram is also unavailable. Confirm the break-glass static auth code is acceptable for manual emergency use.

---

## Summary: Decisions Requiring Founder Input

| DQ | Decision Type | Founder Input Required | Recommendation |
|---|---|---|---|
| DQ-001 | Operating procedure | YES | Accept daily 2-min manual login; Playwright deferred to Phase 3 |
| DQ-002 | Order behavior | YES | Cancel on ambiguous timeout; accept missed entries |
| DQ-003 | Data source | NO | Implement Zerodha `kite.holidays()` directly |
| DQ-004 | Data vendor | NO | Zerodha WebSocket only for Stage 1 |
| DQ-005 | Success criteria | YES (partial) | Confirm Sharpe ≥ 0.80 and min 60 trades thresholds |
| DQ-006 | Governance process | YES | Confirm Sunday review cadence and self-constraint rules |
| DQ-007 | Capital at risk | YES (hard decision) | Confirm exact rupee amount (recommend ₹5,000/day) |
| DQ-008 | Emergency access | YES | Confirm Telegram bot command approach and break-glass code |

**Decisions implementable without Founder input:** DQ-003, DQ-004

**Decisions requiring written Founder confirmation before code is written:** DQ-001, DQ-002, DQ-005, DQ-006, DQ-007, DQ-008

---

## Estimated Implementation Effort

| DQ | Implementation | Effort | Phase |
|---|---|---|---|
| DQ-001 | `scripts/refresh_token.py` + Telegram 7:55 AM alert | 4–6 hours | Phase 1 |
| DQ-002 | `handle_fill_timeout()` in `app/execution/order_manager.py` | 2–3 hours | Phase 2 |
| DQ-003 | `kite.holidays()` call in startup + YAML cache + Redis TTL | 2 hours | Phase 1 |
| DQ-004 | No new work — use existing WebSocket + chain_selector.py | 0 hours | Phase 2 |
| DQ-005 | Paper trading evaluation script + report template | 4 hours | Phase 2 |
| DQ-006 | Weekly learning report template + Telegram report generation | 6 hours | Phase 4 |
| DQ-007 | Config value in `risk.yaml` + paise constant in risk engine | 30 minutes | Phase 2 |
| DQ-008 | Standalone flatten service (full implementation) + Telegram bot command | 16–20 hours | Phase 1 |

**Total estimated effort (all DQs):** 35–42 hours, spread across Phase 1–4.

---

## Next Steps

1. Founder reviews this memo and provides written decisions on DQ-001, 002, 005, 006, 007, 008.
2. Engineering Director begins Phase 1 implementation for DQ-001 (token refresh script), DQ-003 (holiday calendar), DQ-008 (flatten service).
3. DQ-007 confirmed number is hardcoded in paise in `configs/risk.yaml` before `execution_enabled` is ever set to `true`.
4. This memo is filed at `D:\AI_OS\11_reports\archive\2026-06-22\quantara_design_decisions.md`.
5. `open_decisions.md` updated with recommendations (see Research Lead update).
