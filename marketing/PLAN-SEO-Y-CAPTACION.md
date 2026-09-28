# Florario · Plan de SEO, autoridad y captación

Todo lo que no se puede hacer desde el código porque necesita tus cuentas (Google, Pinterest, TikTok, correo) o tu voz. Esta carpeta `marketing/` no se publica en la web (está en `.vercelignore`).

---

## 0. Antes de publicar (imprescindible)

1. ~~Rellena tus datos en `_build/datos.py` → `SITE`~~ Hecho: autor, firma, titular y correo. El Aviso legal presenta Florario como proyecto personal, sin NIF ni dirección. Si algún día la web tiene ingresos (anuncios, afiliados o venta), añade NIF y dirección al Aviso legal y a la Política de privacidad.
2. Regenera: `python _build/build.py --pdf` (y `python _build/pines.py` si cambias textos de los pines).
3. Revisa en local: `python -m http.server` y abre <http://localhost:8000>.
4. Sube los cambios con git (yo no he tocado git). Por ejemplo:
   ```
   git add -A
   git commit -m "SEO: páginas por mes, flor y país, nuevas guías, PDF, recordatorios y datos estructurados"
   git push
   ```

---

## 1. Google Search Console

1. Entra en <https://search.google.com/search-console> → **Añadir propiedad** → tipo **Dominio** → `calendariodeflores.com`.
2. Copia el registro TXT y añádelo en el DNS del dominio (en Vercel: *Project → Settings → Domains*, o en tu proveedor del dominio). Pulsa **Verificar**.
3. **Sitemaps** → envía `https://www.calendariodeflores.com/sitemap.xml` (56 URLs con `lastmod` e imágenes).
4. **Inspección de URLs** → pega cada URL y pulsa **Solicitar indexación**. Google limita las solicitudes diarias (unas 10–12), así que ve por prioridad:
   - Día 1: `/`, `/flores-azules/`, `/octubre/`, `/flores-moradas/`, `/noviembre/`, `/todos-los-santos-dia-de-muertos/`, `/cempasuchil/`, `/crisantemo/`, `/meses/`, `/flores/`
   - Día 2: `/mexico/`, `/espana/`, `/argentina/`, `/colombia/`, `/chile/`, `/peru/`, `/guias/`, `/hortensia/`, `/violeta/`, `/nochebuena/`
   - Día 3: `/diciembre/`, `/rosa/`, `/girasol/`, `/flores-amarillas/`, `/significado-colores-flores/`, `/flores-para-condolencias/`, `/flores-para-cumpleanos/`, `/flores-para-aniversario/`, `/dia-del-maestro/`, `/sobre-florario/`
   - Después, el resto (el sitemap hará que Google las encuentre igualmente).
5. Prueba los datos estructurados de 3–4 páginas en <https://search.google.com/test/rich-results> (FAQ, Breadcrumb, Article, Event) y en <https://validator.schema.org/>.
6. Vuelve cada semana a **Rendimiento → Consultas** y apunta la posición de: *calendario de flores*, *fechas para regalar flores*, *flores de temporada*, *flores azules 3 de octubre*, *flores moradas 9 de noviembre*.

> Nota: Google ya no muestra resultados enriquecidos de FAQ para la mayoría de webs ni de “Event” para fechas festivas; el marcado sigue ayudando a entender la página, pero no esperes estrellas ni desplegables en el buscador.

**Bing Webmaster Tools** (<https://www.bing.com/webmasters>): importa la propiedad desde Search Console en un clic. Bing alimenta también a otros buscadores y asistentes.

---

## 2. Plan de enlaces (autoridad)

Objetivo: 15–25 enlaces de sitios relacionados en los próximos 3 meses. Lo que ofreces a cambio: **el calendario en PDF gratis**, datos para sus artículos y las guías como recurso.

| Tipo de sitio | Cómo encontrarlos | Qué les ofreces |
|---|---|---|
| Floristerías locales (ES, MX, AR, CO, CL, PE) con blog | Google: `floristería blog "día de la madre"`, `florería "flores amarillas" blog` | Permiso por escrito para imprimir el PDF en tienda (es de uso personal por defecto); enlace a su guía de fecha |
| Blogs de bodas | `blog de bodas flores de temporada` | Tabla de flores de temporada por mes (`/#temporada`), páginas de peonía, lilium, hortensia |
| Blogs de jardinería | `blog jardinería calendario floración` | Páginas de cada flor y la tabla de temporada |
| Blogs de maternidad, educación y regalos | `ideas regalo día del maestro`, `qué regalar día del padre` | Guías de Día del Maestro, Padre, Madre, cumpleaños |
| Medios de tendencias (Infobae, Quién, Expansión, El Espectador, La Nación…) | Periodistas que ya escribieron del trend (mira las fuentes de cada guía) | Nota de prensa con datos antes de cada fecha (sección 3) |
| Directorios y recursos educativos | Webs de colegios, bibliotecas, efemérides escolares | Calendario PDF como recurso de aula (con permiso por escrito) |

**Correo tipo (floristerías y blogs):**

> Asunto: Calendario de flores 2026-2027 gratis para tu blog/tienda
>
> Hola, [nombre]:
>
> Soy [tu nombre], de Florario (calendariodeflores.com), un calendario con todas las fechas del año para regalar flores en España y Latinoamérica, con las flores de temporada de cada mes.
>
> He visto vuestro artículo sobre [tema] y creo que a vuestros lectores les puede servir nuestro calendario de flores para imprimir (PDF A4 gratis, con portada ilustrada): https://www.calendariodeflores.com/calendario-de-flores-para-imprimir/. Si preferís algo para la web, tenemos un widget con la próxima fecha que se actualiza solo: https://www.calendariodeflores.com/prensa/#widget. Si os encaja, podéis enlazarlo. Y si queréis imprimirlo para vuestra tienda o publicarlo, decídmelo y os doy permiso por escrito.
>
> Un saludo,
> [firma]

Reglas: nada de comprar enlaces ni intercambios masivos; personaliza cada correo; apunta en una hoja quién respondió.

---

## 3. Notas de prensa antes de cada fecha trend

Envíalas **10–20 días antes** de la fecha a periodistas de tendencias, estilo de vida y virales. Adjunta datos concretos y el enlace a la guía.

| Fecha | Enviar entre | Guía | Ángulo |
|---|---|---|---|
| 14 feb · San Valentín | 20 ene – 1 feb | `/san-valentin/` | “Los otros San Valentín del año” |
| 8 mar · 8M | 15 – 25 feb | `/dia-de-la-mujer/` | Por qué Italia regala mimosa |
| 19 mar · Día del Padre (ES) | 25 feb – 5 mar | `/dia-del-padre/` | “Ellos también merecen flores” |
| 21 mar · Flores amarillas (MX) | 1 – 10 mar | `/flores-amarillas-21-de-marzo/` | ¿21 de marzo o 21 de septiembre? |
| Día de la Madre (ES 1.er dom may, MX 10 may) | 10 – 20 abr | `/dia-de-la-madre/` | La fecha en cada país |
| 1 ago · Día de la Novia | 10 – 20 jul | `/dia-de-la-novia/` | El segundo San Valentín |
| **21 sep · Flores amarillas** | **1 – 10 sep** | `/flores-amarillas/` | Origen Floricienta + cadena 22-23-24 |
| **3 oct · Día del Novio** | **15 – 23 sep** | `/flores-azules/` | Flores azules y Hot Wheels |
| **9 nov · Flores moradas** | **15 – 25 oct** | `/flores-moradas/` | “Un ramito de violetas” y la persona morada |
| 19 nov · Día del Hombre | 25 oct – 5 nov | `/flores-azules/#dia-del-hombre` | Flores para ellos |
| 8 dic · Nochebuena | 15 – 25 nov | `/nochebuena/` | La flor de Navidad es mexicana |

**Plantilla:**

> **Titular:** Qué flores se regalan el [fecha] y por qué: la guía de [trend] que arrasa en TikTok
>
> [Ciudad], [fecha]. — El [fecha], miles de personas en [países] regalarán [flor/color]. El trend nació en [origen] y [dato]. Florario, el calendario de flores de España y Latinoamérica, reúne [N] fechas del año para regalar flores y explica el origen de cada una.
>
> **Datos clave:** [3 viñetas con datos de la guía]
>
> **Recursos:** guía completa en [URL]; calendario en PDF en [URL]; fotos con licencia libre (autor y licencia en la web).
>
> **Contacto:** [nombre], [correo].

---

## 4. Pinterest

Pinterest es un buscador visual con mucha estacionalidad: **publica cada pin 30–45 días antes de su fecha** y vuelve a fijarlo cada año.

1. Crea una **cuenta de empresa** y reclama el sitio web (*Ajustes → Cuentas reclamadas*, meta etiqueta o archivo HTML; si eliges la meta etiqueta, añádela en `head_meta()` de `_build/build.py` y regenera).
2. Tableros: *Calendario de flores*, *Flores amarillas, azules y moradas*, *Día de la Madre y del Padre*, *Flores de temporada*, *Significado de las flores*.
3. Imágenes 1000×1500 ya generadas en `marketing/pines/` (`python _build/pines.py` las vuelve a crear).
4. En cada descripción **incluye el crédito de la foto** (lo exigen las licencias CC BY-SA): “Foto: [autor], [licencia], Wikimedia Commons”. Los autores están en `imagenes/CREDITOS.md`.

| Imagen | Enlace | Título del pin | Descripción (con palabras clave) |
|---|---|---|---|
| `calendario-de-flores.png` | `/` | Calendario de flores 2026: qué flor regalar cada fecha | Todas las fechas para regalar flores en España y Latinoamérica, con flores de temporada y PDF para imprimir. |
| `flores-amarillas.png` | `/flores-amarillas/` | Por qué se regalan flores amarillas el 21 de septiembre | Origen del trend (Floricienta), qué significan y qué flores amarillas regalar. |
| `flores-amarillas-21-de-marzo.png` | `/flores-amarillas-21-de-marzo/` | Flores amarillas el 21 de marzo | La versión de primavera del trend en México: qué regalar y por qué. |
| `flores-azules.png` | `/flores-azules/` | Flores azules para el Día del Novio (3 de octubre) | Hortensias, rosas azules y ramos de Hot Wheels: ideas para el 3 de octubre y el 19 de noviembre. |
| `flores-moradas.png` | `/flores-moradas/` | Flores moradas el 9 de noviembre | “Un ramito de violetas” y tu persona morada: qué flores moradas regalar. |
| `san-valentin.png` | `/san-valentin/` | Flores para San Valentín | Qué significa cada rosa y los otros San Valentín del año. |
| `dia-de-la-madre.png` | `/dia-de-la-madre/` | Flores para el Día de la Madre | Claveles, peonías y liliums, y la fecha del Día de la Madre en cada país. |
| `dia-del-padre.png` | `/dia-del-padre/` | Flores para el Día del Padre | Girasoles, flores azules y plantas: qué regalar a papá y cuándo es en cada país. |
| `dia-de-la-mujer.png` | `/dia-de-la-mujer/` | Flores del 8 de marzo | Por qué se regala mimosa en Italia y tulipanes en Rusia el Día de la Mujer. |
| `sant-jordi.png` | `/sant-jordi/` | Sant Jordi: una rosa y un libro | La leyenda del dragón y cómo se vive el 23 de abril. |
| `todos-los-santos-dia-de-muertos.png` | `/todos-los-santos-dia-de-muertos/` | Flores para Todos los Santos y Día de Muertos | Crisantemo y cempasúchil: qué llevar al cementerio y a la ofrenda. |
| `nochebuena.png` | `/nochebuena/` | Flor de Nochebuena: 8 de diciembre | Origen mexicano de la flor de Pascua y cómo cuidarla. |
| `significado-colores-flores.png` | `/significado-colores-flores/` | Qué significa cada color de flor | Amarillo, rojo, rosa, azul, morado, naranja y blanco: cuándo regalar cada uno. |
| `flores-para-cumpleanos.png` | `/flores-para-cumpleanos/` | Flores para cumpleaños | Qué ramo regalar según la persona y la flor de cada mes de nacimiento. |
| `flores-para-aniversario.png` | `/flores-para-aniversario/` | Flores para aniversarios | La flor de cada año juntos, del clavel a la rosa. |
| `meses.png` | `/meses/` | Flores de temporada mes a mes | Qué flores hay cada mes en España, México y el Cono Sur. |

---

## 5. TikTok (y Reels / Shorts)

Formato: 15–30 s, vertical, texto grande en pantalla, música en tendencia. Publica **5–7 días antes** de cada fecha y repite el día anterior. Enlace en la bio a `calendariodeflores.com` (o a la guía de la fecha más próxima).

**Guion base (vale para cualquier fecha):**
1. *Gancho (0–2 s):* “¿Sabes qué flores tocan el [fecha]?” sobre la foto de la flor.
2. *Origen (3–10 s):* una frase con el porqué (canción, leyenda, país).
3. *Qué regalar (10–20 s):* 3 opciones rápidas, de más barata a más especial.
4. *Cierre (20–30 s):* “Todas las fechas del año, en calendariodeflores.com. Guárdalo para que no se te pase.”

**Ideas de serie:**
- “Fechas para regalar flores que no conocías” (Rose Day, muguet, Dia dos Namorados, Nochebuena).
- “Qué significa el color de las flores que te regalaron”.
- “El calendario de flores de [país]” (una por país, con su página).
- Cuenta atrás: “Faltan 3 días para las flores azules”.
- Dúos o *stitches* con vídeos virales de la fecha, aportando el origen.

Hashtags por fecha: `#floresamarillas`, `#diadelnovio`, `#floresazules`, `#floresmoradas`, `#diadelanovia`, `#galentinesday`, `#diadelamadre`, `#calendariodeflores`.

---

## 6. Newsletter y “Recuérdamelo”

**Ya funciona sin servidor:** cada fecha tiene su archivo `.ics` en `/recordatorios/` con aviso 3 días antes, y `/descargas/calendario-de-flores.ics` reúne todas (también como suscripción en Google Calendar). Algunos calendarios ignoran las alarmas de las suscripciones; el archivo descargado sí las mantiene.

**Newsletter (siguiente paso, requiere tu cuenta):**
1. Elige un servicio con plan gratuito y servidores en la UE si puedes (Brevo, MailerLite) o Buttondown.
2. Crea una lista con **doble confirmación** y automatiza un envío 3 días antes de cada fecha principal (las de la tabla de la sección 3).
3. Inserta su formulario en `_build/plantilla-inicio.html`, dentro de la sección `#recuerdamelo`, y en el pie (`footer()` de `_build/build.py`).
4. **Antes de activarlo, actualiza la política de privacidad** (`_build/paginas/politica-de-privacidad.html`): responsable, finalidad, base legal (consentimiento), proveedor y cómo darse de baja.

---

## 7. Mantenimiento

- **Una vez al mes como mínimo:** ejecuta `python _build/build.py --pdf` y publica. El año del title (desde octubre, “2026-2027”), la tabla rodante de la portada y los PDF (año actual y siguiente) se calculan solos con la fecha del build; ya no hay que tocar ningún año a mano.
- **Antes de cada fecha trend:** revisa la guía, actualiza lo que haya cambiado y pon `"updated"` a la fecha de hoy en la cabecera de su fragmento (`_build/paginas/<guía>.html`). Solo esa página cambia su `lastmod` y su `dateModified`.
- **Widget y prensa:** en los correos a floristerías y blogs ofrece también el widget de la próxima fecha (`/prensa/#widget`) y la página del [calendario para imprimir](https://www.calendariodeflores.com/calendario-de-flores-para-imprimir/): son lo que más fácilmente se enlaza.
- **Cada trimestre:** busca trends nuevos; añadir una fecha es añadir un objeto a `EVENTS` en `datos.py`.
