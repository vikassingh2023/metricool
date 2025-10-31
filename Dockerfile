FROM python:3.12-slim-bookworm

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock README.md ./
RUN pip install --upgrade pip setuptools wheel fastapi uvicorn mcp-metricool

# Copy app code
COPY . .

# Railway will set PORT automatically
ENV PORT=8080

EXPOSE 8080

# Start the HTTP wrapper
CMD ["python", "serve.py"]
