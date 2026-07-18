# Semana 4 — La migración completa y el A/B
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 4 · **Módulo:** 2

**De:** Ing. Samuel Cifuentes — *"Terminen la migración y tráiganme el A/B:
superloop vs. kernel, mismas tareas, misma placa, mismas condiciones. Con esa tabla
decidimos la arquitectura del producto — y la defiendo yo ante Gustavo, así que
quiero poder citarla sin vergüenza."*

Hoy se completa el mapeo de la charla: cada pieza del superloop encuentra su
contraparte del kernel.

| Pieza del superloop | Contraparte kernel |
|---|---|
| Bandera de ISR + chequeo en el loop | ISR corta + `k_msgq` / `k_sem` |
| Trabajo pesado poleado | Hilo con prioridad propia |
| "Bottom half" improvisado en el loop | `k_work` en la workqueue |
| Consola que bloquea todo | Hilo de consola en prioridad baja |

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿El kernel mejora el peor caso, no solo el promedio? | A/B con máximos, no promedios |
| **Gustavo** | ¿Qué compramos con la complejidad nueva? | El comando bloqueante ya no rompe nada — medido |

## Lo que vas a medir

| Medición (S3) | Superloop (sem. 3) | Kernel (hoy) |
|---|---|---|
| Jitter máx del muestreo | (copiar) | ____ µs |
| Jitter máx del muestreo con comando bloqueante | (copiar) | ____ µs |
| Latencia ISR → hilo (vía msgq) | — | ____ µs |
| Overhead: ancho del cambio de contexto visible | — | ____ µs |

## Tareas

### Tarea A — Completar la migración
- Control → hilo de prioridad alta; consola → hilo de prioridad baja; el trabajo
  diferido de la ISR de flujo → `k_work`. El `main` queda casi vacío.
- Mantén los mismos GPIO de instrumentación (la comparación exige simetría).
- **Evidencia:** el nodo completo corriendo, árbol de hilos (`kernel threads` en el shell o listado en código).

### Tarea B — El A/B
- Repite el protocolo de medición de la semana 2 exacto (misma duración, mismas
  condiciones) sobre la versión kernel. Llena la tabla.
- **Evidencia:** tabla A/B completa + capturas de ambas condiciones.

### Tarea C — El costo
- El kernel no es gratis: mide el cambio de contexto (dos toggles consecutivos de
  hilos distintos) y estima el overhead por segundo a tu carga actual.
- **Evidencia:** el número + el cálculo en una línea.

## ¿Y en FreeRTOS?

El mapeo es 1:1: `k_msgq`→`xQueue`, `k_work`→timer daemon o tarea propia,
prioridades apropiativas iguales. La diferencia práctica está en los defaults:
FreeRTOS arranca con menos servicios (footprint menor — su fortaleza en chips
chicos); Zephyr trae consola/log/shell listos (su fortaleza en productos grandes).

## Entregables (RET)

- **§2 ADR-001 — Arquitectura del nodo: kernel multihilo.** Contexto (línea base +
  comando bloqueante), decisión, justificación **citando la tabla A/B**, estado.
- **§3 Evidencia semana 4:** tabla A/B + overhead medido.

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — migración completa según el mapeo (25) · instrumentación simétrica (15) | 40 |
| **Evidencia** — A/B con protocolo idéntico al de la sem. 2 (20) · overhead medido (10) | 30 |
| **Análisis** — ADR-001 citando números, con el costo reconocido (no solo el beneficio) (30) | 30 |
