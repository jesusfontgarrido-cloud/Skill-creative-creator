---
name: creador-skills-creativas
description: >
  Crea una skill creativa PERSONALIZADA para un creativo (diseñador gráfico, diseñador web, director creativo,
  filmmaker, fotógrafo, cinematográfico o content creator) a partir de su gusto real: usa la extensión de Chrome de la
  persona para buscar 200+ referencias en Pinterest, Behance, Dribbble, Are.na y otras plataformas gratuitas, las
  agrupa, hace que el creativo elija y puntúe del 1 al 10, extrae su patrón (qué le gusta y qué evitar) y genera con
  él una skill propia. Úsala SIEMPRE que alguien quiera crear una skill de referencias o de estilo personal, un
  moodboard masivo, «una skill con mi criterio/gusto», buscar muchas referencias visuales para un foco concreto, o
  convertir sus preferencias estéticas en una skill, aunque no diga «skill creativa».
---

# Creador de skills creativas personalizadas

Convierte el gusto de un creativo en una skill que lo aplica. El método es: **mostrar → elegir → ampliar → puntuar →
extraer patrón → generar skill**. Funciona porque el gusto casi nunca se puede describir con palabras, pero siempre se
puede reconocer; esta skill lo hace reconocer 200+ veces y deduce las reglas de lo que la persona realmente puntuó.

Archivos de apoyo (léelos cuando se indique, no antes):
- `references/oficios.md` — focos, 10 grupos y tags por oficio → Fases 0, 1 y 3
- `references/plataformas.md` — cómo usar la extensión de Chrome, plataformas, qué guardar, obstáculos → Fases 1 y 3
- `references/plantilla-skill-final.md` — estructura de la skill generada → Fase 6
- `scripts/refs.py` — base de datos de referencias, tableros HTML, validación y análisis (Python 3, sin dependencias)

Ruta de esta skill: la carpeta que contiene este archivo; en los comandos se escribe `$SKILL`.

## Principios que sostienen todo el proceso

1. **Solo referencias reales.** Cada entrada es una página que has abierto o visto. Inventar o «completar» hasta 200
   invalida el patrón entero porque el creativo puntuaría cosas que no existen. Si no llegas, dilo con la cifra.
2. **Las puntuaciones bajas son tan valiosas como las altas.** Una búsqueda guiada por lo que ya le gusta devuelve
   casi todo «me gusta» y el patrón de «evitar» queda vacío. Por eso en la Fase 3 se incluye a propósito un 15–25 % de
   contraste (cercano pero distinto, o un estilo vecino que suele gustar menos).
3. **Un foco (sector) por skill.** Una skill que lo abarca todo acaba siendo genérica. Si el foco es amplio («todos los sectores»),
   propón partirlo y empezar por uno; el proceso se puede repetir por sector.
4. **Estado en disco.** Todo vive en `refs.json`; así la sesión se puede cortar y retomar sin perder nada.
5. **Referencia ≠ material reutilizable.** Se guardan enlaces, autor y notas; no se descargan ni se rehostean imágenes (ver `plataformas.md`).
6. **Habla en el idioma y con el nivel de la persona.** Evita jerga técnica (JSON, schema…) salvo que ella la use; el tablero HTML
   y los mensajes bastan.

## Antes de empezar: aviso de esfuerzo
Dilo al principio, en una frase: este proceso funciona mejor con **esfuerzo alto o superior** (hay que mirar muchas imágenes
y razonar patrones), y se recomienda **una skill por foco**. Si el esfuerzo está bajo, sugiérele subirlo, pero no bloquees.

## Fase 0 — Encuadre (preguntas)

Pregunta, en este orden y sin bombardear:

1. **Oficio** (ofrece la lista): Diseñador gráfico · Diseñador web · Director creativo · Filmmaker · Fotógrafo · Cinematográfico · Content Creator.
   (Si hay herramienta de pregunta con opciones, úsala en dos tandas; si no, lista numerada.)
2. **Foco = sector o nicho en el que trabaja** (gastronomía, hoteles y turismo, inmobiliaria, finanzas/fintech, moda y belleza, salud y
   bienestar, tecnología/SaaS, deporte, automoción, música, educación, institucional/ONG, lujo, retail…). El sector es lo que más cambia
   qué es «una buena referencia»: un filmmaker de gastronomía y uno de finanzas miran cosas distintas. Ofrece los 4 sectores más
   probables (la herramienta de encuesta admite 4 opciones; el resto, en «Otro») y respeta el que escriba. El formato o entregable
   (spot, videoclip, identidad, landing…) es secundario: si hace falta, pregúntalo después como segunda pregunta; no lo uses como foco.
3. **Palabra o estilo concreto (opcional) — generada para ese sector y oficio.** No uses una lista fija: construye 4 opciones a medida
   con la combinación oficio × sector (tono, estética, subnicho, referencia de época o de mercado). Ejemplo para Filmmaker × gastronomía:
   «cocina real y cercana», «alta cocina / lujo», «street food urbano», «producto sensorial». Para Filmmaker × finanzas serían otras
   («institucional sobrio», «fintech joven», «storytelling humano», «datos y explicación»). Guía para generarlas en `references/oficios.md`
   (sección «Sectores»). Incluye siempre «Sin palabra concreta» como vía de escape. Cuanto más concreta la palabra, más afinada sale la skill.
4. **Navegador:** comprueba que hay extensión de Chrome conectada (ver `plataformas.md`) y si tiene sesión en Pinterest/Behance.
5. **Nombre** con el que firmar la skill (para el `name` final) e idioma.

**Cómo preguntar:** con encuestas de opciones (herramienta de pregunta con opciones), no pidiendo que escriba la respuesta en el chat. Las
preguntas dependientes van en llamadas separadas (sector → luego palabras de estilo generadas para ese sector).

Confirma el encuadre en 2 líneas y crea el espacio de trabajo:

```bash
python3 $SKILL/scripts/refs.py init --dir creative-workspace/<slug> --oficio "<oficio>" --foco "<foco>" --keyword "<palabra>"
```

## Fase 1 — Exploración: 50 referencias en 10 grupos de 5

Objetivo: mapear el territorio y que el creativo revele su gusto *eligiendo*, no describiéndolo.

1. Lee la sección del oficio en `oficios.md` y adapta los **10 grupos** al foco y a la palabra clave (renómbralos si hace falta).
2. Busca con la extensión (método en `plataformas.md`) **5 referencias por grupo = 50 en total**, `phase: "explore"`.
   Las 5 de cada grupo deben ser **estilos claramente distintos entre sí**; si no, elegir una no aporta información.
   Mezcla al menos 3 plataformas en el conjunto.
3. **Cada referencia lleva una `tipologia`**: el nombre corto y llano del *tipo de solución* que ilustra dentro de su grupo. Es lo que el
   creativo va a elegir, así que debe entenderse sin conocer la pieza. En el grupo «Hooks»: «Hook visual», «Hook de personaje»,
   «Hook de acción continua», «Hook de concepto», «Hook de estilo y contraste»; en «Estructura»: «Retrato de una sola voz», «Arco de aprendizaje»,
   «Coral»… Las 5 tipologías de un grupo son distintas entre sí, y la pieza real (`title`, `url`) es solo el *ejemplo*. Acompáñala de una
   frase en lenguaje llano en `note` («Abre con una imagen que impacta sin explicar nada»), sin jerga ni nombres de técnicas que
   haya que conocer. Si dudas entre una pieza y su tipología, pregúntate: ¿puede elegir esto alguien que no ha visto la pieza?
   Ejemplos de tipologías por oficio en `oficios.md`.
4. Guarda cada una en `refs.json` con `id, url, title, author, platform, thumb, group, tipologia, note, tags (4-8), license, phase`. Los tags los pones mirando la imagen.
5. Valida y genera el tablero (`validate` rechaza referencias de explore sin tipología):

```bash
python3 $SKILL/scripts/refs.py validate creative-workspace/<slug>/refs.json --stage explore
python3 $SKILL/scripts/refs.py board creative-workspace/<slug>/refs.json --mode pick --out creative-workspace/<slug>/elegir.html
```

## Fase 2 — Selección: 1 de cada 5

Se elige entre **tipologías**, no entre títulos de piezas. La persona elige **1 de cada 5** por grupo (o «Ninguna») y, si quiere, escribe una frase
de por qué.

- **Con encuesta (lo preferido):** una pregunta por grupo, hasta 4 grupos por llamada. Cada opción = `label` con la tipología («Hook visual»),
  `description` con la frase llana + el ejemplo («Ej.: Déguste, Vimeo»). Las encuestas admiten 4 opciones y el grupo tiene 5: pon 4 como
  opciones y menciona la 5ª tipología al final de la pregunta para que la escriba en «Otro». La pregunta dice qué grupo es y para qué sirve
  en una frase, no en un párrafo.
- **Con tablero:** `elegir.html` muestra la tipología en grande, su explicación y la pieza como ejemplo enlazado; descarga `picks.json`.

```bash
python3 $SKILL/scripts/refs.py apply creative-workspace/<slug>/refs.json picks.json
```

Resultado: **10 semillas** (una por grupo) con `picked: true`. Léelas con atención: qué comparten, qué descartó en cada grupo y lo que dice en los motivos.
Resume en 3–5 líneas lo que has entendido y pregunta si es correcto antes de gastar la búsqueda grande; si se equivoca el diagnóstico, se equivoca todo lo demás.

## Fase 3 — Búsqueda exhaustiva: mínimo 200 referencias nuevas

Es la fase larga. Reparte el trabajo por semilla y por grupo (≈20 por grupo).

1. **Deriva consultas de las semillas.** Para cada semilla, extrae 3–4 rasgos (estética, tema, técnica, época, mood) y formula consultas
   en inglés y en el idioma del creativo, combinando con la palabra clave del foco. Añade autores y estudios de las semillas.
2. **Amplía por similitud** (pines relacionados, «proyectos similares», más obras del autor) antes que por palabras sueltas.
3. **Incluye contraste a propósito (15–25 %)**, marcado `contrast: true`: variantes del mismo tema en estilos vecinos o clichés del sector.
   Así tendrá algo que puntuar bajo y el patrón de «evitar» tendrá datos. No avises de cuáles son; puntuará sin sesgo.
4. **Diversifica:** ≥3 plataformas, ninguna >50 %, ninguna agrupación con menos de ~15 entradas. Marca `phase: "search"`.
5. Guarda por tandas de ~20 con tags consistentes (mismo vocabulario en todo el set) y revisa el progreso cada ~50: cuenta por grupo y plataforma e informa en una línea.
6. Cuando creas haber llegado:

```bash
python3 $SKILL/scripts/refs.py validate creative-workspace/<slug>/refs.json --stage search --min 200
```

Sigue buscando hasta que pase. Si una plataforma bloquea, cambia a otra (ver tabla de obstáculos). Si de verdad no hay más material real, para y
cuéntalo; no rellenes.

## Fase 4 — Target del 1 al 10

```bash
python3 $SKILL/scripts/refs.py board creative-workspace/<slug>/refs.json --mode rate --out creative-workspace/<slug>/puntuar.html
```

Escala que se le explica antes de empezar:

| Puntuación | Significado |
|---|---|
| 9–10 | Quiero esto. Es mi referencia. |
| 6–8 | Me gusta, encaja, pero no es lo mejor. |
| 1–5 | No me gusta / hay que evitarlo (1 = lo rechazo con ganas, 5 = no me dice nada). |

El tablero guarda el avance solo (puede cerrarlo y volver) y se descarga `ratings.json`. Anímale a escribir una nota en los extremos
(1–2 y 9–10): sus palabras sobre *qué* le gusta o molesta valen más que el número. Si no puede usar el HTML, puntúa en chat por tandas de 10–15.

```bash
python3 $SKILL/scripts/refs.py apply creative-workspace/<slug>/refs.json ratings.json
```

## Fase 5 — Patrón de gusto

```bash
python3 $SKILL/scripts/refs.py stats creative-workspace/<slug>/refs.json --min-n 3 > creative-workspace/<slug>/analisis.md
```

Lee `analisis.md` y **mira también las imágenes de los extremos** (≥9 y ≤2): los números orientan, las imágenes explican. Sintetiza:

- **Lo que le define:** rasgos con evidencia (tags con media ≥7 y n≥3, motivos y notas suyas). Redáctalos como reglas verificables.
- **Lo que evita:** anti-patrones con evidencia (media ≤5). Una cosa es «no le gusta X» y otra «no le gusta X *en este contexto*»: usa la tabla de tensiones.
- **Huecos:** tags con poca evidencia no son reglas; márcalos como «por explorar».
- Si el análisis avisa de poco contraste (casi todo ≥6) o de poco acierto (casi todo ≤5), no sigas: ofrece una ronda extra corta
  (40–60 refs) apuntando al hueco, o reajusta las semillas.

**Valida con la persona antes de generar:** presenta el patrón en 8–12 líneas («Te gusta… Evitas… Dudas entre… ¿Te reconoces?»). Corrige con sus respuestas.
Esta es la comprobación más barata de que la skill final sirva.

## Fase 6 — Generar la skill personalizada

Lee `references/plantilla-skill-final.md` y construye la skill:

```bash
python3 $SKILL/scripts/refs.py export-skill creative-workspace/<slug>/refs.json --out <nombre-skill>/references
```

Después escribe `<nombre-skill>/SKILL.md`, `references/patron-de-gusto.md` y `references/busqueda.md` siguiendo la plantilla: reglas con evidencia,
anti-patrones, tensiones, **rúbrica de revisión 1–10 anclada en sus referencias**, y cómo buscar referencias nuevas.

Cierra así:
1. Revisa la lista de calidad de la plantilla (reglas verificables, contraste, descripción «pushy», <500 líneas, sin imágenes copiadas).
2. Haz una prueba con 1–2 encargos reales del creativo («hazme el titular de…», «revisa esta pieza») aplicando la skill; enséñale el resultado y
   ajusta lo que no reconozca como suyo. Si tienes la skill `skill-creator`, úsala para esta iteración y para optimizar la descripción.
3. Entrega la carpeta (o empaquétala como `.skill` si hay herramienta para ello) y dile cómo instalarla en su entorno.
4. Recuérdale el mantenimiento: cada ~50 referencias nuevas puntuadas, se reanaliza.

## Reanudar una sesión
Si existe `creative-workspace/<slug>/refs.json`, léelo antes de preguntar nada: `phase`, `picked` y `score` indican la fase en la que quedó
(sin refs → Fase 1; explore sin `picked` → 2; search < 200 → 3; sin `score` → 4; con scores → 5/6). Retoma desde ahí y confirma con la persona.
