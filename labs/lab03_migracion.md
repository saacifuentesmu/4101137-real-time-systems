# Semana 3 — El porte a la S3 y el primer hilo
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 3 · **Módulo:** 2

**De:** Ing. Samuel Cifuentes — *"Dos noticias. Uno: producción eligió la ESP32-S3
para el nodo — más memoria, radio, y dos núcleos que usaremos después. Dos: vi la
línea base con el comando bloqueante; autorizo evaluar el kernel. Primero muévanme
el superloop a la S3 **sin reescribirlo** — si eligieron bien la plataforma de
software, eso cuesta un overlay, no un porting. Luego, el primer hilo."*

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿Cuánto costó cambiar de silicio? | Líneas cambiadas: contarlas en el diff |
| **Gustavo** | ¿La S3 es "peor" para tiempo real que la M0+? | Comparación de jitter mismo-código, dos chips |

## Lo que vas a medir

| Medición | C0116-DK (sem. 2) | S3 (hoy) |
|---|---|---|
| Jitter máx del muestreo (superloop) | (copiar) | ____ µs |
| Latencia ISR → atención | (copiar) | ____ µs |
| Jitter máx del muestreo **con el hilo de muestreo** (kernel) | — | ____ µs |

## Tareas

### Tarea A — El porte (devicetree en acción)
- `west build -p -b esp32s3_devkitc/esp32s3/procpu firmware/superloop` con el
  overlay de pines para la S3 (los GPIO de instrumentación cambian de puerto).
- Cuenta el costo real del porte: `git diff --stat` — ¿cuántas líneas, y de qué tipo
  (¿código C o descripción de hardware?)?
- **Evidencia:** el diff-stat + el superloop corriendo en la S3.

### Tarea B — Dos silicios, mismo código
- Repite la medición de línea base de la semana 2 sobre la S3; llena la columna S3.
- ¿Dónde aparece jitter que la M0+ no tenía? (Pista de la charla: la flash externa
  y su caché.) Dos frases en el RET.
- **Evidencia:** tabla comparativa + capturas.

### Tarea C — El primer hilo
- Migra **solo la tarea de muestreo** a un hilo del kernel (`K_THREAD_DEFINE`,
  prioridad apropiativa, `k_msgq` hacia el loop principal) siguiendo el mapeo de la
  charla. El resto sigue en el superloop.
- Mide: ¿el comando bloqueante sigue arruinando el muestreo?
- **Evidencia:** captura con el comando bloqueante activo + jitter del hilo.

## ¿Y en FreeRTOS?

La Tarea C sería `xTaskCreate(sample_task, "sample", stack, NULL, prio, NULL)` +
`xQueueSend`/`xQueueReceive` — API distinta, mismo concepto. Lo que FreeRTOS **no**
tiene es la Tarea A: sin devicetree, cambiar de STM32 a ESP32 es cambiar de SDK, no
de overlay.

## Entregables (RET)

- **§3 Evidencia semana 3:** tabla de dos silicios + explicación del jitter nuevo.
- **§1:** `C_i` re-medidos en la S3 (la plataforma definitiva del task set).

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — porte con overlay, sin tocar C (15) · hilo de muestreo funcionando (25) | 40 |
| **Evidencia** — tabla comparativa completa (20) · diff-stat del porte (10) | 30 |
| **Análisis** — lectura correcta del jitter M0+ vs S3 (15) · por qué el hilo sobrevive al comando bloqueante (15) | 30 |
