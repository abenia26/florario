# Florario · Documentación del proyecto

Página web interactiva que reúne todas las fechas del año en las que es tradición (o tendencia) regalar flores. Público objetivo: personas de 15 a 25 años.

- Código: `index.html` (HTML + CSS + JS, sin dependencias salvo Google Fonts).
- Fotos: carpeta `imagenes/` (16 fotos de Wikimedia Commons; autores y licencias en `imagenes/CREDITOS.md`).
- Investigación cerrada: 25 de septiembre de 2026.

---

## Fase 0 · Interpretación del encargo

| Pedido | Cómo lo interpreté |
|---|---|
| "Todos los días del año en los que es tradición regalar flores" | Fechas en las que **regalar u ofrecer flores es la costumbre central** del día. Si solo se *ven* flores (festivales, desfiles) no entra. |
| "Trends de TikTok, partes de canciones que hablen de un día en el que se regalan flores" | Fechas nacidas o relanzadas en redes, sobre todo las que dependen de una canción (Floricienta, "Un ramito de violetas"). |
| "Interactiva, minimalista, atractiva, 15–25 años" | Pocas piezas de interfaz pero una pieza visual fuerte (la rueda del año), filtros tipo chip, detalle en ventana modal y funciones "de uso" (guardar, copiar recordatorio, ir al hashtag). |
| Idioma y región | No se indicó país. Como el encargo está en español, el foco es **España + Latinoamérica**, con algunas fechas globales que el público joven conoce por redes o K-pop (Rose Day, Galentine's). |

**Supuestos tomados**
1. Cada fecha lleva su región, porque no todas se celebran en todos los países.
2. Las fechas que cambian cada año (Día de la Madre, Amor y Amistad) se calculan en el navegador para el año elegido, en vez de escribirlas a mano.
3. Tres categorías: **Clásico** (tradición asentada), **Trend** (nacida o impulsada por redes) y **Memoria** (flores para quienes ya no están). La tercera existe porque llevar flores al cementerio es una tradición real, pero su tono es distinto al de un regalo romántico y no debía mezclarse sin avisar.

---

## Fase 1 · Investigación

### Método
- Búsquedas web sobre cada trend conocido y sobre fechas "por color" que circulan en TikTok.
- Contraste de al menos dos medios por trend (prensa de Argentina, México, Perú, Colombia, España).
- Cuando dos fuentes daban fechas distintas, elegí la más citada y guardé la otra como **variante** visible en la ficha.

### Fechas incluidas (23)

| Fecha | Nombre | Flor | Tipo | Región | Canción / origen |
|---|---|---|---|---|---|
| 7 feb | Rose Day | Rosas | Clásico | India | Primer día de la Valentine's Week |
| 13 feb | Galentine's Day | Ramos para amigas | Trend | Global | Serie *Parks and Recreation* (2010) |
| 14 feb | San Valentín | Rosas rojas | Clásico | Global | — |
| 8 mar | Día Internacional de la Mujer | Mimosa / tulipanes | Clásico | Italia, Rusia, Europa del Este | Nota de contexto sobre el 8M en España y Latam |
| 21 mar | Flores amarillas (primavera norte) | Girasoles, tulipanes | Trend | México, Centroamérica, Perú | "Flores amarillas" · Floricienta |
| 23 abr | Sant Jordi | Rosa roja + libro | Clásico | Cataluña | Leyenda del dragón |
| 1 may | Muguet du 1er mai | Lirio de los valles | Clásico | Francia | Carlos IX, 1561 |
| 1.er domingo de mayo | Día de la Madre | Claveles, peonías | Clásico | España, Portugal | — |
| 10 may | Día de las Madres | Rosas, claveles | Clásico | México, Guatemala, El Salvador | Excélsior, 1922 |
| 2.º domingo de mayo | Día de la Madre | Claveles | Clásico | EE. UU., Colombia, Perú, Chile… | Anna Jarvis, 1908 |
| 14 may | Rose Day | Rosas | Clásico | Corea del Sur | Días "14" de pareja |
| 12 jun | Dia dos Namorados | Rosas rojas | Clásico | Brasil | Campaña de 1949 |
| 1 ago | Día de la Novia | Rosas | Trend | México, Perú, Ecuador, Costa Rica | National Girlfriend Day |
| 3.er sábado de sep | Amor y Amistad | Rosas, girasoles | Clásico | Colombia | — |
| 21 sep | Flores amarillas | Girasoles, tulipanes | Trend | Toda Latinoamérica | "Flores amarillas" · Floricienta (2004); viral en TikTok desde 2021 |
| 3 oct | Día del Novio | Flores azules / ramo de Hot Wheels | Trend | México, Perú, Chile, Colombia, España | #NationalBoyfriendDay (2014) |
| 3.er domingo de oct | Día de la Madre | Rosas, liliums | Clásico | Argentina | — |
| 1 nov | Todos los Santos | Crisantemos | Memoria | España y Latam | — |
| 2 nov | Día de Muertos | Cempasúchil | Memoria | México | — |
| 9 nov | Flores moradas | Violetas | Trend | México, Perú, Colombia, España | "Un ramito de violetas" · Cecilia (1975), versión viral de Zalo Reyes |
| 19 nov | Día Internacional del Hombre | Flores azules, girasoles | Trend | Latinoamérica (redes) | "Ellos también merecen flores" |
| 8 dic | Día Nacional de la Nochebuena | Nochebuena (cuetlaxóchitl) | Clásico | México | — |
| 12 dic | Virgen de Guadalupe | Rosas | Clásico | México | Juan Diego, 1531 |

Además, una tarjeta **fuera del calendario**: "Flowers" de Miley Cyrus (2023), el trend de comprarte flores a ti. No tiene fecha, así que no ocupa un día en la rueda.

### Variantes que se muestran dentro de la ficha
- **Flores amarillas:** la cadena viral 22 (primas/tías), 23 (mamá/abuela) y 24 de septiembre (mejor amiga).
- **Flores moradas:** en Colombia circula el 9 de octubre; la letra de la canción dice 9 de noviembre, que es la fecha más citada.
- **Día de la Novia:** algunos países lo celebran el primer domingo de abril.

### Descartes y por qué
| Candidata | Motivo |
|---|---|
| Qixi (San Valentín chino) | Calendario lunar: cambia cada año y no quise publicar fechas que no pude verificar para varios años. |
| Día del Mejor Amigo (8 jun) | No encontré una costumbre de flores asociada, solo mensajes. |
| Día del Maestro | Se regalan flores, pero no es la costumbre central y varía mucho por país. |
| Batalla de Flores (Valencia), Hanami, Fiesta de los Patios | Se ven o se lanzan flores, no se regalan. |
| White Day (14 mar) | El regalo típico son dulces, no flores. |

### Fuentes
- [La Nación · Flores amarillas y Floricienta](https://www.lanacion.com.ar/sociedad/por-que-se-regalan-flores-amarillas-el-21-de-septiembre-origen-significado-y-que-relacion-tiene-con-nid18092026/)
- [BioBioChile · La nueva costumbre en Chile](https://www.biobiochile.cl/noticias/sociedad/viral/2026/09/21/por-que-regalar-flores-amarillas-este-21-de-septiembre-el-origen-de-la-nueva-costumbre-en-chile.shtml)
- [Gestión · Flores amarillas el 21 de marzo](https://gestion.pe/mix/tendencias-mix/por-que-se-regalan-flores-amarillas-a-las-mujeres-el-21-de-marzo-origen-y-significado-de-la-tendencia-primaveral-en-mexico-nnda-nnrt-noticia/)
- [Quién · ¿21 de marzo o 21 de septiembre?](https://www.quien.com/espectaculos/2026/09/21/flores-amarillas-21-de-marzo-o-21-de-septiembre-diferencia)
- [Ponch' & Capricó · Historia del trend de flores amarillas](https://ponchycaprico.com/en/blogs/tendencias-florales/flores-amarillas-por-que-se-regalan-el-21-de-septiembre-y-21-de-marzo-la-historia-completa-de-esta-tendencia-viralflores-amarillas-por-qu-se-regalan-el-21-de-septiembre-y-21-de-marzo-la-historia-completa-de-esta-tendencia-viral)
- [Expansión · Día del Novio, Hot Wheels y flores azules](https://expansion.mx/tendencias/2026/09/24/dia-del-novio-2026-hot-wheels-flores-azules-octubre)
- [La Nación · Por qué el Día del Novio es el 3 de octubre](https://www.lanacion.com.ar/estados-unidos/por-que-se-celebra-el-dia-del-novio-cada-3-de-octubre-nid03102023/)
- [Infobae · Flores moradas el 9 de noviembre](https://www.infobae.com/mexico/2024/11/08/por-que-se-regalan-flores-moradas-el-9-de-noviembre-y-que-significa/)
- [Milenio · Origen de las flores moradas](https://www.milenio.com/virales/9-noviembre-regalan-flores-moradas-origen)
- [El Espectador · Variante del 9 de octubre](https://www.elespectador.com/actualidad/por-que-se-regalan-flores-moradas-en-octubre-historia-del-trend-de-tiktok/)
- [Excélsior · Día de la Novia](https://www.excelsior.com.mx/estilo-de-vida/cuando-es-dia-novia-2026-y-cual-es-polemico-origen)
- [Vanguardia · Flores el 1 de agosto](https://vanguardia.com.mx/informacion/regalar-flores-el-1-de-agosto-el-dia-de-la-novia-se-convierte-en-una-tendencia-muy-romantica-GL16841733)
- [SEMARNAT · Día Nacional de la Nochebuena](https://www.gob.mx/semarnat/articulos/dia-nacional-de-la-nochebuena-289960)
- [México Desconocido · 8 de diciembre](https://www.mexicodesconocido.com.mx/flor-de-noche-buena-8-de-diciembre-flor-de-pascua-flor-de-navidad.html)
- Páginas de descubrimiento de TikTok: [fechas de regalar flores](https://www.tiktok.com/discover/fechas-de-regalar-flores), [flores azules](https://www.tiktok.com/discover/flores-azules-que-significa), [Día del Hombre](https://www.tiktok.com/discover/que-se-regala-el-19-de-noviembre-dia-del-hombre)

Las fechas clásicas (San Valentín, Sant Jordi, muguet, Día de la Madre por país, Dia dos Namorados, Guadalupe, Todos los Santos, Día de Muertos) son de conocimiento general y no dependen de una fuente única.

---

## Fase 2 · Modelo de datos

Todas las fechas viven en un array `EVENTS` dentro del `<script>`. Añadir una fecha es añadir un objeto.

```js
{
  id: "amarillas",               // también sirve como enlace directo: index.html#amarillas
  m: 9, d: 21,                   // fecha fija…
  // rule: { m: 5, wd: 0, n: 2 }, ruleText: "2.º domingo de mayo",  // …o fecha móvil
  name: "Flores amarillas",
  flower: "Girasoles, tulipanes o rosas amarillas",
  color: "amarillo",             // clave de la paleta COLORS
  petals: 10,                    // pétalos del icono de flor
  type: "trend",                 // clasico | trend | memoria
  region: "Toda Latinoamérica",
  tag: "floresamarillas",        // hashtag de TikTok (opcional)
  song: { title, by },           // canción asociada (opcional)
  variant: "…",                  // fecha alternativa (opcional)
  story: "…"                     // por qué se regalan flores ese día
}
```

**Decisiones**
- `rule` en vez de fechas escritas a mano: `nthWeekday(año, mes, díaSemana, n)` calcula "el 2.º domingo de mayo" para cualquier año, así que la página no caduca.
- `color` es una clave y no un hex suelto, para que los filtros por color y el icono usen siempre el mismo tono.
- No cito letras de canciones: solo el título, el intérprete y de qué trata, para no reproducir letras con derechos.

---

## Fase 3 · Concepto y diseño visual

**Nombre:** *Florario* (flor + calendario). Corto, se entiende en todos los países de habla hispana y funciona como marca.

**Concepto:** el año como una **corona de flores**. Una rueda de 365 marcas donde cada fecha es una flor con tallo, del color que se regala ese día. Es la única pieza "llamativa"; todo lo demás es tranquilo, para que el conjunto se lea como minimalista.

**Paleta**
| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--bg` | `#F3F5EF` | `#10130F` | Fondo, blanco con un leve tono verde tallo |
| `--surface` | `#FFFFFF` | `#181C16` | Tarjetas y ventana de detalle |
| `--ink` | `#1B2118` | `#ECF0E6` | Texto, verde casi negro |
| `--muted` | `#5F685A` | `#9CA595` | Texto secundario |
| `--stem` | `#2F6B45` | `#7FC495` | Tallos, marca de "hoy", foco del teclado |

Los únicos colores fuertes son los de las flores (amarillo `#F2C230`, rojo `#D7263D`, rosa `#EE7FA8`, azul `#3F72E0`, morado `#8A4FD8`, naranja `#F28C1B`, blanco `#F4F2EA`). Así el color de la interfaz **es** la información: significa "qué flor se regala".

**Tipografía**
- *Bricolage Grotesque* (títulos y texto): grotesca con carácter, algo irregular, que se siente actual sin ser la típica sans "de app". Encaja con el público joven.
- *DM Mono* (fechas, contadores, etiquetas): números tabulares que alinean en columna y dan el aire de "calendario".

**Maquetación**
- Cabecera: marca + selector de año.
- Hero en dos columnas (una en móvil): titular, cuenta atrás a la próxima fecha y la rueda.
- Barra de filtros entre líneas finas.
- Lista agrupada por mes: nombre del mes a la izquierda y tarjetas a la derecha (en móvil se apila).
- Tarjeta final "Fuera del calendario" y pie con fuentes.

**Qué evité a propósito:** degradados morado-azul, emojis como iconos de sección, todo centrado, crema con serif. Los iconos de flor se dibujan en SVG con código (pétalos elípticos rotados), así cada fecha tiene su propia flor sin cargar imágenes.

---

## Fase 4 · Interacción

| Función | Detalle | Por qué |
|---|---|---|
| **Cuenta atrás** | "8 días para · Día del Novio". Pulsa para ver la ficha. | Responde a la pregunta real del público: *¿cuándo toca la próxima?* |
| **Rueda del año** | Pasar el cursor o enfocar con teclado muestra nombre y fecha; clic abre la ficha. Marca de "hoy". | Da la visión del año entero de un vistazo. |
| **Filtros por tipo** | Todas · Clásicas · Trends · Memoria · Guardadas, con contador. | Quien busca trends no tiene que leer las tradicionales. |
| **Filtros por color** | Selección múltiple con iconos de flor. | En TikTok las fechas se identifican por color ("las amarillas", "las moradas"). |
| **Ficha de detalle** | Fecha completa, días que faltan, qué se regala, historia, canción, variante. | Toda la información de una fecha en un solo sitio. |
| **Guardar** | Corazón por fecha, guardado en el navegador (`localStorage`). | Hacer tu propia lista ("las fechas que no puedo olvidar"). |
| **Copiar recordatorio** | Copia "21 de septiembre · Flores amarillas: … #floresamarillas". | Para pegarlo en el calendario del móvil o mandarlo por chat. |
| **Ver #hashtag** | Enlace a la etiqueta de TikTok en trends. | Lleva directo a los vídeos del trend. |
| **Selector de año** | ‹ 2026 › | Recalcula fechas móviles y días de la semana. |
| **Enlace directo** | `index.html#moradas` abre esa ficha. | Compartir una fecha concreta. |

---

## Fase 5 · Implementación técnica

- **Un solo archivo** sin frameworks: carga rápido en móvil y se puede abrir con doble clic.
- **Rueda en SVG generado por JS:** 365/366 marcas, etiquetas de mes y flores. Si dos fechas caen a menos de 5 días, la segunda sube a un anillo exterior (hasta 3 anillos) para que no se pisen (ej.: 13 y 14 de febrero, 1 y 2 de noviembre).
- **Fechas sin errores por horario de verano:** las diferencias de días se calculan con `Date.UTC`.
- **Temas claro y oscuro:** tokens CSS en `:root`, redefinidos con `prefers-color-scheme` y con `data-theme`.
- **Accesibilidad:** las flores de la rueda son botones con `tabindex`, `role="button"` y `aria-label` completo; Enter y Espacio las abren; foco visible; `prefers-reduced-motion` desactiva animaciones; la ventana usa `<dialog>` nativo (Esc para cerrar).
- **Robustez:** `localStorage` y `clipboard` van dentro de `try/catch`. Si no se puede copiar, se muestra el texto para copiarlo a mano.
- **Responsive:** grid con `auto-fill` y `minmax`, una columna en móvil y margen lateral mínimo de 16 px.

---

## Fase 6 · Verificación

Revisado sobre el código:
- Fechas móviles para 2026: 1.er domingo de mayo = 3 may; 2.º domingo de mayo = 10 may (coincide con México, la rueda las apila); 3.er sábado de septiembre = 19 sep; 3.er domingo de octubre = 18 oct.
- La cuenta atrás busca en el año actual y el siguiente, así que en diciembre salta bien a febrero.
- Si un filtro deja la lista vacía, aparece un mensaje con botón "Ver todas".

Pendiente de probar en dispositivos reales: Safari iOS (clipboard y `<dialog>`) y lectores de pantalla.

---

## Fase 7 · Siguientes pasos

1. **Añadir el país del usuario** y ordenar primero sus fechas.
2. **Exportar a calendario (.ics)** para las fechas guardadas.
3. **Revisar trends cada trimestre:** los trends de color aparecen rápido (las moradas y azules son de 2023–2024). Basta con añadir objetos a `EVENTS`.
4. Valorar Qixi y otras fechas lunares con una tabla de fechas verificadas por año.

---

## Fase 8 · Rediseño: más color, fotos y explorador por meses (28 sep 2026)

Qué se pidió: página más dinámica, bonita y entretenida; carpeta de imágenes con fotos de todas las flores; la flor colocada en el propio día; contenedores más bonitos sin la lista larga que obliga a bajar; más color.

| Cambio | Detalle |
|---|---|
| **Carpeta `imagenes/`** | 16 fotos (rosa roja, rosa rosa, ramo de rosas, ramo de tulipanes, mimosa, girasol, muguet, clavel, peonía, lilium, hortensia azul, crisantemo, cempasúchil, violeta, nochebuena, ramo silvestre). Todas con licencia libre (CC BY, CC BY-SA o CC0) y en 960 px de ancho. |
| **Foto en el propio día** | Cada fecha tiene `img` en `EVENTS`. En el calendario la casilla del día se rellena con la foto de su flor y lleva el número encima. |
| **Explorador por meses** (sustituye a la lista vertical) | Tira de 12 meses con puntos del color de sus flores y contador, y un panel con el calendario del mes y una ficha destacada con foto grande. Se cambia de mes con la tira, las flechas, las teclas ← → o deslizando en el móvil. Si un día tiene varias fechas, cada toque pasa a la siguiente. |
| **Cinta "Próximas"** | Las 10 fechas más cercanas pasan en bucle con su foto. Se pausa al pasar el ratón y es estática si el usuario pide menos movimiento. |
| **Rueda con meses de color** | Cada mes es un sector de color; al pulsarlo se abre ese mes en el explorador. El tooltip de las flores muestra la foto. |
| **Ficha con foto** | Cabecera con la foto, crédito del autor y una línea del color de la flor. |
| **Flor al azar** | Botón que abre una fecha aleatoria que respete los filtros. |
| **Más color** | Fondo con manchas suaves rosa, amarillo, lila y turquesa; titular con degradado rojo-naranja-amarillo; un color por mes (`MONTH_COLORS`) que tiñe la tira, el panel y la rueda; filtros de tipo con su color; cuenta atrás teñida del color de la próxima flor. Todo tiene versión en modo oscuro. |

**Paleta por mes**: ENE `#7C9CF0` · FEB `#E8475F` · MAR `#F2C230` · ABR `#F07A5A` · MAY `#EE7FA8` · JUN `#E4572E` · JUL `#2BB3A3` · AGO `#F59E6B` · SEP `#F2B705` · OCT `#3F72E0` · NOV `#8A4FD8` · DIC `#C8102E`. El texto sobre cada color se elige solo (oscuro o blanco) según su luminancia.

**Verificación** (Chrome sin interfaz): escritorio a 1280 px, móvil a 390 px y modo oscuro revisados con capturas. Un test automático recorrió los 12 meses, el paso de diciembre a enero del año siguiente, los días con varias fechas, guardar, el filtro de guardadas, el mes vacío, el filtro por color, los sectores de la rueda, la flor al azar y el cambio de año, sin errores de JavaScript.

---

## Fase 9 · SEO y páginas-guía (28 sep 2026)

**Problema de partida.** Toda la web era una sola URL y el contenido de cada fecha se pintaba con JavaScript dentro de una ventana. Los enlaces `#amarillas`, `#moradas`… son anclas: para Google son la misma página, así que no había ninguna URL que pudiera posicionar para "flores amarillas 21 de septiembre" o "flores moradas 9 de noviembre".

**Solución.** Ocho páginas estáticas, una por grupo de palabras clave, con el mismo diseño (tokens, tipografías, manchas de color, modo oscuro). Cada una usa solo información que ya estaba en `EVENTS` o en la investigación de la Fase 1, ampliada con contexto (qué flores regalar, significado del color, preguntas frecuentes).

### Mapa de palabras clave

| URL | Palabra clave principal | Secundarias |
|---|---|---|
| `/` | calendario de flores, fechas para regalar flores | cuándo se regalan flores, días para regalar flores |
| `/flores-amarillas/` | por qué se regalan flores amarillas el 21 de septiembre | flores amarillas 21 de marzo, cuándo se regalan flores amarillas, qué significan las flores amarillas, Floricienta flores amarillas, 22 23 24 de septiembre |
| `/flores-moradas/` | por qué se regalan flores moradas el 9 de noviembre | persona morada, un ramito de violetas, flores moradas 9 de octubre, significado flores moradas |
| `/flores-azules/` | flores azules 3 de octubre | día del novio, ramo de Hot Wheels, flores azules significado, 19 de noviembre día del hombre flores |
| `/san-valentin/` | flores para San Valentín | qué flor se regala en San Valentín, Galentine's Day, Dia dos Namorados, Amor y Amistad Colombia, Día de la Novia 1 de agosto |
| `/dia-de-la-madre/` | flores para el Día de la Madre | cuándo es el Día de la Madre 2027 (España, México, Argentina, Colombia…), clavel Día de la Madre |
| `/sant-jordi/` | por qué se regala una rosa y un libro en Sant Jordi | leyenda de Sant Jordi, rosa de Sant Jordi, 23 de abril |
| `/todos-los-santos-dia-de-muertos/` | flores para Todos los Santos | flores de Día de Muertos, cempasúchil, crisantemo, flores para la ofrenda |
| `/significado-colores-flores/` | significado de los colores de las flores | qué significa regalar flores amarillas / azules / moradas / rojas / blancas |

Método: búsquedas de las consultas reales que responden los medios y floristerías que ya posicionan (patrones "por qué se regalan flores X el [fecha]", "cuándo se regalan flores X", "qué significa regalar flores X") y comparación con las fechas que tiene Florario. No se añadieron fechas nuevas al calendario (por ejemplo, el "29 de febrero de flores amarillas" que citan algunos medios) para no contradecir la investigación de la Fase 1.

### Qué lleva cada guía
- `<title>` de unos 60 caracteres y `description` de 135 a 165, con la palabra clave al principio.
- URL canónica, Open Graph con foto y `twitter:card`.
- Datos estructurados JSON-LD: `Article`, `BreadcrumbList` y `FAQPage` (las preguntas son las mismas que se ven en la página).
- Un solo `h1`, secciones con `h2` e índice con anclas (Google puede mostrarlas como enlaces en el resultado).
- Cuenta atrás a la fecha (`guia.js`), que enlaza a la ficha en el calendario (`../#id`).
- Enlaces internos: migas de pan, "Más fechas para regalar flores", pie con todas las guías y enlaces dentro del texto.
- Créditos de las fotos usadas en esa página (lo exigen las licencias CC BY-SA).

### Cambios en la portada
- `title` y `description` orientados a "fechas para regalar flores" y "calendario de flores".
- `og:image`, `og:site_name`, `twitter:card` y JSON-LD `WebSite`.
- Sección **Guías** (HTML estático, rastreable) con una tarjeta por guía, entre "Fuera del calendario" y el pie.
- En la ficha de cada fecha, botón **Leer la guía →** (mapa `GUIDES` en el `<script>`). Las fechas sin guía propia (8M, muguet, Nochebuena, Guadalupe) llevan a su color en la guía de colores.
- `sitemap.xml` con las 9 URLs y `vercel.json` con `trailingSlash: true` para que no haya dos URLs por guía.

### Mantenimiento
- **Cada año:** la guía del Día de la Madre tiene una tabla con los dos años siguientes (2027 y 2028) y la de San Valentín cita la fecha de Amor y Amistad de 2027. Hay que actualizarlas y cambiar `lastmod` en `sitemap.xml` y la fecha de "Última revisión" de cada guía.
- **Añadir una guía:** copiar la carpeta de una guía, cambiar textos, canónica, JSON-LD y color (`<body class="c-…">`, clases en `guia.css`), añadir su tarjeta en `index.html`, su entrada en `GUIDES` y su URL en `sitemap.xml`.
- **Después de publicar:** dar de alta el dominio en Google Search Console, enviar `sitemap.xml` y pedir la indexación de las guías. Conviene publicar o actualizar cada guía unas semanas antes de su fecha (flores amarillas a principios de septiembre y marzo, azules a mediados de septiembre, moradas a mediados de octubre).

**Verificación.** Capturas con Chrome sin interfaz: escritorio a 1280 px, móvil a 390 px (en iframe) y modo oscuro. Un script comprobó que no hay enlaces locales ni anclas rotas, que los 9 bloques JSON-LD son JSON válido y que cada página tiene un solo `h1`. Se corrigieron dos fallos: el botón del índice heredaba el contador de los enlaces, y la tabla del Día de la Madre desbordaba la columna en móvil.

---

## Fase 10 · SEO para “calendario de flores” (28 sep 2026)

**Problema de partida.** La web no aparecía en el top 10 de Google para “calendario de flores”. La portada estaba orientada a “fechas para regalar flores”, la lista de fechas solo existía dentro del JavaScript, no había contenido de flores de temporada (la otra intención de esa búsqueda), ni páginas por mes o por flor, ni señales de confianza (autor, contacto, páginas legales).

### Qué se hizo

| Área | Cambio |
|---|---|
| **Palabra clave** | Title “Calendario de flores 2026: qué flor regalar y cuándo \| Florario” (63 caracteres) y H1 “Calendario de flores: qué flor regalar en cada fecha del año”. |
| **Contenido rastreable** | La portada incluye en HTML estático la tabla completa de fechas (fecha con `<time datetime>`, flor, color, países y por qué), la tabla **Calendario de flores de temporada** (12 meses × España, México y Centroamérica, Argentina/Chile/Uruguay), descargas, países, guías, flores y FAQ. |
| **Nuevas páginas** | 12 meses (`/enero/`…`/diciembre/`), 14 flores (`/rosa/`, `/girasol/`, `/tulipan/`, `/peonia/`, `/clavel/`, `/margarita/`, `/lilium/`, `/hortensia/`, `/violeta/`, `/crisantemo/`, `/cempasuchil/`, `/mimosa/`, `/lirio-de-los-valles/`, `/nochebuena/`), 9 guías nuevas (8M, Día del Padre, Día del Maestro, 21 de marzo, Día de la Novia, Nochebuena, cumpleaños, aniversarios, condolencias), 6 países con hreflang y 3 índices (`/meses/`, `/flores/`, `/guias/`). Todas las de mes y flor superan las 600 palabras. |
| **Nuevas fechas** | Día del Padre (19 de marzo y 3.er domingo de junio) y Día del Maestro (15 de mayo, México y Colombia): 26 fechas en total. |
| **FAQ** | Preguntas frecuentes visibles y en `FAQPage` en la portada y en cada guía, flor, mes y país. |
| **Imágenes** | AVIF y WebP en 960/480 px y miniatura de 160 px, nombres descriptivos (`girasol-amarillo-960.avif`), `alt` con la flor y su contexto en todas las imágenes, `srcset`/`sizes` y carga diferida. |
| **Datos estructurados** | `Organization` (con logo), `WebSite`, `BreadcrumbList`, `FAQPage`, `ItemList` de `Event` en la portada, `Event` por fecha en meses, países y guías, `Article` con autor (`Person`) y `dateModified`, `CollectionPage` en índices y `AboutPage`/`ContactPage`. |
| **Países** | `/espana/`, `/mexico/`, `/argentina/`, `/colombia/`, `/chile/`, `/peru/` con `hreflang` es-ES, es-MX, es-AR, es-CO, es-CL, es-PE, `es` y `x-default` (la portada), recíprocos en todas. |
| **Sitemap** | 56 URLs con `lastmod` e `image:image`. |
| **Confianza y marca** | Sobre Florario (método de investigación), Contacto, Política de privacidad y Aviso legal; firma del autor y fecha de actualización en cada página; marca “Florario – Calendario de flores” en `og:site_name`, cabecera, pie y JSON-LD; favicon SVG y logo PNG. |
| **Navegación** | Cabecera fija con menú Fechas · Por mes · Por flor · Colores · Guías, y pie con enlaces a todos los meses, flores, guías, países y páginas legales. |
| **Captación** | “Recuérdamelo”: `.ics` por fecha con aviso 3 días antes (se repite cada año) y calendario completo suscribible; enlace a Google Calendar. PDF del calendario 2026 y 2027 (A4, 2 páginas). Imágenes de Pinterest en `marketing/pines/` y plan de enlaces, prensa, Pinterest, TikTok y newsletter en `marketing/PLAN-SEO-Y-CAPTACION.md`. |

### Arquitectura
Se sustituyó la edición a mano por un generador (`_build/build.py`) con una sola fuente de datos (`_build/datos.py`). Las 8 guías existentes se migraron automáticamente a fragmentos (`_build/paginas/`) conservando su texto. El `EVENTS` del JavaScript de la portada se inyecta desde los mismos datos, así la parte interactiva, las tablas estáticas, los PDF, los `.ics` y el sitemap no pueden contradecirse.

### Decisiones
- **Title:** el propuesto (“…qué flor regalar cada fecha y de temporada | Florario”) superaba los 80 caracteres; se acortó a 63 manteniendo la palabra clave al principio. “De temporada” va en el H2 de la sección y en la descripción. En las demás páginas la marca solo se añade si el title cabe en ~65 caracteres.
- **Hreflang:** se hizo con páginas por país con contenido propio (fechas de ese país) en lugar de duplicar la web por idioma, que habría generado contenido duplicado.
- **Nochebuena:** la guía del 8 de diciembre y la página de la flor son la misma URL (`/nochebuena/`) para no competir entre sí.
- **Event:** Google no muestra resultados enriquecidos de eventos para fechas festivas; el marcado se incluye porque ayuda a entender las fechas, sin esperar rich snippets.
- **Newsletter:** no se activó porque necesita un proveedor de correo y actualizar la privacidad; mientras, los `.ics` cubren el “Recuérdamelo”.

### Pendiente (necesita al titular)
- Rellenar autor, titular, NIF, dirección y correo en `SITE` (`_build/datos.py`). El build avisa mientras falten.
- Search Console, Bing, Pinterest, TikTok, prensa y enlaces: pasos en `marketing/PLAN-SEO-Y-CAPTACION.md`.

### Verificación
El build comprueba en las 56 páginas: enlaces internos y anclas, JSON-LD válido, un solo H1 y `alt` en todas las imágenes (sin errores). Capturas con Chrome sin interfaz de portada, ficha de fecha, mes, guía, aviso legal y móvil a 390 px (en iframe), y revisión de los dos PDF.

---

## Fase 11 · Auditoría SEO: tabla rodante, sin `Event`, fechas por página, fuentes locales, imprimible, compartir y guías nuevas (28 sep 2026)

**Punto de partida.** Una auditoría externa puso a la web un 6,7/10. La tabla de la portada estaba anclada en 2026 y empezaba en febrero, cuando ya habían pasado 18 de las 26 fechas. El marcado `Event` presentaba a Florario como organizador de festividades. Todas las páginas decían «Actualizado» con la misma fecha. Google Fonts bloqueaba el primer pintado. La autoría no mostraba experiencia en flores y la web no respondía a la búsqueda de «calendario para imprimir». Tampoco había nada que compartir o enlazar, y Amor y Amistad y la Virgen de Guadalupe no tenían guía.

### Qué se hizo

| Área | Cambio |
|---|---|
| **Tabla rodante** | `date_table(..., rolling=True)` ordena por la próxima fecha respecto a la del build (`HOY`) y cubre los 12 meses siguientes con el año real de cada fila. Se usa en la portada, los países, los meses y las guías. El H2 se calcula («Próximas fechas para regalar flores (oct 2026 – sep 2027)»). |
| **Año automático** | Ya no hay `SITE["year"]`. Desde el 1 de octubre, title, og:title, description y H1 dicen «Calendario de flores {Y}-{Y+1}». Los PDF son siempre del año del build y del siguiente. `FLORARIO_HOY=AAAA-MM-DD` permite probar otra fecha. |
| **Sin `Event`** | Se quitó `event_ld()`. Las fechas van como `ItemList` de `ListItem` (nombre legible y URL de la guía) en la portada, los meses, los países y las guías. `FAQPage` se mantiene. |
| **Fechas por página** | Cada fragmento lleva `published` y `updated` (rellenados con `git log`; todo el historial es del 28 sep 2026). Se usan en la firma («Publicado el…» o «Actualizado el…»), `datePublished`/`dateModified`, `article:modified_time` y `lastmod`. Los índices toman la fecha más reciente de sus páginas y la portada, la de todo el sitio. El build avisa si un fragmento cambia y su `updated` es antiguo. |
| **Fuentes locales** | Bricolage Grotesque (variable 400–800) y DM Mono 400/500, subconjunto latin, en `/fuentes/` con `@font-face` en `comun.css`, precarga del woff2 principal y caché de un año. Ningún HTML carga ya Google Fonts (tampoco la 404 ni el PDF). |
| **Imágenes** | `sizes` de la foto principal ajustado al CSS real: 380 px en escritorio y `min(300px, 100vw - 40px)` en móvil. Nuevo `alt_corto` en `IMAGES` para miniaturas, tarjetas y el JS de la portada, así el `alt` ya no contradice la fecha (p. ej., el girasol del Día del Padre). |
| **E-E-A-T** | Biografía del autor ligada al proyecto. `SITE["reviewer"]` y `SITE["author_sameAs"]` quedan como marcadores. `AUTHOR` lleva `description` y `sameAs`. Si hay revisor, la firma muestra «Revisado por…» y el JSON-LD, `reviewedBy`. /sobre-florario/ pasa a primera persona y tiene la sección «Quién revisa el contenido». |
| **Imprimible** | El PDF tiene una portada A4 con la rueda del año (meses de color, marcas de días y una flor por fecha, con contorno para imprimir en blanco y negro) y una flor pequeña en cada mes: 3 páginas en total. `render_preview()` hace la vista previa JPG (1191 × 1685, unos 175 KB): una captura con el navegador sin interfaz, pasada a JPEG con un `<canvas>`, sin librerías. Nueva página /calendario-de-flores-para-imprimir/ con vistas previas, cómo imprimir, ideas y condiciones de uso. |
| **Compartir** | WhatsApp (enlace `wa.me`, funciona sin JS) y «Compartir» nativo o «Copiar enlace» en todas las guías, flores, meses, países y el imprimible, y en la ficha de cada fecha de la portada. No hay `utm_source` porque la web no tiene analítica. |
| **Widget** | `/widget/`: próxima fecha y cuenta atrás, `noindex`, fuera del sitemap, 6 KB, sin dependencias ni cookies; `?pais=mx` filtra por país. |
| **Prensa** | /prensa/: qué es Florario, cifras sacadas de `datos.py` (tabla por país incluida), temas por fecha, logo y portadas descargables, código del widget y contacto. Enlazada desde /contacto/ y el pie. |
| **Guías nuevas** | /amor-y-amistad/ (Radio Nacional de Colombia, El Tiempo, Infobae) y /virgen-de-guadalupe/ (Milenio, EWTN, Infobae), de más de 950 palabras cada una. Los eventos `amor-amistad-co` y `guadalupe` ya enlazan a ellas. |
| **Países** | `og:locale` por país (`es_MX`, `es_AR`…) con `og:locale:alternate` para el resto. Nuevo índice /paises/, «Países» en el menú y la miga de pan de los países apuntando a él. |
| **Limpieza** | Los títulos del pie son `<p class="foot-h">` (sin H2 en el pie). `strip_tags()` ya no deja espacio antes de la puntuación («Flores de octubre: …»). `--muted` pasa a `#525A4D` (4,9:1 incluso sobre la mancha rosa del fondo). Los meses vacíos usan color en lugar de opacidad. Sin `aria-label` que contradiga el texto visible (logo, pestañas de mes, «próxima fecha», foto destacada). Redirección 308 de `/index.html` y `/…/index.html`. |

### Verificación
- Build del 28 sep 2026: 61 páginas, sin «PROBLEMAS». Primera fila de la portada: Día del Novio (3 oct 2026); última: flores amarillas (21 sep 2027).
- Simulaciones: con `FLORARIO_HOY=2026-10-05` el title es «Calendario de flores 2026-2027…»; con `2027-02-01`, «Calendario de flores 2027…».
- Ningún `"@type": "Event"`; JSON-LD válido en todas las páginas; `og:locale` `es_MX` en /mexico/; ningún H2 en el pie; ningún headline con « :».
- Lighthouse móvil en local: accesibilidad 100 en / y en /octubre/, sin fuentes en *render-blocking*.
- PDF de 3 páginas; vista previa por debajo de 250 KB; menú sin scroll horizontal a 360 px (medido en iframe); widget revisado a 320 × 200.

### Pendiente
- **Titular:** rellenar `SITE["reviewer"]` cuando haya un florista que revise el contenido y `SITE["author_sameAs"]` con los perfiles públicos. El build avisa mientras queden corchetes.
- **Fechas:** como todo el historial es del mismo día, todas las páginas tienen hoy el mismo `published` y `updated`. A partir de ahora, cada revisión debe cambiar solo el `updated` de su página.
- ~~Imagen principal en móvil~~ Hecho después: variantes de 640 px en AVIF y WebP (Pillow, desde los JPG originales) en todos los `srcset`; Lighthouse ya no marca /octubre/.
- ~~Vercel~~ Comprobado: `calendariodeflores.com` ya redirigía con 308 a www en el proyecto `florario-wq96`. El salto previo de http a https lo hace Vercel siempre. Se borró el proyecto duplicado `florario` y `florario-wq96.vercel.app` redirige con 308 a www.

### Automatización (28 sep 2026)
- **`.github/workflows/regenerar.yml`:** GitHub Actions ejecuta el build cada día a las 06:30 UTC (con `--pdf` solo si falta el PDF de algún año). Si hay cambios, hace commit con la identidad de git del titular y push, lo que despliega en Vercel. En CI, Chrome se lanza con `--no-sandbox`.
- **IndexNow:** `_build/indexnow.py` avisa a Bing, Yandex y otros de las URL del sitemap o de las que cambian en un commit; la clave pública está en la raíz. Google no usa IndexNow: para Google está Search Console.
- **Widget:** el HTML estático ya no lleva la cuenta de días (la pone el JavaScript), para que la regeneración diaria no cambie el archivo cada día.

---

## Fase 12 · Versión en inglés (29 sep 2026)

Objetivo: que la web se pueda leer en otro idioma para llegar a un público internacional.

### Qué se hizo
| Parte | Cambio |
|---|---|
| **Estructura** | La web se genera dos veces: español en `/` (sin cambios de URL) e inglés en `/en/`, con slugs en inglés (`/en/rose/`, `/en/valentines-day/`, `/en/months/`…). La tabla de equivalencias está en `SLUGS` de `_build/datos_en.py`. |
| **Selector de idioma** | «ES \| EN» en la cabecera de todas las páginas; lleva a la misma página en el otro idioma. En móvil se queda junto a la marca y el menú baja a su fila. |
| **Textos** | Las 56 páginas de `_build/paginas/` traducidas en `_build/paginas/en/`. Datos (fechas, flores, guías, meses, fotos, temporada) en `datos_en.py`. Textos fijos del generador con `T("español", "english")`; los de la portada, con `<!--es-->…<!--en-->…<!--/-->` y `t()` en el JavaScript. Inglés americano (fechas «February 14», «color», «mom»). |
| **SEO** | `hreflang` es / en / x-default en cada página. La portada y los países mantienen su grupo es-ES, es-MX… y le suman la portada inglesa. `og:locale` en_US en inglés y `es_ES` como alternativo. JSON-LD con `inLanguage` del idioma. El sitemap incluye las 122 URL. |
| **Descargas** | PDF, vista previa y `.ics` propios en inglés: `/en/downloads/flower-calendar-AAAA.pdf`, `/en/downloads/flower-calendar.ics` y `/en/reminders/*.ics` (UID distinto para no pisar el calendario español). El build imprime los PDF que falten aunque no se pase `--pdf`, así el inglés se genera solo en la primera ejecución y en la regeneración diaria. |
| **Otros** | `guia.js` y la página 404 detectan el idioma (`<html lang>` o la ruta `/en/`). `vercel.json` sirve los `.ics` ingleses como `text/calendar`. El widget sigue solo en español. |

### Decisiones
- **Traducción propia y no automática** (Google Translate): una traducción automática no se indexa, falla con nombres de fechas y flores, y no daría tráfico de otros países.
- **Nombres propios en español** donde así se conocen: Sant Jordi, Amor y Amistad, cempasúchil, «Flores amarillas», «Un ramito de violetas». Se explican entre paréntesis la primera vez.
- ~~**Las páginas de país en inglés no llevan `hreflang`**, porque `/mexico/`, `/espana/`… ya son las versiones es-XX de la portada y un mismo URL no puede estar en dos grupos.~~ Cambiado en la fase 16: cada página de país forma pareja con su traducción (`/mexico/` ↔ `/en/mexico/`).
- **Aviso legal y privacidad** en inglés indican que, si hay discrepancia, prevalece la versión española.

### Verificación
- Build con `FLORARIO_HOY=2026-09-29`: 122 páginas, sin «PROBLEMAS» (enlaces, anclas, JSON-LD, `alt`, H1 y traducciones completas).
- Las páginas españolas salen idénticas a las de antes salvo lo añadido a propósito: `hreflang`, `og:locale:alternate` en_US y el selector de idioma. El `.ics` y el HTML del PDF español no cambian.

---

## Fase 13 · Más flores y guías (1 oct 2026)

Objetivo: cubrir búsquedas con mucho volumen que la web no tenía (flores muy buscadas, colores, ocasiones y la temporada de Navidad), a partir de los datos de Search Console.

### Qué se hizo
| Parte | Cambio |
|---|---|
| **Flores nuevas (8)** | Dalia, orquídea, lavanda, gerbera, ranúnculo, alcatraz (cala), jazmín y gladiolo, en español y en inglés (`/en/dahlia/`, `/en/orchid/`, `/en/lavender/`, `/en/gerbera/`, `/en/ranunculus/`, `/en/calla-lily/`, `/en/jasmine/`, `/en/gladiolus/`). Sus nombres ya estaban en la tabla de temporada, así que ahora se enlazan solos desde los meses. |
| **Guías nuevas (7)** | Flores de Navidad, flor de cada mes de nacimiento, flores blancas, rojas y rosas, flores para graduación y flores para boda, en los dos idiomas. |
| **Fotos** | 8 fotos nuevas de Wikimedia Commons, con sus versiones web y sus créditos en `imagenes/CREDITOS.md`. |
| **Temporada** | Se añade la cala a abril y mayo en España (florece en primavera), en `datos.py` y `datos_en.py`. |

### Verificación
- Build del 1 oct 2026: 152 páginas, sin «PROBLEMAS» y ninguna página de flor por debajo de 600 palabras. El sitemap tiene 152 URL.
- Los meses de temporada que dice el texto de cada flor coinciden con los de la tabla de temporada.

---

## Fase 14 · Títulos y respuestas para las búsquedas reales (1 oct 2026)

Objetivo: convertir en clics las impresiones de Search Console. Casi todas venían de "cuándo se regalan flores azules a los hombres" y "cuándo es el día de las flores moradas", pero los títulos respondían a "por qué" y el H1 de las flores azules hablaba del "Día del Novio", que casi nadie busca.

### Qué se hizo
| Página | Cambio |
|---|---|
| `/flores-azules/` | Title, H1 y descripción con "día de las flores azules para hombres" y "3 de octubre"; entradilla que responde en la primera frase; sección "¿Cuándo es el día de las flores azules?" con tabla (3 oct y 19 nov) y sección de Perú; preguntas frecuentes nuevas (hombres, qué se regala el 3 de octubre, Perú, rosas azules). |
| `/flores-moradas/` | Title y H1 "Día de las flores moradas"; respuesta directa al principio, tabla por país y preguntas sobre Perú, qué se regala el 9 de noviembre y flores violetas. |
| `/octubre/`, `/noviembre/` | Title "Qué flores se regalan en octubre/noviembre". |
| `/peru/` | Title "Fechas para regalar flores en Perú" y descripción con las fechas azul y morada. |
| `/hortensia/` | Pregunta "¿Cuándo se regalan hortensias?". |
| Portada | Title "Calendario de flores 2026-2027: fechas para regalar flores", descripción con las próximas fechas y pregunta sobre las flores azules para hombres. |

Solo español: las consultas eran todas en español.

---

## Fase 15 · Botones con el color de cada fecha (1 oct 2026)

Objetivo: dar más color y personalidad a la web para el público de 15 a 30 años sin cambiar la paleta base (crema, tinta oscura y pasteles), que ya encaja con la estética de Pinterest y TikTok.

| Parte | Cambio |
|---|---|
| **Botón principal** (`.btn.primary`) | Deja de ser casi negro: toma el color de la página (`--btn` en cada clase `.c-*` de `guia.css`) con texto de contraste ≥ 4.5:1. El azul se oscurece a `#3A6AD8` y el blanco usa el verde tallo `#2F6B45`; amarillo, naranja y rosa llevan texto oscuro. Sin color propio (hubs, páginas de información) se usa el **fucsia de marca** `#B0306A`. |
| **Flecha de la cuenta atrás y nota musical** | Mismo color que el botón. |
| **Portada** | El botón "Ver ficha" y el de la ventana de cada fecha toman el color de esa fecha (`paintBtn()` en `plantilla-inicio.html`, que usa `textOn()` para el texto). |
| **Tablas** | Espacio entre una tabla y el párrafo que la sigue (`.prose .table-wrap + p`). |

Se mantienen neutros (tinta) el menú, el selector de idioma y los filtros, para que el color quede para lo que se puede pulsar en cada página.

---

## Fase 16 · Mejoras de la auditoría para el público de 15 a 30 años (3 oct 2026)

Objetivo: aplicar la auditoría de UX, contenido y SEO pensada para quien llega desde el móvil (TikTok, Instagram, Pinterest, Google). Todo se comprobó a 390 × 844 con Chrome sin interfaz.

### Obligatorias
| Punto | Qué se hizo | Comprobación |
|---|---|---|
| **Contenido para pasar a la acción** | En flores amarillas, azules y moradas, San Valentín, Día de la Madre y Día de la Novia (ES y EN), tres secciones nuevas: «Qué escribir en la tarjeta» (12 mensajes en 4 tonos con botón Copiar), «Según tu presupuesto» (una flor, ramo pequeño, ramo grande, sin precios) y «Hazlo tú» (materiales y pasos: ramo de Hot Wheels, girasoles de papel, flores de limpiapipas, envolver el ramo, tarro decorado y caja de flores). Los mensajes van en la cabecera del fragmento (`"mensajes"`) y el marcador `<!--@MENSAJES-->` los pinta; el build avisa si alguno pasa de 140 caracteres. | Los tres H2 en las 12 páginas y en el índice. |
| **La respuesta primero en móvil** | Entradillas que empiezan por la fecha en todas las guías con fecha (27 en total contando las dos lenguas). En móvil: foto en franja de 124 px, ficha en tarjetas que se deslizan en horizontal, índice plegado (`guia.js` lo abre en escritorio), «Ver en el calendario» al final, firma en una línea y miga de pan en una línea. «En esta página» ya no es un H2. | Primer H2 de las 52 guías por debajo de 1.000 px (antes, 1.692–1.899). |
| **Compartir** | WhatsApp y Compartir bajo la ficha; barra fija inferior en móvil (WhatsApp · Recuérdamelo) que aparece al hacer scroll y se esconde en el pie; `navigator.share` con texto (fecha, flor y gancho). `_build/pines.py` genera ahora, y publica, la imagen `og` 1200 × 630 de cada página (`imagenes/og/`) y el pin 1000 × 1500 y la story 1080 × 1920 de cada guía y mes (`imagenes/pines/`), con «Guárdalo en Pinterest» y «Descargar para tu story». El build avisa si falta alguna. | WhatsApp en la segunda pantalla de todas las guías. |
| **Portada más corta** | En móvil: 5 próximas fechas, 2 meses de temporada y 6 guías y 6 flores, con botón «Ver todas» (el HTML completo sigue en la página); meses en dos columnas; pie con los enlaces en línea; foto de la próxima fecha en la tarjeta «¡Hoy!»; «Flor al azar» y el año, bajo la rueda. Menú: «Guías» en segunda posición y los 6 enlaces caben a 390 px (en inglés, «Months» y «Flowers»). «Toca hoy» → «Es hoy». Se corrigió la foto de «Cualquier día», que salía estirada por el atributo `height`. | Portada: 23.572 → ~11.630 px (ES) y ~11.550 (EN); con otras fechas de build, menos de 11.900. |
| **Recuérdamelo en Android** | Junto a cada `.ics`, «Añadir a Google Calendar» con repetición anual (`recur=RRULE…`, también las fechas móviles como el 3.er domingo de octubre). Ficha de la portada con 3 acciones visibles: Recuérdamelo (`.ics` o Google Calendar), WhatsApp y Más (Guardar, Copiar texto, Compartir, #hashtag). Se arregló un fallo antiguo: la variable `t` del botón tapaba la función de traducción y «Copiar» no avisaba. | Día de la Madre en Argentina: 18/10/2026 y `BYDAY=3SU`. |
| **Metadatos** | 121 descriptions reescritas (≤ 155 caracteres, empezando por la respuesta) y 18 titles (≤ 60). «| Florario» solo se añade si cabe en 60. El build avisa de cualquier title o description demasiado largos. | Sin avisos de longitud en las 152 páginas. |

### Posibles
- **Hreflang de los países:** cada `/pais/` y su `/en/pais/` se citan mutuamente; la portada queda como pareja es/en. Las páginas de país tienen contenido propio, así que no son variantes es-XX de la portada. El build comprueba que todos los `hreflang` son recíprocos.
- **Calendario para imprimir:** descarga del PDF y del **fondo de pantalla 9:16** (nuevo, `descargas/fondo-calendario-de-flores-AAAA.jpg`) en la primera pantalla; sin el botón «Ver en el calendario». En enero, GitHub Actions genera el fondo del año nuevo (`pines.py --fondos`).
- **«¿A quién se lo regalas?»** en la portada: pareja, amiga o amigo, mamá, papá o a mí. Usa el campo `para` de cada fecha en `datos.py`.
- **Generador de tarjeta** en las guías con mensajes: imagen 1080 × 1920 en `<canvas>` con el mensaje y una flor del color elegido, para descargar o compartir.
- **Fechas guardadas al calendario:** con «♥ Guardadas», un botón genera en el navegador un `.ics` con esas fechas (mismo formato que `/recordatorios/`).
- **Google Discover:** `max-image-preview:large` en todas las páginas y la imagen `og` de 1200 px también en el JSON-LD.

### Menos importantes
- Degradados del H1 con todos los colores a 3:1 o más sobre el fondo, en claro y en oscuro (tokens `--g-*` por tema).
- Etiquetas en mono a .75rem como mínimo; antetítulo de la portada «2026-2027»; zona táctil de 32 px en las flores de la rueda (capa de círculos por debajo, para no tapar a las vecinas); «Hot Wheels» con mayúsculas en los avisos de los `.ics`.

### Lo que faltaba (hecho después, el mismo día)
- **Analítica sin cookies (punto 7):** Vercel Web Analytics, activada en el proyecto `florario-wq96`. El script (`/_vercel/insights/script.js`, en `ANALYTICS` de `build.py`) va en todas las páginas menos el widget, que se inserta en webs ajenas. Cuenta visitas, páginas, país, dispositivo y web de origen, sin cookies. Un único detector de clics manda eventos (`recordatorio_ics`, `google_calendar`, `whatsapp`, `pdf`, `pinterest`, `story`, `fondo_pantalla`, `filtro`, `rueda`, `compartir`, `ics_guardadas`, `tarjeta`), pero **el plan Hobby de Vercel solo registra las visitas**: los eventos aparecerán en el panel si el proyecto pasa a Pro. Política de privacidad (ES y EN) actualizada; de paso se corrigió que decía que las fuentes venían de Google Fonts, cuando están alojadas en `/fuentes/`.
- **Perfiles sociales (punto 15):** Florario no tiene perfiles propios todavía, así que no se añade nada al pie ni a `sameAs` de Organization. Cuando existan, van en `org_ld()` de `build.py` y en el pie.
- **Fotos de ramos reales (punto 12):** seis fotos de Wikimedia Commons (CC BY, CC BY-SA), una por guía principal, en «Según tu presupuesto»: girasol en la mano, ramo con flores azules en la mano, lavanda en las manos, rosas envueltas en papel de periódico, claveles rosas y rosas envueltas para regalo. Se insertan con `<!--@FOTO:clave-->`, que añade el crédito bajo la foto y en el pie; `"pos"` en `IMAGES` fija el encuadre. Créditos en `imagenes/CREDITOS.md`.
- Para la verificación hay medidores en `_build/salida/medir*.html` (no se publican): abren cada página en un iframe de 390 × 844 y devuelven posiciones y alturas.

