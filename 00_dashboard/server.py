"""
AI_OS Company Command Center — Backend
FastAPI + SQLite · Port 8006
"""

import sqlite3
import json
import asyncio
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Path as FPath
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

_probe_pool = ThreadPoolExecutor(max_workers=8)

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "tasks.db"
HTML_PATH = BASE_DIR / "index.html"

app = FastAPI(title="AI_OS Command Center", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

@contextmanager
def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS agents (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            model       TEXT DEFAULT 'claude-sonnet-4-6',
            status      TEXT DEFAULT 'idle',
            color       TEXT DEFAULT '#4f46e5',
            avatar      TEXT DEFAULT '??',
            current_task_id INTEGER,
            last_active TEXT
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT DEFAULT '',
            assigned_to TEXT DEFAULT '',
            assigned_by TEXT DEFAULT 'Founder',
            project     TEXT DEFAULT '',
            status      TEXT DEFAULT 'backlog',
            priority    TEXT DEFAULT 'P2',
            tags        TEXT DEFAULT '[]',
            created_at  TEXT DEFAULT (datetime('now','localtime')),
            updated_at  TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS activity (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            agent       TEXT NOT NULL,
            action      TEXT NOT NULL,
            task_id     INTEGER,
            notes       TEXT DEFAULT '',
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        );
        """)

        # Seed agents
        agents = [
            ("chief_of_staff",      "Chief of Staff",       "claude-sonnet-4-6",          "idle", "#6366f1", "CoS"),
            ("engineering_director","Engineering Director",  "claude-sonnet-4-6",          "idle", "#10b981", "ED"),
            ("operations_manager",  "Operations Manager",   "claude-haiku-4-5-20251001",  "idle", "#f59e0b", "OM"),
            ("research_lead",       "Research Lead",        "claude-sonnet-4-6",          "idle", "#a855f7", "RL"),
            ("growth_director",     "Growth Director",      "claude-sonnet-4-6",          "idle", "#3b82f6", "GD"),
            ("content_director",    "Content Director",     "claude-haiku-4-5-20251001",  "idle", "#ec4899", "CD"),
        ]
        for a in agents:
            conn.execute(
                "INSERT OR IGNORE INTO agents (id,name,model,status,color,avatar) VALUES (?,?,?,?,?,?)",
                a
            )

        # Seed tasks from standup (only if table is empty)
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            tasks = [
                ("Quantara test coverage sprint",
                 "Lift coverage from 14% → 40%+. Order: kill_switch.py → data_validity.py → pre_submission_guard.py. Target 95%+ on these 3 files before Stage 1 capital.",
                 "engineering_director", "Founder", "Quantara", "in_progress", "P0"),

                ("Resolve Quantara design questions (DQ-001 to DQ-008)",
                 "8 open questions block Stage 1 live capital. Priority 3 today: (1) TOTP refresh strategy, (2) 45s fill timeout behavior, (3) NSE holiday calendar source.",
                 "research_lead", "chief_of_staff", "Quantara", "in_progress", "P1"),

                ("CareerPilot LinkedIn Easy Apply worker",
                 "Playwright-based LinkedIn Easy Apply implementation in workers/scrapers/linkedin.ts. Apply worker is the last functional gap before end-to-end test.",
                 "engineering_director", "Founder", "CareerPilot", "backlog", "P1"),

                ("Rotate TradeCopilot secrets (Groq + Razorpay)",
                 "Check git history on D:\\tradecopilot and D:\\AI_OS\\04_projects\\TradingCopilot. If either key was ever committed, rotate immediately. Groq key: gsk_... Razorpay: rzp_live_...",
                 "operations_manager", "chief_of_staff", "TradeCopilot", "backlog", "P1"),

                ("TradeCopilot: Groq → Claude Haiku migration",
                 "Replace Groq API calls with Claude Haiku via server-side Supabase Edge Function. Removes frontend API key exposure (P1 compliance item).",
                 "engineering_director", "Founder", "TradeCopilot", "backlog", "P2"),

                ("Extract reusable modules to AI_SNIPP",
                 "Extract: Zerodha WS client, HA candle builder, LIMIT→MARKET fallback, kill switch, 2-lot exit model. Target: D:\\AI_OS\\05_content\\shared_modules\\",
                 "content_director", "chief_of_staff", "AI_SNIPP", "backlog", "P3"),
            ]
            for t in tasks:
                conn.execute(
                    "INSERT INTO tasks (title,description,assigned_to,assigned_by,project,status,priority) VALUES (?,?,?,?,?,?,?)",
                    t
                )

            # Seed initial activity
            activity = [
                ("chief_of_staff",      "Morning standup completed — all 6 agents reported", None, "OptionHABot live. Quantara paper gate cleared. Test coverage is P0 blocker."),
                ("engineering_director","Test coverage sprint started",                        1,    "Priority: kill_switch.py → data_validity.py → pre_submission_guard.py"),
                ("operations_manager",  "OptionHABot health check: running",                  None, "Port 8004 live. No incidents over weekend."),
            ]
            for act in activity:
                conn.execute(
                    "INSERT INTO activity (agent,action,task_id,notes) VALUES (?,?,?,?)",
                    act
                )


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    assigned_to: str = ""
    assigned_by: str = "Founder"
    project: str = ""
    status: str = "backlog"
    priority: str = "P2"
    tags: list[str] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_by: Optional[str] = None
    project: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[list[str]] = None


class AgentUpdate(BaseModel):
    status: Optional[str] = None
    current_task_id: Optional[int] = None


class ActivityCreate(BaseModel):
    agent: str
    action: str
    task_id: Optional[int] = None
    notes: str = ""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def dashboard():
    if HTML_PATH.exists():
        return HTMLResponse(content=HTML_PATH.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Dashboard HTML not found — run setup</h1>", status_code=404)


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


SYSTEMS = {
    "quantara":    {"port": 8000, "path": "/health",  "label": "Quantara"},
    "optionhabot": {"port": 8004, "path": "/health",  "label": "OptionHABot"},
    "tradingbota": {"port": 8765, "path": "/health",  "label": "TradingBotA"},
    "careerpilot": {"port": 8005, "path": "/health",  "label": "CareerPilot"},
    "tradecopilot":{"port": 3000, "path": "/",        "label": "TradeCopilot"},
}

def _ping(key: str, cfg: dict) -> dict:
    url = f"http://127.0.0.1:{cfg['port']}{cfg['path']}"
    try:
        with urllib.request.urlopen(url, timeout=1.5) as r:
            body = {}
            try: body = json.loads(r.read())
            except Exception: pass
            return {"key": key, "label": cfg["label"], "port": cfg["port"],
                    "up": True, "detail": body}
    except Exception as exc:
        return {"key": key, "label": cfg["label"], "port": cfg["port"],
                "up": False, "detail": str(exc)[:80]}

@app.get("/api/probe")
async def probe_systems():
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(_probe_pool, _ping, k, v) for k, v in SYSTEMS.items()]
    results = await asyncio.gather(*tasks)
    return {r["key"]: r for r in results}


@app.get("/api/agents")
def list_agents():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT a.*, t.title as current_task_title, t.priority as current_task_priority
            FROM agents a
            LEFT JOIN tasks t ON a.current_task_id = t.id
        """).fetchall()
        return [dict(r) for r in rows]


@app.patch("/api/agents/{agent_id}")
def update_agent(agent_id: str, body: AgentUpdate):
    fields, vals = [], []
    if body.status is not None:
        fields.append("status = ?")
        vals.append(body.status)
    if body.current_task_id is not None:
        fields.append("current_task_id = ?")
        vals.append(body.current_task_id)
    fields.append("last_active = datetime('now','localtime')")
    if not fields:
        raise HTTPException(400, "No fields to update")
    vals.append(agent_id)
    with get_db() as conn:
        conn.execute(f"UPDATE agents SET {', '.join(fields)} WHERE id = ?", vals)
    return {"ok": True}


@app.get("/api/tasks")
def list_tasks(status: Optional[str] = None, assigned_to: Optional[str] = None, project: Optional[str] = None):
    where, params = [], []
    if status:
        where.append("status = ?")
        params.append(status)
    if assigned_to:
        where.append("assigned_to = ?")
        params.append(assigned_to)
    if project:
        where.append("project = ?")
        params.append(project)
    clause = f"WHERE {' AND '.join(where)}" if where else ""
    with get_db() as conn:
        rows = conn.execute(f"SELECT * FROM tasks {clause} ORDER BY CASE priority WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 ELSE 3 END, id", params).fetchall()
        return [dict(r) for r in rows]


@app.post("/api/tasks", status_code=201)
def create_task(body: TaskCreate):
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title,description,assigned_to,assigned_by,project,status,priority,tags) VALUES (?,?,?,?,?,?,?,?)",
            (body.title, body.description, body.assigned_to, body.assigned_by,
             body.project, body.status, body.priority, json.dumps(body.tags))
        )
        task_id = cur.lastrowid
        if body.assigned_to:
            conn.execute(
                "INSERT INTO activity (agent,action,task_id,notes) VALUES (?,?,?,?)",
                ("chief_of_staff", f"Task assigned to {body.assigned_to}", task_id, body.title)
            )
        return {"id": task_id}


@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int = FPath(...), body: TaskUpdate = None):
    fields, vals = [], []
    if body.title is not None:
        fields.append("title = ?"); vals.append(body.title)
    if body.description is not None:
        fields.append("description = ?"); vals.append(body.description)
    if body.assigned_to is not None:
        fields.append("assigned_to = ?"); vals.append(body.assigned_to)
    if body.assigned_by is not None:
        fields.append("assigned_by = ?"); vals.append(body.assigned_by)
    if body.project is not None:
        fields.append("project = ?"); vals.append(body.project)
    if body.status is not None:
        fields.append("status = ?"); vals.append(body.status)
    if body.priority is not None:
        fields.append("priority = ?"); vals.append(body.priority)
    if body.tags is not None:
        fields.append("tags = ?"); vals.append(json.dumps(body.tags))
    if not fields:
        raise HTTPException(400, "No fields to update")
    fields.append("updated_at = datetime('now','localtime')")
    vals.append(task_id)
    with get_db() as conn:
        conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", vals)
    return {"ok": True}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    with get_db() as conn:
        conn.execute("UPDATE tasks SET status = 'archived' WHERE id = ?", (task_id,))
    return {"ok": True}


@app.get("/api/activity")
def list_activity(limit: int = 50):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM activity ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


@app.post("/api/activity", status_code=201)
def log_activity(body: ActivityCreate):
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO activity (agent,action,task_id,notes) VALUES (?,?,?,?)",
            (body.agent, body.action, body.task_id, body.notes)
        )
        conn.execute(
            "UPDATE agents SET last_active = datetime('now','localtime') WHERE id = ?",
            (body.agent,)
        )
        return {"id": cur.lastrowid}


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Task not found")
        return dict(row)


@app.get("/api/activity/task/{task_id}")
def activity_for_task(task_id: int):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM activity WHERE task_id = ? ORDER BY id DESC LIMIT 30", (task_id,)
        ).fetchall()
        return [dict(r) for r in rows]


@app.post("/api/session/wrap")
def session_wrap(body: dict):
    """Called by /morning when context limit approaches. Saves wrap state."""
    with get_db() as conn:
        conn.execute(
            "INSERT INTO activity (agent,action,notes) VALUES (?,?,?)",
            ("chief_of_staff", "Session wrapped — context limit",
             body.get("notes", "Resume with /morning in next session"))
        )
        # Reset any agents still marked active back to idle
        conn.execute("UPDATE agents SET status = 'idle', current_task_id = NULL WHERE status = 'active'")
    return {"ok": True}


@app.get("/api/stats")
def stats():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tasks WHERE status != 'archived'").fetchone()[0]
        by_status = {r[0]: r[1] for r in conn.execute(
            "SELECT status, COUNT(*) FROM tasks WHERE status != 'archived' GROUP BY status"
        ).fetchall()}
        by_priority = {r[0]: r[1] for r in conn.execute(
            "SELECT priority, COUNT(*) FROM tasks WHERE status NOT IN ('done','archived') GROUP BY priority"
        ).fetchall()}
        active_agents = conn.execute(
            "SELECT COUNT(*) FROM agents WHERE status = 'active'"
        ).fetchone()[0]
        return {
            "total_tasks": total,
            "by_status": by_status,
            "by_priority": by_priority,
            "active_agents": active_agents,
        }


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8006, reload=False)
