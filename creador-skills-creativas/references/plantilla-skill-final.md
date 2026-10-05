# Plantilla de la skill personalizada (Fase 6)

La skill final es **criterio + normas** para un uso concreto. Hay tres tipos de reglas, y conviene no mezclarlas:

| Tipo | De dónde sale | Ejemplo |
|---|---|---|
| **Criterio** (gusto) | Puntuaciones por dimensión (`analisis.md`) y sus notas | «Luz: natural de ventana, lateral. Nunca flash duro frontal.» |
| **Normas del canal** | `usos.md` → Normas del canal (verificadas) | «Paid: se entiende sin sonido; llamada a la acción explícita.» |
| **Normas de salida** | `usos.md` → normas de salida del uso | «Entrega el guion a dos columnas imagen/sonido con tiempos.» |

Una regla de criterio sin referencias puntuadas detrás es opinión tuya, no su criterio: no la incluyas.

```
<nombre-skill>/
├── SKILL.md
└── references/
    ├── criterio-por-dimension.md   # cada dimensión con evidencia (tabla de analisis.md + anclas)
    ├── referencias-gustan.md       # export-skill
    ├── referencias-evitar.md       # export-skill
    ├── referencias.json            # export-skill (para reanalizar)
    ├── busqueda.md                 # consultas y plataformas que mejor funcionaron
    └── tokens.css | tokens.json    # solo en usos de diseño: colores, tipografía, espaciado (de las referencias de 9–10)
```

Nombre: `<oficio>-<sector>-<uso>` en minúsculas con guiones (por ejemplo, `filmmaker-gastronomia-guiones`).

## SKILL.md de la skill final

```markdown
---
name: <nombre-skill>
description: >
  Criterio de <nombre o "este creativo"> para <uso> en <sector> (<canal>). Úsala siempre que Claude tenga que <verbos del uso:
  escribir guiones / crear imágenes / diseñar en Figma…> o revisar <entregables> de <sector>, aunque no se mencione «mi estilo».
  Aplica <2-3 normas distintivas> y evita <2 anti-normas>.
---

# <Uso> de <sector>: criterio de <nombre>

Construida con <N> referencias puntuadas del 1 al 10 (<fecha>; plataformas: <lista>). 6–10 = le gusta · 1–5 = evitar.

## Cómo trabajar
1. Identifica qué dimensiones toca el encargo. 2. Aplica la norma de cada una y las normas del canal y de salida.
3. Antes de entregar, pasa el checklist. 4. Si dudas, busca la referencia ancla más cercana en `references/criterio-por-dimension.md`.

## Criterio por dimensión
### <Dimensión 1>
- **Norma:** <regla verificable> — evidencia: <tipología> (n=12, media 8,4); ancla: [<ref>](<url>) (10).
- **Evitar:** <regla> — <tipología> (n=9, media 2,9); ancla: [<ref>](<url>) (2).
- **Margen:** <cuándo sí y cuándo no, si lo hay>.
(… las 10 dimensiones; las de poca evidencia van marcadas «por explorar».)

## Normas del canal
<Las del canal o canales elegidos, como reglas duras y verificables.>

## Normas de salida
<Las del uso: formato de guion / ficha de plano y plantilla de prompt / tokens y reglas de Figma o Claude Design / guía de movimiento…>

## Checklist antes de entregar
- [ ] <Una línea por norma, que se pueda contestar sí o no.>

## Rúbrica de revisión (1–10)
Puntúa la pieza por dimensión con su misma escala, usando las anclas. Cualquier dimensión ≤5 se rehace antes de entregar.
Devuelve la nota de cada dimensión y el cambio concreto que la subiría.

## Referencias nuevas
Plataformas y consultas que funcionaron (`references/busqueda.md`). Cada referencia nueva se propone con autor, enlace y la norma que cumple.

## Mantenimiento
Con ~50 referencias nuevas puntuadas, se reanaliza con `references/referencias.json` y se actualizan las normas.
```

## Lista de calidad (antes de entregar)
- Cada norma se puede comprobar en una pieza real («titulares en serif de más de 90 pt» sí; «tipografía elegante» no).
- Cada dimensión tiene «Norma» y «Evitar», o va marcada «por explorar».
- Criterio, normas del canal y normas de salida están separados.
- La descripción nombra el uso, el sector y los entregables, para que se active sola.
- `SKILL.md` tiene menos de 500 líneas; el detalle va a `references/`.
- Ninguna imagen copiada: solo enlaces, autor y notas.
- Está escrita en el idioma del creativo y con su vocabulario (sus notas).
