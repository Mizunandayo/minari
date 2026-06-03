"""Security primitives constant-time API-key auth + security headers"""

from __future__ import annotations
import hmac
from fastapi import Header, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.config import get_settings





_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or missing API key.",
    headers={"WWW-Authenticate": "API-Key"},
)




async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """FastAPI dependency. Rejects requests without a valid demo API key."""
    settings = get_settings()
    expected = settings.demo_api_key.get_secret_value()
    if x_api_key is None or not hmac.compare_digest(x_api_key, expected):
        raise _UNAUTHORIZED



class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds hardened response headers"""

    async def dispatch(self, request: Request, call_next):  
        response: Response = await call_next(request)
        h = response.headers
        h["X-Content-Type-Options"] = "nosniff"
        h["X-Frame-Options"] = "DENY"
        h["Referrer-Policy"] = "no-referrer"
        h["Cross-Origin-Opener-Policy"] = "same-origin"
        h["Cross-Origin-Resource-Policy"] = "same-origin"
        h["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        h["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        if get_settings().is_production:
            h["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        return response
