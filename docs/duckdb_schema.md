# DuckDB Schema and Leaderboard Query Guide

This document describes how the HAKARI-Bench viewer stores leaderboard
data in DuckDB and how a viewer should query that data.

The current warehouse schema version is `7`. Version `7` makes top-ranking
artifacts the source for viewer metric recomputation and drops viewer
compatibility with older warehouse files.

The canonical source table for benchmark results is `task_results`. New DuckDB
builds also materialize `meta_database`, `schema_change_log`, and
`result_extensions` for schema evolution, `ingestion_batches` and
`source_load_state` for idempotent source tracking, `dim_model`, `dim_task`,
`dim_variant`, and `dim_metric` as canonical dimensions, `fact_task_score`,
which represents each leaderboard score target as rows such as `all` and
`reranking`, `fact_metric_score` for detailed metric values, and
`viewer_task_results`, a viewer-optimized table with the metadata join already
applied, `viewer_filter_values`, a precomputed filter-value mart, and
`viewer_leaderboard_rows`, a precomputed leaderboard standings mart for common
no-filter display modes, plus `viewer_leaderboard_language_options` for the
matching language filter choices. The HTMX leaderboard requires the current
schema and reads these mart tables or computes from `viewer_task_results`.
`runs` contains run-level metadata,
`metrics_long` contains task metrics recomputed from top-ranking artifacts for
full-corpus, reranking, and embedding-variant rows, `retrieval_rankings` contains
per-query top-100 retrieved document ids, `task_diagnostics` contains
analysis-oriented rerank, candidate, and latency fields, `dataset_metadata`
exposes YAML task metadata for language, category, citation, and text-stat
analysis, and `model_scores` /
`borda_task_scores` are precomputed tables used by the static HTML report. The
current HTMX viewer reads `task_diagnostics` / `dataset_metadata` for
paper-facing analysis panels. It does not read `model_scores`.

## Generation

Build the DuckDB database from benchmark JSON output:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/results \
  --duckdb-path output/results/hakari_bench.duckdb
```

Use `--incremental` for repeated local or deploy builds against an existing
DuckDB file. The builder compares source JSON hashes from `source_load_state`
with the current files and compares the model-card YAML manifest hash recorded
in `meta_database`. If nothing changed and no secondary outputs are requested,
with the current files and compares the model-card YAML manifest hash recorded
in `meta_database`. If nothing changed and no secondary outputs are requested,
it exits without rewriting the database. If only some source files changed or
new source files were added, it reuses unchanged canonical rows from the
existing DuckDB database and parses only the changed or added JSON files before
rewriting the canonical database. If source paths were removed, any model-card
YAML changed, or the existing database is missing or uses a different schema
version, it falls back to a full rebuild so stale rows cannot leak into the
regenerated warehouse.

Optional outputs and heavier offline-analysis tables are opt-in:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/results \
  --duckdb-path output/results/hakari_bench.duckdb \
  --html-output output/results/report.html \
  --parquet-output-dir output/results/parquet \
  --include-retrieval-rankings \
  --include-result-extensions
```

Multiple result roots can be merged by repeating `--results-dir`. Directory
order is the conflict-resolution policy: when two roots contain the same
logical `model_name`, benchmark, and task JSON, the first directory on the
command line wins. Later directories only fill missing model-task results.
Pass `--overwrite-result-duplicates` to invert that conflict policy so later
directories replace duplicate logical model-task rows from earlier directories.
Models can be omitted from the warehouse with repeated `--exclude-model-name`
options; this filters rows by the JSON `model.id` / DuckDB `model_name` value.
For local training outputs, set `model.id` to the intended unique experiment
identifier, such as `foobar_exp128`; `model_dir` is treated as a storage path,
not as part of the logical model identity.

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/results \
  --results-dir output/results_combined_20260510_1340 \
  --overwrite-result-duplicates \
  --exclude-model-name hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR \
  --duckdb-path output/results/hakari_bench.duckdb \
  --html-output output/results/report.html
```

For a strictly append-only update where new model-task JSON is stored in a
separate result root and the existing DuckDB should be reused directly, use
`--append-results-dir`. This mode reads only the append directory, inserts the
new canonical rows into the existing DuckDB, updates `source_load_state`, and
rebuilds SQL-derived viewer marts. It rejects duplicate result paths and
duplicate logical `(model_name, benchmark, dataset_id, task_key)` base rows.

```bash
uv run python scripts/build_results_database_and_report.py \
  --append-results-dir output/new_model_results \
  --duckdb-path output/results/hakari_bench.duckdb
```

The input files are:

- `output/results/{model_dir}/{huggingface_dataset_name}/{split_or_task}.json`:
  task-level benchmark results.
- `config/model_cards/*.yaml`: static HAKARI model metadata used to backfill
  missing model fields such as active parameters. Store one model card per file,
  using filenames such as `BAAI__bge-m3.yaml` for model id `BAAI/bge-m3`.
  Result JSON remains the primary source; model-card parameters are applied only
  when the model id matches, the total parameter count matches, and the result
  JSON is missing the derived value. `--model-cards-path` may also point at a
  legacy aggregate YAML file with a top-level `models` list. See
  `docs/model_cards.md` for the generation workflow.
- `artifacts.top_rankings` inside each task result JSON: per-query top-100
  ranking rows written by default. These embedded artifacts include both the
  ranked top-100 corpus ids and the binary qrels relevant corpus ids, so metrics
  such as nDCG@10, acc@1/10/100, MAP, MRR, precision, and recall can be
  recomputed later without re-running model inference. Legacy sidecar artifacts
  under `rankings/{split_or_task}.top100.json` are still readable.

`load_results()` determines `benchmark` from `target.dataset_id` and
`target.dataset_name` using `config/viewer/benchmarks.yaml`, then writes only
configured benchmark rows into `task_results`. When multiple result roots are
provided, it first selects one source JSON per logical
`(model_name, benchmark, dataset_id, task_key)` using the command-line
directory order. The base embedding result is stored as a row where
`embedding_variant_name IS NULL`. Derived embedding results from
`evaluation.embedding_evaluations` are stored as additional variant rows.
NanoMTEB family datasets are stored as distinct benchmark groups, separate from
the generic English `NanoMTEB` group, so official-family datasets such as
`NanoCMTEB`, `NanoJMTEB`, `NanoFaMTEB`, `NanoRuMTEB`, `NanoVNMTEB`, and
remaining `NanoMTEB-{language}` groups can be opened as individual viewer tabs
and included separately in grouped overall views. Mixed or separate-source
retrieval tasks are grouped as `NanoMTEB-Misc`; old `NanoMTEB-{language}` names
that were only broad language buckets are not accepted as compatibility aliases.
Run-level rows in `runs` are derived from these task JSON files; no aggregate
JSON file is required.

Each new task JSON includes `experiment_manifest`, a compact reproducibility
record with a SHA-256 fingerprint over model metadata, target metadata, runtime
config, and environment metadata. `task_results.experiment_fingerprint` copies
that fingerprint into DuckDB for SQL-based run comparison. Older JSON files
leave this column `NULL`.

When `--parquet-output-dir` is provided, the generator also writes Parquet
snapshots for the canonical tables: `meta_database`, `schema_change_log`,
`ingestion_batches`, `source_load_state`, `result_extensions`, `runs`,
`dim_model`, `dim_task`, `dim_variant`, `dim_metric`, `task_results`,
`fact_task_score`, `fact_metric_score`, `metrics_long`, `retrieval_rankings`,
`task_diagnostics`, `dataset_metadata`, `viewer_task_results`,
`viewer_filter_values`, `viewer_leaderboard_rows`,
`viewer_leaderboard_language_options`, `model_scores`, and `borda_task_scores`.
These files are intended for notebooks,
ad hoc DuckDB SQL with `read_parquet`, and external analysis workflows that do
not need the mutable DuckDB database file.

Start the web viewer with:

```bash
uv run hakari-bench web
```

By default, the viewer reads `output/viewer/hakari_bench.duckdb`. On each page
load, it copies a newer source database from the benchmark results directory
when one is available. Use `--source-results-dir` to point at another results
directory containing `hakari_bench.duckdb`, or `--source-duckdb-path` for an
explicit database path.

When the source is a Hugging Face dataset, the viewer checks/downloads it at
startup and then caches that source check for 10 minutes per process. During the
TTL window, page loads read the local DuckDB copy directly and skip
`hf_hub_download()`.

## Viewer Configuration

Leaderboard views are defined in YAML, not in DuckDB.

- `config/viewer/benchmarks.yaml`: benchmark views, dataset-name matching,
  display labels, excluded tasks, and benchmark-local score groups.
- `config/viewer/overall.yaml`: overall views and the benchmarks included in
  each overall view.

Main `benchmarks.yaml` fields:

| field | meaning |
| --- | --- |
| `name` | View name. Must match `task_results.benchmark`. |
| `label` | UI label. Defaults to `name`. |
| `matches` | Optional string patterns matched against `{dataset_id}/{dataset_name}` when building DuckDB. Defaults to `[name]`. If multiple benchmarks match, the longest pattern wins. |
| `include_in_overall` | Descriptive metadata. Actual overall composition is defined by `overall.yaml`. |
| `excluded_tasks` | Task names or task keys excluded from ranking. Matched against `task_name` and `task_key`. |
| `score_groups` | Benchmark-local scoring units and optional metric columns. The selected group controls benchmark-view `Mean Score`, Borda, and rank; when `task_scores=1`, the same group also controls the displayed metric columns. |
| `task_labels` | Optional display-only labels for task metric columns, keyed by task name, split name, task key, or the computed metric column key. Use this for compact source splits whose raw task names are ambiguous, such as `NanoMTEB-Misc` `en` -> `EuroPIRQ-en`. |

`score_groups[].group_by` and `overall.yaml` `group_by` can use these values:

| `group_by` | source column |
| --- | --- |
| `task_key` | `task_results.task_key` |
| `dataset_name` | `task_results.dataset_name` |
| `dataset_id` | `task_results.dataset_id` |
| `split_name` | `COALESCE(task_results.split_name, '')` |
| `benchmark` | `task_results.benchmark` |
| `task_name` | `task_results.task_name` |

Unknown `group_by` values and unknown YAML keys are rejected at viewer config
load time.

## HTMX Viewer Query Surfaces

The web viewer exposes four user-facing query surfaces over the DuckDB file:

| UI surface | source tables | semantics |
| --- | --- | --- |
| Summary cards | `task_results`, `dataset_metadata` | Counts distinct models, benchmarks, tasks, languages, base result rows, variant rows, and the latest available evaluation timestamp. |
| Leaderboard | `viewer_task_results`, `fact_metric_score` | Computes Borda and mean scores from complete model-task matrices for the selected YAML view. The `Target` selector filters `score_target`; `All` uses full-corpus retrieval scores, `Reranking` uses materialized `reranking_hybrid` rerank scores plus the BM25 candidate-order baseline from `score_target = 'all'`, and `Reranking without safeguard` removes the optional rank-101 safeguard positive before recomputing metrics. The default JSON metrics are `nDCG@10` and `acc@100`; other viewer metrics are computed from embedded top-ranking artifacts during DuckDB creation. It uses `viewer_task_results.score` for `nDCG@10` and joins `fact_task_score` to `fact_metric_score` for other displayed metrics. Base rows are used unless the user explicitly enables variant categories; reranking can include embedding variants when their candidate-rerank artifact rows are available. |
| Variant impact | `task_results` | Joins each embedding variant row to the matching base row by `(model_name, benchmark, task_key)` and reports mean score plus relative delta versus base. This is intended for quantization-first comparisons; rescore and `truncate_dim` variants are hidden unless explicitly enabled in the panel. |
| Reranking diagnostics | `task_diagnostics` | Aggregates candidate coverage and rerank lift by benchmark for the selected YAML view. |
| Dataset diagnostics | `dataset_metadata`, `task_results` | Aggregates task metadata, query/document sample sizes, text lengths, and the fraction of base rows with `score >= 0.95` as a saturation signal. |

Analysis panels are scoped by the same YAML view selection as the leaderboard.
Configured overall views (`All`, `Core`, and `Group`) expand to their configured
benchmark components before querying. The diagnostics panels are descriptive and
do not alter leaderboard ranking.

## Table Overview

### `meta_database`

`meta_database` records the current warehouse schema contract. Consumers should
check this table before relying on newer canonical tables.

| column | type | meaning |
| --- | --- | --- |
| `schema_version` | `VARCHAR` | Current warehouse schema version. |
| `compatibility_level` | `VARCHAR` | Compatibility contract exposed by this DB. Current builds are `current`. |
| `built_at_utc` | `VARCHAR` | Build timestamp. |
| `source_result_count` | `INTEGER` | Number of source result files represented in this DB. |
| `model_cards_path` | `VARCHAR` | Static model-card YAML file or directory path used for this build, or `NULL` when disabled or missing. |
| `model_cards_sha256` | `VARCHAR` | SHA-256 hash of the model-card file, or a stable manifest hash for a model-card directory. Incremental builds require this to match before cached rows can be reused. |

### `schema_change_log`

`schema_change_log` records schema migrations applied to the generated DB. The
current full writer emits one row for the current schema; future incremental
migrations can append rows here.

| column | type | meaning |
| --- | --- | --- |
| `schema_version` | `VARCHAR` | Schema version after the migration. |
| `migration_name` | `VARCHAR` | Migration or build-step name. |
| `applied_at_utc` | `VARCHAR` | Migration timestamp. |
| `parser_version` | `VARCHAR` | Parser/build logic version used for the migration. |
| `compatibility_level` | `VARCHAR` | Compatibility contract after the migration. |

### `result_extensions`

`result_extensions` preserves unknown top-level fields from source task JSON
when database generation is run with `--include-result-extensions`. The default
viewer database build leaves this table empty to avoid re-reading every result
JSON during deploys. Extension discovery keeps additive JSON changes from being
silently discarded before the field is promoted to a canonical column or table.
Known top-level result sections such as `model`, `target`, `evaluation`,
`metrics`, `config`, `environment`, `experiment_manifest`,
`embedding_evaluations`, and `artifacts` are excluded.

| column | type | meaning |
| --- | --- | --- |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `field_path` | `VARCHAR` | JSONPath-like field path, currently for top-level fields such as `$.future_payload`. |
| `value_json` | `VARCHAR` | Compact JSON representation of the unknown value. |
| `discovered_batch_id` | `VARCHAR` | Batch id that discovered the extension field. |
| `discovered_at_utc` | `VARCHAR` | Discovery timestamp. |

### `ingestion_batches`

`ingestion_batches` records the source-tracking state for the latest DuckDB
build. The current writer still rebuilds the physical DuckDB file, but it
compares incoming source hashes with the previous `source_load_state` before
rewriting tables. Re-running the same inputs against the same database records
`changed_count = 0`, which is the detection layer needed for later
delete/insert incremental updates.

| column | type | meaning |
| --- | --- | --- |
| `batch_id` | `VARCHAR` | Build or ingestion batch id. When not provided, the writer derives one from source hashes and the load timestamp. |
| `started_at_utc` | `VARCHAR` | Batch start timestamp. |
| `finished_at_utc` | `VARCHAR` | Batch finish timestamp. |
| `status` | `VARCHAR` | Batch status. Current successful builds write `success`. |
| `source_count` | `INTEGER` | Number of distinct task JSON result paths represented in the build. |
| `changed_count` | `INTEGER` | Number of source paths whose payload hash differs from the previous database state. |

### `source_load_state`

`source_load_state` stores the latest known hash for each task JSON result
path. It intentionally tracks source files rather than model/task scores so
the loader can distinguish unchanged files from changed reruns before touching
canonical facts.

| column | type | meaning |
| --- | --- | --- |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `payload_sha256` | `VARCHAR` | SHA-256 hash of the result JSON file when the file is available locally, otherwise `NULL`. |
| `canonical_key_hash` | `VARCHAR` | Stable hash of the source identity used for future incremental bookkeeping. |
| `last_successful_batch_id` | `VARCHAR` | Batch id that last loaded this source. |
| `loaded_at_utc` | `VARCHAR` | Load timestamp for this source state row. |

### `task_results`

`task_results` is the canonical leaderboard source. Each row is one score for
one model, one benchmark task, and one embedding variant. Base results use
`embedding_variant_name IS NULL`.

| column | type | meaning |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | Directory name under `output/results/{model_dir}`. |
| `model_name` | `VARCHAR` | `model.id` from result JSON, or `model_dir` when absent. |
| `model_revision` | `VARCHAR` | Resolved Hugging Face model revision, stored as a short commit SHA when available. Existing result JSON may leave this `NULL`. |
| `model_revision_requested` | `VARCHAR` | Requested Hugging Face model revision from the run, or `NULL` when not specified or unavailable. |
| `benchmark` | `VARCHAR` | Viewer benchmark group, such as `MNanoBEIR` or `NanoJMTEB`. |
| `dataset_id` | `VARCHAR` | `target.dataset_id`, usually a Hugging Face dataset repo. |
| `dataset_revision` | `VARCHAR` | Resolved dataset revision, usually a commit SHA. |
| `dataset_revision_requested` | `VARCHAR` | Requested revision from the run, or `NULL` when not specified. |
| `dataset_name` | `VARCHAR` | `target.dataset_name`. |
| `split_name` | `VARCHAR` | `target.split_name`; may be `NULL` for unsplit tasks. |
| `task_name` | `VARCHAR` | `target.task_name`, or `split_name` when task name is missing. |
| `task_key` | `VARCHAR` | Ranking task identity. Generated as `{benchmark}::{dataset_id}::{task_name}` after task-name canonicalization. |
| `score` | `DOUBLE` | Raw aggregate score, usually a 0.0 to 1.0 nDCG-style value. |
| `score_100` | `DOUBLE` | `score * 100.0`, used for display. |
| `aggregate_metric` | `VARCHAR` | `evaluation.aggregate_metric`, such as `ndcg@10`. |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `experiment_fingerprint` | `VARCHAR` | SHA-256 fingerprint from `experiment_manifest`, derived from model, target, config, and environment metadata. |
| `active_parameters` | `BIGINT` | Active parameter count, or `NULL` if unavailable. |
| `total_parameters` | `BIGINT` | Total parameter count, or `NULL` if unavailable. |
| `max_seq_length` | `INTEGER` | Model maximum sequence length. |
| `dtype` | `VARCHAR` | Evaluation dtype, such as `bf16`. |
| `embedding_variant_name` | `VARCHAR` | Derived embedding variant name. Base result rows use `NULL`. |
| `embedding_dim` | `INTEGER` | Embedding dimension for this row. May be present on base rows. |
| `quantization` | `VARCHAR` | Quantization precision, such as `int8`, `uint8`, or `ubinary`. |
| `attn_implementation` | `VARCHAR` | Attention implementation, such as `flash_attention_2`. |
| `query_prompt` | `VARCHAR` | Explicit query prompt/prefix from `config.query_prompt`, such as `query: `. |
| `document_prompt` | `VARCHAR` | Explicit document prompt/prefix from `config.document_prompt`, such as `passage: `. |
| `query_prompt_name` | `VARCHAR` | Query prompt name from `config.query_prompt_name`, such as `query`. |
| `document_prompt_name` | `VARCHAR` | Document prompt name from `config.document_prompt_name`, such as `document`. |
| `query_encode_task` | `VARCHAR` | Query encode task hint from `config.query_encode_task`, when used by model-specific encoders. |
| `document_encode_task` | `VARCHAR` | Document encode task hint from `config.document_encode_task`, when used by model-specific encoders. |
| `trust_remote_code` | `BOOLEAN` | Whether model loading used Hugging Face `trust_remote_code`. |
| `late_interaction_query_length`, `late_interaction_document_length` | `INTEGER` | ColBERT/late-interaction query and document token lengths from `evaluation.late_interaction` or `model.late_interaction`. |
| `late_interaction_query_prefix`, `late_interaction_document_prefix` | `VARCHAR` | ColBERT/late-interaction query and document prefixes used by the run. |
| `late_interaction_query_expansion`, `late_interaction_attend_to_expansion_tokens` | `BOOLEAN` | Late-interaction query expansion and expansion-token attention flags when available. |
| `torch_version` | `VARCHAR` | Torch version used for evaluation. |
| `transformers_version` | `VARCHAR` | Transformers version used for evaluation. |
| `sentence_transformers_version` | `VARCHAR` | Sentence Transformers version used for evaluation. |
| `started_at_utc` | `VARCHAR` | Task evaluation start time as a UTC ISO string. |
| `finished_at_utc` | `VARCHAR` | Task evaluation finish time as a UTC ISO string. |
| `evaluated_at_utc` | `VARCHAR` | Evaluation completion time. Older JSON may only have this timestamp. |
| `duration_seconds_including_dataset_load` | `DOUBLE` | Task duration including dataset loading. |
| `wall_seconds` | `DOUBLE` | Task evaluation wall time in seconds. |

### `dim_model`

`dim_model` contains one deterministic model identity row for each distinct
`model_dir`, `model_name`, and model revision tuple observed in
`task_results`. The integer `model_id` is assigned by sorted natural key so
rebuilding the same inputs produces stable ids.

| column | type | meaning |
| --- | --- | --- |
| `model_id` | `BIGINT` | Deterministic model dimension id. |
| `model_dir` | `VARCHAR` | Directory name under `output/results/{model_dir}`. |
| `model_name` | `VARCHAR` | Model name from result JSON. |
| `model_revision` | `VARCHAR` | Resolved model revision, when available. |
| `model_revision_requested` | `VARCHAR` | Requested model revision, when available. |
| `active_parameters` | `BIGINT` | Active parameter count. |
| `total_parameters` | `BIGINT` | Total parameter count. |
| `max_seq_length` | `INTEGER` | Model maximum sequence length. |
| `dtype` | `VARCHAR` | Evaluation dtype. |
| `attn_implementation` | `VARCHAR` | Attention implementation. |
| `torch_version` | `VARCHAR` | Torch version. |
| `transformers_version` | `VARCHAR` | Transformers version. |
| `sentence_transformers_version` | `VARCHAR` | Sentence Transformers version. |

### `dim_task`

`dim_task` contains one deterministic task identity row for each distinct
`benchmark`, `dataset_id`, and `task_key` tuple observed in `task_results`.
Task identity is separated from mutable display metadata such as language,
category, citations, and dataset statistics.

| column | type | meaning |
| --- | --- | --- |
| `task_id` | `BIGINT` | Deterministic task dimension id. |
| `benchmark` | `VARCHAR` | Viewer benchmark group. |
| `dataset_id` | `VARCHAR` | Dataset id. |
| `dataset_revision` | `VARCHAR` | Resolved dataset revision, when available. |
| `dataset_revision_requested` | `VARCHAR` | Requested dataset revision, when available. |
| `dataset_name` | `VARCHAR` | Dataset name from result JSON. |
| `split_name` | `VARCHAR` | Split name normalized to an empty string when absent. |
| `task_name` | `VARCHAR` | Canonical task name. |
| `task_key` | `VARCHAR` | Canonical ranking task identity. |
| `language` | `VARCHAR` | Primary task language from metadata. |
| `languages` | `VARCHAR[]` | Task languages from metadata. |
| `category` | `VARCHAR` | Task category from metadata. |
| `short_description` | `VARCHAR` | Short task description from metadata. |
| `citation_count` | `INTEGER` | Number of citation records. |
| `reference_count` | `INTEGER` | Number of references. |
| `has_bibtex` | `BOOLEAN` | Whether metadata has BibTeX. |
| `query_count` | `INTEGER` | Number of sampled or configured queries. |
| `document_count` | `INTEGER` | Number of sampled or configured documents. |
| `query_mean_chars` | `DOUBLE` | Mean query text length. |
| `document_mean_chars` | `DOUBLE` | Mean document text length. |

### `dim_variant`

`dim_variant` contains one deterministic embedding variant row for each
distinct `embedding_variant_name`, `embedding_dim`, and `quantization` tuple
observed in `task_results`. The `variant_key` includes all three values so base
rows with different embedding dimensions do not collide.

| column | type | meaning |
| --- | --- | --- |
| `variant_id` | `BIGINT` | Deterministic variant dimension id. |
| `variant_key` | `VARCHAR` | Natural key in `{name}:{dim}:{quantization}` form, using `base` and `none` for missing values. |
| `embedding_variant_name` | `VARCHAR` | Derived embedding variant name. Base rows use `NULL`. |
| `embedding_dim` | `INTEGER` | Embedding dimension for the row. |
| `quantization` | `VARCHAR` | Quantization precision. |
| `is_base` | `BOOLEAN` | Whether this variant represents a base embedding result. |

### `dim_metric`

`dim_metric` contains one deterministic row for each metric name in
`metrics_long`. The writer parses common IR metric names into a metric family
and cutoff, so new cutoffs such as `recall@100` can be stored without adding
columns. Reranking metric names keep their original `_reranking_hybrid_top..._rerank_`
marker so the viewer can distinguish them from full-corpus metrics with the
same family and cutoff while allowing the candidate subset depth to vary.

| column | type | meaning |
| --- | --- | --- |
| `metric_id` | `BIGINT` | Deterministic metric dimension id. |
| `metric_name` | `VARCHAR` | Original metric name from result JSON after canonicalization. |
| `metric_family` | `VARCHAR` | Parsed metric family such as `ndcg`, `recall`, or `map`, when available. |
| `cutoff` | `INTEGER` | Parsed cutoff after `@`, when available. |

### `fact_task_score`

`fact_task_score` is the forward-compatible score fact table. It keeps the
default full-corpus score and candidate-reranking score in the same row shape
with a `score_target` discriminator instead of adding one score column per
target. `score_target = 'all'` rows are copied from `task_results.score`.
Base `score_target = 'reranking'` rows are copied from
`task_diagnostics.rerank_score` when the diagnostic row is available for
`reranking_hybrid` reranking. Embedding-variant reranking rows are derived from
`artifacts.top_rankings` `candidate_rerank` rows whose score name matches the
variant's selected retrieval score. `score_target =
'reranking_without_safeguard'` rows are derived during DuckDB creation from
`artifacts.top_rankings` by removing each query's optional rank-101 safeguard
positive before recomputing metrics for both base rows and available embedding
variants. The viewer also adds the BM25 `score_target = 'all'` rows as the
candidate-order baseline in `Reranking` displays, unless the DuckDB build has
already materialized BM25 rows for `score_target = 'reranking'`.

| column | type | meaning |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | Directory name under `output/results/{model_dir}`. |
| `model_name` | `VARCHAR` | Model display/name identity. |
| `model_revision` | `VARCHAR` | Resolved model revision, when available. |
| `model_revision_requested` | `VARCHAR` | Requested model revision, when available. |
| `benchmark` | `VARCHAR` | Viewer benchmark group. |
| `dataset_id` | `VARCHAR` | Dataset id. |
| `dataset_revision` | `VARCHAR` | Resolved dataset revision, when available. |
| `dataset_revision_requested` | `VARCHAR` | Requested dataset revision, when available. |
| `dataset_name` | `VARCHAR` | Dataset name from result JSON. |
| `split_name` | `VARCHAR` | Split name, or `NULL`. |
| `task_name` | `VARCHAR` | Canonical task name. |
| `task_key` | `VARCHAR` | Canonical ranking task identity. |
| `score_target` | `VARCHAR` | Score target such as `all` or `reranking`. |
| `score` | `DOUBLE` | Raw aggregate score for the target. |
| `score_100` | `DOUBLE` | `score * 100.0`, used for display. |
| `aggregate_metric` | `VARCHAR` | Aggregate metric name, such as `ndcg@10`. |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `experiment_fingerprint` | `VARCHAR` | Run fingerprint copied from `task_results`. |
| `active_parameters` | `BIGINT` | Active parameter count. |
| `total_parameters` | `BIGINT` | Total parameter count. |
| `max_seq_length` | `INTEGER` | Model maximum sequence length. |
| `dtype` | `VARCHAR` | Evaluation dtype. |
| `embedding_variant_name` | `VARCHAR` | Embedding variant name, or `NULL` for base rows. |
| `embedding_dim` | `INTEGER` | Embedding dimension. |
| `quantization` | `VARCHAR` | Quantization precision. |
| `attn_implementation` | `VARCHAR` | Attention implementation copied from `task_results`. |
| `query_prompt` | `VARCHAR` | Explicit query prompt/prefix from `task_results`. |
| `document_prompt` | `VARCHAR` | Explicit document prompt/prefix from `task_results`. |
| `query_prompt_name` | `VARCHAR` | Query prompt name from `task_results`. |
| `document_prompt_name` | `VARCHAR` | Document prompt name from `task_results`. |
| `query_encode_task` | `VARCHAR` | Query encode task hint from `task_results`. |
| `document_encode_task` | `VARCHAR` | Document encode task hint from `task_results`. |
| `trust_remote_code` | `BOOLEAN` | Whether model loading used Hugging Face `trust_remote_code`. |
| `late_interaction_query_length`, `late_interaction_document_length` | `INTEGER` | Late-interaction query and document lengths copied from `task_results`. |
| `late_interaction_query_prefix`, `late_interaction_document_prefix` | `VARCHAR` | Late-interaction prefixes copied from `task_results`. |
| `late_interaction_query_expansion`, `late_interaction_attend_to_expansion_tokens` | `BOOLEAN` | Late-interaction expansion flags copied from `task_results`. |
| `candidate_source` | `VARCHAR` | Candidate source for reranking rows, otherwise `NULL`. |
| `candidate_ranking` | `VARCHAR` | Candidate ranking label such as `bm25`, otherwise `NULL`. |
| `rerank_top_k` | `INTEGER` | Candidate depth for reranking rows, otherwise `NULL`. |
| `rerank_status` | `VARCHAR` | Reranking availability status, otherwise `NULL`. |
| `started_at_utc` | `VARCHAR` | Task evaluation start time. |
| `finished_at_utc` | `VARCHAR` | Task evaluation finish time. |
| `evaluated_at_utc` | `VARCHAR` | Evaluation completion time. |

### `runs`

`runs` is built from task JSON files and stores model/run-level summaries. It
is not used for rank computation, but it is useful for model metadata and run
completeness displays.

| column | type | meaning |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | Directory name under `output/results/{model_dir}`. |
| `model_name` | `VARCHAR` | `model.id` from task JSON, or `model_dir` when absent. |
| `generated_at_utc` | `VARCHAR` | Latest task JSON generation time for the model. |
| `started_at_utc` | `VARCHAR` | Earliest task evaluation start time for the model. |
| `finished_at_utc` | `VARCHAR` | Latest task evaluation finish time for the model. |
| `target_count` | `INTEGER` | Number of distinct target datasets. |
| `split_count` | `INTEGER` | Number of task result JSON files. |
| `cache_hit_count` | `INTEGER` | Number of task cache hits when task JSON contains `evaluation.cache_hit`; otherwise `NULL`. |
| `evaluated_count` | `INTEGER` | Number of evaluated tasks when task JSON contains `evaluation.cache_hit`; otherwise `NULL`. |
| `aggregate_metric_mean` | `DOUBLE` | Mean of task `evaluation.aggregate_metric_value` values. |
| `active_parameters` | `BIGINT` | Model active parameter count. |
| `total_parameters` | `BIGINT` | Model total parameter count. |
| `max_seq_length` | `INTEGER` | Model maximum sequence length. |
| `dtype` | `VARCHAR` | Evaluation dtype. |
| `attn_implementation` | `VARCHAR` | Attention implementation. |
| `torch_version` | `VARCHAR` | Torch version. |
| `transformers_version` | `VARCHAR` | Transformers version. |
| `sentence_transformers_version` | `VARCHAR` | Sentence Transformers version. |

### `metrics_long`

`metrics_long` is a long-format representation of metrics computed while
building DuckDB. The builder reads each result's top-ranking artifact, combines
the ranked corpus ids with artifact qrels, and computes the viewer metric set
for the selected full-corpus, reranking, and embedding-variant rankings. The
small task JSON `metrics` and `rerank_metrics` dictionaries are fallback inputs
for summary values, not the source of the full viewer metric set.

| column | type | meaning |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | Model output directory. |
| `model_name` | `VARCHAR` | Model name. |
| `benchmark` | `VARCHAR` | Benchmark group. |
| `dataset_id` | `VARCHAR` | Dataset id. |
| `task_name` | `VARCHAR` | Task name. |
| `metric_name` | `VARCHAR` | Metric name, such as `NanoJaCWIR_ndcg@10`. |
| `metric_value` | `DOUBLE` | Metric value. |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `score_target` | `VARCHAR` | `all` for full-corpus retrieval, `reranking` for `reranking_hybrid` with safeguard, or `reranking_without_safeguard` with the optional rank-101 safeguard positive removed. |
| `embedding_variant_name` | `VARCHAR` | Embedding variant name, or `NULL` for base rows. |

### `fact_metric_score`

`fact_metric_score` is the normalized metric-value fact table derived from
`metrics_long` and `dim_metric`. It keeps detailed metrics separate from the
primary leaderboard score in `fact_task_score`. For `Target: All`, the viewer
uses metric names that do not contain `_reranking_hybrid_top`. For
`Target: Reranking` and `Target: Reranking without safeguard`, the viewer uses
metric rows with the selected reranking `score_target` and metric names that
contain `_reranking_hybrid_top`.

| column | type | meaning |
| --- | --- | --- |
| `metric_id` | `BIGINT` | Foreign-key-style id from `dim_metric`. |
| `model_dir` | `VARCHAR` | Model output directory. |
| `model_name` | `VARCHAR` | Model name. |
| `benchmark` | `VARCHAR` | Benchmark group. |
| `dataset_id` | `VARCHAR` | Dataset id. |
| `task_name` | `VARCHAR` | Task name. |
| `metric_value` | `DOUBLE` | Metric value. |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `score_target` | `VARCHAR` | Metric target matching `fact_task_score.score_target`. |
| `embedding_variant_name` | `VARCHAR` | Metric variant matching `fact_task_score.embedding_variant_name`. |

### `retrieval_rankings`

`retrieval_rankings` is a normalized view of top-100 ranking artifact
JSON. It is populated only when database generation is run with
`--include-retrieval-rankings`. The default viewer database build reads these
artifacts to recompute metrics but leaves this table empty to avoid expanding
large per-query ranking artifacts during leaderboard deploys.
It is intended for offline metric recomputation, rank-fusion experiments, hybrid
search simulations, and reranker candidate analysis. It is not used for
leaderboard ranking. The source artifact also stores qrels rows with
`query_id` and `relevant_corpus_ids`; the current normalized table contains the
ranking rows only.

| column | type | meaning |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | Model output directory. |
| `model_name` | `VARCHAR` | Model name. |
| `benchmark` | `VARCHAR` | Benchmark group. |
| `dataset_id` | `VARCHAR` | Dataset id. |
| `dataset_revision` | `VARCHAR` | Resolved dataset revision, when recorded. |
| `dataset_name` | `VARCHAR` | Dataset name. |
| `split_name` | `VARCHAR` | Split name. |
| `task_name` | `VARCHAR` | Task name. |
| `task_key` | `VARCHAR` | Ranking task identity. |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `ranking_path` | `VARCHAR` | Source top-100 ranking artifact path. |
| `ranking_name` | `VARCHAR` | Ranking label, such as `base`, variant name, `bm25`, or `reranker`. |
| `ranking_kind` | `VARCHAR` | Ranking type, such as `retrieval` or `candidate_rerank`. |
| `embedding_variant_name` | `VARCHAR` | Embedding variant name, or `NULL` for base rows. |
| `distance` | `VARCHAR` | Distance or scorer label, such as `dot`, `cosine`, `bm25`, or `reranker`. |
| `score_name` | `VARCHAR` | Metric score prefix used by the evaluation. |
| `query_id` | `VARCHAR` | Query id. |
| `rank` | `INTEGER` | One-based rank within the saved top-100 list. |
| `corpus_id` | `VARCHAR` | Retrieved corpus document id. |

### `task_diagnostics`

`task_diagnostics` is a notebook-friendly table for analyzing why a model did
or did not improve under BM25 candidate reranking. The viewer also uses
`rerank_score` for the optional `Target: Reranking` leaderboard mode when
`rerank_status = 'available'`, `candidate_ranking = 'bm25'`, and
`rerank_top_k = 100` where those columns are present.

| column | type | meaning |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | Model output directory. |
| `model_name` | `VARCHAR` | Model name. |
| `benchmark` | `VARCHAR` | Benchmark group. |
| `dataset_id` | `VARCHAR` | Dataset id. |
| `task_name` | `VARCHAR` | Task name. |
| `task_key` | `VARCHAR` | Ranking task identity. |
| `result_path` | `VARCHAR` | Source task JSON path. |
| `base_score` | `DOUBLE` | Base retrieval aggregate score. |
| `rerank_score` | `DOUBLE` | Candidate-reranked aggregate score, or `NULL` when unavailable. |
| `rerank_lift` | `DOUBLE` | `rerank_score - base_score`, or `NULL`. |
| `rerank_status` | `VARCHAR` | Rerank availability status from result JSON. |
| `rerank_top_k` | `INTEGER` | Candidate depth used for reranking. |
| `candidate_source` | `VARCHAR` | Candidate source label, usually `dataset_candidate_subset`. |
| `candidate_ranking` | `VARCHAR` | Configured candidate ranking, usually `bm25`. |
| `bm25_source` | `VARCHAR` | BM25 source metadata, such as `dataset_candidate_subset` or `computed_bm25s`. |
| `query_coverage` | `DOUBLE` | Fraction of qrels-bearing queries with at least one relevant document in top-k candidates. |
| `relevant_coverage` | `DOUBLE` | Fraction of relevant documents covered by top-k candidates. |
| `covered_query_count` | `INTEGER` | Count of qrels-bearing queries covered by candidates. |
| `query_with_relevance_count` | `INTEGER` | Count of queries with at least one relevant document. |
| `covered_relevant_count` | `INTEGER` | Count of relevant documents found in top-k candidates. |
| `relevant_count` | `INTEGER` | Total relevant document count in qrels. |
| `dataset_load_seconds` | `DOUBLE` | Dataset load time. |
| `query_embedding_seconds` | `DOUBLE` | Query encoding time. |
| `corpus_embedding_seconds` | `DOUBLE` | Corpus encoding time. |
| `score_and_topk_seconds` | `DOUBLE` | Retrieval score and top-k time. |
| `metric_compute_seconds` | `DOUBLE` | Metric computation time. |
| `pure_compute_seconds` | `DOUBLE` | Compute duration excluding dataset load. |
| `wall_seconds` | `DOUBLE` | Task evaluation wall time. |
| `duration_seconds_including_dataset_load` | `DOUBLE` | End-to-end task duration including dataset loading. |

### `dataset_metadata`

`dataset_metadata` is derived from built-in dataset YAML and keyed by
`task_key`. Join it to `task_results` or `task_diagnostics` to score models by
language, category, citation coverage, or text length profile.

| column | type | meaning |
| --- | --- | --- |
| `benchmark` | `VARCHAR` | Benchmark group. |
| `dataset_id` | `VARCHAR` | Dataset id. |
| `dataset_name` | `VARCHAR` | Dataset name. |
| `split_name` | `VARCHAR` | Split name. |
| `task_name` | `VARCHAR` | Task name. |
| `task_key` | `VARCHAR` | Ranking task identity. |
| `language` | `VARCHAR` | Primary metadata language code, or `multilingual`. |
| `languages` | `VARCHAR[]` | Main detected language codes for the task, copied from YAML `metadata.languages`. Falls back conceptually to `[language]` for older metadata. |
| `category` | `VARCHAR` | Metadata category, such as `natural_language` or `code`. |
| `short_description` | `VARCHAR` | Short human-readable task description. |
| `citation_count` | `INTEGER` | Number of citation keys recorded for the task. |
| `reference_count` | `INTEGER` | Number of reference entries recorded for the task. |
| `has_bibtex` | `BOOLEAN` | Whether the task metadata includes BibTeX. |
| `query_count` | `INTEGER` | Query count from YAML text stats. |
| `document_count` | `INTEGER` | Corpus document count from YAML text stats. |
| `query_mean_chars` | `DOUBLE` | Mean query length in characters. |
| `document_mean_chars` | `DOUBLE` | Mean document length in characters. |

### `model_scores`

`model_scores` is a precomputed standings table written by
`scripts/build_results_database_and_report.py` for the static HTML report. It
is generated from base rows only.

The current HTMX viewer does not use this table. To match the viewer, compute
from `task_results` using the SQL recipes below or the `LeaderboardService`
logic. In particular, tie behavior differs in older static report helpers:
the viewer uses competition rank (`1, 2, 2, 4`) for leaderboard ranks.

| column | type | meaning |
| --- | --- | --- |
| `view_name` | `VARCHAR` | Configured overall view name, such as `All`, `Core`, or `Group`, or a benchmark view name. |
| `model_name` | `VARCHAR` | Model name. |
| `task_count` | `INTEGER` | Number of tasks used for ranking. |
| `mean_score` | `DOUBLE` | Mean score on a 0 to 100 scale. |
| `score_rank` | `DOUBLE` | Rank by `mean_score`. |
| `borda_score` | `DOUBLE` | Mean per-task Borda score. |
| `borda_rank` | `DOUBLE` | Rank by `borda_score`. |
| `active_parameters` | `BIGINT` | Active parameter count. |
| `total_parameters` | `BIGINT` | Total parameter count. |
| `max_seq_length` | `INTEGER` | Maximum sequence length. |
| `dtype` | `VARCHAR` | Evaluation dtype. |
| `attn_implementation` | `VARCHAR` | Attention implementation. |
| `torch_version` | `VARCHAR` | Torch version. |
| `transformers_version` | `VARCHAR` | Transformers version. |
| `sentence_transformers_version` | `VARCHAR` | Sentence Transformers version. |

### `borda_task_scores`

`borda_task_scores` stores precomputed per-task Borda details for the static
HTML report. The current HTMX viewer does not use it.

| column | type | meaning |
| --- | --- | --- |
| `view_name` | `VARCHAR` | Configured overall view name, such as `All`, `Core`, or `Group`, or a benchmark view name. |
| `model_name` | `VARCHAR` | Model name. |
| `benchmark` | `VARCHAR` | Benchmark group. |
| `task_key` | `VARCHAR` | Task identity. |
| `rank` | `DOUBLE` | Score rank within the task. |
| `model_count` | `INTEGER` | Number of complete models participating in the task. |
| `borda_score` | `DOUBLE` | Borda score for this task. |
| `score` | `DOUBLE` | Raw task score. |

## Leaderboard Semantics

### Score and Rank

- Task score is `task_results.score`.
- Display means are computed from `score * 100.0`.
- Per-task ranks are competition ranks over score descending. Tied models share
  the same rank, and the next rank skips ahead.
- Per-task Borda score is:

```text
100                              when model_count <= 1
100 * (model_count - rank) / (model_count - 1) otherwise
```

A model's `borda_score` is the mean of its per-task Borda scores within the
selected view. `borda_rank` ranks `borda_score` descending. `mean_rank` ranks
`mean_score` descending.

Borda should stay within `0..100` as long as each model identity is unique
within each task. If a viewer collapses multiple embedding variants into the
same displayed model key, the `rank` and `model_count` populations can diverge
and produce invalid values. The current viewer avoids this by expanding
colliding variant display names.

### Complete Model Rule

Only models that have every expected task in the selected view are ranked.

1. Apply benchmark filtering and `excluded_tasks`.
2. Apply embedding variant display settings.
3. Build the expected task set from the remaining rows.
4. Keep only models whose task-key set exactly matches the expected task set.

For overall views with configured grouped components, such as `Core` and
`Group`, the viewer first checks raw task completeness within each
model/benchmark pair, then aggregates rows by the configured group key, and
finally applies the complete model rule again to the aggregated task set.

### Benchmark and Overall Views

For benchmark views, `mean_score` is the mean of all task scores in that
benchmark.

For overall views:

- `All`: all configured benchmark views using raw task rows.
- `Core`: a compact curated set covering broad multilingual retrieval,
  multilingual BEIR, English RTEB domains, multilingual long-document
  retrieval, reasoning-heavy retrieval, and code retrieval
  (`MNanoBEIR`, `NanoMMTEB-v2`, `NanoRTEB`, `NanoMLDR`, `NanoBRIGHT`, and
  `NanoCoIR`). `MNanoBEIR` is grouped by `task_name` in Core so each BEIR
  source task contributes once after averaging language variants.
- `Group`: all configured benchmark views aggregated by each component's
  `group_by` setting before ranking.
- `micro_mean`: mean over all included tasks with equal task weight.
- `macro_mean`: mean of benchmark-level means with equal benchmark weight.
- `mean_score`: `macro_mean` for overall views, task mean for benchmark views.

`All` uses raw `task_key` values. `Core` and `Group` use any component-level
`group_by` settings from `overall.yaml` to average tasks into benchmark-local
units before computing Borda and means. For task x language collections such as
`MNanoBEIR`, Core and Group use the underlying task name (`task_name`) as the
grouped unit.

Grouped overall views also expose the aggregated benchmark-local units as
metric columns. These columns use the aggregated `task_key` values, such as
`NanoMTEB-German::Banking77Classification`, and can be sorted with the
`metric:<task_key>` sort key. Non-grouped overall views keep metric columns
disabled to avoid expanding the table to every raw task.

### Embedding Variants

By default, the viewer displays base results only:

```sql
embedding_variant_name IS NULL
```

When variant display is enabled, base results are always included and selected
variant categories are added.

| UI flag | variant rule |
| --- | --- |
| Quantization | Non-rescore rows where `quantization IS NOT NULL` or `embedding_variant_name` contains `quantize`, excluding rows that also contain `truncate` unless Truncate dims is also enabled. |
| Truncate dims | Rows where `embedding_variant_name` contains `truncate`, excluding quantized rows unless Quantization is also enabled. |
| Rescore | `embedding_variant_name` contains `rescore`. Rescore rows are not included by the Quantization flag by default. |
| Other variants | Variant rows that are neither quantization nor truncation variants. |

Rows that are both quantized and truncated are displayed only when both matching
category flags are enabled. Facet filter query parameters such as `dim_filter` and
`quant_filter` do not infer or re-enable display flags; the display flags come
only from the explicit display controls.
If old results contain a no-op truncation variant whose `truncate_dim_N` matches
the measured `embedding_dim`, and an equivalent non-truncate row exists for the
same model, task, runtime metadata, dimension, and quantization, the leaderboard
drops the no-op truncate row and prefers the original/full-dimension row.

Task score columns are also controlled by an explicit display flag. The viewer
does not render per-task or per-score-group metric columns by default. When
`task_scores=1` is present, the leaderboard computes columns for the current
selection: the selected score group for benchmark views, configured grouped
tasks for grouped overall views, or task-level columns when no score group is
available. By default, `model_filter` only hides rendered model rows,
`task_filter` only narrows displayed task score columns, and facet filters such
as model type, dimensions, quantization, dtype, attention implementation, and
prompt mode only hide rendered model rows. Model type filters use `dense`,
`sparse`, `late-interaction`, and `reranker`; BM25 is grouped under `sparse`.
When `rank_filtered=1` is present, those active filters narrow the ranked
population before Borda, mean scores, task counts, and task score columns are
computed. With a ranking task filter, the viewer ranks
the matching task rows directly; overall views render a single task-level `Mean
Score` column instead of separate macro and micro overall means. Model and task
text filters use case-insensitive whitespace-separated tokens of at least three
characters, with OR semantics.

When variants are displayed, the leaderboard keeps a unique internal row label
by appending `embedding_dim`, `quantization`, and sometimes
`embedding_variant_name` to `model_name`. The rendered model-name cell strips
that suffix back off, shortens Hugging Face-style IDs to the repository name
when that short name is unambiguous, and shows dimensions, quantization, and
variant labels such as `binary_rescore` as badges instead of duplicating them in
the visible model text. Full-dimension rows render compact dimension badges such
as `384d`. Truncation variants render the truncated dimension first, followed by
the source dimension, such as `256d <- 384`, and expose the truncation details in
a tooltip. If a DuckDB build provides an optional `model_type` column, the
viewer uses it for model-type display; older databases fall back to conservative
model-name inference for `dense`, `sparse`, `reranker`, `late-interaction`, and
`bm25`. Non-default neural model types such as sparse encoders, late-interaction
retrievers, and cross-encoder rerankers render a compact badge. Dense and BM25
rows stay unbadged in the table. Sparse models can have very large sparse
vocabulary dimensions, so the table intentionally suppresses sparse `XXXd`
dimension badges. Runtime fields such as model type, dtype,
attention implementation, prompt mode, and `trust_remote_code` are carried in a
`data-model-metadata` JSON attribute on the model-name button and displayed in
the model details modal.

When quantization or truncation variants are displayed, the viewer appends a
`Δ vs Base` column. It compares each variant row's displayed mean score against
the base row for the same source model and renders the relative percentage
change, such as `-24.5%` or `+1.2%`. Base rows and rows without a matching base
row leave this column blank.

Task metric column headers keep their full metric key for sorting and query
state, but shorten long dataset task keys for display. For example,
`MNanoBEIR::hakari-bench/NanoBEIR-ar::arguana` renders as
`NanoBEIR-ar::arguana` when that short label is unique. If two full keys shorten
to the same label, those conflicting headers render their full key. The full key
is also exposed on the header label with `data-metric-column-full-name`.
Benchmark-level `task_labels` from `config/viewer/benchmarks.yaml` override only
the visible header text; sorting, task filters, and metric values continue to
use the underlying metric key.

When `Task std display` is enabled, the viewer renders task metric columns with
the raw 0-100 task score plus its z-score distance from the task distribution.
For each displayed task column, the mean and standard deviation are computed
from base rows only, where `embedding_variant_name IS NULL`; displayed variant
rows are then compared against those base-row statistics for the same task. The
z-score label is rendered to two decimals, while the heatmap color is rounded to
0.25 standard-deviation increments and bucketed from `-2.0` to `+2.0`. A task
with zero base-row standard deviation leaves the z-score cell blank because
there is no meaningful distance from the task distribution.

## Current Viewer Data Access Layer

`hakari_bench/viewer/data.py` contains `TaskResultsRepository`, which
can read DuckDB rows into either the Pydantic DTO `TaskResultRecord` or the
lightweight dataclass `TaskResultRow`. `fetch_task_results()` keeps the
validated DTO contract for compatibility-sensitive callers and tests, while
`LeaderboardService` uses `fetch_task_result_rows()` on the UI hot path to
avoid Pydantic validation for every leaderboard row. The service converts those
rows into the leaderboard-domain `TaskScore`, then performs ranking, overall
aggregation, score grouping, and sorting in Python.

This boundary keeps SQL and the DuckDB schema contract in the data layer while
keeping Borda and complete-model semantics in `LeaderboardService`.
`TaskResultRecord` is a row contract DTO and does not contain ranking logic.

`TaskResultsRepository.fetch_task_results()` is responsible for these SQL
choices:

- Require `meta_database.schema_version` to be one of the viewer-compatible
  schema versions before querying leaderboard rows.
- Filter `viewer_task_results.score_target` by the selected target and read
  `viewer_task_results.score` directly. Current DuckDB builds materialize both
  `all` and available `reranking` rows through `fact_task_score`.
- For the default metric selector value, `nDCG@10`, use
  `viewer_task_results.score`. For other metric selector values, join
  `fact_task_score` with `fact_metric_score` and `dim_metric` by model, task,
	  result path, score target, embedding variant, metric family, and cutoff. Full-corpus targets exclude metric
	  names containing `_reranking_hybrid_top`; reranking targets prefer that marker
  and fall back only for older DuckDB builds.
- The visible metric selector is intentionally limited and ordered with
  `nDCG@10`, `acc@1`, `acc@10`, and `acc@100` first. Additional recomputed
  families/cutoffs can remain in DuckDB for analysis and may be exposed after
  those defaults when present.
- For `score_target = 'reranking'`, append BM25 `score_target = 'all'` task
  rows as the candidate-order baseline before completeness filtering and Borda
  ranking. This keeps BM25 comparable to rerankers without treating BM25 as a
  cross-encoder reranker.
- Omit BM25 only for `@100` metrics because the BM25 candidate subset can carry
  relevant documents at the tail by construction, making BM25 `@100` values
  misleading for leaderboard comparison.
- Exclude `score IS NULL` rows because they cannot participate in ranking.
- Read only benchmarks requested by the selected view.
- Read only base rows when variants are not requested.
- When variants are requested, including for reranking targets, push the
  selected display categories into SQL.
  Base rows are always read, but quantization-only, truncate-only, rescore-only,
  and other-variant views avoid fetching unrelated variant rows before Python
  ranking. Cross variants such as truncate plus quantization are fetched when
  both matching display flags are enabled.
- Surface runtime metadata such as dtype, attention implementation, prompt
  mode, and `trust_remote_code` in model details metadata; dtype, attention,
  and prompt remain available as facet filters.
- Read materialized `language` and `languages` from `viewer_task_results`.
  The HTMX viewer uses `lang_filter` query parameters as
  task-level ranking filters: Borda, mean scores, expected task counts, and
  completeness are recomputed only over tasks whose `languages` contains at
  least one selected language. If no `lang_filter` is set, all tasks in the
  selected view are ranked.
- Benchmarks may override that filter source with
  `language_filter_mode: primary_language`. MNanoBEIR and NanoMIRACL use this
  mode because they are organized around explicit dataset/language axes and
  several multilingual rows include secondary detected languages such as
  English; their Language pages therefore use the primary language, such as
  `NanoBEIR-ja` -> `ja` or the NanoMIRACL split code, rather than expanding
  every code in `languages`.
- Viewer benchmark groups put the compact curated Core set under
  Core benchmarks. Other broader multilingual/domain suites, including
  `NanoMIRACL` and `NanoLaw`, remain Domain-specific unless they are an official
  language-specific NanoMTEB family such as `NanoJMTEB-v2`, `NanoFaMTEB-v2`,
  `NanoRuMTEB`, `NanoVNMTEB`, or `NanoCMTEB`. `NanoIndicQA`, `NanoMuPLeR`, and
  `NanoChemTEB` remain Domain-specific by viewer policy even when they expose
  language pages.

The viewer logs timing records through the `hakari_bench.viewer` logger:

- `viewer.duckdb.connection`, `viewer.duckdb.schema`,
  `viewer.duckdb.query`, and `viewer.duckdb.connection_close` measure DuckDB
  connection, schema inspection, query/fetch, and close time.
- `viewer.transform` measures conversion from DuckDB rows to
  `TaskResultRecord` DTOs and deduplication.
- `viewer.leaderboard.phase` and `viewer.leaderboard.request` measure
  leaderboard service phases and end-to-end leaderboard generation.

The log fields include stable key-value pairs such as `operation`,
`elapsed_ms`, `row_count`, `deduped_row_count`, `task_score_count`, and
`leaderboard_row_count`, so production logs can identify whether UI latency is
coming from DuckDB scans, DTO conversion, variant filtering, overall
aggregation, or row rendering.

Leaderboard task-score loading uses an in-process LRU cache keyed by the
resolved DuckDB path, file `mtime_ns`, file size, benchmark tuple, target, and
variant flags. This lets repeated HTMX requests reuse the expensive DuckDB read
and row-to-`TaskScore` conversion while still invalidating automatically when a
new DuckDB file is downloaded or otherwise modified. The cache emits
`viewer.leaderboard.cache` log records with `hit`, `size`, and
`task_score_count` fields.

DB build scripts create `viewer_task_results` as a physical table after
`dataset_metadata` and `fact_task_score` are written. It selects only the
columns required by `TaskResultsRepository`, includes `score_target`, joins
`dataset_metadata` by `(benchmark, dataset_id, task_key)`, includes
`query_mean_chars` and `document_mean_chars` for task text-length filters,
keeps late-interaction runtime fields for the Model Details modal, and orders
rows by
`(benchmark, score_target, dataset_id, task_name, model_name,
embedding_variant_name)`. This avoids repeated metadata joins and lets the
viewer switch `Target: All` / `Target: Reranking` without joining diagnostics
on the hot path.
Because `viewer_task_results` is already physically ordered, the viewer skips
the query-time `ORDER BY` when reading it.
If an older database has these length columns only in `dataset_metadata`, the
repository falls back to a metadata join so `query_len_min`, `query_len_max`,
`doc_len_min`, and `doc_len_max` viewer filters still work.

`viewer_leaderboard_rows` is generated from `viewer_task_results` and stores
complete leaderboard rows for common no-filter display modes. The default build
materializes overall views, where display-variant toggles are most expensive;
other views fall back to the normal task-score computation unless explicitly
materialized by a custom build. It is keyed by `view_name`, `score_target`, and
the four display flags
`include_quantization_variants`, `include_truncate_variants`,
`include_rescore_variants`, and `include_other_variants`. The viewer uses this
mart when language filters, task-score columns, task text filters, and
component-level overall grouping are not active. Those interactive and grouped
cases still fall back to the normal
`LeaderboardService` computation from task-score rows.
For `score_target = 'reranking'`, the viewer uses this mart only when the
materialized rows already include a BM25 baseline row. Older DuckDB builds that
lack that row fall back to dynamic task-score computation so Borda and mean ranks
are recalculated with BM25 in the reranking population.

| column | type | meaning |
| --- | --- | --- |
| `view_name` | `VARCHAR` | Viewer tab or overall view name. |
| `score_target` | `VARCHAR` | Leaderboard target, such as `all` or `reranking`. |
| `include_quantization_variants` | `BOOLEAN` | Whether quantization variants were included in this materialized view. |
| `include_truncate_variants` | `BOOLEAN` | Whether truncation variants were included. |
| `include_rescore_variants` | `BOOLEAN` | Whether rescore variants were included. |
| `include_other_variants` | `BOOLEAN` | Whether non-categorized variants were included. |
| `expected_tasks` | `INTEGER` | Number of expected complete tasks for the materialized view. |
| `borda_rank`, `mean_rank` | `DOUBLE` | Precomputed display ranks. |
| `model_name` | `VARCHAR` | Display model label, including variant details when needed. |
| `borda_score`, `mean_score`, `macro_mean`, `micro_mean` | `DOUBLE` | Precomputed leaderboard scores on the 0 to 100 display scale. |
| `task_count` | `INTEGER` | Number of tasks for the complete row. |
| `active_parameters`, `total_parameters`, `max_seq_length` | `BIGINT` / `INTEGER` | Model size and sequence length metadata. If older DuckDB materializations have `NULL` values here, the viewer fills missing display values from matching `config/model_cards/*.yaml` entries at runtime without overwriting non-`NULL` DuckDB values. |
| `dtype`, `attn_implementation`, `prompt_summary`, `trust_remote_code` | mixed | Runtime and prompt metadata used by the details modal. |
| `embedding_variant_name`, `embedding_dim`, `quantization`, `source_model_name` | mixed | Variant metadata and source model identity. |
| `base_score_delta_percent` | `DOUBLE` | Precomputed relative delta against the source model's base row. |

Older schema 5 DuckDB builds do not have late-interaction runtime columns in
`viewer_leaderboard_rows`. The viewer fills missing Model Details values from
matching `config/model_cards/*.yaml` `late_interaction` sections at runtime.

`viewer_leaderboard_language_options` uses the same key columns as
`viewer_leaderboard_rows` and stores the language filter choices that should be
shown beside that materialized leaderboard. The remaining columns are `code`,
`label`, and `task_count`. Keeping these options in a companion table lets the
fast precomputed leaderboard path preserve the same filter UI without scanning
and aggregating all task-score rows on every display-toggle request.

`viewer_filter_values` is generated from `viewer_task_results` and stores
precomputed filter values for `target`, `benchmark`, `model`, and `variant`.
It is intended for future viewer endpoints that need filter lists without
running repeated `DISTINCT` scans over the leaderboard source rows.

| column | type | meaning |
| --- | --- | --- |
| `filter_name` | `VARCHAR` | Filter group, such as `target`, `benchmark`, `model`, or `variant`. |
| `value` | `VARCHAR` | Machine-readable filter value. |
| `label` | `VARCHAR` | Display label. |
| `row_count` | `BIGINT` | Number of `viewer_task_results` rows with this value. |
| `sort_key` | `VARCHAR` | Stable sort key for UI display. |

The FastAPI viewer enables gzip compression for responses of at least 1 KiB.
This primarily reduces transfer size for large HTMX leaderboard fragments when
many model or variant rows are visible.

Conceptually, it runs this query:

```sql
SELECT
  model_name,
  benchmark,
  dataset_id,
  dataset_name,
  COALESCE(split_name, '') AS split_name,
  task_name,
  task_key,
  score,
  active_parameters,
  total_parameters,
  max_seq_length,
  dtype,
  attn_implementation,
  query_prompt,
  document_prompt,
  query_prompt_name,
  document_prompt_name,
  query_encode_task,
  document_encode_task,
  trust_remote_code,
  embedding_variant_name,
  embedding_dim,
  quantization,
  query_mean_chars,
  document_mean_chars
FROM viewer_task_results
WHERE benchmark IN ('MNanoBEIR', 'NanoRTEB')
  AND score IS NOT NULL
  AND score_target = 'all'
  AND embedding_variant_name IS NULL;
```

## SQL Recipes

The following SQL snippets show how to reproduce the viewer's leaderboard
directly in DuckDB. In a real viewer, build `selected_benchmarks` and
`excluded_tasks` from `config/viewer/*.yaml`.

### 1. Inspect Schema

```sql
DESCRIBE task_results;
DESCRIBE runs;
DESCRIBE metrics_long;
DESCRIBE task_diagnostics;
DESCRIBE dataset_metadata;
DESCRIBE model_scores;
DESCRIBE borda_task_scores;
```

### 2. Benchmark View Leaderboard

Use this pattern for a single benchmark view. This example displays
`MNanoBEIR`, base rows only, with no excluded tasks.

```sql
WITH
params AS (
  SELECT
    false AS include_quantization_variants,
    false AS include_truncate_variants,
    false AS include_rescore_variants,
    false AS include_other_variants
),
selected_benchmarks(benchmark) AS (
  VALUES ('MNanoBEIR')
),
excluded_tasks(task_id) AS (
  SELECT NULL::VARCHAR WHERE false
),
source_rows AS (
  SELECT
    CASE
      WHEN (
        p.include_quantization_variants
        OR p.include_truncate_variants
        OR p.include_rescore_variants
        OR p.include_other_variants
      ) THEN tr.model_name || COALESCE('::' || tr.embedding_variant_name, '::base')
      ELSE tr.model_name
    END AS model_key,
    CASE
      WHEN NOT (
        p.include_quantization_variants
        OR p.include_truncate_variants
        OR p.include_rescore_variants
        OR p.include_other_variants
      ) THEN tr.model_name
      WHEN tr.embedding_dim IS NOT NULL AND tr.quantization IS NOT NULL
        THEN tr.model_name || ' (' || CAST(tr.embedding_dim AS VARCHAR) || ' dims, ' || tr.quantization || ')'
      WHEN tr.embedding_dim IS NOT NULL
        THEN tr.model_name || ' (' || CAST(tr.embedding_dim AS VARCHAR) || ' dims)'
      WHEN tr.quantization IS NOT NULL
        THEN tr.model_name || ' (' || tr.quantization || ')'
      ELSE tr.model_name
    END AS display_model_name,
    tr.benchmark,
    tr.dataset_id,
    tr.dataset_name,
    COALESCE(tr.split_name, '') AS split_name,
    tr.task_name,
    tr.task_key,
    tr.score,
    tr.score * 100.0 AS score_100,
    dm.language,
    dm.languages,
    tr.active_parameters,
    tr.total_parameters,
    tr.max_seq_length,
    tr.embedding_variant_name,
    tr.embedding_dim,
    tr.quantization
  FROM task_results AS tr
  LEFT JOIN dataset_metadata AS dm ON dm.task_key = tr.task_key
  JOIN selected_benchmarks AS sb USING (benchmark)
  CROSS JOIN params AS p
  WHERE tr.score IS NOT NULL
    AND NOT EXISTS (
      SELECT 1
      FROM excluded_tasks AS e
      WHERE e.task_id = tr.task_name OR e.task_id = tr.task_key
    )
    AND (
      tr.embedding_variant_name IS NULL
      OR (
        p.include_quantization_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%rescore%'
        AND (
          tr.quantization IS NOT NULL
          OR lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%quantize%'
        )
        AND (
          p.include_truncate_variants
          OR lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%truncate%'
        )
      )
      OR (
        p.include_truncate_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%truncate%'
        AND (
          p.include_quantization_variants
          OR NOT (
            tr.quantization IS NOT NULL
            OR lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%quantize%'
          )
        )
      )
      OR (
        p.include_rescore_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%rescore%'
      )
      OR (
        p.include_other_variants
        AND tr.embedding_variant_name IS NOT NULL
        AND lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%rescore%'
        AND NOT (
          tr.quantization IS NOT NULL
          OR lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%quantize%'
        )
        AND lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%truncate%'
      )
    )
),
expected AS (
  SELECT COUNT(DISTINCT task_key) AS expected_tasks
  FROM source_rows
),
complete_models AS (
  SELECT sr.model_key
  FROM source_rows AS sr
  GROUP BY sr.model_key
  HAVING COUNT(DISTINCT sr.task_key) = (SELECT expected_tasks FROM expected)
),
complete_rows AS (
  SELECT sr.*
  FROM source_rows AS sr
  JOIN complete_models AS cm USING (model_key)
),
task_ranked AS (
  SELECT
    cr.*,
    RANK() OVER (PARTITION BY cr.task_key ORDER BY cr.score DESC) AS task_rank,
    COUNT(*) OVER (PARTITION BY cr.task_key) AS model_count
  FROM complete_rows AS cr
),
task_borda AS (
  SELECT
    *,
    CASE
      WHEN model_count <= 1 THEN 100.0
      ELSE 100.0 * (model_count - task_rank) / (model_count - 1)
    END AS task_borda_score
  FROM task_ranked
),
model_agg AS (
  SELECT
    model_key,
    any_value(display_model_name) AS model_name,
    AVG(task_borda_score) AS borda_score,
    AVG(score_100) AS mean_score,
    COUNT(DISTINCT task_key) AS task_count,
    any_value(active_parameters) AS active_parameters,
    any_value(total_parameters) AS total_parameters,
    any_value(max_seq_length) AS max_seq_length,
    any_value(embedding_dim) AS embedding_dim,
    any_value(quantization) AS quantization
  FROM task_borda
  GROUP BY model_key
),
ranked AS (
  SELECT
    RANK() OVER (ORDER BY borda_score DESC) AS borda_rank,
    RANK() OVER (ORDER BY mean_score DESC) AS mean_rank,
    model_name,
    borda_score,
    mean_score,
    NULL::DOUBLE AS macro_mean,
    NULL::DOUBLE AS micro_mean,
    task_count,
    active_parameters,
    total_parameters,
    max_seq_length,
    embedding_dim,
    quantization
  FROM model_agg
)
SELECT *
FROM ranked
ORDER BY borda_rank ASC, mean_rank ASC, lower(model_name) ASC;
```

To include variants, change `params`:

```sql
SELECT
  true AS include_quantization_variants,
  true AS include_truncate_variants,
  false AS include_other_variants
```

### 3. Raw Overall View Leaderboard

For an overall view that uses raw tasks, such as `All`, put the overall
benchmarks into `selected_benchmarks` and replace `model_agg` with this
version:

```sql
benchmark_means AS (
  SELECT
    model_key,
    benchmark,
    AVG(score_100) AS benchmark_mean
  FROM task_borda
  GROUP BY model_key, benchmark
),
model_macro AS (
  SELECT
    model_key,
    AVG(benchmark_mean) AS macro_mean
  FROM benchmark_means
  GROUP BY model_key
),
model_task_agg AS (
  SELECT
    model_key,
    any_value(display_model_name) AS model_name,
    AVG(task_borda_score) AS borda_score,
    AVG(score_100) AS micro_mean,
    COUNT(DISTINCT task_key) AS task_count,
    any_value(active_parameters) AS active_parameters,
    any_value(total_parameters) AS total_parameters,
    any_value(max_seq_length) AS max_seq_length,
    any_value(embedding_dim) AS embedding_dim,
    any_value(quantization) AS quantization
  FROM task_borda
  GROUP BY model_key
),
model_agg AS (
  SELECT
    mta.model_key,
    mta.model_name,
    mta.borda_score,
    mm.macro_mean AS mean_score,
    mm.macro_mean,
    mta.micro_mean,
    mta.task_count,
    mta.active_parameters,
    mta.total_parameters,
    mta.max_seq_length,
    mta.embedding_dim,
    mta.quantization
  FROM model_task_agg AS mta
  JOIN model_macro AS mm USING (model_key)
)
```

The final result should return both `macro_mean` and `micro_mean`. `mean_rank`
for overall views ranks `mean_score`, which is `macro_mean`.

### 4. Grouped Overall View Leaderboard

Grouped overall views such as `Core` and `Group` first average raw tasks into
benchmark-local groups, then compute Borda, means, and per-group metric
columns. Generate `overall_components` from `config/viewer/overall.yaml`.

```sql
WITH
params AS (
  SELECT
    false AS include_quantization_variants,
    false AS include_truncate_variants,
    false AS include_rescore_variants,
    false AS include_other_variants
),
overall_components(benchmark, group_by) AS (
  VALUES
    ('MNanoBEIR', 'task_name'),
    ('NanoRTEB', 'task_name'),
    ('NanoMLDR', 'benchmark')
),
excluded_tasks(task_id) AS (
  SELECT NULL::VARCHAR WHERE false
),
raw_rows AS (
  SELECT
    CASE
      WHEN (
        p.include_quantization_variants
        OR p.include_truncate_variants
        OR p.include_rescore_variants
        OR p.include_other_variants
      ) THEN tr.model_name || COALESCE('::' || tr.embedding_variant_name, '::base')
      ELSE tr.model_name
    END AS model_key,
    tr.model_name AS base_model_name,
    tr.benchmark,
    tr.dataset_id,
    tr.dataset_name,
    COALESCE(tr.split_name, '') AS split_name,
    tr.task_name,
    tr.task_key AS raw_task_key,
    tr.score,
    tr.active_parameters,
    tr.total_parameters,
    tr.max_seq_length,
    tr.embedding_variant_name,
    tr.embedding_dim,
    tr.quantization,
    oc.group_by,
    (
      p.include_quantization_variants
      OR p.include_truncate_variants
      OR p.include_rescore_variants
      OR p.include_other_variants
    ) AS include_any_variants
  FROM task_results AS tr
  JOIN overall_components AS oc USING (benchmark)
  CROSS JOIN params AS p
  WHERE tr.score IS NOT NULL
    AND NOT EXISTS (
      SELECT 1
      FROM excluded_tasks AS e
      WHERE e.task_id = tr.task_name OR e.task_id = tr.task_key
    )
    AND (
      tr.embedding_variant_name IS NULL
      OR (
        p.include_quantization_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%rescore%'
        AND (
          tr.quantization IS NOT NULL
          OR lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%quantize%'
        )
        AND (
          p.include_truncate_variants
          OR lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%truncate%'
        )
      )
      OR (
        p.include_truncate_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%truncate%'
        AND (
          p.include_quantization_variants
          OR NOT (
            tr.quantization IS NOT NULL
            OR lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%quantize%'
          )
        )
      )
      OR (
        p.include_rescore_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%rescore%'
      )
      OR (
        p.include_other_variants
        AND tr.embedding_variant_name IS NOT NULL
        AND lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%rescore%'
        AND NOT (
          tr.quantization IS NOT NULL
          OR lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%quantize%'
        )
        AND lower(COALESCE(tr.embedding_variant_name, '')) NOT LIKE '%truncate%'
      )
    )
),
expected_raw_tasks AS (
  SELECT benchmark, COUNT(DISTINCT raw_task_key) AS expected_raw_tasks
  FROM raw_rows
  GROUP BY benchmark
),
complete_model_benchmarks AS (
  SELECT rr.model_key, rr.benchmark
  FROM raw_rows AS rr
  JOIN expected_raw_tasks AS e USING (benchmark)
  GROUP BY rr.model_key, rr.benchmark, e.expected_raw_tasks
  HAVING COUNT(DISTINCT rr.raw_task_key) = e.expected_raw_tasks
),
complete_raw_rows AS (
  SELECT rr.*
  FROM raw_rows AS rr
  JOIN complete_model_benchmarks AS cmb
    ON cmb.model_key = rr.model_key
   AND cmb.benchmark = rr.benchmark
),
group_inputs AS (
  SELECT
    rr.*,
    CASE group_by
      WHEN 'task_key' THEN raw_task_key
      WHEN 'dataset_name' THEN dataset_name
      WHEN 'dataset_id' THEN dataset_id
      WHEN 'split_name' THEN split_name
      WHEN 'benchmark' THEN benchmark
      ELSE task_name
    END AS aggregate_key,
    benchmark || '::' ||
      CASE group_by
        WHEN 'task_key' THEN raw_task_key
        WHEN 'dataset_name' THEN dataset_name
        WHEN 'dataset_id' THEN dataset_id
        WHEN 'split_name' THEN split_name
        WHEN 'benchmark' THEN benchmark
        ELSE task_name
      END AS task_key
  FROM complete_raw_rows AS rr
),
grouped_rows AS (
  SELECT
    model_key,
    CASE
      WHEN NOT bool_or(include_any_variants)
        THEN any_value(base_model_name)
      WHEN any_value(embedding_dim) IS NOT NULL AND any_value(quantization) IS NOT NULL
        THEN any_value(base_model_name) || ' (' || CAST(any_value(embedding_dim) AS VARCHAR) || ' dims, ' || any_value(quantization) || ')'
      WHEN any_value(embedding_dim) IS NOT NULL
        THEN any_value(base_model_name) || ' (' || CAST(any_value(embedding_dim) AS VARCHAR) || ' dims)'
      WHEN any_value(quantization) IS NOT NULL
        THEN any_value(base_model_name) || ' (' || any_value(quantization) || ')'
      ELSE any_value(base_model_name)
    END AS display_model_name,
    benchmark,
    aggregate_key,
    task_key,
    AVG(score) AS score,
    AVG(score) * 100.0 AS score_100,
    any_value(active_parameters) AS active_parameters,
    any_value(total_parameters) AS total_parameters,
    any_value(max_seq_length) AS max_seq_length,
    any_value(embedding_dim) AS embedding_dim,
    any_value(quantization) AS quantization
  FROM group_inputs
  GROUP BY model_key, benchmark, aggregate_key, task_key
)
```

Use `grouped_rows` in place of `source_rows`, then reuse `expected` and later
CTEs from the benchmark-view query. Because this is an overall view, use the
overall `model_agg` with `macro_mean` and `micro_mean`.

### 5. Score Group Columns

Benchmark views can use score groups as their scoring units. For example,
MNanoBEIR `task_mean` first averages all language rows for each task name, while
`lang_mean` first averages all task rows for each dataset/language name. The
selected group changes benchmark-view `Mean Score`, Borda, and rank. When
`task_scores=1` is active, the same group also determines the extra metric
columns shown in the table.

MNanoBEIR and NanoMIRACL Language pages use
`language_filter_mode: primary_language` rather than the full `languages` array.
This keeps language filters aligned with their dataset/language axis and avoids
over-counting secondary language tags that appear inside multilingual source
rows.

For UI rendering, long format is usually easier than SQL pivoting. Reuse
`complete_rows` from the benchmark leaderboard query:

```sql
SELECT
  model_key,
  any_value(display_model_name) AS model_name,
  dataset_name AS metric_column,
  AVG(score_100) AS metric_value
FROM complete_rows
GROUP BY model_key, dataset_name
ORDER BY metric_column, lower(model_name);
```

For `task_mean`, replace `dataset_name` with `task_name`. Other `group_by`
values follow the mapping in the viewer configuration section.

If you need a wide table in DuckDB, decide the column list first and use
`PIVOT`:

```sql
SELECT *
FROM score_group_values
PIVOT (
  first(metric_value)
  FOR metric_column IN ('NanoBEIR-en', 'NanoBEIR-ja')
);
```

### 6. Model and Run Metadata

Task rows already contain enough metadata for most leaderboard tables. Use
`runs` when you need run-level summaries:

```sql
SELECT
  model_name,
  generated_at_utc,
  started_at_utc,
  finished_at_utc,
  target_count,
  split_count,
  evaluated_count,
  cache_hit_count,
  active_parameters,
  total_parameters,
  max_seq_length,
  dtype,
  attn_implementation,
  torch_version,
  transformers_version,
  sentence_transformers_version
FROM runs
ORDER BY lower(model_name);
```

### 7. Task Detail Drilldown

When a user opens a leaderboard row, query task-level details from
`task_results` using the same view and variant constraints:

```sql
SELECT
  benchmark,
  dataset_name,
  split_name,
  task_name,
  task_key,
  aggregate_metric,
  score,
  score_100,
  dataset_revision,
  result_path,
  evaluated_at_utc,
  duration_seconds_including_dataset_load,
  wall_seconds
FROM task_results
WHERE model_name = 'example/model'
  AND benchmark = 'MNanoBEIR'
  AND embedding_variant_name IS NULL
ORDER BY dataset_name, task_name;
```

When variants are displayed, include `embedding_variant_name` in the lookup,
not just `model_name`.

### 8. Variant Facet Values

For dimension and quantization filter UI, compute options from the same
view/variant population used by the leaderboard:

```sql
SELECT DISTINCT
  CASE
    WHEN embedding_dim IS NULL THEN '__none__'
    WHEN embedding_dim >= 1025 THEN '1025+'
    ELSE CAST(embedding_dim AS VARCHAR)
  END AS dim_filter_value
FROM task_results
WHERE benchmark = 'MNanoBEIR'
  AND score IS NOT NULL
ORDER BY dim_filter_value;

SELECT DISTINCT COALESCE(quantization, '__none__') AS quant_filter_value
FROM task_results
WHERE benchmark = 'MNanoBEIR'
  AND score IS NOT NULL
ORDER BY quant_filter_value;

SELECT DISTINCT
  COALESCE(attn_implementation, '__unknown__') AS attention_filter_value,
  COALESCE(dtype, '__unknown__') AS dtype_filter_value
FROM task_results
WHERE benchmark = 'MNanoBEIR'
  AND score IS NOT NULL
ORDER BY attention_filter_value, dtype_filter_value;
```

The current viewer applies facet filters as display filters after the ranking
population has been selected. When `rank_filtered=1` is enabled, the selected
facet filters are promoted into ranking-population filters before completeness,
Borda, and mean calculations.

## Minimal Viewer Checklist

1. Read `config/viewer/*.yaml` and resolve the selected view into benchmark
   names and excluded tasks.
2. Query `task_results` with benchmark, `score IS NOT NULL`, variant, and
   excluded-task filters.
3. For benchmark views with a selected `score_group`, aggregate complete-model
   raw rows by the selected `group_by` key. For grouped overall views, aggregate
   by the configured `group_by` key.
4. Build the expected task set and keep only complete models.
5. Rank each task by score descending and compute per-task Borda scores.
6. Aggregate per model into `borda_score`, `mean_score`, `task_count`, and
   metadata columns.
7. For overall views, return both `macro_mean` and `micro_mean`, and use
   `macro_mean` as `mean_score`.
8. If `rank_filtered=1`, apply model, task, and active facet filters before the
   completeness rule and ranking. With a task filter, use direct task-level
   means for overall views instead of grouped macro/micro means.
9. Only render benchmark metric columns when `task_scores=1` is active. Use the
   already-selected scoring group rows when present; otherwise use task-level
   values. When `rank_filtered` is not active, apply `task_filter` to the
   displayed metric columns only.
10. Default sort should be `borda_rank ASC`. Metric-column sorts should place
   missing values after present values.
