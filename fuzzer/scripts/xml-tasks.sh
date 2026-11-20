#!/usr/bin/env bash
# Print one trial command per line for a libxml2 transition OLD -> NEW (default 2.14.6 -> 2.15.0).
#   [OLD=2.14.5 NEW=2.14.6 EXTRA="..."] scripts/xml-tasks.sh <out root> <secs> <seeds, e.g. "1 2 3"> <policies...>
# Needs runs/xml/base-$OLD-{1,2,3} (base runs) and runs/xml/inherited-$OLD.names
# (scripts/inherited.sh). Seeds are the outer loop so every wave of a pack job mixes all policies.
ROOT=$1; SECS=$2; SEEDS=$3; shift 3
EXTRA=${EXTRA:-}   # extra fredbear flags for every trial, e.g. EXTRA="--base-from 1800"
OLD=${OLD:-2.14.6}; NEW=${NEW:-2.15.0}
R=runs/xml/base-$OLD; B=targets/libxml2/build/$NEW
for s in $SEEDS; do for pol in "$@"; do
  out=$ROOT/$pol-$s
  echo "scripts/run-trial.sh $out runs/xml/inherited-$OLD.names $B/fredbear --target harness --policy $pol --cap-n 10000 --base-log $R-1/batches.jsonl $R-2/batches.jsonl $R-3/batches.jsonl --corpus $R-1/queue $R-2/queue $R-3/queue --dict $B/xml.dict --secs $SECS --seed $s${EXTRA:+ $EXTRA}"
done; done
