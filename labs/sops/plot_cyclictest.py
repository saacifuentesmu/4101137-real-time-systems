#!/usr/bin/env python3
"""Overlay cyclictest histograms (files produced with -h <us> -q)."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse(path):
    lats, counts, maxes = [], [], []
    with open(path) as f:
        for line in f:
            if line.startswith("# Max Latencies:"):
                maxes = [int(x) for x in line.split(":")[1].split()]
            elif line[:1].isdigit():
                cols = line.split()
                lats.append(int(cols[0]))
                counts.append(sum(int(c) for c in cols[1:]))
    if not lats:
        sys.exit(f"{path}: no histogram found (run cyclictest with -h <us> -q)")
    return lats, counts, max(maxes) if maxes else None


def main():
    files = sys.argv[1:]
    if not files:
        sys.exit("usage: plot_cyclictest.py run1.txt [run2.txt ...]")
    fig, ax = plt.subplots(figsize=(9, 5))
    for path in files:
        lats, counts, lat_max = parse(path)
        label = path.rsplit("/", 1)[-1].removesuffix(".txt")
        if lat_max is not None:
            label += f" (max {lat_max} µs)"
        ax.step(lats, counts, where="mid", label=label)
    ax.set_yscale("log")
    ax.set_xlabel("latency (µs)")
    ax.set_ylabel("samples")
    ax.set_title("cyclictest wake-up latency")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig("cyclictest.png", dpi=150)
    print("wrote cyclictest.png")


if __name__ == "__main__":
    main()
