/* Linked into every libharness.a (compiled without coverage instrumentation).
 *
 * - fredbear_harness_init(): libFuzzer calls LLVMFuzzerInitialize once before the first input when
 *   the harness defines it (libxml2's does: allocator hooks, parser init). fredbear calls this.
 * - LLVMFuzzerMutate(): libxml2's harness also defines a custom mutator that calls libFuzzer's
 *   LLVMFuzzerMutate. fredbear never calls the custom mutator (it uses its own operator
 *   families), but the symbol must exist to link. This stub leaves the input unchanged. */
#include <stddef.h>
#include <stdint.h>

int LLVMFuzzerInitialize(int *argc, char ***argv) __attribute__((weak));

void fredbear_harness_init(void) {
    static char name[] = "fredbear";
    static char *args[] = {name, NULL};
    static int argc = 1;
    static char **argv = args;
    if (LLVMFuzzerInitialize) {
        LLVMFuzzerInitialize(&argc, &argv);
    }
}

__attribute__((weak)) size_t LLVMFuzzerMutate(uint8_t *data, size_t size, size_t max_size) {
    (void) data;
    (void) max_size;
    return size;
}
