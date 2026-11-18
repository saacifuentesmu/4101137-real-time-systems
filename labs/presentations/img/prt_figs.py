#!/usr/bin/env python3
"""Figures for the week-9 deck (09_preempt_rt.md).

    python3 prt_figs.py       # writes the prt_*.svg figures here

Everything is schematic except prt_scale's MCU row, which is week 8's measured max
jitter (ESP32-S3 N16R8, 60 s runs, 2026-10-21). The Linux bands there are the expected
ranges the lab replaces with its own table.
"""
import math
from pathlib import Path

from figlib import C, GRID, INK, MUTED, PANEL, T, line, poly, rect, save, svg, text

HERE = Path(__file__).resolve().parent
CTRL, ISR, SAMP, DISP, TELE = "c5", "c8", "c2", "c7", "c3"
MONO = "'DejaVu Sans Mono', 'Courier New', monospace"
HATCH = (f'<defs><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" '
         f'patternTransform="rotate(45)"><rect width="10" height="10" fill="#fff"/>'
         f'<rect width="4" height="10" fill="{GRID}"/></pattern></defs>')


def nbox(x, y, w, h, label, size=21, sub="", sub_size=None):
    """A neutral box: kernel work and generic tasks carry no palette color."""
    out = [rect(x, y, w, h, PANEL, MUTED, 2, 10)]
    out += _labels(x, y, w, h, label, size, sub, sub_size, INK)
    return "\n".join(out)


def cbox(x, y, w, h, label, col, size=21, sub="", sub_size=None):
    out = [rect(x, y, w, h, T[col], C[col], 2, 10)]
    out += _labels(x, y, w, h, label, size, sub, sub_size, C[col])
    return "\n".join(out)


def wall(x, y, w, h, label, size=20, sub=""):
    """Work that can't be preempted: a solid dark block."""
    out = [rect(x, y, w, h, MUTED, MUTED, 2, 10)]
    out += _labels(x, y, w, h, label, size, sub, None, "#fff", "#e2e8f0")
    return "\n".join(out)


def ghost(x, y, w, h, label, size=19, sub=""):
    """The same work, now in a thread: a dashed outline."""
    out = [rect(x, y, w, h, "#fff", MUTED, 2, 10, "8 6")]
    out += _labels(x, y, w, h, label, size, sub, None, MUTED, INK)
    return "\n".join(out)


def _labels(x, y, w, h, label, size, sub, sub_size, col, sub_col=MUTED):
    if not sub:
        return [text(x + w / 2, y + h / 2 + size / 3, label, size, 700, col, "middle")]
    ss = sub_size or size - 4
    return [text(x + w / 2, y + h / 2 - 5, label, size, 700, col, "middle"),
            text(x + w / 2, y + h / 2 + ss + 3, sub, ss, 600 if sub_col == INK else 400, sub_col, "middle")]


def mono(x, y, s, size, fill=INK, anchor="start", weight=700):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" font-family="{MONO}">{s}</text>')


def hub():
    body = [rect(30, 30, 660, 370, PANEL, MUTED, 2, 16),
            text(54, 68, "the Hub · Raspberry Pi · one Linux kernel", 22, 700, INK),
            text(54, 112, "soft: the average matters", 18, 700, MUTED),
            cbox(54, 126, 196, 76, "GUI", DISP, 23, "touch, web HMI"),
            cbox(266, 126, 196, 76, "routing", TELE, 23, "CAN ↔ IP"),
            cbox(478, 126, 190, 76, "cloud", TELE, 23, "upload, logs"),
            text(54, 246, "hard: the worst case matters", 18, 700, C[CTRL]),
            cbox(54, 260, 300, 100, "pump loop", CTRL, 26, "deadline 10 ms"),
            cbox(370, 260, 298, 100, "interlock", CTRL, 26, "stops the pump")]
    x0, x1, y = 740, 1170, 196
    body.append(text(x0, 112, "the pump loop's 10 ms", 20, 700, INK))
    body.append(rect(x0, y - 70, x1 - x0, 54, "#fff", C[CTRL], 2, 6))
    body.append(rect(x0, y - 70, 70, 54, "url(#hatch)", C[CTRL], 2, 6))
    body.append(text(x0 + 35, y - 36, "?", 24, 800, C[CTRL], "middle"))
    body.append(rect(x0 + 70, y - 70, 120, 54, T[CTRL], C[CTRL], 2, 0))
    body.append(text(x0 + 130, y - 37, "compute", 17, 700, C[CTRL], "middle"))
    body.append(text(x0 + 270, y - 37, "slack", 17, 400, MUTED, "middle"))
    body.append(line(x0 + 35, y - 12, x0 + 35, y + 36, C[CTRL], 2))
    body.append(text(x0, y + 62, "wake-up latency:", 20, 700, INK))
    body.append(text(x0, y + 92, "stock Linux gives it no bound;", 19, 400, INK))
    body.append(text(x0, y + 120, "PREEMPT_RT gives one you measure.", 19, 400, INK))
    body.append(text(x0, y + 172, "today: measure that bound", 20, 700, C[CTRL]))
    return svg(1200, 420, [HATCH] + body)


PATH = [("timer IRQ", 120, False, ""), ("other devices' IRQs", 220, True, "now threads"),
        ("a driver's spinlock", 220, True, "rtmutex + PI"), ("softirq", 150, True, "threaded"),
        ("scheduler", 140, False, ""), ("your thread", 150, False, "")]


def wakeup():
    body, x0 = [], 30
    rows = (("Stock kernel: the dark work can't be preempted", False),
            ("PREEMPT_RT: the same work, now in threads that priority can jump", True))
    for row, (title, rt) in enumerate(rows):
        y = 30 + row * 190
        body.append(text(x0, y + 24, title, 22, 700, INK))
        x = x0
        for name, w, blocking, note in PATH:
            if blocking:
                body.append(ghost(x, y + 44, w, 80, name, 17, note) if rt else wall(x, y + 44, w, 80, name, 17))
            elif name == "timer IRQ":
                body.append(cbox(x, y + 44, w, 80, name, ISR, 18))
            elif name == "your thread":
                body.append(cbox(x, y + 44, w, 80, name, CTRL, 18))
            else:
                body.append(nbox(x, y + 44, w, 80, name, 18))
            x += w + 8
        a, b = x0 + 128, x0 + 128 + 220 + 220 + 150 + 16
        msg = ("your thread outranks them: the wait becomes a switch" if rt
               else "latency = the longest of these, in code you didn't write")
        body.append(line(a, y + 140, b, y + 140, INK, 3))
        for xx in (a, b):
            body.append(line(xx, y + 132, xx, y + 148, INK, 3))
        body.append(text((a + b) / 2, y + 168, msg, 19, 700, INK, "middle"))
    return svg(x0 + sum(w for _, w, _, _ in PATH) + 8 * len(PATH) + 20, 400, body)


def changes():
    rows = [("IRQ handler", "runs above every thread", "IRQ thread", "irq/NN-eth0 · SCHED_FIFO 50", True),
            ("spinlock", "spins, preemption off", "rtmutex", "sleeps · inherits priority (week 6)", False),
            ("softirq", "runs on the way out of an IRQ", "softirq in a thread", "scheduled like the rest", False)]
    body = [HATCH, text(60, 34, "stock kernel", 22, 800, MUTED), text(660, 34, "PREEMPT_RT", 22, 800, INK)]
    for i, (old, old_sub, new, new_sub, irq) in enumerate(rows):
        y = 52 + i * 78
        body.append(wall(60, y, 440, 64, old, 21, old_sub))
        body.append(line(512, y + 32, 646, y + 32, INK, 3, arrow=True))
        body.append(cbox(660, y, 480, 64, new, ISR, 21, new_sub) if irq else nbox(660, y, 480, 64, new, 21, new_sub))
    body.append(line(60, 300, 1140, 300, GRID, 2))
    body.append(text(60, 334, "Still not preemptible, even on PREEMPT_RT: the floor under every max", 21, 800, INK))
    floor = [("hard-IRQ entry", "only wakes the IRQ thread"), ("timer tick, IPIs", "stay in hard-IRQ context"),
             ("raw spinlocks", "scheduler, timers, IRQ core")]
    for i, (lab, sub) in enumerate(floor):
        body.append(wall(60 + i * 274, 352, 260, 84, lab, 20, sub))
    body.append(rect(882, 352, 258, 84, "url(#hatch)", MUTED, 2, 10, "8 6"))
    body.append(rect(902, 368, 218, 52, "#fff", "none", 0, 6))
    body.append(text(1011, 389, "firmware, hardware", 20, 700, INK, "middle"))
    body.append(text(1011, 412, "SMIs, caches: below Linux", 16, 400, MUTED, "middle"))
    body.append(text(60, 470, "The dark three are µs, and the kernel's job to keep short. The hatched one no kernel "
                     "can fix: measure it (hwlatdetect).", 18, 400, INK))
    body.append(text(60, 498, "In mainline Linux since 6.12 (2024): a build option, not a patch.", 18, 400, MUTED))
    return svg(1200, 514, body)

def ladder():
    ax, top, bot = 120, 70, 330
    yp = lambda p: bot - (bot - top) * (p - 1) / 98
    body = [text(40, 40, "SCHED_FIFO priority, PREEMPT_RT", 20, 700, INK),
            line(ax, top - 10, ax, bot + 10, MUTED, 3)]
    for p in (99, 90, 50, 1):
        body.append(line(ax - 8, yp(p), ax, yp(p), MUTED, 3))
        body.append(text(ax - 16, yp(p) + 7, str(p), 20, 700, MUTED, "end"))
    body.append(cbox(150, yp(90) - 32, 470, 64, "pump loop · cyclictest -p90", CTRL, 22))
    body.append(cbox(150, yp(50) - 32, 470, 64, "irq/NN-eth0 · irq/NN-mmc1 · …", ISR, 21))
    body.append(text(636, yp(50) + 7, "every IRQ thread, by default", 18, 400, C[ISR]))
    body.append(line(500, yp(90) + 36, 500, yp(50) - 38, C[CTRL], 3, arrow=True))
    body.append(text(522, (yp(90) + yp(50)) / 2 + 6, "outranks every handler", 18, 700, C[CTRL]))
    body.append(text(40, 384, "SCHED_OTHER, below every RT priority", 18, 700, MUTED))
    body.append(cbox(150, 398, 140, 50, "GUI", DISP, 20))
    body.append(cbox(304, 398, 140, 50, "routing", TELE, 20))
    body.append(nbox(458, 398, 162, 50, "stress-ng", 20))
    body.append(text(1015, 40, "what sits above the whole ladder", 18, 700, MUTED, "middle"))
    body.append(wall(860, 70, 310, 120, "stock kernel", 22, "every handler and softirq"))
    body.append(ghost(860, 230, 310, 120, "PREEMPT_RT", 22, "only the hard-IRQ entry: µs"))
    return svg(1200, 466, body)


def tradeoff():
    x0, x1, y0, h = 80, 1140, 330, 250
    sx = lambda u: x0 + (x1 - x0) * u
    def curve(peak, width, tail, end):
        pts = []
        for i in range(0, 401):
            u = i / 400
            if u > end:
                break
            c = 1e5 * math.exp(-((u - peak) / width) ** 2) + (1e3 * math.exp(-(u - peak) / tail) if u > peak else 0)
            pts.append((sx(u), y0 - h * min(math.log10(c + 1) / 5.2, 1)))
        return [(sx(0), y0)] + pts + [(pts[-1][0], y0)]
    stock, rt = curve(0.16, 0.035, 0.11, 0.9), curve(0.22, 0.04, 0.05, 0.42)
    body = [poly(stock, MUTED, 3, "none", "8 6"), poly(rt, INK, 4),
            line(x0, y0, x1, y0, MUTED, 2, arrow=True), line(x0, y0, x0, y0 - h - 20, MUTED, 2, arrow=True),
            text(x1, y0 + 30, "wake-up latency", 19, 400, MUTED, "end"),
            text(x0 + 8, y0 - h - 26, "samples (log)", 19, 400, MUTED)]
    for u, col, lab, dy in ((0.9, MUTED, "stock max: unbounded", 0), (0.42, INK, "PREEMPT_RT max: bounded", 0)):
        body.append(line(sx(u), y0, sx(u), 90, col, 3, "" if col == INK else "8 6"))
        body.append(text(sx(u), 76 + dy, lab, 20, 700, col, "middle"))
    body.append(text(sx(0.16), y0 + 30, "stock mean", 17, 700, MUTED, "middle"))
    body.append(text(sx(0.27), y0 + 30, "RT mean", 17, 700, INK, "start"))
    body.append(text(x0, y0 + 74, "PREEMPT_RT is often a little slower on average (more switches) and much "
                     "shorter in the tail. The tail is the product.", 19, 400, INK))
    body.append(text(x1, y0 + 104, "schematic shapes, not data", 16, 400, MUTED, "end"))
    return svg(1200, 450, body)


def measure():
    x0, unit, yt, ya = 60, 120, 120, 210
    sx = lambda t: x0 + unit * t
    lat = [0.06, 0.08, 0.05, 0.42, 0.07]
    body = [text(x0, 40, "the thread: sleep, wake, log the lateness", 20, 700, INK),
            line(x0 - 10, ya + 40, sx(5.2), ya + 40, MUTED, 2, arrow=True),
            text(sx(5.2), ya + 70, "time", 17, 400, MUTED, "end")]
    for k in range(5):
        t = k + 0.3
        body.append(line(sx(t), yt - 30, sx(t), ya + 40, GRID, 2, "6 5"))
        body.append(text(sx(t), yt - 38, "expected" if k == 0 else f"+{k} ms", 16, 700, MUTED, "middle"))
        body.append(rect(sx(t + lat[k]), ya - 6, 34, 40, T[SAMP], C[SAMP], 2, 4))
        body.append(line(sx(t), yt + 10 + 0, sx(t + lat[k]), yt + 10, C[SAMP], 3))
        body.append(line(sx(t), yt, sx(t), yt + 20, C[SAMP], 3))
        body.append(line(sx(t + lat[k]), yt, sx(t + lat[k]), yt + 20, C[SAMP], 3))
    body.append(text(sx(3.3) + 2, yt - 8 + 50, "a long one", 16, 700, C[SAMP]))
    body.append(text(x0, ya + 104, "latency = actual − expected, every period", 19, 700, C[SAMP]))
    body.append(text(x0, ya + 134, "the thread runs (box) after the timer it asked for", 18, 400, MUTED))
    hx0, hx1, hy0 = 760, 1160, 300
    bins = [5, 4.6, 3.8, 2.9, 2.0, 1.2, 0.6, 0, 0.3, 0, 0, 0.3]
    bw = (hx1 - hx0) / len(bins)
    body.append(text(hx0, 40, "the histogram (log scale)", 20, 700, INK))
    for i, b in enumerate(bins):
        if b:
            hh = 44 * b
            body.append(rect(hx0 + i * bw + 2, hy0 - hh, bw - 4, hh, T[SAMP], C[SAMP], 2, 2))
    body.append(line(hx0, hy0, hx1 + 10, hy0, MUTED, 2, arrow=True))
    xmax = hx0 + 11.5 * bw
    body.append(line(xmax, hy0 + 6, xmax, 80, INK, 3))
    body.append(text(xmax, 72, "max: the verdict", 18, 700, INK, "end"))
    xp = hx0 + 6.5 * bw
    body.append(line(xp, hy0 + 6, xp, 110, MUTED, 2, "6 5"))
    body.append(text(xp - 6, 106, "p99: context", 17, 700, MUTED, "end"))
    body.append(text(hx1, hy0 + 30, "latency →", 17, 400, MUTED, "end"))
    body.append(text(hx1, hy0 + 104, "schematic", 16, 400, MUTED, "end"))
    return svg(1200, 420, body)


def command():
    cmd = "cyclictest -m -Sp90 -i 1000 -h 400 -D 5m"
    size, cw = 34, 34 * 0.602
    x0 = (1200 - len(cmd) * cw) / 2
    xs = lambda i: x0 + i * cw
    body = [rect(x0 - 24, 30, len(cmd) * cw + 48, 70, INK, INK, 0, 12), mono(x0, 77, cmd, size, "#f8fafc")]
    flags = [("cyclictest", "a thread that only", "wakes up and logs", SAMP, 0),
             ("-m", "lock memory:", "no page faults", None, 1),
             ("-Sp90", "a thread per core,", "SCHED_FIFO 90", CTRL, 0),
             ("-i 1000", "wake every", "1000 µs", None, 1),
             ("-h 400", "histogram", "up to 400 µs", None, 0),
             ("-D 5m", "five minutes:", "300 000 wake-ups", None, 1)]
    for tok, l1, l2, col, lvl in flags:
        i = cmd.index(tok)
        cx = xs(i + len(tok) / 2)
        body.append(line(xs(i), 108, xs(i + len(tok)), 108, C[col] if col else INK, 4))
        ly = 170 if lvl == 0 else 270
        body.append(line(cx, 112, cx, ly - 30, GRID, 2))
        body.append(text(cx, ly, l1, 19, 700, C[col] if col else INK, "middle"))
        body.append(text(cx, ly + 26, l2, 19, 400, INK, "middle"))
    body.append(rect(60, 340, 1080, 96, PANEL, MUTED, 2, 12))
    body.append(text(84, 374, "and around it", 19, 700, MUTED))
    body.append(mono(84, 414, "stress-ng --cpu 0 --io 2", 21))
    body.append(text(430, 414, "+ a ping flood from a laptop", 20, 400, INK))
    body.append(text(760, 414, "· governor:", 20, 400, INK))
    body.append(mono(880, 414, "performance", 21))
    return svg(1200, 452, body)


def runningmax():
    x0, x1, y0, y1 = 90, 1140, 330, 70
    sx = lambda m: x0 + (x1 - x0) * m / 5
    sy = lambda v: y0 - (y0 - y1) * v
    steps_load = [(0, 0.12), (0.05, 0.2), (0.3, 0.28), (1.4, 0.55), (3.6, 0.86), (5, 0.86)]
    steps_idle = [(0, 0.05), (0.1, 0.09), (2.2, 0.13), (5, 0.13)]
    def stairs(st):
        pts = []
        for (t, v), (t2, _) in zip(st, st[1:]):
            pts += [(sx(t), sy(v)), (sx(t2), sy(v))]
        return pts
    body = [line(x0, y0, x1 + 10, y0, MUTED, 2, arrow=True), line(x0, y0, x0, y1 - 20, MUTED, 2, arrow=True),
            text(x0 + 8, y1 - 26, "running max", 19, 400, MUTED),
            poly(stairs(steps_load), C[SAMP], 4), poly(stairs(steps_idle), MUTED, 3, dash="8 6"),
            text(sx(5) - 6, sy(0.86) - 14, "under load", 20, 700, C[SAMP], "end"),
            text(sx(5) - 6, sy(0.13) - 14, "idle", 20, 700, MUTED, "end")]
    for m in range(6):
        body.append(line(sx(m), y0, sx(m), y0 + 8, MUTED, 2))
        body.append(text(sx(m), y0 + 32, f"{m} min", 18, 400, MUTED, "middle"))
    body.append(line(sx(0.5), y0, sx(0.5), y1, C[CTRL], 2, "6 5"))
    body.append(text(sx(0.5) + 8, y1 + 20, "a 30 s run stops here", 18, 700, C[CTRL]))
    body.append(text(x0, y0 + 76, "The max only grows: rare collisions need time to happen, and load to happen at all.",
                     19, 400, INK))
    body.append(text(x1, y0 + 104, "schematic", 16, 400, MUTED, "end"))
    return svg(1200, 446, body)


def scale():
    x0, x1 = 360, 1150
    lo, hi = -1, 5  # log10 µs: 0.1 µs .. 100 ms
    sx = lambda us: x0 + (x1 - x0) * (math.log10(us) - lo) / (hi - lo)
    rows = [("MCU, week 8", "measured: max jitter", 0.25, 21, "0.25–21 µs", False),
            ("PREEMPT_RT, loaded", "you measure it today", 20, 300, "tens to hundreds of µs?", True),
            ("stock, loaded", "you measure it today", 50, 5000, "up to milliseconds?", True)]
    ya = 40 + 3 * 92 + 10
    xd = sx(10_000)
    body = [HATCH, line(xd, 26, xd, ya, C[CTRL], 3, "8 6"),
            text(xd, 20, "pump deadline: 10 ms", 18, 700, C[CTRL], "middle")]
    for i, (name, sub, a, b, lab, hatch) in enumerate(rows):
        y = 40 + i * 92
        body.append(text(x0 - 20, y + 28, name, 21, 700, INK, "end"))
        body.append(text(x0 - 20, y + 52, sub, 17, 400, MUTED, "end"))
        col = MUTED if hatch else C[SAMP]
        if hatch:
            body.append(rect(sx(a), y + 8, sx(b) - sx(a), 44, "url(#hatch)", MUTED, 2, 6, "6 5"))
        else:
            body.append(rect(sx(a), y + 8, sx(b) - sx(a), 44, T[SAMP], C[SAMP], 2, 6))
        body.append(rect(sx(b) + 6, y + 14, 10.4 * len(lab) + 12, 32, "#fff", "none", 0, 4))
        body.append(text(sx(b) + 12, y + 37, lab, 19, 700, col))
    body.append(line(x0, ya, x1, ya, MUTED, 2))
    for k, lab in zip(range(lo, hi + 1), ("0.1 µs", "1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "100 ms")):
        x = sx(10 ** k)
        body.append(line(x, ya, x, ya + 8, MUTED, 2))
        body.append(text(x, ya + 32, lab, 17, 400, MUTED, "middle"))
    body.append(text(40, ya + 74, "Log scale: each step is ×10. MCU row: ESP32-S3, 60 s runs, 2026-10-21.",
                     18, 400, MUTED))
    body.append(text(40, ya + 100, "Linux rows: expected ranges, until your table replaces them.", 18, 400, MUTED))
    return svg(1200, ya + 116, body)


def dfs():
    segs = [("IRQ entry", 100, ISR), ("scheduler", 110, None), ("switch", 80, None), ("thread", 130, CTRL)]
    body = [text(40, 40, "the same wake-up path, two governors", 20, 700, INK)]
    for r, (name, sub, k) in enumerate((("performance", "highest clock, always", 1.0),
                                        ("powersave", "lowest clock", 2.0))):
        y = 70 + r * 130
        body.append(text(40, y + 34, name, 22, 700, INK))
        body.append(text(40, y + 60, sub, 17, 400, MUTED))
        x = 260
        for lab, w, col in segs:
            ww = w * k
            body.append(cbox(x, y, ww, 70, lab, col, 17) if col else nbox(x, y, ww, 70, lab, 17))
            x += ww + 6
        end = x
        body.append(line(260, y + 86, end - 6, y + 86, INK, 3))
        if r == 0:
            body.append(text(end + 10, y + 92, "latency", 18, 700, INK))
        else:
            body.append(text(260, y + 114, "same instructions, slower clock: latency stretches", 18, 700, C[CTRL]))
    body.append(text(40, 386, "A governor that ramps the clock up mid-path adds the frequency switch itself.",
                     19, 400, INK))
    body.append(text(1160, 414, "schematic: stretched by f_max / f_min", 16, 400, MUTED, "end"))
    return svg(1200, 430, body)


def lab():
    body = [text(410, 44, "idle", 22, 800, MUTED, "middle"), text(810, 44, "under load", 22, 800, INK, "middle")]
    rows = [("stock", 64), ("PREEMPT_RT", 184)]
    for name, y in rows:
        body.append(text(196, y + 58, name, 22, 800, INK, "end"))
        for x, loaded in ((220, False), (620, True)):
            verdict = name == "PREEMPT_RT" and loaded
            col = C[CTRL] if verdict else MUTED
            body.append(rect(x, y, 380, 100, T[CTRL] if verdict else PANEL, col, 3 if verdict else 2, 12))
            body.append(text(x + 190, y + 46, "max ____ µs", 26, 700, INK, "middle"))
            body.append(text(x + 190, y + 78, "p99 ____ µs", 19, 400, MUTED, "middle"))
            if verdict:
                body.append(text(x + 392, y + 58, "the verdict for", 18, 700, C[CTRL]))
                body.append(text(x + 392, y + 82, "the pump loop", 18, 700, C[CTRL]))
    body.append(text(196, 360, "row 5", 22, 800, INK, "end"))
    body.append(rect(220, 304, 780, 100, "#fff", MUTED, 2, 12, "8 6"))
    body.append(text(610, 346, "PREEMPT_RT, loaded, powersave governor", 21, 700, INK, "middle"))
    body.append(text(610, 380, "max ____ µs: the DFS penalty", 19, 400, MUTED, "middle"))
    body.append(text(220, 444, "Every cell: cyclictest, 5 minutes. Predict all five before the first run.", 19, 400, INK))
    return svg(1200, 462, body)


def spinlock():
    """One core, two kernels: a low-priority driver holds a spinlock when the timer wakes you."""
    x0, unit = 250, 116
    sx = lambda t: x0 + unit * t
    body = []

    def lane_labels(y):
        body.append(text(x0 - 20, y + 28, "driver", 20, 700, INK, "end"))
        body.append(text(x0 - 20, y + 48, "low priority", 15, 400, MUTED, "end"))
        body.append(text(x0 - 20, y + 88, "your thread", 20, 700, C[CTRL], "end"))
        body.append(text(x0 - 20, y + 108, "FIFO 90", 15, 400, MUTED, "end"))

    def irq(y):
        body.append(line(sx(2), y - 24, sx(2), y + 60, C[ISR], 3, arrow=True))
        body.append(text(sx(2) + 10, y - 10, "timer IRQ: wakes you", 17, 700, C[ISR]))

    y = 76
    body.append(text(40, 30, "stock kernel, one core", 21, 800, INK))
    lane_labels(y)
    body.append(nbox(sx(0), y, unit - 4, 44, "driver code", 16))
    body.append(rect(sx(1), y, unit * 4.5 - 4, 44, MUTED, MUTED, 2, 10))
    body.append(text(sx(3.85), y + 28, "spinlock held: preemption off", 17, 700, "#fff", "middle"))
    irq(y)
    body.append(rect(sx(2), y + 64, unit * 3.5 - 4, 40, "#fff", C[CTRL], 2, 8, "8 6"))
    body.append(text(sx(3.75), y + 90, "runnable, but can't switch", 16, 700, C[CTRL], "middle"))
    body.append(cbox(sx(5.5), y + 64, unit * 2 - 4, 40, "runs", CTRL, 18))
    body.append(line(sx(2), y + 124, sx(5.5) - 4, y + 124, INK, 3))
    for xx in (sx(2), sx(5.5) - 4):
        body.append(line(xx, y + 116, xx, y + 132, INK, 3))
    body.append(text(sx(3.75), y + 152, "latency = the rest of someone else's critical section", 18, 700, INK, "middle"))

    y = 300
    body.append(text(40, y - 46, "PREEMPT_RT, one core", 21, 800, INK))
    lane_labels(y)
    body.append(nbox(sx(0), y, unit - 4, 44, "driver code", 16))
    body.append(ghost(sx(1), y, unit - 4, 44, "rtmutex", 16))
    body.append(line(sx(2), y + 22, sx(4.1), y + 22, GRID, 3, "3 6"))
    body.append(text(sx(3.05), y + 16, "preempted, lock still held", 15, 400, MUTED, "middle"))
    body.append(ghost(sx(4.1), y, unit * 2.4 - 4, 44, "rtmutex … unlock", 16))
    irq(y)
    body.append(cbox(sx(2.1), y + 64, unit * 2 - 4, 40, "runs", CTRL, 18))
    body.append(text(sx(4.4), y + 90, "latency: IRQ entry + a switch, µs", 18, 700, INK))

    body.append(text(40, 476, "spin_lock_irqsave() also masks interrupts: then even the timer IRQ waits for the unlock.",
                     18, 400, INK))
    body.append(text(40, 504, "If your thread needs that same lock, it sleeps and the driver inherits FIFO 90: week 6's PIP.",
                     18, 400, INK))
    return svg(1200, 520, body)


if __name__ == "__main__":
    figs = {"prt_hub.svg": hub, "prt_wakeup.svg": wakeup, "prt_spinlock.svg": spinlock, "prt_changes.svg": changes, "prt_ladder.svg": ladder,
            "prt_tradeoff.svg": tradeoff, "prt_measure.svg": measure, "prt_command.svg": command,
            "prt_runmax.svg": runningmax, "prt_scale.svg": scale, "prt_dfs.svg": dfs, "prt_lab.svg": lab}
    for name, fn in figs.items():
        save(HERE, name, fn())
    print(" ".join(figs))
