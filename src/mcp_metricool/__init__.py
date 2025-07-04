import os

from .server import mcp
from .tools import tools

def main() -> None:
    "Run the Metricool MCP server"
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )
