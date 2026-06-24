# AI_SNIPP — Google Flow Seed Prompts

**Version:** 2.2
**Status:** Canonical
**Updated:** 2026-06-15 — KINETIC LAYER required in ALL clips (not just CTA); TEXT overlays for Clip 1; BADGE + LABEL for split frame clips; kinetic_layer_reference.md added

---

## How This System Works

Two steps before generating any reel:

**Step 1 — Generate session avatar** (before opening Flow)
Create a still image of the character with the exact look and background for this session. The avatar is generated once per session — it locks the face, hair, glasses, beard, clothing, and background.

**Step 2 — Reference `@me` in every prompt**
Flow's `@me` tag attaches the session avatar automatically. Clip 1 uses `@me` twice — once for visual, once for action. Clips 2+ lock with the one-line IDENTITY LOCK & CONTINUITY header. That is the complete identity system.

No Master Seed Block. No multi-paragraph character description written into prompts.

---

## CLIP 1 — CANONICAL FORMAT

```
A [SHOT TYPE] shot, 9:16 vertical ratio, [CAMERA ANGLE] camera angle. @me — Indian male AI founder and creator — talking head avatar stands in a [ENVIRONMENT DESCRIPTION]. Lighting is a [LIGHTING DESCRIPTION]. @me [EYE CONTACT] with [EXPRESSION/BODY LANGUAGE], and delivers this audio script naturally: "[SCRIPT — em-dash connectors, no sentence-ending periods]". Do not repeat any spoken words or phrases in the audio. [CAMERA MOVEMENT]. Clean, stable framing.
```

### Three mandatory elements — never omit

| Element | What it does |
|---|---|
| `@me — Indian male AI founder and creator — talking head avatar` | Attaches the session avatar and anchors Indian English voice delivery — locks face, hair, glasses, beard, skin tone, clothing |
| `@me [eye contact] with [expression/body language], and delivers` | Second `@me` anchors the action and voice character |
| `[CAMERA MOVEMENT]. Clean, stable framing.` | Closes every Clip 1 prompt — signals a finished, stable shot to Flow |

### Clip 1 variables

**Shot type:** `medium close-up`

**Camera angle:**
- Hook (B1): `eye-level`
- CTA (B5): `eye-level`
- List/demo clips: `slightly below eye level`

**Environment description (Environment W — Warm Creator Home Studio):**
`warm creator home studio background with soft-focused bookshelves, warm amber fairy light bokeh orbs, a small potted plant, and a dark condenser mic at the frame edge`

**Lighting description (Environment W):**
`warm golden key light from above-front`

**Eye contact:** `looks directly into the camera lens`

**Body language:**
- Hook: `an engaging expression, steepled hands`
- Informative: `an open, direct expression`
- CTA: `a warm direct expression, open palm forward on "[trigger word]"`

**Camera movement:**
- Hook: `Subtle 3% camera push-in over [N] seconds`
- CTA: `Static, completely locked-off framing`

**KINETIC LAYER (mandatory in every Clip 1):**
Add after the camera movement line, before "Do not repeat any spoken words or phrases in the audio."

Use TEXT elements only — no BADGE or LABEL in full-frame clips.

```
KINETIC LAYER:
→ TEXT: "[FACT/NUMBER]" — white ExtraBold — center-top — pops in as "[spoken word]" is spoken at [0:0X] — 1.5s hold — fades
→ TEXT: "SAVE THIS ↓" — warm amber ExtraBold — center-top — pops in as "save this" is spoken at [0:0X] — holds through clip end
```

- white ExtraBold: facts, numbers, named concepts
- warm amber (#F59E0B) ExtraBold: action prompts ("SAVE THIS ↓"), urgency lines
- Each element triggered by a specific spoken word — include the trigger word AND its timestamp
- Last TEXT element always holds through clip end — no final fade
- Rule 26 inline: list every number in the script — "Do not raise [N] fingers"
- Max 4 TEXT elements per hook clip

See `03_character/kinetic_layer_reference.md` — REFERENCE 1 for a complete worked example.

---

## CLIPS 2+ — SPLIT FRAME FORMAT

Use when the clip shows a content panel above the character (tool intro, proof, list — B2/B3 clips).

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip [N-1]. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: [SCENE NAME]. DURATION: [X] seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): [Content description — specific interface, GitHub repo, tool UI. Include readable text. For multi-state panels, describe STATE A (0–Xs) and STATE B (Xs–end) with cross-dissolve transition.]
BOTTOM PANEL (bottom 42% of frame): Character fills this panel edge to edge. Chest to top of head visible. Face centered horizontally.

CAMERA ON CHARACTER: Slightly below eye level. Shallow depth of field. Static frame. Slight push-in (2% over [N]s).

ACTING DIRECTION: [2-3 sentences: behavior, glance direction, energy]. Indian English delivery — same accent as Clip 1. Do not repeat any spoken words or phrases. No counting gestures.

SCRIPT: "[em-dash connectors — no sentence-ending periods — Rule 17]"
```

**TOP PANEL content rules:**
- Name the specific interface (e.g., "GitHub.com dark mode repository page for 'username/repo'")
- Include actual readable text — repo description, README sections, star counts, file lists, tool output
- Specify motion: "scrolls slowly downward" OR "holds static" OR cross-dissolve at [N]s from STATE A to STATE B
- Multi-state panels: describe each state with exact timestamps and what changes

**BOTTOM PANEL is always:**
`Character fills this panel edge to edge. Chest to top of head visible. Face centered horizontally.`

**Acting direction pattern for list/tool clips:**
`[Energy description]. Glances briefly upward toward the top panel on "[specific spoken content]", returns to camera on "[value line]". No counting gestures.`

**Continuity note:** Always reference the immediately previous clip (Clip 2 references Clip 1, Clip 3 references Clip 2). Do not always write "from Clip 1" — chain forward.

**KINETIC LAYER (mandatory in every split frame clip):**
Add a KINETIC LAYER block after SCRIPT, before "Do not repeat any spoken words or phrases in the audio."

Use BADGE + LABEL elements only — all positioned within the TOP PANEL, not the full frame.

```
KINETIC LAYER:
→ BADGE: "STEP [N]" — emerald green (#10B981), pill shape — pops in bottom-left of top panel at 0:00.3 — holds through clip
→ LABEL: "[STEP LABEL]" — white, JetBrains Mono — fades in top of top panel at 1.0s — holds [N]s — fades
→ BADGE: "✓ [COMPLETION TEXT]" — emerald (#10B981) — bottom-right of top panel — pops in at [last 1.5s timestamp] — holds through clip end
```

- STEP badge anchors the viewer: appears at 0:00.3, before the character speaks
- LABEL shows the step action in JetBrains Mono — always specify fade-in time + hold duration + fade
- Completion badge: emerald, bottom-right of TOP PANEL, pops in near clip end to confirm the step result
- For multi-state panels: STEP badge + LABEL fade at STATE B transition; new set appears for STATE B immediately
- Warning/gap badge: amber (#F59E0B) pill, appears when a gap or issue is revealed in the content panel
- Color system: emerald #10B981 (steps, confirm), amber #F59E0B (warning, gap)

See `03_character/kinetic_layer_reference.md` — REFERENCE 2 for a complete worked example.

---

## CLIPS 2+ — CTA FULL FRAME FORMAT

Use for the final CTA clip of every reel. Drops the split screen. Eye level only.

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip [N-1]. Do NOT change face, [curl pattern / shirt / hair], glasses, or skin tone.

SCENE: CTA — FULL SCREEN TALKING HEAD. DURATION: [X] seconds. Vertical 9:16. Drop split screen.

CAMERA: Eye level — NOT below eye level. Peer-to-peer warmth. Static, completely locked-off framing.

BODY LANGUAGE: [Specific actions tied to spoken words — e.g., "Slight nod at start. Shoulders relaxed. Open palm forward on '[trigger word].' Warm, direct close."]

SCRIPT: "[em-dash connectors — no sentence-ending periods — Rule 17]"

Do not repeat any spoken words or phrases in the audio.

KINETIC LAYER:
[timestamp] — "[trigger word]" spoken → [icon type] pops in [position], white, 0.3s pop, fades at [timestamp]
[timestamp] — "[TRIGGER WORD]" spoken → "[TRIGGER WORD]" kinetic text appears center frame, bold white condensed caps, 0.3s scale-pop in, holds [N]s, fades
[timestamp] — "@ai_snipp" handle fades in bottom-left, white clean sans-serif, holds through clip end
```

**KINETIC LAYER rules:**
- Every kinetic element is tied to a specific spoken word — describe the exact timestamp and the word that triggers it
- DM CTAs: DM chat bubble icon on "DM" → trigger word typography on the trigger word → @ai_snipp at end
- Follow CTAs: subscribe/bell icon on "follow" → @ai_snipp at end
- Save CTAs: bookmark icon on "save" → @ai_snipp at end
- Trigger word typography: bold white condensed caps, scale-pop in 0.3s, hold ~1.5s, fade out — always center frame
- @ai_snipp lower-third: always the final element, fades in ~0.5s before clip end, white clean sans-serif, bottom-left
- Do not stack more than 3 kinetic elements in a 6s CTA clip — space them evenly

---

## CLIPS 2+ — FULL FRAME CONTINUATION FORMAT

Use for non-CTA full-screen clips after Clip 1 (e.g., storytelling, reaction beats).

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip [N-1]. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

[SHOT TYPE], 9:16 vertical, [CAMERA ANGLE] camera angle. Full frame — no split. [CHARACTER POSTURE AND EXPRESSION]. Delivers this audio script naturally: "[SCRIPT — em-dash connectors, no sentence-ending periods]". Indian English delivery — same accent as Clip 1. Do not repeat any spoken words or phrases in the audio. [CAMERA MOVEMENT].
```

---

## WORKED EXAMPLE — F07 News Flash (4 clips, validated 2026-06-14)

These 4 clips were generated and confirmed perfect. They are the canonical format reference.

### Clip 1 — Hook (8s)

```
A medium close-up shot, 9:16 vertical ratio, eye-level camera angle. @me — Indian male AI founder and creator — talking head avatar stands in a warm creator home studio background with soft-focused bookshelves, warm amber fairy light bokeh orbs, a small potted plant, and a dark condenser mic at the frame edge. Lighting is a warm golden key light from above-front. @me looks directly into the camera lens with an engaging expression, steepled hands, and delivers this audio script naturally: "Microsoft put a complete GenAI course on GitHub — 21 lessons, free — 100,000 developers starred it — most Indian developers have never opened it". Do not repeat any spoken words or phrases in the audio. Subtle 3% camera push-in over the 8 seconds. Clean, stable framing.
```

### Clip 2 — Tool Intro (8s, split frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 1. Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: TOOL INTRO — SPLIT FRAME. DURATION: 8 seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.
TOP PANEL (top 58% of frame): GitHub.com dark mode repository page for "microsoft/generative-ai-for-beginners". Shows Star count badge (★ 112k), README description ("21 Lessons..."), and file list folders (00 to 06) scrolling slowly downward. Language bar at bottom showing Jupyter Notebook 87.4%.
BOTTOM PANEL (bottom 42% of frame): Character fills this panel edge to edge. Chest to top of head visible. Face centered horizontally.

CAMERA ON CHARACTER: Slightly below eye level. Shallow depth of field. Static frame. Slight push-in (2% over 8s).

ACTING DIRECTION: Informative and direct. Glances briefly upward toward the top panel on "prompt engineering, RAG, AI agents", returns to camera on "working code in every lesson." Indian English delivery — same accent as Clip 1. Do not repeat any spoken words or phrases. No counting gestures.

SCRIPT: "It's called generative-ai-for-beginners — prompt engineering, RAG, AI agents, fine-tuning — all in Python — working code in every lesson"
```

### Clip 3 — Proof (8s, split frame with STATE transition)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 2.

SCENE: PROOF — SPLIT FRAME. DURATION: 8 seconds. Vertical 9:16.

FRAME LAYOUT:
TOP PANEL (top 58% of frame): Floating card on charcoal-gray (#1A1A1A). Cross-dissolve at 4.0s from STATE A to STATE B. STATE A (0-4s): Lesson 04 folder open, showing README preview and green "Open in GitHub Codespaces" button. STATE B (4-8s): Jupyter notebook open in GitHub Codespaces dark-mode browser tab running a visible code cell (import os, from openai import OpenAI) with a green "✓ Kernel running" indicator and text output generated below.
BOTTOM PANEL (bottom 42% of frame): Character fills panel edge to edge. Chest to top of head visible. Static frame — intentional stillness.

ACTING DIRECTION: Calm proof presentation. Knowing smirk as the running notebook (STATE B) appears. Hold that expression for 1.5 seconds during the proof hold. Brief upward glance toward top panel as STATE B appears, then returns to camera. Indian English delivery — same accent as Clip 2. Do not repeat any spoken words or phrases.

SCRIPT: "No sign-up — zero cost to read — run the code free using GitHub Models, just a GitHub account — every lesson has a Jupyter notebook ready to run"
```

### Clip 4 — CTA (6s, full frame)

```
IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 3. Do NOT change face, shirt, hair, glasses, or skin tone.

SCENE: CTA — FULL SCREEN TALKING HEAD. DURATION: 6 seconds. Vertical 9:16. Drop split screen.

CAMERA: Eye level — NOT below eye level. Peer-to-peer warmth. Static, completely locked-off framing.

BODY LANGUAGE: Slight nod at start. Shoulders relaxed. Open palm forward on "DM." Warm, direct close.

SCRIPT: "DM 'FREE' — I'll send you the link and the 3 lessons to start with"

Do not repeat any spoken words or phrases in the audio.

KINETIC LAYER:
0:01 — "DM" spoken → DM chat bubble icon pops in upper-right, white, 0.3s pop, fades at 1.8s
0:02 — "FREE" spoken → "FREE" kinetic text appears center frame, bold white condensed caps, 0.3s scale-pop in, holds 1.5s, fades at 3.8s
0:05 — "@ai_snipp" handle fades in bottom-left, white clean sans-serif, holds through clip end
```

---

## SESSION AVATAR IMAGE — REQUIREMENTS

Generate before opening Flow. This image is the visual anchor for the entire reel.

The avatar image must show:
- Character in medium close-up (chest to top of head)
- Camera at eye level or slightly below eye level
- The exact background and lighting for this session

**Environment W — Warm Creator Home Studio (default):**
Deep warm brown tones. Bookshelf with books, soft-focused. Clusters of warm amber/orange fairy light bokeh orbs scattered across the background — glowing softly. Small lush green potted plant on shelf. Black studio condenser microphone on boom arm partially visible at frame edge, soft-focused. Warm amber/golden key light from above-front. Zero cool or blue light anywhere — exclusively warm tones. Brightly lit subject against a softer, darker background.

**Environment A — Dark Premium Studio:**
Deep charcoal/near-black background. Monitors emitting cool blue/teal glow in background. Warm amber key light on subject. Cool background. High contrast. Cinematic. Use for high-intensity content (breaking news, urgent topics).

---

## AFTER GENERATING — CHECKLIST

1. **Hair:** Dense tight natural coil curls? Full volume rounded afro crown? NOT faded or cropped on sides?
2. **Glasses:** Matte black rectangular frames? Same shape/color throughout?
3. **Skin tone:** Warm medium-brown preserved? Not too light?
4. **Beard:** Sparse goatee-pattern stubble (mustache + chin strongest, light cheeks)? NOT a full thick beard? NOT clean-shaven?
5. **Clothing:** Dark neutral tones? No logos or patterns?
6. **Kinetic layer (ALL clips):**
   - Clip 1: TEXT overlays popped in on trigger words? "SAVE THIS ↓" amber text holds through end?
   - Split frame clips: STEP badge visible at 0:00.3? LABEL in JetBrains Mono appeared? Completion badge at clip end?
   - CTA clip: Trigger word ExtraBold text appeared? @ai_snipp lower-third visible at clip end?
7. **Word repetition:** Did any spoken line repeat? → Add "Do not repeat any spoken words or phrases in the audio." to the SCRIPT line and regenerate.

---

## CORRECTION PHRASES

**Accent neutral/Western:**
> "CORRECTION: The character is an Indian male AI founder and creator. The delivery must be in a clear, confident Indian English accent — not neutral American or British. Regenerate with the same visual identity, changing only the voice delivery to Indian English."

**Words repeating in audio:**
> "CORRECTION: The previous generation repeated spoken words. Do not repeat any spoken words or phrases under any circumstances. Each word in the script is spoken exactly once. Regenerate."

**Hair generates wrong:**
> "CORRECTION: Hair must be tight natural coil curls — small defined circles, not waves or loose curls. Densely packed, kinky-curly texture. Refer to attached image. Regenerate maintaining all other elements."

**Glasses generate wrong:**
> "CORRECTION: Glasses must be matte BLACK rectangular frames — not wire-frame, not round, not rimless. Black frame throughout. Refer to attached image. Regenerate."

**Skin generates too light:**
> "CORRECTION: Warm medium-brown skin tone — not light, not pale. Rich amber undertones. Indian complexion. Match the attached image precisely."

**Face changes between clips:**
> "CORRECTION: The character's face must match the attached reference exactly. This is a continuation of the same character. Do not alter face structure, features, or any visual identity elements. Regenerate."

**Beard generates wrong (too full or clean-shaven):**
> "CORRECTION: The beard must be sparse short stubble in a goatee pattern — stronger mustache and chin coverage, light/patchy on cheeks. Approximately 3–5mm natural growth. NOT a full thick beard. NOT clean-shaven. Refer to attached reference image. Regenerate maintaining all other elements."

**Hair generates faded/cropped sides:**
> "CORRECTION: The hair must have full natural curl density on the sides as well as the top. NOT a fade or tapered cut. NOT cropped short on sides. Dense natural coil curls all around — full rounded afro crown. Regenerate."

**Kinetic layer missing:**
> "CORRECTION: The CTA clip must include kinetic text overlay — '[TRIGGER WORD]' in bold white condensed caps appearing center frame when the trigger word is spoken, and @ai_snipp lower-third at clip end. Regenerate with these overlays."

---

## REVISION LOG

| Version | Change | Date |
|---|---|---|
| 1.0 | Initial — MASTER SEED BLOCK, Scene Blocks A–D, Environment Blocks A/B/C/W/D, Examples 1–4 | 2026-06-08 |
| 2.0 | Complete format overhaul. Master Seed Block removed — replaced by attached image system. Character description removed from prompt bodies. Character introduction line (`Indian male AI founder and creator, mid-to-late 20s —`) added inline in Clip 1 for voice anchoring. Clips 2+ use single-line IDENTITY LOCK. Split frame standardized as TOP 58% / BOTTOM 42% with 1px white line divider. VISUAL ACTION MAP and KINETIC LAYER removed from Flow prompts — these are now Assembly items. Environment blocks preserved as avatar image generation reference. | 2026-06-14 |
| 2.1 | Clip 1 format changed from "Use the attached image" to `@me` syntax — validated from 4 perfect clips generated 2026-06-14. CTA full frame format updated to labeled structure (SCENE / CAMERA / BODY LANGUAGE / SCRIPT blocks) matching validated Clip 4. KINETIC LAYER restored to CTA clip prompts — trigger word typography, icon, and @ai_snipp lower-third described inline in the Flow prompt so Flow generates them as part of the clip. Continuity chain updated to reference Clip N-1 (not always Clip 1). Worked example replaced with the 4 validated clips. | 2026-06-14 |
| 2.2 | KINETIC LAYER required in ALL clips — not just CTA. Clip 1: TEXT overlays (word-triggered, ExtraBold, white/amber #F59E0B, center-top; last element holds through end). Split frame clips: BADGE + LABEL elements within TOP PANEL (STEP badge emerald #10B981 at 0:00.3, JetBrains Mono LABEL, completion badge near clip end; amber #F59E0B for warnings). Rule 26 finger-counting constraint required inline in every Clip 1. Added kinetic_layer_reference.md with 3 worked examples (Clip 1, Split frame, CTA). | 2026-06-15 |
| 2.3 | Voice anchoring baked into all canonical formats. Clip 1: `@me — Indian male AI founder and creator —` added to character description line (anchors Indian English accent — without it @me locks visual only and Flow defaults to neutral/Western). `Do not repeat any spoken words or phrases in the audio.` added after SCRIPT in all formats. Clips 2+ split frame and full frame: `Indian English delivery — same accent as Clip 1.` added to ACTING DIRECTION. Worked example updated to match. | 2026-06-15 |
