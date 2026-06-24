# /review — Build Review & Grading Skill

You are running the `/review` skill for AI_OS. Your job is to grade the current build against the spec with zero tolerance for vague "looks good" verdicts. You are the last gate before the Founder sees the work.

## Before you review

1. **Find the spec.** Read `D:\AI_OS\02_skills\specs\<project>\<feature-slug>.md` in full.
2. **Read the build coverage report** produced by `/build` (it will be in the conversation or in a file if `/build` saved it).
3. **Read the actual code** that was written. Do not trust the coverage report — verify every claim against the real files.
4. **Read the project's CLAUDE.md** to know which standards apply.

## Review protocol

Go through every item in this order. Do not skip items. Do not group failures vaguely.

### Layer 1 — Spec requirements (REQ-XXX)

For each REQ-XXX in the spec:
- Find the code that implements it.
- Verify it matches the spec's exact wording.
- Verify edge cases (EDGE-XXX) are handled.
- Mark: **PASS**, **PARTIAL** (note what's missing), or **FAIL** (note what's wrong and the exact spec line).

### Layer 2 — AI_OS standards (STD-XXX)

Check every STD-XXX that applies to this project/feature:

**Python projects:**
- [ ] No hardcoded thresholds — all parameters in YAML config
- [ ] Type annotations on every function signature
- [ ] Pydantic validation on all external inputs (API inputs, config parsing, broker responses)
- [ ] All I/O is async (asyncio + asyncpg/Motor/aiosqlite) — no blocking calls in async handlers
- [ ] `black` formatting compatible (line-length 100) + `ruff` linting clean

**Trading projects (Quantara, OptionHABot, TradingBotA):**
- [ ] `market_protection=-1` present on every MARKET order
- [ ] Kill switch gate checked before any trade submission
- [ ] Paper gate enforced (if in Quantara)
- [ ] LIMIT → MARKET fallback pattern: LTP+2, wait 10s, slippage < 4pts, else cancel
- [ ] Append-only JSONL logging for all audit-critical events
- [ ] No synchronous Claude API calls in market-hours handlers

**Claude API calls (any project):**
- [ ] `cache_control: {"type": "ephemeral"}` on system prompt block
- [ ] Haiku used for high-frequency tasks, Sonnet only for reasoning tasks
- [ ] Structured output (tool_use / JSON mode) where the consumer is code

**TypeScript / React projects:**
- [ ] `"strict": true` in tsconfig — no `any`
- [ ] Functional components only
- [ ] Server state via React Query; no global state libraries without justification
- [ ] No secrets in `REACT_APP_*` or other frontend env vars
- [ ] Numeric columns right-aligned, JetBrains Mono font

**All projects:**
- [ ] No new external dependency added without justification
- [ ] `.env.example` updated if new secrets added
- [ ] No documentation files created unless the spec required them

### Layer 3 — Test coverage

- Do tests exist for each REQ-XXX item that can be tested?
- Do tests actually run? Attempt to run them: use the project's venv and pytest/vitest.
- For Quantara: kill_switch, data_validity, pre_submission_guard require 95%+ coverage — check if new code in these modules has tests.
- Report: tests run, tests passed, tests failed, coverage estimate.

### Layer 4 — Flags from /build

Check every FLAG-XXX from the build coverage report. For each flag, determine if it is a real problem, a non-issue, or something that needs Founder input.

---

## Output format

### If all layers pass:

```
## Review Result: ✅ PASS

**Spec:** <path>
**Reviewed:** <YYYY-MM-DD>
**Loops to pass:** <N>

All REQ-XXX, STD-XXX, and test checks passed.

### Summary
<2–3 sentences describing what was built and why it's correct>

### Test Results
- Tests run: N | Passed: N | Failed: 0
```

### If any layer fails:

```
## Review Result: ❌ FAIL — Send back to /build

**Spec:** <path>
**Reviewed:** <YYYY-MM-DD>

### Failures (fix all before re-review)

**REQ failures:**
- FAIL · REQ-002: "<requirement text>" — the build does X but the spec requires Y. Fix: <specific fix>
- PARTIAL · REQ-005: "<requirement text>" — edge case EDGE-002 not handled. Fix: <specific fix>

**STD failures:**
- FAIL · STD-001: `configs/strategy.yaml` is missing — threshold `MIN_CONFIDENCE` is hardcoded as `0.65` in `app/signal_engine/validator.py:L47`. Move to YAML.
- FAIL · STD-003: `api/routes/webhook.py:L23` — `request.body` parsed as raw dict, not a Pydantic model.

**Test failures:**
- FAIL · REQ-003 has no test. Write `tests/test_<module>.py::test_<requirement>`.
- FAIL · Running `pytest tests/test_new_feature.py` → 2 errors (paste exact error lines)

**Flag resolutions:**
- FLAG-001 → REAL PROBLEM: REQ-003 ambiguity must be resolved before this passes. Escalate to Founder.
- FLAG-002 → NON-ISSUE: httpx already in venv. No action needed.

### Instructions for /build
Fix every FAIL and PARTIAL above in order. After fixing, re-run /review.
Do not change anything that passed. Do not add new features.
```

---

## Loop cap

After 3 consecutive FAIL → /build → /review cycles on the same failures, **stop the loop and escalate to the Founder** with:
- The exact failures that keep recurring
- Why they are not resolving
- A recommended decision (clarify spec? change approach? accept limitation?)

Do not burn tokens indefinitely on a loop that isn't converging.
