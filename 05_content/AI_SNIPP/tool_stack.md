# AI_SNIPP — Complete Tool Stack
## Every tool used in production, with role and priority

**Last updated:** 2026-06-09  
**Format reference:** `references/heygen_video_format_analysis.md`

---

## Tier 1 — Core (Required for Every Reel)

### HeyGen
**Role:** AI avatar video generation — the talking head  
**What it does:** Takes your script text → outputs a photorealistic video of your AI avatar speaking it  
**Why:** Single most important tool. Replaces 4–8 hours of Flow generation with 5 minutes. Consistent character, automatic lip sync.  
**Plan:** Creator ($29/mo) — sufficient for ~4 reels/week  
**URL:** heygen.com  
**Setup:** See `04_storyboards/heygen_production_guide.md` → One-Time Setup section  
**Key feature to use:** Instant Avatar (fast) or Studio Avatar (better quality)

**For you specifically:** Upload a 2-min video of yourself → creates YOUR face as the avatar. Every reel you generate will have your face speaking your script. The reference videos use a white woman — yours will use you.

---

### CapCut (Desktop)
**Role:** Video editing, split-screen compositing, word-by-word captions, music, SFX  
**What it does:** Combines avatar video + screen recordings + captions + audio into the final reel  
**Why:** Has native "Auto Captions" with word-by-word animation built in. Free. Designed for 9:16 vertical content.  
**Plan:** Free tier is sufficient  
**Key features to use:**
- Auto Captions → word highlight mode (the animated captions in the reference videos)
- Overlay track for split-screen composition
- Template animations for card slide-up effect

---

### OBS Studio
**Role:** Screen recording for B-roll footage  
**What it does:** Records your screen — website scrolls, tool demos, GitHub pages  
**Why:** Free, zero watermark, high quality, configurable resolution  
**Plan:** Free  
**Settings to use:** 1920×1080, 30fps, MP4 output, Window Capture mode  
**Alternative:** Windows Game Bar (Win+G) works fine for simple recordings

---

### ElevenLabs
**Role:** Voice cloning for natural Hindi/English delivery  
**What it does:** Clones your voice from a 1-minute sample. HeyGen uses it to speak your script in your voice.  
**Why:** HeyGen's built-in voice is decent but ElevenLabs quality is noticeably better, especially for Hindi.  
**Plan:** Starter ($5/mo) or Free (limited characters)  
**Integration:** HeyGen natively integrates ElevenLabs — select your EL voice inside HeyGen  
**Alternative:** HeyGen's built-in voice clone (good enough to start)

---

## Tier 2 — Production Quality (Strongly Recommended)

### Claude (this system)
**Role:** Script writing, hook generation, caption writing  
**What it does:** Write your reel scripts, generate hook variations, draft captions  
**Why:** You already have Claude Pro. Use it for all scripting — it knows your brand voice from the character sheet.  
**How to use:** Feed it the formula file + character sheet → ask for a script on your topic  
**Key prompt:** Use the Production Brief Template as the Claude input format

---

### Canva
**Role:** Creating animated card overlays (Pattern A — product/service card showcase)  
**What it does:** Design the cards shown over the avatar in reference1-style videos  
**Why:** Faster than CapCut for card design. Canva Pro has animated templates.  
**Plan:** Free tier works. Canva Pro ($13/mo) for animated elements.  
**Output:** Export card designs as MP4 animated videos or PNG statics, then overlay in CapCut

---

### Suno / Udio
**Role:** Background music generation  
**What it does:** Generates royalty-free background music matching your mood description  
**Why:** Avoids Instagram copyright strikes. Mood-matched music is better than generic tracks.  
**Prompt template:** "Confident forward-moving electronic instrumental, medium-fast tempo, no lyrics, 60 seconds, builds slightly over time"  
**Plan:** Suno Free tier (10 songs/day)

---

## Tier 3 — Optional / Format-Specific

### Loom
**Role:** Screen recording with instant shareable link  
**Alternative to:** OBS Studio (easier, slightly lower quality)  
**Use when:** You need to record quickly and OBS feels like overkill

---

### DaVinci Resolve
**Role:** Advanced color grading and editing  
**Alternative to:** CapCut (for color-critical reels)  
**Use when:** You need precise color matching between avatar and B-roll clips  
**Plan:** Free tier is excellent

---

### Descript
**Role:** Edit video by editing the transcript  
**What it does:** Shows your avatar video as text — delete a word in text, it removes it from video  
**Use when:** You need to cut or rearrange sections of the HeyGen output  
**Plan:** Hobbyist ($12/mo)

---

### CapCut Auto-Subtitle Alternatives
If CapCut's auto-caption quality is poor for your speech:
- **Captions.ai** — better accuracy, same word-by-word style
- **Opus Clip** — auto-caption + auto-clip selection for repurposing long content
- **Submagic** — purpose-built for this exact caption style

---

## Tool Stack by Production Stage

| Stage | Tool | Alternative |
|---|---|---|
| Script writing | Claude (this session) | ChatGPT |
| Avatar video | HeyGen | Synthesia, D-ID |
| Voice clone | ElevenLabs → HeyGen | HeyGen built-in voice |
| Screen recording | OBS Studio | Windows Game Bar, Loom |
| Card design | Canva | Adobe Express |
| Final editing | CapCut Desktop | DaVinci Resolve |
| Captions | CapCut Auto Captions | Captions.ai, Submagic |
| Background music | Suno AI | Udio, Pixabay Music |
| Export + publish | CapCut → Instagram | Manual upload |

---

## Cost Summary (Monthly)

| Tool | Plan | Monthly Cost |
|---|---|---|
| HeyGen | Creator | $29 |
| ElevenLabs | Starter | $5 |
| Canva | Pro | $13 (optional) |
| Suno | Free | $0 |
| CapCut | Free | $0 |
| OBS Studio | Free | $0 |
| **Total minimum** | | **$34/mo** |
| **Total recommended** | | **$47/mo** |

At 4 reels/week = ~16 reels/month → cost per reel ≈ $2.10–$2.90

---

## Existing Flow System — When to Still Use It

The Flow (AI image generation) system is NOT retired. Use it for:
- **F03 Hollywood VFX** — AI-generated cinematic visuals are the point
- **F08 Mind-Blowing Transformation** — before/after visual transformation
- Any reel where the AI-generated aesthetic is itself the content

Use **HeyGen HASR** for everything else — it is faster, more realistic, and the format the reference videos use.
