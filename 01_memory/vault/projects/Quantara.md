# Quantara

Tags: #project #flagship #trading #python

**Status:** Production-ready — gold standard for all other projects
**Priority:** P1 — highest priority in portfolio
**Location:** `D:\AI_OS\04_projects\Quantara`

## What It Is
Deterministic NIFTY weekly options signal engine. Probability engine, not a prediction engine.
Subscriber signal delivery via Telegram.

## Stack
Python 3.12 · FastAPI · PostgreSQL 16 · asyncpg · Redis · Zerodha Kite Connect · Telegram Bot API · Docker

## Architecture
12+ modular subsystems with a finite state machine:
`IDLE → WATCHING → CANDIDATE → VALIDATING → SIGNAL_READY → IN_TRADE → EXITING → EXITED`

## Key Standards
- 10 YAML config files (zero hardcoded thresholds)
- 37 pytest files, GitHub Actions CI
- 11-layer immutable JSONL logging
- SHA-256 replay verification
- Paper trading gate: 8 weeks minimum before live

## Core Design Principles
- **Hard gates before soft gates** — 12 hard rejection criteria before confidence scoring
- **Append-only logs** — signal decisions and trade outcomes are never updated
- **Determinism** — every signal traceable by reading logs
- **State machine** — prevents undefined state transitions

## Identity
"Personal Hedge Fund OS" — 3 books: Investment, Swing, Intraday
Stage 0 paper phase. Not revenue-focused yet.
Frontend + comprehensive tests + deployment still missing.

## Related
- [[AI_OS Overview]]
- [[Canonical Tech Stack]]
- [[Architecture Decisions]]
