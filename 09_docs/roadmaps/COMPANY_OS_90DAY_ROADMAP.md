# AI_OS Company Operating System — 90-Day Implementation Roadmap

**Start Date:** 2026-06-21  
**Target Date:** 2026-09-19  
**Owner:** Founder  
**Status:** Phase 1 Active

---

## Objective

Transform AI_OS from a project collection into a functional company operating system where:
- All departments operate with clear responsibilities
- The Founder reads one brief, not six dashboards
- Recurring tasks are automated, not manual
- Exceptions surface upward; routine work runs without attention

---

## Phase 1: Foundation (Days 1–30 | June 21 – July 21)
**Theme:** Design and structure. Everything runs manually via Claude.  
**Mode:** Founder triggers workflows by asking Claude. Claude runs them.

### Week 1 (June 21–28): Architecture Complete ✅
- [x] Design COMPANY_OS_ARCHITECTURE.md
- [x] Create all folder structure (00_dashboard through 11_reports)
- [x] Write all 6 company-level agent definitions
- [x] Write all daily/weekly/monthly workflow definitions
- [x] Write all report templates
- [x] Expand memory layer (opportunities, competitors, company_history, founder_preferences)
- [x] Create archive structure for first reports (11_reports/archive/YYYY-MM-DD/)
- [x] Write all 5 missing prompt templates in 03_prompts/daily/ and 03_prompts/monthly/
- [x] Create 07_templates/ python-trading-bot scaffold + README
- [x] Create 08_mcp/ README (active MCPs, planned MCPs, token status)
- [x] Move architecture_inventory.md to 09_docs/ (stray artifact resolved)
- [x] AI_OS Command Center Dashboard live at port 8006 (FastAPI + SQLite)

### Week 2 (June 28 – July 5): First Runs
- [ ] Run first Daily Founder Brief (manually, using the workflow and template)
- [ ] Run first Daily Research Cycle
- [ ] Run first Project Health Check
- [ ] Run first Engineering Review
- [ ] Identify gaps in the workflow definitions from first run
- [ ] Update workflow files based on actual experience

### Week 3 (July 5–12): Growth and Content Workflows
- [ ] Run first Growth Review
- [ ] Run first Content Cycle (using Content Director agent)
- [ ] Run first Weekly Company Review (July 6, Sunday)
- [ ] Populate `01_memory/opportunities/` with first 3 opportunities
- [ ] Populate `01_memory/competitors/` with first 5 competitors

### Week 4 (July 12–21): Stabilization
- [ ] All 6 daily workflows running smoothly
- [ ] First monthly review planned for July 27
- [ ] Gaps identified, workflows v1.1 updated
- [ ] 03_prompts/ populated with prompt templates for all workflows
- [ ] Phase 1 retrospective complete

**Phase 1 Success Criteria:**
- Daily brief is generated and useful within 5 minutes
- All 6 workflows can be executed in < 30 minutes total
- Founder reads brief daily and acts on ≤ 2 exceptions per week
- No manual dashboard checking needed during Phase 1

---

## Phase 2: Scheduled Execution (Days 31–60 | July 21 – August 20)
**Theme:** Automation. Workflows trigger without the Founder asking.  
**Mode:** Claude Code hooks or scheduled tasks trigger workflows automatically.

### Milestone 2.1: Automated Morning Stack (by Day 45)
- [ ] Project Health Check runs automatically at 8:45 AM
- [ ] Research Cycle runs automatically at 8:30 AM
- [ ] Engineering Review runs automatically at 9:30 AM
- [ ] Growth Review runs automatically at 9:30 AM
- [ ] Daily Founder Brief auto-generated at 9:00 AM
- [ ] Founder receives brief without having to ask

### Milestone 2.2: Content Automation (by Day 50)
- [ ] Content Cycle runs automatically at 10:00 AM
- [ ] Reel registry updated automatically
- [ ] Content Director selects from backlog when no calendar entry

### Milestone 2.3: Weekly Automation (by Day 55)
- [ ] Weekly Company Review auto-generated on Sunday at 7:00 PM
- [ ] Open decisions auto-surfaced with aging alerts

### Milestone 2.4: Reporting Archive (by Day 60)
- [ ] All reports auto-saved to `11_reports/archive/[DATE]/`
- [ ] Monthly report auto-triggered on last Sunday of month

**Phase 2 Success Criteria:**
- Founder reads the daily brief (not generates it)
- Zero manual workflow triggers required on a normal day
- One content piece produced daily without Founder prompting
- Weekly review delivered on Sunday without request

---

## Phase 3: Autonomous Execution with Exception Alerts (Days 61–90 | August 20 – September 19)
**Theme:** Autonomy. Departments operate. Only exceptions reach the Founder.  
**Mode:** AI agents handle routine decisions within their authority. Founder receives exceptions only.

### Milestone 3.1: Exception-Only Communication (by Day 70)
- [ ] Daily brief reduced to exception-only format for non-event days
- [ ] Departments handle routine decisions independently
- [ ] Founder only reads full brief when exception count > 0
- [ ] P0 alert system operational (immediate notification)

### Milestone 3.2: Content Pipeline Autonomous (by Day 75)
- [ ] Script + Flow prompts generated automatically
- [ ] Content Director queues for Founder approval (not generation)
- [ ] Approval takes < 2 minutes (review, not create)

### Milestone 3.3: Growth Director Autonomous (by Day 80)
- [ ] Growth metrics tracked without daily Founder input
- [ ] Weekly growth experiment proposals generated automatically
- [ ] Founder reviews proposals (approve/reject), not generates them

### Milestone 3.4: Operations Manager Autonomous (by Day 85)
- [ ] Pre-market clearance issued automatically
- [ ] Zerodha token lifecycle managed without Founder prompting
- [ ] P0 incidents surface to Founder immediately via push notification
- [ ] Routine incidents logged and resolved without escalation

### Milestone 3.5: Phase 3 Complete (by Day 90)
- [ ] Founder time spent on AI_OS: < 30 minutes/day
- [ ] 90% of daily operations require zero Founder input
- [ ] All exceptions are high-value decisions, not operational noise
- [ ] Phase 4 dashboard requirements defined

**Phase 3 Success Criteria:**
- Founder daily AI_OS time ≤ 30 minutes
- < 3 Founder-required decisions per week on average
- Zero missed P0 alerts
- Content pipeline producing 5 reels/week with < 15 minutes Founder time

---

## Phase 4: Dashboard-Driven Operation (Day 90+ | September 2026+)
**Theme:** Visibility. Everything visible from one screen. Founder makes decisions from the dashboard.  
**Mode:** Web application serving live company metrics, decision queue, and exception alerts.

### Dashboard Application Build
- [ ] React 19 + TypeScript + Tailwind + Radix UI
- [ ] Port: 3999 (reserved)
- [ ] Panels: Executive, Quantara, TradeCopilot, AI_SNIPP, Company Health
- [ ] Data sources: JSON outputs from all workflow runs
- [ ] Real-time: OptionHABot, TradingBotA health endpoints during market hours
- [ ] Decision queue: Pending approvals from all departments
- [ ] Mobile-responsive: Founder can approve from phone

### Integration Points
- [ ] Reports output both `.md` (readable) and `.json` (parseable) formats
- [ ] Dashboard polls archive for latest JSON
- [ ] WebSocket connection to trading bot health endpoints
- [ ] Razorpay and Supabase metrics pulled directly

---

## Parallel Tracks (Running Alongside All Phases)

### Quantara Progress (independent of AI_OS phases)
- Paper trading: 40 trading days minimum
- Paper gate criteria: 60%+ win rate, no system errors (5 consecutive days), calibration complete
- Paper gate review: Founder approves live deployment when criteria met

### TradeCopilot Growth (Growth Director drives)
- Target: 100 subscribers by Phase 2 end
- Target: 500 subscribers by Phase 3 end
- Target: 1000 subscribers by Phase 4 start

### AI_SNIPP Content (Content Director drives)
- Target: 1 reel/day from Phase 2
- Target: 1000 followers by end of Phase 3
- Target: Fully automated pipeline in Phase 4

### Tech Debt (Engineering Director drives)
- P1: Groq → Claude migration in TradeCopilot
- P1: Razorpay key rotation if ever committed
- P2: Extract shared Zerodha WebSocket client
- P2: Extract shared Heikin Ashi candle builder

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Phase 1 workflows take >30 min to run manually | Medium | Low | Simplify; remove any workflow that doesn't generate value |
| Phase 2 scheduling infra not available in Claude Code | Low | Medium | Fall back to cron + shell scripts |
| Founder attention diverted to a single project | High | Medium | Weekly review surfaces portfolio imbalance |
| Quantara paper gate takes longer than expected | Medium | Low | Independent of AI_OS phases — run in parallel |
| Content Director outputs low-quality scripts | Low | Medium | Founder review in Phase 1 catches this; update system prompt |

---

## Review Schedule

- **Phase 1 retrospective:** July 21
- **Phase 2 retrospective:** August 20
- **Phase 3 retrospective:** September 19
- **Phase 4 kickoff:** September 22

Each retrospective updates this document with:
- What was completed
- What was deferred and why
- What changed in the roadmap
- Updated success criteria if needed
