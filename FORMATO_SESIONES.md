# Session format

Format inherited from 4201327 (where it worked), adapted and compacted. Each
session has up to three documents, each with a distinct job:

| Doc | Audience | Content | Budget |
|---|---|---|---|
| **lab.md** | Students | Mission (GreenField memo) → what gets measured → tasks with evidence → RET deliverables → rubric | ≤ ~1,500 words |
| **lecture.md** | Instructor (script for the 40 min) | Objectives, timing table, board sketches, misconceptions to anticipate, bridge to the lab | a script, not prose |
| **sop.md** | Students (mechanics) | Commands, wiring, checks, and troubleshooting only — the *why* lives in the lab | **only if the session needs it** (heavy bring-ups: Linux SBC, AMP/sysbuild, tracing) |

Compactness rules (mandatory): one explanation per concept; tables and diagrams
over prose; questions without the answer included; advanced math in `<details>`;
no "TL;DR + In plain English + technical" sections repeating each other.

Fixed lab.md sections:

1. **Memo** from the stakeholder (opens the session; it is also the objective).
2. **What you'll measure** — the evidence table with `____` cells the lab fills in.
3. **Tasks** A/B/C, each with its **Evidence:** line.
4. **What about FreeRTOS?** — 3–5 lines: how it would be done with that API and when that option wins.
5. **Deliverables (RET)** — which RET sections get updated today.
6. **Rubric** (table, 100 pts).

The course's living deliverable is the **RET — Timing Evidence Report**
(template in [plantillas/ret.md](plantillas/ret.md)): the lightweight equivalent
of 4201327's DDR. Updated every week, handed in at the workshop (week 8) and at
the close.

Templates: [plantillas/lab.md](plantillas/lab.md) ·
[plantillas/lecture.md](plantillas/lecture.md) ·
[plantillas/sop.md](plantillas/sop.md) · [plantillas/ret.md](plantillas/ret.md)
