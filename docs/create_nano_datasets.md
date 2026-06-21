# Creating Nano Datasets

This document is the canonical workflow for recreating Nano-set retrieval
datasets in this repository, including MTEB-derived Nano families.

## Goal

Create upload-ready Nano datasets that can be evaluated by HAKARI-Bench. The
standard Hugging Face Datasets shape is:

- config `corpus`
- config `queries`
- config `qrels`
- config `bm25`
- config `harrier_oss_v1_270m` for dense candidates when building
  reranking-hybrid Nano-sets
- config `reranking_hybrid` for default reranking candidates when building
  reranking-hybrid Nano-sets
- task/subset names stored as split names in every config

Example local output:

```text
output/NanoExample/
  README.md
  manifest.json
  corpus/NanoTask.parquet
  queries/NanoTask.parquet
  qrels/NanoTask.parquet
  bm25/NanoTask.parquet
  harrier_oss_v1_270m/NanoTask.parquet
  reranking_hybrid/NanoTask.parquet
  metadata/NanoTask.json
  reranking_hybrid_metadata.json
```

The matching HAKARI dataset YAML is generated at the same time when
`--dataset-config-dir` is supplied:

```text
config/datasets/nanoexample.yaml
```

## Supported Sources

Use `scripts/create_nano_dataset.py` for single-task conversions from a
Hugging Face or local source. Use
`scripts/recreate_mteb_nano_datasets.py` for NanoMTEB-family recreation from
the installed MTEB registry, and use
`scripts/build_reranking_hybrid_nano_dataset.py` or
`scripts/build_all_reranking_hybrid_nano_datasets.py` when adding the current
BM25 top-500, dense top-500, and `reranking_hybrid` candidate subsets.

Supported Hugging Face MTEB/BEIR-style source layout:

- corpus: config `corpus`, split `corpus`
- queries: config `queries`, split `queries`
- qrels: config `default`, source evaluation split such as `test`

Supported local parquet layouts:

- nested task layout:
  - `<source-split>/corpus/test.parquet`
  - `<source-split>/queries/test.parquet`
  - `<source-split>/qrels/test.parquet`
- flat Nano-like layout:
  - `corpus/<source-split>.parquet`
  - `queries/<source-split>.parquet`
  - `qrels/<source-split>.parquet`
- simple single-task layout:
  - `corpus/test.parquet`
  - `queries/test.parquet`
  - `qrels/test.parquet`

The converter normalizes common source column variants:

- corpus ids: `_id`, `id`, `docid`, `doc_id`, `corpus-id`, `corpus_id`,
  `document_id`
- query ids: `_id`, `id`, `qid`, `query-id`, `query_id`
- qrels query ids: `query-id`, `query_id`, `qid`, `query`
- qrels corpus ids: `corpus-id`, `corpus_id`, `doc-id`, `doc_id`, `docid`,
  `document_id`
- query text: `text`, `query`, `question`
- corpus text: `title` plus `text`, or `document`, `contents`, `content`,
  `body`, `passage`
- qrels score: `score`, `relevance`, `label`

If a source uses a different schema, add a focused test and extend
`hakari_bench.nano_dataset_builder` rather than patching a one-off script.

## Qrels Policy

Published Nano qrels are positive-only:

- `score > 0`: keep as `qrels`
- `score <= 0`: exclude from `qrels`
- missing score: treat as positive only when the source qrels table is
  positive-only by convention

Rows with `score <= 0` are useful hard negatives. The converter uses them as
preferred corpus candidates for the selected queries, but they are never written
to `qrels`.

The output `qrels` schema is:

```text
query-id: string
corpus-id: string
```

## Corpus Sampling

The default q200 recipe is:

1. Normalize source corpus, queries, and qrels.
2. Select up to 200 queries with at least one positive qrel.
3. Remove exact duplicate query text.
4. Add all selected positive qrels documents to the corpus first.
5. Add source hard negatives for selected queries with deterministic
   query-round-robin sampling.
6. Fill remaining corpus slots from source corpus order up to 10,000 documents.
7. Skip duplicate document ids, empty text, and exact duplicate document text.
8. Verify qrels reference only selected queries and selected corpus documents.

Override limits with `--query-limit` and `--doc-limit` only when reproducing a
different Nano shape.

## BM25 Generation

HAKARI-Bench already has BM25 implementation in `hakari_bench.bm25`.
`scripts/create_nano_dataset.py` uses that implementation instead of carrying a
separate BM25 stack.

The BM25 candidate generation flow is:

1. Convert selected corpus and queries into dictionaries keyed by `_id`.
2. Call `rank_bm25_candidates()` with a `BM25Config`.
3. The BM25 implementation tokenizes corpus and query text with the selected
   tokenizer, builds a `bm25s.BM25` index, and retrieves top-k corpus ids for
   each query.
4. Convert rankings to rows:

```text
query-id: string
corpus-ids: list[string]
```

5. Force qrels-positive documents into each `corpus-ids` list when missing by
   replacing a tail non-positive candidate.
6. Record `forced_queries`, `forced_doc_count`, and
   `missing_positive_doc_count_after_forcing` in `metadata/<split>.json`.
7. Record `candidate_coverage` in `metadata/<split>.json` and surface query and
   relevant coverage in the generated README BM25 table.

`missing_positive_doc_count_after_forcing` should normally be `0`. If it is not
zero, the split has more positives than the BM25 candidate cap can cover, or the
candidate list is too short. Fix this by changing query selection, increasing
`--top-k`, or explicitly documenting a qrels capping policy.

## Reranking Hybrid Candidate Generation

For datasets used by `reranking_hybrid` diagnostics, build three candidate
configs:

- `bm25`: local BM25 top-500. The tokenizer should be selected from task
  metadata first, then from deterministic query-language detection. For example,
  Japanese uses `wordseg@ja`; code tasks use `regex`.
- `harrier_oss_v1_270m`: dense top-500 from
  `microsoft/harrier-oss-v1-270m`. In README tables this is shown as `Dense`.
  `Dense` means this Harrier model with the `web_search_query` prompt for
  queries and cosine similarity over normalized embeddings.
- `reranking_hybrid`: RRF over `bm25` and `harrier_oss_v1_270m`.

The hybrid candidate subset should follow the "RRF top-100 plus optional
safeguard positive at rank 101" policy. Rows with 100 candidates mean the RRF
top-100 already contains a qrels-positive document; rows with 101 candidates
mean the 101st document is a safeguard positive appended only because the RRF
top-100 missed all positives. Small corpus tasks with fewer than 100 documents
should cover every qrels-positive document present in the corpus without adding
a safeguard row. `candidate_coverage` should show both `query_coverage` and
`relevant_coverage` as `1.0` for the safeguarded candidate set.

README candidate quality tables should report `nDCG@10` and `Recall@100` as
0-100 scores with two decimals. Put ranking quality columns together before
recall columns:

```text
BM25 nDCG@10 | Dense nDCG@10 | Hybrid nDCG@10 |
BM25 Recall@100 | Dense Recall@100 | Hybrid Recall@100
```

`Recall@100` uses only the top 100 candidates, so the optional rank-101
safeguard positive is not counted in `Recall@100`. Also include the resolved
BM25 tokenizer, hybrid candidate count range, and safeguard-positive count per
split.

To rebuild MNanoBEIR BM25 subsets without changing the existing corpus, queries,
or qrels, use:

```bash
uv run python scripts/rebuild_mnanobeir_bm25.py \
  --output-dir output/nano_datasets_mnanobeir_bm25_rebuilt \
  --overwrite
```

The script snapshots the published `hakari-bench/NanoBEIR-*` dataset layouts,
regenerates `bm25/*.parquet`, updates split metadata, rewrites dataset READMEs,
and fails by default if any rebuilt split is not 100% covered at top-k. It uses
`--tokenizer auto` by default: code tasks use `regex`, and natural-language tasks
use metadata language or deterministic query-language detection to choose a
language-specific tokenizer. Multilingual rebuilds should be run in an
environment prepared with `uv sync --extra wordseg`; otherwise languages that
auto-select `wordseg` will fail with an actionable missing-dependency error.

Supported tokenizers are the existing HAKARI BM25 tokenizers:

- `regex`
- `whitespace`
- `transformer`
- `stemmer`
- `english_regex`
- `english_porter`
- `english_porter_stop`
- `wordseg`

Use a fixed tokenizer for reproducible dataset creation unless a dataset family
has a documented reason to vary tokenizers per split.

## Creating From MTEB Sources

MTEB-derived Nano datasets should be planned from the installed MTEB registry,
not only from existing repository YAML. Inspect:

- `task.metadata.name`
- `task.metadata.dataset["path"]`
- `task.metadata.dataset["revision"]`
- `task.metadata.eval_splits`
- `task.metadata.hf_subsets`
- `task.metadata.languages`
- benchmark membership from `mteb.get_benchmarks()`

Group tasks by provenance in this order:

1. official MTEB benchmark family, such as `MTEB(eng, v2)`,
   `MTEB(Multilingual, v2)`, `JMTEB(v2)`, `MTEB(fas, v2)`,
   `MTEB(cmn, v1)`, `MTEB(rus, v1.1)`, or `VN-MTEB (vie, v1)`;
2. independent benchmark or source-family collection, such as MuPLeR or
   IndicQA;
3. language-family collection with enough retrieval coverage;
4. `NanoMTEB-Misc` only as a final fallback.

Use versioned Nano names when the official MTEB benchmark is versioned, for
example `NanoMTEB-v2`, `NanoMMTEB-v2`, `NanoJMTEB-v2`, and
`NanoFaMTEB-v2`. Existing v1-compatible names such as `NanoCMTEB`,
`NanoRuMTEB`, and `NanoVNMTEB` remain unversioned unless a migration explicitly
changes them.

In uploaded Hugging Face datasets, configs should be source groups rather than
MTEB task subsets:

- `mteb` for datasets under the official `mteb/` namespace;
- `{org_or_user}__{dataset_name}` for other Hugging Face namespaces.

Use split names for the source-local evaluation task or slice. Do not expose
MTEB `hf_subsets` as public Nano configs unless the upstream source dataset
itself is a distinct data source. Record the MTEB task name, source dataset id,
source revision, upstream subset/slice, eval split, reference, and license in
README text and split metadata.

When a base task and a `HardNegatives` task share the same underlying dataset,
publish one Nano split. Prefer the `HardNegatives` source for Nano creation,
record the base task as related provenance, and omit `HardNegatives` from the
public split name unless it is needed to distinguish genuinely different
retrieval tasks.

For full NanoMTEB-family recreation:

```bash
uv run python scripts/recreate_mteb_nano_datasets.py \
  --output-root output/nano_datasets \
  --config-root config \
  --top-k 500 \
  --bm25-tokenizer regex \
  --plan-json output/nano_datasets/plan.json
```

Then build current reranking candidates from the built-in Nano dataset registry
or uploaded Hub datasets:

```bash
uv run python scripts/build_all_reranking_hybrid_nano_datasets.py \
  --output-root output/nano_reranking_hybrid \
  --bm25-top-k 500 \
  --dense-top-k 500 \
  --hybrid-top-k 100
```

Use `scripts/push_mteb_nano_datasets_to_hub.py` only after reviewing the plan,
generated READMEs, metadata, and deletion/upload target list. The upload script
can delete replaced Hub datasets when `--delete` is used, so run `--dry-run`
first.

For a one-off Hugging Face MTEB/BEIR-style source, use
`scripts/create_nano_dataset.py` directly. Use `--top-k 500` for datasets that
will feed the current reranking-hybrid candidate pipeline.

Example:

```bash
uv run python scripts/create_nano_dataset.py \
  --source-dataset-id mteb/scifact \
  --dataset-name NanoExample \
  --dataset-id hakari-bench/NanoExample \
  --split-name NanoSciFact \
  --output-dir output/NanoExample \
  --dataset-config-dir config/datasets \
  --qrels-config default \
  --qrels-split test \
  --query-limit 200 \
  --doc-limit 10000 \
  --top-k 500 \
  --bm25-tokenizer regex
```

For non-default source configs or splits, set:

- `--corpus-config`
- `--queries-config`
- `--qrels-config`
- `--corpus-split`
- `--queries-split`
- `--qrels-split`
- `--revision`

## Creating From Local Parquet

Example:

```bash
uv run python scripts/create_nano_dataset.py \
  --source-dir output/source_mteb_like \
  --source-split-name SourceTask \
  --dataset-name NanoExample \
  --dataset-id hakari-bench/NanoExample \
  --split-name NanoSourceTask \
  --output-dir output/NanoExample \
  --dataset-config-dir config/datasets \
  --query-limit 200 \
  --doc-limit 10000 \
  --top-k 500 \
  --bm25-tokenizer whitespace
```

The output uses flat Nano config directories even when the input is nested. This
is intentional: uploaded Nano datasets should use split names as task/subset
names.

## Dataset YAML

When `--dataset-config-dir config/datasets` is supplied, the script writes or
updates a dataset YAML file such as `config/datasets/nanoexample.yaml`.

Generated YAML shape:

```yaml
name: NanoExample
dataset_id: hakari-bench/NanoExample
benchmark_kind: nano
corpus_config: corpus
queries_config: queries
qrels_config: qrels
candidate_config: reranking_hybrid
splits:
- NanoTask
metadata:
  language: unknown
  category: natural_language
  short_description: NanoExample Nano retrieval dataset.
  description: NanoExample is a Nano-set retrieval dataset generated from retrieval source tables.
```

If source metadata is known, pass `--metadata-json` with the final metadata
object. The object should satisfy the normal HAKARI dataset metadata
requirements: `language`, `category`, `short_description`, and `description`.

## README Template

Use [`NanoREADME.template.md`](NanoREADME.template.md) as the canonical dataset
README template. The converter writes `README.md` from this template and fills
the generated split paths, split statistics, split mapping, candidate coverage,
and candidate quality table from the parquet files and split metadata.

The template includes a fill checklist for maintainers. That checklist is only
for editing the template and must not remain in a published dataset README. The
generated README strips the checklist and should not contain any `{{...}}`
placeholders. Do not hand-maintain `dataset_info` metadata in the template;
leave it to `ds.push_to_hub()` and Hugging Face automatic dataset card
generation.

Before publishing, review the generated README and revise source-specific text
when needed:

- upstream benchmark name and source links
- source split policy
- skipped task list and reasons
- tokenizer policy if it differs by split
- BM25, Dense, and Hybrid candidate quality metrics if the dataset is used for
  reranking diagnostics
- the one-line safeguard definition for `reranking_hybrid`
- license and upstream attribution wording
- any source schema differences from the standard Nano layout

## Validation

Run focused tests during development:

```bash
uv run --group all pytest tests/test_nano_dataset_builder.py tests/test_create_nano_dataset_script.py -q
```

Run full validation before committing or uploading:

```bash
uv run tox
```

Before upload, verify:

- every config has the same split names
- every query id is unique
- every corpus id is unique
- query text has no exact duplicates within the split
- corpus text has no exact duplicates within the split
- qrels are positive-only and have no `score <= 0` rows
- every qrel references selected query and corpus ids
- every candidate row references an existing query
- every candidate `corpus-ids` value references an existing corpus id
- every candidate row has unique candidate ids
- `missing_positive_doc_count_after_forcing` is `0`, or the exception is
  documented in metadata and README
- candidate `candidate_coverage.query_coverage` and
  `candidate_coverage.relevant_coverage` are `1.0` for safeguarded reranking
  datasets
- the generated HAKARI dataset YAML points to the intended final dataset id

## Upload Shape

Upload four base `DatasetDict`s or equivalent parquet files:

- config `corpus`
- config `queries`
- config `qrels`
- config `bm25`

For reranking-hybrid Nano-sets, also upload:

- config `harrier_oss_v1_270m`
- config `reranking_hybrid`

Each config must expose the same Nano task/subset names as Hugging Face split
names. Do not upload a layout where each task is a separate config or where the
task name is hidden only in file paths.

Keep generated large artifacts under `output/` and do not commit them unless a
specific task asks for generated dataset artifacts to be versioned.
