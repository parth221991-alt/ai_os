---
name: Create Reel
description: Generate a complete AI_SNIPP reel package - script, Flow prompts, assembly, caption, CTA, hashtags. Use when asked to create a reel, produce AI_SNIPP content, or generate a social media video. Args: topic, formula (F01-F11), priority (P0/P1/P2). Scripts are written as discovery narratives by a skilled scriptwriter persona — enthusiastic, interactive, specific — not instructional walkthroughs.
---

# /create-reel

This skill produces a complete AI_SNIPP reel package. One command → 9 production assets, copy-paste ready.

**Scriptwriter Persona:** All scripts are written from inside the experience — the creator has already used the tool, run the workflow, and measured the result. Scripts are discovery narratives, not tutorials. Every body beat uses interactive language techniques and enthusiasm markers from `script_writer_guide.md`. Instructional command chains ("go to X, click Y, copy Z") are banned as the primary script body.

## Invocation Syntax

```
/create-reel                              → full auto: Claude selects topic + formula
/create-reel [topic]                      → topic locked, formula auto-selected
/create-reel [formula]                    → formula locked (F01–F11), topic auto-selected
/create-reel [topic] [formula]            → both locked, immediate production
/create-reel [topic] [formula] [priority] → full spec (P0=now, P1=this week, P2=queue)
```

Arguments are in `$ARGUMENTS`.

---

## SYSTEM LOAD ORDER

Before producing any output, read these files in sequence. All rules, character identity, formulas, and production standards live in these canonical files — not here.

```
LOAD 1 — Execution contract (this file — already loaded)

LOAD 2 — Workflow engine:
  05_content/AI_SNIPP/daily_reel_generator.md

LOAD 3 — Production rules (Rules 1–20, output format, failure modes):
  05_content/AI_SNIPP/production_mode.md

LOAD 4 — Character system (read all four):
  05_content/AI_SNIPP/03_character/flow_seed_prompts.md
  05_content/AI_SNIPP/03_character/character_consistency_guide.md
  05_content/AI_SNIPP/03_character/prompt_blocks.md
  05_content/AI_SNIPP/03_character/visual_identity.md

LOAD 4 — Visual production standards:
  05_content/AI_SNIPP/flow_generation_template.md

LOAD 5 — Formula system:
  05_content/AI_SNIPP/02_formulas/formula_index.md
  05_content/AI_SNIPP/02_formulas/F[NN]_[name].md   ← selected formula only

LOAD 6 — Research layer (read all five):
  05_content/AI_SNIPP/01_research/hook_library.md
  05_content/AI_SNIPP/01_research/viral_pattern_library.md
  05_content/AI_SNIPP/01_research/cta_library.md
  05_content/AI_SNIPP/01_research/topic_evaluation_framework.md
  05_content/AI_SNIPP/01_research/script_writer_guide.md
```

Do not produce any output until all LOAD 2–6 files are read.

---

## EXECUTION FLOW

```
1. Parse $ARGUMENTS → lock topic / formula / priority if provided
2. Read all LOAD 2–6 files silently
3. Run topic selection (if needed) — priority order P0→P5 from daily_reel_generator.md
4. Run formula selection (if needed) — decision tree from formula_index.md
5. Run 6 hard gates from topic_evaluation_framework.md — any failure → rejection notice, stop
6. Run frequency checks (F02 once/week, F07 48h limit, F11 output quality gate)
7. Execute Production Mode engine (production_mode.md) — generate all 9 items
8. Self-apply quality checklist from production_mode.md — fix failures before output
9. Deliver output
```

---

## OUTPUT CONTRACT

Deliver exactly 9 items in this order. All 9 or a rejection notice. Nothing else.

```
1. REEL HEADER     — formula, duration, CTA, viral pattern, source, why
2. HOOK            — single Hinglish line + hook type + VP applied
3. FULL SCRIPT     — all beats with exact timing and word count
4. SCENE BREAKDOWN — clip table with block codes, camera, environment
5. FLOW PROMPTS    — one complete self-contained prompt per clip (≤10s each)
6. ASSEMBLY        — numbered steps: cuts, color grade, text overlays, SFX, export
7. CAPTION         — full Hinglish caption, copy-paste ready, under 300 words
8. CTA             — on-camera line + caption CTA + DM automation text + first comment
9. HASHTAGS        — 15 tags across 3 sets of 5
```

No analysis before the output. No explanation of formula selection. No partial packages.

---

## FORMULA REFERENCE

| Code | Name | Primary Metric |
|---|---|---|
| F01 | AI Cheat Code | DM rate |
| F02 | Future Shock | Follow rate |
| F03 | Hollywood VFX | Save + Share |
| F04 | Hidden Tool | DM rate |
| F05 | Career List | Save + Follow |
| F06 | AI vs Human | Share + Save |
| F07 | News Flash | Follow rate |
| F08 | Mind Blowing Transformation | Save + DM |
| F09 | Three Step System | Save rate |
| F10 | Comment React | Comment rate |
| F11 | Ego Output | Comment + Share |

Full formula files: `05_content/AI_SNIPP/02_formulas/F[NN]_[name].md`

---

## FAILURE HANDLING

Output a rejection notice and stop. No partial output.

```
/create-reel HALTED — [YYYY-MM-DD]
══════════════════════════════════
REASON: [one line]
GATE:   [which gate failed]
DETAIL: [specific — not generic]
RESOLUTION:
→ [corrective action]
══════════════════════════════════
```

The one permitted question: if topic maps equally to two formulas AND the choice changes production approach — ask which metric matters. Reply with F[NN] to continue. No other questions.

---

## NEVER DO

- Do not produce output before reading all LOAD 2–6 files
- Do not explain formula selection in the output
- Do not deliver partial packages — all 9 items or rejection
- Do not leave placeholder text in any Flow prompt
- Do not use 3+ CTAs in one reel
- Do not use DM trigger for F11 — Comment trigger only
- Do not cap proof display at 1.5s for F03 or F11 — Rule 19 applies (min 10s hold)
- Do not produce F02 if F02 was used this week
- Do not produce F07 for news older than 48h without reframing
- Do not produce F11 if the AI output is average — quality gate requires visually stunning output
- Do not produce on Carousel days (Tuesday, Saturday) without explicit P0 override
