# Week-3 talk — The scheduler: threads, priorities, preemption (40 min)

**Precedes:** `labs/lab03_port.md` · **Audience:** students right before the lab.

## Objectives
By the end, the student can: 1. explain what a devicetree overlay buys in a port;
2. describe the RT-kernel anatomy (thread states, ready queue, context switch);
3. map the superloop's polled sampling to a thread + message queue.

## Structure
| Min | Segment | Purpose in one line |
|---|---|---|
| 0–5 | Hook: two pieces of news | production picked the S3; the kernel evaluation is authorized |
| 5–15 | The port: hardware as data | devicetree/overlay — why the C doesn't change |
| 15–27 | Anatomy of an RT kernel | states, ready queue, preemption, switch cost (§10.1–10.3) |
| 27–33 | The first mapping | polled sampling → thread + `k_msgq` |
| 33–37 | What about FreeRTOS? | same scheduler model, no devicetree |
| 37–40 | Bridge to the lab | the diff-stat and the new jitter |

## Segment 1 — The port: hardware as data
- Key idea: the application names hardware by role (`aliases`, bindings), not by
  pin; the board's devicetree resolves the role. Changing silicon = changing the
  description, not the C. Today's port is the proof: an overlay moving the
  instrumentation GPIOs, zero application lines.
- **Board sketch:** same `main.c` box with two DT files feeding it — C0116-DK pins
  vs. S3 pins.
- **Question for the room:** what would this port cost in week 1's toolchain map
  without devicetree? (SDK change — they'll verify in the FreeRTOS segment.)

## Segment 2 — Anatomy of an RT kernel
- Key idea: threads have states (ready/running/blocked); the scheduler always runs
  the highest-priority *ready* thread; preemption means "immediately, not at the
  next loop iteration". The context switch has a measurable cost — they'll measure
  it in week 4, and it's the price of a bounded hand-off wait.
- **Board sketch:** the state diagram, then the superloop's "wait for the loop to
  come around" link (wk 2) replaced by "preempt: bounded by switch cost".
- **Question for the room:** what should the blocking command do to a *higher-priority*
  sampling thread? (Nothing — that's this afternoon's measurement.)

> **Misconception to anticipate:** "the kernel adds overhead, so it's slower."
> Slower on average by µs of switching — but the *worst case* stops depending on
> the longest loop body. The A/B in week 4 shows both effects.

## Segment 3 — The first mapping
- Key idea: migration is mechanical, one piece at a time. Today only sampling:
  `K_THREAD_DEFINE` at preemptive priority, ISR posts to a `k_msgq`, the loop
  consumes. The rest stays superloop — mixed systems are normal mid-migration.
- **Board sketch:** first row of the mapping table (the full table is week 4's talk).

## What about FreeRTOS?
`xTaskCreate` ↔ `K_THREAD_DEFINE`, `xQueueSend` ↔ `k_msgq_put` — same preemptive
fixed-priority model, near-1:1 API. What has no equivalent is Segment 1: moving
STM32 → ESP32 under FreeRTOS means changing vendor SDKs, not a 20-line overlay.

## Bridge to the lab
Two numbers to predict: the port's `git diff --stat` (expect ~0 lines of C) and the
S3's baseline jitter (expect *worse* than the M0+ — external flash + cache; write
down why before measuring).
