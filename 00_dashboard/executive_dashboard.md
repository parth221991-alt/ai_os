# Executive Dashboard — Specification

**Audience:** Founder  
**Purpose:** Single-screen view of the entire company  
**Update frequency:** Daily (populated from today's Founder Brief)

---

## Layout

```
┌─────────────────────────────────────────────────────────┐
│  AI_OS EXECUTIVE DASHBOARD          [DATE] [TIME]       │
├─────────────────────────────────────────────────────────┤
│  COMPANY STATUS                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ 🟢 ENG   │ │ 🟢 OPS   │ │ 🟡 GROWTH│ │ 🟢 CONT  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────────────────┤
│  REVENUE           │  TRADING              │  CONTENT   │
│  MRR: ₹___         │  Quantara: PAPER      │  Reels: N  │
│  Users: ___        │  OptionHABot: ACTIVE  │  Views: N  │
│  Δ week: ▲/▼       │  TradingBotA: ACTIVE  │  Follow: N │
├─────────────────────────────────────────────────────────┤
│  OPEN DECISIONS                                          │
│  [List ordered by urgency]                               │
├─────────────────────────────────────────────────────────┤
│  EXCEPTIONS                                              │
│  [Any P0/P1 items requiring Founder action today]        │
└─────────────────────────────────────────────────────────┘
```

---

## Data Specification

### Company Status Panel
| Widget | Data Source | Type |
|---|---|---|
| Engineering status | `engineering_review.md` → overall status | Status indicator |
| Operations status | `project_health.md` → overall status | Status indicator |
| Growth status | `growth_review.md` → overall status | Status indicator |
| Content status | content cycle output → completion | Status indicator |

### Revenue Panel
| Metric | Source | Refresh |
|---|---|---|
| MRR | Razorpay subscriptions API | Daily |
| Active subscribers | Supabase auth.users + subscription status | Daily |
| Week-over-week delta | Compare to previous weekly review | Weekly |

### Trading Panel
| Metric | Source | Refresh |
|---|---|---|
| Quantara status | Quantara health endpoint | Daily |
| Quantara paper P&L | Quantara logs / report | Daily |
| OptionHABot session | OptionHABot health endpoint | Real-time (market hours) |
| TradingBotA status | TradingBotA health endpoint | Real-time (market hours) |

### Open Decisions Panel
| Field | Source |
|---|---|
| Decision text | `01_memory/decisions.md` |
| Age (days open) | Creation date |
| Priority | Assigned in decisions.md |

### Exceptions Panel
| Field | Source |
|---|---|
| Exception list | Today's Founder Brief exceptions section |
| Severity | P0 / P1 |
| Recommended action | Brief recommendation |

---

## Phase 4 Implementation Notes

- All panels pull from structured JSON outputs of each workflow
- Workflows must output both `.md` (human readable) and `.json` (machine readable) versions
- Dashboard polls `11_reports/archive/[today]/` for JSON files
- Real-time trading data uses WebSocket to OptionHABot / TradingBotA health endpoints
- Quantara data is read-only — dashboard does NOT interact with trading logic
