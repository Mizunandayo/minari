"""Structured JSON logging via structlog"""

from __future__ import annotations
import logging
import sys
from typing import Any
import structlog

_SENSITIVE_KEYS = {"token", "api_key", "password", "secret", "authorization", "database_url"}




def _redact(_: Any, __: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    for key in list(event_dict.keys()):
        if any(marker in key.lower() for marker in _SENSITIVE_KEYS):
            event_dict[key] = "***REDACTED***"
    return event_dict

 
def configure_logging(*, json_logs: bool, level: str = "INFO") -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=level)

    shared = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        _redact,
        structlog.processors.StackInfoRenderer(),
    ]
    renderer = (
        structlog.processors.JSONRenderer()
        if json_logs
        else structlog.dev.ConsoleRenderer(colors=True)
    )

    structlog.configure(
        processors=[*shared, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(level)),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "minari") -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)


