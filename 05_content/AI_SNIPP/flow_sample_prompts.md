# AI_SNIPP — Flow Sample Prompts
**Version:** 1.0 · **Format:** flow_seed_prompts.md v2.3 · **Updated:** 2026-06-21

---

## Critical Rules (read before copying any prompt)

| Rule | What it means |
|---|---|
| `@me` appears twice in Clip 1 | First anchors the visual, second anchors the action + Indian English voice |
| English scripts only | No Hindi, no Hinglish in SCRIPT field. Em-dash connectors between beats. No sentence-ending periods |
| KINETIC LAYER in every clip | Not just CTA. Clip 1 = TEXT only. Split frames = BADGE + LABEL. CTA = ICON + trigger TEXT + @ai_snipp |
| No hex codes in KINETIC LAYER | "emerald green" not "#10B981" — hex renders as on-screen text |
| Duration floor: 8 seconds | Flow repeats audio if clip is under ~8s. CTA is the only exception at 6s |
| Discovery narrative, not tutorial | "I found this" — not "go to X, click Y." Hook creates a promise gap |
| IDENTITY LOCK in every Clip 2+ | Chain forward: Clip 2 references Clip 1, Clip 3 references Clip 2 |
| Session rule | All 4 clips generated in the same Flow session with Character.png attached |

---

## SAMPLE 1 — Claude MCP Servers (Tool Discovery · F01 AI Cheat Code)

**Topic:** Claude MCP connects to your tools — files, databases, APIs — without copy-pasting anything  
**Script style:** Discovery — founder reports what they found  
**Duration:** 8s / 8s / 9s / 6s = 31s total

---

### Clip 1 — Hook (8s, full frame)

```
A medium close-up shot, 9:16 vertical ratio, eye-level camera angle. @me — Indian male AI founder and creator — talking head avatar stands in a warm creator home studio background with soft-focused bookshelves, warm amber fairy light bokeh orbs, a small potted plant, and a dark condenser mic at the frame edge. Lighting is a warm golden key light from above-front. @me looks directly into the camera lens with an engaging expression, steepled hands, and delivers this audio script naturally: "Claude just connected to my codebase, my Postgres database, and my Notion — without me copy-pasting a single thing — this changed how I work". Do not count with fingers. Keep hands steepled and natural throughout. Subtle 3% camera push-in over 8 seconds. Clean, stable framing.

KINETIC LAYER:
→ TEXT: "CODEBASE + DB + NOTION" — white ExtraBold — center-top — pops in as "Postgres database" is spoken at 0:03 — 1.5s hold — fades
→ TEXT: "ZERO COPY-PASTE" — warm amber ExtraBold — center-top — pops in as "copy-pasting" is spoken at 0:05 — 1.5s hold — fades
→ TEXT: "SAVE THIS ↓" — warm amber ExtraBold — center-top — pops in as "save this" is spoken at 0:07 — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 2 — What It Is (8s, split frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 1. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: WHAT IS MCP — SPLIT FRAME. DURATION: 8 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): Claude.ai dark-mode interface showing the "Tools" or "Integrations" settings panel. A list of connected integrations is visible: "Filesystem (local files) ✓", "PostgreSQL ✓", "Notion ✓". Each item has a green connected indicator dot. Clean, modern interface — no hallucinated text beyond these labels.
BOTTOM PANEL (bottom 42% of frame): Character fills this panel edge to edge. Chest to top of head visible. Face centered horizontally.

CAMERA ON CHARACTER: Slightly below eye level. Shallow depth of field. Static frame. Slight push-in (2% over 8s).

ACTING DIRECTION: Calm and measured — the pace of someone explaining a concept that genuinely surprised them. Glances briefly upward toward the top panel on "any tool that matters," returns to camera on "Claude reads it directly." No counting gestures. Hands relaxed.

SCRIPT: "MCP is a protocol — you point Claude at any tool that matters — your files, your database, your APIs — Claude reads it directly — no manual context ever again"

KINETIC LAYER:
→ BADGE: "MCP" — emerald green, pill shape — pops in bottom-left of top panel at 0:00.3 — holds through clip
→ LABEL: "MODEL CONTEXT PROTOCOL" — white, JetBrains Mono — fades in top of top panel at 1.0s — holds 5s — fades
→ BADGE: "✓ 3 tools connected" — emerald green — bottom-right of top panel — pops in at 6.5s — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 3 — The Proof (9s, split frame with STATE transition)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 2. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: LIVE PROOF — SPLIT FRAME. DURATION: 9 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): Floating card on charcoal gray background. Cross-dissolve at 4.5s from STATE A to STATE B.
STATE A (0–4.5s): Claude chat input field. User types: "Which tables in my database have more than 50,000 rows?" The question appears character by character, then Claude responds with an actual SQL query result listing: "orders (2.1M rows), users (890K rows), events (4.4M rows)." The response cites the live connected database — not a hypothetical.
STATE B (4.5–9s): Claude's follow-up message visible: "I can also check indexes on these tables or identify slow queries — want me to?" Real-time database awareness on display.
BOTTOM PANEL (bottom 42% of frame): Character fills panel edge to edge. Chest to top of head visible. Face centered horizontally.

CAMERA ON CHARACTER: Slightly below eye level. Shallow depth of field. Static frame — intentional stillness as the proof speaks for itself.

ACTING DIRECTION: Knowing smirk as STATE B loads. Hold that expression for 1.5 seconds. Brief upward glance toward top panel as STATE B appears — "see?" energy — then returns to camera. No performance. Just quiet confirmation.

SCRIPT: "I asked Claude which database tables are large — it queried my actual Postgres live — came back with real row counts — then offered to check the indexes"

KINETIC LAYER:
→ BADGE: "LIVE QUERY" — emerald green, pill shape — pops in bottom-left of top panel at 0:00.3 — holds through STATE A
→ LABEL: "ACTUAL DATABASE · NOT HALLUCINATED" — white, JetBrains Mono — fades in top of top panel at 1.0s — holds 3s — fades at 4.5s
→ BADGE: "LIVE QUERY" — emerald green, pill shape — pops in bottom-left at 4.5s (STATE B) — holds through clip end
→ BADGE: "✓ No copy-paste. No prompt stuffing." — emerald green — bottom-right of top panel — pops in at 7.5s — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 4 — CTA (6s, full frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 3. Do NOT change face, shirt, hair, glasses, or skin tone.

SCENE: CTA — FULL SCREEN TALKING HEAD. DURATION: 6 seconds. Vertical 9:16. Drop split screen.

CAMERA: Eye level — NOT below eye level. Peer-to-peer warmth. Static, completely locked-off framing.

BODY LANGUAGE: Slight nod at start. Shoulders fully relaxed. Open palm forward on "DM." Warm, direct close — not a pitch, an invitation.

SCRIPT: "DM 'MCP' — I'll send you the exact config I use for all three tools"

Do not repeat any spoken words or phrases in the audio.

KINETIC LAYER:
→ ICON: DM chat bubble — white — upper-right — pops in as "DM" is spoken at 0:01 — fades at 1.8s
→ TEXT: "MCP" — white ExtraBold — center frame — pops in as "MCP" is spoken at 0:02 — 1.5s hold — fades at 3.8s
→ TEXT: "@ai_snipp" — white, JetBrains Mono — bottom-left — fades in at 0:05 — holds through clip end
```

---

## SAMPLE 2 — Claude Projects (Workflow Upgrade · F09 Three-Step System)

**Topic:** Claude Projects gives Claude permanent memory of your context — no re-explaining  
**Script style:** Discovery — shows the before/after  
**Duration:** 8s / 8s / 9s / 6s = 31s total

---

### Clip 1 — Hook (8s, full frame)

```
A medium close-up shot, 9:16 vertical ratio, eye-level camera angle. @me — Indian male AI founder and creator — talking head avatar stands in a warm creator home studio background with soft-focused bookshelves, warm amber fairy light bokeh orbs, a small potted plant, and a dark condenser mic at the frame edge. Lighting is a warm golden key light from above-front. @me looks directly into the camera lens with an engaging expression, steepled hands, and delivers this audio script naturally: "Every Claude conversation I started — I was re-explaining myself — my stack, my role, my tone — until I found Projects — this is the fix". Do not count with fingers. Keep hands steepled and natural throughout. Subtle 3% camera push-in over 8 seconds. Clean, stable framing.

KINETIC LAYER:
→ TEXT: "RE-EXPLAINING EVERY TIME" — warm amber ExtraBold — center-top — pops in as "re-explaining myself" is spoken at 0:03 — 1.5s hold — fades
→ TEXT: "PROJECTS = PERMANENT MEMORY" — white ExtraBold — center-top — pops in as "Projects" is spoken at 0:06 — 1.5s hold — fades
→ TEXT: "SAVE THIS ↓" — warm amber ExtraBold — center-top — pops in as "fix" is spoken at 0:07 — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 2 — Step 1: Create the Project (8s, split frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 1. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: STEP 1 — SPLIT FRAME. DURATION: 8 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): Claude.ai dark-mode interface. Left sidebar shows "Projects" section with a "New Project" button. User clicks it. A project creation modal appears: name field filled as "My SaaS Product," a description field being typed into: "Full-stack SaaS. Stack: FastAPI + React + Supabase. My role: solo founder, product and code." The "Create" button is visible at the bottom of the modal.
BOTTOM PANEL (bottom 42% of frame): Character fills this panel edge to edge. Chest to top of head visible. Face centered horizontally.

CAMERA ON CHARACTER: Slightly below eye level. Shallow depth of field. Static frame. Slight push-in (2% over 8s).

ACTING DIRECTION: Crisp and deliberate. Glances briefly upward toward the top panel on "your stack, your role, your product," returns to camera on "that's all it needs." No counting gestures.

SCRIPT: "Step one — create a Project in Claude.ai — name it, describe your stack, your role, your product — that's all it needs"

KINETIC LAYER:
→ BADGE: "STEP 1" — emerald green, pill shape — pops in bottom-left of top panel at 0:00.3 — holds through clip
→ LABEL: "CREATE PROJECT" — white, JetBrains Mono — fades in top of top panel at 1.0s — holds 5s — fades
→ BADGE: "✓ 30 seconds to set up" — emerald green — bottom-right of top panel — pops in at 6.5s — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 3 — Steps 2 + 3: Add Files + See the Difference (9s, split frame with STATE transition)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 2. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: STEPS 2 AND 3 — SPLIT FRAME. DURATION: 9 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): Floating card on charcoal gray background. Cross-dissolve at 5.0s from STATE A to STATE B.
STATE A (0–5s): Claude.ai project view showing "Project Knowledge" panel. User uploads three files: "product_requirements.md," "api_schema.json," "design_system.md." Each file shows a green upload success indicator after appearing.
STATE B (5–9s): A new Claude conversation inside the project. Claude's first response begins immediately with: "Your FastAPI endpoints should use async handlers. Based on your schema, the /users route needs..." — no greeting, no context request. Claude is already operating from the project files.
BOTTOM PANEL (bottom 42% of frame): Character fills panel edge to edge. Chest to top of head visible.

CAMERA ON CHARACTER: Slightly below eye level. Static frame — slight push-in (1.5% over 9s). Expression shifts at STATE B — quiet satisfaction, slight lean back.

ACTING DIRECTION: Informative through STATE A, visibly pleased at STATE B. Upward glance as STATE B loads — "there it is" — returns to camera for last line. No counting gestures.

SCRIPT: "Step two — drop in your key files — step three — open any conversation inside the project — Claude already knows everything — no re-explaining — ever"

KINETIC LAYER:
→ BADGE: "STEP 2" — emerald green, pill shape — pops in bottom-left of top panel at 0:00.3 — holds through STATE A
→ LABEL: "ADD PROJECT FILES" — white, JetBrains Mono — fades in top of top panel at 1.0s — holds 3s — fades at 5.0s
→ BADGE: "STEP 3" — emerald green, pill shape — pops in bottom-left at 5.0s (STATE B) — holds through clip end
→ BADGE: "✓ Claude knows your context. Permanently." — emerald green — bottom-right of top panel — pops in at 7.5s — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 4 — CTA (6s, full frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 3. Do NOT change face, shirt, hair, glasses, or skin tone.

SCENE: CTA — FULL SCREEN TALKING HEAD. DURATION: 6 seconds. Vertical 9:16. Drop split screen.

CAMERA: Eye level — NOT below eye level. Peer-to-peer warmth. Static, completely locked-off framing.

BODY LANGUAGE: Slight nod at start. Shoulders fully relaxed. Open palm forward on "DM." Warm, direct close.

SCRIPT: "DM 'PROJECTS' — I'll send you the exact files I upload into every project"

Do not repeat any spoken words or phrases in the audio.

KINETIC LAYER:
→ ICON: DM chat bubble — white — upper-right — pops in as "DM" is spoken at 0:01 — fades at 1.8s
→ TEXT: "PROJECTS" — white ExtraBold — center frame — pops in as "PROJECTS" is spoken at 0:02 — 1.5s hold — fades at 3.8s
→ TEXT: "@ai_snipp" — white, JetBrains Mono — bottom-left — fades in at 0:05 — holds through clip end
```

---

## SAMPLE 3 — Claude Code in 3 Prompts (F09 Three-Step System)

**Topic:** Claude Code builds a working feature in under an hour with 3 prompts in the right order  
**Script style:** Discovery — founder shows the exact 3-prompt sequence  
**Duration:** 8s / 8s / 9s / 6s = 31s total

---

### Clip 1 — Hook (8s, full frame)

```
A medium close-up shot, 9:16 vertical ratio, eye-level camera angle. @me — Indian male AI founder and creator — talking head avatar stands in a warm creator home studio background with soft-focused bookshelves, warm amber fairy light bokeh orbs, a small potted plant, and a dark condenser mic at the frame edge. Lighting is a warm golden key light from above-front. @me looks directly into the camera lens with a calm, settled expression — the quiet confidence of someone showing a result — steepled hands, and delivers this audio script naturally: "Blank file to working SaaS feature — 47 minutes — 3 Claude Code prompts — most developers skip Prompt 2 and get garbage — save this". Do not count with fingers. Do not raise 3 fingers. Keep hands steepled and natural throughout. Subtle 3% camera push-in over 8 seconds. Clean, stable framing.

KINETIC LAYER:
→ TEXT: "47 MINUTES" — white ExtraBold — center-top — pops in as "47 minutes" is spoken at 0:02 — 1.5s hold — fades
→ TEXT: "3 PROMPTS" — warm amber ExtraBold — center-top — pops in as "3 Claude Code prompts" is spoken at 0:04 — 1.5s hold — fades
→ TEXT: "SKIP PROMPT 2 = GARBAGE OUTPUT" — warm amber ExtraBold — center-top — pops in as "skip Prompt 2" is spoken at 0:06 — 1.5s hold — fades
→ TEXT: "SAVE THIS ↓" — warm amber ExtraBold — center-top — pops in as "save this" is spoken at 0:07 — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 2 — Prompts 1 + 2 (8s, split frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 1. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: PROMPTS 1 AND 2 — SPLIT FRAME. DURATION: 8 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): Claude Code dark terminal interface. Prompt 1 is already visible at the top of the panel — a full feature description in plain English (3–4 lines). Below it, Claude's response is generating — a structured plan showing: "1. Models: User, Subscription, Plan. 2. Endpoints: /subscribe, /webhook, /cancel. 3. Stripe events to handle: payment_failed, customer.subscription.deleted." The plan is concise, scannable — no code yet.
BOTTOM PANEL (bottom 42% of frame): Character fills this panel edge to edge. Chest to top of head visible. Face centered horizontally.

CAMERA ON CHARACTER: Slightly below eye level. Shallow depth of field. Static frame. Slight push-in (2% over 8s).

ACTING DIRECTION: Deliberate — the energy of someone teaching a pattern they learned the hard way. Glances briefly upward toward the top panel on "Prompt 2 asks for a plan," returns to camera on "no code yet." No counting gestures.

SCRIPT: "Prompt 1 — describe the feature in full — Prompt 2 is the one people skip — ask Claude for a plan only — models, endpoints, data flow — no code yet"

KINETIC LAYER:
→ BADGE: "PROMPT 1" — emerald green, pill shape — pops in bottom-left of top panel at 0:00.3 — fades at 3.5s
→ LABEL: "DESCRIBE THE FEATURE" — white, JetBrains Mono — fades in top of top panel at 1.0s — holds 2.5s — fades at 3.5s
→ BADGE: "PROMPT 2" — emerald green, pill shape — pops in bottom-left of top panel at 3.5s — holds through clip end
→ LABEL: "GET A PLAN — NO CODE" — white, JetBrains Mono — fades in top of top panel at 4.0s — holds 3s — fades
→ BADGE: "✓ Claude plans before it builds" — emerald green — bottom-right of top panel — pops in at 6.5s — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 3 — Prompt 3 + Result (9s, split frame with STATE transition)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 2. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: PROMPT 3 AND RESULT — SPLIT FRAME. DURATION: 9 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): Floating card on charcoal gray background. Cross-dissolve at 5.0s from STATE A to STATE B.
STATE A (0–5s): Claude Code terminal. Prompt 3 typed in: "Now build it. Follow the plan exactly." Claude response begins generating rapidly — actual Python/FastAPI code appearing line by line. Class definitions, endpoint decorators, Stripe webhook handler. Fast code generation — the terminal fills.
STATE B (5–9s): VS Code dark-mode view of a working project folder: models.py, routes.py, webhooks.py, tests/test_subscription.py — all populated. A terminal at the bottom shows: "pytest tests/ ........ 8 passed in 1.4s".
BOTTOM PANEL (bottom 42% of frame): Character fills panel edge to edge. Slight lean back at STATE B. Quiet satisfaction.

CAMERA ON CHARACTER: Slightly below eye level. Static frame. Knowing smirk at STATE B — holds for 1.5 seconds.

ACTING DIRECTION: Measured through STATE A, visibly satisfied at STATE B. Brief upward glance as tests pass — returns to camera for the last line. No gestures.

SCRIPT: "Prompt 3 — 'build it, follow the plan' — Claude writes the full feature — then I run the tests — 8 passing — 47 minutes total"

KINETIC LAYER:
→ BADGE: "PROMPT 3" — emerald green, pill shape — pops in bottom-left of top panel at 0:00.3 — holds through STATE A
→ LABEL: "BUILD IT — FOLLOW THE PLAN" — white, JetBrains Mono — fades in top of top panel at 1.0s — holds 3.5s — fades at 5.0s
→ BADGE: "8 TESTS PASSING" — emerald green, pill shape — pops in bottom-left at 5.0s (STATE B) — holds through clip end
→ BADGE: "✓ 47 minutes. Working feature." — emerald green — bottom-right of top panel — pops in at 7.5s — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

### Clip 4 — CTA (6s, full frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 3. Do NOT change face, shirt, hair, glasses, or skin tone.

SCENE: CTA — FULL SCREEN TALKING HEAD. DURATION: 6 seconds. Vertical 9:16. Drop split screen.

CAMERA: Eye level — NOT below eye level. Peer-to-peer warmth. Static, completely locked-off framing.

BODY LANGUAGE: Slight nod at start. Shoulders fully relaxed. Open palm forward on "DM." Warm, direct close.

SCRIPT: "DM 'BUILD' — I'll send you all 3 prompts with the exact wording I use"

Do not repeat any spoken words or phrases in the audio.

KINETIC LAYER:
→ ICON: DM chat bubble — white — upper-right — pops in as "DM" is spoken at 0:01 — fades at 1.8s
→ TEXT: "BUILD" — white ExtraBold — center frame — pops in as "BUILD" is spoken at 0:02 — 1.5s hold — fades at 3.8s
→ TEXT: "@ai_snipp" — white, JetBrains Mono — bottom-left — fades in at 0:05 — holds through clip end
```

---

## Quick-Copy Correction Phrases

Paste these directly into Flow when a clip has issues:

**Audio repeating words:**
> "CORRECTION: The previous generation repeated spoken words. Do not repeat any spoken words or phrases under any circumstances. Each word in the script is spoken exactly once. Regenerate."

**Wrong accent (neutral/Western instead of Indian English):**
> "CORRECTION: The character is an Indian male AI founder and creator. The delivery must be in a clear, confident Indian English accent — not neutral American or British. Regenerate with the same visual identity, changing only the voice delivery to Indian English."

**Hair generates as waves instead of coil curls:**
> "CORRECTION: Hair must be tight natural coil curls — small defined circles, not waves or loose curls. Densely packed, kinky-curly texture. Refer to attached image. Regenerate maintaining all other elements."

**Face drifts between clips:**
> "CORRECTION: The character's face must match the attached reference exactly. This is a continuation of the same character. Do not alter face structure, features, or any visual identity elements. Regenerate."

**Kinetic layer missing or wrong:**
> "CORRECTION: The clip must include the kinetic text overlays as described — [describe what's missing]. Regenerate with these overlays included."

**Glasses change shape or color:**
> "CORRECTION: Glasses must be matte BLACK rectangular frames — not wire-frame, not round, not rimless. Black frame throughout. Refer to attached image. Regenerate."

---

## After-Generation Checklist

Before approving any clip:

- [ ] Hair: Tight coil curls — not waves, not straight
- [ ] Glasses: Matte black rectangular frames
- [ ] Beard: Short, clean, dark
- [ ] Shirt: Plain black V-neck
- [ ] Skin tone: Warm medium-brown preserved
- [ ] Clip 1 kinetic: TEXT pops triggered on spoken words — "SAVE THIS ↓" holds through end
- [ ] Split frame kinetic: STEP badge visible at 0:00.3 — LABEL in JetBrains Mono — completion badge at clip end
- [ ] CTA kinetic: Trigger word ExtraBold appeared — @ai_snipp lower-third visible at end
- [ ] No word repetition in audio
- [ ] Duration: 8s minimum (CTA 6s is the only exception)
