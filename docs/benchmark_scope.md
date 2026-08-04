# Benchmark Scope

HAKARI-Bench is a lightweight proxy for repeated model selection, regression
detection, and quality-efficiency trade-off analysis. It is not intended to
replace full benchmark evaluation.

Each Nano-set task uses a shared IR layout: `corpus`, `queries`, `qrels`, and
fixed candidate subsets such as `bm25`, `harrier_oss_v1_270m`, and
`reranking_hybrid`. This makes candidate generation and reranking comparable
under the same metrics.

The benchmark currently evaluates 557 retrieval tasks across 35+ benchmark
groups and 43+ languages, including BEIR-style retrieval, MTEB/MMTEB language
families, MIRACL, MLDR, code retrieval, long-context retrieval, and expert
domains such as legal, medical, chemistry, finance, and built-environment
search.

## Evaluation Count And Overall Count

The evaluation task count and the leaderboard Overall task count are
intentionally different:

- A complete evaluation runs and preserves results for all **557 tasks**.
- The leaderboard excludes **13 overlapping task copies** from its Overall
  calculation, so a complete Overall result is based on **538 tasks**.

The excluded copies are still valid evaluation artifacts and remain in the
results dataset. They are omitted only from the Overall aggregate so that the
same underlying benchmark task is not weighted more than once. The exclusions
are `NanoIFIRFiQA`, `NanoIFIRNFCorpus`, `NanoIFIRScifact`,
`NanoAILACasedocs`, `NanoAILAStatutes`, `NanoLegalSummarization`,
`NanoLegalBenchCorporateLobbying`, `NanoCUREv1`, `NanoNFCorpus`,
`NanoSciFact`, `NanoWinoGrande`, `NanoSpartQA`, and `NanoTempReasonL1`.

`NanoBEIR-en` is the English component of `MNanoBEIR`. It is part of the 557
evaluation tasks and is not one of the 13 Overall exclusions. Referring to the
same dataset through the `MNanoBEIR` collection does not create a second result
row or cause it to be counted twice.

The canonical exclusion rules live in
[`config/viewer/benchmarks.yaml`](../config/viewer/benchmarks.yaml). Do not
remove evaluation outputs merely to make their file count match the 538-task
Overall count.

`NanoMTEB-BR` contributes six native Brazilian Portuguese Retrieval tasks to
the complete evaluation target. It has a dedicated viewer page but is not added
to Overall because the language-focused NanoMTEB family is diagnostic coverage
rather than an additional Overall component. See
[NanoMTEB-BR](nanomteb_br.md) for task provenance and validation details.

Built-in dataset definitions live under [`config/datasets/`](../config/datasets/),
and benchmark collections live under
[`config/dataset_collections/`](../config/dataset_collections/).

For Nano-set construction details and source attribution policy, see
[create_nano_datasets.md](create_nano_datasets.md).
