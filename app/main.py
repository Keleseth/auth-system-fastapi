from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.core.config import settings
from app.api import main_router
from app.scripts.test_users import create_admin_author_moderator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.db_engine = None
    try:
        engine = create_async_engine(settings.database_url, pool_pre_ping=True)
        async with engine.begin() as _:
            pass
        app.state.db_engine = engine

        async with AsyncSession(engine, expire_on_commit=False) as session:
            await create_admin_author_moderator(session)
        yield
    finally:
        engine: AsyncEngine | None = getattr(app.state, 'db_engine', None)
        if engine is not None:
            await engine.dispose()


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version='1.0.0',
    lifespan=lifespan,
)
app.include_router(main_router)
