# ADR-001: Zerodha TOTP Login Strategy
Date: 2026-06-15
Status: Accepted

## Context
Zerodha KiteConnect requires a daily login to obtain an access_token. The token is valid for one calendar day. The system must refresh it automatically for production systemd deployment while remaining accessible during paper trading.

## Decision
Two modes controlled by a single env var:

- **Automated (production):** If `ZERODHA_TOTP_SECRET` is set, the system performs a fully automated 3-step login using `pyotp` + `httpx`:
  1. POST credentials → get `request_id`
  2. POST TOTP code → get `request_token` from redirect Location header
  3. Exchange `request_token` via KiteConnect SDK → cache `access_token`

- **Manual fallback (paper trading / dev):** If `ZERODHA_TOTP_SECRET` is absent, the system prints the login URL, waits for the operator to paste the `request_token`. This matches the 8:00 AM alert workflow for paper trading.

Token cached to `.kite_token.json` with today's date. `load_cached_token()` is always called first.

## Consequences
**Enables:** Zero-touch production deployment via systemd. Paper trading works without storing TOTP secret.

**Forecloses:** Google Authenticator cannot be used if TOTP secret is not accessible as a string (requires base32 export from Zerodha 2FA setup). Playwright-based browser automation was rejected due to fragility and maintenance burden.

**Risk:** TOTP secret stored in `.env` file — must not be committed to git. Covered by `.gitignore`.
