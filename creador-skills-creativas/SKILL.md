---
name: creador-skills-creativas
description: >
  Crea una skill creativa PERSONALIZADA, con criterio y normas, para que Claude trabaje como un creativo concreto:
  guiones, imágenes, motion graphics, branding, diseños en Claude Design o en Figma (MCP), piezas para redes y paid,
  fotografía o look cinematográfico. Para diseñadores gráficos y web, directores creativos, filmmakers, fotógrafos,
  cinematográficos y content creators. Pregunta con encuestas oficio, uso, sector y canal; con la extensión de Chrome
  de la persona busca 200 o más referencias en Pinterest, Behance y otras plataformas gratuitas; el creativo elige y
  puntúa del 1 al 10; su criterio se convierte en normas por dimensión y en una skill lista para instalar. Úsala
  SIEMPRE que alguien quiera una skill con su criterio, gusto o estilo, que Claude diseñe, escriba o dirija como él,
  convertir un moodboard o sus referencias en reglas, o crear skills creativas para su equipo, aunque no diga skill.
---

# Creador de skills creativas personalizadas

La skill que se genera es **criterio + normas** para que Claude produzca o revise un tipo concreto de trabajo (guiones, imágenes,
motion, branding, diseños en Claude Design o Figma…) como lo haría este creativo.

El hilo que une todo: **uso de la skill → 10 dimensiones → normas de la skill final.** Lo que se pregunta, se busca y se puntúa es
exactamente lo que la skill final tendrá que decidir. Si una pregunta o una dimensión no acaba siendo una norma, sobra.

El método: 3 encuestas → 50 referencias (10 dimensiones × 5 tipologías) → elige 1 de cada 5 → **200 o más referencias en
plataformas** → puntuación del 1 al 10 → criterio por dimensión → skill. La búsqueda de las 200 es la fase estrella; todo lo demás
existe para dirigirla bien y para convertir sus puntuaciones en normas.

Archivos de apoyo (léelos cuando se indique):
- `references/preguntas.md` — las 3 encuestas, con opciones por oficio → Fase 0
- `references/usos.md` — dimensiones y tipologías por uso, dónde buscar, normas de salida, del canal y del sector → Fases 1, 3 y 6
- `references/plataformas.md` — extensión de Chrome, plataformas, qué guardar, obstáculos → Fases 1 y 3
- `references/plantilla-skill-final.md` — estructura de la skill generada → Fase 6
- `scripts/refs.py` — base de referencias, tableros, análisis y exportación (Python 3.8+, sin dependencias; `--help` en cada comando)

Ruta de esta skill: la carpeta de este archivo (`$SKILL` en los comandos). Espacio de trabajo: `creative-workspace/<slug>/`.

## Principios

1. **Solo referencias reales.** Cada entrada es una página que has abierto o visto. Inventar o rellenar hasta 200 invalida el criterio.
   Si no llegas, dilo con la cifra.
2. **Las puntuaciones bajas valen tanto como las altas.** Sin ejemplos de lo que no le gusta, la skill no sabe qué evitar: en la
   Fase 3 entra a propósito un 15–25 % de contraste.
3. **Todo sirve a la skill final.** No preguntes lo que no cambie la búsqueda o las normas. Tampoco lo que dicta el canal (ritmo de
   cortes, duración, formato, longitud del hook): eso son normas del canal, no gusto.
4. **Las normas salen de sus notas, no de ti.** Una tipología es norma solo si puntúa claramente por encima del resto de su dimensión.
   Si ninguna destaca, la dimensión queda libre: imponer una norma sin evidencia hace la skill más rígida y no más fiel.
5. **Un uso y un sector por skill.** Con 2 usos se reparten las dimensiones; con más, propón dos skills.
6. **Estado en disco.** Todo vive en `refs.json`; `refs.py status` dice en qué fase está y qué falta.
7. **Referencia ≠ material reutilizable.** Se guardan enlaces, autor y notas; no se descargan imágenes (`plataformas.md`).
8. **Encuestas, no chat.** Toda pregunta va con la herramienta de encuesta de opciones, en su idioma y sin jerga técnica.

**Al empezar**, una línea: funciona mejor con **esfuerzo alto o superior** y con **una skill por uso y sector**. Comprueba en silencio si
hay extensión de Chrome conectada (`plataformas.md`). Si no la hay, dilo y ofrece dos caminos: activarla (lo recomendable, sobre todo
en usos visuales, donde se elige viendo imágenes) o seguir en **modo reducido** (búsqueda web, sin miniaturas; `init --modo reducido`).

## Fase 0 — Encuadre: 3 encuestas

Guion y opciones en `references/preguntas.md`. Cada encuesta depende de la anterior:

1. **Tipo de trabajo:** Diseño y dirección · Imagen y vídeo.
2. **Oficio** (según 1) · **Sector** · **Canal** (dónde se verá; selección múltiple).
3. **Uso**: qué hará Claude con la skill (según el oficio; 1, como mucho 2) · **Estilo** (opcional, generado para oficio × sector × canal).

El nombre se genera (`<oficio>-<sector>-<uso>`). Confirma en 2–3 líneas el encuadre **y las 10 dimensiones** sobre las que la skill
tendrá criterio, y crea el espacio de trabajo:

```bash
python3 $SKILL/scripts/refs.py init --dir creative-workspace/<slug> --oficio "<oficio>" --foco "<sector>" \
  --uso "<uso>" --canal "<canal>" --keyword "<estilo>"
```

## Fase 1 — 50 referencias: 10 dimensiones × 5 tipologías

1. **Dimensiones:** las 10 del tipo de uso en `references/usos.md`, adaptadas al sector y al canal.
2. **Tipologías primero:** 5 por dimensión antes de buscar, con nombre llano de 2–5 palabras y una frase que se entienda sin ver
   la pieza. Que no se solapen; una puede ser el cliché del sector.
3. **Un ejemplo real por tipología**, buscado con la extensión en las plataformas del uso. Si no encuentras uno bueno, cambia la
   tipología; no la deformes para que encaje con lo que encontraste.
4. **Usos visuales** (Imagen, Motion, Identidad, Maquetación, Redes): la miniatura (`thumb`: `og:image` o el `src` de la imagen) es
   obligatoria, porque el creativo elegirá viéndola. **Uso Texto**: pon en `note` la frase clave de la pieza (arranque o claim).

Guarda las 50 en un archivo de tanda y añádelas (el script pone ids, deduplica y etiqueta cada una con su tipología):

```json
[{"url": "https://www.behance.net/gallery/…", "title": "Bistró Lumbre — identidad", "author": "Estudio X",
  "thumb": "https://…/imagen.jpg", "group": "Tipografía principal", "tipologia": "Serif editorial",
  "note": "Titulares serif grandes y cálidos"}]
```

```bash
python3 $SKILL/scripts/refs.py add creative-workspace/<slug>/refs.json tanda-explore.json --phase explore
python3 $SKILL/scripts/refs.py validate creative-workspace/<slug>/refs.json --stage explore
python3 $SKILL/scripts/refs.py board creative-workspace/<slug>/refs.json --mode pick --out creative-workspace/<slug>/elegir.html
```

## Fase 2 — Elige 1 de cada 5

**En usos visuales se elige viendo.** Un estilo visual no se puede elegir por su nombre:
1. Entrega `elegir.html` (como archivo de la sesión, o ábrelo en su Chrome con la extensión): por dimensión, las 5 imágenes con su
   letra (A–E), su tipología y el enlace a la pieza.
2. Recoge la elección por encuesta con las mismas letras («A · Serif editorial»): mira el tablero y contesta en la encuesta.

**En el uso Texto** basta la encuesta, porque se elige leyendo.

Encuestas: 4 dimensiones por llamada (4 + 4 + 2). Cada pregunta, en clave de su trabajo y en una línea («3/10 · LUZ: ¿qué luz quieres
en tus imágenes?»). Cada opción: `label` = letra + tipología, `description` = su frase + «Ej.: pieza (plataforma)». Caben 4 opciones:
la 5ª tipología se nombra al final de la pregunta para escribirla en «Otro». Registra las respuestas:

```bash
python3 $SKILL/scripts/refs.py pick creative-workspace/<slug>/refs.json "Luz=A" "Color=Tierra cálida" "3=ninguna" \
  "Arranque=Presentar el problema" --reason "Color=me recuerda a las tabernas"
```

Acepta letra, nombre de la tipología, «ninguna» o un texto propio. Si escribe su propia tipología en «Otro», es información valiosa:
queda como tipología propia y se busca en la Fase 3 como una más. (Si eligió en el tablero: `refs.py apply … picks.json`.)

Las elegidas son el **criterio inicial**. Resúmelo en 3–5 líneas y confírmalo con una encuesta («¿Te reconoces?») antes de la búsqueda
grande: si el diagnóstico falla, falla todo lo demás.

## Fase 3 — La estrella: 200 o más referencias en plataformas

**Plan de búsqueda.** Unas 20 por dimensión, repartidas para que cada tipología tenga evidencia:
- **~8 alrededor de la semilla:** variaciones de la tipología elegida (otros autores, países, épocas, formatos, marcas del sector).
- **~3 de cada tipología no elegida:** sin ellas no se puede saber si la semilla gana de verdad.
- **Contraste (15–25 % del total)**, con `contrast: true`: clichés del sector y opuestos. No avises de cuáles son.

Cada pieza suma en varias dimensiones a la vez (una identidad muestra logotipo, tipografía y color), así que los huecos se cubren
antes de lo que parece: `refs.py status` muestra la evidencia por dimensión y por tipología. Úsalo cada ~50 para dirigir la búsqueda.

**Cómo buscar.** Consultas por tipología × sector × estilo, en inglés y en su idioma. Amplía por similitud (pines relacionados,
proyectos similares, más obras del autor) antes que por palabras sueltas. Plataformas del uso en `usos.md`; método y obstáculos en
`plataformas.md`. Mínimo 3 plataformas, ninguna por encima del 50 %.

**Cómo etiquetar.** Cada referencia lleva `tags` con la forma `dimensión:tipología` para **cada** dimensión que se vea en ella, con los
nombres de la Fase 1 (`Luz:Natural de ventana`, `Color:Tierra cálida`). Si aparece una solución que no estaba entre las 5, crea la
tipología nueva. Sin estas etiquetas no hay criterio por dimensión. `group` es la dimensión que motivó la búsqueda.

```json
[{"url": "https://…", "title": "…", "author": "…", "thumb": "https://…", "group": "Color",
  "tags": ["Color:Tierra cálida", "Tipografía principal:Serif editorial", "Logotipo:Sello o emblema"], "contrast": false}]
```

Guarda por tandas de ~20 (`add … --phase search`) y avisa del progreso cada ~50 en una línea. Cuando creas haber llegado:

```bash
python3 $SKILL/scripts/refs.py status creative-workspace/<slug>/refs.json
python3 $SKILL/scripts/refs.py validate creative-workspace/<slug>/refs.json --stage search --min 200
```

Sigue hasta que pase. Si una plataforma bloquea, cambia de plataforma. Si no hay más material real, para y cuéntalo con la cifra.

## Fase 4 — Puntuación del 1 al 10

```bash
python3 $SKILL/scripts/refs.py board creative-workspace/<slug>/refs.json --mode rate --out creative-workspace/<slug>/puntuar.html
```

El tablero mezcla el orden y oculta las etiquetas, para que puntúe la pieza y no la categoría. Guarda el avance solo y al final
descarga `ratings.json` (`refs.py apply … ratings.json`).

| Puntuación | Significado |
|---|---|
| 9–10 | Quiero esto. Es mi referencia. |
| 6–8 | Me gusta, encaja, pero no es lo mejor. |
| 1–5 | No me gusta / hay que evitarlo (1 = lo rechazo con ganas, 5 = no me dice nada). |

Pídele una nota en los extremos (1–2 y 9–10): sus palabras explican el porqué y acaban en la skill. Si no puede abrir el tablero,
puntúa por encuestas: 4 referencias por llamada y 4 franjas por pregunta (9–10 · 6–8 · 3–5 · 1–2), registradas con
`refs.py score … s001=9 s002=4` como 9, 7, 4 y 2. Avísale de que es menos fino que el tablero.

## Fase 5 — Criterio por dimensión

```bash
python3 $SKILL/scripts/refs.py stats creative-workspace/<slug>/refs.json > creative-workspace/<slug>/analisis.md
```

Por cada dimensión, `analisis.md` compara cada tipología con el resto de su dimensión («dif. vs resto»). Así se lee:
- **Norma candidata:** supera al resto por 1 punto o más, con evidencia **fuerte** o **débil**. Una débil se escribe con cautela.
- **Evitar:** queda 1 punto o más por debajo del resto y su media es ≤5.
- **Sin preferencia clara:** ninguna destaca. La dimensión queda libre en la skill (su elección de la Fase 2 vale como preferencia suave).
- **Fase 2:** dice si la búsqueda confirma su elección. Si **no se confirma**, pregúntale; no decidas tú.

Mira también las anclas (sus referencias de 9–10 y de 1–2) y sus notas: los números dicen qué, las piezas y sus palabras dicen por qué.
Si una dimensión importante tiene poca evidencia, haz una ronda corta (40–60) sobre ella, puntúala y vuelve a analizar.

**Valida con la persona** en 8–12 líneas, una por dimensión («Luz: natural de ventana; nunca flash duro de frente»), y pregunta con una
encuesta si se reconoce o qué ajustaría. Si corrige algo, manda su palabra; anota que contradice los datos.

## Fase 6 — Generar la skill

```bash
python3 $SKILL/scripts/refs.py export-skill creative-workspace/<slug>/refs.json --out <nombre-skill>/references
```

Exporta `criterio-por-dimension.md` (la evidencia, con anclas), las referencias que le gustan y las que evita, y `referencias.json`.
Con `references/plantilla-skill-final.md`, escribe `<nombre-skill>/SKILL.md`:
- **Criterio por dimensión:** norma, evitar, margen y anclas; las dimensiones sin preferencia, marcadas como libres.
- **Normas del canal** y **normas de salida del uso** (`usos.md`).
- **Normas del sector**, si está regulado (finanzas, salud, alimentación, alcohol, juego…): solo lo verificado en la fuente oficial del
  país; lo que no puedas verificar, márcalo «pendiente de revisar con un experto».
- **Checklist** de cumplimiento y **rúbrica** del 1 al 10.

Después:
1. Revisa la lista de calidad de la plantilla.
2. Pruébala con 1–2 encargos reales del creativo y ajusta lo que no reconozca como suyo (si tienes `skill-creator`, úsala para iterar).
3. Entrégala como carpeta o `.skill`, con instrucciones de instalación, y recuerda el mantenimiento: reanalizar cada ~50 referencias nuevas.

## Reanudar

Si ya existe `creative-workspace/<slug>/refs.json`, ejecuta `refs.py status` antes de preguntar nada: dice qué fase falta y cuál es el
siguiente paso. Retoma desde ahí y confírmalo con la persona.
