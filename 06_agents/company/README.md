# Company-Level Agents — AI_OS Executive Layer

These agents define the executive layer of AI_OS. They are distinct from Quantara's internal agents (`06_agents/quantara/`).

**Quantara's agents** manage trading intelligence: signals, regime, risk, execution.  
**Company agents** manage the business: operations, growth, content, research, engineering health.

## Agent Roster

| Agent | Role | Primary Domain | File |
|---|---|---|---|
| Chief of Staff | Orchestrator + Founder interface | All departments | `chief_of_staff.md` |
| Engineering Director | Code health + technical delivery | All codebases | `engineering_director.md` |
| Growth Director | Revenue growth + user acquisition | TradeCopilot | `growth_director.md` |
| Research Lead | Market intelligence + strategy R&D | Quantara + AI research | `research_lead.md` |
| Content Director | AI_SNIPP pipeline + publishing | Content operations | `content_director.md` |
| Operations Manager | Uptime + infra + incidents | All live systems | `operations_manager.md` |

## How to Use an Agent (Phase 1 — Manual)

Tell Claude which agent role to adopt:
> "Act as the Engineering Director and run the daily engineering review."

Claude adopts the persona, follows the agent's responsibilities, and produces the expected output.

## Agent Hierarchy

```
Founder
    │ (reads: Daily Brief, approves: gates)
Chief of Staff
    │ (orchestrates, routes exceptions, compiles reports)
    ├── Engineering Director
    ├── Growth Director  
    ├── Research Lead
    ├── Content Director
    └── Operations Manager
```

## Agent Design Rules

1. Each agent has a clearly bounded domain. They do not step on each other.
2. Agents surface exceptions upward — they never make decisions above their authority level.
3. Agents do NOT interact with live trading systems (read-only observation only).
4. Agents use Claude Haiku for routine outputs. Claude Sonnet only for strategic reasoning.
5. Each agent produces structured output that can be consumed by the Chief of Staff.
