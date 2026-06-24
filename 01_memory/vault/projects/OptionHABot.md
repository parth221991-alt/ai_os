# OptionHABot

Tags: #project #trading #python #mongodb

**Status:** Active — multi-user, per-session isolation
**Priority:** P3 — bugs affecting trading sessions are P1
**Location:** `D:\AI_OS\04_projects\OptionHABot` / `D:\OptionHABot`

## What It Is
Heikin Ashi Doji + Confirmation pattern on 5-min ATM option candles.

## Strategy
- Doji (C-2) + Bull Confirmation (C-1) → MARKET entry
- 7-point ratchet trailing stop: breakeven at +7, lock-in at +14, +21, etc.

## Stack
Python 3.11 · FastAPI · MongoDB (Motor) · Zerodha Kite Connect · HTML/JS frontend
Port: 8004 (backend), 3001 (frontend)

## Architecture Note
MongoDB is a deliberate choice — per-user dynamic trade collections.
Multi-user isolation: isolated TradingSession, per-user collections, per-user risk limits.

## Related
- [[Quantara]] (reference architecture)
- [[Canonical Tech Stack]]
