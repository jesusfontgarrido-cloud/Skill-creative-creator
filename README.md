# Skill creative creator

Una skill de Claude que crea **skills creativas personalizadas, con criterio y normas**. Pregunta con encuestas qué hará Claude con la
skill (guiones, imágenes, motion, branding, diseños en Claude Design o Figma, piezas para redes…), usa la extensión de Chrome de cada
persona para buscar 200 o más referencias en Pinterest, Behance y otras plataformas gratuitas, deja que el creativo elija y puntúe del
1 al 10, y convierte sus notas en normas por dimensión dentro de una skill lista para instalar.

## Flujo

Todo encadena: **uso de la skill → 10 dimensiones → normas de la skill final.**

| Fase | Qué pasa | Resultado |
|---|---|---|
| 0 | 3 encuestas: tipo de trabajo → oficio, sector y canal → uso y estilo | Encuadre y las 10 dimensiones de criterio |
| 1 | Por cada dimensión, 5 tipologías con una pieza real de ejemplo | 50 referencias |
| 2 | El creativo elige 1 de cada 5: viendo las imágenes en usos visuales, leyendo en guiones y copy | Criterio inicial |
| 3 | **La estrella:** búsqueda de 200 o más en plataformas, etiquetada por dimensión | ≥200 referencias (15–25 % de contraste) |
| 4 | El creativo puntúa del 1 al 10 (6–10 le gusta, 1–5 evitar) en un tablero | Referencias puntuadas |
| 5 | Análisis por dimensión: norma, evitar o sin preferencia clara; confirma o corrige la Fase 2 | Criterio validado con la persona |
| 6 | Genera la skill: criterio + normas del canal, del sector y de salida + checklist + rúbrica | Skill lista para instalar |

Oficios: diseñador gráfico, diseñador web, director creativo, filmmaker, fotógrafo, cinematográfico y content creator.
Recomendación: **una skill por uso y sector**, y esfuerzo alto o superior.

## Instalación

- **Claude Code:** copia `creador-skills-creativas/` a `~/.claude/skills/` (o a `.claude/skills/` de tu proyecto).
- **claude.ai / app de Claude:** sube el paquete `.skill` desde la configuración de skills. Un `.skill` es un zip de la carpeta:
  `zip -r creador-skills-creativas.skill creador-skills-creativas -x '*/__pycache__/*'`.
- Activa la **extensión de Chrome de Claude** para la búsqueda. Sin ella funciona en modo reducido (búsqueda web, sin miniaturas).
- Los scripts necesitan Python 3.8 o superior, sin dependencias.

## Script de referencias

`creador-skills-creativas/scripts/refs.py` guarda todo en `creative-workspace/<slug>/refs.json`, para poder cortar y retomar:

| Comando | Para qué |
|---|---|
| `init` | Crea el espacio de trabajo con el encuadre |
| `add` | Añade una tanda de referencias desde un JSON (pone ids, quita repetidas y parámetros de seguimiento) |
| `validate` | Comprueba la Fase 1 (10 × 5) o la Fase 3 (≥200, plataformas, contraste, etiquetas) |
| `board` | Tablero HTML para elegir (Fase 2) o puntuar (Fase 4) |
| `pick` / `score` | Registran lo contestado por encuesta: elecciones y notas |
| `apply` | Aplica lo descargado del tablero (`picks.json`, `ratings.json`) |
| `status` | Dice en qué fase está el trabajo, cuánta evidencia hay por dimensión y el siguiente paso |
| `stats` | Criterio por dimensión: cada tipología comparada con el resto de su dimensión |
| `export-skill` | Escribe la evidencia y las referencias en `references/` de la skill final |

## Contenido

```
creador-skills-creativas/
├── SKILL.md                         # el flujo completo
├── references/
│   ├── preguntas.md                 # las 3 encuestas de la Fase 0
│   ├── usos.md                      # dimensiones, tipologías, plataformas y normas por uso, canal y sector
│   ├── plataformas.md               # extensión de Chrome, modo reducido, qué guardar, obstáculos
│   └── plantilla-skill-final.md     # estructura de la skill generada
└── scripts/refs.py                  # base de referencias, tableros, análisis y exportación
tests/test_refs.py                   # pruebas del script: python3 -m unittest discover tests
```

## Notas

- Se guardan enlaces, autor y notas; **no** se descargan ni se suben imágenes. Que una plataforma sea gratuita no significa que sus
  obras se puedan reutilizar.
- Las normas solo salen de lo que el creativo puntúa: si una dimensión no marca diferencia en sus notas, queda libre en la skill.
