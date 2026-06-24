# /build — Spec-Driven Build Skill

You are running the `/build` skill for AI_OS. Your job is to build exactly what the spec says — nothing more, nothing less.

## Before you write a single line of code

1. **Find the spec.** Look in `D:\AI_OS\02_skills\specs\` for the relevant `<feature-slug>.md`. If the Founder specified a name, use that. If multiple specs exist, ask which one.
2. **Read the spec completely.** Do not start until you have read every REQ-XXX, EDGE-XXX, STD-XXX, and the Definition of Done.
3. **Read the project's CLAUDE.md.** Find it at `D:\AI_OS\04_projects\<project>\CLAUDE.md` or at `D:\AI_OS\CLAUDE.md`. The standards in CLAUDE.md are non-negotiable — they override any temptation to take shortcuts.
4. **Identify the project root** from the spec's Project field and the port assignment table in CLAUDE.md.

## Build rules (non-negotiable)

- Build **only** what the spec requires. If a requirement is ambiguous, implement the minimal interpretation and flag it in your coverage report — do not invent behavior.
- **No magic numbers.** Every threshold, window, and parameter goes in the project's YAML config file. If no config file exists and the spec requires one, create it.
- **No new external dependencies** without checking if an existing one covers the need. If you must add one, state the justification explicitly in your coverage report.
- **Type annotations on every function signature** (Python). TypeScript strict mode, no `any` (TS/React).
- **Pydantic models** for all external data validation.
- **asyncio + async I/O** — no blocking calls in async handlers.
- If the feature calls the **Claude API**: add `cache_control: {"type": "ephemeral"}` to the system prompt block. No exceptions.
- If the feature touches **broker order submission**: verify `market_protection=-1` is present on every MARKET order.
- If the feature touches **trading logic**: verify the kill switch gate is checked before any trade submission.
- Write **tests** for every REQ-XXX item that can be tested. Place them in the project's `tests/` directory following existing patterns.
- Do **not** refactor surrounding code, clean up unrelated files, or rename things not mentioned in the spec.

## After building

Print a coverage report in this exact format:

```
## Build Coverage Report

**Spec:** <path to spec file>
**Project:** <project name>
**Build date:** <YYYY-MM-DD>

### Requirements
- [x] REQ-001: <title> — <brief note on how it was implemented>
- [x] REQ-002: ...
- [ ] REQ-003: <title> — NOT IMPLEMENTED: <reason or ambiguity>

### Standards Applied
- [x] STD-001: YAML config — thresholds in <config file>
- [x] STD-002: Type annotations — all functions annotated
- [ ] STD-005: Prompt caching — NOT APPLICABLE (no Claude API calls)

### Edge Cases
- [x] EDGE-001: <handled how>
- [ ] EDGE-002: <not handled — explain why>

### Tests Written
- <test file path>: <what is tested>

### Flags for /review
- FLAG-001: REQ-003 not implemented — spec says "X" but existing code does "Y", needs Founder clarification
- FLAG-002: Added dependency `httpx` — already present in Quantara venv, no new install needed
```

Hand this report to `/review` — it will use it alongside the spec to grade the build.
