# Workflow: Daily Founder Brief

**Owner:** Chief of Staff  
**Trigger:** 9:00 AM (after Research, Ops, Engineering, Growth have run)  
**Output:** `11_reports/archive/YYYY-MM-DD/founder_brief.md`  
**Duration:** ~5 minutes to generate, ~3 minutes to read  
**Founder action required:** Only on flagged exceptions

---

## Purpose

Consolidate the outputs of all morning workflows into a single, scannable brief that tells the Founder exactly what happened, what needs attention, and what can be ignored.

The brief must be readable in under 3 minutes. If it takes longer, it has failed its purpose.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| Research brief | `11_reports/archive/YYYY-MM-DD/research_brief.md` | Run workflow 02 first |
| Engineering health | `11_reports/archive/YYYY-MM-DD/engineering_review.md` | Run workflow 04 first |
| Growth metrics | `11_reports/archive/YYYY-MM-DD/growth_review.md` | Run workflow 05 first |
| Project health | `11_reports/archive/YYYY-MM-DD/project_health.md` | Run workflow 06 first |
| Open decisions from yesterday | `01_memory/decisions.md` | Claude reads automatically |
| Opportunities being tracked | `01_memory/opportunities/` | Claude reads automatically |

---

## Process

Claude (acting as Chief of Staff) will:

1. Read all input reports from today
2. Identify exceptions: anything that needs Founder action or awareness
3. Summarize each department in 2–4 bullet points
4. Flag exceptions prominently (🔴 P0 / 🟡 P1 / 🟢 OK)
5. List open decisions requiring Founder input
6. List one recommended focus for the day
7. Write to the archive

---

## Output Format

See template: `11_reports/templates/founder_brief.md`

---

## Escalation Rules

Founder must be interrupted immediately (not waiting for brief) if:
- Any live trading system is down during market hours
- Zerodha token has expired and bots cannot trade
- Razorpay/Supabase critical service failure
- Any unresolved incident from overnight

---

## Phase 2 Automation Plan

When Claude Code scheduled execution is available:
- Trigger at 9:00 AM IST (UTC+5:30) on weekdays
- All sub-workflows (02–06) must complete by 8:55 AM
- Output saved to archive
- Push notification to Founder with 2-line summary
