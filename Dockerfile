FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Environment variables
ENV PYTHONPATH=/app

# Run the server
CMD ["python", "src/mcp_metricool/server.py"] 