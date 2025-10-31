import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Metricool MCP Server running"}

@app.post("/run")
def run_metricool():
    """Run MCP Metricool CLI and return output"""
    try:
        result = subprocess.run(
            ["mcp-metricool"],
            capture_output=True,
            text=True,
            check=True
        )
        return JSONResponse({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return JSONResponse(
            {"error": e.stderr or "Command failed"},
            status_code=500
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
