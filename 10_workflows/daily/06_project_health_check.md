# Workflow: Daily Project Health Check

**Owner:** Operations Manager  
**Trigger:** 8:45 AM (before market open)  
**Output:** `11_reports/archive/YYYY-MM-DD/project_health.md`  
**Duration:** ~5 minutes to generate

---

## Purpose

Verify all live systems are operational before market hours. This is the pre-flight check. If anything is red, the Founder knows before the market opens, not after a missed trade.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| Zerodha API token status | Check if token valid | Try a simple API call or check expiry |
| OptionHABot service status | `http://localhost:8004/health` | Run health check |
| TradingBotA service status | `http://localhost:8765/health` | Run health check |
| Quantara service status | `http://localhost:8000/health` | Run health check |
| AWS Lightsail status (if Quantara on VPS) | AWS console | Check instance status |
| Any overnight incidents | Logs / notification | Any alerts received? |

---

## Health Check Protocol

### Tier 0 (Blocking — fix before market open)
- [ ] Zerodha token valid and will not expire during market hours
- [ ] OptionHABot running if user sessions active
- [ ] TradingBotA running if active
- [ ] Kill switch states are INACTIVE (not erroneously triggered)

### Tier 1 (Warning — note but may not block)
- [ ] Quantara paper trading health (if in paper phase)
- [ ] Database connections responding
- [ ] Redis responding (Quantara)
- [ ] MongoDB responding (OptionHABot)

### Tier 2 (Informational)
- [ ] AWS Lightsail CPU/memory normal
- [ ] Supabase service healthy (TradeCopilot)
- [ ] Any unusual error rates in logs overnight

---

## Zerodha Token Check Protocol

Zerodha access tokens expire at midnight. Before every trading day:
1. Verify token was refreshed (manual login or automated TOTP flow)
2. Confirm token expiry time is after 3:30 PM IST
3. If expired: alert Founder immediately — trading cannot proceed

---

## Output Format

```
# Project Health Check — [DATE] [TIME]

## System Status
| System | Status | Last Check | Notes |
|---|---|---|---|
| Zerodha Token | 🟢/🔴 | | Expires: |
| OptionHABot | 🟢/🟡/🔴 | | |
| TradingBotA | 🟢/🟡/🔴 | | |
| Quantara | 🟢/🟡/🔴 | | |
| Supabase | 🟢/🔴 | | |

## Overnight Incidents
[None / describe]

## Pre-Market Clearance
🟢 CLEAR — All systems go
🔴 BLOCKED — [reason] — Founder action required before trading

## Actions Required
[List any — else "None"]
```

---

## Escalation Triggers (Interrupt Founder Immediately)
- Zerodha token expired at market open time
- Any live bot with open position and service is DOWN
- Kill switch erroneously in Level 2 or 3 state
- AWS Lightsail instance unreachable
