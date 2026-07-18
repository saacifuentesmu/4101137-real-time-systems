# Guía de Lectura — Buttazzo, *Hard Real-Time Computing Systems* (4.ª ed.)

Referencia del curso: Giorgio Buttazzo, *Hard Real-Time Computing Systems*, 4.ª ed.,
Springer, 2024 (ver nota de ediciones en el [README](README.md#reference); disponible
vía SpringerLink/SINAB).

**Regla general: leer enunciados, ejemplos y figuras; saltar las demostraciones.**
El libro encierra cada derivación en bloques *Proof* explícitos — la mayoría de la
matemática del libro es el autor *demostrando* los resultados, no usándolos. En este
curso los laboratorios reemplazan a las demostraciones: donde el libro prueba un
teorema, ustedes lo verifican con el analizador lógico y las trazas. La matemática
que sí se usa (la de los reportes de evidencia de tiempos) cabe en unas diez fórmulas
y dos algoritmos cortos — están listados al final.

## Lectura por semana

| Semana | Módulo | Leer | Saltar | Nota |
|--------|--------|------|--------|------|
| 1 | 0 | §1.1–1.2 | — | Cierre del repaso (digitales → estructuras → control): qué es tiempo real; las historias del Shuttle y del Patriot son el argumento del curso |
| 2 | 1 | §1.3, §2.1–2.3 | §2.4 (se retoma en la semana 10) | El vocabulario del semestre: modelos de tarea, tipos de restricción, fuentes de impredecibilidad (DMA, caché, interrupciones, syscalls) |
| 3 | 2 | §10.1–10.3 | §10.4–10.5 (detalle de implementación) | Anatomía de un kernel RT: estados, colas de listos, cambio de contexto — Zephyr como ejemplo vivo |
| 4 | 2 | §10.6–10.7 | Implementación de CABs (§10.6.2) | Comparar los CABs con las message queues de Zephyr; §10.7: el overhead del kernel existe y se mide (A/B contra la línea base de la semana 2) |
| 5 | 5 | §13.5.1; §1.3 (releer con ojos de medición) | — | El libro es corto en *cómo* medir; eso lo cubre el laboratorio de tracing |
| 6 | 3 | §4.1–4.4 (enunciados, tablas y ejemplos), §4.7; enunciado de optimalidad de EDF (§3.3.1) | Las derivaciones de U_lub (§4.3.2–4.3.3, ~7 páginas de cálculo), demostraciones de Teo. 4.1 y 4.2; el resto del cap. 3 | El ejemplo de la Fig. 4.13 (RM falla, EDF no, con U = 0.97) se reproduce en el lab sobre la S3; además se induce jitter en el lazo de flujo y se mide la degradación del control. **Taller 1**: ejercicios de caps. 2 y 4 (soluciones en cap. 14; entrega en el parcial). Opcional (PDF gratuito): Lee & Seshia, *Introduction to Embedded Systems*, cap. 2 — control realimentado |
| 7 | 3 | §4.5.1–4.5.2 (RTA); §7.1–7.3, reglas de PIP (§7.6.1) y PCP (§7.7.1), enunciado del Teo. 7.2 | §4.5.3–4.5.4; cadena de lemas de §7.6.2, cómputo exacto de bloqueo (§7.6.3), §7.8 (SRP) | La RTA es un algoritmo de 15 líneas (Fig. 4.17), no un teorema: en el lab se implementa en Python con los C_i medidos. **Taller 2**: ejercicios de cap. 7 + RTA (entrega semana 9) |
| 8 | 3 | Repaso: caps. 2, 4 y 7 | — | **Parcial** — el cap. 14 trae soluciones de los ejercicios de los caps. 1–9 para practicar |
| 9 | 4 | §13.1–13.2 | — | FreeRTOS **no está en el libro**; la referencia práctica es la documentación de ESP-IDF. El cap. 13 da el panorama: muchos kernels, una teoría |
| 10 | 5 | §13.5 (herramientas de WCET y análisis); §2.4 | — | El libro no tiene capítulo de multiprocesador — las anomalías de §2.4 son el gancho teórico; el resto es material del curso. WCET: medición vs. análisis estático vs. high-water-mark + margen. El lab SMP corre bajo ESP-IDF/FreeRTOS (el SMP de Zephyr en Xtensa sigue no funcional) |
| 11 | 6 | §6.9.1–6.9.4 (CBS); §9.3 (la idea de reserva de recursos); §13.3.4–13.3.5 (PREEMPT_RT, SCHED_DEADLINE) | Resto de caps. 5–6 (los demás servidores: una lámina de intuición basta); §6.9.5–6.9.6 | El CBS son 3 reglas en pseudocódigo (Fig. 6.15) más dos resultados de una línea: aislamiento (U_s = Q_s/T_s pase lo que pase) y R_i ≈ C_i/U_s. Eso *es* SCHED_DEADLINE |
| 12 | 6 | **Cap. 12 completo**; §13.1.1 (RT-POSIX) | — | Casi sin matemática: es código C (pthread + biblioteca ptask). El laboratorio lo sigue casi literalmente |
| 13 | 7 | Cap. 11: §11.2 (de requisitos a restricciones de tiempo), §11.3, §11.5.2 (criticidad mixta) | — | La tabla de tareas del robot en §11.4 (períodos, WCETs, duro/suave) es el espejo del task set del SoilSense Control. Vocabulario de seguridad funcional (no está en el libro): watchdog, estado seguro, IEC 61508 / DO-178C |
| 14–16 | 7 | — | — | Sin lectura nueva; caps. 11–12 como referencia de trabajo del proyecto |

## La matemática que sí se usa

Estas son las fórmulas y algoritmos que aparecen en los entregables (análisis de
planificabilidad de los reportes de evidencia de tiempos):

- Modelo de tarea periódica: `a_{i,j} = Φ_i + (j−1)T_i`, `d_{i,j} = a_{i,j} + D_i` (§4.5).
- Factor de utilización: `U = Σ C_i/T_i` (§4.1.1).
- Prueba RM (Liu & Layland): `U ≤ n(2^{1/n} − 1)` — el resultado y la Tabla 4.2 (§4.3.3).
- Prueba hiperbólica (menos pesimista): `∏(U_i + 1) ≤ 2` (Teo. 4.1).
- Prueba EDF: `U ≤ 1`, necesaria y suficiente (Teo. 4.2).
- Recurrencia de la RTA: `R_i = C_i + Σ_{h<i} ⌈R_i/T_h⌉ C_h`, iterada hasta punto
  fijo (Fig. 4.17) — se implementa como script.
- Cota de bloqueo bajo PIP: a lo sumo `min(l_i, s_i)` secciones críticas; `B_i` = suma
  de las más largas (Teo. 7.2); la RTA extendida usa `R_i = C_i + B_i + interferencia`.
- CBS/SCHED_DEADLINE: ancho de banda `U_s = Q_s/T_s` (aislamiento, Teo. 6.8) y
  tiempo de respuesta `R_i ≈ C_i/U_s` (§6.9.6).

Todo lo demás — las minimizaciones con derivadas del cap. 4, las cadenas de lemas del
cap. 7, los análisis de servidores de los caps. 5–6, el cap. 8 y casi todo el cap. 9 —
queda fuera del alcance del curso.
