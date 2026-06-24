# TradeCopilot Dashboard — Specification

**Audience:** Founder + Growth Director  
**Purpose:** SaaS growth metrics and product health  
**Update frequency:** Daily  
**Goal tracking:** Path to 1000 subscribers

---

## Layout

```
┌──────────────────────────────────────────────────────────┐
│  TRADECOPILOT                                [DATE]       │
│  Live at tradecopilot.in                                  │
├──────────────────────────────────────────────────────────┤
│  MRR          SUBSCRIBERS     CHURN        CONVERSION    │
│  ₹_____       ___             ___/mo       ___%          │
│  ▲ ___% WoW   ▲/▼ ___ WoW    Target: <5%  Free→Paid     │
├──────────────────────────────────────────────────────────┤
│  PATH TO 1000 SUBSCRIBERS                                 │
│  ████████░░░░░░░░░░░░░░░░░░  N/1000 (N%)                 │
│  At current growth: N months to target                    │
├──────────────────────────────────────────────────────────┤
│  PRODUCT HEALTH                                           │
│  Supabase: 🟢  |  Razorpay: 🟢  |  Frontend: 🟢         │
│  AI Analysis: Groq (⚠️ tech debt — migrate to Claude)     │
├──────────────────────────────────────────────────────────┤
│  RECENT SIGNUPS (last 7 days)                             │
│  [List: email | plan | date | source]                     │
├──────────────────────────────────────────────────────────┤
│  GROWTH EXPERIMENTS ACTIVE                                │
│  [List experiments with hypothesis and current data]      │
└──────────────────────────────────────────────────────────┘
```

---

## Data Specification

### Revenue Metrics
| Metric | Source | API |
|---|---|---|
| MRR | Razorpay subscriptions | `GET /v1/subscriptions` filter active |
| Active subscribers | Razorpay + Supabase | Count active + paid profiles |
| New signups | Supabase `auth.users` | Count by created_at |
| Churn | Razorpay cancelled subscriptions | Rolling 30-day |
| Conversion rate | (paid users) / (total users) | Computed |

### Product Health
| Service | Check | How |
|---|---|---|
| Supabase | API responding | `GET /rest/v1/` |
| Razorpay | Webhook endpoint responding | Health check |
| Frontend | `tradecopilot.in` loading | HTTP check |
| AI Analysis | Groq API responding | Health check (note: migration pending) |

### Growth Tracking
| Metric | Frequency | Target |
|---|---|---|
| Subscriber count | Daily | 1000 |
| MRR | Daily | ₹1L |
| Net growth (new – churn) | Weekly | Positive |
| Time to target (at current growth) | Weekly | < 12 months |

---

## Tech Debt Warning

The dashboard prominently shows the Groq → Claude migration status until resolved:
- **Current:** Groq (`llama-3.3-70b-versatile`) via frontend env var (security risk)
- **Target:** Claude Haiku via Supabase Edge Function (server-side, no key exposure)
- **Migration status:** [NOT STARTED / IN PROGRESS / COMPLETE]

This is a P1 security and architecture item. It surfaces here until closed.
