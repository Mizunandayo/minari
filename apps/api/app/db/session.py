"""Async POSTRGRES POOL (asyncpg)"""


from __future__ import annotations
import asyncpg
from app.core.config import get_settings
from app.core.logging import get_logger


log = get_logger(__name__)
_pool: asyncpg.Pool | None = None


def get_pool() -> asyncpg.Pool | None:
    """Live accessor — always reflects the current pool (not a stale import).

    Callers must use this, NOT ``from app.db.session import _pool``: that binds the
    name to ``None`` at import time and never sees ``init_pool()``'s reassignment.
    """
    return _pool


async def init_pool() -> None:
    """Create the connection pool.

    A connection failure must NOT crash the whole service: Cloud Run should still
    start and serve ``/healthz`` (reporting ``db: "fail"``) so the platform's
    health check — not an import-time exception — governs readiness. We log the
    error and leave ``_pool`` as ``None``; ``ping_db()`` then reports the outage.
    """
    global _pool
    settings = get_settings()
    try:
        _pool = await asyncpg.create_pool(
            dsn=settings.database_url.get_secret_value(),
            min_size=1,
            max_size=5,
            command_timeout=10,
        )
        log.info("db.pool.created")
    except Exception as exc:  # noqa: BLE001 - startup must survive a DB outage
        _pool = None
        log.error("db.pool.failed", error=str(exc), error_type=type(exc).__name__)




async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        log.info("db.pool.closed")


async def ping_db() -> bool:
    if _pool is None:
        return False
    try:
        async with _pool.acquire() as conn:
            return await conn.fetchval("SELECT 1") == 1
    except Exception as exc: 
        log.warning("db.ping.failed", error=str(exc))
        return False
    