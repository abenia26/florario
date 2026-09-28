# Florario

Calendario interactivo con todas las fechas del año en las que es tradición (o tendencia en TikTok) regalar flores: qué flor se regala, en qué países y por qué.

- 23 fechas: clásicas (San Valentín, Sant Jordi, Día de la Madre…), trends (flores amarillas, flores moradas, Día del Novio…) y fechas de memoria.
- Rueda del año, explorador por meses con la foto de cada flor en su día, filtros por tipo y por color, fechas guardadas y recordatorio para copiar.
- Las fechas móviles (Día de la Madre, Amor y Amistad) se calculan para cualquier año.

## Estructura

| Archivo | Qué es |
|---|---|
| `index.html` | La página completa (HTML, CSS y JS, sin frameworks). |
| `imagenes/` | Fotos de las flores. Autores y licencias en `imagenes/CREDITOS.md`. |
| `404.html` | Página de error personalizada ("Esta página se ha marchitado"). |
| `flores-amarillas/`, `flores-moradas/`, `flores-azules/`, `san-valentin/`, `dia-de-la-madre/`, `sant-jordi/`, `todos-los-santos-dia-de-muertos/`, `significado-colores-flores/` | Páginas-guía para SEO: una por grupo de búsquedas, cada una con su `index.html`. |
| `guia.css`, `guia.js` | Estilos y cuenta atrás compartidos por las guías. |
| `vercel.json` | Redirige las URLs sin barra final (`/flores-amarillas` → `/flores-amarillas/`). |
| `sitemap.xml`, `robots.txt` | Para que Google encuentre e indexe la web. |
| `DOCUMENTACION.md` | Investigación, decisiones de diseño y cambios del proyecto. |

Web publicada: <https://www.calendariodeflores.com/>

Para ver solo el calendario basta con abrir `index.html` en el navegador. Para navegar entre las guías hace falta un servidor local, por ejemplo `python -m http.server` en la carpeta del proyecto y abrir <http://localhost:8000>.

## Créditos

Las fotos son de Wikimedia Commons con licencias CC BY, CC BY-SA y CC0; el detalle de cada una está en [`imagenes/CREDITOS.md`](imagenes/CREDITOS.md).
