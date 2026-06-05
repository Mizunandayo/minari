"""Security primitives constant-time API-key auth + security headers"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time as _time

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





def _stream_key() -> bytes:
    return hashlib.sha256(
        b"minari-stream:" + get_settings().demo_api_key.get_secret_value().encode()
    ).digest()




def mint_stream_token(run_id: str) -> str:
    """Single-use-ish, TTL-bounded HMAC token binding the bearer to one run."""
    exp = int(_time.time()) + get_settings().stream_token_ttl_seconds
    msg = f"{run_id}.{exp}".encode()
    sig = hmac.new(_stream_key(), msg, hashlib.sha256).digest()
    return f"{exp}.{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"






def verify_stream_token(run_id: str, token: str) -> bool:
    try:
        exp_str, sig_b64 = token.split(".", 1)
        exp = int(exp_str)
    except (ValueError, AttributeError):
        return False
    if exp < int(_time.time()):
        return False
    expected = hmac.new(_stream_key(), f"{run_id}.{exp}".encode(), hashlib.sha256).digest()
    pad = "=" * (-len(sig_b64) % 4)
    try:
        given = base64.urlsafe_b64decode(sig_b64 + pad)
    except Exception:
        return False
    return hmac.compare_digest(expected, given)
