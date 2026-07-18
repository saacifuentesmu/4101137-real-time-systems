# Semana 11 — Tareas periódicas en Linux: de CBS a SCHED_DEADLINE
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 11 · **Módulo:** 5

**De:** Ing. Samuel Cifuentes — *"En el MCU las prioridades nos alcanzaban porque
controlábamos cada línea de código. En el Hub no: la GUI y el enrutamiento son
software que no escribimos. Necesito que el lazo de bombas tenga su CPU
**garantizada por contrato**, corra lo que corra al lado. Eso existe y viene de la
teoría que ya vieron: se llama SCHED_DEADLINE. Impleménten el lazo como tarea
periódica y demuéstrenme el aislamiento."*

Hoy se sigue el cap. 12 del libro casi al pie de la letra (pthread + patrón ptask).

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿El lazo cumple su período aunque un vecino se enloquezca? | Misses con FIFO vs. DEADLINE bajo un "hog" |
| **Edward** | ¿Un proceso comprometido puede matar de hambre al lazo? | Con DEADLINE, el contrato lo impide — demostrado |

## Lo que vas a medir

| Medición (lazo de 10 ms, ≥ 5 min) | Misses | Jitter máx (µs) |
|---|---|---|
| `SCHED_FIFO` prio 90, sistema tranquilo | ____ | ____ |
| `SCHED_FIFO` prio 90 + **hog FIFO prio 95** | ____ | ____ |
| `SCHED_DEADLINE` (runtime 2 ms / period 10 ms) + el mismo hog | ____ | ____ |

## Tareas

### Tarea A — La tarea periódica (cap. 12)
- Implementa el lazo de bombas como pthread periódico con `clock_nanosleep(TIMER_ABSTIME)`
  y contador de misses — el patrón ptask del libro (§12, código dado).
- Instrumenta con un GPIO del SBC (el analizador sigue siendo el juez).
- **Evidencia:** el lazo corriendo con misses = 0 en sistema tranquilo.

### Tarea B — Prioridades no bastan
- Corre el lazo con `chrt -f 90`. Lanza el "hog": un busy-loop con `chrt -f 95`
  (una prioridad mal asignada — error realista de integración).
- Llena la fila 2. El lazo se muere de hambre: captúralo.
- **Evidencia:** conteo de misses + captura del GPIO congelado.

### Tarea C — El contrato CBS
- Misma tarea, ahora `sched_setattr` con `SCHED_DEADLINE` (runtime 2 ms,
  deadline = period = 10 ms). El mismo hog al lado.
- Llena la fila 3. Conecta con la teoría en dos frases: el runtime/period es el
  `U_s = Q_s/T_s` del CBS — el aislamiento que el libro promete, observado.
- **Evidencia:** misses = 0 bajo el hog + las dos frases en el RET.

## ¿Y en FreeRTOS?

No hay equivalente: FreeRTOS (y Zephyr) dan prioridades, no *contratos de CPU*.
En un MCU el hog de la Tarea B se previene revisando el código propio; en un
sistema con software de terceros esa revisión es imposible — por eso el
reservation-based scheduling vive en Linux y por eso el Hub lo necesita.

## Entregables (RET)

- **§3 Evidencia semana 11:** la tabla de tres regímenes + capturas.
- **§4:** el presupuesto del lazo del Hub como CBS: `U_s` elegido y su margen
  (runtime medido de la Tarea A + colchón justificado).

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — tarea periódica ptask correcta (15) · hambruna reproducida (10) · DEADLINE aislando (15) | 40 |
| **Evidencia** — tabla completa + capturas de los tres regímenes (30) | 30 |
| **Análisis** — conexión CBS↔SCHED_DEADLINE en sus palabras (15) · presupuesto U_s justificado (15) | 30 |
