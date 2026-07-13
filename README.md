# Real-Time Systems — UNAL 4101137

A course about **real-time behavior** — scheduling, latency, jitter, deadlines — using
an **ESP32-S3** and **ESP-IDF (FreeRTOS)** as the vehicle. Taught at the Universidad
Nacional de Colombia, Sede Manizales. The goal isn't the framework — it's understanding
*when* code runs and how to guarantee it: why a superloop misses deadlines, how a
preemptive scheduler fixes it, and what the theory (RMS/EDF, priority inversion, WCET)
predicts about both.

This is the course hub: the material lives across the repositories below, ordered the
way the semester runs.

The through-line is one system — a **real-time acquisition & control node** (periodic
sampling, a control loop with a hard deadline, telemetry, and a command console) —
built three times:

1. first as a **bare-metal superloop** (in simulation — no hardware required), to
   measure its jitter and watch it miss deadlines;
2. then **rebuilt on FreeRTOS via ESP-IDF** on the ESP32-S3, with tasks, queues, and
   ISR deferral — measured again;
3. then **translated to Zephyr**, to see the same real-time concepts under a different
   kernel (devicetree, Kconfig, priority-inheritance mutexes) and learn portability.

Course material is in Spanish; repo names and this overview are in English.

## Course path

| # | Module | Repository | What it covers |
|---|--------|-----------|----------------|
| 0 | Setup — dev env & first blink | `4101137-0-intro-project` *(planned)* | ESP-IDF toolchain on the ESP32-S3: `idf.py`, first build/flash/monitor. Wokwi browser simulation as the no-hardware fallback |
| 1 | Bare-metal showcase | [4101137-1-bare-metal-showcase](../4101137-1-bare-metal-showcase) | The superloop node in a Cortex-M simulator: foreground/background, blocking, measured latency and jitter — why an RTOS. No hardware required |
| 2 | FreeRTOS fundamentals | `4101137-2-freertos-fundamentals` *(planned)* | The same node on ESP-IDF: tasks, queues, semaphores, ISR deferral, priorities — jitter measured again and compared |
| 3 | Midterm — scheduling & timing | `4101137-3-midterm-scheduling` *(planned)* | RMS/EDF schedulability, priority inversion reproduced and traced, WCET estimation |
| 4 | Zephyr translation | `4101137-4-zephyr-translation` *(planned)* | Port one lab to Zephyr on the same ESP32-S3: west, devicetree, Kconfig, kernel API mapping |
| 5 | Lab — instrumented measurement | `4101137-5-tracing-lab` *(planned)* | Latency/jitter/CPU-load measurement with trace tooling; memory/time trade-offs |
| 6 | Final project | `4101137-6-final-project` *(planned)* | Networked real-time node: Wi-Fi telemetry + command console with deadline guarantees. Optional audio-pipeline track (ESP-ADF, I2S hard deadlines) |

## Hardware & tooling

ESP32-S3 devkit · ESP-IDF (`idf.py`, CMake) · VS Code · Wokwi / Renode / QEMU for
no-hardware paths · Zephyr (west) for the translation module · trace tooling for
latency and jitter measurement. Modules 0–1 require no hardware.

## Reference

**Giorgio Buttazzo — *Hard Real-Time Computing Systems: Predictable Scheduling
Algorithms and Applications*, 4th ed., Springer, 2024**
([link.springer.com/book/10.1007/978-3-031-45410-3](https://link.springer.com/book/10.1007/978-3-031-45410-3)).
The course's theory modules (schedulability, RMS/EDF, response-time analysis,
resource-access protocols) follow this text; the labs validate its predictions by
measurement. Likely available to students at no cost through UNAL's SpringerLink
subscription (SINAB). For practice, the primary references are the official ESP-IDF
and Zephyr documentation.

## What it demonstrates

Real-time engineering taught through a single product measured at every stage — the
same node as a superloop, on FreeRTOS, and on Zephyr, with the scheduling theory tied
to observed latency and jitter rather than slides. The ESP32-S3 is the teaching
instrument; the lasting takeaway is knowing *when* your code runs.

---

Maintained by Sam C · Universidad Nacional de Colombia, Sede Manizales.
