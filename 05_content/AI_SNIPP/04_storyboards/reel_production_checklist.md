# Reel Production Checklist
## AI_SNIPP Production System — Master Checklist (All 8 Stages)

*One checklist per reel. This document tracks every reel from topic selection to publish confirmation.*
*Stages 1–5 are covered in their own templates. Stages 6–8 (Editing Plan, Publishing Package, Post-Publish) are detailed here.*

---

## REEL TRACKER

| Field | Value |
|---|---|
| Reel ID | REEL_[NNN] |
| Formula | F[NN] — [Formula Name] |
| Topic | [FILL] |
| Target Duration | [XX]s |
| Target Post Date | YYYY-MM-DD |
| Target Post Time | [HH:MM] IST |
| Actual Post Date | YYYY-MM-DD |
| Final Status | In Progress / Published / Shelved |

---

## STAGE 1 — CONTENT REQUEST

*Template: content_request_template.md*

- [ ] Topic identified and pain point defined
- [ ] Formula selected with justification
- [ ] Hook written in creator's Hinglish voice
- [ ] Hook source is real audience language or verified stat
- [ ] CTA intent defined — one action, one trigger
- [ ] Proof points specific and citable
- [ ] Not a repeat of last 14 days
- [ ] **Content Request signed off — CR_[NNN] assigned**

---

## STAGE 2 — PRODUCTION BRIEF

*Template: production_brief_template.md*

- [ ] Reel goal defined with specific measurable metric
- [ ] Full script written — all 5 beats (Hook, Agitate, Insight, Proof, CTA)
- [ ] Script read-aloud test passed at target duration
- [ ] Visual plan complete — all clips have Block Type
- [ ] Clip durations sum to target ± 2s
- [ ] Caption complete — hook line, body, CTA line, hashtag set
- [ ] Formula mandatory caption line present
- [ ] Audio plan specifies music mood AND SFX per clip
- [ ] **Production Brief signed off — REEL_[NNN] assigned**

---

## STAGE 3 — STORYBOARD

*Template: storyboard_template.md*

- [ ] All clips storyboarded — no blank blocks
- [ ] Every clip has: Block Type, acting direction, overlay spec, transition
- [ ] Frame sketches show creator position and overlay position
- [ ] CTA clip (Block 5) is final clip — camera angle is eye level
- [ ] Creator absent in Clips 1-2 only for F03/F08
- [ ] Continuity notes explain cross-clip changes
- [ ] Asset checklist complete — all required materials identified
- [ ] **Storyboard signed off**

---

## STAGE 4+5 — AVATAR GENERATION

*Two paths depending on formula. Choose one:*

### PATH A — HeyGen HASR Format (Default — use for most formulas)
*Full guide: `04_storyboards/heygen_production_guide.md`*

- [ ] Script finalized and marked with [PAUSE] and [EMPHASIS] cues
- [ ] Script pasted into HeyGen — avatar and voice selected
- [ ] HeyGen preview (first 5 seconds) reviewed — lip sync accurate
- [ ] Full video generated and downloaded: `REEL_[NNN]_AVATAR_v1.mp4`
- [ ] Avatar quality check: no glitch frames, lip sync accurate throughout
- [ ] Screen B-roll recorded for each split-screen segment
- [ ] B-roll files named: `REEL_[NNN]_SCREEN_[A/B/C]_v1.mp4`
- [ ] **All HASR assets ready for edit**

**Use HASR for:** F01, F04, F05, F06, F07, F09, F10, F02

### PATH B — Flow Generation (Cinematic / VFX formulas)
*Template: flow_generation_template.md*

- [ ] Character.png attached to session
- [ ] Test clip generated — 5-Point Check passed (5/5)
- [ ] Session seed recorded
- [ ] All clips accepted — 5-Point Check ✓ on each
- [ ] Session log complete — takes, issues, corrections, file names
- [ ] Files renamed: `REEL_[NNN]_CLIP[N]_v[N].mp4`
- [ ] **All clips accepted and organized**

**Use Flow for:** F03 (Hollywood VFX), F08 (Mind-Blowing Transformation)

---

## STAGE 6 — EDITING PLAN

*Editing happens in CapCut (HASR path) or DaVinci Resolve / Premiere Pro (Flow path).*  
*For HASR full CapCut workflow: see `heygen_production_guide.md — Stage 6-HASR`*

### 6A — Assembly Plan

**HASR path:**
| Step | Action | Notes |
|---|---|---|
| Import | Import REEL_[NNN]_AVATAR_v1.mp4 + all SCREEN files | Verify all clips load |
| Layout | Set up split-screen per storyboard pattern (A/B/C) | See heygen_production_guide.md |
| Captions | Auto Captions → word-highlight style → review all words | Fix tool names, Hindi words |

**Flow path:**
| Step | Action | Notes |
|---|---|---|
| Import | Import all REEL_[NNN]_CLIP[N]_v[N].mp4 files | Verify all clips load correctly |
| Sequence | Arrange in Clip 1 → 2 → 3 → 4 order on timeline | |
| Rough cut | Trim any dead air or false starts at clip edges | |
| Transitions | Apply planned transitions (from storyboard) | |

**Transition specs:**
- Hard cut: no transition effect, instantaneous
- Whoosh + cut: 0.2s whoosh SFX before cut, no visual dissolve
- Fade: 0.3s fade to black between clips (CTA only if used)

### 6B — Audio Edit

**Music:**
- [ ] Source track confirmed: [FILL — track name / source]
- [ ] Music entry point: [FILL — e.g., "Starts at 3s — on AGITATE beat"]
- [ ] Music volume: Background only — speech always dominant
  - Hook (0-3s): [FILL — silent OR music at 20%]
  - Main content (3-25s): Music at 30-40%
  - CTA (25-30s): Music at 25% (warm, not distracting)
- [ ] Music fade-out at end: 0.5s fade at reel end
- [ ] Music does NOT overlap with key spoken words

**SFX (per clip):**
| Clip | SFX | Source | Timing in Clip |
|---|---|---|---|
| 1 | [FILL] | [FILL] | [X.Xs] |
| 2 | [FILL] | | |
| 3 | [FILL] | | |
| 4 | None (CTA — clean audio) | | |

**Voice audio:**
- [ ] Audio is clear — no background noise, no echo
- [ ] Pace is fast but every word is intelligible
- [ ] Hinglish delivery sounds natural — not read off a script
- [ ] No dead air pockets > 0.2s between sentences

### 6C — Text Overlays and Graphics

**Captions:**
- [ ] Auto-captions generated (CapCut / Captions.ai)
- [ ] Captions reviewed and corrected — especially Hindi/Hinglish words
- [ ] Caption style: Bold sans-serif (Inter Bold or Montserrat ExtraBold), ALL CAPS for emphasis, white text, black shadow
- [ ] Caption timing synced to speech — no lag

**On-screen text (per storyboard overlay spec):**
| Clip | Text | Style | Entry timing | Exit timing |
|---|---|---|---|---|
| [N] | [FILL] | [Bold / Normal] | [Xs] | [Xs] |

**@ai_snipp watermark:**
- [ ] Present on CTA clip (Clip 4) lower-right
- [ ] Size: Small — present but not distracting
- [ ] Present on every clip if brand watermark policy — [confirm preference]

**End card (CTA clip):**
- [ ] Text: "AI Tools • AI Certifications • AI Updates • AI Cheat Codes"
- [ ] Position: Lower-third
- [ ] Style: White, small, warm off-white (#F5E6D0 optional)

### 6D — Color Grade

**Subject:**
- [ ] Warm amber key light preserved — creator is warm, not cool
- [ ] Skin tone maintained — no green or blue cast from monitor glow

**Background:**
- [ ] Deep charcoal, near-black maintained
- [ ] Monitor glow (electric blue/teal) present and not overblown

**Formula-specific grade adjustment:**
- [ ] F02 (Future Shock): -5 to -10% saturation, slightly cooler overall
- [ ] F06 (AI vs Human): "Before" side desaturated/cooler, "After" side full/warm
- [ ] F08 (Transformation): Same as F06 — before cool, after warm
- [ ] F10 (Comment React): Warmest grade — most amber, least contrast
- [ ] All others: Standard warm grade

### 6E — Final Review Before Export

Watch full edit once end-to-end:

- [ ] Pacing: Pattern interrupt every 1.5-2s (cut, text reveal, zoom pop, or SFX)
- [ ] Audio: Music does not overpower speech at any point
- [ ] Character: Consistent across all clips — same person visible
- [ ] Captions: No errors in Hinglish words, timing correct
- [ ] CTA: Clear, single action, warm delivery
- [ ] Duration: [XX]s ± 2s — confirmed
- [ ] No jarring color jumps between clips
- [ ] @ai_snipp watermark visible on appropriate clips

### 6F — Export Settings

| Setting | Value |
|---|---|
| Format | MP4 (H.264) |
| Resolution | 1080 × 1920 (9:16, 1080p) |
| Frame rate | 30fps |
| Bitrate | 8-15 Mbps |
| Audio | AAC 320kbps stereo |
| File name | REEL_[NNN]_FINAL_v[N].mp4 |

- [ ] Export complete — file size reasonable (< 200MB preferred for Instagram)
- [ ] Exported file spot-checked on mobile device at actual size

**STAGE 6 SIGN OFF:** _____________________ Date: _________

---

## STAGE 7 — PUBLISHING PACKAGE

*All assets prepared before opening Instagram. Everything ready before posting.*

### 7A — Caption File

**Final caption (copy-paste ready):**
```
[PASTE FINAL CAPTION HERE — complete, with emojis, line breaks, hashtags]
```

**Caption character check:**
- [ ] First line is hook — no "Hey guys", no "In today's reel"
- [ ] First 125 characters visible before "more" — confirmed engaging
- [ ] Mandatory formula line present (Save karo / Comment mein poocho / etc.)
- [ ] CTA line present with trigger word in quotes if DM CTA
- [ ] Hashtags in final paragraph (not mixed in body text)
- [ ] Hashtag count: 5-15 (Instagram optimal range)
- [ ] No broken characters or encoding errors in Hindi text

### 7B — Thumbnail / Cover Frame

**Cover frame selection:**
> [FILL — which clip, which timestamp, what the still shows]

**Cover frame requirements:**
- [ ] Creator's face clearly visible (not mid-blink, not obscured)
- [ ] High contrast against typical Instagram grid
- [ ] Represents the reel's topic — viewer should understand the value from the cover alone
- [ ] If adding cover text: Bold, minimal, white on dark — max 5 words

**Cover file:** `REEL_[NNN]_COVER.jpg`

### 7C — Instagram Upload Checklist

- [ ] Video file: REEL_[NNN]_FINAL_v[N].mp4
- [ ] Cover frame selected or uploaded
- [ ] Caption pasted from caption file — verify no truncation
- [ ] Location tag: [optional — add if relevant]
- [ ] Collaborator tag: [optional — only if featuring another account]
- [ ] Alt text: [optional — accessibility, also aids discoverability]
- [ ] Audio: Confirm volume levels play correctly on Instagram preview
- [ ] Posting time: [HH:MM] IST — scheduled or ready to post

### 7D — Cross-Post Plan (optional)

| Platform | Format | Adjustments needed |
|---|---|---|
| YouTube Shorts | 9:16, same file | Title and description separate |
| LinkedIn | 9:16 supported | More professional caption angle |
| Twitter/X | 9:16 supported | Shorter caption, no hashtag block |

- [ ] Cross-post assets prepared
- [ ] Platform-specific captions drafted if different tone needed

**STAGE 7 SIGN OFF:** _____________________ Date: _________

---

## STAGE 8 — POST-PUBLISH

*24 hours, 72 hours, and 7-day performance review.*

### 8A — Immediate (First 30 Minutes)

- [ ] Reel posted — confirm it appears on profile grid
- [ ] First comment posted from creator (seeding engagement)
  > [FILL — e.g., "Comment: 'DM karo "SYSTEM" 👇 — main bhej deta hun'"]
- [ ] Story posted with reel link (poll or question sticker to boost engagement)
- [ ] All DMs responded to within 30 minutes of first DM received

### 8B — 24-Hour Review

| Metric | Target | Actual |
|---|---|---|
| Views | [FILL] | |
| Likes | [FILL] | |
| Comments | [FILL] | |
| Shares | [FILL] | |
| Saves | [FILL] | |
| DMs received | [FILL] | |
| Followers gained | [FILL] | |
| Watch time % | > 60% | |

**24-hour assessment:**
- [ ] Performing above target — no action needed
- [ ] Underperforming — hook issue → note for next reel
- [ ] Underperforming — algorithm delay (normal if <100 followers) → wait 72h

### 8C — 72-Hour Review

*Repeat metric table with 72-hour actuals. Assess trajectory (growing or flatlined).*

**Primary metric vs target:**
> [FILL — e.g., "DMs: 47 received vs 150 target. Hook underperformed. Reason: topic too niche for current audience size."]

**Formula performance note:**
> [FILL — did this formula work for this topic? What would you change?]

### 8D — 7-Day Review and Learning Log

**Final metrics:**
> [FILL — full metric snapshot at 7 days]

**What worked:**
> [FILL — specific elements that drove performance]

**What to improve:**
> [FILL — specific elements to change in next reel using this formula]

**Learning logged:**
- [ ] Findings added to formula file (if formula-level insight)
- [ ] Hook variation tested (if A/B) — result recorded
- [ ] Reel logged in reel tracker with final metrics

**STAGE 8 SIGN OFF:** _____________________ Date: _________

---

## FULL WORKFLOW SUMMARY

### PATH A — HeyGen HASR (Default)
```
Stage 1 — Content Request         [content_request_template.md]
    ↓ Approved → REEL_[NNN] assigned
Stage 2 — Production Brief        [production_brief_template.md]
    ↓ Approved → Script + visual plan locked
Stage 3 — Storyboard (HASR)       [heygen_production_guide.md — storyboard section]
    ↓ Approved → Layout patterns + B-roll list ready
Stage 4 — HeyGen Avatar Video     [heygen_production_guide.md — Stage 4]
    ↓ Complete → File: REEL_[NNN]_AVATAR_v1.mp4
Stage 5 — Screen B-Roll           [heygen_production_guide.md — Stage 5]
    ↓ Complete → Files: REEL_[NNN]_SCREEN_[x]_v1.mp4
Stage 6 — Edit in CapCut          [this checklist — Stage 6 + heygen_production_guide.md Stage 6]
    ↓ Exported → File: REEL_[NNN]_FINAL_v1.mp4
Stage 7 — Publishing Package      [this checklist — Stage 7]
    ↓ Published → Reel live
Stage 8 — Post-Publish Review     [this checklist — Stage 8]
    ↓ 7-day log complete → Learning captured
```

### PATH B — Flow Generation (F03, F08 only)
```
Stage 1–3: Same as above
Stage 4 — Flow Scene Plan         [flow_generation_template.md — Stage 4]
Stage 5 — Flow Prompt Pack        [flow_generation_template.md — Stage 5]
    ↓ All clips accepted → Files: REEL_[NNN]_CLIP[N]_v[N].mp4
Stage 6–8: Same as above
```

**Flow Generation Rules (applies to both paths when Flow is used):**
- Generate ALL clips in a single Flow session — different sessions produce different characters
- Attach Character.png at session start — required for every session
- If regenerating one clip: attach Character.png + a frame from an approved clip as reference
- Full-frame clips and split-screen clips must be in the same session (Rule 25)
- Check per-clip word count against Rule 22 table before generating
- All generated clips will have a sparkle watermark in bottom-right — cover in CapCut (Rule 23)

---

**Target time from approved Content Request to published reel:**
| Formula | Path | Production Time | Notes |
|---|---|---|---|
| F07 — News Flash | HASR | 45 min | Fastest — HeyGen + 1 screen clip |
| F01 — AI Cheat Code | HASR | 60 min | |
| F04 — Hidden Tool | HASR | 60 min | |
| F10 — Comment React | HASR | 60 min | No screen clips needed |
| F05 — Career List | HASR | 90 min | Multiple screen clips to record |
| F09 — Three Step System | HASR | 90 min | 3 screen clips |
| F02 — Future Shock | HASR | 60–90 min | |
| F06 — AI vs Human | HASR | 90 min | Before/after B-roll to record |
| F03 — Hollywood VFX | Flow | 6-8 hours | AI visuals are the content |
| F08 — Mind Transformation | Flow | 6-8 hours | Before/after quality gate is highest |
