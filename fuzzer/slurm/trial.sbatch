#!/usr/bin/env bash
# One fuzzing trial on one CPU. Every argument is the command to run, usually a fredbear binary
# plus its flags:
#
#   sbatch slurm/trial.sbatch targets/libpng/build/1.6.46/fredbear --target harness \
#       --policy adaptive --base-log runs/base-1.6.45/batches.jsonl \
#       --corpus runs/base-1.6.45/queue --dict targets/libpng/build/1.6.46/png.dict \
#       --secs 3600 --seed 1 --out runs/1.6.46-adaptive-1
#
# Relative paths resolve against the directory you ran sbatch from (submit from fuzzer/).
# Override any #SBATCH line on the command line, e.g. sbatch -t 3:00:00 slurm/trial.sbatch ...
# Set the time limit a few minutes above --secs: loading the corpus and writing it out take time too.
#SBATCH --job-name=fredbear
#SBATCH --partition=interactive
#SBATCH --qos=interactive
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:10:00
#SBATCH --output=slurm-logs/%x-%j.out
set -euo pipefail
echo "job $SLURM_JOB_ID on $(hostname) at $(date -Is)"
echo "cmd: $*"
"$@"
echo "done at $(date -Is)"
