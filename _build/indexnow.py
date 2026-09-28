"""Avisa a Bing, Yandex y el resto de buscadores de IndexNow de las páginas nuevas o cambiadas.

Uso:  python _build/indexnow.py                 (todas las URL de sitemap.xml)
      python _build/indexnow.py --commit HEAD   (solo las páginas que cambió ese commit)
      python _build/indexnow.py URL [URL…]      (las URL indicadas)

La clave es pública: está en la raíz de la web (<clave>.txt) para que los buscadores comprueben
que el aviso viene del dueño del dominio. Google no usa IndexNow: para Google está Search Console.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from datos import SITE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = "7e8fe03e1617c657b1014097a1ffc5ae"
URL = SITE["url"]


def sitemap_urls():
    return re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())


def commit_urls(ref):
    """URL públicas de las páginas (index.html) que cambian en ese commit."""
    out = subprocess.run(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", ref], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.split()
    urls = []
    for path in out:
        if path == "index.html":
            urls.append(f"{URL}/")
        elif path.endswith("/index.html") and not path.startswith(("_build/", "widget/")):
            urls.append(f"{URL}/{path[:-len('index.html')]}")
    return urls


def submit(urls):
    if not urls:
        print("IndexNow: no hay páginas que avisar.")
        return
    body = json.dumps({"host": URL.split("://")[1], "key": KEY, "keyLocation": f"{URL}/{KEY}.txt",
                       "urlList": urls[:10000]}).encode("utf-8")
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: {len(urls)} URL enviadas (HTTP {r.status}).")
    except urllib.error.HTTPError as e:
        # 200 y 202 = aceptado; 403 = la clave aún no está publicada; 422 = URL de otro dominio
        print(f"IndexNow: error HTTP {e.code} ({e.reason}).")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--commit"]:
        submit(commit_urls(args[1] if len(args) > 1 else "HEAD"))
    elif args:
        submit(args)
    else:
        submit(sitemap_urls())
