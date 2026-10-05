# Plataformas y uso de la extensión de Chrome

Contenido: [Antes de empezar](#antes-de-empezar) · [Cómo navegar con la extensión](#cómo-navegar-con-la-extensión) ·
[Modo reducido](#modo-reducido-sin-extensión) · [Plataformas](#plataformas) · [Qué guardar y qué no](#qué-guardar-y-qué-no) ·
[Obstáculos](#obstáculos-y-qué-hacer)

## Antes de empezar

La skill trabaja con **la extensión de Chrome de la propia persona** (Claude en Chrome u otra extensión de navegador conectada a Claude).
Usa su sesión ya abierta en Pinterest o Behance, así que ve lo mismo que ella, y permite **ver** las piezas, que es lo que importa.

1. Mira qué herramientas de navegador tienes (suelen llamarse algo como `*chrome*` o `*browser*`: abrir pestaña, navegar, leer la
   página, hacer clic, desplazar, captura de pantalla). Los nombres cambian entre versiones: descúbrelos, no los supongas.
2. Si no hay ninguna, dilo en la primera respuesta y ofrece: activar la extensión y reintentar (recomendado), o seguir en
   [modo reducido](#modo-reducido-sin-extensión). Nunca finjas haber navegado.
3. No pidas contraseñas ni las escribas. Si hay muro de login, pide a la persona que inicie sesión ella en su Chrome.

## Cómo navegar con la extensión

Patrón por plataforma y consulta (es mecánico, repítelo):

1. Navega a la búsqueda de la plataforma con la consulta (tabla de abajo).
2. Haz scroll gradual (3–6 pantallas) y espera a que carguen las miniaturas.
3. Haz captura y **mira** las imágenes: se elige y se etiqueta lo que se ve, no lo que dice el título.
4. Por cada candidato, extrae: URL del pin o proyecto, título, autor, URL de la imagen (`og:image` o el `src` de la imagen) y plataforma.
5. Abre solo los dudosos; la mayoría se decide viendo la rejilla.
6. Escribe la tanda (~20) en un JSON y añádela con `refs.py add`: si la sesión se corta, no se pierde nada.
7. Pausa breve entre acciones; ritmo humano, sin ráfagas de peticiones.

Para ampliar una semilla: «más como este», pines relacionados, «proyectos similares» u otras obras del mismo autor. Rinde más que buscar
palabras sueltas, porque la plataforma ya agrupa por semejanza visual.

**Uso Texto (guiones, copy).** La referencia es una pieza cuyo texto se puede analizar. Anota en `note` la frase clave (el arranque o el
claim), sacada de la transcripción, la descripción o un artículo sobre la pieza; si no hay texto, describe en una línea cómo empieza y
cómo acaba. Si es un vídeo, añade el minuto.

## Modo reducido (sin extensión)

Con búsqueda web y lectura de páginas (`init --modo reducido`):
- Busca con filtros de dominio por plataforma (Vimeo, YouTube, Behance, Ads of the World, Film Grab…) y lee las páginas para sacar
  título, autor y miniatura (`og:image`).
- Pinterest, Meta Ad Library y TikTok Creative Center necesitan navegador: en este modo casi no sirven.
- Muchos resultados serán artículos sobre las piezas en vez de las piezas: valen como referencia si describen la pieza concreta.
- En **usos visuales**, sin miniaturas el creativo no puede elegir viendo: avísalo y recomienda activar la extensión antes de la Fase 2.
  En el **uso Texto** el modo reducido funciona razonablemente.

## Plataformas

Las URLs y los límites de cada sitio cambian: **comprueba** que la búsqueda funciona antes de apoyarte en ella.

| Plataforma | Mejor para | Búsqueda (patrón habitual) | Notas |
|---|---|---|---|
| Pinterest | casi todo; moodboards | `pinterest.com/search/pins/?q=` | Muro de login tras varios scrolls: depende de su sesión. Muchos pines no tienen crédito: sigue hasta el origen cuando puedas. |
| Behance | proyectos completos: identidad, packaging, web, foto, motion | `behance.net/search/projects?search=` | Guarda el enlace del proyecto, no el de la imagen suelta. |
| Dribbble | UI, branding, ilustración, motion | `dribbble.com/search/` | Piezas pequeñas, poco contexto. |
| Awwwards / Godly / Siteinspire / Land-book / Httpster | web | navegar por categorías | Guarda la URL de la web, no solo la de la galería. |
| Are.na | moodboards curados | `are.na/search/` | Muy buena señal: la selección es humana. |
| Savee / Cosmos | fotografía, arte, diseño | navegar o buscar | Pueden pedir cuenta. |
| Unsplash / Pexels / Pixabay | fotografía | `unsplash.com/s/photos/`, `pexels.com/search/` | Licencias libres: aquí sí se puede reutilizar. |
| Wikimedia Commons / Flickr (filtro CC) | fotografía, arquitectura, histórico | buscadores propios | Revisa la licencia de cada obra. |
| The Dieline / Brand New / Fonts In Use / Typewolf | packaging, identidad, tipografía | navegar | Casos explicados: buen texto para el «por qué». |
| Ads of the World / Ads of the Brands | campañas | navegar | Para directores creativos y guiones. |
| Film Grab | fotogramas de cine | `film-grab.com` | Para cinematográfico y filmmaker. |
| Vimeo / YouTube | vídeo | buscadores propios | Anota el minuto concreto en `note`. |
| TikTok Creative Center / Meta Ad Library | tendencias y anuncios | herramientas públicas (necesitan navegador) | Para content creator y paid. |

Reparto de la Fase 3: **3 plataformas o más**, ninguna por encima del 50 %, y prioridad a las del uso (sección «Dónde buscar las 200»
de cada uso en `usos.md`).

## Qué guardar y qué no

«Gratuito y libre» describe a qué plataformas se puede **acceder** sin pagar, no qué imágenes se pueden **reutilizar**. Una referencia
es inspiración, no material de producción. Por eso:

- **Guarda:** URL, título, autor, plataforma, URL de la imagen, tags, nota y `license` si la plataforma la indica (`CC0`, `Unsplash`,
  `CC-BY`; por defecto `referencia` = solo para mirar). Guarda siempre el autor: se le acredita al citar.
- **No hagas:** descargar imágenes en masa, subirlas a un repositorio ni incrustarlas en la skill final. La skill enlaza, no copia.
  (El tablero carga las miniaturas desde la plataforma en el navegador de la persona; no las almacena.)
- **No hagas:** saltarte muros de pago, límites de uso, captchas ni cuentas privadas. Si una plataforma bloquea, di cuál y sigue con otra.
- **Nunca inventes** una referencia. Cada entrada es una página que has abierto o visto. Si no llegas a 200 reales, dilo con la cifra.

## Obstáculos y qué hacer

| Problema | Respuesta |
|---|---|
| Muro de login (Pinterest) | Pide a la persona que inicie sesión en su Chrome y continúa. Si no puede, cambia de plataforma. |
| Captcha o «actividad inusual» | Deja esa plataforma, avisa y pasa a otra. No intentes resolverlo ni esquivarlo. |
| El scroll infinito no carga | Menos scroll y más consultas distintas. |
| No se puede sacar la miniatura | En usos visuales, busca otra pieza equivalente; si no hay, déjala sin `thumb` y el tablero mostrará el enlace. |
| Resultados repetidos | `refs.py add` descarta las URLs repetidas (aunque cambien mayúsculas o parámetros de seguimiento). Cambia el ángulo de la consulta: sinónimos, autor, época, país. |
| Sesión cortada | Todo está en `refs.json`: `refs.py status` dice qué falta y por dónde seguir. |
