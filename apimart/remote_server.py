#!/usr/bin/env python3
"""Versión en línea del conector APIMart (MCP sobre HTTP) para agregarlo en Claude > Conectores.

Variables de entorno:
  APIMART_API_KEY  tu key de APIMart
  MCP_SECRET       texto largo y secreto; forma parte de la URL y hace de contraseña
  PORT             lo pone el servicio de hosting (por defecto 8000)
La URL del conector queda: https://<tu-servicio>/<MCP_SECRET>/mcp
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uvicorn
from mcp_server import mcp

SECRET = os.environ.get("MCP_SECRET", "").strip()
if len(SECRET) < 20:
    sys.exit("Define MCP_SECRET con al menos 20 caracteres (letras y números, sin espacios).")

mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
mcp.settings.stateless_http = True
inner = mcp.streamable_http_app()
PREFIX = f"/{SECRET}"


async def app(scope, receive, send):
    if scope["type"] == "http":
        path = scope["path"]
        if path == PREFIX or path.startswith(PREFIX + "/"):
            scope = dict(scope, path=path[len(PREFIX):] or "/",
                         raw_path=scope.get("raw_path", b"")[len(PREFIX):] or b"/")
        else:
            await send({"type": "http.response.start", "status": 404, "headers": []})
            await send({"type": "http.response.body", "body": b"Not found"})
            return
    await inner(scope, receive, send)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=mcp.settings.port)
