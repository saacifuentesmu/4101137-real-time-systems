# EV-W02-FLOWLAT-003 — Flow ISR to loop-service latency

## Identification

| Field | Value |
|---|---|
| Date | 2026-09-26 |
| Operator | Juan Pablo Vargas Cordoba |
| Objective | Characterize the delay from the flow-pulse ISR to `task_flow_batch()` |
| Platform | NUCLEO-G474RE (`nucleo_g474re/stm32g474xx`) |
| Firmware | `firmware/superloop/`, cache ON |
| Instrument | Analog Discovery 2; WaveForms 3.25.1 Logic Analyzer and Patterns |
| Capture | Record mode, 30,000,000 samples, 1 MHz, 30 s, 1 us sample resolution |
| Verdict | INCONCLUSIVE for a requirement — no flow-service deadline has been allocated yet |

## Stimulus and connections

The AD2 Pattern generator drove DIO6 as a 100 Hz, 50% duty-cycle, 3.3 V push-pull
clock with idle low. DIO6 was wired to Nucleo D9/PC7, configured as `flow_pulse`.
The existing analyzer connection DIO4 to Nucleo D7/PA8 observed `instr_flow`.

At 100 Hz, one rising edge arrives every 10 ms and the firmware calls the flow
batch task after 100 edges, about once per second. The low stimulus rate makes the
triggering (100th) edge unambiguous: no further DIO6 rising edge occurs before a
service latency below 10 ms has elapsed.

## Result

In the selected event, DIO6 rose first and DIO4 rose 6.046 us later. Since the
capture resolution is 1 us, the reported observed latency is **approximately
6 us**. This is the interval from ISR event arrival to loop service, not the ISR
execution time and not a worst-case bound.

## Artifacts

- [30 s stimulus and batch overview](EV-W02-FLOWLAT-003-overview.png)
- [Zoomed DIO6-to-DIO4 measurement](EV-W02-FLOWLAT-003-latency.png)
