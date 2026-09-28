# Florario – Calendario de flores

Calendario interactivo con todas las fechas del año en las que es tradición (o tendencia en TikTok) regalar flores en España y Latinoamérica: qué flor se regala, en qué países y por qué, con flores de temporada mes a mes, guías, calendario en PDF y recordatorios.

- 26 fechas: clásicas (San Valentín, Sant Jordi, Día de la Madre, Día del Padre…), trends (flores amarillas, azules, moradas, Día de la Novia…) y fechas de memoria.
- Rueda del año, explorador por meses, filtros por tipo y color, fechas guardadas y “Recuérdamelo” (.ics con aviso 3 días antes).
- 61 páginas: portada, 19 guías, 14 flores, 12 meses, 6 países (con hreflang), 4 índices, calendario para imprimir, prensa y 4 páginas de confianza (sobre, contacto, privacidad, aviso legal), más un widget insertable (`/widget/`, noindex).

Web publicada: <https://www.calendariodeflores.com/>

## Cómo se genera

La web es HTML estático, pero las páginas se generan con un script de Python sin dependencias:

```
python _build/build.py          # páginas, portada, sitemap, .ics, widget
python _build/build.py --pdf    # además, los PDF y sus vistas previas JPG (necesita Chrome o Edge)
python _build/pines.py          # imágenes para Pinterest en marketing/pines/
python _build/indexnow.py       # avisa a Bing/Yandex de las URL del sitemap (IndexNow)
```

| Archivo | Qué es |
|---|---|
| `_build/datos.py` | **Fuente única de datos**: fechas (`EVENTS`), fotos, flores de temporada, países, guías y datos del sitio (`SITE`, con autor y titular). |
| `_build/paginas/*.html` | Texto de cada página (cabecera JSON con title, description, FAQ, `published` y `updated`… y el cuerpo en HTML). |
| `_build/plantilla-inicio.html` | Plantilla de la portada (CSS y JS del calendario interactivo). |
| `_build/build.py` | Generador: escribe `index.html`, las carpetas de cada página, `sitemap.xml`, `recordatorios/*.ics`, `descargas/` y comprueba enlaces, anclas, JSON-LD, `alt` y H1. |
| `comun.css` | Cabecera fija con menú, pie con enlaces internos, tablas de fechas y temporada. |
| `guia.css`, `guia.js` | Estilos, cuenta atrás y botón de compartir de las páginas interiores. |
| `fuentes/` | Bricolage Grotesque y DM Mono en woff2 (subconjunto latin, licencia OFL), alojadas en la propia web. |
| `imagenes/web/` | Fotos en AVIF y WebP (960, 640, 480 y miniatura 160). Créditos en `imagenes/CREDITOS.md`. |
| `.github/workflows/regenerar.yml` | Regeneración diaria automática (GitHub Actions): si algo cambia, commit, push (despliega en Vercel) y aviso por IndexNow. |
| `7e8fe03e1617c657b1014097a1ffc5ae.txt` | Clave pública de IndexNow; no la borres. |
| `descargas/` | Calendario de flores del año y del siguiente en PDF (portada ilustrada + 2 páginas), su vista previa en JPG y `.ics` con todas las fechas. |
| `vercel.json`, `.vercelignore` | Barra final en las URLs, redirección de `/index.html`, cabeceras de `.ics`, imágenes y fuentes; `_build/` y `marketing/` no se publican. |
| `marketing/` | Plan de SEO, enlaces, prensa, Pinterest y TikTok, y las imágenes de los pines. |
| `DOCUMENTACION.md` | Investigación, decisiones y cambios del proyecto. |

**No edites a mano** `index.html` ni las carpetas de páginas: se sobrescriben al generar. Edita `_build/` y vuelve a ejecutar el build.

**La web se regenera sola cada día** (GitHub Actions, 06:30 UTC). La tabla de la portada, las de países y meses y el año del title se calculan con la fecha del build: empiezan por la próxima fecha y, desde el 1 de octubre, el title pasa a “2026-2027”. En enero el trabajo genera también el PDF del año nuevo. Solo hay commit cuando algo cambia, con tu identidad de git. Se puede lanzar a mano desde GitHub: *Actions → Regenerar la web → Run workflow*. Para probar otra fecha: `FLORARIO_HOY=2026-12-15 python _build/build.py`.

**Cuando cambies el contenido de una página,** pon su `"updated"` a la fecha del día en la cabecera del fragmento. Esa fecha se usa en la firma, el JSON-LD y el `lastmod` del sitemap. El build avisa si un fragmento tiene cambios sin confirmar en git y su `updated` es anterior a hoy.

Para verla en local: `python -m http.server` en la carpeta del proyecto y abrir <http://localhost:8000>.

## Créditos

Las fotos son de Wikimedia Commons con licencias CC BY, CC BY-SA y CC0; el detalle está en [`imagenes/CREDITOS.md`](imagenes/CREDITOS.md).
