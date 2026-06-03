import os

os.environ.setdefault("MINARI_DEMO_API_KEY", "test-key-0123456789abcdef0123456789")
os.environ.setdefault("MINARI_DATABASE_URL", "postgresql://u:p@localhost:5432/db")
os.environ.setdefault("MINARI_REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("MINARI_GITLAB_MCP_URL", "https://example.invalid/mcp")
os.environ.setdefault("MINARI_GITLAB_TOKEN", "glpat-test")
os.environ.setdefault("MINARI_DEMO_PROJECT_ID", "demo/minari")


