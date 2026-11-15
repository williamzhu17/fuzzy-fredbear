//! A LibAFL mutator that applies one operator family per execution (PLAN section 2, "What one
//! action is"): the policy picks a family, then a havoc-sized stack of mutations is applied, all
//! from that family. Success means the executed input was added to the corpus.

use std::borrow::Cow;
use std::fs::File;
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::num::NonZero;
use std::time::Instant;

use libafl::Error;
use libafl::corpus::CorpusId;
use libafl::mutators::{
    BitFlipMutator, ByteAddMutator, ByteDecMutator, ByteFlipMutator, ByteIncMutator, ByteInterestingMutator,
    ByteNegMutator, ByteRandMutator, BytesCopyMutator, BytesDeleteMutator, BytesExpandMutator,
    BytesInsertCopyMutator, BytesInsertMutator, BytesRandInsertMutator, BytesRandSetMutator, BytesSetMutator,
    BytesSwapMutator, CrossoverInsertMutator, CrossoverReplaceMutator, DwordAddMutator, DwordInterestingMutator,
    MutationResult, Mutator, MutatorsTuple, QwordAddMutator, TokenInsert, TokenReplace, WordAddMutator,
    WordInterestingMutator,
};
use libafl::state::HasRand;
use libafl_bolts::Named;
use libafl_bolts::rands::Rand;
use libafl_bolts::tuples::{tuple_list, tuple_list_type};
use serde::Serialize;

use crate::policy::{BaseCounts, BatchRecord, Policy};

pub const FAMILIES: [&str; 9] =
    ["bitflip", "arith", "interesting", "random_bytes", "delete", "insert", "copy_swap", "splice", "dictionary"];

/// Indices into `AllMutations` for each family, in `FAMILIES` order.
const MEMBERS: [&[usize]; 9] = [
    &[0, 1, 2],
    &[3, 4, 5, 6, 7, 8],
    &[9, 10, 11],
    &[12, 13, 14],
    &[15],
    &[16, 17, 18],
    &[19, 20, 21],
    &[22, 23],
    &[24, 25],
];

type AllMutations = tuple_list_type!(
    BitFlipMutator, ByteFlipMutator, ByteNegMutator,
    ByteIncMutator, ByteDecMutator, ByteAddMutator, WordAddMutator, DwordAddMutator, QwordAddMutator,
    ByteInterestingMutator, WordInterestingMutator, DwordInterestingMutator,
    ByteRandMutator, BytesSetMutator, BytesRandSetMutator,
    BytesDeleteMutator,
    BytesExpandMutator, BytesInsertMutator, BytesRandInsertMutator,
    BytesCopyMutator, BytesInsertCopyMutator, BytesSwapMutator,
    CrossoverInsertMutator, CrossoverReplaceMutator,
    TokenInsert, TokenReplace,
);

fn all_mutations() -> AllMutations {
    tuple_list!(
        BitFlipMutator::new(), ByteFlipMutator::new(), ByteNegMutator::new(),
        ByteIncMutator::new(), ByteDecMutator::new(), ByteAddMutator::new(), WordAddMutator::new(),
        DwordAddMutator::new(), QwordAddMutator::new(),
        ByteInterestingMutator::new(), WordInterestingMutator::new(), DwordInterestingMutator::new(),
        ByteRandMutator::new(), BytesSetMutator::new(), BytesRandSetMutator::new(),
        BytesDeleteMutator::new(),
        BytesExpandMutator::new(), BytesInsertMutator::new(), BytesRandInsertMutator::new(),
        BytesCopyMutator::new(), BytesInsertCopyMutator::new(), BytesSwapMutator::new(),
        CrossoverInsertMutator::new(), CrossoverReplaceMutator::new(),
        TokenInsert::new(), TokenReplace::new(),
    )
}

#[derive(Serialize)]
struct LogLine<'a> {
    /// Seconds since the campaign started.
    t: f64,
    #[serde(flatten)]
    rec: &'a BatchRecord,
}

pub struct FamilyMutator {
    name: Cow<'static, str>,
    mutations: AllMutations,
    policy: Policy,
    /// Family used for the input currently being executed.
    pending: Option<usize>,
    log: BufWriter<File>,
    start: Instant,
}

impl FamilyMutator {
    /// `log` receives one JSON line per batch.
    pub fn new(policy: Policy, log: File, start: Instant) -> Self {
        FamilyMutator {
            name: Cow::from("FamilyMutator"),
            mutations: all_mutations(),
            policy,
            pending: None,
            log: BufWriter::new(log),
            start,
        }
    }
}

impl Named for FamilyMutator {
    fn name(&self) -> &Cow<'static, str> {
        &self.name
    }
}

impl<I, S> Mutator<I, S> for FamilyMutator
where
    AllMutations: MutatorsTuple<I, S>,
    S: HasRand,
{
    fn mutate(&mut self, state: &mut S, input: &mut I) -> Result<MutationResult, Error> {
        // A family can be unable to mutate this input (no dictionary tokens, a one-entry corpus
        // for splice, deleting from a 1-byte input). No execution happens then, so it is not
        // counted; try another family instead.
        let mut skipped = Vec::new();
        while let Some(family) = self.policy.choose(&skipped) {
            let members = MEMBERS[family];
            // Stack depth 2^(1..=7), the same distribution as LibAFL's stock havoc.
            let depth = 1 << (1 + state.rand_mut().below_or_zero(7));
            let mut result = MutationResult::Skipped;
            for _ in 0..depth {
                let pick = state.rand_mut().below(NonZero::new(members.len()).unwrap());
                if self.mutations.get_and_mutate(members[pick].into(), state, input)? == MutationResult::Mutated {
                    result = MutationResult::Mutated;
                }
            }
            if result == MutationResult::Mutated {
                self.pending = Some(family);
                return Ok(result);
            }
            skipped.push(family);
        }
        Ok(MutationResult::Skipped)
    }

    fn post_exec(&mut self, state: &mut S, new_corpus_id: Option<CorpusId>) -> Result<(), Error> {
        if let Some(family) = self.pending.take()
            && let Some(rec) = self.policy.record(family, new_corpus_id.is_some())
        {
            let line = LogLine { t: self.start.elapsed().as_secs_f64(), rec: &rec };
            serde_json::to_writer(&mut self.log, &line).map_err(|e| Error::unknown(e.to_string()))?;
            self.log.write_all(b"\n")?;
            self.log.flush()?;
        }
        self.mutations.post_exec_all(state, new_corpus_id)
    }
}

/// Sum the per-family counts of a base run's batches.jsonl over batches that ended before
/// `cutoff` seconds.
pub fn base_counts_from_log(path: &std::path::Path, cutoff: f64) -> Result<BaseCounts, String> {
    let file = File::open(path).map_err(|e| format!("{}: {e}", path.display()))?;
    let k = FAMILIES.len();
    let (mut s, mut n) = (vec![0.0; k], vec![0.0; k]);
    for (i, line) in BufReader::new(file).lines().enumerate() {
        let line = line.map_err(|e| e.to_string())?;
        let v: serde_json::Value =
            serde_json::from_str(&line).map_err(|e| format!("{}:{}: {e}", path.display(), i + 1))?;
        if v["t"].as_f64().ok_or("missing t")? > cutoff {
            break;
        }
        for a in 0..k {
            s[a] += v["s"][a].as_f64().ok_or("missing s")?;
            n[a] += v["n"][a].as_f64().ok_or("missing n")?;
        }
    }
    if n.iter().sum::<f64>() == 0.0 {
        return Err(format!("{}: no batches before {cutoff}s", path.display()));
    }
    Ok(BaseCounts { families: FAMILIES.iter().map(|f| f.to_string()).collect(), s, n })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_mutation_belongs_to_exactly_one_family() {
        let mut all: Vec<usize> = MEMBERS.iter().flat_map(|m| m.iter().copied()).collect();
        all.sort();
        assert_eq!(all, (0..26).collect::<Vec<_>>());
    }

    fn write_log(name: &str, lines: &[&str]) -> std::path::PathBuf {
        let path = std::env::temp_dir().join(format!("fredbear-test-{}-{name}.jsonl", std::process::id()));
        std::fs::write(&path, lines.join("\n")).unwrap();
        path
    }

    #[test]
    fn base_counts_sum_batches_before_cutoff() {
        let path = write_log("ok", &[
            r#"{"t":1.0,"n":[2,0,0,0,0,0,0,0,1],"s":[1,0,0,0,0,0,0,0,0]}"#,
            r#"{"t":2.0,"n":[3,0,0,0,0,0,0,0,0],"s":[0,0,0,0,0,0,0,0,0]}"#,
            r#"{"t":9.0,"n":[100,0,0,0,0,0,0,0,0],"s":[50,0,0,0,0,0,0,0,0]}"#,
        ]);
        let base = base_counts_from_log(&path, 5.0).unwrap();
        assert_eq!((base.n[0], base.s[0], base.n[8]), (5.0, 1.0, 1.0));
    }

    #[test]
    fn base_counts_errors() {
        assert!(base_counts_from_log(std::path::Path::new("/nonexistent.jsonl"), 1.0).is_err());
        let late = write_log("late", &[r#"{"t":9.0,"n":[1,0,0,0,0,0,0,0,0],"s":[0,0,0,0,0,0,0,0,0]}"#]);
        assert!(base_counts_from_log(&late, 5.0).is_err());
        let short = write_log("short", &[r#"{"t":1.0,"n":[1],"s":[0]}"#]);
        assert!(base_counts_from_log(&short, 5.0).is_err());
    }
}
