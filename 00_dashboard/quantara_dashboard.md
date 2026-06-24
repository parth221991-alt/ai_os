# Quantara Dashboard — Specification

**Audience:** Founder (as CIO)  
**Purpose:** Business-level view of Quantara's performance — NOT execution-level  
**Update frequency:** Daily (after market close)  
**Critical rule:** This dashboard OBSERVES Quantara. It does NOT control it.

---

## What This Dashboard Shows (Business View)

```
┌──────────────────────────────────────────────────────────┐
│  QUANTARA OS                              [DATE]          │
│  Phase: PAPER TRADING  |  Day: N of 40 minimum           │
├────────────────┬─────────────────┬────────────────────────┤
│ TODAY          │ THIS WEEK       │ PAPER CUMULATIVE        │
│ P&L: ₹___      │ P&L: ₹___       │ P&L: ₹___              │
│ Trades: N      │ Win Rate: N%    │ Win Rate: N%            │
│ Result: W/L    │ Sharpe: N       │ Brier: N               │
├────────────────┴─────────────────┴────────────────────────┤
│ REGIME: [BULL_TRENDING / RANGE_BOUND / BEAR / RISK_OFF]   │
│ Book Allocation: INV N% | SWG N% | INTRA N% | CASH N%    │
├───────────────────────────────────────────────────────────┤
│ SYSTEM HEALTH                                              │
│ Backend: 🟢  |  Paper Gate: ACTIVE  |  Kill Switch: L0    │
│ Pre-market package: ✓ Complete by 9:10 AM                 │
├───────────────────────────────────────────────────────────┤
│ PAPER GATE CRITERIA (40 trading days minimum)             │
│ Days elapsed: N | Win rate: N% (≥60% req) | Errors: N/5  │
│ Progress: ████████░░░░░░░ N%                              │
└───────────────────────────────────────────────────────────┘
```

---

## Data Specification

### Performance Metrics
| Metric | Source | Notes |
|---|---|---|
| Daily P&L | Quantara trade logs | In paise → convert to ₹ for display |
| Win rate | Quantara trade logs | Rolling N trades |
| Sharpe ratio | Quantara performance report | Weekly calculation |
| Brier score | Quantara calibration logs | Confidence accuracy |
| Trade count | Quantara execution logs | Intraday + swing |

### System Health
| Metric | Source | Refresh |
|---|---|---|
| Backend status | `localhost:8000/health` | 5-minute poll |
| Kill switch level | Quantara kill switch API | On change |
| Pre-market package status | Quantara logs | 9:10 AM daily |
| Paper gate status | `configs/system.yaml → execution_enabled` | On config change |

### Paper Gate Tracker
| Criterion | Source | Status |
|---|---|---|
| Days elapsed | Trade log count | Cumulative |
| Win rate ≥ 60% | Trade logs | Rolling |
| No system errors (5 consecutive days) | Error logs | Pass/Fail |
| Reconciliation verified | Reconciliation logs | Pass/Fail |
| Brier score computed | Calibration logs | Pass/Fail |

---

## Live Promotion Gate

When all paper gate criteria are met, this dashboard shows:

```
🟡 PAPER GATE PASSED — AWAITING FOUNDER APPROVAL FOR LIVE CAPITAL
[Button: Review criteria] [Button: Approve live deployment]
```

The Founder must manually approve before `execution_enabled: true` is set.

---

## What This Dashboard Does NOT Show

- Signal internals (confidence scores, gate results, debate rationale) — those are in Quantara's internal dashboard
- Raw tick data or option chains
- Order book details
- Individual agent outputs

This is the CEO view of Quantara as a business/product, not the CIO view of individual trades.
