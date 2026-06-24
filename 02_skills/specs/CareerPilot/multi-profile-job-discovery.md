# Spec: Multi-Profile Job Discovery Engine
**Project:** CareerPilot
**Date:** 2026-06-24
**Status:** Draft

## Objective
Replace the single-profile discovery model with multi-profile intelligence: each user maintains up to 5 named `JobProfile` personas (e.g., "Senior Data Analyst — Remote", "ML Engineer — Startup"), each with its own curated job feed, preferred resumes, and apply settings. Add 7 new remote job sources. Implement resume auto-selection per JD so every application uses the best-matching resume variant.

## Context / Schema Notes
- `CareerProfile` (existing) = the career VAULT (experiences, projects, skills). One per user. Do not modify.
- `JobProfile` (new) = a persona/intent layer. Many per user. Sits alongside `CareerProfile`.
- `BaseResume` (existing) already supports multiple per user — no schema constraint change needed. Must add `jobProfileId` FK to indicate the "home profile" for each resume.
- `Platform` enum (existing: LINKEDIN, NAUKRI, INDEED, WELLFOUND, REMOTEOK, COMPANY) needs 4 new values.
- `Job` needs `jobProfileId` FK so the curated feed is per-profile.

---

## Requirements

### Schema Changes
- [ ] REQ-001: Add `JobProfile` model to `prisma/schema.prisma` with fields:
  - `id UUID PK`, `userId UUID FK`, `name String`, `description String?`
  - `targetRoles String[]`, `targetLocations String[]`
  - `salaryMin Int?`, `salaryMax Int?`, `currency String @default("INR")`
  - `remotePreference RemotePref @default(REMOTE_ONLY)`
  - `preferredSources Platform[]` (which boards to pull from for this profile)
  - `minMatchScore Int @default(70)` (jobs below this threshold not shown)
  - `autoApplyEnabled Boolean @default(false)`
  - `autoApplyPlatforms Platform[]`
  - `dailyApplyLimit Int @default(10)`
  - `isActive Boolean @default(true)`
  - `createdAt`, `updatedAt` (standard timestamps)
  - Relation: `User`, `BaseResume[]`, `Job[]`
- [ ] REQ-002: Add `jobProfileId String? @map("job_profile_id") @db.Uuid` to `BaseResume` model with optional FK to `JobProfile`.
- [ ] REQ-003: Add `jobProfileId String? @map("job_profile_id") @db.Uuid` to `Job` model with optional FK to `JobProfile`. Add index on `[jobProfileId, matchScore(sort: Desc)]`.
- [ ] REQ-004: Extend `Platform` enum with: `REMOTIVE`, `WEWORKREMOTELY`, `HIMALAYAS`, `ARBEITNOW`, `JSEARCH`.
- [ ] REQ-005: Generate and apply a Prisma migration: `npx prisma migrate dev --name add_job_profiles`.

### Resume Upload (Multi-Resume)
- [ ] REQ-006: `POST /api/vault/upload` must accept a `profileId` field in the multipart form body. If provided, set `jobProfileId` on the created `BaseResume`. If omitted, `jobProfileId` is null (global resume available to all profiles).
- [ ] REQ-007: Each uploaded PDF must be stored in Supabase Storage bucket `resumes` at path `{userId}/{resumeId}/{filename}`. Store the public URL in `BaseResume.filePath`.
- [ ] REQ-008: `GET /api/resume` must return all `BaseResume` rows for the user, grouped by `jobProfileId` (null = "General"). Include `label`, `fileName`, `isActive`, `createdAt`, `variantsCount`.
- [ ] REQ-009: `PATCH /api/resume/[id]` must allow updating `label`, `isActive`, `jobProfileId`. Deactivating a resume (`isActive: false`) must not affect existing `ResumeVariant` rows that reference it.
- [ ] REQ-010: A user may have at most 10 active `BaseResume` rows total. Enforce at the API layer and return 422 if exceeded.

### Resume Auto-Selection Agent
- [ ] REQ-011: Create `lib/claude/agents/ResumeSelectAgent.ts` exporting `selectBestResume(userId: string, jd: string, profileId?: string): Promise<AgentOutput<ResumeSelectResult>>`.
  - Fetch all active `BaseResume` rows for the user (filtered to `profileId` if provided, else all).
  - For each resume, score fit against the JD using Claude Haiku (max 3 concurrent calls).
  - Return: `{ baseResumeId, label, score, reasoning }` for the highest scoring resume.
  - If only one resume exists, return it immediately without a Claude call.
- [ ] REQ-012: `POST /api/resume/select` accepts `{ jobId, profileId? }`, calls `selectBestResume`, and returns the winning `baseResumeId` and score. Used by the apply flow to pre-select the resume before tailoring.
- [ ] REQ-013: `ResumeSelectResult` type added to `types/agents.ts`: `{ baseResumeId: string; label: string; score: number; reasoning: string }`.

### Job Profile CRUD API
- [ ] REQ-014: `GET /api/profiles` — list all `JobProfile` rows for the authenticated user.
- [ ] REQ-015: `POST /api/profiles` — create a new `JobProfile`. Validate: `name` required, max 50 chars; `minMatchScore` 50–95; `dailyApplyLimit` 1–25. Enforce plan limits: FREE = 1 profile, PRO = 3 profiles, ENTERPRISE = 5 profiles.
- [ ] REQ-016: `PATCH /api/profiles/[id]` — update any editable field. User can only update their own profiles.
- [ ] REQ-017: `DELETE /api/profiles/[id]` — soft-delete by setting `isActive: false`. Do not cascade-delete jobs or applications.

### Job Discovery Sources
- [ ] REQ-018: Create `lib/scrapers/` directory with one file per source. Each scraper exports `fetchJobs(profile: JobProfileConfig): Promise<RawJob[]>`. `RawJob` is a common normalized type: `{ platformJobId, title, company, location, isRemote, remoteType, description, url, salaryMin?, salaryMax?, postedAt?, source: Platform }`.
- [ ] REQ-019: Implement `lib/scrapers/remoteok.ts` — call `https://remoteok.com/api` (public JSON, no auth). Filter by tags matching `profile.targetRoles`. Map to `RawJob`. Rate-limit: 1 req/10s.
- [ ] REQ-020: Implement `lib/scrapers/remotive.ts` — call `https://remotive.com/api/remote-jobs` with `category` query param derived from `profile.targetRoles`. Map to `RawJob`. Free, no auth.
- [ ] REQ-021: Implement `lib/scrapers/arbeitnow.ts` — call `https://www.arbeitnow.com/api/job-board-api` with `remote=true`. Map to `RawJob`. Free, no auth.
- [ ] REQ-022: Implement `lib/scrapers/weworkremotely.ts` — fetch RSS `https://weworkremotely.com/remote-jobs.rss`, parse XML with `fast-xml-parser`, map to `RawJob`. Free.
- [ ] REQ-023: Implement `lib/scrapers/adzuna.ts` — call Adzuna Jobs API `https://api.adzuna.com/v1/api/jobs/in/search/1` (India) with `what` = role, `where` = location, `max_days_old=7`. Requires `ADZUNA_APP_ID` + `ADZUNA_APP_KEY` env vars.
- [ ] REQ-024: Implement `lib/scrapers/jsearch.ts` — call JSearch RapidAPI `https://jsearch.p.rapidapi.com/search` with `query` = role, `num_pages=5`, `date_posted=week`. Requires `RAPIDAPI_KEY` env var. Covers Google Jobs / LinkedIn / Indeed / Glassdoor in one call.
- [ ] REQ-025: Update `lib/scrapers/naukri.ts` (already exists in `workers/scrapers/`) to conform to the `RawJob` type and export `fetchJobs(profile: JobProfileConfig): Promise<RawJob[]>`.
- [ ] REQ-026: Create `lib/scrapers/index.ts` — `runDiscovery(profile: JobProfile): Promise<RawJob[]>` that fans out to all sources in `profile.preferredSources` in parallel (Promise.allSettled), deduplicates by `platformJobId`, and returns merged results.
- [ ] REQ-027: After fetching raw jobs, score each with `scoreJobMatch` (existing agent). Store scored jobs in `Job` table with `jobProfileId` set. Skip insert if `[userId, platform, platformJobId]` unique constraint would be violated (upsert on conflict).
- [ ] REQ-028: `POST /api/jobs/discover` — triggers discovery for a specific `profileId`. Queues a BullMQ `discover` job. Returns `{ queued: true, jobCount: 0 }` immediately.
- [ ] REQ-029: `GET /api/jobs?profileId=<id>&minScore=<n>&page=<n>` — return paginated job feed filtered to a profile. Default `minScore` = profile's `minMatchScore`. Include `matchScore`, `matchReasoning`, `isEasyApply`, `platform`.

### `/profiles` UI Page
- [ ] REQ-030: Create `app/profiles/page.tsx` — profile cards grid. Each card shows: name, active job count, auto-apply status, preferred sources as pills. "Create Profile" button opens a drawer.
- [ ] REQ-031: Profile creation/edit drawer: fields for name, targetRoles (tag input), targetLocations, salary range, remotePreference, preferredSources (multi-select checkboxes with source logos), minMatchScore (slider 50–95), autoApplyEnabled toggle, dailyApplyLimit.
- [ ] REQ-032: `/jobs` page must render a profile switcher (tabs or dropdown) at the top. Switching profile reloads the job feed for that profile's curated jobs.
- [ ] REQ-033: `/resume` page must show resumes grouped by profile, with a "General" group for unassigned resumes. Upload button on each group defaults `profileId` to that group.

### Environment Variables
- [ ] REQ-034: Add to `.env.local.example`: `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`, `RAPIDAPI_KEY`.

---

## Edge Cases
- EDGE-001: User deletes a `JobProfile` that has active jobs and applications — soft delete only, jobs and applications retain their `jobProfileId` FK for historical purposes, but the profile no longer appears in the active profile switcher.
- EDGE-002: A `BaseResume` has `jobProfileId` null (general) — `selectBestResume` must include it in the candidate pool for all profiles.
- EDGE-003: Adzuna or JSearch API is down — `runDiscovery` uses `Promise.allSettled`, so other sources continue. Log the failure; do not throw.
- EDGE-004: `scoreJobMatch` for a 500-job discovery run — batch concurrency must be capped at 5 concurrent Claude calls to avoid rate limiting. Use a concurrency-limited queue.
- EDGE-005: Same job appears on RemoteOK and JSearch — deduplicate by `platformJobId` after normalizing URLs. If two sources return the same job URL, prefer the source with more data (description length).
- EDGE-006: FREE plan user tries to create a second profile — return 403 with message "Upgrade to Pro to create multiple profiles."
- EDGE-007: `selectBestResume` called when user has 0 active resumes — return 422 "No active resume found. Upload a resume first."

---

## Out of Scope
- Wellfound scraper (no public API; requires Playwright — deferred to Sprint 2).
- LinkedIn job scraping (ban risk — jobs sourced via JSearch which covers LinkedIn listings).
- FlexJobs (paid subscription required for API access).
- Profile sharing or team features.
- Resume parsing from uploaded PDF (already handled by existing VaultAgent).

---

## AI_OS Standards That Apply
- [ ] STD-001: TypeScript strict mode, no `any` — all scraper return types use `RawJob`, agent args typed explicitly
- [ ] STD-002: Prompt caching on all Claude system prompts — `selectBestResume` must use `cachedText()` on the system prompt block
- [ ] STD-003: No magic numbers — `minMatchScore` default (70), `dailyApplyLimit` default (10), concurrency cap (5) all sourced from config or profile settings
- [ ] STD-004: All external API calls in async handlers only — no blocking calls
- [ ] STD-005: All new env vars added to `.env.local.example` with descriptions
- [ ] STD-006: Prisma migration required for every schema change — no raw SQL patches

---

## Definition of Done
Every REQ-XXX and STD-XXX item above is checked. `next build` passes with zero TypeScript errors. `/profiles` page renders, profile CRUD works, job feed switches per profile. At least 3 scrapers return real job data in local testing. `selectBestResume` returns correct winner when user has 2+ resumes. `/review` passes clean with zero failures listed.
