import os
import socket
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# -------------------------------
# DNS fallback (Railway safe)
# -------------------------------
dns_servers = ["1.1.1.1", "8.8.8.8"]

def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return original_getaddrinfo(host, port, family, type, proto, flags)
    except socket.gaierror:
        for dns in dns_servers:
            try:
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (dns, port))]
            except Exception:
                continue
        raise

original_getaddrinfo = socket.getaddrinfo
socket.getaddrinfo = custom_getaddrinfo

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(title="Metricool MCP Server")

METRICOOL_USER_ID = os.getenv("METRICOOL_USER_ID")
METRICOOL_USER_TOKEN = os.getenv("METRICOOL_USER_TOKEN")  # X-Mc-Auth key
BASE_URL = "https://app.metricool.com/api"


def safe_json(response):
    """Return JSON if possible, else text"""
    try:
        return response.json()
    except Exception:
        return {"non_json_response": response.text[:500]}  # capture first 500 chars


@app.get("/")
async def root():
    return {"status": "ok", "message": "Metricool MCP Server running"}


@app.get("/brands")
async def get_brands():
    """Fetch brands using Metricool X-Mc-Auth header"""
    try:
        url = f"{BASE_URL}/brands?user_id={METRICOOL_USER_ID}"
        headers = {"X-Mc-Auth": METRICOOL_USER_TOKEN}
        response = requests.get(url, headers=headers, timeout=20)

        data = safe_json(response)
        return {
            "status": "success" if response.ok else "error",
            "http_status": response.status_code,
            "data": data,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/run")
async def run_tool(request: Request):
    """Run Metricool actions"""
    try:
        body = await request.json()
        action = body.get("action")
        headers = {"X-Mc-Auth": METRICOOL_USER_TOKEN}

        if action == "brands":
            url = f"{BASE_URL}/brands?user_id={METRICOOL_USER_ID}"
        elif action == "max_profiles":
            url = f"{BASE_URL}/admin/max-profiles"
        else:
            return {"status": "error", "message": f"Unknown action '{action}'"}

        response = requests.get(url, headers=headers, timeout=20)
        data = safe_json(response)
        return {
            "status": "success" if response.ok else "error",
            "http_status": response.status_code,
            "data": data,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"status": "error", "detail": str(exc)})
