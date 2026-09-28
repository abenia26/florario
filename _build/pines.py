"""Genera imágenes verticales 1000×1500 para Pinterest (y portadas de TikTok) de las páginas principales.

Uso:  python _build/pines.py
Salida: marketing/pines/<slug>.png  (no se publica en la web: está en .vercelignore)
Necesita Chrome o Edge instalado. Los textos de cada pin están en marketing/PINTEREST-TIKTOK.md.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build import ROOT, IMAGES, find_browser, esc, bloom  # noqa: E402

PINS = [
    ("calendario-de-flores", "girasol", "#F2C230", "Calendario de flores", "Qué flor regalar en cada fecha del año"),
    ("flores-amarillas", "girasol", "#F2C230", "21 de septiembre", "Por qué se regalan flores amarillas"),
    ("flores-amarillas-21-de-marzo", "girasol", "#F2C230", "21 de marzo", "Flores amarillas de primavera en México"),
    ("flores-azules", "hortensia-azul", "#3F72E0", "3 de octubre", "Flores azules para el Día del Novio"),
    ("flores-moradas", "violeta", "#8A4FD8", "9 de noviembre", "Flores moradas para tu persona morada"),
    ("san-valentin", "ramo-rosas", "#D7263D", "14 de febrero", "Flores para San Valentín"),
    ("dia-de-la-madre", "peonia", "#EE7FA8", "Día de la Madre", "Qué flores regalar y cuándo es en tu país"),
    ("dia-del-padre", "girasol", "#3F72E0", "Día del Padre", "Flores para papá (sí, ellos también)"),
    ("dia-de-la-mujer", "mimosa", "#F2C230", "8 de marzo", "Mimosa y tulipanes: las flores del 8M"),
    ("sant-jordi", "rosa-roja", "#D7263D", "23 de abril", "Sant Jordi: una rosa y un libro"),
    ("todos-los-santos-dia-de-muertos", "cempasuchil", "#F28C1B", "1 y 2 de noviembre", "Crisantemo y cempasúchil"),
    ("nochebuena", "nochebuena", "#D7263D", "8 de diciembre", "La flor mexicana de la Navidad"),
    ("significado-colores-flores", "ramo-tulipanes", "#EE7FA8", "Todo el año", "Qué significa cada color de flor"),
    ("flores-para-cumpleanos", "ramo-tulipanes", "#EE7FA8", "Cumpleaños", "Qué ramo regalar según la persona"),
    ("flores-para-aniversario", "ramo-rosas", "#D7263D", "Aniversarios", "Una flor para cada año juntos"),
    ("meses", "ramo-silvestre", "#2BB3A3", "Mes a mes", "Flores de temporada en España y Latinoamérica"),
]


def pin_html(img, color, kicker, title):
    src = "file:///" + os.path.join(ROOT, "imagenes", "web", IMAGES[img]["file"] + "-960.webp").replace("\\", "/")
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=DM+Mono:wght@500&display=swap">
<style>
html,body{{margin:0;width:1000px;height:1500px;overflow:hidden;background:#F6F4EC;font-family:"Bricolage Grotesque",sans-serif;color:#1B2118}}
.photo{{position:absolute;inset:0 0 520px 0;background:url("{src}") center/cover}}
.card{{position:absolute;left:0;right:0;bottom:0;height:560px;padding:64px 72px;box-sizing:border-box;background:#F6F4EC;border-radius:48px 48px 0 0;border-top:14px solid {color}}}
.k{{font-family:"DM Mono",monospace;font-size:34px;letter-spacing:.06em;text-transform:uppercase;color:#5F685A}}
h1{{margin:18px 0 0;font-size:92px;line-height:1;font-weight:800;letter-spacing:-.035em}}
.brand{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;align-items:center;gap:16px;font-size:34px;font-weight:800}}
.brand small{{margin-left:auto;font-family:"DM Mono",monospace;font-weight:500;font-size:28px;color:#5F685A}}
.brand svg{{width:56px;height:56px}} .petal{{stroke:rgba(27,33,24,.32);stroke-width:.7}} .pistil{{fill:#2A2F25}}
</style></head><body><div class="photo"></div>
<div class="card"><div class="k">{esc(kicker)}</div><h1>{esc(title)}</h1>
<div class="brand">{bloom("#F2C230", 10)}Florario<small>calendariodeflores.com</small></div></div></body></html>'''


def main():
    browser = find_browser()
    if not browser:
        sys.exit("Necesito Chrome o Edge para generar los pines.")
    out_dir = os.path.join(ROOT, "marketing", "pines")
    tmp = os.path.join(ROOT, "_build", "salida", "pines")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    for slug, img, color, kicker, title in PINS:
        src = os.path.join(tmp, slug + ".html")
        with open(src, "w", encoding="utf-8") as f:
            f.write(pin_html(img, color, kicker, title))
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1000,1500",
                        "--virtual-time-budget=5000", "--allow-file-access-from-files",
                        f"--screenshot={os.path.join(out_dir, slug + '.png')}", "file:///" + src.replace("\\", "/")],
                       check=True, capture_output=True)
        print("pin:", slug)


if __name__ == "__main__":
    main()
