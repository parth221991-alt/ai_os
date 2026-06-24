---
role: visual-production-standard
version: 1.1
status: Canonical
applies_to: All Flow prompt generation in AI_SNIPP
source: REEL_001 post-production analysis — 2026-06-08
updated: 2026-06-14
---

# AI_SNIPP — Flow Generation Template
## Visual Production Standards

**Purpose:** This file defines visual production standards and rules for AI_SNIPP reels.

**When loaded:** Every `/create-reel` execution. Applied silently — not announced.

---

## FORMAT UPDATE — 2026-06-14

**Current Flow prompt format is defined in `flow_seed_prompts.md` v2.0.**

Two changes that affect this file:

**1. VISUAL ACTION MAP (Rule 11) is no longer written into Flow prompts.**
The current prompt format (attached image + IDENTITY LOCK) does not include a VISUAL ACTION MAP block. Rules 11–16 below remain as reference for understanding visual principles, but do not write a VISUAL ACTION MAP section into production prompts. Scene behavior is described concisely inside the ACTING DIRECTION field instead.

**2. KINETIC LAYER (Rule 19) is now an Assembly item — not a Flow prompt item.**
Text overlays (skill numbers, labels, trigger cards, @ai_snipp handle) are added in CapCut/editor during Assembly. Do not write a KINETIC LAYER block into Flow prompts. The Assembly section of each reel package specifies all overlay instructions.

**What still applies from this file:**
- Rule 17 — No sentence-ending periods in SCRIPT fields (still active — em-dash connectors required)
- Rule 22 — Per-clip word count limits (still active)
- Rule 16 — On-screen content must be real (still active — TOP PANEL content must include actual readable text)
- Motion principles (Rules 14–15) — inform how ACTING DIRECTION is written, even without a formal VAM block
- Rule 18 — @ai_snipp branding is now added as an Assembly overlay (not in the Flow prompt), except where the Flow prompt CTA clip explicitly warrants it

---

---

## THE CORE PRINCIPLE

Every clip has two simultaneous tracks:

```
TRACK 1 — AUDIO:   What the character says (the script)
TRACK 2 — VISUAL:  What happens on screen while they say it
```

These two tracks must be synchronized. If a spoken line describes an action, the
visual track shows that action happening in real time. If the spoken line describes a
result, the visual track reveals the result in the same moment.

A clip where Track 1 and Track 2 are not synchronized is a failed clip.

---

## RULE 11 — VISUAL ACTION MAPPING

**The requirement:** Every spoken sentence in a Flow prompt has an associated Visual
Action and Camera Movement. No sentence is left without both.

**The format** (inside the VISUAL ACTION MAP block of every Flow prompt):

```
VISUAL ACTION MAP:
"[Exact spoken sentence 1]"
  → Visual: [what moves or appears on screen during this line]
  → Camera: [named movement — push-in / pull-out / focus shift / parallax / zoom / rack]
"[Exact spoken sentence 2]"
  → Visual: [what moves or appears on screen]
  → Camera: [named movement]
[Continue for every sentence. No sentence without both entries.]
```

**Worked example — F01 Clip 2 (Tool Demo):**

```
VISUAL ACTION MAP:
"Claude.ai mein jao."
  → Visual: Browser navigates to Claude.ai homepage — URL bar visible, page loads smoothly
  → Camera: Slight push-in toward the screen (2% zoom over 1.5s)
"Profile icon, Custom Instructions."
  → Visual: Cursor moves to top-right profile icon and clicks — dropdown menu appears
  → Camera: Subtle zoom toward the dropdown (3% zoom over 0.8s)
"Do fields hain."
  → Visual: Custom Instructions panel opens — two text fields visible, both currently empty
  → Camera: Focus shifts to panel (slight rack focus or frame tighten)
"Pehli: tum kaun ho."
  → Visual: Cursor moves to the first field — text begins typing: "I'm a content creator..."
  → Camera: Hold on panel — slight push-in toward the first field
"Doosri: response style."
  → Visual: Cursor jumps to second field — text begins typing: "Respond in Hinglish..."
  → Camera: Pan down to second field
"Ek baar fill karo — hamesha apply hoga."
  → Visual: Both fields now show filled content — Save button click — success toast appears
  → Camera: Pull back slightly to show both fields complete (zoom out 2%)
```

**Rule:** If you cannot describe a visual action for a spoken line, the script must be
rewritten until every line has a natural visual correlate.

---

## RULE 12 — DEMO SCENE STANDARDS

**Applies to:** All B3 (Tool Demo) clips. All clips containing interface interaction.

### What to show

```
PERMITTED — shows actual workflow:

"Open Claude.ai"          → Browser navigates to claude.ai — URL visible
"Click profile"           → Cursor moves to profile icon, clicks, dropdown opens
"Go to Settings"          → Settings page loads — menu items visible
"Type the prompt"         → Text appears in input field, cursor blinking
"Click Generate"          → Button click — generation animation begins (dots, progress)
"Upload the image"        → Upload dialog opens — file selected — preview appears
"See the output"          → Output text streams in — readable on screen
"Open Flow"               → Flow interface opens — project visible
"Click a clip"            → Clip selected, highlighted, properties panel opens
"Export the video"        → Export dialog opens — progress bar visible
```

```
PROHIBITED — does not show the workflow:

Static prompt box         → A rectangle containing text, nothing moving
Blurry UI panel           → Interface screenshot that is out of focus or low resolution
Generic dashboard         → Placeholder dashboard with fake/random data
Unreadable text block     → Text too small or too compressed to read at mobile size
Abstract animation        → Motion graphics that represent the tool but do not show it
Logo + name               → Just showing the tool's logo instead of the tool working
```

### Demo scene prompt language

Write the visual description as a sequence of micro-actions — not a static state:

```
WRONG:  "Claude.ai interface is visible on screen with Custom Instructions panel open."

RIGHT:  "Browser navigates to Claude.ai homepage — URL bar shows claude.ai — the
        interface loads. Cursor moves to the top-right profile icon and clicks.
        A dropdown menu slides down. Cursor moves to 'Custom Instructions' and clicks.
        The Custom Instructions panel slides open from the right — two empty text fields
        visible with placeholder text. Cursor moves to the first field and begins typing."
```

The difference: the correct version describes a sequence of actions happening in time.
The wrong version describes a static end-state.

---

## RULE 13 — PROOF SCENE STANDARDS

**Applies to:** Any clip that reveals a result, comparison, transformation, or output.

### Motion requirements for proof

Every proof clip must contain one or more of the following:

```
ANIMATED COMPARISON:
Before state appears first (left or top). After state slides/fades in alongside it.
The transition between before and after has motion — a wipe, a split reveal, a
simultaneous fade-in. Neither state is static for more than 1 second.

HIGHLIGHT REVEAL:
Output text or result appears on screen. A highlight or glow draws attention to the
key difference — animated, not a static colored box.

DYNAMIC BEFORE/AFTER:
Before: shown with visual treatment that signals "suboptimal" (slight desaturation,
monochrome, dim). The transformation: a visual transition. After: full warm, bright,
the result dominant on screen. The visual treatment change IS the proof.

STREAMING OUTPUT:
AI output streams onto screen in real time — text appearing word by word or line by
line. This is inherently dynamic. Use it.

CURSOR + HIGHLIGHT:
Cursor navigates to the key finding in an output. Highlights the critical word or
number. The viewer's eye is guided to the proof by the cursor movement.
```

### Proof scene prompt language

```
WRONG:  "Split-screen showing two Claude responses — one generic, one on-brand."

RIGHT:  "The screen begins showing a single Claude.ai interface in dark mode. A
        soft label fades in: 'WITHOUT Custom Instructions.' The response is visible —
        generic tone, plain formatting, no personality. After 1.5 seconds, the screen
        wipes from center-left: the right half now shows the same interface with the
        same prompt, labeled 'WITH Custom Instructions.' The response streams in —
        warm Hinglish tone, structured, clearly on-brand. A subtle glow highlight
        appears on the key differentiating lines. Creator facecam (25% BR) watches
        with a controlled knowing nod."
```

### Proof Hold — VP09 (mandatory when proof reveals a result)

After the key result is revealed:
- Music drops to 10-15% volume
- No narration for 1.5 seconds
- No camera movement during the hold
- Let the viewer absorb the result before the next line

---

## RULE 14 — MOTION-FIRST DESIGN

**The test:** Before finalizing any clip description, ask: "What is moving?"

If the answer is "nothing," the clip is wrong. Fix it before generating.

### Movement types (at least one required per clip)

```
CHARACTER MOVEMENT:
- Body: lean forward / pull back / turn to face screen / nod / gesture
- Face: expression shift (flat → smirk, neutral → wide-eyed)
- Hands: open palm / steeple / point toward screen / gesture to content

CAMERA MOVEMENT:
- Push-in: camera moves toward subject (creates urgency, emphasis)
- Pull-out: camera moves away from subject (creates context, reveals scope)
- Parallax: depth shift between foreground and background layers
- Focus rack: plane of focus shifts from one element to another
- Dynamic reframe: frame tightens or loosens on subject mid-clip

INTERFACE MOVEMENT:
- Page loading / navigating
- Cursor moving and clicking
- Text appearing / streaming
- Panel opening / closing
- Dropdown expanding
- Progress bar filling
- Upload animation
- Generation animation

OBJECT MOVEMENT:
- Text overlay sliding in
- Highlight animating over content
- Label fading in
- Counter or timer running
- Before/after wipe transition

COLOR GRADE DRIFT (permitted as motion substitute on static assets — F03 and F11 only):
When a clip holds a static AI-generated image for 10+ seconds (Extended Proof, Rule 19),
a subtle color grade shift (±5% warmth, ±3% saturation drift over 8–10s) creates
perceived motion at zero production cost. This satisfies the motion requirement for
that clip.
Use in: B-PROOF clips in F03 and F11 formulas only.
Prompt language: "Subtle color temperature drift over [X]s — image begins at natural grade,
warms gradually (+5% over 8s), returns slightly toward neutral by clip end. Imperceptible
as a transition; experienced as life."
```

### The motion budget per clip

| Clip Type | Minimum motion elements |
|---|---|
| B1 — Hook | Character movement + Camera push-in |
| B3 — Tool Demo | Interface movement + Camera follow |
| B3 — Proof Reveal | Interface motion + Camera movement + Character reaction |
| B4 — News | Character movement + Camera movement |
| B5 — CTA | Character movement (intentional stillness on camera is permitted) |
| B8 — Visual Problem Open | Animated overlay motion + Color grade shift (desaturated/cool) |
| B-PROOF — Extended Reveal | Color grade drift (Rule 19) + Creator facecam reaction (optional) |
| B-SOCIAL — Platform Context | Camera push-in (platform reveal movement) |
| B6 — Storytelling | Character movement + Camera movement |
| B7 — Reaction | Character movement + Camera movement |

---

## RULE 15 — CAMERA LANGUAGE

**Applies to:** Every clip. Every Flow prompt. No exceptions except B5 CTA.

### Named camera movements — use these exact terms in prompts

```
PUSH-IN:
Camera moves toward the subject. Creates urgency, intimacy, emphasis.
Use on: Hook clips (authority builds as camera closes), key claim moments.
Prompt language: "Slow push-in over [X]s — camera moves [N]% closer from start to end."

PULL-OUT:
Camera moves away from subject. Creates context, releases tension, reveals scope.
Use on: After proof reveal (zoom out to show full result), transition to a wider view.
Prompt language: "Slow pull-out — camera widens [N]% from [START STATE] to [END STATE]."

FOCUS SHIFT (RACK FOCUS):
The plane of focus shifts from one element to another. Creator comes into focus /
interface comes into focus.
Use on: Transition from creator-centered to content-centered in demo clips.
Prompt language: "Rack focus from creator (sharp) to interface (sharp) over 0.5s."

PARALLAX:
Foreground and background move at slightly different rates — creates depth and
cinematic dimensionality.
Use on: Any clip with depth layers (studio backdrop vs creator vs foreground elements).
Prompt language: "Subtle parallax — background shifts [direction] at 50% of foreground rate."

DYNAMIC REFRAME:
The frame tightens or loosens on the subject mid-clip in response to content emphasis.
Use on: When creator leans forward for emphasis — frame follows and tightens.
Prompt language: "Frame tightens to ECU [Extreme Close-Up] on 'hamesha apply hoga' — 
returns to MCU for CTA."

STATIC (CTA CLIP ONLY):
Completely locked-off camera. No movement. Intentional contrast with dynamic earlier clips.
The stillness signals: we have arrived at the action moment.
Prompt language: "Camera completely static — no movement — intentional contrast with 
prior clips."
```

### Camera assignment by clip position

```
Clip 1 (Hook):               Slow push-in (2-4% over the full clip duration)
Clip 2 (Demo 1):             Camera follows action — zoom toward interface on key moments
Clip 3 (Proof):              Camera pull-out to reveal full comparison, or focus rack to result
Clip 4 (Demo 2):             Camera follows action — zoom, rack, or parallax
B8 (Visual Problem Open):    Static or very slow pull-back — the animated overlay is the motion
B-PROOF (Extended Reveal):   Lock frame for full duration — color grade drift is the motion (Rule 19)
B-SOCIAL (Platform Context): Platform Reveal — begin pulled back (full app UI), push-in toward output
CTA clip:                    Static — intentional stillness (VP13 warmth contrast)
```

### Prohibited camera descriptions

```
"Static shot"             → unless CTA clip — specify a named movement instead
"No camera movement"      → unless CTA clip — specify why if intentional
"The camera stays still"  → unless CTA clip — this is a failed prompt
"Standard framing"        → not a camera instruction — specify the movement
```

---

## RULE 16 — ON-SCREEN CONTENT MUST BE REAL

**Applies to:** Every clip where text, prompts, responses, interface settings, or comparison panels are visible on screen.

**The pause test:** A viewer who pauses the video on any frame where text is visible must be able to read something useful. If the paused frame shows a label, an empty box, a placeholder, or dummy text — the visual fails. Every screen element must teach, not decorate.

### What is prohibited on screen

```
PROHIBITED — placeholder and dummy content:

"MY EXACT PROMPT"          → write the actual prompt
"PROMPT HERE"              → write the actual prompt
"AI response"              → write an actual Claude response excerpt
"Custom Instructions"      → write actual About Me and Response Style text
"settings"                 → show actual settings menu with readable labels
"Sample output"            → write actual topic-matched output
Lorem ipsum / filler text  → write real content
Unreadable small-text blocks → size for mobile; if unreadable, restructure
Generic labels on cards    → no label-only cards; the card IS the content
```

### The requirement: write the actual content in the Visual Action Map

When a spoken line causes text to appear on screen, the Visual Action Map entry for that line must include the actual on-screen text — not a description of what type of text will appear. The content written in the map entry is the generation direction.

```
WRONG:
"Claude.ai pe jao aur prompt daalo."
  → Visual: Prompt typed into Claude input field
  → Camera: Zoom toward input (2%)

RIGHT:
"Claude.ai pe jao aur prompt daalo."
  → Visual: Cursor clicks Claude's input field — text types character by character:
    "You are an expert content strategist for Indian creators.
     Generate 10 Instagram reel hooks for AI-curious professionals aged 25–35.
     Each hook: under 12 words, Hinglish, creates immediate curiosity or mild FOMO."
  → Camera: Zoom toward input field as text fills in (2% over 3s)
```

```
WRONG:
"Dekho — Custom Instructions fill karo."
  → Visual: Custom Instructions panel shows filled content
  → Camera: Rack focus from creator to panel

RIGHT:
"Dekho — Custom Instructions fill karo."
  → Visual: Custom Instructions panel — both fields populated and readable:
    About Me: "AI entrepreneur from India. Building Quantara, TradeCopilot, AI_SNIPP."
    Response Style: "Use Hinglish. Be direct. No corporate language. Actionable first."
  → Camera: Rack focus from creator to panel (0.5s) — panel snaps sharp
```

```
WRONG:
"Proof dekho — before aur after."
  → Visual: Split-screen showing two Claude responses — one generic, one on-brand
  → Camera: Pull-out to show both panels

RIGHT:
"Proof dekho — before aur after."
  → Visual: Left panel labeled "WITHOUT Instructions" — response visible:
    "Here are some tips for creating content..." (flat, generic, no personality)
    Right panel labeled "WITH Instructions" — response streams in:
    "Bhai, yeh 3 hooks try kar — pehla wala toh guaranteed scroll-stopper hai:
     1. Bete... LinkedIn pe AI skill nahi? 2027 mein regret pakka hai."
  → Camera: Pull-out to show both panels balanced in frame
```

### Proof scene content rule

Before/after comparisons must show meaningful, readable content in both states. Showing a blurry left panel and a readable right panel is not a comparison — it is a misdirection. Both sides must be legible. The contrast comes from content quality, not from obscuring one side.

### Acting direction and on-screen content are interdependent

If the character says "Look at the output," the output must be on screen and readable. The acting direction for a proof reveal should reference what is on screen: "Creator reads the response visible on screen — slow nod on 'meri voice, mera brand' line — genuine 'told you' micro-expression."

---

## VISUAL ACTION MAP — WORKED EXAMPLES BY FORMULA

---

### F01 — AI Cheat Code (4 clips)

**Clip 1 — Hook (B1, Dark Studio):**

```
VISUAL ACTION MAP:
"Bete... Claude use karte ho roz — aur Custom Instructions abhi tak empty hai?"
  → Visual: Creator full frame, centered. Steepled hands. Expression shifts from neutral
    to mock-disappointed on "empty hai."
  → Camera: Slow push-in (2% over 8s) — authority builds as camera closes in
"Claude nahin jaanta tum kaun ho."
  → Visual: Slight forward lean — weight shifts toward lens
  → Camera: Push-in continues — tightens slightly on "jaanta"
"Ye aaj fix karo."
  → Visual: Single decisive nod. Expression shifts: disappointment out, resolve in.
  → Camera: Push-in holds — frame slightly tighter than start
```

**Clip 2 — Tool Demo Phase 1 (B3, Desk Setup):**

```
VISUAL ACTION MAP:
"Claude.ai mein jao."
  → Visual: Browser navigates to claude.ai — URL bar visible — page loads
  → Camera: Slight zoom toward screen (2% over 1s)
"Profile, Custom Instructions."
  → Visual: Cursor moves to profile icon — clicks — dropdown slides down — cursor
    moves to Custom Instructions — clicks — panel opens
  → Camera: Follow zoom toward dropdown (3% zoom as menu appears)
"Do fields hain."
  → Visual: Custom Instructions panel visible — two empty fields with placeholder text
  → Camera: Rack focus from creator to panel — panel snaps to sharp focus
"Pehli: tum kaun ho. Doosri: response style."
  → Visual: Cursor moves to first field — text types in real time ("I'm a...") —
    cursor jumps to second field — text types in real time ("Respond in Hinglish...")
  → Camera: Slow pan down to follow cursor from field 1 to field 2
"Ek baar fill karo — hamesha apply hoga."
  → Visual: Save button click — success confirmation toast slides in ("Saved")
  → Camera: Pull back 2% to show both fields complete — small zoom out for context
```

**Clip 3 — Proof Reveal (B3, Facecam overlay):**

```
VISUAL ACTION MAP:
"Same prompt — bina instructions: generic output."
  → Visual: Claude.ai interface in dark mode. Label fades in top-left: "WITHOUT."
    Response is visible — flat, generic, impersonal tone. Slight desaturation on this half.
  → Camera: Frame on left half — slight pull-out to widen view
"Instructions ke saath: exactly meri voice, mera brand."
  → Visual: Right half wipes in from center — label: "WITH." Response streams in —
    warm Hinglish tone, structured, on-brand. Glow highlight animates over key lines.
    Full warm grade on this half.
  → Camera: Frame widens to show both halves — balanced reframe
"Ek 3-minute setup ka fark."
  → Visual: Both panels stable — highlight pulses once on the key differentiating phrase
    in the right panel — VP09 Proof Hold begins (music drops, 1.5s silence)
  → Camera: Static hold during Proof Hold — no movement
"Dekho."
  → Visual: Creator facecam (bottom-right) glances toward main content then returns to
    camera — small nod
  → Camera: Slight tighten on facecam for the nod — returns
```

**Clip 4 — CTA (B5, Dark Studio):**

```
VISUAL ACTION MAP:
"DM karo 'SYSTEM' — mera exact Custom Instructions template bhej dunga."
  → Visual: Creator full frame, eye level, open palm forward. "DM 'SYSTEM'" text
    overlay pops in at center frame as the word is spoken.
  → Camera: Static — intentional stillness (VP13 — warmth contrast with prior clips)
"Free hai. Aaj set karo."
  → Visual: Slight nod. Warm close expression. Text overlay fades.
  → Camera: Static — holds through fade to black (0.5s)
```

---

### F06 — AI vs Human (5 clips)

**Clip 1 — Hook (B1, Dark Studio):**
Camera: Slow push-in (3% over 5s)
Visual: Creator full frame — roast energy — steepled hands

**Clip 2 — Human Way (B6, Desk Setup):**
Camera: Parallax (creator moves right, background holds)
Visual: Creator mimes manual work — typing slowly, frustrated expression — timer
visible in corner, counting up — desaturated color grade

**Clip 3 — AI Way (B3, Desk Setup):**
Camera: Zoom in toward interface (4% over 8s)
Visual: Prompt typed into Claude — generation animation — output streams in —
timer in corner resets and counts: "2:47" — full warm grade returns

**Clip 4 — Proof (B7, Facecam overlay):**
Camera: Rack focus from creator to result — then pull back to show both
Visual: Side-by-side timer comparison animates — numbers grow — creator raises
eyebrow — "I told you" smirk

**Clip 5 — CTA (B5, Dark Studio):**
Camera: Static (VP13)
Visual: Creator eye level — open palm — warm close

---

### F09 — Three Step System (4 clips)

**Clip 1 — Hook (B1, Dark Studio):**
Camera: Push-in (3% over 5s)
Visual: Pre-save hook delivery — creator leans back on "Save karo pehle, phir dekho"

**Clip 2 — Step 1 (B2, Facecam overlay):**
Camera: Zoom toward content (3% as step appears)
Visual: Step 1 text overlay appears (number + action) — creator glances toward
content — interface shows Step 1 in action

**Clip 3 — Steps 2 + 3 (B2, Facecam overlay):**
Camera: Pan across steps as they appear — slight pull-out at end to show all three
Visual: Steps 2 and 3 appear sequentially — each with interface action — numbered
overlays animate in

**Clip 4 — CTA (B5, Dark Studio):**
Camera: Static (VP13)
Visual: Creator eye level — open palm — "Save karo" delivery — fade to black

---

## RULE 17 — NO SENTENCE-ENDING PERIODS IN FLOW PROMPT SCRIPTS

**Applies to:** The SCRIPT field and all quoted script lines in Visual Action Map entries.

Flow AI repeats dialogue when the SCRIPT field contains sentence-ending periods ("." or ".."). This is a generation engine behavior — not an occasional bug. It is consistent and must be designed around.

### The rule

Replace all sentence-ending periods with "—" (em-dash). Omit terminal punctuation on the last line. Sentences within a clip's script run together with "—" as the separator.

```
WRONG — periods cause dialogue repetition:
SCRIPT: "Claude.ai pe jao. Profile pe click karo. Custom Instructions kholo."

RIGHT — em-dash separates, no repetition:
SCRIPT: "Claude.ai pe jao — profile pe click karo — Custom Instructions kholo"
```

```
WRONG:
"Free hai. Aaj set karo."
  → Visual: ...

RIGHT:
"Free hai — aaj set karo"
  → Visual: ...
```

### What is still permitted

```
"?"  → Question marks are fine — intonation signal, not a repeat trigger
"..."  → Ellipsis in "Bete..." is fine — dramatic pause, not a trigger
"Claude.ai"  → Domain name dot is fine — not a sentence-ending dot
```

### Where this rule does NOT apply

Scene descriptions, camera directions, acting directions, and environment blocks may use periods normally. Flow does not read those as dialogue. The restriction is SCRIPT fields only.

---

## RULE 18 — BRANDING IN FINAL CLIP LAST 2 SECONDS

**Applies to:** The B5/CTA clip — always the final clip of every reel.

Flow generates each clip as a standalone video. Post-assembly overlays (added in CapCut/Premiere) are applied after generation. But because Flow generates and the editor assembles separately, branding that must be inside the clip must be written into the Flow prompt — not the Assembly Instructions.

### The requirement

The last Visual Action Map entry of the final CTA clip always includes @ai_snipp handle appearing on screen in the final 2 seconds of the clip. Flow generates this as part of the clip.

### Mandatory Visual Action Map entry for the last line of every CTA clip

```
"[Last spoken line of CTA script — no period]"
  → Visual: [Character action] "@ai_snipp" handle fades in bottom-left —
    white, clean sans-serif, readable at mobile size — appears 2 seconds
    before clip end — holds through fade-to-black.
  → Camera: Static (VP13 — CTA clip intentional stillness)
```

### What this looks like in a complete entry

```
"Aaj set karo"
  → Visual: Small sincere closing nod. "@ai_snipp" handle fades in
    bottom-left — white, Inter Regular, 14sp — appears at the 4-second
    mark of this 6-second clip — holds through the 0.5s fade-to-black.
  → Camera: Static — no movement — holds through fade.
```

### Why this is in the Flow prompt, not the Assembly Instructions

Assembly Instructions are applied in CapCut/Premiere after generation. If the editor forgets, or the clip is used standalone (shared, clipped, or reposted), there is no branding. Embedding branding in the Flow prompt guarantees it is always present, regardless of what happens in post.

---

## RULE 19 — KINETIC TEXT & FLOATING ICONS

**Applies to:** Every clip. Kinetic text and floating icons are embedded visual motion elements
written directly into Flow prompts. They are NOT added in the editor (unlike Assembly Instructions).
Because Flow generates them as part of the clip, they persist even if the clip is used standalone.

**Why they matter:** Kinetic text converts spoken words into on-screen proof that a viewer can
read without audio. On Instagram, 65%+ of reels are watched without sound on first pass.
A floating icon gives the eye a visual anchor while the character is speaking.

---

### KINETIC TEXT TYPES

```
POP-IN TEXT:
A single keyword or short phrase appears with a snap animation exactly as it is spoken.
Holds 1.5–2 seconds. Fades cleanly. Never overlaps the character's face.

Use for: Stats, key numbers, free/paid distinctions, trigger words.
Position: Center-top or center-bottom of frame. Never center-eye.
Style: White text, Inter ExtraBold, 1.5× the body text size. All-caps for numbers and verbs.
Prompt language: "As '[spoken word]' is delivered, '[OVERLAY TEXT]' pops in at center-top —
white, bold, 1.5s hold — fades before next line."

FADE-IN LABEL:
A context label fades in slowly (0.5s), holds for 2–4 seconds, fades out.
Lower energy than pop-in — sets context rather than punctuating a beat.

Use for: Repo names, tool names, section headings in list reels.
Position: Upper-left or upper-center of frame (top panel in split-screen clips).
Style: White or warm white, JetBrains Mono (for code/repo names), Inter Regular for labels.
Prompt language: "The label '[text]' fades in [position] — JetBrains Mono, white — holds [Xs]."

DM TRIGGER CARD:
The CTA trigger word appears in a styled callout — larger, center frame, slightly elevated.
This is the primary kinetic element in every Clip 4 (CTA clip).

Use for: The trigger word in DM campaigns (FREE, SYSTEM, LEARN, etc.)
Style: White, Inter ExtraBold, 2× body size. Clean. No border or shadow.
Prompt language: "As 'FREE' is spoken, 'DM "FREE"' appears center frame — white ExtraBold,
2× size — snaps in — holds 3 seconds — fades as the clip ends."

BADGE / PILL:
Small rounded badge appearing near relevant content. Contains a checkmark, number, or label.
Used for feature lists, step numbers, topic tags, and proof confirmation.

Use for: "✓ Free to run" on proof reveal; topic tags in B4 tool intro clips; step numbers in F09.
Style: White background, dark text, 12px border-radius. Emerald-500 (#10B981) for checkmarks.
Prompt language: "A small badge '✓ Free to run' in emerald-green pops in [position] as the
proof is revealed — holds 2s, fades."
```

---

### FLOATING ICONS

```
FLOATING ICON:
A small brand, category, or status icon drifts gently on screen. It is NOT static —
it has a subtle float animation (±3px vertical, 2s period). This prevents it from
reading as a watermark.

Use for: GitHub logo when showing GitHub repo; Python logo in code clips; star icon for
star counts; checkmark badge for proof reveal.

Opacity: 30–50% when decorative. 70–80% when it carries information (e.g., star count badge).
Position: Corner of the relevant panel — never overlapping character face or key text.
Size: Small — no larger than 24×24px equivalent in the generated frame.

Prompt language: "A small [icon name/description] icon drifts softly in the [position] corner —
[opacity]% opacity — gentle float animation — present throughout the clip / appears at [Xs] /
fades at [Xs]."
```

---

### KINETIC LAYER BLOCK — PER CLIP DEFAULTS FOR F04 (HIDDEN TOOL)

This is the baseline kinetic layer for F04 reels. Apply these defaults unless the clip's
specific content requires different overlays.

```
CLIP 1 — HOOK:
POP-IN TEXT:
  → "[N] LESSONS" — white bold — center-top — pops in on the lesson count — 1.5s hold
  → "FREE" — emerald-500 (#10B981) — center-top — pops in on "free" — 1.5s hold
  → "★ [N]K+" — white bold — center-top — pops in on star count — 1.5s hold
FLOATING ICONS:
  → None in Clip 1 — clean hook, no distractions

CLIP 2 — TOOL INTRO (TOP PANEL — GitHub repo):
FADE-IN LABEL:
  → Tool/repo name in JetBrains Mono — white — upper-center of top panel — fades in as
    name is spoken — holds for the duration of the clip
BADGE:
  → Topic badges fade in sequentially as topics are spoken (one per topic mentioned)
    e.g., "PROMPT ENG." → "RAG" → "AI AGENTS" → "FINE-TUNING" — white pills
    Position: bottom of top panel or lower-right of bottom panel — not overlapping face
FLOATING ICON:
  → GitHub mark (Octocat outline) — top-right of top panel — 35% opacity — gentle float

CLIP 3 — PROOF:
BADGE (STATE A — folder view):
  → "OPEN IN CODESPACES →" label near the green button in the top panel — white label,
    appears when the Codespaces button is visible — fades at STATE B transition
BADGE (STATE B — notebook running):
  → "✓ Free via GitHub Models" — emerald badge — pops in as Jupyter notebook STATE B
    appears — holds through proof hold
FLOATING ICON (STATE B):
  → Python logo — top-right of top panel — 40% opacity — appears at STATE B (4.0s)

CLIP 4 — CTA:
DM TRIGGER CARD:
  → 'DM "FREE"' — white ExtraBold — center frame — pops in exactly as "FREE" is spoken
    — 3s hold — fades before clip end
FADE-IN LABEL:
  → "@ai_snipp" — white Inter Regular — bottom-left — fades in 2 seconds before clip end
    — holds through fade-to-black (Rule 18 compliance)
```

---

### WRITING KINETIC LAYER IN A FLOW PROMPT

Add a KINETIC LAYER block to every Flow prompt immediately after the SCRIPT field.
The KINETIC LAYER replaces the need to write kinetic elements into the VISUAL ACTION MAP —
it lives as its own declared section so it is never omitted.

```
KINETIC LAYER:
→ TEXT: "21 LESSONS" — white ExtraBold — center-top — pops in on "21 lessons" — 1.5s hold
→ TEXT: "FREE" — emerald-500 — center-top — pops in on "free" — 1.5s hold — fades
→ ICON: GitHub Octocat outline — top-right corner — 35% opacity — gentle 2s float animation
→ BADGE: "✓ Free via GitHub Models" — emerald — pops in at 4.0s with STATE B — 3s hold
```

**Format rule:** Each item begins with its type (TEXT / ICON / BADGE / LABEL), then content
in quotes, then position, then timing. One line per element. No limit on elements per clip.

---

## APPLYING THIS TO NEW REELS

When generating Flow prompts, follow this sequence per clip:

```
1. Read the clip's script (exact words from the FULL SCRIPT section)
2. Break the script into individual sentences
3. For each sentence:
   a. Identify what visual action naturally accompanies those words
   b. Name the camera movement that supports that action
   c. Write both into the VISUAL ACTION MAP
4. Verify: is something moving in every sentence? If not — add motion.
5. Verify: is this a B3 clip? If yes — is the visual an actual interface interaction?
   (Not a static screenshot. Not a blurry panel. Actual interaction sequence.)
6. Verify: is this a proof clip? If yes — is the comparison animated or dynamic?
   (Not a static split-screen. Not two screenshots side by side.)
7. Verify: is the camera movement named? (Not "static" unless CTA clip.)
8. Verify: does any sentence cause text to appear on screen? If yes — is the actual
   text content written in the Visual Action Map entry?
   (Not "prompt appears" — write the actual prompt.
    Not "response visible" — write the actual response excerpt.
    Not "custom instructions filled" — write the actual field content.
    Apply the pause test: if a viewer froze this frame, could they read something useful?)
9. Verify: does the SCRIPT field contain any sentence-ending periods "." or ".."?
   If yes — replace with "—" before generating. (Rule 17 — Flow repeats on periods.)
10. Verify: is this the final CTA clip? If yes — does the last Visual Action Map entry
    include "@ai_snipp" branding fading in during the last 2 seconds? (Rule 18.)
    If not — add it before generating.
11. Verify: do the SCRIPT fields in this reel's Flow Prompts read as natural speech?
12. Verify (Lean Format only): does Clip 1 contain BOTH of the following?
    a. `@me — Indian male AI founder and creator —` in the character description line
    b. `Do not repeat any spoken words or phrases in the audio.` after the script line
    If either is missing — add before generating. These two lines solve the two most
    common Lean Format failures: accent drift (neutral instead of Indian) and
    word repetition in the generated audio.
    Verify Clips 2+ contain `Indian English delivery — same accent as Clip 1.` and
    `Do not repeat any spoken words or phrases.` in their ACTING DIRECTION blocks.
    Rule 17 requires em-dashes to replace sentence-ending periods — that is correct.
    But "—" should only connect sentences that would otherwise end in a period.
    Invalid: "Step — browse — click — copy karo" (fragment chain — sounds like bullet points)
    Valid:   "Meigen.ai kholo — apni pasand ka style choose karo — prompt copy kar lo"
             (three complete thoughts, each replacing a sentence-ending period)
    Each "—" separator must replace a period, not join unrelated micro-actions into a run-on.
    If a SCRIPT field reads like a fragmented command chain, rewrite as full spoken sentences
    joined by "—" only at natural sentence boundaries.
```

---

## FLOW ARCHITECTURE — GENERATION VS. ASSEMBLY

This is the model for how AI_SNIPP reels are produced:

```
FLOW AI (generation):
  One prompt → one standalone video clip → maximum 10 seconds per clip
  Flow cannot edit existing clips, assemble clips, or add post-production elements
  What goes in Flow prompts: character, scene, script, camera, Visual Action Map
  What Flow generates: the raw clip, including any branding described in the prompt

EDITOR — CapCut / Premiere / DaVinci (assembly):
  Imports all Flow-generated clips in order
  Joins clips with cuts or transitions
  Adds music, SFX, color grade, and text overlays not generated by Flow
  Exports the final reel

FLOW PROMPTS (Section 4 of every reel package):
  These go to Flow. One prompt per clip. Each clip ≤10 seconds.

ASSEMBLY INSTRUCTIONS (Section 5 of every reel package):
  These go to the editor. Flow cannot execute these.
```

This is why scripts are split into clips of 8–10 seconds each — not because of creative preference, but because of Flow's generation limit.

---

## WHAT THIS FILE DOES NOT DO

- Does not change the Master Seed Block (character identity is locked)
- Does not change the Continuation Block
- Does not change Scene Blocks B1–B7 descriptions
- Does not change Environment Blocks A–D descriptions
- Does not change the formula clip structures
- Does not change the script format or duration targets
- Does not change the acting direction system
- Does not change the CTA clip standards (eye level, static camera, warmth — these stay)

This file adds one new requirement to every Flow prompt: the VISUAL ACTION MAP block.
Everything else in the prompt architecture is unchanged.

---

## REVISION LOG

| Version | Change | Date |
|---|---|---|
| 1.0 | Created from REEL_001 post-production analysis. Rules 11–15 codified. | 2026-06-08 |
| 1.1 | Rule 16 added — On-Screen Content Must Be Real. Pause test defined. Step 8 added to clip generation sequence. | 2026-06-08 |
| 1.2 | Rule 17 added — No sentence-ending periods in Flow scripts (causes dialogue repetition). Rule 18 added — Branding in final clip last 2 seconds via Flow prompt. Flow architecture section added. Steps 9–10 added to generation sequence. | 2026-06-08 |
| 1.3 | Color Grade Drift added as motion technique for static assets (F03/F11 extended proof holds). B8 (Visual Problem Open) and B-SOCIAL (Platform Context Frame) added to motion budget table and camera assignment table. Platform Reveal camera movement added to Rule 15. | 2026-06-08 |
| 1.4 | Step 11 added to the generation sequence — natural speech quality check for Flow Prompt SCRIPT fields. Clarifies the correct use of Rule 17 em-dashes: valid when replacing sentence-ending periods; invalid when chaining unrelated micro-action fragments. Distinguishes the Flow Prompt SCRIPT field (Rule 17) from the FULL SCRIPT beats section (Rule 21 — natural spoken sentences). | 2026-06-09 |
| 1.5 | Rule 19 added — Kinetic Text & Floating Icons. Defines POP-IN TEXT, FADE-IN LABEL, DM TRIGGER CARD, BADGE/PILL, and FLOATING ICON types. Adds KINETIC LAYER block as a required section in every Flow prompt (after SCRIPT). Defines per-clip defaults for F04 formula. Verified on REEL_013 — kinetic text must be written into Flow prompts, not left for editor assembly, to ensure persistence when clips are used standalone. | 2026-06-13 |
| 1.6 | Step 12 added to generation checklist — two mandatory Lean Format checks. Fix 1: `@me — Indian male AI founder and creator —` anchors voice accent (without it, @me locks visual only and Flow defaults to neutral/Western accent). Fix 2: `Do not repeat any spoken words or phrases in the audio.` eliminates dialogue repetition in Flow generation. Both are verbatim phrases — do not paraphrase. Verified fixes from REEL_014 post-production. | 2026-06-13 |
| 1.1 | FORMAT UPDATE — VISUAL ACTION MAP and KINETIC LAYER blocks removed from Flow prompt format. Current prompt format uses attached image + IDENTITY LOCK (see flow_seed_prompts.md v2.0). VAM rules (11–16) and Rule 19 retained as reference. Rules 17 and 22 remain active. Rule 18 branding moved to Assembly. Format update section added at top of file. | 2026-06-14 |

*The failure mode this file prevents: a clip where the character speaks about clicking
something and nothing on screen clicks. Narration and visuals must be one synchronized
track — not two independent pieces running in parallel.*
