"""Git-ref-safe slugs repo path validation"""


from __future__ import annotations

import re

_UNSAFE = re.compile(r"[^a-zA-Z0-9._-]+")
_DASHES = re.compile(r"-{2,}")
_NODE_NAME = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_\-\[\]]*$")
_REPO_PATH = re.compile(r"^(?!.*\.\.)[\w./-]+\.(py|js|ts|tsx|go|java)$")



def safe_slug(text: str, *, max_len: int = 48) -> str:
    """Lowercase, git-ref-safe, collision-resistant slug."""
    slug = _UNSAFE.sub("-", text.strip().lower())
    slug = _DASHES.sub("-", slug).strip("-._")
    slug = slug[:max_len].strip("-._")
    return slug or "test"





def fix_branch_name(test_name: str, run_id: str) -> str:
    """e.g. minari/fix-test-checkout-flow-1a2b3c4d  (never a protected branch)."""
    return f"minari/fix-{safe_slug(test_name)}-{run_id[:8]}"


def is_safe_repo_path(path: str) -> bool:
    return bool(_REPO_PATH.match(path)) and not path.startswith("/")


def is_safe_node_name(test_name: str) -> bool:
    return bool(_NODE_NAME.match(test_name))