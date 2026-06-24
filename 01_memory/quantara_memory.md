# Quantara OS — Project Memory

**Last Updated:** 2026-06-08  
**Version:** Aligned with QUANTARA_OS_MASTER.md v3.1 (frozen)  
**Status:** Architecture frozen. Implementation: Phase 1 (not started).

---

## Project Overview

Quantara is a **Personal Hedge Fund Operating System** — not an intraday signal engine. It operates three capital books autonomously (Investment, Swing, Intraday/F&O) with a target of ₹5 crore under management. The system acts as a CIO, allocating capital across books based on opportunity quality and risk state.

**Core insight:** Probability engine, not a prediction engine. Every decision must be traceable through logs. Determinism, auditability, and survival take priority over raw alpha.

**Production target:** AWS Lightsail Mumbai (4GB, 2vCPU, 50GB SSD, Ubuntu 22.04), systemd, Nginx.

---

## Business Context

- Solo founder operation — every complexity has a maintenance cost
- Three books: Investment (wealth compounding), Swing (trend capture), Intraday F&O (high-frequency alpha)
- Subscriber signal delivery via Telegram is an eventual revenue stream
- Paper trading minimum: **40 trading days** with statistical significance (not calendar weeks)
- Live capital cannot deploy until all Phase 1 Definition of Done items pass

---

## Capital Allocation Model

| Book | Target Allocation | Notes |
|---|---|---|
| Investment | 40–60% | Long-term equity, Sonnet thesis per INITIATE |
| Swing | 15–30% | Overnight holds, Haiku pre-market debate |
| Intraday/F&O | 10–30% | NIFTY weekly options, no Claude at execution time |
| Cash Reserve | 10% minimum | Hard floor — never deployed |

**Capital Graduation:**
- Stage 0 (Paper): 40 trading days, ≥60% intraday WR, no errors 5 consecutive days
- Stage 1 (₹2–5L): Intraday only, 1 position, 4 weeks, <10% drawdown
- Stage 2 (₹10–25L): + Swing, 3 positions max, 8 weeks, Sharpe >1.0
- Stage 3 (₹5 Cr): All three books, continuous monitoring

---

## Current State

**Phase:** Pre-Phase 1 (architecture frozen, no code written yet)  
**What exists:** Complete specification documentation in `D:\AI_OS\06_agents\quantara\`  
**What doesn't exist:** Any production code, database schemas, deployed services

**Documentation inventory:**
- `QUANTARA_OS_MASTER.md` — v3.1 master spec (frozen)
- `00_system-overview.md` — Agent inventory, event bus, state keys
- `04_debate-agent.md` — Pre-market scenario agent (Tier 3)
- `05_risk-agent.md` — Tier 0 risk engine spec
- `06_portfolio-agent.md` — Portfolio State Manager (Tier 2)
- `09_investment-alpha-agent.md` — Investment Alpha Agent
- `10_swing-alpha-agent.md` — Swing Alpha Agent
- `11_microstructure-agent.md` — Market Microstructure Agent
- `12_emergency-flatten-service.md` — Emergency Flatten (standalone)
- `ROADMAP.md` — 5-phase implementation roadmap
- `KNOWLEDGE_ARCHITECTURE.md` — Storage, freshness, and access rules

---

## System Architecture

### Four-Tier Design

| Tier | Name | Key Components |
|---|---|---|
| Tier 0 | Survivability Foundation | Kill switch, reconciliation, risk engine, emergency flatten |
| Tier 1 | Alpha Generation | Intraday SMC+F&O agent, execution engine, regime engine |
| Tier 2 | CIO Allocation | Portfolio State Manager, swing agent, investment agent |
| Tier 3 | AI Intelligence | Pre-market package, debate/scenarios, news, sector ranking |
| Tier 4 | Learning | Learning agent, performance analysis, parameter recommendations |

### Service Topology
```
Nginx → FastAPI:8000 → [Tier 0-4 agents] → Zerodha API
                     → Emergency Flatten:8001 (standalone)
                     → PostgreSQL 15 / MongoDB 6 / Redis 7
```

### Database Split Rule
- **PostgreSQL 15**: ALL financial state — positions, orders, capital, risk_state, audit_trail, kill_switch_log, reconciliation_log, system_checkpoints, strategy_parameters, learning_recommendations
- **MongoDB 6**: Intelligence and analytical — market_data, options_data, microstructure_analysis, signals, intelligence_feed, premarket_packages, learning_metrics, ai_cache, system_logs
- **Redis 7**: Ephemeral cache + event bus — regime, scenarios, options chain, microstructure, AI cache hot tier
- **RULE:** Financial state → always PostgreSQL. Redis is never authoritative for execution decisions.

---

## Agent System (13 Agents)

| # | Agent | Tier | Claude? | Notes |
|---|---|---|---|---|
| 00 | System Overview | — | No | Architecture document |
| 01 | News/Intelligence | 3 | Haiku | Batch news summarization, 4h TTL |
| 02 | Zerodha Session Manager | 0 | No | 5-state FSM, heartbeat, reconnect |
| 03 | Regime/Context Engine | 1 | No | ADX, ATR, VIX, regime output |
| 04 | Pre-Market Scenario/Debate | 3 | Haiku | 9:00 AM batch, cached 24h |
| 05 | Tier 0 Risk Engine | 0 | No | 8 hard checks, kill switch, drawdown sizing |
| 06 | Portfolio State Manager | 2 | No | 3-book CIO, sector concentration |
| 07 | Intraday SMC+F&O | 1 | No (uses cache) | OPA/PES/SFR setups |
| 08 | Weighted Signal Engine | 1 | No | Regime-adaptive weights |
| 09 | Investment Alpha | 2 | Sonnet | 48h thesis TTL, 4-factor scoring |
| 10 | Swing Alpha | 2 | Haiku | Overnight screener, pre-market debate |
| 11 | Market Microstructure | 1 | No | GEX, max pain, OI dynamics |
| 12 | Emergency Flatten Service | 0 | No | Standalone process, port 8001 |

---

## Key Components

### 3-Level Kill Switch

| Level | Effect | Reset Method |
|---|---|---|
| Level 1 | No new entries, existing positions managed | API endpoint (authenticated) |
| Level 2 | All trading blocked, monitoring active | API endpoint + two-factor |
| Level 3 | Emergency flatten triggered | Manual system restart ONLY — no API reset |

### 13-Check Pre-Submission Guard
All 13 checks must pass. Any failure = REJECTED. No exceptions.
1. Kill switch at Level 0
2. Capital available
3. Margin sufficient (settlement-aware, paise arithmetic)
4. Duplicate order check (idempotency key)
5. Position limit check
6. Daily loss limit check
7. Reconciliation clean (no discrepancy flag)
8. Data validity (market data VALID, not STALE)
9. Options chain freshness (<60s)
10. Market hours (not in no-trade window)
11. Confidence floor ≥ 0.50
12. RR floor ≥ 2.0
13. Margin utilization ceiling <70%

### Trade Grades

| Grade | Confidence | RR Required | Action |
|---|---|---|---|
| A+ | ≥ 0.82 | ≥ 2.5 | Full size |
| A | ≥ 0.72 | ≥ 2.0 | Standard size |
| B | ≥ 0.65 | ≥ 2.0 | Reduced size |
| D | Below floors | Any | BLOCKED |

### Emergency Flatten Service
- Standalone Python process, port 8001
- **ZERO imports from main quantara backend**
- Own requirements.txt: fastapi, uvicorn, asyncpg, kiteconnect, pydantic, python-dotenv
- systemd `Requires: postgresql.service` ONLY — independent of MongoDB, Redis, main backend
- Reads positions directly from Zerodha (bypasses internal state)
- Authorization: one-time hash, wrong code = 403, no retries
- Order stagger: 500ms between each order

### Drawdown-Adjusted Sizing

| Drawdown | Size Multiplier |
|---|---|
| 0–5% | 1.0× (full) |
| 5–10% | 0.75× |
| 10–15% | 0.50× |
| 15–20% | 0.25× |
| >20% | 0.0× (HALT) |

### Consecutive Loss Governor (rolling 60-min window)
- 2 losses: −25% size
- 3 losses: −50% size + CRITICAL alert
- 4 losses: pause 2 hours
- 5 losses: halt for day

---

## Immutable Constants (Layer 1 — cannot change without redeployment)

- Confidence floor: **0.50** — absolute minimum, no exceptions
- RR floor: **2.0** — no trade below this ratio
- Margin utilization ceiling: **70%**
- Max simultaneous flatten stagger: **500ms**
- No-trade windows: **9:15–9:30** and **15:25–15:30**

---

## Important Constraints

1. **Integer paise rule**: All monetary values are INTEGER in paise. `₹1,234.56 = 123456`. Float arithmetic on money is **BANNED**. Display layer converts.
2. **Claude never on critical path**: Engineering Rule 6 — no live Claude call at execution time for intraday or swing. All AI context is pre-cached.
3. **Audit trail before action**: Rule 8 — INSERT into `audit_trail` BEFORE every action that affects money.
4. **Append-only tables**: `order_state_transitions`, `audit_trail`, `alert_log`, `kill_switch_log` — INSERT only, never UPDATE or DELETE.
5. **Emergency Flatten independence**: If the main backend crashes, the flatten service must still work. Zero shared code.
6. **Learning cannot write strategy_parameters**: DB-level permission enforcement. Learning service writes to `learning_recommendations` only.
7. **Paper trading minimum**: 40 trading days with statistical significance testing. Not a calendar estimate.
8. **Level 3 kill switch**: Requires manual system restart. No API reset path.
9. **No intrabar entries**: All entries on candle close only.
10. **EOD square-off**: All intraday positions by 15:25 IST.

---

## Claude Integration

| Knowledge Type | Model | Cache TTL | Fallback |
|---|---|---|---|
| Intraday scenarios | Haiku | 24h | Yesterday's cached scenarios |
| Swing debate | Haiku | 24h | Skip — raise threshold +0.10 |
| News summaries | Haiku | 4h | Skip news component entirely |
| Sector analysis | Haiku | 2h | Rule-based ranking |
| Investment thesis | Sonnet | 48h | Block new INITIATE, existing rule-based |
| Post-trade postmortems | Sonnet | Permanent | Queue for next batch |
| Weekly synthesis | Sonnet | Permanent | Defer to next week |

**Cache-before-call protocol:**
1. Deterministic key = hash(prompt_type + input_hash + date)
2. Check Redis hot cache → hit: return
3. Check MongoDB warm cache → hit: promote to Redis, return
4. Miss: call Claude API, write to both caches, log cost

**Target model distribution:** 90–95% Haiku, 5–10% Sonnet. Mandatory batching: 20 headlines → 1 call.

---

## Architecture Decisions (Key)

- **PostgreSQL for financial state**: ACID guarantees, no eventual consistency on money
- **MongoDB for intelligence**: Flexible schema for signals, scenarios, AI cache
- **Redis for hot cache + event bus**: Sub-millisecond access for execution path
- **Pre-cached scenarios (not real-time Claude)**: Engineering Rule 6 — Claude latency unacceptable at execution
- **Standalone Emergency Flatten**: Main backend failure must not affect position closure
- **Systemd over Docker for production**: Simpler restart semantics on single VPS
- **Integer paise**: Eliminates floating-point rounding on monetary arithmetic

---

## Known Risks

1. **Open Question #1**: Zerodha TOTP — fully automated or semi-manual 8 AM? Not yet decided.
2. **Open Question #2**: Fill timeout (45s, ambiguous status) — wait or cancel? Not decided.
3. **Open Question #4**: Stage 1 max daily loss in absolute rupees — not hardcoded yet.
4. **Open Question #6**: Primary options chain data source — Zerodha sufficient or external vendor?
5. **Open Question #7**: Exact paper trading statistical success criteria (Sharpe, WR, sample size)?
6. **Open Question #8**: Learning reviewer identity — who approves parameter recommendations?
7. **MACRO_EVENT gap**: `NoTradeReason.MACRO_EVENT` exists in the signal system but no agent currently generates it. News Agent spec (01_news-agent.md) is intended to fill this.
8. **Phase 1 is the longest**: Tier 0 survivability requires all safety systems before any signal logic.

---

## Future Opportunities

- Expansion to equity intraday (not just F&O) once books are established
- Subscriber signal delivery via Telegram (revenue stream)
- Portfolio analytics dashboard (Phase 5)
- Learning governance enabling autonomous parameter optimization (Phase 4)

---

## Open Questions

See `ROADMAP.md` — 8 questions listed, all required before Stage 1 live deployment.

---

## Important Learnings

- The system's value is not alpha generation alone — it is the **combination of alpha + risk control + auditability** that makes it institutional-grade.
- Black Swan Protocol: do NOT auto-flatten into a black swan. Stop-widening is the correct response. Auto-flatten into a black swan locks in losses at the worst possible price.
- Capital preservation mode (50% of max daily loss reached) is separate from and less severe than kill switch activation.
- The pre-market intelligence package must complete by 9:10 AM every day — it is the dependency for every first signal of the day.
- HOLD is not a default state for Investment positions — every hold requires a documented reason.
