# DuckDB Schema and Leaderboard Query Guide

この文書は、Nano IR Benchmark の結果 DuckDB
`nano_ir_bench.duckdb` から leaderboard viewer を作るためのデータ定義と
SQL の引き方をまとめたものです。

結論として、viewer が leaderboard を作るときの主データは
`task_results` です。`runs` は run 単位の補足情報、`metrics_long` は詳細
metric、`model_scores` と `borda_task_scores` は静的 HTML レポート用に
事前計算された派生テーブルです。現在の HTMX viewer は
`model_scores` ではなく `task_results` から毎回 leaderboard を計算します。

## 生成方法

DuckDB は benchmark の JSON 出力から生成します。

```bash
uv run python scripts/build_results_database_and_report.py \
  --results-dir output/results \
  --duckdb-path output/results/nano_ir_bench.duckdb \
  --html-output output/results/report.html
```

入力は主に次の JSON です。

- `output/results/{model_dir}/all.json`: model/run 単位の summary。
- `output/results/{model_dir}/{dataset_name}/{split_or_task}.json`: task 単位の結果。

`load_results()` は task JSON の `target.dataset_id` と
`target.dataset_name` から `benchmark` を判定し、対象 benchmark だけを
`task_results` に入れます。base embedding の結果は
`embedding_variant_name IS NULL` の行になり、`evaluation.embedding_evaluations`
に入っている派生 embedding 結果は variant 行として追加されます。

web viewer は `uv run nano-ir-bench web` で起動します。デフォルトでは
`output/viewer/nano_ir_bench.duckdb` をローカル閲覧用 DB として使い、ページ
load 時に benchmark output 側の DB が新しければコピーします。

## Viewer 設定

leaderboard の view は DuckDB 内ではなく YAML で定義します。

- `config/viewer/benchmarks.yaml`: benchmark view の一覧、表示 label、除外
  task、benchmark view 内の score group。
- `config/viewer/overall.yaml`: Overall 系 view と、どの benchmark を含めるか。

`benchmarks.yaml` の主な項目:

| 項目 | 意味 |
| --- | --- |
| `name` | `task_results.benchmark` と一致する view 名。 |
| `label` | UI 表示名。省略時は `name`。 |
| `include_in_overall` | 現状は説明用 metadata。実際の Overall 構成は `overall.yaml` が決める。 |
| `excluded_tasks` | ranking から除外する task。`task_name` または `task_key` と照合する。 |
| `score_groups` | benchmark view の横持ち metric 列定義。ranking 自体は変えない。 |

`score_groups[].group_by` と `overall.yaml` の `group_by` は次のキーを使えます。

| `group_by` | group key として使う列 |
| --- | --- |
| `task_key` | `task_results.task_key` |
| `dataset_name` | `task_results.dataset_name` |
| `dataset_id` | `task_results.dataset_id` |
| `split_name` | `COALESCE(task_results.split_name, '')` |
| `benchmark` | `task_results.benchmark` |
| `task_name` | `task_results.task_name` |

不明な `group_by` は実装上 `task_name` と同じ扱いになります。

## Table Overview

### `task_results`

leaderboard の canonical source です。1 行は「1 model / 1 benchmark task /
1 embedding variant」の score を表します。base result は
`embedding_variant_name IS NULL` です。

| column | type | 意味 |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | `output/results/{model_dir}` のディレクトリ名。 |
| `model_name` | `VARCHAR` | JSON の `model.name_or_path`。なければ `model_dir`。 |
| `benchmark` | `VARCHAR` | viewer 上の benchmark group。例: `MNanoBEIR`, `NanoJMTEB`。 |
| `dataset_id` | `VARCHAR` | `target.dataset_id`。Hugging Face dataset repo など。 |
| `dataset_revision` | `VARCHAR` | 解決済み dataset revision。通常は commit SHA。 |
| `dataset_revision_requested` | `VARCHAR` | 実行時に要求した revision。未指定なら `NULL`。 |
| `dataset_name` | `VARCHAR` | `target.dataset_name`。 |
| `split_name` | `VARCHAR` | `target.split_name`。task split がなければ `NULL` の場合がある。 |
| `task_name` | `VARCHAR` | `target.task_name`。なければ `split_name`。 |
| `task_key` | `VARCHAR` | ranking の task identity。生成式は `{benchmark}::{dataset_id}::{task_name}`。 |
| `score` | `DOUBLE` | raw aggregate score。通常は 0.0 から 1.0 の nDCG 系値。 |
| `score_100` | `DOUBLE` | `score * 100.0`。表示用。 |
| `aggregate_metric` | `VARCHAR` | `evaluation.aggregate_metric`。例: `ndcg@10`。 |
| `result_path` | `VARCHAR` | 元 task JSON の path。 |
| `active_parameters` | `BIGINT` | active parameter 数。取れない場合は `NULL`。 |
| `total_parameters` | `BIGINT` | total parameter 数。取れない場合は `NULL`。 |
| `max_seq_length` | `INTEGER` | model の max sequence length。 |
| `dtype` | `VARCHAR` | 評価時 dtype。例: `bf16`。 |
| `embedding_variant_name` | `VARCHAR` | 派生 embedding variant 名。base result は `NULL`。 |
| `embedding_dim` | `INTEGER` | その行の embedding dimension。base 行にも入る場合がある。 |
| `quantization` | `VARCHAR` | quantization precision。例: `int8`, `uint8`, `ubinary`。 |
| `attn_implementation` | `VARCHAR` | attention implementation。例: `flash_attention_2`。 |
| `torch_version` | `VARCHAR` | 評価環境の torch version。 |
| `transformers_version` | `VARCHAR` | 評価環境の transformers version。 |
| `sentence_transformers_version` | `VARCHAR` | 評価環境の sentence-transformers version。 |
| `started_at_utc` | `VARCHAR` | task 評価開始時刻。UTC ISO 文字列。 |
| `finished_at_utc` | `VARCHAR` | task 評価終了時刻。UTC ISO 文字列。 |
| `evaluated_at_utc` | `VARCHAR` | 評価完了時刻。古い JSON ではこの列だけの場合がある。 |
| `duration_seconds_including_dataset_load` | `DOUBLE` | dataset load を含む task 所要秒数。 |
| `wall_seconds` | `DOUBLE` | task 評価 wall time 秒数。 |

### `runs`

`all.json` から作られる model/run 単位の summary です。leaderboard の rank
計算には使いませんが、model metadata や run completeness を表示する用途で
使えます。

| column | type | 意味 |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | `output/results/{model_dir}` のディレクトリ名。 |
| `model_name` | `VARCHAR` | JSON の `model.name_or_path`。 |
| `all_json_path` | `VARCHAR` | 元 `all.json` の path。 |
| `generated_at_utc` | `VARCHAR` | `all.json` 生成時刻。 |
| `started_at_utc` | `VARCHAR` | run 開始時刻。 |
| `finished_at_utc` | `VARCHAR` | run 終了時刻。 |
| `target_count` | `INTEGER` | 評価対象 target 数。 |
| `split_count` | `INTEGER` | split/task 数。 |
| `cache_hit_count` | `INTEGER` | cache hit 数。 |
| `evaluated_count` | `INTEGER` | 実評価数。 |
| `aggregate_metric_mean` | `DOUBLE` | `all.json` 側の aggregate metric mean。 |
| `active_parameters` | `BIGINT` | model active parameter 数。 |
| `total_parameters` | `BIGINT` | model total parameter 数。 |
| `max_seq_length` | `INTEGER` | model max sequence length。 |
| `dtype` | `VARCHAR` | 評価時 dtype。 |
| `attn_implementation` | `VARCHAR` | attention implementation。 |
| `torch_version` | `VARCHAR` | torch version。 |
| `transformers_version` | `VARCHAR` | transformers version。 |
| `sentence_transformers_version` | `VARCHAR` | sentence-transformers version。 |

### `metrics_long`

task JSON の `metrics` dict を long format にした table です。特定 metric の
詳細確認用で、現行 viewer の rank 計算には使いません。

| column | type | 意味 |
| --- | --- | --- |
| `model_dir` | `VARCHAR` | model output directory。 |
| `model_name` | `VARCHAR` | model name。 |
| `benchmark` | `VARCHAR` | benchmark group。 |
| `dataset_id` | `VARCHAR` | dataset id。 |
| `task_name` | `VARCHAR` | task name。 |
| `metric_name` | `VARCHAR` | metric 名。例: `NanoJaCWIR_ndcg@10`。 |
| `metric_value` | `DOUBLE` | metric 値。 |
| `result_path` | `VARCHAR` | 元 task JSON の path。 |

### `model_scores`

`scripts/build_results_database_and_report.py` が静的 HTML report 用に作る
precomputed standings です。base 行だけを使って生成されます。

現行 viewer はこの table を使いません。viewer と同じ結果を出したい場合は、
`task_results` から後述の SQL または `LeaderboardService` と同じロジックで
計算してください。特に tie rank は現行 viewer が competition rank
(`1, 2, 2, 4`) を使う一方、静的 report 側の helper は average rank を使う
箇所があります。

| column | type | 意味 |
| --- | --- | --- |
| `view_name` | `VARCHAR` | `Overall` または benchmark 名。 |
| `model_name` | `VARCHAR` | model name。 |
| `task_count` | `INTEGER` | ranking に使った task 数。 |
| `mean_score` | `DOUBLE` | 平均 score。100 点換算。 |
| `score_rank` | `DOUBLE` | `mean_score` による rank。 |
| `borda_score` | `DOUBLE` | task 別 Borda score の平均。 |
| `borda_rank` | `DOUBLE` | `borda_score` による rank。 |
| `active_parameters` | `BIGINT` | active parameter 数。 |
| `total_parameters` | `BIGINT` | total parameter 数。 |
| `max_seq_length` | `INTEGER` | max sequence length。 |
| `dtype` | `VARCHAR` | dtype。 |
| `attn_implementation` | `VARCHAR` | attention implementation。 |
| `torch_version` | `VARCHAR` | torch version。 |
| `transformers_version` | `VARCHAR` | transformers version。 |
| `sentence_transformers_version` | `VARCHAR` | sentence-transformers version。 |

### `borda_task_scores`

静的 report 用の per-task Borda detail です。現行 viewer の rank 計算には使いません。

| column | type | 意味 |
| --- | --- | --- |
| `view_name` | `VARCHAR` | `Overall` または benchmark 名。 |
| `model_name` | `VARCHAR` | model name。 |
| `benchmark` | `VARCHAR` | benchmark group。 |
| `task_key` | `VARCHAR` | task identity。 |
| `rank` | `DOUBLE` | task 内 score rank。 |
| `model_count` | `INTEGER` | その task に参加した complete model 数。 |
| `borda_score` | `DOUBLE` | その task での Borda score。 |
| `score` | `DOUBLE` | raw task score。 |

## Leaderboard Semantics

### score と rank

- task score は `task_results.score` を使います。
- 表示用 mean は `score * 100.0` の平均です。
- task ごとの rank は score 降順の competition rank です。同点は同じ rank
  になり、次の rank は飛びます。
- task ごとの Borda score は次の式です。

```text
model_count <= 1 のとき 100
それ以外は 100 * (model_count - rank) / (model_count - 1)
```

model の `borda_score` は、view 内の各 task Borda score の平均です。
`borda_rank` は `borda_score` 降順 rank、`mean_rank` は `mean_score` 降順
rank です。

### complete model rule

ranking に入る model は、view 内の期待 task をすべて持つ model だけです。

1. `benchmark` filter と `excluded_tasks` を適用する。
2. embedding variant 表示設定を適用する。
3. 残った行の `task_key` 集合を expected tasks とする。
4. model ごとの `task_key` 集合が expected tasks と完全一致する model だけを
   leaderboard に出す。

OverallGrouped のように `group_by` を使う Overall では、先に benchmark 内の
raw task completeness を満たす model/benchmark だけを group に集約し、その
集約後 task 集合に対して complete model rule を再適用します。

### Benchmark view と Overall view

benchmark view の `mean_score` は、その benchmark の task score mean です。

Overall view では次を区別します。

- `micro_mean`: Overall に含めた task をすべて同じ重みで平均した値。
- `macro_mean`: benchmark ごとの平均を作り、それを benchmark 間で平均した値。
- `mean_score`: Overall view では `macro_mean`。benchmark view では task mean。

`Overall` は通常 raw `task_key` をそのまま使います。`OverallGrouped` は
`overall.yaml` の `group_by` に従って、benchmark 内 task を平均した集約 unit
を作ってから Borda と mean を計算します。

### embedding variants

デフォルトの viewer は base result のみを表示します。

```sql
embedding_variant_name IS NULL
```

variant 表示を有効にした場合も base result は常に含め、選択された variant
種別だけを追加します。

| UI flag | variant 判定 |
| --- | --- |
| Quantization | `quantization IS NOT NULL` または `embedding_variant_name` に `quantize` を含む。 |
| Truncate dims | `embedding_variant_name` に `truncate` を含む。 |
| Other variants | quantization でも truncate でもない variant。 |

現行 viewer は variant 表示時に `model_name` に `embedding_dim` と
`quantization` を付けた表示名を ranking key として扱います。同じ表示名に
複数の `embedding_variant_name` が衝突する場合は、表示名に variant 名も足し
ます。これは同一 task 内で複数 variant が同じ model として潰れ、Borda の
`rank` と `model_count` の母集団がずれるのを防ぐためです。

新しく viewer を作る場合は、内部 key には `model_name` と
`embedding_variant_name` を組み合わせた安定 key を持ち、表示 label は別に作る
ほうがさらに衝突に強くなります。

## 現行 viewer の取得層

`nano_ir_benchmark/viewer/data.py` の `TaskResultsRepository` が、DuckDB
から Pydantic DTO の `TaskResultRecord` を取得します。
`LeaderboardService` はこの DTO を leaderboard 計算用の `TaskScore` に変換し、
ranking、Overall 集約、score group、sort を Python 側で行います。

この分離の意図は、SQL と DB schema 互換処理を取得層に閉じ込め、Borda や
complete model rule などの leaderboard semantics を `LeaderboardService` 側に
残すことです。`TaskResultRecord` は DuckDB の row contract を表す DTO であり、
計算ロジックは持ちません。

`TaskResultsRepository.fetch_task_results()` が担う SQL 上の判断は次の通りです。

- canonical source の `task_results` だけを読む。
- ranking できない `score IS NULL` の行は除外する。
- view が要求した `benchmark` だけを読む。
- variant 表示が不要なときは `embedding_variant_name IS NULL` の base rows だけを読む。
- 古い DuckDB に variant 列がない場合は、該当 DTO field を `NULL` として返す。

概念的には次の SQL です。

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
  embedding_variant_name,
  embedding_dim,
  quantization
FROM task_results
WHERE benchmark IN ('MNanoBEIR', 'NanoRTEB')
  AND score IS NOT NULL
  AND embedding_variant_name IS NULL;
```

`embedding_variant_name` などの variant 列が存在しない古い DB では、現行
viewer はそれらを `NULL` として扱います。

## SQL Recipes

以降の SQL は、DuckDB だけで viewer と同じ leaderboard を再現するための
雛形です。実際には `selected_benchmarks` と `excluded_tasks` を YAML 設定
から組み立ててください。

### 1. schema 確認

```sql
DESCRIBE task_results;
DESCRIBE runs;
DESCRIBE metrics_long;
DESCRIBE model_scores;
DESCRIBE borda_task_scores;
```

### 2. benchmark view の leaderboard

単一 benchmark view はこの形で引けます。例では `MNanoBEIR` を表示し、
variant は base のみ、除外 task なしにしています。

```sql
WITH
params AS (
  SELECT
    false AS include_quantization_variants,
    false AS include_truncate_variants,
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
        OR p.include_other_variants
      ) THEN tr.model_name || COALESCE('::' || tr.embedding_variant_name, '::base')
      ELSE tr.model_name
    END AS model_key,
    CASE
      WHEN NOT (
        p.include_quantization_variants
        OR p.include_truncate_variants
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
    tr.active_parameters,
    tr.total_parameters,
    tr.max_seq_length,
    tr.embedding_variant_name,
    tr.embedding_dim,
    tr.quantization
  FROM task_results AS tr
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
        p.include_other_variants
        AND tr.embedding_variant_name IS NOT NULL
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

variant を含める場合は `params` を変更します。

```sql
SELECT
  true AS include_quantization_variants,
  true AS include_truncate_variants,
  false AS include_other_variants
```

### 3. Overall view の leaderboard

`Overall` のように raw task をそのまま使う場合は、前節の
`selected_benchmarks` に Overall 対象 benchmark を並べます。その上で
`model_agg` を次の形に変更します。

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

最終 `SELECT` では `macro_mean` と `micro_mean` をそのまま返します。Overall
の `mean_rank` は `mean_score = macro_mean` の rank です。

### 4. OverallGrouped の leaderboard

`OverallGrouped` は、benchmark ごとに raw task を group に平均してから
leaderboard を計算します。例の `overall_components` は
`config/viewer/overall.yaml` から生成してください。

```sql
WITH
params AS (
  SELECT
    false AS include_quantization_variants,
    false AS include_truncate_variants,
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
        p.include_other_variants
        AND tr.embedding_variant_name IS NOT NULL
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

この `grouped_rows` を、benchmark view SQL の `source_rows` の代わりに使って
`expected` 以降を同じように計算します。Overall なので最終 aggregation は
前節の `macro_mean` / `micro_mean` 付き `model_agg` を使います。

### 5. score group の横持ち metric 列

benchmark view では、ranking とは別に score group 列を出せます。たとえば
MNanoBEIR の `lang_mean` は `dataset_name` ごとの平均を列として出します。

UI で pivot するなら、SQL は long format のまま返すのが扱いやすいです。
`complete_rows` は benchmark leaderboard SQL の CTE を流用してください。

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

`task_mean` の場合は `dataset_name` を `task_name` に置き換えます。その他の
`group_by` も `Viewer 設定` の対応表と同じです。

DuckDB 側で横持ちにする場合は、列一覧を先に決めてから `PIVOT` します。

```sql
SELECT *
FROM score_group_values
PIVOT (
  first(metric_value)
  FOR metric_column IN ('NanoBEIR-en', 'NanoBEIR-ja')
);
```

### 6. model/run metadata

task 結果に紐づく runtime 情報は `task_results` だけでも表示できます。run 単位
の summary を出したい場合は `runs` を使います。

```sql
SELECT
  model_name,
  all_json_path,
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

### 7. task detail drilldown

leaderboard 行をクリックして task 別 score を見せる場合は、
`task_results` を model と view 条件で引きます。

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

variant 表示時は `model_name` だけでなく `embedding_variant_name` も条件に
入れてください。

### 8. variant facet 用の候補値

dimension と quantization の filter UI を作る場合は、leaderboard と同じ
view/variant 条件をかけたうえで候補値を出します。

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
```

UI で filter を適用するときは、base rows を残すかどうかを明示してください。
現行 viewer は「表示 variant の候補を ranking に含めた後、画面上で行を隠す」
という動きです。filter は ranking の母集団そのものを変える用途ではなく、表示
を絞る用途です。

## Viewer を作るときの最小 checklist

1. `config/viewer/*.yaml` を読み、view 名から対象 benchmark と除外 task を決める。
2. `task_results` から `benchmark`, `score IS NOT NULL`, variant 条件、
   `excluded_tasks` を適用して source rows を作る。
3. benchmark view なら raw rows のまま、OverallGrouped なら group_by で集約する。
4. expected task set を作り、complete model だけを残す。
5. task ごとに score 降順 `RANK()` を計算し、Borda score を出す。
6. model ごとに `borda_score`, `mean_score`, `task_count`, parameter/runtime
   metadata を集計する。
7. Overall view では `macro_mean` と `micro_mean` を分け、`mean_score` には
   `macro_mean` を使う。
8. benchmark view の追加列が必要なら `score_groups` の `group_by` で
   long format の metric values を作り、UI 側で pivot する。
9. sort は `borda_rank ASC` をデフォルトにし、metric 列 sort は missing を
   後ろに送る。
