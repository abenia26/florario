"""Generador estático de Florario.

Uso:  python _build/build.py          (genera páginas, portada, sitemap, .ics y HTML de los PDF)
      python _build/build.py --pdf    (además imprime los PDF con Chrome o Edge sin interfaz)

Lee los datos de _build/datos.py, los textos de _build/paginas/*.html y la plantilla de la
portada _build/plantilla-inicio.html. Todo lo que genera va a la raíz del proyecto, que es
lo que publica Vercel. No necesita dependencias fuera de la biblioteca estándar.

Idiomas: la web se genera dos veces, en español en / y en inglés en /en/. La versión inglesa
lee las traducciones de _build/datos_en.py y los textos de _build/paginas/en/*.html. Los textos
fijos del código van en pares T("español", "english").
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
import datos
import datos_en
from datos import SITE, MONTH_COLORS

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
LOCALE = {c["slug"]: c["hreflang"].replace("-", "_") for c in datos.COUNTRIES.values()}
HUB_CARDS_ES = {
    "meses": ("Calendario", "Flores por mes", "Qué regalar y qué hay de temporada cada mes", "ramo-tulipanes", "rosa"),
    "flores": ("Calendario", "Flores de la A a la Z", "Significado y temporada de cada flor", "ramo-silvestre", "amarillo"),
    "guias": ("Calendario", "Todas las guías", "Fechas y ocasiones para regalar flores", "ramo-rosas", "rojo"),
    "paises": ("Calendario", "Fechas por país", "España, México, Argentina, Colombia, Chile y Perú", "ramo-silvestre", "rosa"),
}
WARN = []


# ---------------------------------------------------------------- idiomas
LANGS = ("es", "en")
SLUG_EN = datos_en.SLUGS                          # slug español -> slug inglés
SLUG_ES = {v: k for k, v in SLUG_EN.items()}      # slug inglés -> slug español
LANG, PREFIX = "es", ""


def localized(lang):
    """Datos del idioma lang: los de datos.py, con los textos y slugs de datos_en.py si es inglés."""
    if lang == "es":
        return {"COLORS": datos.COLORS, "TYPES": datos.TYPES, "MONTHS": datos.MONTHS, "MONTH_SHORT": datos.MONTH_SHORT,
                "WEEKDAYS": datos.WEEKDAYS, "IMAGES": datos.IMAGES, "COUNTRIES": datos.COUNTRIES, "EVENTS": datos.EVENTS,
                "SEASON": datos.SEASON, "SEASON_REGIONS": datos.SEASON_REGIONS, "SEASON_NOTE": datos.SEASON_NOTE,
                "FLOWERS": datos.FLOWERS, "GUIDES": datos.GUIDES, "HUB_CARDS": HUB_CARDS_ES, "AUTHOR_BIO": SITE["author_bio"]}
    en = datos_en
    events = []
    for e in datos.EVENTS:
        ev = {**e, **en.EVENTS[e["id"]], "guia": SLUG_EN[e["guia"]]}
        if "song" in e:
            ev["song"] = en.SONGS[e["id"]]
        events.append(ev)
    return {
        "COLORS": {k: {**v, "label": en.COLORS[k]} for k, v in datos.COLORS.items()},
        "TYPES": en.TYPES, "MONTHS": en.MONTHS, "MONTH_SHORT": en.MONTH_SHORT, "WEEKDAYS": en.WEEKDAYS,
        "IMAGES": {k: {**v, **en.IMAGES[k]} for k, v in datos.IMAGES.items()},
        "COUNTRIES": {code: {**c, "slug": SLUG_EN[c["slug"]], "name": en.COUNTRIES[code]["name"],
                             "de": en.COUNTRIES[code]["in"], "en": en.COUNTRIES[code]["in"]}
                      for code, c in datos.COUNTRIES.items()},
        "EVENTS": events,
        "SEASON": en.SEASON, "SEASON_REGIONS": [(k, en.SEASON_REGIONS[k]) for k, _ in datos.SEASON_REGIONS],
        "SEASON_NOTE": en.SEASON_NOTE,
        "FLOWERS": [{**f, "slug": SLUG_EN[f["slug"]], **en.FLOWERS[f["slug"]]} for f in datos.FLOWERS],
        "GUIDES": [{**g, "slug": SLUG_EN[g["slug"]], **en.GUIDES[g["slug"]]} for g in datos.GUIDES],
        "HUB_CARDS": {SLUG_EN[k]: en.HUB_CARDS[k] + v[3:] for k, v in HUB_CARDS_ES.items()},
        "AUTHOR_BIO": en.SITE["author_bio"],
    }


def set_lang(lang):
    """Cambia el idioma con el que se generan las páginas: los datos globales pasan a ese idioma."""
    global LANG, PREFIX, COLORS, TYPES, MONTHS, MONTH_SHORT, WEEKDAYS, IMAGES, COUNTRIES, EVENTS, SEASON, \
        SEASON_REGIONS, SEASON_NOTE, FLOWERS, GUIDES, HUB_CARDS, AUTHOR_BIO, EV, GUIDE, FLOWER, COUNTRY_BY_SLUG
    LANG, PREFIX = lang, ("" if lang == "es" else f"{lang}/")
    d = localized(lang)
    COLORS, TYPES, MONTHS, MONTH_SHORT, WEEKDAYS = d["COLORS"], d["TYPES"], d["MONTHS"], d["MONTH_SHORT"], d["WEEKDAYS"]
    IMAGES, COUNTRIES, EVENTS, SEASON = d["IMAGES"], d["COUNTRIES"], d["EVENTS"], d["SEASON"]
    SEASON_REGIONS, SEASON_NOTE, FLOWERS, GUIDES = d["SEASON_REGIONS"], d["SEASON_NOTE"], d["FLOWERS"], d["GUIDES"]
    HUB_CARDS, AUTHOR_BIO = d["HUB_CARDS"], d["AUTHOR_BIO"]
    EV = {e["id"]: e for e in EVENTS}
    GUIDE = {g["slug"]: g for g in GUIDES}
    FLOWER = {f["slug"]: f for f in FLOWERS}
    COUNTRY_BY_SLUG = {c["slug"]: (code, c) for code, c in COUNTRIES.items()}


def T(es, en):
    """Texto fijo en el idioma que se está generando."""
    return en if LANG == "en" else es


def href(slug):
    """Ruta de una página del idioma actual ("" = portada): /rosa/ o /en/rose/."""
    return f"/{PREFIX}{slug}/" if slug else f"/{PREFIX}"


def other_lang():
    return "en" if LANG == "es" else "es"


def es_slug(slug):
    """Slug español de una página del idioma actual."""
    return slug if LANG == "es" or not slug else SLUG_ES[slug]


def lang_url(slug, lang):
    """URL de la misma página en otro idioma (slug = el del idioma actual)."""
    s = es_slug(slug)
    if lang == "en":
        s = SLUG_EN[s] if s else ""
        return f"/en/{s}/" if s else "/en/"
    return f"/{s}/" if s else "/"


def month_name(i):
    """Nombre del mes para mostrar: "enero" en español, "January" en inglés."""
    return MONTHS[i].capitalize() if LANG == "en" else MONTHS[i]


set_lang("es")


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
    if "rule" in ev:
        return ev["ruleText"]
    return T(f'{ev["d"]} de {MONTHS[ev["m"] - 1]}', f'{month_name(ev["m"] - 1)} {ev["d"]}')


def fmt(d, year=True, weekday=False):
    """14 de febrero de 2027 · February 14, 2027 (con weekday: sábado 14… · Saturday, February 14…)."""
    if LANG == "en":
        s = f"{month_name(d.month - 1)} {d.day}" + (f", {d.year}" if year else "")
        return f"{WEEKDAYS[d.weekday()]}, {s}" if weekday else s
    s = f"{d.day} de {MONTHS[d.month - 1]}"
    if year:
        s += f" de {d.year}"
    if weekday:
        s = f"{WEEKDAYS[d.weekday()]} {s}"
    return s


def day_month_short(d, year=False):
    """14 feb (2027) · Feb 14 (2027)."""
    s = T(f"{d.day} {MONTH_SHORT[d.month - 1]}", f"{MONTH_SHORT[d.month - 1]} {d.day}")
    return f"{s} {d.year}" if year else s


def time_tag(d, text=None, **kw):
    return f'<time datetime="{d.isoformat()}">{esc(text or fmt(d, **kw))}</time>'


def events_sorted(evs, y=YEAR):
    return sorted(evs, key=lambda e: date_for(e, y))


def full_title(t):
    """Añade la marca solo si el title sigue cabiendo en ~65 caracteres."""
    return f"{t} | Florario" if len(t) + 11 <= 65 else t


def page_url(slug):
    return URL + href(slug)


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
    avif = ", ".join(f'{img_path(key, w, "avif")} {w}w' for w in (480, 640, 960))
    webp = ", ".join(f'{img_path(key, w)} {w}w' for w in (480, 640, 960))
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
def nav_items():
    return [("fechas", href("") + "#fechas", T("Fechas", "Dates")), ("meses", href(T("meses", "months")), T("Por mes", "By month")),
            ("flores", href(T("flores", "flowers")), T("Por flor", "By flower")),
            ("paises", href(T("paises", "countries")), T("Países", "Countries")),
            ("colores", href(T("significado-colores-flores", "flower-color-meanings")), T("Colores", "Colors")),
            ("guias", href(T("guias", "guides")), T("Guías", "Guides"))]


def lang_switch(slug):
    """Selector de idioma de la cabecera: lleva a la misma página en el otro idioma."""
    links = []
    for lang, label, name in (("es", "ES", "Español"), ("en", "EN", "English")):
        cur = ' aria-current="true"' if lang == LANG else ""
        links.append(f'<a href="{lang_url(slug, lang)}" hreflang="{lang}" lang="{lang}" title="{name}"{cur}>{label}</a>')
    return f'<nav class="lang" aria-label="{T("Idioma", "Language")}">{"".join(links)}</nav>'


def header(active=None, slug=""):
    items = "".join(
        f'<li><a href="{url}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for key, url, label in nav_items())
    return f'''<header class="site-head">
    <div class="site-head-in">
      <a class="brand" href="{href("")}">{bloom("#F2C230", 10)}<span><b>Florario</b><small>{T("Calendario de flores", "Flower calendar")}</small></span></a>
      <nav class="site-nav" aria-label="{T("Menú principal", "Main menu")}"><ul>{items}</ul></nav>
      {lang_switch(slug)}
    </div>
  </header>'''


# Descargas: los PDF, sus vistas previas y los .ics tienen nombre propio en cada idioma.
def pdf_href(y, ext="pdf"):
    return T(f"/descargas/calendario-de-flores-{y}.{ext}", f"/en/downloads/flower-calendar-{y}.{ext}")


def ics_href(ev_id=None):
    if ev_id:
        return T(f"/recordatorios/{ev_id}.ics", f"/en/reminders/{ev_id}.ics")
    return T("/descargas/calendario-de-flores.ics", "/en/downloads/flower-calendar.ics")


def footer(current="", fuentes=(), images=()):
    def links(pairs):
        return "".join(
            f'<li><a href="{url}"{" aria-current=\"page\"" if url == current else ""}>{esc(label)}</a></li>'
            for url, label in pairs)
    home = href("")
    meses = [(href(m), month_name(i).capitalize()) for i, m in enumerate(MONTHS)]
    flores = [(href(f["slug"]), f["name"]) for f in FLOWERS]
    guias = [(href(g["slug"]), g["name"]) for g in GUIDES]
    paises = [(href(c["slug"]), c["name"]) for c in COUNTRIES.values()] + [(href(T("paises", "countries")), T("Todos los países", "All countries"))]
    cal = [(home + "#fechas", T("Todas las fechas", "All dates")), (home + "#temporada", T("Flores de temporada", "Seasonal flowers")),
           (href(T("calendario-de-flores-para-imprimir", "printable-flower-calendar")), T("Calendario para imprimir", "Printable calendar")),
           (pdf_href(YEAR), T(f"Calendario {YEAR} en PDF", f"{YEAR} calendar (PDF)")),
           (pdf_href(YEAR + 1), T(f"Calendario {YEAR + 1} en PDF", f"{YEAR + 1} calendar (PDF)")),
           (home + "#recuerdamelo", T("Recuérdamelo (.ics)", "Remind me (.ics)"))]
    florario = [(href(T("sobre-florario", "about")), T("Sobre Florario", "About Florario")), (href(T("contacto", "contact")), T("Contacto", "Contact")),
                (href(T("prensa", "press")), T("Prensa", "Press")),
                (href(T("politica-de-privacidad", "privacy-policy")), T("Política de privacidad", "Privacy policy")),
                (href(T("aviso-legal", "legal-notice")), T("Aviso legal", "Legal notice"))]
    src = ""
    if fuentes:
        src = (f'<div><p class="foot-h">{T("Fuentes consultadas", "Sources (most in Spanish)")}</p><ul class="foot-inline">' + "".join(
            f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{t}</a></li>' for t, u in fuentes) + "</ul></div>")
    cred = ""
    keys = list(dict.fromkeys(images))
    if keys:
        cred = (f'<details><summary>{T("Créditos de las fotos", "Photo credits")} · Wikimedia Commons</summary><ul>'
                + "".join(credit(k) for k in keys) + "</ul></details>")
    return f'''<footer class="site-foot">
    <div class="foot-grid">
      <div class="foot-about">
        <p class="foot-h">Florario – {T("Calendario de flores", "Flower calendar")}</p>
        <p>{T("Todas las fechas del año para regalar flores en España y Latinoamérica: qué flor se regala, dónde y por qué, con flores de temporada y guías por fecha, mes y flor.",
              "Every date of the year for giving flowers in Spain and Latin America: which flower, where and why, with seasonal flowers and guides by date, month and flower.")}</p>
      </div>
      <nav aria-label="{T("Calendario", "Calendar")}"><p class="foot-h">{T("Calendario", "Calendar")}</p><ul>{links(cal)}</ul></nav>
      <nav aria-label="{T("Por mes", "By month")}"><p class="foot-h">{T("Por mes", "By month")}</p><ul>{links(meses)}</ul></nav>
      <nav aria-label="{T("Por flor", "By flower")}"><p class="foot-h">{T("Por flor", "By flower")}</p><ul>{links(flores)}</ul></nav>
      <nav aria-label="{T("Guías", "Guides")}"><p class="foot-h">{T("Guías", "Guides")}</p><ul>{links(guias)}</ul></nav>
      <nav aria-label="{T("Por país", "By country")}"><p class="foot-h">{T("Por país", "By country")}</p><ul>{links(paises)}</ul></nav>
      <nav aria-label="Florario"><p class="foot-h">Florario</p><ul>{links(florario)}</ul></nav>
    </div>
    {src}
    {cred}
    <p class="foot-legal"><span>© {UPDATED.year} Florario – {T("Calendario de flores", "Flower calendar")}</span><span>{T("Última actualización", "Last updated")}: {time_tag(UPDATED)}</span></p>
  </footer>'''


# ---------------------------------------------------------------- JSON-LD
ORG_ID = f"{URL}/#org"


def org_ld():
    return {"@type": "Organization", "@id": ORG_ID, "name": "Florario",
            "alternateName": "Florario – Calendario de flores", "url": f"{URL}/",
            "logo": {"@type": "ImageObject", "url": f"{URL}/imagenes/logo-florario.png", "width": 512, "height": 512},
            "description": T("Calendario de fechas para regalar flores en España y Latinoamérica.",
                             "Calendar of dates for giving flowers in Spain and Latin America.")}


def website_id():
    return page_url("") + "#website"


def author_id():
    return page_url(T("sobre-florario", "about")) + "#autor"


def website_ld():
    return {"@type": "WebSite", "@id": website_id(), "name": "Florario", "alternateName": T("Calendario de flores", "Flower calendar"),
            "url": page_url(""), "inLanguage": LANG, "publisher": {"@id": ORG_ID}}


def author_ld():
    a = {"@type": "Person", "@id": author_id(), "name": SITE["author"],
         "url": page_url(T("sobre-florario", "about")), "worksFor": {"@id": ORG_ID}}
    if not pending(SITE["author_bio"]):
        a["description"] = AUTHOR_BIO
    if not pending(SITE["author_sameAs"]):
        a["sameAs"] = SITE["author_sameAs"]
    return a


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


def hreflang_links(slug):
    """Versiones de la página en cada idioma. La portada y las páginas de país españolas forman un
    grupo propio (cada país es la versión es-XX de la portada), al que se suma la portada inglesa."""
    s = es_slug(slug)
    country_slugs = [c["slug"] for c in datos.COUNTRIES.values()]
    if s == "" or s in country_slugs:
        if LANG == "en" and s:
            return ""  # /en/mexico/ no tiene pareja: /mexico/ ya es la versión es-MX de la portada
        out = [f'<link rel="alternate" hreflang="es" href="{URL}/">',
               f'<link rel="alternate" hreflang="x-default" href="{URL}/">']
        out += [f'<link rel="alternate" hreflang="{c["hreflang"]}" href="{URL}/{c["slug"]}/">' for c in datos.COUNTRIES.values()]
        out.append(f'<link rel="alternate" hreflang="en" href="{URL}/en/">')
        return "\n".join(out)
    return "\n".join([f'<link rel="alternate" hreflang="es" href="{URL}{lang_url(slug, "es")}">',
                      f'<link rel="alternate" hreflang="en" href="{URL}{lang_url(slug, "en")}">',
                      f'<link rel="alternate" hreflang="x-default" href="{URL}{lang_url(slug, "es")}">'])


# Google no siempre usa el SVG en los resultados: se ofrecen también ICO y PNG (múltiplos de 48 px).
FAVICON = ('<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
           '<link rel="icon" href="/favicon-96.png" sizes="96x96" type="image/png">\n'
           '<link rel="icon" href="/favicon-192.png" sizes="192x192" type="image/png">\n'
           '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
           '<link rel="apple-touch-icon" href="/imagenes/logo-florario.png">')
# Fuentes alojadas en /fuentes/ (el @font-face está en comun.css). Se precarga la del texto.
FONTS = '<link rel="preload" href="/fuentes/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>'


def head_meta(title, description, slug, img, og_type="article", og_title=None, extra="",
              modified=None, locale=None, og_image=None):
    """og_image = {"url", "w", "h", "alt"} para una imagen que no está en IMAGES (vista previa del PDF)."""
    if og_image is None:
        im = IMAGES[img]
        og_image = {"url": jpg_url(img), "w": im["w"], "h": im["h"], "alt": im["alt"]}
    if LANG == "en":
        locale = "en_US"
        alternates = '\n<meta property="og:locale:alternate" content="es_ES">'
    else:
        locale = locale or "es_ES"
        alternates = "".join(f'\n<meta property="og:locale:alternate" content="{l}">'
                             for l in LOCALE.values() if l != locale) if locale != "es_ES" or slug in LOCALE else ""
        alternates += '\n<meta property="og:locale:alternate" content="en_US">'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="{esc(SITE["author"])}">
<meta name="theme-color" content="#F2C230">
<link rel="canonical" href="{page_url(slug)}">
{hreflang_links(slug)}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(T(SITE["brand"], "Florario – Flower calendar"))}">
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


def short_label(d, year=False):
    """Fecha corta de las tablas: "sáb 14 feb (2027)" · "Sat Feb 14 (2027)"."""
    return f"{WEEKDAYS[d.weekday()][:3]} {day_month_short(d, year)}"


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
            name = month_name(d0.month - 1).capitalize()
            cell = f'<a href="{href(MONTHS[d0.month - 1])}">{name}</a>' if show_month_links else name
            if rolling:
                cell += f" {d0.year}"
            anchor = f"m-{MONTHS[d0.month - 1]}" + (f"-{d0.year}" if rolling else "")
            rows.append(f'<tr class="mhead"><th colspan="5" scope="colgroup" id="{anchor}">{cell}</th></tr>')
            last_m = m
        guide = ev["guia"]
        name = f'<a href="{href(guide)}">{esc(ev["name"])}</a>'
        every = f'<small>{T("cada año", "every year")}</small>'
        if rolling:
            other = f'<small>{ev["ruleText"]}</small>' if "rule" in ev else every
            label = short_label(d0, year=True)
        else:
            d1 = date_for(ev, y1)
            other = (f'<small>{y1}: {time_tag(d1, day_month_short(d1))}</small>'
                     if "rule" in ev else every)
            label = short_label(d0)
        rows.append(
            f'<tr id="f-{ev["id"]}" style="--dc:{color_hex(ev["color"])}">'
            f'<td class="when">{time_tag(d0, label)}{other}</td>'
            f'<td><span class="ev-name">{name}</span><p class="why">{esc(ev["story"])}</p></td>'
            f'<td data-label="{T("Flor", "Flower")}">{esc(ev["flower"])}</td>'
            f'<td data-label="Color"><span class="swatch">{COLORS[ev["color"]]["label"]}</span></td>'
            f'<td data-label="{T("Dónde", "Where")}">{esc(ev["region"])}</td></tr>')
    cap = f"<caption>{caption}</caption>" if caption else ""
    first_col = T("Fecha", "Date") if rolling else T(f"Fecha {y0}", f"Date {y0}")
    return (f'<div class="dtable-wrap"><table class="dtable">{cap}<thead><tr><th scope="col">{first_col}</th>'
            f'<th scope="col">{T("Qué se celebra y por qué", "What is celebrated and why")}</th><th scope="col">{T("Flor", "Flower")}</th><th scope="col">Color</th>'
            f'<th scope="col">{T("Dónde", "Where")}</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def flower_match(name, f):
    low = name.lower()
    return any(low == mt.lower() or low.startswith(mt.lower() + " ") or f"({mt.lower()})" in low for mt in f["match"])


def flower_link(name):
    for f in FLOWERS:
        if flower_match(name, f):
            return f'<a href="{href(f["slug"])}">{esc(name)}</a>'
    return esc(name)


def season_table(months=range(12), link_months=True):
    head = "".join(f'<th scope="col">{label}</th>' for _, label in SEASON_REGIONS)
    rows = []
    for m in months:
        name = month_name(m).capitalize()
        cell = f'<a href="{href(MONTHS[m])}">{name}</a>' if link_months else f"<span>{name}</span>"
        tds = "".join(f'<td>{", ".join(flower_link(x) for x in SEASON[m][k])}</td>' for k, _ in SEASON_REGIONS)
        rows.append(f'<tr data-m="{m}" style="--mc:{MONTH_COLORS[m]}"><th scope="row">{cell}</th>{tds}</tr>')
    return (f'<div class="season-wrap"><table class="season"><caption class="sr-only">{T("Flores de temporada por mes y región", "Seasonal flowers by month and region")}</caption>'
            f'<thead><tr><th scope="col">{T("Mes", "Month")}</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="season-note">{SEASON_NOTE} {T("Tabla orientativa: la temporada cambia con la zona y el año, y los invernaderos alargan casi todas.", "This table is a guide: the season changes with the area and the year, and greenhouses extend almost all of them.")}</p>')


def gcard(slug, alt=None):
    if slug in GUIDE:
        g = GUIDE[slug]
        small, name, desc, img, col = g["small"], g["name"], g["desc"], g["img"], g["color"]
    elif slug in FLOWER:
        f = FLOWER[slug]
        small, name, desc, img, col = (T("Por flor", "By flower"), f["name"],
                                       T("Significado, temporada y cuándo regalarla", "Meaning, season and when to give it"), f["img"], f["color"])
    elif slug in MONTHS:
        m = MONTHS.index(slug)
        evs = [e for e in EVENTS if month_of(e) == m + 1]
        small, name = T("Por mes", "By month"), T(f"Flores de {slug}", f"Flowers in {month_name(m)}")
        desc = T(f'{len(evs)} {"fecha" if len(evs) == 1 else "fechas"} y flores de temporada',
                 f'{len(evs)} {"date" if len(evs) == 1 else "dates"} and seasonal flowers')
        img = evs[0]["img"] if evs else "ramo-silvestre"
        col = None
    elif slug in HUB_CARDS:
        small, name, desc, img, col = HUB_CARDS[slug]
    elif slug in COUNTRY_BY_SLUG:
        code, c = COUNTRY_BY_SLUG[slug]
        n = len([e for e in EVENTS if code in e["paises"]])
        small, name, desc, img, col = (T("Por país", "By country"), T(f'Fechas {c["de"]}', f'Dates {c["en"]}'),
                                       T(f"{n} fechas para regalar flores", f"{n} dates for giving flowers"), "ramo-silvestre", "rosa")
    else:
        raise KeyError(slug)
    gc = MONTH_COLORS[MONTHS.index(slug)] if col is None else color_hex(col)
    return (f'<a class="gcard" href="{href(slug)}" style="--gc:{gc}">{thumb(img, alt or f"{name}: {IMAGES[img]['alt_corto']}")}'
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
    text = quote(T(f'Comprar flores: {ev["name"]} ({fmt(next_date(ev), year=False)})',
                   f'Buy flowers: {ev["name"]} ({fmt(next_date(ev), year=False)})'))
    det = quote(f'{ev["flower"]}. {ev["story"]} {T("Más en", "More at")} {page_url(ev["guia"])}')
    return (f"https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text={text}"
            f"&amp;dates={d:%Y%m%d}/{e:%Y%m%d}&amp;details={det}")


def gcal_subscribe():
    return f'https://calendar.google.com/calendar/r?cid=webcal://{URL.split("://")[1]}{ics_href()}'


def remind_box(evs, heading="h2"):
    btns = []
    if len(evs) > 4:
        btns.append(f'<a class="btn primary" href="{ics_href()}" download>{T("Todas las fechas (.ics)", "All dates (.ics)")}</a>')
        btns.append(f'<a class="btn" href="{gcal_subscribe()}" target="_blank" rel="noopener">{T("Suscribirme en Google Calendar ↗", "Subscribe in Google Calendar ↗")}</a>')
    else:
        for ev in evs:
            label = ev["name"] if len(evs) > 1 else T("Añadir a mi calendario", "Add to my calendar")
            btns.append(f'<a class="btn primary" href="{ics_href(ev["id"])}" download>{esc(label)} (.ics)</a>')
        btns.append(f'<a class="btn" href="{gcal_link(evs[0])}" target="_blank" rel="noopener">Google Calendar ↗</a>')
    return f'''<section class="remind" id="recuerdamelo" aria-labelledby="recuerdamelo-t">
          <{heading} id="recuerdamelo-t">{T("Recuérdamelo 3 días antes", "Remind me 3 days before")}</{heading}>
          <p>{T("Descarga el recordatorio y ábrelo con el calendario del móvil: se repite cada año y te avisa tres días antes para que te dé tiempo a encargar el ramo.",
                "Download the reminder and open it with your phone’s calendar: it repeats every year and alerts you three days before, so you have time to order the bouquet.")}</p>
          <div class="remind-actions">{"".join(btns)}</div>
        </section>'''


def next_widget(evs):
    evs = sorted(evs, key=next_date)
    first = evs[0]
    d = next_date(first)
    names = "|".join(e["name"] for e in evs)
    ids = "|".join(e["id"] for e in evs)
    whens = " ".join(when_code(e) for e in evs)
    label = T(f"de {MONTHS[d.month - 1]} de {d.year}", f"{month_name(d.month - 1)} {d.year}")
    return (f'<a class="next" href="{href("")}#{first["id"]}" data-when="{whens}" data-names="{esc(names)}" data-ids="{ids}">'
            f'<span class="next-num">{d.day}</span><span class="next-label">{label}</span>'
            f'<span class="next-name">{esc(first["name"])}</span><span class="next-go" aria-hidden="true">→</span></a>')


def facts_html(facts):
    if isinstance(facts, str):
        return facts
    return '<dl class="facts">' + "".join(
        f'<div><dt>{dt_}</dt><dd>{dd}{f"<small>{sm}</small>" if sm else ""}</dd></div>' for dt_, dd, sm in facts) + "</dl>"


def when_line(published, updated):
    """“Publicado el …” si la página no ha cambiado desde que se publicó; si no, “Actualizado el …”."""
    if updated > published:
        return f'{T("Actualizado el", "Updated")} {time_tag(updated)}'
    return f'{T("Publicado el", "Published")} {time_tag(published)}'


def byline(published=None, updated=None, author=True):
    published, updated = published or PUBLISHED, updated or UPDATED
    parts = []
    if author:
        parts.append(f'{T("Por", "By")} <a href="{href(T("sobre-florario", "about"))}" rel="author">{esc(SITE["author"])}</a>')
        if REVIEWER:
            r = REVIEWER
            parts.append(f'{T("Revisado por", "Reviewed by")} <a href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(r["name"])}</a>, '
                         f'{esc(r["business"])} ({esc(r["city"])})')
    parts.append(when_line(published, updated))
    return '<p class="byline">' + '<span class="dot">·</span>'.join(f"<span>{p}</span>" for p in parts) + "</p>"


def share_box(text, url):
    """WhatsApp (enlace normal, funciona sin JavaScript) y compartir nativo o copiar enlace (guia.js)."""
    from urllib.parse import quote
    wa = "https://wa.me/?text=" + quote(f"{text} {url}")
    return (f'<div class="share"><p>{T("¿Conoces a alguien que siempre llega tarde a estas fechas? Pásaselo.", "Know someone who’s always late for these dates? Send it to them.")}</p>'
            f'<div class="share-actions"><a class="btn" href="{wa}" target="_blank" rel="noopener">{T("Compartir por WhatsApp", "Share on WhatsApp")}</a>'
            f'<button type="button" class="btn" data-share data-url="{esc(url)}" data-title="{esc(text)}" hidden>{T("Compartir", "Share")}</button></div>'
            f'<p class="share-status" role="status"></p></div>')


def author_box():
    return (f'<aside class="author-box" aria-label="{T("Sobre el autor", "About the author")}">{bloom("#F2C230", 10)}'
            f'<p><b>{esc(SITE["author"])}</b> · Florario</p><p>{esc(AUTHOR_BIO)} '
            f'<a href="{href(T("sobre-florario", "about"))}">{T("Cómo hacemos Florario", "How we make Florario")}</a>.</p></aside>')


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
    # Ruta dentro de _build/paginas/ ("rosa.html" o "en/rose.html")
    meta["file"] = os.path.relpath(path, os.path.join(BUILD, "paginas")).replace(os.sep, "/")
    return meta, body


def fragments(lang):
    """Textos de las páginas de un idioma: _build/paginas/*.html o _build/paginas/<lang>/*.html."""
    d = os.path.join(BUILD, "paginas", *([] if lang == "es" else [lang]))
    return [read_fragment(os.path.join(d, n)) for n in sorted(os.listdir(d)) if n.endswith(".html")]


def stale_dates(frags):
    """Avisa si un fragmento tiene cambios sin confirmar en git pero su "updated" es anterior a hoy."""
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--", "paginas"], cwd=BUILD,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return
    changed = {l[3:].strip().strip('"').split("paginas/", 1)[-1] for l in out.splitlines() if l[:2].strip() in ("M", "MM", "AM")}
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
    for k in ("author", "owner", "email"):
        body = body.replace("{{" + k + "}}", esc(SITE[k]))
    body = body.replace("{{author_bio}}", esc(AUTHOR_BIO))
    body = body.replace("{{updated}}", time_tag(meta["updated"])).replace("{{site_updated}}", time_tag(UPDATED))
    for k, v in stats().items():
        body = body.replace("{{" + k + "}}", str(v))
    body = body.replace("{{n_pages}}", str(N_PAGES))
    if "<!--@REVISOR-->" in body:
        contact = href(T("contacto", "contact"))
        if REVIEWER:
            r = REVIEWER
            block = T(f'<p>Las guías las revisa <strong>{esc(r["name"])}</strong>, de <a href="{esc(r["url"])}" target="_blank" rel="noopener">'
                      f'{esc(r["business"])}</a> ({esc(r["city"])}). Comprueba que las flores que recomiendo se encuentran de verdad '
                      f'en esas fechas, que los consejos de cuidado son correctos y que los precios y la temporada tienen sentido. '
                      f'Cada página revisada lo indica debajo del título.</p>',
                      f'<p>The guides are reviewed by <strong>{esc(r["name"])}</strong>, from <a href="{esc(r["url"])}" target="_blank" rel="noopener">'
                      f'{esc(r["business"])}</a> ({esc(r["city"])}), who checks that the flowers I recommend are really available '
                      f'on those dates, that the care tips are correct and that prices and seasons make sense. '
                      f'Every reviewed page says so below its title.</p>')
        else:
            block = T(f'<p>Por ahora escribo y reviso yo todo el contenido, a partir de las fuentes que cito al pie de cada guía. '
                      f'No soy florista, y por eso busco una floristería o un productor que revise las guías antes de cada fecha: '
                      f'comprobar que las flores que recomiendo se encuentran de verdad en esa época y que los consejos de cuidado son correctos. '
                      f'Si te dedicas a las flores y te interesa, <a href="{contact}">escríbeme</a>. Cuando haya una revisión profesional, '
                      f'cada página lo indicará debajo del título con el nombre de quien la ha hecho.</p>',
                      f'<p>For now I write and review all the content myself, based on the sources cited at the bottom of each guide. '
                      f'I am not a florist, so I am looking for a flower shop or grower to review the guides before each date: '
                      f'checking that the flowers I recommend are really available at that time of year and that the care tips are correct. '
                      f'If you work with flowers and are interested, <a href="{contact}">write to me</a>. Once there is a professional review, '
                      f'each page will say so below its title, with the name of the reviewer.</p>')
        body = body.replace("<!--@REVISOR-->", block)
    if "<!--@CIFRAS-->" in body:
        rows = "".join(f'<tr><th scope="row">{c["name"]}</th><td>{len([e for e in EVENTS if code in e["paises"]])}</td></tr>'
                       for code, c in COUNTRIES.items())
        body = body.replace("<!--@CIFRAS-->", f'<div class="dtable-wrap"><table class="dtable"><caption>{T("Fechas para regalar flores por país", "Dates for giving flowers by country")}</caption>'
                                              f'<thead><tr><th scope="col">{T("País", "Country")}</th><th scope="col">{T("Fechas", "Dates")}</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if "<!--@WIDGET_CODE-->" in body:
        code = (f'<iframe src="{URL}/widget/" title="{T("Próxima fecha para regalar flores", "Next date for giving flowers")} · Florario" '
                f'width="320" height="200" style="border:0;max-width:100%" loading="lazy"></iframe>')
        body = body.replace("<!--@WIDGET_CODE-->", f'<pre class="code"><code>{esc(code)}</code></pre>')
    if "<!--@WIDGET_DEMO-->" in body:
        body = body.replace("<!--@WIDGET_DEMO-->", f'<iframe src="/widget/" title="{T("Vista previa del widget de Florario", "Preview of the Florario widget")}" width="320" height="200" style="border:0;max-width:100%" loading="lazy"></iframe>')
    if "<!--@PREVIEWS-->" in body:
        figs = "".join(
            f'<figure class="pdf-preview"><a href="{pdf_href(y)}" download>'
            f'<img src="{pdf_href(y, "jpg")}" width="{PREVIEW_W}" height="{PREVIEW_H}" '
            f'alt="{T(f"Portada del calendario de flores {y} para imprimir: corona de flores con los doce meses", f"Cover of the printable {y} flower calendar: a wreath of flowers with the twelve months")}" loading="lazy" decoding="async"></a>'
            f'<figcaption><a href="{pdf_href(y)}" download>{T(f"Calendario de flores {y} · PDF A4", f"{y} flower calendar · PDF, A4")}</a></figcaption></figure>'
            for y in (YEAR, YEAR + 1))
        body = body.replace("<!--@PREVIEWS-->", f'<div class="pdf-previews">{figs}</div>')
    if "<!--@FECHAS_MES-->" in body:
        m = MONTHS.index(slug) + 1
        evs = [e for e in EVENTS if month_of(e) == m]
        yr = min(next_date(e) for e in evs).year if evs else YEAR
        block = date_table(evs, T(f"Fechas con flores en {slug} de {yr}", f"Flower dates in {month_name(m - 1)} {yr}"), group_by_month=False, rolling=True) if evs else \
            T('<p class="note">Este mes no hay ninguna fecha del calendario en la que la costumbre sea regalar flores.</p>',
              '<p class="note">This month there is no date in the calendar on which giving flowers is the custom.</p>')
        body = body.replace("<!--@FECHAS_MES-->", block)
    if "<!--@TEMPORADA_MES-->" in body:
        m = MONTHS.index(slug)
        body = body.replace("<!--@TEMPORADA_MES-->", season_table([m], link_months=False))
    if "<!--@FECHAS_PAIS-->" in body:
        code = meta["pais"]
        evs = [e for e in EVENTS if code in e["paises"]]
        body = body.replace("<!--@FECHAS_PAIS-->", date_table(
            evs, T(f'Próximas fechas para regalar flores {COUNTRIES[code]["en"]} ({rolling_label(evs)})',
                   f'Upcoming dates for giving flowers {COUNTRIES[code]["en"]} ({rolling_label(evs)})'), rolling=True))
    if "<!--@FECHAS-->" in body:
        evs = [EV[i] for i in meta.get("eventos", [])]
        body = body.replace("<!--@FECHAS-->", date_table(evs, "", group_by_month=False, rolling=True))
    if "<!--@TEMPORADA_FLOR-->" in body:
        f = FLOWER[slug]
        rows = []
        for k, label in SEASON_REGIONS:
            ms = [i for i in range(12) if any(flower_match(x, f) for x in SEASON[i][k])]
            txt = ", ".join(f'<a href="{href(MONTHS[i])}">{month_name(i)}</a>' for i in ms) if ms else \
                T("fuera de temporada local (llega de invernadero o importada)", "out of local season (greenhouse-grown or imported)")
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
        meta["og_image"] = {"url": URL + pdf_href(PRINT_YEAR, "jpg"), "w": PREVIEW_W, "h": PREVIEW_H,
                            "alt": T(f"Portada del calendario de flores {PRINT_YEAR} para imprimir", f"Cover of the printable {PRINT_YEAR} flower calendar")}
    parent = {"flor": (T("Por flor", "By flower"), href(T("flores", "flowers"))), "mes": (T("Por mes", "By month"), href(T("meses", "months"))),
              "guia": (T("Guías", "Guides"), href(T("guias", "guides"))), "pais": (T("Por país", "By country"), href(T("paises", "countries")))}.get(tipo)
    crumbs = [(T("Calendario de flores", "Flower calendar"), page_url(""))]
    if parent:
        crumbs.append((parent[0], URL + parent[1]))
    crumbs.append((meta.get("crumb", meta["title"]), page_url(slug)))

    # JSON-LD
    graph = [org_ld(), website_ld()]
    if tipo in ("guia", "flor", "mes", "pais", "descarga"):
        graph.append(author_ld())
        graph.append({"@type": "Article", "@id": page_url(slug) + "#articulo",
                      "headline": strip_tags(meta.get("headline", meta["h1"]))[:110],
                      "description": meta["description"], "image": jpg_url(img) if img else None,
                      "inLanguage": LANG, "datePublished": meta["published"].isoformat(),
                      "dateModified": meta["updated"].isoformat(), "mainEntityOfPage": page_url(slug),
                      "author": {"@id": author_id()}, "publisher": {"@id": ORG_ID},
                      "isPartOf": {"@id": website_id()}})
        if REVIEWER:
            graph.append({"@type": "WebPage", "@id": page_url(slug), "url": page_url(slug),
                          "reviewedBy": reviewer_ld(), "lastReviewed": meta["updated"].isoformat()})
    else:
        graph.append({"@type": meta.get("schema", "WebPage"), "@id": page_url(slug), "name": meta["title"],
                      "description": meta["description"], "inLanguage": "es", "isPartOf": {"@id": website_id()},
                      "datePublished": meta["published"].isoformat(), "dateModified": meta["updated"].isoformat()})
        if slug == "sobre-florario":
            graph.append(author_ld())
    graph.append(breadcrumb(crumbs))
    if faq:
        graph.append(faq_ld(faq))
    ld_events = evs
    if tipo == "mes":
        ld_events = [e for e in EVENTS if month_of(e) == MONTHS.index(slug) + 1]
    if tipo == "pais":
        ld_events = [e for e in EVENTS if meta["pais"] in e["paises"]]
    if ld_events:
        graph.append(dates_list_ld(ld_events, f'{T("Fechas para regalar flores", "Dates for giving flowers")}: {strip_tags(meta.get("crumb", meta["title"]))}'))
    graph = [g for g in graph if g]
    for g in graph:
        if g.get("image") is None:
            g.pop("image", None)

    title = full_title(meta["title"])
    head = head_meta(title, meta["description"], slug, img or "ramo-silvestre",
                     og_type="article" if tipo in ("guia", "flor", "mes", "pais", "descarga") else "website",
                     og_title=meta.get("og_title"),
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
          <figcaption>{T("Foto", "Photo")}: <a href="{im["source"]}" target="_blank" rel="noopener">{esc(im["author"])}</a> · {im["license"]}</figcaption>
        </figure>'''
    facts = facts_html(meta["facts"]) if meta.get("facts") else ""
    toc = toc_from(body)
    if faq:
        toc += f'<li><a href="#preguntas">{T("Preguntas frecuentes", "FAQ")}</a></li>'
    cal_link = meta.get("cal_link") or (f'#{evs[0]["id"]}' if evs else "#fechas")
    faq_block = f'''<section id="preguntas" aria-labelledby="preguntas-t">
          <h2 id="preguntas-t">{T("Preguntas frecuentes", "Frequently asked questions")}</h2>
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
      <h2 id="related-t">{meta.get("related_title", T("Sigue explorando", "Keep exploring"))}</h2>
      <div class="gcards">
      {rel_html}
      </div>
    </section>''' if rel_html else ""
    n_events = len(EVENTS)
    cta = f'''<section class="cta" aria-labelledby="cta-t">
      <div>
        <h2 id="cta-t">{T("Todas las fechas en un solo calendario", "Every date in one calendar")}</h2>
        <p>{T(f"{n_events} fechas para regalar flores, de San Valentín al Día de Muertos, con la foto de cada flor, filtros por color, cuenta atrás y versión en PDF para imprimir.",
              f"{n_events} dates for giving flowers, from Valentine’s Day to the Day of the Dead, with a photo of each flower, color filters, a countdown and a printable PDF.")}</p>
      </div>
      <a class="btn primary" href="{href("")}">{T("Abrir el calendario de flores", "Open the flower calendar")}</a>
    </section>'''
    on_page = T("En esta página", "On this page")
    toc_nav = f'''<nav class="toc" aria-label="{on_page}">
          <details open>
            <summary>{on_page}</summary>
            <h2>{on_page}</h2>
            <ol>{toc}</ol>
          </details>
          <a class="btn primary" href="{href("")}{cal_link}">{T("Ver en el calendario", "See it in the calendar")}</a>
        </nav>''' if toc and is_article else ""
    crumb_html = "".join(f'<li><a href="{u.replace(URL, "") or "/"}">{esc(n)}</a></li>' for n, u in crumbs[:-1])
    hero_cls = "hero" if img else "hero hero-text"
    page = f'''<!doctype html>
<html lang="{LANG}">
<head>
{head}
</head>
<body class="{meta.get("color", "c-todos")}">
<div class="wrap">
  {header(meta.get("nav"), slug)}
  <nav class="crumbs" aria-label="{T("Estás aquí", "You are here")}">
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

  {footer(href(slug), meta.get("fuentes", []), used_imgs)}
</div>
<script src="/guia.js" defer></script>
</body>
</html>
'''
    write(f"{PREFIX}{slug}/index.html", page)
    return {"slug": PREFIX + slug, "tipo": tipo, "words": words(body + faq_html(faq)), "img": img, "title": meta["title"],
            "updated": meta["updated"], "img_url": (meta.get("og_image") or {}).get("url")}


# ---------------------------------------------------------------- hubs
def render_hub(slug, title, description, h1, eyebrow, lede, items, nav, intro_html, img, updated=None):
    """updated = la fecha más reciente de las páginas que enlaza."""
    updated = updated or UPDATED
    graph = [org_ld(), website_ld(),
             {"@type": "CollectionPage", "@id": page_url(slug), "name": title, "description": description,
              "inLanguage": LANG, "isPartOf": {"@id": website_id()}, "datePublished": PUBLISHED.isoformat(),
              "dateModified": updated.isoformat()},
             breadcrumb([(T("Calendario de flores", "Flower calendar"), page_url("")), (h1 if "<" not in h1 else strip_tags(h1), page_url(slug))]),
             {"@type": "ItemList", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "url": page_url(s),
                  "name": title_of(s) if s not in MONTHS else T(f"Flores de {s}", f"Flowers in {month_name(MONTHS.index(s))}")}
                 for i, s in enumerate(items)]}]
    head = head_meta(full_title(title), description, slug, img, og_type="website", modified=updated,
                     extra='<link rel="stylesheet" href="/guia.css">\n<link rel="stylesheet" href="/comun.css">\n' + ld_script(graph))
    html_cards, imgs = cards(items)
    page = f'''<!doctype html>
<html lang="{LANG}">
<head>
{head}
</head>
<body class="c-todos">
<div class="wrap">
  {header(nav, slug)}
  <nav class="crumbs" aria-label="{T("Estás aquí", "You are here")}"><ol><li><a href="{href("")}">{T("Calendario de flores", "Flower calendar")}</a></li><li aria-current="page">{strip_tags(h1)}</li></ol></nav>
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
  {footer(href(slug), (), imgs)}
</div>
</body>
</html>
'''
    write(f"{PREFIX}{slug}/index.html", page)
    return {"slug": PREFIX + slug, "tipo": "hub", "words": words(intro_html), "img": img, "title": title, "updated": updated}


# ---------------------------------------------------------------- portada
def home_faq_en():
    return [
        ("What is a flower calendar?",
         f"It is a list of the dates of the year on which it is customary to give flowers, with the right flower for each one. Florario gathers {len(EVENTS)} dates from Spain and Latin America, from Valentine’s Day and Mother’s Day to TikTok trends like yellow, blue and purple flowers, and adds which flowers are in season each month."),
        ("Which flowers are given on September 21?",
         "Yellow flowers: sunflowers, tulips or yellow roses. The trend was born with the song “Flores amarillas” from the Argentine series Floricienta and went viral on TikTok in 2021 to welcome spring in the southern hemisphere. In Mexico it is repeated on March 21."),
        ("Which flowers are given in October?",
         "On October 3, Boyfriend Day, people give blue flowers or Hot Wheels bouquets. In Argentina the third Sunday of October is Mother’s Day, with roses and lilies. In Mexico, the cempasúchil season for the Day of the Dead begins at the end of the month."),
        ("Which flowers are given on November 9?",
         "Purple flowers, such as violets, lavender or lisianthus, for your “purple person”. The trend comes from the song “Un ramito de violetas” by the Spanish singer Cecilia."),
        ("Which flowers are in season in autumn?",
         "In Spain, chrysanthemums, dahlias, asters and second-bloom roses. In Mexico, cempasúchil, cockscomb and chrysanthemums. In Argentina, Chile and Uruguay autumn falls in March, April and May, with dahlias, chrysanthemums and roses."),
        ("Can I download the flower calendar as a PDF?",
         f"Yes. The {YEAR} and {YEAR + 1} flower calendars are available as PDFs, with an illustrated cover, every date and the seasonal flowers table, ready to print on A4. You’ll find them on the printable flower calendar page, with a preview of each one."),
        ("How can I remember the dates?",
         "With the “Remind me” button: download the .ics file for a date or subscribe to the full calendar, and your phone will alert you three days before each date."),
    ]


def render_home():
    tpl = open(os.path.join(BUILD, "plantilla-inicio.html"), encoding="utf-8").read()
    # Textos fijos de la plantilla: <!--es-->español<!--en-->english<!--/-->
    tpl = re.sub(r"<!--es-->(.*?)<!--en-->(.*?)<!--/-->", lambda m: m.group(2 if LANG == "en" else 1), tpl, flags=re.S)
    title = full_title(T(f"Calendario de flores {YEAR_LABEL}: fechas para regalar flores",
                         f"Flower calendar {YEAR_LABEL}: which flower to give and when"))
    description = T(f"Todas las fechas para regalar flores en {YEAR_LABEL}: flores azules (3 de octubre), moradas (9 de noviembre), "
                    "amarillas, Día de la Madre y más, en España y Latinoamérica. Con flores de temporada y PDF para imprimir.",
                    f"Flower calendar {YEAR_LABEL}: every date for giving flowers in Spain and Latin America, "
                    "seasonal flowers month by month and a printable PDF calendar.")
    first, last = rolling_range(EVENTS)
    fechas_t = T("Próximas fechas para regalar flores", "Upcoming dates for giving flowers") + \
        f" ({MONTH_SHORT[first.month - 1]} {first.year} – {MONTH_SHORT[last.month - 1]} {last.year})"
    home_faq = home_faq_en() if LANG == "en" else [
        ("¿Qué es un calendario de flores?",
         f"Es una lista de las fechas del año en las que es costumbre regalar flores, con la flor que toca en cada una. Florario reúne {len(EVENTS)} fechas de España y Latinoamérica, desde San Valentín y el Día de la Madre hasta los trends de TikTok como las flores amarillas, azules y moradas, y añade qué flores están de temporada cada mes."),
        ("¿Qué flores se regalan el 21 de septiembre?",
         "Flores amarillas: girasoles, tulipanes o rosas amarillas. El trend nació con la canción “Flores amarillas” de Floricienta y se hizo viral en TikTok en 2021 para recibir la primavera del hemisferio sur. En México se repite el 21 de marzo."),
        ("¿Qué flores se regalan en octubre?",
         "El 3 de octubre, Día del Novio, se regalan flores azules o ramos de Hot Wheels. En Argentina el tercer domingo de octubre es el Día de la Madre, con rosas y liliums. En México, a finales de mes empieza la temporada del cempasúchil para el Día de Muertos."),
        ("¿Cuándo se regalan flores azules a los hombres?",
         "El 3 de octubre, Día del Novio, y otra vez el 19 de noviembre, Día Internacional del Hombre. Se regalan flores azules, como hortensias o rosas azules, o un ramo de Hot Wheels."),
        ("¿Qué flores se regalan el 9 de noviembre?",
         "Flores moradas, como violetas, lavanda o lisianthus, para tu “persona morada”. El trend sale de la canción “Un ramito de violetas” de Cecilia."),
        ("¿Qué flores son de temporada en otoño?",
         "En España, crisantemos, dalias, asters y rosas de segunda floración. En México, cempasúchil, terciopelo y crisantemos. En Argentina, Chile y Uruguay el otoño cae en marzo, abril y mayo, con dalias, crisantemos y rosas."),
        ("¿Puedo descargar el calendario de flores en PDF?",
         f"Sí. Tienes el calendario de flores {YEAR} y el de {YEAR + 1} en PDF, con portada ilustrada, todas las fechas y la tabla de flores de temporada, listos para imprimir en A4. Están en la página del calendario de flores para imprimir, con una vista previa de cada uno."),
        ("¿Cómo puedo acordarme de las fechas?",
         "Con el botón “Recuérdamelo”: descarga el archivo .ics de una fecha o suscríbete al calendario completo y tu móvil te avisará tres días antes de cada fecha."),
    ]
    graph = [org_ld(), website_ld(),
             {"@type": "WebPage", "@id": page_url("") + "#webpage", "url": page_url(""), "name": title,
              "description": description, "inLanguage": LANG, "isPartOf": {"@id": website_id()},
              "datePublished": PUBLISHED.isoformat(), "dateModified": UPDATED.isoformat(),
              "primaryImageOfPage": jpg_url("girasol")},
             breadcrumb([(T("Calendario de flores", "Flower calendar"), page_url(""))]),
             faq_ld(home_faq),
             dates_list_ld(EVENTS, fechas_t)]
    head = head_meta(title, description, "", "girasol", og_type="website",
                     og_title=T(f"Calendario de flores {YEAR_LABEL}: qué flor regalar en cada fecha",
                                f"Flower calendar {YEAR_LABEL}: which flower to give on each date"),
                     extra='<link rel="stylesheet" href="/comun.css">\n' + ld_script(graph))
    guide_cards, gimgs = cards([g["slug"] for g in GUIDES])
    flower_cards, fimgs = cards([f["slug"] for f in FLOWERS])
    month_tiles = "".join(
        f'<a class="tile" href="{href(m)}" style="--tc:{MONTH_COLORS[i]}"><span class="k">{MONTH_SHORT[i]}</span>'
        f'<b>{T(f"Flores de {m}", f"Flowers in {month_name(i)}")}</b><small>{", ".join(SEASON[i]["es"][:3])}…</small></a>' for i, m in enumerate(MONTHS))
    country_tiles = "".join(
        f'<a class="tile" href="{href(c["slug"])}"{T(f" hreflang=\"{c['hreflang']}\"", "")}><span class="k">{T(c["hreflang"], code)}</span>'
        f'<b>{c["name"]}</b><small>{len([e for e in EVENTS if code in e["paises"]])} {T("fechas para regalar flores", "dates for giving flowers")}</small></a>'
        for code, c in COUNTRIES.items())
    downloads = f'''<div class="tiles">
        <a class="tile" href="{href(T("calendario-de-flores-para-imprimir", "printable-flower-calendar"))}" style="--tc:#8A4FD8"><span class="k">{T("Para imprimir", "Printable")}</span><b>{T(f"Calendario de flores {PRINT_YEAR} ilustrado", f"Illustrated {PRINT_YEAR} flower calendar")}</b><small>{T("Vista previa y cómo imprimirlo, gratis para uso personal", "Preview and printing tips, free for personal use")}</small></a>
        <a class="tile" href="{pdf_href(YEAR)}" download style="--tc:#F2C230"><span class="k">PDF · A4</span><b>{T(f"Calendario de flores {YEAR}", f"{YEAR} flower calendar")}</b><small>{T("Todas las fechas y las flores de temporada", "Every date and the seasonal flowers")}</small></a>
        <a class="tile" href="{pdf_href(YEAR + 1)}" download style="--tc:#EE7FA8"><span class="k">PDF · A4</span><b>{T(f"Calendario de flores {YEAR + 1}", f"{YEAR + 1} flower calendar")}</b><small>{T("Con las fechas móviles ya calculadas", "With the movable dates already worked out")}</small></a>
        <a class="tile" href="{ics_href()}" download style="--tc:#2BB3A3"><span class="k">{T(".ics · Recuérdamelo", ".ics · Remind me")}</span><b>{T("Todas las fechas en tu calendario", "Every date in your calendar")}</b><small>{T("Aviso 3 días antes de cada una", "An alert 3 days before each one")}</small></a>
        <a class="tile" href="{gcal_subscribe()}" target="_blank" rel="noopener" style="--tc:#3F72E0"><span class="k">{T("Suscripción", "Subscription")}</span><b>{T("Añadir a Google Calendar", "Add to Google Calendar")}</b><small>{T("Se actualiza sola cuando añadimos fechas", "It updates itself when we add dates")}</small></a>
      </div>'''
    data_js = "\n".join([
        f"  const LANG = {json.dumps(LANG)};",
        f"  const BASE = {json.dumps(href(''))};",
        f"  const ICS_BASE = {json.dumps(ics_href('ID').replace('ID.ics', ''))};",
        f"  const MONTHS = {json.dumps([month_name(i) for i in range(12)], ensure_ascii=False)};",
        f"  const MONTH_SHORT = {json.dumps([s.upper() for s in MONTH_SHORT], ensure_ascii=False)};",
        f"  const COLORS = {json.dumps(COLORS, ensure_ascii=False)};",
        f"  const TYPES = {json.dumps(TYPES, ensure_ascii=False)};",
        f"  const MONTH_COLORS = {json.dumps(MONTH_COLORS)};",
        f"  const IMAGES = {json.dumps({k: {x: v[x] for x in ('file', 'alt_corto', 'author', 'license', 'source')} for k, v in IMAGES.items()}, ensure_ascii=False)};",
        f"  const GUIDE_NAMES = {json.dumps({g['slug']: g['name'] for g in GUIDES} | {f['slug']: f['name'] for f in FLOWERS}, ensure_ascii=False)};",
        "  const EVENTS = " + json.dumps(EVENTS, ensure_ascii=False, indent=1).replace("\n", "\n  ") + ";",
    ])
    rep = {
        "HEAD": head,
        "HEADER": header("fechas", ""),
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
        "FOOTER": footer(href(""), [
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
    write(f"{PREFIX}index.html", out)
    return {"slug": PREFIX.rstrip("/"), "tipo": "home", "words": words(re.sub(r"<script.*?</script>", "", out, flags=re.S)), "img": "girasol",
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
    # El UID cambia con el idioma para que quien se suscriba a los dos calendarios no vea eventos pisados
    uid = ev["id"] + ("" if LANG == "es" else f"-{LANG}")
    lines = ["BEGIN:VEVENT", f'UID:{uid}@calendariodeflores.com', f"DTSTAMP:{stamp}",
             f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}", rrule,
             f'SUMMARY:{ics_escape("🌷 " + ev["name"] + ": " + ev["flower"])}',
             f'DESCRIPTION:{ics_escape(ev["story"] + T(" Dónde: ", " Where: ") + ev["region"] + T(". Guía: ", ". Guide: ") + page_url(ev["guia"]))}',
             f'URL:{page_url(ev["guia"])}', "TRANSP:TRANSPARENT",
             "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:-P3D",
             f'DESCRIPTION:{ics_escape(T("En 3 días: ", "In 3 days: ") + ev["name"] + T(". Encarga ", ". Order ") + ev["flower"].lower() + ".")}',
             "END:VALARM", "END:VEVENT"]
    return lines


def ics_calendar(evs, name):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", T("PRODID:-//Florario//Calendario de flores//ES", "PRODID:-//Florario//Flower calendar//EN"),
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", f"X-WR-CALNAME:{ics_escape(name)}", "X-WR-TIMEZONE:Europe/Madrid",
             "REFRESH-INTERVAL;VALUE=DURATION:P7D", "X-PUBLISHED-TTL:P7D"]
    for ev in evs:
        lines += ics_vevent(ev)
    lines.append("END:VCALENDAR")
    return "\r\n".join(ics_fold(l) for l in lines) + "\r\n"


def render_ics():
    write(ics_href().lstrip("/"), ics_calendar(EVENTS, f'Florario – {T("Calendario de flores", "Flower calendar")}'))
    for ev in EVENTS:
        write(ics_href(ev["id"]).lstrip("/"), ics_calendar([ev], f'Florario · {ev["name"]}'))


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
    out.append(f'<text class="wy" y="6">{y}</text><text class="ws" y="20">{len(EVENTS)} {T("FECHAS CON FLORES", "FLOWER DATES")}</text>')
    return f'<svg class="wheel" viewBox="-124 -124 248 248" aria-hidden="true">{"".join(out)}</svg>'


def render_pdf_html(y):
    months = []
    for m in range(12):
        evs = [e for e in events_sorted(EVENTS, y) if date_for(e, y).month == m + 1]
        items = "".join(
            f'<li style="--dc:{color_hex(e["color"])}"><b>{date_for(e, y).day}</b>'
            f'<span><strong>{esc(e["name"])}</strong> · {esc(e["flower"])}<small>{esc(e["region"].split(" · ")[0])}</small></span></li>'
            for e in evs) or f'<li class="empty"><span>{T("Sin fechas: flores para ti", "No dates: flowers for you")}</span></li>'
        ill = bloom(MONTH_COLORS[m], [6, 8, 10, 12][m % 4], "mo-bloom")
        months.append(f'<section class="mo" style="--mc:{MONTH_COLORS[m]}"><h2>{ill}{month_name(m).capitalize()}</h2><ul>{items}</ul></section>')
    season_rows = "".join(
        f'<tr style="--mc:{MONTH_COLORS[m]}"><th>{month_name(m).capitalize()}</th>'
        + "".join(f'<td>{", ".join(SEASON[m][k])}</td>' for k, _ in SEASON_REGIONS) + "</tr>" for m in range(12))
    heads = "".join(f"<th>{label}</th>" for _, label in SEASON_REGIONS)
    st = stats()
    # Las fuentes se cargan de /fuentes/ con una ruta relativa desde _build/salida/
    fonts = os.path.relpath(os.path.join(ROOT, "fuentes"), os.path.join(BUILD, "salida")).replace(os.sep, "/")
    return f'''<!doctype html>
<html lang="{LANG}"><head><meta charset="utf-8"><title>{T(f"Calendario de flores {y}", f"Flower calendar {y}")} · Florario</title>
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
{pdf_body(y, months, heads, season_rows, st)}
</body></html>'''


def pdf_body(y, months, heads, season_rows, st):
    if LANG == "en":
        return f'''<section class="cover">
<div class="cover-top"><span>{bloom("#F2C230", 10)}Florario</span><span>calendariodeflores.com/en</span></div>
<h1>Flower calendar <span>{y}</span></h1>
<p class="sub">Which flower to give on every date of the year in Spain and Latin America, with the movable dates already worked out for {y}.</p>
{pdf_wheel(y)}
<ul class="inside">
<li><b>{st["n_events"]} dates</b>From Valentine’s Day and Sant Jordi to the yellow, blue and purple flower trends.</li>
<li><b>12 months</b>What is given each month, where, and the right flower.</li>
<li><b>Seasonal flowers</b>In Spain, in Mexico and Central America and in the Southern Cone.</li>
</ul>
<div class="cover-foot"><span>Free for personal use · © Florario · calendariodeflores.com</span><span>A4 · 3 pages</span></div>
</section>
<header><div><h1>Flower calendar <em>{y}</em></h1><p>Which flower to give on every date of the year in Spain and Latin America · Movable dates already worked out for {y}.</p></div>
<div class="brand">{bloom("#F2C230", 10)}<br>Florario<br>calendariodeflores.com</div></header>
<div class="grid">{"".join(months)}</div>
<footer><span>Florario – Flower calendar · www.calendariodeflores.com/en/</span><span>Guides for each date, photos and countdown on the website</span></footer>
<div class="page2">
<h3>Seasonal flowers month by month</h3>
<table><thead><tr><th>Month</th>{heads}</tr></thead><tbody>{season_rows}</tbody></table>
<p class="note">{SEASON_NOTE} This table is a guide: the season changes with the area, and greenhouses extend almost all of them.</p>
<div class="legend">
<div class="box"><b>By color</b>Yellow: joy and friendship (Sep 21, Mar 21) · Red: love (Feb 14, Sant Jordi) · Pink: affection (Mother’s Day) · Blue: loyalty (Oct 3, Nov 19) · Purple: admiration (Nov 9) · White: peace and remembrance (Nov 1).</div>
<div class="box"><b>Remind me</b>Subscribe to the calendar at calendariodeflores.com/en/#recuerdamelo and your phone will alert you 3 days before each date.</div>
</div>
<footer><span>© {UPDATED.year} Florario – Flower calendar</span><span>www.calendariodeflores.com/en/</span></footer>
</div>'''
    return f'''<section class="cover">
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
</div>'''


def browser_cmd(browser, *args):
    # En GitHub Actions (Ubuntu 24.04) el sandbox de Chrome no arranca
    extra = ["--no-sandbox"] if os.environ.get("CI") else []
    return [browser, "--headless=new", "--disable-gpu", *extra, *args]


def find_browser():
    for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              shutil.which("google-chrome") or "", shutil.which("chromium") or ""]:
        if p and os.path.exists(p):
            return p
    return None


def render_pdfs(print_pdf):
    for y in (YEAR, YEAR + 1):
        name = f"pdf-{y}" if LANG == "es" else f"pdf-{LANG}-{y}"
        src = os.path.join(BUILD, "salida", f"{name}.html")
        os.makedirs(os.path.dirname(src), exist_ok=True)
        with open(src, "w", encoding="utf-8") as f:
            f.write(render_pdf_html(y))
        # Sin --pdf solo se imprimen los PDF que falten (p. ej. los del idioma nuevo)
        out = os.path.join(ROOT, *pdf_href(y).lstrip("/").split("/"))
        if print_pdf or not os.path.exists(out):
            browser = find_browser()
            if not browser:
                WARN.append("No encontré Chrome ni Edge: los PDF no se han regenerado.")
                return
            os.makedirs(os.path.dirname(out), exist_ok=True)
            subprocess.run(browser_cmd(browser, "--no-pdf-header-footer",
                                       "--virtual-time-budget=8000", f"--print-to-pdf={out}", "file:///" + src.replace("\\", "/")),
                           check=True, capture_output=True)
            pages = len(re.findall(rb"/Type\s*/Page[^s]", open(out, "rb").read()))
            if pages > 3:
                WARN.append(f"El PDF {pdf_href(y)} tiene {pages} páginas (máximo 3).")
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
    png_name = f"portada-{y}.png" if LANG == "es" else f"portada-{LANG}-{y}.png"
    png = os.path.join(tmp, png_name)
    subprocess.run(browser_cmd(browser, "--hide-scrollbars",
                               f"--window-size={PREVIEW_CSS[0]},{PREVIEW_CSS[1]}", f"--force-device-scale-factor={PREVIEW_SCALE}",
                               "--virtual-time-budget=8000", f"--screenshot={png}", "file:///" + src.replace("\\", "/")),
                   check=True, capture_output=True)
    out = os.path.join(ROOT, *pdf_href(y, "jpg").lstrip("/").split("/"))
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
img.src = "{png_name}";
</script></body>''')
        res = subprocess.run(browser_cmd(browser, "--allow-file-access-from-files",
                                         "--virtual-time-budget=8000", "--dump-dom", "file:///" + conv.replace("\\", "/")),
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
  <p class="k" id="k">Próxima fecha para regalar flores</p>
  <div class="m"><span class="n" id="n">{d.day}</span><span class="t" id="t">{esc(first["name"])}</span><span class="f" id="f">{esc(first["flower"])}</span></div>
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
        loc = f'{URL}/{p["slug"]}/' if p["slug"] else f"{URL}/"
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
                # En la portada, #<id de fecha> abre la ficha con JavaScript
                if f'id="{frag}"' not in other and not (path in ("/", "/en/") and frag in ev_ids):
                    problems.append(f'{p["slug"] or "/"}: ancla rota {href}')
    return problems


# ---------------------------------------------------------------- main
def render_hubs_es(pages, by_type):
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


def render_hubs_en(pages, by_type):
    pages.append(render_hub("months", "Flowers by month: what to give and what’s in season",
                            "Which flowers to give each month of the year and which are in season in Spain, Mexico and the Southern Cone, with every date for giving flowers from January to December.",
                            "Flowers <em>by month</em>", "Flower calendar · by month",
                            "Pick a month to see its dates for giving flowers, which flowers are in season in each region and tips for that time of year.",
                            MONTHS, "meses",
                            "<p>Each month has its own page with the calendar dates, the seasonal flowers in Spain, in Mexico and Central America and in Argentina, Chile and Uruguay, and a FAQ. If you’d rather see everything together, the home page has the <a href=\"/en/#temporada\">seasonal flowers table</a> and the <a href=\"/en/#fechas\">full calendar</a>, and there is also a <a href=\"/en/printable-flower-calendar/\">printable calendar</a>.</p>"
                            "<p>The seasons are reversed on each side of the equator: in March, while tulips are starting in Spain, Argentina and Chile get the dahlias and chrysanthemums of autumn. That is why each month splits its seasonal flowers by region. And in Colombia and Ecuador, with a mountain climate all year round, almost every cut flower can be found in any month.</p>",
                            "ramo-tulipanes", by_type("mes")))
    pages.append(render_hub("flowers", "Flowers: meaning, season and when to give them",
                            "A guide to flowers for giving: rose, sunflower, tulip, peony, carnation, chrysanthemum, cempasúchil, violet and more, with their meaning, their season and the dates on which they are given.",
                            "What <em>each flower</em> means", "Flower calendar · by flower",
                            "Each flower has its own page with its meaning, its colors, the months when it is in season, the dates of the year on which it is given and how to make it last longer in the vase.",
                            [f["slug"] for f in FLOWERS], "flores",
                            "<p>Looking by color rather than by flower? See the <a href=\"/en/flower-color-meanings/\">meaning of flower colors</a>. And if you need a specific date, they are all in the <a href=\"/en/#fechas\">flower calendar</a>.</p>"
                            "<p>The same flower can say different things depending on the country and the color: the chrysanthemum is the All Saints’ Day flower in Spain, but elsewhere it is given without that meaning; the red rose is love on Valentine’s Day and Sant Jordi, and the yellow one means friendship. Each page explains these nuances and lists the calendar dates on which that flower takes center stage.</p>",
                            "ramo-silvestre", by_type("flor")))
    pages.append(render_hub("guides", "Guides to giving flowers for every date and occasion",
                            "Florario guides: yellow, blue and purple flowers, Valentine’s Day, Mother’s Day, Father’s Day, Women’s Day, Teachers’ Day, birthdays, anniversaries, sympathy flowers and more.",
                            "Guides to <em>giving flowers</em>", "Flower calendar · guides",
                            "The origin of each date and each trend, which flowers to give, what each color means and how to get it right on occasions without a fixed date, such as birthdays, anniversaries or condolences.",
                            [g["slug"] for g in GUIDES], "guias",
                            "<p>The guides are reviewed before each date. If a tradition from your country is missing, <a href=\"/en/contact/\">tell us about it</a>.</p>"
                            "<p>Each guide explains where the date comes from (a song, a legend, a law or a hashtag), in which countries it is celebrated, which flowers are given and which ones are a good alternative if you can’t find the typical ones. At the bottom of each guide are the sources consulted: at least two media outlets from different countries for each trend.</p>",
                            "ramo-rosas", by_type("guia")))
    pages.append(render_hub("countries", "Dates for giving flowers by country",
                            "Which dates for giving flowers are celebrated in Spain, Mexico, Argentina, Colombia, Chile and Peru: Mother’s Day, Father’s Day, flower trends and more, with each country’s date.",
                            "Dates for giving flowers <em>by country</em>", "Flower calendar · by country",
                            "Mother’s Day, Father’s Day and the flower trends don’t fall on the same day in every country. Pick one to see only its dates, worked out for this year and next.",
                            [c["slug"] for c in COUNTRIES.values()], "paises",
                            "<p>Some dates belong to everyone, like Valentine’s Day or the yellow flowers of September 21, and others only make sense in one country: Sant Jordi in Catalonia, the Day of the Dead and Our Lady of Guadalupe in Mexico, or Amor y Amistad in Colombia. Mother’s Day is the best example: the first Sunday of May in Spain, May 10 in Mexico, the second Sunday of May in Colombia, Chile and Peru, and the third Sunday of October in Argentina.</p>"
                            "<p>If your country isn’t on the list, the <a href=\"/en/#fechas\">full calendar</a> also includes the dates from Brazil, France, India and South Korea that have become known on social media.</p>",
                            "ramo-silvestre", by_type("pais")))


def render_lang(lang, frags, print_pdf):
    """Genera todas las páginas de un idioma y devuelve la lista para el sitemap."""
    global N_PAGES
    set_lang(lang)
    N_PAGES = len(frags) + 5  # + portada y los 4 índices
    pages = [render_home()]
    for meta, body in frags:
        pages.append(render_article(meta, body))
    by_type = lambda t: max([p["updated"] for p in pages if p["tipo"] == t] or [UPDATED])
    if lang == "en":
        render_hubs_en(pages, by_type)
    else:
        render_hubs_es(pages, by_type)
    render_ics()
    render_pdfs(print_pdf)
    return pages


def main():
    global UPDATED
    print_pdf = "--pdf" in sys.argv
    frags = {lang: fragments(lang) for lang in LANGS}
    # La última revisión del sitio es la de la página más reciente (portada, pie, .ics)
    UPDATED = max([PUBLISHED] + [m["updated"] for fr in frags.values() for m, _ in fr])
    stale_dates(frags["es"] + frags["en"])
    # Cada página española necesita su traducción (y al revés): si falta, el selector de idioma daría 404
    es_slugs = {m["slug"] for m, _ in frags["es"]}
    en_slugs = {m["slug"] for m, _ in frags["en"]}
    missing_tr = sorted(f"en/{SLUG_EN.get(s, '¿?')}.html (de {s}.html)" for s in es_slugs if SLUG_EN.get(s) not in en_slugs)
    missing_tr += sorted(f"{SLUG_ES.get(s, '¿?')}.html (de en/{s}.html)" for s in en_slugs if SLUG_ES.get(s) not in es_slugs)

    pages = []
    for lang in LANGS:
        pages += render_lang(lang, frags[lang], print_pdf)
    set_lang("es")
    render_widget()
    render_sitemap(pages)

    problems = check_site(pages)
    problems += [f"falta la traducción {m}" for m in missing_tr]
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
