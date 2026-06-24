# Workflow: Daily Growth Review

**Owner:** Growth Director  
**Trigger:** 9:30 AM  
**Output:** `11_reports/archive/YYYY-MM-DD/growth_review.md`  
**Duration:** ~5 minutes to generate

---

## Purpose

Track TradeCopilot's growth metrics daily. Identify trends before they become problems. Surface opportunities before they close. The Founder should not need to check Razorpay or Supabase manually — this workflow surfaces what matters.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| New signups today/yesterday | Supabase dashboard | Check auth.users count |
| Active subscriptions | Razorpay dashboard | Subscription count + MRR |
| Churn (cancellations) | Razorpay dashboard | Cancelled subscriptions this week |
| Feature usage (any notes) | Founder observation | Any user feedback received? |
| Competitor news | News / social | Any competitor moves noticed? |

---

## Metrics Tracked

### Primary (check daily)
- New signups (D-1)
- Active paying subscribers (current)
- MRR (current vs. last week)
- Churn rate (rolling 7-day)

### Secondary (note if changed)
- Free-to-paid conversion rate
- Most used features
- Support/feedback themes

### Growth Experiments Active
- [List any A/B tests, pricing tests, or acquisition experiments running]

---

## Output Format

```
# Growth Review — [DATE]

## TradeCopilot Metrics
- New signups (yesterday): 
- Total active subscribers:
- MRR: ₹___ (▲/▼ vs. last week: __)
- Churn this week:

## Trend Assessment
[1–2 lines: is growth accelerating, stable, or declining?]

## Opportunity
[One action that could move the needle this week]

## Competitor Watch
[Any relevant competitor move or market signal]

## Recommended Action
[If any — else "No action required"]
```

---

## Weekly Growth Questions (answer in Weekly Review)

1. What is the primary acquisition channel this week?
2. What feature do users mention most?
3. What is the biggest friction point in onboarding?
4. What would double signups if fixed?

---

## Escalation Triggers
- MRR drops >10% week-over-week → flag in Daily Brief
- Churn spike (3+ cancellations in a day) → flag with reason analysis
- Razorpay payment failure pattern → interrupt Founder
