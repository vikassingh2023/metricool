FROM python:3.12-slim-bookworm

# Install system dependencies (certs, DNS tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl dnsutils \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
