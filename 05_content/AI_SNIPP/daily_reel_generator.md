# AI_SNIPP — Daily Reel Generator

**Status:** Canonical — runs on top of Production Mode  
**Purpose:** One command, one complete reel package. Handles research, topic selection, and full production in a single execution. No decisions pushed back to the user.  
**Engine:** Calls `production_mode.md` for execution after topic and formula are resolved.  
**Location:** `D:\AI_OS\05_content\AI_SNIPP\daily_reel_generator.md`

---

## COMMAND SYNTAX

```
/create-reel
```
Full auto. No topic, no formula. Claude reviews available context, selects the best opportunity, applies the best formula, generates the complete package.

```
/create-reel [topic]
```
Topic provided. Claude auto-selects the best formula and generates. Topic can be a sentence, a keyword, or a concept.

```
/create-reel [formula]
```
Formula provided (e.g., `F06`, `F01`, `F09`). Claude selects the best topic for that formula and generates.

```
/create-reel [topic] [formula]
```
Both provided. Claude skips all selection logic and goes directly to production. Fastest path.

```
/create-reel [topic] [formula] CTA=[WORD]
```
Maximum specification. Topic, formula, and DM trigger word provided. No decisions required from Claude. Pure production.

```
/create-reel [article URL]
/create-reel [pasted article text]
```
Article or URL provided → fetch/read the source → extract topic → fact-verify all key claims → auto-select formula based on content type → produce reel. This is the P-1 (highest priority) input path. All claims in the article are verified before they enter the script — user providing the article does not bypass fact-checking.

---

**Examples:**

| Command | What Happens |
|---|---|
| `/create-reel` | Full auto — social research → select trending topic → produce |
| `/create-reel ChatGPT vs Claude for writing tasks` | Topic locked, formula auto-selected (likely F06) |
| `/create-reel F01` | Formula locked, best F01 evergreen topic selected |
| `/create-reel Claude memory feature F01` | Both locked, straight to production |
| `/create-reel Claude Projects F01 CTA=SYSTEM` | Fully specified, immediate production |
| `/create-reel https://techcrunch.com/...` | Article fetched, claims verified, reel produced from verified content |
| `/create-reel [pasted article text]` | Article parsed, claims verified, reel produced |

---

## DAILY WORKFLOW

```
/create-reel command received
          ↓
    PARSE INPUTS
    ├── Article/URL provided?  ──→ YES: fetch + fact-verify → lock topic at P-1 (highest priority)
    ├── Topic provided?        ──→ YES: lock topic, go to FORMULA SELECTION
    ├── Formula provided?      ──→ YES: lock formula, go to TOPIC SELECTION (if needed)
    └── Both provided?         ──→ YES: go directly to GATE CHECK
          ↓
    CONTEXT SCAN (silent — two parallel steps)
    Step 1 — Conversation scan:
    ├── Article/URL pasted? → P-1 candidate (highest — fact-verify before locking)
    ├── reel-analyzer teardown present? → use as Research Phase input (skip internal research step for this topic)
    ├── content-repurposer batch present? → 5 concepts treated as P1 candidates (rank 1 concept selected first)
    ├── --hook "[line]" provided via /create-reel? → hook locked, skip BEAT 1 generation
    ├── Breaking AI news mentioned? → P0 candidate
    ├── Queued ideas mentioned? → P1 candidates
    └── Trend data mentioned? → P2 candidates

    Step 2 — Social Research (runs when no topic is locked, uses WebSearch):
    Search each platform for AI trending content from the last 24-48 hours:
    ├── Twitter/X: top AI posts, trending AI tool names, viral threads
    ├── Reddit: r/artificial + r/MachineLearning + r/ChatGPT + r/AItools — top posts last 48h
    ├── YouTube: trending AI videos — title + view velocity signal
    ├── LinkedIn: high-engagement AI posts targeting Indian tech professionals
    └── Product Hunt: new AI tool launches this week — upvote count
    Score each discovered topic: Freshness + Indian Relevance + Audience Pain + Competition Gap + Proof Availability
    Any topic scoring 18+ with <3 competing creator reels in last 3 days → Social Trending candidate (P0 level)
          ↓
    REGISTRY CONSULTATION (reads reel_registry.md — not reported)
    ├── Last 30 entries → topic exclusion list (Evergreen ID + keywords)
    ├── Last 5 entries → formula frequency map (block if formula appears 2× in last 5)
    ├── Last 7 entries → pillar frequency map (block if pillar appears 4× in last 7)
    └── Blocked topics, formulas, and pillars removed before selection begins
          ↓
    TOPIC SELECTION (if needed)
    Apply rules in priority order → one topic selected (registry-filtered)
          ↓
    INTENT CLASSIFICATION (silent — determines research strategy)
    Classify topic as one of:
    Discovery Tool / Workflow Tool / News / Transformation / Comparison / Experiment
    → Adapts research focus before any information is gathered
          ↓
    RESEARCH PHASE (silent — mandatory — applies to every topic, provided or selected)
    ├── Apply Outcome-First principle: "What result would make a viewer immediately try this?"
    ├── Adapt research focus to intent type:
    │     Discovery Tool → shortcuts, ready-made assets, instant wins — not walkthroughs
    │     Workflow Tool  → non-obvious systems, hidden features — not feature lists
    │     News           → Indian relevance, immediate viewer impact — not press release
    │     Transformation → proof quality, gap size — not creation steps
    │     Comparison     → decisive winner, surprising result — not balanced review
    │     Experiment     → unexpected outcome, replication difficulty — not methodology
    ├── Search for current information on the topic
    ├── Identify: key features, recent developments, common misconceptions,
    │   surprising facts, hidden capabilities, practical use cases
    ├── Identify what most creators are NOT covering on this topic
    └── Generate at least 10 candidate angles before selecting:
        (1) Obvious — the expected take most creators publish
        (2) Contrarian — challenges the common narrative with evidence
        (3) Hidden Feature — underused or unknown capabilities
        (4) Workflow — practical, repeatable system
        (5) Future Impact — what this means 6–12 months from now
        (6) Shortcut — fastest path to the result, skips steps most people don't know are skippable
        (7) Mistake — the common error most people make, with the correction
        (8) Comparison — head-to-head, ends with a decisive winner
        (9) Experiment — unexpected outcome from trying something
        (10) Transformation — same input, dramatically different output
          ↓
    TOPIC VALIDATION (silent — 5 questions)
    ├── Is this topic still relevant and timely?
    ├── Has this exact angle been covered by competitors recently?
    ├── Is there a stronger angle available from the 10 candidates?
    ├── Is there sufficient proof — verifiable, demonstrable on screen?
    └── Can this become a compelling reel in ≤35 seconds?
    Any NO → reject topic → return to TOPIC SELECTION (next available candidate)
          ↓
    ANGLE SELECTION (silent)
    Primary question: "Which angle makes a viewer immediately want to try this?"
    Select highest-scoring angle from 10 candidates.
    Prefer: outcomes a viewer can replicate now, shortcuts, transformations, surprising results,
            mistakes with corrections, hidden workflows, strong opinions with evidence.
    Avoid: "Top N features" / "Best AI tool" / "New update" framing / tutorial walkthroughs
           when a shortcut or outcome angle exists.
    Tiebreaker: select the angle where a viewer could reproduce the result in the next 30 minutes.
    Selected angle becomes the lens for formula selection and hook direction.
          ↓
    FORMULA SELECTION (if needed)
    Apply decision tree → one formula selected
          ↓
    GATE CHECK (internal — not reported unless failure)
    All six hard gates from topic_evaluation_framework.md
    Any failure → REJECTION NOTICE → stop
          ↓
    PRODUCTION (Production Mode engine)
    All 8 sections generated in sequence
          ↓
    SELF-QC (internal — checklist applied before output)
          ↓
    COMPLETE PACKAGE OUTPUT
```

---

## TOPIC SELECTION RULES

Applied when no topic is provided. Rules run in priority order — first match wins.

**Registry filter applies before all priorities.** Before any topic is selected, reel_registry.md is consulted. Topics whose Evergreen ID or keywords match the last 30 registry entries are removed. Formulas appearing 2+ times in the last 5 entries are blocked (next-best selected automatically). Pillars appearing 4+ times in the last 7 entries are blocked (most underrepresented pillar selected). Selection proceeds to the next available option without user prompt.

---

### Priority 0 — User-Provided Article or URL (P-1 — highest priority)

**Trigger:** User pastes a URL or article text directly after or alongside the `/create-reel` command.

**Action:**
1. Fetch and read the article (WebFetch if URL, parse if text)
2. Extract: headline, key claims, statistics, dates, source credibility
3. Fact-verify all key claims — cross-check each specific number, feature, or attribution against at least one independent source
4. Flag any unverified or disputed claims — these do NOT enter the script
5. Apply the 10-angle framework to the verified content — select the strongest angle
6. Proceed to formula selection

**Output header addition:**
```
SOURCE: User-provided article — [publication / URL]
VERIFIED CLAIMS: [N of N claims passed fact-check]
EXCLUDED: [any claims dropped for insufficient verification]
```

**Note:** The user trusting an article enough to share it does not mean every claim in it is accurate. Fact-verification is non-negotiable even for user-provided sources. The script will only contain claims that can be independently confirmed.

---

### Priority 1 — Social Trending (P0 — from Social Research step)

**Trigger:** Social Research step (CONTEXT SCAN Step 2) discovered a topic scoring 18+ with verified social signal and <3 competing creator reels from top accounts in last 3 days.

**Action:** Apply the Social Trending candidate as the primary topic. Verify it passes registry filter. Run through the 10-angle framework on the researched topic. Select the highest-scoring angle. Proceed to formula selection.

**Output header addition:**
```
SOURCE: Social Trending — [platform] — [signal descriptor, e.g. "8.2K retweets in 18h"]
```

---

### Priority 2 — Breaking News from Conversation (P0)

**Trigger:** AI news mentioned in the current conversation that is under 24 hours old.

**Action:** Auto-select F07. Topic = the news event. Note the age of the news in the output header.

**Override:** If F07 has already been used today (two F07 in one day = saturation), apply the `[Kya Matlab Hai Tumhare Liye]` pivot (VP15) and redirect to F02 with the trend angle.

---

### Priority 3 — Queued P0 / P1 Ideas

**Trigger:** User has shared queued ideas from the content ideas database in this conversation.

**Action:** Select the highest-scoring P0 item first, then highest P1. If tied, apply the D3 tiebreaker (select the idea with the strongest Proof Quality — executable beats conceptual).

**Rule:** Do not select an idea where D3 = 1 (opinion only, no proof). Skip to next.

---

### Priority 4 — Trend-Driven Opportunity (from conversation)

**Trigger:** User has shared trend data (tool releases, news items, competitor coverage) in this conversation.

**Action:** Apply the 5-dimension opportunity scoring from `01_research/trend_tracking.md`. Select the candidate scoring 18+ across Freshness + Indian Relevance + Audience Pain + Competition Gap + Proof Availability.

If two candidates tie: select the one where the competition gap is highest (topic not covered by @thevarunmayya, @ezexplains, @thenawazshaikh in the last 3 days).

---

### Priority 5 — Formula Balance (No Context Required)

**Trigger:** No context in conversation, but weekly formula usage is known or can be inferred.

**Action:** Check which formula category is underrepresented this week against the target mix:

| Category | Target | Formulas | If Behind |
|---|---|---|---|
| Tool / Demo | 2–3×/week | F01, F04, F08 | Select F01 or F04 evergreen topic |
| Career / Education | 1×/week | F02, F05 | Select F05 evergreen topic |
| Proof / Comparison | 1–2×/week | F03, F06, F08 | Select F06 evergreen topic |
| News | 1×/week | F07 | Only if news exists — skip if not |
| Community | 1×/week | F09, F10 | Select F09 evergreen topic |

Select from the most underrepresented category. Pick the evergreen topic with the highest inherent audience demand from the Evergreen Topic Pool (end of this document).

---

### Priority 6 — Pillar Balance (No Context Required)

**Trigger:** Formula balance is even, but a specific content pillar is underrepresented.

**Pillar targets (weekly):**
- AI Cheat Codes: 35% of posts → 2–3 of 7 posts
- AI Tools: 30% → 2 of 7
- AI News & Updates: 20% → 1–2 of 7
- AI Certifications & Career: 15% → 1 of 7

**Action:** Select a formula from the underrepresented pillar. Apply the Evergreen Topic Pool for that pillar.

---

### Priority 7 — Default Evergreen

**Trigger:** No context, balanced week, all priorities tied, and Social Research step found no topic scoring 18+.

**Action:** Default to the highest audience-demand evergreen topic from the Evergreen Topic Pool that is NOT blocked by reel_registry.md Filter 1. Applied in this order — skip any entry whose Evergreen ID appears in the last 30 registry entries:

1. F01 — Claude system prompt / custom instructions (E01) — skip if E01 in last 30
2. F06 — AI vs manual for a specific professional task (E04 or E05) — skip if all E04–E05 in last 30
3. F09 — 3-step workflow for a common problem (E03 or E08) — skip if all E03, E08 in last 30
4. F04 — Specific underrated tool for Indian users (E09–E13) — skip if all E09–E13 in last 30

Add one line to the output header: `SOURCE: Evergreen default — add today's AI news or queued ideas for news-reactive selection.`

---

## FORMULA SELECTION RULES

Applied when no formula is provided. Run through the decision tree in order. First match wins.

```
WHAT BEST DESCRIBES THE TOPIC?

├── Breaking AI news, model release, announcement (< 48h)
│       → F07 — News Flash
│       → If > 48h: ask — reframe as F02 trend or archive?
│
├── AI trend creating career urgency (verifiable, traceable)
│       → F02 — Future Shock
│       → Check: F02 used this week? Yes → redirect to F07 or F09
│
├── Time comparison — manual task vs AI task (real numbers)
│       → F06 — AI vs Human
│       → Check: Do real timing numbers exist? No → defer until tested
│
├── Before/after quality gap (same input → dramatically better output)
│       → F08 — Mind Blowing Transformation
│       → Check: Is "before" genuinely bad? Is "after" genuinely impressive? Both must be true.
│
├── Brand-new AI tool (under 6 months Indian audience awareness)
│       → F04 — Hidden Tool
│       → Check: Personally tested? Indian accessible pricing? Both must be true.
│
├── Non-obvious shortcut / trick in a tool the audience already uses
│       → F01 — AI Cheat Code
│       → Check: Shortcut actually saves time/effort? Personally tested?
│
├── Impressive AI-generated visual, video, or output
│       → F03 — Hollywood VFX
│       → Check: Is output genuinely impressive (not just AI-generated)? If average → reject F03
│
├── Complete 3-step workflow that anyone can run in 24 hours
│       → F09 — Three Step System
│       → Check: System personally run end-to-end? All steps work without prerequisites?
│
├── 3–5 verified resources, certifications, or career tools
│       → F05 — Career List
│       → Check: Every resource personally reviewed? Under 5 items?
│
└── Real viewer comment or DM question representing common confusion
        → F10 — Comment React
        → Check: Real comment exists (not hypothetical)? Answerable in ≤30 seconds?
```

**Tiebreaker:** If two formulas fit equally, select the one used least recently this week. If still tied, select the one with the higher Primary Metric alignment with today's growth priority (Saves → F06/F09, Follows → F07/F02, DMs → F01/F04).

**Frequency limits (enforced automatically):**
- F02: Max 1× per week. If already used → redirect.
- F03: Only when impressive output exists and has been reviewed. Cannot be generated speculatively.
- F07: Max 2× per week. Third F07 in a week → redirect to F09 or F02.

---

## RESEARCH PHASE

Executes silently after topic selection, before formula selection. Applies to every topic — whether provided by the user or selected from the Evergreen Pool. Research output is never shown to the user.

### Outcome-First Principle

Research does not start with features. Research starts with the outcome.

Before gathering any information, ask: **"What result would make a viewer immediately try this?"**

The answer to that question is the reel. The tool, platform, or topic is supporting evidence.

Priority order for every research session:
1. **Outcome** — what transformation, win, or shortcut is possible?
2. **Workflow** — how does a viewer replicate the result?
3. **Features** — only when no stronger outcome angle exists

Example of the shift:
- Bad angle: "How Meigen.ai works"
- Good angle: "Pick a style from Meigen.ai's 3,000 prompts, upload your photo to ChatGPT, paste the prompt — done. Your photo now matches that poster."

The outcome is the story. The tool is supporting evidence.

### Intent Classification

Classify the topic into one of six intent types before gathering information. The intent type determines research focus — and the angle pool that gets scored highest.

| Intent Type | Definition | Research Focus |
|---|---|---|
| **Discovery Tool** | A platform or tool the audience hasn't used yet | Shortcuts, templates, galleries, ready-made assets, copy-paste wins — not platform walkthroughs |
| **Workflow Tool** | A tool the audience uses but underutilizes | The non-obvious workflow, hidden feature, or time-saving system — not feature lists |
| **News** | A recent event, release, or announcement | Indian relevance angle, immediate impact on the viewer — not press release summary |
| **Transformation** | Before/after output quality gap | The gap's size, proof quality, replicability — not creation steps |
| **Comparison** | Head-to-head between tools or approaches | The decisive winner, surprising result, decision shortcut — not balanced review |
| **Experiment** | Testing something to see what happens | The unexpected outcome, replication difficulty, real result — not methodology |

**For Discovery Tool intent:** do NOT research platform walkthroughs. Research shortcuts, templates, galleries, ready-made assets, and copy-paste workflows. The viewer needs an instant win, not an orientation.

### Social Trending Scan

Runs during CONTEXT SCAN Step 2 (before topic selection). Uses WebSearch tool. Silent — not reported to user.

**Platforms to search and what to look for:**

| Platform | Query | Signal to capture |
|---|---|---|
| Twitter/X | "AI" trending + top AI creator posts last 24h | Retweet/bookmark velocity — signals what the audience is already sharing |
| Reddit | r/artificial, r/MachineLearning, r/ChatGPT, r/AItools — top posts last 48h | Upvotes + comment count — signals what the audience is actively discussing |
| YouTube | AI trending / suggested videos last 48h | View velocity + title keywords — signals what video content is pulling traffic |
| LinkedIn | AI posts from Indian tech audience last 48h | Likes + comments + saves — signals professional career interest |
| Product Hunt | New AI tool launches this week | Upvote count — signals tools the creator audience is excited about |

**Scoring each discovered topic (same 5-dimension system as trend_tracking.md):**
- Freshness: < 24h = 5pts, 24-48h = 3pts, 48-72h = 1pt
- Indian Relevance: directly impacts Indian users = 5pts, indirectly = 2pts, not relevant = 0pts
- Audience Pain: solves a known pain = 5pts, nice to know = 2pts, irrelevant = 0pts
- Competition Gap: <3 competitor reels on this in 3 days = 5pts, 3-6 = 2pts, >6 = 0pts
- Proof Availability: can be demonstrated on screen = 5pts, verbal only = 2pts, no proof = 0pts

**Threshold:** Score 18+ → Social Trending candidate. Becomes Priority 1 topic.

**Output (internal, included in header if used):**
```
SOCIAL RESEARCH: [N] topics evaluated — top scorer: [topic] at [score]/25
SOURCE: Social Trending — [platform] — [signal: e.g., "4.2K upvotes in 14h on r/ChatGPT"]
```

---

### Fact Verification

Runs after angle selection, before formula selection. Every key claim that will appear in the script is verified. Silent — verification process not shown; failed claims dropped without notice in the output unless all claims for an angle fail (then angle is rejected).

**Verification checklist for each claim:**

| Check | Question | Action if fails |
|---|---|---|
| Currency | Is the statistic or fact less than 6 months old? | Find current version or remove |
| Source quality | Is the source official documentation, verified media, or primary source? | Find better source or remove |
| Specificity accuracy | Is the specific number/name/feature correct? | Verify exact figure or use verified approximate |
| Demonstrability | Can this claim be shown on screen, not just stated? | If not demonstrable, flag as verbal-only (lower proof score) |
| Conflicts | Does a credible source contradict this claim? | Note both versions — use the more conservative one |

**Safe language for approximate facts (use when exact figure isn't verifiable):**
- "around [N]K" not "[exact N]K"
- "more than [round number]" not "[precise number]"
- "reportedly" when citing a single source not yet widely confirmed

**The REEL_013 lesson:** The Microsoft course had 21 lessons in Version 3 — but an older companion video series had 18. Using the wrong number in the script would have been factually incorrect even though both numbers appear online. Fact verification requires finding the current, authoritative version, not just any mention.

**Claims that always require independent verification before entering a script:**
- Star/follower/user counts (change constantly — use "100K+" not "112,413")
- Lesson/feature/module counts for courses or tools
- Pricing (changes frequently)
- API access and free tier details
- Any "first," "only," "largest," or "most" superlative
- Any statistic from a single social media post or non-primary source

---

### Research Execution

For any selected topic, gather:

- **Key features** — what the tool, system, or event actually does
- **Recent developments** — anything new in the last 7–30 days
- **Common misconceptions** — what most people get wrong
- **Surprising facts** — results or behaviors that contradict expectations
- **Hidden capabilities** — features or use cases the mainstream audience has not discovered
- **Practical use cases** — specific, demonstrable applications

Identify what most creators are NOT talking about. This gap is the content opportunity.

### Angle Discovery — 10 Candidates

Research must generate at least 10 candidate angles before selection. Do not default to the first plausible angle. The best angle is rarely the first one found.

| # | Angle Type | Description |
|---|---|---|
| 1 | **Obvious Angle** | The expected take — what 80% of creators would publish on this topic |
| 2 | **Contrarian Angle** | Challenges the common narrative. Requires evidence to support it. |
| 3 | **Hidden Feature Angle** | Surfaces a capability or workflow the mainstream audience doesn't know exists |
| 4 | **Workflow Angle** | Shows a practical, repeatable system. Demonstrates value through steps, not claims. |
| 5 | **Future Impact Angle** | Connects the topic to a larger trajectory — what this means 6–12 months from now |
| 6 | **Shortcut Angle** | The fastest path to the result — skips steps most people don't realize are skippable |
| 7 | **Mistake Angle** | The common error most people are making, with a concrete correction |
| 8 | **Comparison Angle** | Head-to-head between two approaches — ends with a decisive winner |
| 9 | **Experiment Angle** | Unexpected outcome from trying something — result surprises even the creator |
| 10 | **Transformation Angle** | Same input, dramatically different output — the gap between approaches is the content |

Angles 6–10 skew toward outcomes and results. Score these higher when intent type is Discovery Tool, Transformation, or Experiment.

### Angle Selection

Select the highest-scoring angle from the 10 candidates. Scoring criteria:

**Primary question before scoring:** "Which angle makes a viewer immediately want to try this themselves?"

**Score higher:**
- Outcome or transformation the viewer can replicate in the next 30 minutes
- Shortcut that skips steps most people don't know are skippable
- Surprising insight the audience hasn't seen before
- Hidden workflow that saves real time or effort
- Mistake most people are making, with a concrete correction
- Unexpected benefit or result with demonstrated proof
- Strong opinion supported by verifiable evidence

**Score lower (avoid):**
- "Top N features of [tool]" framing
- "Best AI tool for [use case]" framing
- "New update / just released" framing without a specific outcome angle
- Restatement of official documentation or platform walkthrough
- Tutorial-style content when a shortcut, transformation, or outcome angle is available
- Any angle already covered by @thevarunmayya, @ezexplains, or @thenawazshaikh in the last 3 days

**Tiebreaker:** If two angles score equally, select the one where a viewer could reproduce the result in the next 30 minutes.

The selected angle becomes the lens for formula selection and the hook's specific claim.

### Topic Validation — 5 Gates

After research and angle selection, validate the topic against 5 questions:

| Gate | Question | Fail Action |
|---|---|---|
| **Relevance** | Is this topic still timely and current? | Reject — select next candidate |
| **Competitor Coverage** | Has this exact angle been published by a top competitor in the last 3 days? | Reject — select a differentiated angle or next topic |
| **Angle Strength** | Is the selected angle genuinely non-obvious? | Upgrade to next-best angle from the 5 candidates |
| **Proof Availability** | Can the claim be demonstrated on screen with real output? | Reject — topic without demonstrable proof cannot pass Gate 3 (Personal Proof) |
| **Format Fit** | Can this become a compelling reel in ≤35 seconds? | Redirect to Carousel or narrow the angle |

Any gate fails → reject current topic → return to TOPIC SELECTION with the next available candidate. Do not surface the rejection to the user unless all candidates are exhausted.

### What Research Improves

Research is not a formality — it changes the output:

- **Topic quality** — research surfaces the non-obvious angle that makes the reel share-worthy
- **Novelty** — validates that the chosen angle isn't already covered
- **Accuracy** — prevents claims based on assumption or outdated information
- **Authority** — grounds the script in verified, specific facts rather than generalities
- **Retention** — surprising or hidden insights create genuine watch-through pressure
- **Shareability** — angles that reveal something unexpected outperform generic angles consistently

A reel built from assumption competes on production quality. A reel built from research competes on content quality. Content quality wins.

---

## DAY-OF-WEEK GUIDANCE

When the day of week is known, apply these production slot defaults:

| Day | Recommended Formula | Notes |
|---|---|---|
| Monday | F07 or top P1 F01/F04 | Start week with either news or a strong cheat code |
| Tuesday | — (Carousel day) | Not a reel day. Redirect to carousel format if asked. |
| Wednesday | F01, F06, or F09 | Mid-week proof and workflow content |
| Thursday | F07 or F10 | Fast-produce day — use lowest-production-time formulas |
| Friday | F04 or F05 | End-of-week discovery + career content |
| Saturday | — (Carousel day) | Not a reel day. Redirect if asked. |
| Sunday | F02 or F08 | Momentum/urgency for the week ahead |

If the user runs `/create-reel` on a Carousel day, output:
```
Today is [day] — Carousel day in the weekly production schedule.
To generate a reel anyway: /create-reel [topic] [formula]
To generate a Carousel instead: /create-carousel [topic]
```

---

## OUTPUT FORMAT

Every `/create-reel` execution produces this structure — no exceptions.

---

```
══════════════════════════════════════════════════════
/create-reel — [YYYY-MM-DD]  |  [Day of Week]
══════════════════════════════════════════════════════
REEL:      REEL_[NNN]
TOPIC:     [selected or provided topic]
FORMULA:   F[NN] — [Formula Name]
SOURCE:    [P0 Breaking / P1 Queue / P2 Trend / P3 Formula Balance / P4 Pillar / Evergreen]
WHY:       [One sentence — e.g., "F01 not used in 3 days + AI Cheat Code pillar underweight"]
DURATION:  [XX]s
CTA:       [DM [WORD] / Follow / Save / Comment]
PATTERN:   VP[NN] — [Viral Pattern Name]
══════════════════════════════════════════════════════
```

Then immediately — with no gap, no additional commentary:

---

### HOOK

```
[Single hook line — English — max 15 words]

HOOK TYPE:  [from hook_library.md]
VP APPLIED: [VP0X — how it's applied in this specific reel]
```

---

### FULL SCRIPT

```
BEAT 1 — HOOK ([Xs]):
[Exact English words — em-dash connectors between beats within a line]

BEAT 2 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 3 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 4 — [Beat Name] ([Xs]):
[Exact English words]

BEAT 5 — CTA ([Xs]):
[Exact English words]

TOTAL: [N] words | ~[X]s at 2.5 words/sec
```

---

### SCENE BREAKDOWN

```
| Clip | Dur  | Block | Script (first 8 words)         | Camera       | Env     | Note                    |
|------|------|-------|-------------------------------|--------------|---------|-------------------------|
|  1   | 8s   | B1    | "[words]..."                  | Below E.L.   | ENV-W   | Hook — full-screen      |
|  2   | 8s   | B3    | "[words]..."                  | Below E.L.   | 58/42   | Split — TOP tool/BOTTOM char |
|  3   | 9s   | B3    | "[words]..."                  | Below E.L.   | 58/42   | Split — TOP tool/BOTTOM char |
|  4   | 6s   | B5    | "[CTA words]..."              | Eye level    | ENV-W   | CTA — full-screen       |
```

Block: B1=Hook · B3=Tool Demo · B5=CTA · B6=Storytelling · B7=Reaction  
Camera: "Below E.L." = slightly below eye level (builds credibility). CTA clip always Eye Level (warmth).  
Env: ENV-W=Warm Creator Studio · A=Dark Studio (Env C retired — policy violations)

---

### FLOW PROMPTS

Clips 1 through [N] — one complete, copy-paste-ready prompt each.

**Every prompt uses the validated master format (confirmed 2026-06-17):**
- Clip 1: CHARACTER IDENTITY LOCK verbatim + ENV-W + KINETIC LAYER + anti-repetition constraint
- Clips 2–3: IDENTITY LOCK & CONTINUITY header + TOP 58% / BOTTOM 42% split-screen + KINETIC LAYER + anti-repetition constraint
- Clip 4: IDENTITY LOCK & CONTINUITY + Eye Level camera + KINETIC LAYER with @ai_snipp label + anti-repetition constraint
- Exact English script in quotes — no Hindi, no Hinglish, no Roman transliteration
- Specific acting direction (named emotion, body language — no vague instructions)
- Duration and format: "[X] seconds, vertical 9:16" — minimum 8s except CTA (6s)
- KINETIC LAYER in every clip — color names only (no hex codes)
- No Environment C, no news/broadcast language in any prompt

**CTA clip always uses Eye Level camera** (VP13 — warmth conversion, not authority angle).  
**B2 corner-facecam format is retired** — use TOP 58% / BOTTOM 42% split-screen only.

---

### ASSEMBLY INSTRUCTIONS

```
ASSEMBLY (numbered — do in order):
1. [Step]
2. [Step]
...

COLOR GRADE:
[Formula-specific grade + any per-clip adjustments]
F06 rule: Clip 2 (Human) → -10% saturation, -5% warmth. Return full warm from Clip 3.
F07 rule: Clip 1 → -5% saturation, slight cool. Full warm from Clip 2.
F08 rule: Before clips → -15% saturation, -8% warmth. After clips → +5% warmth, +5% vibrance.

TEXT OVERLAYS (timestamped):
[Timestamp] — [Text] — [Position] — [Entry: pop/fade]

SFX SEQUENCE (timestamped):
[Timestamp] — [SFX] — [Level %]
[Proof Hold instruction if reveal present: drop music to 10-15%, hold 1.5s silence after reveal]

MUSIC: [Mood descriptor] | Background level: 25-30% | Speech always primary

EXPORT:
1080×1920 · H.264 · 30fps · 10 Mbps
```

---

### CAPTION

```
[Full caption — copy-paste ready]

[Hook line — mirrors reel opening — discovery framing, under 12 words]
[Body — value + proof + reusable asset — 2–3 lines]
[Formula-mandatory line: Save karo / DM [WORD] / Follow karo]
[Comment-debate question — F02, F06, F08 only]
.
.
.
[Set A] [Set B] [Set C] hashtags below fold
```

---

### CTA

```
ON-CAMERA: "[Exact words — under 10 words — single action]"

CAPTION:   "[Secondary CTA — one sentence]"

DM AUTO-RESPONSE (if DM CTA):
Trigger: [WORD]
Message: "[Complete response text — includes the promised deliverable]"

FIRST COMMENT: "[Seeding comment — post immediately after publishing]"
```

---

### HASHTAGS

```
SET A — BROAD REACH (5):
#[tag] #[tag] #[tag] #[tag] #[tag]

SET B — NICHE AUTHORITY (5):
#[tag] #[tag] #[tag] #[tag] #[tag]

SET C — ENGAGEMENT (5):
#[tag] #[tag] #[tag] #[tag] #[tag]
```

---

## QUALITY CHECKLIST

Self-applied before output is produced. Any item that fails is fixed — not listed as a to-do.

### Topic Selection Quality
- [ ] Topic sourced from research, trend, or queue — not creator assumption alone
- [ ] Topic not covered by @ai_snipp in the last 14 days (novelty gate)
- [ ] Topic not covered identically by top competitors in the last 3 days
- [ ] Formula choice aligns with weekly balance (no formula used more than its weekly max)

### Script Quality
- [ ] Hook under 15 words and creates genuine tension or curiosity
- [ ] Script within formula duration window (≤70 words for ≤28s, ≤88 words for ≤35s)
- [ ] One specific, verifiable claim — passes the "specifically" test
- [ ] Zero hedging language (no "maybe," "possibly," "I think")
- [ ] Formula-appropriate opener applied ("You've been doing this wrong..." / "I found something..." / "Three things changed everything...")
- [ ] CTA is single action, single trigger word
- [ ] FULL SCRIPT beats read as natural spoken sentences — short, complete thoughts with line breaks between sentences, no chained em-dash fragment chains (Rule 21; Flow Prompt SCRIPT fields remain governed by Rule 17)

### Flow Prompt Quality
- [ ] Master Seed Block in every Clip 1 prompt (verbatim)
- [ ] Continuation Block in every Clip 2+ prompt (verbatim)
- [ ] All five character locks in every prompt: HAIR / GLASSES / SKIN TONE / BEARD / FACE
- [ ] Scene Block selected and applied (B1–B7)
- [ ] Environment Block selected and applied (A–D)
- [ ] Exact script in quotes — zero placeholders remain
- [ ] Acting direction is specific (named emotion, specific body language — not "be natural")
- [ ] CTA clip uses Eye Level camera (not authority angle)
- [ ] Proof Hold embedded in editing if any reveal is present
- [ ] Visual Action Map present in every Flow prompt — one entry per spoken sentence
- [ ] Every non-CTA clip has a named camera movement (push-in / pull-out / focus shift / parallax)
- [ ] B3 demo clips: actual interface interaction described — no static UI panels
- [ ] Proof clips: animated comparison or dynamic motion — no static screenshots
- [ ] On-screen text elements contain actual, readable content — no placeholder labels, no dummy text, no unreadable blocks (Rule 16)
- [ ] Visual Action Map entries for text-visible lines include the actual on-screen content written out — not "prompt appears" or "response visible" (Rule 16)
- [ ] Pause test applied: any paused frame showing text reveals something useful to the viewer (Rule 16)
- [ ] Zero sentence-ending periods in any SCRIPT field — "—" used as separator (Rule 17 — Flow repeats on periods)
- [ ] No ".." anywhere in any SCRIPT field (Rule 17)
- [ ] Every clip is ≤10 seconds — Flow generation hard limit
- [ ] Final CTA clip Visual Action Map last entry includes @ai_snipp branding in last 2 seconds (Rule 18)

### Caption Quality
- [ ] Opens with hook or tension — not a greeting
- [ ] Reusable asset embedded (prompt, list, or tip)
- [ ] Formula-mandatory line present
- [ ] Comment-debate question for F02, F06, F08
- [ ] No em-dash characters (use " — " to prevent Instagram auto-correct)
- [ ] Under 300 words

### Hashtag and CTA Quality
- [ ] Exactly 15 hashtags in 3 sets of 5
- [ ] Mix of broad / niche / community tags
- [ ] On-camera CTA under 10 words
- [ ] DM automation response includes the actual promised deliverable (not "coming soon")
- [ ] First comment seeding text ready

---

## FAILURE MODES

### FAILURE MODE 1 — No Topic Available, No Context

**When:** `/create-reel` is run with no topic and no trend context in the conversation.

**Action:** Apply Priority 6 (Evergreen Default). Generate the package using the first available evergreen topic from the Evergreen Topic Pool below. Add to output header:

```
SOURCE: Evergreen default
NOTE: No trend context in session. For news-reactive selection, share today's AI 
headlines or queued ideas before running /create-reel.
```

Do not ask for context. Generate immediately.

---

### FAILURE MODE 2 — Topic Fails a Hard Gate

**When:** The selected or provided topic fails any of the six hard gates.

**Output:**
```
GATE FAIL — /create-reel halted

Topic: [topic]
Gate failed: [Gate N — Gate Name]
Reason: [One sentence — specific, not generic]

Options:
  → [Suggested fix or narrowed angle that passes the gate]
  → [Alternative topic from same formula that does pass]
  → /create-reel [alternative topic] [formula]
```

---

### FAILURE MODE 3 — Topic Too Long for Reel Format

**When:** The topic cannot be delivered honestly in ≤35 seconds.

**Output:**
```
FORMAT REDIRECT — topic exceeds Reel format

[Topic] requires more than 35 seconds to be honest and useful.
Options:
  → Carousel: [rephrased topic as 3-7 slide concept]
  → Narrow: /create-reel "[narrowed version that fits 35s]" [formula]
  → Split: Day 1 — [part 1 as reel], Day 2 — [part 2 as reel]
```

---

### FAILURE MODE 4 — F07 News Is Stale

**When:** Topic requires F07 but news is older than 48 hours.

**Output:**
```
NEWS STALE — F07 not available

Topic: [topic] — Age: [X] hours
Options:
  → Reframe evergreen: "Agar miss kiya — [topic] — yeh matter karta hai kyunki [Indian angle]"
  → Switch to F02 with the trend angle
  → /create-reel [topic] F02
```

---

### FAILURE MODE 5 — DM Deliverable Missing

**When:** Formula requires a DM CTA but no deliverable exists.

**Output:**
```
CTA BLOCKED — DM deliverable not specified

F[NN] uses a DM CTA. Specify what to send:
  → Prompt template      → /create-reel [topic] [formula] CTA=PROMPT
  → Tool list            → /create-reel [topic] [formula] CTA=TOOLS
  → Step-by-step system  → /create-reel [topic] [formula] CTA=SYSTEM
  → Resource list        → /create-reel [topic] [formula] CTA=LIST
  → Free tool / link     → /create-reel [topic] [formula] CTA=FREE
```

---

### FAILURE MODE 6 — Formula Ambiguity

**When:** Topic maps to two formulas with equal fit and the distinction changes the production approach.

**Output:**
```
FORMULA CHOICE — two options fit equally

F[NN] — [Name]: [one reason] — Primary metric: [metric]
F[NN] — [Name]: [one reason] — Primary metric: [metric]

Which metric matters most today?
[After user responds — immediately generate without further questions]
```

This is the only question the Daily Reel Generator is permitted to ask.

---

### FAILURE MODE 7 — F02 Already Used This Week

**When:** Topic maps to F02 but F02 has been used this week.

**Output:**
```
F02 LIMIT — Future Shock already used this week (max 1×/week)

Options:
  → F07 (News Flash): if topic is breaking news under 48h
  → F09 (Three Step System): if topic has an action path
  → Queue: save for next Monday
  → /create-reel [topic] F07
```

---

### FAILURE MODE 8 — Topic and Formula Conflict

**When:** User provides both topic and formula, but they conflict (e.g., topic is clearly F07 news but user specified F06).

**Output:**
```
INPUT CONFLICT — topic and formula mismatch

Topic: [topic] → Best fit: F[NN]
Specified: F[NN]

Options:
  → Use best-fit formula: /create-reel [topic] F[best-fit]
  → Force specified formula (if you have a specific reason): confirm with "force F[NN]"
```

---

### FAILURE MODE 9 — Carousel Day

**When:** `/create-reel` is run on Tuesday or Saturday (Carousel days in the weekly schedule).

**Output:**
```
CAROUSEL DAY — Tuesday/Saturday is Carousel format in the weekly schedule

To generate a reel anyway: /create-reel [topic] [formula]
To generate a Carousel: /create-carousel [topic]
To override the schedule and generate a reel: /create-reel force [topic] [formula]
```

---

### FAILURE MODE 10 — Registry Duplicate

**When:** The selected topic's Evergreen ID or keywords match any entry in the last 30 reel_registry.md rows.

**Action:** Skip to the next topic in the selection chain. Do not halt unless all viable options at the current priority level are blocked.

**Output (only if ALL options exhausted):**
```
REGISTRY HALT — [YYYY-MM-DD]
══════════════════════════════════════════════════════
REASON: All available evergreen topics blocked by recent coverage
LAST PRODUCED: [REEL_ID] on [date] — [topic]

FIRST AVAILABLE SLOTS:
→ [Evergreen ID] — [topic] — eligible after [earliest available date]

OPTIONS:
→ Provide a fresh topic directly: /create-reel [new topic] [formula]
→ Share today's AI news for P0 reactive selection
══════════════════════════════════════════════════════
```

---

### FAILURE MODE 11 — Examples Folder Topic

**When:** Topic selection would produce content matching a topic from `04_storyboards/examples/` files, AND that topic already has a registry entry (Generated or Published).

**Action:** Treat as Registry Duplicate — Filter 1 applies. The examples folder is a production archive, not an idea source. Skip to the next available topic.

**Note:** The examples folder is never read during topic selection. Its topics are blocked only via the registry. If EX01 maps to REEL_001 (Generated) — topic is blocked. If EX02 has no registry entry — topic is not blocked by this failure mode (but Filter 1 and all hard gates still apply).

---

## REGISTRY UPDATE REQUIREMENT

After every successful `/create-reel` output is delivered, `reel_registry.md` must be updated before the session ends. This update is silent — no user-facing output.

```
1. Determine next REEL_ID: read "Next REEL_ID" line from reel_registry.md
2. Append new row to Registry Table:
   | REEL_[NNN] | YYYY-MM-DD | Generated | F[NN] | [PILLAR] | [Topic from REEL HEADER] | [E-code or —] | [3–5 keywords] |
3. Update "Next REEL_ID" line: increment by 1
```

Skipping this update causes the next session's novelty filter to treat the topic as unused. The update is non-optional.

---

## EVERGREEN TOPIC POOL

Fallback topics when no research context is available. These pass all hard gates under any conditions — the proof can always be demonstrated on-screen.

### Pillar: AI Cheat Codes

| # | Topic | Formula | Trigger Word | Proof |
|---|---|---|---|---|
| E01 | Claude system prompt setup — most users skip this | F01 | SYSTEM | Demo on screen |
| E02 | ChatGPT custom instructions — what to put in them | F01 | PROMPT | Demo on screen |
| E03 | 3-step LinkedIn post workflow using Claude | F09 | POST | Demo on screen |
| E04 | AI vs manual — LinkedIn post (time + quality) | F06 | POST | Timer + post quality |
| E05 | AI vs manual — cold email research | F06 | EMAIL | Timer + email quality |
| E06 | Claude Projects — context that never resets | F01 | SYSTEM | Demo Projects feature |
| E07 | Resume before/after — Claude transformation | F08 | RESUME | Side-by-side output |
| E08 | 3-step AI code review workflow | F09 | CODE | Demo on screen |

### Pillar: AI Tools

| # | Topic | Formula | Trigger Word | Proof |
|---|---|---|---|---|
| E09 | Perplexity vs Google — for research tasks | F06 | TOOLS | Time comparison |
| E10 | Notion AI — features most users ignore | F01 | TOOLS | Demo on screen |
| E11 | Claude.ai free vs paid — what actually differs | F04 | FREE | Feature comparison |
| E12 | Gamma.app for AI presentations (under-known) | F04 | TOOLS | Demo on screen |
| E13 | ElevenLabs voice cloning — how it actually works | F04 | TOOLS | Audio demo |

### Pillar: AI Certifications & Career

| # | Topic | Formula | Trigger Word | Proof |
|---|---|---|---|---|
| E14 | 3 free AI certifications that actually matter | F05 | CERTIFICATIONS | Course review |
| E15 | Google AI Essentials — worth it or not? | F10 | LIST | Personal review |
| E16 | IBM AI certifications — free, recognized, Hindi? | F05 | CERTIFICATIONS | Course walkthrough |
| E17 | AI skills that matter on Indian LinkedIn | F02 | LIST | Job posting data |

### Pillar: AI News & Updates

*(Only usable if news exists. If no news available, select from another pillar.)*

| # | Topic | Formula | Notes |
|---|---|---|---|
| E18 | Latest Claude update — what changed | F07 | Only if Anthropic news in last 48h |
| E19 | ChatGPT pricing change — Indian users affected | F07 | Only if pricing news in last 48h |
| E20 | Google Gemini vs Claude — latest benchmark | F07 | Only if benchmark news in last 48h |

**Default fallback if all else fails:** The first Evergreen Pool entry NOT in the last 30 reel_registry.md rows. If E01 (Claude system prompt setup) is not in the last 30 entries, it is the default — it has the highest universal audience demand, can always be demonstrated on-screen, and has never been fully exhausted. If E01 is blocked, proceed to E02, then E03, in order.

---

## CONTEXT BRIEF FORMAT

To maximize topic selection quality, optionally provide a brief before running `/create-reel`:

```
Today: [1-3 lines of context]
/create-reel
```

**Example:**
```
Today: Anthropic released Claude 3.5 Haiku pricing update, Indian users now get 20% 
cheaper API. Saw 3 comments on competitor's reel asking "which Claude plan to use." 
F01 or F07 probably fits.
/create-reel
```

With this brief, Claude selects from P0 (news) or P1 (comment-based F10) using real signals. Without the brief, Claude uses the evergreen pool.

The brief is optional. The generator runs without it. But with it, the output is better calibrated to what the audience is discussing right now.

---

## INTEGRATION MAP

| When the generator needs... | It pulls from... |
|---|---|
| Visual Action Mapping standard | `flow_generation_template.md` — Rules 11–16, examples, camera language, on-screen content |
| Character in Flow prompts | `03_character/flow_seed_prompts.md` — Master Seed Block |
| Character consistency rules | `03_character/character_consistency_guide.md` — 5-Point Check |
| Scene block descriptions | `03_character/prompt_blocks.md` — B1–B7 |
| Environment descriptions | `03_character/flow_seed_prompts.md` — Environments A–D |
| Formula clip structure | `02_formulas/formula_index.md` — clip count, duration, CTA type |
| Formula selection logic | `02_formulas/formula_index.md` — decision tree |
| Formula-specific quality gate | Individual formula files — `02_formulas/F[NN]_*.md` |
| Hook patterns | `01_research/hook_library.md` — 10 categories |
| Viral patterns | `01_research/viral_pattern_library.md` — VP01–VP15 |
| CTA specs and automation text | `01_research/cta_library.md` — per-formula CTA |
| Topic evaluation gates | `01_research/topic_evaluation_framework.md` — 6 gates |
| Weekly balance targets | `01_research/content_pillars.md` — pillar mix |
| Topic exclusion + frequency filters | `reel_registry.md` — Publishing Memory Layer |
| Social media trending research | WebSearch tool — Twitter/X, Reddit, YouTube, LinkedIn, Product Hunt scans |
| Article/URL input (user-provided) | WebFetch tool — fetch article → extract claims → fact-verify |
| Trend context (when provided) | `01_research/trend_tracking.md` — opportunity scoring |
| Execution rules | `production_mode.md` — Rules 1–18 |
| Flow architecture (generation vs. assembly) | `flow_generation_template.md` — Flow Architecture section |
| Reference reel benchmark | `references/AI_SNIPP_REEL.md` — quality standard |

---

## WHAT THIS GENERATOR DOES NOT DO

- Does not ask for topic confirmation before generating. It selects and produces.
- Does not produce research summaries, research reports, planning documents, or analysis outputs — all research is internal and silent.
- Does not skip the Research Phase — research executes for every topic before formula selection, without exception.
- Does not generate a reel from a topic that has not been researched and angle-validated.
- Does not start research by listing features — Outcome-First Principle applies: research begins by asking "What result would make a viewer immediately try this?"
- Does not skip Intent Classification — topic intent is classified before any information is gathered, and determines research focus.
- Does not generate fewer than 10 angle candidates before selecting — 10 angles is the minimum, not a target.
- Does not proceed to formula selection before generating 10 candidate angles and selecting the strongest one.
- Does not default to tutorial-style or feature-explanation angles when a shortcut, transformation, or outcome angle is available.
- Does not use generic angle framing ("Top N features", "Best AI tool", "New update") unless research produces no stronger alternative.
- Does not write chained em-dash fragment chains in FULL SCRIPT beats ("Step — action — detail — result — done") — script beats must read as natural spoken sentences. Em-dashes are allowed within a single sentence, not as a substitute for sentences.
- Does not produce partial packages. Either all sections or a rejection notice.
- Does not ask more than one question (Formula Ambiguity — Failure Mode 6 only).
- Does not produce a reel on a Carousel day without explicit override.
- Does not use F02 more than once per week without forcing.
- Does not produce F07 content for news older than 48 hours without reframing.
- Does not leave placeholders in any Flow prompt.
- Does not produce without applying at least one VP01–VP15 pattern.
- Does not write "I'm going to use F06 because..." — it uses F06, then produces.
- Does not select topics from `04_storyboards/examples/` — that folder is a production archive, not an idea source.
- Does not skip reel_registry.md consultation before topic selection — the registry check is non-optional.
- Does not skip updating reel_registry.md after successful output — every generated reel must be recorded.
- Does not skip social media research when running in full auto mode — WebSearch across Twitter/X, Reddit, YouTube, LinkedIn, and Product Hunt is required before topic selection when no topic is provided.
- Does not include unverified claims in any script — every specific number, statistic, feature count, or superlative is fact-verified against an independent source before entering production. User providing an article does not bypass fact-checking.
- Does not treat user-provided articles or URLs as automatically accurate — all key claims are extracted and independently verified. Unverified claims are dropped, not included with a caveat.
- Does not use exact figures that change frequently (star counts, user counts, pricing) — uses verified approximate language ("100K+", "around 2M") unless the exact figure is from the official source and verified current.

---

## REVISION LOG

| Version | Change | Date |
|---|---|---|
| 1.0 | Initial daily reel generator. Topic selection priorities P0–P6. Formula selection decision tree. Day-of-week guidance. Evergreen Topic Pool (E01–E20). Failure modes 1–9. Integration map. | 2026-06-08 |
| 1.1 | Publishing Memory Layer integrated. Registry consultation step added to DAILY WORKFLOW (after context scan, before topic selection). Registry filter preamble added to TOPIC SELECTION RULES. Priority 6 updated to skip registry-blocked evergreen entries. Failure modes 10 (Registry Duplicate) and 11 (Examples Folder Topic) added. REGISTRY UPDATE REQUIREMENT section added. Evergreen default fallback updated to reference registry. reel_registry.md added to INTEGRATION MAP. Three new WHAT THIS GENERATOR DOES NOT DO items added. | 2026-06-08 |
| 1.2 | Mandatory Research Phase added between topic selection and formula selection. Research Phase (insight gathering, angle discovery), Topic Validation (5 gates), and Angle Selection steps added to DAILY WORKFLOW. Full RESEARCH PHASE section added: angle discovery framework (5 types), angle scoring criteria, topic validation gates, and rationale for what research improves. Generic angle framing explicitly blocked. Four new WHAT THIS GENERATOR DOES NOT DO items added. | 2026-06-09 |
| 1.3 | Outcome-First Research Principle added. Intent Classification added as a step before Research Phase (6 types: Discovery Tool / Workflow Tool / News / Transformation / Comparison / Experiment). Angle discovery expanded from 5 to 10 types (added Shortcut, Mistake, Comparison, Experiment, Transformation angles). Research focus adapts per intent type — Discovery Tool explicitly blocks platform walkthrough angles. Angle selection updated with outcome-first scoring and 30-minute replicability tiebreaker. Natural script format check added to quality checklist (FULL SCRIPT beats as natural spoken sentences). Seven new WHAT THIS GENERATOR DOES NOT DO items added. | 2026-06-09 |
| 1.4 | Social Research layer added. CONTEXT SCAN now runs two parallel steps: conversation scan (existing) + social media web search (new). Social Trending Scan section added to Research Phase — searches Twitter/X, Reddit, YouTube, LinkedIn, Product Hunt for AI trending topics (last 24-48h) and scores each on 5 dimensions. Social Trending candidate (P0 level) added as Priority 1 in topic selection chain. User-Provided Article/URL (P-1) added as highest-priority input — new command syntax variants `/create-reel [URL]` and `/create-reel [article text]`. Existing Priorities 1–6 renumbered to 2–7. Fact Verification subsection added to Research Phase — every key claim verified against independent source before entering script; unverified claims dropped. Safe language rules for approximate facts defined. WebSearch and WebFetch added to Integration Map. Four new WHAT THIS GENERATOR DOES NOT DO items added. | 2026-06-13 |

---

*Type `/create-reel` every morning. The system handles the rest.*
