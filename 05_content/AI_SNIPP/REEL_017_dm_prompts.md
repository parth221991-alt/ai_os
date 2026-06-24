# REEL_017 — DM Response: 3 Claude Code Prompts

**Trigger word:** SYSTEM
**Reel topic:** Blank file to working SaaS feature in 47 minutes
**Status:** Ready to send

---

## Copy-Paste DM Content

Send this exactly when someone DMs "SYSTEM":

---

Here are the exact 3 Claude Code prompts from the reel 👇

Fill the brackets with your feature — works for any project.

━━━━━━━━━━━━━━━━━━━━━━
PROMPT 1 — DESCRIBE
━━━━━━━━━━━━━━━━━━━━━━

I need you to build [feature name].

Full scope:
- What it does: [plain English — what happens, what it produces]
- Who uses it: [users / admins / external systems]
- Key behaviors: [what should happen in each main scenario]
- Edge cases: [every failure case, boundary condition, or exception]
- Tech stack: [e.g., FastAPI + PostgreSQL, or React + Supabase]

Do NOT write any code yet. Confirm you understand the full scope and ask me anything that's unclear before we proceed.

━━━━━━━━━━━━━━━━━━━━━━
PROMPT 2 — REVIEW
━━━━━━━━━━━━━━━━━━━━━━

Before writing any code:

1. List every file you will create — file name + one sentence on what it does
2. Tell me every gap, ambiguity, or missing requirement you see
3. Flag anything that could become a problem during implementation

Wait for my confirmation before you start building.

━━━━━━━━━━━━━━━━━━━━━━
PROMPT 3 — BUILD
━━━━━━━━━━━━━━━━━━━━━━

Build it now. Backend first, then UI.

Rules:
- No placeholders
- No TODOs
- No "you'll need to add X later"
- Complete, working code only

━━━━━━━━━━━━━━━━━━━━━━

That's the system. The gap detection in Prompt 2 is what saves you 2 hours of debugging later.

Follow @ai_snipp for more 🔖

---

## Notes

- Prompt 2 is the one most people skip — it's why Claude finds gaps before writing a line of code
- "Backend first" in Prompt 3 matters — UI built on a broken API wastes 30 minutes
- If Claude asks a clarifying question after Prompt 1, answer it before moving to Prompt 2 — that question is a gap it found
