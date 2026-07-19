# Week-1 talk — Recap: why real-time (40 min)

**Precedes:** `labs/lab01_bringup.md` · **Audience:** students right before the lab.

## Objectives
By the end, the student can: 1. explain why a correct result at the wrong time is
a wrong result, citing a real failure; 2. describe the course contract (GreenField,
the RET, "show me the trace"); 3. verify their toolchain builds both starter targets.

## Structure
| Min | Segment | Purpose in one line |
|---|---|---|
| 0–5 | Hook: the Patriot clock | correct code, 28 dead — time was the bug |
| 5–15 | Recap → convergence | digital systems + computation structures + control meet at *when* |
| 15–25 | What real-time is (and isn't) | predictable ≠ fast; the tail is the verdict |
| 25–32 | The course contract | GreenField, the RET, evidence culture, grading |
| 32–37 | The toolchain map | why Zephyr; where FreeRTOS lives in this course |
| 37–40 | Bridge to the lab | today's deliverable is a working environment |

## Segment 1 — The Patriot clock (hook)
- Key idea: Dhahran 1991 — a 0.1 s tick accumulated 0.34 s of drift in 100 h;
  the intercept window moved 687 m; the software computed *correctly*. §1.2 also
  has the Shuttle STS-1 sync scrub. Time was the spec, not the optimization.
- **Board sketch:** timeline of the drift accumulating; the missed window.
- **Question for the room:** was this a performance bug? (No — it met its throughput.)

## Segment 2 — Recap → convergence
- Key idea: they already own the three pieces — logic + ISRs (digital systems),
  what the CPU does per cycle (computation structures), loops with deadlines
  implied by physics (control). This course adds the missing axis: *when* code runs,
  guaranteed.
- **Board sketch:** three arrows converging on "when?".

## Segment 3 — What real-time is (and isn't)
- Key idea: real-time = the worst case is bounded and proven. A fast average with a
  fat tail fails; a slow constant loop can pass.
- **Board sketch:** two latency distributions, same mean — one long tail crossing
  the deadline line.
- **Question for the room:** which one ships in a ventilator?

> **Misconception to anticipate:** "real-time means fast." Dismantle with the sketch:
> the deadline line doesn't care about the mean.

## Segment 4 — The course contract
- Key idea: they join GreenField as firmware engineers; every claim needs a number
  (the RET is the living deliverable); Samuel's house rule: *"show me the trace"*.
  Grading: weekly labs, workshop (wk 8), final project (wks 13–16).

## Segment 5 — The toolchain map
- Key idea: one toolchain for the whole course (Zephyr: `west`, devicetree) across
  both boards and `native_sim`; FreeRTOS appears every week as the industry
  comparison — nothing to install, everything to compare.

## Bridge to the lab
No timing today: the measured thing is the *setup* (blinky per member, serial cycle,
team RET created). If the environment works, the semester's iteration loop is < 1 min.
