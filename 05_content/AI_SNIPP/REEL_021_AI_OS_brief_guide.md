# Your Claude OS — Quick Setup Guide

*Sent to you because you DM'd "AI OS" — this is the exact 3-step system from the reel.*

---

## What This Is

Most people use Claude by starting a new chat and re-explaining their entire context every single time.

This guide shows you a different approach: a permanent workspace where Claude already knows who you are, what you're building, and how to think — every session, automatically.

It takes about 20 minutes to set up. After that, you stop repeating yourself.

---

## Step 1 — Create the Folder Structure (20 minutes)

Create a root folder anywhere on your machine. Name it something you'll remember — this is your Claude workspace.

Inside it, create exactly 9 numbered sub-folders:

```
YourWorkspace/
├── 01_memory/      ← Notes, decisions, context you want Claude to remember
├── 02_skills/      ← Reusable task definitions for recurring work
├── 03_prompts/     ← Prompt templates you've tested and want to reuse
├── 04_projects/    ← Your actual project folders live here (or links to them)
├── 05_content/     ← Content drafts, scripts, research outputs
├── 06_agents/      ← Agent definitions if you build multi-step automations
├── 07_templates/   ← Starter templates for common project types
├── 08_mcp/         ← MCP server configs (Claude's external tool connections)
└── 09_docs/        ← Architecture notes, decisions you want auditable
```

The numbering is intentional — Claude reads them in order when it builds context. 01 loads before 09.

**You don't need to fill all folders on day one.** The structure is what matters. Start with 01, 03, and 04. The rest fills over time.

---

## Step 2 — Write CLAUDE.md (30 minutes)

This is the most important file in the entire system. It is a single markdown file saved in your root workspace folder (not inside any sub-folder).

`YourWorkspace/CLAUDE.md`

It tells Claude exactly who it's talking to and how to behave — permanently, across every session.

### What to Include in CLAUDE.md

**Section 1 — Who You Are**
One paragraph. Your role, what you do, your domain. Be specific. "Freelance developer" is less useful than "freelance React developer building client dashboards, mostly fintech."

**Section 2 — What You're Building**
List your active projects with one sentence each — what it is, what stack, current status. Claude uses this to give contextually relevant responses without you needing to explain which project you're asking about.

**Section 3 — How to Think**
This is the section most people skip, and it's the most valuable one. Tell Claude:
- What tradeoffs you care about (e.g., "simplicity over premature abstraction")
- What you won't compromise on (e.g., "never hardcode values that belong in config")
- How you like feedback ("tell me if my approach is wrong before writing code")
- What to avoid ("don't add error handling for scenarios that can't happen")

**Section 4 — Technical Standards** *(optional but powerful)*
If your work has consistent patterns — a preferred stack, naming conventions, file structure rules — list them here. Claude will apply them without being reminded.

### Example CLAUDE.md Template

```markdown
# My Claude Workspace

## Who I Am
[Your role in 2-3 sentences. Be specific about your domain and experience level.]

## Active Projects
- **Project A** — [What it is, one sentence. Stack. Current status.]
- **Project B** — [What it is, one sentence. Stack. Current status.]

## How to Think
- Correctness first. Then simplicity. Then performance.
- If I ask for a fix, fix only the broken thing — don't refactor.
- Tell me when my approach is wrong before writing code.
- No placeholder comments. No TODO stubs. Complete implementations only.
- When in doubt, ask. One clarifying question beats a wrong output.

## Technical Preferences
- [Your preferred language/framework]
- [Your linting/formatting rules]
- [Your testing approach]
- [Any non-negotiables specific to your work]
```

Fill this in honestly. The more specific you are, the less Claude will ask you to repeat yourself.

---

## Step 3 — Activate with Claude Code (5 minutes)

Once your folder structure and CLAUDE.md exist, open Claude Code (the CLI tool from Anthropic) inside your workspace folder.

```bash
cd /path/to/YourWorkspace
claude
```

Claude Code reads CLAUDE.md automatically on startup. The first response will reference your context. You won't need to explain your setup.

**If you don't have Claude Code yet:**
Install it with: `npm install -g @anthropic-ai/claude-code`

You'll need a Claude Pro subscription or an API key. The CLI is free — you pay for what you use via API, or it's included in Pro.

---

## What Happens After Activation

From this point forward, every Claude session inside this folder starts with full context.

When you say "help me fix this bug in Project A," Claude already knows what Project A is, what stack you use, and that you want the minimum viable fix — not a refactor. You don't explain it. It already knows.

Over time, your 01_memory folder becomes a knowledge base. Your 03_prompts folder becomes a library of things that actually worked. Your projects run faster because the overhead of context-setting disappears.

---

## The System Logic

```
Structure → Brief → Activate

Structure:  9 folders give Claude a place for everything
Brief:      CLAUDE.md tells Claude who it's working with
Activate:   Claude Code reads both and starts working with full context
```

That's the entire system. No tool to buy, no subscription beyond what you already have for Claude, no complex setup.

---

## Questions?

Follow **@ai_snipp** — I post AI workflows like this every day.

If you want to go deeper on any step, reply to the DM with your specific question and I'll help you work through it.

---

*Guide version: 1.0 — 2026-06-21*
*For personal use. Not for redistribution.*
