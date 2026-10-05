# Skill creative creator

Una skill de Claude que crea **skills creativas personalizadas**. Usa la extensión de Chrome de cada persona para buscar
200+ referencias en Pinterest, Behance y otras plataformas gratuitas, deja que el creativo las elija y puntúe del 1 al 10, y
con ese gusto real genera una skill propia.

## Flujo

| Fase | Qué pasa | Resultado |
|---|---|---|
| 0 | Pregunta oficio, foco (y, opcional, una palabra/estilo) | Encuadre + espacio de trabajo |
| 1 | Busca 50 referencias en 10 grupos de 5 (según oficio) | Tablero «elige 1 de cada 5» |
| 2 | El creativo elige 1 por grupo | 10 semillas de gusto |
| 3 | Búsqueda exhaustiva guiada por las semillas | ≥200 referencias (con un 15–25 % de contraste) |
| 4 | El creativo puntúa del 1 al 10 (6–10 le gusta, 1–5 evitar) | Dataset puntuado |
| 5 | Análisis de patrón: qué le define, qué evita, tensiones | Patrón validado con la persona |
| 6 | Genera la skill personalizada | Carpeta de skill lista para instalar |

Oficios: diseñador gráfico, diseñador web, director creativo, filmmaker, fotógrafo, cinematográfico y content creator.
Recomendación: **una skill por foco** y esfuerzo alto o superior.

## Instalación

Copia la carpeta `creador-skills-creativas/` a `~/.claude/skills/` (o al directorio de skills de tu proyecto) y activa la
extensión de Chrome de Claude. Necesita Python 3 para los scripts (sin dependencias).

## Contenido

```
creador-skills-creativas/
├── SKILL.md                         # el flujo completo
├── references/
│   ├── oficios.md                   # focos, grupos y tags por oficio
│   ├── plataformas.md               # extensión de Chrome, plataformas, qué guardar
│   └── plantilla-skill-final.md     # estructura de la skill generada
└── scripts/refs.py                  # base de datos, tableros HTML, validación y análisis
```

## Notas

- Se guardan enlaces, autor y notas; **no** se descargan ni rehostean imágenes. Que una plataforma sea gratuita no implica que sus obras sean reutilizables.
- El trabajo de cada persona vive en `creative-workspace/<slug>/refs.json` (se puede cortar y retomar).
