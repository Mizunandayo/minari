"""Adaptive model router"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.config import get_settings


@dataclass(frozen=True)
class Route:
    provider: str
    model: str
    reason: str







def choose_model(pfs_score: float, *, cost_budget_used: float = 0.0) -> Route:
    s = get_settings()
    if cost_budget_used >= 0.95:
        return Route("gemini", s.gemini_flash_model,
                     f"cost budget {cost_budget_used:.0%} → forced Flash")
    if pfs_score < 40:
        return Route("gemini", s.gemini_flash_model,
                     f"PFS {pfs_score:.0f} (simple) → Gemini Flash")
    if pfs_score <= 75:
        return Route("gemini", s.gemini_pro_model,
                     f"PFS {pfs_score:.0f} (medium) → Gemini Pro")
    if s.deepseek_api_key is not None:
        return Route("deepseek", s.deepseek_model,
                     f"PFS {pfs_score:.0f} (complex) → DeepSeek-R1 (deep CoT)")
    return Route("gemini", s.gemini_pro_model,
                 f"PFS {pfs_score:.0f} complex but no DeepSeek key → Gemini Pro")