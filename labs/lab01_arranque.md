# Semana 1 — Arranque: el equipo, la placa, el toolchain
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 1 · **Módulo:** 0
> **Prerrequisito:** [setup_previo.md](setup_previo.md) hecho en casa.

**De:** Ing. Samuel Cifuentes (Arquitecto Senior) — *"Bienvenidos al equipo de
Sistemas de Control. SoilSense ya mide; ahora tiene que **actuar**, y una válvula
que cierra tarde revienta mangueras. Antes de hablar de kernels: quiero a todo el
mundo compilando y flasheando sin fricción. Esta semana el entregable es un entorno
que funciona."*

Hoy: formar parejas, verificar el entorno de cada uno, y correr código en las dos
plataformas de arranque (STM32C0116-DK física y `native_sim`).

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿El equipo puede iterar rápido? | Ciclo compilar→flashear→monitor < 1 min, demostrado |

## Lo que vas a medir

Todavía nada de tiempos — esta semana se mide el *setup*:

| Verificación | ✓ |
|---|---|
| blinky corre en la C0116-DK de la pareja | |
| `hello_world` corre en `native_sim` | |
| Consola serial abierta y con eco | |
| RET del equipo creado desde la plantilla | |

## Tareas

### Tarea A — Verificación cruzada del entorno
- Cada integrante compila y flashea blinky en la C0116-DK **desde su propio portátil**.
- `west build -p -b stm32c0116_dk zephyr/samples/basic/blinky && west flash`
- **Evidencia:** LED parpadeando, un flash por integrante.

### Tarea B — Consola serial
- Flashea `zephyr/samples/hello_world` y abre el monitor serial (115200 8N1).
- Cambia el mensaje, recompila, verifica el ciclo completo de iteración.
- **Evidencia:** captura del monitor con el mensaje modificado.

### Tarea C — Crear el RET del equipo
- Copien [plantillas/ret.md](../plantillas/ret.md) a su repo de equipo; llenen
  encabezado y la fila del lazo de control con los valores del
  [escenario](../PROJECT_SCENARIO.md) (período 10 ms; `C_i` queda `____` hasta medirlo).
- **Evidencia:** enlace al repo del equipo con el RET versionado.

## ¿Y en FreeRTOS?

No hay equivalente de `west`/devicetree: cada silicio trae su SDK del fabricante
(ESP-IDF, STM32Cube, nRF Connect) y FreeRTOS va embebido dentro. Ese es el
trade-off que iremos midiendo: Zephyr paga curva de aprendizaje una vez y viaja
entre chips; FreeRTOS se aprende rápido pero el entorno cambia con cada fabricante.

## Entregables (RET)

- **Encabezado + §1:** equipo, placas, task set inicial del Control (de la charla y
  el escenario), todos los `C_i` en `____`.

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — blinky por integrante (20) · ciclo serial completo (20) | 40 |
| **Evidencia** — capturas + repo del equipo con RET (30) | 30 |
| **Análisis** — task set inicial correcto en el RET: tipos D/F/S bien asignados (30) | 30 |
