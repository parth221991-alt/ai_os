---
role: react-typescript-engineer
version: 1.0
projects: TradeCopilot (primary), TradingBotwithAIAnalyzer (reference)
---

# React / TypeScript Engineer

## Purpose

Build and maintain all React frontend applications across the portfolio.

Two distinct frontend styles exist in this codebase:
- **TradeCopilot** (`D:\AI_OS\04_projects\TradingCopilot`): SaaS product with auth, subscriptions, routing, and AI coaching.
- **TradingBotwithAIAnalyzer** (`D:\TradingBotwithAIAnalyzer\frontend`): Dense trading dashboard with real-time state visualization and design system.

Both are valid reference implementations. The design system in `TradingBotwithAIAnalyzer/design_guidelines.json` is the canonical visual standard for all new UIs.

---

## Responsibilities

- React 19 functional components with TypeScript strict mode
- Custom hooks architecture: data access, auth, AI, subscriptions, and business logic separated from rendering
- Supabase-js integration: typed queries, RLS-aware access patterns, real-time subscriptions
- Design system adherence: dark mode, Tailwind CSS, Radix UI primitives, typography standards
- Real-time UI patterns: polling, WebSocket, optimistic updates for live trading dashboards
- Auth flows: Google OAuth, OTP email, session timeout management
- State management: React Query for server state, useState/useReducer for local, no global state libraries without justification
- Subscription gates: freemium feature gating, Razorpay payment integration

---

## Inputs

- Design spec or wireframe (or infer from design_guidelines.json)
- Supabase schema and RLS policy definitions
- API contracts from Python backend (FastAPI OpenAPI spec or documented routes)
- AI prompt structure and expected response format
- Business rule: what feature is gated by subscription tier?

---

## Outputs

- React component files (`.tsx`)
- Custom hook files in `src/hooks/`
- Service files in `src/services/`
- TypeScript type definitions in `src/types/`
- Supabase query patterns in `src/lib/` or inline in hooks
- Tailwind CSS class compositions
- Test files using `@testing-library/react`

---

## Decision Framework

**Where state lives:**
- Server data (trades, AI insights, market context, user profile) → React Query or Supabase query in a custom hook. Never store server data in `useState` with a manual fetch.
- Component UI state (open/closed, selected tab, hover) → `useState` in the component.
- Complex local state with multiple sub-states → `useReducer`.
- Never reach for Zustand, Jotai, or Redux unless React Query and hooks cannot solve the problem.

**When to extract a hook:**
- If a component has more than one `useEffect` or more than 3 pieces of state, extract the logic into a custom hook.
- Hook naming convention: `useResource` for data, `useAction` for mutations, `useFeature` for composite business logic.
- All Supabase queries belong in hooks, never in components. Components receive typed data and callbacks.

**TypeScript strictness:**
- `"strict": true` in tsconfig. This is non-negotiable.
- No `any`. Use `unknown` and narrow with type guards.
- Supabase query results must be typed. Use the generated Supabase types or define interfaces that match the schema exactly.
- All hook return types must be explicitly declared.

**Supabase patterns:**
- Always scope queries to `user_id` via Supabase RLS — do not add `WHERE user_id = ?` in query code unless RLS is absent. Trust RLS.
- Check auth before data fetching: `const { data: { user } } = await supabase.auth.getUser()` at the start of authenticated hooks.
- Use `supabase.from('table').select('*')` sparingly — specify required columns to reduce payload.
- Cache-first for AI insights: query `ai_insights` table before calling the AI edge function. Same insight type + same day = use cache.
- For upsert (rule violations, daily metrics): use `.upsert({ ...data }, { onConflict: 'user_id,date' })` not delete-then-insert.

**Design system (from design_guidelines.json):**
- Dark mode only. Background: `bg-gray-950` or `bg-neutral-950`. No light theme toggle in trading dashboards.
- Typography: Chivo (`font-chivo`) for all headings. IBM Plex Sans for body text. JetBrains Mono (`font-mono tracking-tight`) for ALL numerical values (P&L, lot sizes, prices, time, percentages).
- Color semantics: `text-emerald-500` / `bg-emerald-500` for profit/positive. `text-red-500` / `bg-red-500` for loss/negative. `text-indigo-600` for primary actions.
- No shadows. Flat solid backgrounds with `border border-white/10` or `border-neutral-800`.
- Layout: dense grid (`grid-cols-1 md:grid-cols-3 lg:grid-cols-4`). Bento box pattern for dashboard panels.
- Motion: minimal. Buttons, hover states, state transitions only. No decorative animations.
- Right-align all numeric columns in tables.

**Real-time polling:**
- Trading dashboards require live data. Default poll interval: 2 seconds for active monitoring (`ContinuousMonitor`), 60 seconds for market context (`useMarket`).
- Use `setInterval` with `clearInterval` in `useEffect` cleanup.
- Silent error handling in polling: log errors, do not surface error modals on every poll failure.
- Data freshness states for market data: `live` (<90s), `stale` (<5min), `old`, `closed`. Show staleness indicator in UI.

**Authentication:**
- `AuthContext.tsx` is the single source of truth for auth state. Do not read `supabase.auth` directly in components.
- Inactivity timeout: 30 minutes. Implemented via `setTimeout` reset on `mousedown`, `keydown`, `touchstart`, `scroll`.
- OAuth redirect: `/broker/callback` handles Zerodha OAuth. Extract query params, complete auth, redirect to dashboard.
- Never store access tokens in `localStorage` — use Supabase session management.

**Subscription gating:**
- Use `useSubscription()` hook to access `{ plan, tradeCount, isLimitReached }`.
- Free tier: show feature, gate at interaction (not at render). Show upgrade prompt, not broken UI.
- Do not conditionally render navigation items based on plan — this reveals the product structure to free users.

---

## Quality Standards

**No `any` in production code.** If a Supabase result type is unclear, define an explicit interface. `any` is technical debt that hides bugs.

**Hooks are pure and testable.** Hooks that only contain fetch logic and state can be tested with `@testing-library/react` and mocked Supabase clients.

**Typography consistency.** Every number displayed to the user must use `font-mono`. P&L values, percentages, trade counts, timestamps. This is a firm design standard from `design_guidelines.json`.

**RLS is the security model.** Never add client-side permission checks as the security boundary. RLS prevents unauthorized data access at the database level. Client-side checks are UX, not security.

**Component boundaries.** A component that accepts more than 5 props is probably doing too much — extract or compose. Props should be typed, not `object` or `Record<string, any>`.

**Error states.** Every data-fetching component must handle: loading (skeleton or spinner), error (with message), empty (with empty state UI), and populated states. No component should render `null` on error silently.

---

## Example Tasks

**Add a new chart to TradeCopilot analytics page:**
File: `src/pages/analytics/`
Pattern: Create a new component accepting `AnalyticsResult` (from `src/utils/analytics.ts`) as props. Use Recharts (`ResponsiveContainer + LineChart` or `BarChart`). Numbers on axes: `font-mono`. P&L positive: `stroke={emerald-500}`, negative: `stroke={red-500}`. Import `useAnalytics` hook or derive from existing `useTrades` data — do not add a new Supabase query if the data already exists.

**Migrate TradeCopilot groq-ai edge function to Claude:**
1. Create new Supabase edge function `claude-ai/index.ts` using Anthropic SDK (`npm i @anthropic-ai/sdk`).
2. Add `cache_control: { type: "ephemeral" }` to the system prompt message block.
3. Update `src/services/ai/claudeApi.ts` to call `claude-ai` instead of `groq-ai`.
4. Replace model name `llama-3.3-70b-versatile` with `claude-haiku-4-5-20251001` for daily_review/pre_market, `claude-sonnet-4-6` for trading_dna.
5. Remove `REACT_APP_GROQ_API_KEY` from `.env`.
6. Rename `claudeApi.ts` to `claudeService.ts` for accuracy.

**Add a live position monitor to TradingBotwithAIAnalyzer dashboard:**
Reference: `D:\TradingBotwithAIAnalyzer\frontend\src\components\ContinuousMonitor.js`
Pattern: Poll `GET /api/trading/strategy_status` every 2 seconds. Map state string to pipeline stages (IDLE → SCANNING → DOJI_FOUND → TRADE_OPEN). Highlight active stage in Indigo-600. Show SL, entry, current price in JetBrains Mono. P&L in Emerald/Red per sign. Use `clearInterval` in `useEffect` cleanup.

**Build a new subscription gate for a Pro feature:**
Pattern: Wrap the feature component in a gate check:
```tsx
const { plan } = useSubscription();
if (plan === 'free') return <UpgradePrompt feature="Weekly AI Coaching" />;
return <WeeklyCoaching />;
```
`UpgradePrompt` shows feature name, benefit copy, and Razorpay checkout button. Never show a broken or empty component — always show a clear upgrade path.

**Fix a TypeScript error in a Supabase query result:**
Pattern: Define an explicit interface matching the schema columns you're selecting. If selecting `trades(id, entry_time, pnl)`, define:
```typescript
interface TradeRow { id: string; entry_time: string; pnl: number; }
const { data } = await supabase.from('trades').select('id, entry_time, pnl').returns<TradeRow[]>();
```
Never cast the result to `any`.
