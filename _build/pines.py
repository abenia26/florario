"""Genera las imágenes para compartir de cada página, en español y en inglés.

Uso:  python _build/pines.py            (solo las que faltan o cuyo texto ha cambiado)
      python _build/pines.py --todas    (todas otra vez)
      python _build/pines.py --fondos   (solo los fondos de pantalla que falten)

Salida (se publica en la web):
  imagenes/og/<slug>.jpg              1200×630, vista previa de WhatsApp, X, Facebook… (todas las páginas)
  imagenes/pines/<slug>-pin.jpg       1000×1500, para «Guárdalo en Pinterest» (guías y meses)
  imagenes/pines/<slug>-story.jpg     1080×1920, para «Descargar para tu story» (guías y meses)
  descargas/fondo-calendario-de-flores-<año>.jpg   1080×1920, fondo de pantalla del calendario (año en curso y siguiente)
Las páginas en inglés van en imagenes/og/en/ e imagenes/pines/en/.

Necesita Chrome o Edge (captura) y Pillow (paso a JPEG). Se ejecuta a mano, no en GitHub Actions:
build.py avisa si a alguna página le falta su imagen. _build/pines.json guarda una huella de cada
imagen para no rehacer las que no cambian.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import build  # noqa: E402
from build import ROOT, BUILD, esc, bloom, strip_tags, find_browser, browser_cmd, color_hex  # noqa: E402

try:
    from PIL import Image
except ImportError:
    sys.exit("Necesito Pillow para pasar las capturas a JPEG: pip install pillow")

MANIFEST = os.path.join(BUILD, "pines.json")
SIZES = {"og": (1200, 630), "pin": (1000, 1500), "story": (1080, 1920), "fondo": (1080, 1920)}
QUALITY = {"og": 84, "pin": 82, "story": 80, "fondo": 86}
FONTS = "file:///" + os.path.join(ROOT, "fuentes").replace("\\", "/")


def photo_url(img):
    return "file:///" + os.path.join(ROOT, "imagenes", "web", build.IMAGES[img]["file"] + "-960.webp").replace("\\", "/")


CSS = f'''
@font-face {{ font-family: "Bricolage Grotesque"; font-weight: 400 800; src: url("{FONTS}/bricolage-grotesque-latin.woff2") format("woff2"); }}
@font-face {{ font-family: "DM Mono"; font-weight: 500; src: url("{FONTS}/dm-mono-500-latin.woff2") format("woff2"); }}
html, body {{ margin: 0; overflow: hidden; background: #F6F4EC; color: #1B2118; font-family: "Bricolage Grotesque", sans-serif; }}
.petal {{ stroke: rgba(27,33,24,.32); stroke-width: .7; }} .pistil {{ fill: #2A2F25; }}
.k {{ font-family: "DM Mono", monospace; letter-spacing: .06em; text-transform: uppercase; color: #525A4D; }}
h1 {{ margin: 0; font-weight: 800; letter-spacing: -.035em; line-height: 1; text-wrap: balance; }}
.brand {{ display: flex; align-items: center; gap: .45em; font-weight: 800; }}
.brand small {{ margin-left: auto; font-family: "DM Mono", monospace; font-weight: 500; color: #525A4D; }}
'''


def title_size(title, big, small, long_at=34, longer_at=56):
    n = len(title)
    return big if n <= long_at else (big + small) // 2 if n <= longer_at else small


def page_html(kind, d):
    """d = {"img", "color", "kicker", "title", "url"}."""
    w, h = SIZES[kind]
    photo, c, k, t, url = photo_url(d["img"]), d["color"], esc(d["kicker"]), esc(d["title"]), esc(d["url"])
    flower = bloom("#F2C230", 10)
    if kind == "og":
        body = f'''<div style="position:absolute;inset:0 0 0 640px;background:url('{photo}') center/cover;border-left:14px solid {c}"></div>
<div style="position:absolute;inset:0 560px 0 0;padding:56px 56px 52px 64px;box-sizing:border-box;display:flex;flex-direction:column">
  <div class="brand" style="font-size:34px">{flower.replace('<svg', '<svg style="width:46px;height:46px"')}Florario</div>
  <div style="margin-top:auto">
    <div class="k" style="font-size:24px">{k}</div>
    <h1 style="margin-top:16px;font-size:{title_size(d['title'], 66, 50)}px">{t}</h1>
  </div>
  <div class="k" style="margin-top:34px;font-size:22px;text-transform:none;letter-spacing:.02em">{url}</div>
</div>'''
    elif kind == "pin":
        body = f'''<div style="position:absolute;inset:0 0 520px 0;background:url('{photo}') center/cover"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:560px;padding:64px 72px;box-sizing:border-box;background:#F6F4EC;border-radius:48px 48px 0 0;border-top:14px solid {c}">
  <div class="k" style="font-size:32px">{k}</div>
  <h1 style="margin-top:18px;font-size:{title_size(d['title'], 88, 66)}px">{t}</h1>
  <div class="brand" style="position:absolute;left:72px;right:72px;bottom:56px;font-size:34px">{flower.replace('<svg', '<svg style="width:56px;height:56px"')}Florario<small style="font-size:26px">{url}</small></div>
</div>'''
    else:  # story: deja libres arriba y abajo las zonas que tapa la interfaz de Instagram o TikTok
        body = f'''<div style="position:absolute;inset:0 0 760px 0;background:url('{photo}') center/cover"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:820px;padding:72px 80px;box-sizing:border-box;background:#F6F4EC;border-radius:56px 56px 0 0;border-top:16px solid {c}">
  <div class="k" style="font-size:34px">{k}</div>
  <h1 style="margin-top:20px;font-size:{title_size(d['title'], 96, 72)}px">{t}</h1>
  <div class="brand" style="position:absolute;left:80px;right:80px;bottom:300px;font-size:38px">{flower.replace('<svg', '<svg style="width:60px;height:60px"')}Florario<small style="font-size:28px">{url}</small></div>
</div>'''
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}html,body{{width:{w}px;height:{h}px}}</style></head>'
            f'<body>{body}</body></html>')


def short_region(region):
    """Primer país o zona de la región: "España, Portugal…" → "España"; "EE. UU., Colombia…" → "EE. UU."."""
    return region.split(" · ")[0].split(", ")[0].split(" y ")[0].split(" and ")[0]


def wallpaper_html(y):
    """Fondo de pantalla 1080×1920 con las fechas del año y por mes. Deja libre la parte de arriba
    (reloj de la pantalla de bloqueo) y los extremos de abajo (linterna y cámara)."""
    T = build.T
    months = []
    for m in range(12):
        evs = [e for e in build.events_sorted(build.EVENTS, y) if build.date_for(e, y).month == m + 1]
        items = "".join(
            f'<li style="--dc:{color_hex(e["color"])}"><b>{build.date_for(e, y).day}</b>'
            f'<span>{esc(e["name"])}<small>{esc(short_region(e["region"]))}</small></span></li>' for e in evs) \
            or f'<li class="none"><span>{T("Flores para ti", "Flowers for you")}</span></li>'
        months.append(f'<section style="--mc:{build.MONTH_COLORS[m]}"><h2>{build.month_name(m).capitalize()}</h2><ul>{items}</ul></section>')
    w, h = SIZES["story"]
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
html,body{{width:{w}px;height:{h}px}}
body{{background:radial-gradient(700px 520px at 0% 8%, rgba(238,127,168,.30), transparent 70%),
  radial-gradient(640px 480px at 100% 4%, rgba(242,194,48,.30), transparent 70%),
  radial-gradient(700px 520px at 100% 96%, rgba(43,179,163,.18), transparent 70%), #F6F4EC}}
.top{{position:absolute;left:64px;right:64px;top:430px}}
.top h1{{font-size:76px}} .top h1 span{{color:#B98700}}
.grid{{position:absolute;left:48px;right:48px;top:570px;display:grid;grid-template-columns:1fr 1fr;align-content:start;gap:14px}}
section{{background:rgba(255,255,255,.82);border-radius:22px;border-top:8px solid var(--mc);padding:14px 18px;min-width:0}}
h2{{margin:0 0 6px;font-size:30px;font-weight:800;letter-spacing:-.02em}}
ul{{margin:0;padding:0;list-style:none;display:grid;gap:5px}}
li{{display:grid;grid-template-columns:44px 1fr;gap:10px;align-items:center;font-size:22px;line-height:1.2}}
li span{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
li b{{font-family:"DM Mono",monospace;font-weight:500;text-align:center;border-radius:8px;padding:2px 0;background:color-mix(in srgb,var(--dc) 35%,#fff)}}
li small{{margin-left:6px;font-size:16px;color:#525A4D}}
li.none{{display:block;color:#525A4D;font-style:italic}}
.foot{{position:absolute;left:0;right:0;bottom:70px;text-align:center;font-family:"DM Mono",monospace;font-size:24px;color:#525A4D}}
</style></head><body>
<div class="top"><div class="k" style="font-size:26px">Florario</div><h1>{T("Calendario de flores", "Flower calendar")} <span>{y}</span></h1></div>
<div class="grid">{"".join(months)}</div>
<div class="foot">calendariodeflores.com{"/en" if build.LANG == "en" else ""}</div>
</body></html>'''


def out_path(kind, prefix, slug):
    if kind == "og":
        return os.path.join(ROOT, "imagenes", "og", *([prefix.strip("/")] if prefix else []), f"{slug or 'portada'}.jpg")
    return os.path.join(ROOT, "imagenes", "pines", *([prefix.strip("/")] if prefix else []), f"{slug}-{kind}.jpg")


def jobs_for_lang(lang):
    """(tipo de imagen, ruta de salida, datos) de todas las páginas de un idioma."""
    build.set_lang(lang)
    T, prefix = build.T, build.PREFIX
    domain = "calendariodeflores.com" + ("/en" if lang == "en" else "")
    jobs = []

    def add(kinds, slug, img, color, kicker, title):
        d = {"img": img, "color": color, "kicker": kicker, "title": title,
             "url": domain + (f"/{slug}" if slug else "")}
        for kind in kinds:
            jobs.append((kind, out_path(kind, prefix, slug), d))

    add(["og"], "", "girasol", "#F2C230", T("Calendario de flores", "Flower calendar"),
        T("Todas las fechas para regalar flores", "Every date for giving flowers"))
    for slug, (small, name, desc, img, col) in build.HUB_CARDS.items():
        add(["og"], slug, img, color_hex(col), T("Calendario de flores", "Flower calendar"), name)
    # Fondos de pantalla del calendario, del año en curso y del siguiente
    for y in (build.YEAR, build.YEAR + 1):
        jobs.append(("fondo", os.path.join(ROOT, *build.wallpaper_href(y).lstrip("/").split("/")), {"html": wallpaper_html(y)}))
    for meta, _ in build.fragments(lang):
        kinds = ["og", "pin", "story"] if meta["tipo"] in ("guia", "mes") else ["og"]
        color = meta.get("color", "c-rosa")[2:]
        hex_ = color_hex(color if color in build.COLORS else "rosa")
        add(kinds, meta["slug"], meta.get("img") or "ramo-silvestre", hex_, strip_tags(meta["eyebrow"]),
            strip_tags(meta.get("pin_title") or meta["h1"]))
    return jobs


def render(browser, kind, out, html_text, tmp):
    w, h = SIZES[kind]
    key = hashlib.md5(out.encode()).hexdigest()
    src, png = os.path.join(tmp, key + ".html"), os.path.join(tmp, key + ".png")
    with open(src, "w", encoding="utf-8") as f:
        f.write(html_text)
    subprocess.run(browser_cmd(browser, "--hide-scrollbars", f"--window-size={w},{h}", "--force-device-scale-factor=1",
                               "--allow-file-access-from-files", "--virtual-time-budget=6000",
                               f"--screenshot={png}", "file:///" + src.replace("\\", "/")),
                   check=True, capture_output=True)
    im = Image.open(png).convert("RGB")
    if im.size != (w, h):
        im = im.crop((0, 0, w, h))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "JPEG", quality=QUALITY[kind], optimize=True, progressive=True)
    return os.path.getsize(out)


def main():
    browser = find_browser()
    if not browser:
        sys.exit("Necesito Chrome o Edge para generar las imágenes.")
    force = "--todas" in sys.argv
    # --fondos: solo los fondos de pantalla que falten (lo usa GitHub Actions en enero, con los PDF del año nuevo)
    only_missing_wallpapers = "--fondos" in sys.argv
    manifest = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}
    todo = []
    for lang in build.LANGS:
        for kind, out, d in jobs_for_lang(lang):
            if only_missing_wallpapers and (kind != "fondo" or os.path.exists(out)):
                continue
            html_text = d.get("html") or page_html(kind, d)
            rel = os.path.relpath(out, ROOT).replace(os.sep, "/")
            photo_time = str(os.path.getmtime(photo_url(d["img"])[8:])) if "img" in d else ""
            digest = hashlib.md5((html_text + photo_time).encode()).hexdigest()
            if force or manifest.get(rel) != digest or not os.path.exists(out):
                todo.append((kind, out, html_text, rel, digest))
            else:
                manifest[rel] = digest
    print(f"{len(todo)} imágenes por generar.")
    with tempfile.TemporaryDirectory() as tmp, cf.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(render, browser, kind, out, html_text, tmp): (rel, digest)
                   for kind, out, html_text, rel, digest in todo}
        for i, fut in enumerate(cf.as_completed(futures), 1):
            rel, digest = futures[fut]
            kb = fut.result() // 1024
            manifest[rel] = digest
            print(f"  {i}/{len(todo)} {rel} ({kb} KB)")
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(manifest.items())), f, indent=1, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
