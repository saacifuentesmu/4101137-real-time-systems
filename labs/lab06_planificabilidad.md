# Semana 6 — Planificabilidad: la teoría, puesta a prueba
> **Lectura:** [LECTURAS.md](../LECTURAS.md), semana 6 (incluye el opcional de Lee & Seshia) · **Módulo:** 3
> **Taller 1 sale hoy** (ejercicios de caps. 2 y 4; se entrega en el workshop (semana 8)).

**De:** Ing. Samuel Cifuentes — *"Daniela pregunta si puede agregar dos sensores más
al nodo. Hoy ustedes responden como ingenieros: no 'probemos a ver', sino 'la
utilización queda en X, la prueba dice Y'. Y como no les creo a los teoremas más
que a ustedes, repro­dúzcanme el caso famoso: un task set que RM pierde y EDF
cumple — en nuestra placa, no en el libro."*

| Stakeholder | Su pregunta | Cómo la responde esta sesión |
|---|---|---|
| **Samuel** | ¿Cabe más carga en el nodo? | U calculada con `C_i` medidos + la prueba aplicable |
| **Daniela** | ¿Y si el riego llega tarde *un poquito*? | El lazo con jitter inducido: la degradación, medida |

## Lo que vas a medir

| Medición | Tu valor | Predicción |
|---|---|---|
| U del task set sintético (3 tareas) | ____ | diseñado a U ≈ 0.97 |
| Deadline miss bajo RM (¿cuál tarea, cuándo?) | ____ | la teoría dice: sí pierde (Fig. 4.13) |
| Deadline miss bajo EDF | ____ | la teoría dice: U ≤ 1 ⇒ cumple |
| Error del lazo de flujo con jitter inducido de 0 / 2 / 5 ms | ____ / ____ / ____ | crece con el jitter |

## Tareas

### Tarea A — Fig. 4.13 en vivo
- Implementa el task set de la Fig. 4.13 del libro (períodos y cómputos dados; el
  "cómputo" es busy-wait calibrado). Corre con prioridades RM; captura el miss.
- Cambia a EDF (`CONFIG_SCHED_DEADLINE=y`, misma prioridad estática,
  `k_thread_deadline_set` por período). Verifica que cumple.
- **Evidencia:** dos capturas del analizador — el miss bajo RM, el cumplimiento bajo EDF.

### Tarea B — ¿Cabe la carga nueva?
- Con los `C_i` medidos del nodo real: calcula U, aplica Liu & Layland y la prueba
  hiperbólica. Agrega las "dos tareas de Daniela" (parámetros en clase) y repite.
- **Evidencia:** el cálculo en el RET §4, con veredicto y qué prueba lo sostiene.

### Tarea C — Jitter vs. control (el puente con control)
- Inyecta jitter artificial en el lazo de flujo (retardo aleatorio 0–N ms antes de
  actuar). Para N = 0, 2, 5 ms: mide el error del lazo (desviación del caudal
  objetivo, o del setpoint del montaje del curso).
- **Evidencia:** tabla error-vs-jitter + una frase: ¿en qué N el lazo deja de ser útil?

## ¿Y en FreeRTOS?

FreeRTOS solo trae prioridades fijas — no hay EDF en el kernel. La Tarea A no se
puede reproducir tal cual: con U = 0.97 y FreeRTOS, la respuesta profesional es
re-diseñar el task set para que pase la prueba RM (o bajar U). Esa restricción es
real en la industria — y es la razón por la que el libro dedica medio capítulo a RM.

## Entregables (RET)

- **§4 Planificabilidad:** U, ambas pruebas, veredicto de la carga de Daniela.
- **§3 Evidencia semana 6:** capturas de Fig. 4.13 + tabla jitter-vs-control.

## Rúbrica (100 pts)

| | pts |
|---|---|
| **Ejecución** — task set 4.13 con miss bajo RM (15) · EDF cumpliendo (15) · jitter inyectado (10) | 40 |
| **Evidencia** — capturas de ambos regímenes (15) · tabla error-vs-jitter (15) | 30 |
| **Análisis** — U y pruebas bien aplicadas al caso Daniela (20) · lectura control-jitter (10) | 30 |
