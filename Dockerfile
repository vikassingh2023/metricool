FROM python:3.12-slim-bookworm

# Install system dependencies (for HTTPS + DNS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl dnsutils \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy everything
COPY . .

# Install project (from pyproject.toml)
RUN pip install --no-cache-dir .

# Expose app port
EXPOSE 8080

# Start FastAPI server
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
