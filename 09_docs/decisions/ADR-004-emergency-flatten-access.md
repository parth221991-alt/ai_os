# ADR-004: Emergency Flatten Access When Main Backend Crashed
Date: 2026-06-15
Status: Accepted

## Context
The main backend (port 8000) may crash during a trading session while a position is open. If this happens, the operator needs a way to close the position without the main backend running.

Options considered:
1. Standalone HTTP service on port 8001 (separate process, separate systemd unit)
2. Direct KiteConnect API via a separate CLI script
3. Manual Zerodha web interface

## Decision
**Standalone HTTP service** (`flatten_service.py`, port 8001).

Critical isolation rule enforced by code: `flatten_service.py` imports **nothing** from `app.*`. If `app/` is partially initialized or crashed, the flatten service still runs. It uses:
- `kiteconnect` directly (no app wrappers)
- `asyncpg` directly for audit trail (no SQLAlchemy)
- File-based kill flag (`.flatten_kill_flag`) as a belt-and-suspenders safety

Systemd unit: `quantara-flatten.service` — only depends on `postgresql.service`, not on `quantara-backend.service`.

Authentication: `POST /flatten?auth={FLATTEN_AUTH_TOKEN}` — token in environment variable.

Reset path: `POST /reset-kill-flag?auth=...` — removes the kill flag after operator reviews the incident.

## Consequences
**Enables:** Flatten works even if the main backend (FastAPI, SQLAlchemy, Redis, MongoDB) is completely down. The operator can also trigger it from a Telegram alert or a phone with mobile data.

**Forecloses:** This service cannot access the main app's in-memory state. It fetches positions fresh from Zerodha API at flatten time, which is the correct behavior (Engineering Rule 3: never assume broker state).

**Note:** The kill flag file (`.flatten_kill_flag`) is checked at main backend startup. If it exists, the backend refuses to start trading until `reset-kill-flag` is called. This prevents automatic restart from immediately reopening positions after an emergency flatten.
