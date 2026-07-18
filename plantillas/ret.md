# RET — Reporte de Evidencia de Tiempos

**Equipo:** <nombres> · **Placas:** <seriales/apodos> · Documento **vivo**: se
actualiza cada semana; se entrega en el workshop (semana 8) y al cierre (semana 16).
Regla de la casa: *"muéstrame la traza"* — toda afirmación temporal cita una medición.

## 1. El sistema y su task set

Requisitos primero — una frase cada uno, estilo EARS (*cuando/mientras
<condición>, el sistema <respuesta> en <plazo>*) — y luego la tarea que
los implementa:

| ID | Requisito |
|---|---|
| REQ-CTRL-01 | Mientras el sistema riega, el lazo de control ejecutará cada 10 ms (deadline = período). |

| Tarea | Req. | Tipo (D/F/S) | Período | Deadline | C_i medido | Cómo se midió |
|---|---|---|---|---|---|---|
| Lazo de control | REQ-CTRL-01 | Duro | 10 ms | = T | ____ | <GPIO + analizador / traza> |

## 2. ADRs

### ADR-001 — <título>
**Contexto:** … · **Decisión:** … · **Justificación (con números):** … · **Estado:** …

## 3. Evidencia por semana

Cada entrada cita el/los `REQ` que verifica.

### Semana 2 — línea base superloop (C0116-DK)
<tabla de jitter/latencia + una frase de lectura>

### Semana 3 — línea base S3 y comparación de silicio
…

## 4. Análisis de planificabilidad

U = ΣC_i/T_i con los C_i **medidos**; prueba usada (RM / hiperbólica / EDF); RTA
como script con su salida; bloqueo B_i si hay mutexes. (Fórmulas: LECTURAS.md,
"La matemática que sí se usa".)

## 5. Seguridad funcional (proyecto final)

Estado seguro declarado (falla ⇒ válvula cerrada), watchdog, y la evidencia del
fail-safe disparándose.
