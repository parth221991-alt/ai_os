# Quantara OS — Knowledge Architecture

**Version:** 3.1  
**Purpose:** Defines how Quantara stores, retrieves, updates, and uses knowledge — market data, system state, intelligence, learning, and configuration.

This document answers: *"What does Quantara know, where does it store it, how stale can it be, and who can change it?"*

---

## Knowledge Taxonomy

Quantara's knowledge falls into six categories:

| Category | Examples | Storage | Staleness Budget |
|---|---|---|---|
| **Financial State** | Positions, capital, orders, P&L | PostgreSQL (ACID) | Never stale — real-time |
| **Market Data** | OHLCV, ticks, options chain | MongoDB + Redis cache | Ticks: 5s; Options: 60s; OHLC: 1 candle |
| **Computed Intelligence** | Microstructure, regime, sector rankings | Redis (hot) + MongoDB (warm) | 5–7 minutes |
| **AI-Generated Context** | Scenarios, playbooks, investment thesis, news summaries | MongoDB + Redis cache | 2h–48h per type |
| **System State** | Kill switch, health, session, circuit breakers | Redis (fast access) + PostgreSQL (audit) | Real-time |
| **Learning** | Strategy stats, performance metrics, recommendations | MongoDB + PostgreSQL | Daily (not real-time) |

---

## Rule: What Reads What for Execution

```
Any execution decision (order placement) must read from:
  → Financial State     : PostgreSQL (positions, capital, risk_state)
  → Kill switch status  : Redis quantara:state:kill_switch (backed by PostgreSQL)
  → Reconciliation      : PostgreSQL reconciliation_log

Any signal evaluation reads from:
  → Regime context      : Redis quantara:cache:regime:current (max 7 min old)
  → Microstructure      : Redis quantara:cache:microstructure:{underlying} (max 6 min old)
  → Pre-market package  : Redis quantara:cache:premarket:{date} (same day only)
  → Sector rankings     : Redis quantara:cache:sector:rankings:{date} (max 2h old)

Any AI context reads from:
  → Redis hot cache FIRST
  → MongoDB warm cache if Redis miss
  → Claude API only if both miss (log cache miss, write result back to both)
```

---

## Financial State Knowledge (PostgreSQL)

### What it is
The authoritative record of everything that affects real money. This data is never stale, never cached for execution, and append-only where possible.

### Key tables and their update frequency

| Table | Update Frequency | Writer | Staleness Permitted |
|---|---|---|---|
| `positions` | On every fill, every modification | Execution Engine | None |
| `capital_accounts` | Daily (settlement) + on fill | Portfolio State Manager | None |
| `orders` | Every state transition | Execution Engine | None |
| `order_state_transitions` | Append-only, every transition | Execution Engine | None |
| `risk_state` | After every trade close | Tier 0 Risk Engine | None |
| `audit_trail` | BEFORE every action | All agents | None |
| `kill_switch_log` | On activation/reset | Tier 0 Risk Engine | None |
| `reconciliation_log` | Every reconciliation run | Reconciliation Engine | None |
| `system_checkpoints` | Every 5 minutes | System | 5 minutes |
| `strategy_parameters` | Human approval only | Ops (not learning agent) | N/A — manual |
| `learning_recommendations` | Weekly (learning agent) | Learning Agent only | Daily |

### Integer paise rule
All monetary values: INTEGER in paise. `₹1,234.56 = 123456`. No exceptions.
Display layer converts. Arithmetic always integer.

### Append-only discipline
`order_state_transitions`, `audit_trail`, `alert_log`, `kill_switch_log`: INSERT only. Never UPDATE or DELETE.
This makes these tables the authoritative history of system behavior.

---

## Market Data Knowledge (MongoDB + Redis)

### Data flow
```
Zerodha WebSocket → Market Data Validity Engine → MongoDB market_data + Redis cache
```

### Staleness budgets

| Data Type | Redis TTL | Staleness Limit | On Exceeded |
|---|---|---|---|
| Live tick | No cache (streaming) | 5 seconds | `is_valid = False` on data type |
| 1-minute candle | 600s | 1 candle | Invalidate downstream features |
| Options chain | 90s | 60 seconds | `MicrostructureSnapshot.is_valid = False` |
| Microstructure computed | 6 minutes | 7 minutes | Zero options weight in signal |
| Regime context | 7 minutes | 1 candle | Raise downstream thresholds +0.05 |

### MongoDB collections

| Collection | Document type | Retention |
|---|---|---|
| `market_data` | Daily OHLCV per instrument | Indefinite (learning data) |
| `options_data` | Options chain snapshots | 90 days (then aggregate) |
| `microstructure_analysis` | Computed GEX/max pain per 5-min bar | 30 days |

---

## AI-Generated Knowledge (MongoDB ai_cache + Redis)

### Cache-Before-Call Protocol
```
1. Deterministic cache key = hash(prompt_type + input_hash + date)
2. Check Redis hot cache → hit: return
3. Check MongoDB ai_cache → hit: promote to Redis, return
4. Miss: call Claude API
5. Write result to: MongoDB ai_cache + Redis
6. Log: model_used, tokens_in, tokens_out, cost_usd, cache_hit=false
```

### AI knowledge types and TTLs

| Knowledge Type | Model | Cache TTL | Written By | Read By |
|---|---|---|---|---|
| Intraday scenarios (3–5) | Haiku | 24 hours | Pre-Market Package | Intraday SMC+F&O Agent |
| Swing setup debates (up to 5) | Haiku | 24 hours | Pre-Market Package | Swing Alpha Agent |
| News summaries (batch) | Haiku | 4 hours | Intelligence Agent | All agents |
| Sector analysis | Haiku | 2 hours | Intelligence Agent | Swing + Investment agents |
| Pre-market CIO briefing | Haiku | 24 hours | Pre-Market Package | Dashboard |
| Earnings concall key points | Haiku | 24 hours | Intelligence Agent | Investment Alpha Agent |
| Investment thesis (per stock) | Sonnet | 48 hours | Investment Alpha Agent | Portfolio State Manager |
| Post-trade postmortem (batch) | Sonnet | Permanent | Learning Agent | Human review |
| Weekly learning synthesis | Sonnet | Permanent | Learning Agent | Human review |

### Cache invalidation rules
- News summaries: invalidated if new major event detected (black swan trigger)
- Intraday scenarios: expire at market close (24h TTL covers single day only)
- Investment thesis: invalidated on REDUCE or EXIT signal (thesis changed)
- Postmortems: never invalidated (permanent record)

### When Claude is unavailable

| Knowledge Type | Fallback Behavior |
|---|---|
| Intraday scenarios | Use yesterday's cached scenarios |
| Swing debate | Skip — raise confidence threshold +0.10 for today |
| Investment thesis | Block new INITIATE decisions. Existing positions rule-based. |
| News summaries | Skip news signal component entirely |

Rule: Claude unavailability NEVER halts intraday or swing trading.

---

## System State Knowledge (Redis)

### State key map

| Key | Content | TTL | Update Frequency |
|---|---|---|---|
| `quantara:state:session:zerodha` | UNINITIALIZED/AUTHENTICATING/ACTIVE/... | None | On transition |
| `quantara:state:health:system` | HEALTHY/WARNING/CRITICAL/OFFLINE | None | Every 30s |
| `quantara:state:risk:daily` | Current daily P&L, drawdown, loss count | None | After every trade |
| `quantara:state:kill_switch` | Level (0/1/2/3), reason, reset_hash | None | On activation/reset |
| `quantara:state:circuit_breakers:{svc}` | CLOSED/OPEN/HALF_OPEN | None | On failure/recovery |
| `quantara:state:data_validity:{type}` | VALID/STALE/INVALID per data type | None | Per validation cycle |

### Reconciliation checkpoint
`system_checkpoints` in PostgreSQL written every 5 minutes. On warm start:
1. Load checkpoint
2. Reconcile with Zerodha positions
3. If match → resume
4. If mismatch → HALT, require human

---

## Configuration Knowledge (YAML + PostgreSQL)

### Three-layer configuration model

| Layer | Location | Can be changed by | Takes effect |
|---|---|---|---|
| **Layer 1 — Immutable constants** | Python code (`constants.py`) | Code deployment only | On next deployment |
| **Layer 2 — Environment/YAML** | `configs/*.yaml` + `.env` | Ops team, with ADR | On restart |
| **Layer 3 — Runtime** | `strategy_parameters` PostgreSQL table | API endpoint (authenticated) | Immediately |

**Layer 1 constants (hardcoded, cannot be changed without redeployment):**
- Confidence floor: 0.50
- RR floor: 2.0
- Margin utilization ceiling: 70%
- Max simultaneous flatten orders: staggered at 500ms
- No trading window: 9:15–9:30, 15:25–15:30

**Layer 2 YAML files (change requires restart + human approval):**

| File | Governs |
|---|---|
| `configs/risk.yaml` | Kill switch thresholds, sizing multipliers, drawdown table |
| `configs/confidence.yaml` | Grade thresholds (A/B/C/D), component weights |
| `configs/execution.yaml` | Slippage model, fill logic, strike selection |
| `configs/setups.yaml` | OPA/PES/SFR time windows and thresholds |
| `configs/features.yaml` | Feature computation parameters |
| `configs/telegram.yaml` | Notification delivery settings |
| `configs/system.yaml` | App env, market hours, execution_enabled gate |
| `configs/database.yaml` | Pool settings, Redis TTLs |
| `configs/learning.yaml` | Clustering, review settings |
| `configs/replay.yaml` | Determinism settings |
| `configs/events.yaml` | Macro event calendar (to be created) |
| `configs/monitoring.yaml` | Alert thresholds (to be created) |
| `configs/portfolio.yaml` | Allocation targets, concentration limits (to be created) |
| `configs/swing.yaml` | Swing entry thresholds, hold limits (to be created) |

**Layer 3 runtime parameters (API-adjustable, human auth required):**
- Signal weight adjustments (±20% of Layer 2 baseline)
- Confidence thresholds (within defined range)
- Sizing multipliers (±10% of baseline)
- No-trade filter parameters

**Learning service CANNOT write Layer 2 or Layer 3.** Database permission on PostgreSQL `strategy_parameters` is read-only for the learning service user. Recommendations go to `learning_recommendations` only.

---

## Learning Knowledge (MongoDB + PostgreSQL)

### What learning knows
- Historical signal quality per strategy type (win rate, expectancy, Brier score)
- Regime-specific performance (which setups work in which regimes)
- Directional bias detection (long vs short win rate differential)
- Anti-drift monitoring (regime balance in training window)

### Learning governance flow
```
1. Learning Agent: analyze past week's signals → MongoDB learning_metrics
2. Generate recommendations → PostgreSQL learning_recommendations
3. Shadow mode comparison: new params vs current on past data
4. Human reviews: approve / reject each recommendation
5. Approved: deploy to staging for 5 trading days
6. If staging matches expectation: promote to production (Layer 3 update)
7. Any promoted change can be reverted in < 5 minutes
```

**What learning can change:** Signal weights (±20%), confidence thresholds (within range), sizing multipliers (±10%), no-trade filter parameters.

**What learning cannot change:** Any Tier 0 component, hard risk limits, order execution logic, capital allocation targets, core strategy logic.

---

## Explainability Knowledge (MongoDB signals collection)

### Every signal must carry

Per Rule 13: every signal stored in MongoDB `signals` must contain a complete explainability block. This is the record of why a trade was (or wasn't) taken.

```python
# Written at signal time (multiple components populate their section)
ExplainabilityBlock:
  why_trade          → WeightedSignalEngine
  why_not_rejected   → PreSubmissionGuard (after all 13 checks pass)
  counter_argument   → Pre-market scenario bear case (cached)
  risk_factors       → Tier 0 Risk Engine
  confidence_breakdown → WeightedSignalEngine (per-component before weighting)
  regime_context     → RegimeEngine snapshot at signal time
  scenario_match     → Pre-market package cache lookup
  trade_grade        → ProbabilityEngine (A/B/C/D)

# Written at close
PostTradeWriteback:
  actual_outcome         → Execution Engine
  actual_return_pct      → Execution Engine
  confidence_was_accurate → Learning Agent (post-analysis)
  primary_failure_reason  → Learning Agent
  learning_flags          → Learning Agent
```

### Query patterns
- "Why did this trade fire?" → `signals.{trace_id}.why_trade`
- "Why wasn't it rejected?" → `signals.{trace_id}.why_not_rejected`
- "What was the regime at entry?" → `signals.{trace_id}.regime_context`
- "Did the confidence predict the outcome?" → join `signals.confidence` vs `signals.post_trade.actual_outcome`

---

## Knowledge Freshness Contract

Every component that consumes knowledge must check freshness before using it.

| Consumer | Knowledge it consumes | Freshness check |
|---|---|---|
| Intraday SMC+F&O Agent | Regime context | `now() < regime.valid_until` |
| Intraday SMC+F&O Agent | Microstructure | `snapshot.data_age_seconds < 360` |
| Intraday SMC+F&O Agent | Pre-market scenarios | `cache_date == today()` |
| Swing Alpha Agent | Sector rankings | Redis TTL (2h max) |
| Swing Alpha Agent | Pre-market swing debate | `cache_date == today()` |
| All execution agents | Position state | Always read PostgreSQL — never cache |
| All execution agents | Kill switch state | Redis `quantara:state:kill_switch` (no TTL, always current) |
| Portfolio State Manager | Capital figures | Always read PostgreSQL `capital_accounts` |

---

## Knowledge Audit Trail

Every action that touches financial state is preceded by an audit trail entry in PostgreSQL. This is Rule 8 and it is never violated.

```
BEFORE order submission:
  INSERT INTO audit_trail (action="ORDER_ATTEMPT", order_spec, timestamp)
  
BEFORE kill switch activation:
  INSERT INTO audit_trail (action="KILL_SWITCH_TRIGGER", level, reason, timestamp)
  
BEFORE reconciliation decision:
  INSERT INTO audit_trail (action="RECONCILIATION_DECISION", outcome, evidence, timestamp)
  
BEFORE learning parameter promotion:
  INSERT INTO audit_trail (action="PARAMETER_CHANGE", old_value, new_value, approved_by, timestamp)
```

This means: if a crash occurs between the audit trail write and the action, the investigation starts with a known, committed intent record.
