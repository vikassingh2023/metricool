import os
import socket
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# -------------------------------
# DNS fallback for Railway
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
METRICOOL_USER_TOKEN = os.getenv("METRICOOL_USER_TOKEN")  # This is the X-Mc-Auth key
BASE_URL = "https://app.metricool.com/api"


@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "message": "Metricool MCP
