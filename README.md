# Florario – Calendario de flores

Calendario interactivo con todas las fechas del año en las que es tradición (o tendencia en TikTok) regalar flores en España y Latinoamérica: qué flor se regala, en qué países y por qué, con flores de temporada mes a mes, guías, calendario en PDF y recordatorios.

- 26 fechas: clásicas (San Valentín, Sant Jordi, Día de la Madre, Día del Padre…), trends (flores amarillas, azules, moradas, Día de la Novia…) y fechas de memoria.
- Rueda del año, explorador por meses, filtros por tipo y color, fechas guardadas y “Recuérdamelo” (.ics con aviso 3 días antes).
- 56 páginas: portada, 17 guías, 14 flores, 12 meses, 6 países (con hreflang), 3 índices y 4 páginas de confianza (sobre, contacto, privacidad, aviso legal).

Web publicada: <https://www.calendariodeflores.com/>

## Cómo se genera

La web es HTML estático, pero las páginas se generan con un script de Python sin dependencias:

```
python _build/build.py          # páginas, portada, sitemap, .ics
python _build/build.py --pdf    # además, los PDF (necesita Chrome o Edge)
python _build/pines.py          # imágenes para Pinterest en marketing/pines/
```

| Archivo | Qué es |
|---|---|
| `_build/datos.py` | **Fuente única de datos**: fechas (`EVENTS`), fotos, flores de temporada, países, guías y datos del sitio (`SITE`, con autor y titular). |
| `_build/paginas/*.html` | Texto de cada página (cabecera JSON con title, description, FAQ… y el cuerpo en HTML). |
| `_build/plantilla-inicio.html` | Plantilla de la portada (CSS y JS del calendario interactivo). |
| `_build/build.py` | Generador: escribe `index.html`, las carpetas de cada página, `sitemap.xml`, `recordatorios/*.ics`, `descargas/` y comprueba enlaces, anclas, JSON-LD, `alt` y H1. |
| `comun.css` | Cabecera fija con menú, pie con enlaces internos, tablas de fechas y temporada. |
| `guia.css`, `guia.js` | Estilos y cuenta atrás de las páginas interiores. |
| `imagenes/web/` | Fotos en AVIF y WebP (960, 480 y miniatura 160). Créditos en `imagenes/CREDITOS.md`. |
| `descargas/` | Calendario de flores 2026 y 2027 en PDF y `.ics` con todas las fechas. |
| `vercel.json`, `.vercelignore` | Barra final en las URLs, cabeceras de `.ics` e imágenes; `_build/` y `marketing/` no se publican. |
| `marketing/` | Plan de SEO, enlaces, prensa, Pinterest y TikTok, y las imágenes de los pines. |
| `DOCUMENTACION.md` | Investigación, decisiones y cambios del proyecto. |

**No edites a mano** `index.html` ni las carpetas de páginas: se sobrescriben al generar. Edita `_build/` y vuelve a ejecutar el build.

Para verla en local: `python -m http.server` en la carpeta del proyecto y abrir <http://localhost:8000>.

## Créditos

Las fotos son de Wikimedia Commons con licencias CC BY, CC BY-SA y CC0; el detalle está en [`imagenes/CREDITOS.md`](imagenes/CREDITOS.md).
