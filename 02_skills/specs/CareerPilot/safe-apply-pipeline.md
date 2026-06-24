# Spec: Safe Apply Pipeline
**Project:** CareerPilot
**Date:** 2026-06-24
**Status:** Draft

## Objective
Implement a two-tier safe application pipeline: (1) LinkedIn Assisted Apply — Claude pre-fills all application answers in a CareerPilot UI panel; the user pastes answers into LinkedIn manually, zero automation risk; (2) Naukri Auto-Apply — rate-limited BullMQ Playwright worker (max 10 apps/day per user, 3–8 min randomized delays, CAPTCHA pause) that runs in a user-authorized browser session. Both tiers auto-select and tailor the best-matching resume before applying.

## Context / Architecture Notes
- `workers/apply.ts` (existing) — BullMQ worker skeleton. Has approval gate check. TODO: Playwright not yet implemented.
- `ApprovalGate` (existing schema) — human approval model already in DB. `actionType: SUBMIT_APPLICATION`.
- `ResumeVariant` (existing) — tailored resume per job. Apply worker must reference this.
- `selectBestResume` (new, from Spec 1) — selects best base resume for a JD before tailoring.
- LinkedIn automation is explicitly banned in 2026. This spec uses ZERO LinkedIn Playwright automation. LinkedIn = assisted apply (Claude answer generation + user pastes manually).
- `JobProfile.autoApplyEnabled` and `JobProfile.autoApplyPlatforms` (new, from Spec 1) — govern which profiles and platforms allow auto-apply.

---

## Requirements

### Apply Flow — Shared Pre-Apply Steps (both tiers)
- [ ] REQ-001: Before queuing any apply job, the system must:
  1. Call `POST /api/resume/select` (from Spec 1 — `selectBestResume`) to find the best base resume for the job's JD and the active profile.
  2. Call `POST /api/resume/tailor` (existing) with the selected `baseResumeId` and `jobId` to generate a `ResumeVariant`.
  3. Wait for the variant to reach status `READY` before proceeding. If tailoring fails, abort and notify user.
  4. Create or update an `Application` row with `resumeVariantId` set to the new variant.
- [ ] REQ-002: The pre-apply steps must complete within 60 seconds. If exceeded, surface a timeout error: "Resume tailoring is taking too long — try again."
- [ ] REQ-003: ATS score from the `ResumeVariant` must be surfaced to the user before apply is triggered. If ATS score < 65, show a warning: "Low ATS match ({score}%). Proceed or improve your resume?"

### Tier 1 — LinkedIn Assisted Apply
- [ ] REQ-004: `POST /api/apply/linkedin/prep` — accepts `{ jobId, applicationId }`. Calls a new `AssistAgent` function (see REQ-011) that reads the JD, the tailored resume variant content, and generates structured answers for common LinkedIn Easy Apply questions:
  - Cover letter / why interested (200 words max)
  - Years of relevant experience
  - Expected salary (formatted per job's currency)
  - Notice period / availability
  - Work authorization / visa status (default from user profile)
  - Any screening questions detected in the JD
  Returns `{ answers: Record<string, string>, coverLetter: string }`.
- [ ] REQ-005: On `/applications/[id]` page, add a "Prepare LinkedIn Apply" button (visible only for LINKEDIN platform jobs). Clicking calls `prep`, then opens a slide-over panel "LinkedIn Apply Assistant" showing:
  - Tailored resume ATS score and key matched keywords
  - Cover letter (copyable)
  - All Q&A answers (each copyable individually)
  - A prominent "Open LinkedIn Job" button that opens the job URL in a new tab
  - Instruction: "Paste each answer into LinkedIn Easy Apply, then click 'Submit Application' in LinkedIn."
- [ ] REQ-006: After user confirms they submitted on LinkedIn (checkbox: "I submitted the application on LinkedIn"), call `POST /api/applications/[id]` with `{ status: "APPLIED", isAutoApplied: false, appliedAt: now() }`. Record `StatusHistory` with `triggeredBy: USER`.
- [ ] REQ-007: LinkedIn Assisted Apply must work without any ApprovalGate (since no automated action is taken). Skip the gate check for LINKEDIN platform.

### Tier 2 — Naukri Auto-Apply (BullMQ Worker)
- [ ] REQ-008: Update `workers/apply.ts` to implement real Naukri Playwright automation:
  - Load stored session cookies for the user from Supabase Vault key `naukri_session:{userId}`.
  - If no session cookie exists, abort with `NO_SESSION` error and notify user to run the Naukri login setup tool.
  - Launch Chromium in non-headless mode for local use, headless for server with `--no-sandbox`.
  - Navigate to `jobUrl`. Detect the "Apply" button (Naukri `button[class*="apply"]` or text "Apply Now").
  - Click Apply, fill any quick-apply form fields (resume is pre-selected by the platform from the uploaded resume on Naukri — no file upload in Playwright).
  - On CAPTCHA detection (iframe or hCaptcha element): pause worker, emit `CAPTCHA_REQUIRED` event, send `Notification` to user, wait up to 5 minutes for user to solve manually (session stays open). Resume after CAPTCHA clears.
  - On success: capture screenshot, store in `Application.screenshotPath` (Supabase Storage bucket `screenshots`). Update status to `APPLIED`, `isAutoApplied: true`.
- [ ] REQ-009: Rate limiting — enforce per-user daily apply limit:
  - Read `JobProfile.dailyApplyLimit` for the active profile (default 10).
  - Track applied count in Redis key `naukri:daily:{userId}:{YYYY-MM-DD}` with TTL = end of IST business day.
  - If limit reached, delay the BullMQ job to 9:00 AM IST next day using BullMQ `delay` option.
  - Worker must add a randomized delay between 3 and 8 minutes between each apply job using `await sleep(randomBetween(180_000, 480_000))`.
- [ ] REQ-010: ApprovalGate enforcement for Naukri auto-apply:
  - When `JobProfile.autoApplyEnabled = true` for NAUKRI, skip the gate (auto-approve). Create an `ApprovalGate` row with `status: APPROVED` for audit trail.
  - When `JobProfile.autoApplyEnabled = false`, create a `PENDING` gate. Surface in `/applications` under "Awaiting Approval". User approves/rejects. After approval, queue the BullMQ job.
  - Gates expire in 48 hours. After expiry, status → EXPIRED, application returns to `SAVED`.

### Assist Agent (LinkedIn Answer Generator)
- [ ] REQ-011: Create `lib/claude/agents/AssistAgent.ts` exporting `generateApplyAnswers(resumeVariantContent: string, jd: string, userProfile: UserProfileContext): Promise<AgentOutput<ApplyAnswers>>`.
  - Use REASONING_MODEL (`claude-sonnet-4-6`) — answer quality matters here.
  - System prompt must use `cachedText()`.
  - `UserProfileContext`: `{ name, yearsExperience, expectedSalaryMin, expectedSalaryMax, currency, noticePeriodDays, location, remotePreference }`.
  - `ApplyAnswers` type: `{ coverLetter: string; whyInterested: string; expectedSalary: string; noticePeriod: string; yearsExperience: number; workAuthorization: string; screeningAnswers: Record<string, string> }`.
  - Add `ApplyAnswers` and `UserProfileContext` to `types/agents.ts`.
- [ ] REQ-012: `generateApplyAnswers` must not invent facts. All claims in the cover letter and answers must be traceable to content in `resumeVariantContent`. Instruct this explicitly in the system prompt.

### Apply API Routes
- [ ] REQ-013: `POST /api/apply/linkedin/prep` — runs pre-apply steps (REQ-001–003) then calls `generateApplyAnswers`. Returns the answers and tailored resume ATS score. Auth required.
- [ ] REQ-014: `POST /api/apply/naukri` — accepts `{ jobId, profileId }`. Runs pre-apply steps, creates/updates `Application`, creates `ApprovalGate` (PENDING or auto-APPROVED per profile settings), queues BullMQ apply job if approved. Returns `{ status: "queued" | "pending_approval" }`.
- [ ] REQ-015: `POST /api/apply/[applicationId]/approve` — (existing route) must trigger the BullMQ apply job after gate approval. Currently a stub — implement the BullMQ enqueue logic.
- [ ] REQ-016: `GET /api/apply/status/[applicationId]` — returns `{ status, gateStatus, workerStatus, screenshotUrl? }`. Polled by the UI to show real-time apply progress.

### Naukri Session Setup Tool
- [ ] REQ-017: Create `workers/scrapers/naukri-login.ts` — interactive one-time login tool analogous to `workers/scrapers/linkedin-login.ts`. Launches visible Chromium, navigates to Naukri login, waits for user to log in manually, extracts session cookies, encrypts and stores in Supabase Vault as `naukri_session:{userId}`. Prints success confirmation.
- [ ] REQ-018: Add setup instructions to `.env.local.example` and document the command: `npx tsx workers/scrapers/naukri-login.ts`.

### `/jobs` and `/applications` UI Updates
- [ ] REQ-019: Job card on `/jobs` — add an "Apply" button with a dropdown: "LinkedIn Assisted" (only for LINKEDIN platform) or "Auto-Apply Naukri" (only for NAUKRI platform). For other platforms, show "Visit Job" link.
- [ ] REQ-020: Application detail page `/applications/[id]` — add a "Apply Progress" section showing: gate status, worker status (polling `/api/apply/status/[id]` every 5s while pending), screenshot thumbnail if available, daily quota indicator (X of Y applies used today).
- [ ] REQ-021: Approval queue on `/applications` — new tab "Awaiting Approval" showing all `ApprovalGate` rows with `status: PENDING`. Each row: job title, company, ATS score, approve/reject buttons. Approve calls `/api/apply/[id]/approve`; reject updates gate to REJECTED.

### Queue and Worker Config
- [ ] REQ-022: Add `apply` queue config to `lib/redis/queue.ts` if not already present. Queue options: `attempts: 3`, `backoff: { type: "fixed", delay: 60_000 }`, `removeOnComplete: { count: 50 }`, `removeOnFail: { count: 100 }`.
- [ ] REQ-023: Worker concurrency must be `1` (already set). Do not increase — single-user sequential applies are intentional to mimic human behavior.

---

## Edge Cases
- EDGE-001: Naukri session cookie expired mid-apply — Playwright detects redirect to login page. Worker must abort, emit `SESSION_EXPIRED` notification, stop applying for that user. User must re-run naukri-login.ts.
- EDGE-002: Naukri job no longer available (404 or "Job Closed" banner) — detect, update `Job.isActive = false`, mark `Application.status = WITHDRAWN` with note "Job no longer available", do not count toward daily limit.
- EDGE-003: `generateApplyAnswers` returns a cover letter > 200 words — truncate to 200 words at the nearest sentence boundary before displaying.
- EDGE-004: User triggers LinkedIn prep for a job that has no job description text — return a partial `ApplyAnswers` with cover letter based only on company name and title, plus a warning "Job description unavailable — answers may be generic."
- EDGE-005: Two profiles both have `autoApplyEnabled = true` for Naukri and both trigger discovery simultaneously — the BullMQ queue serializes at concurrency 1; jobs process sequentially. Daily limit is per user (not per profile), so shared across both profiles.
- EDGE-006: ATS score < 65 warning dismissed by user — still allow apply. Log the override. Surface in analytics as "low-match applications" metric.
- EDGE-007: BullMQ job fails all 3 retry attempts — update `Application.notes` with the error, set `Application.status` back to `APPROVAL_PENDING` (not APPLIED), create error `Notification`. Do not mark as APPLIED on failure.

---

## Out of Scope
- LinkedIn Playwright automation (explicitly banned — zero tolerance for account ban risk).
- Indeed, Wellfound, or company-site auto-apply (deferred to Sprint 2 as email-apply drafter).
- Chrome Extension approach (Sprint 2).
- Multi-user concurrent Naukri sessions (all applies are sequential at concurrency 1).
- CAPTCHA solving service (2Captcha, CapSolver) — user solves manually in V1.

---

## AI_OS Standards That Apply
- [ ] STD-001: TypeScript strict mode, no `any`
- [ ] STD-002: Prompt caching on `AssistAgent` system prompt via `cachedText()`
- [ ] STD-003: Human approval required before any external action — ApprovalGate enforced for auto-apply; LinkedIn is always manual submit
- [ ] STD-004: Append-only audit trail — `StatusHistory` row for every apply event, screenshot stored immutably in Supabase Storage
- [ ] STD-005: No hardcoded rate limits — `dailyApplyLimit` comes from `JobProfile`, min/max delay range should be configurable via env vars `NAUKRI_MIN_DELAY_MS` and `NAUKRI_MAX_DELAY_MS`
- [ ] STD-006: All async workers use async I/O only — no blocking Playwright calls without `await`
- [ ] STD-007: Worker retry with fixed backoff — `attempts: 3`, `delay: 60_000ms` (1 minute between retries)

---

## Definition of Done
Every REQ-XXX and STD-XXX item above is checked. `next build` passes. LinkedIn prep panel opens on a LINKEDIN job and renders all answer fields. Naukri apply queue enqueues a job and rate-limit counter increments in Redis. Worker skeleton processes a test job and logs correctly. ApprovalGate flow works end-to-end (pending → approved → queued). `/review` passes clean with zero failures listed.
