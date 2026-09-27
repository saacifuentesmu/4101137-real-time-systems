# EV-W02-CACHE-004 — STM32G474 flash-accelerator comparison

## Identification

| Field | Value |
|---|---|
| Date | 2026-09-26 |
| Operator | Juan Pablo Vargas Cordoba |
| Objective | Re-measure sampling with flash instruction/data caches and prefetch disabled |
| Linked requirement | REQ-CTRL-03 |
| Platform | NUCLEO-G474RE (`nucleo_g474re/stm32g474xx`) |
| Instrument | Analog Discovery 2; WaveForms 3.25.1 Logic Analyzer |
| Capture | Record mode, 30,000,000 samples, 1 MHz, 30 s, 1 us sample resolution |
| Workload | Normal operation; no console command; Pattern generator stopped |
| Verdict | FAIL — 1 ms hard sampling period remains exceeded |

## G474 adaptation

The lab originally constrained `LAB_FLASH_CACHE_OFF` to STM32L4. The G474 has the
same ART instruction cache, data cache, and prefetch controls, but Zephyr enables
the two caches unconditionally in its G4 early initialization. The Week 2 port:

1. permits `LAB_FLASH_CACHE_OFF` for `SOC_SERIES_STM32G4X` as well as L4;
2. compiles `cache_stm32_art.c`, whose `PRE_KERNEL_1` hook disables instruction
   and data caches with the G4 LL API; and
3. applies `CONFIG_STM32_FLASH_PREFETCH=n` from `nocache.conf`.

The generated configuration was checked as:

```text
CONFIG_LAB_FLASH_CACHE_OFF=y
# CONFIG_STM32_FLASH_PREFETCH is not set
```

## Reproduction

```bash
source ~/zephyrproject/.venv/bin/activate
cd ~/zephyrproject/zephyr
west build -p always -b nucleo_g474re \
  ~/4101137-real-time-systems/firmware/superloop \
  -d build/superloop-g474-nocache \
  -- -DEXTRA_CONF_FILE=nocache.conf
west flash -d build/superloop-g474-nocache --runner pyocd
```

## Results

| DIO0 statistic | Cache ON | Cache OFF |
|---|---:|---:|
| Mean period | 1.0001 ms | 1.0001 ms |
| Minimum period | 6 us | 7 us |
| Maximum period | 6.845 ms | 6.857 ms |
| Maximum absolute jitter | 5.845 ms | 5.857 ms |
| Mean positive width | 2.4886 us | 3.3888 us |
| Positive width maximum | 3 us | 4 us |

Cache-off increased observed sampling width by 0.9002 us (about 36.2%). The
worst sampling jitter increased only 12 us because the dominant interference is
the blocking telemetry path, not the sampling instruction-fetch cost.

## Artifact

- [Cache-off statistics](EV-W02-CACHE-004-statistics.png)
