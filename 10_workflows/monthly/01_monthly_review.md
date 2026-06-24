# Workflow: Monthly Executive Review

**Owner:** Chief of Staff  
**Trigger:** Last Sunday of each month, 6:00 PM  
**Output:** `11_reports/archive/YYYY-MM/monthly_executive_summary.md`  
**Duration:** ~30 minutes to generate, ~15 minutes to read  
**Founder action required:** Strategy pivots, resource reallocation, product decisions

---

## Purpose

The monthly review is the Founder's strategic operating rhythm. Daily briefs are operational. Weekly reviews are tactical. Monthly reviews are strategic. This is where you decide if the portfolio is heading in the right direction — and make moves before small drifts become big problems.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| All weekly reviews from the month | `11_reports/archive/` | Claude reads automatically |
| MRR for the month (start vs. end) | Razorpay | Provide MRR |
| Quantara paper trading stats (full month) | Quantara logs | Win rate, Sharpe, Brier score |
| Content performance (monthly) | Platform analytics | Views, followers gained |
| Engineering: major completions | Git / memory | List shipped features |
| Costs for the month | Bank / invoices | AWS, API costs, subscriptions |
| Open opportunities | `01_memory/opportunities/` | Claude reads |
| Company history entries this month | `01_memory/company_history.md` | Claude reads |

---

## Review Structure

### 1. Financial Summary
- MRR (start, end, delta, %)
- Annualized run rate
- Monthly costs breakdown
- Net operating position (revenue – costs)

### 2. Product Progress Report
| Product | This Month | Goal | On Track? |
|---|---|---|---|
| Quantara | [paper trading status] | [milestone] | |
| TradeCopilot | [user count, MRR] | [1000 users] | |
| OptionHABot | [sessions run] | [stable ops] | |
| AI_SNIPP | [reels published, followers] | [audience goal] | |

### 3. Strategy Assessment
- What is working better than expected?
- What is underperforming vs. plan?
- Is the portfolio allocation (attention + time) correct?
- What would you do differently if starting this month over?

### 4. Opportunity Review
- Opportunities opened this month: [list]
- Opportunities closed (pursued or dismissed): [list]
- Top opportunity to pursue next month: [one]

### 5. Decisions Made This Month
- Log of major decisions made (summary from weekly reviews)
- Were they correct in hindsight?
- What patterns emerge from the decision log?

### 6. Priorities for Next Month
- Rank the products by where marginal attention creates maximum return
- Name 1–2 experiments to run
- Name 1 thing to STOP doing
- Confirm or revise the 90-day roadmap

---

## Output Format

See template: `11_reports/templates/monthly_executive_summary.md`

---

## Time Budget

The monthly review takes 90 minutes total: 30 to generate, 15 to read, 45 for the Founder to think, decide, and record decisions. Block it.
