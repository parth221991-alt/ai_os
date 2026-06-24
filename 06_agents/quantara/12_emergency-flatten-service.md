# Emergency Flatten Service Specification (Tier 0)

**Service ID:** `emergency_flatten`  
**Status:** NOT IMPLEMENTED  
**Priority:** Critical — last line of defense when the main system cannot manage positions  
**Process:** Standalone systemd service (separate from `quantara-backend`)  
**Port:** 8001 (internal only — not exposed through Nginx)  
**Tier:** 0 — Survivability Foundation  
**Claude dependency:** NONE

---

## Mission

Close all open positions immediately, safely, and completely — independent of the state of the main backend.

The Emergency Flatten Service is a standalone Python process. It has **ZERO imports from the main quantara backend**. Its own requirements.txt contains: `fastapi`, `uvicorn`, `asyncpg`, `kiteconnect`, `pydantic`, `python-dotenv`. Nothing else.

If the main backend crashes, deadlocks, or enters an unrecoverable state, this service is still running and can accept flatten commands. It reads positions directly from Zerodha (bypassing internal state entirely) and places market orders.

---

## Trigger Conditions

The flatten service activates when any of these occur:

| Trigger | Source | Method |
|---|---|---|
| **Level 3 Kill Switch** | Main backend | Internal HTTP POST to port 8001 |
| **Manual command** | Human operator | `POST /flatten` with authorization_code |
| **System health OFFLINE** | Health monitor | Main backend calls port 8001 |
| **Watchdog timeout** | External watchdog (UptimeRobot or systemd) | Configurable — manual only by default |

---

## Flatten Behavior (Exact Sequence)

```
1. Receive trigger (Level 3 command or manual POST /flatten)
2. Validate authorization_code against stored hash (from kill_switch_log)
3. Signal all backend services to stop accepting new orders (write to Redis: quantara:state:flatten_in_progress = true)
4. Fetch positions DIRECTLY from Zerodha API (bypass all internal state)
5. Cross-reference with PostgreSQL positions table — take the UNION (more conservative)
6. For each position:
   a. Place MARKET order with market_protection=-1
   b. Stagger orders: 500ms gap between each (reduce market impact)
   c. Wait for fill confirmation (max 2 minutes per order)
   d. On fill: write to PostgreSQL audit_trail
7. After all fills (or 2-minute timeout):
   a. Write flatten summary to PostgreSQL (position, fill price, P&L)
   b. Send complete flatten report via Telegram
   c. Set system state to HALTED in PostgreSQL
8. Service remains running but accepts no more trading commands (HALTED state)
```

**Never place orders for positions not in Zerodha's live data.** Internal state may be wrong. Zerodha's live API is the authority on what is actually open.

---

## Standalone Process Design

### Startup
```
systemd: quantara-flatten.service
  Requires: postgresql.service
  Does NOT require: mongod, redis-server, quantara-backend
  ExecStart: python -m flatten_service.main
  Restart: always
  Environment: /etc/quantara-flatten/env
```

### Own Configuration
```python
# flatten_service/config.py
@dataclass(frozen=True)
class FlattenConfig:
    kite_api_key: str          # from env
    kite_access_token: str     # from env (or from PostgreSQL kill_switch_log)
    db_url: str                # PostgreSQL only
    telegram_bot_token: str    # from env
    telegram_chat_id: str      # from env
    order_gap_ms: int = 500    # 500ms between orders
    fill_timeout_seconds: int = 120
    port: int = 8001
```

### Own Database Access
```python
# flatten_service/db.py — reads PostgreSQL ONLY
async def get_positions_from_db() -> List[PositionRecord]:
    """Read open positions from PostgreSQL positions table."""

async def write_flatten_record(position: PositionRecord, fill_price: int) -> None:
    """Append to audit_trail. One record per position flattened."""

async def set_system_halted() -> None:
    """Update system_checkpoints.state = 'HALTED'."""

async def get_access_token() -> str:
    """Read Kite access token from PostgreSQL (stored by main backend on auth)."""
```

---

## API Endpoints

### `POST /flatten` — Main endpoint
```python
class FlattenRequest(BaseModel):
    authorization_code: str

class FlattenResponse(BaseModel):
    status: str                    # "initiated" | "rejected" | "already_flattening"
    positions_found: int
    estimated_completion_seconds: int
    flatten_id: str                # UUID for tracking
```

**Authorization:** Code generated at Level 3 kill switch activation. Stored hash in PostgreSQL `kill_switch_log`. Incorrect code = 403 Forbidden. No retries.

### `GET /health` — Health check
```python
class FlattenHealthResponse(BaseModel):
    status: str        # "ready" | "flattening" | "halted"
    db_connected: bool
    kite_connected: bool
    last_check: datetime
```

### `GET /status/{flatten_id}` — Progress tracking
```python
class FlattenStatus(BaseModel):
    flatten_id: str
    started_at: datetime
    positions_total: int
    positions_closed: int
    positions_failed: int
    status: str          # "in_progress" | "complete" | "partial_failure"
    report: Optional[str]  # Telegram-formatted summary on completion
```

---

## Order Execution

```python
async def flatten_position(position: Position) -> FillResult:
    """
    Place MARKET order for position.
    Always include market_protection=-1 (SEBI compliance — same as main backend).
    Stagger: wait 500ms after each order.
    Max fill wait: 120 seconds.
    On timeout: log FILL_TIMEOUT, mark position as MANUAL_REQUIRED.
    Never retry a MARKET order on timeout — query Zerodha to check status first.
    """
```

**Special case: Positions Zerodha shows as open but internal DB shows as closed:**
- Trust Zerodha. Include in flatten.
- Flag as `DESYNC_POSITION` in the flatten report.

**Special case: DB shows position open but Zerodha shows none:**
- Do NOT place an order for a phantom position.
- Flag as `PHANTOM_POSITION` in the flatten report.
- Log for manual investigation.

---

## Telegram Report

Sent immediately on completion:

```
🔴 EMERGENCY FLATTEN COMPLETE

Flatten ID: {flatten_id}
Triggered by: {trigger_type} | Auth: {authorized_by}
Started: {start_time} | Completed: {end_time}

Positions closed:
  {symbol} | {qty} | Entry: ₹{entry} | Exit: ₹{fill} | P&L: ₹{pnl}
  ...

Status: {complete | partial_failure}
System: HALTED — manual restart required

[If partial_failure]:
⚠️ Failed positions — MANUAL CLOSE REQUIRED:
  {symbol} | {qty} | REASON: {reason}
```

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| PostgreSQL unavailable | `asyncpg.ConnectionError` on startup | Do not start. Alert via Telegram (direct HTTP, no SDK). This is a deployment error — flatten service must always have DB access. |
| Kite token expired | `KiteConnectError` on position fetch | Read fresh token from PostgreSQL (stored on daily auth). If no valid token: alert `CANNOT_FLATTEN_NO_TOKEN`. Human must manually intervene. |
| Market closed during flatten | NSE exchange error on order | Wait until market opens if within 30 minutes. Otherwise: mark as pending, send alert. Never queue indefinitely. |
| Partial fill (Zerodha partial) | `fill_qty < requested_qty` | Accept partial. Place second order for remainder. Track as single flatten operation. |
| Zerodha timeout on market order | No response in 120s | Query position from Zerodha before retrying. Never place a duplicate MARKET order without confirmation the first failed. |
| Multiple simultaneous flatten calls | Concurrent requests | Lock: only one flatten can run at a time. Second request returns 409 with `flatten_id` of running operation. |

---

## Security

- Service bound to `127.0.0.1:8001` — not accessible from outside the VPS without explicit port forward
- Authorization code is a one-time hash — once used, it cannot be reused
- No API keys stored in code — only in systemd environment file (`/etc/quantara-flatten/env`, mode 600)
- All flatten actions written to PostgreSQL `audit_trail` with timestamp and authorization evidence
- Telegram bot token in env file — not shared with main backend (dedicated flatten-notification bot token preferred)

---

## Testing Requirements (Phase 1 Definition of Done)

Before Phase 2 begins, flatten must pass ALL of these tests:

- [ ] `POST /flatten` with valid code → correctly closes all simulated positions
- [ ] `POST /flatten` with invalid code → 403, no action taken
- [ ] Flatten when main backend is stopped (kill backend, run flatten) → works independently
- [ ] Partial fill handling → remainder order placed correctly
- [ ] Phantom position (DB open, Zerodha closed) → not ordered, flagged correctly
- [ ] Desync position (Zerodha open, DB closed) → ordered, flagged correctly
- [ ] Telegram report delivered on completion
- [ ] 72-hour continuous uptime without error
- [ ] `GET /health` reflects actual DB and Kite connectivity status

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Flatten success rate** | 100% (all Zerodha-confirmed positions closed) | Count positions still open post-flatten |
| **Time to flatten** | < 5 minutes for ≤ 10 positions | Timestamp: trigger → last fill confirmation |
| **Independent operation** | Works when main backend is stopped | Manual test: stop quantara-backend, trigger flatten |
| **Telegram delivery** | 100% (report sent on every flatten) | Check Telegram message log after each flatten test |
| **No duplicate orders** | Zero duplicate fills | Monitor Zerodha order history for doubles |
