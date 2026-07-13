# Real-Time Systems — UNAL 4101137

A course about **real-time behavior** — scheduling, latency, jitter, deadlines — using
an **ESP32-S3** and **Zephyr RTOS** as the vehicle. Taught at the Universidad Nacional
de Colombia, Sede Manizales. The goal isn't the framework — it's understanding *when*
code runs and how to guarantee it: what the theory (RMS/EDF, response-time analysis,
priority inversion, WCET) predicts, verified by measurement at every stage.

Zephyr is the shared platform strategy across the embedded curriculum (4100901,
4201327, 4101137): one toolchain (`west`, CMake, Kconfig) and **devicetree** as the
hardware-description language — the same syntax students later meet again in the
Linux kernel. Its portability also gives every lab a no-hardware path (`native_sim`,
Renode).

This is the course hub: the material lives across the repositories below, ordered the
way the semester runs.

## Project scenario — GreenField Technologies

The course is **project-oriented**: students work inside a realistic product scenario
rather than doing isolated assignments (see
[PROJECT_SCENARIO.md](PROJECT_SCENARIO.md)). They join **GreenField Technologies** —
a fictional agri-tech startup — as **Firmware Engineers on the new Control Systems
team**. GreenField's sensing product (SoilSense, a soil-monitoring mesh) already
shipped; monitoring alone doesn't close the loop, so the next product line is
automated irrigation:

- **SoilSense Control** — an ESP32-S3 real-time irrigation controller: a flow/pressure
  control loop with a **hard** deadline, periodic sensor sampling, **soft** telemetry,
  and a **firm** command console. This is the node the course builds and rebuilds.
- **SoilSense Hub** — a Linux SBC gateway with **hard real-time duties of its own**:
  it runs the pump station's control loop and safety interlock *while also* serving a
  local touchscreen **GUI** and routing telemetry between Control nodes and the cloud.
  A mixed-criticality box — the final project (weeks 13–16) is proving the hard loop
  survives the GUI and routing load.

The briefing is self-contained. Deliverables are professional engineering documents:
ADRs and design records, extended here with **timing evidence** (schedulability
analysis + measured latency/jitter tables). *(Instructor note: GreenField is the same
fictional universe used in 4201327; students who took it will recognize the company,
but nothing depends on it.)*

## Through-line

The one system — **SoilSense Control** — is rebuilt as the course climbs the stack:

1. first as a **superloop** — single Zephyr main thread plus ISRs, the 4100901
   architecture revisited — with its latency and jitter measured as the baseline;
2. then **multithreaded on the Zephyr kernel** — threads, message queues, workqueues,
   priorities — measured again against that baseline;
3. then **translated to ESP-IDF/FreeRTOS**, the industry-dominant kernel, to see the
   same concepts under a different API and learn portability;
4. finally **one level up on embedded Linux** (PREEMPT_RT, `SCHED_DEADLINE`), closing
   with the **SoilSense Hub**: a mixed-criticality gateway whose hard control loop
   must coexist with a GUI and data routing on the same box — where real-time
   *design* (priority/deadline assignment, CPU isolation, Linux-vs-MCU partitioning)
   is the deliverable, not just working code.

The node's tasks embody the deadline taxonomy the course teaches — labeled in the
spec and verified in the traces. Course material is in Spanish; repo names and this
overview are in English.

## Course path

| # | Module | Repository | What it covers |
|---|--------|-----------|----------------|
| 0 | Setup — dev env & first blink | `4101137-0-intro-project` *(planned)* | Zephyr toolchain: `west`, devicetree at a glance, first build/flash on the ESP32-S3; `native_sim` and Renode as no-hardware fallbacks |
| 1 | Superloop baseline | [4101137-1-superloop-baseline](../4101137-1-superloop-baseline) | Real-time taxonomy (hard/firm/soft) and latency anatomy; the node as a superloop (main thread + ISRs — 4100901 remembered), its jitter measured as the course baseline |
| 2 | Zephyr kernel fundamentals | `4101137-2-zephyr-fundamentals` *(planned)* | The same node multithreaded: threads, message queues, workqueues, ISR deferral, a first devicetree overlay — jitter measured against the module 1 baseline |
| 3 | Midterm — scheduling & timing | `4101137-3-midterm-scheduling` *(planned)* | RMS/EDF schedulability, response-time analysis, WCET estimation; priority inversion reproduced and fixed live (Zephyr mutexes do priority inheritance) |
| 4 | Translation — ESP-IDF/FreeRTOS | `4101137-4-freertos-translation` *(planned)* | Port one lab to ESP-IDF on the same ESP32-S3: FreeRTOS tasks/queues/semaphores, kernel API mapping — the RTOS students will most likely meet in industry |
| 5 | Lab — instrumented measurement | `4101137-5-tracing-lab` *(planned)* | Zephyr tracing subsystem (SystemView/CTF), latency/jitter/CPU-load measurement; a proper Zephyr driver with its devicetree binding. Multicore scheduling on the S3's two cores (Zephyr SMP) |
| 6 | Embedded Linux real-time | `4101137-6-linux-rt` *(planned)* | The same concepts on a PREEMPT_RT Linux SBC: `cyclictest` latency, `SCHED_FIFO`/`SCHED_DEADLINE` (RMS/EDF in a mainline kernel — Buttazzo's Linux chapter); students arrive already reading devicetree. Done in larger groups sharing boards |
| 7 | Final project — SoilSense Hub | `4101137-7-final-project` *(planned)* | The GreenField gateway as a mixed-criticality system: a hard control loop (pump station + safety interlock) sharing a PREEMPT_RT Linux SBC with a local GUI (e.g. LVGL/touchscreen or web HMI) and Control-node/cloud data routing. Deliverables: the Linux-vs-MCU partitioning ADR, priority/deadline/CPU-isolation design, and interference evidence showing the hard loop holds under GUI + routing load |

## Semester schedule

16 weekly sessions (Wednesdays, 4–7 pm). Each session runs as a **40-minute talk +
2-hour lab**, with the remaining time for wrap-up and Q&A. Content closes at week 12;
weeks 13–16 belong to the final project.

| Week | Module | Talk (40 min) | Lab (2 h) |
|------|--------|---------------|-----------|
| 1 | 0 | Course overview; why real-time; the curriculum's Zephyr strategy | `west` install, first build; blink on ESP32-S3 and `native_sim` |
| 2 | 0 | Toolchain anatomy: devicetree at a glance, Kconfig, build → flash → monitor | First DT overlay; debug and serial console on the S3 |
| 3 | 1 | RT taxonomy (hard/firm/soft), task models; 4100901's superloop remembered | Build the node as a Zephyr superloop (main thread + ISRs) |
| 4 | 1 | Latency anatomy: interrupt → activation → jitter; measurement methods | Baseline experiments: jitter growth, the blocking command, baseline table |
| 5 | 2 | The scheduler: threads, priorities, preemption | Rebuild the node with threads; sampling task meets its deadline |
| 6 | 2 | IPC: message queues, workqueues, ISR deferral | Complete the threaded node; A/B measurement against week 4 baseline |
| 7 | 3 | Schedulability: utilization bounds, RM/DM, EDF | Implement and analyze a periodic task set; verify the math in traces |
| 8 | 3 | Response-time analysis; priority inversion, PI/PC protocols | **Midterm workshop**: reproduce inversion, fix with PI mutex, quiz |
| 9 | 4 | FreeRTOS/ESP-IDF: the industry kernel, API mapping from Zephyr | Port one lab to ESP-IDF on the same S3; compare |
| 10 | 5 | Tracing and WCET measurement; multicore scheduling (S3 SMP) | Zephyr tracing (SystemView/CTF); driver with DT binding |
| 11 | 6 | Aperiodic servers, CBS → `SCHED_DEADLINE`; PREEMPT_RT | Linux SBC bring-up (shared per group); `cyclictest` latency |
| 12 | 6 | Linux RT in practice: `SCHED_FIFO`/`SCHED_DEADLINE`, affinity | Periodic tasks under Linux; content closes |
| 13 | 7 | SoilSense Hub kickoff: mixed criticality, Linux-vs-MCU partitioning | Proposal + architecture ADRs: what runs where, priorities/deadlines, CPU isolation plan |
| 14 | 7 | — | Checkpoint 1: Hub's hard control loop meets deadlines under synthetic load |
| 15 | 7 | — | Checkpoint 2: GUI + data routing integrated; interference evidence + end-to-end deadline budget |
| 16 | 7 | — | **Demo day**: live demos + timing-evidence reports |

## Hardware & tooling

ESP32-S3 devkit · Zephyr (`west`, CMake, devicetree, Kconfig) · VS Code ·
`native_sim` / Renode for no-hardware paths · ESP-IDF for the translation module ·
Zephyr tracing (SystemView/CTF) · a PREEMPT_RT Linux SBC (e.g. Raspberry Pi) for
modules 6–7, shared per group.

## Reference

**Giorgio Buttazzo — *Hard Real-Time Computing Systems: Predictable Scheduling
Algorithms and Applications*, 4th ed., Springer, 2024**
([link.springer.com/book/10.1007/978-3-031-45410-3](https://link.springer.com/book/10.1007/978-3-031-45410-3)).
The course's theory modules (schedulability, RMS/EDF, response-time analysis,
resource-access protocols, aperiodic servers/CBS) follow this text — it covers soft
real-time as well as hard, and its Linux chapters anchor module 6 and the final
project; the labs validate its predictions by measurement. Likely available to
students at no cost through UNAL's SpringerLink subscription (SINAB). For practice,
the primary references are the official Zephyr and ESP-IDF documentation.

**Edition note:** the 3rd edition (2011) is acceptable for the theory modules — its
chapters 1–9 match the 4th almost one-to-one. It is **not** sufficient for weeks
11–16: the 4th edition's ch. 12 (*Implementing Periodic Tasks in Linux*) is new, and
its ch. 13 covers `PREEMPT_RT` and `SCHED_DEADLINE`, which post-date the 3rd
edition's Linux coverage (the 3rd's final chapter is the RTLinux/RTAI/Xenomai era).

## What it demonstrates

Real-time engineering taught through a single product measured at every stage — the
same node as a superloop, multithreaded on Zephyr, translated to FreeRTOS, and scaled
to Linux — with the scheduling theory tied to observed latency and jitter rather than
slides. The ESP32-S3 is the teaching instrument; the lasting takeaway is knowing
*when* your code runs.

---

Maintained by Sam C · Universidad Nacional de Colombia, Sede Manizales.
