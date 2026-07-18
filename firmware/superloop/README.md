# firmware/superloop — el superloop provisto

**Estado: pendiente de autoría (Sam).** App Zephyr de referencia que los estudiantes
**corren, leen y miden** en la semana 2 — su *get started* con Zephyr — y que el
módulo 2 migra guiadamente a hilos del kernel.

Especificación (del [escenario](../../PROJECT_SCENARIO.md)):

- Un solo hilo `main` + ISRs — sin scheduler. La arquitectura de 4100901, en Zephyr.
- Tareas del nodo: muestreo periódico (duro), lazo de control → PWM, consola UART
  (firme), telemetría por consola (suave).
- **Instrumentación por GPIO** en cada tarea (toggle al entrar/salir) para medir
  latencia y jitter con el analizador lógico — el lab de la semana 2 vive de esto.
- Un "comando bloqueante" en la consola que degrada el jitter a propósito — el
  argumento vivo para el módulo 2.

Targets: `stm32c0116_dk` (primario, semanas 1–2) y `esp32s3_devkitc` vía overlay
(semana 3 — el porte es parte de la lección). `native_sim` compila para desarrollo;
no sirve para medir tiempos.

Cada pieza (banderas de ISR, trabajo poleado, bottom halves) debe tener su
contraparte nombrada en la migración del módulo 2 — el mapeo superloop → kernel es
el contenido de la charla de la semana 3.
