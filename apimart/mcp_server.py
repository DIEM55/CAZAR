#!/usr/bin/env python3
"""Servidor MCP de APIMart: expone la herramienta `generate_image` (gpt-image-2-official).

La key se lee de la variable de entorno APIMART_API_KEY (nunca se escribe en archivos).
"""
import os, sys, time, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as g  # reutiliza call(), find_key(), find_images()
import urllib.request
from mcp.server.fastmcp import FastMCP, Image

mcp = FastMCP("apimart")
OUT = pathlib.Path(os.environ.get("APIMART_OUT", "output"))


def _key():
    key = os.environ.get("APIMART_API_KEY", "").strip().strip("\"'")
    if not key or not key.isascii() or " " in key:
        raise RuntimeError("APIMART_API_KEY falta o tiene caracteres no válidos.")
    return key


@mcp.tool()
def generate_image(prompt: str, size: str = "16:9", resolution: str = "1k",
                   quality: str = "high", n: int = 1, timeout_s: int = 600):
    """Genera una imagen con GPT Image 2 oficial (APIMart), la guarda en ./output y la devuelve.

    size: proporción (1:1, 16:9, 4:5, ...). resolution: 1k, 2k o 4k. quality: auto, low, medium, high.
    """
    key = _key()
    body = {"model": g.MODEL, "prompt": prompt, "size": size, "resolution": resolution, "n": n}
    if quality:
        body["quality"] = quality
    resp = g.call("POST", g.GEN_PATH, key, body)
    task_id = g.find_key(resp, {"task_id", "id"})
    if not task_id:
        raise RuntimeError(f"Respuesta inesperada de APIMart: {str(resp)[:300]}")
    deadline = time.time() + timeout_s
    time.sleep(10)
    imgs, st = [], {}
    while time.time() < deadline:
        st = g.call("GET", g.STATUS_PATH.format(task_id=task_id), key)
        imgs = g.find_images(st)
        status = (g.find_key(st, {"status", "state"}) or "").lower()
        if imgs:
            break
        if status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"La tarea falló: {str(st)[:400]}")
        time.sleep(10)
    if not imgs:
        raise RuntimeError(f"Tiempo agotado. task_id={task_id} (puedes consultarlo más tarde).")
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = int(time.time())
    first = None
    for i, (kind, val) in enumerate(imgs, 1):
        path = OUT / f"img_{stamp}_{i}.png"
        if kind == "b64":
            import base64
            path.write_bytes(base64.b64decode(val))
        else:
            urllib.request.urlretrieve(val, path)
        first = first or path
    return Image(path=str(first))


if __name__ == "__main__":
    mcp.run()
