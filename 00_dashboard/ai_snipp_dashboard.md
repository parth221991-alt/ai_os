# AI_SNIPP Dashboard — Specification

**Audience:** Founder + Content Director  
**Purpose:** Content pipeline health and audience growth tracking  
**Update frequency:** Weekly (content metrics don't need daily refresh)

---

## Layout

```
┌──────────────────────────────────────────────────────────┐
│  AI_SNIPP                                    [DATE]       │
│  AI-First Content Company                                 │
├────────────────┬─────────────────┬────────────────────────┤
│ THIS WEEK      │ THIS MONTH      │ ALL TIME                │
│ Reels: N       │ Reels: N        │ Reels: N               │
│ Views: N       │ Views: N        │ Followers: N           │
│ Eng. rate: N%  │ Followers: +N   │ Avg views/reel: N      │
├────────────────┴─────────────────┴────────────────────────┤
│ CONTENT PIPELINE                                          │
│ Reel registry: REEL_NNN (latest)                         │
│ Next scheduled: [topic] on [date]                        │
│ Formula performance: F01: N avg | F02: N avg | ...        │
├───────────────────────────────────────────────────────────┤
│ TOP PERFORMING CONTENT                                    │
│ 1. [Reel title] — N views                                │
│ 2. [Reel title] — N views                                │
│ 3. [Reel title] — N views                                │
├───────────────────────────────────────────────────────────┤
│ CONTENT CALENDAR (next 7 days)                           │
│ [Day]: [Topic] | [Formula] | [Status]                    │
└──────────────────────────────────────────────────────────┘
```

---

## Data Specification

### Content Production
| Metric | Source | Notes |
|---|---|---|
| Reels produced | `reel_registry.md` | Count entries |
| Reels published | Manual update or platform API | Published ≠ produced |
| Next scheduled | `reel_registry.md` calendar | Next empty slot |
| Formula performance | Manual from platform analytics | Average views by formula |

### Audience Metrics (Manual until platform API available)
| Metric | Source | Refresh |
|---|---|---|
| Total followers | Platform analytics (manual) | Weekly |
| Weekly views | Platform analytics (manual) | Weekly |
| Engagement rate | Likes+comments / views | Weekly |
| Top content | Platform analytics (manual) | Weekly |

### Pipeline Health
| Status | Meaning |
|---|---|
| 🟢 ON TRACK | Reel ready for today |
| 🟡 QUEUED | Reel scripted, not produced in Flow |
| 🔴 GAP | No content for today — pipeline empty |

---

## Content Velocity Goal

At Phase 4, the target is:
- 5 reels/week published
- 1 longer-form piece/week (guide, post, thread)
- Fully automated pipeline (script → Flow → publish) for P1/P2 content
- Only P0 content requires Founder review before publishing

Current state (Phase 1): All content requires Founder approval before publishing.
