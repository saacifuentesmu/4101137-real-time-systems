# Semana 8 — Workshop — la revisión de diseño
> **Lectura:** repaso de caps. 2, 4 y 7 — el cap. 14 trae soluciones de práctica. · **Módulo:** 3
> **Se entrega hoy:** Taller 1. **Alcance del workshop:** caps. 2, 4 y 7 + todo lo medido hasta la semana 7.

**De:** Ing. Samuel Cifuentes — *"Revisión de diseño formal. Cada pareja me presenta
el análisis completo de su nodo: task set, utilización, RTA con bloqueo, y la
evidencia que lo respalda. Es el mismo ejercicio que harán toda su carrera con otro
nombre: design review. El quiz es individual — necesito saber que **ambos** saben."*

## Formato de la sesión (3 h)

| Tiempo | Actividad |
|---|---|
| 0:00–0:40 | **Quiz individual** (teoría de caps. 2, 4, 7 — al estilo de los talleres) |
| 0:40–2:30 | **Workshop**: cada pareja completa y defiende su análisis (abajo) |
| 2:30–3:00 | Revisión cruzada: cada pareja audita el RET de otra con la rúbrica |

## El análisis a defender (con el RET al frente)

1. **Task set** (§1): las cinco tareas del Control, `C_i` medidos y su instrumento.
2. **Utilización** (§4): U, prueba aplicable (RM/hiperbólica/EDF) y veredicto.
3. **RTA** (§4): script, salida por tarea, `R_i ≤ D_i` — incluyendo `B_i` del mutex.
4. **Evidencia** (§3): cada número de arriba apunta a una captura o traza.
5. **Pregunta sorpresa**: Samuel cambia un parámetro (un período, un `C_i`) en vivo
   — la pareja re-corre el script y re-lee el veredicto en minutos, no en días.

## Entregables

- Quiz individual (en el aula).
- **RET congelado v1** (tag `workshop` en el repo del equipo) con §1–§4 completos.
- Taller 1 resuelto (se entrega al inicio). Taller 2 sigue en curso (semana 9).

## Rúbrica (100 pts del workshop)

| | pts |
|---|---|
| **Quiz individual** — teoría caps. 2, 4, 7 | 40 |
| **Análisis defendido** — task set + U + RTA correctos y coherentes con la evidencia (30) · respuesta al cambio en vivo (10) | 40 |
| **RET v1** — completo, versionado, evidencia enlazada (15) · auditoría cruzada hecha con criterio (5) | 20 |
