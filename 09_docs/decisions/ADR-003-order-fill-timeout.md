# ADR-003: Order Fill Timeout — LIMIT to MARKET Conversion
Date: 2026-06-15
Status: Accepted

## Context
After placing a LIMIT order at LTP+2, the system waits for a fill. If the order is not filled within 45 seconds, a decision must be made: wait longer, convert to MARKET, or cancel.

Three options:
1. Wait indefinitely until filled or market close
2. Cancel after 45s regardless of slippage
3. Convert to MARKET if slippage is acceptable, else cancel

## Decision
**Option 3:** After 45s timeout, fetch current LTP and check drift from plan entry price.
- If `|LTP - plan_entry_price| < 4 pts` → cancel LIMIT, place MARKET with `market_protection=-1`
- If `|LTP - plan_entry_price| ≥ 4 pts` → cancel LIMIT, abort order (missed fill)

Constants (Layer 1 — broker/SEBI constraints, not in YAML):
- `_FILL_TIMEOUT_SECONDS = 45`
- `_MARKET_SLIPPAGE_GATE_PTS = 4.0`
- `_LIMIT_OFFSET_PTS = 2.0` (LIMIT price = LTP + 2)

## Consequences
**Enables:** The system never waits indefinitely (removes risk of stale orders persisting). The slippage gate prevents converting to MARKET after the price has moved significantly against us (4pts = approximately 0.5R on a typical NIFTY options trade with 7-8pt SL).

**Forecloses:** Partial fills are not handled — this is intentional for Stage 1 (1-lot only). If the quantity grows, the order manager will need a partial-fill reconciliation path.

**Anti-pattern 3:** If the MARKET order fills but the broker response is ambiguous (status ≠ COMPLETE after 2s), the system flags it as `fill_ambiguous_manual_check_required` and alerts the operator. It does NOT infer fill from absence of a rejection.
