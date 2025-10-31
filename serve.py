import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/run")
def run_metricool():
    try:
        result = subprocess.run(
            ["mcp-metricool"], capture_output=True, text=True, check=True
        )
        return JSONResponse({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return JSONResponse({"error": e.stderr}, status_code=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
