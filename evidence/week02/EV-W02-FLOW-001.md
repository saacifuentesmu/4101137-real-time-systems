# EV-W02-FLOW-001 — Superloop flow and instrumentation map

## Identification

| Field | Value |
|---|---|
| Date | 2026-09-26 |
| Operator | Juan Pablo Vargas Cordoba |
| Objective | Explain the execution paths of the supplied superloop before timing measurements |
| Platform | NUCLEO-G474RE (`nucleo_g474re/stm32g474xx`) |
| Firmware | `firmware/superloop/`, Week 2 worktree based on `0bb975b` |
| Linked requirements | REQ-CTRL-01, REQ-CTRL-03, REQ-CTRL-06 |
| Verdict | PASS — architecture read and instrumentation map completed |

## Artifact

- [Flow diagram](EV-W02-FLOW-001.svg) — editable source.
- [Flow diagram PNG](EV-W02-FLOW-001.png) — rendered view.

## Reading

The 1 kHz timer ISR only increments `ticks_pending`; it never samples. The main
`while (1)` loop runs console, display, telemetry, at most one pending sampling
job, every tenth control job, and flow-batch work. A flow edge ISR only increments
`flow_pulses`; `task_flow_batch()` performs the expensive work after 100 pulses.

Instrumentation mapping on this board is D3/PB3 sampling, D4/PB5 control,
D5/PB4 console, D6/PB10 telemetry, D7/PA8 flow batch, D8/PA9 display, and
D9/PC7 flow input. The diagram identifies these paths and the execution contexts.
