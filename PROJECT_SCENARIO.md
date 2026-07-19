# GreenField Technologies: Project Briefing

**Document type**: Project context and stakeholder guide

**Audience**: Firmware Engineers — Control Systems team (students)

---

## 📌 TL;DR

**Your role**: Firmware Engineer on GreenField Technologies' new **Control
Systems team** (a fictional agri-tech startup).

**The context**: GreenField already sells **SoilSense**, a soil-sensor mesh
network for small farms, built before you joined. But monitoring doesn't close
the loop: farmers want irrigation to be **automated**. Your team builds the new
product line:

- **SoilSense Control** — real-time irrigation controller (ESP32-S3 + Zephyr):
  flow/pressure control loop with a **hard** deadline, periodic sampling,
  **soft** telemetry, **firm** console.
- **SoilSense Hub** — Linux gateway with a local GUI (touchscreen) and a remote
  dashboard, supervising the controllers. It's the final project (weeks 13–16).

**Your deliverables**: professional ADRs and design records, plus **timing
evidence**: schedulability analysis and measured latency/jitter tables. "It
works" isn't enough — you have to show *when*.

**Your mentor**: Eng. Samuel Cifuentes, who expects you to understand the
"why" — and to show the numbers.

---

## 1. The Company

**GreenField Technologies** is a fictional precision-agriculture startup for
small and mid-size farms (5–50 ha). Values: affordability, simplicity,
sustainability, resilience. Its first product, the **SoilSense** sensor network,
is already deployed on pilot farms reporting soil moisture and temperature.

**The new problem**: the data tells the farmer *when* to irrigate, but she still
opens valves by hand. She over-irrigates to be safe, or arrives late. GreenField
decided to close the loop: sensing → decision → **actuation**.

**Why this is a real-time problem**: a valve that closes late during an
overpressure bursts a hose; a flow control loop with jitter irrigates poorly; an
emergency stop has a deadline, not a suggestion. The deadlines are now physical.

## 2. The Products

### SoilSense Control (course modules 1–4)
ESP32-S3 + Zephyr irrigation controller. Its tasks embody the course taxonomy:

| Task | Type | Example requirement |
|------|------|---------------------|
| Flow/pressure control loop (PWM to valve/pump) | **Hard** | period 10 ms, deadline = period |
| Overpressure emergency stop | **Hard** | response < 5 ms |
| Sensor sampling | **Hard** | 1 kHz, bounded jitter |
| Telemetry to the Hub | **Soft** | delays degrade, don't break |
| Command console | **Firm** | a late response is worthless, but harmless |

*(Numbers are references; they're fixed and justified in each module's ADRs.)*

### SoilSense Hub (final project, weeks 13–16)
Gateway on a Linux SBC (PREEMPT_RT), shared per group. The Hub is **not just a
supervisor**: it's a mixed-criticality system with hard requirements of its own,
and its real-time design is the heart of the final project. In the same box coexist:

- **Local hard control**: the pump station's pressure loop and its safety
  interlock (`SCHED_FIFO`/`SCHED_DEADLINE`, CPU isolation).
- **Local GUI** (touchscreen — e.g. LVGL or a web HMI) for field operation.
- **Data routing**: telemetry from the Control nodes to the remote
  dashboard/cloud, and commands back, with an end-to-end deadline budget.

**The design challenge**: prove the hard loop meets its deadlines *while* the GUI
renders and the routing takes traffic bursts — with evidence (`cyclictest` and
traces under synthetic load). Plus the partitioning ADR: which functions live in
Linux and which on the MCU (ESP32-S3), and why.

**Safety requirement (explicit deliverable)**: the system declares its **safe
state** (failure ⇒ valve closed) and protects it with a **watchdog** — if the
control loop dies, the hardware reaches the safe state on its own. It's the
design answer to Edwin's question ("what if the Hub goes down with a valve open?").

## 3. Your Role and Team

- **Role**: Firmware Engineer, Control Systems team.
- **Modules 1–4**: in pairs, one ESP32-S3 kit per pair.
- **Modules 5–6**: pairs merge into groups (4–6) sharing the Hub's SBC.
- **Mentor**: Eng. Samuel Cifuentes (Senior Architect). Reviews ADRs and timing
  evidence. Signature phrase: *"show me the trace"*.

### Stakeholders

| Stakeholder | Role | Cares about | Typical question |
|-------------|------|-------------|------------------|
| **Samuel** | Senior Architect | Correctness, schedulability analysis | "What's the worst case, and how did you measure it?" |
| **Gustavo** | Product Owner | Cost, customer value | "Why does a real-time kernel make the product more expensive?" |
| **Edwin** | Field Operations | Reliability, failures | "What happens if the Hub goes down while a valve is open?" |
| **Edward** | Security | Attack surface | "Can a malicious remote command violate a deadline?" |
| **Daniela** | Pilot customer | Usability, ROI | "Does the screen tell me what's going on without calling support?" |

## 4. Project Phases (mapped to modules)

> **Draft — per-phase detail pending authoring.** Planned structure
> (context → tasks → stakeholder questions → deliverables):

1. **Phase 1 — Prototype and baseline** (modules 1–2 + module 4's tracing): the
   Control node as a superloop, baseline measurement; rebuild with threads;
   A/B against the baseline with instrumented tracing.
2. **Phase 2 — Guarantees** (module 3): schedulability analysis of the Control
   task set; priority inversion reproduced and fixed. *(Workshop: week 8.)*
3. **Phase 3 — Measurement and drivers** (module 4): driver with a devicetree
   binding, WCET, and multicore (partitioned AMP). The talk compares with
   FreeRTOS: what if a customer demands the industry's kernel?
4. **Phase 4 — The Hub** (modules 5–6): RT Linux in groups; final-project
   kickoff, two checkpoints, and demo day with a timing-evidence report.

## 5. Documentation Standards

ADRs before implementing, decisions justified with numbers, explicit trade-offs.
Additionally, in this project every timing requirement is declared with an ID
(`REQ-…`, one EARS-style sentence: condition → response → deadline; hard/firm/soft
type, period, deadline) and **verified with measured evidence** (latency/jitter
table or trace) — all of it lives in the **RET** (Timing Evidence Report, template
in [plantillas/ret.md](plantillas/ret.md)), the team's living document.
