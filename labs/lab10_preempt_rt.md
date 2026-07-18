# Semana 10 — PREEMPT_RT: Linux entra al lazo
> **Guía técnica:** SOP-10 *(pendiente: imagen del SBC + kernel RT)* · **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 10 · **Módulo:** 5
> **Desde hoy:** grupos grandes (dos parejas), un SBC por grupo. El Kit Hub se necesita esta semana ([BOM](../BOM.md)).

**De:** Ing. Samuel Cifuentes — *"El Hub corre Linux: GUI, enrutamiento, nube — eso
no se hace en un MCU. Pero el Hub también controla la estación de bombas, y ahí
Linux tiene fama merecida de impuntual. La fama se acabó de discutir con opiniones:
instalen el kernel PREEMPT_RT y tráiganme la distribución de latencias — stock vs.
RT, sin carga y bajo carga. Con esa curva decidimos si el Hub puede tener deberes duros."*

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿Cuál es el peor caso de despertar en este SBC? | Histograma de `cyclictest`, máx bajo carga |
| **Gustavo** | ¿Necesitamos un MCU extra en el Hub, o basta Linux RT? | La cola del histograma responde |

## Lo que vas a medir

| Medición (`cyclictest`, ≥ 5 min c/u) | Máx (µs) | p99 (µs) |
|---|---|---|
| Kernel stock, sin carga | ____ | ____ |
| Kernel stock, **bajo carga** (`stress-ng` + tráfico) | ____ | ____ |
| Kernel PREEMPT_RT, sin carga | ____ | ____ |
| Kernel PREEMPT_RT, bajo carga | ____ | ____ |

## Tareas

### Tarea A — Bring-up del SBC
- Imagen con kernel PREEMPT_RT en el SBC del grupo (SOP-10: imagen preparada del
  curso o kernel RT del distro). Verifica: `uname -v` debe decir `PREEMPT_RT`.
- **Evidencia:** salida de `uname -a` + acceso SSH del grupo.

### Tarea B — La curva que decide
- `cyclictest -m -Sp90 -i 1000 -h 400 -D 5m` en las cuatro condiciones de la tabla.
  Carga: `stress-ng --cpu 0 --io 2` + un `ping -f` desde un portátil (tráfico real).
- Grafica los cuatro histogramas (el SOP trae el script de ploteo).
- **Evidencia:** los cuatro histogramas + la tabla llena.

### Tarea C — Leer la cola
- En el RET: ¿dónde está el máximo de PREEMPT_RT bajo carga vs. el deadline de
  10 ms del lazo de bombas? ¿Y vs. los ~µs del MCU (semana 9)? Tres frases: qué
  puede y qué no puede prometer este SBC.
- **Evidencia:** el párrafo, citando los números de la tabla.

## ¿Y en FreeRTOS?

Cambio de escala, misma pregunta. En el MCU, el peor caso lo daba el kernel chico
(FreeRTOS o Zephyr: ~µs); en Linux lo da el kernel gigante (~decenas–cientos de µs
incluso con RT). La arquitectura del Hub —qué vive en Linux y qué exigiría volver a
un MCU— es exactamente esa comparación, y es el ADR central del proyecto final.

## Entregables (RET)

- **§3 Evidencia semana 10:** tabla + histogramas de las cuatro condiciones.
- **§1:** nueva sección del task set: las tareas del Hub (bombas, interlock, GUI,
  enrutamiento) con sus tipos y deadlines — `C_i` pendientes.

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — kernel RT verificado (15) · cuatro corridas con protocolo constante (25) | 40 |
| **Evidencia** — histogramas legibles + tabla (30) | 30 |
| **Análisis** — lectura de la cola vs. deadlines del Hub y vs. el MCU (30) | 30 |
