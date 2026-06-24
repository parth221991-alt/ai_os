# Spec: Email Intelligence + Application Auto-Status Update + Market Intelligence
**Project:** CareerPilot
**Date:** 2026-06-24
**Status:** Draft

## Objective
Extend the existing Gmail classifier from 6 labels to 8, wire it to automatically advance the application FSM when an email event is detected (no manual status changes needed), surface follow-up reminders for ghosted threads, and populate the `/market` stub page with real intelligence derived from scraped job data — no external salary API required.

## Context / Schema Notes
- `classifyEmail` (existing in `EmailAgent.ts`) returns `INTERVIEW_INVITE | REJECTION | ASSESSMENT | OFFER | FOLLOW_UP | GENERAL`. Two new labels needed: `GHOSTED`, `FOLLOW_UP_NEEDED`.
- `EmailClassType` enum in `schema.prisma` must be extended.
- `AppStatus` FSM (existing): `SAVED → APPROVAL_PENDING → APPLIED → HR_ROUND → TECHNICAL_ROUND → MANAGER_ROUND → OFFER → ACCEPTED | REJECTED | WITHDRAWN`.
- `StatusHistory` (existing) records every FSM transition with `triggeredBy: TriggerType`. Email-driven transitions must use `EMAIL_DETECTION`.
- `EmailThread.applicationId` (existing nullable FK) — the auto-status logic requires this to be populated during email sync. Currently it is set by a naive subject-line match. Must be improved.

---

## Requirements

### Schema Changes
- [ ] REQ-001: Extend `EmailClassType` enum with two new values: `GHOSTED`, `FOLLOW_UP_NEEDED`.
- [ ] REQ-002: Add `followUpSentAt DateTime? @map("follow_up_sent_at") @db.Timestamptz(6)` to `EmailThread` model (tracks when a follow-up was drafted/sent).
- [ ] REQ-003: Add `ghostedAt DateTime? @map("ghosted_at") @db.Timestamptz(6)` to `Application` model (set when no reply detected after 14 days post-apply).
- [ ] REQ-004: Generate and apply migration: `npx prisma migrate dev --name email_intelligence_v2`.

### Email Classifier Extension
- [ ] REQ-005: Update the `classifyEmail` system prompt in `lib/claude/prompts/email-agent.ts` to include the two new labels:
  - `GHOSTED` — email thread where last outbound was >14 days ago and no reply has been received (detected by thread metadata, not email content alone).
  - `FOLLOW_UP_NEEDED` — recruiter or hiring manager email that requires a response within 48 hours (e.g., "Are you still interested?", scheduling request with a deadline, assessment link).
- [ ] REQ-006: Update the `classifyEmail` user prompt enum string to include `GHOSTED` and `FOLLOW_UP_NEEDED`.
- [ ] REQ-007: Update `EmailClassification` type in `types/agents.ts` to include the two new union values.

### Email ↔ Application Matching (improved)
- [ ] REQ-008: During `POST /api/email/sync`, after classifying each thread, attempt to match it to an `Application` using this priority order:
  1. Exact company name match in thread subject/body against `Application.job.company` (case-insensitive).
  2. Partial role title match against `Application.job.title`.
  3. If match confidence < 0.7, leave `applicationId` null and surface in a "Unmatched Emails" section on `/email`.
- [ ] REQ-009: `POST /api/email/match` — manual override endpoint. Accepts `{ threadId, applicationId }`. Sets the FK and re-runs status update logic for that thread. Used from the "Unmatched Emails" UI.

### Application FSM Auto-Update
- [ ] REQ-010: After classifying an email and successfully matching it to an `Application`, automatically advance the FSM if the classification maps to a clear status transition:
  - `INTERVIEW_INVITE` → advance to `HR_ROUND` (if current status is `APPLIED`).
  - `REJECTION` → advance to `REJECTED` (from any non-terminal status).
  - `OFFER` → advance to `OFFER`.
  - `ASSESSMENT` → do not change status; add a `Notification` with urgency and deadline if detected.
  - `FOLLOW_UP` / `FOLLOW_UP_NEEDED` → do not change status; create a `Notification` with action_required = true.
  - `GHOSTED` → do not change status; set `Application.ghostedAt`, create a "Follow up now?" `Notification`.
  - `GENERAL` → no action.
- [ ] REQ-011: Every FSM transition triggered by email must create a `StatusHistory` row with `triggeredBy: EMAIL_DETECTION` and `note` = email subject + classification.
- [ ] REQ-012: FSM transition must be idempotent — if `Application.status` is already at or beyond the target status, skip the update and log a warning. Do not regress status.

### Ghosted Detection (Scheduled Job)
- [ ] REQ-013: Create `lib/automation/ghosted-detector.ts` exporting `detectGhostedApplications(userId: string): Promise<number>` that:
  - Finds all `Application` rows where `status = APPLIED` and `appliedAt < now() - 14 days` and `ghostedAt IS NULL`.
  - For each, sets `ghostedAt = now()` on the `Application`.
  - Updates the linked `EmailThread.classification` to `GHOSTED` if a thread exists.
  - Creates a `Notification` of type `GHOSTED_ALERT` with a "Send follow-up?" CTA.
  - Returns count of newly ghosted applications.
- [ ] REQ-014: `POST /api/automation/ghosted` — triggers `detectGhostedApplications` for the authenticated user. Called by a scheduled cron or manually from `/applications` page. Returns `{ ghostedCount }`.

### Follow-Up Drafter
- [ ] REQ-015: `POST /api/email/followup` — accepts `{ applicationId }`. Calls existing `draftEmailReply` with classification `FOLLOW_UP` and candidate context (role, company, appliedAt). Returns the drafted email body. Stores draft in `EmailThread.draftReply`. Does NOT send.
- [ ] REQ-016: On `/applications`, show a "Send Follow-up" button on any application with `ghostedAt` set. Clicking opens a modal with the draft for review. User edits if needed, clicks "Send" — which calls `POST /api/email/send` (Gmail API send via stored OAuth token). Requires explicit user action.

### `/email` Page UI
- [ ] REQ-017: `/email` page must show 4 tabbed sections: "Action Required" (FOLLOW_UP_NEEDED, ASSESSMENT), "Interviews" (INTERVIEW_INVITE), "Rejections", "Unmatched". Badge counts on each tab.
- [ ] REQ-018: Each email card must show: classification badge (color-coded), company + role linked to Application, summary one-liner, urgency chip, "Draft Reply" button (calls followup drafter), "Mark as Read" button.
- [ ] REQ-019: "Unmatched Emails" section shows threads with no `applicationId`. Each has a "Link to Application" dropdown (searchable by company/role) that calls `POST /api/email/match`.

### Market Intelligence (from scraped job data — no external API)
- [ ] REQ-020: Create `lib/analytics/market.ts` exporting `computeMarketIntelligence(userId: string): Promise<MarketIntelligence>` that queries the `Job` table for the authenticated user's discovered jobs and computes:
  - `salaryByRole`: for jobs where `salaryMin` and `salaryMax` are not null, group by normalized role title, compute median min/max salary and currency.
  - `topSkills`: aggregate `requiredSkills[]` across all discovered jobs, count frequency, return top 20.
  - `companyHiringVelocity`: count distinct `company` values, return top 10 companies by job count in last 30 days.
  - `remoteBySource`: breakdown of `isRemote = true` job percentage by `platform`.
  - `freshJobsToday`: count jobs with `discoveredAt >= today`.
- [ ] REQ-021: `GET /api/market` — calls `computeMarketIntelligence`, caches result in Redis for 1 hour (`market:intelligence:{userId}`). Returns `MarketIntelligence` object.
- [ ] REQ-022: Replace `/market` stub page with a real dashboard showing: salary ranges chart (Recharts horizontal bar), top skills word-cloud-style pills sorted by frequency, company hiring velocity bar chart, remote vs onsite donut, fresh jobs today counter.
- [ ] REQ-023: Add `MarketIntelligence` type to `types/agents.ts`.

---

## Edge Cases
- EDGE-001: Email thread matches multiple applications (same company, multiple roles applied) — match to the most recently applied application. Surface the ambiguity as a warning in the UI.
- EDGE-002: REJECTION email received after OFFER — FSM must NOT regress. Log as anomaly. Do not change status.
- EDGE-003: `detectGhostedApplications` runs for a user with no applied applications — returns 0, no writes.
- EDGE-004: Gmail OAuth token expired when follow-up send is triggered — return 401 with message "Reconnect your Gmail account" and surface re-auth button.
- EDGE-005: Market intelligence computed with <5 jobs discovered — return partial data with a `dataQualityWarning: "Discover more jobs for accurate market data"` field.
- EDGE-006: Same skill appears with different spellings across job postings (e.g., "ReactJS", "React.js", "React") — normalize before counting. Use a static alias map for the top 50 tech skills.

---

## Out of Scope
- Outlook / non-Gmail email providers.
- Sending emails without user review (auto-send is never allowed — human approval always required for outbound email).
- Real-time email push (webhook from Gmail) — polling on demand is sufficient for V1.
- NLP-based salary parsing from job description text (use only structured `salaryMin`/`salaryMax` fields for now).

---

## AI_OS Standards That Apply
- [ ] STD-001: TypeScript strict mode, no `any`
- [ ] STD-002: Prompt caching on `classifyEmail` system prompt (already present via `cachedText()` — verify it remains after prompt update)
- [ ] STD-003: Append-only principle — `StatusHistory` rows are never deleted or updated; new row per transition
- [ ] STD-004: Human approval required for all outbound actions — `draftEmailReply` returns a draft; only `POST /api/email/send` with explicit user action sends
- [ ] STD-005: Redis cache for market intelligence with 1-hour TTL — prevent repeated heavy DB aggregation queries
- [ ] STD-006: FSM idempotency — never regress application status, guard in API layer before writing

---

## Definition of Done
Every REQ-XXX and STD-XXX item above is checked. `next build` passes. Email sync correctly classifies and auto-advances at least INTERVIEW_INVITE → HR_ROUND and REJECTION → REJECTED in local testing. Ghosted detector correctly identifies applications past 14 days. `/market` page renders 5 charts with real data from discovered jobs. `/review` passes clean with zero failures listed.
