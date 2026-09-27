# EV-W02-BASELINE-002 — Cache-on superloop baseline

## Identification

| Field | Value |
|---|---|
| Date | 2026-09-26 |
| Operator | Juan Pablo Vargas Cordoba |
| Objective | Measure sampling period, release jitter, and observed execution width in the supplied superloop |
| Linked requirement | REQ-CTRL-03 |
| Platform | NUCLEO-G474RE (`nucleo_g474re/stm32g474xx`), STLINK-V3 `003400303232510139353236` |
| Firmware | `firmware/superloop/`, cache ON / flash prefetch ON |
| Instrument | Analog Discovery 2; WaveForms 3.25.1 Logic Analyzer |
| Capture | Record mode, 30,000,000 samples, 1 MHz, 30 s, 1 us sample resolution |
| Workload | Normal operation; no console command; Pattern generator stopped |
| Verdict | FAIL — hard 1 ms sampling period is exceeded |

## Connections

| AD2 input | Nucleo pin | Signal |
|---|---|---|
| DIO0 | D3 / PB3 | `instr_samp` |
| DIO1 | D4 / PB5 | `instr_ctrl` |
| DIO2 | D5 / PB4 | `instr_cons` |
| DIO3 | D6 / PB10 | `instr_tele` |
| DIO4 | D7 / PA8 | `instr_flow` |
| DIO5 | D8 / PA9 | `instr_disp` |
| GND | GND | Common reference |

## Reproduction

```bash
source ~/zephyrproject/.venv/bin/activate
cd ~/zephyrproject/zephyr
west build -p always -b nucleo_g474re \
  ~/4101137-real-time-systems/firmware/superloop \
  -d build/superloop-g474
west flash -d build/superloop-g474 --runner pyocd
```

Configure WaveForms Logic as Record, `30 M` samples at `1 MHz`, data compression
enabled, and capture for 30 s. Add `DIO0 Period` and `DIO0 PosWidth` statistics.

## Results

| DIO0 statistic | Value |
|---|---:|
| Period count | 29,998 |
| Mean period | 1.0001 ms |
| Minimum period | 6 us |
| Maximum period | 6.845 ms |
| Period standard deviation | 199.62 us |
| Mean positive width | 2.4886 us |
| Positive width minimum–maximum | 2–3 us |

With nominal period `T = 1000 us`, the maximum absolute period deviation is:

`max(|6 - 1000|, |6845 - 1000|) = 5845 us`.

The measured maximum period exceeds the 1 ms deadline by 5.845 ms. The average
remains near 1 ms because delayed jobs are followed by rapid catch-up jobs; it is
not evidence of deadline compliance. `C_obs,max` for sampling is 3 us under this
protocol, not a proven WCET.

## Artifacts

- [30 s overview](EV-W02-BASELINE-002-overview.png)
- [Pulse statistics](EV-W02-BASELINE-002-statistics.png)

## Limitation

WaveForms screenshots are preserved as the supplied raw visual record. The
WaveForms transition export/workspace was not retained, so this evidence supports
the stated analyzer statistics but not offline re-analysis of every edge.
