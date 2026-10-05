# Skill creative creator

Una skill de Claude que crea **skills creativas personalizadas**. Usa la extensión de Chrome de cada persona para buscar
200+ referencias en Pinterest, Behance y otras plataformas gratuitas, deja que el creativo las elija y puntúe del 1 al 10, y
con ese gusto real genera una skill propia.

## Flujo

La skill final es **criterio + normas** para un uso concreto (guiones, imágenes, motion, branding, Claude Design, Figma, redes…).
Todo encadena: **uso de la skill → 10 dimensiones → normas de la skill final.**

| Fase | Qué pasa | Resultado |
|---|---|---|
| 0 | 3 encuestas: tipo de trabajo → oficio, sector y canal → uso y estilo | Encuadre y las 10 dimensiones de criterio |
| 1 | Por cada dimensión, 5 tipologías con una pieza real de ejemplo | 50 referencias |
| 2 | El creativo elige 1 de cada 5 (encuestas) | Criterio inicial |
| 3 | **La estrella:** búsqueda de 200 o más en plataformas, etiquetada por dimensión | ≥200 referencias (15–25 % de contraste) |
| 4 | El creativo puntúa del 1 al 10 (6–10 le gusta, 1–5 evitar) | Datos puntuados |
| 5 | Análisis por dimensión: norma, evitar, margen; confirma o corrige la Fase 2 | Criterio validado con la persona |
| 6 | Genera la skill: criterio + normas del canal + normas de salida + checklist | Skill lista para instalar |

Oficios: diseñador gráfico, diseñador web, director creativo, filmmaker, fotógrafo, cinematográfico y content creator.
Recomendación: **una skill por uso y sector** y esfuerzo alto o superior.

## Instalación

Copia la carpeta `creador-skills-creativas/` a `~/.claude/skills/` (o al directorio de skills de tu proyecto) y activa la
extensión de Chrome de Claude. Necesita Python 3 para los scripts (sin dependencias).

## Contenido

```
creador-skills-creativas/
├── SKILL.md                         # el flujo completo
├── references/
│   ├── preguntas.md                 # las 3 encuestas de la Fase 0
│   ├── usos.md                      # dimensiones, tipologías, plataformas y normas por uso
│   ├── plataformas.md               # extensión de Chrome, plataformas, qué guardar
│   └── plantilla-skill-final.md     # estructura de la skill generada
└── scripts/refs.py                  # base de datos, tableros HTML, validación y análisis
```

## Notas

- Se guardan enlaces, autor y notas; **no** se descargan ni rehostean imágenes. Que una plataforma sea gratuita no implica que sus obras sean reutilizables.
- El trabajo de cada persona vive en `creative-workspace/<slug>/refs.json` (se puede cortar y retomar).
