# AI_SNIPP Character Sheet — Canonical Identity

**Version:** 2.0
**Status:** Canonical — do not modify without approval
**Source:** Parth.png — actual reference photo of the creator
**Updated:** 2026-06-23 — corrected beard, age, accessories, wardrobe from photo analysis
**Purpose:** Single source of truth for all AI_SNIPP content generation

---

## Identity

| Field | Value |
|---|---|
| **Brand handle** | @ai_snipp |
| **Character archetype** | The Smart Insider — the friend who actually understands AI and shares it without gatekeeping |
| **On-screen persona** | Confident educator with playful sarcasm. Never condescending. Always in on the joke. |
| **Language** | English (script), Indian English accent (delivery) |
| **Audience relationship** | Feels like a slightly older batchmate who got into AI early and is now showing you the shortcut |

---

## Physical Specification — LOCKED

These attributes are fixed across ALL generated content. Any deviation is a generation failure.
Reference image: `D:\AI_OS\05_content\AI_SNIPP\03_character\Parth.png`

### Face
- **Ethnicity:** South Asian / Indian male
- **Age appearance:** Early-to-mid 30s
- **Skin tone:** Medium-brown, warm olive undertones. Not dark, not light. Warm copper-brown.
- **Face shape:** Defined jawline, slight angularity, lean face
- **Expression default:** Calm intensity — direct gaze, slightly serious, on the edge of saying something important

### Hair — KEY IDENTIFIER #1
- **Texture:** Dense, tight natural coil curls. Densely packed coil pattern — not waves, not loose curls, actual tight coils.
- **Color:** Deep black, no highlights
- **Volume:** High — full, rounded afro-style crown. Curls extend upward with significant height on top.
- **Style:** Natural, unstyled. Full volume all around — NOT cropped or faded on sides. Consistent curl density top and sides.
- **Must preserve:** The curl pattern and crown volume are the single most visually distinctive features.

### Beard — SPARSE GOATEE PATTERN
- **Style:** Sparse short stubble — goatee pattern. Mustache and chin area have the most coverage. Cheek coverage is light/patchy.
- **Density:** NOT a full beard. NOT dense. Sparse, natural growth.
- **Length:** Approximately 3–5mm.
- **Color:** Deep black, matching hair
- **Shape:** Natural — looks like 4–5 day growth. Not sharply edged or groomed to clean lines.
- **CRITICAL CORRECTION (v1.0 was wrong):** Previous version said "short full beard covering jaw, chin, cheeks fully." That was INCORRECT. The beard is sparse goatee-pattern stubble, NOT a full beard.

### Glasses — KEY IDENTIFIER #2
- **Style:** Bold rectangular frames, slightly wide-set
- **Color:** Matte black frame throughout (no metal accents)
- **Lens:** Standard clear lenses, slight glare/reflection possible in studio light
- **Fit:** Sits mid-bridge, natural position
- **Must preserve:** Black rectangular glasses are the single most recognizable brand element. Never remove, never change frame style.

### Eyes
- **Color:** Dark brown, nearly black
- **Expression:** Direct, sharp, engaged. Slightly intense.
- **Contact:** Usually looking directly into the camera lens

### Build
- **Frame:** Lean/slim build. Defined jaw and cheekbones.
- **Posture:** Naturally upright. Engaged, not stiff.

---

## Wardrobe

### LOCKED elements (never change between clips)
Face, skin tone, hair (curl pattern + volume + color), beard (sparse goatee pattern), glasses (black rectangular).

### VARIABLE elements (change per reel — by design)
Background environment and clothing. Different outfits keep the content visually fresh while the face locks identity.

### Reference look (Parth.png — default)
- Dark olive/army green button-up casual overshirt, collar open, worn OVER a black t-shirt
- Layered look — the button-up is not a jacket, it's an unbuttoned overshirt
- No patterns, no logos, no bright colors

### Approved clothing variations

| Variation | When to Use | Notes |
|---|---|---|
| Dark olive overshirt over black tee | Default — matches reference photo | Parth.png look |
| Plain black t-shirt alone | Clean/minimal content | Well-fitted, no graphics |
| Dark navy or charcoal t-shirt | Different energy | Plain, same fit |
| Smart casual button-up (dark) | Investment/serious topics | Collar open |
| Black hoodie | Late-night/casual tone | Plain, no branding |
| White/off-white t-shirt | Contrast segments (before/after) | Same fit |

**Rule:** Dark neutrals only. No patterns, no logos, no bright colors.

### Studio equipment (visible in frame — NOT wardrobe but part of the studio look)
- **Microphone:** Large professional condenser microphone (large diaphragm, silver/black) on a boom arm — partially visible at frame edge, soft-focused. This is a studio setup.
- **CORRECTION (v1.0 was wrong):** Previous version said "small lavalier clip-on mic clipped to shirt." That was INCORRECT. It's a large studio condenser mic, not a lavalier.
- **Watch:** Not part of the character spec — not visible in reference photo and should not be specified.

---

## CHARACTER IDENTITY LOCK TEXT BLOCK

Embed this in every Higgsfield MCP clip prompt, after `<<<element_id>>>`, before the scene description.
This text provides additional conditioning alongside the visual Element.

```
CHARACTER IDENTITY LOCK — Parth (@ai_snipp):
Indian male, early-to-mid 30s. Medium-brown skin, warm olive undertones. Dense tight natural coil curls — deep black, high-volume rounded afro crown, full curl density top and sides, NOT faded or cropped on sides. Sparse short stubble beard — 3–5mm, goatee pattern — mustache and chin strongest, light on cheeks, NOT a full dense beard covering all cheeks. Bold black rectangular glasses, clear lenses. Lean build, defined jaw. Background and clothing vary per reel. Face, hair curl pattern, beard pattern, and glasses ARE LOCKED and DO NOT CHANGE between clips.
```

Do not shorten or paraphrase. The negative descriptors ("NOT faded", "NOT a full dense beard") are
necessary to counter Seedance's tendency to generate faded sides and full beards by default.

---

## Personality & On-Screen Behavior

### Core Personality Traits

**1. Confidently Casual**
Never tries too hard. Confidence comes from competence, not performance.

**2. Playfully Sarcastic**
Uses roasting as a teaching tool. Gentle mentor energy. Never mean. Always accompanied by warmth.

**3. Genuinely Helpful**
The sarcasm lowers guard. Underneath every roast is real, actionable information.

**4. Fast-Brained**
Speaks quickly. Gets to the point. Respects the audience's time.

**5. Insider Positioning**
Always positioned as someone who found something before others. Creates FOMO while delivering the solution.

### Speaking Style
- **Pace:** Fast — 20–30% above average delivery speed
- **Pauses:** Strategic — after hooks, after key reveals
- **Vocabulary:** English with authentic Indian English delivery
- **Sentence structure:** Short, punchy. Every line earns its place.
- **Humor type:** Situational irony, self-aware observations, gentle audience roasting

### Hand Gestures
- Default: Hands interlocked or steepled in front
- **NEVER:** Finger-counting (1, 2, 3 fingers) — looks forced on camera
- **NEVER:** Pointing directly at the lens — feels aggressive
- **PREFERRED:** Open palm forward (emphasis), slight forward lean (important reveal)

---

## Voice Profile

| Quality | Description |
|---|---|
| **ElevenLabs Voice ID** | `2UVVG78koJmSOKFywat7` |
| **Model** | `eleven_multilingual_v2` |
| **Tone** | Warm baritone. Mid-register male voice. |
| **Energy** | High energy but controlled. Confident without being aggressive. |
| **Pace** | Fast. 20–30% faster than conversational speed. |
| **Accent** | Natural Indian English accent. Authentic desi inflection. Not neutralized. |
| **Emotional range** | Curiosity → insight → emphasis → warmth |

---

## Revision Log

| Version | Change | Date |
|---|---|---|
| 1.0 | Initial — reverse-engineered from Character.png | 2026-06-08 |
| 2.0 | Full correction from actual Parth.png photo analysis. Fixed: age (early-to-mid 30s, not 20s), beard (sparse goatee stubble NOT full beard), accessories (studio condenser mic not lavalier, watch removed), wardrobe default (olive overshirt over black tee). Added CHARACTER IDENTITY LOCK text block for Higgsfield MCP. Added ElevenLabs voice ID. | 2026-06-23 |
