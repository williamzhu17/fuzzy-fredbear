# fuzzy-fredbear: adaptive policy transfer for cross-version fuzzing

When a program moves from version *v* to *v+1*, should a fuzzer reuse the mutation-operator
preferences it learned on *v*, or start fresh? This project tests an adaptive controller that
weighs both options and detects when old experience has become misleading.

- **Stage 1: simulation (done).** A synthetic K-armed Bernoulli bandit stands in for mutation-operator
  families, so we control exactly how the program changes between versions. Lives in [`sim/`](sim/).
- **Stage 2: real fuzzing (in progress).** Real campaigns across several version transitions.
  The LibAFL fuzzer in [`fuzzer/`](fuzzer/) runs every policy end to end on a toy target; real
  targets are next.

> Work in progress. `sim/` is exploratory test code written before the real implementation.

## Start here

1. [`docs/PLAN.md`](docs/PLAN.md): the current project plan (v3): problem, controller, Stage 2 design.
2. [`sim/README.md`](sim/README.md): Stage 1 lab notebook. Read the **Bottom line** first, then
   **Overall conclusions** and **Proposed next steps**. The run log gives the exact command for every run.
3. [`sim/results/final/summary.md`](sim/results/final/summary.md): tables from the consolidated final sweep.
4. [`fuzzer/README.md`](fuzzer/README.md): the Stage 2 fuzzer: how to run a transition, policies,
   operator families, and its next steps.

## Layout

```
.
├── README.md             this file
├── requirements.txt      pinned Python dependencies
├── docs/
│   ├── PLAN.md           current project plan (v3)
│   └── archive/
│       └── PLAN_v2.md    plan before the Stage 1 simulation
├── fuzzer/               Stage 2 LibAFL fuzzer (Rust); see fuzzer/README.md
└── sim/                  Stage 1 simulation
    ├── README.md         model, policies, scenarios, run log and findings
    ├── bandit_sim.py     simulator core: scenarios, priors, policies, statistics
    ├── run_stage1.py     scenario × policy grid driver
    ├── rank_sweep.py     rank-correlation sweep
    ├── final_sweep.py    consolidated final sweep (resumable)
    ├── final_report.py   analysis of the final sweep
    ├── compare_table.py  compact tables from a results dir
    ├── power_check.py    power at Stage 2 trial counts
    ├── run_next.sh       commands for runs 6–10
    └── results/<run>/    one folder per run: summary.md (plots, raw.pkl and logs are git-ignored)
```

## Setup

Requires Python 3.12 (other 3.10+ versions probably work).

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Running

Scripts read and write paths relative to `sim/`, whatever directory you start in. Examples:

```bash
cd sim
# quick grid (run 1: 4 scenarios, about 4 min on 8 processes)
../.venv/bin/python run_stage1.py --R 30 --T 1000000 --out results/original

# consolidated final sweep (about 90 min on 8 processes; resumes if interrupted), then its report
../.venv/bin/python final_sweep.py --out results/final
../.venv/bin/python final_report.py results/final --reps 2000
```

Most drivers take `--jobs` (default 8) for the number of worker processes.

## Data

Only each run's `results/<run>/summary.md` is committed; it has every table. Not committed:
the full per-trial `raw.pkl` files (about 1.2 GB), the plots (`*.png`, about 15 MB) and run logs
(`*.log`). Every script regenerates its plots when it runs, and `rank_sweep.py --replot` redraws
from an existing `raw.pkl`. To rerun an
analysis script or get the plots for an existing run, either regenerate that run (command in `sim/README.md`) or
get the pickles from a teammate (shared drive).
