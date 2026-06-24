# Architecture Inventory — AI_OS Ecosystem
**Last updated:** 2026-06-08  
**Maintained by:** Solo founder — update this file whenever a project is added, a service changes port, or a new external dependency is introduced.

---

## Table of Contents
1. [Ecosystem Overview](#1-ecosystem-overview)
2. [Projects](#2-projects)
3. [Services & Ports](#3-services--ports)
4. [Databases](#4-databases)
5. [External APIs](#5-external-apis)
6. [Brokers](#6-brokers)
7. [Deployment Targets](#7-deployment-targets)
8. [Shared Libraries & Patterns](#8-shared-libraries--patterns)
9. [Agent Systems](#9-agent-systems)
10. [Automation & CI/CD](#10-automation--cicd)
11. [Configuration Files Index](#11-configuration-files-index)
12. [Environment Variables Reference](#12-environment-variables-reference)
13. [Dependency Matrix](#13-dependency-matrix)
14. [Tech Debt Register](#14-tech-debt-register)

---

## 1. Ecosystem Overview

The AI_OS workspace (`D:\AI_OS`) is the intelligence layer for a portfolio of quantitative trading and AI products operated by a solo founder. Projects are located at the `D:\` root and symlinked into `D:\AI_OS\04_projects\`.

```
AI_OS Ecosystem
├── Quantara          — Personal Hedge Fund OS: 3-book (Investment/Swing/Intraday), ₹5Cr target (flagship)
├── TradeCopilot      — SaaS trading rule engine + AI coaching (live revenue)
├── OptionHABot       — Heikin Ashi Doji pattern, multi-user, NIFTY options
├── TradingBotA       — C1+C2 momentum bot, 2-lot multi-exit, NIFTY options
├── TradingBotwithAI  — Most advanced frontend; Anthropic + HA + EMA filters
└── ai_sql_assistant  — NLP→SQL prototype on Neon PostgreSQL
```

**Technology foundations used across multiple projects:**
- Python 3.12 + FastAPI (backend standard)
- React 19 + TypeScript (frontend standard)
- Zerodha Kite Connect 5.x (broker universal)
- Anthropic Claude API (AI primary — partially deployed)

---

## 2. Projects

### 2.1 Quantara
| Property | Value |
|---|---|
| **Location** | `D:\quantara` (symlink: `D:\AI_OS\04_projects\Quantara`) |
| **Type** | Personal Hedge Fund Operating System — 3-book autonomous trading |
| **Status** | Phase 1 (Tier 0 Survivability) — not yet in production |
| **Priority** | P1 — flagship |
| **Capital target** | ₹5 crore autonomous operation |
| **Python** | 3.12 |
| **Framework** | FastAPI 0.115+ / uvicorn |
| **Port** | 8000 (main backend, internal behind Nginx) |
| **Emergency Flatten** | Port 8001 (separate process, independent of main backend) |
| **App entry** | `app/api/main:app` |
| **Books** | Investment (40–60%), Swing (15–30%), Intraday/F&O (10–30%), Cash (10% min) |
| **Architecture doc** | `D:\AI_OS\06_agents\quantara\QUANTARA_OS_MASTER.md` (v3.1, frozen) |
| **Trade grades** | A (≥0.82, RR≥2.5), B (≥0.72, RR≥2.0), C (≥0.65, RR≥2.0), D (blocked) |
| **Confidence floor** | 0.50 (Layer 1 constant — no exceptions) |
| **RR floor** | 2.0 (Layer 1 constant — no exceptions) |
| **Pre-submission guard** | 13 checks — all must pass before any order |
| **Kill switch** | 3 levels: Level 1 (no new entries), Level 2 (all blocked), Level 3 (emergency flatten) |
| **Paper gate** | `configs/system.yaml → execution_enabled: false` — manual flip only |
| **Paper minimum** | 40 trading days (not 8 weeks) with statistical significance testing |
| **Docker** | Local dev only — `docker/docker-compose.yml` (app + postgres + redis) |
| **Production** | AWS Lightsail Mumbai + systemd + Nginx (see §7.1) |
| **CI** | GitHub Actions — `ci.yml` (lint, test, threshold check) |
| **Tests** | 37 pytest files (existing). Target: validity_engine 95%+, kill_switch 95%+ |
| **Exchange** | NSE / NIFTY (intraday). NSE equities (investment/swing). |
| **Monetary values** | Integer paise only — no floating point |

**System tiers:**
- Tier 0: Survivability (kill switch, reconciliation, idempotency, data validity, emergency flatten)
- Tier 1: Alpha Generation (regime, intraday SMC+F&O, microstructure, swing, investment)
- Tier 2: CIO Allocation (portfolio state, capital per book, cross-book concentration)
- Tier 3: AI Intelligence (pre-market package, news, Claude model routing — non-blocking)
- Tier 4: Learning (recommendations only, human approval required)

**Intraday signal pipeline (existing, Phase 2 upgrade):**
```
Ticks → Ingestion → Features → Liquidity → Setups (OPA/PES/SFR) → StateMachine
→ 13-Check Guard → WeightedSignalEngine → ProbabilityEngine → RiskEngine → Execution
```

**Agent inventory:** 13 agents/services defined in `D:\AI_OS\06_agents\quantara\`  
**Roadmap:** `D:\AI_OS\06_agents\quantara\ROADMAP.md`  
**Knowledge architecture:** `D:\AI_OS\06_agents\quantara\KNOWLEDGE_ARCHITECTURE.md`

---

### 2.2 TradeCopilot
| Property | Value |
|---|---|
| **Location** | `D:\tradecopilot` (symlink: `D:\AI_OS\04_projects\TradingCopilot`) |
| **Type** | React SaaS — trading journal + AI coaching |
| **Status** | Live at `tradecopilot.in` with paying subscribers |
| **Priority** | P2 — active revenue |
| **Frontend** | React 19.2 + TypeScript 4.9 + Tailwind CSS 3.4 |
| **Backend** | Supabase (PostgreSQL + Auth + Edge Functions + pg_cron) |
| **AI** | Groq `llama-3.3-70b-versatile` (TECH DEBT — migrate to Claude) |
| **Payments** | Razorpay live (`rzp_live_*`) |
| **Supabase project** | `qtjmirkmgbpslpfztbra.supabase.co` |
| **Dev port** | 3000 |
| **Build tool** | react-scripts 5.0.1 |

**Key features:** 8 behavioral rules engine (revenge trading, overtrading, FOMO, etc.), 4 AI insight types (daily_review, pre_market, weekly_coaching, trading_dna), Kite Connect auto-login via pg_cron

**Supabase Edge Functions:**
- `groq-ai` — Groq API proxy (should become `claude-ai`)
- `kite-auto-login` — auto-refreshes Kite access token at 08:30 IST

---

### 2.3 OptionHABot
| Property | Value |
|---|---|
| **Location** | `D:\OptionHABot` (symlink: `D:\AI_OS\04_projects\OptionHABot`) |
| **Type** | Python backend + HTML/JS frontend — multi-user trading bot |
| **Status** | Active. Multi-user per-session isolation. |
| **Priority** | P3 — active bot |
| **Python** | 3.11 |
| **Framework** | FastAPI 0.111 / uvicorn 0.29 |
| **Port** | 8002 |
| **Database** | MongoDB 8.2 (Motor 3.3.2 async driver) |
| **Broker** | Zerodha Kite Connect 5.0.1 |
| **AI** | Anthropic Claude (package installed, not yet wired to strategy) |
| **Auth** | JWT (python-jose + passlib/bcrypt) |
| **Strategy** | HA Doji (C-2) + Bull Confirmation (C-1) → MARKET entry |
| **Startup** | `start.ps1` → MongoDB → venv → FastAPI |

**Per-user MongoDB collections:** `trades_{user_id}`, `positions_{user_id}`  
**Trailing stop:** 7-point ratchet (+7=breakeven, +14=+7, +21=+14, ...)

---

### 2.4 TradingBotA
| Property | Value |
|---|---|
| **Location** | `D:\Trading_bot_a` (symlink: `D:\AI_OS\04_projects\TradingBotA`) |
| **Type** | Python backend + React frontend — NIFTY options bot |
| **Status** | Active. Documented backtest WR ~90% over 60 days. |
| **Priority** | P4 — active bot |
| **Python** | 3.12 |
| **Framework** | FastAPI 0.111 / uvicorn 0.29 |
| **Port** | 8765 |
| **Database** | SQLite via aiosqlite 0.20 + SQLAlchemy 2.0 |
| **Broker** | Zerodha Kite Connect 5.0.1 |
| **Strategy** | C1+C2 momentum on 1-min HA candles. ATM±50 strikes. 2-lot exit. |
| **Startup** | `run.bat` → venv → FastAPI → opens browser |

**2-lot exit model:** Lot 1: TP +30pts / SL -15pts. Lot 2: SL → entry after Lot1 TP, trails +10pts.  
**SEBI compliance:** `market_protection=-1` on all MARKET orders.

---

### 2.5 TradingBotwithAIAnalyzer
| Property | Value |
|---|---|
| **Location** | `D:\TradingBotwithAIAnalyzer` |
| **Type** | Python backend + React frontend — most advanced design system |
| **Status** | Active. Reference for frontend design decisions. |
| **Python** | 3.x |
| **Backend framework** | FastAPI (uvicorn 0.25) |
| **Frontend framework** | React 19 + TypeScript + Tailwind CSS + Radix UI (shadcn/ui pattern) |
| **Database** | MongoDB (Motor 3.3.1) |
| **AI** | Anthropic integrated |
| **TA library** | TA-Lib 0.6.7 |
| **Cloud** | AWS S3 (boto3 1.40) |
| **Design system** | `frontend/design_guidelines.json` — canonical reference for all frontends |

**Design system values (canonical for all projects):**
- Typography: Chivo (headings), IBM Plex Sans (body), JetBrains Mono (numerics)
- Palette: Emerald-500 (profit), Red-500 (loss), Indigo-600 (primary)
- Mode: Dark only. No shadows. Flat solid backgrounds, 1px borders. Minimal motion.

---

### 2.6 ai_sql_assistant
| Property | Value |
|---|---|
| **Location** | `D:\ai_sql_assistant` |
| **Type** | Python CLI + Streamlit web app — NLP→SQL prototype |
| **Status** | Prototype only. Not production. |
| **Priority** | P6 — lowest |
| **Database** | Neon PostgreSQL (cloud, Azure GWC region) |
| **Interface** | Streamlit web app (`streamlit_app.py`) |
| **Purpose** | Proof-of-concept for natural language database querying |

---

## 3. Services & Ports

| Service | Project | Port | Protocol | Notes |
|---|---|---|---|---|
| Quantara API | Quantara | **8000** | HTTP | FastAPI / uvicorn (internal, behind Nginx) |
| Quantara Emergency Flatten | Quantara | **8001** | HTTP | Standalone process — zero main backend imports |
| Quantara PostgreSQL | Quantara | **5432** | TCP | Prod: systemd. Local: Docker postgres:16-alpine |
| Quantara MongoDB | Quantara | **27017** | TCP | Prod: systemd. Intelligence + signals data. |
| Quantara Redis | Quantara | **6379** | TCP | Prod: systemd. Local: Docker redis:7-alpine |
| Nginx (Quantara) | Quantara | **80/443** | HTTP/HTTPS | SSL reverse proxy → port 8000 |
| TradeCopilot UI | TradeCopilot | **3000** | HTTP | React dev server (conflicts with TradingBotwithAI backend) |
| OptionHABot API | OptionHABot | **8002** | HTTP | FastAPI / uvicorn |
| OptionHABot MongoDB | OptionHABot | **27017** | TCP | Local MongoDB 8.2 install |
| TradingBotA Dashboard | TradingBotA | **8765** | HTTP | FastAPI + static React build |
| TradingBotwithAI Backend | TradingBotwithAI | **8000** | HTTP | Conflicts with Quantara — never run together |
| TradingBotwithAI Frontend | TradingBotwithAI | **3000** | HTTP | React dev server — conflicts with TradeCopilot |
| ai_sql_assistant | ai_sql_assistant | **8501** | HTTP | Streamlit default port |

**Port conflict table:**

| Port | Conflict |
|---|---|
| 8000 | Quantara API vs TradingBotwithAI backend |
| 3000 | TradeCopilot dev server vs TradingBotwithAI frontend |

**Resolution:** Never run conflicting services simultaneously. Use `APP_ENV` or docker profiles to isolate.

---

## 4. Databases

### 4.1 PostgreSQL 16 — Quantara
| Property | Value |
|---|---|
| **Image** | postgres:16-alpine (Docker) |
| **Host (Docker)** | postgres_db |
| **Host (local)** | localhost |
| **Port** | 5432 |
| **Database** | quantara |
| **Driver** | asyncpg 0.29 |
| **ORM** | SQLAlchemy 2.0 async + Alembic migrations |
| **Migration** | `alembic upgrade head` — never auto-migrates in production |
| **Pool** | size=10, max_overflow=20, timeout=30s |

**Tables (17):**

| Table | Type | Purpose |
|---|---|---|
| `market_candles` | Append-only | Raw OHLCV + VWAP + ATR by timeframe |
| `option_candles` | Append-only | Option chain OHLCV + IV + spreads |
| `feature_vectors` | Append-only | All computed features per bar |
| `signal_decisions` | Append-only | Signal generation record (immutable) |
| `trade_executions` | Append-only | Order details, fill price, slippage |
| `trade_outcomes` | Append-only | P&L, MFE/MAE, exit reason |
| `no_trade_events` | Append-only | Rejection reasons, would_have_won |
| `state_transitions` | Append-only | FSM state changes with timestamps |
| `replay_sessions` | Append-only | SHA-256 hash chain per replay |
| `monthly_clusters` | Write | Trade clustering by month/setup/regime |
| `telegram_events` | Append-only | Delivery status per message |
| `system_health` | Upsert | Feed/broker/DB health (current state) |
| *(5 supporting)* | Various | Schema tables for signals and features |

**Schema standard:** `id UUID PRIMARY KEY`, `created_at TIMESTAMPTZ DEFAULT NOW()`, `updated_at TIMESTAMPTZ`

---

### 4.2 Redis 7 — Quantara
| Property | Value |
|---|---|
| **Image** | redis:7-alpine (Docker) |
| **Host** | redis_cache (Docker) / localhost (local) |
| **Port** | 6379 |
| **DB index** | 0 |
| **Key prefix** | `qnt:` (database.yaml) / `quantara:` (agent bus) |
| **Default TTL** | 600s (config), varies by key type |

**Key namespace map:**

| Namespace | Content | TTL |
|---|---|---|
| `quantara:bus:features` | FeatureVector pub/sub | — |
| `quantara:bus:regime` | RegimeContext pub/sub | — |
| `quantara:bus:agent_decisions` | AgentDecision pub/sub | — |
| `quantara:bus:signal_candidates` | SignalDecision pub/sub | — |
| `quantara:bus:debate_verdicts` | DebateVerdict pub/sub | — |
| `quantara:bus:trade_events` | Trade lifecycle pub/sub | — |
| `quantara:bus:alerts` | SystemAlert pub/sub | — |
| `quantara:ks:{session_id}` | KillSwitchState HSET | No TTL (manual reset) |
| `quantara:regime:{session_id}` | RegimeContext JSON | 360s (1 bar) |
| `quantara:portfolio:{session_id}` | PortfolioState JSON | 3600s |
| `quantara:portfolio:stats:{sid}:{setup}` | StrategyStats JSON | 3600s |
| `quantara:trade:{trade_id}` | TradeState JSON | Until closed |
| `quantara:news:{YYYY-MM-DD}` | NewsAgentOutput JSON | 86400s |
| `quantara:debate:{signal_id}` | DebateVerdict JSON | 3600s |
| `quantara:alerts:{session_id}` | Active alerts sorted set | Session |

---

### 4.3 MongoDB 8.2 — OptionHABot
| Property | Value |
|---|---|
| **Install** | Local Windows `C:\Program Files\MongoDB\Server\8.2\` |
| **Port** | 27017 |
| **Database** | option_ha_bot |
| **Driver** | Motor 3.3.2 (async) |
| **Connection** | 5s timeout, 3 retries |

**Collections (per-user pattern):**

| Collection | Pattern | Purpose |
|---|---|---|
| `users` | Shared | User accounts |
| `sessions` | Shared | Active trading sessions |
| `trades_{user_id}` | Per-user | Trade records for isolation |
| `positions_{user_id}` | Per-user | Open position state |

---

### 4.4 SQLite — TradingBotA
| Property | Value |
|---|---|
| **File** | `data/trades.db` (relative to project root) |
| **Driver** | aiosqlite 0.20 |
| **ORM** | SQLAlchemy 2.0 async |
| **Use case** | Local single-user, no concurrent writes needed |

---

### 4.5 Supabase PostgreSQL — TradeCopilot
| Property | Value |
|---|---|
| **Project** | `qtjmirkmgbpslpfztbra.supabase.co` |
| **Auth** | Supabase Auth (JWT, email+password) |
| **RLS** | Enabled on all tables — `USING (auth.uid() = user_id)` |
| **Realtime** | Used for live data sync |
| **Edge Functions** | `groq-ai`, `kite-auto-login` (Deno runtime) |
| **pg_cron jobs** | See §10 Automation |
| **Client** | `@supabase/supabase-js 2.105` |

**Subscription tiers:** free (30 trades max), pro (unlimited)

---

### 4.6 Neon PostgreSQL — ai_sql_assistant
| Property | Value |
|---|---|
| **Provider** | Neon (Azure GWC region) |
| **Pool** | Connection pooler enabled (`*-pooler.gwc.azure.neon.tech`) |
| **SSL** | Required + channel binding |
| **Use** | Prototype only — sample sales data |

---

## 5. External APIs

| API | Used By | Purpose | SDK / Package | Notes |
|---|---|---|---|---|
| **Anthropic Claude** | OptionHABot, Quantara (planned) | AI reasoning, debate agent | `anthropic==0.28.0` (OptionHABot) | Quantara Debate Agent requires sonnet-4-6 |
| **Groq** | TradeCopilot | AI coaching insights | Direct HTTP (`REACT_APP_GROQ_API_KEY`) | TECH DEBT — migrate to Claude |
| **Telegram Bot API** | Quantara | Signal delivery to subscribers | `python-telegram-bot` or direct HTTP | Token in `TELEGRAM_BOT_TOKEN` |
| **Supabase** | TradeCopilot | BaaS: auth, database, edge functions | `@supabase/supabase-js 2.105` | Project: `qtjmirkmgbpslpfztbra` |
| **Razorpay** | TradeCopilot | Payment processing for subscriptions | Frontend SDK | Live key: `rzp_live_Stdk1eyBls5D7n` |
| **AWS S3** | TradingBotwithAI | Storage (purpose TBD) | `boto3 1.40` | Not in other projects |
| **Neon** | ai_sql_assistant | Cloud PostgreSQL | SQLAlchemy + psycopg2 | Prototype only |

**Anthropic model usage (current + planned):**

| Model | Project | Purpose |
|---|---|---|
| `claude-sonnet-4-6` | Quantara Debate Agent (planned) | Adversarial signal review |
| `claude-haiku-4-5-20251001` | Quantara News Agent (planned) | Calendar event parsing |
| `claude-haiku-4-5-20251001` | Quantara Monitoring Agent (planned) | Alert classification |
| Any Claude | OptionHABot | Strategy support (installed, not wired) |
| Any Claude | TradeCopilot (tech debt) | Replace Groq coaching insights |

**Groq model in use:** `llama-3.3-70b-versatile` (TradeCopilot `groq-ai` edge function)

---

## 6. Brokers

### Zerodha Kite Connect 5.x
The universal broker across all active trading projects.

| Property | Value |
|---|---|
| **Package** | `kiteconnect==5.0.1` |
| **API key** | `ZERODHA_API_KEY` / `REACT_APP_KITE_API_KEY` |
| **Auth flow** | Login URL → callback → `generate_session()` → access token |
| **Token refresh** | Daily (Kite tokens expire at 06:00 IST next day) |
| **Data transport** | WebSocket (authoritative for ticks) → REST (reconnection fallback) |
| **NIFTY spot token** | `256265` |
| **Lot size** | 75 (NIFTY, updated regularly — verify before trading) |
| **Strike gap** | 50 points |

**SEBI compliance requirements (non-negotiable in all projects):**
- All MARKET orders: `market_protection=-1` — no exceptions
- LIMIT→MARKET fallback: place LIMIT at LTP+buffer → wait 5–10s → convert if slippage < 3–4pts → else cancel
- No intrabar entries (Quantara rule — all entries on candle close only)
- EOD square-off: all positions closed by 15:20 IST

**Projects using Kite:**

| Project | Usage | Live? |
|---|---|---|
| Quantara | Feed + (future) order execution | Paper only |
| TradeCopilot | Account data, trade import, auto-login | Read-only |
| OptionHABot | Feed + MARKET orders | Potentially live |
| TradingBotA | Feed + MARKET orders | Paper default |
| TradingBotwithAI | Feed + MARKET orders | Has live integration |

### Dhan (Secondary Broker — Placeholder)
- Configured in Quantara `.env` as `DHAN_API_KEY` (empty)
- Not integrated into any project
- Future consideration only

---

## 7. Deployment Targets

### 7.1 Quantara — Production: AWS Lightsail + systemd

**Production target:** AWS Lightsail Mumbai (4GB RAM, 2 vCPU, 50GB SSD, Ubuntu 22.04)

**systemd service startup order:**
```
postgresql.service (15)
  → mongod.service (6)
    → redis-server.service (7)
      → quantara-backend.service (port 8000, internal)
quantara-flatten.service (independent, requires postgresql.service only)
Nginx: SSL reverse proxy on 80/443
```

**Key services:**
- `quantara-backend.service` — main FastAPI backend, bound to 127.0.0.1:8000
- `quantara-flatten.service` — Emergency Flatten, bound to 127.0.0.1:8001, ZERO backend imports
- `nginx.service` — SSL termination, serves React SPA, proxies API calls

**Health monitoring:** UptimeRobot pings `GET /api/v1/health` every 5 minutes. Telegram + email on downtime.

**Backup:** Daily `pg_dump` (PostgreSQL) + `mongodump` (MongoDB) → S3 bucket (automated via cron).

**Local development:** Docker Compose (`docker/docker-compose.yml`) still valid for local dev.

```
Docker services (local only):
  quantara_app     — python:3.12-slim, port 8000:8000
  postgres_db      — postgres:16-alpine, port 5432:5432
  redis_cache      — redis:7-alpine, port 6379:6379
  (MongoDB not in Docker compose — install locally for full dev)
```

---

### 7.2 OptionHABot — Local Windows
**Startup:** `start.ps1`
1. Launch MongoDB from `C:\Program Files\MongoDB\Server\8.2\bin\mongod.exe`
2. Create `D:\data\db` and `D:\data\log` directories
3. Activate venv at `D:\OptionHABot\venv\`
4. Launch FastAPI backend (port 8002)

---

### 7.3 TradingBotA — Local Windows
**Startup:** `run.bat`
1. Validate Python 3.12
2. Create/activate `.venv`
3. `pip install -r requirements.txt --only-binary :all:`
4. Create `data/` and `data/logs/`
5. Copy `.env` from `.env.example` if missing
6. Open browser at `http://localhost:8765` (3s delay)
7. Launch `python -m api.main`

---

### 7.4 TradeCopilot — Cloud (Supabase + Vercel/Static Host)
- **Backend:** Supabase (fully managed, no deployment required)
- **Frontend:** `npm run build` → static files → deployed to hosting provider
- **Live domain:** `tradecopilot.in`
- **Edge Functions:** Deployed via Supabase CLI (`supabase functions deploy`)

---

### 7.5 TradingBotwithAIAnalyzer — Local Development
- Backend: Manual Python venv startup
- Frontend: `yarn start` (craco dev server, port 3000)
- No production deployment configured

---

### 7.6 ai_sql_assistant — Local Streamlit
- `streamlit run streamlit_app.py` (port 8501)
- Prototype only — no deployment

---

## 8. Shared Libraries & Patterns

These patterns exist in multiple projects with duplicated code. Each is a candidate for extraction to a shared module.

### 8.1 Zerodha WebSocket Client
| | |
|---|---|
| **Duplicated in** | Quantara (`app/ingestion/broker/zerodha_feed.py`), OptionHABot (`backend/routes/broker.py`), TradingBotA (`api/routes/feed.py`), TradingBotwithAI |
| **Pattern** | Connect on startup, subscribe tokens, handle reconnect with exponential backoff, REST fallback |
| **Reference impl** | Quantara — has FeedHealth monitoring, safe_mode gate |
| **Target location** | `D:\AI_OS\05_content\` (shared broker module) |

### 8.2 Heikin Ashi Candle Builder
| | |
|---|---|
| **Duplicated in** | OptionHABot, TradingBotA, TradingBotwithAIAnalyzer |
| **Formula** | `HA_close = (O+H+L+C)/4`, `HA_open = (prev_HA_open + prev_HA_close)/2` |
| **Interpretation** | Doji (≤40% body) = institutional accumulation; Confirmation = directional resolution |
| **Target location** | `D:\AI_OS\05_content\` |

### 8.3 Kill Switch / Daily Loss Limiter
| | |
|---|---|
| **Duplicated in** | Quantara (most robust), TradingBotA (basic), OptionHABot (partial) |
| **Reference thresholds** | 2 losses → 75% size; 5 losses → pause; daily 2.5% → pause; weekly 6% → pause; drawdown 10% → pause |
| **Reference impl** | Quantara `app/risk/kill_switch.py` + `configs/risk.yaml` |
| **Target location** | Port to all trading projects |

### 8.4 LIMIT→MARKET Fallback Order Logic
| | |
|---|---|
| **Duplicated in** | TradingBotA, TradingBotwithAIAnalyzer |
| **Pattern** | LIMIT at LTP±buffer → wait 5–10s → convert to MARKET if slippage < 3–4pts → else cancel |
| **SEBI note** | MARKET orders always use `market_protection=-1` |
| **Target location** | `D:\AI_OS\05_content\` |

### 8.5 2-Lot Multi-Exit Risk Model
| | |
|---|---|
| **Duplicated in** | TradingBotA, TradingBotwithAIAnalyzer |
| **Pattern** | Lot1 exit at TP1 + SL. Lot2 SL → entry price after Lot1 TP. Lot2 trails from there. |
| **Reference impl** | TradingBotA (cleaner implementation) |

### 8.6 Design System
| | |
|---|---|
| **Source** | `D:\TradingBotwithAIAnalyzer\frontend\design_guidelines.json` |
| **Use** | Canonical reference for all new frontend work |
| **Target location** | Copy to `D:\AI_OS\07_templates\design_guidelines.json` |
| **Key values** | Dark mode. Chivo/IBM Plex Sans/JetBrains Mono. Emerald-500/Red-500/Indigo-600. No shadows. 1px borders. |

---

## 9. Agent Systems

### 9.1 Quantara Agent System
**Specification files:** `D:\AI_OS\06_agents\quantara\`

| File | Agent | Status | Priority |
|---|---|---|---|
| `00_system-overview.md` | System architecture | Spec complete | — |
| `01_news-agent.md` | News / Macro Events | NOT IMPLEMENTED | Medium |
| `02_regime-agent.md` | Regime (Vol, Market, Session) | PARTIALLY IMPLEMENTED | Medium |
| `03_signal-agent.md` | Signal Generation | IMPLEMENTED (formalized) | — |
| `04_debate-agent.md` | Adversarial Signal Review | NOT IMPLEMENTED | High |
| `05_risk-agent.md` | Kill Switch + Sizing | IMPLEMENTED (formalized) | — |
| `06_portfolio-agent.md` | Portfolio Heat + Learning | NOT IMPLEMENTED | Medium |
| `07_execution-agent.md` | Trade Lifecycle | PARTIALLY IMPLEMENTED | Critical |
| `08_monitoring-agent.md` | Observability + Alerts | PARTIALLY IMPLEMENTED | High |

**Agent activation order:**
```
08:00 IST  — News Agent (load events.yaml, optionally call Claude haiku)
09:14 IST  — Regime Agent, Risk Agent, Portfolio Agent initialize
09:44 IST  — Signal Agent activates (first bar eligible at 09:45)
On signal  — Debate Agent (Claude sonnet, only on A/A+ signals)
On signal  — Execution Agent (paper: immediate; live: after Debate)
Always     — Monitoring Agent (StatusWriter every 5s, alerts streaming)
```

**Shared Redis bus channels:**
```
quantara:bus:features          — FeatureVector (per bar)
quantara:bus:regime            — RegimeContext (per bar)
quantara:bus:agent_decisions   — All AgentDecision verdicts
quantara:bus:signal_candidates — SignalDecision (per A/A+ signal)
quantara:bus:debate_verdicts   — DebateVerdict (per signal)
quantara:bus:trade_events      — Trade lifecycle (ENTRY/EXIT/SL/TP/KILL)
quantara:bus:alerts            — SystemAlert (streaming)
```

**Standard AgentDecision contract:**
```python
AgentDecision:
    agent_id: str
    trace_id: UUID
    timestamp: datetime
    verdict: "PROCEED" | "BLOCK" | "WARN" | "ABSTAIN"
    confidence: float        # 1.0 for deterministic agents
    reasons: List[str]
    blocking_reasons: List[str]
    metadata: Dict[str, Any]
```

**Claude integration points:**

| Agent | Model | Purpose | Failure behavior |
|---|---|---|---|
| Debate Agent | claude-sonnet-4-6 | Adversarial signal review | CONFIRM (never blocks) |
| News Agent | claude-haiku-4-5-20251001 | Unstructured text event parsing | WARN (not BLOCK) |
| Monitoring Agent | claude-haiku-4-5-20251001 | Alert classification (optional) | Skip AI, use rule-based |

**Prompt caching:** `cache_control: {type: "ephemeral"}` mandatory on all system prompt blocks.

---

### 9.2 Other Projects — Agent Status
- **TradeCopilot:** No agent system. Groq used for single-turn coaching insights.
- **OptionHABot:** `anthropic` package installed, not wired to any agent.
- **TradingBotA:** No AI agents.
- **TradingBotwithAI:** Anthropic integrated at backend level (details TBD).

---

## 10. Automation & CI/CD

### 10.1 Quantara — GitHub Actions
**File:** `.github/workflows/ci.yml`

```yaml
Trigger:
  push:    branches: [main, develop]
  pull_request: branches: [main]

Jobs:
  test (ubuntu-latest):
    - Python 3.12 setup
    - pip install ruff pytest pytest-cov pytest-asyncio
    - ruff check app/ tests/                    (linting)
    - pytest tests/ --cov=app --cov-report=term-missing -v
    - Check for hardcoded thresholds in strategy files
```

Coverage target: 30%+ (currently). No deploy step in CI.

---

### 10.2 TradeCopilot — Supabase pg_cron

| Job | Schedule | Purpose |
|---|---|---|
| `kite-auto-login` | 08:30 IST daily | Auto-refresh Zerodha access token |
| `market-snapshot` | Every 1 minute | Capture market data during session |
| `daily-trade-sync` | 16:00 IST daily | Sync trade data, trigger AI daily review |

---

### 10.3 Missing Automation (gaps)
- OptionHABot: No CI/CD. No test suite.
- TradingBotA: No CI/CD. `run.bat` only.
- TradingBotwithAI: No CI/CD.
- ai_sql_assistant: No CI/CD.

---

## 11. Configuration Files Index

### Quantara (`D:\quantara\configs\`)

| File | Contents | Key values |
|---|---|---|
| `system.yaml` | App env, market hours, timeframes | `execution_enabled: false`, market open 09:15, signal_start 09:45, hard_square_off 15:20, lunch_chop 11:45–13:15 |
| `risk.yaml` | Kill switch thresholds, sizing multipliers | risk_per_trade 1%, daily_loss 2.5%, weekly_loss 6%, drawdown_pause 10%, kill_at 5 losses, reduce_at 2 |
| `confidence.yaml` | Score weights and thresholds | A+≥0.72, A≥0.58; weights: setup 0.30, premium 0.25, liquidity 0.15, structure 0.10, htf 0.10, regime 0.07, execution 0.03 |
| `execution.yaml` | Slippage, fill logic, strike selection | slippage: low 0.10, normal 0.20, high 0.40, expiry 0.60; premium_max_loss: OPA 0.40, PES 0.35, SFR 0.35 |
| `setups.yaml` | OPA/PES/SFR time windows + thresholds | OPA 09:45–10:20, PES 10:00–14:30, SFR anytime |
| `features.yaml` | Feature computation parameters | P_DIV strong_bullish=1.25, RS_spread bullish=1.0, ATR period=14, zscore_window=20 |
| `telegram.yaml` | Delivery settings | max_signals_per_day=4, no_trade_limit=3 |
| `database.yaml` | Pool settings, Redis TTL | pool_size=10, max_overflow=20, redis_ttl=600s |
| `learning.yaml` | Clustering, review settings | min_sample=30, monthly_review, no auto_optimization |
| `replay.yaml` | Determinism settings | strict_mode=true, parity_required=true, deterministic_hash=true |

**Files to be created (per agent specs):**

| File | Required by | Purpose |
|---|---|---|
| `configs/events.yaml` | News Agent | Macro event calendar (RBI, Budget, etc.) |
| `configs/monitoring.yaml` | Monitoring Agent | Alert thresholds (all magic numbers) |

---

### TradingBotA (`D:\Trading_bot_a\`)

All configuration via `.env`:
- `TRADING_MODE=paper`
- `SIGNAL_THRESHOLD=0.005` (0.5% body move minimum)
- `TP1_POINTS=30`, `SL_POINTS=15` (Lot 1)
- `TRAIL_STEP=10` (Lot 2 trailing)
- `LOT_SIZE=75`, `TRADE_LOTS=2`
- `START_TIME=09:20`, `END_TIME=15:15`

---

## 12. Environment Variables Reference

Variables listed by category. **Do not store real values here.** Reference `.env` and `.env.example` files.

### Broker
| Variable | Used by | Purpose |
|---|---|---|
| `ZERODHA_API_KEY` | Quantara, TradeCopilot, TradingBotA | Kite Connect API key |
| `ZERODHA_API_SECRET` | Quantara, TradingBotA | Kite Connect API secret |
| `REACT_APP_KITE_API_KEY` | TradeCopilot | Kite key (frontend — READ ONLY) |
| `DHAN_API_KEY` | Quantara | Placeholder — not active |

### AI APIs
| Variable | Used by | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | OptionHABot | Claude API key |
| `REACT_APP_GROQ_API_KEY` | TradeCopilot | Groq key — SECURITY RISK (frontend) |

**CRITICAL:** `REACT_APP_GROQ_API_KEY` in TradeCopilot's `.env` is exposed to the browser. This key must be rotated and moved to Supabase Edge Function secrets.

### Databases
| Variable | Used by | Purpose |
|---|---|---|
| `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` | Quantara | PostgreSQL connection |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` | Quantara | Redis connection |
| `MONGO_URL` / `DB_NAME` | OptionHABot | MongoDB connection |
| `REACT_APP_SUPABASE_URL` / `REACT_APP_SUPABASE_ANON_KEY` | TradeCopilot | Supabase client |
| `DATABASE_URL` | ai_sql_assistant | Neon PostgreSQL connection string |

### Messaging
| Variable | Used by | Purpose |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Quantara | Bot API token |
| `TELEGRAM_CHAT_ID` | Quantara | Subscriber channel / chat ID |

### Payments & Auth
| Variable | Used by | Purpose |
|---|---|---|
| `REACT_APP_RAZORPAY_KEY_ID` | TradeCopilot | Razorpay live key (frontend) |
| `SECRET_KEY` | OptionHABot | JWT signing key |

### App Config
| Variable | Used by | Purpose |
|---|---|---|
| `APP_ENV` | Quantara | `paper` / `live` — controls execution gate and docs |
| `TRADING_MODE` | TradingBotA | `paper` / `live` |
| `LOG_LEVEL` | Quantara, TradingBotA | `INFO` / `DEBUG` |
| `PORT` | OptionHABot | Server port (default 8002) |
| `DASHBOARD_PORT` | TradingBotA | Dashboard port (default 8765) |
| `FRONTEND_URL` | OptionHABot | CORS allowed origin |

---

## 13. Dependency Matrix

### Python packages (cross-project)

| Package | Quantara | OptionHABot | TradingBotA | TradingBotwithAI |
|---|---|---|---|---|
| fastapi | 0.115+ | 0.111 | 0.111 | 0.110 |
| uvicorn | latest | 0.29 | 0.29 | 0.25 |
| pydantic | 2.7+ | 2.6.4 | 2.7.1 | 2.12 |
| kiteconnect | — | 5.0.1 | 5.0.1 | 5.0.1 |
| websockets | 12.0+ | 12.0 | 12.0 | 15.0 |
| asyncpg | 0.29+ | — | — | — |
| sqlalchemy | 2.0+ | — | 2.0.30 | — |
| motor | — | 3.3.2 | — | 3.3.1 |
| redis | 5.0.4+ | — | — | — |
| anthropic | — | 0.28.0 | — | present |
| pandas | 2.2+ | — | 2.1+ | 2.3.3 |
| numpy | 1.26+ | — | 1.26+ | 2.3.3 |
| aiosqlite | — | — | 0.20 | — |
| python-dotenv | 1.0.1 | 1.0.1 | 1.0.1 | 1.1.1 |
| pytz | 2024.1 | 2024.1 | — | — |
| loguru | 0.7.2 | — | — | — |
| TA-Lib | — | — | — | 0.6.7 |
| boto3 | — | — | — | 1.40 |

### JavaScript packages (cross-project)

| Package | TradeCopilot | TradingBotwithAI |
|---|---|---|
| react | 19.2 | 19.0 |
| react-dom | 19.2 | 19.0 |
| typescript | 4.9 | (via craco) |
| tailwindcss | 3.4 | 3.x |
| @supabase/supabase-js | 2.105 | — |
| @radix-ui/* | — | Full suite |
| react-router-dom | 7.15 | 7.5 |
| lucide-react | 1.16 | 0.507 |
| recharts | — | 3.2 |
| zod | — | 3.24 |
| react-hook-form | — | 7.56 |
| framer-motion | 12.38 | — |
| xlsx | 0.18.5 | — |

---

## 14. Tech Debt Register

Ordered by impact. Each item has a clear remediation path.

| # | Issue | Affected | Severity | Remediation |
|---|---|---|---|---|
| 1 | **Groq API key in browser** | TradeCopilot | Critical | Move to Supabase Edge Function secret. Remove `REACT_APP_GROQ_API_KEY` from frontend `.env`. |
| 2 | **Groq → Claude migration** | TradeCopilot | High | Create `claude-ai` Supabase Edge Function. Update `claudeApi.ts`. Retire `groq-ai` function. |
| 3 | **No CI/CD for OptionHABot, TradingBotA, TradingBotwithAI** | 3 projects | High | Copy Quantara's `ci.yml` pattern. Add pytest coverage gates. |
| 4 | **Anthropic installed in OptionHABot but not wired** | OptionHABot | Medium | Design OptionHABot agent spec. Wire `anthropic` package to a strategy advisor. |
| 5 | **Kill switch duplicated across 3 bots** | OptionHABot, TradingBotA, TradingBotwithAI | Medium | Extract `D:\AI_OS\05_content\risk\kill_switch.py` from Quantara pattern. Import in all bots. |
| 6 | **Zerodha WS client duplicated in 4 projects** | All trading | Medium | Extract to shared module. Single source of truth for reconnect logic. |
| 7 | **HA candle builder duplicated in 3 projects** | OptionHABot, TradingBotA, TradingBotwithAI | Medium | Extract to `D:\AI_OS\05_content\market\heikin_ashi.py`. |
| 8 | **No test coverage on OptionHABot** | OptionHABot | Medium | Add pytest suite. Focus on: pattern detection, trailing stop ratchet, user isolation. |
| 9 | **Design system not extracted to templates** | All frontend | Low | Copy `design_guidelines.json` to `D:\AI_OS\07_templates\`. |
| 10 | **Quantara News Agent gap** | Quantara | Medium | `NoTradeReason.MACRO_EVENT` exists in enum but nothing populates it. Implement News Agent (1 day — calendar-based, no Claude required). |
| 11 | **Port 8000 conflict** | Quantara + TradingBotwithAI | Low | Assign TradingBotwithAI backend a non-conflicting port. |
| 12 | **MongoDB version drift** | OptionHABot vs TradingBotwithAI | Low | Motor 3.3.2 vs 3.3.1 — align to latest. |
| 13 | **TradingBotA `.env` has placeholder Kite keys** | TradingBotA | Info | Confirm paper mode is default before any live trading. |
| 14 | **ai_sql_assistant hardcoded DB URL** | ai_sql_assistant | Info | Move `DATABASE_URL` to `.env`. Prototype only — low urgency. |

---

*This document is derived from actual repository analysis. Update it when: a new project is added, a port changes, a new external service is integrated, a tech debt item is resolved, or a new agent is deployed.*
