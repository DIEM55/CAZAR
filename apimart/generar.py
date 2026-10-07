#!/usr/bin/env python3
"""Genera una imagen con GPT Image 2 vía APIMart (flujo asíncrono).

Uso:
    export APIMART_API_KEY="tu-key"
    python3 generar.py "un gato astronauta" [--size 1:1] [--resolution 1k] [--quality auto] [--n 1]

Flujo: crea la tarea -> espera 20 s -> consulta el estado -> descarga la imagen.
Los endpoints y el modelo se pueden cambiar con variables de entorno si la
documentación de APIMart difiere de los valores por defecto.
"""
import argparse, base64, json, os, sys, time, urllib.request, urllib.error

BASE = os.environ.get("APIMART_BASE_URL", "https://api.apimart.ai")
GEN_PATH = os.environ.get("APIMART_GEN_PATH", "/v1/images/generations")      # confirmado en la doc
STATUS_PATH = os.environ.get("APIMART_STATUS_PATH", "/v1/tasks/{task_id}")  # confirmado en la doc
MODEL = os.environ.get("APIMART_MODEL", "gpt-image-2-official")             # variante oficial (la otra es gpt-image-2-ext)
WAIT_FIRST = int(os.environ.get("APIMART_WAIT", "20"))
POLL_EVERY = 10
POLL_MAX = 60


def call(method, path, key, body=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Error HTTP {e.code} en {path}: {e.read().decode(errors='replace')[:500]}")


def find_key(obj, names):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in names and isinstance(v, (str, int)):
                return str(v)
        for v in obj.values():
            r = find_key(v, names)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_key(v, names)
            if r:
                return r
    return None


def find_images(obj, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "b64_json" and isinstance(v, str):
                out.append(("b64", v))
            else:
                find_images(v, out)
    elif isinstance(obj, list):
        for v in obj:
            find_images(v, out)
    elif isinstance(obj, str) and obj.startswith("http"):
        if any(x in obj.lower().split("?")[0] for x in (".png", ".jpg", ".jpeg", ".webp")):
            out.append(("url", obj))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--size", default="1:1", help="proporción: 1:1, 16:9, ...")
    ap.add_argument("--resolution", default="1k", help="1k, 2k o 4k")
    ap.add_argument("--quality", default="high", help="auto, low, medium, high")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--out", default="output")
    a = ap.parse_args()

    key = os.environ.get("APIMART_API_KEY")
    if not key:
        sys.exit("Falta la variable de entorno APIMART_API_KEY.")
    key = key.strip().strip("\"'")
    if not key.isascii() or " " in key:
        sys.exit("APIMART_API_KEY tiene caracteres no válidos (acentos, espacios o texto de ejemplo). "
                 "Vuelve a copiar la key desde APIMart y pégala sin comillas ni espacios.")

    body = {"model": MODEL, "prompt": a.prompt, "size": a.size, "resolution": a.resolution, "n": a.n}
    if a.quality:
        body["quality"] = a.quality
    resp = call("POST", GEN_PATH, key, body)
    print("Respuesta de creación:", json.dumps(resp)[:500])
    task_id = find_key(resp, {"task_id", "id"})
    imgs = find_images(resp)

    if not imgs:
        if not task_id:
            sys.exit("No encontré task_id ni imagen en la respuesta. Revisa la documentación.")
        print(f"Tarea {task_id}. Esperando {WAIT_FIRST} s antes de consultar...")
        time.sleep(WAIT_FIRST)
        for i in range(POLL_MAX):
            st = call("GET", STATUS_PATH.format(task_id=task_id), key)
            imgs = find_images(st)
            status = find_key(st, {"status", "state"})
            print(f"Consulta {i + 1}: estado={status}")
            if imgs:
                break
            if status and status.lower() in ("failed", "error", "cancelled"):
                sys.exit(f"La tarea falló: {json.dumps(st)[:500]}")
            time.sleep(POLL_EVERY)

    if not imgs:
        sys.exit("No se obtuvo ninguna imagen. Vuelve a consultar más tarde.")

    os.makedirs(a.out, exist_ok=True)
    stamp = int(time.time())
    for i, (kind, val) in enumerate(imgs, 1):
        path = os.path.join(a.out, f"img_{stamp}_{i}.png")
        if kind == "b64":
            open(path, "wb").write(base64.b64decode(val))
        else:
            urllib.request.urlretrieve(val, path)
        print("Guardada:", path)


if __name__ == "__main__":
    main()
