# AI_OS Reports

Reports are the outputs of workflows. They are the primary interface between the AI_OS operating system and the Founder.

## Design Principles

1. **Scannable in 3 minutes.** If the Founder needs to read carefully to understand what happened, the report failed.
2. **Exceptions first.** Lead with what needs attention. Green status goes last.
3. **One recommended action.** Not five options. One clear recommendation.
4. **Archive everything.** Reports are institutional memory. Never delete.

## Directory Structure

```
11_reports/
├── templates/          Reusable templates for each report type
│   ├── founder_brief.md
│   ├── eod_report.md
│   ├── weekly_company_review.md
│   └── monthly_executive_summary.md
└── archive/            Generated reports organized by date
    ├── 2026-06-21/
    │   ├── founder_brief.md
    │   ├── research_brief.md
    │   ├── engineering_review.md
    │   ├── growth_review.md
    │   └── project_health.md
    └── 2026-06/
        └── monthly_executive_summary.md
```

## Report Types

| Report | Frequency | Audience | Source Workflow |
|---|---|---|---|
| Founder Brief | Daily | Founder | 01_founder_brief |
| Research Brief | Daily (internal) | Chief of Staff | 02_research_cycle |
| Engineering Review | Daily (internal) | Chief of Staff | 04_engineering_review |
| Growth Review | Daily (internal) | Chief of Staff | 05_growth_review |
| Project Health | Daily (internal) | Chief of Staff | 06_project_health_check |
| Weekly Company Review | Weekly | Founder | 01_weekly_review |
| Monthly Executive Summary | Monthly | Founder | 01_monthly_review |

## How to Generate a Report (Phase 1 — Manual)

Tell Claude:
> "Generate today's founder brief" or "Run the weekly review for this week"

Claude will use the appropriate workflow definition + report template and save to `archive/`.
