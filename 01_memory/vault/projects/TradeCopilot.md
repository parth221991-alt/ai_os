# TradeCopilot

Tags: #project #saas #typescript #react

**Status:** Active — live at tradecopilot.in with real subscribers
**Priority:** P2 — fix regressions immediately, new features after Quantara
**Location:** `D:\AI_OS\04_projects\TradingCopilot` / `D:\tradecopilot`

## What It Is
SaaS trading rule engine and dashboard with AI analysis.
Razorpay subscriptions (live keys). Real paying users.

## Stack
React 19 · TypeScript · Tailwind CSS · Radix UI · Supabase (PostgreSQL + Auth) · Recharts · Groq API

## Tech Debt
- Uses Groq API, not Anthropic — new AI features should use Claude
- Migration of Groq calls to Claude is medium-priority backlog
- `.env` file contains live Groq key + Razorpay live key — must rotate if ever committed to git

## Related
- [[AI Agent Philosophy]] (Groq → Claude migration note)
- [[Canonical Tech Stack]]
