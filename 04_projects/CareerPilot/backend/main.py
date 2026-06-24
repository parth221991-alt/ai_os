import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

from api.applications import router as applications_router
from api.email_routes import router as email_router
from api.jobs import router as jobs_router
from api.profiles import router as profiles_router
from api.resume import router as resume_router
from core.config import get_settings, get_yaml_config
from models.database import Base, get_engine
from scheduler.jobs import create_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
log = logging.getLogger("careerpilot")

_scheduler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler
    settings = get_settings()
    cfg = get_yaml_config()

    # Init DB tables
    engine: AsyncEngine = get_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.info("Database tables initialized")

    # Start scheduler
    _scheduler = create_scheduler(cfg)
    _scheduler.start()
    log.info("Scheduler started")

    yield

    # Shutdown
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
    await engine.dispose()
    log.info("CareerPilot shutdown complete")


def create_app() -> FastAPI:
    cfg = get_yaml_config()

    app = FastAPI(
        title="CareerPilot",
        version=cfg["app"]["version"],
        description="Personal career assistant — job discovery, auto-apply, resume intelligence",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3003"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(profiles_router)
    app.include_router(jobs_router)
    app.include_router(applications_router)
    app.include_router(resume_router)
    app.include_router(email_router)

    @app.get("/health")
    async def health():
        return {"status": "ok", "app": "CareerPilot"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    cfg = get_yaml_config()
    uvicorn.run(
        "main:app",
        host=cfg["app"]["host"],
        port=cfg["app"]["port"],
        reload=True,
    )
