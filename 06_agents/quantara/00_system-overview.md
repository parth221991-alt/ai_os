# Quantara Agent System — Overview

**Version:** 3.1 (aligned with QUANTARA_OS_MASTER.md)
**Source of truth:** `D:\AI_OS\06_agents\quantara\QUANTARA_OS_MASTER.md`

This document defines the formal agent architecture for Quantara OS — a three-book Personal Hedge Fund Operating System.

---

## System Scope

Quantara manages three capital books:

| Book | Allocation | Timeframe | Alpha Source |
|---|---|---|---|
| Investment | 40–60% | 3 months → multi-year | Investment Alpha Agent |
| Swing | 15–30% | 2–30 days | Swing Alpha Agent |
| Intraday / F&O | 10–30% | Minutes → intraday | Intraday SMC+F&O Agent |
| Cash Reserve | 10% min | Always | N/A — never traded |

The agent system operates across four tiers:

| Tier | Role | Agents |
|---|---|---|
| **Tier 0** | Survivability Foundation | Emergency Flatten Service (standalone) |
| **Tier 1** | Alpha Generation | Context/Regime Agent, Intraday SMC+F&O Agent, Market Microstructure Agent, Swing Alpha Agent, Investment Alpha Agent, Execution Engine |
| **Tier 2** | CIO Allocation | Portfolio State Manager (cross-book) |
| **Tier 3** | AI Intelligence | Intelligence/News Agent, Claude Model Router |
| **Tier 4** | Learning | Learning Agent (recommendations only) |

---

## Agent Inventory

### Existing (Implemented or Partially Implemented)

| Agent File | Agent | Status | Tier |
|---|---|---|---|
| `02_regime-agent.md` | Context / Regime Engine | PARTIALLY IMPLEMENTED | 1 |
| `03_signal-agent.md` | Intraday SMC + F&O Agent | IMPLEMENTED (formalized) | 1 |
| `05_risk-agent.md` | Tier 0 Risk Engine + Kill Switch | IMPLEMENTED (needs upgrade to 3-level) | 0 |
| `07_execution-agent.md` | Execution Engine (Paper) | PARTIALLY IMPLEMENTED | 1 |
| `08_monitoring-agent.md` | Monitoring / Alert System | PARTIALLY IMPLEMENTED | 0 |

### New (Not Yet Implemented)

| Agent File | Agent | Status | Tier |
|---|---|---|---|
| `01_news-agent.md` | Intelligence / News Agent | NOT IMPLEMENTED | 3 |
| `04_debate-agent.md` | Pre-Market Scenario & Debate | NOT IMPLEMENTED | 3 |
| `06_portfolio-agent.md` | CIO Portfolio State Manager | NOT IMPLEMENTED | 2 |
| `09_investment-alpha-agent.md` | Investment Alpha Agent | NOT IMPLEMENTED | 1 |
| `10_swing-alpha-agent.md` | Swing Alpha Agent | NOT IMPLEMENTED | 1 |
| `11_microstructure-agent.md` | Market Microstructure Agent | NOT IMPLEMENTED | 1 |
| `12_emergency-flatten-service.md` | Emergency Flatten Service | NOT IMPLEMENTED | 0 |

---

## Shared Interface Contracts

All agents communicate through typed data contracts. No agent reads internal state of another agent directly.

### Market Data Contracts

```python
# app/ingestion/schemas.py
MarketTick           # Normalized broker tick
Candle1M             # 1-minute OHLCV (source of truth)
CandleHTF            # Derived 5m/15m/1h/4h candle
FeedHealth           # GOOD | WARNING | CRITICAL | SAFE_MODE

# app/features/schemas.py
FeatureVector        # 13+ intraday features (P_DIV, RS_spread, PMP, RVI, ...)

# app/liquidity/schemas.py
LiquidityContext     # Sweep, MSS, BOS, FVG, HTF alignment (intraday)
```

### Regime Contract (Tier 1 output)

```python
@dataclass(frozen=True)
class RegimeContext:
    trend_state: str           # trending_bullish | trending_bearish | range | breakout
    volatility_state: str      # low | normal | elevated | extreme
    market_bias: str           # bullish | bearish | neutral
    breadth_state: str         # strong | weak | diverging
    expiry_proximity: bool
    event_flag: bool
    regime_confidence: float   # 0.0 to 1.0
    valid_until: datetime      # Stale if now() > valid_until
```

### Signal Contracts

```python
# Intraday (existing)
SignalDecision       # setup, direction, confidence, grade (A/B/C/D), reasons
NoTradeResult        # reason_codes, is_hard_gate, is_pre_submission_failure

# New (multi-book)
SwingSignal          # symbol, direction, confidence, entry_zone, target, stop
InvestmentSignal     # symbol, action (INITIATE/ADD/REDUCE/EXIT/HOLD), confidence, thesis_id

# Execution
ExecutionPlan        # entry, SL, TP1, TP2, quantity, risk_amount_paise, idempotency_key
TradeState           # sub_state, entry_price, current_price, sl, MFE, MAE
```

### Risk and Portfolio Contracts

```python
KillSwitchState      # level (0/1/2/3), reason, activated_at, reset_code_hash
PortfolioState       # capital per book, open heat, cross-book exposure, drawdown

# Order lifecycle (PostgreSQL)
Order                # idempotency_key, state (CREATED→SUBMITTED→ACKNOWLEDGED→FILLED...)
Position             # book, symbol, quantity, entry_price_paise, strategy_type
```

### Intelligence Contracts

```python
RegimePackage        # Pre-market: scenarios, playbooks, sector rankings, risk events
MacroEvent           # event_type, datetime, severity, blackout_window
IntraScenario        # name, probability, playbook, bull_case, bear_case
```

### Explainability Block (Rule 13 — every signal)

```python
@dataclass
class ExplainabilityBlock:
    why_trade: List[str]
    why_not_rejected: List[str]       # Populated by 13-check guard (all 13 passed)
    counter_argument: List[str]       # From pre-market scenario bear case
    risk_factors: List[str]
    confidence_breakdown: Dict[str, float]
    regime_context: RegimeContext
    scenario_match: ScenarioMatch
    trade_grade: str                  # A / B / C / D
    generated_by: str                 # agent name
    post_trade: Optional[PostTradeWriteback]  # Written on close
```

### Standard AgentDecision (all agents)

```python
@dataclass(frozen=True)
class AgentDecision:
    agent_id: str
    trace_id: UUID
    timestamp: datetime
    verdict: str                # PROCEED | BLOCK | WARN | ABSTAIN
    confidence: float           # 1.0 for deterministic agents
    reasons: List[str]
    blocking_reasons: List[str]
    metadata: Dict[str, Any]
```

---

## Communication Architecture

### Tier 0 (Survivability) — Synchronous, PostgreSQL-backed

Tier 0 components are NOT on the event bus. They are synchronous guards:

```
Every order submission → Pre-Submission Guard (13 checks) → Idempotency Engine → Zerodha API
                                   ↑
                            Risk Engine (hard limits)
                                   ↑
                            Reconciliation status check
```

### Tier 1–3 — Async Event Bus (Redis Streams)

```
                    ┌──────────────────────────────────────────┐
                    │         Market Data Ingestion            │
                    │  Ticks → Candles → Features → Regime     │
                    └──────────────┬───────────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────────┐
                    │           Redis Streams (Event Bus)       │
                    │   quantara:stream:market_events           │
                    │   quantara:stream:signals                 │
                    │   quantara:stream:orders                  │
                    │   quantara:stream:alerts                  │
                    └────┬──────┬────────┬──────────┬──────────┘
                         │      │        │          │
              ┌──────────▼┐  ┌──▼──────┐  ┌────────▼──┐  ┌──▼─────────┐
              │ Intraday  │  │  Swing  │  │Investment │  │ Portfolio  │
              │  SMC+F&O  │  │  Alpha  │  │   Alpha   │  │   State    │
              │   Agent   │  │  Agent  │  │   Agent   │  │  Manager   │
              └──────┬────┘  └────┬────┘  └─────┬─────┘  └────────────┘
                     │            │              │
                     └────────────┴──────┬───────┘
                                         │ all signals → quantara:stream:signals
                              ┌──────────▼──────────┐
                              │   Execution Engine  │
                              │  (pre-sub guard →   │
                              │   idempotency →     │
                              │   Zerodha API)      │
                              └──────────┬──────────┘
                                         │ → quantara:stream:orders
                              ┌──────────▼──────────┐
                              │   Monitoring Agent  │
                              │   (always active)   │
                              └─────────────────────┘
```

### Intelligence Layer (Tier 3) — Non-blocking, Pre-computed

```
Intelligence Agent runs 24/7 on a separate schedule:
  8:30 AM → Macro data collection
  8:40 AM → News batch + Haiku summarization
  8:45 AM → Options chain pre-open analysis
  8:50 AM → Sector strength ranking
  8:55 AM → Regime preliminary assessment
  9:00 AM → Intraday scenario generation (Haiku: 3-5 scenarios + playbooks)
  9:05 AM → Risk limit refresh
  9:08 AM → Swing position review
  9:10 AM → Pre-market package cached to Redis. System declared READY.

All cached to Redis. Execution agents READ cache. They never call Claude directly.
```

---

## Redis Key Architecture

### State Keys (No TTL — explicit management)

```
quantara:state:session:zerodha          — Zerodha session state machine
quantara:state:health:system            — Overall system health
quantara:state:risk:daily               — Daily risk metrics
quantara:state:circuit_breakers:{svc}  — Per-service circuit breakers
quantara:state:data_validity:{type}    — Per-data-type validity flags
```

### Cache Keys (TTL-based)

```
quantara:cache:regime:current                   TTL: 7 minutes
quantara:cache:premarket:{date}                 TTL: 24 hours
quantara:cache:options:chain:{underlying}       TTL: 90 seconds
quantara:cache:microstructure:{underlying}      TTL: 6 minutes
quantara:cache:ai:{cache_key}                   TTL: per prompt type (see model routing)
quantara:cache:scenarios:intraday:{date}        TTL: 24 hours
quantara:cache:scenarios:swing:{date}           TTL: 24 hours
quantara:cache:sector:rankings:{date}           TTL: 2 hours
```

### Streams (Event Bus)

```
quantara:stream:market_events           — Ticks, candle closes
quantara:stream:signals                 — All signals from all books
quantara:stream:orders                  — Order lifecycle events
quantara:stream:alerts                  — System alerts (all levels)
```

### Kill Switch (No TTL)

```
quantara:state:kill_switch              — Level (0/1/2/3), reason, reset_code_hash
```

---

## Database Split Reference

| What | Where | Why |
|---|---|---|
| All positions | PostgreSQL | ACID — affects money |
| All orders | PostgreSQL | Idempotency, audit trail |
| Capital per book | PostgreSQL | Settlement-aware |
| Risk state | PostgreSQL | Kill switch source of truth |
| OHLC / tick history | MongoDB | Schema-flexible, analytical |
| Options chain snapshots | MongoDB | High-volume, analytical |
| Microstructure analysis | MongoDB | Computed, not transactional |
| All signals (with explainability) | MongoDB | Rich documents, not normalized |
| Pre-market packages | MongoDB | Document structure |
| Claude cache | MongoDB | TTL + schema-free |
| Learning metrics | MongoDB | Analytical |
| Feature/regime cache | Redis | Ephemeral, sub-second |
| AI output cache | Redis (hot) + MongoDB (warm) | Cache-before-call protocol |

---

## Agent Activation Schedule

```
System startup (before market hours)
  → Tier 0 verification (PostgreSQL, MongoDB, Redis, Zerodha session)
  → Only if Tier 0 HEALTHY: proceed

8:00 AM  — Intelligence Agent: load news, macro calendar, global markets
8:30 AM  — Pre-market package begins (see schedule above)
9:00 AM  — Intraday scenario cache populated
9:05 AM  — Risk limits refreshed, drawdown state updated
9:10 AM  — System declared READY (or CAUTIOUS if package incomplete)
9:14 IST — Portfolio State Manager: initialize session, load positions
9:15 IST — Market opens (read-only: no orders 9:15–9:30)
9:30 IST — Trading begins

09:30+   — Intraday SMC+F&O Agent: active per 5-minute candle
09:30+   — Swing Alpha Agent: monitors watchlist
09:30+   — Context/Regime Engine: updates every 5-minute candle
Any time — Market Microstructure Agent: updates every 5 minutes
Any time — Investment Alpha Agent: processes new data (not time-bound)

15:20 IST — EOD square-off: all intraday positions force-closed
15:25 IST — No new positions
15:30 IST — Market close, reconciliation, session summary

Always   — Monitoring Agent: health checks, alerts, status writes
Always   — Tier 0 Risk Engine: hard limit guardian
```

---

## Claude Integration Points

| Agent | Model | When | Latency Budget | Cache Strategy |
|---|---|---|---|---|
| Intelligence Agent | claude-haiku-4-5-20251001 | Pre-market batch | No budget (non-blocking) | 4–24 hours |
| Pre-Market Scenarios | claude-haiku-4-5-20251001 | Daily 9:00 AM | No budget | 24 hours |
| Swing Debate | claude-haiku-4-5-20251001 | Pre-market batch, ≤5 setups/call | No budget | 24 hours |
| Investment Thesis | claude-sonnet-4-6 | Per new INITIATE decision | No budget (async) | 48 hours |
| Conflicting Signals | claude-sonnet-4-6 | Per occurrence | No budget (async) | No cache |
| Post-trade Postmortem | claude-sonnet-4-6 | Batch of 3, weekly | No budget | Permanent |
| Weekly Learning | claude-sonnet-4-6 | Weekly | No budget | Permanent |

**Absolute rule: No Claude call is ever on the critical path for intraday or swing execution. All Claude outputs are pre-computed and cached before market hours.**

---

## Non-Negotiable System Rules

1. No LLM in any execution critical path. Claude assists intelligence, never execution.
2. Every AgentDecision logged to PostgreSQL `audit_trail` before any downstream action.
3. Kill switch Level 2+ is a hard stop. No agent bypasses it.
4. Paper mode is default. Execution checks `execution_enabled` before every order.
5. Replay parity must hold. All agent decisions deterministic given same inputs.
6. PostgreSQL is the only source of truth for monetary state.
7. All monetary values in integer paise. No floats.
8. Every order has an idempotency key. Created in PostgreSQL BEFORE Zerodha API call.
9. Reconciliation status must be CLEAN before any order in production.
10. Emergency Flatten Service has zero imports from main backend.
