# Viral Pattern Library
## AI_SNIPP Research & Intelligence System

*A viral pattern is a repeatable structural element that reliably increases retention, engagement, or sharing behavior. This library extracts patterns from the canonical @ai_snipp reference reel (AI_SNIPP_REEL_011), the formula library, and the character system — converting observed behavior into reusable production assets.*

*Every pattern here has a documented source. No speculation. If a pattern can't be traced to a real reel or validated research data, it doesn't belong in this library.*

---

## PATTERN INDEX

| ID | Pattern Name | Source | Primary Formulas | Primary Metric |
|---|---|---|---|---|
| VP01 | The "Bete..." Roast Opener | AI_SNIPP_REEL_011 | F01, F04, F05 | Hook retention |
| VP02 | 8-Second Clip Rhythm | AI_SNIPP_REEL_011 | All | Watch completion |
| VP03 | Premium UI > Generic Animation | AI_SNIPP_REEL_011 (lessons) | F04, F05, F06 | Trust + credibility |
| VP04 | Facecam 25-28% + Content 70-75% | AI_SNIPP_REEL_011 (layout) | F01, F04, F05 | Info density + face |
| VP05 | Single Trigger Word DM Lead Magnet | APIFY doc, formula library | F01, F04, F03 | DM conversion |
| VP06 | Hinglish Delivery Formula | AI_SNIPP_REEL_011 (all parts) | All | Retention + trust |
| VP07 | Hard Cut Rhythm (no dissolves) | AI_SNIPP_REEL_011, prompt_blocks | All | Pace + attention |
| VP08 | Pre-Save Hook ("Save karo pehle") | formula library (F09) | F09, F06, F08 | Save rate |
| VP09 | Proof Hold — Silent 2 Seconds | formula library (F08) | F08, F03 | Absorption + saves |
| VP10 | Continuation Prompt Language | flow_seed_prompts.md | All (multi-clip) | Character consistency |
| VP11 | "Build. Solve. Scale. Repeat." Background | visual_identity.md | All | Brand recall |
| VP12 | Career List 3-Item Format | AI_SNIPP_REEL_011 | F05 | Completion + saves |
| VP13 | Eye Level CTA Reset | prompt_blocks.md (Block 5) | All (CTA clip) | CTA warmth conversion |
| VP14 | Hook Silence (No Music First 3s) | formula library (F01, F02) | F01, F02, F08 | Hook gravity |
| VP15 | The "Kya Matlab Hai Tumhare Liye" Pivot | AI_SNIPP_REEL_011, F07 | F07, F02 | Indian relevance lock-in |

---

## PATTERN CARDS

---

### VP01 — The "Bete..." Roast Opener

**Source:** AI_SNIPP_REEL_011, Part 1 — "बेटे... अगर सही से पढ़ा होता ना, तो आज ये हाल नहीं होता।"

**What it is:**
The creator opens with "Bete..." — a mock-parental sarcasm roast in Hinglish. The tone is warm exasperation: "I can't believe you don't know this" combined with genuine affection. It's the feeling of a sharp, slightly older friend gently ribbing you while simultaneously caring about your success.

**Why it works:**
1. "Bete" is a pattern interrupt — it's not a typical opening word, so it stops the scroll reflex
2. It creates identification — the viewer has had this experience (being lightly scolded by someone wiser)
3. The roast creates a mild shame-curiosity loop — "wait, what am I missing?" — that drives retention past the 3-second mark
4. It's warm enough to not alienate: the viewer knows they're being teased, not attacked
5. It signals the creator has insider knowledge — why else would they say "you should already know this"?

**Implementation:**
```
STRUCTURE:
"Bete... [observation of what viewer is missing or doing wrong, in one sentence]. 
[Optional: natural consequence of ignorance]. 
[Implicit setup: I'm about to fix this for you.]"

ACTING DIRECTION: SARCASTIC ROAST
- Hands steepled or interlocked (NOT finger-counting)
- Slight head shake on "Bete..."
- Direct camera gaze throughout
- Half-smile that says: I'm roasting you but I want you to win
- Slight forward lean on the pain word (e.g., "80% power waste")
- Camera: slightly below eye level (authority angle — this is the correction angle)
```

**When to use:**
- Topic where the audience should already know this but most don't (F01, F04, F05)
- Career/education content where the ignorance has a real cost (F05, F02)
- Avoid for: F07 (news needs straight urgency, not roast), F03 (output-first, no creator in opener)

**Performance signal:** If comments contain "hahaha" + "sharing with my friend who..." → pattern is landing correctly. If comments are defensive → delivery was too harsh, reduce exasperation, increase warmth.

**AI_SNIPP Example:** REEL_011, REEL_001 (EX01 — "Bete... Claude use karte ho roz, aur system prompt nahi jaante?")

---

### VP02 — 8-Second Clip Rhythm

**Source:** AI_SNIPP_REEL_011 — all 4 parts are exactly 8 seconds. LESSONS_LEARNED: "Use 8-second Flow clips."

**What it is:**
Each clip in a multi-clip reel is exactly 8 seconds. This is not aesthetic preference — it is a calibrated attention-management decision. 8 seconds is long enough to deliver one complete thought, short enough to prevent mid-thought dropout.

**Why it works:**
1. Instagram's attention cycle peaks and troughs approximately every 6–10 seconds for short-form video
2. 8 seconds forces the writer to distill one idea per clip — no padding
3. The cut at 8 seconds acts as a pattern interrupt that re-hooks attention for the next clip
4. A 4-clip reel of 8-second clips (32s total) hits the sweet spot for Instagram Reels algorithm completion rate
5. Forces the script to be tight: 8 seconds × 2.5 words/second = ~20 words max per clip

**Implementation:**
```
CLIP BUDGET:
Standard reel: 4 clips × 8s = 32s total
Extended reel: 5 clips × 7s = 35s (use for F09, F05 where more steps needed)
Short reel: 3 clips + CTA (5-6s) = 29-30s (use for F07, F10)

PER-CLIP WORD COUNT:
8s × 2.5 words/s = 20 words (minimum)
8s × 3.0 words/s = 24 words (maximum for fast delivery)

CLIP STRUCTURE:
Each clip delivers one complete thought:
- Clip 1: Hook (the problem/curiosity)
- Clip 2: Agitate/Insight Part 1 (the why/the context)
- Clip 3: Proof/Insight Part 2 (the demonstration)
- Clip 4: CTA (the next action)
```

**When to use:** All formulas, all reels. Non-negotiable rhythm for multi-clip Reels.

**Violation signal:** If any clip feels like it needs "just a few more seconds" — the script is too dense for that clip. Split into two clips or cut the content.

---

### VP03 — Premium UI > Generic Animation

**Source:** AI_SNIPP_REEL_011, LESSONS_LEARNED: "Premium UI visuals outperform generic AI animations."

**What it is:**
When showing tool interfaces, course platforms, dashboards, or AI output — always use real, high-fidelity UI screenshots (IBM learning dashboard, Google AI Essentials interface, DeepLearning.AI certificate visuals) rather than generic AI animations, stock footage, or animated illustrations.

**Why it works:**
1. Real UI screenshots signal: "Creator actually used this." Generic animations signal: "Creator is talking about something they haven't done."
2. High-fidelity interfaces activate the viewer's pattern recognition — they immediately understand "that's a real product"
3. Premium-looking interfaces make the content feel valuable — "this creator covers serious tools"
4. Specific platform visuals (IBM, Google, DeepLearning.AI) are credibility anchors — these are recognizable brands that transfer trust to the creator
5. Generic animations look the same as every other AI content creator — premium UIs differentiate

**Implementation:**
```
PRIORITY ORDER for visual assets:
1. Real screenshot of actual interface (dark mode preferred)
2. Creator-filmed screen recording
3. Platform's own marketing screenshot (official)
4. Clean recreation of interface layout (only if real screenshot unavailable)
5. Generic animation (last resort — avoid)

QUALITY STANDARDS for screenshots:
- Dark mode: Always preferred — matches @ai_snipp's dark studio aesthetic
- Resolution: Full 1080p or higher — no blurry captures
- Content: Show a realistic use case (pre-fill example content, not empty fields)
- Size in frame: 70-75% of frame when using facecam layout
- Legibility: Text must be readable at mobile viewing size
```

**When to use:** F04 (tool demos), F05 (certification platform visuals), F06 (comparison screens), F08 (before/after interfaces), F09 (workflow tool screens). Any clip where the tool interface is the main visual.

**Performance signal:** Comments mentioning the specific tool by name ("I didn't know IBM had this course") → pattern is working. Generic positive comments → pattern may not be driving specific recognition.

---

### VP04 — Facecam 25-28% + Content 70-75%

**Source:** AI_SNIPP_REEL_011, Parts 2, 3, 4 layout. prompt_blocks.md, Block 2 (FACECAM SCENE).

**What it is:**
A specific frame composition where the creator's face occupies the bottom-right 25-28% of the 9:16 frame in a clean rounded rectangle with warm amber border glow, while the main content (tool interface, certificate, workflow) occupies the remaining 70-75% of the frame.

**Why it works:**
1. Face in frame maintains emotional connection — viewers tune out faceless screen recordings
2. The 25-28% rule keeps the creator present without obscuring the content being shown
3. Bottom-right positioning follows natural reading pattern — content first, then check the face reaction
4. Warm amber border on the facecam oval creates visual hierarchy that distinguishes creator from background
5. Creator glancing at the content + returning to camera mimics "guided tour" energy — feels like the creator is teaching, not just showing

**Implementation:**
```
FACECAM SPECIFICATIONS:
Position: Bottom-right corner
Size: 25-28% of total frame width
Shape: Clean rounded rectangle
Border: Warm amber glow (#D4894A), 2-3px, subtle outer glow
Creator behavior in facecam:
  - Occasionally glances toward main content area (natural, not forced)
  - Returns to direct camera at key emphasis moments
  - Slight nod when confirming what's shown
  - Active listening energy (engaged, not static)

MAIN CONTENT AREA (70-75%):
Fill: Real UI screenshot or screen recording
Position: Center to upper portion of frame
Text legibility: Must be readable at mobile viewing size
Overlay text: Tool name or step number added in editing (not blocking content)
```

**Interaction rhythm within clip:**
```
0-2s: Creator looks at camera (establishing connection)
2-4s: Creator glances toward content (directing viewer attention)
4-6s: Creator nods at the content being shown
6-8s: Creator returns to camera for emphasis line
```

**When to use:** F01 (Clip 2 — settings reveal), F04 (tool demo), F05 (certification platform reveal), F06 (AI side of comparison). Any clip where content is the hero but creator presence is needed for trust.

**Do NOT use for:** F03 and F08 opening clips (creator absent is intentional — output is the hero). CTA clip (creator returns full screen).

---

### VP05 — Single Trigger Word DM Lead Magnet

**Source:** APIFY doc: "Signature CTA: 'DM me the word TOOLS and I'll send you the full list.'" Formula library, CTA Strategy table.

**What it is:**
A single, capitalized, memorable keyword that viewers DM to the creator to receive a promised deliverable. The keyword is: always exactly one word, always capitalized in text, always quoted when spoken or written.

**Why it works:**
1. Reduces friction to zero — "DM me" is too vague, "DM the word TOOLS" is a specific, executable instruction
2. The deliverable promise converts casual viewers into active leads — they've taken an action
3. Single-word keywords are compatible with automation (Influish, ManyChat) — scales without creator time
4. The specificity signals the creator is organized and prepared — "this person has a system"
5. Creates a flywheel: DM → reply with value → viewer becomes follower → viewer re-engages

**Implementation:**
```
TRIGGER WORD SYSTEM:

"TOOLS" — generic tool list (highest volume CTA)
"SYSTEM" — workflow template or system document
"PROMPT" — specific prompt template
"LIST" — resource or certification list
"FREE" — free resources specifically
"CERTIFICATIONS" — certification links
"TEMPLATE" — document template

ON-CAMERA DELIVERY (CTA clip):
Voice: conversational, not pushy
"DM karo '[TRIGGER]' — main bhejtaa hun [deliverable]. Free hai."

IN CAPTION (written):
'DM me "[TRIGGER]" and I'll send you [deliverable] 👇'
OR
'DM karo "[TRIGGER]" — [deliverable] bhejtaa hun'

AUTOMATION REQUIREMENT:
Every trigger word that appears in a reel must have:
1. An active automation response pre-configured (Influish or ManyChat)
2. The deliverable ready (Google Doc, Notion page, or text response)
3. A follow-up message in the automation that encourages @ai_snipp follow
4. The automation must be tested before the reel posts
```

**Performance tracking:** Track DM volume by trigger word weekly. If "TOOLS" consistently outperforms "SYSTEM" → use TOOLS as the default trigger for ambiguous topics.

---

### VP06 — Hinglish Delivery Formula

**Source:** AI_SNIPP_REEL_011 — all 4 parts. Character_sheet.md voice profile. APIFY doc: "Language: Hinglish (Hindi + English)."

**What it is:**
A specific language mixing pattern where Hindi serves as the emotional and connective tissue, while English serves as the technical vocabulary. The ratio shifts based on content type — more Hindi for emotion-heavy moments, more English for technical specifics.

**Why it works:**
1. English technical terms are already the vocabulary of the Indian AI/tech audience — translating them into Hindi creates friction
2. Hindi connective words, jokes, CTAs, and emotional moments feel authentic — the audience uses these words in real conversation
3. The mix signals: "this creator is one of us" — not trying to be Western, not condescending with overly formal Hindi
4. "Bete...", "main bhejtaa hun", "kal kaam aayega" feel warm in Hindi in a way "I'll send you", "useful tomorrow" don't
5. It's more memorable — code-switching creates slight cognitive novelty that aids retention

**Implementation:**
```
HINDI: Use for
- Emotional moments: "Bete...", "yaar", "suno", "dekho"
- CTAs: "Save karo", "follow karo", "DM karo", "comment mein batao"
- Connectors: "kyunki", "isliye", "lekin", "aur", "matlab"
- Time references: "kal", "aaj", "abhi", "2 mahine mein"
- Pain descriptions: "mushkil", "waste", "pata nahi tha", "koi nahi batata"
- Personal voice: "main ne test kiya", "mera suggestion hai"

ENGLISH: Use for
- Tool names: Claude, ChatGPT, Gemini, Perplexity, NotebookLM
- Technical terms: API, prompt, certification, system prompt, custom instructions
- Numbers + metrics: "80%", "3 minutes", "8-second clips"
- Platform names: LinkedIn, Instagram, ProductHunt
- Action verbs in tech context: demo, test, integrate, deploy

NEVER translate: Tool names, platform names, technical acronyms (API, UI, LLM)
ALWAYS in Hindi: Opening hook emotion word, CTAs, "Bete...", "yaar"
VARIABLE: Body of explanation — lean Hindi for emotional/career content, lean English for technical demos

PACE: Fast. 2.5-3 words/second. Hinglish at fast pace feels energetic. 
Slow Hinglish feels like a news broadcast.
```

**Voice profile (from character_sheet.md):**
- Warm baritone, high energy but controlled
- Natural Indian accent — NOT westernized
- Emotional arc: sarcasm → excitement → emphasis → warmth
- Signature: "Bete..." opener

---

### VP07 — Hard Cut Rhythm (No Dissolves)

**Source:** AI_SNIPP_REEL_011 — "Merge clips into one reel." prompt_blocks.md transition specifications.

**What it is:**
All cuts between clips are hard cuts (instantaneous, no visual transition effect) except for the final clip which fades to black. Whoosh SFX is added to hard cuts on high-energy transitions — the visual cut is hard, but an audio transition bridges the clips.

**Why it works:**
1. Hard cuts are faster — dissolves add 0.3–0.5s of dead air that compounds across a 4-clip reel into 1.5–2s of wasted attention
2. Hard cuts signal confidence and pace — "we're not lingering, we have more to show you"
3. Consistent hard cuts create a rhythmic cadence — the viewer learns the rhythm and stays with it
4. Whoosh SFX on hard cuts signals the cut before it happens (sub-0.2s audio cue) — brain processes it as intentional, not jarring

**Implementation:**
```
TRANSITION RULES:
Clip 1 → Clip 2: Whoosh SFX (0.2s) + hard cut
Clip 2 → Clip 3: Hard cut (or Whoosh + hard cut for high-energy transition)
Clip 3 → Clip 4 (CTA): Hard cut
Clip 4 end: Fade to black (0.5s)

FACECAM TRANSITIONS (within a clip that has two phases):
Phase 1 → Phase 2: Hard cut (no SFX needed within a clip)

NEVER USE:
- Dissolve transitions (too slow, too soft for this creator's energy)
- Swipe transitions (too casual/amateur aesthetic)
- Zoom transitions (inconsistent with camera movement strategy)
- Glitch transitions (wrong brand aesthetic for premium AI creator)

EXCEPTION: The CTA clip always ends with a 0.5s fade to black.
This signals closure — "the reel is over, take action now."
```

---

### VP08 — Pre-Save Hook ("Save karo pehle, phir dekho")

**Source:** Formula library (F09 hook type E: "Save before watch"). EX03, Clip 1 hook.

**What it is:**
A hook variant where the creator explicitly asks the viewer to save the reel before they've seen the value. "Save karo pehle, phir dekho" — save it first, then watch.

**Why it works:**
1. Pre-save hooks prime the save behavior before the viewer has assessed the content — by the time they assess, the save habit is already primed
2. It signals: "this is reference content" — the creator is implicitly saying "you'll want to come back to this"
3. It separates this reel from entertainment reels (which are watched once) — positions content as a tool
4. It challenges the viewer: "if I'm confident enough to ask you to save before watching, this must be worth it"
5. Instagram's algorithm notices saves that happen early in the watch session (within first 3 seconds) — pre-save hooks are algorithm-friendly

**Implementation:**
```
WHEN TO USE:
Only on F09 (Three Step System), F06 (AI vs Human — when prompt is complex), F08 (Transformation — when prompt is the asset)
DO NOT use on F07 (news), F10 (community), F05 (list — "save karo" in body is sufficient)

HOOK STRUCTURE:
"[System/value name in one line]. Save karo pehle, phir dekho."

EXAMPLES:
"Yeh 3-step AI system hai jo tumhara reply rate teen guna karega. Save karo pehle, phir dekho."
"Is prompt se resume 45 minute se 8 minute ho jaata hai. Save karo pehle, phir dekho."
"Claude ka yeh workflow mera 4-hour task 25 minute mein karta hai. Save karo pehle, phir dekho."

DELIVERY:
On "Save karo pehle" — creator nods once (subtle instruction, not command)
On "phir dekho" — slight lean back (I'm waiting for you to save)
```

---

### VP09 — Proof Hold — Silent 2 Seconds

**Source:** Formula library (F08): "Proof hold is 2-3s SILENT (viewer absorbs quality)." visual_identity.md: "audio retreat prompts eye."

**What it is:**
After revealing the "after" state (F08/F03), the creator goes silent for 2–3 seconds while the output remains on screen. Music drops to 10-15% volume (or cuts entirely). No narration, no gesture — just the output.

**Why it works:**
1. Silence forces the viewer to actually look at the output — with narration present, the brain splits between listening and looking
2. 2 seconds is enough time for the visual quality to register — the viewer forms their own judgment
3. The silence creates a "proof" feeling — no selling, just showing. It signals: "I'm confident enough to let this speak for itself"
4. After the silence, when the creator speaks again, the emphasis carries more weight
5. Audio retreat (music volume drop) triggers the eye to look harder at the visual — a known attention mechanism

**Implementation:**
```
TIMING:
"After" reveal → music drops to 10-15% → 2-3 seconds silence → creator reacts

CREATOR BEHAVIOR DURING PROOF HOLD:
- No dialogue
- No exaggerated reaction (no "look at THAT!" — let the output speak)
- Subtle facial expression: controlled impressed or satisfied
- Eyes may briefly glance at output (not dramatically)
- Facecam stays active — creator is present, just quiet

CAMERA: Static during proof hold (no movement — let the output be still)
OVERLAY: No new overlays during proof hold

AFTER THE PROOF HOLD:
Creator resumes narration: "[What changed] — [the prompt/tool that created this]"
Music rises back to 30-40%

WHERE IT APPEARS:
F08: Between "after" clip and CTA
F03: After cold open (output-only) before transition to creator reaction
```

---

### VP10 — Continuation Prompt Language

**Source:** flow_seed_prompts.md, Assembly Guide: "CONTINUATION: This is Clip [N] of [TOTAL]..."

**What it is:**
A specific natural-language instruction prepended to every Flow prompt after Clip 1, explicitly telling the AI video generator that this is part of a series with the same character. The continuation block preserves character identity across sessions.

**Why it works:**
1. AI video generators lose character consistency between separate generation sessions — the continuation block re-anchors the identity
2. Naming specific locked elements (coil curls, rectangular glasses, beard) prevents the generator from "averaging" toward a different character
3. Stating "same studio" + "only action changes" helps the generator understand what to vary vs what to keep
4. The language is designed to signal CONTINUATION, not REPLACEMENT — "same character" triggers identity preservation mode

**Implementation:**
```
STANDARD CONTINUATION BLOCK:
"CONTINUATION: This is Clip [N] of [TOTAL]. Same character — same face, same tight coil curls, 
same matte black rectangular glasses, same beard, same dark studio. Only action, script, and 
specified variations change."

CROSS-SESSION CONTINUATION:
For clips generated in different sessions, add:
"STRICT MATCH to Character.png reference — same person across all clips. 
Session seed: [seed from original session]."

WHERE TO INSERT:
After Master Seed Block, before scene-specific prompt.
Add to Clips 2, 3, 4, 5 — never to Clip 1.
```

**Performance signal:** If clips 2+ have character drift despite continuation block → increase specificity of locked elements, reduce total prompt length (shorter prompts improve character focus), attach Character.png to every clip.

---

### VP11 — "Build. Solve. Scale. Repeat." Background

**Source:** visual_identity.md: "'Build. Solve. Scale. Repeat.' brand element in background." prompt_blocks.md: "Build. Solve. Scale. Repeat." visible in background."

**What it is:**
A persistent text element visible in the creator's dark studio background. It appears on a shelf or wall behind the creator — readable but not dominant. It is the brand's philosophical statement, not a logo.

**Why it works:**
1. Repeated visual exposure across every reel builds unconscious brand recall — viewers recognize the studio before they consciously identify it
2. The phrase communicates the creator's philosophy without needing to say it — ambitious, action-oriented, iterative
3. It differentiates the studio from generic "dark room" setups — it's a specific, intentional studio
4. It targets the right audience segment: the phrase appeals to builders and problem-solvers (the core AI audience)
5. The background text appears in compressed/shared screenshots — passive brand exposure outside the platform

**Implementation:**
```
VISIBILITY: Background element — visible but not dominant. 
Creator and content always take visual priority.
Opacity guidance: Readable at 70-80% opacity — do NOT make it the focal point.

PLACEMENT: Bookshelf or wall behind creator
NOT: As a lower-third, NOT as an overlay on creator, NOT as a title card

INCLUDED IN: All prompts using Environment A (Dark Premium Studio)
EXCLUDED FROM: Environment B (Minimal), Environment C (News Room — different feel needed)

PROMPT LANGUAGE: "Build. Solve. Scale. Repeat.' text visible on shelf in background"
```

---

### VP12 — Career List 3-Item Format

**Source:** AI_SNIPP_REEL_011 — 3 certifications in 3 clips. Formula F05 scene structure: "5 clips (Hook ROAST → Facecam Resource 1 → Facecam Resource 2 → Facecam Resource 3 + CTA)."

**What it is:**
When delivering a resource or certification list (F05), each resource gets exactly one dedicated clip with facecam + platform visual. Resources are numbered with the same visual overlay system (01, 02, 03). The reel ends at the third resource + CTA in a combined clip.

**Why it works:**
1. One resource per clip gives each resource enough screen time to register (8 seconds)
2. Numbering creates a completeness expectation — viewer waits for all three
3. The combined "resource 3 + CTA" at the end is efficient — the creator transitions naturally from value delivery to action
4. Three is the cognitive magic number — more than 3 items loses memorability, fewer than 3 feels thin for a "list" format

**Implementation:**
```
F05 CLIP STRUCTURE:
Clip 1: Hook — ROAST (8s) — "Bete... X log AI career mein peeche hain kyunki..."
Clip 2: Resource 1 (8s) — Facecam + Platform UI — "Pehli hai [Resource Name]..."
Clip 3: Resource 2 (8s) — Facecam + Platform UI — "Doosri hai [Resource Name]..."
Clip 4: Resource 3 + CTA (8s) — "Teesri — aur meri personal recommendation — [Resource]. Follow karo."

VISUAL OVERLAY for each resource clip:
Large resource name: Center-top frame, white, Inter ExtraBold, pop-in at 0.5s, hold 2s
Platform UI: 70-75% of frame, dark mode, showing actual dashboard/certificate

CAPTION FORMAT:
1️⃣ [Resource 1] — [one-line benefit]
2️⃣ [Resource 2] — [one-line benefit]
3️⃣ [Resource 3] — [one-line benefit]
```

**Reference reel:** AI_SNIPP_REEL_011: IBM AI Fundamentals → Google AI Essentials → DeepLearning.AI

---

### VP13 — Eye Level CTA Reset

**Source:** prompt_blocks.md, Block 5: "Eye level (peer-to-peer, different from authority hook)." flow_generation_template.md: "Eye level — NOT slightly below."

**What it is:**
The CTA clip always uses eye-level camera angle, intentionally different from the slightly-below angle used in Hook clips. This creates a visible energy shift — the creator steps down from "authority" positioning into "peer" positioning to deliver the CTA.

**Why it works:**
1. The hook's slightly-below angle creates authority — "this person knows something I don't." The CTA's eye-level creates warmth — "this person is talking to me as an equal."
2. The visible angle shift signals: "we've moved from teaching to inviting." The viewer's emotional state shifts from "receiving information" to "being invited to act."
3. Eye-level CTAs feel less like advertising — they feel like a friend telling you what to do next
4. The contrast between the hook angle and CTA angle creates a structural rhythm that the viewer can feel (consciously or not)

**Implementation:**
```
HOOK CLIPS (1-3): Camera slightly below eye level
  Purpose: Authority, "I know something you don't"
  Angle: Camera lens is at creator's chest level, creator looks slightly down

CTA CLIP (always last): Camera at eye level
  Purpose: Warmth, invitation, peer-to-peer
  Angle: Camera lens at creator's eye level — direct gaze, not down-gaze

ACTING SHIFT on CTA clip:
  From Hook: Forward lean, steepled hands, higher energy
  To CTA: Shoulders drop, open palm, slower pace, genuine warmth
  The physical shift matches the visual angle shift

PROMPT LANGUAGE FOR CTA CLIP:
"CAMERA ANGLE: Eye level — NOT slightly below. Peer-to-peer warmth."
"ACTING: Shoulders relaxed, open palm forward, unhurried. Inviting, not selling."
```

---

### VP14 — Hook Silence (No Music First 3 Seconds)

**Source:** Formula library (F01): "No music on hook (silence)." (F02): "Silence on hook, tension-building music starts on AGITATE."

**What it is:**
For F01, F02, and F08 (and any high-stakes hook), the first 3 seconds of the reel play with no background music. The creator's voice is the only audio. Music enters on the AGITATE beat (3s mark).

**Why it works:**
1. Silence forces the viewer's attention to the voice — there is nothing else to process
2. Silence signals gravity — "this is important enough that we don't need music to make it interesting"
3. The contrast between silent hook and music-entry creates a natural emphasis moment — the music entry at AGITATE signals "now we're getting into it"
4. On a platform where every Reel has music, a silent opening creates a pattern interrupt at the audio level, not just visual

**Implementation:**
```
TIMING:
0-3s: Silence — no music, no SFX (notification ping only acceptable for F07 cold open)
3s: Music enters — upbeat electronic instrumental at 35% volume
3-25s: Music holds at 30-40%
25-30s: Music at 25% (CTA — warm, not distracting)
30s: Music fades (0.5s)

FORMULAS THAT USE SILENCE ON HOOK:
F01 (AI Cheat Code) — standard
F02 (Future Shock) — standard
F08 (Mind Transformation) — standard (matches the gravity of quality gap)
F03 (Hollywood VFX) — cold open is silent (different rule — output is silent before creator appears)

FORMULAS THAT DO NOT USE SILENCE:
F07 (News Flash) — music enters at Clip 1 to create news-desk energy
F04 (Hidden Tool) — can enter music under hook (lower stakes, more excitement)
F09 (Three Step System) — music from frame 1 (system formulas benefit from productive energy)
F10 (Comment React) — music at low volume throughout (most casual formula)
```

---

### VP15 — The "Kya Matlab Hai Tumhare Liye" Pivot

**Source:** AI_SNIPP_REEL_011 — each certification explained with "useful hai" (practical implication). EX02: "Tumhare liye iska matlab:" section in caption. F07 caption template from formula library.

**What it is:**
After presenting a fact, tool, or news item, the creator explicitly pivots to the Indian-audience implication: "aur yeh tumhare liye matlab kya hai?" (and what does this mean for you?). In captions, this appears as the "Tumhare liye iska matlab:" section.

**Why it works:**
1. News and tool information is useless without an action implication — the pivot converts information into instruction
2. The "for you" framing is parasocial — it makes the creator feel like a personal advisor, not a broadcaster
3. Indian-specific implications are @ai_snipp's primary differentiation from Western AI creators who don't speak to this audience's specific situation (Indian job market, rupee pricing, regional language features)
4. The pivot structure trains the viewer to expect actionable takeaways — creating a listening mode where they stay through the explanation to reach the implication

**Implementation:**
```
ON-CAMERA PIVOT PHRASES:
"Aur yeh tumhare liye matlab kya hai?"
"Indian developers ke liye iska matlab hai..."
"Jo Indian students AI seekh rahe hain — unke liye yeh change hai..."
"Freelancers ke liye iska practical matlab hai..."

CAPTION FORMAT (F07 — from formula library):
"Kya hua: → [facts with bullets]
Tumhare liye iska matlab: → [implications with bullets]"

TIMING WITHIN REEL:
News/fact content: 8-18s
Pivot signal: "Matlab..." or "Tumhare liye iska matlab..." at ~18s
Implication content: 18-24s
CTA: 24-30s

WHERE TO DEPLOY:
Always in F07 (News Flash) — mandatory
Always in F02 (Future Shock) — mandatory
Optional but recommended in F04 (Hidden Tool), F05 (Career List) — "aur kaam aata hai kyunki..."
```

---

## PATTERN COMBINATION EXAMPLES

**High-performing combination for F05 (Career List):**
VP01 (Bete Roast) + VP02 (8s rhythm) + VP03 (Premium UI) + VP04 (Facecam layout) + VP12 (3-item format) + VP06 (Hinglish) + VP13 (Eye Level CTA)
→ Reference: AI_SNIPP_REEL_011 — all patterns present

**High-performing combination for F09 (Three Step System):**
VP08 (Pre-Save Hook) + VP02 (8s rhythm) + VP06 (Hinglish) + VP07 (Hard Cuts) + VP13 (Eye Level CTA) + VP14 (Hook Silence)
→ Reference: EX03 — most of these patterns applied

**High-performing combination for F07 (News Flash):**
VP15 (Kya Matlab) + VP02 (8s rhythm) + VP06 (Hinglish) + VP04 (Facecam for implication clip) + VP13 (Eye Level CTA)
→ Reference: EX02

---

## PATTERN LIBRARY MAINTENANCE

**Add a new pattern when:**
- A reel outperforms baseline by 2× and the performance can be traced to a specific structural element
- A competitor reel goes viral and its pattern is identifiable, adaptable, and not already in the library

**Update an existing pattern when:**
- Performance data suggests the pattern is working differently than documented
- A new variation of the pattern is discovered

**Retire a pattern when:**
- The pattern has become ubiquitous across all AI content creators — no longer differentiating
- Platform changes (Instagram algorithm, format changes) make the pattern less effective
- 10+ reels using the pattern show declining returns

**Track performance impact:** After implementing a pattern combination for the first time, log the reel's performance metrics at 24h, 72h, and 7 days against the account baseline. This is how patterns get validated, refined, or retired.
