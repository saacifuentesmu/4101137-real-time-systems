# Semana N — <Título de la sesión>
> **Guía técnica:** [SOP-NN](sop.md) *(borrar esta línea si la sesión no tiene SOP)*
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana N · **Módulo:** M

**De:** <Stakeholder> (<rol>) — *"<El problema, en una o dos frases del proyecto.>"*

<Un párrafo: qué se construye/mide hoy y por qué importa. Cerrar con:>
**Misión:** <una frase operativa>.

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **<Nombre>** | <pregunta> | <respuesta medible> |

## Lo que vas a medir

<La tabla que esta sesión debe llenar — columnas definidas, celdas vacías:>

| Medición | Tu valor | Objetivo | Nota |
|---|---|---|---|
| <p. ej. jitter p99 del lazo> | ____ µs | < ___ µs | <condición> |

## Tareas

### Tarea A — <nombre>
- <pasos mínimos; los comandos exactos van en el SOP>
- **Evidencia:** <log / captura del analizador / tabla llena>

### Tarea B — <nombre>
- ...
- **Evidencia:** ...

## ¿Y en FreeRTOS?

<3–5 líneas: la API equivalente (`xTaskCreate`/`xQueueSend`/...), qué cambia, y
cuándo elegir FreeRTOS sería lo correcto. Sin instalar nada — es comparación.>

## Entregables (RET)

- **§1 Task set:** <qué fila se agrega/actualiza, con C_i medido>
- **§2 ADR-NNN:** <decisión de hoy: contexto, decisión, números, estado>
- **§3 Evidencia semana N:** la tabla de arriba, llena, con una frase de lectura.
- **§4 Planificabilidad:** <si aplica: U, prueba usada, RTA>

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — <ítem> (xx) · <ítem> (xx) | 40 |
| **Evidencia** — tabla completa y bien leída (xx) · trazas anexas (xx) | 30 |
| **Análisis** — ADR justificado con números (xx) · <ítem> (xx) | 30 |
