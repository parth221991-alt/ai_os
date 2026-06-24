# Storyboard Template
## AI_SNIPP Production System — Stage 3 of 8

*One storyboard block per clip. Completed once Production Brief (Stage 2) is approved.*
*Reference files: prompt_blocks.md, visual_identity.md, character_sheet.md*
*Each storyboard block becomes the direct input to the Flow Generation Template (Stage 4).*

---

## STORYBOARD HEADER

| Field | Value |
|---|---|
| Reel ID | REEL_[NNN] |
| Production Brief | Approved ✓ |
| Formula | F[NN] — [Formula Name] |
| Total Clips | [N] |
| Total Target Duration | [XX]s |
| Storyboard Version | v1 |
| Last Updated | YYYY-MM-DD |

---

## CLIP STORYBOARD BLOCKS

---

### CLIP 1 — [SCENE NAME IN CAPS]

**Block Type:** Block [N] — [Block Name from prompt_blocks.md]  
**Duration:** [X]s

| Field | Specification |
|---|---|
| Script Line | "[FILL — exact words creator speaks in this clip]" |
| Shot Type | [MCU — Medium Close-Up / CU — Close-Up / Wide] |
| Camera Angle | [Slightly below eye level / Eye level / Slightly above eye level] |
| Camera Movement | [Slow push-in / Subtle zoom-in 2-3% / Static lock] |
| Creator Presence | [Full screen / Facecam overlay bottom-right 25-28% / Absent] |
| Environment | [A — Dark Studio / B — Minimal / C — News Room / D — Desk] |
| Acting Direction | [SARCASTIC ROAST / URGENCY / INSIDER SECRET / SHOCK VALUE / PEER-TO-PEER / WARM CTA] |
| Key Visual Element | [What viewer sees beyond the creator — UI, overlay, background element] |
| Overlay Text | [On-screen text: tool name, statistic, step number, or "none"] |
| Overlay Position | [Top-left / Bottom-left / Center / Lower-third / "none"] |
| Transition Out | [Hard cut / Whoosh + cut / Fade] |

**Frame Layout (9:16 vertical):**
```
┌─────────────────────┐
│                     │
│                     │
│   [describe what    │
│    fills the frame] │
│                     │
│   [creator pos]     │
│   [overlay pos]     │
│                     │
│                     │
└─────────────────────┘
```

**Acting Notes:**
> [Specific body language, gesture, facial expression, energy cue. Reference character_sheet.md gesture rules — no finger-counting, no pointing at lens.]

**Production Notes:**
> [Any edge cases, alternatives, assets needed, failure risk]

---

### CLIP 2 — [SCENE NAME IN CAPS]

**Block Type:** Block [N] — [Block Name]  
**Duration:** [X]s

| Field | Specification |
|---|---|
| Script Line | "[FILL]" |
| Shot Type | |
| Camera Angle | |
| Camera Movement | |
| Creator Presence | |
| Environment | |
| Acting Direction | |
| Key Visual Element | |
| Overlay Text | |
| Overlay Position | |
| Transition Out | |

**Frame Layout (9:16 vertical):**
```
┌─────────────────────┐
│                     │
│  [main content      │
│   area if facecam]  │
│                     │
│                     │
│             ┌─────┐ │
│             │ cam │ │
│             └─────┘ │
└─────────────────────┘
```
*For facecam overlay: creator occupies bottom-right 25-28% in rounded rectangle with warm amber border glow.*

**Acting Notes:**
> 

**Production Notes:**
> 

---

### CLIP 3 — [SCENE NAME IN CAPS]

**Block Type:** Block [N] — [Block Name]  
**Duration:** [X]s

| Field | Specification |
|---|---|
| Script Line | "[FILL]" |
| Shot Type | |
| Camera Angle | |
| Camera Movement | |
| Creator Presence | |
| Environment | |
| Acting Direction | |
| Key Visual Element | |
| Overlay Text | |
| Overlay Position | |
| Transition Out | |

**Frame Layout (9:16 vertical):**
```
┌─────────────────────┐
│                     │
│                     │
│                     │
│                     │
│                     │
└─────────────────────┘
```

**Acting Notes:**
> 

**Production Notes:**
> 

---

### CLIP 4 — CTA CLOSE

**Block Type:** Block 5 — CTA SCENE  
**Duration:** [X]s (target 5–8s)

*CTA clip is always the final clip. Always Block 5. Never vary the block type.*

| Field | Specification |
|---|---|
| Script Line | "[FILL — exact CTA words]" |
| Shot Type | MCU — chest to head |
| Camera Angle | Eye level — peer-to-peer (NOT slightly below — that is the hook angle) |
| Camera Movement | Static lock |
| Creator Presence | Full screen |
| Environment | A — Dark Premium Studio |
| Acting Direction | WARM CTA — warm, direct, genuine. Shoulders relaxed. Inviting, not selling. |
| Key Visual Element | @ai_snipp watermark, end card text |
| Overlay Text | "@ai_snipp" bottom-right watermark + end card: "AI Tools • AI Certifications • AI Updates • AI Cheat Codes" |
| Overlay Position | Watermark: lower-right / End card: lower-third |
| Transition Out | Fade to black |

**Frame Layout (9:16 vertical):**
```
┌─────────────────────┐
│                     │
│                     │
│  [Creator — eye     │
│   level, centered,  │
│   MCU, warm look]   │
│                     │
│  [End card text     │
│   lower-third]      │
│          [@ai_snipp]│
└─────────────────────┘
```

**Acting Notes:**
> Eye level is non-negotiable for CTA — creates peer warmth, different energy from hook's authority angle. Shoulders down. Natural breathing. Direct gaze with slight warmth at corners of eyes. No urgency. No tension.

**Production Notes:**
> CTA clip does not carry forward any tension from earlier clips. It is a reset. One action, one line, warm delivery.

---

## CONTINUITY NOTES

**Character consistency plan across all [N] clips:**
> [Note wardrobe, expression arc, or camera angle changes that must be managed clip to clip. e.g., "Clips 1-3 use slightly below eye level (authority). Clip 4 resets to eye level (warmth). This is intentional — note in prompt as acting contrast."]

**Environment consistency:**
> [Note if environment changes across clips and why. e.g., "All clips use Environment A. No change." OR "Clip 2 switches to Environment D for tool demo clarity."]

**Clip-to-clip transition plan:**

| Exit Clip | Transition Type | Enter Clip |
|---|---|---|
| Clip 1 | [Hard cut / Whoosh + cut] | Clip 2 |
| Clip 2 | [Hard cut / Whoosh + cut] | Clip 3 |
| Clip 3 | [Hard cut / Whoosh + cut] | Clip 4 |

**Pattern interrupt cadence:**
> [One pattern interrupt per 1.5–2s of screen time. List where cuts, zoom pops, text reveals, or SFX land within each clip to maintain this cadence.]

---

## ASSET CHECKLIST

Assets required before Flow Generation begins:

- [ ] Character.png — verified and accessible
- [ ] UI screenshots / dashboards — [list if needed]
- [ ] Before/after materials — [list if F08]
- [ ] Comment card asset — [if F10]
- [ ] News ticker graphic — [if F07 cold open]
- [ ] Prompt text prepared for on-screen display — [if F01/F08/F09]

---

## QUALITY STANDARDS

Before passing to Flow Generation:

- Every clip has a Block Type assigned from prompt_blocks.md
- Every clip has an acting direction (not just "be natural")
- Every clip has an overlay specification (even if "none")
- Clip durations sum to target ± 2s
- CTA clip (Block 5) is always last
- Camera angle for CTA is eye level (not the hook's slightly-below)
- Creator is absent in Clips 1-2 ONLY for F03/F08 formulas
- No finger-counting or pointing-at-lens in acting notes

---

## APPROVAL CHECKLIST

- [ ] All [N] clips storyboarded — no blank blocks
- [ ] Frame sketches show creator position and overlay position for each clip
- [ ] Acting direction is specific for each clip
- [ ] Transitions defined for every clip pair
- [ ] Continuity notes explain any cross-clip changes
- [ ] Asset checklist complete
- [ ] Storyboard reviewed against Production Brief script — all script lines allocated

**SIGN OFF:** _____________________ Date: _________

---

*On approval → Flow Generation Template (Stage 4)*
