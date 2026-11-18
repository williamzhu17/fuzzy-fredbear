#!/usr/bin/env bash
# Build one libpng version into a fuzzer binary with SanitizerCoverage.
#
#   ./build.sh 1.6.40
#
# Produces build/<version>/: fredbear (the fuzzer), png.dict, seeds/ (PngSuite images).
# Every version uses its own tag's OSS-Fuzz harness; pick transitions where it is unchanged
# (see fuzzer/README.md) so only the library differs.
set -euo pipefail

VERSION=${1:?usage: build.sh <version, e.g. 1.6.40>}
HERE=$(cd "$(dirname "$0")" && pwd)
FUZZER=$(cd "$HERE/../.." && pwd)
REPO=$HERE/repo
OUT=$HERE/build/$VERSION

[ -d "$REPO" ] || git clone -q https://github.com/pnggroup/libpng.git "$REPO"
if ! git -C "$REPO" rev-parse -q --verify "refs/tags/v$VERSION" >/dev/null; then
    echo "error: no tag v$VERSION in $REPO" >&2
    exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT/src" "$OUT/obj" "$OUT/seeds"
git -C "$REPO" archive "v$VERSION" | tar -x -C "$OUT/src"

# Same configuration as libpng's contrib/oss-fuzz/build.sh: stdio and write support off. Without
# stdio, libpng cannot print a message to stderr on almost every execution. (OSS-Fuzz's third
# edit, for warnings, matches nothing in these versions, so it is left out.)
(
    cd "$OUT/src"
    sed -e "s/option STDIO/option STDIO disabled/" \
        -e "s/option WRITE enables WRITE_INT_FUNCTIONS/option WRITE disabled/" \
        scripts/pnglibconf.dfa > scripts/pnglibconf.dfa.tmp
    mv scripts/pnglibconf.dfa.tmp scripts/pnglibconf.dfa
    make -s -f scripts/pnglibconf.mak AWK=awk CPP="clang -E" pnglibconf.h 2>/dev/null
)
# SIMD code is off so every platform runs the same C filter code.
# "-include math.h": libpng <= 1.6.39 includes the obsolete <fp.h> on macOS unless math.h came first.
FLAGS="-O1 -g -fsanitize-coverage=trace-pc-guard -DPNG_ARM_NEON_OPT=0 -DPNG_INTEL_SSE_OPT=0 -include math.h -I$OUT/src"

for f in "$OUT"/src/png*.c; do
    # pngtest.c has its own main(); pnglibconf.c is left over from the configuration step.
    case "$(basename "$f")" in pngtest.c | pnglibconf.c) continue ;; esac
    clang $FLAGS -c "$f" -o "$OUT/obj/$(basename "$f" .c).o"
done
clang++ $FLAGS -std=c++11 -c "$OUT/src/contrib/oss-fuzz/libpng_read_fuzzer.cc" -o "$OUT/obj/harness.o"
# Calls LLVMFuzzerInitialize if present, and stubs LLVMFuzzerMutate (see the file). Not instrumented.
clang -O1 -c "$HERE/../harness_shim.c" -o "$OUT/obj/harness_shim.o"
ar rcs "$OUT/libharness.a" "$OUT"/obj/*.o

cp "$OUT/src/contrib/oss-fuzz/png.dict" "$OUT/"
cp "$OUT"/src/contrib/pngsuite/*.png "$OUT/seeds/"

# Relinks fuzzer/target/release/fredbear against this version; copy it out before building another.
(cd "$FUZZER" && FREDBEAR_HARNESS="$OUT/libharness.a" cargo build --release)
cp "$FUZZER/target/release/fredbear" "$OUT/fredbear"
echo "built $OUT/fredbear"
