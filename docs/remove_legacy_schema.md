# Remove Legacy DuckDB Schema Support

This document records the planned removal of legacy DuckDB schema support from
the leaderboard viewer and warehouse builder. The legacy schema compatibility
paths are intentionally temporary. They must be removed after the deployed
Spaces database and published dataset database have been rebuilt with the
current schema.

## Why This Must Be Removed

Keeping both the old and new schemas in active code makes the viewer harder to
reason about. The new schema has explicit score targets, canonical dimensions,
source load state, schema metadata, metric facts, and viewer materialized marts.
Once every supported DuckDB file has these tables, the old fallback logic should
be deleted so future changes only target one contract.

## Removal Preconditions

- The Hugging Face dataset database at
  `hakari-bench/leaderboard_database/duckdb/hakari_bench.duckdb` has been
  rebuilt with the current schema.
- The Hugging Face Space `hakari-bench/leaderboard` is deployed from code that
  can read the current schema.
- Local development databases under `output/viewer/` and `output/results/`
  have been regenerated.
- `docs/duckdb_schema.md` lists the current schema as the only supported
  runtime schema.
- Headless browser tests pass against a database that includes
  `meta_database`, `fact_task_score`, `dim_model`, `dim_task`, `dim_variant`,
  `dim_metric`, `fact_metric_score`, `viewer_task_results`, and
  `viewer_filter_values`.

## Removal Steps

1. Remove viewer fallback from `hakari_bench/viewer/data.py`:
   - Stop reading plain `task_results` as a runtime source.
   - Stop joining `task_diagnostics` for `Target: Reranking`.
   - Require `viewer_task_results.score_target` and read all leaderboard scores
     from `viewer_task_results`.

2. Remove old-schema tests:
   - Delete tests that create only legacy `task_results` tables.
   - Replace them with tests that assert the viewer fails clearly when required
     current-schema tables are missing.

3. Tighten DuckDB validation:
   - Check `meta_database.schema_version` at viewer startup or before the first
     query.
   - Return an actionable error when the schema is too old.

4. Update documentation:
   - Remove legacy schema fallback language from `docs/duckdb_schema.md`.
   - Keep this document until the removal commit is merged, then delete this
     document in the same pull request or a follow-up cleanup commit.

5. Rebuild and deploy:
   - Rebuild the DuckDB database from result JSON.
   - Upload the rebuilt database to the Hugging Face dataset.
   - Deploy the Space and verify the production URL.

6. Verify:
   - Run the focused viewer and DuckDB tests.
   - Run the Playwright browser smoke test.
   - Open the local viewer and verify `Target: All` and `Target: Reranking`.
   - Confirm no code path depends on `task_diagnostics.rerank_score` for the
     leaderboard hot path.

## Suggested Test Commands

```bash
uv run pytest tests/test_results_database_report.py tests/test_viewer_data.py tests/test_viewer.py -q
uv run --group viewer-browser-test pytest -q -m browser tests/test_viewer_browser.py
uv run ruff check hakari_bench/viewer/data.py scripts/build_results_database_and_report.py tests
```

## Non-Goals

- Do not delete `task_results` immediately if notebooks or external analysis
  still use it as a compatibility table.
- Do not delete `task_diagnostics`; it remains useful for analysis panels and
  reranking audits.
- Do not change benchmark scoring semantics during the removal. This cleanup is
  only about removing runtime support for obsolete DuckDB layouts.
