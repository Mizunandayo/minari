"""Tree-sitter parser factory.

IMPORTANT: tree-sitter-language-pack ships its OWN parser binding whose
get_parser() returns objects with a divergent method-based API (no .type/.text/
.children) and whose parse() wants str. We use the pack ONLY for grammars
(get_language) and drive parsing with the standard py-tree-sitter Parser, which
gives the documented property API (node.type, node.text, node.children,
node.has_error, child_by_field_name) and takes BYTES.

A fresh Parser is cheap; the Language is cached. New Parser per call keeps
concurrent diagnosis runs independent.
"""

from __future__ import annotations

from functools import lru_cache

from tree_sitter import Language, Parser
from tree_sitter_language_pack import get_language


@lru_cache(maxsize=8)
def _language(grammar: str) -> Language:
    return get_language(grammar)  # type: ignore[arg-type]  # pack name -> tree_sitter.Language


def parser_for(grammar: str) -> Parser:
    return Parser(_language(grammar))
