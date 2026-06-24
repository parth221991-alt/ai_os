# HeyGen Avatar + Screen Recording — Production Guide
## AI_SNIPP Production System — HASR Format

**Version:** 1.0  
**Status:** Canonical  
**Format:** HeyGen Avatar + Screen Recording (HASR)  
**Target output:** 720×1280 → upscale export 1080×1920, 25fps, 27–45 seconds  
**Reference:** See `references/heygen_video_format_analysis.md`

---

## Overview

This guide covers the complete production pipeline for the HASR format — the same format used in reference1.mp4, reference2.mp4, reference3.mp4. It replaces Stages 4+5 (Flow Generation) for reels using this format.

**Total production time (once avatar is set up):** 30–60 minutes per reel

---

## One-Time Setup: Create Your HeyGen Avatar

Do this once. All future reels use the same avatar.

### Step 1 — Record Avatar Training Video
- **Duration:** 2–3 minutes (Instant Avatar) or 5 minutes (Studio Avatar — higher quality)
- **Background:** Plain wall or neutral background — HeyGen composites a studio background later
- **Lighting:** Face well-lit, even. No harsh shadows. Ring light or window light works.
- **Camera:** Phone camera, 1080p, horizontal or vertical both work
- **Clothing:** The outfit you record in is locked to the avatar — choose carefully
  - Recommendation: Plain dark t-shirt (disappears, timeless, matches AI_SNIPP aesthetic)
- **What to say:** Read any 2-3 minute text — a Wikipedia article, a script, anything. HeyGen just needs lip movement data.
- **Do NOT:** Move your head too much, touch your face, look away constantly

### Step 2 — Upload to HeyGen
1. Go to HeyGen → Avatars → Create Avatar
2. Choose "Instant Avatar" (fast, good) or "Studio Avatar" (slower, better)
3. Upload your training video
4. Wait for processing (Instant: 5 min, Studio: up to 1 hour)

### Step 3 — Clone Your Voice
1. In HeyGen: Voice → Clone Voice
2. Record 30–60 seconds of yourself speaking clearly
3. Or: Use ElevenLabs (better quality) and connect via HeyGen's ElevenLabs integration
4. Name it with your channel name for reuse

### Step 4 — Test the Avatar
- Paste a 10-second test script
- Check: lip sync accuracy, voice naturalness, head movement realism
- If off: re-record training video with more varied head angles

---

## Per-Reel Production Workflow

### STAGE 1–3: Same as Standard Pipeline
Content request → Production brief → Storyboard — no changes needed.

**Additional storyboard consideration for HASR format:**
- Identify which clips use Pattern A (avatar full + card overlay), Pattern B (split screen), or Pattern C (full content)
- For each screen-recording clip: note exactly which website/URL and what interaction to record
- Avatar is always present — no "creator absent" clips in HASR format

---

### STAGE 4-HASR: Generate Avatar Video

**Step 1 — Prepare Script**
- Final script from production brief
- Break into sections that match your layout patterns
- Mark [PAUSE] wherever you want a natural pause in delivery
- Mark [EMPHASIS: word] for words to speak with extra weight

**Step 2 — Enter Script in HeyGen**
1. HeyGen → Create Video → select your Avatar
2. Paste full script
3. Select your cloned voice
4. Adjust speaking pace: set to slightly faster than default (matches reference video energy)
5. Preview first 5 seconds — check lip sync and pacing

**Step 3 — Generate and Download**
- Generate (typically 2–5 minutes for a 30-second script)
- Download as MP4
- File name: `REEL_[NNN]_AVATAR_v1.mp4`

**Step 4 — Quality Check**
- [ ] Lip sync accurate throughout
- [ ] No visible AI artifacts (warping, mouth glitches)
- [ ] Voice pace matches your script's energy
- [ ] Head movement looks natural — not robotic
- If issues: adjust pacing/pauses in script and regenerate

---

### STAGE 5-HASR: Record Screen B-Roll

Record the screen content for your split-screen segments.

**Setup:**
- Browser zoom: 110–125% (so UI text is legible when scaled to mobile)
- Dark mode: always — light mode UI looks washed out in this format
- Resolution: record at 1920×1080
- Tool: OBS Studio (free), Loom, or Windows Game Bar (Win+G)

**Recording technique:**
- Slow deliberate scroll — pause 1–2 seconds on key elements
- Keep mouse cursor away from important text if possible
- Record 10–20% more than you need — trim in edit
- For each screen clip needed, record a clean take separately

**File naming:** `REEL_[NNN]_SCREEN_[A/B/C]_v1.mp4`

**B-roll types by formula:**
| Formula | B-roll to record |
|---|---|
| F01 AI Cheat Code | The tool being used, input → output |
| F04 Hidden Tool | Tool homepage, key feature, pricing page |
| F05 Career List | Each tool's website, certification page |
| F07 News Flash | GitHub repo, announcement tweet, product page |
| F09 Three-Step | Each tool/step in sequence |

---

### STAGE 6-HASR: Edit in CapCut

CapCut is the recommended editor for this format. It has native word-by-word captions and easy split-screen compositing.

#### 6A — Project Setup
1. New project → set ratio to 9:16
2. Import: `REEL_[NNN]_AVATAR_v1.mp4` and all screen B-roll files
3. Add avatar video to main track

#### 6B — Layout Compositing

**Pattern B — Split Screen (most common):**
1. Add avatar to main track (full canvas)
2. Add screen recording to overlay track
3. Scale screen recording to fill top 50% of frame
4. Scale avatar to fill bottom 50% of frame
5. Align so the split is clean at center
6. Add thin divider line (1–2px white) at split if desired

**Pattern A — Avatar Full + Card Overlay:**
1. Avatar on main track (full screen)
2. For each card: add as overlay, position in lower 35% of frame
3. Animate cards: slide up from bottom (0.3s ease-out)
4. Cards appear when narrator mentions them, exit when moving on

**Pattern C — Full Content Screen:**
1. Screen recording on main track (full frame)
2. Avatar as small PiP overlay in corner (optional — can be audio only)
3. Scale content to fill frame (crop/zoom as needed)

#### 6C — Word-by-Word Captions (Critical — This Is The Visual Signature)

1. On avatar track: Text → Auto Captions → Generate
2. Set voice language to match your recording
3. After generation, select all captions → change style:
   - Font: Montserrat ExtraBold or Inter Bold (Bold is mandatory)
   - Color: White `#FFFFFF`
   - Shadow: Black, small offset (2–3px)
   - Background: None (no pill, no box)
   - Size: Large (test on mobile — must be readable without squinting)
4. Animation: Set to "Pop" or word-by-word reveal
5. **Review every line** — auto-captions misread proper nouns (tool names, Hindi words)
6. Position: Center frame, 55–65% from top

**Emphasis size trick:**
- Select individual words and increase size by 30–50% for key words
- This creates the "big word small word" rhythm seen in reference videos
- Apply to: numbers, tool names, strong verbs ("FORGET", "Claude", "$10,000")

#### 6D — Audio Layers
1. Avatar audio is already embedded in HeyGen download — keep it
2. Add background music: start at 3s mark, volume 25%
3. SFX on transitions: short whoosh (0.1–0.2s) on each layout change
4. Fade out music 0.5s before end

#### 6E — Color Consistency
- HeyGen avatar may have slightly different color temperature than screen recordings
- Apply a warm LUT or gentle +10 warmth to screen clips to match avatar tone
- Screen recordings: slight contrast boost for legibility

#### 6F — Transitions
- Between layout patterns: hard cut + whoosh SFX (no dissolves)
- Between points within same layout: hard cut only
- Keep all transitions under 0.2s — fast paced is the format

#### 6G — Export
| Setting | Value |
|---|---|
| Resolution | 1080 × 1920 |
| Frame rate | 30fps |
| Format | MP4 H.264 |
| Bitrate | High (10–15 Mbps) |
| Audio | AAC 320kbps |
| File name | `REEL_[NNN]_FINAL_v1.mp4` |

---

## Storyboard Template for HASR Format

Use this structure when planning a HASR reel (replaces clip-by-clip Flow storyboard):

```
REEL_[NNN] — HASR STORYBOARD

TOTAL DURATION: [XX]s

AVATAR SCRIPT (full, broken by layout beat):
---
[0:00–0:08] LAYOUT: Pattern A/B/C
Script: "[exact words]"
Screen B-roll: [URL or description]
Caption emphasis words: [list key words to make large]
---
[0:08–0:20] LAYOUT: Pattern A/B/C
Script: "[exact words]"
Screen B-roll: [URL or description]
Caption emphasis words: [list]
---
[0:20–0:27] LAYOUT: Pattern A/B/C  
Script: "[CTA words]"
Screen B-roll: none (avatar full or PiP)
Caption emphasis words: [list]
---

SCREEN RECORDINGS TO CAPTURE:
1. [URL] — [what to record, how long, what to show]
2. [URL] — [same]

MUSIC MOOD: [e.g., confident electronic, medium-fast, starts at 3s]
```

---

## Quality Gate — Before Publishing

- [ ] Avatar lips sync accurately to audio throughout
- [ ] No AI glitch frames (especially at beginning and end of avatar clip)
- [ ] Screen recording is legible on a 6" phone screen
- [ ] Captions reviewed — no misread words, especially tool/product names
- [ ] Emphasis words are visually larger for key terms
- [ ] Music does not overpower voice at any point
- [ ] Export spot-checked on actual phone before uploading
- [ ] Duration within formula target (±2s)
