#!/usr/bin/env bash
# Run one fredbear trial in node-local scratch, then copy back only what the analysis needs.
#
#   scripts/run-trial.sh <out dir> <inherited names file> <fredbear command without --out ...>
#
# Why: every trial on v+1 copies the whole inherited corpus into its queue/ (about 280 MB for
# libxml2). Writing that to NFS from 16 trials at once stalled each trial for minutes before
# fuzzing started. So the trial runs with --out in $TMPDIR (node-local, deleted when the job
# ends), and afterwards <out dir> gets:
#   coverage.csv, batches.jsonl, start_epoch (written by fredbear at t = 0), crashes/
#   new/      the trial's own new inputs: queue/ names not in the inherited names file, mtimes kept
#   time.txt  /usr/bin/time -v output (peak memory: "Maximum resident set size")
set -uo pipefail
OUT=$1; INHERITED=$2; shift 2
if [ -e "$OUT" ]; then echo "error: $OUT already exists" >&2; exit 1; fi
LOCAL=$(mktemp -d "${TMPDIR:-/tmp}/fredbear.XXXXXX")
trap 'rm -rf "$LOCAL"' EXIT
/usr/bin/time -v -o "$LOCAL/time.txt" "$@" --out "$LOCAL/run"
STATUS=$?
mkdir -p "$OUT/new"
for f in coverage.csv batches.jsonl start_epoch crashes; do
    [ -e "$LOCAL/run/$f" ] && cp -rp "$LOCAL/run/$f" "$OUT/"
done
cp "$LOCAL/time.txt" "$OUT/"
if [ -d "$LOCAL/run/queue" ]; then
    comm -23 <(ls "$LOCAL/run/queue" | grep -v '^\.' | sort) "$INHERITED" |
        while read -r f; do cp -p "$LOCAL/run/queue/$f" "$OUT/new/"; done
fi
exit $STATUS
