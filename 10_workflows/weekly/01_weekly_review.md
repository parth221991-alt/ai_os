# Workflow: Weekly Company Review

**Owner:** Chief of Staff  
**Trigger:** Sunday, 7:00 PM  
**Output:** `11_reports/archive/YYYY-MM-DD/weekly_company_review.md`  
**Duration:** ~20 minutes to generate, ~10 minutes to read  
**Founder action required:** Resource allocation decisions, strategic direction

---

## Purpose

Step back from daily operations. Review the week as a CEO, not an operator. Assess progress against goals, identify what's working and what's not, and make 1–3 decisions that shape the next week.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| Daily briefs from the week | `11_reports/archive/YYYY-MM-DD/` | Claude reads all 5 |
| TradeCopilot MRR (week close) | Razorpay | Provide current MRR |
| Quantara paper trading results (if active) | Quantara logs | Provide win rate, P&L |
| Content published this week | `reel_registry.md` | Claude reads automatically |
| Engineering work completed | Git logs / memory | Describe major completions |
| Open decisions from the week | `01_memory/decisions.md` | Claude reads automatically |
| Opportunities being tracked | `01_memory/opportunities/` | Claude reads automatically |

---

## Review Structure

### Section 1: Business Health (5 minutes to write)
- Revenue: MRR this week vs. last week
- Trading: Quantara P&L (paper or live), OptionHABot sessions
- Content: Reels published, follower growth, best performing piece

### Section 2: Engineering Progress (3 minutes)
- Features shipped this week
- Bugs fixed
- Technical debt addressed
- What was NOT done (and why)

### Section 3: Strategic Review (5 minutes)
- Is Quantara on track for paper trading milestone?
- Is TradeCopilot growing toward 1000 users?
- Is AI_SNIPP building audience?
- What is the highest-leverage thing NOT being done right now?

### Section 4: Decisions Required (3 minutes)
- Open decisions that have aged past 7 days
- New decisions that emerged this week
- Rank by reversibility (easy to fix = can decide now; hard to fix = slow down)

### Section 5: Next Week Plan (3 minutes)
- Top 3 priorities for each product
- Any milestone dates in the next 7 days
- One experiment to run

---

## Output Format

See template: `11_reports/templates/weekly_company_review.md`

---

## Founder Commitment

After reading this report, the Founder should be able to answer:
1. Is the company moving toward its goals?
2. What needs my attention this week that nothing else can get?
3. What should the AI_OS departments focus on?

These answers should take <5 minutes. If they take longer, the report is too detailed.
