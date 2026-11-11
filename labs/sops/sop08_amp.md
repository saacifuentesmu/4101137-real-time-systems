# SOP-08 — Two images on the two cores (sysbuild / AMP)

- **Serves:** [lab08_amp.md](../lab08_amp.md)
- **Hardware:** ESP32-S3 DevKitC + logic analyzer; for the hop row, a free channel
  on GPIO18.
- **Firmware:** [firmware/amp_node/](../../firmware/amp_node/), the reference the
  session builds step by step.

Steps, checks, and troubleshooting only — the *why* lives in the lab. The session
is guided: the instructor runs each step on the projector first.

## 1. The reference sample first

Prove the AMP plumbing before touching your code:

```bash
west build -p -b esp32s3_devkitc/esp32s3/procpu \
    zephyr/samples/drivers/ipm/ipm_esp32 --sysbuild -- -DSB_CONFIG_BOOTLOADER_NONE=y
west flash
```

`SB_CONFIG_BOOTLOADER_NONE` keeps ESP simple boot: sysbuild's default bootloader
(MCUboot) is a module the course's `west.yml` doesn't fetch.

**Verify:** the console shows PROCPU's requests and APPCPU's replies (`APP_CPU
uptime ticks …`): both cores alive from one `west flash`.

## 2. Project layout

Two apps, one sysbuild. This layout is the project's node from here on:

```
amp_node/
├── common/node_ipm.h    # the messages both images share
├── app_procpu/          # console, telemetry, flow, display, synthetic load
│   ├── CMakeLists.txt   # project(app_procpu)
│   ├── prj.conf         # CONFIG_IPM=y: PROCPU starts the APPCPU only with IPM on
│   ├── app.overlay      # &ipm0 { status = "okay"; }; + PROCPU's pins
│   ├── sysbuild.cmake   # registers app_appcpu
│   └── sysbuild.conf    # SB_CONFIG_BOOTLOADER_NONE=y
└── app_appcpu/          # sampling, control, e-stop, valve; no console
    ├── CMakeLists.txt   # project(app_appcpu)
    ├── prj.conf         # CONFIG_GPIO=y, CONFIG_IPM=y
    ├── app.overlay      # only the hard path's pins: GPIO4, 5, 21
    └── iram.conf        # step 4
```

`app_procpu/sysbuild.cmake` registers the second image and builds it first
(PROCPU's image needs the APPCPU image's load address):

```cmake
ExternalZephyrProject_Add(
	APPLICATION app_appcpu
	SOURCE_DIR ${APP_DIR}/../app_appcpu
	BOARD esp32s3_devkitc/esp32s3/appcpu
)
add_dependencies(app_procpu app_appcpu)
sysbuild_add_dependencies(CONFIGURE app_procpu app_appcpu)
```

Every IPM message carries the full state, and each `ipm_register_callback()`
handler copies it and returns: the talk's IPM slide gives the reason.

## 3. Build, flash, run

```bash
west build -p -b esp32s3_devkitc/esp32s3/procpu firmware/amp_node/app_procpu --sysbuild
west flash
```

**Verify:**
- The console (UART jack) answers `status`, with `ipm_msgs` growing ≈ 10 per second.
- `instr_samp` toggles at 1 kHz on the analyzer: the only APPCPU health signal you get.
- `set 3300` trips the e-stop: the valve stops (APPCPU), `estop=1` in `status`
  (PROCPU); `set 1500` then `clear` resumes.

**The hop row:** analyzer on GPIO4 (`instr_samp`) and GPIO18 (`instr_ipm`), trigger
on GPIO18 rising, ≥ 4 MHz. Then, five times:

1. `set 3300` and wait for the trigger (under a second).
2. Measure from the rising edge of the `instr_samp` pulse that contains the trip
   to the GPIO18 edge.
3. `set 1500`, then `clear`.

**Verify:** five GPIO18 edges, one per trip, each after the rising edge of its
`instr_samp` pulse.

## 4. The one-core rows

The week-4 kernel node with the same synthetic load, on one core. Build it into
its own directory so the two-core build stays in `build/`:

```bash
west build -p -d build/one_core -b esp32s3_devkitc/esp32s3/procpu firmware/kernel \
  -- -DEXTRA_CONF_FILE=load.conf
west flash -d build/one_core
```

**Verify:** `help` lists `load on|off`, and `instr_samp` toggles at 1 kHz. Measure
the first row with `load off` and the second with `load on`, ≥ 60 s each. Then
`west flash` puts the two-core node back.

## 5. The hard path in internal RAM

```bash
west build -p -b esp32s3_devkitc/esp32s3/procpu firmware/amp_node/app_procpu --sysbuild \
  -- -Dapp_appcpu_EXTRA_CONF_FILE=iram.conf
west flash
```

`iram.conf` places the APPCPU's sampling and control path in IRAM and writes its
pins through the GPIO registers: the GPIO driver and the pin specs live in flash.

**Verify:** the APPCPU's `sampling_thread` sits in internal RAM. The SDK's `nm` isn't
on your `PATH`; the build records where it is:

```bash
NM=$(sed -n 's/^CMAKE_NM:FILEPATH=//p' build/app_appcpu/CMakeCache.txt)
$NM build/app_appcpu/zephyr/zephyr.elf | grep sampling_thread
```

The address starts with `0x403…` (IRAM), not `0x42…`/`0x43…` (flash).

## 6. Debugging the APPCPU

There is **no Zephyr console on the APPCPU**. If you must print during bring-up:

```c
extern int ets_printf(const char *fmt, ...);
ets_printf("appcpu alive: %d\n", counter);   /* ROM UART, bring-up only */
```

Remove it before measuring — it perturbs the loop. Measurement is by GPIO, as always.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| CMake can't find `mcuboot` | Sysbuild's default bootloader | `-DSB_CONFIG_BOOTLOADER_NONE=y`, or `sysbuild.conf` as in the reference |
| APPCPU GPIO never toggles, `instr_samp` flat | `CONFIG_GPIO` missing from the APPCPU's `prj.conf` | Add it; the pins come from `app_appcpu/app.overlay` |
| APPCPU GPIO never toggles, `ipm_msgs` stays 0 | Second core not started | PROCPU starts it only with IPM enabled: `CONFIG_IPM=y` and `&ipm0 { status = "okay"; };` in the **procpu** image; confirm sysbuild built both (`build/app_appcpu/` exists) |
| `west flash` writes only one image | Built without `--sysbuild` | Rebuild with `--sysbuild`; flash from the sysbuild build dir |
| Both cores fight over a pin | Same GPIO claimed in both DTs | Keep pin maps disjoint: the hard path's pins only in `app_appcpu/app.overlay` |
| `load on` answers `? (try: help)` | One-core build without `load.conf` | Rebuild as in §4 |
| GPIO18 never rises on a trip | Two-core node not flashed back after §4 | `west flash` from `build/` |
| `iram.conf` build: `PIN_CTRL` errors | The HAL defines `PIN_CTRL` as a macro | Don't name your own symbols `PIN_*` |
| `ets_printf` output interleaves garbage | Both cores writing the ROM UART | Print from one core at a time; delete the prints before measuring |
