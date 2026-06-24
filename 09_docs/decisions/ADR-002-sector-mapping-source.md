# ADR-002: Sector Mapping Data Source for ConcentrationMonitor
Date: 2026-06-15
Status: Accepted

## Context
`ConcentrationMonitor.check()` requires each position to carry a sector label. Three options were considered:
1. Static YAML file maintained by the operator
2. Live NSE/BSE API fetch at runtime
3. Third-party vendor (Screener.in, Ticker.finology, etc.)

## Decision
**Static YAML** (`configs/tier2.yaml → sector_mapping`) as the source of truth.

`SectorMapper` reads this mapping at startup. Lookup is O(1) synchronous. Option instrument suffixes (CE/PE) are stripped before lookup so `NIFTY24000CE` resolves to `NIFTY → DERIVATIVES`.

## Consequences
**Enables:** Zero API cost. Zero latency at lookup time. Deterministic and auditable — same input always produces same sector label. Editable without code deployment.

**Forecloses:** Automatic discovery of new tickers. When a new stock is added to the investment book, the operator must manually add it to `tier2.yaml`. This is acceptable for Stage 0/1 (small portfolio, <20 positions).

**Revisit at Stage 3:** If the portfolio grows to 50+ positions, migrate to a nightly BSE API sync job that populates a Redis cache. The `SectorMapper` interface (`sector(ticker) -> str`) remains unchanged.
