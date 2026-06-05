"""AST-level"""


from __future__ import annotations

from tree_sitter import Node

from app.core.logging import get_logger
from app.services.fixes.grammars import parser_for

log = get_logger(__name__)













def _node_text(node: Node) -> str:
    return (node.text or b"").decode("utf-8", errors="replace")


def _normalize(text: str) -> str:
    return " ".join(text.split())




def _callee_text(call: Node) -> str:
    fn = call.child_by_field_name("function") or (call.children[0] if call.children else None)
    return _node_text(fn).lower() if fn is not None else ""




def _is_assertion(grammar: str, node: Node) -> bool:
    t = node.type
    text = _node_text(node)

    if grammar == "python":
        if t == "assert_statement":           
            return True
        if t == "call":                       
            
            callee = _callee_text(node).rsplit(".", 1)[-1]
            return callee.startswith("assert") or callee in {"raises", "fail"}

    elif grammar in {"javascript", "typescript", "tsx"}:
        if t == "call_expression":
            low = text.lower()
            return (
                low.startswith("expect(")
                or low.startswith("assert.")
                or low.startswith("assert(")
            )

    elif grammar == "go":
        if t == "call_expression":
            callee = _callee_text(node)
            return (
                callee.startswith("assert.") or callee.startswith("require.")
                or callee in {"t.error", "t.errorf", "t.fatal", "t.fatalf"}
            )

    elif grammar == "java":
        if t == "method_invocation":
            name = _node_text(node.child_by_field_name("name") or node).lower()
            return name.startswith("assert")
    return False






def _walk(node: Node):
    yield node
    for child in node.children:
        yield from _walk(child)







def _extract(grammar: str, source: str) -> list[str]:
    try:
        tree = parser_for(grammar).parse(source.encode("utf-8", errors="replace"))
    except Exception as exc:
        log.warning("fix.assert.parse_error", grammar=grammar, error=str(exc))
        return []
    found: list[str] = []
    for node in _walk(tree.root_node):
        if _is_assertion(grammar, node):
            found.append(_normalize(_node_text(node)))
    return found





def assertions_preserved(grammar: str, original: str, fixed: str) -> bool:
    """True iff every assertion in `original` still appears verbatim in `fixed`."""
    original_asserts = _extract(grammar, original)
    if not original_asserts:
      return True
    fixed_set = set(_extract(grammar, fixed))
    missing = [a for a in original_asserts if a not in fixed_set]
    if missing:
        log.warning("fix.assert.violation", grammar=grammar, missing=missing[:3])
        return False
    return True

