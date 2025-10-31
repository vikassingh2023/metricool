import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Metricool MCP API")

METRICOOL_USER_TOKEN = os.getenv("METRICOOL_USER_TOKEN")
METRICOOL_USER_ID = os.getenv("METRICOOL_USER_ID")

BASE_URL = "https://api.metricool.com/v2"  # current Metricool REST endpoint


@app.get("/")
async def root():
    return {"status": "ok", "message": "Metricool MCP Server running"}


def call_metricool(endpoint: str, params: dict = None):
    """Helper to call Metricool API with auth."""
    headers = {"Authorization": f"Bearer {METRICOOL_USER_TOKEN}"}
    params = params or {}
    params["user_id"] = METRICOOL_USER_ID

    try:
        r = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@app.get("/brands")
async def get_brands():
    """List all brands (accounts) in Metricool."""
    data = call_metricool("brands")
    return JSONResponse({"status": "success", "data": data})


@app.get("/posts")
async def get_posts(brand_id: str):
    """Fetch posts for a given brand."""
    data = call_metricool(f"brands/{brand_id}/posts")
    return JSONResponse({"status": "success", "data": data})


@app.get("/analytics")
async def get_analytics(brand_id: str):
    """Fetch analytics for a brand."""
    data = call_metricool(f"brands/{brand_id}/analytics")
    return JSONResponse({"status": "success", "data": data})


@app.post("/run")
async def run_generic(request: dict):
    """
    Generic endpoint to run custom Metricool API calls.
    Example JSON body:
      {"endpoint": "brands/123/posts", "params": {"limit": 5}}
    """
    endpoint = request.get("endpoint")
    params = request.get("params", {})
    data = call_metricool(endpoint, params)
    return JSONResponse({"status": "success", "data": data})
