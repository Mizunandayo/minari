"""Rate limiting via slowapi.

In production, Redis (Upstash) is the shared counter store so limits hold across
multiple Cloud Run instances. In development/test, we fall back to in-process
memory storage so a running Redis is not required to boot or run the suite.
Limits are still enforced per-process locally — only cross-instance sharing is
dropped, which does not matter for a single dev process.
"""

from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import get_settings

settings = get_settings()

_storage_uri = (
    settings.redis_url.get_secret_value() if settings.is_production else "memory://"
)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=_storage_uri,
    strategy="fixed-window",
    default_limits=["60/minute"],
)

DIAGNOSIS_LIMIT = "10/minute"