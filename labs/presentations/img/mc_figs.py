#!/usr/bin/env python3
"""Figures for the week-8 deck (08_freertos_multicore_wcet.md).

    python3 mc_figs.py        # writes the mc_*.svg figures here
"""
import math
from pathlib import Path

from figlib import C, GRID, INK, MUTED, PANEL, T, line, poly, rect, save, svg, text

HERE = Path(__file__).resolve().parent
SAMP, VALVE, ISR = "c2", "c5", "c8"  # sampling, the valve (control's output), interrupts
LIGHT = "#e2e8f0"


def nbox(x, y, w, h, label, size=22, sub="", sub_size=None):
    """A neutral box: hardware and generic tasks carry no palette color."""
    out = [rect(x, y, w, h, PANEL, MUTED, 2, 10)]
    if sub:
        out.append(text(x + w / 2, y + h / 2 - 6, label, size, 700, INK, "middle"))
        out.append(text(x + w / 2, y + h / 2 + (sub_size or size - 4) + 2, sub, sub_size or size - 4, 400, MUTED, "middle"))
    else:
        out.append(text(x + w / 2, y + h / 2 + size / 3, label, size, 700, INK, "middle"))
    return "\n".join(out)


def cbox(x, y, w, h, label, col, size=22, sub=""):
    out = [rect(x, y, w, h, T[col], C[col], 2, 10)]
    if sub:
        out.append(text(x + w / 2, y + h / 2 - 6, label, size, 700, C[col], "middle"))
        out.append(text(x + w / 2, y + h / 2 + size - 2, sub, size - 4, 400, INK, "middle"))
    else:
        out.append(text(x + w / 2, y + h / 2 + size / 3, label, size, 700, C[col], "middle"))
    return "\n".join(out)


def models():
    body = [text(290, 36, "Global: one queue, any core", 24, 700, INK, "middle"),
            text(910, 36, "Partitioned: one queue per core", 24, 700, INK, "middle")]
    body.append(nbox(130, 70, 320, 70, "ready queue: τ1 τ2 τ3 τ4", 22))
    for i, cpu in enumerate(("CPU 0", "CPU 1")):
        x = 80 + i * 240
        body.append(nbox(x, 230, 180, 80, cpu, 24))
        body.append(line(290, 140, x + 90, 230, MUTED, 3, arrow=True))
    body.append(text(290, 360, "tasks migrate: best average use,", 20, 400, INK, "middle"))
    body.append(text(290, 388, "per-core analysis no longer holds", 20, 400, INK, "middle"))
    body.append(text(290, 426, "ESP-IDF on the S3", 20, 700, MUTED, "middle"))
    for i, (cpu, q, col) in enumerate((("PROCPU", "node + load", None), ("APPCPU", "hard loop alone", SAMP))):
        x = 690 + i * 260
        body.append(cbox(x, 70, 200, 70, q, col, 21) if col else nbox(x, 70, 200, 70, q, 21))
        body.append(nbox(x + 10, 230, 180, 80, cpu, 24))
        body.append(line(x + 100, 140, x + 100, 230, MUTED, 3, arrow=True))
    body.append(line(620, 60, 620, 440, GRID, 2))
    body.append(text(910, 360, "each core analyzed alone:", 20, 400, INK, "middle"))
    body.append(text(910, 388, "week 6 holds, core by core", 20, 400, INK, "middle"))
    body.append(text(910, 426, "Zephyr AMP on the S3: one image per core", 20, 700, MUTED, "middle"))
    return svg(1220, 450, body)


def dhall():
    """Dhall's effect (Dhall & Liu 1978) with numbers: U = 1.31 on two cores."""
    x0, x1, t_end = 210, 1170, 12.5
    sx = lambda t: x0 + (x1 - x0) * t / t_end
    h = 40

    def job(t0, t1, y, name, heavy):
        fill, stroke = (T[SAMP], C[SAMP]) if heavy else (LIGHT, MUTED)
        out = [rect(sx(t0), y, sx(t1) - sx(t0), h, fill, stroke, 2, 4)]
        out.append(text((sx(t0) + sx(t1)) / 2, y + 27, name, 19, 700, C[SAMP] if heavy else INK, "middle"))
        return out

    body = []
    panels = (("Global, EDF or RM: one queue for both cores", 40, 0,
               [(0, 2, 0, "τ1", False), (2, 12, 0, "τ3", True), (0, 2, 1, "τ2", False), (10, 12, 1, "τ1", False)]),
              ("Partitioned: τ3 alone on core 1", 220, 1,
               [(0, 2, 0, "τ1", False), (2, 4, 0, "τ2", False), (10, 12, 0, "τ1", False), (12, 12.5, 0, "", False),
                (0, 10, 1, "τ3", True), (11, 12.5, 1, "", True)]))
    for title, top, t3_core, jobs in panels:
        body.append(text(x0, top, title, 22, 700, INK))
        for core in (0, 1):
            y = top + 16 + core * 52
            body.append(text(x0 - 14, y + 27, f"core {core}", 20, 700, MUTED, "end"))
            body.append(line(x0, y + h, x1, y + h, GRID, 1))
        for t0, t1, core, name, heavy in jobs:
            body += job(t0, t1, top + 16 + core * 52, name, heavy)
        yr = top + 16 + t3_core * 52
        body.append(line(sx(11), yr - 10, sx(11), yr + h + 6, C["c5"], 3, "8 6"))
        body.append(text(sx(11) + 6, top + 4, "τ3 deadline", 17, 700, C["c5"]))
    y_miss = 40 + 16
    body.append(rect(sx(11), y_miss, sx(12) - sx(11), h, T["c5"], C["c5"], 3, 4))
    body.append(text(sx(11.5), y_miss + 27, "miss", 19, 700, C["c5"], "middle"))
    body.append(text(sx(10) - 6, 220 + 16 + 52 + h + 22, "τ3 done at 10 ms", 18, 700, C[SAMP], "end"))
    ya = 400
    body.append(line(x0, ya, x1, ya, MUTED, 2, arrow=True))
    for t in range(0, 13, 2):
        body.append(line(sx(t), ya - 6, sx(t), ya + 6, MUTED, 2))
        body.append(text(sx(t), ya + 28, f"{t}", 18, 400, MUTED, "middle"))
    body.append(text(x1, ya - 12, "ms", 18, 400, MUTED, "end"))
    body.append(text(20, ya + 62, "τ1, τ2: C = 2, T = D = 10 ms · τ3: C = 10, T = D = 11 ms · "
                     "U = 0.2 + 0.2 + 0.91 = 1.31 of 2 cores (65 %)", 19, 400, INK))
    return svg(1200, 480, body)


def s3mem():
    """ESP32-S3 datasheet v2.2 §4.1.2; addresses from hal_espressif soc.h and the week-8 builds."""
    body = [nbox(330, 24, 220, 64, "PROCPU", 24), nbox(650, 24, 220, 64, "APPCPU", 24)]
    body.append(nbox(40, 170, 520, 92, "ICache 16 KB + DCache 32 KB", 22, "one pair, shared by both cores"))
    body.append(nbox(640, 170, 520, 92, "Internal SRAM, 512 KB", 22, "IRAM 0x4037_0000 … 0x403D_FFFF"))
    body.append(nbox(40, 340, 520, 92, "External flash, over SPI0", 22, "code 0x4200_0000 … · constants 0x3C00_0000 …"))
    for x_from, x_to in ((400, 260), (720, 400), (480, 820), (800, 980)):
        body.append(line(x_from, 88, x_to, 168, MUTED, 3, arrow=True))
    body.append(line(300, 262, 300, 338, MUTED, 3, arrow=True))
    body.append(text(316, 306, "a miss from either core", 18, 400, MUTED))
    body.append(text(316, 328, "waits on the same flash", 18, 400, MUTED))
    body.append(text(900, 296, "no cache in the path:", 19, 400, MUTED, "middle"))
    body.append(text(900, 320, "same cost every fetch", 19, 400, MUTED, "middle"))
    body.append(text(900, 354, "sampling_thread with iram.conf:", 19, 700, C[SAMP], "middle"))
    body.append(text(900, 378, "0x403B_57B8", 19, 700, C[SAMP], "middle"))
    body.append(text(580, 414, "sampling_thread by default:", 19, 700, C[SAMP]))
    body.append(text(580, 438, "0x43E0_02EC, through the cache", 19, 700, C[SAMP]))
    return svg(1200, 470, body)


def amp_boot():
    """soc/espressif/esp32s3/esp32s3-mp.c at the pinned Zephyr; offsets from the amp_node build."""
    body = [text(190, 30, "Flash, one west flash", 22, 700, INK, "middle")]
    body.append(nbox(60, 50, 260, 130, "PROCPU image", 22, "0x00_0000"))
    body.append(text(190, 222, "⋮", 30, 700, MUTED, "middle"))
    body.append(cbox(60, 250, 260, 110, "APPCPU image", SAMP, 22, "0x2C_0000"))
    steps = (("1  The ROM boots PROCPU's image (ESP simple boot)", None),
             ("2  PROCPU's Zephyr starts and, with IPM on, reads APPCPU's image", None),
             ("3  It copies that image's RAM parts and maps its flash code", None),
             ("4  It releases APPCPU: a second Zephyr, its own scheduler", SAMP))
    for i, (s, col) in enumerate(steps):
        y = 40 + i * 90
        body.append(rect(360, y, 820, 64, T[col] if col else PANEL, C[col] if col else MUTED, 2, 10))
        body.append(text(380, y + 40, s, 20, 700, C[col] if col else INK))
    body.append(line(320, 110, 358, 72, MUTED, 3, arrow=True))
    body.append(line(320, 300, 358, 252, C[SAMP], 3, arrow=True))
    body.append(text(60, 410, "No shared kernel: each core schedules only its own threads.", 21, 400, INK))
    return svg(1200, 430, body)


def ipm():
    """drivers/ipm/ipm_esp32.c and the esp32s3 devicetree at the pinned Zephyr."""
    body = [nbox(40, 170, 220, 90, "PROCPU", 24), nbox(940, 170, 220, 90, "APPCPU", 24)]
    body.append(rect(360, 60, 480, 290, PANEL, MUTED, 2, 12))
    body.append(text(600, 92, "shared RAM, 1 KB", 22, 700, INK, "middle"))
    body.append(nbox(390, 112, 420, 80, "PROCPU → APPCPU", 21, "512 B, one slot: set, clear"))
    body.append(cbox(390, 222, 420, 80, "APPCPU → PROCPU", SAMP, 21, "512 B, one slot: status"))
    body.append(text(600, 334, "+ a lock and the message ID", 18, 400, MUTED, "middle"))
    body.append(line(940, 250, 812, 262, C[SAMP], 3, arrow=True))
    body.append(text(1050, 300, "1  lock, copy, unlock", 19, 700, C[SAMP], "middle"))
    body.append(poly([(1050, 170), (1050, 26), (150, 26), (150, 166)], C[ISR], 3, arrow=True))
    body.append(text(600, 18, "2  cross-core interrupt", 19, 700, C[ISR], "middle"))
    body.append(line(388, 262, 262, 240, C[ISR], 3, arrow=True))
    body.append(text(150, 300, "3  handler copies", 19, 700, C[ISR], "middle"))
    body.append(text(150, 324, "and returns", 19, 700, C[ISR], "middle"))
    body.append(text(600, 392, "A second send before the handler copies replaces the first.", 21, 700, INK, "middle"))
    body.append(text(600, 420, "So every message carries the full state.", 21, 400, INK, "middle"))
    return svg(1200, 440, body)


def hop():
    """What the hop row measures. Schematic: pulses widened, hop not to scale."""
    x0, unit = 290, 330
    sx = lambda t: x0 + unit * t
    rows = (("instr_samp", "GPIO4 · APPCPU", SAMP, 50), ("valve", "GPIO21 · APPCPU", VALVE, 140),
            ("instr_ipm", "GPIO18 · PROCPU", ISR, 230))
    body = []
    for name, sub, col, y in rows:
        body.append(text(x0 - 30, y + 24, name, 21, 700, C[col], "end"))
        body.append(text(x0 - 30, y + 48, sub, 17, 400, MUTED, "end"))
    lo, hi, w = 50 + 50, 50 + 10, 0.07
    pts = [(sx(-0.05), lo)]
    for t in (0, 1, 2):
        pts += [(sx(t), lo), (sx(t), hi), (sx(t + w), hi), (sx(t + w), lo)]
    pts.append((sx(2.6), lo))
    body.append(poly(pts, C[SAMP], 3))
    vlo, vhi = 140 + 50, 140 + 10
    vpts = [(sx(-0.05), vlo)]
    for t in (0.0, 0.35, 0.7):
        vpts += [(sx(t), vlo), (sx(t), vhi), (sx(t + 0.2), vhi), (sx(t + 0.2), vlo)]
    vpts.append((sx(2.6), vlo))
    body.append(poly(vpts, C[VALVE], 3))
    hop_t = 1.22
    ilo, ihi = 230 + 50, 230 + 10
    body.append(poly([(sx(-0.05), ilo), (sx(hop_t), ilo), (sx(hop_t), ihi), (sx(2.6), ihi)], C[ISR], 3))
    body.append(line(sx(1), 30, sx(1), 300, C[SAMP], 2, "6 5"))
    body.append(text(sx(1) - 8, 28, "pressure > 3000 mV in this job", 18, 700, C[SAMP], "end"))
    body.append(text(sx(1.1), 128, "valve low in the same job (ADR-005)", 18, 700, C[VALVE]))
    body.append(line(sx(1), 318, sx(hop_t), 318, INK, 3))
    for x in (sx(1), sx(hop_t)):
        body.append(line(x, 308, x, 328, INK, 3))
    body.append(text(sx(hop_t) + 14, 324, "the hop: today's last row", 20, 700, INK))
    body.append(text(40, 372, "From week 12: PROCPU sends the CAN e-stop frame → the Hub stops the pump"
                     " (≤ 20 ms end to end)", 19, 400, MUTED))
    body.append(text(sx(2.6), 404, "schematic: pulses widened, hop not to scale", 16, 400, MUTED, "end"))
    return svg(1200, 420, body)


def tail():
    """Max sampling jitter over 60 s, ESP32-S3 N16R8, 2026-10-21 (amp_node README, RET §3 wk 8)."""
    cases = (("1 core, no load", 2.25, None), ("1 core, load on", 10.5, None),
             ("APPCPU, PROCPU idle", 0.25, None), ("APPCPU, load on PROCPU", 12.0, 21.0),
             ("APPCPU in IRAM, load on PROCPU", 0.25, None))
    x0, x1, vmax = 420, 1100, 22
    sx = lambda v: x0 + (x1 - x0) * v / vmax
    body = []
    for i, (name, lo, hi) in enumerate(cases):
        y = 30 + i * 66
        body.append(text(x0 - 16, y + 32, name, 21, 700, INK, "end"))
        body.append(rect(x0, y + 6, max(sx(lo) - x0, 3), 38, T[SAMP], C[SAMP], 2, 4))
        if hi:
            body.append(rect(sx(lo), y + 6, sx(hi) - sx(lo), 38, PANEL, C[SAMP], 2, 4, "6 5"))
            body.append(text((sx(lo) + sx(hi)) / 2, y + 32, "12–21 µs, run to run", 20, 700, C[SAMP], "middle"))
        else:
            body.append(text(max(sx(lo), x0 + 3) + 10, y + 32, f"{lo:g} µs", 20, 700, C[SAMP]))
    ya = 30 + len(cases) * 66 + 8
    body.append(line(x0, ya, x1, ya, MUTED, 2))
    for v in range(0, 23, 5):
        body.append(line(sx(v), ya, sx(v), ya + 8, MUTED, 2))
        body.append(text(sx(v), ya + 30, f"{v}", 18, 400, MUTED, "middle"))
    body.append(text(x1 + 10, ya + 30, "µs", 18, 400, MUTED))
    body.append(text(40, ya + 70, "Max sampling jitter over 60 s, ESP32-S3 N16R8, 2026-10-21. "
                     "Average period 1000.12 µs in every case.", 18, 400, MUTED))
    return svg(1200, ya + 86, body)


def wcet():
    """After Wilhelm et al. (2008), Fig. 1: what measurement and analysis each bound."""
    x0, x1, y0 = 80, 1180, 300
    sx = lambda u: x0 + (x1 - x0) * u
    xs = [i / 400 for i in range(0, 401)]
    dens = lambda u: max(u - 0.12, 0) ** 3 * math.exp(-max(u - 0.12, 0) / 0.05)
    top = max(dens(u) for u in xs)
    pts = [(sx(u), y0 - 200 * dens(u) / top) for u in xs if u < 0.56]
    body = [line(x0, y0, x1, y0, MUTED, 2, arrow=True), text(x1, y0 + 30, "execution time", 20, 400, MUTED, "end"),
            poly([(sx(0.12), y0)] + pts + [(pts[-1][0], y0)], C["c2"], 3, T["c2"])]
    marks = [(0.55, "observed max", "c2", "measurement"), (0.66, "high-water mark + margin", "c3", "industry default"),
             (0.74, "true WCET", "c5", "unknown"), (0.9, "static bound", "c6", "safe, pessimistic")]
    for k, (u, name, col, sub) in enumerate(marks):
        dash = "8 6" if name == "true WCET" else ""
        body.append(line(sx(u), y0 + 8, sx(u), 80, C[col], 3, dash))
        body.append(text(sx(u), y0 + 58 + (k % 2) * 50, name, 20, 700, C[col], "middle"))
        body.append(text(sx(u), y0 + 82 + (k % 2) * 50, sub, 17, 400, MUTED, "middle"))
    body.append(line(sx(0.555), 70, sx(0.735), 70, C["c5"], 3))
    body.append(text(sx(0.645), 50, "measurement can miss this", 18, 700, C["c5"], "middle"))
    return svg(1240, 450, body)


if __name__ == "__main__":
    figs = {"mc_models.svg": models, "mc_dhall.svg": dhall, "mc_s3mem.svg": s3mem, "mc_boot.svg": amp_boot,
            "mc_ipm.svg": ipm, "mc_hop.svg": hop, "mc_tail.svg": tail, "mc_wcet.svg": wcet}
    for name, fn in figs.items():
        save(HERE, name, fn())
    print(" ".join(figs))
