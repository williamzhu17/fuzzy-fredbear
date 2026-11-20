/* Coverage replay driver: runs a libFuzzer-style harness once on every file named on stdin (one
 * path per line). Linked into the coverage build (-fprofile-instr-generate -fcoverage-mapping),
 * so the profile written at exit (LLVM_PROFILE_FILE) records which code those inputs reach. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int LLVMFuzzerInitialize(int *argc, char ***argv) __attribute__((weak));
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size);

/* libxml2's harness defines a custom mutator that calls libFuzzer's LLVMFuzzerMutate; it is never
 * called here, but the symbol must exist to link. */
__attribute__((weak)) size_t LLVMFuzzerMutate(uint8_t *data, size_t size, size_t max_size) {
    (void) data;
    (void) max_size;
    return size;
}

int main(int argc, char **argv) {
    char line[4096];
    size_t n = 0;
    if (LLVMFuzzerInitialize) {
        LLVMFuzzerInitialize(&argc, &argv);
    }
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\n")] = 0;
        if (!*line) continue;
        FILE *f = fopen(line, "rb");
        if (!f) { fprintf(stderr, "replay: cannot open %s\n", line); continue; }
        fseek(f, 0, SEEK_END);
        long size = ftell(f);
        fseek(f, 0, SEEK_SET);
        uint8_t *buf = malloc(size > 0 ? (size_t) size : 1);
        if (size > 0 && fread(buf, 1, (size_t) size, f) != (size_t) size) { size = 0; }
        fclose(f);
        LLVMFuzzerTestOneInput(buf, (size_t) size);
        free(buf);
        n++;
    }
    fprintf(stderr, "replay: ran %zu inputs\n", n);
    return 0;
}
