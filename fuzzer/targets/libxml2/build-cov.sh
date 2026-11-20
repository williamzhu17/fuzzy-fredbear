#!/usr/bin/env bash
# Build one libxml2 version for independent coverage measurement (as FuzzBench does): the
# library and the same fuzz/xml.c harness, compiled with Clang source-based coverage and linked
# with ../replay_main.c instead of the fuzzer.
#
#   ./build-cov.sh 2.15.0      -> build/2.15.0-cov/replay
#
# Score a set of inputs with scripts/coverage.py.
set -euo pipefail

VERSION=${1:?usage: build-cov.sh <version, e.g. 2.15.0>}
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$HERE/repo
OUT=$HERE/build/$VERSION-cov
JOBS=${SLURM_CPUS_PER_TASK:-4}

git -C "$REPO" rev-parse -q --verify "refs/tags/v$VERSION" >/dev/null || { echo "no tag v$VERSION" >&2; exit 1; }
rm -rf "$OUT"
mkdir -p "$OUT/src"
git -C "$REPO" archive "v$VERSION" | tar -x -C "$OUT/src"
SRC=$OUT/src
FLAGS="-O1 -g -fprofile-instr-generate -fcoverage-mapping"
(
    cd "$SRC"
    NOCONFIGURE=1 ./autogen.sh >/dev/null 2>&1
    CC=clang CFLAGS="$FLAGS" ./configure -q \
        --disable-shared --without-debug --without-http --without-python \
        --with-zlib --without-lzma >/dev/null
    make -s -j"$JOBS" libxml2.la >/dev/null
)
INC="-I$SRC/include -I$SRC"
clang $FLAGS $INC "$SRC/fuzz/xml.c" "$SRC/fuzz/fuzz.c" "$HERE/../replay_main.c" \
    "$SRC/.libs/libxml2.a" -lz -lm -o "$OUT/replay"
echo "built $OUT/replay"
