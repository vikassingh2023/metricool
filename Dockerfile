# ---- Stage 1: Build dependencies using uv ----
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

WORKDIR /app

# Enable bytecode compilation and copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy project files needed for dependency installation
COPY pyproject.toml uv.lock README.md ./

# Install dependencies (no cache mounts)
RUN uv sync --frozen --no-install-project --no-dev --no-editable

# Copy all source code
COPY . .

# Install the project into its venv
RUN uv sync --frozen --no-dev --no-editable


# ---- Stage 2: Runtime ----
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy from the build stage
COPY --from=uv /app/.venv /app/.venv
COPY --from=uv /app /app

# Add venv binaries to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose Railway default port
EXPOSE 8080

# Environment variables (you’ll set actual secrets in Railway)
ENV METRICOOL_USER_TOKEN=""
ENV METRICOOL_USER_ID=""

# Start the MCP server
CMD ["mcp-metricool", "--host", "0.0.0.0", "--port", "8080"]
