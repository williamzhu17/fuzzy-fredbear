#!/usr/bin/env bash
# Run many single-CPU trials inside one job: as many at a time as the job has CPUs.
# TASKS is a file with one shell command per line (blank lines and # comments are skipped):
#
#   sbatch -c 16 --mem=64G -t 05:00:00 slurm/pack.sbatch tasks.txt
#
# Each command's output goes to slurm-logs/<job id>/<line number>.log. Use this to fit more than
# 4 trials into the interactive QOS (4 jobs, 16 CPUs, 64 GB per user). The job's time limit has to
# cover the longest wave: ceil(#tasks / CPUs) * per-trial time.
#SBATCH --job-name=fredbear-pack
#SBATCH --partition=interactive
#SBATCH --qos=interactive
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=01:10:00
#SBATCH --output=slurm-logs/%x-%j.out
set -euo pipefail
TASKS=${1:?usage: sbatch slurm/pack.sbatch <tasks file>}
LOGS=slurm-logs/$SLURM_JOB_ID
mkdir -p "$LOGS"
echo "job $SLURM_JOB_ID on $(hostname): $SLURM_CPUS_PER_TASK at a time from $TASKS"
# Number the commands, then run them $SLURM_CPUS_PER_TASK at a time.
grep -vnE '^[[:space:]]*(#|$)' "$TASKS" | tr '\n' '\0' |
    xargs -0 -P "$SLURM_CPUS_PER_TASK" -I{} bash -c '
        n=${1%%:*}; cmd=${1#*:}
        echo "start $n: $cmd"
        if bash -c "$cmd" > "$2/$n.log" 2>&1; then echo "ok    $n"; else echo "FAIL  $n (exit $?)"; fi
    ' _ {} "$LOGS"
echo "all done at $(date -Is)"
