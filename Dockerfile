# ---- Stage 1: Build dependencies using uv ----
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

WORKDIR /app

# Enable bytecode compilation and copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy required files
COPY pyproject.toml uv.lock README.md ./

# Sync dependencies and update the lockfile
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Add the rest of the source code and install the project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# Explicitly install dependencies into /root/.local to make sure the folder exists
RUN mkdir -p /root/.local && \
    uv pip install --target /root/.local -r <(uv export requirements) || true


# ---- Stage 2: Runtime image ----
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy only what’s needed from the build stage
COPY --from=uv /app/.venv /app/.venv
# Remove the problematic COPY of /root/.local — not needed for runtime

# Add venv binaries to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Render expects the app to listen on port 8080
EXPOSE 8080

# Define environment variables (use Render’s dashboard to set actual secrets)
ENV METRICOOL_USER_TOKEN=""
ENV METRICOOL_USER_ID=""

# Start your MCP server
CMD ["mcp-metricool"]
