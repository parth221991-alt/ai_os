# Founder Preferences — Working Style and Defaults

**Purpose:** Calibrate all AI_OS agent behavior to the Founder's preferences so the same guidance is never given twice.  
**Last Updated:** 2026-06-21

---

## Communication Style

- **Brevity over completeness.** If it takes more than 3 minutes to read, it's too long. Cut ruthlessly.
- **Exceptions first.** Never bury a problem in a positive summary. If something needs attention, lead with it.
- **One recommendation.** Not options A, B, C. One clear recommendation with a short rationale.
- **No corporate speak.** Direct language. Not "we should consider exploring the possibility of…" — say "do X."
- **Numbers over adjectives.** "MRR up 12%" not "MRR growing well." "3 bugs" not "a few issues."

## Decision-Making Style

- **Solo founder, high autonomy.** Claude can prepare, draft, analyze, and recommend. Founder decides.
- **Irreversible decisions get more scrutiny.** Quick to decide on reversible things. Slow on: live capital deployment, pricing, product pivots, public commitments.
- **Paper before live.** Non-negotiable. No trading system goes live without completing the paper gate.
- **Simplicity wins.** Every added layer of complexity has a maintenance cost. Justify complexity or remove it.

## Priority Mental Model

1. Any live system with an open position → P0 always
2. Quantara milestone progress → High priority every day
3. TradeCopilot subscriber growth → High priority
4. Everything else → Important but not urgent

## Content Preferences

- English only for AI_SNIPP scripts. No Hinglish.
- Discovery narrative style. Not tutorial/walkthrough.
- Em-dash connectors between beats.
- One quotable line per clip — the kind that gets screenshotted.
- Flow AI video generation (not HeyGen — see feedback memories).

## Engineering Preferences

- Quantara is the gold standard. When in doubt, ask how Quantara does it.
- No new dependencies without checking if an existing one covers the need.
- YAML config for all thresholds. No magic numbers.
- Append-only logs. No updating, only appending.
- Typed everything. `mypy`/`pyright` compliance.

## Meeting/Session Preferences

- Start every session with: what needs immediate attention today?
- End every session with: what is the one most important thing to do next?
- No mid-session tangents. If something comes up, note it and return to the priority.

---

*This document is a living record. Update when the Founder corrects Claude's approach or confirms a non-obvious preference.*
