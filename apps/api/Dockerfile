# build stage install deps with uv

FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY app ./app




# Runtime stage: Python 3.12 + Node 20 (for the GitLab MCP server), non-root
FROM python:3.12-slim AS runtime

# Install Node 20 (NodeSource) and pre-install the GitLab MCP server globally so
# the agent spawns it instantly via stdio — no runtime npx download (which would
# fail for the non-root user with no writable cache).
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g @zereight/mcp-gitlab \
    # Symlink the installed bin to a stable name so the app spawns it directly
    # (no npx -> no registry download, no per-user npm cache write).
    && ln -sf "$(command -v mcp-gitlab || command -v better-gitlab-mcp-server || command -v gitlab-mcp)" /usr/local/bin/minari-mcp \
    && apt-get purge -y curl gnupg \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Non-root user WITH a writable home (Node/npm need one even when invoked directly)
RUN groupadd --system minari \
    && useradd --system --gid minari --create-home --home-dir /home/minari minari
WORKDIR /app
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH" \
    HOME=/home/minari \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_ENV=production
USER minari
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]