# AI_OS Dashboard Architecture

The dashboard layer is the visual operating surface of AI_OS. In Phase 1–3, dashboards are defined here as data specifications. In Phase 4, they become a real web application.

## Dashboard Catalog

| Dashboard | Audience | Primary Data | Update Frequency |
|---|---|---|---|
| Executive Dashboard | Founder | All products, all departments | Daily |
| Quantara Dashboard | Founder + Research Director | Paper/live P&L, regime, signals | Real-time (live) / Daily (paper) |
| TradeCopilot Dashboard | Founder + Growth Director | MRR, users, churn, features | Daily |
| AI_SNIPP Dashboard | Founder + Content Director | Reels, views, followers, pipeline | Weekly |
| Company Health Dashboard | Founder | System uptime, costs, incidents | Daily |

## Phase 4 Implementation Plan

The dashboard will be built as a React + TypeScript application following the AI_OS frontend standard:
- **Stack:** React 19 · TypeScript · Tailwind CSS · Radix UI
- **Design system:** Reference `D:\TradingBotwithAIAnalyzer\design_guidelines.json`
- **Typography:** Chivo (headings) · IBM Plex Sans (body) · JetBrains Mono (numerics)
- **Palette:** Emerald-500 (positive) · Red-500 (negative) · Indigo-600 (primary)
- **Data source:** Reports in `11_reports/archive/` + direct API calls to Supabase / Razorpay
- **Port:** 3999 (reserved for AI_OS dashboard)
- **Mode:** Dark only

Until Phase 4, each dashboard file in this folder defines what data is displayed and where it comes from. This is the specification, not the implementation.
