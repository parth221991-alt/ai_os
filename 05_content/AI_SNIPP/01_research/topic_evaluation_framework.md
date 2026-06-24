# Topic Evaluation Framework
## AI_SNIPP Research & Intelligence System

*This framework answers one question: does this topic deserve a reel? It is a gate, not a guide. Ideas that pass all gates move into production. Ideas that fail any hard gate are rejected — no exceptions, no "but this one might work." The Indian AI audience is sharp. One low-quality reel costs more in trust than it gains in reach.*

---

## THE EVALUATION SEQUENCE

```
TOPIC IDEA
    ↓
HARD GATES (all must pass — any fail = immediate reject)
    ↓
FORMULA FIT CHECK (maps to exactly one formula)
    ↓
AUDIENCE SIGNAL CHECK (pain is real, not invented)
    ↓
TIMING GATE (formula-specific freshness requirements)
    ↓
PRODUCTION FEASIBILITY CHECK (can produce without bottleneck)
    ↓
SOFT SCORING (1–25 — determines priority tier)
    ↓
DECISION + ASSIGNMENT
```

---

## STAGE 1 — HARD GATES

*Six gates. Any single failure = immediate reject. No exceptions. No "this is close enough." Document why each idea fails so the pattern of rejection informs future idea generation.*

---

### GATE 1 — GENUINE VALUE GATE

**Question:** Can a viewer execute on this information without following up with the creator?

**Pass criteria:** The core value claim is specific enough that a viewer who screenshots the script (without watching the reel or DMing the creator) gains real, actionable value.

**Fail criteria:**
- The value claim is: "AI is important" / "You should learn AI" / "Here's why AI matters"
- The insight requires a paid resource the viewer doesn't have access to
- The value only exists if the viewer DMs or follows (teaser without value)

**Test:** Imagine a viewer watches the reel but doesn't follow, save, or DM. Did they still get something useful? If no → FAIL.

**Common failure example:** "Here are 10 AI tools [teaser] — DM me for the list." The reel itself has no value; the DM is the only value. The correct approach: share 3 real tools in the reel, then DM for the extended 20+ tool list.

---

### GATE 2 — SPECIFICITY GATE

**Question:** Is the core claim specific enough to be verifiable?

**Pass criteria:** The claim can be independently tested by the viewer or traced to a citable source.

**Fail criteria:**
- "AI saves time" (how much time? for what task? with what tool?)
- "This tool is amazing" (what specifically does it do? better than what alternative?)
- "AI is replacing jobs" (which jobs? which companies? in what timeframe?)

**Test:** Add "specifically" to the claim. Does the sentence still hold? "AI saves time specifically by reducing cold email research from 20 minutes to 3 minutes using Claude's web search." → PASS. "AI saves time specifically" → not a complete thought → FAIL.

---

### GATE 3 — PERSONAL PROOF GATE

**Question:** Has the creator personally tested, verified, or experienced the claim being made?

**Pass criteria:** The creator can say "main ne personally test kiya hai" and mean it.

**Fail criteria:**
- Reposting a claim from another creator without independent verification
- Sharing a tool without having used it
- Citing a statistic from a secondary source without verifying the primary source
- Showing a "transformation" that was prepared by someone else
- Promising a workflow that the creator hasn't personally run end-to-end

**Test:** Could the creator be asked "show me your test" and produce evidence? If no → FAIL.

**Why this matters for @ai_snipp specifically:** The Indian AI audience (developers, students, professionals) will test claims. One viral reel with a bad claim produces 100 negative comments that erode months of credibility. The channel's authority is built on "creator tested this for you" — violate this and the brand loses its primary differentiator.

---

### GATE 4 — NOVELTY GATE

**Question:** Is this topic new enough — relative to what @ai_snipp and direct competitors have already covered?

**Pass criteria:**
- @ai_snipp has not covered this specific topic in the last 14 days
- The angle being used is not identical to a major competitor's recent viral coverage
- If the topic was covered before, a meaningfully different angle is being used

**Fail criteria:**
- Exact same topic covered by @ai_snipp in last 14 days
- Topic just went viral on a major competitor's account (within 3 days) with a thorough treatment
- Same information packaged identically — no new angle, no deeper insight

**Exception:** News content (F07) can be repeated if the situation develops (e.g., coverage of GPT-5 release → 48 hours later → coverage of Indian developer response to GPT-5 pricing).

---

### GATE 5 — FORMAT GATE

**Question:** Can this topic be delivered compellingly in under 35 seconds?

**Pass criteria:** The core value (Hook + Agitate + Insight + Proof + CTA) can be scripted to ≤35 seconds at fast Hinglish pace.

**Fail criteria:**
- The topic genuinely requires 90+ seconds to explain correctly (use Carousel format instead)
- The topic is a nuanced debate that can't be resolved in a Reel (use Carousel)
- The proof requires extended screen recording that breaks the 35-second format

**If fails:** The topic may still be worth producing — as a Carousel (2–10 slides) or Static (quick tip format). Redirect to appropriate format, don't discard the topic.

---

### GATE 6 — BRAND SAFETY GATE

**Question:** Does this content maintain @ai_snipp's brand standards and trust?

**Pass criteria:** Content is factually accurate, doesn't make claims the creator can't defend, and doesn't create legal or reputational risk.

**Fail criteria:**
- False comparison claims (e.g., "Claude is 10× better than ChatGPT" without benchmarkable proof)
- Tool promotion without disclosure if paid (affiliate/paid partnership must be labeled)
- Confidential or unreleased features shared without authorization
- News presented as fact that is actually unverified rumor
- Content that could embarrass the creator if screenshot out of context

---

### Hard Gate Summary Checklist

```
HARD GATE EVALUATION — [Topic Title]

GATE 1 — Genuine Value:
  Viewer gains value without DM/follow/save? [ ] Yes  [ ] No → REJECT
  Fail reason: [FILL if fails]

GATE 2 — Specificity:
  Claim is verifiable/traceable? [ ] Yes  [ ] No → REJECT
  Fail reason: [FILL if fails]

GATE 3 — Personal Proof:
  Creator personally tested this? [ ] Yes  [ ] No → REJECT
  Fail reason: [FILL if fails]

GATE 4 — Novelty:
  Not covered in last 14 days, not identical to competitor's viral content? [ ] Yes  [ ] No → REJECT
  Fail reason: [FILL if fails]

GATE 5 — Format:
  Can be delivered in ≤35 seconds? [ ] Yes  [ ] No → [Redirect to Carousel/Static]
  Alternative format: [FILL if redirected]

GATE 6 — Brand Safety:
  No false claims, no disclosure issues, no reputational risk? [ ] Yes  [ ] No → REJECT
  Fail reason: [FILL if fails]

RESULT:
[ ] ALL 6 PASS → proceed to Stage 2
[ ] ANY FAIL → REJECT (document reason below)
Rejection reason: [FILL]
```

---

## STAGE 2 — FORMULA FIT CHECK

*Assign exactly one formula. Use the decision tree. If two formulas seem equally valid, the topic may be underspecified — sharpen the angle until one formula wins clearly.*

```
FORMULA ASSIGNMENT

Best fit formula: F[NN] — [Formula Name]
Why this formula over alternatives: [one sentence]
Backup formula (if primary can't be executed): F[NN] — [Formula Name]

Formula's minimum quality gate (from formula_index.md):
[PASTE the relevant quality gate for this formula]

Does this topic meet that quality gate? [ ] Yes  [ ] No → REJECT (don't force formula)
```

**Hard stop:** If no formula cleanly fits, and the backup also doesn't fit, this topic is not ready. Either the topic needs reframing or the asset needed for the formula doesn't exist yet.

---

## STAGE 3 — AUDIENCE SIGNAL CHECK

*The topic must be grounded in real audience pain — not creator assumption.*

```
AUDIENCE SIGNAL VALIDATION

Pain point source:
[ ] Real comment observed this week — exact quote: "[FILL]" — Source: @[handle]/r/[subreddit]
[ ] Documented APIFY research pattern — reference: [phase and finding]
[ ] Personal DM from viewer — topic: [topic]
[ ] Multiple competitor comment requests: "[examples]"
[ ] Observed from trend monitoring: [source]
[ ] Creator assumption only — NO SOURCE ← FLAG: score D1=1 in content_ideas_database.md

Signal strength:
[ ] Strong — 5+ instances in real comments this week (D1 = 5)
[ ] Moderate — recurring theme in research data (D1 = 3-4)
[ ] Weak — single instance or inferred (D1 = 1-2)

If weak signal: Is there a specific angle or hook that makes the topic worth producing despite weak signal?
[FILL or write "No — evaluate D1 penalty in scoring"]
```

---

## STAGE 4 — TIMING GATE

*Formula-specific freshness requirements. These are non-negotiable.*

```
TIMING GATE EVALUATION

Formula: F[NN]

For F07 (News Flash):
  Age of news: [X] hours
  [ ] Under 24 hours → FAST TRACK — produce today
  [ ] 24–48 hours → produce this week
  [ ] Over 48 hours without acknowledgment → REJECT (stale) or reframe as evergreen with disclosure
  Reframe option: "In case you missed it — [topic] — yeh matter karta hai kyunki..."

For F02 (Future Shock):
  F02 count in current week: [N]
  [ ] 0 in current week → OK to use
  [ ] 1 in current week → review carefully — is this more urgent than last F02?
  [ ] 2+ in current week → DEFER to next week — fear fatigue risk

For F03 (Hollywood VFX):
  AI-generated output exists and has been reviewed? [ ] Yes  [ ] No → DEFER
  Output quality assessment: [ ] Genuinely impressive (proceed)  [ ] Average (REJECT — wrong formula)

For F04 (Hidden Tool):
  Tool personally tested? [ ] Yes  [ ] No → DEFER until tested
  Indian accessibility verified? [ ] Yes  [ ] No → verify before scheduling

For all other formulas (F01, F05, F06, F08, F09, F10):
  No timing gate → proceed to Stage 5
```

---

## STAGE 5 — PRODUCTION FEASIBILITY CHECK

*Before committing to production, verify that required assets exist or can be created within production timeline.*

```
PRODUCTION FEASIBILITY

Required assets (check all that apply):
[ ] Claude.ai / tool access — do I have it? [ ] Yes  [ ] No — acquire before starting
[ ] Screenshot / UI visual — prepared? [ ] Yes  [ ] No — create before Flow session
[ ] Before/after material (F08) — ready? [ ] Yes  [ ] No — what's needed: [FILL]
[ ] Real viewer comment card (F10) — screenshot ready? [ ] Yes  [ ] No
[ ] Comparison materials (F06) — both sides tested? [ ] Yes  [ ] No
[ ] News source / citation ready (F07) — link confirmed? [ ] Yes  [ ] No

Character.png — accessible for Flow session? [ ] Yes  [ ] No — locate before starting

Estimated production time (from formula_index.md): [X] minutes
Is a full production block available this week? [ ] Yes  [ ] No → defer to when block available

Any blockers?
[ ] None — ready to produce
[ ] Blocker: [FILL] — estimated resolution: [FILL]
```

---

## STAGE 6 — SOFT SCORING

*Five soft dimensions. Total determines urgency tier within the P1/P2/P3 classification from content_ideas_database.md.*

| Dimension | Score (1–5) |
|---|---|
| Audience pain intensity | |
| Freshness / timing | |
| Indian relevance | |
| CTA clarity | |
| Viral potential | |
| **TOTAL** | **/25** |

**CTA clarity (1–5):**
| Score | Criteria |
|---|---|
| 5 | CTA is obvious — one action, one trigger word, delivers exactly what the reel promised |
| 4 | CTA is clear — one action, minor ambiguity |
| 3 | CTA needs refinement — two possible actions exist, need to choose |
| 2 | CTA is unclear — no obvious deliverable or next step |
| 1 | No CTA identified — reel has no conversion mechanism |

**Viral potential (1–5):**
| Score | Criteria |
|---|---|
| 5 | Has "pass it on" quality — viewer will share to a friend who is experiencing this exact problem |
| 4 | High saves potential — content is reference material viewers will return to |
| 3 | Good engagement potential — comments and likes, modest share/save |
| 2 | Niche appeal — valuable to small segment, limited amplification |
| 1 | Creator-interest content — interesting to creator, low resonance for broad audience |

**Soft Score Priority:**
| Score | Within-Tier Action |
|---|---|
| 22–25 | Top of queue within tier — produce first |
| 16–21 | Standard queue — produce in order |
| Below 16 | Bottom of queue — produce when higher-scoring content is depleted |

---

## STAGE 7 — DECISION + ASSIGNMENT

```
FINAL DECISION

Hard Gate Result: [ ] All pass  [ ] Rejected (reason: [FILL])
Formula Assignment: F[NN] — [Name]
Audience Signal Strength: [ ] Strong  [ ] Moderate  [ ] Weak
Timing Gate: [ ] Clear  [ ] Gated — condition: [FILL]
Production Feasibility: [ ] Clear  [ ] Blocked — resolution: [FILL]
Soft Score: [N/25]

DECISION:
[ ] PRODUCE IMMEDIATELY (news, P0 condition)
[ ] PRODUCE THIS WEEK (P1 — score 22–30 combined)
[ ] QUEUE NEXT WEEK (P2 — score 16–21 combined)
[ ] DEFERRED — waiting on: [FILL]
[ ] REJECTED — reason: [FILL]

If proceeding:
  Content Request ID: CR_[NNN]
  Production start date: YYYY-MM-DD
  Production brief due: YYYY-MM-DD
  Target post date: YYYY-MM-DD
```

---

## FORMULA-SPECIFIC EVALUATION CHECKLISTS

*Quick reference — the minimum verifiable conditions required before assigning each formula.*

**F01 — AI Cheat Code:**
- [ ] The shortcut is specific (not general advice)
- [ ] Creator has personally tested it
- [ ] It works on a tool Indian audience already uses
- [ ] The time/effort saving is demonstrable on-screen
- [ ] DM deliverable is ready (template, link, or list)

**F02 — Future Shock:**
- [ ] Urgency is based on a real, citable trend (not manufactured)
- [ ] Indian career relevance is direct, not forced
- [ ] Action path is included (not just fear)
- [ ] This is the only F02 this week

**F03 — Hollywood VFX:**
- [ ] AI-generated output exists and has been viewed
- [ ] Output quality assessment: genuinely impressive? If no → reject
- [ ] Prompt is documented and ready to share
- [ ] DM deliverable is the prompt itself

**F04 — Hidden Tool:**
- [ ] Tool is under 6 months of Indian awareness (verified)
- [ ] Creator has used it personally
- [ ] Free tier or Indian-accessible pricing exists
- [ ] DM trigger word and deliverable list are ready

**F05 — Career List:**
- [ ] Every resource on the list has been personally reviewed
- [ ] Minimum 3, maximum 5 resources
- [ ] Each resource has a verifiable benefit claim
- [ ] Save karo mandatory line is in caption plan

**F06 — AI vs Human:**
- [ ] Both sides (manual + AI) have been personally timed/tested
- [ ] Numbers are real — not estimated
- [ ] The quality of AI output is genuinely acceptable (not just faster)
- [ ] Save + prompt as CTA is planned

**F07 — News Flash:**
- [ ] News is under 48 hours old (or delay is disclosed)
- [ ] Indian relevance angle is specific and non-forced
- [ ] Creator understands the news well enough to explain it incorrectly-free
- [ ] Source is citeable

**F08 — Mind Blowing Transformation:**
- [ ] Before state is genuinely bad (not mildly suboptimal)
- [ ] After state is genuinely impressive (not just better)
- [ ] Both before and after were created by the creator in this session
- [ ] Exact prompt is documented

**F09 — Three Step System:**
- [ ] System has been personally run end-to-end
- [ ] Result is reproducible by any viewer
- [ ] Each step is clear enough to execute without additional explanation
- [ ] Save karo mandatory line is in caption plan

**F10 — Comment React:**
- [ ] The comment is real (screenshot exists)
- [ ] The commenter represents a common question (not a fringe edge case)
- [ ] Answer is completable in 30 seconds
- [ ] Creator has a definitive, helpful answer (not opinion)
