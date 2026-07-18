# GreenField Technologies: Briefing del Proyecto

**Tipo de documento**: Contexto de proyecto y guía de stakeholders

**Audiencia**: Ingenieros de Firmware — Equipo de Sistemas de Control (estudiantes)

---

## 📌 TL;DR

**Tu rol**: Ingeniero/a de Firmware en el nuevo **equipo de Sistemas de Control** de
GreenField Technologies (startup ficticia de agro-tecnología).

**El contexto**: GreenField ya vende **SoilSense**, una red mesh de sensores de suelo
para fincas pequeñas, desarrollada antes de que te unieras. Pero monitorear no cierra
el lazo: los agricultores quieren que el riego se **automatice**. Tu equipo construye
la nueva línea de producto:

- **SoilSense Control** — controlador de riego en tiempo real (ESP32-S3 + Zephyr):
  lazo de control de flujo/presión con deadline **duro**, muestreo periódico,
  telemetría **suave**, consola **firme**.
- **SoilSense Hub** — gateway Linux con GUI local (pantalla táctil) y dashboard
  remoto, que supervisa los controladores. Es el proyecto final (semanas 13–16).

**Tus entregables**: ADRs y registros de diseño profesionales, más **evidencia de
tiempos**: análisis de planificabilidad y tablas de latencia/jitter medidas. "Funciona"
no basta — hay que demostrar *cuándo*.

**Tu mentor**: Ing. Samuel Cifuentes, que espera que entiendas el "por qué" — y que
muestres los números.

---

## 1. La Empresa

**GreenField Technologies** es una startup ficticia de agricultura de precisión para
fincas pequeñas y medianas (5–50 ha). Valores: asequibilidad, simplicidad,
sostenibilidad, resiliencia. Su primer producto, la red de sensores **SoilSense**,
ya está desplegado en fincas piloto y reporta humedad y temperatura del suelo.

**El problema nuevo**: los datos le dicen a la agricultora *cuándo* regar, pero ella
sigue abriendo válvulas a mano. Sobre-riega por precaución, o llega tarde. GreenField
decidió cerrar el lazo: sensado → decisión → **actuación**.

**Por qué esto es un problema de tiempo real**: una válvula que cierra tarde ante una
sobrepresión revienta una manguera; un lazo de control de flujo con jitter riega mal;
una parada de emergencia tiene un plazo, no una sugerencia. Los deadlines ahora son
físicos.

## 2. Los Productos

### SoilSense Control (módulos 1–4 del curso)
Controlador de riego basado en ESP32-S3 + Zephyr. Sus tareas encarnan la taxonomía
del curso:

| Tarea | Tipo | Ejemplo de requisito |
|-------|------|----------------------|
| Lazo de control de flujo/presión (PWM sobre válvula/bomba) | **Duro** | período 10 ms, deadline = período |
| Parada de emergencia por sobrepresión | **Duro** | respuesta < 5 ms |
| Muestreo de sensores | **Duro** | 1 kHz, jitter acotado |
| Telemetría hacia el Hub | **Suave** | atrasos degradan, no rompen |
| Consola de comandos | **Firme** | respuesta tardía no vale, pero no daña |

*(Los números son de referencia; se fijan y justifican en los ADRs de cada módulo.)*

### SoilSense Hub (proyecto final, semanas 13–16)
Gateway sobre SBC Linux (PREEMPT_RT), compartido por grupo. El Hub **no es solo un
supervisor**: es un sistema de criticidad mixta con requisitos duros propios, y su
diseño de tiempo real es el corazón del proyecto final. En la misma caja conviven:

- **Control duro local**: el lazo de presión de la estación de bombeo y su interlock
  de seguridad (`SCHED_FIFO`/`SCHED_DEADLINE`, aislamiento de CPU).
- **GUI local** (pantalla táctil — p. ej. LVGL o HMI web) para operación en campo.
- **Enrutamiento de datos**: telemetría de los nodos Control hacia el dashboard
  remoto/nube, y comandos de vuelta, con presupuesto de deadline extremo a extremo.

**El reto de diseño**: demostrar que el lazo duro cumple sus plazos *mientras* la GUI
renderiza y el enrutamiento recibe ráfagas de tráfico — con evidencia (`cyclictest` y
trazas bajo carga sintética). Además, el ADR de particionamiento: qué funciones viven
en Linux y cuáles en el MCU (ESP32-S3), y por qué.

**Requisito de seguridad (entregable explícito)**: el sistema declara su **estado
seguro** (falla ⇒ válvula cerrada) y lo protege con un **watchdog** — si el lazo de
control muere, el hardware llega solo al estado seguro. Es la respuesta de diseño a
la pregunta de Edwin ("¿qué pasa si el Hub se cae con una válvula abierta?").

## 3. Tu Rol y Equipo

- **Rol**: Ingeniero/a de Firmware, equipo de Sistemas de Control.
- **Módulos 1–4**: en parejas, un kit ESP32-S3 por pareja.
- **Módulos 5–6**: parejas se fusionan en grupos (4–6) compartiendo el SBC del Hub.
- **Mentor**: Ing. Samuel Cifuentes (Arquitecto Senior). Revisa ADRs y evidencia de
  tiempos. Frase de cabecera: *"muéstrame la traza"*.

### Stakeholders

| Stakeholder | Rol | Le importa | Pregunta típica |
|-------------|-----|-----------|-----------------|
| **Samuel** | Arquitecto Senior | Correctitud, análisis de planificabilidad | "¿Cuál es el peor caso, y cómo lo mediste?" |
| **Gustavo** | Product Owner | Costo, valor al cliente | "¿Por qué un kernel de tiempo real encarece el producto?" |
| **Edwin** | Operaciones de Campo | Confiabilidad, fallas | "¿Qué pasa si el Hub se cae mientras una válvula está abierta?" |
| **Edward** | Seguridad | Superficie de ataque | "¿Un comando remoto malicioso puede violar un deadline?" |
| **Daniela** | Clienta piloto | Usabilidad, ROI | "¿La pantalla me dice qué está pasando sin llamar a soporte?" |

## 4. Fases del Proyecto (mapeadas a módulos)

> **Borrador — detalle por fase pendiente de autoría.** Estructura prevista
> (contexto → tareas → preguntas de stakeholders → entregables):

1. **Fase 1 — Prototipo y línea base** (módulos 1–2 + tracing del módulo 4): el
   Control como superloop, medición de la línea base; reconstrucción con hilos;
   A/B contra la línea base con tracing instrumentado.
2. **Fase 2 — Garantías** (módulo 3): análisis de planificabilidad del task set del
   Control; inversión de prioridad reproducida y corregida. *(Workshop: semana 8.)*
3. **Fase 3 — Medición y drivers** (módulo 4): driver con binding de devicetree,
   WCET y multinúcleo (AMP particionado). La charla compara con FreeRTOS: ¿y si un
   cliente exige el kernel de la industria?
4. **Fase 4 — El Hub** (módulos 5–6): Linux RT en grupos; kickoff del proyecto final,
   dos checkpoints y demo day con reporte de evidencia de tiempos.

## 5. Estándares de Documentación

ADRs antes de implementar, decisiones justificadas con números, trade-offs
explícitos. Además, en este proyecto todo requisito temporal se declara (tipo
duro/firme/suave, período, deadline) y se **verifica con evidencia medida** (tabla de
latencia/jitter o traza) — todo vive en el **RET** (Reporte de Evidencia de Tiempos,
plantilla en [plantillas/ret.md](plantillas/ret.md)), el documento vivo del equipo.
