# AI_SNIPP — Kinetic Layer Reference

**Version:** 1.0
**Status:** Canonical
**Updated:** 2026-06-15 — Validated from user's June 14 generation; KINETIC LAYER required in all clip types

---

## What This File Is

Three reference prompts — one for each Flow clip type. When generating Flow prompts for any reel, these are the format templates. Copy the structure, replace the content.

**The rule that changed:** KINETIC LAYER now appears in EVERY clip, not just CTA. This was the format that produced the user's "perfect" generation on 2026-06-14.

---

## REFERENCE 1 — Clip 1 (Full Frame Hook)

**Kinetic type:** TEXT overlays only. Each triggered by a spoken word at an exact timestamp.

```
A medium close-up shot, 9:16 vertical ratio, eye-level camera angle. @me talking head
avatar stands in a warm creator home studio background with soft-focused bookshelves,
warm amber fairy light bokeh orbs, a small potted plant, and a dark condenser mic at
the frame edge. Lighting is a warm golden key light from above-front. @me looks directly
into the camera lens with a calm, completely settled expression — the quiet confidence
of someone showing a result, not performing one — steepled hands, and delivers this
audio script naturally: "Blank file to working SaaS feature — 47 minutes — 3 Claude
Code prompts — save this". Do not count with fingers. Do not raise 3 fingers. Keep
hands steepled and natural throughout. Subtle 3% camera push-in over 5 seconds. Clean,
stable framing.

KINETIC LAYER:
→ TEXT: "BLANK → FEATURE" — white ExtraBold — center-top — pops in as "SaaS feature"
   is spoken at 0:01 — 1.5s hold — fades
→ TEXT: "47 MIN" — warm amber ExtraBold — center-top — pops in as "47 minutes" is
   spoken at 0:02 — 1.5s hold — fades
→ TEXT: "3 PROMPTS" — white ExtraBold — center-top — pops in as "3 Claude Code
   prompts" is spoken at 0:03 — 1.5s hold — fades
→ TEXT: "SAVE THIS ↓" — warm amber ExtraBold — center-top — pops in as "save this"
   is spoken at 0:04 — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

**Clip 1 kinetic rules:**
- TEXT elements only — no BADGE or LABEL in full-frame clips
- white ExtraBold: facts, numbers, named concepts
- warm amber (#F59E0B) ExtraBold: action prompts, urgency, "SAVE THIS ↓"
- Each element triggered by a specific spoken word — include both the trigger word and the timestamp
- Last TEXT element always holds through clip end — no fade
- Add end-of-script "save this" if word count allows — it anchors the save-prompt kinetic
- Max 4 TEXT elements per hook clip
- Rule 26 inline: list all numbers in the script — "Do not raise [N] fingers"

---

## REFERENCE 2 — Split Frame Clip (Steps / Proof)

**Kinetic type:** BADGE + LABEL elements. All positioned within the TOP PANEL.

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 1. Do NOT
change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: STEP 1 — SPLIT FRAME. DURATION: 8 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px
bright white line.
TOP PANEL (top 58% of frame): Claude Code dark terminal interface. The user's first
prompt types in character by character at a natural pace, cursor blinking:

  "I need a subscription billing system for a SaaS dashboard. Users choose monthly
  ($12) or annual ($99) plans. Stripe handles payments. PostgreSQL stores subscription
  state. When Stripe fires payment_failed, automatically downgrade user to free tier.
  Admin users can manually override any subscription. REST endpoints for the dashboard
  frontend and a Stripe webhook handler. Stack: FastAPI + asyncpg."

Text fills the panel as it types. At 7.0s, Enter is pressed — a subtle "Claude is
thinking..." indicator pulses in teal below the input field.
BOTTOM PANEL (bottom 42% of frame): Character fills this panel edge to edge. Chest to
top of head visible. Face centered horizontally.

CAMERA ON CHARACTER: Slightly below eye level. Shallow depth of field. Static frame.
Slight push-in (2% over 8s).

ACTING DIRECTION: Informative and deliberate — the pace of someone who knows this step
is the one most developers skip. Glances briefly upward toward the top panel on "describe
the full feature in plain English," returns to camera on "no code yet" with a slow nod.
Do not raise 1 finger on "Prompt one." No counting gestures. Hands relaxed.

SCRIPT: "Prompt one — describe the full feature in plain English — what it does, who
uses it, every edge case — no code yet"

KINETIC LAYER:
→ BADGE: "STEP 1" — emerald green (#10B981), pill shape — pops in bottom-left of top
   panel at 0:00.3 — holds through clip
→ LABEL: "PROMPT 1 — DESCRIBE" — white, JetBrains Mono — fades in top of top panel at
   1.0s — holds 5s — fades
→ BADGE: "✓ No code — just clarity" — emerald (#10B981) — bottom-right of top panel —
   pops in at 6.5s as Enter is pressed — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

**Split frame kinetic rules:**
- BADGE: pill shape. bottom-left = step indicator, bottom-right = completion/confirmation
- LABEL: JetBrains Mono, white. Top of TOP PANEL. Always specify: fade-in time + hold duration + fade
- STEP badge appears at 0:00.3 — anchors the viewer to the step number immediately
- Completion badge appears near clip end (last 1–1.5s) — confirms the step result
- Color system: emerald #10B981 (steps, confirm), amber #F59E0B (warning, gap detected)
- Multi-state panels: STEP badge + LABEL for STATE A fade at transition; new set appears for STATE B
- Warning badge: amber pill, appears at the moment the gap/issue line reveals in the content panel

---

## REFERENCE 3 — CTA Full Frame

**Kinetic type:** ICON + TEXT trigger word + handle lower-third.

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 3. Do NOT
change face, curl pattern, shirt, hair, glasses, or skin tone.

SCENE: CTA — FULL SCREEN TALKING HEAD. DURATION: 5 seconds. Vertical 9:16. Drop
split screen.

CAMERA: Eye level — NOT below eye level. Peer-to-peer warmth. Static, completely
locked-off framing.

BODY LANGUAGE: Warm, grounded, unhurried. Slight nod at "save this." Open palm
forward on "DM." No performance — one person talking directly to one person.

SCRIPT: "Save this — DM SYSTEM — the exact 3 prompts right now"

KINETIC LAYER:
→ ICON: Bookmark — white — upper-right — pops in as "save" is spoken at 0:01 — fades at 1.8s
→ TEXT: "SYSTEM" — white ExtraBold — center frame — pops in as "SYSTEM" is spoken at
   0:02 — 1.5s hold — fades at 3.8s
→ TEXT: "@ai_snipp" — white, JetBrains Mono — bottom-left — fades in at 0:04 — holds
   through clip end

Do not repeat any spoken words or phrases in the audio.
```

**CTA kinetic rules:**
- Max 3 elements in a 5–6s CTA clip — space them evenly
- ICON on first CTA trigger: bookmark (save), DM chat bubble (DM), bell (follow)
- Trigger word: ExtraBold white, center frame, 0.3s scale-pop, ~1.5s hold, fade
- @ai_snipp lower-third: always last, JetBrains Mono, bottom-left, holds through clip end

---

## Quick Element Spec

| Element | Weight | Color | Position | Font |
|---------|--------|-------|----------|------|
| TEXT | ExtraBold | White (fact) · Amber #F59E0B (action) | Center-top (hook) · Center (CTA) | System sans |
| BADGE | Pill shape | Emerald #10B981 (step/confirm) · Amber #F59E0B (warning) | TOP PANEL — bottom-left (step) · bottom-right (confirm) | System sans |
| LABEL | Regular | White | Top of TOP PANEL | JetBrains Mono |
| ICON | — | White | Upper-right (CTA only) | — |
| Handle @ai_snipp | Regular | White | Bottom-left lower-third | JetBrains Mono |

---

## Pop-In Timing Pattern

```
Clip 1 (full frame):
  → Each TEXT element: trigger word spoken → 0.3s pop-in → hold → fade before next element
  → Last element: holds through clip end — never fades

Split frame clips:
  → STEP badge: 0:00.3 (appears before character speaks — anchors the step)
  → LABEL: fades in ~1s — holds until near end of STATE A — fades
  → Completion badge: pops in last 1–1.5s of clip

CTA:
  → ICON: first trigger word → pop-in → fade ~1.8s
  → Trigger word TEXT: second word → pop-in → hold 1.5s → fade
  → @ai_snipp: ~0.5s before clip end → fades in → holds
```

**The core rule:** Every number, step name, or action word in the script gets a kinetic echo in the prompt.
