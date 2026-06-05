"""Deterministic unified-diff"""



from __future__ import annotations

import difflib


def unified_diff(original: str, fixed: str, file_path: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        fixed.splitlines(keepends=True),
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
        n=3,
    )
    return "".join(diff)




def imports_present(grammar: str, fixed: str) -> bool:
    needles = {
        "python": [("uuid.", "import uuid"), ("threading.", "import threading"),
                   ("asyncio.", "import asyncio"), ("time.", "import time")],
    }
    for token, imp in needles.get(grammar, []):
        if token in fixed and imp not in fixed:
            return False
    return True