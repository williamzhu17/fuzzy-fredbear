# Running jobs on FarmShare (Slurm)

> **Scope: Stanford FarmShare compute nodes only.** Everything in this file (partitions, limits,
> the Rust toolchain path, the C++ header fix, the job scripts in `fuzzer/slurm/`) is specific
> to FarmShare's Slurm cluster and its Ubuntu 24.04 compute nodes. It does not apply to a laptop
> (see [`fuzzer/README.md`](../fuzzer/README.md) for the macOS setup) or to other clusters.

How to build the fuzzer and run fuzzing campaigns on FarmShare compute nodes through Slurm.
Everything here was tested on Nov 16, 2026, submitting from an OnDemand desktop on `iron-01`;
the jobs ran on FarmShare `iron` compute nodes. FarmShare's own docs:
<https://docs.farmshare.stanford.edu/docs/slurm/>.

## TL;DR

```bash
cd ~/cs238/fuzzy-fredbear/fuzzer
mkdir -p slurm-logs                       # sbatch won't create the log directory itself
# From an OnDemand desktop, always submit through slurm/fresh (see the gotcha below).

# One trial (1 CPU). Arguments after the script are the command to run.
slurm/fresh sbatch -t 01:10:00 slurm/trial.sbatch ./targets/libpng/build/1.6.45/fredbear --target harness \
    --policy uniform --corpus targets/libpng/build/1.6.45/seeds \
    --dict targets/libpng/build/1.6.45/png.dict --secs 3600 --out runs/base-1.6.45

# Many trials packed into one 16-CPU job (one command per line in tasks.txt)
slurm/fresh sbatch -c 16 --mem=64G -t 02:30:00 slurm/pack.sbatch tasks.txt

squeue -a -u $USER                        # -a matters: the interactive partition is hidden
```

## Where you are

- FarmShare has login nodes (`rice`, reached with `ssh <sunetid>@login.farmshare.stanford.edu`
  or through OnDemand at <https://ondemand.farmshare.stanford.edu/>) and compute nodes (`barley`,
  `rye` with extra memory, `oat` with GPUs, `wheat`, and `iron` for specific workloads). You can
  reach compute nodes only by submitting Slurm jobs.
- The login nodes allow some real work, but FarmShare enforces unpublished limits there. A fuzzer
  pegs a core for hours, so always run builds and trials on compute nodes.
- If you work from an **OnDemand desktop**, you are already inside a Slurm job (on an `iron`
  node, partition `caddyshack`, **1 CPU**). Check with `echo $SLURM_JOB_ID`. That desktop is
  not a place to fuzz either: everything you start there shares its one CPU.

## Storage

From <https://docs.farmshare.stanford.edu/docs/storage/>, plus what this account has used so far:

| Path | Seen by | Limit | Use for |
|---|---|---|---|
| `~` (`/home/users/$USER`) | every node (NFS) | **50 GB quota**, short-term backups | Code, the toolchain (~0.3 GB), built fuzzers, results we keep. About 15 GB was in use on Nov 16. |
| `/scratch/users/$USER` | every node (NFS) | **files not modified for 90 days are purged** | Bulky campaign outputs (`queue/`, `crashes/`) while a study is in progress |
| `/tmp` | one node only | per job, **deleted when the job ends** | Nothing here; a trial's outputs would vanish |

- Keep job inputs and outputs on `/home` or `/scratch` so every node sees them. A trial writing
  to `/tmp` loses its outputs when the job ends.
- Fuzzer corpora are small (the 60 s test run's queue was about 500 files), but hundreds of trials
  add up. If `~` gets close to 50 GB, point `--out` at `/scratch/users/$USER/fredbear/...` and copy
  back only what you keep (`coverage.csv`, `batches.jsonl`, the base runs' `queue/`). Check usage
  with `du -sh ~/cs238 /scratch/users/$USER`.
- Each trial on v+1 copies its whole inherited corpus into its own `queue/`. With three base
  queues merged that is about 60 MB per trial, so 360 main-run trials come to about 22 GB. Point
  the main runs' `--out` at `/scratch`, or delete each trial's `queue/` once it finishes: the
  analysis needs only `coverage.csv` and `batches.jsonl`, and only base-run queues get reused.

## Gotcha: submitting from inside a job (OnDemand desktop)

The desktop job leaves `SLURM_*` variables in your shell. They break `srun`, and they can break
`sbatch` jobs too:

- A plain `srun ...` tries to start a *step inside the desktop job* instead of a new job. It warns
  `--cpus-per-task value exceeds that of job (2 > 1)` and then hangs forever.
- Unsetting only `SLURM_JOB_ID` gets you a new job, but the inherited `SLURM_EXPORT_ENV=NONE`
  starts it with an empty `PATH`: `execve(): bash: No such file or directory`.
- A plain `sbatch` submits and starts normally, but the job runs with the desktop's variables.
  On Nov 16 a build job submitted this way failed with exit code 2 and no error message. It
  failed in libpng's configure step, which hides its stderr. The same build submitted through
  `slurm/fresh` succeeded twice. Which variable is responsible is still unknown. Simple trials
  and the smoke tests worked without `fresh`, so the failure doesn't show up every time.

Fix: submit **every** `srun` and `sbatch` through `fuzzer/slurm/fresh`, which removes every
`SLURM_*` variable. Outside a job (an ssh shell on a login node) it changes nothing, so using it
everywhere is safe. All examples in this guide do.

```bash
slurm/fresh srun -n 1 -p interactive -q interactive -c 4 --mem=8G -t 1:00:00 --pty bash   # interactive shell
slurm/fresh srun -n 1 -p interactive -q interactive -c 8 --mem=16G -t 0:30:00 cargo build --release
slurm/fresh sbatch slurm/trial.sbatch ...
```

**Always pass `-n 1` to `srun`.** On Nov 17, `slurm/fresh srun -c 1 ... fredbear ...` started *two*
copies of the command. One created `--out` and the other failed with "already exists". `-n 1`
fixed it. `sbatch` scripts are not affected: their body runs once.

**Use a new `--out` name after deleting one on another node.** After a compute node created
`runs/x` and it was deleted from the desktop, a new job on that node still saw `runs/x` for a
while, probably because of NFS attribute caching, and `fredbear` refused it. A different name
avoids the problem.

`squeue`/`sacct`/`scancel` are unaffected. Inside an sbatch script, `srun` is fine because Slurm
sets that job's own variables.

If a job submitted with `--dependency=afterok:<id>` waits on a job that fails, Slurm cancels it
automatically (state `CANCELLED`, elapsed `00:00:00`). Resubmit it once the first job is fixed.

## Partitions and limits (this account, `operator`)

FarmShare's docs name the partitions and QOS but give no numbers. The numbers below come from
`sacctmgr show qos` and `scontrol show partition` on Nov 16, 2026, and can change. Recheck with
`sacctmgr -n -P show qos format=name,maxtrespu,maxjobspu,maxsubmitpu,maxwall`. The docs' QOS table
reads as if `-q interactive` goes with `-p normal`, but `-p interactive -q interactive` is the
pairing tested here (and the one the docs' own `salloc` example uses).

| Partition / QOS | Nodes | Per-user limits | Max time | Use for |
|---|---|---|---|---|
| `-p interactive -q interactive` (hidden) | iron-[01-15], wheat, oat | **16 CPUs, 64 GB, 4 jobs** | 1 day | **Default for us.** Started within seconds every time today. |
| `-p normal` (default) | barley, rye, wheat, oat | 512 CPUs, 128 running jobs | 2 days (2 h default) | Big sweeps, if you can wait. **Full today**: test submissions were estimated to start 5 days later. |
| `-p normal -q long` | same as normal | 128 CPUs, 4 running jobs | 7 days | Campaigns longer than 2 days. |
| `caddyshack` (hidden) | iron | 8 CPUs, **1 job** | 90 days | Taken by the OnDemand desktop. Don't use. |

- Memory per CPU is capped at 4000 MB (2400 MB default). Asking for more `--mem` than
  `4000 MB × CPUs` does not fail: Slurm quietly raises the CPU count (`-c 2 --mem=8G` gets 3 CPUs).
- FarmShare's docs warn that some nodes hand out 2 CPUs per request because of hyperthreading.
  That is harmless for us: it only leaves an idle hyperthread beside each trial.
- Hidden partitions don't show in plain `squeue`/`sinfo`. Use `squeue -a -u $USER` and `sinfo -a`.
- An OnDemand desktop in `caddyshack` does not count against the interactive limits, but desktops
  started in `interactive` do. Check `squeue -a -u $USER` before planning a 16-CPU job.
- To see what is free right now: `sinfo -a -o "%P %C"` (CPUs allocated/idle/other/total). To get
  a start estimate without submitting: `sbatch --test-only <same flags> script`.
- Array jobs (`--array`, max size 1024) work on `normal`. On `interactive` each array task counts
  as one of your 4 jobs, so use `pack.sbatch` there instead.

## One-time setup on FarmShare: Rust toolchain

LibAFL 0.16.1 needs rustc ≥ 1.93.1. The system `rustc` is 1.75, and the newest module
(`module load rust/1.86.0`) is also too old. So rustup is installed in your home directory
(`~/.rustup`, `~/.cargo`; installed with `--no-modify-path`, so no shell rc file was changed):

```bash
export PATH=$HOME/.cargo/bin:$PATH        # add to ~/.bashrc if you like; every job script needs it
rustc --version                           # 1.100.0 when installed
```

The system `clang` 18, `ar` and zlib are used for libpng. FarmShare compute nodes can reach
GitHub, so `build.sh` can clone libpng inside a job.

**C++ headers:** on FarmShare's Ubuntu 24.04 nodes, `clang++` picks GCC 14 but only GCC 13's
libstdc++ headers are installed, so the libpng harness fails with `'vector' file not found`.
Point clang at the GCC 13 headers before running `build.sh`:

```bash
export CPLUS_INCLUDE_PATH=/usr/include/c++/13:/usr/include/x86_64-linux-gnu/c++/13
```

## Building on a FarmShare compute node (in a job, not on the login node)

```bash
cd ~/cs238/fuzzy-fredbear/fuzzer
cat > slurm-logs/build.sbatch <<'EOF'
#!/usr/bin/env bash
#SBATCH -J fredbear-build -p interactive -q interactive -c 8 --mem=16G -t 00:45:00
#SBATCH -o slurm-logs/%x-%j.out
set -euo pipefail
export PATH=$HOME/.cargo/bin:$PATH
export CPLUS_INCLUDE_PATH=/usr/include/c++/13:/usr/include/x86_64-linux-gnu/c++/13
cargo build --release
./targets/libpng/build.sh 1.6.45
./targets/libpng/build.sh 1.6.46
EOF
slurm/fresh sbatch slurm-logs/build.sbatch
```

Tested: a clean Rust build takes about 45 s on 8 CPUs, and each libpng version about 10 s more.
All five plan versions (1.6.39, 1.6.40, 1.6.45, 1.6.46, 1.6.47) build and run on Linux. The binaries are self-contained, so trials need
neither the toolchain nor `CPLUS_INCLUDE_PATH`.

Smoke test (Nov 16): a 60 s uniform base run on 1.6.45 through `trial.sbatch`, then `adaptive`
and `fresh` 30 s trials on 1.6.46 through `pack.sbatch` (chained with
`--dependency=afterok:<jobid>`). All three finished and reached about 1,240 edges, at roughly
70–85k executions per second per trial.

## Running trials

The fuzzer is single-process and single-threaded, so **one trial = one CPU**. Give each trial
about 2–4 GB.

### One trial per job: `slurm/trial.sbatch`

Defaults: interactive partition, 1 CPU, 4 GB, 1 h 10 min. Everything after the script name is the
command. Submit from `fuzzer/` so relative paths work, and override any default on the command
line (flags before the script name win over the `#SBATCH` lines):

```bash
slurm/fresh sbatch -t 04:10:00 -J v46-adaptive-1 slurm/trial.sbatch ./targets/libpng/build/1.6.46/fredbear \
    --target harness --policy adaptive --base-log runs/base-1.6.45/batches.jsonl \
    --corpus runs/base-1.6.45/queue --dict targets/libpng/build/1.6.46/png.dict \
    --secs 14400 --seed 1 --out runs/1.6.46-adaptive-1
```

At most 4 of these run at once on `interactive`; the rest wait (`QOSMaxJobsPerUserLimit`) and
start as earlier ones finish. For more parallelism use `pack.sbatch`.

### Many trials per job: `slurm/pack.sbatch`

Takes a file with one command per line and runs as many at a time as the job has CPUs. One 16-CPU
job uses the whole interactive allowance in one job slot. Each command's output goes to
`slurm-logs/<jobid>/<line>.log`, and the job log lists `ok`/`FAIL` per line.

```bash
# 16 trials: 8 seeds × 2 policies on 1.6.46, all from the same base run
B=./targets/libpng/build/1.6.46/fredbear
for pol in adaptive fresh; do for s in $(seq 1 8); do
  echo "$B --target harness --policy $pol --base-log runs/base-1.6.45/batches.jsonl --corpus runs/base-1.6.45/queue --dict targets/libpng/build/1.6.46/png.dict --secs 3600 --seed $s --out runs/1.6.46-$pol-$s"
done; done > tasks.txt
slurm/fresh sbatch -c 16 --mem=64G -t 01:15:00 slurm/pack.sbatch tasks.txt
```

The time limit has to cover every wave: `ceil(tasks / CPUs) × per-trial time`, plus a few
minutes. With 32 tasks on 16 CPUs and `--secs 3600`, ask for about 2 h 15 min.

**Rerunning after a failure:** `fredbear` refuses an `--out` directory that already exists. Delete
the partial `runs/...` directories of failed or killed trials before resubmitting them.

Chain a base run and its trials with a dependency, so the trials wait for the base corpus:

```bash
base=$(slurm/fresh sbatch --parsable -t 01:10:00 slurm/trial.sbatch ...base-run command...)
slurm/fresh sbatch --dependency=afterok:$base -c 16 --mem=64G -t 01:15:00 slurm/pack.sbatch tasks.txt
```

### Large sweeps on `normal`

When `normal` has room, an array job is the simplest way to fan out (each task gets one line of
`tasks.txt`; `%32` caps how many run at once):

```bash
cat > slurm-logs/array.sbatch <<'EOF'
#!/usr/bin/env bash
#SBATCH -J fredbear-array -p normal -c 1 --mem=4G -t 01:10:00
#SBATCH -o slurm-logs/%x-%A_%a.out
set -euo pipefail
cmd=$(grep -vE '^[[:space:]]*(#|$)' "$1" | sed -n "$((SLURM_ARRAY_TASK_ID + 1))p")
echo "$cmd"; bash -c "$cmd"
EOF
slurm/fresh sbatch --array=0-$(($(grep -cvE '^[[:space:]]*(#|$)' tasks.txt) - 1))%32 slurm-logs/array.sbatch tasks.txt
```

Check the queue first (`sbatch --test-only ...`). On Nov 16 the estimated start was days away.

## Monitoring and cleanup

```bash
squeue -a -u $USER                               # your jobs, including hidden partitions
squeue -a -u $USER --start                       # estimated start times of pending jobs
sacct -X -u $USER -S today --format=jobid,jobname%25,partition,state,elapsed,maxrss,nodelist
tail -f slurm-logs/fredbear-pack-<jobid>.out     # per-task progress of a pack job
tail -n 3 runs/<trial>/coverage.csv              # a live trial's latest t,execs,corpus,edges
scancel <jobid>                                  # never cancel the sys/dashboard/... desktop job
seff <jobid>                                     # CPU and memory efficiency after a job ends
```

A job that hits its time limit is killed with no clean shutdown. The last `coverage.csv` row still
says how far it got, but treat that trial as incomplete. Set `-t` comfortably above `--secs`.

## Files

| File | Purpose |
|---|---|
| `fuzzer/slurm/fresh` | Run a command with `SLURM_*` cleared (use for every `srun`/`sbatch` from an OnDemand desktop) |
| `fuzzer/slurm/trial.sbatch` | One trial in one 1-CPU job |
| `fuzzer/slurm/pack.sbatch` | Many 1-CPU trials inside one multi-CPU job |
| `fuzzer/slurm-logs/` | Job logs (git-ignored) |
