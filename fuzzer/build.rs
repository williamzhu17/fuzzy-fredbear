//! Links a libFuzzer-style harness (LLVMFuzzerTestOneInput) when FREDBEAR_HARNESS points to a
//! static library named libharness.a. Without it, the binary only has the toy targets.

use std::path::Path;

fn main() {
    println!("cargo::rustc-check-cfg=cfg(harness)");
    println!("cargo::rerun-if-env-changed=FREDBEAR_HARNESS");
    let Ok(lib) = std::env::var("FREDBEAR_HARNESS") else {
        return;
    };
    let path = Path::new(&lib);
    if !path.is_file() || path.file_name() != Some("libharness.a".as_ref()) {
        panic!("FREDBEAR_HARNESS={lib} must be an existing file named libharness.a");
    }
    println!("cargo::rerun-if-changed={lib}");
    println!("cargo::rustc-link-search=native={}", path.parent().unwrap().display());
    println!("cargo::rustc-link-lib=static=harness");
    println!("cargo::rustc-link-lib=z");
    let cxx = if std::env::var("CARGO_CFG_TARGET_OS").as_deref() == Ok("macos") { "c++" } else { "stdc++" };
    println!("cargo::rustc-link-lib={cxx}");
    println!("cargo::rustc-cfg=harness");
}
