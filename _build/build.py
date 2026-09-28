"""Generador estático de Florario.

Uso:  python _build/build.py          (genera páginas, portada, sitemap, .ics y HTML de los PDF)
      python _build/build.py --pdf    (además imprime los PDF con Chrome o Edge sin interfaz)

Lee los datos de _build/datos.py, los textos de _build/paginas/*.html y la plantilla de la
portada _build/plantilla-inicio.html. Todo lo que genera va a la raíz del proyecto, que es
lo que publica Vercel. No necesita dependencias fuera de la biblioteca estándar.
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from datos import (SITE, COLORS, TYPES, MONTHS, MONTH_SHORT, MONTH_COLORS, WEEKDAYS, IMAGES,
                   COUNTRIES, EVENTS, SEASON, SEASON_REGIONS, SEASON_NOTE, FLOWERS, GUIDES)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.dirname(os.path.abspath(__file__))
URL = SITE["url"]
# Fecha del build: de ella salen la tabla rodante, el año del title y los PDF.
# Para probar otra fecha: FLORARIO_HOY=2026-12-15 python _build/build.py
HOY = dt.date.fromisoformat(os.environ["FLORARIO_HOY"]) if os.environ.get("FLORARIO_HOY") else dt.date.today()
YEAR = HOY.year
# Desde octubre la búsqueda mira ya al año siguiente: title y H1 pasan a "2026-2027".
YEAR_LABEL = f"{YEAR}-{YEAR + 1}" if HOY >= dt.date(YEAR, 10, 1) else str(YEAR)
# Año del calendario para imprimir: desde septiembre se ofrece el del año siguiente.
PRINT_YEAR = YEAR + 1 if HOY.month >= 9 else YEAR
PUBLISHED = dt.date.fromisoformat(SITE["published"])
# Última revisión de todo el sitio (la más reciente de las páginas); se calcula en main().
UPDATED = PUBLISHED
EV = {e["id"]: e for e in EVENTS}
GUIDE = {g["slug"]: g for g in GUIDES}
FLOWER = {f["slug"]: f for f in FLOWERS}
COUNTRY_BY_SLUG = {c["slug"]: (code, c) for code, c in COUNTRIES.items()}
LOCALE = {c["slug"]: c["hreflang"].replace("-", "_") for c in COUNTRIES.values()}
HUB_CARDS = {
    "meses": ("Calendario", "Flores por mes", "Qué regalar y qué hay de temporada cada mes", "ramo-tulipanes", "rosa"),
    "flores": ("Calendario", "Flores de la A a la Z", "Significado y temporada de cada flor", "ramo-silvestre", "amarillo"),
    "guias": ("Calendario", "Todas las guías", "Fechas y ocasiones para regalar flores", "ramo-rosas", "rojo"),
    "paises": ("Calendario", "Fechas por país", "España, México, Argentina, Colombia, Chile y Perú", "ramo-silvestre", "rosa"),
}
WARN = []


# ---------------------------------------------------------------- utilidades
def esc(s):
    return html.escape(str(s), quote=True)


def strip_tags(s):
    s = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
    return re.sub(r"\s+([:;,.!?])", r"\1", s)


def pending(v):
    """True si el dato de SITE sigue siendo un marcador entre corchetes."""
    if isinstance(v, dict):
        return any(pending(x) for x in v.values())
    if isinstance(v, list):
        return not v or any(pending(x) for x in v)
    return isinstance(v, str) and v.startswith("[")


def words(s):
    return len(re.findall(r"\w+", strip_tags(s)))


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def nth_weekday(y, m, wd, n):
    """n-ésimo día de la semana wd (0 = domingo, como en JS) del mes m."""
    first = dt.date(y, m, 1)
    js_day = (first.weekday() + 1) % 7
    return dt.date(y, m, 1 + (wd - js_day) % 7 + (n - 1) * 7)


def date_for(ev, y):
    if "rule" in ev:
        r = ev["rule"]
        return nth_weekday(y, r["m"], r["wd"], r["n"])
    return dt.date(y, ev["m"], ev["d"])


def month_of(ev):
    return ev["rule"]["m"] if "rule" in ev else ev["m"]


def next_date(ev, ref=HOY):
    d = date_for(ev, ref.year)
    return d if d >= ref else date_for(ev, ref.year + 1)


def when_code(ev):
    if "rule" in ev:
        r = ev["rule"]
        return f'{r["m"]}-w{r["wd"]}-{r["n"]}'
    return f'{ev["m"]}-{ev["d"]}'


def when_text(ev):
    return ev["ruleText"] if "rule" in ev else f'{ev["d"]} de {MONTHS[ev["m"] - 1]}'


def fmt(d, year=True, weekday=False):
    s = f"{d.day} de {MONTHS[d.month - 1]}"
    if year:
        s += f" de {d.year}"
    if weekday:
        s = f"{WEEKDAYS[d.weekday()]} {s}"
    return s


def time_tag(d, text=None, **kw):
    return f'<time datetime="{d.isoformat()}">{esc(text or fmt(d, **kw))}</time>'


def events_sorted(evs, y=YEAR):
    return sorted(evs, key=lambda e: date_for(e, y))


def full_title(t):
    """Añade la marca solo si el title sigue cabiendo en ~65 caracteres."""
    return f"{t} | Florario" if len(t) + 11 <= 65 else t


def page_url(slug):
    return f"{URL}/{slug}/" if slug else f"{URL}/"


def title_of(slug):
    if slug in GUIDE:
        return GUIDE[slug]["name"]
    if slug in FLOWER:
        return FLOWER[slug]["name"]
    if slug in COUNTRY_BY_SLUG:
        return COUNTRY_BY_SLUG[slug][1]["name"]
    return slug


# ---------------------------------------------------------------- imágenes
def img_path(key, size, ext="webp"):
    return f'/imagenes/web/{IMAGES[key]["file"]}-{size}.{ext}'


def jpg_url(key):
    return f"{URL}/imagenes/{key}.jpg"


# Foto principal de las páginas: 380 px de ancho máximo en escritorio y 300 px por debajo de 880 px
# (.hero-photo en guia.css), o el ancho de la pantalla menos los márgenes si es aún más estrecha.
HERO_SIZES = "(min-width: 880px) 380px, min(300px, calc(100vw - 40px))"


def picture(key, alt=None, sizes=HERO_SIZES, eager=False, cls=""):
    im = IMAGES[key]
    alt = im["alt_corto"] if alt is None else alt
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    avif = f'{img_path(key, 480, "avif")} 480w, {img_path(key, 960, "avif")} 960w'
    webp = f'{img_path(key, 480)} 480w, {img_path(key, 960)} 960w'
    return (f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f'<img{c} src="{img_path(key, 960)}" srcset="{webp}" sizes="{sizes}" '
            f'width="{im["w"]}" height="{im["h"]}" alt="{esc(alt)}" {load}></picture>')


def thumb(key, alt):
    return (f'<img src="{img_path(key, 160)}" width="160" height="160" alt="{esc(alt)}" '
            f'loading="lazy" decoding="async">')


def credit(key):
    im = IMAGES[key]
    return (f'<li>{esc(im["alt_corto"])}: <a href="{im["source"]}" target="_blank" rel="noopener">'
            f'{esc(im["author"])}</a> · {im["license"]}</li>')


# ---------------------------------------------------------------- flor SVG
def petals(hex_, s, count):
    out = []
    rx = s * (0.22 if count > 8 else 0.32)
    for k in range(count):
        out.append(f'<ellipse class="petal" cx="0" cy="{-s * .5:.2f}" rx="{rx:.2f}" ry="{s * .5:.2f}" '
                   f'transform="rotate({k * 360 / count:.1f})" fill="{hex_}"/>')
    return "".join(out) + f'<circle class="pistil" r="{s * .24:.2f}"/>'


def bloom(hex_, count=10, cls="", size=11):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="-12 -12 24 24" aria-hidden="true">{petals(hex_, size, count)}</svg>'


def color_hex(c):
    return "#9DBF9E" if c == "blanco" else COLORS[c]["hex"]


# ---------------------------------------------------------------- cabecera y pie
NAV = [("fechas", "/#fechas", "Fechas"), ("meses", "/meses/", "Por mes"), ("flores", "/flores/", "Por flor"),
       ("paises", "/paises/", "Países"), ("colores", "/significado-colores-flores/", "Colores"),
       ("guias", "/guias/", "Guías")]


def header(active=None):
    items = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for key, href, label in NAV)
    return f'''<header class="site-head">
    <div class="site-head-in">
      <a class="brand" href="/">{bloom("#F2C230", 10)}<span><b>Florario</b><small>Calendario de flores</small></span></a>
      <nav class="site-nav" aria-label="Menú principal"><ul>{items}</ul></nav>
    </div>
  </header>'''


def footer(current="", fuentes=(), images=()):
    def links(pairs):
        return "".join(
            f'<li><a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{esc(label)}</a></li>'
            for href, label in pairs)
    meses = [(f"/{m}/", m.capitalize()) for m in MONTHS]
    flores = [(f'/{f["slug"]}/', f["name"]) for f in FLOWERS]
    guias = [(f'/{g["slug"]}/', g["name"]) for g in GUIDES]
    paises = [(f'/{c["slug"]}/', c["name"]) for c in COUNTRIES.values()] + [("/paises/", "Todos los países")]
    cal = [("/#fechas", "Todas las fechas"), ("/#temporada", "Flores de temporada"),
           ("/calendario-de-flores-para-imprimir/", "Calendario para imprimir"),
           (f"/descargas/calendario-de-flores-{YEAR}.pdf", f"Calendario {YEAR} en PDF"),
           (f"/descargas/calendario-de-flores-{YEAR + 1}.pdf", f"Calendario {YEAR + 1} en PDF"),
           ("/#recuerdamelo", "Recuérdamelo (.ics)")]
    florario = [("/sobre-florario/", "Sobre Florario"), ("/contacto/", "Contacto"), ("/prensa/", "Prensa"),
                ("/politica-de-privacidad/", "Política de privacidad"), ("/aviso-legal/", "Aviso legal")]
    src = ""
    if fuentes:
        src = ('<div><p class="foot-h">Fuentes consultadas</p><ul class="foot-inline">' + "".join(
            f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{t}</a></li>' for t, u in fuentes) + "</ul></div>")
    cred = ""
    keys = list(dict.fromkeys(images))
    if keys:
        cred = ('<details><summary>Créditos de las fotos · Wikimedia Commons</summary><ul>'
                + "".join(credit(k) for k in keys) + "</ul></details>")
    return f'''<footer class="site-foot">
    <div class="foot-grid">
      <div class="foot-about">
        <p class="foot-h">Florario – Calendario de flores</p>
        <p>Todas las fechas del año para regalar flores en España y Latinoamérica: qué flor se regala, dónde y por qué, con flores de temporada y guías por fecha, mes y flor.</p>
      </div>
      <nav aria-label="Calendario"><p class="foot-h">Calendario</p><ul>{links(cal)}</ul></nav>
      <nav aria-label="Por mes"><p class="foot-h">Por mes</p><ul>{links(meses)}</ul></nav>
      <nav aria-label="Por flor"><p class="foot-h">Por flor</p><ul>{links(flores)}</ul></nav>
      <nav aria-label="Guías"><p class="foot-h">Guías</p><ul>{links(guias)}</ul></nav>
      <nav aria-label="Por país"><p class="foot-h">Por país</p><ul>{links(paises)}</ul></nav>
      <nav aria-label="Florario"><p class="foot-h">Florario</p><ul>{links(florario)}</ul></nav>
    </div>
    {src}
    {cred}
    <p class="foot-legal"><span>© {UPDATED.year} Florario – Calendario de flores</span><span>Última actualización: {time_tag(UPDATED)}</span></p>
  </footer>'''


# ---------------------------------------------------------------- JSON-LD
ORG = {"@type": "Organization", "@id": f"{URL}/#org", "name": "Florario",
       "alternateName": "Florario – Calendario de flores", "url": f"{URL}/",
       "logo": {"@type": "ImageObject", "url": f"{URL}/imagenes/logo-florario.png", "width": 512, "height": 512},
       "description": "Calendario de fechas para regalar flores en España y Latinoamérica."}
WEBSITE = {"@type": "WebSite", "@id": f"{URL}/#website", "name": "Florario", "alternateName": "Calendario de flores",
           "url": f"{URL}/", "inLanguage": "es", "publisher": {"@id": f"{URL}/#org"}}
AUTHOR = {"@type": "Person", "@id": f"{URL}/sobre-florario/#autor", "name": SITE["author"],
          "url": f"{URL}/sobre-florario/", "worksFor": {"@id": f"{URL}/#org"}}
if not pending(SITE["author_bio"]):
    AUTHOR["description"] = SITE["author_bio"]
if not pending(SITE["author_sameAs"]):
    AUTHOR["sameAs"] = SITE["author_sameAs"]
REVIEWER = None if pending(SITE["reviewer"]) else SITE["reviewer"]


def reviewer_ld():
    r = REVIEWER
    return {"@type": "Person", "name": r["name"],
            "worksFor": {"@type": "Organization", "name": r["business"], "url": r["url"],
                         "address": {"@type": "PostalAddress", "addressLocality": r["city"]}}}


def dates_list_ld(evs, name, ref=None):
    """Lista de fechas como ItemList de ListItem (sin Event: son festividades, no eventos organizados)."""
    evs = sorted(evs, key=lambda e: next_date(e, ref or HOY))
    return {"@type": "ItemList", "name": name, "itemListOrder": "https://schema.org/ItemListOrderAscending",
            "numberOfItems": len(evs), "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": f'{fmt(next_date(e, ref or HOY))}: {e["name"]} – {e["flower"]}',
                 "url": page_url(e["guia"])} for i, e in enumerate(evs)]}


def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
        for q, a in faq]}


def ld_script(graph):
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
            + "\n</script>")


def hreflang_links():
    out = [f'<link rel="alternate" hreflang="es" href="{URL}/">',
           f'<link rel="alternate" hreflang="x-default" href="{URL}/">']
    out += [f'<link rel="alternate" hreflang="{c["hreflang"]}" href="{URL}/{c["slug"]}/">' for c in COUNTRIES.values()]
    return "\n".join(out)


FAVICON = ('<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
           '<link rel="apple-touch-icon" href="/imagenes/logo-florario.png">')
# Fuentes alojadas en /fuentes/ (el @font-face está en comun.css). Se precarga la del texto.
FONTS = '<link rel="preload" href="/fuentes/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>'


def head_meta(title, description, slug, img, og_type="article", og_title=None, hreflang=False, extra="",
              modified=None, locale="es_ES", og_image=None):
    """og_image = {"url", "w", "h", "alt"} para una imagen que no está en IMAGES (vista previa del PDF)."""
    if og_image is None:
        im = IMAGES[img]
        og_image = {"url": jpg_url(img), "w": im["w"], "h": im["h"], "alt": im["alt"]}
    alternates = "".join(f'\n<meta property="og:locale:alternate" content="{l}">'
                         for l in LOCALE.values() if l != locale) if locale != "es_ES" or slug in LOCALE else ""
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="{esc(SITE["author"])}">
<meta name="theme-color" content="#F2C230">
<link rel="canonical" href="{page_url(slug)}">
{hreflang_links() if hreflang else ""}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(SITE["brand"])}">
<meta property="og:url" content="{page_url(slug)}">
<meta property="og:locale" content="{locale}">{alternates}
<meta property="og:title" content="{esc(og_title or title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{og_image["url"]}">
<meta property="og:image:width" content="{og_image["w"]}">
<meta property="og:image:height" content="{og_image["h"]}">
<meta property="og:image:alt" content="{esc(og_image["alt"])}">
<meta name="twitter:card" content="summary_large_image">
<meta property="article:modified_time" content="{(modified or UPDATED).isoformat()}">
{FAVICON}
{FONTS}
{extra}'''


# ---------------------------------------------------------------- bloques de contenido
def rolling_range(evs, ref=None):
    """Primera y última fecha de la tabla rodante: 12 meses a partir de la próxima fecha."""
    ds = sorted(next_date(e, ref or HOY) for e in evs)
    return ds[0], ds[-1]


def rolling_label(evs, ref=None):
    a, b = rolling_range(evs, ref)
    return f"{MONTH_SHORT[a.month - 1]} {a.year} – {MONTH_SHORT[b.month - 1]} {b.year}"


def date_table(evs, caption, group_by_month=True, years=(YEAR, YEAR + 1), show_month_links=True, rolling=False, ref=None):
    """Tabla estática con fecha, flor, color, país y por qué, con <time datetime>.

    rolling=True: empieza por la próxima fecha (respecto a la del build) y cubre los 12 meses
    siguientes, con el año real de cada fila. Si no, ordena el año years[0] y muestra también
    la fecha de years[1] en las fechas móviles."""
    rows = []
    last_m = None
    y0, y1 = years
    if rolling:
        order = [(ev, next_date(ev, ref or HOY)) for ev in evs]
        order.sort(key=lambda x: x[1])
    else:
        order = [(ev, date_for(ev, y0)) for ev in events_sorted(evs, y0)]
    for ev, d0 in order:
        m = (d0.year, d0.month) if rolling else d0.month
        if group_by_month and m != last_m:
            name = MONTHS[d0.month - 1].capitalize()
            cell = f'<a href="/{MONTHS[d0.month - 1]}/">{name}</a>' if show_month_links else name
            if rolling:
                cell += f" {d0.year}"
            anchor = f"m-{MONTHS[d0.month - 1]}" + (f"-{d0.year}" if rolling else "")
            rows.append(f'<tr class="mhead"><th colspan="5" scope="colgroup" id="{anchor}">{cell}</th></tr>')
            last_m = m
        guide = ev["guia"]
        name = f'<a href="/{guide}/">{esc(ev["name"])}</a>'
        if rolling:
            other = f'<small>{ev["ruleText"]}</small>' if "rule" in ev else "<small>cada año</small>"
            label = f"{WEEKDAYS[d0.weekday()][:3]} {d0.day} {MONTH_SHORT[d0.month - 1]} {d0.year}"
        else:
            d1 = date_for(ev, y1)
            other = (f'<small>{y1}: {time_tag(d1, f"{d1.day} {MONTH_SHORT[d1.month - 1]}")}</small>'
                     if "rule" in ev else "<small>cada año</small>")
            label = f"{WEEKDAYS[d0.weekday()][:3]} {d0.day} {MONTH_SHORT[d0.month - 1]}"
        rows.append(
            f'<tr id="f-{ev["id"]}" style="--dc:{color_hex(ev["color"])}">'
            f'<td class="when">{time_tag(d0, label)}{other}</td>'
            f'<td><span class="ev-name">{name}</span><p class="why">{esc(ev["story"])}</p></td>'
            f'<td data-label="Flor">{esc(ev["flower"])}</td>'
            f'<td data-label="Color"><span class="swatch">{COLORS[ev["color"]]["label"]}</span></td>'
            f'<td data-label="Dónde">{esc(ev["region"])}</td></tr>')
    cap = f"<caption>{caption}</caption>" if caption else ""
    first_col = "Fecha" if rolling else f"Fecha {y0}"
    return (f'<div class="dtable-wrap"><table class="dtable">{cap}<thead><tr><th scope="col">{first_col}</th>'
            f'<th scope="col">Qué se celebra y por qué</th><th scope="col">Flor</th><th scope="col">Color</th>'
            f'<th scope="col">Dónde</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def flower_link(name):
    low = name.lower()
    for f in FLOWERS:
        for mt in f["match"]:
            if low == mt.lower() or low.startswith(mt.lower() + " ") or f"({mt.lower()})" in low:
                return f'<a href="/{f["slug"]}/">{esc(name)}</a>'
    return esc(name)


def season_table(months=range(12), link_months=True):
    head = "".join(f'<th scope="col">{label}</th>' for _, label in SEASON_REGIONS)
    rows = []
    for m in months:
        name = MONTHS[m].capitalize()
        cell = f'<a href="/{MONTHS[m]}/">{name}</a>' if link_months else f"<span>{name}</span>"
        tds = "".join(f'<td>{", ".join(flower_link(x) for x in SEASON[m][k])}</td>' for k, _ in SEASON_REGIONS)
        rows.append(f'<tr data-m="{m}" style="--mc:{MONTH_COLORS[m]}"><th scope="row">{cell}</th>{tds}</tr>')
    return (f'<div class="season-wrap"><table class="season"><caption class="sr-only">Flores de temporada por mes y región</caption>'
            f'<thead><tr><th scope="col">Mes</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="season-note">{SEASON_NOTE} Tabla orientativa: la temporada cambia con la zona y el año, y los invernaderos alargan casi todas.</p>')


def gcard(slug, alt=None):
    if slug in GUIDE:
        g = GUIDE[slug]
        small, name, desc, img, col = g["small"], g["name"], g["desc"], g["img"], g["color"]
    elif slug in FLOWER:
        f = FLOWER[slug]
        small, name, desc, img, col = "Por flor", f["name"], "Significado, temporada y cuándo regalarla", f["img"], f["color"]
    elif slug in MONTHS:
        m = MONTHS.index(slug)
        evs = [e for e in EVENTS if month_of(e) == m + 1]
        small, name = "Por mes", f"Flores de {slug}"
        desc = f'{len(evs)} {"fecha" if len(evs) == 1 else "fechas"} y flores de temporada'
        img = evs[0]["img"] if evs else "ramo-silvestre"
        col = None
    elif slug in HUB_CARDS:
        small, name, desc, img, col = HUB_CARDS[slug]
    elif slug in COUNTRY_BY_SLUG:
        code, c = COUNTRY_BY_SLUG[slug]
        n = len([e for e in EVENTS if code in e["paises"]])
        small, name, desc, img, col = "Por país", f'Fechas {c["de"]}', f"{n} fechas para regalar flores", "ramo-silvestre", "rosa"
    else:
        raise KeyError(slug)
    gc = MONTH_COLORS[MONTHS.index(slug)] if col is None else color_hex(col)
    return (f'<a class="gcard" href="/{slug}/" style="--gc:{gc}">{thumb(img, alt or f"{name}: {IMAGES[img]['alt_corto']}")}'
            f'<span><small>{esc(small)}</small><b>{esc(name)}</b><i>{esc(desc)}</i></span></a>'), img


def cards(slugs):
    out, imgs = [], []
    for s in slugs:
        h, i = gcard(s)
        out.append(h)
        imgs.append(i)
    return "\n".join(out), imgs


def faq_html(faq):
    return "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)


def gcal_link(ev):
    d = next_date(ev) - dt.timedelta(days=3)
    e = d + dt.timedelta(days=1)
    from urllib.parse import quote
    text = quote(f'Comprar flores: {ev["name"]} ({fmt(next_date(ev), year=False)})')
    det = quote(f'{ev["flower"]}. {ev["story"]} Más en {page_url(ev["guia"])}')
    return (f"https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text={text}"
            f"&amp;dates={d:%Y%m%d}/{e:%Y%m%d}&amp;details={det}")


def remind_box(evs, heading="h2"):
    btns = []
    if len(evs) > 4:
        btns.append('<a class="btn primary" href="/descargas/calendario-de-flores.ics" download>Todas las fechas (.ics)</a>')
        btns.append(f'<a class="btn" href="https://calendar.google.com/calendar/r?cid=webcal://{URL.split("://")[1]}/descargas/calendario-de-flores.ics" target="_blank" rel="noopener">Suscribirme en Google Calendar ↗</a>')
    else:
        for ev in evs:
            label = ev["name"] if len(evs) > 1 else "Añadir a mi calendario"
            btns.append(f'<a class="btn primary" href="/recordatorios/{ev["id"]}.ics" download>{esc(label)} (.ics)</a>')
        btns.append(f'<a class="btn" href="{gcal_link(evs[0])}" target="_blank" rel="noopener">Google Calendar ↗</a>')
    return f'''<section class="remind" id="recuerdamelo" aria-labelledby="recuerdamelo-t">
          <{heading} id="recuerdamelo-t">Recuérdamelo 3 días antes</{heading}>
          <p>Descarga el recordatorio y ábrelo con el calendario del móvil: se repite cada año y te avisa tres días antes para que te dé tiempo a encargar el ramo.</p>
          <div class="remind-actions">{"".join(btns)}</div>
        </section>'''


def next_widget(evs):
    evs = sorted(evs, key=next_date)
    first = evs[0]
    d = next_date(first)
    names = "|".join(e["name"] for e in evs)
    ids = "|".join(e["id"] for e in evs)
    whens = " ".join(when_code(e) for e in evs)
    return (f'<a class="next" href="/#{first["id"]}" data-when="{whens}" data-names="{esc(names)}" data-ids="{ids}">'
            f'<span class="next-num">{d.day}</span><span class="next-label">de {MONTHS[d.month - 1]} de {d.year}</span>'
            f'<span class="next-name">{esc(first["name"])}</span><span class="next-go" aria-hidden="true">→</span></a>')


def facts_html(facts):
    if isinstance(facts, str):
        return facts
    return '<dl class="facts">' + "".join(
        f'<div><dt>{dt_}</dt><dd>{dd}{f"<small>{sm}</small>" if sm else ""}</dd></div>' for dt_, dd, sm in facts) + "</dl>"


def when_line(published, updated):
    """“Publicado el …” si la página no ha cambiado desde que se publicó; si no, “Actualizado el …”."""
    if updated > published:
        return f"Actualizado el {time_tag(updated)}"
    return f"Publicado el {time_tag(published)}"


def byline(published=None, updated=None, author=True):
    published, updated = published or PUBLISHED, updated or UPDATED
    parts = []
    if author:
        parts.append(f'Por <a href="/sobre-florario/" rel="author">{esc(SITE["author"])}</a>')
        if REVIEWER:
            r = REVIEWER
            parts.append(f'Revisado por <a href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(r["name"])}</a>, '
                         f'{esc(r["business"])} ({esc(r["city"])})')
    parts.append(when_line(published, updated))
    return '<p class="byline">' + '<span class="dot">·</span>'.join(f"<span>{p}</span>" for p in parts) + "</p>"


def share_box(text, url):
    """WhatsApp (enlace normal, funciona sin JavaScript) y compartir nativo o copiar enlace (guia.js)."""
    from urllib.parse import quote
    wa = "https://wa.me/?text=" + quote(f"{text} {url}")
    return (f'<div class="share"><p>¿Conoces a alguien que siempre llega tarde a estas fechas? Pásaselo.</p>'
            f'<div class="share-actions"><a class="btn" href="{wa}" target="_blank" rel="noopener">Compartir por WhatsApp</a>'
            f'<button type="button" class="btn" data-share data-url="{esc(url)}" data-title="{esc(text)}" hidden>Compartir</button></div>'
            f'<p class="share-status" role="status"></p></div>')


def author_box():
    return (f'<aside class="author-box" aria-label="Sobre el autor">{bloom("#F2C230", 10)}'
            f'<p><b>{esc(SITE["author"])}</b> · Florario</p><p>{esc(SITE["author_bio"])} '
            f'<a href="/sobre-florario/">Cómo hacemos Florario</a>.</p></aside>')


# ---------------------------------------------------------------- páginas con texto
def read_fragment(path):
    raw = open(path, encoding="utf-8").read()
    # {{year}}, {{year_next}} y {{print_year}} también valen en la cabecera (title, description…)
    raw = (raw.replace("{{year}}", str(YEAR)).replace("{{year_next}}", str(YEAR + 1))
           .replace("{{print_year}}", str(PRINT_YEAR)))
    _, fm, body = raw.split("---\n", 2)
    meta = json.loads(fm)
    meta["published"] = dt.date.fromisoformat(meta.get("published", SITE["published"]))
    meta["updated"] = dt.date.fromisoformat(meta.get("updated", meta["published"].isoformat()))
    meta["file"] = os.path.basename(path)
    return meta, body


def stale_dates(frags):
    """Avisa si un fragmento tiene cambios sin confirmar en git pero su "updated" es anterior a hoy."""
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--", "paginas"], cwd=BUILD,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return
    changed = {os.path.basename(l[3:].strip().strip('"')) for l in out.splitlines() if l[:2].strip() in ("M", "MM", "AM")}
    for meta, _ in frags:
        if meta["file"] in changed and meta["updated"] < HOY:
            WARN.append(f'{meta["file"]} tiene cambios pero su "updated" sigue en {meta["updated"]}: '
                        f'si el cambio es de contenido, ponlo a {HOY}.')


def stats():
    """Cifras para /prensa/ y /sobre-florario/, siempre sacadas de datos.py."""
    by_type = {t: len([e for e in EVENTS if e["type"] == t]) for t in TYPES}
    return {"n_events": len(EVENTS), "n_trend": by_type["trend"], "n_clasico": by_type["clasico"],
            "n_memoria": by_type["memoria"], "n_guides": len(GUIDES), "n_flowers": len(FLOWERS),
            "n_countries": len(COUNTRIES), "n_songs": len([e for e in EVENTS if e.get("song")])}


def auto_blocks(meta, body):
    """Sustituye los marcadores <!--@...--> de los fragmentos por bloques generados."""
    slug = meta["slug"]
    for k in ("author", "author_bio", "owner", "email"):
        body = body.replace("{{" + k + "}}", esc(SITE[k]))
    body = body.replace("{{updated}}", time_tag(meta["updated"])).replace("{{site_updated}}", time_tag(UPDATED))
    for k, v in stats().items():
        body = body.replace("{{" + k + "}}", str(v))
    body = body.replace("{{n_pages}}", str(N_PAGES))
    if "<!--@REVISOR-->" in body:
        if REVIEWER:
            r = REVIEWER
            block = (f'<p>Las guías las revisa <strong>{esc(r["name"])}</strong>, de <a href="{esc(r["url"])}" target="_blank" rel="noopener">'
                     f'{esc(r["business"])}</a> ({esc(r["city"])}). Comprueba que las flores que recomiendo se encuentran de verdad '
                     f'en esas fechas, que los consejos de cuidado son correctos y que los precios y la temporada tienen sentido. '
                     f'Cada página revisada lo indica debajo del título.</p>')
        else:
            block = (f'<p>Por ahora escribo y reviso yo todo el contenido, a partir de las fuentes que cito al pie de cada guía. '
                     f'No soy florista, y por eso busco una floristería o un productor que revise las guías antes de cada fecha: '
                     f'comprobar que las flores que recomiendo se encuentran de verdad en esa época y que los consejos de cuidado son correctos. '
                     f'Si te dedicas a las flores y te interesa, <a href="/contacto/">escríbeme</a>. Cuando haya una revisión profesional, '
                     f'cada página lo indicará debajo del título con el nombre de quien la ha hecho.</p>')
        body = body.replace("<!--@REVISOR-->", block)
    if "<!--@CIFRAS-->" in body:
        rows = "".join(f'<tr><th scope="row">{c["name"]}</th><td>{len([e for e in EVENTS if code in e["paises"]])}</td></tr>'
                       for code, c in COUNTRIES.items())
        body = body.replace("<!--@CIFRAS-->", f'<div class="dtable-wrap"><table class="dtable"><caption>Fechas para regalar flores por país</caption>'
                                              f'<thead><tr><th scope="col">País</th><th scope="col">Fechas</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if "<!--@WIDGET_CODE-->" in body:
        code = f'<iframe src="{URL}/widget/" title="Próxima fecha para regalar flores · Florario" width="320" height="200" style="border:0;max-width:100%" loading="lazy"></iframe>'
        body = body.replace("<!--@WIDGET_CODE-->", f'<pre class="code"><code>{esc(code)}</code></pre>')
    if "<!--@WIDGET_DEMO-->" in body:
        body = body.replace("<!--@WIDGET_DEMO-->", '<iframe src="/widget/" title="Vista previa del widget de Florario" width="320" height="200" style="border:0;max-width:100%" loading="lazy"></iframe>')
    if "<!--@PREVIEWS-->" in body:
        figs = "".join(
            f'<figure class="pdf-preview"><a href="/descargas/calendario-de-flores-{y}.pdf" download>'
            f'<img src="/descargas/calendario-de-flores-{y}.jpg" width="{PREVIEW_W}" height="{PREVIEW_H}" '
            f'alt="Portada del calendario de flores {y} para imprimir: corona de flores con los doce meses" loading="lazy" decoding="async"></a>'
            f'<figcaption><a href="/descargas/calendario-de-flores-{y}.pdf" download>Calendario de flores {y} · PDF A4</a></figcaption></figure>'
            for y in (YEAR, YEAR + 1))
        body = body.replace("<!--@PREVIEWS-->", f'<div class="pdf-previews">{figs}</div>')
    if "<!--@FECHAS_MES-->" in body:
        m = MONTHS.index(slug) + 1
        evs = [e for e in EVENTS if month_of(e) == m]
        yr = min(next_date(e) for e in evs).year if evs else YEAR
        block = date_table(evs, f"Fechas con flores en {slug} de {yr}", group_by_month=False, rolling=True) if evs else \
            '<p class="note">Este mes no hay ninguna fecha del calendario en la que la costumbre sea regalar flores.</p>'
        body = body.replace("<!--@FECHAS_MES-->", block)
    if "<!--@TEMPORADA_MES-->" in body:
        m = MONTHS.index(slug)
        body = body.replace("<!--@TEMPORADA_MES-->", season_table([m], link_months=False))
    if "<!--@FECHAS_PAIS-->" in body:
        code = meta["pais"]
        evs = [e for e in EVENTS if code in e["paises"]]
        body = body.replace("<!--@FECHAS_PAIS-->", date_table(
            evs, f'Próximas fechas para regalar flores {COUNTRIES[code]["en"]} ({rolling_label(evs)})', rolling=True))
    if "<!--@FECHAS-->" in body:
        evs = [EV[i] for i in meta.get("eventos", [])]
        body = body.replace("<!--@FECHAS-->", date_table(evs, "", group_by_month=False, rolling=True))
    if "<!--@TEMPORADA_FLOR-->" in body:
        f = FLOWER[slug]
        rows = []
        for k, label in SEASON_REGIONS:
            ms = [MONTHS[i] for i in range(12) if any(
                x.lower() == mt.lower() or x.lower().startswith(mt.lower() + " ") or f"({mt.lower()})" in x.lower()
                for x in SEASON[i][k] for mt in f["match"])]
            txt = ", ".join(f'<a href="/{m}/">{m}</a>' for m in ms) if ms else "fuera de temporada local (llega de invernadero o importada)"
            rows.append(f"<li><strong>{label}:</strong> {txt}.</li>")
        body = body.replace("<!--@TEMPORADA_FLOR-->", "<ul>" + "".join(rows) + "</ul>")
    return body


def toc_from(body):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    return "".join(f'<li><a href="#{i}">{strip_tags(t)}</a></li>' for i, t in items)


def render_article(meta, body):
    slug = meta["slug"]
    tipo = meta["tipo"]
    body = auto_blocks(meta, body)
    evs = [EV[i] for i in meta.get("eventos", [])]
    if tipo == "mes" and not evs:
        evs = events_sorted([e for e in EVENTS if month_of(e) == MONTHS.index(slug) + 1])
    if tipo == "pais" and not evs:
        evs = [e for e in EVENTS if meta["pais"] in e["paises"]]
    faq = meta.get("faq", [])
    img = meta.get("img")
    if meta.get("og_image") == "preview":
        meta["og_image"] = {"url": f"{URL}/descargas/calendario-de-flores-{PRINT_YEAR}.jpg", "w": PREVIEW_W, "h": PREVIEW_H,
                            "alt": f"Portada del calendario de flores {PRINT_YEAR} para imprimir"}
    parent = {"flor": ("Por flor", "/flores/"), "mes": ("Por mes", "/meses/"), "guia": ("Guías", "/guias/"),
              "pais": ("Por país", "/paises/")}.get(tipo)
    crumbs = [("Calendario de flores", f"{URL}/")]
    if parent:
        crumbs.append((parent[0], URL + parent[1]))
    crumbs.append((meta.get("crumb", meta["title"]), page_url(slug)))

    # JSON-LD
    graph = [ORG, WEBSITE]
    if tipo in ("guia", "flor", "mes", "pais", "descarga"):
        graph.append(AUTHOR)
        graph.append({"@type": "Article", "@id": page_url(slug) + "#articulo",
                      "headline": strip_tags(meta.get("headline", meta["h1"]))[:110],
                      "description": meta["description"], "image": jpg_url(img) if img else None,
                      "inLanguage": "es", "datePublished": meta["published"].isoformat(),
                      "dateModified": meta["updated"].isoformat(), "mainEntityOfPage": page_url(slug),
                      "author": {"@id": AUTHOR["@id"]}, "publisher": {"@id": ORG["@id"]},
                      "isPartOf": {"@id": WEBSITE["@id"]}})
        if REVIEWER:
            graph.append({"@type": "WebPage", "@id": page_url(slug), "url": page_url(slug),
                          "reviewedBy": reviewer_ld(), "lastReviewed": meta["updated"].isoformat()})
    else:
        graph.append({"@type": meta.get("schema", "WebPage"), "@id": page_url(slug), "name": meta["title"],
                      "description": meta["description"], "inLanguage": "es", "isPartOf": {"@id": WEBSITE["@id"]},
                      "datePublished": meta["published"].isoformat(), "dateModified": meta["updated"].isoformat()})
        if slug == "sobre-florario":
            graph.append(AUTHOR)
    graph.append(breadcrumb(crumbs))
    if faq:
        graph.append(faq_ld(faq))
    ld_events = evs
    if tipo == "mes":
        ld_events = [e for e in EVENTS if month_of(e) == MONTHS.index(slug) + 1]
    if tipo == "pais":
        ld_events = [e for e in EVENTS if meta["pais"] in e["paises"]]
    if ld_events:
        graph.append(dates_list_ld(ld_events, f'Fechas para regalar flores: {strip_tags(meta.get("crumb", meta["title"]))}'))
    graph = [g for g in graph if g]
    for g in graph:
        if g.get("image") is None:
            g.pop("image", None)

    title = full_title(meta["title"])
    head = head_meta(title, meta["description"], slug, img or "ramo-silvestre",
                     og_type="article" if tipo in ("guia", "flor", "mes", "pais", "descarga") else "website",
                     og_title=meta.get("og_title"), hreflang=tipo == "pais",
                     modified=meta["updated"], locale=LOCALE.get(slug, "es_ES"), og_image=meta.get("og_image"),
                     extra='<link rel="stylesheet" href="/guia.css">\n<link rel="stylesheet" href="/comun.css">\n' + ld_script(graph))

    # Cuerpo
    used_imgs = [img] if img else []
    nxt = meta.get("next_html") or (next_widget(evs) if evs else "")
    hero_photo = ""
    bloom_color = meta.get("color", "c-amarillo")[2:]
    if bloom_color not in COLORS:
        bloom_color = "rosa"
    if img:
        im = IMAGES[img]
        hero_photo = f'''<figure class="hero-photo">
          {picture(img, meta.get("img_alt") or (IMAGES[img]["alt"] if tipo == "flor" else None), eager=True)}
          {bloom(color_hex(bloom_color), 10, "hero-bloom")}
          <figcaption>Foto: <a href="{im["source"]}" target="_blank" rel="noopener">{esc(im["author"])}</a> · {im["license"]}</figcaption>
        </figure>'''
    facts = facts_html(meta["facts"]) if meta.get("facts") else ""
    toc = toc_from(body)
    if faq:
        toc += '<li><a href="#preguntas">Preguntas frecuentes</a></li>'
    cal_link = meta.get("cal_link") or (f'#{evs[0]["id"]}' if evs else "#fechas")
    faq_block = f'''<section id="preguntas" aria-labelledby="preguntas-t">
          <h2 id="preguntas-t">Preguntas frecuentes</h2>
          <div class="faq">
            {faq_html(faq)}
          </div>
        </section>''' if faq else ""
    remind = remind_box(evs) if evs else ""
    is_article = tipo in ("guia", "flor", "mes", "pais", "descarga")
    related_slugs = meta.get("related") or []
    rel_html, rel_imgs = cards(related_slugs) if related_slugs else ("", [])
    used_imgs += rel_imgs
    related = f'''<section class="related" aria-labelledby="related-t">
      <h2 id="related-t">{meta.get("related_title", "Sigue explorando")}</h2>
      <div class="gcards">
      {rel_html}
      </div>
    </section>''' if rel_html else ""
    n_events = len(EVENTS)
    cta = f'''<section class="cta" aria-labelledby="cta-t">
      <div>
        <h2 id="cta-t">Todas las fechas en un solo calendario</h2>
        <p>{n_events} fechas para regalar flores, de San Valentín al Día de Muertos, con la foto de cada flor, filtros por color, cuenta atrás y versión en PDF para imprimir.</p>
      </div>
      <a class="btn primary" href="/">Abrir el calendario de flores</a>
    </section>'''
    toc_nav = f'''<nav class="toc" aria-label="En esta página">
          <details open>
            <summary>En esta página</summary>
            <h2>En esta página</h2>
            <ol>{toc}</ol>
          </details>
          <a class="btn primary" href="/{cal_link}">Ver en el calendario</a>
        </nav>''' if toc and is_article else ""
    crumb_html = "".join(f'<li><a href="{u.replace(URL, "") or "/"}">{esc(n)}</a></li>' for n, u in crumbs[:-1])
    hero_cls = "hero" if img else "hero hero-text"
    page = f'''<!doctype html>
<html lang="es">
<head>
{head}
</head>
<body class="{meta.get("color", "c-todos")}">
<div class="wrap">
  {header(meta.get("nav"))}
  <nav class="crumbs" aria-label="Estás aquí">
    <ol>{crumb_html}<li aria-current="page">{esc(crumbs[-1][0])}</li></ol>
  </nav>

  <main>
    <article>
      <div class="{hero_cls}">
        <div class="hero-copy">
          <p class="eyebrow">{meta["eyebrow"]}</p>
          <h1>{meta["h1"]}</h1>
          <p class="lede">{meta["lede"]}</p>
          {byline(meta["published"], meta["updated"], author=is_article)}
          {nxt}
        </div>
        {hero_photo}
      </div>
      {facts}
      <div class="layout{"" if toc_nav else " layout-single"}">
        {toc_nav}
        <div class="prose">
        {body.strip()}
        {remind}
        {share_box(meta.get("og_title") or meta["title"], page_url(slug)) if tipo != "info" or meta.get("share") else ""}
        {faq_block}
        {author_box() if is_article else ""}
        </div>
      </div>
    </article>
    {related}
    {cta if tipo != "info" else ""}
  </main>

  {footer("/" + slug + "/", meta.get("fuentes", []), used_imgs)}
</div>
<script src="/guia.js" defer></script>
</body>
</html>
'''
    write(f"{slug}/index.html", page)
    return {"slug": slug, "tipo": tipo, "words": words(body + faq_html(faq)), "img": img, "title": meta["title"],
            "updated": meta["updated"], "img_url": (meta.get("og_image") or {}).get("url")}


# ---------------------------------------------------------------- hubs
def render_hub(slug, title, description, h1, eyebrow, lede, items, nav, intro_html, img, updated=None):
    """updated = la fecha más reciente de las páginas que enlaza."""
    updated = updated or UPDATED
    graph = [ORG, WEBSITE,
             {"@type": "CollectionPage", "@id": page_url(slug), "name": title, "description": description,
              "inLanguage": "es", "isPartOf": {"@id": WEBSITE["@id"]}, "datePublished": PUBLISHED.isoformat(),
              "dateModified": updated.isoformat()},
             breadcrumb([("Calendario de flores", f"{URL}/"), (h1 if "<" not in h1 else strip_tags(h1), page_url(slug))]),
             {"@type": "ItemList", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "url": page_url(s), "name": title_of(s) if s not in MONTHS else f"Flores de {s}"}
                 for i, s in enumerate(items)]}]
    head = head_meta(full_title(title), description, slug, img, og_type="website", modified=updated,
                     extra='<link rel="stylesheet" href="/guia.css">\n<link rel="stylesheet" href="/comun.css">\n' + ld_script(graph))
    html_cards, imgs = cards(items)
    page = f'''<!doctype html>
<html lang="es">
<head>
{head}
</head>
<body class="c-todos">
<div class="wrap">
  {header(nav)}
  <nav class="crumbs" aria-label="Estás aquí"><ol><li><a href="/">Calendario de flores</a></li><li aria-current="page">{strip_tags(h1)}</li></ol></nav>
  <main>
    <div class="hero hero-text">
      <div class="hero-copy">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <p class="lede">{lede}</p>
        {byline(PUBLISHED, updated, author=False)}
      </div>
    </div>
    <section class="related hub" aria-label="{esc(strip_tags(h1))}">
      <div class="gcards">
      {html_cards}
      </div>
    </section>
    <div class="prose hub-intro">{intro_html}</div>
  </main>
  {footer("/" + slug + "/", (), imgs)}
</div>
</body>
</html>
'''
    write(f"{slug}/index.html", page)
    return {"slug": slug, "tipo": "hub", "words": words(intro_html), "img": img, "title": title, "updated": updated}


# ---------------------------------------------------------------- portada
def render_home():
    tpl = open(os.path.join(BUILD, "plantilla-inicio.html"), encoding="utf-8").read()
    title = full_title(f"Calendario de flores {YEAR_LABEL}: qué flor regalar y cuándo")
    description = (f"Calendario de flores {YEAR_LABEL}: todas las fechas para regalar flores en España y Latinoamérica, "
                   "flores de temporada mes a mes y calendario en PDF para imprimir.")
    first, last = rolling_range(EVENTS)
    fechas_t = (f"Próximas fechas para regalar flores ({MONTH_SHORT[first.month - 1]} {first.year} – "
                f"{MONTH_SHORT[last.month - 1]} {last.year})")
    home_faq = [
        ("¿Qué es un calendario de flores?",
         f"Es una lista de las fechas del año en las que es costumbre regalar flores, con la flor que toca en cada una. Florario reúne {len(EVENTS)} fechas de España y Latinoamérica, desde San Valentín y el Día de la Madre hasta los trends de TikTok como las flores amarillas, azules y moradas, y añade qué flores están de temporada cada mes."),
        ("¿Qué flores se regalan el 21 de septiembre?",
         "Flores amarillas: girasoles, tulipanes o rosas amarillas. El trend nació con la canción “Flores amarillas” de Floricienta y se hizo viral en TikTok en 2021 para recibir la primavera del hemisferio sur. En México se repite el 21 de marzo."),
        ("¿Qué flores se regalan en octubre?",
         "El 3 de octubre, Día del Novio, se regalan flores azules o ramos de Hot Wheels. En Argentina el tercer domingo de octubre es el Día de la Madre, con rosas y liliums. En México, a finales de mes empieza la temporada del cempasúchil para el Día de Muertos."),
        ("¿Qué flores se regalan el 9 de noviembre?",
         "Flores moradas, como violetas, lavanda o lisianthus, para tu “persona morada”. El trend sale de la canción “Un ramito de violetas” de Cecilia."),
        ("¿Qué flores son de temporada en otoño?",
         "En España, crisantemos, dalias, asters y rosas de segunda floración. En México, cempasúchil, terciopelo y crisantemos. En Argentina, Chile y Uruguay el otoño cae en marzo, abril y mayo, con dalias, crisantemos y rosas."),
        ("¿Puedo descargar el calendario de flores en PDF?",
         f"Sí. Tienes el calendario de flores {YEAR} y el de {YEAR + 1} en PDF, con portada ilustrada, todas las fechas y la tabla de flores de temporada, listos para imprimir en A4. Están en la página del calendario de flores para imprimir, con una vista previa de cada uno."),
        ("¿Cómo puedo acordarme de las fechas?",
         "Con el botón “Recuérdamelo”: descarga el archivo .ics de una fecha o suscríbete al calendario completo y tu móvil te avisará tres días antes de cada fecha."),
    ]
    graph = [ORG, WEBSITE,
             {"@type": "WebPage", "@id": f"{URL}/#webpage", "url": f"{URL}/", "name": title,
              "description": description, "inLanguage": "es", "isPartOf": {"@id": WEBSITE["@id"]},
              "datePublished": PUBLISHED.isoformat(), "dateModified": UPDATED.isoformat(),
              "primaryImageOfPage": jpg_url("girasol")},
             breadcrumb([("Calendario de flores", f"{URL}/")]),
             faq_ld(home_faq),
             dates_list_ld(EVENTS, fechas_t)]
    head = head_meta(title, description, "", "girasol", og_type="website",
                     og_title=f"Calendario de flores {YEAR_LABEL}: qué flor regalar en cada fecha", hreflang=True,
                     extra='<link rel="stylesheet" href="/comun.css">\n' + ld_script(graph))
    guide_cards, gimgs = cards([g["slug"] for g in GUIDES])
    flower_cards, fimgs = cards([f["slug"] for f in FLOWERS])
    month_tiles = "".join(
        f'<a class="tile" href="/{m}/" style="--tc:{MONTH_COLORS[i]}"><span class="k">{MONTH_SHORT[i]}</span>'
        f'<b>Flores de {m}</b><small>{", ".join(SEASON[i]["es"][:3])}…</small></a>' for i, m in enumerate(MONTHS))
    country_tiles = "".join(
        f'<a class="tile" href="/{c["slug"]}/" hreflang="{c["hreflang"]}"><span class="k">{c["hreflang"]}</span>'
        f'<b>{c["name"]}</b><small>{len([e for e in EVENTS if code in e["paises"]])} fechas para regalar flores</small></a>'
        for code, c in COUNTRIES.items())
    downloads = f'''<div class="tiles">
        <a class="tile" href="/calendario-de-flores-para-imprimir/" style="--tc:#8A4FD8"><span class="k">Para imprimir</span><b>Calendario de flores {PRINT_YEAR} ilustrado</b><small>Vista previa y cómo imprimirlo, gratis para uso personal</small></a>
        <a class="tile" href="/descargas/calendario-de-flores-{YEAR}.pdf" download style="--tc:#F2C230"><span class="k">PDF · A4</span><b>Calendario de flores {YEAR}</b><small>Todas las fechas y las flores de temporada</small></a>
        <a class="tile" href="/descargas/calendario-de-flores-{YEAR + 1}.pdf" download style="--tc:#EE7FA8"><span class="k">PDF · A4</span><b>Calendario de flores {YEAR + 1}</b><small>Con las fechas móviles ya calculadas</small></a>
        <a class="tile" href="/descargas/calendario-de-flores.ics" download style="--tc:#2BB3A3"><span class="k">.ics · Recuérdamelo</span><b>Todas las fechas en tu calendario</b><small>Aviso 3 días antes de cada una</small></a>
        <a class="tile" href="https://calendar.google.com/calendar/r?cid=webcal://{URL.split("://")[1]}/descargas/calendario-de-flores.ics" target="_blank" rel="noopener" style="--tc:#3F72E0"><span class="k">Suscripción</span><b>Añadir a Google Calendar</b><small>Se actualiza sola cuando añadimos fechas</small></a>
      </div>'''
    data_js = "\n".join([
        f"  const COLORS = {json.dumps(COLORS, ensure_ascii=False)};",
        f"  const TYPES = {json.dumps(TYPES, ensure_ascii=False)};",
        f"  const MONTH_COLORS = {json.dumps(MONTH_COLORS)};",
        f"  const IMAGES = {json.dumps({k: {x: v[x] for x in ('file', 'alt_corto', 'author', 'license', 'source')} for k, v in IMAGES.items()}, ensure_ascii=False)};",
        f"  const GUIDE_NAMES = {json.dumps({g['slug']: g['name'] for g in GUIDES} | {f['slug']: f['name'] for f in FLOWERS}, ensure_ascii=False)};",
        "  const EVENTS = " + json.dumps(EVENTS, ensure_ascii=False, indent=1).replace("\n", "\n  ") + ";",
    ])
    rep = {
        "HEAD": head,
        "HEADER": header("fechas"),
        "YEAR": str(YEAR),
        "YEAR_LABEL": YEAR_LABEL,
        "FECHAS_T": fechas_t,
        "BYLINE": byline(PUBLISHED, UPDATED),
        "N_EVENTS": str(len(EVENTS)),
        "FECHAS": date_table(EVENTS, "", rolling=True),
        "TEMPORADA": season_table(),
        "DESCARGAS": downloads,
        "MESES": month_tiles,
        "PAISES": country_tiles,
        "GUIAS": guide_cards,
        "FLORES": flower_cards,
        "FAQ": faq_html(home_faq),
        "FOOTER": footer("/", [
            ("La Nación · flores amarillas", "https://www.lanacion.com.ar/sociedad/por-que-se-regalan-flores-amarillas-el-21-de-septiembre-origen-significado-y-que-relacion-tiene-con-nid18092026/"),
            ("Quién · 21 de marzo o 21 de septiembre", "https://www.quien.com/espectaculos/2026/09/21/flores-amarillas-21-de-marzo-o-21-de-septiembre-diferencia"),
            ("Expansión · Día del Novio", "https://expansion.mx/tendencias/2026/09/24/dia-del-novio-2026-hot-wheels-flores-azules-octubre"),
            ("Infobae · flores moradas", "https://www.infobae.com/mexico/2024/11/08/por-que-se-regalan-flores-moradas-el-9-de-noviembre-y-que-significa/"),
            ("El Espectador · variante 9 de octubre", "https://www.elespectador.com/actualidad/por-que-se-regalan-flores-moradas-en-octubre-historia-del-trend-de-tiktok/"),
            ("Excélsior · Día de la Novia", "https://www.excelsior.com.mx/estilo-de-vida/cuando-es-dia-novia-2026-y-cual-es-polemico-origen"),
            ("SEMARNAT · Día de la Nochebuena", "https://www.gob.mx/semarnat/articulos/dia-nacional-de-la-nochebuena-289960"),
        ], list(IMAGES.keys())),
        "DATA_JS": data_js,
    }
    out = tpl
    for k, v in rep.items():
        out = out.replace(f"<!--@{k}-->", v)
    left = re.findall(r"<!--@([A-Z_]+)-->", out)
    if left:
        raise SystemExit(f"Marcadores sin rellenar en la portada: {left}")
    write("index.html", out)
    return {"slug": "", "tipo": "home", "words": words(re.sub(r"<script.*?</script>", "", out, flags=re.S)), "img": "girasol",
            "title": title, "updated": UPDATED}


# ---------------------------------------------------------------- .ics
def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def ics_fold(line):
    b = line.encode("utf-8")
    if len(b) <= 75:
        return line
    out, cur = [], b""
    for ch in line:
        c = ch.encode("utf-8")
        if len(cur) + len(c) > (75 if not out else 74):
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += c
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


def ics_vevent(ev):
    d = next_date(ev)
    if "rule" in ev:
        r = ev["rule"]
        day = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"][r["wd"]]
        rrule = f'RRULE:FREQ=YEARLY;BYMONTH={r["m"]};BYDAY={r["n"]}{day}'
    else:
        rrule = "RRULE:FREQ=YEARLY"
    stamp = dt.datetime.combine(UPDATED, dt.time()).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VEVENT", f'UID:{ev["id"]}@calendariodeflores.com', f"DTSTAMP:{stamp}",
             f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}", rrule,
             f'SUMMARY:{ics_escape("🌷 " + ev["name"] + ": " + ev["flower"])}',
             f'DESCRIPTION:{ics_escape(ev["story"] + " Dónde: " + ev["region"] + ". Guía: " + page_url(ev["guia"]))}',
             f'URL:{page_url(ev["guia"])}', "TRANSP:TRANSPARENT",
             "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:-P3D",
             f'DESCRIPTION:{ics_escape("En 3 días: " + ev["name"] + ". Encarga " + ev["flower"].lower() + ".")}',
             "END:VALARM", "END:VEVENT"]
    return lines


def ics_calendar(evs, name):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Florario//Calendario de flores//ES", "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH", f"X-WR-CALNAME:{ics_escape(name)}", "X-WR-TIMEZONE:Europe/Madrid",
             "REFRESH-INTERVAL;VALUE=DURATION:P7D", "X-PUBLISHED-TTL:P7D"]
    for ev in evs:
        lines += ics_vevent(ev)
    lines.append("END:VCALENDAR")
    return "\r\n".join(ics_fold(l) for l in lines) + "\r\n"


def render_ics():
    write("descargas/calendario-de-flores.ics", ics_calendar(EVENTS, "Florario – Calendario de flores"))
    for ev in EVENTS:
        write(f'recordatorios/{ev["id"]}.ics', ics_calendar([ev], f'Florario · {ev["name"]}'))


# ---------------------------------------------------------------- PDF
def pdf_wheel(y):
    """Rueda del año en SVG para la portada del PDF: meses de color, marcas de días y una flor por fecha."""
    import math
    total = 366 if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0 else 365

    def doy(d):
        return (d - dt.date(y, 1, 1)).days

    def polar(r, deg):
        a = math.radians(deg - 90)
        return r * math.cos(a), r * math.sin(a)

    def arc(r1, r2, a0, a1):
        large = 1 if a1 - a0 > 180 else 0
        p = lambda r, a: "%.2f %.2f" % polar(r, a)
        return f"M{p(r2, a0)} A{r2} {r2} 0 {large} 1 {p(r2, a1)} L{p(r1, a1)} A{r1} {r1} 0 {large} 0 {p(r1, a0)}Z"

    out = []
    for m in range(12):
        a0 = doy(dt.date(y, m + 1, 1)) / total * 360 + .7
        a1 = (total if m == 11 else doy(dt.date(y, m + 2, 1))) / total * 360 - .7
        out.append(f'<path d="{arc(56, 76, a0, a1)}" fill="{MONTH_COLORS[m]}" fill-opacity=".38" '
                   f'stroke="{MONTH_COLORS[m]}" stroke-width=".6"/>')
        x, yy = polar(66, (a0 + a1) / 2)
        out.append(f'<text class="wm" x="{x:.1f}" y="{yy:.1f}">{MONTH_SHORT[m].upper()}</text>')
    out.append('<circle r="81" fill="none" stroke="#DCDDD0" stroke-width=".6"/>')
    for i in range(total):
        d = dt.date(y, 1, 1) + dt.timedelta(days=i)
        big = d.day == 1
        x1, y1 = polar(81 - (3 if big else 0), (i + .5) / total * 360)
        x2, y2 = polar(81 + (3 if big else 1.8), (i + .5) / total * 360)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1B2118" '
                   f'stroke-opacity="{.7 if big else .25}" stroke-width="{.6 if big else .35}"/>')
    # Flores: se apilan en otro anillo si caen a menos de 5 días de otra (igual que la rueda de la web)
    rings, last = [91, 100, 109, 118], [-99, -99, -99, -99]
    stems, flowers = [], []
    for e in sorted(EVENTS, key=lambda e: date_for(e, y)):
        i = doy(date_for(e, y))
        k = next((n for n, l in enumerate(last) if i - l >= 4), len(rings) - 1)
        last[k] = i
        ang = (i + .5) / total * 360
        sx, sy = polar(84, ang)
        ex, ey = polar(rings[k] - 3.2, ang)
        stems.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#2F6B45" stroke-width=".7"/>')
        fx, fy = polar(rings[k], ang)
        flowers.append(f'<g transform="translate({fx:.1f} {fy:.1f})">{petals(COLORS[e["color"]]["hex"], 6.4, e.get("petals", 6))}</g>')
    out += stems + flowers
    out.append(f'<text class="wy" y="6">{y}</text><text class="ws" y="20">{len(EVENTS)} FECHAS CON FLORES</text>')
    return f'<svg class="wheel" viewBox="-124 -124 248 248" aria-hidden="true">{"".join(out)}</svg>'


def render_pdf_html(y):
    months = []
    for m in range(12):
        evs = [e for e in events_sorted(EVENTS, y) if date_for(e, y).month == m + 1]
        items = "".join(
            f'<li style="--dc:{color_hex(e["color"])}"><b>{date_for(e, y).day}</b>'
            f'<span><strong>{esc(e["name"])}</strong> · {esc(e["flower"])}<small>{esc(e["region"].split(" · ")[0])}</small></span></li>'
            for e in evs) or '<li class="empty"><span>Sin fechas: flores para ti</span></li>'
        ill = bloom(MONTH_COLORS[m], [6, 8, 10, 12][m % 4], "mo-bloom")
        months.append(f'<section class="mo" style="--mc:{MONTH_COLORS[m]}"><h2>{ill}{MONTHS[m].capitalize()}</h2><ul>{items}</ul></section>')
    season_rows = "".join(
        f'<tr style="--mc:{MONTH_COLORS[m]}"><th>{MONTHS[m].capitalize()}</th>'
        + "".join(f'<td>{", ".join(SEASON[m][k])}</td>' for k, _ in SEASON_REGIONS) + "</tr>" for m in range(12))
    heads = "".join(f"<th>{label}</th>" for _, label in SEASON_REGIONS)
    st = stats()
    # Las fuentes se cargan de /fuentes/ con una ruta relativa desde _build/salida/
    fonts = os.path.relpath(os.path.join(ROOT, "fuentes"), os.path.join(BUILD, "salida")).replace(os.sep, "/")
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Calendario de flores {y} · Florario</title>
<style>
@font-face {{ font-family: "Bricolage Grotesque"; font-weight: 400 800; src: url("{fonts}/bricolage-grotesque-latin.woff2") format("woff2"); }}
@font-face {{ font-family: "DM Mono"; font-weight: 400; src: url("{fonts}/dm-mono-400-latin.woff2") format("woff2"); }}
@font-face {{ font-family: "DM Mono"; font-weight: 500; src: url("{fonts}/dm-mono-500-latin.woff2") format("woff2"); }}
@page {{ size: A4; margin: 9mm 10mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: "Bricolage Grotesque", system-ui, sans-serif; color: #1B2118; font-size: 7.9pt; line-height: 1.22; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
/* En pantalla (vista previa JPG): una hoja A4 con los mismos márgenes que al imprimir */
@media screen {{ html {{ background: #fff; }} body {{ width: 210mm; padding: 9mm 10mm; }} .cover {{ margin-bottom: 14mm; }} }}
.petal {{ stroke: #1B2118; stroke-opacity: .45; stroke-width: .35; }}
.pistil {{ fill: #2A2F25; }}
.cover {{ height: 276mm; display: flex; flex-direction: column; break-after: page; }}
.cover-top {{ display: flex; justify-content: space-between; align-items: center; font-family: "DM Mono", monospace; font-size: 9pt; letter-spacing: .08em; text-transform: uppercase; color: #525A4D; }}
.cover-top span {{ display: inline-flex; align-items: center; gap: 2mm; }}
.cover-top svg {{ width: 8mm; height: 8mm; }}
.cover h1 {{ margin: 12mm 0 0; font-size: 44pt; line-height: .95; letter-spacing: -.035em; font-weight: 800; }}
.cover h1 span {{ display: block; font-size: 78pt; letter-spacing: -.04em; }}
.cover h1 span::after {{ content: ""; display: block; width: 62mm; height: 4mm; margin-top: 2mm; border-radius: 2mm; background: linear-gradient(90deg, #E8475F, #F28C1B 25%, #F2C230 45%, #2BB3A3 65%, #3F72E0 82%, #8A4FD8); }}
.cover .sub {{ margin: 5mm 0 0; max-width: 150mm; font-size: 13pt; line-height: 1.3; color: #353B31; }}
.wheel {{ display: block; width: 150mm; height: 150mm; margin: auto; }}
.wheel .wm {{ font-family: "DM Mono", monospace; font-size: 6.4px; letter-spacing: .06em; fill: #1B2118; text-anchor: middle; dominant-baseline: middle; }}
.wheel .wy {{ font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; font-size: 26px; fill: #1B2118; text-anchor: middle; }}
.wheel .ws {{ font-family: "DM Mono", monospace; font-size: 5.2px; letter-spacing: .08em; fill: #525A4D; text-anchor: middle; }}
.inside {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin: 0; padding: 0; list-style: none; }}
.inside li {{ border-top: 1.5px solid #1B2118; padding-top: 2mm; font-size: 9pt; color: #353B31; }}
.inside b {{ display: block; font-size: 11pt; color: #1B2118; }}
.cover-foot {{ margin-top: 5mm; display: flex; justify-content: space-between; font-family: "DM Mono", monospace; font-size: 7.5pt; color: #525A4D; }}
header {{ display: flex; justify-content: space-between; align-items: end; margin-bottom: 3.5mm; padding-bottom: 2.5mm; border-bottom: 1.5px solid #1B2118; }}
header h1 {{ margin: 0; font-size: 22pt; line-height: 1; letter-spacing: -.03em; }}
h1 em {{ font-style: normal; color: #B98700; }}
header p {{ margin: 2mm 0 0; color: #525A4D; }}
.brand {{ text-align: right; font-family: "DM Mono", monospace; font-size: 8pt; color: #525A4D; }}
.brand svg {{ width: 12mm; height: 12mm; }}
.grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5mm; }}
.mo {{ border: 1px solid #DCDDD0; border-top: 4px solid var(--mc); border-radius: 3mm; padding: 2mm 2.6mm; break-inside: avoid; }}
.mo h2 {{ display: flex; align-items: center; gap: 1.6mm; margin: 0 0 1.2mm; font-size: 11pt; letter-spacing: -.02em; }}
.mo-bloom {{ width: 5mm; height: 5mm; flex: none; }}
.mo ul {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 1.1mm; }}
.mo li {{ display: grid; grid-template-columns: 7mm 1fr; gap: 1.5mm; align-items: start; }}
.mo li b {{ font-family: "DM Mono", monospace; font-weight: 500; font-size: 10pt; text-align: center; border-radius: 1.5mm; background: color-mix(in srgb, var(--dc) 30%, #fff); padding: .4mm 0; }}
.mo li small {{ display: block; color: #525A4D; font-size: 6.6pt; }}
.mo li.empty {{ display: block; color: #525A4D; font-style: italic; }}
.page2 {{ break-before: page; }}
h3 {{ margin: 0 0 3mm; font-size: 16pt; letter-spacing: -.02em; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8.4pt; }}
th, td {{ text-align: left; vertical-align: top; padding: 2mm 2.4mm; border-bottom: 1px solid #DCDDD0; }}
thead th {{ font-family: "DM Mono", monospace; font-weight: 500; font-size: 7pt; text-transform: uppercase; letter-spacing: .06em; color: #525A4D; }}
tbody th {{ border-left: 4px solid var(--mc); white-space: nowrap; }}
.note {{ margin-top: 3mm; color: #525A4D; font-size: 7.8pt; }}
.legend {{ margin-top: 6mm; display: grid; grid-template-columns: repeat(2, 1fr); gap: 3mm; }}
.box {{ border: 1px solid #DCDDD0; border-radius: 3mm; padding: 3mm; }}
.box b {{ display: block; font-size: 10pt; margin-bottom: 1mm; }}
footer {{ margin-top: 3mm; font-family: "DM Mono", monospace; font-size: 7.5pt; color: #525A4D; display: flex; justify-content: space-between; }}
</style></head><body>
<section class="cover">
<div class="cover-top"><span>{bloom("#F2C230", 10)}Florario</span><span>calendariodeflores.com</span></div>
<h1>Calendario de flores <span>{y}</span></h1>
<p class="sub">Qué flor regalar en cada fecha del año en España y Latinoamérica, con las fechas móviles ya calculadas para {y}.</p>
{pdf_wheel(y)}
<ul class="inside">
<li><b>{st["n_events"]} fechas</b>De San Valentín y Sant Jordi a los trends de flores amarillas, azules y moradas.</li>
<li><b>12 meses</b>Qué se regala cada mes, dónde y la flor que toca.</li>
<li><b>Flores de temporada</b>En España, en México y Centroamérica y en el Cono Sur.</li>
</ul>
<div class="cover-foot"><span>Gratis para uso personal · © Florario · calendariodeflores.com</span><span>A4 · 3 páginas</span></div>
</section>
<header><div><h1>Calendario de flores <em>{y}</em></h1><p>Qué flor regalar en cada fecha del año en España y Latinoamérica · Las fechas móviles ya están calculadas para {y}.</p></div>
<div class="brand">{bloom("#F2C230", 10)}<br>Florario<br>calendariodeflores.com</div></header>
<div class="grid">{"".join(months)}</div>
<footer><span>Florario – Calendario de flores · www.calendariodeflores.com</span><span>Guías de cada fecha, fotos y cuenta atrás en la web</span></footer>
<div class="page2">
<h3>Flores de temporada mes a mes</h3>
<table><thead><tr><th>Mes</th>{heads}</tr></thead><tbody>{season_rows}</tbody></table>
<p class="note">{SEASON_NOTE} Tabla orientativa: la temporada cambia con la zona y los invernaderos alargan casi todas.</p>
<div class="legend">
<div class="box"><b>Por colores</b>Amarillo: alegría y amistad (21 sep, 21 mar) · Rojo: amor (14 feb, Sant Jordi) · Rosa: cariño (Día de la Madre) · Azul: lealtad (3 oct, 19 nov) · Morado: admiración (9 nov) · Blanco: paz y recuerdo (1 nov).</div>
<div class="box"><b>Recuérdamelo</b>Suscríbete al calendario en calendariodeflores.com/#recuerdamelo y tu móvil te avisará 3 días antes de cada fecha.</div>
</div>
<footer><span>© {UPDATED.year} Florario – Calendario de flores</span><span>www.calendariodeflores.com</span></footer>
</div>
</body></html>'''


def find_browser():
    for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              shutil.which("google-chrome") or "", shutil.which("chromium") or ""]:
        if p and os.path.exists(p):
            return p
    return None


def render_pdfs(print_pdf):
    for y in (YEAR, YEAR + 1):
        src = os.path.join(BUILD, "salida", f"pdf-{y}.html")
        os.makedirs(os.path.dirname(src), exist_ok=True)
        with open(src, "w", encoding="utf-8") as f:
            f.write(render_pdf_html(y))
        if print_pdf:
            browser = find_browser()
            if not browser:
                WARN.append("No encontré Chrome ni Edge: los PDF no se han regenerado.")
                return
            out = os.path.join(ROOT, "descargas", f"calendario-de-flores-{y}.pdf")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--virtual-time-budget=8000", f"--print-to-pdf={out}", "file:///" + src.replace("\\", "/")],
                           check=True, capture_output=True)
            pages = len(re.findall(rb"/Type\s*/Page[^s]", open(out, "rb").read()))
            if pages > 3:
                WARN.append(f"El PDF de {y} tiene {pages} páginas (máximo 3).")
            render_preview(browser, src, y)


# Vista previa de la portada: 794 × 1123 px CSS (A4 a 96 ppp) × 1,5 = unos 1190 px de ancho.
PREVIEW_CSS = (794, 1123)
PREVIEW_SCALE = 1.5
PREVIEW_W, PREVIEW_H = (-int(-c * PREVIEW_SCALE // 1) for c in PREVIEW_CSS)  # redondeo hacia arriba, como el navegador


def render_preview(browser, src, y, max_kb=250):
    """JPG de la primera página del PDF: captura PNG con el navegador y la pasa a JPEG con un
    <canvas> en el propio navegador (así no hace falta ninguna librería de imágenes)."""
    import base64
    tmp = os.path.join(BUILD, "salida")
    png = os.path.join(tmp, f"portada-{y}.png")
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={PREVIEW_CSS[0]},{PREVIEW_CSS[1]}", f"--force-device-scale-factor={PREVIEW_SCALE}",
                    "--virtual-time-budget=8000", f"--screenshot={png}", "file:///" + src.replace("\\", "/")],
                   check=True, capture_output=True)
    out = os.path.join(ROOT, "descargas", f"calendario-de-flores-{y}.jpg")
    for q in (.82, .74, .66, .58):
        conv = os.path.join(tmp, "a-jpeg.html")
        with open(conv, "w", encoding="utf-8") as f:
            f.write(f'''<!doctype html><body><script>
const img = new Image();
img.onload = () => {{
  const c = document.createElement("canvas");
  c.width = img.naturalWidth; c.height = img.naturalHeight;
  const x = c.getContext("2d");
  x.fillStyle = "#fff"; x.fillRect(0, 0, c.width, c.height); x.drawImage(img, 0, 0);
  document.body.textContent = "JPEG:" + c.toDataURL("image/jpeg", {q}) + ":" + c.width + "x" + c.height;
}};
img.src = "portada-{y}.png";
</script></body>''')
        res = subprocess.run([browser, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                              "--virtual-time-budget=8000", "--dump-dom", "file:///" + conv.replace("\\", "/")],
                             capture_output=True, text=True)
        m = re.search(r"JPEG:data:image/jpeg;base64,([A-Za-z0-9+/=]+):(\d+)x(\d+)", res.stdout)
        if not m:
            WARN.append(f"No se pudo generar la vista previa JPG de {y}.")
            return
        data = base64.b64decode(m.group(1))
        if (int(m.group(2)), int(m.group(3))) != (PREVIEW_W, PREVIEW_H):
            WARN.append(f"La vista previa de {y} mide {m.group(2)}×{m.group(3)} y no {PREVIEW_W}×{PREVIEW_H}.")
        if len(data) <= max_kb * 1024:
            break
    with open(out, "wb") as f:
        f.write(data)
    if len(data) > max_kb * 1024:
        WARN.append(f"La vista previa de {y} pesa {len(data) // 1024} KB (más de {max_kb}).")


# ---------------------------------------------------------------- widget
def render_widget():
    """/widget/: página mínima para insertar en un <iframe> (noindex, sin dependencias, fuera del sitemap).
    Muestra la próxima fecha y su cuenta atrás. ?pais=mx (o es, ar, co, cl, pe) filtra por país."""
    data = [{"n": e["name"], "f": e["flower"], "c": color_hex(e["color"]), "p": e["paises"],
             **({"r": [e["rule"]["m"], e["rule"]["wd"], e["rule"]["n"]]} if "rule" in e else {"m": e["m"], "d": e["d"]})}
            for e in EVENTS]
    first = min(EVENTS, key=next_date)
    d = next_date(first)
    page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Próxima fecha para regalar flores · Florario</title>
<link rel="canonical" href="{URL}/">
<style>
  :root {{ --ink: #1B2118; --muted: #525A4D; --bg: #FFFFFF; --line: #DCDDD0; --c: {color_hex(first["color"])}; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --ink: #ECF0E6; --muted: #A2AA9B; --bg: #181C16; --line: #2C3229; }} }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; height: 100%; }}
  body {{ font: 15px/1.35 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: var(--ink); background: var(--bg); }}
  .w {{ height: 100%; display: grid; grid-template-rows: auto 1fr auto; gap: 6px; padding: 14px 16px; border: 1px solid var(--line);
        border-radius: 16px; border-top: 5px solid var(--c); background: color-mix(in srgb, var(--c) 10%, var(--bg)); }}
  .k {{ margin: 0; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
  .m {{ display: grid; grid-template-columns: auto 1fr; gap: 2px 12px; align-items: center; align-content: center; }}
  .n {{ grid-row: span 2; font-size: 44px; font-weight: 800; line-height: 1; letter-spacing: -.03em; font-variant-numeric: tabular-nums; }}
  .t {{ font-weight: 700; font-size: 17px; line-height: 1.2; }}
  .f {{ font-size: 13px; color: var(--muted); }}
  a {{ color: var(--ink); font-size: 13px; font-weight: 600; text-underline-offset: 3px; text-decoration-color: var(--c); text-decoration-thickness: 2px; }}
</style>
</head>
<body>
<div class="w">
  <p class="k" id="k">{d.day} de {MONTHS[d.month - 1]}</p>
  <div class="m"><span class="n" id="n">{(d - HOY).days}</span><span class="t" id="t">{esc(first["name"])}</span><span class="f" id="f">{esc(first["flower"])}</span></div>
  <a href="{URL}/" target="_blank" rel="noopener">Calendario de flores · Florario</a>
</div>
<script>
(() => {{
  const EV = {json.dumps(data, ensure_ascii=False, separators=(",", ":"))};
  const M = {json.dumps(MONTHS, ensure_ascii=False)};
  const pais = (new URLSearchParams(location.search).get("pais") || "").toUpperCase();
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const nth = (y, m, wd, n) => {{ const f = new Date(y, m - 1, 1); return new Date(y, m - 1, 1 + (wd - f.getDay() + 7) % 7 + (n - 1) * 7); }};
  const at = (e, y) => e.r ? nth(y, e.r[0], e.r[1], e.r[2]) : new Date(y, e.m - 1, e.d);
  let best = null;
  for (const e of EV) {{
    if (pais && !e.p.includes(pais)) continue;
    for (const y of [today.getFullYear(), today.getFullYear() + 1]) {{
      const d = at(e, y), n = Math.round((d - today) / 864e5);
      if (n >= 0 && (!best || n < best.n)) best = {{ e, d, n }};
    }}
  }}
  if (!best) return;
  document.documentElement.style.setProperty("--c", best.e.c);
  document.getElementById("k").textContent = `${{best.d.getDate()}} de ${{M[best.d.getMonth()]}} · ${{best.n === 0 ? "es hoy" : best.n === 1 ? "falta 1 día" : `faltan ${{best.n}} días`}}`;
  document.getElementById("n").textContent = best.n === 0 ? "¡Hoy!" : best.n;
  document.getElementById("t").textContent = best.e.n;
  document.getElementById("f").textContent = best.e.f;
}})();
</script>
</body>
</html>
'''
    write("widget/index.html", page)
    kb = len(page.encode("utf-8")) / 1024
    if kb > 15:
        WARN.append(f"/widget/ pesa {kb:.1f} KB (máximo 15).")


# ---------------------------------------------------------------- sitemap
def render_sitemap(pages):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p in pages:
        loc = page_url(p["slug"])
        img = ""
        src = p.get("img_url") or (jpg_url(p["img"]) if p.get("img") else "")
        if src:
            img = f'\n    <image:image><image:loc>{src}</image:loc></image:image>'
        out.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{p['updated'].isoformat()}</lastmod>{img}\n  </url>")
    out.append("</urlset>")
    write("sitemap.xml", "\n".join(out) + "\n")


# ---------------------------------------------------------------- comprobaciones
def check_site(pages):
    problems = []
    for p in pages:
        rel = os.path.join(ROOT, p["slug"], "index.html") if p["slug"] else os.path.join(ROOT, "index.html")
        h = open(rel, encoding="utf-8").read()
        if h.count("<h1") != 1:
            problems.append(f'{p["slug"] or "/"}: {h.count("<h1")} h1')
        for m in re.finditer(r'<img\b[^>]*>', h):
            if 'alt="' not in m.group(0):
                problems.append(f'{p["slug"]}: img sin alt')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                json.loads(block)
            except ValueError as e:
                problems.append(f'{p["slug"]}: JSON-LD inválido ({e})')
        ids = set(re.findall(r'\bid="([^"]+)"', h))
        for href in re.findall(r'href="(/[^"]*)"', h):
            path, _, frag = href.partition("#")
            if path.startswith("//") or "${" in path:
                continue
            target = os.path.join(ROOT, path.lstrip("/"))
            if path.endswith("/"):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                problems.append(f'{p["slug"] or "/"}: enlace roto {href}')
            elif frag and path == "/" + (p["slug"] + "/" if p["slug"] else ""):
                if frag not in ids:
                    problems.append(f'{p["slug"] or "/"}: ancla rota #{frag}')
            elif frag and path.endswith("/"):
                other = open(target, encoding="utf-8").read()
                ev_ids = {e["id"] for e in EVENTS}
                if f'id="{frag}"' not in other and not (path == "/" and frag in ev_ids):
                    problems.append(f'{p["slug"] or "/"}: ancla rota {href}')
    return problems


# ---------------------------------------------------------------- main
def main():
    global UPDATED, N_PAGES
    print_pdf = "--pdf" in sys.argv
    frag_dir = os.path.join(BUILD, "paginas")
    frags = [read_fragment(os.path.join(frag_dir, n)) for n in sorted(os.listdir(frag_dir)) if n.endswith(".html")]
    # La última revisión del sitio es la de la página más reciente (portada, pie, .ics)
    UPDATED = max([PUBLISHED] + [m["updated"] for m, _ in frags])
    N_PAGES = len(frags) + 5  # + portada y los 4 índices
    stale_dates(frags)

    pages = [render_home()]
    for meta, body in frags:
        pages.append(render_article(meta, body))
    by_type = lambda t: max([p["updated"] for p in pages if p["tipo"] == t] or [UPDATED])
    pages.append(render_hub("meses", "Flores por mes: qué regalar y qué está de temporada",
                            "Qué flores regalar cada mes del año y cuáles están de temporada en España, México y el Cono Sur, con todas las fechas para regalar flores de enero a diciembre.",
                            "Flores <em>por mes</em>", "Calendario de flores · por mes",
                            "Elige un mes para ver sus fechas para regalar flores, qué flores están de temporada en cada región y consejos para ese momento del año.",
                            MONTHS, "meses",
                            "<p>Cada mes tiene su página con las fechas del calendario, las flores de temporada en España, México y Centroamérica y en Argentina, Chile y Uruguay, y preguntas frecuentes. Si prefieres verlo todo junto, tienes la <a href=\"/#temporada\">tabla de flores de temporada</a> y el <a href=\"/#fechas\">calendario completo</a> en la portada, además del <a href=\"/calendario-de-flores-para-imprimir/\">calendario para imprimir</a>.</p>"
                            "<p>Las estaciones van al revés a cada lado del ecuador: en marzo, mientras en España empiezan los tulipanes, en Argentina y Chile llegan las dalias y los crisantemos del otoño. Por eso cada mes separa las flores de temporada por región. Y en Colombia y Ecuador, con clima de montaña todo el año, casi todas las flores de corte se encuentran en cualquier mes.</p>",
                            "ramo-tulipanes", by_type("mes")))
    pages.append(render_hub("flores", "Flores: significado, temporada y cuándo regalarlas",
                            "Guía de flores para regalar: rosa, girasol, tulipán, peonía, clavel, crisantemo, cempasúchil, violeta y más, con su significado, su temporada y las fechas en que se regalan.",
                            "Qué significa <em>cada flor</em>", "Calendario de flores · por flor",
                            "Cada flor tiene su página con su significado, sus colores, en qué meses está de temporada, las fechas del año en que se regala y cómo hacer que dure más en el jarrón.",
                            [f["slug"] for f in FLOWERS], "flores",
                            "<p>¿Buscas por color en lugar de por flor? Mira el <a href=\"/significado-colores-flores/\">significado de los colores de las flores</a>. Y si lo que necesitas es una fecha concreta, todas están en el <a href=\"/#fechas\">calendario de flores</a>.</p>"
                            "<p>Una misma flor puede decir cosas distintas según el país y el color: el crisantemo es la flor de Todos los Santos en España, pero en otros lugares se regala sin ese sentido; la rosa roja es amor en San Valentín y en Sant Jordi, y la amarilla, amistad. Cada página explica esos matices y recoge las fechas del calendario en las que esa flor es la protagonista.</p>",
                            "ramo-silvestre", by_type("flor")))
    pages.append(render_hub("guias", "Guías para regalar flores en cada fecha y ocasión",
                            "Guías de Florario: flores amarillas, azules y moradas, San Valentín, Día de la Madre, Día del Padre, 8M, Día del Maestro, cumpleaños, aniversarios, condolencias y más.",
                            "Guías para <em>regalar flores</em>", "Calendario de flores · guías",
                            "El origen de cada fecha y de cada trend, qué flores regalar, qué significa cada color y cómo acertar en ocasiones sin fecha fija, como cumpleaños, aniversarios o condolencias.",
                            [g["slug"] for g in GUIDES], "guias",
                            "<p>Las guías se revisan antes de cada fecha. Si echas en falta una tradición de tu país, <a href=\"/contacto/\">cuéntanosla</a>.</p>"
                            "<p>Cada guía cuenta de dónde viene la fecha (una canción, una leyenda, una ley o un hashtag), en qué países se celebra, qué flores se regalan y cuáles son una buena alternativa si no encuentras las típicas. Al pie de cada una están las fuentes consultadas: al menos dos medios de países distintos para cada trend.</p>",
                            "ramo-rosas", by_type("guia")))
    pages.append(render_hub("paises", "Fechas para regalar flores por país",
                            "Qué fechas para regalar flores se celebran en España, México, Argentina, Colombia, Chile y Perú: Día de la Madre, Día del Padre, trends de flores y más, con la fecha de cada país.",
                            "Fechas para regalar flores <em>por país</em>", "Calendario de flores · por país",
                            "El Día de la Madre, el Día del Padre y los trends de flores no caen el mismo día en todos los países. Elige el tuyo para ver solo sus fechas, calculadas para este año y el siguiente.",
                            [c["slug"] for c in COUNTRIES.values()], "paises",
                            "<p>Algunas fechas son de todos, como San Valentín o las flores amarillas del 21 de septiembre, y otras solo tienen sentido en un país: Sant Jordi en Cataluña, el Día de Muertos y la Virgen de Guadalupe en México o Amor y Amistad en Colombia. El Día de la Madre es el mejor ejemplo: primer domingo de mayo en España, 10 de mayo en México, segundo domingo de mayo en Colombia, Chile y Perú y tercer domingo de octubre en Argentina.</p>"
                            "<p>Si tu país no está en la lista, el <a href=\"/#fechas\">calendario completo</a> incluye también las fechas de Brasil, Francia, India o Corea del Sur que se han hecho conocidas en redes.</p>",
                            "ramo-silvestre", by_type("pais")))
    render_widget()
    render_ics()
    render_pdfs(print_pdf)
    render_sitemap(pages)

    problems = check_site(pages)
    thin = [f'{p["slug"]} ({p["words"]})' for p in pages if p["tipo"] in ("flor", "mes") and p["words"] < 600]
    print(f"{len(pages)} páginas generadas (fecha del build: {HOY}; año de la portada: {YEAR_LABEL}).")
    for p in pages:
        print(f'  {p["tipo"]:8} {p["words"]:5} palabras  /{p["slug"]}{"/" if p["slug"] else ""}')
    if thin:
        print("Páginas de flor o mes por debajo de 600 palabras:", ", ".join(thin))
    for w in WARN:
        print("AVISO:", w)
    missing = []
    for k, v in SITE.items():
        if isinstance(v, dict):
            missing += [f"{k}.{kk}" for kk, vv in v.items() if pending(vv)]
        elif pending(v):
            missing.append(k)
    if missing:
        print("AVISO: faltan datos en SITE (datos.py):", ", ".join(missing))
    if problems:
        print("PROBLEMAS:")
        for pr in problems:
            print("  -", pr)
        sys.exit(1)


if __name__ == "__main__":
    main()
