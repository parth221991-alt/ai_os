# Project History

**Purpose:** Per-project decision history, incident log, and milestone tracking.  
**Format:** One file per project, updated as events occur.

---

## Files in This Directory

| File | Project | Contents |
|---|---|---|
| `quantara.md` | Quantara | Paper trading milestones, architecture decisions, incidents |
| `tradecopilot.md` | TradeCopilot | Subscriber milestones, feature launches, incidents |
| `optionhabot.md` | OptionHABot | Session stats, incidents, user milestones |
| `tradingbota.md` | TradingBotA | Performance history, incidents, strategy changes |
| `ai_snipp.md` | AI_SNIPP | Reel milestones, audience growth, format experiments |
| `incidents.md` | All | Cross-project incident log |

---

## Entry Format

Each project file uses this format for new events:

```
## [DATE] — [Event Type]: [Title]
**Type:** Milestone / Decision / Incident / Launch / Change
**Impact:** P0 / P1 / P2 / Low
**Description:** [What happened in 2–3 sentences]
**Outcome:** [What was the result?]
**Lesson:** [What should be remembered for future decisions?]
```

---

## Incidents File

The `incidents.md` file is the cross-project operational incident log. Every incident that:
- Affected live trading
- Caused user-facing downtime
- Resulted in capital risk
- Revealed a systemic gap

...gets logged here with full details (what, when, duration, root cause, fix, prevention).
