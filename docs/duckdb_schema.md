# DuckDB Schema and Leaderboard Query Guide

This document describes how the HAKARI-Bench viewer stores leaderboard
data in DuckDB and how a viewer should query that data.

The main source table for the HTMX leaderboard viewer is `task_results`.
`runs` contains run-level metadata, `metrics_long` contains detailed task
metrics, `retrieval_rankings` contains per-query top-100 retrieved document ids,
`task_diagnostics` contains analysis-oriented rerank, candidate, and latency
fields, `dataset_metadata` exposes YAML task metadata for language, category,
citation, and text-stat analysis, and `model_scores` /
`borda_task_scores` are precomputed tables used by the static HTML report. The
current HTMX viewer computes the leaderboard from `task_results` on each
request and reads `task_diagnostics` / `dataset_metadata` for paper-facing
analysis panels. It does not read `model_scores`.

## Generation

Build the DuckDB database from benchmark JSON output:

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/results \
  --duckdb-path output/results/hakari_bench.duckdb \
  --html-output output/results/report.html \
  --parquet-output-dir output/results/parquet
```

The input files are:

- `output/results/{model_dir}/{huggingface_dataset_name}/{split_or_task}.json`:
  task-level benchmark results.
- `output/results/{model_dir}/{huggingface_dataset_name}/rankings/{split_or_task}.top100.json`:
  optional per-query top-100 ranking artifacts written only when evaluation is
  run with `--save-top-rankings` and referenced by task JSON
  `artifacts.top_rankings`.

`load_results()` determines `benchmark` from `target.dataset_id` and
`target.dataset_name` using `config/viewer/benchmarks.yaml`, then writes only
configured benchmark rows into `task_results`. The base embedding result is
stored as a row where
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
snapshots for the canonical tables: `runs`, `task_results`, `metrics_long`,
`retrieval_rankings`, `task_diagnostics`, `dataset_metadata`, `model_scores`,
and `borda_task_scores`. These files are intended for notebooks,
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
| `score_groups` | Additional metric columns for a benchmark view. These do not change ranking. |

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
| Leaderboard | `task_results`, optionally joined to `dataset_metadata` and `task_diagnostics` | Computes Borda and mean scores from complete model-task matrices for the selected YAML view. The `Target` selector defaults to `All`, which uses `task_results.score` for full-corpus retrieval. `Reranking` joins `task_diagnostics` and uses available BM25 top-100 `rerank_score` values. Base rows are used unless the user explicitly enables variant categories; reranking currently ranks base rows because `task_diagnostics` has no embedding-variant identity. |
| Variant impact | `task_results` | Joins each embedding variant row to the matching base row by `(model_name, benchmark, task_key)` and reports mean score plus relative delta versus base. This is intended for quantization-first comparisons; rescore and `truncate_dim` variants are hidden unless explicitly enabled in the panel. |
| Reranking diagnostics | `task_diagnostics` | Aggregates candidate coverage and rerank lift by benchmark for the selected YAML view. |
| Dataset diagnostics | `dataset_metadata`, `task_results` | Aggregates task metadata, query/document sample sizes, text lengths, and the fraction of base rows with `score >= 0.95` as a saturation signal. |

Analysis panels are scoped by the same YAML view selection as the leaderboard.
`Overall` views expand to their configured benchmark components before querying.
The diagnostics panels are descriptive and do not alter leaderboard ranking.

## Table Overview

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
| `torch_version` | `VARCHAR` | Torch version used for evaluation. |
| `transformers_version` | `VARCHAR` | Transformers version used for evaluation. |
| `sentence_transformers_version` | `VARCHAR` | Sentence Transformers version used for evaluation. |
| `started_at_utc` | `VARCHAR` | Task evaluation start time as a UTC ISO string. |
| `finished_at_utc` | `VARCHAR` | Task evaluation finish time as a UTC ISO string. |
| `evaluated_at_utc` | `VARCHAR` | Evaluation completion time. Older JSON may only have this timestamp. |
| `duration_seconds_including_dataset_load` | `DOUBLE` | Task duration including dataset loading. |
| `wall_seconds` | `DOUBLE` | Task evaluation wall time in seconds. |

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

`metrics_long` is a long-format representation of each task JSON `metrics`
dictionary. It is intended for detailed metric inspection. The current viewer
does not use it for ranking.

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

### `retrieval_rankings`

`retrieval_rankings` is a normalized view of optional top-100 ranking artifact
JSON. It is populated only for task results that were produced with
`--save-top-rankings`. It is intended for offline metric recomputation,
rank-fusion experiments, hybrid search simulations, and reranker candidate
analysis. It is not used for leaderboard ranking.

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
| `view_name` | `VARCHAR` | `Overall` or benchmark view name. |
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
| `view_name` | `VARCHAR` | `Overall` or benchmark view name. |
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

For grouped overall views such as `OverallGrouped`, the viewer first checks raw
task completeness within each model/benchmark pair, then aggregates rows by the
configured group key, and finally applies the complete model rule again to the
aggregated task set.

### Benchmark and Overall Views

For benchmark views, `mean_score` is the mean of all task scores in that
benchmark.

For overall views:

- `micro_mean`: mean over all included tasks with equal task weight.
- `macro_mean`: mean of benchmark-level means with equal benchmark weight.
- `mean_score`: `macro_mean` for overall views, task mean for benchmark views.

`Overall` normally uses raw `task_key` values. `OverallGrouped` uses the
`group_by` settings from `overall.yaml` to average tasks into benchmark-local
units before computing Borda and means.

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
| Quantization | Non-rescore rows where `quantization IS NOT NULL` or `embedding_variant_name` contains `quantize`. |
| Truncate dims | `embedding_variant_name` contains `truncate`. |
| Rescore | `embedding_variant_name` contains `rescore`. Rescore rows are not included by the Quantization flag by default. |
| Other variants | Variant rows that are neither quantization nor truncation variants. |

Rows that are both quantized and truncated are displayed only when both the
Quantization and Truncate dims flags are enabled. Facet filter query parameters
such as `dim_filter` and `quant_filter` do not infer or re-enable display
flags; the display flags come only from the explicit display controls.

Task score columns are also controlled by an explicit display flag. The viewer
does not render per-task or per-score-group metric columns by default. When
`task_scores=1` is present, the leaderboard computes columns for the current
selection: the selected score group for benchmark views, configured grouped
tasks for grouped overall views, or task-level columns when no score group is
available. `task_filter` filters only those task score columns, not the ranked
model population. It uses the same matching behavior as the model-name filter:
case-insensitive whitespace-separated tokens of at least three characters, with
OR semantics.

When variants are displayed, the leaderboard keeps a unique internal row label
by appending `embedding_dim`, `quantization`, and sometimes
`embedding_variant_name` to `model_name`. The rendered model-name cell strips
that suffix back off, shortens Hugging Face-style IDs to the repository name
when that short name is unambiguous, and shows dimensions, quantization, and
variant labels such as `binary_rescore` as badges instead of duplicating them in
the visible model text. Full-dimension rows render compact dimension badges such
as `384d`. Truncation variants render the truncated dimension first, followed by
the source dimension, such as `256d <- 384`, and expose the truncation details in
a tooltip. Runtime fields such as dtype, attention implementation, prompt mode,
and `trust_remote_code` are carried in a `data-model-metadata` JSON attribute on
the model-name button and displayed in the model details modal.

When quantization or truncation variants are displayed, the viewer appends a
`Δ vs Base` column. It compares each variant row's displayed mean score against
the base row for the same source model and renders the relative percentage
change, such as `-24.5%` or `+1.2%`. Base rows and rows without a matching base
row leave this column blank.

## Current Viewer Data Access Layer

`hakari_bench/viewer/data.py` contains `TaskResultsRepository`, which
can read DuckDB rows into either the Pydantic DTO `TaskResultRecord` or the
lightweight dataclass `TaskResultRow`. `fetch_task_results()` keeps the
validated DTO contract for compatibility-sensitive callers and tests, while
`LeaderboardService` uses `fetch_task_result_rows()` on the UI hot path to
avoid Pydantic validation for every leaderboard row. The service converts those
rows into the leaderboard-domain `TaskScore`, then performs ranking, overall
aggregation, score grouping, and sorting in Python.

This boundary keeps SQL and DB-schema compatibility in the data layer while
keeping Borda and complete-model semantics in `LeaderboardService`.
`TaskResultRecord` is a row contract DTO and does not contain ranking logic.

`TaskResultsRepository.fetch_task_results()` is responsible for these SQL
choices:

- Read `task_results.score` for the default `Target: All` leaderboard source.
- Join `task_diagnostics` and read `rerank_score` for `Target: Reranking`;
  rows without available BM25 top-100 rerank scores are excluded.
- Exclude `score IS NULL` rows because they cannot participate in ranking.
- Read only benchmarks requested by the selected view.
- Read only base rows when variants are not requested; reranking also reads
  base rows because diagnostics are not variant-specific.
- When variants are requested, push the selected display categories into SQL.
  Base rows are always read, but quantization-only, truncate-only, rescore-only,
  and other-variant views avoid fetching unrelated variant rows before Python
  ranking. Cross variants such as truncate plus quantization are fetched only
  when both required display flags are enabled.
- Select missing variant/runtime columns as `NULL` for old DuckDB files.
- Surface runtime metadata such as dtype, attention implementation, prompt
  mode, and `trust_remote_code` in model details metadata; dtype, attention,
  and prompt remain available as facet filters.
- Join `dataset_metadata` when present to attach `language` and `languages`
  to task rows. The HTMX viewer uses `lang_filter` query parameters as
  task-level ranking filters: Borda, mean scores, expected task counts, and
  completeness are recomputed only over tasks whose `languages` contains at
  least one selected language. If no `lang_filter` is set, all tasks in the
  selected view are ranked. When `benchmark` and `dataset_id` are available,
  the metadata join includes them in addition to `task_key` to avoid row
  multiplication from task-key reuse across datasets.

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
  quantization
FROM task_results
WHERE benchmark IN ('MNanoBEIR', 'NanoRTEB')
  AND score IS NOT NULL
  AND embedding_variant_name IS NULL;
```

For older databases without `embedding_variant_name`, `embedding_dim`,
`quantization`, prompt, attention, dtype, or remote-code columns, the viewer
treats those fields as `NULL`.

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
      )
      OR (
        p.include_truncate_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%truncate%'
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

### 3. Overall View Leaderboard

For an `Overall` view that uses raw tasks, put the overall benchmarks into
`selected_benchmarks` and replace `model_agg` with this version:

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

### 4. OverallGrouped Leaderboard

`OverallGrouped` first averages raw tasks into benchmark-local groups, then
computes Borda, means, and per-group metric columns. Generate
`overall_components` from `config/viewer/overall.yaml`.

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
      )
      OR (
        p.include_truncate_variants
        AND lower(COALESCE(tr.embedding_variant_name, '')) LIKE '%truncate%'
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

Benchmark views can show additional score group columns that do not affect
ranking. For example, MNanoBEIR `lang_mean` groups by `dataset_name`.

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
population has been selected. They should not silently change the ranking
population unless the UI makes that behavior explicit.

## Minimal Viewer Checklist

1. Read `config/viewer/*.yaml` and resolve the selected view into benchmark
   names and excluded tasks.
2. Query `task_results` with benchmark, `score IS NOT NULL`, variant, and
   excluded-task filters.
3. For benchmark views, use raw rows. For grouped overall views, aggregate by
   the configured `group_by` key.
4. Build the expected task set and keep only complete models.
5. Rank each task by score descending and compute per-task Borda scores.
6. Aggregate per model into `borda_score`, `mean_score`, `task_count`, and
   metadata columns.
7. For overall views, return both `macro_mean` and `micro_mean`, and use
   `macro_mean` as `mean_score`.
8. Only compute and render benchmark metric columns when `task_scores=1` is
   active. Use the selected score group when present; otherwise use task-level
   values. Apply `task_filter` to the displayed metric columns only.
9. Default sort should be `borda_rank ASC`. Metric-column sorts should place
   missing values after present values.
