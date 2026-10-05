# Fase 0 — Las 3 encuestas

Objetivo: saber **qué hará Claude con la skill final** (el uso), para qué oficio, en qué sector y dónde se verá el trabajo.
Con eso se deducen las 10 dimensiones de la Fase 1 (`usos.md`) y las normas de la skill final. Nada más.

Reglas:
- Siempre con la herramienta de encuesta (opciones), nunca pidiendo que escriba en el chat.
- Cada encuesta depende de la anterior: no adelantes preguntas cuyas opciones dependen de una respuesta que aún no tienes.
- Máximo 4 opciones por pregunta: ofrece las 4 más probables; el resto cabe en «Otro».
- No preguntes: nombre de la skill (se genera: `<oficio>-<sector>-<uso>`), ritmo de cortes, duración, formato o longitud del hook
  (lo dictan las normas del canal), ni nada que no cambie la búsqueda o las normas de la skill final.

---

## Encuesta 1 — Tipo de trabajo

| Pregunta | Opciones |
|---|---|
| ¿Para qué tipo de trabajo quieres la skill? | **Diseño y dirección** (branding, piezas gráficas, webs, Claude Design, Figma, campañas) · **Imagen y vídeo** (guiones, imágenes, motion, fotografía, contenido) |

## Encuesta 2 — Oficio, sector y canal (tres preguntas en la misma llamada)

**Oficio** (depende de la encuesta 1):
- Diseño y dirección → Diseñador gráfico · Diseñador web · Director creativo
- Imagen y vídeo → Filmmaker · Fotógrafo · Cinematográfico · Content Creator

**Sector** (el foco de la skill; una skill por sector): Gastronomía · Inmobiliaria · Finanzas · Hoteles y turismo (+ «Otro»: moda, salud,
tecnología, deporte, automoción, música, educación, lujo, retail…).

**Canal: ¿dónde se va a ver tu trabajo?** (selección múltiple; fija las normas del canal de la skill final):
- Diseño y dirección → Paid y redes · Impreso y espacio físico (packaging, cartelería, señalética) · Web y producto digital · Presentaciones y documentos
- Imagen y vídeo → Paid (anuncios) · Orgánico (redes) · Marca (web, presentaciones, eventos) · Pieza larga (documental, festival, TV)

## Encuesta 3 — Uso y estilo (dos preguntas en la misma llamada)

**Uso: ¿qué quieres que Claude haga con esta skill?** (selección múltiple, recomienda 1 y como mucho 2). Cada opción lleva a un tipo de
`usos.md`, que da las 10 dimensiones:

| Oficio | Opciones (→ tipo en `usos.md`) |
|---|---|
| Filmmaker | Guiones (→ Texto) · Imágenes: frames, storyboard, IA (→ Imagen) · Motion graphics (→ Motion) |
| Cinematográfico | Look y color (→ Imagen, variante cine) · Planificación de planos y luz (→ Imagen, variante cine) · Imágenes de referencia e IA (→ Imagen, variante cine) |
| Fotógrafo | Dirección de sesiones (→ Imagen) · Edición y retoque (→ Imagen, variante retoque) · Selección y series (→ Imagen) · Imágenes con IA (→ Imagen) |
| Content Creator | Guiones y hooks (→ Texto) · Miniaturas y portadas (→ Redes) · Carruseles y posts (→ Redes) · Edición y motion (→ Motion) |
| Diseñador gráfico | Branding e identidad (→ Identidad) · Diseños en Claude Design (→ Maquetación) · Diseños en Figma con MCP (→ Maquetación) · Piezas para redes y paid (→ Redes) |
| Diseñador web | Webs y landings en Claude Design o código (→ Maquetación, ajuste web) · Diseño en Figma con MCP (→ Maquetación, ajuste web) · UI de producto y apps (→ Maquetación, ajuste web) · Sistema de diseño (→ Maquetación) |
| Director creativo | Conceptos y campañas (→ Texto, variante concepto) · Copy y claims (→ Texto) · Dirección de arte y key visuals (→ Imagen) · Revisión de propuestas (→ Texto, variante concepto + Imagen) |

Si elige 2 usos, la Fase 1 reparte 5 dimensiones de cada uno (las 5 más decisivas de cada tipo). Si elige más, propón partir en dos skills.

**Estilo (opcional): generado para oficio × sector × canal.** No uses una lista fija. Construye 4 opciones, una por eje:
1. *Registro* del sector (cercano ↔ premium, sobrio ↔ desenfadado).
2. *Subnicho* (en gastronomía: alta cocina, street food, producto, bebidas; en inmobiliaria: lujo, obra nueva, alquiler, comercial).
3. *Estética dominante* en ese sector y oficio (lo que se lleva).
4. *Apuesta distinta* al cliché del sector.

| Oficio × sector | Opciones de ejemplo |
|---|---|
| Filmmaker × gastronomía | Cocina real y cercana · Alta cocina / lujo · Street food urbano · Producto sensorial |
| Filmmaker × finanzas | Institucional sobrio · Fintech joven · Historias humanas · Datos que se entienden |
| Filmmaker × inmobiliaria | Lujo y estilo de vida · Obra nueva · Recorrido inmersivo · Barrio y comunidad |
| Fotógrafo × hoteles | Lujo silencioso · Boutique con carácter · Naturaleza y escapada · Gente y servicio |
| Diseñador gráfico × gastronomía | Artesanal y cálido · Minimal contemporáneo · Retro / vintage · Irreverente |
| Diseñador web × finanzas | Confianza y sobriedad · Producto primero (fintech) · Editorial y educativo · Oscuro y atrevido |

Son ejemplos de nivel de concreción, no una lista a copiar.

## Después de las encuestas

Confirma en 2–3 líneas: oficio · uso · sector · canal · estilo, **y las 10 dimensiones** sobre las que la skill tendrá criterio
(nombres de `usos.md`, adaptados). Ejemplo: «Tu skill tendrá criterio sobre: luz, color, plano, composición, protagonista, acabado,
escenario, momento, foco y mood». No pidas confirmación salvo que algo sea ambiguo: sigue con la Fase 1.
