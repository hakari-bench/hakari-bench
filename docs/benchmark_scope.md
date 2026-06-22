# Benchmark Scope

HAKARI-Bench is a lightweight proxy for repeated model selection, regression
detection, and quality-efficiency trade-off analysis. It is not intended to
replace full benchmark evaluation.

Each Nano-set task uses a shared IR layout: `corpus`, `queries`, `qrels`, and
fixed candidate subsets such as `bm25`, `harrier_oss_v1_270m`, and
`reranking_hybrid`. This makes candidate generation and reranking comparable
under the same metrics.

The benchmark currently covers 35+ benchmark groups and 551+ retrieval tasks
across 43+ languages, including BEIR-style retrieval, MTEB/MMTEB language
families, MIRACL, MLDR, code retrieval, long-context retrieval, and expert
domains such as legal, medical, chemistry, finance, and built-environment
search.

Built-in dataset definitions live under [`config/datasets/`](../config/datasets/),
and benchmark collections live under
[`config/dataset_collections/`](../config/dataset_collections/).

For Nano-set construction details and source attribution policy, see
[create_nano_datasets.md](create_nano_datasets.md).
