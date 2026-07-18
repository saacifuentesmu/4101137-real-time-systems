# Semana 9 — Driver con devicetree y los dos núcleos (AMP)
> **Guía técnica:** SOP-09 *(pendiente: sysbuild/AMP)* · **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 9 · **Módulo:** 4
> **Se entrega hoy:** Taller 2.

**De:** Ing. Samuel Cifuentes — *"Dos encargos. Uno: el sensor de flujo merece un
driver de verdad, con su binding — no un `gpio_get` suelto en la app. Dos: la S3
tiene dos núcleos y estamos usando uno; quiero saber si el segundo núcleo puede
darle al lazo de control un **peor caso** mejor. La charla de hoy también les debe
una respuesta honesta: cuándo conviene FreeRTOS — porque algún cliente lo va a exigir."*

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿El segundo núcleo mejora la cola de la distribución? | Jitter p-máx con y sin núcleo dedicado |
| **Edwin** | ¿El sensor sobrevive un cambio de placa? | El driver queda detrás del binding, no en la app |

## Lo que vas a medir

| Medición | Tu valor | Nota |
|---|---|---|
| Jitter máx del lazo, 1 núcleo, sin carga | ____ µs | referencia (sem. 4) |
| Jitter máx del lazo, 1 núcleo, **con carga sintética** | ____ µs | la carga: hilo que revienta caché |
| Jitter máx del lazo en APPCPU, carga en PROCPU | ____ µs | el aislamiento particionado |
| Promedios de los tres casos | ____ | pista: casi no cambian — la cola sí |

## Tareas

### Tarea A — El driver con binding
- Convierte la lectura del YF-S401 en un driver Zephyr mínimo: binding devicetree
  propio (`vendor,yf-s401`), API de sensor, la app lo consume por `DEVICE_DT_GET`.
- **Evidencia:** el nodo funcionando igual que antes, pero con el sensor declarado
  en el overlay y ni un pin quemado en la app.

### Tarea B — AMP con sysbuild
- Dos imágenes (SOP-09): el **lazo duro** (con su GPIO de instrumentación) para
  `esp32s3_devkitc/esp32s3/appcpu`; el resto del nodo + una **carga sintética**
  para `.../procpu`. Sin consola en la APPCPU (limitación real — `ets_printf` si
  necesitas depurar): se mide por GPIO, como siempre.
- **Evidencia:** ambas imágenes corriendo a la vez, toggle del lazo visible.

### Tarea C — La cola de la distribución
- Protocolo de siempre, ≥ 60 s por caso, llena la tabla. Compara **máximos**, no
  promedios: la tesis de la charla es que particionar no mejora el caso típico sino
  que corta los picos raros.
- **Evidencia:** tabla + las tres capturas.

## ¿Y en FreeRTOS?

Aquí FreeRTOS gana en esta placa: ESP-IDF trae SMP real en la S3 (scheduler global
sobre ambos núcleos, con pinning opcional por tarea), mientras el port Xtensa de
Zephyr aún no tiene SMP — hoy lo esquivamos con AMP. Criterio honesto: si tu
producto es "esta S3 con radio y dos núcleos exprimidos", ESP-IDF/FreeRTOS es la
opción madura; si es "una familia de productos sobre silicios variados", Zephyr.

## Entregables (RET)

- **§3 Evidencia semana 9:** la tabla de tres casos + lectura en una frase.
- **§2 ADR-003 — ¿El lazo duro vive en su propio núcleo?** Decisión con los números
  de la cola; incluye el costo (dos imágenes, sin consola en APPCPU).

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — driver con binding limpio (20) · AMP corriendo (20) | 40 |
| **Evidencia** — tabla de tres casos con protocolo constante (20) · capturas (10) | 30 |
| **Análisis** — máximos vs. promedios bien leídos (15) · ADR-003 con costo reconocido (15) | 30 |
