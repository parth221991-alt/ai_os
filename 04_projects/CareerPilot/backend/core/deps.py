from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from models.database import get_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    settings = get_settings()
    factory = get_session_factory(settings.database_url)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
