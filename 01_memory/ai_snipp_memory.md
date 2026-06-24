# AI_SNIPP — Project Memory

**Last Updated:** 2026-06-08  
**Status:** Scaffolded — directory exists, no content yet  
**Location:** `D:\AI_OS\05_content\`

---

## Project Overview

AI_SNIPP is the content and reusability arm of AI_OS. It is the intended home for:
- Reusable code snippets extracted from trading projects
- Prompt templates and system prompts
- Creator content for an AI content business
- Shared utilities that multiple projects can consume

**Current state:** `D:\AI_OS\05_content\` exists but contains no files.

---

## Business Context

- Parallel investment alongside the trading system business
- Goal: extract reusable value from the trading bots into a monetizable content library
- Potential products: prompt packs, code snippet libraries, trading bot templates
- Not the primary focus — but should receive artifacts continuously as they are extracted

---

## What Should Be Here (Identified Extraction Candidates)

The following patterns appear in 2–3 projects and should be extracted into shared, reusable form:

### 1. Zerodha WebSocket Client
**Found in:** OptionHABot, TradingBotA, TradingBotwithAIAnalyzer (3 independent implementations)  
**What to extract:** Connection, heartbeat monitoring, reconnect backoff, tick handler registration  
**Target:** `D:\AI_OS\05_content\snippets\zerodha_websocket_client.py`

### 2. Heikin Ashi Candle Builder
**Found in:** OptionHABot (5-min), TradingBotA (1-min), TradingBotwithAIAnalyzer  
**What to extract:** HA OHLC calculation from regular candles, real-time incremental update  
**Target:** `D:\AI_OS\05_content\snippets\heikin_ashi_builder.py`

### 3. Zerodha LIMIT→MARKET Fallback Order Logic
**Found in:** TradingBotA, TradingBotwithAIAnalyzer (identical logic, duplicated)  
**What to extract:** LIMIT at LTP+buffer, wait N seconds, convert to MARKET if slippage < threshold, else cancel  
**Target:** `D:\AI_OS\05_content\snippets\zerodha_order_fallback.py`  
**Note:** Must include `market_protection=-1` on all MARKET orders (SEBI compliance)

### 4. Kill Switch / Daily Loss Limiter
**Found in:** Quantara (most robust), TradeCopilot (rule-based), OptionHABot (partial)  
**What to extract:** Consecutive loss governor, daily drawdown halt, configurable thresholds via YAML  
**Target:** `D:\AI_OS\05_content\snippets\kill_switch.py`  
**Note:** Port Quantara's version — it is the most battle-tested

### 5. 2-Lot Multi-Exit Risk Model
**Found in:** TradingBotA, TradingBotwithAIAnalyzer  
**What to extract:** Open 2 lots, exit Lot 1 at TP, move Lot 2 SL to breakeven, trail remainder  
**Target:** `D:\AI_OS\05_content\snippets\two_lot_exit_model.py`

### 6. Frontend Design System
**Found in:** TradingBotwithAIAnalyzer (`design_guidelines.json`)  
**What to extract:** Dark mode config, Tailwind palette, typography (Chivo/IBM Plex/JetBrains Mono), Radix UI component conventions  
**Target:** `D:\AI_OS\07_templates\design_system\` (belongs in templates, not snippets)

---

## Directory Structure (Proposed)

```
D:\AI_OS\05_content\
├── snippets/              # Reusable Python modules
│   ├── zerodha_websocket_client.py
│   ├── heikin_ashi_builder.py
│   ├── zerodha_order_fallback.py
│   ├── kill_switch.py
│   └── two_lot_exit_model.py
├── prompts/               # Prompt templates (may overlap with 03_prompts/)
│   ├── trading_analysis.md
│   └── signal_review.md
└── creator/               # AI content business assets
    └── [future content]
```

**Note:** Prompt templates may be better housed in `D:\AI_OS\03_prompts\` — avoid duplicating between `05_content\prompts\` and `03_prompts\`. Decide on one canonical location.

---

## Important Constraints

1. **Snippets must be dependency-clean**: Each extracted snippet should have minimal, explicit dependencies. No importing from a specific project's internal modules.
2. **Snippets must include tests**: Any snippet added to `05_content\snippets\` should have a companion test file.
3. **SEBI compliance must travel with the code**: Any snippet involving MARKET orders must include `market_protection=-1`. This is non-negotiable and must be documented in the snippet's docstring.
4. **No hardcoded thresholds**: Extracted snippets should accept configuration via parameters, not hardcoded values.
5. **Version the snippets**: As projects evolve, snippets can diverge. Consider a simple versioning convention (e.g., header comment with version and last-updated date).

---

## Architectural Decisions

- **Separation from `03_prompts/`**: `05_content/` is for Python code and creator content. `03_prompts/` is for Claude prompt files. The boundary is: code → `05_content/`, prompts → `03_prompts/`.
- **Snippets, not a shared library**: The goal is copy-paste reusability with clear attribution, not a formal pip-installable package. Keeping it simple avoids versioning and packaging overhead.

---

## Known Risks

1. **Extraction debt grows**: Every day that shared code lives in three projects instead of one canonical snippet, the divergence risk grows. Extract early.
2. **Snippet drift**: Once a snippet is extracted and used in multiple projects, improvements to one project's version won't automatically flow to others. Document the canonical source.
3. **Unused directory**: An empty `05_content/` directory has no value. The commitment to route artifacts here must be active, not eventual.

---

## Open Questions

1. Should `05_content/` contain a `README.md` index of available snippets?
2. Should prompts live in `05_content/prompts/` or all prompts in `03_prompts/`? Pick one.
3. Is the creator content business (AI content monetization) still an active goal?
4. What is the target audience for extracted snippets — internal use only, or public release?

---

## Priority Extraction Order

Based on impact and code duplication severity:

1. **Zerodha WebSocket Client** — 3 independent copies, most likely to diverge on bug fixes
2. **Kill Switch / Daily Loss Limiter** — safety-critical, every bot needs it, Quantara's is best
3. **Heikin Ashi Candle Builder** — 3 copies, identical math
4. **LIMIT→MARKET Order Fallback** — 2 copies, SEBI compliance concern
5. **2-Lot Exit Model** — 2 copies, complex logic that must stay consistent
6. **Design System** → `07_templates/` (different target directory)
