# Plantilla de la skill personalizada (Fase 6)

Genera la skill final con esta estructura. Rellena **todo** con evidencia del análisis (`refs.py stats`) y con las
palabras del propio creativo (notas y motivos). Una regla sin referencias detrás es opinión tuya, no su gusto: no la incluyas.

```
<nombre-skill>/
├── SKILL.md
└── references/
    ├── patron-de-gusto.md        # el patrón completo con evidencias
    ├── referencias-gustan.md     # export-skill
    ├── referencias-evitar.md     # export-skill
    ├── referencias.json          # export-skill (datos para reanalizar)
    └── busqueda.md               # consultas y plataformas que mejor funcionaron
```

Nombre: `<oficio>-<foco>-<apellido o marca>` en minúsculas con guiones (p. ej. `disenador-grafico-gastro-hoteles-font`).

## SKILL.md de la skill final

```markdown
---
name: <nombre-skill>
description: >
  <Oficio> especializado en <foco> con el criterio de <nombre>. Úsala al idear, diseñar/dirigir/producir, revisar
  o buscar referencias de <foco>: <3-5 verbos/entregables concretos>. Aplica su patrón de gusto (<2-3 rasgos
  distintivos>) y evita <2 anti-patrones>, aunque el usuario no mencione «mi estilo».
---

# <Título>: criterio creativo de <nombre> en <foco>

Construida a partir de <N> referencias puntuadas del 1 al 10 el <fecha> (plataformas: <lista>).
Escala: 6–10 = le gusta; 1–5 = evitar.

## Cómo usar esta skill
1. Antes de crear, lee «Patrón» y «Evitar». 2. Crea o propone aplicando las reglas. 3. Antes de entregar, pasa la pieza por la
rúbrica. 4. Si hay duda de gusto, consulta `references/referencias-gustan.md` y busca la referencia más cercana.

## Patrón: lo que le define
Reglas accionables, cada una con su evidencia. Formato:
- **<Regla en imperativo y concreta>** — por qué: <motivo en sus palabras>. Evidencia: tag `x` (n=12, media 8,1);
  ej.: [<ref>](<url>) (10).

(8–12 reglas máximo, ordenadas por fuerza de la evidencia.)

## Evitar
- **<Anti-patrón concreto>** — evidencia: tag `y` (n=9, media 2,8); ej.: [<ref>](<url>) (1).

## Tensiones y matices
Lo que a veces sí y a veces no, y la variable que lo decide (sale de la tabla de «tensiones» del análisis).

## Rúbrica de revisión (1–10)
Puntúa la pieza propia con la misma escala que él/ella usó. Una fila por dimensión del patrón (p. ej. tipografía,
color, composición, tono): descripción de qué es un 9–10, un 6–7 y un ≤4 **usando sus referencias como anclas**.
Si cualquier dimensión sale ≤5, hay que rehacerla antes de entregar. Devuelve la nota por dimensión y el cambio concreto que subiría la nota.

## Encontrar referencias nuevas
Plataformas y consultas que funcionaron (ver `references/busqueda.md`). Al entregar referencias nuevas: autor, enlace y por qué encajan
con una regla del patrón. Puntúalas con la rúbrica antes de proponerlas.

## Mantenimiento
Cuando haya ~50 referencias nuevas puntuadas, reanaliza con `references/referencias.json` y actualiza el patrón. El gusto evoluciona.
```

## Criterios de calidad de la skill final (revísalos antes de entregar)
- Cada regla es verificable sobre una pieza real («titulares en serif de más de 90 pt» sí; «tipografía elegante» no).
- Hay tantas reglas de «evitar» como de «hacer» o casi: el contraste es lo que hace que la skill discrimine.
- La descripción es «pushy»: nombra el oficio, el foco y los entregables para que se dispare sola.
- `SKILL.md` < 500 líneas; el detalle va a `references/`.
- Ninguna imagen copiada: solo enlaces, autor y notas.
- El tono está en el idioma del creativo y usa su vocabulario (sus notas y motivos).
