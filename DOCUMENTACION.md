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
