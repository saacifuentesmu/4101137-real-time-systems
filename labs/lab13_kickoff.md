# Semana 13 — Kickoff del SoilSense Hub
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 13 · **Módulo:** 6
> Cubre también los checkpoints (sem. 14–15) y el demo day (sem. 16).

**De:** Ing. Samuel Cifuentes — *"Arranca el proyecto. El Hub es una sola caja con
tres personalidades: controla las bombas (duro), atiende a un humano (GUI) y mueve
datos (enrutamiento). Ya midieron todo lo que necesitan para diseñarlo — hoy no se
programa: hoy se **decide**, por escrito. Un sistema de criticidad mixta se diseña
antes de teclear, o se depura para siempre."* — Detalle del reto y stakeholders en
el [escenario](../PROJECT_SCENARIO.md).

## Lo que se decide hoy (los ADRs del kickoff)

| ADR | La decisión | La evidencia que la sostiene |
|---|---|---|
| **ADR-P1 — Partición Linux vs. MCU** | Qué corre en el SBC y qué exigiría un MCU (S3) | Colas: sem. 9 (µs, MCU) vs. sem. 10 (Linux RT) |
| **ADR-P2 — Presupuesto temporal** | Task set del Hub con sus `REQ-HUB-xx` (EARS, como en la sem. 2): tipos D/F/S, períodos, deadlines, presupuesto extremo-a-extremo sensor→válvula | Task set del RET §1 + RTA/CBS de §4 |
| **ADR-P3 — Aislamiento** | Política + runtime/period + CPU + IRQs del lazo | La receta de la sem. 12 (ADR-004), adaptada |
| **ADR-P4 — Seguridad funcional** | **Estado seguro** (falla ⇒ válvula cerrada) + watchdog: quién patea, quién muerde, qué pasa al morder | Requisito del escenario; se demuestra en el checkpoint 2 |

## Tareas de la sesión

### Tarea A — Propuesta de arquitectura
- Diagrama de la caja: procesos/hilos, políticas de scheduling, CPUs, y el camino
  del dato crítico (sensor de presión → interlock → válvula) marcado en rojo.
- **Evidencia:** el diagrama + los 4 ADRs en borrador defendido ante Samuel (en el aula).

### Tarea B — Plan de checkpoints
- Declaren *qué número* demostrará cada checkpoint (no "avance": un número).
- **Evidencia:** las dos metas escritas en el RET, con su condición de carga.

## Los tres hitos

| Semana | Hito | Se aprueba si… |
|---|---|---|
| 14 | **Checkpoint 1** | El lazo duro del Hub cumple deadlines bajo carga sintética (protocolo sem. 12), misses = 0, tabla presentada |
| 15 | **Checkpoint 2** | GUI + enrutamiento reales integrados; evidencia de interferencia + presupuesto extremo-a-extremo medido; **el watchdog muerde en vivo** (se mata el lazo y la válvula cierra sola) |
| 16 | **Demo day** | Demo en vivo + **RET final** + reporte de evidencia de tiempos del Hub |

## Rúbrica del proyecto (100 pts)

| | pts |
|---|---|
| **Kickoff** — 4 ADRs defendidos, con evidencia citada, no opinión (20) | 20 |
| **Checkpoint 1** — meta numérica cumplida y medida con protocolo declarado (15) | 15 |
| **Checkpoint 2** — interferencia real + presupuesto e2e + fail-safe demostrado (20) | 20 |
| **Demo day** — demo en vivo estable (15) · RET final: task set, análisis y evidencia coherentes de punta a punta (25) · postmortem honesto: qué no cumplió y por qué (5) | 45 |
