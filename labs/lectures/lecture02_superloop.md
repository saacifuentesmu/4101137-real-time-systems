# Week-2 talk — The vocabulary: taxonomy, task models, latency anatomy (40 min)

**Precedes:** `labs/lab02_superloop.md` · **Audience:** students right before the lab.

## Objectives
By the end, the student can: 1. classify a task as hard/firm/soft by the
*consequence of a miss*; 2. name each component of the interrupt→response chain and
where jitter comes from; 3. write a measurable timing requirement in EARS form with an ID.

## Structure
| Min | Segment | Purpose in one line |
|---|---|---|
| 0–5 | Hook: Samuel's memo | measure what we have before pitching a kernel |
| 5–15 | The taxonomy + task model | H/F/S by consequence; T_i, C_i, D_i, jitter |
| 15–25 | Latency anatomy | the interrupt→response chain, delay by delay |
| 25–35 | Requirements you can measure (EARS) | from "fast enough" to a testable sentence |
| 35–40 | Bridge to the lab | the baseline table and what numbers to expect |

## Segment 1 — Taxonomy + task model
- Key idea: the type is defined by what a miss *costs*: hard = damage (burst hose),
  firm = the late result is worthless but harmless (stale console reply), soft =
  degradation (laggy telemetry). Then the model: period T_i, computation C_i,
  deadline D_i, and jitter as the variation of any of them.
- **Board sketch:** one period's timeline — arrival, start, finish, deadline — and
  the three miss consequences under it.
- **Question for the room:** classify the node's five tasks (scenario table) before
  I show the answer.

> **Misconception to anticipate:** "jitter averages out." The control loop and the
> analyzer both disagree: the worst sample is the one that bursts the hose.

## Segment 2 — Latency anatomy
- Key idea: between the physical event and the response there's a chain — interrupt
  latency (hardware + masked sections) → ISR → hand-off (flag, in the superloop) →
  wait for the loop to come around → service. Each link adds delay; the *variable*
  links add jitter. In a superloop, the longest loop body bounds the hand-off wait.
- **Board sketch:** the chain with a brace over each delay and its cause; circle the
  "wait for the loop" link — today's villain.
- **Question for the room:** which link does the blocking command stretch?

## Segment 3 — Requirements you can measure (EARS)
- Key idea: "the valve must respond fast" cannot fail a test. EARS form: *when/while
  ⟨condition⟩, the system shall ⟨response⟩ within ⟨deadline⟩* — one sentence, one
  condition, one number. Give it an ID (`REQ-CTRL-01`) and every future measurement
  can cite it.
- **Board sketch:** a bad requirement rewritten live into EARS, the class supplying
  condition and number.
- **Question for the room:** write the e-stop requirement (they'll need it in Task D).

> **Misconception to anticipate:** "requirements are paperwork." Counter: in Task D
> they write 5–8 and from then on *every* piece of evidence cites one — that's what
> makes week 8's defense possible.

## What about FreeRTOS?
Two minutes: nothing in this talk is Zephyr's — taxonomy, task model, latency chain,
and EARS apply identically under FreeRTOS or bare metal. The vocabulary is the
transferable asset.

## Bridge to the lab
They run the provided superloop and fill the baseline table: expect ~µs-level jitter
on the cache-free M0+ — until the blocking command turns it into ms. That number is
the course baseline; everything after week 2 is measured against it.
