# AI_SNIPP — Production Mode

**Status:** Canonical — this is the execution layer of AI_SNIPP OS  
**Purpose:** When Production Mode is ON, Claude produces only production assets. Input goes in, complete reel package comes out.  
**Location:** `D:\AI_OS\05_content\AI_SNIPP\production_mode.md`

---

## CONTENT PIPELINE SKILLS

The AI_SNIPP pipeline has these Claude Code skills:

| Skill | When to use |
|---|---|
| `/automate-reel` | **FULL AUTOMATION** — topic → assembled video, ready to post. Runs /create-reel + Higgsfield generation + FFmpeg assembly. One command, video is ready. |
| `/create-reel` | Script + Flow prompts + caption package only (no video generation — for manual Flow workflow) |
| `/reel-analyzer` | Study a viral reel → extract structure → inform your script |
| `/viral-hook-writer` | Generate 10 hook options before committing to a script |
| `/content-repurposer` | Turn one source (insight, milestone, tool demo) into 5 reel concepts |
| `/caption-and-hashtags` | Write publish-ready caption + tiered hashtags + first comment |

**Full automation pipeline (recommended — one command, video is ready):**  
`/automate-reel [topic]` → ready-to-post MP4 + caption package

**Research-first automation:**  
`/reel-analyzer` → `/viral-hook-writer` → `/automate-reel [topic]`

**Prompts-only pipeline (if you prefer manual clip generation in Flow web):**  
`/create-reel` → `/caption-and-hashtags`

**One-time setup required before first `/automate-reel` run:**  
`/automate-reel setup` → registers your character as a Higgsfield Element (2 minutes)

---

## ACTIVATION

Give Claude one of these inputs and nothing else:

```
PRODUCTION MODE: [topic description]
```
> Formula auto-selected. Example: `PRODUCTION MODE: LinkedIn post likhne mein AI vs manually`

```
PRODUCTION MODE F[NN]: [topic description]
```
> Formula pre-specified. Example: `PRODUCTION MODE F06: LinkedIn post likhne mein AI vs manually`

```
PRODUCTION MODE F[NN] CTA=[WORD]: [topic description]
```
> Formula + trigger word specified. Example: `PRODUCTION MODE F01 CTA=SYSTEM: Claude custom instructions`

No other input is needed. Claude does not ask questions before generating (see Failure Modes for the one exception).

---

## RESEARCH PHASE — MANDATORY PRE-PRODUCTION

Before any production rule runs, research executes on the topic. This applies whether Production Mode is triggered via `/create-reel` or invoked directly.

**When invoked via `/create-reel`:** Research runs inside the daily_reel_generator workflow — before Production Mode activates. The angle is already selected when production begins.

**When invoked directly via `PRODUCTION MODE: [topic]`:** Research runs immediately after the topic is parsed, before Rule 1 applies.

Research is never reported. It produces no user-facing output. It informs:
- The specific angle the script leads with
- The hook's claim (surprising insight vs. generic statement)
- The proof evidence cited in the script

**Outcome-First Principle (applied before any angle is scored):**
Ask: "What result would make a viewer immediately try this?" The angle that answers this question most compellingly is scored highest. Research starts with the outcome — not with features, not with a platform walkthrough.

**Intent Classification (internal — before information gathering):**
Classify the topic into one of six types. Research focus adapts:

| Intent Type | Research Focus |
|---|---|
| Discovery Tool | Shortcuts, ready-made assets, instant wins — not walkthroughs |
| Workflow Tool | Non-obvious systems, hidden features — not feature lists |
| News | Indian relevance, immediate viewer impact — not press release |
| Transformation | Proof quality, gap size — not creation steps |
| Comparison | Decisive winner, surprising result — not balanced review |
| Experiment | Unexpected outcome, replication difficulty — not methodology |

**Script Emotion Map (internal — runs after angle is selected, before any beat is written):**

Map the viewer's emotional state across the reel's beats. Content follows function — the map tells you what each beat must *accomplish*, not what it must *contain*.

| Beat | Viewer Entry State | Script Goal | Exit State Target |
|---|---|---|---|
| Hook | Passive scroll, identity unknown | Pattern interrupt → identity claim | Stopped. Leaning in. |
| Beat 2 | Curious, skeptical | Deliver the surprising insight — not features | "Wait — I didn't know that" |
| Beat 3 | Interested, engaged | Show proof + surface the counterintuitive piece | "I need to try this today" |
| Beat 4 (CTA) | Convinced, processing | Remove last friction. Make action feel obvious. | Taking action now |

For each beat, answer before scripting: **"What single line will the viewer quote to a friend tomorrow?"** That line is the keystone of the beat — write toward it.

**10-angle discovery (internal — not reported):**

| Angle | What It Surfaces |
|---|---|
| Obvious | The expected take — used only if no stronger angle exists |
| Contrarian | Challenges the common narrative with verifiable evidence |
| Hidden Feature | Underused or unknown capability most creators have missed |
| Workflow | A practical, repeatable system demonstrable in ≤35s |
| Future Impact | What this topic means for the audience 6–12 months from now |
| Shortcut | Fastest path to the result — skips steps most people don't know are skippable |
| Mistake | The common error most people are making, with the correction |
| Comparison | Head-to-head, ends with a decisive winner |
| Experiment | Unexpected outcome from trying something |
| Transformation | Same input, dramatically different output — the gap is the content |

Generate all 10 before selecting. Angles 6–10 score higher for Discovery Tool and Transformation intent types.

**Topic Validation (5 gates — internal — not reported):**

1. Is this topic still relevant and timely?
2. Has this exact angle been published by a top competitor in the last 3 days?
3. Is there a stronger angle available from the 5 candidates?
4. Is there sufficient proof — demonstrable on screen with real output?
5. Can this become a compelling reel in ≤35 seconds?

Any gate fails → topic rejected → QUALITY GATE DEFERRED notice output (Failure Mode 7). No partial production.

**Angle selection rule:** The highest-scoring outcome-oriented angle wins. Generic framing ("Top N features," "Best AI tool," "New update") and tutorial-style walkthrough angles are used only when research produces no stronger outcome or shortcut alternative. Tiebreaker: select the angle where a viewer could reproduce the result in the next 30 minutes.

---

## PRODUCTION MODE RULES

**Rule 1 — Output Only**  
Production Mode produces production assets. It does not explain formula selection, discuss alternatives, or write analysis paragraphs. Every line of output is either a production asset or a section header. No commentary before, between, or after sections.

**Rule 2 — Character Auto-Lock**  
The character identity lock is applied in every clip. Two formats are available — choose based on clip type:

**FULL FORMAT (required for):** Clip 1 of any reel. Any split-screen or facecam clip (B2, B3, B4) where the character appears at reduced size. Any clip where the environment changes significantly from the previous clip.

Use the complete CHARACTER IDENTITY LOCK block verbatim. The Continuity Block (Clips 2+) comes AFTER the identity lock — it supplements it, never replaces it.

**SIMPLIFIED FORMAT (permitted for):** Full-screen talking head clips only (B1, B6, B7) in Clip 2+ position, when generating in a session with Character.png attached. Frame the prompt as a continuation and use this 2-line lock:

```
Character Continuity: Use the attached image as a strict identity lock.
Maintain the exact same face, glasses, curly hair, black t-shirt, camera framing and lighting.
```

Then open the task with: `"Generate an [X]-second vertical (9:16) continuation of the previous clip."`

Why: For full-screen clips in a single session, the attached image carries the identity. "Continuation" framing instructs Flow to treat all clips as one creative act — same person, same world — which produces stronger consistency than repeating a 15-line text block. Verified: best character quality observed (best clip analysis, 2026-06-10) used this format.

Claude never writes "[PASTE MASTER SEED BLOCK]", "[SAME AS CLIP 1]", or any placeholder shorthand. Claude never asks about the character. The character is always applied.

**Rule 3 — Formula Auto-Select**  
If no formula is specified, Claude selects the best-fit formula using the decision tree in `02_formulas/formula_index.md`. The choice appears in the REEL HEADER. It is applied, not explained.

**Rule 4 — All Six Hard Gates Checked Before Output**  
Before generating anything, Claude internally verifies all six gates from `01_research/topic_evaluation_framework.md`: Genuine Value, Specificity, Personal Proof, Novelty, Format (≤35s), Brand Safety. Any failure stops production and outputs only the rejection notice. See Failure Modes.

**Rule 5 — Flow Prompts Are Complete**  
Every Flow prompt is copy-paste ready. No `[INSERT SCRIPT HERE]` placeholders remain. No `[CHOOSE ONE]` options remain. Every decision is made by Claude before output is produced.

**Rule 6 — Script Word Count Discipline**  
Scripts stay within the formula's duration window. Self-check: at 2.5 words/second, 70 words = 28s. If script exceeds the window, Claude cuts it — it does not note the excess or ask permission.

**Rule 7 — Single Primary CTA**  
Every reel has one primary CTA spoken on camera. A secondary CTA may appear in the caption. Never three CTAs. Never a vague CTA ("let me know in the comments what you think").

**Rule 8 — English Scripts by Default**  
All scripts are delivered in English. Clean, direct, conversational English with em-dash connectors between beats — not comma-separated run-ons, not Hinglish. No Hindi words, no "Bete...", no Hindi openers. Technical terms (Claude, ChatGPT, API, prompt, workflow) stay in English as they always were. Captions may use Hinglish phrasing for audience resonance, but the spoken SCRIPT field in every Flow prompt is English.

**Rule 9 — No Soft Language**  
Scripts do not include "possibly," "maybe," "you might want to," "I think," or "kind of." Claims are stated as facts. Delivery is confident. The character already knows this works.

**Rule 10 — Viral Pattern Applied**  
Minimum one viral pattern from `01_research/viral_pattern_library.md` (VP01–VP15) is selected and applied per reel. The pattern is noted in the HOOK section. Its implementation spec is applied in the Flow prompts and editing instructions.

**Rule 11 — Visual Action Mapping**  
Every spoken line in a Flow prompt must have a corresponding Visual Action and Camera Movement. Narration and visuals are never disconnected. If the script says "jao," the interface opens. If the script says "click karo," a cursor clicks. A clip where the character speaks and nothing on screen responds is a failed clip. See `flow_generation_template.md` for the full standard.

**Rule 12 — Demo Scene Standards (B3)**  
Tool demo clips must show actual interface interaction: browser opening, cursor moving, menus expanding, panels loading, generation starting. Prohibited without exception: static prompt boxes, blurry UI panels, generic dashboard placeholders, large unreadable text blocks. The visual must mirror the spoken instruction — word for word.

**Rule 13 — Proof Scene Standards**  
Proof clips must use animated comparisons, highlighted outputs, reveal motion, or dynamic before/after transitions. Prohibited: static screenshots, static split-screens without motion. The proof must communicate the outcome visually — not through narration alone. If a proof clip cannot be made dynamic, the clip structure must be redesigned.

**Rule 14 — Motion-First Design**  
Every clip must answer: "What is moving?" If nothing is moving, the clip is wrong. Required — at least one of the following per clip: character movement, camera movement, interface movement, object movement. Static clips are a production failure, not a style choice.

**Rule 15 — Camera Language**  
Camera direction must specify a named movement for every clip: push-in, pull-out, parallax shift, focus rack, dynamic reframe. "Static" is only permitted on the CTA clip where intentional stillness creates warmth contrast with the preceding clips. Every other clip must name its camera movement explicitly.

**Rule 16 — On-Screen Content Must Be Real**  
Any text, prompt, response, settings panel, or comparison element visible on screen must contain realistic, substantive, and topic-matched content. Placeholder labels, dummy text, and unreadable blocks are production failures.

The pause test: if a viewer pauses on any frame where text is visible, they must be able to read something useful. A paused frame showing "MY EXACT PROMPT," "AI response," "custom instructions," or lorem ipsum fails. Every screen element must teach, not decorate.

When writing the Visual Action Map entry for a line that causes text to appear on screen, write the actual on-screen text inside the entry — not a description of the content type. "Prompt appears on screen" is wrong; the actual prompt text is right. This applies equally to: prompts typed into AI tools, AI responses shown on screen, custom instructions panels, settings menus, before/after comparison panels, and all overlaid text cards. See `flow_generation_template.md` Rule 16 for worked examples.

**Rule 17 — No Sentence-Ending Periods in Flow Prompt Scripts**  
Flow AI repeats dialogue when it encounters sentence-ending periods ("." or "..") in the SCRIPT field of a Flow prompt. These characters trigger repetition artifacts in the generation engine.

In every SCRIPT field inside a Flow prompt: replace sentence-ending periods with em-dashes ("—") or omit terminal punctuation entirely. Run sentences together with "—" as the separator.

Permitted: "?" question marks — intonation signal, not a repeat trigger  
Permitted: "..." ellipsis in openers like "Bete..." — dramatic pause, not a repeat trigger  
Permitted: Dots within domain names — "Claude.ai" is a non-sentence dot, not a repeat trigger  
Prohibited: "." at the end of any sentence in a SCRIPT field  
Prohibited: ".." anywhere in a SCRIPT field  

Wrong: `"Claude.ai pe jao. Profile pe click karo. Custom Instructions kholo."`  
Right: `"Claude.ai pe jao — profile pe click karo — Custom Instructions kholo"`  

Wrong: `"Free hai. Aaj set karo."`  
Right: `"Free hai — aaj set karo"`  

This rule applies to: the SCRIPT field in every Flow prompt, and quoted script lines inside Visual Action Map entries. Scene descriptions, camera directions, and acting directions may use periods normally — Flow does not read those fields as dialogue.

**Rule 19 — Extended Proof Hold for Visual Output Formulas**  
When the AI output being demonstrated is primarily visual (a poster, image, design, video frame), the proof clip is NOT limited to the standard 1.5s Proof Hold (VP09).

The output must hold on screen for a **minimum of 10 seconds**.  
No narration during the first 5 seconds — let the image speak.  
Music drops to 10% for the first 5 seconds, then returns to 25%.  
Color grade may drift subtly (±5% warmth) during the hold to create implied motion on a static asset.

The 10-second floor is a confidence signal: a short hold signals the creator doesn't trust their own output. Extended holds signal quality.

This rule supersedes VP09 for F03 and F11 formulas only. All other formulas retain the 1.5s standard VP09 Proof Hold.

**Rule 20 — Platform Context Frame (F03 and F11 only)**  
Every F03 and F11 reel must contain one clip showing the AI output inside the real platform where it will be distributed.

This clip shows: the Instagram Reels upload interface, or the LinkedIn post composer, or the WhatsApp share screen — with the AI output loaded and ready to post.

Purpose: answers the viewer's implicit "but does this actually work and can I really post it?" before they ask.

This is NOT a demo clip. It does not show the creation process. It shows the output in its final platform context.

Clip duration: 3–5 seconds. Camera: slow push-in toward the output inside the interface.  
Block code: B-SOCIAL (see prompt_blocks.md).

**Rule 18 — Branding in Final Clip Last 2 Seconds**  
The final clip of every reel (always the B5/CTA clip) must display the @ai_snipp handle visibly in its last 2 seconds. This branding is written into the Flow prompt's Visual Action Map so Flow generates it as part of the clip. It cannot be added reliably in post-assembly.

Required: "@ai_snipp" handle — white, clean sans-serif, readable at mobile size. Positioned bottom-left or bottom-center. Fades in over 0.3s — holds through clip end.

The last Visual Action Map entry of the CTA clip always includes:  
`→ Visual: "@ai_snipp" handle fades in bottom-left — white, clean, readable — holds for the final 2 seconds of the clip through fade-to-black.`

**Rule 22 — Flow Clip Word Limit**  
Flow AI repeats dialogue when the script contains more words than can be naturally spoken in the clip duration. This produces audible looping and is the most common Flow generation failure.

Word limits differ by script language. Apply the correct column based on the SCRIPT field language:

| Clip Duration | English Max | English Hard Limit | Pure Hindi Max | Pure Hindi Hard Limit | Action if exceeded |
|---|---|---|---|---|---|
| 5s | 12 words | 14 words | 18 words | 22 words | Split into two clips |
| 6s | 14 words | 17 words | 22 words | 26 words | Split into two clips |
| 7s | 16 words | 20 words | 26 words | 30 words | Trim script |
| 8s | 20 words | 24 words | 35 words | 40 words | Trim script |
| 9s | 22 words | 26 words | 38 words | 44 words | Trim script |
| 10s | 25 words | 28 words | 42 words | 48 words | Maximum — do not exceed |

**English pace:** 2.3–2.5 words/second.  
**Pure Hindi pace:** 4.0–4.6 words/second (conversational Hindi flows faster — verified: 37 words at 8s, perfect sync, best clip analysis 2026-06-10).  
**Mixed scripts:** Count Hindi and English words separately. Use English limit for English words, Hindi limit for Hindi words, then add — the blend falls between columns.

Count words in the SCRIPT field of each individual clip prompt. Total reel word count (Rule 6) does not substitute for per-clip checking.

Note: Flow always generates clips at exactly the requested duration. A 5s CTA clip requested at 10s will loop its script to fill the remaining 5 seconds. Always specify the correct target duration in the CLIP DURATION field.

**Mandatory pre-output word count table (required before writing any SCRIPT field in SECTION 4):**

Every reel must include this table between SECTION 2 and SECTION 3. Words are explicitly counted — never estimated. If any clip fails, the SCRIPT is trimmed before proceeding.

```
WORD COUNT VERIFICATION:
| Clip | Duration | Word Count | Limit (Max/Hard) | Status |
|------|----------|------------|------------------|--------|
|  1   | [X]s     | [N] words  | [M] / [H]        | ✓ / ❌ |
|  2   | [X]s     | [N] words  | [M] / [H]        | ✓ / ❌ |
|  3   | [X]s     | [N] words  | [M] / [H]        | ✓ / ❌ |
|  4   | [X]s     | [N] words  | [M] / [H]        | ✓ / ❌ |
|  5   | [X]s     | [N] words  | [M] / [H]        | ✓ / ❌ |
```

Any ❌ = script trimmed immediately. No ❌ may appear in the final output. The table is reported in the output between SECTION 2 and SECTION 3 so the user can verify.

**Rule 23 — Flow Watermark Coverage**  
All Flow-generated clips contain a 4-pointed sparkle watermark icon in the bottom-right corner. It is always present and must be addressed in every reel's Assembly Instructions.

Required in every Assembly Instructions section:
```
WATERMARK: Add a solid 50×50px black rectangle overlay in the bottom-right corner of every clip OR crop 50px from the right + 60px from the bottom on all clips before color grade.
```

**Rule 24 — Flow Session Discipline**  
Character consistency breaks when clips are generated across different Flow sessions without a reference frame. All clips for a single reel must be generated in the same Flow session with Character.png attached at session start. If a session must be reopened for regeneration, add this to the regenerated clip's prompt:

```
VISUAL REFERENCE: This character must match the attached approved frame exactly. Same face structure, same skin tone, same curl texture, same glasses. This is a regeneration — do not interpret as a new character.
```

Attach both Character.png AND a frame from an already-approved clip from the same reel when regenerating.

**Rule 25 — Full-Frame and Split-Screen Sessions**  
When a reel contains both full-frame character clips AND split-screen clips (where the character appears in one half), generate them in the same session. Split-screen clips generate a bottom-half character from the same description — if the session changes, the character in the split-screen bottom half becomes a different person.

If sessions must be separate: provide Character.png + an approved full-frame clip frame as the reference in the split-screen session, and state explicitly: "The character in the lower half of this split-screen must match the attached reference frame exactly."

**Rule 26 — Negative Gesture Constraints for Number Mentions**  
Flow defaults to having the character hold up fingers when spoken numbers are detected in the script. This breaks authentic delivery — it looks like teaching, not talking. A creator never counts their fingers when speaking to a friend.

When a script contains any number word or digit (3, teen, ek, do, char, 5, etc.), add explicit negative gesture constraints to the Acting Direction field:

```
Do not count with fingers. Do not raise [N] fingers. Do not make number gestures while speaking. Keep hands relaxed and natural throughout.
```

Substitute [N] with the specific number in the script. If multiple numbers: list each. ("Do not raise 2 fingers. Do not raise 3 fingers.")

Applies to: numbered lists ("teen cheezein"), specific counts ("3 AI tools"), step references ("Step 1", "Step 2"), any digit in the SCRIPT field.

This constraint is required — not optional. Verified: the best clip (2026-06-10) mentioned "3 certifications" and used these exact negative constraints. Zero finger gestures appeared.

**Rule 21 — Natural Spoken Script Format**  
Script beats in SECTION 2 (FULL SCRIPT) must read as natural spoken language. Each beat consists of short sentences separated by line breaks — not chained by em-dashes or pipe symbols.

Write script beats as a human would speak them:
```
BEAT 2 — DEMO (8s):
Meigen.ai kholo.
Yahan 3000 se zyada ready-made prompts hain.
Apni pasand ka style choose karo.
Bas prompt copy kar lo.
```

Not as fragment chains:
```
BEAT 2 — DEMO (8s):
Step 1 — BROWSE — Meigen.ai pe jao — 3000 prompts hain — copy karo
```

Fragment chains sound like bullet points when spoken — not like a person talking. Short sentences with natural breathing rhythm match the character's conversational delivery.

**Scope:** This rule applies to SECTION 2 (FULL SCRIPT) beats — what the creator reads and speaks. Rule 17 (em-dashes replace sentence-ending periods) applies to the SCRIPT field inside Flow Prompts only — what Flow AI reads. These two rules govern different parts of the package and do not conflict.

---

**Rule 27 — Script Energy, Interactivity & Discovery Standard**

Every script is written as a **discovery narrative**, not an instructional walkthrough. The voice is a skilled, enthusiastic scriptwriter reporting on something already experienced — not a teacher dictating steps to a student.

**The two modes — one is banned:**

INSTRUCTIONAL (banned for body beats):
```
Claude.ai pe jao — Custom Instructions open karo — yeh paste karo — save karo.
```
Effect: sounds like a tutorial. Viewer shifts to passive reception. Scroll risk spikes.

DISCOVERY NARRATIVE (required):
```
There's a setting in Claude most people skip right past — Custom Instructions.
I added one line there — 27 words — and my response quality immediately doubled.
I'm showing you the exact line right now.
```
Effect: viewer leans in. A reveal is coming. They need to know what the line is.

**Interactive language techniques — apply minimum 2 per reel:**

| Technique | What It Sounds Like |
|---|---|
| Direct address | "your tool", "watch what happens when you do this", "I'm showing you exactly" |
| Micro-reveal | Hint at the payoff before delivering it — "and this is where it gets interesting" |
| Curiosity gap within beats | "But here's what I didn't expect..." mid-script — a beat-level cliffhanger |
| Discovery framing | "I was doing X when I noticed Y" — narrative arc, not step-by-step |
| Contrast setup | "Everyone does it this way. I tried this instead. The gap surprised me." |
| Present-tense immediacy | "I'm opening this right now — watch what loads" |
| Reaction invitation | "The output? I'll show you in a second — stay with me" |

**Enthusiasm markers — required, minimum 1 per clip:**

| Marker | What It Sounds Like |
|---|---|
| Time compression reveal | "This took 3 seconds. 3 seconds." |
| Insider signal | "I use this every single day" |
| Payoff signaling | "And this is the part that made me stop" |
| Discovery confirmation | "I couldn't believe this was already built in" |
| Value assertion (evidence-backed) | "This alone makes the subscription worth it" |
| Specificity anchor | "Not 'a while' — 8 minutes. Clocked it." |

**What is banned:**
- Command chains as primary content: "go to X, click Y, copy Z" as the body of a beat
- Passive delivery: "This tool has 3 features" → replace with: "I found 3 things in this tool I now use every day — and none of them were in the launch post"
- Hedged enthusiasm: "I think you might like this" → replace with: "This changed how I work"
- Generic reaction: "Isn't that amazing?" → replace with a specific reaction to a specific detail — "The response came back in 4 seconds. The manual version takes me 40 minutes."

**Script research before writing (internal — inform every beat):**

Before scripting beats 2–4, answer for each beat:
1. **What is the viewer thinking right now?** (Skeptical? Curious? Hooked? About to scroll?)
2. **What is the one surprising thing in this beat?** (Not the feature — the insight the feature enables.)
3. **What single line will the viewer quote to a friend tomorrow?** — Write the rest of the beat to build toward this line.

The answer to #3 is the keystone line of the beat. It is never generic. It is specific, quotable, and deliverable in 6–10 words.

**Applies to:** All body beats (beats 2, 3, 4) in every formula. Hook beat (beat 1) is governed by hook_library.md — these rules extend the hook's energy into the body. CTA beat: enthusiasm markers apply; command chains permitted only for the CTA action itself ("DM karo 'TOOLS'").

**Source file:** `01_research/script_writer_guide.md` — full vocabulary, beat patterns, worked examples, and formula-specific discovery wirings.

---

## PRODUCTION MODE OUTPUT FORMAT

Every Production Mode session produces exactly these sections, in this order. No section is optional.

---

```
════════════════════════════════════════════════════════
REEL: REEL_[NNN]  |  [YYYY-MM-DD]
════════════════════════════════════════════════════════
TITLE:          [10-word max working title]
FORMULA:        F[NN] — [Formula Name]
DURATION:       [XX]s
PRIMARY METRIC: [Save / Follow / DM / Comment — one only]
EST. TIME:      [Production time from formula_index.md]
CTA TYPE:       [DM / Follow / Save / Comment]
TRIGGER WORD:   [CAPITALIZED — for DM CTAs] or [N/A]
VIRAL PATTERN:  VP[NN] — [Pattern Name]
════════════════════════════════════════════════════════
```

---

### SECTION 1 — HOOK

```
[Single hook line — English — max 15 words]

HOOK TYPE:   [Category from hook_library.md]
PATTERN:     [VP0X — how applied]
```

---

### SECTION 2 — FULL SCRIPT

```
BEAT 1 — HOOK ([Xs]):
[Exact English words]

BEAT 2 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 3 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 4 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 5 — CTA ([Xs]):
[Exact English words]

WORD COUNT: [N] words | EST. DURATION: [X]s at 2.5 words/sec
```

---

### SECTION 3 — SCENE BREAKDOWN

```
| Clip | Dur | Block | Script (first 8 words)     | Camera     | Env | Special          |
|------|-----|-------|----------------------------|------------|-----|------------------|
|  1   | 8s  | B1    | "[hook words...]"          | MCU below  | A   | Push-in          |
|  2   | 8s  | B2    | "[beat 2 words...]"        | MCU below  | A   | Facecam overlay  |
|  3   | 8s  | B3    | "[beat 3 words...]"        | MCU below  | D   | Tool demo        |
|  4   | 7s  | B7    | "[reveal words...]"        | Eye level  | A   | Proof hold 1.5s  |
|  5   | 5s  | B5    | "[CTA words...]"           | Eye level  | A   | Warm close       |
```

Block codes: B1=Hook · B2=Facecam · B3=Tool Demo · B4=News · B5=CTA · B6=Storytelling · B7=Reaction  
Environment codes: A=Dark Studio · B=Clean Minimal · C=News Room · D=Desk Setup · W=Warm Creator Home Studio

---

### SECTION 4 — FLOW PROMPTS

One complete, copy-paste-ready prompt per clip. No fill-in-the-blank fields remain.

**FLOW CLIP LIMIT: Each clip must be ≤10 seconds.** Flow AI cannot generate clips longer than 10 seconds. If any beat exceeds 10 seconds, split it into two clips and add a row to the Scene Breakdown. All formula clip durations are designed to stay within this limit.

**Prompt structure (applied to every clip — CHARACTER IDENTITY LOCK is written in full in EVERY clip, never replaced with a placeholder):**

```
CLIP [N] OF [TOTAL] — [SCENE TYPE]
════════════════════════════════════════════════════════
CHARACTER IDENTITY LOCK — DO NOT DEVIATE FROM THIS DESCRIPTION:

Use the attached reference image as the strict visual anchor for the character.

The character is an Indian male, mid-to-late 20s. Warm medium-brown skin tone with amber undertones.

Hair: Tight natural coil curls, densely packed, deep black, medium length on top with natural volume, short and close-cropped on the sides. The curl texture is a defining feature — preserve it exactly.

Beard: Short full beard, approximately 5–10mm length, well-trimmed edges, deep black, covers full jaw and chin area cleanly.

Glasses: Matte black rectangular frames, medium-width, slightly wide-set. Standard clear lenses. Always present. This is a brand-defining element.

Build: Average to lean athletic. Broad shoulders visible. Natural upright posture.

Clothing: Plain black V-neck t-shirt, well-fitted. A small black lavalier microphone is clipped at the center chest. A dark/black sports watch is visible on the left wrist.

IDENTITY RULE: The face, hair texture, beard, and glasses must remain identical across all clips. These are LOCKED.

════════════════════════════════════════════════════════
[CONTINUITY BLOCK — Clip 2+ only — add AFTER identity lock, not instead of it:]
CONTINUITY NOTE: This is Clip [N] in a series. The character is the same individual as in previous clips. DO NOT change the character's appearance. All identity elements are locked: same face, same tight coil curls, same matte black rectangular glasses, same beard, same skin tone. Only the action, script, and [approved variation if any] changes.

════════════════════════════════════════════════════════
SCENE TYPE: [Scene block from prompt_blocks.md — full text]

ENVIRONMENT: [Environment block from flow_seed_prompts.md — full text]

CLIP DURATION: [X] seconds, vertical 9:16.

SCRIPT: "[Exact English script — complete — no ellipsis]"

ACTING DIRECTION: [Specific direction — named emotion + specific body language, not "be natural"]

VISUAL ACTION MAP:
"[First sentence of script — exact words]"
  → Visual: [what moves or appears on screen during this line]
  → Camera: [named movement — push-in / pull-out / focus shift / parallax / zoom / rack]
"[Second sentence of script — exact words]"
  → Visual: [what moves or appears on screen]
  → Camera: [named movement]
[one entry per spoken sentence — no sentence may be left without a visual action and camera movement]

OUTPUT: High quality, high retention vertical 9:16. Professional creator aesthetic.
════════════════════════════════════════════════════════
```

---

### SECTION 5 — ASSEMBLY INSTRUCTIONS

**FLOW ARCHITECTURE — HOW THIS WORKS:**  
Flow AI generates standalone video clips. One prompt → one clip → max 10 seconds. Flow does not edit clips, assemble clips, apply color grades, add music, or add text overlays after generation.

Section 4 (Flow Prompts) → sent to Flow → generates raw clips, one at a time.  
Section 5 (Assembly Instructions) → applied by the human editor in CapCut / Premiere / DaVinci AFTER all Flow clips are downloaded and assembled.  

Flow cannot execute these instructions. They are for the editor only.  
Exception: Branding and text described inside a Flow prompt's Visual Action Map are generated by Flow as part of the clip.

Numbered steps only. No paragraphs.

```
ASSEMBLY:
1. Import Flow-generated clips in order: Clip 1 → Clip 2 → Clip 3 → [...]
2. [Specific cut timing or transition between clips]
3. [Any composite instruction — e.g., text overlay added in editor on Clip N]

COLOR GRADE:
1. Clip [N]: [Specific grade — e.g., -10% saturation, -5% warmth]
2. Clips [N–N]: Full warm grade (default — no adjustment needed)
3. [Formula-specific grade from the table below]

TEXT OVERLAYS (added in editor — not in Flow):
1. 0:00 — [Text content] — [Position] — [Entry style: pop/fade] — Exit at [timestamp]
2. 0:[XX] — [Text content] — [Position] — [Entry style] — Exit at [timestamp]
Note: @ai_snipp branding in the final clip is generated by Flow (Rule 18).
      All other watermarks and labels are added by the editor here.

SOUND FX (added in editor — not in Flow):
1. 0:[XX] — [SFX type] — [Level %]
2. 0:[XX] — [SFX type] — [Level %]
[Music: Track mood: [descriptor]. Background level: 25–30%. Speech always primary.]

EXPORT:
Resolution: 1080×1920 | Codec: H.264 | Frame rate: 30fps | Bitrate: 10 Mbps
```

**Formula-specific color grade rules (auto-applied):**

| Formula | Special Grade Instruction |
|---|---|
| F06 — AI vs Human | Clip 2 (Human Way): -10% saturation, -5% warmth. Visual signal of "before." Return to full warm grade from Clip 3 onward. |
| F07 — News Flash | Clip 1: -5% saturation, slight cool shift (+3% blue). News-desk urgency signal. Warm grade from Clip 2 onward. |
| F08 — Transformation | Clips 1–2 (Before): -15% saturation, -8% warmth. Clip 3+ (After): +5% warmth, +5% vibrance. Make the gap visual. |
| F02 — Future Shock | Clip 1: Slight cool grade, slight vignette. Urgency signal. Warm from Clip 2 onward. |
| F11 — Ego Output | Clip 1 (B8): -8% saturation, +3% blue — "before" signal. Clips 2–3: Full warm grade. Clip 4 (Proof): Grade drifts +5% warmth over first 8s, returns -3% by clip end — creates perceived motion on static image. Clip 5 (B-SOCIAL): Neutral — platform UI must look exactly like the real app. Clip 6 (CTA): Full warm grade. |
| All others | Full warm grade throughout. No formula-specific adjustment. |

**Proof Hold rule (VP09 — auto-applied when a reveal is present):**  
On the frame immediately after revealing the "after" result: music drops to 10–15% volume, no SFX, hold for 1.5 seconds. Let the viewer absorb the result. Then music returns.

---

### SECTION 6 — CAPTION

```
[Full caption — copy-paste ready — no editing needed]

Line 1: [Hook or tension statement that mirrors the reel's opening — under 12 words]
[Body: Value + proof + reusable asset — prompt, list, or tip]
[Formula-mandatory line — Save karo / DM [WORD] / Follow karo]
[Comment-debate question — for F06, F08, F02 formulas]
.
.
.
[Filler dots to push hashtags below fold]
```

**Caption rules auto-applied:**
- Opens with tension (not with "Hey guys" or the creator's name)
- Includes the exact prompt, list, or resource shown in the reel (so the caption has standalone value)
- Mandatory line for formula: F01/F04/F03 → "DM '[WORD]'" · F06/F08/F09 → "Save karo" · F07/F02 → "Follow karo" · F05 → "Save karo + Follow"
- No em-dashes — use " — " (space dash space) to avoid Instagram auto-correct
- Caption is under 300 words

---

### SECTION 7 — CTA

```
ON-CAMERA LINE:
"[Exact words delivered on screen — under 10 words — single action]"

CAPTION CTA:
"[Secondary CTA for caption — one sentence]"

DM AUTOMATION RESPONSE (for DM CTAs — set in Influish/ManyChat):
Trigger: [WORD]
Message:
"[Exact automation message — includes the promised deliverable — under 150 words]"

FIRST COMMENT (post immediately after publishing):
"[Seeding comment to boost early comment count — question or debate prompt]"
```

---

### SECTION 8 — HASHTAGS

```
SET A — BROAD REACH (5):
#[tag] #[tag] #[tag] #[tag] #[tag]

SET B — NICHE AUTHORITY (5):
#[tag] #[tag] #[tag] #[tag] #[tag]

SET C — ENGAGEMENT / COMMUNITY (5):
#[tag] #[tag] #[tag] #[tag] #[tag]

USAGE: Post all 15 in caption below the fold (after the dots).
```

---

## SYSTEMS AUTO-APPLIED — REFERENCE MAP

These systems are applied without being asked. Claude does not announce what it is applying.

| System | Applied In | Source File |
|---|---|---|
| Master Seed Block | Every Flow prompt — ALL clips verbatim, no placeholders (Rule 2) | `03_character/flow_seed_prompts.md` |
| Continuation Block | Every Flow prompt — Clips 2+ (in addition to, not instead of, Master Seed) | `03_character/character_consistency_guide.md` |
| 5-Point Consistency Check | Embedded as generation rules in every prompt | `03_character/character_consistency_guide.md` |
| Scene Blocks B1–B7 | Flow prompt scene type section | `03_character/prompt_blocks.md` |
| Environment Blocks A–D | Flow prompt environment section | `03_character/flow_seed_prompts.md` |
| Formula clip structure | Scene Breakdown table | `02_formulas/formula_index.md` + individual formula files |
| Formula CTA assignment | CTA section | `02_formulas/formula_index.md` (CTA strategy table) |
| Formula color grade rule | Editing Instructions — color grade | production_mode.md formula color table (above) |
| Hook category | Hook section | `01_research/hook_library.md` |
| Viral pattern | Hook section + Editing Instructions | `01_research/viral_pattern_library.md` |
| English delivery spec | Script + acting directions | `03_character/character_sheet.md` (speaking style) |
| Camera angle spec | Scene Breakdown + Flow prompt | `03_character/visual_identity.md` |
| Typography spec | Editing Instructions — text overlays | `03_character/visual_identity.md` |
| Sound design palette | Editing Instructions — SFX | `03_character/visual_identity.md` |
| Proof Hold (VP09) | Editing Instructions — SFX | `01_research/viral_pattern_library.md` |
| Eye Level CTA Reset (VP13) | Flow Prompt Clip [CTA clip] | `01_research/viral_pattern_library.md` |

---

## PRODUCTION MODE QUALITY CHECKLIST

Claude self-applies this before finalizing output. Items that fail are fixed before output is produced — not listed as "to-do."

### Script
- [ ] Hook under 15 words
- [ ] Hook creates genuine tension or curiosity (not a statement of fact)
- [ ] Word count within formula window (target ≤70 words for ≤28s, ≤88 words for ≤35s)
- [ ] "Bete..." or formula-appropriate opener applied
- [ ] Script contains one specific, verifiable claim (not general)
- [ ] Zero hedging language present
- [ ] CTA is a single action with a single trigger
- [ ] FULL SCRIPT beats read as natural spoken sentences — short, complete thoughts on separate lines, no chained em-dash fragment chains (Rule 21)
- [ ] Script Emotion Map completed (Rule 27) — viewer entry state and beat goal identified for beats 2–4
- [ ] Each body beat (beats 2–4) uses minimum 1 interactive language technique from Rule 27 (direct address / micro-reveal / curiosity gap / discovery framing / contrast setup / present-tense immediacy / reaction invitation)
- [ ] Each clip contains minimum 1 enthusiasm marker from Rule 27 (time compression / insider signal / payoff signaling / discovery confirmation / value assertion / specificity anchor)
- [ ] Zero command chains used as primary content delivery in body beats (no "go to X, click Y, copy Z" as the main script body — Rule 27)
- [ ] At least one beat uses discovery narrative framing (not instructional walkthrough)
- [ ] "Quotable line" identified for each body beat — one memorable, specific line per beat

### Flow Prompts
- [ ] Character lock applied to EVERY clip — full format OR simplified format (Rule 2) — no clip left without an identity anchor
- [ ] Full CHARACTER IDENTITY LOCK used for: Clip 1, all split-screen/facecam clips, any clips with environment change (Rule 2)
- [ ] Simplified format used only for: full-screen talking head clips (B1/B6/B7) in Clip 2+ position (Rule 2)
- [ ] No placeholder text ("[PASTE MASTER SEED BLOCK]" or similar) in any clip prompt (Rule 2)
- [ ] Continuation Block present in Clips 2+ (full format) — placed AFTER the identity lock, not replacing it
- [ ] All five locks explicit in every prompt: HAIR / GLASSES / SKIN TONE / BEARD / FACE
- [ ] Script word count EXPLICITLY COUNTED (not estimated) per clip — each word counted against Rule 22 table
- [ ] Word Count Verification table completed and all clips show ✓ before SECTION 4 is written
- [ ] No clip SCRIPT field was written before its word count was confirmed within limits
- [ ] Scene Block assigned (B1–B7) and applied
- [ ] Environment Block assigned (A–D) and applied
- [ ] Exact script in quotes — no placeholders, no ellipsis
- [ ] Specific acting direction (named emotion + specific body language)
- [ ] Duration and format stated: "[X] seconds, vertical 9:16"
- [ ] CTA clip uses Eye Level camera (not below eye level)
- [ ] Proof Hold instruction in editing if reveal is present
- [ ] Visual Action Map present in every prompt — one entry per spoken sentence
- [ ] Every Visual Action Map entry specifies both a Visual action and a Camera movement
- [ ] At least one movement element per clip (character / camera / interface / object) — Rule 14
- [ ] B3 demo clips: actual interface interaction described — no static UI, no blurry panels — Rule 12
- [ ] Proof clips: animated comparison or dynamic motion specified — no static screenshots — Rule 13
- [ ] Camera movement is a named type in every non-CTA prompt — Rule 15
- [ ] Every on-screen text element (prompt, response, settings, comparison panel) is realistic and readable — no placeholder labels or dummy text — Rule 16
- [ ] Visual Action Map entries for text-visible lines include the actual on-screen content written out — not "prompt appears" or "response visible" — Rule 16
- [ ] Pause test applied: any paused frame showing text reveals something useful to the viewer — Rule 16
- [ ] Zero sentence-ending periods in any SCRIPT field — "—" used as sentence separator — Rule 17
- [ ] No ".." anywhere in any SCRIPT field — Rule 17
- [ ] If any number (digit or word) appears in a SCRIPT field: Acting Direction includes "Do not count with fingers / Do not raise [N] fingers / Keep hands relaxed" — Rule 26
- [ ] Final clip (B5/CTA) Visual Action Map last entry includes @ai_snipp branding fade-in in last 2 seconds — Rule 18
- [ ] Every clip is ≤10 seconds — Flow generation limit enforced
- [ ] Assembly Instructions include Flow watermark coverage instruction (Rule 23)
- [ ] Session note included if reel uses split-screen clips alongside full-frame clips (Rule 25)

### Caption
- [ ] Opens with hook or tension (not greeting)
- [ ] Contains reusable asset (prompt, list, or tip — not just description)
- [ ] Formula-mandatory line present (Save karo / DM [WORD] / Follow karo)
- [ ] Comment-debate question present (F06, F08, F02 only)
- [ ] No em-dash characters — uses " — " instead
- [ ] Under 300 words

### Hashtags
- [ ] Exactly 15 total across 3 sets of 5
- [ ] Mix of broad (100K+ posts), niche (10K–100K), and community-specific

### CTA
- [ ] On-camera line under 10 words
- [ ] DM trigger word is single capitalized word (DM CTAs only)
- [ ] DM automation response text ready (DM CTAs only)
- [ ] First comment seeding text ready

---

## PRODUCTION MODE FAILURE MODES

### FAILURE MODE 1 — Format Gate (Topic Too Long)

**When:** Script exceeds 88 words after all cuts, or the topic genuinely requires more than 35 seconds to be honest.

**Output:**
```
FORMAT REDIRECT — [topic]
This topic cannot be delivered honestly in ≤35 seconds.
Options:
  → Carousel (3–7 slides): [topic rephrased as carousel concept]
  → Narrow the angle: "[suggested narrowed hook that fits Reel format]"
No reel produced.
```

---

### FAILURE MODE 2 — Personal Proof Gate

**When:** The reel would require claiming something that hasn't been personally tested or verified.

**Output:**
```
PROOF GATE FAIL — [topic]
Cannot produce: reel would claim [specific untested assertion].
Required before production: Test [specific action] and confirm the result.
No reel produced.
```

---

### FAILURE MODE 3 — F07 News Is Stale

**When:** Topic is news-dependent (F07) and the event is over 48 hours old.

**Output:**
```
NEWS GATE FAIL — [topic] — Age: [X] hours old
Options:
  → Reframe evergreen: "Agar miss kiya — [topic] — yeh matter karta hai kyunki [Indian angle]"
  → Switch to F02 (Future Shock) with the trend angle
  → Archive — news value expired
```

---

### FAILURE MODE 4 — DM Deliverable Undefined

**When:** Selected formula requires a DM CTA but no deliverable exists or has been specified.

**Output:**
```
CTA INCOMPLETE — F[NN] requires a DM deliverable.
Specify one:
  → Prompt (Claude/ChatGPT prompt)   → trigger word: PROMPT
  → Tool list (3–5 tools)            → trigger word: TOOLS
  → Template (document template)     → trigger word: TEMPLATE
  → Resource list                    → trigger word: LIST
  → Free resource / link             → trigger word: FREE
Then re-run: PRODUCTION MODE F[NN] CTA=[WORD]: [topic]
```

---

### FAILURE MODE 5 — Formula Ambiguity (Only Permitted Question)

**When:** Topic maps to two formulas with equal fit and the distinction matters for production.

**Output:**
```
FORMULA AMBIGUITY — [topic]
Two formulas fit equally:

  F[NN] — [Name]: [one-sentence reason it fits] — Primary metric: [metric]
  F[NN] — [Name]: [one-sentence reason it fits] — Primary metric: [metric]

Which metric matters most for this reel?
```

This is the only question Production Mode is permitted to ask. All other decisions are made without asking.

---

### FAILURE MODE 6 — F02 Frequency Gate

**When:** Topic maps to F02 (Future Shock) but F02 has already been used this week.

**Output:**
```
F02 GATE — F02 already used this week (max 1×/week — fear fatigue rule).
Options:
  → F07 (News Flash) if topic is under 48 hours old
  → Hold F02 for next week
  → Reframe as F09 (Three Step System) with an action path
```

---

### FAILURE MODE 7 — Quality Gate Below Threshold

**When:** After self-applying the quality checklist, a critical item fails and cannot be fixed by Claude alone (e.g., F06 requires real timing numbers that don't exist, or F03 output hasn't been generated yet).

**Output:**
```
QUALITY GATE DEFERRED — [topic]
Blocking issue: [specific unfixable issue]
Required before production: [specific action the creator must take]
Status: DEFERRED — re-run Production Mode after completing the above.
```

---

## FORMULA CLIP STRUCTURE — QUICK REFERENCE

| Formula | Clip 1 | Clip 2 | Clip 3 | Clip 4 | Clip 5 | Total |
|---|---|---|---|---|---|---|
| **F01** AI Cheat Code | Hook 8s | Trick Setup 8s | Tool Demo 8s | CTA 6s | — | 30s |
| **F02** Future Shock | Hook 8s | Trend Data 8s | Action Path 8s | CTA 6s | — | 30s |
| **F03** Hollywood VFX | Hook 6s | AI Output Reveal 10s | Prompt Share 8s | CTA 6s | — | 30s |
| **F04** Hidden Tool | Hook 8s | Tool Intro 8s | 3 Features 8s | CTA 6s | — | 30s |
| **F05** Career List | Hook 8s | Items 1–2 (9s) | Items 3–5 (9s) | CTA 5s | — | 31s |
| **F06** AI vs Human | Hook 5s | Human Way 7s | AI Way 8s | Proof 7s | CTA 5s | 32s |
| **F07** News Flash | Hook 6s | What Happened 8s | Indian Angle 7s | CTA 5s | — | 26s |
| **F08** Transformation | Hook 6s | Before State 6s | Transformation 8s | After Reveal 6s | CTA 5s | 31s |
| **F09** Three Step System | Hook 5s | Step 1 (8s) | Steps 2+3 (9s) | CTA 5s | — | 27s |
| **F10** Comment React | Comment Card 4s | Hook Response 6s | Answer 10s | CTA 5s | — | 25s |
| **F11** Ego Output | Visual Problem 4s | Hook 7s | Demo 10s | Output Reveal 15s | Ctx Frame 4s / CTA 5s | 45s |

Block assignment per formula:
- **F01:** Clip 1 = B1, Clip 2 = B3, Clip 3 = B3, Clip 4 = B5
- **F02:** Clip 1 = B4, Clip 2 = B6, Clip 3 = B6, Clip 4 = B5
- **F03:** Clip 1 = B7, Clip 2 = B3, Clip 3 = B2, Clip 4 = B5
- **F04:** Clip 1 = B1, Clip 2 = B4, Clip 3 = B2, Clip 4 = B5
- **F05:** Clip 1 = B1, Clip 2 = B2, Clip 3 = B2, Clip 4 = B5
- **F06:** Clip 1 = B1, Clip 2 = B6, Clip 3 = B3, Clip 4 = B7, Clip 5 = B5
- **F07:** Clip 1 = B4, Clip 2 = B4, Clip 3 = B1, Clip 4 = B5
- **F08:** Clip 1 = B1, Clip 2 = B6, Clip 3 = B3, Clip 4 = B7, Clip 5 = B5
- **F09:** Clip 1 = B1, Clip 2 = B2, Clip 3 = B2, Clip 4 = B5
- **F10:** Clip 1 = B4 (comment card cold open), Clip 2 = B1, Clip 3 = B6, Clip 4 = B5
- **F11:** Clip 1 = B8 (visual problem open — no creator), Clip 2 = B1, Clip 3 = B3, Clip 4 = B-PROOF (extended), Clip 5 = B-SOCIAL, Clip 6 = B5

---

## CTA QUICK REFERENCE — BY FORMULA

| Formula | On-Camera Line | Trigger Word | Caption Secondary |
|---|---|---|---|
| F01 | "DM karo '[WORD]' — list bhej dunga." | TOOLS / PROMPT / TEMPLATE | "💬 DM '[WORD]' for the full list" |
| F02 | "AI Snipp follow karo — ye miss mat karna." | N/A | "🔔 Follow for AI career updates" |
| F03 | "DM karo '[WORD]' — exact prompt bhej dunga." | PROMPT | "💬 DM '[WORD]' for the exact prompt" |
| F04 | "DM karo '[WORD]' — tool list bhej dunga." | TOOLS / FREE | "💬 DM '[WORD]' for the tool list" |
| F05 | "Follow karo, aur DM karo '[WORD]' — full list deta hun." | LIST / CERTIFICATIONS | "💾 Save karo + 🔔 Follow" |
| F06 | "Save karo — kal kaam aayega." | POST / PROMPT | "💾 Save this. 💬 DM '[WORD]' for prompt" |
| F07 | "AI Snipp follow karo — har update pe pehle yahan aata hun." | N/A | "🔔 Follow for AI news first" |
| F08 | "Save karo — yeh prompt screen pe hai." | PROMPT | "💾 Save + 💬 DM '[WORD]' for full prompt" |
| F09 | "Save karo — teen steps wala system abhi screen pe hai." | SYSTEM / TEMPLATE | "💾 Save this system." |
| F10 | "Comment mein batao — [specific question]?" | N/A | "💬 Drop your answer below" |
| F11 | "Comment karo '[TRIGGER]' — tumhara poster bhejta hun." | [Personal identifier — city/name/profession] | "💬 Comment [word] for your personalized poster prompt" |

---

## ACTING DIRECTION QUICK REFERENCE

Select the acting direction that matches the formula's emotional goal. Insert verbatim into Flow prompt acting direction field.

| Emotional Goal | Acting Direction Text |
|---|---|
| Sarcastic roast (F01, F04) | "Playful exasperation, light roasting. Smart friend who's slightly disappointed in you but in a good way. Speaks fast. Eyes slightly narrowed, one corner of mouth slightly raised. Natural hand gestures — open palm for emphasis, no finger counting." |
| Urgency without panic (F02, F07) | "Higher energy than standard. Slightly wider eyes. Faster speech. Leaning slightly more forward. 'You need to know this right now' body language. Controlled — not panicking. Confident urgency, not breathless." |
| Insider secret reveal (F01, F04) | "Slight conspiratorial head tilt. Lowered voice. Like sharing something exclusive with someone who deserves to know. Subtle — not theatrical. Holds a brief pause before the key reveal." |
| Proof presentation (F06, F08) | "Calm confidence. Not boasting. The result is speaking — creator presents it as self-evident. Subtle nod. 'I told you' energy without saying it. Slight knowing smirk at the key number." |
| Warm and direct CTA | "Warm, direct, genuine. The sarcasm is gone. Speaks like talking to one specific person. Slight nod at the start. Shoulders relaxed. This is the 'end of a good conversation' feeling. Eye level camera. No performance." |
| Tutorial (F09) | "Informed, enthusiastic but controlled. 'I'm showing you something useful' tone. Not shouting, not flat. Engaged professional. Looks occasionally toward main content, returns to camera for emphasis beats." |
| Community response (F10) | "Conversational. Like explaining something to a friend over chai. Energy builds through the answer. End on confidence — 'this is what I think and I'm clear about it.' Pacing can breathe — short pauses are authenticity signals here." |

---

## WHAT PRODUCTION MODE DOES NOT DO

- Does not produce partial packages. All 8 sections or a rejection notice. Nothing in between.
- Does not write analysis paragraphs, research summaries, or research reports before or after sections.
- Does not skip the Research Phase — research executes before production begins, for every topic without exception.
- Does not generate a reel from a topic that has not been researched and angle-validated.
- Does not start research by listing features — Outcome-First Principle applies: "What result would make a viewer immediately try this?" is always the first question.
- Does not skip Intent Classification — topic intent is classified before information is gathered and determines research focus.
- Does not generate fewer than 10 angle candidates before selecting one — 10 is the floor.
- Does not default to tutorial-style or feature-explanation angles when a shortcut, transformation, or outcome angle is available from research.
- Does not default to generic angles ("Top N features," "Best AI tool," "New update") when a stronger angle is available from research.
- Does not write chained em-dash fragment chains in FULL SCRIPT beats ("Step — action — detail — copy karo") — script beats must read as natural spoken sentences (Rule 21).
- Does not ask questions except for Formula Ambiguity (Failure Mode 5).
- Does not produce a reel for a topic that fails any of the six hard gates.
- Does not leave placeholder text in Flow prompts — never writes "[PASTE MASTER SEED BLOCK]", "[SAME AS CLIP 1]", or any shorthand requiring the user to manually insert the character description (Rule 2).
- Does not check only total word count — per-clip word count is explicitly counted (not estimated) against the Rule 22 table for every clip individually, before any SCRIPT field is written.
- Does not estimate word counts — every word in every SCRIPT field is counted before the SCRIPT is written into the prompt. If a count fails, the script is trimmed before proceeding.
- Does not produce a reel without a specific, named viral pattern applied.
- Does not default to Hinglish scripts. English is the default for all spoken script fields — see Rule 8. Captions may use Hinglish for audience resonance.
- Does not write body beats as instructional walkthroughs ("go to X, click Y, copy Z") — all body beats must be discovery narrative format (Rule 27).
- Does not skip the Script Emotion Map — viewer entry state and beat goal are identified for beats 2–4 before writing.
- Does not write body beats without a "quotable line" — each beat has one specific, memorable sentence identifiable as the keystone.
- Does not use hedged enthusiasm ("I think you might like this", "you might want to") — claims are stated with confidence and backed by specific detail (Rule 27).
- Does not include three or more CTAs in one reel.
- Does not produce F02 if F02 was used this week.
- Does not produce F07 content for news older than 48 hours without reframing.

---

*This document is the execution layer. All system intelligence lives in the referenced files. Production Mode's job is to apply that intelligence at speed — without analysis, without hesitation, without asking for permission.*
