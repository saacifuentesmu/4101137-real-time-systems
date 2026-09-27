# EV-W02-BLOCK-005 — Blocking `calib` command degradation

## Identification

| Field | Value |
|---|---|
| Date | 2026-09-26 |
| Operator | Juan Pablo Vargas Cordoba |
| Objective | Reproduce and measure the impact of a synchronous console command on hard sampling |
| Linked requirements | REQ-CTRL-03, REQ-CTRL-06 |
| Platform | NUCLEO-G474RE (`nucleo_g474re/stm32g474xx`), cache ON |
| Instrument | Analog Discovery 2; WaveForms 3.25.1 Logic Analyzer; ST-LINK VCP at 115200 8N1 |
| Capture | Record mode, 30,000,000 samples, 1 MHz, 30 s, 1 us sample resolution |
| Workload | `calib` entered once during capture; Pattern generator stopped |
| Verdict | FAIL — hard sampling deadline and console non-interference requirement are violated |

## Stimulus

The console command was entered exactly as `calib`. Its handler executes 1,000
rounds of a pressure read followed by `k_busy_wait(400)`, so it blocks the only
superloop context for at least 400 ms plus read and printing overhead:

```c
for (int i = 0; i < CALIB_ROUNDS; i++) {
	(void)read_pressure_mv();
	k_busy_wait(400);
}
```

Timer interrupts remain enabled during this loop. Each 1 kHz ISR increments
`ticks_pending`, but `task_sampling()` cannot run until `task_console()` returns.

## Results

| Measurement | Idle / baseline | During `calib` |
|---|---:|---:|
| `backlog_peak` from serial `status` | 6 ticks | 414 ticks |
| DIO0 maximum period | 6.845 ms | 414.06 ms |
| DIO0 maximum absolute jitter | 5.845 ms | 413.06 ms |
| DIO0 period standard deviation | 199.62 us | 2.3963 ms |

`414 ticks × 1 ms/tick ≈ 414 ms`, matching the analyzer's 414.06 ms gap. The
wide DIO2 pulse marks the synchronous console command and the coincident DIO0 gap
marks the missed sampling releases. The hard 1 ms sampling deadline is exceeded
by 413.06 ms; the superloop then runs catch-up sampling jobs with very short
inter-arrival times.

## Artifact

- [Blocking-command statistics and overview](EV-W02-BLOCK-005-statistics.png)
