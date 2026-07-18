# Semana 12 — Aislamiento e interferencia: el ensayo general del Hub
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 12 · **Módulo:** 5
> **Hoy cierra el contenido del curso** — lo que sigue es el proyecto.

**De:** Ing. Samuel Cifuentes — *"Último ensayo antes del proyecto. El Hub real
tendrá una GUI renderizando y telemetría entrando en ráfagas — quiero el lazo de
bombas blindado contra eso por **diseño**: afinidad, aislamiento de CPU y su
contrato DEADLINE, todo junto. Móntenme la maqueta de interferencia y muéstrenme el
lazo impávido. Ese montaje es, literalmente, el checkpoint 2 del proyecto."*

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿El diseño de aislamiento completo funciona junto? | Lazo + GUI sintética + ráfagas, medido |
| **Edwin** | ¿Qué configuración exacta despliego en campo? | La receta queda en el ADR, reproducible |

## Lo que vas a medir

| Medición (lazo de 10 ms, ≥ 5 min c/u) | Misses | Jitter máx (µs) |
|---|---|---|
| Lazo DEADLINE, CPUs compartidas, interferencia completa | ____ | ____ |
| Lazo DEADLINE **+ afinidad a CPU aislada**, misma interferencia | ____ | ____ |
| Igual que la anterior + IRQs movidas fuera de la CPU aislada | ____ | ____ |

Interferencia completa = carga de render sintética (`glxgears`/`stress-ng --vm`) +
ráfagas de red (`iperf3` hacia el SBC) — la GUI y el enrutamiento del Hub, simulados.

## Tareas

### Tarea A — La CPU del lazo
- Aísla un core (cmdline: `isolcpus=3 nohz_full=3 rcu_nocbs=3`, SOP-10) y fija el
  lazo con `taskset -c 3` (o `sched_setaffinity`).
- **Evidencia:** `cat /sys/devices/system/cpu/isolated` + el lazo corriendo allí (`ps -o psr`).

### Tarea B — La maqueta de interferencia
- Lanza la interferencia completa en las CPUs restantes. Corre las tres filas de la
  tabla (sin aislamiento / con aislamiento / con IRQs movidas — `/proc/irq/*/smp_affinity`).
- **Evidencia:** tabla + histogramas por condición.

### Tarea C — La receta de despliegue
- Escribe el ADR: la configuración completa del lazo del Hub (política + runtime/period
  + CPU + IRQs) como lista reproducible de comandos/cmdline, con el porqué de cada línea
  citando una fila de la tabla.
- **Evidencia:** ADR-004 en el RET; otro grupo debe poder replicarlo en 10 min.

## ¿Y en FreeRTOS?

La afinidad existe en FreeRTOS SMP (`vTaskCoreAffinitySet`) y el aislamiento es
"no pongas nada más en ese core" — posible porque todo el software es tuyo. Linux
necesita `isolcpus` + contratos porque el sistema corre software ajeno. Misma idea
de la semana 9 (particionar corta colas), un ecosistema más hostil.

## Entregables (RET)

- **§3 Evidencia semana 12:** tabla de tres configuraciones + histogramas.
- **§2 ADR-004 — Configuración RT del Hub** (la receta completa, justificada).

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — aislamiento verificado (15) · maqueta de interferencia completa (25) | 40 |
| **Evidencia** — tres configuraciones con protocolo constante (30) | 30 |
| **Análisis** — ADR-004 reproducible, cada línea justificada con una medición (30) | 30 |
