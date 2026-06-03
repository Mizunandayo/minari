"""Minari API entrypoint"""


from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.api.v1.router import api_v1
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.core.rate_limit import limiter
from app.core.security import SecurityHeadersMiddleware
from app.db.session import close_pool, init_pool








settings = get_settings()
configure_logging(json_logs=settings.is_production)
log = get_logger("minari")





@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    log.info("app.startup", env=settings.env)
    yield
    await close_pool()
    log.info("app.shutdown")







def create_app() -> FastAPI:
    app = FastAPI(
        title="Minari API",
        version="0.1.0",
        docs_url=None if settings.is_production else "/docs",  # no public docs in prod
        redoc_url=None,
        openapi_url=None if settings.is_production else "/openapi.json",
        lifespan=lifespan,
    )


    

    # Rate limiting (order matters: register limiter + handler + middleware)
    app.state.limiter = limiter
    app.add_exception_handler(
        RateLimitExceeded,
        lambda r, e: JSONResponse({"ok": False, "error": "rate_limited"}, status_code=429),
    )
    app.add_middleware(SlowAPIMiddleware)




    # CORS exact origins only
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["X-API-Key", "Content-Type"],
        max_age=600,
    )

    app.add_middleware(SecurityHeadersMiddleware)
    app.include_router(api_v1)
    return app




app = create_app()





@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"service": "minari-api", "status": "ok"}


