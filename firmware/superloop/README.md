# firmware/superloop — the provided superloop

Reference Zephyr app that students **run, read, and measure** in week 2 — their
Zephyr *get started* — and that module 2 migrates, guided, to kernel threads.

> **Draft** — builds pending validation on course hardware (pin map assumptions
> flagged in each overlay).

One `main` loop + ISRs, no scheduler. The node's tasks and their instrumentation:

| Task | Type | Instrumentation pin (C0116-DK) |
|---|---|---|
| Sampling (1 kHz: pressure ADC, e-stop check, valve PWM phase) | Hard | `instr_samp` PA1 |
| Control (PI → valve duty, every 10th sample) | Hard | `instr_ctrl` PA4 |
| Console (UART commands) | Firm | `instr_cons` PA5 |
| Telemetry (CSV line, 1 Hz) | Soft | `instr_tele` PA6 |
| Flow batch math (every 100 pulses) | — | `instr_flow` PA7 |

Each pin goes high on task entry, low on exit — hook the analyzer there.

## Build and run

```bash
west build -p -b stm32c0116_dk firmware/superloop && west flash
west build -p -b native_sim firmware/superloop && ./build/zephyr/zephyr.exe
```

`native_sim` is for development only — no ADC/pins wired, the plant is synthetic
(pressure follows the valve command), and its timing is not real.

## Wiring (C0116-DK)

- **Joystick** (on-board, PA8/ADC): up = setpoint +10 mV · down (held) =
  **e-stop** · center = clear e-stop. Calibrate the bands with the `joy` command.
- **"Pressure" pot** (breadboard kit) → PA0 (wiper), 3V3, GND. Without it the
  synthetic plant takes over.
- **Flow pulse input** → PB7 (wire the YF-S401 signal, a button module, or a
  square wave; internal pull-down).
- **Valve** = user LED (`led0`), software-PWM'd at 50 Hz.
- Console on the ST-LINK VCP, 115200 8N1.

## Console commands

`help` · `status` · `joy` (raw mV, for calibrating the bands) · `set <mv>`
(setpoint) · `clear` (e-stop) · `calib` — the **blocking command**: a zero-flow
calibration that takes several hundred ms. Week 2's Task C triggers it while
capturing; explaining *what* it degrades and *why* is the lab.

## Week 3

`boards/esp32s3_devkitc_esp32s3_procpu.overlay` is the port: pins and ADC
channels move, the C does not.

```bash
west build -p -b esp32s3_devkitc/esp32s3/procpu firmware/superloop && west flash
```

Every piece here (ISR flags, polled work, batch bottom halves) has a named
counterpart in module 2's migration — that mapping is the week-3/4 talks.
