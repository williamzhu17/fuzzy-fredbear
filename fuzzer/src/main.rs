//! One fuzzing campaign with a chosen operator-family policy. Writes to --out:
//!   batches.jsonl  one line per batch of executions (see policy::BatchRecord)
//!   coverage.csv   t, executions, corpus size, covered map entries
//!   queue/         the corpus (used as the inherited corpus for the next version)
//!   crashes/       crashing inputs

use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::time::{Duration, Instant};

use clap::Parser;
use libafl::corpus::{Corpus, InMemoryOnDiskCorpus, OnDiskCorpus};
use libafl::events::SimpleEventManager;
use libafl::executors::{ExitKind, inprocess::InProcessExecutor};
use libafl::feedbacks::{CrashFeedback, MapFeedbackMetadata, MaxMapFeedback};
use libafl::fuzzer::{Evaluator, Fuzzer, StdFuzzer};
use libafl::inputs::{BytesInput, HasTargetBytes};
use libafl::monitors::NopMonitor;
use libafl::mutators::Tokens;
use libafl::observers::{HitcountsMapObserver, StdMapObserver};
use libafl::schedulers::QueueScheduler;
use libafl::stages::StdMutationalStage;
use libafl::state::{HasCorpus, HasExecutions, StdState};
use libafl::{Error, HasMetadata, HasNamedMetadata};
use libafl_bolts::ToSlice;
use libafl_bolts::rands::StdRand;
use libafl_bolts::tuples::tuple_list;

use fredbear::mutator::{FAMILIES, FamilyMutator, base_counts_from_log};
use fredbear::policy::{Policy, PolicyConfig, PolicyKind, PriorSet};
use fredbear::toy;

#[cfg(harness)]
unsafe extern "C" {
    fn LLVMFuzzerTestOneInput(data: *const u8, size: usize) -> i32;
}

/// The libFuzzer-style harness linked in by build.rs (FREDBEAR_HARNESS).
fn run_harness(_data: &[u8]) {
    #[cfg(harness)]
    unsafe {
        LLVMFuzzerTestOneInput(_data.as_ptr(), _data.len());
    }
}

#[derive(Parser)]
struct Args {
    /// Target to fuzz. "harness" is the library linked in at build time (targets/libpng/build.sh).
    #[arg(long, value_parser = ["toy-v1", "toy-v2", "harness"])]
    target: String,
    #[arg(long, value_enum)]
    policy: PolicyKind,
    /// batches.jsonl from a uniform base run on the previous version; builds the priors.
    #[arg(long)]
    base_log: Option<PathBuf>,
    /// Only base-run batches before this many seconds feed the prior (PLAN section 3: first hour).
    #[arg(long, default_value_t = 3600.0)]
    base_cutoff: f64,
    /// N: the most new-version observations the old evidence is worth, per family.
    #[arg(long, default_value_t = 5000.0)]
    cap_n: f64,
    #[arg(long, default_value_t = 256)]
    batch: u64,
    /// DTS only: per-batch decay of the transfer prior toward calib.
    #[arg(long, default_value_t = 0.999)]
    gamma_prior: f64,
    /// DTS only: per-batch decay of the observed counts (1 = no decay).
    #[arg(long, default_value_t = 1.0)]
    gamma_data: f64,
    /// Initial corpus directory (the inherited corpus on version v+1).
    #[arg(long)]
    corpus: Option<PathBuf>,
    /// Dictionary in AFL format.
    #[arg(long)]
    dict: Option<PathBuf>,
    #[arg(long, default_value_t = 60)]
    secs: u64,
    #[arg(long, default_value_t = 0)]
    seed: u64,
    #[arg(long)]
    out: PathBuf,
}

fn main() -> Result<(), Error> {
    let args = Args::parse();
    let needs_prior = !matches!(args.policy, PolicyKind::Uniform | PolicyKind::Fresh);
    if needs_prior && args.base_log.is_none() {
        return Err(Error::illegal_argument(format!("--policy {:?} needs --base-log", args.policy)));
    }
    let priors = match &args.base_log {
        Some(path) if needs_prior => {
            let base = base_counts_from_log(path, args.base_cutoff).map_err(Error::illegal_argument)?;
            base.validate(&FAMILIES).map_err(Error::illegal_argument)?;
            PriorSet::build(&base, args.cap_n, args.seed)
        }
        _ => PriorSet::flat(FAMILIES.len()),
    };
    let real = args.target == "harness";
    if real && !cfg!(harness) {
        return Err(Error::illegal_argument("this binary has no harness; build it with targets/libpng/build.sh"));
    }
    if real && args.corpus.is_none() {
        return Err(Error::illegal_argument("--target harness needs --corpus (seeds or an inherited corpus)"));
    }
    if fs::exists(&args.out)? {
        return Err(Error::illegal_argument(format!("{} already exists", args.out.display())));
    }
    fs::create_dir_all(&args.out)?;

    let (target, map): (fn(&[u8]), _) = match args.target.as_str() {
        "toy-v1" => (|d| toy::run(d, 1), unsafe {
            StdMapObserver::from_mut_ptr("edges", (&raw mut toy::MAP).cast::<u8>(), toy::MAP_SIZE)
        }),
        "toy-v2" => (|d| toy::run(d, 2), unsafe {
            StdMapObserver::from_mut_ptr("edges", (&raw mut toy::MAP).cast::<u8>(), toy::MAP_SIZE)
        }),
        _ => (run_harness, unsafe { libafl_targets::std_edges_map_observer("edges") }),
    };
    let observer = HitcountsMapObserver::new(map);
    let mut feedback = MaxMapFeedback::new(&observer);
    let mut objective = CrashFeedback::new();
    let mut state = StdState::new(
        StdRand::with_seed(args.seed),
        InMemoryOnDiskCorpus::new(args.out.join("queue"))?,
        OnDiskCorpus::new(args.out.join("crashes"))?,
        &mut feedback,
        &mut objective,
    )?;
    if let Some(dict) = &args.dict {
        state.add_metadata(Tokens::from_file(dict)?);
    }
    let mut fuzzer = StdFuzzer::new(QueueScheduler::new(), feedback, objective);
    let mut mgr = SimpleEventManager::new(NopMonitor::new());
    let mut harness = |input: &BytesInput| {
        target(&input.target_bytes().to_slice());
        ExitKind::Ok
    };
    let mut executor = InProcessExecutor::builder()
        .harness(&mut harness)
        .observers(tuple_list!(observer))
        .fuzzer(&mut fuzzer)
        .state(&mut state)
        .event_mgr(&mut mgr)
        .build()?;

    match &args.corpus {
        Some(dir) => state.load_initial_inputs(&mut fuzzer, &mut executor, &mut mgr, &[dir.clone()])?,
        None => {
            fuzzer.add_input(&mut state, &mut executor, &mut mgr, BytesInput::new(b"FRED".to_vec()))?;
        }
    }

    let start = Instant::now();
    let cfg = PolicyConfig {
        kind: args.policy,
        batch: args.batch,
        gamma_prior: args.gamma_prior,
        gamma_data: args.gamma_data,
    };
    let mutator = FamilyMutator::new(Policy::new(cfg, priors, args.seed), File::create(args.out.join("batches.jsonl"))?, start);
    let mut stages = tuple_list!(StdMutationalStage::new(mutator));

    // The t=0 row is the inherited corpus's own coverage; only later gains count for a policy.
    let mut coverage = File::create(args.out.join("coverage.csv"))?;
    writeln!(coverage, "t,execs,corpus,edges")?;
    writeln!(coverage, "{}", coverage_row(&state, 0.0)?)?;
    // About one row per second. The iteration that crosses the deadline always writes the last row.
    let mut next_row = 1;
    while start.elapsed() < Duration::from_secs(args.secs) {
        fuzzer.fuzz_one(&mut stages, &mut executor, &mut state, &mut mgr)?;
        let now = start.elapsed();
        if now.as_secs() >= next_row {
            writeln!(coverage, "{}", coverage_row(&state, now.as_secs_f64())?)?;
            next_row = now.as_secs() + 1;
        }
    }
    Ok(())
}

fn coverage_row<I, S>(state: &S, t: f64) -> Result<String, Error>
where
    S: HasExecutions + HasCorpus<I> + HasNamedMetadata,
{
    let edges = state.named_metadata::<MapFeedbackMetadata<u8>>("edges")?.num_covered_map_indexes;
    Ok(format!("{t:.1},{},{},{edges}", state.executions(), state.corpus().count()))
}
