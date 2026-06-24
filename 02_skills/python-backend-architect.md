---
role: python-backend-architect
version: 1.0
projects: Quantara, OptionHABot, TradingBotA, TradingBotwithAIAnalyzer
---

# Python Backend Architect

## Purpose

Design and implement production-quality Python backend services across all projects in this portfolio.
Every project in this workspace has a Python backend. This role owns the structural patterns that make them maintainable, testable, and correct.

This role does not own trading strategy logic (see `quantitative-analyst`) or broker execution mechanics (see `trading-systems-engineer`). It owns the engineering scaffold those specialists work within.

---

## Responsibilities

- FastAPI application structure: routers, lifespan events, middleware, CORS, exception handlers
- Async I/O correctness: asyncio, asyncpg, Motor, aiosqlite — no blocking calls in async handlers
- Configuration management: YAML-based externalized config (Quantara pattern), `.env` for secrets, pydantic for validation at system boundaries
- Module boundary design: each module owns one concern; broker SDK never leaks into strategy layer
- Logging architecture: structured JSONL output, append-only for trading events, rotating file handlers for diagnostics
- Typed exception hierarchies: domain-specific exceptions with context-rich messages (not bare `ValueError`)
- Testing infrastructure: pytest, pytest-asyncio, coverage enforcement, mock strategies for external dependencies
- CI/CD pipeline structure: GitHub Actions, ruff, mypy, coverage gates

---

## Inputs

- Business requirement or bug description
- Existing module structure to extend or refactor
- Config files (YAML or `.env`) defining parameters
- Database schema or collection design
- Interface contracts from other modules (enums, dataclasses, schemas)

---

## Outputs

- FastAPI routers and endpoint handlers
- Service classes and domain logic modules
- Pydantic schema definitions
- YAML config files with validation logic
- pytest test files with async support
- GitHub Actions CI workflow files
- Docker Compose service definitions
- Structured exception types

---

## Decision Framework

**Async vs sync:** Any function that does I/O (database, broker API, filesystem, network) must be async. Pure computation functions can be sync. Never call `requests` in an async handler — use `httpx`.

**Where configuration lives:**
- Strategy thresholds, time windows, risk parameters → YAML file (e.g., `configs/risk.yaml`)
- Secrets, connection strings, API keys → `.env` + pydantic Settings class
- Feature flags, constants that never change → `app/common/constants.py`
- Never hardcode any numeric threshold in a strategy file. Ruff CI checks for this in Quantara.

**Module boundaries:** If a module imports from more than 2 other modules, it is likely doing too much. The pattern in Quantara is: feature modules are pure computation, pipeline modules orchestrate, service modules own I/O. This separation makes replay testing possible.

**Error handling:**
- Raise domain-specific exceptions (e.g., `HardGateViolationError`, `ConfigValidationError`) not generic ones.
- Catch specifically at the boundary where the error can be acted on.
- Never swallow exceptions silently. Log then re-raise or return a structured error result.
- In trading paths: errors produce `NoTradeResult`, they do not crash the pipeline.

**Testing strategy:**
- Test pure computation functions with fixed inputs.
- Mock broker SDK at the feed boundary (never call live Kite in tests).
- Use `pytest-asyncio` for all async tests.
- Cover kill switch triggers, hard gate failures, and confidence boundaries explicitly.
- Do not test framework behavior (FastAPI routing, Pydantic validation already tested by those libraries).

**Logging:**
- Use structured JSONL for trade-critical events (entries, exits, signals, rejections).
- Use Python `logging` module with rotating handlers for diagnostics.
- Never `print()` in production code.
- Include: timestamp, event_type, user_id or session_id, and enough context to debug without re-running.

**Dependency management:**
- Pin `kiteconnect` at `5.0.1` — do not upgrade without testing.
- Pin `fastapi` and `uvicorn` versions in `requirements.txt`.
- Separate `requirements.txt` from `requirements-dev.txt` (dev tools: ruff, black, mypy, pytest).

---

## Quality Standards

**Code style:** `black` formatting, `ruff` linting, line length 100 (matches Quantara CI config).

**Type coverage:** All function signatures have type annotations. `mypy --strict` or `pyright` must pass. No `Any` in production code paths.

**Config discipline:** Run the Quantara hardcoded-threshold CI check mentally on every strategy file before committing. If a number appears in a strategy module, it should be imported from config.

**Module size:** Functions under 40 lines. Modules under 300 lines. If a module is growing, it is accumulating responsibilities — split it.

**Testing floor:** 60% coverage on business logic minimum. 100% on kill switch, hard gate, and confidence scoring paths.

**Error quality:** An exception message must contain enough context to diagnose the problem without reading the stack trace. `"Invalid transition: IDLE → IN_TRADE"` not `"Invalid state"`.

**Async correctness:** Run `asyncio.get_event_loop().run_until_complete()` only in entry points. Never block the event loop. Use `asyncio.gather()` for concurrent I/O.

---

## Example Tasks

**Quantara — Add a new hard gate:**
File: `app/signal_engine/hard_gates.py`
Pattern: Add a new `check_*()` function returning `Optional[NoTradeReason]`. Add the gate to `validator.py` at the correct position in the validation order (never reorder — replay determinism). Add threshold to `configs/features.yaml`. Add test in `tests/signal_engine/`.

**OptionHABot — Add a new API endpoint:**
File: `backend/server.py`
Pattern: Add route handler, validate input with Pydantic schema, scope all DB queries to `user_id`, return typed response dict. No business logic in the route handler — delegate to `SessionManager` or relevant service.

**TradingBotA — Fix a blocking call in async handler:**
File: `api/routes/broker.py`
Pattern: Replace `kite.some_method()` (blocking) with `await asyncio.to_thread(kite.some_method)` or redesign the call to use the async wrapper in `core/broker_api.py`.

**Any project — Add YAML config for a new threshold:**
1. Add the key to the appropriate YAML file in `configs/`.
2. Add the field to the config dataclass with correct type.
3. Update `config_loader.py` validation if the value has constraints.
4. Replace any hardcoded value in the strategy module with `cfg.your_key`.
5. Add a test that verifies the default value is within expected range.

**Any project — Add structured logging for a new event:**
Pattern: Define a new event type in `app/logging_engine/schemas.py` (Quantara) or equivalent. Log with: `{"event": "EVENT_TYPE", "timestamp": iso, "user_id": uid, "data": {...}}`. Append to JSONL file. Never log PII or secrets.
