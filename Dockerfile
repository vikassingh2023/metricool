# ---- Stage 1: Build dependencies using uv ----
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

WORKDIR /app

# Enable bytecode compilation and copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy required files
COPY pyproject.toml uv.lock README.md ./

# Sync dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Add the rest of the source code
COPY . .

# Final sync to install the project into its venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable


# ---- Stage 2: Runtime image ----
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy built virtual environment from build stage
COPY --from=uv /app/.venv /app/.venv
COPY --from=uv /app /app

# Add venv binaries to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Render expects the app to listen on port 8080
EXPOSE 8080

# Environment variables (set real ones in Render dashboard)
ENV METRICOOL_USER_TOKEN=""
ENV METRICOOL_USER_ID=""

# Start the MCP server
CMD ["mcp-metricool"]
