# Fase 0 — Las 3 encuestas

Objetivo: saber **qué hará Claude con la skill final** (el uso), para qué oficio, en qué sector y dónde se verá el trabajo.
Con eso salen las 10 dimensiones de la Fase 1 (`usos.md`) y las normas de la skill final. Nada más.

Reglas:
- Siempre con la herramienta de encuesta de opciones, nunca pidiendo que escriba la respuesta en el chat.
- Cada encuesta depende de la anterior: no adelantes una pregunta cuyas opciones dependen de una respuesta que aún no tienes.
- Formato de la herramienta: de 2 a 4 opciones por pregunta («Otro» lo añade ella), etiqueta (`label`) de 1 a 5 palabras, detalle en
  `description` y cabecera (`header`) de 12 caracteres como máximo.
- No preguntes el nombre de la skill (se genera: `<oficio>-<sector>-<uso>`), ni ritmo de cortes, duración, formato o longitud del
  hook (lo dictan las normas del canal), ni nada que no cambie la búsqueda o las normas de la skill final.

---

## Encuesta 1 — Tipo de trabajo (1 pregunta)

| header | Pregunta | Opciones (`label` — `description`) |
|---|---|---|
| Tipo | ¿Para qué tipo de trabajo quieres la skill? | **Diseño y dirección** — branding, piezas gráficas, webs, Claude Design, Figma, campañas · **Imagen y vídeo** — guiones, imágenes, motion graphics, fotografía, contenido para redes |

## Encuesta 2 — Oficio, sector y canal (3 preguntas en la misma llamada)

| header | Pregunta | Opciones |
|---|---|---|
| Oficio | ¿Cuál es tu oficio? | Diseño y dirección → **Diseñador gráfico** · **Diseñador web** · **Director creativo**. Imagen y vídeo → **Filmmaker** · **Fotógrafo** · **Cinematográfico** · **Content Creator** |
| Sector | ¿En qué sector trabajas? (una skill por sector) | **Gastronomía** · **Inmobiliaria** · **Finanzas** · **Hoteles y turismo** (en «Otro»: moda, salud, tecnología, deporte, automoción, música, educación, lujo, retail…) |
| Canal | ¿Dónde se va a ver tu trabajo? (puedes marcar varias) — `multiSelect` | Diseño y dirección → **Paid y redes** · **Impreso y espacio físico** — packaging, cartelería, señalética · **Web y producto digital** · **Presentaciones y documentos**. Imagen y vídeo → **Paid (anuncios)** — tiene que vender · **Orgánico (redes)** — comunidad y alcance · **Marca (web, eventos)** — película de marca · **Pieza larga** — documental, festival, TV |

## Encuesta 3 — Uso y estilo (2 preguntas en la misma llamada)

**Uso** — header `Uso`, `multiSelect` — «¿Qué quieres que Claude haga con esta skill? (recomendado 1; máximo 2)». Cada opción lleva a un
tipo de `usos.md`, que da las 10 dimensiones:

| Oficio | `label` — `description` → tipo en `usos.md` |
|---|---|
| Filmmaker | **Guiones** — escribir y revisar guiones → Texto · **Imágenes** — frames, storyboards y prompts para IA → Imagen · **Motion graphics** — grafismo, rotulación y animación → Motion |
| Cinematográfico | **Look y color** — referencias de etalonaje y LUT → Imagen (variante cine) · **Planos y luz** — planificación de planos e iluminación → Imagen (variante cine) · **Imágenes de referencia** — frames y prompts para IA → Imagen (variante cine) |
| Fotógrafo | **Dirección de sesiones** — moodboard, lista de planos, estilismo → Imagen · **Edición y retoque** — criterio de color y retoque → Imagen (variante retoque) · **Selección y series** — editar y secuenciar → Imagen · **Imágenes con IA** — prompts con tu mirada → Imagen |
| Content Creator | **Guiones y hooks** → Texto · **Miniaturas y portadas** → Redes · **Carruseles y posts** → Redes · **Edición y motion** → Motion |
| Diseñador gráfico | **Branding e identidad** → Identidad · **Diseños en Claude Design** → Maquetación · **Diseños en Figma** — con el MCP de Figma → Maquetación · **Piezas para redes y paid** → Redes |
| Diseñador web | **Webs y landings** — en Claude Design o código → Maquetación (ajuste web) · **Diseño en Figma** — con el MCP de Figma → Maquetación (ajuste web) · **UI de producto** — apps y paneles → Maquetación (ajuste web) · **Sistema de diseño** → Maquetación |
| Director creativo | **Conceptos y campañas** → Texto (variante concepto) · **Copy y claims** → Texto · **Dirección de arte** — key visuals y mundo visual → Imagen · **Revisión de propuestas** → Texto (variante concepto) + Imagen, 5 y 5 |

Con 2 usos, la Fase 1 toma las 5 dimensiones más decisivas de cada tipo. Con más, propón partirlo en dos skills.

**Estilo (opcional)** — header `Estilo` — «¿Qué estilo buscas dentro de <sector>? (opcional)». No uses una lista fija: genera 4 opciones
para oficio × sector × canal, una por eje:
1. *Registro* del sector (cercano ↔ premium, sobrio ↔ desenfadado).
2. *Subnicho* (en gastronomía: alta cocina, street food, producto, bebidas; en inmobiliaria: lujo, obra nueva, alquiler, comercial).
3. *Estética dominante* en ese sector y oficio (lo que se lleva).
4. *Apuesta distinta* al cliché del sector.

Si no contesta, se explora sin estilo concreto.

| Oficio × sector | Opciones de ejemplo |
|---|---|
| Filmmaker × gastronomía | Cocina real y cercana · Alta cocina / lujo · Street food urbano · Producto sensorial |
| Filmmaker × finanzas | Institucional sobrio · Fintech joven y directo · Historias humanas reales · Humor que desmitifica |
| Filmmaker × inmobiliaria | Lujo y estilo de vida · Obra nueva · Recorrido inmersivo · Barrio y comunidad |
| Fotógrafo × hoteles | Lujo silencioso · Boutique con carácter · Naturaleza y escapada · Gente y servicio |
| Diseñador gráfico × gastronomía | Artesanal y cálido · Minimal contemporáneo · Retro / vintage · Irreverente |
| Diseñador web × finanzas | Confianza y sobriedad · Producto primero · Editorial y educativo · Oscuro y atrevido |

Son ejemplos del nivel de concreción, no una lista a copiar.

## Después de las encuestas

Confirma en 2–3 líneas el encuadre (oficio · uso · sector · canal · estilo) **y las 10 dimensiones** sobre las que la skill tendrá
criterio, con los nombres de `usos.md` adaptados. Ejemplo: «Tu skill tendrá criterio sobre: arranque, estructura, quién cuenta, tono,
protagonista, tensión, prueba, lenguaje, punto de vista y cierre». Menciona también las normas fijas que entrarán sin preguntar (las
del canal y, si el sector está regulado, las del sector). No pidas confirmación salvo que algo sea ambiguo: sigue con la Fase 1.
