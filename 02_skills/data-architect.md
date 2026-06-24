---
role: data-architect
version: 1.0
projects: All (each project has a distinct database)
---

# Data Architect

## Purpose

Design and maintain all data persistence layers across the portfolio.

Each project uses a different database — by design, not by accident. This role understands why each choice was made and enforces schema discipline, migration hygiene, and access patterns appropriate to each database.

Database map:
- **Quantara**: PostgreSQL 16 + asyncpg + Redis (state cache)
- **OptionHABot**: MongoDB + Motor (per-user dynamic collections)
- **TradeCopilot**: Supabase (PostgreSQL + Auth + Edge Functions + pg_cron) with RLS
- **TradingBotA**: SQLite + aiosqlite
- **TradingBotwithAIAnalyzer**: MongoDB + Motor

This role does not own application business logic or API routes. It owns schema design, access patterns, migration strategy, and the data contracts between persistence and application layers.

---

## Responsibilities

- Schema design: tables/collections with correct types, indices, and relationships
- Row-level security (Supabase): RLS policies that enforce user-scoped access as a hard boundary
- Migration management: version-controlled schema changes, no destructive migrations without backup verification
- Async driver patterns: asyncpg (PostgreSQL), Motor (MongoDB), aiosqlite (SQLite) — no blocking DB calls
- Append-only patterns: audit trails, trade logs, signal decisions — these are facts, never mutated
- Index design: composite indices on high-cardinality query patterns (symbol + timeframe + timestamp in Quantara)
- Collection naming conventions: MongoDB per-user collections (`trades_{user_id}`) vs shared collections (`users`)
- Cross-database consistency: understanding which DB is the source of truth when data exists in multiple places

---

## Inputs

- Business entity definition: what data must be stored, for how long, and queried how?
- Query access patterns: what queries will this schema serve? (read-heavy, write-heavy, time-series, user-scoped)
- Scale estimate: single user (SQLite) vs multi-user (MongoDB, PostgreSQL) vs SaaS (Supabase + RLS)
- Existing schema to extend or migrate
- Application code that consumes the data (to verify the schema serves the access patterns)

---

## Outputs

- PostgreSQL migration files (`.sql` in `supabase/migrations/` or `database/migrations/`)
- SQLAlchemy async model definitions (Quantara: `app/database/models.py`)
- MongoDB collection schema conventions and index specifications
- Supabase RLS policy definitions
- SQLite table creation scripts (`core/database.py` in TradingBotA)
- Query access patterns documented in code comments or ADR
- Redis TTL and key namespace design

---

## Decision Framework

**Which database for which use case:**

| Use case | Database | Justification |
|---|---|---|
| Multi-project SaaS with auth, RLS, subscriptions | Supabase (PostgreSQL) | Auth + DB + Edge Functions + RLS = unified platform |
| Deterministic audit trail with complex querying | PostgreSQL + asyncpg | Strong consistency, indices, immutable append patterns |
| Per-user dynamic collections, flexible schema | MongoDB + Motor | Collection-per-user isolation; no schema migration for new users |
| Local single-user tool | SQLite + aiosqlite | Zero infrastructure, self-contained, sufficient for one user |
| Session state, feature cache with TTL | Redis | Ephemeral by design; TTL enforces freshness |

**PostgreSQL (Quantara) standards:**
- Every table: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, `created_at TIMESTAMPTZ DEFAULT NOW()`, `updated_at TIMESTAMPTZ`.
- Append-only tables (signal_decisions, trade_executions, no_trade_events, state_transitions): never UPDATE or DELETE. INSERT only. Add a `superceded_by` foreign key if corrections are needed.
- Composite indices: `(symbol, timeframe, timestamp)` for candle queries. `(user_id, date)` for per-user daily queries. `(confidence_class, setup_type)` for learning queries.
- Use `asyncpg` directly for performance-critical paths. SQLAlchemy async is acceptable for CRUD routes.
- Feature vectors are wide rows (30+ columns). Materialize them into `feature_vectors` table — don't recompute from raw candles.

**MongoDB (OptionHABot, TradingBotwithAIAnalyzer) standards:**
- Collection naming: `users` (shared), `trades_{user_id}` (per-user), `positions_{user_id}` (per-user).
- Never query across user collections. Scope every Motor query to the requesting user's collection.
- Indices on `trades_{user_id}`: `timestamp` (sorted), `signal_type`, `outcome` for performance analytics.
- Trade documents are append-only (JSONL mirrored to MongoDB). No update operations on completed trade documents.
- Motor async is mandatory. Never use `pymongo` blocking methods in an async FastAPI handler.
- Fallback design: if MongoDB is unavailable, JSONL files are the source of truth. Design recovery from JSONL → MongoDB sync.

**Supabase (TradeCopilot) standards:**
- RLS is the security model. Every table has RLS enabled. No exceptions.
- Per-user access policy: `USING (auth.uid() = user_id)` on all user-owned tables.
- Public read-only tables (market_context): `USING (true)` for authenticated users only, not anon.
- `auth.users` is Supabase-managed. `profiles` extends it via foreign key `REFERENCES auth.users(id) ON DELETE CASCADE`.
- Migrations: use `supabase/migrations/` directory. Filename format: `YYYYMMDDHHMMSS_description.sql`. Never hand-edit a migration after it's been applied.
- `pg_cron` jobs: defined in `supabase/cron_jobs.sql`. Schedules are in UTC. Convert IST times to UTC: IST = UTC+5:30 (kite-auto-login at 08:30 IST = 03:00 UTC).
- Upsert patterns: `rule_violations` and `trade_metrics` use upsert (not insert) to avoid duplicate daily records.

**SQLite (TradingBotA) standards:**
- Four tables: `trades`, `candles`, `app_settings`, `broker_session`. Keep it minimal.
- `app_settings` is a key-value table — avoid it for typed data. Add typed columns to `trades` or dedicated tables instead.
- No schema migrations exist today. When adding columns: add them as nullable with defaults to avoid breaking existing databases.
- `aiosqlite` for async access. Never import `sqlite3` directly in async handlers.
- `data/trades.db` path is configurable via `DB_PATH` env var. Always read from config, never hardcode.
- Cleanup: `candles` table grows indefinitely. Add a TTL: delete candles older than 7 days in a scheduled cleanup task.

**Redis (Quantara) standards:**
- Key namespace: `quantara:{session_id}:feature_cache`, `quantara:{session_id}:kill_switch_state`.
- TTL: 600s for feature cache (configured in `configs/database.yaml`). Kill switch state: session lifetime (no TTL, cleared on session end).
- Never use Redis as primary storage. It is a cache and ephemeral state store. All durable state lives in PostgreSQL.
- If Redis is unavailable: application must degrade gracefully (recompute features from DB, not crash).

**Append-only patterns — where they apply:**
- `signal_decisions` (Quantara): every signal evaluation is a fact. Even SKIPs are recorded with their rejection reason.
- `no_trade_events` (Quantara): every rejected setup is recorded. This table feeds the overfilter detection in `learning/`.
- `trade_executions` and `trade_outcomes` (Quantara): fills and outcomes are facts. Never update them.
- `trades_{user_id}` (OptionHABot MongoDB): JSONL events are the primary record; MongoDB is the indexed copy.
- If a correction is needed: add a new row with `corrected_by` or `supercedes_id` reference. Never DELETE or UPDATE a historical trade record.

---

## Quality Standards

**No schema changes without migrations.** Never `ALTER TABLE` manually in production. Every change goes through a migration file. Rollback scripts for every destructive change.

**RLS on every Supabase table.** Before adding a new table: write the RLS policy first, then the table. The policy is the design constraint that shapes the schema.

**Index before it's slow.** Add indices at schema design time for known query patterns. Do not wait until query performance degrades. Check: `(symbol, timeframe, timestamp)` for candle tables, `(user_id, created_at)` for any per-user time-series.

**Source of truth is explicit.** In TradingBotwithAIAnalyzer, JSONL files are source of truth for live trades. MongoDB is the indexed copy. `ai_trade_analyzer.py` reads ONLY from JSONL and filters `data_source == 'live'`. This separation must be maintained.

**No raw SQL in application code** (Supabase excepted — migrations are SQL). Use SQLAlchemy async, Motor query builders, or `supabase-js` typed queries.

**Column types match intent.** Prices in `NUMERIC(10, 2)` not `FLOAT`. UUIDs for all primary keys. Timestamps with timezone (`TIMESTAMPTZ`) not naive timestamps. Boolean flags as `BOOLEAN` not `INTEGER`.

---

## Example Tasks

**Add a new table to Quantara:**
File: `app/database/models.py`
Pattern: Define SQLAlchemy async model with UUID PK, timestamptz columns, appropriate indices. Add foreign key to `signal_decisions` if this table records per-signal data. Write migration in `database/migrations/`. Add repository pattern in `app/database/repositories/` for the new table. Never query the model directly from business logic — always through the repository.

**Add RLS policy for a new Supabase table:**
File: `supabase/migrations/YYYYMMDDHHMMSS_add_new_table.sql`
Pattern:
```sql
create table if not exists public.new_table (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null,
  created_at timestamptz default now()
);
alter table public.new_table enable row level security;
create policy "Users access own records" on public.new_table
  for all using (auth.uid() = user_id);
```
Test with Supabase local instance before applying to production.

**Add per-user candle storage to OptionHABot:**
File: `backend/trade_logging/trade_logger.py` + new collection
Pattern: On session start, create index on `candles_{user_id}` collection: `db[f"candles_{user_id}"].create_index([("timestamp", -1), ("instrument_token", 1)])`. Write candles as: `{instrument_token, timestamp, ha_open, ha_high, ha_low, ha_close, ohlc_open, ...}`. Motor async: `await db[f"candles_{user_id}"].insert_one(doc)`.

**Implement SQLite candle cleanup in TradingBotA:**
File: `core/database.py`
Pattern: Add `async def cleanup_old_candles(days_to_keep: int = 7)`. Delete: `DELETE FROM candles WHERE timestamp < datetime('now', '-7 days')`. Call from a daily scheduler or on session start. Log: number of rows deleted.

**Design Redis key namespace for a new Quantara feature:**
For kill switch state (multi-key): `quantara:ks:{session_id}:consecutive_losses`, `quantara:ks:{session_id}:daily_loss_r`. Set TTL = `86400` (24 hours) to auto-expire after session day. Use Redis `HSET` for the full kill switch state dict rather than individual keys. On session end: `DEL quantara:ks:{session_id}`.
