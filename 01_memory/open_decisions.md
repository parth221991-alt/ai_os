# Open Decisions — Founder Decision Queue

**Purpose:** Track decisions that require Founder input, with aging and context. Closed by Founder with a decision + reasoning. Chief of Staff surfaces aging decisions in the Weekly Review.  
**Format:** Newest first. Close decisions by moving to the archive section.

---

## Open Decisions

### DEC-003: Quantara Paper Gate — Start Date Confirmation
**Opened:** 2026-06-21
**Aging:** New
**Urgency:** P2 (planning)
**Decision needed:** Confirm when the 40-day paper trading clock formally starts.
**Context:** Paper gate requires 40 TRADING DAYS with ≥60% win rate, no system errors (5 consecutive days), calibration complete. The clock should start only when all systems are healthy and logging correctly.
**Options:**
- A: Paper trading already started (confirm date)
- B: Not started — identify what's needed to start the clock

---

### DEC-001: Groq → Claude Migration in TradeCopilot
**Opened:** 2026-06-08  
**Aging:** Ongoing  
**Urgency:** P1 (security) — Groq key is exposed in frontend `.env`  
**Decision needed:** Approve the migration plan and assign to Engineering Director  
**Options:**
- A: Migrate Groq → Claude Haiku via Supabase Edge Function (recommended — eliminates security risk, converges on Claude)
- B: Keep Groq, move it server-side only (reduces risk, doesn't converge tech stack)
- C: Defer (increases security exposure with each passing day)

**Recommendation:** Option A. The migration is low-risk (same AI use case, swap model + provider) and eliminates the frontend key exposure.

---

### DEC-002: Razorpay Live Key Git History Audit
**Opened:** 2026-06-08  
**Aging:** Ongoing  
**Urgency:** P1 (compliance)  
**Decision needed:** Authorize git history audit of TradeCopilot repo. If key was committed, rotate it.  
**Options:**
- A: Run `git log -p` to check if key was ever committed. Rotate immediately if found.
- B: Rotate proactively regardless (safest — costs nothing)

**Recommendation:** Option B. Rotate proactively. Razorpay key rotation takes 5 minutes. Git audit is slower and uncertainty is not worth the risk.

---

### DEC-003: Quantara Paper Gate — Start Date Confirmation
**Opened:** 2026-06-21  
**Aging:** New  
**Urgency:** P2 (planning)  
**Decision needed:** Confirm when the 40-day paper trading clock formally starts.  
**Context:** Paper gate requires 40 TRADING DAYS with ≥60% win rate, no system errors (5 consecutive days), calibration complete. The clock should start only when all systems are healthy and logging correctly.  
**Options:**
- A: Paper trading already started (confirm date)
- B: Not started — identify what's needed to start the clock

---

## Closed Decisions Archive

| Decision | Opened | Closed | Choice | Reasoning |
|---|---|---|---|---|
| DEC-004: DQ-001 TOTP refresh | 2026-06-22 | 2026-06-22 | Semi-manual: 7:55 AM Telegram alert + `scripts/refresh_token.py` | Reliability over convenience; Playwright deferred to Phase 3 |
| DEC-005: DQ-002 Fill timeout | 2026-06-22 | 2026-06-22 | Cancel on ambiguous 45s timeout, mark MISSED | Duplicate fill risk from auto-MARKET conversion outweighs missed entry cost |
| DEC-006: DQ-005 Paper criteria | 2026-06-22 | 2026-06-22 | 40 days + 60 trades + 60% WR + Sharpe ≥ 0.80 + Brier < 0.25 + DD < 15% | Statistical significance floor for Stage 1 promotion |
| DEC-007: DQ-006 Learning reviewer | 2026-06-22 | 2026-06-22 | Sunday self-review, 5-day shadow, no approval within 3 days of drawdown, max 2 changes/cycle | Solo operation — protocol enforces discipline in place of external accountability |
| DEC-008: DQ-007 Daily loss limit | 2026-06-22 | 2026-06-22 | ₹5,000/day (500000 paise) written to `configs/risk.yaml` | 2.5% of ₹2L base — within standard Stage 1 range (1–3%) |
| DEC-009: DQ-008 Emergency flatten | 2026-06-22 | 2026-06-22 | Telegram `/flatten {auth_code}` as primary + SSH fallback + break-glass static code in VPS env | Port 8001 internal-only; Telegram bot as separate systemd service survives backend crash |
| DEC-004a: DQ-003 NSE Holidays | 2026-06-22 | 2026-06-22 | Zerodha `kite.holidays()` + YAML cache | Uses existing integration; authoritative for NSE; no additional dependency |
| DEC-004b: DQ-004 Options Chain Data | 2026-06-22 | 2026-06-22 | Zerodha WebSocket only for Stage 1 | Cost-justified for 1-position intraday; external vendors deferred to Stage 2 |

---

## Decision Principles

1. **Reversible decisions** — make them fast. Wrong is better than stuck.
2. **Irreversible decisions** — slow down. Paper-test. Get it right.
3. **Aging >14 days** — Chief of Staff escalates with a recommendation to force a choice.
4. **Never make a decision in a brief** — decisions are made consciously, not in reaction to a summary.
