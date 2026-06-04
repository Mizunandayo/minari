"""pgvector KNN over tests.embedding column"""



from __future__ import annotations
from pgvector.asyncpg import register_vector
from app.core.logging import get_logger
from app.db.session import get_pool





log = get_logger(__name__)









async def find_similar_diagnoses(project_id: str, embedding: list[float], k: int = 5) -> list[str]:
    """Return short human-readable summaries"""
    pool = get_pool()
    if pool is None:
        return []
    try:
        async with pool.acquire() as conn:
            await register_vector(conn)
            rows = await conn.fetch(
                """
                select t.test_name, d.category, d.confidence
                from tests t
                join diagnoses d on d.test_id = t.id
                where t.project_id = $1 and t.embedding is not null
                order by t.embedding <=> $2
                limit $3
                """,
                project_id, embedding, k,
            )
        return [
            f"`{r['test_name']}` → {r['category']} (confidence {float(r['confidence']):.2f})"
            for r in rows
        ]
    except Exception as exc:  
        log.warning("similarity.failed", error=str(exc))
        return []