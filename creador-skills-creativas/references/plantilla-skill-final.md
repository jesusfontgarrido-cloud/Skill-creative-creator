# Plantilla de la skill personalizada (Fase 6)

La skill final es **criterio + normas** para un uso concreto. Hay cuatro tipos de reglas, y conviene no mezclarlas:

| Tipo | De dónde sale | Ejemplo |
|---|---|---|
| **Criterio** (su gusto) | `criterio-por-dimension.md` (sus puntuaciones), sus notas y la validación de la Fase 5 | «Luz: natural de ventana, lateral. Nunca flash duro de frente.» |
| **Normas del canal** | `usos.md` → Normas del canal | «Paid: se entiende sin sonido; llamada a la acción explícita.» |
| **Normas del sector** | `usos.md` → Normas del sector, verificadas en la fuente oficial | «Finanzas: muestra la TAE junto a cualquier rentabilidad.» |
| **Normas de salida** | `usos.md` → normas de salida del uso | «Entrega el guion a dos columnas, imagen y sonido, con tiempos.» |

Una regla de criterio sin referencias puntuadas detrás es opinión tuya, no su criterio: no la incluyas. Una dimensión «sin preferencia
clara» no lleva norma: se marca como libre.

```
<nombre-skill>/
├── SKILL.md
└── references/
    ├── criterio-por-dimension.md   # export-skill: tablas por dimensión, normas candidatas, evitar y anclas
    ├── referencias-gustan.md       # export-skill
    ├── referencias-evitar.md       # export-skill
    ├── referencias.json            # export-skill (para reanalizar)
    ├── busqueda.md                 # tú: consultas y plataformas que mejor funcionaron
    └── tokens.css o tokens.json    # tú, solo en usos de diseño: colores, tipografía, espaciado, radios
```

Nombre: `<oficio>-<sector>-<uso>` en minúsculas, sin tildes y con guiones (por ejemplo, `filmmaker-finanzas-guiones`).

En usos de diseño, saca los tokens de sus referencias de 9–10 mirándolas (o de los archivos de marca que te dé): colores en HEX,
tipografías con pesos, escala de tamaños, espaciado y radios. Para Claude Design, como variables CSS en `:root` con modo oscuro; para
Figma con MCP, como variables y estilos de texto.

## SKILL.md de la skill final

```markdown
---
name: <nombre-skill>
description: >
  Criterio de <nombre o «este creativo»> para <uso> en <sector> (<canal>). Úsala siempre que Claude tenga que <verbos del uso:
  escribir guiones, crear imágenes, diseñar en Figma…> o revisar <entregables> de <sector>, aunque no se mencione «mi estilo».
  Aplica <2-3 normas distintivas> y evita <2 anti-normas>.
---

# <Uso> de <sector>: criterio de <nombre>

Construida con <N> referencias puntuadas del 1 al 10 (<fecha>; plataformas: <lista>). 6–10 = le gusta · 1–5 = evitar.

## Cómo trabajar
1. Identifica qué dimensiones toca el encargo.
2. Aplica la norma de cada una, y las normas del canal, del sector y de salida.
3. Antes de entregar, pasa el checklist y la rúbrica.
4. Si dudas, busca el ancla más cercana en `references/criterio-por-dimension.md`.

## Criterio por dimensión
### <Dimensión 1>
- **Norma:** <regla verificable> — <tipología> (media 8,4, +3,1 sobre el resto, n=12, evidencia fuerte); ancla: [<pieza>](<url>) (10).
- **Evitar:** <regla> — <tipología> (media 2,9, n=9); ancla: [<pieza>](<url>) (2).
- **Margen:** <cuándo sí y cuándo no, según sus notas>.
### <Dimensión sin preferencia clara>
- **Libre:** sus notas no marcan diferencia entre opciones. Preferencia suave: <su elección de la Fase 2>.
(… las 10 dimensiones.)

## Normas del canal
<Las del canal o canales elegidos, como reglas duras y verificables.>

## Normas del sector
<Solo si el sector está regulado: lo verificado, con la fuente. Lo no verificado: «pendiente de revisar con un experto».>

## Normas de salida
<Las del uso: formato de guion · ficha de plano y plantilla de prompt · tokens y reglas de Claude Design o Figma · guía de movimiento…>

## Checklist antes de entregar
- [ ] <Una línea por norma, que se pueda contestar sí o no.>

## Rúbrica de revisión (1–10)
Puntúa la pieza en cada dimensión con su misma escala, comparándola con las anclas. Cualquier dimensión con norma que quede en 5 o menos
se rehace antes de entregar. Devuelve la nota por dimensión y el cambio concreto que la subiría.

## Referencias nuevas
Plataformas y consultas que funcionaron (`references/busqueda.md`). Cada referencia nueva se propone con autor, enlace y la norma que cumple.

## Mantenimiento
Con ~50 referencias nuevas puntuadas, se reanaliza con `references/referencias.json` y se actualizan las normas.
```

## Lista de calidad (antes de entregar)
- Cada norma se puede comprobar en una pieza real («titulares en serif de más de 90 pt» sí; «tipografía elegante» no).
- Cada dimensión tiene norma y evitar con su evidencia, o va marcada como libre o «por explorar». Las de evidencia débil, redactadas
  con cautela («preferiblemente»).
- Criterio, normas del canal, normas del sector y normas de salida están separados.
- La descripción nombra el uso, el sector y los entregables, para que se active sola; tiene 1024 caracteres como máximo y **sin los
  signos `<` ni `>`** (la validación de skills los rechaza).
- `name` en minúsculas, cifras y guiones (máximo 64 caracteres).
- `SKILL.md` tiene menos de 500 líneas; el detalle va a `references/`.
- Ninguna imagen copiada: solo enlaces, autor y notas.
- Está escrita en el idioma del creativo y con su vocabulario (sus notas y motivos).
