# Spec: Market Intelligence — Claude Insights Layer
**Project:** CareerPilot
**Date:** 2026-06-24
**Status:** Draft

## Objective
Add a Claude-synthesized "Market Signal" section to the existing `/market` page. Claude reads the raw analytics already computed from the user's discovered jobs (salary bands, skill frequency, company velocity) plus the user's resume and profile targets, and returns 4 structured insight bullets the user can act on.

## Requirements
- [ ] REQ-001: `POST /api/market/insights` — accepts `{ userId: string }` (from session). Calls `computeMarketIntelligence()` and reads the user's active resumes and job profile. Passes this context to Claude. Returns `{ insights: MarketSignal[]; computedAt: string; cached: boolean }`.
- [ ] REQ-002: Four insight types are always computed (return empty string for each if data is insufficient, never omit the key):
  - `salary_positioning`: Compare user's `salaryMin`/`salaryMax` from their job profile against the market `medianMin`/`medianMax` for their target roles. Output: one sentence describing whether they're above/below/at market.
  - `skill_gap`: List up to 5 skills that appear in >10% of job postings but are absent from the user's resume `rawText`. Output: comma-separated skill list or "No gaps detected."
  - `market_heat`: Compare `freshJobsToday` against the 7-day rolling daily average (computed from DB). Output: one sentence on whether market is heating up, cooling, or stable.
  - `best_source`: Which platform in `remoteBySource` has the highest share of jobs discovered (most postings for this user). Output: platform name + count.
- [ ] REQ-003: Claude call uses `claude-haiku-4-5-20251001` (high-frequency, not reasoning-heavy). System prompt uses `cachedText()` wrapper (mandatory prompt caching).
- [ ] REQ-004: Response is validated against a Zod schema before returning to the client. If any field is missing or Claude errors, return the raw analytics without insights (graceful degradation) — never a 500.
- [ ] REQ-005: Insights are cached in Redis under key `market:insights:{userId}` with 3600s TTL (same as the raw analytics cache). Cache busted when `?bust=1` query param is present.
- [ ] REQ-006: `/market` page calls `GET /api/market/insights` on load (after raw analytics load) and renders the "Market Signal" section above the salary chart. Four items shown as a 2×2 grid of metric cards with icon + label + one-line value.
- [ ] REQ-007: `MarketSignal` type added to `types/agents.ts`: `{ type: 'salary_positioning' | 'skill_gap' | 'market_heat' | 'best_source'; label: string; value: string; icon: string }`.

## Edge Cases
- EDGE-001: User has no resumes → skill_gap returns "Upload a resume to detect skill gaps."
- EDGE-002: User has no job profile → salary_positioning returns "Create a Job Profile to see salary positioning."
- EDGE-003: Fewer than 5 jobs discovered → all insights return "Not enough data yet — discover more jobs."
- EDGE-004: Claude API error or timeout → `POST /api/market/insights` returns `{ insights: [], error: 'Insights unavailable', cached: false }` with HTTP 200 (not 500). Page shows "Market signals unavailable — refresh to retry."
- EDGE-005: 7-day rolling average for market heat — if fewer than 7 days of job data exist, use available days; never divide by zero.

## Out of Scope
- External company review APIs (Glassdoor, LinkedIn company data) — not available without additional API keys.
- Real-time salary data from external sources — all salary data is derived from scraped job postings only.
- LinkedIn Easy Apply automation — user curates and applies manually.
- AI-generated "best fit job" recommendations — that belongs to the jobs feed, not market intelligence.

## AI_OS Standards That Apply
- [ ] STD-001: No thresholds hardcoded — skill gap threshold (10%), cache TTL (3600s), and rolling window (7 days) go in `config/careerpilot.yaml`.
- [ ] STD-005: Prompt caching mandatory on Claude system prompt — use `cachedText()` wrapper.
- [ ] STD-009: TypeScript strict mode, no `any` — `MarketSignal` type fully typed.
- [ ] STD-011: Haiku for high-frequency tasks — use `claude-haiku-4-5-20251001`, not Sonnet, for this route.

## Definition of Done
Every REQ-XXX and STD-XXX item above is checked. Tests written and passing for skill gap computation and graceful degradation. `/review` passes clean with zero failures listed.
