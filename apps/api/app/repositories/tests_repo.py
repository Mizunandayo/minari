"""Test registry persistence"""




from __future__ import annotations

from pgvector.asyncpg import register_vector

from app.db.session import get_pool


async def upsert_test(
    *, project_id: str, file_path: str, test_name: str,
    language: str | None, framework: str | None, embedding: list[float] | None,
) -> str | None:
    pool = get_pool()
    if pool is None:
        return None
    async with pool.acquire() as conn:
        await register_vector(conn)
        row = await conn.fetchrow(
            """
            insert into tests (project_id, file_path, test_name, language, framework, embedding)
            values ($1, $2, $3, $4, $5, $6)
            on conflict (project_id, file_path, test_name)
            do update set language = excluded.language,
                          framework = excluded.framework,
                          embedding = coalesce(excluded.embedding, tests.embedding),
                          updated_at = now()
            returning id
            """,
            project_id, file_path, test_name, language, framework, embedding,
        )
        return str(row["id"]) if row else None


async def list_tests(project_id: str, limit: int = 100) -> list[dict]:
    """Tests in a project with their most-recent diagnosis (for the dashboard)."""
    pool = get_pool()
    if pool is None:
        return []
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            select t.id::text as id, t.test_name, t.file_path, t.language,
                   d.pfs_score, d.category, d.confidence
            from tests t
            left join lateral (
                select pfs_score, category, confidence
                from diagnoses
                where test_id = t.id
                order by created_at desc
                limit 1
            ) d on true
            where t.project_id = $1
            order by t.updated_at desc
            limit $2
            """,
            project_id, limit,
        )
    return [
        {
            "id": r["id"],
            "test_name": r["test_name"],
            "file_path": r["file_path"],
            "language": r["language"],
            "pfs_score": float(r["pfs_score"]) if r["pfs_score"] is not None else None,
            "category": r["category"],
            "confidence": float(r["confidence"]) if r["confidence"] is not None else None,
        }
        for r in rows
    ]