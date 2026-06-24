# AI_SNIPP — Reel Registry
## Publishing Memory Layer

**Version:** 1.0
**Status:** Canonical — must be read before every topic selection
**Location:** `D:\AI_OS\05_content\AI_SNIPP\reel_registry.md`
**Updated:** After every successful `/create-reel` execution

---

## Purpose

This file is the publishing memory for AI_SNIPP. It prevents duplicate content, enforces formula variety, and maintains pillar balance — automatically, across sessions. Every `/create-reel` execution must load this file before topic selection begins.

**The problem this file solves:** Without a session-persistent registry, the topic selection system defaults to the same evergreen topic (E01 — Claude Custom Instructions) every time `/create-reel` is run with no context. This file provides the state that makes diversity enforcement mechanical rather than judgment-dependent.

---

## Registry Rules

Four filters apply before any topic is selected. They run in order. All four must pass.

---

### FILTER 1 — Topic Novelty (last 30 reels)

A candidate topic is **blocked** if any of the following match any entry in the last 30 registry rows:

- **Exact Evergreen ID match** — same E-code (E01–E20) as any entry in the last 30
- **Near-identical angle** — same primary tool + same primary benefit, regardless of hook framing
- **Keyword overlap of 2+** — two or more of the candidate's keywords appear in the same row's Keywords column

If blocked: move to the next topic in the selection chain. Only halt if all options at the current priority level are exhausted.

---

### FILTER 2 — Formula Frequency (last 5 reels)

A formula is **blocked** if it appears **2 or more times** in the last 5 registry rows.

**Example:** Last 5 reels used F01, F07, F01, F06, F09. F01 appears 2× → F01 is blocked for the next reel. Select the next-best formula from the decision tree.

If blocked: select the next-best formula. Do not override. Do not produce the blocked formula "just this once."

---

### FILTER 3 — Pillar Balance (last 7 reels)

A pillar is **blocked** if it appears **4 or more times** in the last 7 registry rows (>50% of recent content).

Pillar codes used in this registry:

| Code   | Pillar                      | Weekly Target | Formulas          |
|--------|-----------------------------|---------------|-------------------|
| CHEAT  | AI Cheat Codes              | 2–3 of 7      | F01, F06, F08, F09, F10 |
| TOOLS  | AI Tools                    | 2 of 7        | F03, F04, F11     |
| NEWS   | AI News & Updates           | 1–2 of 7      | F02, F07          |
| CAREER | AI Certifications & Career  | 1 of 7        | F05               |

If blocked: select from the most underrepresented pillar instead. The pillar with the lowest count in the last 7 rows is the highest priority.

---

### FILTER 4 — Examples Folder Prohibition (always)

The files in `04_storyboards/examples/` are production templates and worked examples — not idea candidates.

| File | Assigned Reel | Topic |
|------|---------------|-------|
| EX01_claude_system_prompt_cheat_code.md | REEL_001 | Claude Custom Instructions |
| EX02_anthropic_claude4_news_flash.md | (pending assignment) | Claude 4 launch |
| EX03_cold_email_three_step_system.md | (pending assignment) | Cold email 3-step system |

Rule: Any topic that matches an examples file topic is subject to Filter 1. If the corresponding REEL_ID appears in the registry as Generated or Published → topic is blocked. If the REEL_ID is not yet in the registry → the topic may be produced, but the examples file must not be used as a production brief (it is a reference only).

**The examples folder is never read as part of topic selection. It is only consulted to verify Filter 4 against the registry.**

---

## Registry Lookup Procedure

Before topic selection, run this sequence silently:

```
STEP 1 — Load state
  Count total rows in REGISTRY TABLE.
  Identify:
    → last_30 = last 30 rows (or all rows if fewer than 30 exist)
    → last_5  = last 5 rows
    → last_7  = last 7 rows

STEP 2 — Build exclusion structures
  topic_exclusion_set  = all Evergreen IDs in last_30
  formula_frequency    = count of each formula code in last_5
  pillar_frequency     = count of each pillar code in last_7
  keyword_pairs        = all (keyword_A, keyword_B) pairs from last_30 Keywords column

STEP 3 — Apply filters to each candidate topic (in priority order P0→P6)
  For each candidate:
    Filter 1: Is Evergreen_ID in topic_exclusion_set? → BLOCK
    Filter 1: Do 2+ of the candidate's keywords appear together in keyword_pairs? → BLOCK
    Filter 2: Does formula_frequency[formula] ≥ 2? → BLOCK formula, try next-best
    Filter 3: Does pillar_frequency[pillar] ≥ 4? → BLOCK pillar, try underrepresented pillar
    All pass? → PROCEED with this topic

STEP 4 — First passing combination → topic selection complete
  If no combination passes at the current priority level → move to next priority level
  If no combination passes at any level → output REGISTRY HALT notice
```

---

## Registry Halt Notice

Output this if all viable options are blocked:

```
REGISTRY HALT — [YYYY-MM-DD]
══════════════════════════════════════════════════════
REASON: All available evergreen topics blocked by recent coverage
LAST PRODUCED: [REEL_ID] on [date] — [topic]

FIRST AVAILABLE SLOTS:
→ [Evergreen ID] — [topic name] — eligible after [date 30 reels prior expires]

OPTIONS:
→ Provide a fresh topic directly: /create-reel [new topic] [formula]
→ Share today's AI news for P0 reactive selection
══════════════════════════════════════════════════════
```

---

## Registry Update Procedure

After every successful `/create-reel` output delivery, update this file immediately. The update is silent — no user-facing output.

```
STEP 1: Determine next REEL_ID
  Read "Next REEL_ID" line at bottom of this file.

STEP 2: Extract metadata from completed output
  → Date: today's date (YYYY-MM-DD)
  → Status: Generated
  → Formula: F-code from REEL HEADER
  → Pillar: derive from formula using pillar table above
  → Topic: working title from REEL HEADER (exact text)
  → Evergreen: E-code if topic came from Evergreen Topic Pool, otherwise "—"
  → Keywords: 3–5 terms extracted from topic title (tool name, feature name, benefit)

STEP 3: Append new row to REGISTRY TABLE
  Format:
  | REEL_[NNN] | YYYY-MM-DD | Generated | F[NN] | [PILLAR] | [Topic title] | [E-code or —] | [keyword1, keyword2, keyword3] |

STEP 4: Update "Next REEL_ID" line
  Increment by 1.
```

**Status progression:** A reel starts as `Generated` (created by Claude). Update to `Published` when confirmed posted to Instagram. Update to `Archived` if unused/deprecated.

---

## Registry Table

Pillar codes: CHEAT · TOOLS · NEWS · CAREER
Status codes: Generated · Published · Archived

| REEL_ID  | Date         | Status    | Formula | Pillar | Topic                                                           | Evergreen | Keywords                                           |
|----------|--------------|-----------|---------|--------|-----------------------------------------------------------------|-----------|----------------------------------------------------|
| REEL_011 | Pre-system   | Published | F05     | CAREER | IBM AI Fundamentals, Google AI Essentials, DeepLearning.AI certs | —        | IBM, Google, DeepLearning, certification, free     |
| REEL_001 | 2026-06-08   | Generated | F01     | CHEAT  | Claude Custom Instructions — most users leave this empty        | E01       | Claude, custom instructions, system prompt, setup  |
| REEL_002 | 2026-06-09   | Generated | F04     | TOOLS  | Gamma.app — AI presentation tool jo 90% Indian creators miss karte hain | E12 | Gamma, presentations, AI deck, hidden tool, browser |
| REEL_003 | 2026-06-09   | Generated | F04     | TOOLS  | meigen.ai — GPT Image 2 free, Nano tier, banana prompt gallery | —   | meigen, GPT Image 2, free, image generation, banana prompt |
| REEL_004 | 2026-06-09   | Generated | F09     | CHEAT  | meigen.ai — 3-step professional icon creation (browse → enhance → export) | —  | meigen, icon, workflow, Prompt Enhance, transparent SVG, Figma |
| REEL_005 | 2026-06-09   | Generated | F01     | CHEAT  | Claude Artifacts — run HTML/JS/React live in chat, no IDE needed           | —  | Claude, Artifacts, live preview, code, IDE                     |
| REEL_006 | 2026-06-09   | Generated | F09     | CHEAT  | 3-step AI system: Brief → Practice → Story Bank for tech interview prep    | —  | Claude, interview prep, STAR format, question bank, mock interview |
| REEL_007 | 2026-06-10   | Generated | F02     | NEWS   | 3 AI skills Indian recruiters actually want — not what 80% list on LinkedIn | E17 | AI skills, LinkedIn, RAG pipeline, prompt chaining, API project, Indian recruiters |
| REEL_008 | 2026-06-10   | Generated | F07     | NEWS   | Claude Fable 5 — Anthropic ka naya model, 4.x era ke baad naya chapter      | —   | Fable 5, claude-fable-5, Anthropic, model release, Indian developers           |
| REEL_009 | 2026-06-11   | Generated | F01     | CHEAT  | 3 things to try with Claude Fable 5 that most Pro users haven't found yet    | —   | Fable 5, Claude Pro, extended tasks, PDF extraction, analytics benchmark        |
| REEL_010 | 2026-06-11   | Generated | F09     | CHEAT  | Claude MCP inside TradingView — Claude writes Pine Script live on your chart  | —   | Claude, TradingView, MCP, Pine Script, debug flag, npm                         |
| REEL_012 | 2026-06-12   | Generated | F04     | TOOLS  | Claude.ai Projects — persistent memory across chats, most Pro users haven't set this up | — | Claude, Projects, persistent memory, Pro, custom instructions, workspace |
| REEL_013 | 2026-06-13   | Generated | F04     | TOOLS  | microsoft/generative-ai-for-beginners — 21-lesson free GenAI course on GitHub, 100K+ stars | — | Microsoft, generative-ai-for-beginners, GitHub, GenAI, free course, prompt engineering, RAG, AI agents, fine-tuning, GitHub Models, Jupyter |
| REEL_014 | 2026-06-13   | Generated | F05     | CAREER | 5 free YouTube channels that teach AI better than any paid bootcamp | E18 | YouTube, channels, Andrej Karpathy, 3Blue1Brown, Yannic Kilcher, Sentdex, Two Minute Papers, free, neural networks, AI learning, bootcamp |
| REEL_015 | 2026-06-13   | Generated | F09     | CHEAT  | Build any web app in 3 prompts — Google AI Studio vibe coding system | — | Google AI Studio, vibe coding, Gemini, Netlify, web app, no-code, deploy, HTML |
| REEL_016 | 2026-06-14   | Generated | F05     | CAREER | 3 Claude Code skills repos no one names — marketingskills, remotion/skills, coding | — | Claude Code, skills, npx skills add, coreyhaines31, remotion-dev, nicholasgasior, career, developer tools |
| REEL_017 | 2026-06-15   | Generated | F09     | CHEAT  | Blank file to working SaaS feature in 47 minutes — 3 Claude Code prompts           | — | Claude Code, vibe coding, SaaS feature, 3 prompts, blank file                                             |
| REEL_018 | 2026-06-17   | Generated | F01     | CHEAT  | 3 Ways to Use Claude — API vs Desktop vs CLI: Which One Is Yours                    | — | Claude API, Claude Desktop, Claude Code, CLI, setup, console.anthropic.com, MCP, npm                      |
| REEL_019 | 2026-06-18   | Generated | F07     | NEWS   | Gemini CLI deprecated today — Antigravity CLI migration, hidden rate limit change   | — | Gemini CLI, Antigravity CLI, AV_API_KEY, compute cap, migration, deprecation                              |
| REEL_020 | 2026-06-19   | Generated | F04     | TOOLS  | OpenClaw — local AI that works on WhatsApp, zero subscription, zero cloud           | — | OpenClaw, WhatsApp AI, local AI, open-source, zero subscription, 247K stars                               |
| REEL_021 | 2026-06-21   | Generated | F09     | CHEAT  | AI_OS — 3-step system to build a private Claude OS (Structure → Brief → Activate)  | E19 | AI_OS, CLAUDE.md, Claude workspace, folder structure, Claude Code, operating system, context memory |
| REEL_022 | 2026-06-21   | Generated | F02     | NEWS   | AI Agent Production Gap — Google Cloud confirms 70% enterprise adoption, most Indian developers never built one | — | AI agents, enterprise adoption, Google Cloud, Indian developers, 2026, production |
| REEL_023 | 2026-06-22   | Generated | F07     | NEWS   | Anthropic Claude Corps Fellowship — full paid program, no degree required, 12 months, nonprofits | — | Anthropic, Claude Corps, fellowship, paid, no degree, nonprofits |

---

## Next REEL_ID: REEL_024

*(Increment this line after each new row is appended.)*

> **Note:** REEL_011 is a pre-system entry (published before this registry was created). The counter jumped from REEL_010 → REEL_012 in session 2026-06-12 to avoid the REEL_011 collision.

---

## Pre-System Reels

**REEL_011** is the benchmark reel that predates this registry system. It was produced before formal tracking began and is included here to prevent the AI Certifications topic (F05) from being re-used prematurely.

Earlier reels (REEL_002 through REEL_010) may exist as pre-system content. If they are identified, add them with `Status: Published` and best-available metadata. Until then, they are treated as unknown and do not affect filter calculations.

---

## Revision Log

| Version | Change | Date |
|---|---|---|
| 1.0 | Initial publishing memory layer. Four filters defined. Registry table seeded with REEL_011 (pre-system) and REEL_001 (first system-generated reel). Lookup, halt, and update procedures specified. | 2026-06-08 |
