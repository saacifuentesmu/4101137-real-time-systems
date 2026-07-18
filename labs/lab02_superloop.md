# Semana 2 — El superloop provisto: correr, leer, medir
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 2 · **Módulo:** 1
> **Firmware:** [firmware/superloop/](../firmware/superloop/) (provisto — hoy no se escribe código)

**De:** Ing. Samuel Cifuentes — *"Antes de proponerme un kernel, midan lo que ya
tenemos. Les entrego el nodo Control como superloop — la arquitectura de 4100901,
la que la empresa sabe mantener. Quiero la línea base: latencia y jitter de cada
tarea, con números, no con adjetivos. Si el superloop alcanza, nos quedamos con él."*

El firmware ya trae **instrumentación por GPIO** (un toggle al entrar/salir de cada
tarea): tu instrumento es el analizador lógico.

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿El superloop cumple el task set del escenario? | Tabla de jitter por tarea vs. sus deadlines |
| **Gustavo** | ¿Por qué pagaríamos la complejidad de un kernel? | El comando bloqueante: la degradación, medida |

## Lo que vas a medir

| Medición (C0116-DK, silicio sin caché) | Tu valor | Referencia |
|---|---|---|
| Período real del muestreo (nominal 1 kHz): promedio | ____ µs | 1000 µs |
| Jitter del muestreo: máx sobre ≥ 30 s | ____ µs | anótalo: es *la línea base del curso* |
| Latencia ISR → atención en el loop (botón/flujo) | ____ µs | |
| Jitter del muestreo **con el comando bloqueante activo** | ____ µs | compara contra la fila 2 |

## Tareas

### Tarea A — Correr y leer
- Compila y flashea `firmware/superloop/` para `stm32c0116_dk`; verifica la consola.
- Lee `main.c` con tu pareja: identifica las banderas de ISR, el trabajo poleado y
  dónde toggle-a cada GPIO de instrumentación. Dibuja el flujo en ≤ 10 cajas.
- **Evidencia:** el diagrama (foto de papel vale) con los GPIO de instrumentación marcados.

### Tarea B — La línea base
- Conecta el analizador lógico a los GPIO de instrumentación; captura ≥ 30 s.
- Llena las tres primeras filas de la tabla. Usa las estadísticas de pulso del
  software del analizador (period/width min–max).
- **Evidencia:** capturas del analizador + tabla llena en el RET.

### Tarea C — Romperlo a propósito
- Activa el **comando bloqueante** de la consola mientras capturas.
- Llena la fila 4. ¿Cuál tarea sufre y por qué? Explícalo en 2–3 frases apuntando a
  la línea de código responsable.
- **Evidencia:** captura del "antes/después" + la explicación en el RET.

## ¿Y en FreeRTOS?

Igual que en Zephyr: muchos productos con FreeRTOS *también* empiezan como
superloop + ISRs, y migran al kernel cuando aparece exactamente lo que viste en la
Tarea C — una tarea que bloquea a las demás. La pregunta de la próxima semana es la
misma en ambos mundos: ¿qué te da un scheduler apropiativo?

## Entregables (RET)

- **§1 Task set:** primera columna de `C_i` medidos (ancho de pulso de cada tarea).
- **§3 Evidencia semana 2:** la tabla de arriba, llena, con una frase de lectura.
- **§2 (aún no):** la decisión superloop-vs-kernel se toma en la semana 4, con el A/B.

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — firmware corriendo (10) · diagrama de flujo correcto (15) · comando bloqueante reproducido (15) | 40 |
| **Evidencia** — tabla completa con capturas (20) · condiciones de medición anotadas (duración, carga) (10) | 30 |
| **Análisis** — explicación causa-raíz de la degradación, con línea de código (20) · lectura de la línea base en una frase (10) | 30 |
