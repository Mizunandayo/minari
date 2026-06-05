"""tree-sitter syntax validation"""






from __future__ import annotations

from app.core.logging import get_logger
from app.services.fixes.grammars import parser_for

log = get_logger(__name__)
MAX_SOURCE_BYTES = 200_000












def is_syntax_valid(grammar: str, source: str) -> bool:
    data = source.encode("utf-8", errors="replace")
    if len(data) > MAX_SOURCE_BYTES:
        log.warning("fix.syntax.oversize", grammar=grammar, bytes=len(data))
        return False
    try:
        tree = parser_for(grammar).parse(data)
    except Exception as exc:  
        log.warning("fix.syntax.parse_error", grammar=grammar, error=str(exc))
        return False
    return not tree.root_node.has_error