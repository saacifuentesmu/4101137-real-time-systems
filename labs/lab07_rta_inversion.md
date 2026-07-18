# Semana 7 — RTA e inversión de prioridad
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 7 · **Módulo:** 3
> **Taller 2 sale hoy** (ejercicios de cap. 7 + RTA; entrega semana 9).

**De:** Ing. Samuel Cifuentes — *"La prueba de utilización me dice si el conjunto
cabe; no me dice **cuánto tarda cada tarea en el peor caso** — y el e-stop tiene un
plazo de 5 ms, no un porcentaje. Impleménteme la RTA como script, con los C_i
medidos. Y ojo con los mutex: el Pathfinder se reinició en Marte por una inversión
de prioridad. Reprodúzcanla aquí, donde cuesta risa y no una misión."*

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿R_i ≤ D_i para *cada* tarea, con bloqueo incluido? | RTA en script + B_i medido |
| **Edward** | ¿Un comando malicioso lento puede retrasar el e-stop? | La inversión: reproducida y cerrada con PI |

## Lo que vas a medir

| Medición | Tu valor | Predicción RTA |
|---|---|---|
| R máx de la tarea de control (sin mutex) | ____ µs | ____ µs |
| R máx del control **durante la inversión** | ____ µs | — (eso es lo roto) |
| R máx del control con mutex PI | ____ µs | ≤ C + B_i + interferencia: ____ µs |
| B_i real (sección crítica más larga del tercero) | ____ µs | |

## Tareas

### Tarea A — La RTA como herramienta
- Escribe el script (Python) de la recurrencia `R_i = C_i + Σ⌈R_i/T_h⌉·C_h`
  (Fig. 4.17 del libro) y aliméntalo con los `C_i` medidos del nodo.
- Verifica: ¿el R que predice para el control coincide con el máximo observado en
  30 s de captura? (¿por qué "casi"? — el peor caso es raro; anótalo.)
- **Evidencia:** el script en el repo + salida vs. medición.

### Tarea B — La inversión, en vivo
- Tres hilos: control (alta) y consola-lenta (baja) comparten un mutex **sin PI**
  (`k_sem` de 1 usado como lock — así se rompe); telemetría (media) no usa el lock.
- Dispara la secuencia clásica: baja toma el lock → alta lo pide → media apropia a
  la baja. Captura el retraso de la alta.
- **Evidencia:** captura del analizador con la inversión anotada (quién corre en cada tramo).

### Tarea C — El arreglo
- Sustituye por `k_mutex` (Zephyr hereda prioridad). Repite la secuencia; llena las
  filas 3–4. Extiende tu script: `R_i = C_i + B_i + interferencia`.
- **Evidencia:** captura del "después" + RTA extendida coincidiendo con lo medido.

## ¿Y en FreeRTOS?

Los mutex de FreeRTOS (`xSemaphoreCreateMutex`) también heredan prioridad — y sus
semáforos binarios también permiten el mismo error de la Tarea B. La lección es
idéntica en ambos kernels: para exclusión mutua entre prioridades, mutex con PI,
nunca un semáforo desnudo.

## Entregables (RET)

- **§4:** RTA completa del task set real (script + salida), con B_i.
- **§3 Evidencia semana 7:** las tres capturas (sin lock / inversión / PI).
- **§2 ADR-002 — Política de exclusión mutua del nodo** (mutex PI, dónde y por qué).

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — script RTA correcto (15) · inversión reproducida (15) · cerrada con PI (10) | 40 |
| **Evidencia** — capturas anotadas de los tres regímenes (20) · B_i medido (10) | 30 |
| **Análisis** — RTA vs. medición bien leída (15) · ADR-002 con números (15) | 30 |
