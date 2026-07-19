# firmware/superloop — the provided superloop

**Status: pending authoring (Sam).** Reference Zephyr app that students **run,
read, and measure** in week 2 — their Zephyr *get started* — and that module 2
migrates, guided, to kernel threads.

Spec (from the [scenario](../../PROJECT_SCENARIO.md)):

- A single `main` thread + ISRs — no scheduler. The 4100901 architecture, in Zephyr.
- Node tasks: periodic sampling (hard), control loop → PWM, UART console (firm),
  console telemetry (soft).
- **GPIO instrumentation** on every task (toggle on entry/exit) to measure latency
  and jitter with the logic analyzer — the week-2 lab lives off this.
- A "blocking command" in the console that degrades jitter on purpose — the living
  argument for module 2.

Targets: `stm32c0116_dk` (primary, weeks 1–2) and `esp32s3_devkitc` via overlay
(week 3 — the port is part of the lesson). `native_sim` builds for development;
it is not valid for timing measurements.

Every piece (ISR flags, polled work, bottom halves) must have a named counterpart
in module 2's migration — the superloop → kernel mapping is the content of the
week-3 talk.
