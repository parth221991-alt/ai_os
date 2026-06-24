# AI_SNIPP Character Consistency Guide

**Version:** 1.0  
**Status:** Canonical  
**Purpose:** Maintain visual character consistency across hundreds of AI-generated clips. This document is for production operators — anyone generating clips must read this before touching Flow.

---

## The Core Problem

AI video generation (Google Flow, Sora, etc.) does not have persistent memory across sessions. Each generation is stateless. Without a system, the character's face, hair, glasses, and skin tone will drift — sometimes subtly, sometimes dramatically — between clips within the same reel.

A single reel with 4 clips from different sessions can look like 4 different people. This destroys brand trust faster than any bad content decision.

This guide solves that.

---

## The Two-Layer Consistency System

### Layer 1: Structural Lock (Never Changes)
These elements must be identical in every single clip, no exceptions:

| Element | Exact Specification | Why It Cannot Change |
|---|---|---|
| **Face structure** | As per Character.png — oval face, defined jaw | The face IS the brand |
| **Curl pattern** | Tight natural coil curls, black, medium top length | Most distinctive physical feature |
| **Glasses** | Matte black rectangular frames | Single most recognizable brand marker |
| **Beard** | Short full beard, ~5–10mm, clean edges, black | Core part of character identity |
| **Skin tone** | Warm medium-brown, amber undertones | Must not lighten or darken between clips |
| **Age** | Mid-to-late 20s appearance | Must not age up or down |

### Layer 2: Flexible Elements (Can Vary)
These can change between content types and should change to keep content fresh:

| Element | Allowed Variations | Notes |
|---|---|---|
| **Clothing** | Black tee (default), dark navy, white tee, dark button-up | See Clothing Variations in character_sheet.md |
| **Expression** | Direct confident, slight smile, raised brow, serious, playful | Match content energy |
| **Hand position** | Interlocked, steepled, open gesture, relaxed | No finger-counting |
| **Body position** | Forward lean, relaxed back, slight side angle | Natural variation |
| **Camera angle** | Slightly below, eye level, slightly above | Per scene type |
| **Environment** | Dark studio, minimal, news energy, desk setup | Per content type |
| **Lighting mood** | Warm amber default, slightly cooler for news content | Keep warm key on face |

---

## Session Management Protocol

### Starting a New Production Session

**Step 1: Prepare your reference**
- Open `character/Character.png` — this is your ground truth
- Have it ready to attach to every Flow prompt

**Step 2: Generate a test clip first**
- Before generating any content clip, generate a 3-second test clip using only the Master Seed Block + Dark Studio Environment
- Compare output against Character.png
- If face/hair/glasses match → proceed
- If anything is off → correct before generating any production content

**Step 3: Lock your session**
- Once you have a passing test frame, note any additional phrases that helped achieve the correct output
- Add those to your session notes
- Use the same exact prompt structure for all clips in this session

**Step 4: Document passing prompts**
- When a prompt generates a clip that passes the 5-point consistency check → save it in `06_prompts/flow/` with the date
- This becomes your reference for next session

---

## Consistency Across Multi-Clip Reels

A single reel has 3–5 clips (each 8 seconds). All must look like the same person.

### Method 1: Single-Session Generation (Preferred)
Generate all clips for one reel in the same Flow session. The model's internal context tends to maintain better consistency within a session.

**Workflow:**
1. Generate Clip 1 (hook scene)
2. Verify it passes consistency check
3. Generate Clip 2 using the same base prompt, adding "CONTINUATION: This is a direct continuation of the previous clip. The character is identical. Same face, same hair, same glasses, same environment. Only the action and script change."
4. Repeat for all clips
5. Review all clips side by side before merging

### Method 2: Cross-Session Generation (When Necessary)
When clips are generated across multiple sessions (different days, different tools):

**Protocol:**
- Use the same Character.png reference image
- Use identical Master Seed Block text
- After generating, compare frame grabs side by side
- If character looks different in Clip 3 vs Clip 1, regenerate Clip 3 with an explicit note: "STRICT MATCH REQUIRED: The character in this clip must be pixel-consistent with the attached reference frame from Clip 1. Same person, same features, same lighting. Do not introduce any variation in face structure, hair texture, or glasses."

---

## The 5-Point Consistency Check

Run this check on every generated clip before approving it:

```
CONSISTENCY CHECKLIST — Run on every clip

□ 1. HAIR: Tight coil curls preserved? 
      ✓ Coils are defined and dense
      ✗ Fail if: wavy, straight, loose curls, different length, different color

□ 2. GLASSES: Matte black rectangular frames intact?
      ✓ Black frame, rectangular shape, clear lenses
      ✗ Fail if: wire frames, round shape, different color, removed

□ 3. SKIN TONE: Warm medium-brown maintained?
      ✓ Brown with amber undertones, same as reference
      ✗ Fail if: noticeably lighter or darker than reference image

□ 4. BEARD: Short, clean, full coverage?
      ✓ Covers jaw/chin cleanly, trimmed edges, black
      ✗ Fail if: no beard, much longer, patchy, different color

□ 5. FACE STRUCTURE: Same person?
      ✓ Recognizable as the same individual across clips
      ✗ Fail if: face shape changed, different nose/eyes/jaw structure

PASS THRESHOLD: All 5 must pass. 4/5 may be acceptable if the failure is minor
and can be hidden by editing (e.g., slight lighting variation on skin tone when 
facecam is small). 3/5 or below = regenerate.
```

---

## Common Failure Modes and Fixes

### Failure Mode 1: Hair Goes Wavy
**Symptom:** Generated character has loose waves instead of tight coil curls  
**Why it happens:** AI models default to common hair patterns; tight natural coils are underrepresented  
**Fix prompt addition:**
```
HAIR CORRECTION: The character's hair texture is specifically tight natural coil curls — 
the hair forms small defined coil rings, not waves. The curl pattern is kinky-curly, 
African-textured coil pattern. Dense. The curls are compressed — they bounce up from 
the scalp in tight springs. Reference image attached. Do not generate waves or loose curls.
```

### Failure Mode 2: Glasses Disappear or Change
**Symptom:** Character appears without glasses, or with different frame style  
**Why it happens:** Action-heavy prompts cause model to drop accessory details  
**Fix prompt addition:**
```
GLASSES CRITICAL: The character MUST wear matte black rectangular glasses in this clip. 
This is non-negotiable. The glasses have thick black plastic frames with a rectangular lens 
shape. They are a defining brand element. Generate with glasses always present, 
in correct position on face.
```

### Failure Mode 3: Skin Tone Shifts Light
**Symptom:** Character appears significantly lighter than in Character.png  
**Why it happens:** High-key lighting prompts can cause model to lighten skin  
**Fix prompt addition:**
```
SKIN TONE ANCHOR: Maintain the character's skin tone as warm medium-brown 
with amber undertones — approximately the skin tone visible in the attached 
reference image. Do not lighten the skin despite any changes in lighting direction.
```

### Failure Mode 4: Face Structure Drifts
**Symptom:** The character looks like a different person — same hair/glasses but different face  
**Why it happens:** Reference image influence weakens across long prompts  
**Fix:** Shorten the prompt. Place the reference image anchor description in the first 50 words. Then use: "Refer to attached image for exact face structure. All other descriptions are supplementary — the attached image is the primary visual reference."

### Failure Mode 5: Beard Grows or Disappears
**Symptom:** Character has full long beard, or no beard  
**Fix prompt addition:**
```
BEARD: Short, well-maintained full beard. Approximately 5-10mm in length. 
Clean trimmed edges at neck and cheeks. Full coverage from jaw to upper lip. 
Black. Not long, not stubble — short beard.
```

### Failure Mode 6: Character Looks Too Old or Too Young
**Symptom:** Generated character appears noticeably older or younger  
**Fix:**
```
AGE: The character appears to be in his mid-to-late twenties — approximately 26–29 years old. 
Not a teenager, not a 40-year-old. Young professional, post-college, early career.
```

---

## Clip-to-Clip Transition Consistency

When writing the prompt for Clip 2, 3, 4 in a reel, always include:

```
CONTINUITY NOTE: This is Clip [N] in a series. The character is the same individual 
as in previous clips. DO NOT change the character's appearance. 
All identity elements are locked: same face, same tight coil curls, same matte black 
rectangular glasses, same beard, same skin tone. Only the action, script, and 
[any approved variation] changes in this clip.
```

---

## What NEVER Changes — The Non-Negotiables

This list is the brand's survival rules. Breaking any of these is a brand failure:

1. **Glasses are always on.** Even in casual content, even in dynamic scenes. They are never removed. They do not change shape or color.
2. **Curl texture is always natural coils.** Never blown out, never straightened, never a different curl pattern.
3. **The face is always the same person.** If you generated a clip and the face looks different from Character.png, do not use it.
4. **The character is always Indian.** Skin tone, features, and appearance must reflect South Asian / Indian origin.
5. **The format is always 9:16.** No horizontal clips in the final output.
6. **The character is always male.** Always the same age range.
7. **The character does not age.** Even across months of content, the character remains the same age appearance.

---

## Quality Gates Before Final Merge

Before merging clips into a final reel:

1. Play all clips in sequence. Does it look like the same person throughout? If no → find the outlier clip → regenerate.
2. Check skin tone consistency across clips — lighting variations can make it look different.
3. Check glasses — did any clip generate without glasses?
4. Check hair — did any clip generate with a different hair pattern?
5. Color-grade after merge to even out any remaining variation.

---

## Archiving Passing Prompts

When a prompt generates a clip that passes all 5 checks:

1. Save the exact prompt text to `06_prompts/flow/passing/YYYY-MM-DD_scene-type.md`
2. Note any additional phrases you added that helped
3. Next session: start from a passing prompt rather than building from scratch

Over time, your library of passing prompts becomes the single most valuable asset in the system. It encodes what actually works with the current generation model, which changes faster than any documentation.
