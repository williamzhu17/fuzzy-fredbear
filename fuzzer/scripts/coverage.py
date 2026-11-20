#!/usr/bin/env python3
"""Independent coverage of fuzzing trials, measured as FuzzBench does: replay the corpus on a
separate build compiled with Clang source-based coverage, then read llvm-cov's totals.

    scripts/coverage.py --replay targets/libxml2/build/2.15.0-cov/replay \\
        --inherited runs/xml/inherited-2.14.6.paths --out runs/xml/main/coverage-llvm.csv \\
        runs/xml/main/*-*/

Each trial's corpus at time t is the inherited corpus plus the trial's new inputs (<trial>/new/,
written by scripts/run-trial.sh) whose mtime is at most t seconds after <trial>/start_epoch.
The inherited corpus is replayed once and its profile merged into every trial's, which gives the
coverage of the union (profile counts add). Harness files (fuzz/) are excluded from the totals.

Output: one row per trial and time, with covered and total branches, lines, regions, functions.
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
from multiprocessing import Pool

PROFDATA = "llvm-profdata-18"
COV = "llvm-cov-18"
IGNORE = r"fuzz/|replay_main"


def replay(binary, paths, profraw):
    env = dict(os.environ, LLVM_PROFILE_FILE=profraw)
    subprocess.run([binary], input="\n".join(paths) + "\n", text=True, env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def totals(binary, profdata):
    out = subprocess.run([COV, "export", "-summary-only", f"-ignore-filename-regex={IGNORE}",
                          f"-instr-profile={profdata}", binary],
                         capture_output=True, text=True, check=True).stdout
    t = json.loads(out)["data"][0]["totals"]
    return {k: (t[k]["covered"], t[k]["count"]) for k in ("branches", "lines", "regions", "functions")}


def score(job):
    binary, base_profdata, trial, times = job
    start = float(open(os.path.join(trial, "start_epoch")).read())
    new_dir = os.path.join(trial, "new")
    files = []
    if os.path.isdir(new_dir):
        for f in os.listdir(new_dir):
            p = os.path.join(new_dir, f)
            files.append((os.path.getmtime(p) - start, p))
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for t in times:
            paths = [p for (dt, p) in files if dt <= t]
            merged = os.path.join(tmp, f"{t}.profdata")
            if paths:
                raw = os.path.join(tmp, f"{t}.profraw")
                replay(binary, paths, raw)
                subprocess.run([PROFDATA, "merge", "-sparse", base_profdata, raw, "-o", merged], check=True)
            else:
                merged = base_profdata
            tot = totals(binary, merged)
            row = {"trial": os.path.basename(trial.rstrip("/")), "t": t, "new_inputs": len(paths)}
            for k, (cov, cnt) in tot.items():
                row[f"{k}_covered"], row[f"{k}_total"] = cov, cnt
            rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", required=True)
    ap.add_argument("--inherited", required=True, help="file with one inherited input path per line")
    ap.add_argument("--out", required=True)
    ap.add_argument("--times", default="0,300,600,900")
    ap.add_argument("--jobs", type=int, default=int(os.environ.get("SLURM_CPUS_PER_TASK", 4)))
    ap.add_argument("trials", nargs="+")
    a = ap.parse_args()
    times = [int(x) for x in a.times.split(",")]

    base = os.path.splitext(a.inherited)[0] + ".profdata"
    if not os.path.exists(base) or os.path.getmtime(base) < os.path.getmtime(a.replay):
        paths = [l.strip() for l in open(a.inherited) if l.strip()]
        with tempfile.TemporaryDirectory() as tmp:
            raw = os.path.join(tmp, "inherited.profraw")
            replay(a.replay, paths, raw)
            subprocess.run([PROFDATA, "merge", "-sparse", raw, "-o", base], check=True)
        print(f"inherited corpus: {len(paths)} inputs -> {base}", file=sys.stderr)

    jobs = [(a.replay, base, t, times) for t in a.trials]
    with Pool(a.jobs) as pool:
        rows = [r for rs in pool.map(score, jobs) for r in rs]
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
