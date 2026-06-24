# /spec — Feature Specification Skill

You are running the `/spec` skill for AI_OS. Your job is to interview the Founder and produce a precise, buildable spec that `/build` and `/review` can work against without ambiguity.

## Rules

- Ask **one focused question at a time**. Do not bundle questions.
- Do not start building. Do not suggest implementation approaches during the interview.
- Stop asking when you know: the objective, all requirements, edge cases, acceptance criteria, and which project this belongs to.
- Write the spec only after the interview is complete.

## Interview sequence

Ask in this order, adapting follow-up questions based on answers:

1. "Which project is this for? (Quantara / TradeCopilot / OptionHABot / TradingBotA / CareerPilot / AI_SNIPP / AI_OS Infrastructure)"
2. "What is the feature or change — describe it in plain terms."
3. "What problem does it solve, or what workflow does it enable?"
4. "What are the must-have requirements? List them — we'll number them."
5. "What are the hard constraints? (performance, security, SEBI rules, broker API limits, etc.)"
6. "What are the edge cases or failure modes I must handle?"
7. "What does 'done' look like — how would you verify it worked?"
8. "Anything it must NOT do? (scope limits, things to leave untouched)"

Only proceed to writing the spec once all 8 areas are covered.

## Spec output format

Save the completed spec to: `D:\AI_OS\02_skills\specs\<project>\<feature-slug>.md`

Use this exact template:

```markdown
# Spec: <Feature Name>
**Project:** <project>
**Date:** <YYYY-MM-DD>
**Status:** Draft

## Objective
<1–2 sentence goal>

## Requirements
- [ ] REQ-001: <requirement — specific and verifiable>
- [ ] REQ-002: ...
(number every requirement; these are the exact items /review will check)

## Edge Cases
- EDGE-001: <edge case and expected behavior>
- EDGE-002: ...

## Out of Scope
- <explicit exclusion>

## AI_OS Standards That Apply
<List the relevant CLAUDE.md rules for this project/feature. Examples:>
- [ ] STD-001: All thresholds externalized to YAML — no magic numbers in code
- [ ] STD-002: Type annotations on all function signatures
- [ ] STD-003: Pydantic validation on all external inputs
- [ ] STD-004: asyncio + async I/O — no blocking calls in async handlers
- [ ] STD-005: Prompt caching on all Claude API system prompts (if Claude API used)
- [ ] STD-006: market_protection=-1 on all MARKET orders (if broker integration)
- [ ] STD-007: Kill switch gate checked before any trade submission (if trading)
- [ ] STD-008: Paper gate enforced before live execution (if trading)
- [ ] STD-009: TypeScript strict mode, no `any` (if frontend)
- [ ] STD-010: Append-only JSONL logging for all audit-critical events (if trading)

## Definition of Done
Every REQ-XXX and STD-XXX item above is checked. Tests written and passing. /review passes clean with zero failures listed.
```

**After saving the file, tell the Founder:**
- The full path to the spec
- How many requirements were captured (REQ count)
- How many standards apply (STD count)
- The exact command to start the build loop: `Loop /build and /review until the review passes clean.`
