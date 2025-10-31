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

    # Debug log
    print(f"Running mcp-metricool {cmd} {args}")
    print(f"METRICOOL_USER_ID={METRICOOL_USER_ID}")
    print(f"METRICOOL_USER_TOKEN={METRICOOL_USER_TOKEN[:5]}***")  # hide sensitive parts


    # Add Metricool environment variables for the subprocess
    env = os.environ.copy()
    env["METRICOOL_USER_TOKEN"] = METRICOOL_USER_TOKEN or ""
    env["METRICOOL_USER_ID"] = METRICOOL_USER_ID or ""

    try:
        process = subprocess.run(
            ["mcp-metricool", cmd, *args],
            capture_output=True,
            text=True,
            env=env,
            check=True
        )

        # Parse the CLI output
        try:
            output = json.loads(process.stdout)
        except json.JSONDecodeError:
            output = {"raw_output": process.stdout.strip()}

        return JSONResponse({"status": "success", "data": output})

    except subprocess.CalledProcessError as e:
        return JSONResponse(
            {"status": "error", "stderr": e.stderr or str(e)},
            status_code=500
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
