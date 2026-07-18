# Semana 5 — Tracing: ver lo que el analizador no ve
> **Guía técnica:** SOP-05 *(pendiente)* · **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 5 · **Módulo:** 4

**De:** Ing. Samuel Cifuentes — *"El analizador lógico ve los pines; yo necesito ver
el **scheduler**: quién corrió, cuándo, por qué, y quién esperó. La próxima semana
empezamos análisis de planificabilidad y no pienso discutir sobre suposiciones.
Instrumenten el nodo con tracing y tráiganme la primera traza donde se vea una
apropiación completa."*

El GPIO + analizador seguirá siendo el juez de los *números* (no perturba); el
tracing es el juez de la *historia* (quién y por qué). Se usan juntos.

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿Puedo ver una apropiación, no inferirla? | Traza con el instante exacto del switch |
| **Edwin** | En campo, ¿cómo diagnostico sin analizador? | El tracing viaja en el firmware |

## Lo que vas a medir

| Medición | Tu valor | Contraste |
|---|---|---|
| Cambio de contexto según la traza | ____ µs | vs. GPIO (sem. 4): ____ µs |
| Latencia ISR → hilo según la traza | ____ µs | vs. GPIO: ____ µs |
| CPU load por hilo (%) en operación normal | ____ | suma ≈ 100 % con idle |
| Overhead del tracing sobre el jitter del muestreo | ____ µs | medido con GPIO, tracing on/off |

## Tareas

### Tarea A — Habilitar el tracing
- Activa el subsistema de tracing de Zephyr en el nodo (SystemView si hay sonda;
  CTF por UART si no — el SOP da ambas rutas).
- **Evidencia:** primera traza abierta en el visor, con los hilos del nodo nombrados.

### Tarea B — La historia de una apropiación
- Genera un evento de flujo mientras corre la consola: captura en la traza la
  cadena ISR → `k_msgq` → despertar del hilo → apropiación de la consola.
- Anota los timestamps y compara contra la medición por GPIO.
- **Evidencia:** captura de la traza anotada (flechas sobre los eventos).

### Tarea C — El precio de mirar
- El tracing también es carga. Mide el jitter del muestreo (protocolo de siempre,
  por GPIO) con tracing encendido y apagado; llena la fila 4.
- **Evidencia:** las dos capturas + el delta.

## ¿Y en FreeRTOS?

Mismo concepto, herramientas distintas: `configUSE_TRACE_FACILITY` + Tracealyzer
(comercial) o SystemView. La lección transferible es la del instrumento: todo
observador perturba — por eso el curso mide *con* GPIO y *explica* con trazas.

## Entregables (RET)

- **§3 Evidencia semana 5:** tabla + la traza anotada de la apropiación.
- **§1:** anota junto a cada `C_i` con qué instrumento se midió de aquí en adelante.

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — tracing operativo con hilos nombrados (20) · apropiación capturada (20) | 40 |
| **Evidencia** — tabla completa con ambos instrumentos (20) · traza anotada legible (10) | 30 |
| **Análisis** — traza vs. GPIO explicado (¿por qué difieren?) (15) · overhead del tracing leído correctamente (15) | 30 |
