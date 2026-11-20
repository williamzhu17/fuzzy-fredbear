#!/usr/bin/env bash
# List the inherited corpus of a libxml2 transition: the union of the three base runs' queues.
#   scripts/inherited.sh 2.14.5   -> runs/xml/inherited-2.14.5.names (sorted unique file names,
#                                    read by run-trial.sh) and .paths (one path per name, read by
#                                    coverage.py)
# Queue file names are content hashes, so equal names are equal inputs.
set -euo pipefail
OLD=${1:?usage: inherited.sh <old version>}
R=runs/xml/base-$OLD
for i in 1 2 3; do
    ls "$R-$i/queue" | grep -v '^\.' | sed "s|^|$R-$i/queue/|"
done | awk -F/ '!seen[$NF]++' > "runs/xml/inherited-$OLD.paths"
sed 's|.*/||' "runs/xml/inherited-$OLD.paths" | sort > "runs/xml/inherited-$OLD.names"
wc -l "runs/xml/inherited-$OLD.names"
