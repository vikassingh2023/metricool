import os
import socket
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# -------------------------------
# DNS fallback (for Railway)
# -------------------------------
dns_servers = ["1.1.1.1", "8.8.8.8"]

def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        # Try normal resolution first
        return original_getaddrinfo(host, port, family, type, proto, flags)
    except socket.gaierror:
        # Fallback DNS resolution
        for dns in dns_servers:
            try:
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (dns, port))]
            except Exception:
                continue
        raise

# Patch resolver
original_getaddrinfo = socket.getaddrinfo
socket.getaddrinfo = custom_getaddrinfo

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(title="Metricool MCP Server")

# Load environment variables
METRICOOL_USER_ID = os.getenv("METRICOOL_USER_ID")
METRICOOL_USER_TOKEN = os.getenv("METRICOOL_USER_TOKEN")

BASE_URL = "https://api.metricool.com/v2"


@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "message": "Metricool MCP Server running"}


@app.get("/brands")
async def get_brands():
    """Fetch all Metricool brands"""
    try:
        url = f"{BASE_URL}/brands?user_id={METRICOOL_USER_ID}"
        headers = {"Authorization": f"Bearer {METRICOOL_USER_TOKEN}"}

        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        return {"status": "success", "data": response.json()}
    except Exception as e:
        return {"status": "success", "data": {"error": str(e)}}


@app.post("/run")
async def run_tool(request: Request):
    """
    Mimics an MCP /run endpoint to trigger Metricool tasks
    Expected JSON body:
    {
        "action": "brands"
    }
    """
    try:
        body = await request.json()
        action = body.get("action")

        if action == "brands":
            url = f"{BASE_URL}/brands?user_id={METRICOOL_USER_ID}"
            headers = {"Authorization": f"Bearer {METRICOOL_USER_TOKEN}"}
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}

        return {"status": "success", "data": {"message": "Unknown action"}}

    except Exception as e:
        return {"status": "success", "data": {"error": str(e)}}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler"""
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": str(exc)},
    )
