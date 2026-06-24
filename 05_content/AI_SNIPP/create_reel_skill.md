# /create-reel — Claude Skill Definition

```
SKILL:     /create-reel
VERSION:   1.5
STATUS:    Canonical — default daily production command for AI_SNIPP
PURPOSE:   Generate a complete production-ready AI_SNIPP reel package
ENGINE:    Loads Daily Reel Generator → Production Mode → Character + Formula + Research
OUTPUT:    9 production assets, in order, copy-paste ready
```

**Location:** `D:\AI_OS\05_content\AI_SNIPP\create_reel_skill.md`

This file is the entry point for the `/create-reel` skill. When Claude reads this file, it knows exactly what to execute. All system intelligence lives in the referenced documents — this file defines the contract, invocation, and execution flow.

---

## INVOCATION SYNTAX

```
/create-reel
```
Zero inputs. Full auto. Claude selects topic, formula, and all parameters. Generates complete package.

```
/create-reel [topic]
```
Topic provided. Claude selects formula. Generates complete package.

```
/create-reel [formula]
```
Formula code provided (F01–F10). Claude selects best topic for that formula. Generates complete package.

```
/create-reel [topic] [formula]
```
Both provided. No selection logic runs. Immediate production.

```
/create-reel [topic] [formula] [priority]
```
Full specification. Priority values: `P0` (produce immediately), `P1` (this week), `P2` (queue). Overrides the generator's natural priority assignment.

```
/create-reel [topic] [formula] --hook "[hook line]"
```
Pre-generated hook provided (from `/viral-hook-writer`). Skips internal hook generation. Uses the provided hook verbatim for BEAT 1 and the CONTRACT ITEM 2 hook field.

```
/create-reel [topic] [formula]   (with reel-analyzer teardown in conversation)
```
When a `/reel-analyzer` teardown is present in the conversation context, it replaces the internal Research Phase. Claude reads the teardown's beat structure, visual technique, and "why it works" section as research input. The selected angle must be an original AI_SNIPP remake — not a copy.

```
/create-reel   (with content-repurposer batch in conversation)
```
When `/content-repurposer` has generated 5 reel concepts in the conversation, those concepts are treated as P1 candidates in topic selection (higher priority than evergreen). The highest-ranked concept is selected first.

---

**Quick reference:**

| Invocation | Topic | Formula | Goes to |
|---|---|---|---|
| `/create-reel` | Auto | Auto | Full selection + production |
| `/create-reel Claude Projects feature` | Locked | Auto | Formula selection + production |
| `/create-reel F01` | Auto | Locked | Topic selection + production |
| `/create-reel Claude Projects F01` | Locked | Locked | Immediate production |
| `/create-reel Claude Projects F01 P1` | Locked | Locked | Immediate production, P1 priority flagged |

---

## SYSTEM LOAD ORDER

When `/create-reel` is invoked, Claude loads these systems in sequence before producing any output:

```
LOAD 0 → reel_registry.md             (Publishing Memory Layer — topic history, loaded before topic selection)
LOAD 1 → create_reel_skill.md          (this file — defines the contract)
LOAD 2 → daily_reel_generator.md       (topic selection + formula selection + workflow)
LOAD 3 → production_mode.md            (execution rules + output format + rules 1–10)
LOAD 4 → 03_character/flow_seed_prompts.md         (Master Seed Block)
LOAD 4 → 03_character/character_consistency_guide.md (Continuation Block + 5-Point Check)
LOAD 4 → 03_character/prompt_blocks.md              (Scene Blocks B1–B7)
LOAD 4 → 03_character/visual_identity.md            (color, camera, typography, sound)
LOAD 4 → flow_generation_template.md                (Visual Action Mapping + Motion Standards + Camera Language + On-Screen Content Standards)
LOAD 5 → 02_formulas/formula_index.md               (formula selection + clip structure)
LOAD 5 → 02_formulas/F[NN]_[name].md                (specific formula file for selected formula)
LOAD 5 → 02_formulas/F11_ego_output.md               (ego output — loaded when F11 selected)
LOAD 6 → 01_research/hook_library.md                (hook category selection)
LOAD 6 → 01_research/viral_pattern_library.md       (VP01–VP15)
LOAD 6 → 01_research/cta_library.md                 (CTA spec + automation text)
LOAD 6 → 01_research/topic_evaluation_framework.md  (6 hard gates)
LOAD 6 → 01_research/content_pillars.md             (weekly balance check)
```

LOAD 1–3 run always. LOAD 4–6 are applied silently — Claude does not announce which files are being consulted.

---

## EXECUTION FLOW

```
/create-reel [args]
       ↓
  PARSE INPUTS
  ├── Topic locked?    → YES → skip topic selection
  ├── Formula locked?  → YES → skip formula selection
  └── Both locked?     → YES → jump to GATE CHECK
       ↓
  CONTEXT SCAN (silent — not reported)
  Scan conversation for:
  ├── reel-analyzer teardown present? → use as Research Phase input (replaces internal research)
  ├── content-repurposer batch present? → treat concepts as P1 candidates
  ├── --hook "[line]" provided? → lock hook, skip BEAT 1 generation in Research → skip Contract Item 2 generation
  ├── Breaking AI news mentioned? → P0 candidate
  ├── Queued ideas shared? → P1 candidates
  ├── Trend data shared? → P2 candidates
  └── No context? → Evergreen pool (daily_reel_generator.md § Evergreen Topic Pool)
       ↓
  REGISTRY CHECK (silent — reads reel_registry.md)
  ├── Extract last 30 entries → topic exclusion list (Evergreen ID + keyword match)
  ├── Extract last 5 entries → formula frequency map (block formula if already 2× in last 5)
  ├── Extract last 7 entries → pillar frequency map (block pillar if already 4× in last 7)
  └── Any candidate blocked by these filters is removed before topic selection begins
       ↓
  TOPIC SELECTION (if needed)
  Priority order from daily_reel_generator.md:
  P0 → Breaking news → F07 auto
  P1 → Queued idea, highest D3 score
  P2 → Trend-driven, highest opportunity score
  P3 → Formula balance — fill underrepresented formula category
  P4 → Pillar balance — fill underrepresented content pillar
  P5 → Evergreen default — highest inherent demand
       ↓
  INTENT CLASSIFICATION (silent)
  Classify topic as: Discovery Tool / Workflow Tool / News / Transformation / Comparison / Experiment
  → Determines research focus (see daily_reel_generator.md RESEARCH PHASE)
       ↓
  RESEARCH PHASE (silent — mandatory — applies to every topic, provided or selected)
  ├── Apply Outcome-First principle: "What result would make a viewer immediately try this?"
  ├── Adapt research focus to intent type:
  │     Discovery Tool → shortcuts, ready-made assets, instant wins — not walkthroughs
  │     Workflow Tool  → non-obvious systems, hidden features — not feature lists
  │     News           → Indian relevance, immediate viewer impact — not press release
  │     Transformation → proof quality, gap size — not creation steps
  │     Comparison     → decisive winner, surprising result — not balanced review
  │     Experiment     → unexpected outcome, replication difficulty — not methodology
  ├── Search for current information on the topic
  ├── Identify: key features, recent developments, common misconceptions,
  │   surprising facts, hidden capabilities, practical use cases
  ├── Identify what most creators are NOT covering on this topic
  └── Generate at least 10 candidate angles before selecting:
      (1) Obvious     (2) Contrarian     (3) Hidden Feature
      (4) Workflow    (5) Future Impact  (6) Shortcut
      (7) Mistake     (8) Comparison     (9) Experiment     (10) Transformation
       ↓
  TOPIC VALIDATION (silent — 5 gates)
  ├── Is this topic still relevant and timely?
  ├── Has this exact angle been covered by competitors recently?
  ├── Is there a stronger angle available from the 10 candidates?
  ├── Is there sufficient proof — verifiable, demonstrable on screen?
  └── Can this become a compelling reel in ≤35 seconds?
  Any gate fails → reject topic → return to TOPIC SELECTION with next candidate
       ↓
  ANGLE SELECTION (silent)
  Primary question: "Which angle makes a viewer immediately want to try this?"
  Select highest-scoring angle from 10 candidates.
  Prefer: outcomes a viewer can replicate now, shortcuts, transformations, surprising results,
          mistakes with corrections, hidden workflows, strong opinions with evidence.
  Avoid: "Top N features" / tutorial walkthroughs / feature-explanation angles when outcome angles exist.
  Tiebreaker: select the angle where a viewer could reproduce the result in the next 30 minutes.
  Selected angle becomes the lens for formula selection and hook direction.
       ↓
  FORMULA SELECTION (if needed)
  Decision tree from formula_index.md → one formula, no alternatives offered
       ↓
  GATE CHECK (silent — only surfaces on failure)
  Run all 6 hard gates from topic_evaluation_framework.md:
  Gate 1: Genuine Value      Gate 4: Novelty
  Gate 2: Specificity        Gate 5: Format (≤35s)
  Gate 3: Personal Proof     Gate 6: Brand Safety
  Any failure → REJECTION NOTICE → stop. No partial output.
       ↓
  FREQUENCY CHECK (silent)
  F02 used this week? → redirect if yes
  F07 > 48h old? → redirect if yes
  F03 output reviewed? → require if F03 selected
       ↓
  PRODUCTION (Production Mode engine — production_mode.md)
  Generate all 9 output items in sequence.
  Character system auto-applied. Viral pattern auto-selected. Color grade auto-applied.
       ↓
  SELF-QC (silent — checklist from production_mode.md)
  All items must pass before output is delivered. Failures are fixed, not flagged.
       ↓
  OUTPUT DELIVERED
  9 items. In order. Nothing else.
       ↓
  REGISTRY UPDATE (silent — no user-facing output)
  Append new entry to reel_registry.md:
  REEL_[NNN] | [date] | Generated | F[NN] | [pillar] | [topic] | [evergreen ID or —] | [3–5 keywords]
  Update "Next REEL_ID" line — increment by 1.
```

---

## OUTPUT CONTRACT

This is the binding specification. Every `/create-reel` invocation MUST deliver all nine items. No item is optional. No item may be abbreviated, summarized, or replaced with a reference. No additional items are produced.

---

### CONTRACT ITEM 1 — REEL HEADER

```
══════════════════════════════════════════════════════
/create-reel — [YYYY-MM-DD]  |  [Day]
══════════════════════════════════════════════════════
REEL:      REEL_[NNN]
TOPIC:     [selected or provided topic — one line]
FORMULA:   F[NN] — [Formula Name]
SOURCE:    [P0 / P1 / P2 / P3 Formula Balance / P4 Pillar / Evergreen]
WHY:       [One sentence — specific reason this topic + formula was selected]
DURATION:  [XX]s
CTA:       [DM [WORD] / Follow / Save / Comment]
PATTERN:   VP[NN] — [Viral Pattern Name]
══════════════════════════════════════════════════════
```

**Contract requirements:**
- `WHY` is one sentence. Not a paragraph. Not a list.
- `SOURCE` uses exactly one of the listed values.
- `PATTERN` is a specific VP from VP01–VP15. "Various" is not valid.

---

### CONTRACT ITEM 2 — HOOK

```
[Single hook line — English — max 15 words]

HOOK TYPE:  [Category from hook_library.md]
VP APPLIED: [VP0X — one sentence describing how the pattern manifests in this specific hook]
```

**Contract requirements:**
- Hook is one line. Not a paragraph. Not two options.
- English only. No Hindi, no Hinglish, no Roman transliteration.
- Passes the 1-second test: if the first word doesn't stop the scroll, rewrite.
- No soft language, no questions unless the formula specifically requires a question hook.
- If `--hook "[line]"` was provided: use that line verbatim. Do not generate an alternative.

---

### CONTRACT ITEM 3 — FULL SCRIPT

```
BEAT 1 — HOOK ([Xs]):
[Exact English words — complete sentence(s), no truncation — em-dash connectors between phrases]

BEAT 2 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 3 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 4 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 5 — CTA ([Xs]):
[Exact English words — under 10 words on camera]

WORD COUNT: [N] words | ~[X]s at 2.5 words/sec
```

**Contract requirements:**
- Every beat has exact timing in parentheses.
- Word count is accurate.
- Script stays within formula duration window.
- No `[...]` or ellipsis representing skipped content.
- **English only.** No Hindi, no Hinglish, no Roman transliteration. Technical AI/product names stay as-is (Claude, Anthropic, API, etc.). Connectives are English.
- Em-dash connectors between beats within a line ("Step one — clone the repo — run npm install — done"). Full stops between separate lines/sentences.
- Target: 14–15 words per 6s clip, 18–20 words per 8s clip, 20–22 words per 9s clip. Never sparse — Flow repeats words to fill empty time.

---

### CONTRACT ITEM 4 — SCENE BREAKDOWN

```
| Clip | Dur  | Block | Script (first 8 words)          | Camera     | Env | Note                |
|------|------|-------|---------------------------------|------------|-----|---------------------|
|  1   | [X]s | B[N]  | "[first 8 words of script]..."  | MCU below  | A   | [any special note]  |
|  2   | [X]s | B[N]  | "[first 8 words]..."            | MCU below  | A   | Facecam + content   |
|  3   | [X]s | B[N]  | "[first 8 words]..."            | MCU below  | D   | [note]              |
|  4   | [X]s | B[N]  | "[first 8 words]..."            | Eye level  | A   | Proof hold if F06   |
|  5   | [X]s | B5    | "[CTA words]..."                | Eye level  | A   | Warm close          |
```

**Contract requirements:**
- One row per clip. No merged rows.
- Block codes always used (B1–B7, not descriptions).
- Environment codes always used (A–D, not descriptions).
- CTA clip always uses Eye Level camera. Always.
- Duration column must sum to the value in the REEL HEADER.

---

### CONTRACT ITEM 5 — FLOW PROMPTS

One complete, self-contained prompt per clip. Standard reel = 4 clips. Every prompt is copy-paste ready — zero editing required by the user.

**Validated master format (confirmed 2026-06-17 — "everything was just perfect"):**

---

#### CLIP 1 — HOOK (8 seconds, full-screen talking head)

```
CLIP 1 OF 4 — HOOK

A [shot type — e.g., medium close-up] shot, 9:16 vertical ratio, [angle — e.g., slightly below eye level] camera angle.

CHARACTER IDENTITY LOCK — DO NOT DEVIATE FROM THIS DESCRIPTION:

Use the attached reference image as the strict visual anchor for the character.

The character is an Indian male, mid-to-late 20s. Warm medium-brown skin tone with amber undertones.

Hair: Tight natural coil curls, densely packed, deep black, medium length on top with natural volume. The curl texture is a defining feature — preserve it exactly.

Beard: Short full beard, approximately 5–10mm length, well-trimmed edges, deep black, covers full jaw and chin area cleanly.

Glasses: Matte black rectangular frames, medium-width, slightly wide-set. Standard clear lenses. Always present. This is a brand-defining element.

Build: Average to lean athletic. Broad shoulders visible. Natural upright posture.

Clothing: Plain black V-neck t-shirt, well-fitted. A small black lavalier microphone is clipped at the center chest. A dark/black sports watch is visible on the left wrist.

IDENTITY RULE: The face, hair texture, beard, and glasses must remain identical across all clips. These are LOCKED.

The character stands in a warm, high-end creator studio. Dark charcoal walls. Soft warm amber rim lighting. Slight bokeh background. Warm cinematic tone.

The character looks directly into the camera lens with [specific expression and body language — not "be natural"] and delivers this audio script naturally: "[EXACT ENGLISH SCRIPT — no ellipsis, no abbreviation]"

[Gesture constraints — e.g., "Do not count with fingers. Keep hands loosely at sides throughout."]

[Camera movement — e.g., "Slight push-in: 3% zoom over 8 seconds."] Clean, stable framing.

KINETIC LAYER:
→ TEXT: "[TEXT]" — [color name, e.g., emerald green] ExtraBold — [position] — pops in as "[trigger word]" is spoken at [Xs] — holds [Ns] — fades
→ ICON: [icon description, e.g., DM envelope icon] — [color name] — [position] — pops in at [Xs] — holds [Ns] — fades
→ TEXT: "[TEXT]" — [color name] — [position] — pops in at [Xs] — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

#### CLIPS 2–3 — STEPS (8–9 seconds each, split-screen)

```
CLIP [2 or 3] OF 4 — [STEP NAME]

IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip [N-1].
Do NOT change face, curl pattern, glasses, beard, shirt, or skin tone.

SCENE: [STEP NAME] — SPLIT FRAME. DURATION: [8 or 9] seconds. Vertical 9:16.

FRAME LAYOUT: The 9:16 frame is divided into TWO horizontal panels by a clean 1px bright white line.

TOP PANEL (top 58% of frame): [Full description of the tool/interface/content shown.
If multi-state:
  STATE A (0–[X]s): [describe what appears]
  STATE B ([X]–[total]s): [describe change — cross-dissolve transition]]

BOTTOM PANEL (bottom 42% of frame): Character fills this panel edge to edge. Chest to top of head visible. Face centered horizontally. ENV-W background (warm creator studio, soft amber lighting).

CAMERA ON CHARACTER: [angle — e.g., slightly below eye level]. Shallow depth of field. Static frame. Slight push-in ([N]% over [N]s).

ACTING DIRECTION: [specific demeanor and named emotion]. [Glance direction tied to script moment]. [Gesture constraints — e.g., "No finger counting, relaxed hands throughout."]

SCRIPT: "[EXACT ENGLISH SCRIPT — complete — no ellipsis]"

KINETIC LAYER:
→ BADGE: "[TEXT]" — [color name], pill shape — pops in [position] at [Xs] — holds [Ns]
→ LABEL: "[TEXT]" — [color name], [font weight] — fades in [position] at [Xs] — holds [Ns] — fades
→ BADGE: "[TEXT]" — [color name] — pops in at [Xs] — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

#### CLIP 4 — CTA (6 seconds, full-screen, eye-level)

```
CLIP 4 OF 4 — CTA

IDENTITY LOCK & CONTINUITY: Exact same character and environment from Clip 3.
Do NOT change face, shirt, hair, glasses, or skin tone.

SCENE: CTA — FULL SCREEN TALKING HEAD. DURATION: 6 seconds. Vertical 9:16. Drop split screen.

CAMERA: Eye level — NOT below eye level. Peer-to-peer warmth. Static, completely locked-off framing.

BODY LANGUAGE: [specific gestures tied to script moments — e.g., "Open palm toward camera on 'DM me', relaxed and direct."]. No performance — speaks like talking to one specific person.

SCRIPT: "[EXACT ENGLISH CTA SCRIPT — under 10 words on camera]"

KINETIC LAYER:
→ TEXT: "[TRIGGER WORD or CTA TEXT]" — [color name] ExtraBold — [position] — pops in at [trigger time]s — holds [Ns] — fades
→ ICON: [e.g., DM envelope icon] — [color name] — [position] — pops in at [trigger time]s — holds [Ns] — fades
→ LABEL: "@ai_snipp" — white, clean sans-serif — bottom-left — fades in at [Xs] — holds through clip end

Do not repeat any spoken words or phrases in the audio.
```

---

**Contract requirements — zero exceptions:**
- Every prompt is fully self-contained. Zero placeholders. No `[PASTE X]`, `[SAME AS CLIP 1]`, `[INSERT BLOCK]`.
- CHARACTER IDENTITY LOCK written verbatim in Clip 1. All five locks present: HAIR / GLASSES / SKIN TONE / BEARD / FACE.
- Clips 2–4 use IDENTITY LOCK & CONTINUITY header — not the full block, but all locks named.
- Clip 2 and 3 use TOP 58% / BOTTOM 42% split-screen format. B2 format is retired.
- Clip 4 is always eye level camera. Never below eye level.
- KINETIC LAYER present in every clip. Color names only — never hex codes (hex codes render as literal on-screen text in Flow).
- SCRIPT is English only. No Hindi, no Hinglish, no Roman transliteration.
- Anti-repetition constraint on final line of every clip: "Do not repeat any spoken words or phrases in the audio."
- Minimum 8 seconds per clip (Flow repeats words to fill shorter clips). CTA clip is 6 seconds minimum.
- Environment C ("News Room Energy") and any news/broadcast language ("BREAKING", "AI NEWS", "lower-third", "bulletin") are prohibited in Flow prompts — policy violations. Use Environment A or ENV-W.
- Hair description omits "short and close-cropped on the sides" — correct line: "medium length on top with natural volume."
- Scripts fill 90%+ of clip duration: 14–15 words for 6s, 18–20 words for 8s, 20–22 words for 9s.

---

### CONTRACT ITEM 6 — ASSEMBLY INSTRUCTIONS

**FLOW ARCHITECTURE:**  
Flow AI generates standalone video clips — one prompt, one clip, maximum 10 seconds each. Flow cannot edit clips, assemble clips, add music, apply color grades, or add text overlays after generation. These instructions are for the human editor in CapCut / Premiere / DaVinci, applied after all Flow clips are downloaded.

Exception: Branding described inside a Flow prompt's Visual Action Map is generated by Flow as part of the clip (Rule 18). All other post-production elements below are editor-applied.

```
ASSEMBLY:
1. [Exact action — import Flow-generated clips in order]
2. [Exact action — cut timing and transitions]
[...]

COLOR GRADE:
[Per-clip instructions. Formula-specific rules auto-applied:]
F06 → Clip 2 (Human): -10% sat, -5% warmth. Full warm from Clip 3.
F07 → Clip 1: -5% sat, cool shift. Full warm from Clip 2.
F08 → Before clips: -15% sat, -8% warmth. After clips: +5% warmth, +5% vibrance.
All others → Full warm grade throughout.

TEXT OVERLAYS (editor-applied — not generated by Flow):
[Timestamp] — [Exact text] — [Position] — [Entry animation]
Note: @ai_snipp branding in the final clip is generated by Flow (Rule 18).

SFX SEQUENCE (editor-applied — not generated by Flow):
[Timestamp] — [SFX type] — [Volume %]
[Proof Hold if reveal present: music → 10-15%, silence 1.5s after reveal]

MUSIC (editor-applied — not generated by Flow):
[Mood descriptor] | Background: 25-30% | Speech primary

EXPORT:
1080×1920 · H.264 · 30fps · 10 Mbps
```

**Contract requirements:**
- Assembly is numbered steps. Not prose.
- Every clip receives explicit color grade instruction.
- Every text overlay has a timestamp, content, position, and entry animation.
- Every SFX has a timestamp and volume level.
- Export settings are always present on the final line.

---

### CONTRACT ITEM 7 — CAPTION

```
[Hook or tension line — mirrors reel opening — no greeting]

[Body — value delivered in text: prompt, list, tip, or insight]
[Formula-mandatory line: Save karo / DM [WORD] for X / Follow karo]
[Comment-debate question — F02, F06, F08 formulas only]

.
.
.

[Set A hashtags] [Set B hashtags] [Set C hashtags]
```

**Contract requirements:**
- Opens with tension or hook — never "Hey guys," never the creator's name.
- Body contains a reusable asset (not just a description of the reel).
- Formula-mandatory line is always present. It is not optional for any formula.
- Caption under 300 words.
- No em-dash characters — uses ` — ` (space-dash-space) throughout.
- Dots (`.`) push hashtags below the fold — exactly as shown.

---

### CONTRACT ITEM 8 — CTA

```
ON-CAMERA LINE: "[Exact words — under 10 words — single action]"

CAPTION CTA: "[Secondary CTA sentence for caption body]"

DM AUTOMATION RESPONSE:
Trigger: [CAPITALIZED WORD]
Message:
[Complete automation response text — includes the actual promised deliverable, not a placeholder]

FIRST COMMENT:
"[Seeding comment — post immediately after publishing — question or debate prompt]"
```

**Contract requirements:**
- On-camera line is under 10 words. Always.
- DM automation response contains the actual content Claude can draft (prompt templates, tool list, steps) — not `[content to be added later]`.
- First comment seeding text is always present. It is not optional.
- For Follow and Save CTAs: DM automation response section is labeled `N/A — [Follow/Save] CTA`.

---

### CONTRACT ITEM 9 — HASHTAGS

```
SET A — BROAD REACH (5):
#[tag] #[tag] #[tag] #[tag] #[tag]

SET B — NICHE AUTHORITY (5):
#[tag] #[tag] #[tag] #[tag] #[tag]

SET C — ENGAGEMENT (5):
#[tag] #[tag] #[tag] #[tag] #[tag]
```

**Contract requirements:**
- Exactly 15 hashtags. No more, no fewer.
- Exactly 3 sets of exactly 5.
- Set A: Tags with 100K+ posts (broad discovery).
- Set B: Tags with 10K–100K posts (niche authority).
- Set C: Tags with under 10K posts or community-specific engagement tags.
- No hashtag appears in more than one set.

---

## QUALITY GATES

These gates are evaluated before output is delivered. Any gate failure triggers a fix — not a flag. Output is only delivered when all gates pass.

| Gate | What It Checks | Fail Action |
|---|---|---|
| **Completeness** | All 9 contract items present | Generate missing items before delivering |
| **Character Lock** | Master Seed Block verbatim in every Clip 1 prompt | Rewrite prompt with correct block |
| **Continuation** | Continuation Block verbatim in every Clip 2+ prompt | Rewrite prompt with correct block |
| **Zero Placeholders** | No `[FILL]`, `[INSERT]`, `[CHOOSE]`, `[...]` in any Flow prompt | Complete every placeholder before delivering |
| **Duration** | Script word count within formula window | Cut script to fit — do not note the cut |
| **Single CTA** | One primary CTA spoken on-camera | Remove excess CTAs |
| **Pattern Applied** | At least one VP01–VP15 explicitly applied | Select and apply a pattern |
| **English Script** | All SCRIPT fields in plain English — no Hindi, no Hinglish, no Roman transliteration. AI/product names (Claude, Anthropic, API, etc.) are English and stay as-is. | Rewrite any non-English script content |
| **Eye Level CTA** | CTA clip uses Eye Level camera (not below eye level) | Correct camera spec in Scene Breakdown and Flow prompt |
| **No Soft Language** | Zero instances of "maybe," "possibly," "I think," "kind of" | Rewrite affected lines as direct claims |
| **Natural Script Format** | FULL SCRIPT beats read as natural spoken sentences — no chained em-dash fragment chains (Rule 21) | Rewrite affected beats as short, complete sentences on separate lines |
| **Registry: Topic Dedup** | Topic not present in last 30 reel_registry.md entries (Evergreen ID or keyword match) | Move to next available topic; output REGISTRY HALT only if all options exhausted |
| **Registry: Formula Freq** | Selected formula appears fewer than 2× in last 5 registry entries | Select next-best formula from the formula decision tree |
| **Registry: Pillar Balance** | Selected pillar appears fewer than 4× in last 7 registry entries | Select from the most underrepresented pillar |
| **Visual Action Map** | Every spoken sentence has a Visual action and Camera movement in the prompt | Complete missing entries before delivering |
| **Motion Present** | Every non-CTA clip contains at least one movement element | Identify and add the missing movement type |
| **Demo Scene Quality** | B3 clips describe actual interface interaction — no static UI | Replace static description with interaction sequence |
| **Proof Scene Quality** | Proof clips specify animated comparison or reveal motion | Rewrite static screenshot instruction as dynamic comparison |
| **Camera Named** | Every non-CTA clip names a specific camera movement | Specify push-in / pull-out / focus shift / parallax — not "static" |
| **On-Screen Content Real** | Every on-screen text element (prompts, responses, settings, comparison panels) contains actual, readable content — no placeholder labels or dummy text | Replace placeholder with realistic, topic-matched content before delivering |
| **Visual Map Includes Content** | Visual Action Map entries for text-visible lines include the actual on-screen text written out — not "prompt appears" or "response visible" | Write the actual prompt, response, or setting text in the map entry |
| **Pause Test Pass** | Any paused frame showing text on screen reveals something useful to the viewer | Remove placeholder content; generate realistic on-screen text for the topic |
| **No Periods in Script** | Zero sentence-ending periods in any SCRIPT field — "—" used as separator | Replace all "." sentence-enders with "—" — Flow repeats dialogue on periods (Rule 17) |
| **No Double-Period** | No ".." anywhere in any SCRIPT field | Remove or replace with "—" (Rule 17) |
| **Clip Duration 8–10s** | Every clip is between 8 and 10 seconds. CTA clip minimum 6s. Minimum 8s for all other clips — Flow repeats words to fill shorter clips. | Split clips exceeding 10s; extend script on clips under 8s to fill duration |
| **Final Clip Branding** | Final CTA clip KINETIC LAYER includes `@ai_snipp` lower-third fading in at ~4s | Add @ai_snipp label entry to CTA clip KINETIC LAYER (Rule 18) |
| **No Hex Codes in Kinetic Layer** | All KINETIC LAYER color references use color names — zero hex codes (hex renders as literal on-screen text in Flow) | Replace all `(#XXXXXX)` with color names: "emerald green", "warm amber", "charcoal gray" |
| **Anti-Repetition Constraint** | Every clip prompt ends with "Do not repeat any spoken words or phrases in the audio." | Add the constraint to any prompt missing it |
| **No News Language in Prompts** | Zero instances of "BREAKING", "AI NEWS", "lower-third", "bulletin", "News Room Energy", or Environment C in any Flow prompt — policy violations | Remove prohibited language; use Environment A or ENV-W; move text overlays to Assembly only |
| **Split-Screen Format** | Clips 2–3 use TOP 58% / BOTTOM 42% horizontal split. B2 corner-facecam format is retired. | Rewrite any B2-style prompt with the validated split-screen layout |

---

## FAILURE HANDLING

When a topic or configuration cannot be produced, the skill outputs a rejection notice and stops. No partial output is delivered.

### Rejection Notice Format

```
/create-reel HALTED — [YYYY-MM-DD]
══════════════════════════════════
REASON: [Failure type — one line]
TOPIC:  [Topic that failed]
GATE:   [Which gate or constraint failed]
DETAIL: [One sentence — specific, not generic]

RESOLUTION:
→ [Specific corrective action the user can take]
→ [Alternative command if applicable]
══════════════════════════════════
```

### Failure Type Reference

| Failure | Trigger | Resolution Offered |
|---|---|---|
| Gate fail — Personal Proof | Topic claims untested result | Specify what to test first |
| Gate fail — Format | Topic needs >35s to be honest | Suggest Carousel or narrowed angle |
| Gate fail — Novelty | Topic covered in last 14 days | Offer differentiated angle |
| Gate fail — Brand Safety | Claim can't be defended | Reframe or reject |
| News stale | F07 topic >48h old | Offer F02 redirect or evergreen reframe |
| F02 frequency | F02 already used this week | Offer F07 or F09 redirect |
| DM deliverable missing | DM CTA selected, no deliverable | List CTA=WORD options |
| Carousel day | Command on Tuesday/Saturday | Offer `/create-carousel` redirect |

### The One Permitted Question

If topic maps equally to two formulas AND the formula choice changes the production approach significantly, the skill outputs:

```
FORMULA CHOICE NEEDED

F[NN] — [Name]: [one reason] — Primary metric: [metric]
F[NN] — [Name]: [one reason] — Primary metric: [metric]

Reply with F[NN] to continue.
```

After the user replies with a formula code, the skill resumes without further questions.

This is the **only** question the `/create-reel` skill is permitted to ask. Every other decision is made autonomously.

---

## EXAMPLES

These examples show the command → selection summary → abbreviated output structure. They are not full packages — they show the format and decision logic.

---

### EXAMPLE 1 — Zero Input

**Command:**
```
/create-reel
```

**Context in conversation:** None. No news, no queued ideas, no trend data.

**Selection logic applied:**
- Context scan: nothing found.
- Priority P5 (Evergreen Default) applied.
- Formula balance: F09 not used this week.
- Pillar: AI Cheat Codes underrepresented.
- Selected topic from Evergreen Pool: E03 (3-step LinkedIn post workflow using Claude).
- Formula confirmed: F09 — Three Step System.
- Pattern selected: VP08 (Pre-Save Hook).

**Output header:**
```
══════════════════════════════════════════════════════
/create-reel — 2026-06-08  |  Monday
══════════════════════════════════════════════════════
REEL:      REEL_005
TOPIC:     3-step LinkedIn post workflow using Claude
FORMULA:   F09 — Three Step System
SOURCE:    Evergreen — AI Cheat Codes pillar underweight
WHY:       F09 unused this week + AI Cheat Codes at 1 of target 3 posts
DURATION:  27s
CTA:       Save
PATTERN:   VP08 — Pre-Save Hook
══════════════════════════════════════════════════════
```

**[Then immediately: full 9-item output package]**

---

### EXAMPLE 2 — Topic + Formula Provided

**Command:**
```
/create-reel Claude Projects memory feature F01
```

**Selection logic applied:**
- Topic locked: Claude Projects memory/context feature.
- Formula locked: F01 — AI Cheat Code.
- Gate check: All 6 pass. Personal Proof = yes (demoed live). Novelty = yes (not covered in 14 days). Format = yes (4-clip structure fits 30s).
- Pattern selected: VP01 (Roast Opener — Ignorance Consequence) — F01 primary pattern.

**Output header:**
```
══════════════════════════════════════════════════════
/create-reel — 2026-06-08  |  Monday
══════════════════════════════════════════════════════
REEL:      REEL_005
TOPIC:     Claude Projects — context that never resets
FORMULA:   F01 — AI Cheat Code
SOURCE:    User-specified
WHY:       User-specified topic + formula
DURATION:  30s
CTA:       DM SYSTEM
PATTERN:   VP01 — Bete... Roast Opener
══════════════════════════════════════════════════════
```

**Hook:**
```
You use Claude every day — and you've never set up Projects? You're resetting your context every single time.

HOOK TYPE:  Ignorance Consequence — Scroll-Stop Indictment
VP APPLIED: VP01 — Direct challenge with mild exasperation. Slow head shake on "never set up Projects" — slight lean forward on "every single time."
```

**Script (abbreviated for example — full script in actual output):**
```
BEAT 1 — HOOK (8s): "You use Claude every day — and you've never set up Projects — you're resetting your context every single time — 80% of your setup just gone."

BEAT 2 — PROBLEM (8s): "Every new Claude conversation starts from zero — system prompt gone — your preferences gone — project context gone — you're rebuilding from scratch every session."

BEAT 3 — SOLUTION (8s): "Claude Projects — set your system prompt once — every conversation starts there — context never resets — Claude finally behaves like your assistant — not a stranger."

BEAT 4 — CTA (6s): "DM me SYSTEM — I'll send you my exact system prompt template."

WORD COUNT: 76 words | ~30s at 2.5 words/sec
```

**[Then: Scene Breakdown, 4 complete Flow Prompts, Editing Instructions, Caption, CTA, Hashtags]**

---

### EXAMPLE 3 — Formula Only (News Day)

**Command:**
```
/create-reel F07
```

**Context in conversation:** User mentioned earlier: "Anthropic just dropped Claude 3.5 Haiku pricing change for Indian API users — 20% cheaper."

**Selection logic applied:**
- Formula locked: F07 — News Flash.
- Context scan: Breaking news found in conversation — Haiku pricing change.
- Age check: News mentioned as "just dropped" — assumed under 24h. F07 time gate: PASS.
- Topic selected: Anthropic Claude Haiku pricing — Indian developers save 20% on API calls.
- Pattern selected: VP15 (Kya Matlab Hai Tumhare Liye Pivot) — F07 primary pattern.

**Output header:**
```
══════════════════════════════════════════════════════
/create-reel — 2026-06-08  |  Monday
══════════════════════════════════════════════════════
REEL:      REEL_005
TOPIC:     Claude Haiku pricing — Indian devs save 20% on API
FORMULA:   F07 — News Flash
SOURCE:    P0 — Breaking news (user-provided context, <24h)
WHY:       Breaking news in conversation + F07 unused today + Indian relevance is direct
DURATION:  26s
CTA:       Follow
PATTERN:   VP15 — Kya Matlab Hai Tumhare Liye Pivot
══════════════════════════════════════════════════════
```

**[Then: full 9-item output package]**

---

## SKILL INTEGRATION MAP

| Output Item | System Used | Source File |
|---|---|---|
| **UPSTREAM INPUT SKILLS (optional — run before `/create-reel`)** | | |
| Pre-research teardown | `/reel-analyzer` skill | `~/.claude/skills/reel-analyzer/SKILL.md` |
| Pre-generated hook | `/viral-hook-writer` skill | `~/.claude/skills/viral-hook-writer/SKILL.md` |
| Batched concept queue | `/content-repurposer` skill | `~/.claude/skills/content-repurposer/SKILL.md` |
| **CORE PIPELINE** | | |
| Topic selection | Daily Reel Generator | `daily_reel_generator.md` |
| Formula selection | Formula Index | `02_formulas/formula_index.md` |
| Hard gate check | Topic Evaluation | `01_research/topic_evaluation_framework.md` |
| Hook | Hook Library | `01_research/hook_library.md` |
| Script / English voice | Character Sheet | `03_character/character_sheet.md` |
| Clip structure by formula | Formula Index + Formula Files | `02_formulas/F[NN]_*.md` |
| Validated Flow prompt format | Production Mode / Feedback Memory | `production_mode.md` |
| Scene Blocks B1–B7 | Prompt Blocks | `03_character/prompt_blocks.md` |
| Environment Blocks (A / ENV-W) | Flow Seed Prompts | `03_character/flow_seed_prompts.md` |
| Acting directions | Prompt Blocks + Production Mode | `03_character/prompt_blocks.md` |
| Color grade rules | Visual Identity + Production Mode | `03_character/visual_identity.md` |
| Camera angles | Visual Identity | `03_character/visual_identity.md` |
| SFX palette | Visual Identity | `03_character/visual_identity.md` |
| Viral pattern | Viral Pattern Library | `01_research/viral_pattern_library.md` |
| Proof Hold (VP09) | Viral Pattern Library | `01_research/viral_pattern_library.md` |
| Eye Level CTA (VP13) | Viral Pattern Library | `01_research/viral_pattern_library.md` |
| CTA specs + automation text | CTA Library | `01_research/cta_library.md` |
| Caption format | Production Mode | `production_mode.md` |
| Hashtag mix | Content Pillars | `01_research/content_pillars.md` |
| Execution rules | Production Mode | `production_mode.md` |
| Output format | Production Mode | `production_mode.md` |
| Publishing memory check | Reel Registry | `reel_registry.md` |
| **POST-PRODUCTION SKILL (optional — run after `/create-reel`)** | | |
| Refined caption + hashtags | `/caption-and-hashtags` skill | `~/.claude/skills/caption-and-hashtags/SKILL.md` |

---

## WHAT THE SKILL NEVER DOES

The following behaviors are outside the skill's contract. If they appear in output, the skill has malfunctioned:

- Does not explain which formula it selected or why.
- Does not produce a research summary, research report, or analysis document before the output — research is internal and silent.
- Does not skip the Research Phase — research is mandatory for every topic, provided or selected, without exception.
- Does not start research by listing features — Outcome-First Principle applies: "What result would make a viewer immediately try this?" is the first question of every research session.
- Does not skip Intent Classification — topic intent is classified before any information is gathered.
- Does not generate fewer than 10 angle candidates before selecting — 10 is the minimum.
- Does not proceed to formula selection before generating 10 candidate angles and selecting the strongest one.
- Does not default to tutorial-style or feature-explanation angles when a shortcut, transformation, or outcome angle is available.
- Does not write chained em-dash fragment chains in FULL SCRIPT beats — script beats must read as natural spoken sentences (Rule 21).
- Does not produce an architecture discussion or planning document.
- Does not ask questions before generating (except Formula Ambiguity).
- Does not deliver partial packages — all 9 items or a rejection notice.
- Does not leave any placeholder text in any Flow prompt.
- Does not produce two formulas as options — one is selected.
- Does not write "you may want to consider" or "one option would be."
- Does not produce an F07 reel for news older than 48 hours without reframing.
- Does not produce F02 if F02 has already been used this week.
- Does not produce a reel on Carousel days (Tuesday, Saturday) without explicit override.
- Does not use three or more CTAs in one reel.
- Does not change the character's physical appearance between clips.
- Does not cap the proof display at 1.5s for F11 or F03 — Rule 19 supersedes VP09 (minimum 10s hold).
- Does not use a DM trigger for F11 — F11 always uses a Comment trigger with a personal identifier word.
- Does not produce F11 when the AI output is average — F11 quality gate requires visually stunning output.
- Does not derive topic ideas from `04_storyboards/examples/` — EX01, EX02, and EX03 are production templates, not idea candidates.
- Does not skip updating reel_registry.md after successful output delivery — every generated reel must be recorded before the session ends.
- Does not write any script in Hindi, Hinglish, or Roman transliteration — all SCRIPT fields are English only. Product names (Claude, Anthropic, API, etc.) stay as English proper nouns.
- Does not use hex codes in KINETIC LAYER descriptions — hex codes like `(#10B981)` render as literal on-screen text in Flow. Color names only.
- Does not use Environment C (News Room Energy) or any news/broadcast language ("BREAKING", "AI NEWS", "lower-third", "bulletin") in Flow prompts — policy violations in Flow.
- Does not use the retired B2 split-screen format (corner facecam) — the validated format is TOP 58% / BOTTOM 42% horizontal panels.
- Does not produce clips shorter than 8 seconds (Flow repeats words to fill shorter clips). CTA clip is always exactly 6 seconds.
- Does not write Flow prompts without the "Do not repeat any spoken words or phrases in the audio." anti-repetition constraint on the final line.
- Does not suggest HeyGen as an alternative production platform — all reels use Flow AI generation.
- Does not duplicate research that was already done by `/reel-analyzer` if a teardown is present in the conversation context — use it as input instead.

---

## SKILL REVISION LOG

| Version | Change | Date |
|---|---|---|
| 1.0 | Initial skill definition. All 9 contract items specified. | 2026-06-08 |
| 1.1 | Rule 16 (On-Screen Content Must Be Real) added to quality gates. Three new gates: On-Screen Content Real, Visual Map Includes Content, Pause Test Pass. | 2026-06-08 |
| 1.2 | Rule 17 (No Periods in Flow Scripts) and Rule 18 (Branding in Final Clip) added. Contract Item 6 renamed to Assembly Instructions with Flow architecture note. Four new quality gates: No Periods in Script, No Double-Period, Clip Duration ≤10s, Final Clip Branding. | 2026-06-08 |
| 1.3 | F11 (Ego Output) added to system load order and decision logic. Rule 19 (Extended Proof Hold for visual outputs — supersedes VP09 for F03/F11) and Rule 20 (Platform Context Frame for F03/F11) added. Three new skill contract rules: no 1.5s cap on F11/F03 proof, no DM trigger for F11, F11 quality gate. | 2026-06-08 |
| 1.4 | Publishing Memory Layer integrated. reel_registry.md added as LOAD 0. Registry Check step added to execution flow (before topic selection). Registry Update step added (after output delivery, silent). Three registry quality gates added: Topic Dedup, Formula Freq, Pillar Balance. Examples folder prohibition formalized. Registry update obligation added to WHAT THE SKILL NEVER DOES. | 2026-06-08 |
| 1.5 | Mandatory Research Phase added between topic selection and formula selection. Research Phase, Topic Validation (5 gates), and Angle Selection steps added to execution flow. Five-angle discovery framework established: Obvious / Contrarian / Hidden Feature / Workflow / Future Impact. Research output is internal — no reports produced. Generic angle framing (Top N, Best AI tool, New update) explicitly blocked. Three new WHAT THE SKILL NEVER DOES items added. | 2026-06-09 |
| 1.6 | Outcome-First Research Principle added — research begins with "What result would make a viewer immediately try this?" not features. Intent Classification added as execution step before Research Phase (6 types). Angle discovery expanded from 5 to 10 types (Shortcut, Mistake, Comparison, Experiment, Transformation added). Research strategy adapts per intent type. Outcome-first scoring and 30-minute replicability tiebreaker added to angle selection. Natural Script Format quality gate added (Rule 21 — FULL SCRIPT beats as natural spoken sentences). Six new WHAT THE SKILL NEVER DOES items added. | 2026-06-09 |
| 1.7 | **Language: Hinglish → English.** All SCRIPT fields changed to English only (confirmed 2026-06-11, REEL_009). **Flow prompt format updated** to validated master format (confirmed 2026-06-17): CHARACTER IDENTITY LOCK corrected (hair description fixed), B2 split-screen retired, TOP 58% / BOTTOM 42% split-screen adopted, KINETIC LAYER added to all clips, ENV-W established as standard environment, anti-repetition constraint added to every clip, minimum 8s clip duration enforced. **4 new upstream/downstream skills integrated:** reel-analyzer (replaces internal research when teardown present), viral-hook-writer (--hook flag), content-repurposer (P1 batch queue), caption-and-hashtags (post-production). **New invocation modes:** --hook, teardown context, repurposer batch. **Quality gates updated:** Hinglish Script → English Script; Clip Duration ≤10s → 8–10s; 6 new gates (No Hex Codes, Anti-Repetition, No News Language, Split-Screen Format). **10 new WHAT THE SKILL NEVER DOES items added.** SKILL INTEGRATION MAP expanded with upstream/downstream skill categories. | 2026-06-21 |

*When Flow AI updates its generation behavior, update the validated master format in `feedback_flow_prompts.md` (in memory). The CHARACTER IDENTITY LOCK in this file mirrors the authoritative description in `03_character/character_sheet.md`.*

---

*`/create-reel` — one command, complete reel package. Every time.*
