# Plataformas y uso de la extensión de Chrome

Contenido: [Antes de empezar](#antes-de-empezar) · [Cómo navegar con la extensión](#cómo-navegar-con-la-extensión) ·
[Plataformas](#plataformas) · [Qué guardar y qué no](#qué-guardar-y-qué-no) · [Obstáculos](#obstáculos-y-qué-hacer)

## Antes de empezar

La skill trabaja con **la extensión de Chrome de la propia persona** (Claude en Chrome u otra extensión de navegador
conectada a Claude). Ventajas: usa su sesión ya abierta en Pinterest/Behance (el contenido que ve es el que verá ella),
y nada sale de su máquina salvo lo que ella ya consulta.

1. Mira qué herramientas de navegador tienes disponibles (suelen llamarse algo como `*chrome*` / `*browser*`: abrir pestaña,
   navegar a URL, leer página/texto, hacer clic, desplazar, captura de pantalla). Los nombres cambian entre versiones:
   descúbrelos, no los supongas.
2. Si no hay ninguna: dilo en la primera respuesta, explica que sin la extensión la búsqueda será más pobre
   (solo búsqueda web/fetch, sin ver imágenes ni scroll infinito) y ofrece dos caminos: instalar/activar la extensión y
   reintentar, o continuar en «modo reducido» con WebSearch/WebFetch. No finjas haber navegado.
3. No pidas contraseñas ni las escribas. Si hay muro de login, pide a la persona que inicie sesión ella en su Chrome.

## Cómo navegar con la extensión

Patrón por plataforma y consulta (repítelo, es mecánico):

1. Navega a la URL de búsqueda de la plataforma con la consulta (tabla abajo).
2. Haz scroll gradual (3–6 pantallas) y espera a que carguen las miniaturas.
3. Captura/mira la página para **ver** las imágenes: puntúas lo que ves, no lo que dice el título.
4. Extrae por cada candidato: URL del pin/proyecto/foto, título, autor, URL de la miniatura (`og:image` o `src` de la imagen) y plataforma.
5. Abre solo los candidatos dudosos; la mayoría se decide viendo la rejilla.
6. Anota en `refs.json` por tandas (cada ~20), no al final: si la sesión se corta, no pierdes el trabajo.
7. Pausa breve entre acciones; ritmo humano. Sin bucles agresivos de peticiones.

Para ampliar una semilla: usa «más como este» / pines relacionados / «proyectos similares» / otras obras del mismo autor.
Suele rendir más que buscar palabras sueltas, porque la plataforma ya agrupa por semejanza visual.

## Plataformas

Las URLs y los límites de cada sitio cambian: **comprueba** que la búsqueda funciona antes de apoyarte en ella.

| Plataforma | Mejor para | Búsqueda (patrón habitual) | Notas |
|---|---|---|---|
| Pinterest | casi todo; moodboards | `pinterest.com/search/pins/?q=` | Muro de login tras varios scrolls: depende de su sesión. Muchos pines son repins sin crédito: sigue al origen cuando puedas. |
| Behance | proyectos completos: identidad, packaging, web, foto, motion | `behance.net/search/projects?search=` | Ver el proyecto entero; guarda el enlace del proyecto, no de la imagen suelta. |
| Dribbble | UI, branding, ilustración, motion | `dribbble.com/search/` | Shots pequeños; poco contexto. |
| Awwwards / Godly / Siteinspire / Land-book / Httpster | web | navegar por categorías | Guarda la URL de la página de la web, no solo de la galería. |
| Are.na | moodboards curados | `are.na/search/` | Muy buena señal: la curación es humana. |
| Savee / Cosmos | fotografía, arte, diseño | navegar / buscar | Pueden pedir cuenta. |
| Unsplash / Pexels / Pixabay | fotografía | `unsplash.com/s/photos/`, `pexels.com/search/` | Licencias libres: aquí sí se puede reutilizar. |
| Wikimedia Commons / Flickr (filtro CC) | fotografía, arquitectura, histórico | buscadores propios | Revisa la licencia por obra. |
| The Dieline / Brand New / Fonts In Use / Typewolf | packaging, identidad, tipografía | navegar | Casos explicados: buen texto para extraer el «por qué». |
| Ads of the World / Ads of the Brands | campañas | navegar | Para directores creativos. |
| Film Grab | fotogramas de cine | `film-grab.com` | Para cinematográfico/filmmaker. |
| Vimeo Staff Picks / YouTube | vídeo | buscadores propios | Referencia el vídeo y el minuto concreto en `note`. |
| TikTok Creative Center / Meta Ad Library | tendencias y anuncios | herramientas públicas | Para content creator y paid. |

Reparto orientativo de la Fase 3 (≥200): **mínimo 3 plataformas**, ninguna por encima del 50 %, y favorece las que mejor
encajen con el oficio (ver el final de cada oficio en `oficios.md`).

## Qué guardar y qué no

«Gratuito y libre» describe a qué plataformas se puede **acceder** sin pagar, no a qué imágenes se pueden **reutilizar**.
Una referencia es inspiración, no material de producción. Por eso:

- **Guarda:** URL, título, autor, plataforma, URL de la miniatura, tags, nota y `license` si la plataforma la indica
  (`CC0`, `Unsplash`, `CC-BY`, `referencia` = solo para mirar). Guarda siempre el autor: se le acredita al citar.
- **No hagas:** descargar masivamente imágenes, rehostearlas en un repositorio público ni incrustarlas en la skill final.
  La skill enlaza; no copia. (El tablero hotlinkea las miniaturas en el navegador de la persona, no las almacena.)
- **No hagas:** saltarte muros de pago, límites de uso, captchas ni cuentas privadas. Si la plataforma bloquea, di cuál y sigue con otra.
- **Nunca inventes** una referencia. Cada entrada debe ser una página que hayas abierto o visto de verdad. Si no llegas a 200 reales,
  repórtalo con la cifra exacta en lugar de rellenar.

## Obstáculos y qué hacer

| Problema | Respuesta |
|---|---|
| Muro de login (Pinterest) | Pide a la persona que inicie sesión en su Chrome; continúa. Si no puede, cambia de plataforma. |
| Captcha / «actividad inusual» | Para esa plataforma, avisa y pasa a otra. No intentes resolverlo ni evitarlo. |
| Scroll infinito que no carga | Prueba menos scroll y más consultas distintas. |
| Miniatura no extraíble | Deja `thumb` vacío; el tablero mostrará el enlace. |
| Resultados repetidos entre consultas | `refs.py validate` detecta URLs duplicadas; cambia el ángulo de la consulta (sinónimos, autor, época, país). |
| Sesión larga cortada | Todo está en `refs.json`; reanuda leyéndolo y contando por grupo y plataforma lo que falta. |
