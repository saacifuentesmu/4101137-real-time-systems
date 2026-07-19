# Week 2 — The provided superloop: run, read, measure
> **Reading:** [LECTURAS.md](../LECTURAS.md), week 2 · **Module:** 1
> **Firmware:** [firmware/superloop/](../firmware/superloop/) (provided — no code is written today)

**From:** Eng. Samuel Cifuentes — *"Before you pitch me a kernel, measure what we
already have. I'm handing you the Control node as a superloop — the 4100901
architecture, the one this company knows how to maintain. I want the baseline:
latency and jitter for every task, with numbers, not adjectives. If the superloop
is enough, we keep it."*

The firmware already ships with **GPIO instrumentation** (a toggle on entry/exit of
each task): your instrument is the logic analyzer.

| Stakeholder | Their question | How this session answers it |
|---|---|---|
| **Samuel** | Does the superloop meet the scenario's task set? | Per-task jitter table vs. its deadlines |
| **Gustavo** | Why would we pay for a kernel's complexity? | The blocking command: the degradation, measured |

## What you'll measure

| Measurement (C0116-DK, cache-free silicon) | Your value | Reference |
|---|---|---|
| Actual sampling period (nominal 1 kHz): average | ____ µs | 1000 µs |
| Sampling jitter: max over ≥ 30 s | ____ µs | write it down: it's *the course baseline* |
| ISR → loop-service latency (button/flow) | ____ µs | |
| Sampling jitter **with the blocking command active** | ____ µs | compare against row 2 |

## Tasks

### Task A — Run and read
- Build and flash `firmware/superloop/` for `stm32c0116_dk`; verify the console.
- Read `main.c` with your partner: identify the ISR flags, the polled work, and
  where each instrumentation GPIO toggles. Draw the flow in ≤ 10 boxes.
- **Evidence:** the diagram (a photo of paper is fine) with the instrumentation GPIOs marked.

### Task B — The baseline
- Hook the logic analyzer to the instrumentation GPIOs; capture ≥ 30 s.
- Fill in the first three rows of the table. Use the pulse statistics in the
  analyzer software (period/width min–max).
- **Evidence:** analyzer screenshots + filled table in the RET.

### Task C — Break it on purpose
- Trigger the console's **blocking command** while capturing.
- Fill in row 4. Which task suffers, and why? Explain in 2–3 sentences pointing at
  the responsible line of code.
- **Evidence:** before/after capture + the explanation in the RET.

### Task D — The requirements, in writing
- From the task table in the [scenario](../PROJECT_SCENARIO.md), extract **5–8
  timing requirements** and write each as one **EARS-style** sentence
  (*when/while <condition>, the system shall <response> within <deadline>*), with an ID:

| ID | Requirement |
|---|---|
| REQ-CTRL-01 | While the system is irrigating, the control loop shall run every 10 ms (deadline = period). |
| REQ-CTRL-02 | When pressure exceeds the threshold, the system shall close the valve within 5 ms. |

- They go in **RET §1**, and from today on every piece of evidence cites the REQ it
  verifies (e.g. "row 2 of the table verifies REQ-CTRL-03"). In week 8 you'll learn
  what industry calls this discipline.
- **Evidence:** the requirements table in RET §1.

## What about FreeRTOS?

Same as in Zephyr: many FreeRTOS products *also* start as superloop + ISRs, and
migrate to the kernel when exactly what you saw in Task C shows up — one task
blocking the rest. Next week's question is the same in both worlds: what does a
preemptive scheduler buy you?

## Deliverables (RET)

- **§1 Task set:** the requirements table (Task D) + first column of measured
  `C_i` (each task's pulse width).
- **§3 Week-2 evidence:** the table above, filled in, with a one-sentence reading.
- **§2 (not yet):** the superloop-vs-kernel decision is made in week 4, with the A/B.

## Rubric (100 pts)

| | pts |
|---|---|
| **Execution** — firmware running (10) · correct flow diagram (15) · blocking command reproduced (15) | 40 |
| **Evidence** — complete table with captures (20) · measurement conditions noted (duration, load) (10) | 30 |
| **Analysis** — root-cause explanation of the degradation, with the line of code (15) · baseline reading in one sentence (5) · well-formed EARS requirements, with verifiable condition and deadline (10) | 30 |
