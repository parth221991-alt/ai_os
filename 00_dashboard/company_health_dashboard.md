# Company Health Dashboard — Specification

**Audience:** Founder + Operations Manager  
**Purpose:** Infrastructure uptime, costs, incidents, and compliance  
**Update frequency:** Daily (ops check) + Real-time during market hours

---

## Layout

```
┌──────────────────────────────────────────────────────────┐
│  COMPANY HEALTH                              [DATE]       │
├──────────────────────────────────────────────────────────┤
│  INFRASTRUCTURE STATUS                                    │
│  AWS Lightsail:  🟢  |  Supabase:  🟢  |  Railway:  🟢  │
│  Quantara:       🟢  |  TradeCopilot:  🟢               │
│  OptionHABot:    🟢  |  TradingBotA:  🟢                │
├──────────────────────────────────────────────────────────┤
│  ZERODHA                                                  │
│  Token status: ✓ Valid | Expires: [TIME IST]             │
│  Market hours: [PRE / OPEN / CLOSED]                     │
├──────────────────────────────────────────────────────────┤
│  MONTHLY COSTS                                            │
│  AWS: ₹___ | Supabase: ₹___ | Anthropic: ₹___           │
│  Total: ₹___ | Budget: ₹___ | Variance: ▲/▼ ___         │
├──────────────────────────────────────────────────────────┤
│  INCIDENT LOG (last 30 days)                             │
│  Open: N | Resolved: N | MTTR avg: N hours               │
│  [List open incidents]                                    │
├──────────────────────────────────────────────────────────┤
│  COMPLIANCE & SECRETS                                     │
│  Groq key in frontend: ⚠️ EXPOSED (migrate to server)    │
│  Razorpay key: ⚠️ CHECK git history (may be exposed)     │
│  All other secrets: ✓ Server-side only                   │
└──────────────────────────────────────────────────────────┘
```

---

## Data Specification

### Infrastructure Health
| Service | Check Method | Alert Threshold |
|---|---|---|
| AWS Lightsail | EC2 health check | Unreachable > 2 min |
| Supabase | REST health endpoint | Response > 5s |
| Quantara backend | `localhost:8000/health` | Down > 1 min during market |
| OptionHABot | `localhost:8004/health` | Down during active session |
| TradingBotA | `localhost:8765/health` | Down during market hours |

### Zerodha Token Status
| Check | Method | Alert |
|---|---|---|
| Token validity | API call to Kite | Invalid → interrupt Founder |
| Expiry time | Token decode | < 2 hours to expiry → warn |
| Market status | Time check IST | Inform context |

### Cost Tracking
| Service | Billing Cycle | Notes |
|---|---|---|
| AWS Lightsail | Monthly | Check AWS console |
| Supabase | Monthly | Free tier until exceeded |
| Anthropic API | Monthly | Track by project tag |
| Railway | Monthly | If used |

### Compliance Register
| Item | Status | Priority |
|---|---|---|
| Groq key in TradeCopilot frontend | ⚠️ Open | P1 — migrate to Edge Function |
| Razorpay key git history | ⚠️ Review | P1 — rotate if committed |
| All `.env.example` files current | ✓/✗ | Check quarterly |
| Paper trading gate intact (Quantara) | ✓ | Confirm `execution_enabled: false` |

---

## Port Conflict Monitor

All projects have assigned ports. This panel turns 🔴 if a conflict is detected:

| Project | Backend | Frontend | Status |
|---|---|---|---|
| Quantara | 8000 | — | 🟢 |
| Emergency Flatten | 8001 | — | 🟢 |
| TradingBotwithAI | 8003 | 3002 | 🟢 |
| OptionHABot | 8004 | 3001 | 🟢 |
| CareerPilot | 8005 | 3003 | 🟢 |
| TradingBotA | 8765 | — | 🟢 |
| TradeCopilot | — | 3000 | 🟢 |
| AI_OS Dashboard | — | 3999 | Reserved |
