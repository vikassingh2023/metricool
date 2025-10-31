import os
import json
import subprocess
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# Environment variables from Railway
API_KEY = os.environ.get("MCP_API_KEY", "dev-secret")
METRICOOL_USER_TOKEN = os.environ.get("METRICOOL_USER_TOKEN")
METRICOOL_USER_ID = os.environ.get("METRICOOL_USER_ID")

@app.get("/")
def health():
    return {"status": "ok", "message": "Metricool MCP Server running"}

@app.post("/run")
async def run_metricool(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    cmd = data.get("command", "get_brands")
    args = data.get("args", [])

    # Add Metricool credentials to the subprocess environment
    env = os.environ.copy()
    env["METRICOOL_USER_TOKEN"] = METRICOOL_USER_TOKEN or ""
    env["METRICOOL_USER_ID"] = METRICOOL_USER_ID or ""

    # --- Debug logging ---
    print(f"[DEBUG] Running command: mcp-metricool {cmd} {args}")
    print(f"[DEBUG] METRICOOL_USER_ID: {METRICOOL_USER_ID}")
    print(f"[DEBUG] METRICOOL_USER_TOKEN (first 8 chars): {METRICOOL_USER_TOKEN[:8]}...")

    process = subprocess.run(
        ["mcp-metricool", cmd, *args],
        capture_output=True,
        text=True,
        env=env
    )

    print(f"[DEBUG] Exit code: {process.returncode}")
    print(f"[DEBUG] Stdout: {process.stdout.strip()}")
    print(f"[DEBUG] Stderr: {process.stderr.strip()}")

    # Return both stdout/stderr to API for clarity
    return JSONResponse({
        "status": "success" if process.returncode == 0 else "error",
        "stdout": process.stdout.strip(),
        "stderr": process.stderr.strip(),
        "exit_code": process.returncode
    })



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
