"""768-d embeddings"""

from __future__ import annotations

from google import genai
from google.genai import types

from app.core.config import get_settings
from app.core.logging import get_logger

log = get_logger(__name__)
EMBED_DIM = 768






async def embed_text(text: str) -> list[float]:
    s = get_settings()
    if s.gemini_api_key is None:
        raise RuntimeError("MINARI_GEMINI_API_KEY is not set")
    client = genai.Client(api_key=s.gemini_api_key.get_secret_value())
    resp = await client.aio.models.embed_content(
        model=s.gemini_embed_model,
        contents=text[:20000],  
        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
    )
    return list(resp.embeddings[0].values)