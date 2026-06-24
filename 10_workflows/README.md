# AI_OS Workflows

Workflows are the operational heartbeat of AI_OS. Each workflow defines a repeating process: what triggers it, what data it needs, what Claude produces, and what reaches the Founder.

## Workflow Catalog

### Daily Workflows (Monday–Friday)
| # | Workflow | Owner | Trigger | Output |
|---|---|---|---|---|
| 01 | Founder Brief | Chief of Staff | 9:00 AM | Daily Brief report |
| 02 | Research Cycle | Research Director | 8:30 AM | Research brief |
| 03 | Content Cycle | Content Director | 10:00 AM | Reel package or content brief |
| 04 | Engineering Review | Engineering Director | 9:30 AM | Engineering health summary |
| 05 | Growth Review | Growth Director | 9:30 AM | Growth metrics summary |
| 06 | Project Health Check | Operations Manager | 8:45 AM | Project health status |

### Weekly Workflows (Sunday)
| # | Workflow | Owner | Trigger | Output |
|---|---|---|---|---|
| 01 | Weekly Review | Chief of Staff | Sunday 7:00 PM | Weekly Company Review |

### Monthly Workflows (Last Sunday of Month)
| # | Workflow | Owner | Trigger | Output |
|---|---|---|---|---|
| 01 | Monthly Review | Chief of Staff | Monthly | Monthly Executive Summary |

## How to Run a Workflow (Phase 1 — Manual)

Tell Claude:
> "Run the [workflow name] workflow for today."

Claude will:
1. Read the workflow definition
2. Pull required inputs (you provide what Claude cannot access)
3. Generate the report using the template in `11_reports/templates/`
4. Save the output to `11_reports/archive/YYYY-MM-DD/`

## Execution Phases

- **Phase 1 (current):** Manual — you ask Claude to run a workflow
- **Phase 2:** Scheduled — Claude Code hooks trigger workflows automatically
- **Phase 3:** Autonomous — workflows run and only exceptions reach you
- **Phase 4:** Dashboard-driven — outputs visible in `00_dashboard/`
