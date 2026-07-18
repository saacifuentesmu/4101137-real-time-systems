# Formato de las sesiones

Formato heredado de 4201327 (donde funcionó), adaptado y compactado. Cada sesión
tiene hasta tres documentos, cada uno con un trabajo distinto:

| Doc | Audiencia | Contenido | Presupuesto |
|---|---|---|---|
| **lab.md** | Estudiantes | Misión (memo GreenField) → qué se mide → tareas con evidencia → entregables RET → rúbrica | ≤ ~1.500 palabras |
| **lecture.md** | Profesor (guion de los 40 min) | Objetivos, tabla de tiempos, ideas de tablero, malentendidos a anticipar, puente al lab | guion, no prosa |
| **sop.md** | Estudiantes (mecánica) | Solo comandos, cableado, verificaciones y troubleshooting — el *porqué* vive en el lab | **solo si la sesión lo necesita** (bring-ups pesados: SBC Linux, AMP/sysbuild, tracing) |

Reglas de compacidad (obligatorias): una sola explicación por concepto; tablas y
diagramas antes que prosa; preguntas sin respuesta incluida; matemática avanzada en
`<details>`; nada de secciones "TL;DR + In plain English + técnico" repitiéndose.

Secciones fijas del lab.md:

1. **Memo** del stakeholder (abre la sesión; también es el objetivo).
2. **Lo que vas a medir** — la tabla de evidencia con celdas `____` que el lab llena.
3. **Tareas** A/B/C, cada una con su línea **Evidencia:**.
4. **¿Y en FreeRTOS?** — 3–5 líneas: cómo se haría con esa API y cuándo esa opción gana.
5. **Entregables (RET)** — qué secciones del RET se actualizan hoy.
6. **Rúbrica** (tabla, 100 pts).

El entregable vivo del curso es el **RET — Reporte de Evidencia de Tiempos**
(plantilla en [plantillas/ret.md](plantillas/ret.md)): el equivalente ligero del DDR
de 4201327. Se actualiza cada semana, se entrega en el parcial y al cierre.

Plantillas: [plantillas/lab.md](plantillas/lab.md) ·
[plantillas/lecture.md](plantillas/lecture.md) ·
[plantillas/sop.md](plantillas/sop.md) · [plantillas/ret.md](plantillas/ret.md)
