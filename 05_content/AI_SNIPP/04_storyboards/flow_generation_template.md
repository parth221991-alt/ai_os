# Flow Generation Template
## AI_SNIPP Production System — Stages 4 + 5 of 8

*Generates the AI video prompts (Flow Scene Plan) and the assembled prompt pack (Flow Prompt Pack) for each clip. Completed once Storyboard (Stage 3) is approved.*

*Required inputs: Approved Storyboard + Character.png + flow_seed_prompts.md*
*Output: One accepted MP4 per clip, session log, passing prompt notes*

---

## SESSION HEADER

| Field | Value |
|---|---|
| Reel ID | REEL_[NNN] |
| Storyboard | Approved ✓ |
| Formula | F[NN] — [Formula Name] |
| Session Date | YYYY-MM-DD |
| Flow Tool | [Kling AI / Runway Gen-3 / Luma Dream Machine / Google Veo 3] |
| Character Reference File | Character.png — attached ✓ |
| Session Seed | [Record after first accepted clip — critical for cross-clip continuity] |
| Total Clips to Generate | [N] |

---

## STAGE 4 — FLOW SCENE PLAN

*The scene plan translates each storyboard block into a structured production brief for the AI video tool. One scene plan per clip. Fill before writing prompts.*

### Scene Plan: Clip 1

| Field | Value |
|---|---|
| Clip ID | REEL_[NNN]_CLIP1 |
| Block Type | Block [N] — [Name] |
| Duration | [X]s |
| Aspect | 9:16 vertical |
| Script Delivered | "[FILL — exact words]" |
| Environment Summary | [e.g., "Dark premium studio, charcoal background, monitor blue glow, warm amber key light on subject, Build.Solve.Scale.Repeat. visible on shelf"] |
| Camera Summary | [e.g., "MCU, slightly below eye level, slow push-in 2-3% over 8s"] |
| Acting Summary | [e.g., "SARCASTIC ROAST — playful exasperation, steepled hands, direct camera gaze, slight forward lean on emphasis"] |
| Overlay Required | [e.g., "None" / "Tool name pop-in at 2s, top-left" / "@ai_snipp watermark lower-right"] |
| Character.png Attached | [ ] Yes / [ ] No — attach before generating |

### Scene Plan: Clip 2

| Field | Value |
|---|---|
| Clip ID | REEL_[NNN]_CLIP2 |
| Block Type | Block [N] — [Name] |
| Duration | [X]s |
| Aspect | 9:16 vertical |
| Script Delivered | "[FILL]" |
| Environment Summary | |
| Camera Summary | |
| Acting Summary | |
| Overlay Required | |
| Character.png Attached | [ ] Yes |

### Scene Plan: Clip 3

| Field | Value |
|---|---|
| Clip ID | REEL_[NNN]_CLIP3 |
| Block Type | Block [N] — [Name] |
| Duration | [X]s |
| Aspect | 9:16 vertical |
| Script Delivered | "[FILL]" |
| Environment Summary | |
| Camera Summary | |
| Acting Summary | |
| Overlay Required | |
| Character.png Attached | [ ] Yes |

### Scene Plan: Clip 4 — CTA

| Field | Value |
|---|---|
| Clip ID | REEL_[NNN]_CLIP4 |
| Block Type | Block 5 — CTA |
| Duration | [X]s |
| Aspect | 9:16 vertical |
| Script Delivered | "[FILL — CTA exact words]" |
| Environment Summary | Dark premium studio, same as Clip 1 |
| Camera Summary | MCU, eye level (NOT slightly below), static lock |
| Acting Summary | WARM CTA — relaxed shoulders, direct gaze, warm corners of eyes, inviting tone |
| Overlay Required | @ai_snipp watermark lower-right + end card lower-third |
| Character.png Attached | [ ] Yes |

---

## STAGE 5 — FLOW PROMPT PACK

*Assembled AI video prompts. Each prompt = Master Seed Block + Continuation Block (Clips 2+) + Scene-Specific Block.*
*Copy-paste ready. Do not modify Master Seed Block between clips.*

---

### PRE-SESSION PROTOCOL

**Step 1 — Attach Character.png to session**
> Character.png must be attached before any generation. This is non-negotiable.

**Step 2 — Generate 3-second test clip using this prompt:**
```
CHARACTER IDENTITY LOCK:
- Indian male, mid-to-late 20s, warm medium-brown skin with amber undertones
- Hair: Tight natural coil curls, densely packed, deep black, medium length top, short close-cropped sides
- Beard: Short full, 5-10mm, well-trimmed edges, deep black
- Glasses: Matte black rectangular frames, medium-width, slightly wide-set, standard clear lenses, always present
- Build: Average to lean athletic, broad shoulders, natural upright posture
- Clothing: Plain black V-neck t-shirt, well-fitted, black lavalier microphone at center chest, dark/black sports watch on left wrist
- IDENTITY RULE: Face, hair texture, beard, and glasses are LOCKED

TEST CLIP: Creator standing in dark studio, looking directly at camera, neutral confident expression. 3 seconds. 9:16 vertical. No dialogue.
```

**Step 3 — Run 5-Point Consistency Check on test clip:**

| Check | Pass Criteria | Result |
|---|---|---|
| HAIR | Tight coil curls — spring-like, dense, NOT wavy, NOT loose | ✓ / ✗ |
| GLASSES | Matte black rectangular frames — present, correct shape | ✓ / ✗ |
| SKIN TONE | Warm medium-brown with amber undertones — NOT light, NOT shifted | ✓ / ✗ |
| BEARD | Short full 5-10mm — clean edges, NOT stubble, NOT long | ✓ / ✗ |
| FACE STRUCTURE | Same person — recognizable as consistent character | ✓ / ✗ |

**Pass threshold: 5/5 required. 4/5 acceptable only if failure is minor and hidden by frame.**
**If any fail: apply relevant Correction Block before generating any reel clips.**

**Step 4 — Record session seed:**
> Session Seed: [FILL after test clip passes]

---

### MASTER SEED BLOCK

*Prepend to EVERY prompt. Never modify. Never abbreviate.*

```
CHARACTER IDENTITY LOCK:
- Indian male, mid-to-late 20s, warm medium-brown skin with amber undertones
- Hair: Tight natural coil curls, densely packed, deep black, medium length top, short close-cropped sides
- Beard: Short full, 5-10mm, well-trimmed edges, deep black
- Glasses: Matte black rectangular frames, medium-width, slightly wide-set, standard clear lenses, always present
- Build: Average to lean athletic, broad shoulders, natural upright posture
- Clothing: Plain black V-neck t-shirt, well-fitted, black lavalier microphone at center chest, dark/black sports watch on left wrist
- IDENTITY RULE: Face, hair texture, beard, and glasses are LOCKED
```

### CONTINUATION BLOCK

*Add after Master Seed Block on Clips 2, 3, 4, and any subsequent clip. Swap [N] and [TOTAL] values.*

```
CONTINUATION: This is Clip [N] of [TOTAL]. Same character — same face, same tight coil curls, same matte black rectangular glasses, same beard, same dark studio. Only action, script line, and specified variations change.
```

---

### CLIP 1 PROMPT

```
[PASTE MASTER SEED BLOCK]

SCENE: [Scene name from storyboard — e.g., HOOK — SARCASTIC ROAST]
FORMAT: [X] seconds, 9:16 vertical
SETTING: [Full environment description — e.g., "Deep charcoal background (#0D0D0D–#1A1A1A). Multiple monitors with electric blue/teal glow (#1E6FBF–#0FBCD4). Bookshelves visible. Small green plant. Overhead pendant light. 'Build. Solve. Scale. Repeat.' text visible on shelf in background. Shallow depth of field — creator sharp, background soft. Warm amber key light (#D4894A) on subject."]
SHOT: [e.g., "Medium close-up, chest to top of head. Slightly below eye level — creator has natural authority in frame."]
CAMERA MOVEMENT: [e.g., "Slow subtle push-in — starts slightly wider, ends 2-3% closer. Barely perceptible. Builds intensity over clip duration."]
ACTING: [e.g., "SARCASTIC ROAST — playful exasperation. Hands interlocked or steepled (NOT finger-counting, NOT pointing at lens). Direct camera gaze, sustained. Slight forward lean on key word. Corners of mouth hint at knowing smile. High energy but controlled."]
DIALOGUE: "[Exact script line for this clip]"
OVERLAY: [e.g., "None" / "Bold text overlay: '[TOOL NAME]' — white, Inter Bold, ALL CAPS, center frame, pop-in at [Xs]"]
MOOD: [e.g., "Confident insider. The creator knows something you don't, and is about to share it."]
```

**Post-generation 5-Point Check:**
- [ ] HAIR ✓ — GLASSES ✓ — SKIN TONE ✓ — BEARD ✓ — FACE ✓
- [ ] Script line audible/represented in performance
- [ ] Camera angle is correct (slightly below for hook)
- [ ] Overlay present if required
- [ ] **Accepted:** Yes / No — if No, regenerate with: [note specific change]

**What worked (note for future sessions):**
> [any additional prompt language that improved output beyond the template]

---

### CLIP 2 PROMPT

```
[PASTE MASTER SEED BLOCK]

[PASTE CONTINUATION BLOCK — Clip 2 of [TOTAL]]

SCENE: [Scene name]
FORMAT: [X] seconds, 9:16 vertical
SETTING: [Environment description]
SHOT: [Shot type and position]
CAMERA MOVEMENT: [Movement]
ACTING: [Acting direction]
DIALOGUE: "[Script line]"
[For Facecam: FACECAM: "Creator occupies bottom-right 25-28% of frame in a clean rounded rectangle with warm amber glow border (#D4894A). Creator occasionally glances toward main content area, nods, reacts. Returns to direct camera at emphasis moments."]
[For Facecam: MAIN CONTENT AREA: "[Description of what fills the remaining 70-75% — tool interface, dashboard, certificate, etc.]"]
OVERLAY: [Overlay specification]
MOOD: [Mood]
```

**Post-generation 5-Point Check:**
- [ ] HAIR ✓ — GLASSES ✓ — SKIN TONE ✓ — BEARD ✓ — FACE ✓
- [ ] [Facecam if applicable:] Creator positioned bottom-right, 25-28% frame
- [ ] [Facecam if applicable:] Main content visible and legible
- [ ] **Accepted:** Yes / No — regenerate with: [note]

**What worked:**
> 

---

### CLIP 3 PROMPT

```
[PASTE MASTER SEED BLOCK]

[PASTE CONTINUATION BLOCK — Clip 3 of [TOTAL]]

SCENE: [Scene name]
FORMAT: [X] seconds, 9:16 vertical
SETTING: [Environment]
SHOT: [Shot]
CAMERA MOVEMENT: [Movement]
ACTING: [Acting]
DIALOGUE: "[Script line]"
OVERLAY: [Overlay]
MOOD: [Mood]
```

**Post-generation 5-Point Check:**
- [ ] HAIR ✓ — GLASSES ✓ — SKIN TONE ✓ — BEARD ✓ — FACE ✓
- [ ] **Accepted:** Yes / No — regenerate with: [note]

**What worked:**
> 

---

### CLIP 4 PROMPT — CTA

```
[PASTE MASTER SEED BLOCK]

[PASTE CONTINUATION BLOCK — Clip 4 of [TOTAL]]

SCENE: CTA CLOSE — WARM INVITE
FORMAT: [X] seconds, 9:16 vertical
SETTING: Environment A — Dark Premium Studio. Same studio as Clip 1. Unchanged.
SHOT: Medium close-up, chest to head.
CAMERA ANGLE: Eye level — direct peer-to-peer. NOT slightly below (that is the hook authority angle). This is warmth.
CAMERA MOVEMENT: Static lock. No camera movement.
ACTING: WARM CTA. Shoulders down and relaxed. Natural breathing visible. Direct gaze with warmth at corners of eyes. Slight open-palm gesture at chest level — inclusive, not commanding. Unhurried delivery. The energy is "I'm on your side and this is the next step."
DIALOGUE: "[Exact CTA words]"
OVERLAY: "@ai_snipp" watermark lower-right corner, small, white text. End card lower-third: "AI Tools • AI Certifications • AI Updates • AI Cheat Codes"
MOOD: Warm authority. Not selling. Not begging. Offering.
```

**Post-generation 5-Point Check:**
- [ ] HAIR ✓ — GLASSES ✓ — SKIN TONE ✓ — BEARD ✓ — FACE ✓
- [ ] Camera is eye level (NOT slightly below)
- [ ] @ai_snipp watermark visible
- [ ] End card text legible
- [ ] **Accepted:** Yes / No — regenerate with: [note]

**What worked:**
> 

---

## CORRECTION BLOCKS

*Apply these immediately after Master Seed Block when the 5-Point Check fails. Do not skip. Do not regenerate without applying the relevant block first.*

**HAIR CORRECTION — when curls go wavy or straight:**
```
HAIR CORRECTION — CRITICAL: Hair MUST be tight natural coil curls. NOT loose waves. NOT slightly curly. 
NOT straight. The curl texture is kinky-coily, densely packed, spring-like. Each individual curl is 
small and compact, not flowing. This is the most important visual identifier of this character. 
If the hair is not tight coil curls, the character identity is broken.
```

**GLASSES CORRECTION — when glasses disappear or change shape:**
```
GLASSES CRITICAL — ALWAYS PRESENT: The character wears matte black rectangular glasses in every 
single frame. They do not come off. They are NOT oversized. They are NOT round. They are NOT 
tinted. Standard rectangular matte black frames, medium width, slightly wide-set, clear standard 
lenses. Fully visible from any angle shown.
```

**SKIN TONE CORRECTION — when skin shifts lighter or changes tone:**
```
SKIN TONE ANCHOR: Warm medium-brown skin, amber undertones. NOT light brown. NOT olive. NOT dark 
brown. Medium-brown with warmth. The amber quality gives a natural earthy richness. This skin tone 
is consistent across all lighting — warm key light enhances the amber, cool background light does 
not wash it out.
```

**BEARD CORRECTION — when beard grows long or disappears:**
```
BEARD SPECIFICATION: Short full beard, exactly 5-10mm. NOT a long beard. NOT clean-shaven. NOT 
heavy stubble (too short). Full coverage of jaw and chin. Clean, well-defined edges along the 
cheek line. Deep black, same color as hair. Consistent density throughout.
```

**AGE CORRECTION — when character ages or de-ages:**
```
AGE LOCK: Character is mid-to-late 20s (25-30 years old). NOT older. NOT younger. Smooth skin 
with natural vitality. No visible aging lines. No juvenile softness. The face reads as a confident 
professional in their late 20s — experienced but energetic.
```

**FACE DRIFT CORRECTION — when a different person appears:**
```
[Shorten prompt by 30%. Move character description to first 50 words. Re-attach Character.png 
reference explicitly. Add note: "STRICT MATCH to reference image — same person across all clips."]
```

---

## SESSION LOG

*Complete this log for every generation session. This data informs future sessions and identifies recurring failure patterns.*

| Clip | Target Takes | Actual Takes | 5-Point Result | Issues Encountered | Correction Applied | Final File Name |
|---|---|---|---|---|---|---|
| 1 | 1-2 | [N] | [✓/✗ per check] | [issue or "none"] | [block name or "none"] | REEL_[NNN]_CLIP1_v[N].mp4 |
| 2 | 1-2 | [N] | | | | REEL_[NNN]_CLIP2_v[N].mp4 |
| 3 | 1-2 | [N] | | | | REEL_[NNN]_CLIP3_v[N].mp4 |
| 4 | 1-2 | [N] | | | | REEL_[NNN]_CLIP4_v[N].mp4 |

**Session total generation time:** [HH:MM]  
**Session seed (save for future cross-session use):** [FILL]  
**Prompt phrases that improved output beyond template (save to flow_seed_prompts.md):**
> [FILL — any language discovered in this session that consistently improved character fidelity]

---

## QUALITY STANDARDS

Before passing to Editing Plan:

- All [N] clips generated and accepted
- 5-Point Consistency Check passed for every accepted clip
- Session log complete — takes count, issues, corrections, file names
- Accepted files renamed: `REEL_[NNN]_CLIP[N]_v[N].mp4`
- Session seed recorded

---

## APPROVAL CHECKLIST

- [ ] All clips generated and accepted
- [ ] All 5-Point Checks passed
- [ ] Session log complete
- [ ] Files renamed and organized
- [ ] Session seed recorded
- [ ] New prompt phrases documented for flow_seed_prompts.md

**SIGN OFF:** _____________________ Date: _________

---

*On approval → Editing Plan + Publishing Package (Stages 6–8, tracked in Reel Production Checklist)*
