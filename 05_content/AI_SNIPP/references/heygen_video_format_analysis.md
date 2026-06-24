# Reference Video Format Analysis — HeyGen Talking Head Style
## AI_SNIPP Production Intelligence

**Source:** reference1.mp4, reference2.mp4, reference3.mp4  
**Analyzed:** 2026-06-09  
**Format name (internal):** HeyGen Avatar + Screen Recording (HASR)  
**Status:** Canonical production reference — this is the exact format to replicate

---

## What These Videos Are

All three are AI-generated "faceless brand" reels where:
- A **HeyGen AI avatar** delivers the narration (talking head — continuous video, not generated images)
- **Real screen recordings** of websites/apps serve as B-roll content
- **Word-by-word kinetic captions** appear in sync with speech
- The composition is a **split-screen or overlay** of avatar + screen content

The original creator uses a white brunette woman. You replace her with your own HeyGen avatar.

---

## Technical Specs (Measured)

| Property | Value |
|---|---|
| Resolution | 720 × 1280 (9:16 vertical) |
| Frame rate | 25 fps |
| Video codec | H.264 High Profile |
| Audio codec | AAC HE-AAC, 48kHz stereo |
| Duration range | 27–43 seconds |
| Bitrate | 737–919 kbps video |

Production target: match at 1080 × 1920 for higher quality export.

---

## Layout System (3 Patterns Identified)

### Pattern A — Avatar Full + Cards at Bottom (reference1)
```
┌─────────────────────────┐
│                         │
│    AVATAR — FULL        │
│    FRAME (talking)      │
│                         │
├────────┬────────────────┤
│ CARD 1 │   CARD 2       │  ← Animated cards appear in lower 35%
│        │                │     while avatar speaks about them
└────────┴────────────────┘
```
Use case: Reviewing product/service content, showing multiple examples

### Pattern B — Screen Top / Avatar Bottom (reference2, reference3 partial)
```
┌─────────────────────────┐
│   SCREEN RECORDING      │
│   (website scroll /     │  ← 50% of frame — real website recording
│   app demo)             │
├─────────────────────────┤
│                         │
│   AVATAR (talking)      │  ← 50% of frame — HeyGen avatar
│                         │
└─────────────────────────┘
```
Use case: Showing a specific tool/website while narrating about it

### Pattern C — Full Screen Content + Avatar Inset (reference3 partial)
```
┌─────────────────────────┐
│                         │
│   FULL SCREEN CONTENT   │
│   (logo, graphic, map,  │  ← Content takes entire frame
│   bold text visual)     │
│                         │
│           WORD TEXT     │  ← Bold kinetic word overlaid
│  [AVATAR small PiP]     │  ← Optional small avatar corner
└─────────────────────────┘
```
Use case: Strong visual hooks, news/announcement content

---

## Caption / Text Style (Exact Specification)

The captions are the most distinctive visual element. Copy this exactly:

### Word-by-Word Pop Style
- **Font:** Bold sans-serif — Montserrat ExtraBold or Inter Bold
- **Color:** Pure white `#FFFFFF`
- **Shadow:** Subtle black drop shadow for legibility
- **Size:** Large — roughly 15–18% of frame width per character
- **Animation:** Each word pops in as it is spoken (not letter by letter, not slide)
- **Emphasis words:** Displayed LARGER and/or BOLDER than surrounding words
- **Position:** Center frame, vertically around 55–65% down from top
- **No background pill/box** — text floats directly over video with shadow only

### Mixed Size Emphasis
The reference videos use **2-tier sizing**:
- Normal words: standard large white text
- Key emphasis words: 30–50% larger, often on their own line
- Example: "What if i" (normal) → "told you" (2× bigger, new line)

### Tool: CapCut Auto Captions
- Generate auto-captions from audio
- Set style to "Pop" or "Karaoke" word-highlight mode
- Customize: white font, no box background, large size
- Review and fix any misrecognized Hindi/Hinglish words manually

---

## Avatar Analysis (HeyGen Signature)

The talking-head avatar has these characteristics confirming it is HeyGen:

1. **Consistent character across all 3 videos** — identical face, clothes, background. HeyGen avatar is cloned once and reused indefinitely.
2. **Background:** Cozy home office — warm bokeh lights on plants/shelves, black microphone, bookshelves. This is a HeyGen **studio background preset** (or close to one).
3. **Lip sync:** Natural, smooth — HeyGen's lip sync quality.
4. **Clothing consistency:** Same red top across all videos — avatar is locked to one appearance.
5. **Frame rate:** 25 fps matches HeyGen's default export.
6. **No motion blur on edges** — AI-generated clean compositing.

**To replicate with yourself:**
1. Record 2–3 minutes of yourself on camera (well-lit, neutral background, face centered)
2. Upload to HeyGen → Create "Instant Avatar" (takes ~5 minutes)
3. For better quality: Create "Studio Avatar" (requires 3-minute consent video + 30-min wait)
4. Clone your voice in the same session
5. All future reels: paste your script → HeyGen generates the video automatically

---

## Screen Recording B-Roll Analysis

The screen recordings are real recordings, not AI-generated:
- Real website interactions (scrolling, hover states, animated UI transitions)
- Resolution matched to 720×1280 (cropped/scaled for mobile)
- Gentle scroll animations — not fast, gives viewer time to absorb the UI
- Recording tool: OBS Studio, Loom, or Windows screen recorder (Win+G)

**B-roll recording tips from reference style:**
- Record at 1920×1080, crop to 720×640 for the top half of the split
- Keep scroll speed slow and deliberate — pause on key elements
- Use browser zoom at 110–125% so text is legible at mobile scale
- Dark mode websites look significantly better in this format

---

## Audio Profile

- **Voice:** Clearly AI-generated (ElevenLabs or HeyGen's built-in voice clone)
- **Pace:** Conversational, slightly above average speed
- **Background music:** Subtle, warm — present but not competing with voice
- **SFX:** Minimal — occasional soft whoosh on transitions
- **Mix:** Voice 100%, music ~25%, SFX as accents

---

## Full Production Breakdown Per Video

### reference1.mp4 (27 seconds)
- Content: AI-generated social media cards for Jakarta Varices Clinic
- Pattern: A (avatar full + cards at bottom)
- Cards animate in from bottom — slide up, 2 at a time
- Avatar occupies full upper 65%
- Bold white word captions overlay the avatar area

### reference2.mp4 (31 seconds)
- Content: Website builder / design demo ($10k website)
- Pattern: B (screen top / avatar bottom) + C (full content)
- Transitions between layout patterns
- Screen recording shows website scroll in upper half

### reference3.mp4 (43 seconds)
- Content: AI tool comparison (LangChain vs AgentScope, Claude)
- Pattern: B + C mixed
- Uses full-screen graphics (tool logos, GitHub page, China map) for visual variety
- More complex edit — multiple B-roll clips

---

## Key Differentiators vs Current Flow-Based System

| Aspect | Current Flow System | HeyGen HASR Format |
|---|---|---|
| Avatar generation | Flow (image-by-image) | HeyGen (continuous video) |
| Character consistency | Requires identity lock prompts | Automatic — same avatar always |
| Production time | 4–8 hours (clip generation) | 30–60 min total |
| Lip sync | Not applicable (static frames) | Automatic, native |
| B-roll | AI-generated visuals | Real screen recordings |
| Cost | Flow subscription | HeyGen ~$29/mo |
| Realism | Stylized/illustrated | Photorealistic |
| Scale | Each clip is manual | Script → video in 5 min |

**Recommendation:** Use HeyGen HASR format as the primary production pipeline. Reserve Flow-based system for creative/cinematic formulas (F03 Hollywood VFX, F08 Mind-Blowing Transformation) where AI-generated visuals are the content.
