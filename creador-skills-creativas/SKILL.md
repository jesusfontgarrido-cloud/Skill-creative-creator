---
name: creador-skills-creativas
description: >
  Crea una skill creativa PERSONALIZADA, con criterio y normas, para que Claude haga el trabajo de un creativo como lo haría él:
  guiones, imágenes, motion graphics, branding, diseños en Claude Design o en Figma (MCP), piezas para redes y paid, fotografía o
  look cinematográfico. Para diseñadores gráficos y web, directores creativos, filmmakers, fotógrafos, cinematográficos y content
  creators. Pregunta con encuestas el oficio, el uso, el sector y el canal; usa la extensión de Chrome de la persona para buscar
  200+ referencias en Pinterest, Behance y otras plataformas gratuitas; el creativo elige y puntúa del 1 al 10; extrae su criterio y
  lo convierte en una skill. Úsala SIEMPRE que alguien quiera una skill con su criterio, gusto o estilo, un moodboard masivo
  convertido en reglas, o «que Claude diseñe/escriba/grabe como yo», aunque no diga «skill».
---

# Creador de skills creativas personalizadas

La skill que se genera es **criterio + normas** para que Claude produzca o revise un tipo concreto de trabajo (guiones, imágenes,
motion, branding, diseños en Claude Design o Figma…) como lo haría este creativo.

El hilo que une todo el proceso: **uso de la skill → 10 dimensiones → normas de la skill final.** Lo que se pregunta, se busca y se
puntúa es exactamente lo que la skill final tendrá que decidir. Si una pregunta o una dimensión no acaba siendo una norma, sobra.

El método: 3 encuestas → 50 referencias (10 dimensiones × 5 tipologías) → elige 1 de cada 5 → **mínimo 200 referencias en plataformas**
→ puntuación del 1 al 10 → criterio → skill. La fase de las 200 es la estrella: el resto existe para que esa búsqueda vaya bien dirigida
y para convertir sus puntuaciones en normas.

Archivos de apoyo (léelos cuando se indique):
- `references/preguntas.md` — las 3 encuestas, con opciones por oficio → Fase 0
- `references/usos.md` — dimensiones y tipologías por uso, dónde buscar, normas de salida y del canal → Fases 1, 3 y 6
- `references/plataformas.md` — extensión de Chrome, plataformas, qué guardar, obstáculos → Fases 1 y 3
- `references/plantilla-skill-final.md` — estructura de la skill generada → Fase 6
- `scripts/refs.py` — base de referencias, tableros HTML, validación y análisis (Python 3, sin dependencias)

Ruta de esta skill: la carpeta que contiene este archivo; en los comandos se escribe `$SKILL`.

## Principios

1. **Solo referencias reales.** Cada entrada es una página que has abierto o visto. Inventar o rellenar hasta 200 invalida el criterio.
   Si no llegas, dilo con la cifra.
2. **Las puntuaciones bajas valen tanto como las altas.** Sin ejemplos de lo que no le gusta, la skill no sabe qué evitar. Por eso en la
   Fase 3 entra a propósito un 15–25 % de contraste.
3. **Todo sirve a la skill final.** No preguntes lo que no cambie la búsqueda o las normas. Tampoco lo que dicta el canal (ritmo de
   cortes, duración, formato, longitud del hook): eso son normas del canal, no gusto.
4. **Un uso y un sector por skill.** Con 2 usos se reparte; con más, propón dos skills.
5. **Estado en disco.** Todo vive en `refs.json`; la sesión se puede cortar y retomar.
6. **Referencia ≠ material reutilizable.** Se guardan enlaces, autor y notas; no se descargan imágenes (ver `plataformas.md`).
7. **Encuestas, no chat.** Toda pregunta va con la herramienta de encuesta de opciones, en el idioma y el nivel de la persona.

Al empezar, una línea: funciona mejor con **esfuerzo alto o superior** y con **una skill por uso y sector**. Comprueba en silencio si hay
extensión de Chrome conectada (`plataformas.md`); si no la hay, dilo en una línea y explica el modo reducido.

## Fase 0 — Encuadre: 3 encuestas

Guion y opciones exactas en `references/preguntas.md`. Cada encuesta depende de la anterior:

1. **Tipo de trabajo:** Diseño y dirección · Imagen y vídeo.
2. **Oficio** (según 1) · **Sector** · **Canal** (dónde se verá; selección múltiple).
3. **Uso**: qué hará Claude con la skill (según el oficio; 1, como mucho 2) · **Estilo** (opcional, generado para oficio × sector × canal).

No preguntes el nombre (se genera `<oficio>-<sector>-<uso>`). Confirma en 2–3 líneas el encuadre **y las 10 dimensiones** sobre las que
la skill tendrá criterio, y crea el espacio de trabajo:

```bash
python3 $SKILL/scripts/refs.py init --dir creative-workspace/<slug> --oficio "<oficio>" --foco "<sector>" \
  --uso "<uso>" --canal "<canal>" --keyword "<estilo>"
```

## Fase 1 — 50 referencias: 10 dimensiones × 5 tipologías

1. **Dimensiones:** toma las 10 del tipo de uso en `references/usos.md` y adáptalas al sector y al canal. Son las futuras secciones
   de criterio de la skill.
2. **Tipologías primero:** define 5 por dimensión antes de buscar. Cada una con nombre llano de 2–5 palabras (`tipologia`) y una frase
   que se entienda sin ver la pieza (`note`). Que no se solapen.
3. **Un ejemplo real por tipología:** búscalo con la extensión en las plataformas del uso (`usos.md`). Si no encuentras uno bueno,
   cambia la tipología. No la deformes para que encaje con lo encontrado: así salen opciones sin sentido.
4. Guarda cada una (`phase: "explore"`, `group` = dimensión) con `id, url, title, author, platform, thumb, group, tipologia, note,
   tags, license`. Mezcla al menos 3 plataformas.

```bash
python3 $SKILL/scripts/refs.py validate creative-workspace/<slug>/refs.json --stage explore
python3 $SKILL/scripts/refs.py board creative-workspace/<slug>/refs.json --mode pick --out creative-workspace/<slug>/elegir.html
```

## Fase 2 — Elige 1 de cada 5

Encuestas, 4 dimensiones por llamada (4 + 4 + 2). Cada pregunta, en clave de su trabajo y en una línea: «3/10 · LUZ: ¿qué luz quieres
en tus imágenes?». Cada opción: `label` = tipología, `description` = su frase + «Ej.: <pieza> (<plataforma>)». Las encuestas admiten
4 opciones: la 5ª tipología se nombra al final de la pregunta para escribirla en «Otro». Alternativa visual: `elegir.html` → `picks.json`.

```bash
python3 $SKILL/scripts/refs.py apply creative-workspace/<slug>/refs.json picks.json
```

Si escribe su propia tipología en «Otro» («presentamos el problema»), es información valiosa: no la fuerces a una de las 5. Regístrala en
`refs.json` → `profile.custom_picks` (`{"<dimensión>": "<tipología>"}`) y búscala en la Fase 3 como una tipología más.

Las 10 elegidas son el **criterio inicial** (una tipología por dimensión). Resúmelo en 3–5 líneas antes de la búsqueda grande: si el
diagnóstico falla, falla todo lo demás.

## Fase 3 — La estrella: mínimo 200 referencias en plataformas

1. **Busca dentro del encuadre:** mismo sector, canal y uso. Parte de las semillas: rasgos, autores y estudios, en inglés y en el idioma
   del creativo. Amplía por similitud (pines relacionados, proyectos similares, más obras del autor) antes que por palabras sueltas.
2. **Etiqueta por dimensión:** cada referencia lleva `tags` con la forma `dimensión:tipología` para cada dimensión que se vea en ella,
   con los mismos nombres de la Fase 1 (por ejemplo `luz:natural de ventana`, `color:cálido terroso`). Si aparece una solución que no
   estaba entre las 5, crea la tipología nueva. Es lo que permite convertir las puntuaciones en normas por dimensión. `group` es la
   dimensión que motivó la búsqueda.
3. **Contraste a propósito (15–25 %)**, con `contrast: true`: tipologías no elegidas y clichés del sector. No avises de cuáles son.
4. **Diversifica:** 3 o más plataformas, ninguna por encima del 50 %, unas 20 por dimensión. Usa `phase: "search"`.
5. Guarda por tandas de ~20 y avisa del progreso cada ~50 en una línea.

```bash
python3 $SKILL/scripts/refs.py validate creative-workspace/<slug>/refs.json --stage search --min 200
```

Sigue hasta que pase. Si una plataforma bloquea, cambia de plataforma (`plataformas.md`). Si no hay más material real, para y cuéntalo.

## Fase 4 — Puntuación del 1 al 10

```bash
python3 $SKILL/scripts/refs.py board creative-workspace/<slug>/refs.json --mode rate --out creative-workspace/<slug>/puntuar.html
```

| Puntuación | Significado |
|---|---|
| 9–10 | Quiero esto. Es mi referencia. |
| 6–8 | Me gusta, encaja, pero no es lo mejor. |
| 1–5 | No me gusta / hay que evitarlo (1 = lo rechazo con ganas, 5 = no me dice nada). |

El tablero guarda el avance y descarga `ratings.json`. Pide una nota en los extremos (1–2 y 9–10): sus palabras valen más que el número.
Sin HTML, puntúa por tandas de 10–15 en encuestas.

```bash
python3 $SKILL/scripts/refs.py apply creative-workspace/<slug>/refs.json ratings.json
```

## Fase 5 — Criterio por dimensión

```bash
python3 $SKILL/scripts/refs.py stats creative-workspace/<slug>/refs.json --min-n 3 > creative-workspace/<slug>/analisis.md
```

`analisis.md` da, por dimensión, la media de cada tipología, marca con ★ la elegida en la Fase 2 y dice si la búsqueda la confirma.
Mira también las referencias de los extremos (≥9 y ≤2). Para cada dimensión, redacta:

- **Norma:** la tipología ganadora, convertida en regla verificable.
- **Evitar:** las tipologías con media ≤5.
- **Margen:** lo que a veces sí y a veces no, y de qué depende (tabla de tensiones).
- Si una dimensión tiene poca evidencia, márcala como «por explorar»; no la conviertas en norma.

Si el análisis avisa de poco contraste o de poco acierto, propone una ronda corta (40–60) sobre la dimensión floja. **Valida con la
persona** en 8–12 líneas, una por dimensión («Luz: natural de ventana; nunca dura de flash. ¿Te reconoces?»).

## Fase 6 — Generar la skill

Lee `references/plantilla-skill-final.md`, exporta las referencias y escribe la skill:

```bash
python3 $SKILL/scripts/refs.py export-skill creative-workspace/<slug>/refs.json --out <nombre-skill>/references
```

La skill final tiene: criterio por dimensión (norma, evitar, margen, anclas), **normas del canal** y **normas de salida del uso**
(ambas en `usos.md`), un checklist de cumplimiento y una rúbrica del 1 al 10. Después:

1. Revisa la lista de calidad de la plantilla.
2. Pruébala con 1–2 encargos reales del creativo y ajusta lo que no reconozca como suyo. Si tienes `skill-creator`, úsala para iterar.
3. Entrégala (carpeta o `.skill`) con instrucciones de instalación. Recuerda el mantenimiento: reanalizar cada ~50 referencias nuevas.

## Reanudar
Si existe `creative-workspace/<slug>/refs.json`, léelo antes de preguntar: sin refs → Fase 1; explore sin `picked` → 2; search < 200 → 3;
sin `score` → 4; con scores → 5/6. Retoma desde ahí.
