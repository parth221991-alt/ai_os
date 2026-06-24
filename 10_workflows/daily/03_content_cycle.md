# Workflow: Daily Content Cycle

**Owner:** Content Director  
**Trigger:** 10:00 AM  
**Output:** Reel script + Flow prompts OR content brief, saved to `05_content/AI_SNIPP/`  
**Duration:** ~15–20 minutes to generate

---

## Purpose

Produce one publishable content piece per day via the AI_SNIPP pipeline. Content is the primary acquisition channel for brand building. The pipeline must run daily with minimal Founder involvement.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| Content calendar status | `05_content/AI_SNIPP/reel_registry.md` | Claude reads automatically |
| Today's topic | Calendar OR research brief | From workflow 02 or content calendar |
| Formula for today (F01–F11) | Content calendar | Pre-planned or Claude selects |
| Priority (P0/P1/P2) | Founder judgment | Default P1 unless event-driven |

---

## Decision Tree

```
Is there a P0 event today (breaking AI news, trending topic)?
  YES → Trigger create_reel skill with event as topic, P0 priority
  NO  → Check content calendar for scheduled topic
        → Use scheduled topic + formula
        → If no calendar entry → Claude selects from backlog
```

---

## Process

Claude (acting as Content Director) will:

1. Check `reel_registry.md` for today's scheduled content
2. Confirm no P0 event overrides the schedule
3. Select formula based on topic type
4. Invoke `/create-reel` skill with topic, formula, priority
5. Save output to `05_content/AI_SNIPP/REEL_NNN_topic.md`
6. Update `reel_registry.md` with today's entry
7. Report to Chief of Staff: reel produced, ready for Flow generation

---

## Content Calendar Rhythm

| Day | Content Type | Formula |
|---|---|---|
| Monday | Tactical tool/hack | F02 (Hook + Demo) |
| Tuesday | AI concept explained | F01 (Discovery) |
| Wednesday | Quantara / trading insight | F07 (Before/After) |
| Thursday | Community prompt or challenge | F05 (Framework) |
| Friday | Week-in-AI recap | F11 (Listicle) |

---

## Metrics to Track (Weekly)

- Reels produced vs. reels published
- Average views per reel (by formula)
- Follower delta week-over-week
- Best-performing topic category

---

## Quality Gate (Before Publishing)

- [ ] Script is English only (no Hinglish)
- [ ] All Flow SCRIPT fields have word count within per-clip limits
- [ ] Discovery narrative style (not instructional)
- [ ] Watermark coverage confirmed in Flow prompts
- [ ] CTA is specific, not generic
