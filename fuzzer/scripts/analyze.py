#!/usr/bin/env python3
"""Compare policies on the three outcomes of a main run.

    scripts/analyze.py runs/xml/main

Outcomes per trial (gains over the trial's own t = 0, at --t seconds, wall-clock):
  branches  independent branch coverage (coverage-llvm.csv from scripts/coverage.py)  [primary]
  edges     fredbear's own edge count (<trial>/coverage.csv)
  inputs    new corpus inputs (<trial>/coverage.csv corpus column; equals the files in new/)

Comparisons, fixed before the main run was analysed (Nov 17, 2026):
  adaptive vs transfer, adaptive vs uniform, transfer vs fresh.
Each uses a two-sided Mann-Whitney U test (normal approximation with tie correction) and the
Vargha-Delaney A12 effect size (P(first > second) + 0.5 P(tie)), Holm-corrected across the three
comparisons within each outcome. Other pairs are printed as exploratory, uncorrected.
"""
import argparse
import csv
import glob
import math
import os
import statistics
from collections import defaultdict
from itertools import combinations

PLANNED = [("adaptive", "transfer"), ("adaptive", "uniform"), ("transfer", "fresh")]


def mann_whitney(x, y):
    """Two-sided p-value, normal approximation with tie and continuity correction."""
    n1, n2 = len(x), len(y)
    allv = sorted((v, i) for i, v in enumerate(x + y))
    ranks = [0.0] * (n1 + n2)
    i, ties = 0, 0.0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[allv[k][1]] = r
        t = j - i + 1
        ties += t ** 3 - t
        i = j + 1
    u1 = sum(ranks[:n1]) - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    n = n1 + n2
    var = n1 * n2 / 12 * ((n + 1) - ties / (n * (n - 1)))
    if var == 0:
        return 1.0
    z = (abs(u1 - mu) - 0.5) / math.sqrt(var)
    return min(1.0, math.erfc(max(z, 0) / math.sqrt(2)))


def a12(x, y):
    return sum((a > b) + 0.5 * (a == b) for a in x for b in y) / (len(x) * len(y))


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj


def at_time(rows, t, col):
    """Value of column col in the last coverage.csv row with time <= t."""
    best = rows[0]
    for r in rows:
        if float(r["t"]) <= t + 0.5:
            best = r
    return float(best[col])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--t", type=int, default=900)
    a = ap.parse_args()

    data = defaultdict(lambda: defaultdict(list))  # outcome -> policy -> values
    llvm = defaultdict(dict)
    llvm_path = os.path.join(a.root, "coverage-llvm.csv")
    if os.path.exists(llvm_path):
        for r in csv.DictReader(open(llvm_path)):
            llvm[r["trial"]][int(r["t"])] = int(r["branches_covered"])
    for trial in sorted(glob.glob(os.path.join(a.root, "*-[0-9]*/"))):
        name = os.path.basename(trial.rstrip("/"))
        policy = name.rsplit("-", 1)[0]
        rows = list(csv.DictReader(open(os.path.join(trial, "coverage.csv"))))
        data["edges"][policy].append(at_time(rows, a.t, "edges") - float(rows[0]["edges"]))
        data["inputs"][policy].append(at_time(rows, a.t, "corpus") - float(rows[0]["corpus"]))
        if name in llvm and a.t in llvm[name]:
            data["branches"][policy].append(llvm[name][a.t] - llvm[name][0])

    for outcome in ("branches", "edges", "inputs"):
        pols = data[outcome]
        if not pols:
            print(f"\n## {outcome}: no data")
            continue
        print(f"\n## {outcome} gained by t = {a.t} s")
        print(f"{'policy':10s} {'n':>3s} {'mean':>8s} {'median':>8s} {'sd':>7s} {'min':>6s} {'max':>6s}")
        for p in ("uniform", "fresh", "transfer", "adaptive", "dts"):
            v = pols.get(p)
            if v:
                sd = statistics.stdev(v) if len(v) > 1 else 0.0
                print(f"{p:10s} {len(v):3d} {statistics.mean(v):8.1f} {statistics.median(v):8.1f} "
                      f"{sd:7.1f} {min(v):6.0f} {max(v):6.0f}")
        planned = [(x, y) for x, y in PLANNED if x in pols and y in pols]
        ps = [mann_whitney(pols[x], pols[y]) for x, y in planned]
        print("planned (Holm across these):")
        for (x, y), p, ph in zip(planned, ps, holm(ps)):
            print(f"  {x:9s} vs {y:9s} A12 = {a12(pols[x], pols[y]):.2f}  p = {p:.4f}  Holm p = {ph:.4f}")
        print("exploratory (uncorrected):")
        for x, y in combinations(sorted(pols), 2):
            if (x, y) in PLANNED or (y, x) in PLANNED:
                continue
            print(f"  {x:9s} vs {y:9s} A12 = {a12(pols[x], pols[y]):.2f}  p = {mann_whitney(pols[x], pols[y]):.4f}")


if __name__ == "__main__":
    main()
