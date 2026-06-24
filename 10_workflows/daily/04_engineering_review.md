# Workflow: Daily Engineering Review

**Owner:** Engineering Director  
**Trigger:** 9:30 AM  
**Output:** `11_reports/archive/YYYY-MM-DD/engineering_review.md`  
**Duration:** ~5 minutes to generate

---

## Purpose

Verify that all codebases are healthy, CI is passing, no critical bugs are open, and the tech debt backlog is tracked. Engineering should not require daily Founder attention — only exceptions surface.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| Quantara CI status | GitHub Actions | Check last run status |
| Open critical bugs | Memory / Founder knowledge | Describe any known issues |
| Recent code changes | `git log --oneline -10` in each project | Run in terminal |
| Test failures | CI output | Check GitHub |
| New technical debt discovered | Code review notes | Describe if any |

---

## Engineering Health Checklist

Claude (acting as Engineering Director) reviews:

### Quantara
- [ ] CI passing (lint + tests)
- [ ] No P0 bugs open
- [ ] Paper trading health (if in paper phase)
- [ ] Config files unchanged (no hardcoded values slipped in)

### TradeCopilot
- [ ] Build passing (Vite/TypeScript)
- [ ] Supabase auth functioning
- [ ] Razorpay webhook healthy
- [ ] No exposed API keys in frontend (audit `REACT_APP_*` vars)

### OptionHABot
- [ ] FastAPI backend starting cleanly
- [ ] MongoDB connection healthy
- [ ] WebSocket reconnect logic intact

### TradingBotA
- [ ] SQLite WAL mode enabled
- [ ] Kill switch logic unchanged
- [ ] 2-lot exit logic correct

### Cross-Project
- [ ] No port conflicts (per CLAUDE.md port assignments)
- [ ] All `.env.example` files current with actual `.env` structure

---

## Output Format

```
# Engineering Review — [DATE]

## Status Summary
| Project | Status | Last CI | Notes |
|---|---|---|---|
| Quantara | 🟢 / 🟡 / 🔴 | [date] | |
| TradeCopilot | | | |
| OptionHABot | | | |
| TradingBotA | | | |

## Open Issues
[List any P0/P1 bugs]

## Tech Debt This Week
[One item moved forward]

## Recommended Action
[If any — else "No action required"]
```

---

## Escalation Triggers
- P0 bug in live trading system → interrupt Founder immediately
- Security vulnerability discovered → interrupt Founder immediately
- CI failing for >24 hours → surface in Daily Brief
