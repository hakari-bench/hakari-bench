# Documentation Index

This page is the shared entry point for humans and coding agents. It points to
the canonical document for each workflow so that operational rules stay in one
place and AGENTS.md can stay focused on repository-level guardrails.

## Start Here

| Need | Primary document | Notes |
| --- | --- | --- |
| Find the right project document | [index.md](index.md) | This map for humans and agents: canonical docs, workflow routes, and artifact boundaries. |
| Install HAKARI-Bench and run a first local evaluation | [quickstart.md](quickstart.md) | Shortest path from installation to evaluation, DuckDB build, local viewer, and result submission pointers. |
| Decide benchmark settings before running models | [evaluation_policy.md](evaluation_policy.md) | Source of truth for prompts, dtype, attention, variants, target scope, cache policy, and coverage audits. |
| Run concrete evaluation and DuckDB commands | [evaluation_runbook.md](evaluation_runbook.md) | Runnable commands for full/partial evaluation, remote result sync, DuckDB rebuild/append, and viewer startup. |
| Evaluate a new model and submit results | [new_model_results_workflow.md](new_model_results_workflow.md) | End-to-end checklist from model research through model card review, full evaluation, audit, and result PRs. |
| Understand benchmark scope | [benchmark_scope.md](benchmark_scope.md) | Compact explanation of Nano-set task layout, coverage, dataset locations, and intended use. |

## Source Of Truth By Area

| Area | Canonical document | What belongs there |
| --- | --- | --- |
| Evaluation policy | [evaluation_policy.md](evaluation_policy.md) | Prompt/runtime choices, embedding variants, BM25/reranker settings, offline/cache policy, coverage audits. |
| Evaluation commands | [evaluation_runbook.md](evaluation_runbook.md) | Copy-pasteable CLI workflows for evaluation, DuckDB rebuild, append, remote sync, and viewer launch. |
| Model onboarding | [new_model_results_workflow.md](new_model_results_workflow.md) | New-model research, small validation, full runs, PR body generation, and submission sequence. |
| Result contribution | [contributing_results.md](contributing_results.md) | Result repository layout, `.json.xz` expectations, Hugging Face Dataset PR workflow, reviewer checklist. |
| Model metadata | [model_cards.md](model_cards.md) | Static model-card schema and which model-specific settings belong in `config/model_cards/`. |
| Model-specific runtime notes | [model_specific_benchmarking_notes.md](model_specific_benchmarking_notes.md) | Verified prompts, prompt names, attention choices, compatibility notes, and model-family exceptions. |
| Custom backends | [custom_model_backends.md](custom_model_backends.md) | Loader contract, backend kwargs, metadata, secrets handling, and examples for non-standard model APIs. |
| Late interaction | [late_interaction_evaluation.md](late_interaction_evaluation.md) | PyLate/ColBERT workflow, reviewed cards, prefixes, token lengths, expansion-token attention, validation. |
| OpenAI embeddings | [openai_embedding_evaluation.md](openai_embedding_evaluation.md) | OpenAI loader setup, API keys, dimensions, token limits, concurrency, and batch-evaluation pointers. |
| Batch inference | [batch_inference.md](batch_inference.md) | Register/fetch/materialize workflow for offline embedding providers and normal HAKARI result JSON output. |
| SentenceTransformers integration | [sentence_transformers_evaluation_integration.md](sentence_transformers_evaluation_integration.md) | Training-time evaluators, Nano target selection, smoke runs, variants, and integration tests. |
| Nano dataset creation | [create_nano_datasets.md](create_nano_datasets.md) | Nano-set construction, qrels policy, BM25/dense candidates, reranking-hybrid safeguards, upload shape. |
| Generated Nano README | [NanoREADME.template.md](NanoREADME.template.md) | Hugging Face dataset-card template and fill checklist for generated Nano dataset READMEs. |
| Task documentation | [create_benchmark_tasks_document.md](create_benchmark_tasks_document.md) | Public task page policy, metadata JSON, examples, leakage notes, group index pages, prose quality review. |
| Dataset citation metadata | [dataset_citation_metadata.md](dataset_citation_metadata.md) | YAML citation/source metadata, reference confidence labels, language/category fields, citation audits. |
| Leaderboard metrics | [leaderboard_metrics.md](leaderboard_metrics.md) | Visible metric policy and rationale for nDCG, MRR, recall, accuracy, MAP, and stored top-ranking artifacts. |
| DuckDB warehouse and viewer semantics | [duckdb_schema.md](duckdb_schema.md) | Schema contract, tables, score targets, variants, viewer SQL, semantic rules, query recipes. |
| Space deployment | [huggingface_space_deploy.md](huggingface_space_deploy.md) | Public Hugging Face Space operations, DuckDB publishing, image refresh, verification, rollback. |
| Historical benchmark-scope rationale | [core_set_selection.md](core_set_selection.md) | Historical rationale for retired Core/Core (EN) presets and current Overall scope context. |

## Workflow Routes

### Run Or Compare Models

1. Use [new_model_results_workflow.md](new_model_results_workflow.md) when the
   run may become a contributed result.
2. Use [evaluation_policy.md](evaluation_policy.md) to decide prompts,
   attention, dtype, variants, target scope, offline mode, and coverage
   expectations.
3. Use [model_specific_benchmarking_notes.md](model_specific_benchmarking_notes.md)
   and [model_cards.md](model_cards.md) for model-specific settings.
4. Use [evaluation_runbook.md](evaluation_runbook.md) for runnable commands.
5. Use [duckdb_schema.md](duckdb_schema.md) and
   [leaderboard_metrics.md](leaderboard_metrics.md) when interpreting or
   comparing results.

### Create Or Maintain Nano Datasets

1. Use [create_nano_datasets.md](create_nano_datasets.md) for conversion,
   sampling, qrels policy, candidate generation, validation, and upload shape.
2. Use [dataset_citation_metadata.md](dataset_citation_metadata.md) before
   editing dataset YAML citation/source metadata.
3. Use [NanoREADME.template.md](NanoREADME.template.md) for generated dataset
   README structure.
4. Use [create_benchmark_tasks_document.md](create_benchmark_tasks_document.md)
   for public task pages and task metadata JSON.

### Update Viewer Or Leaderboard Infrastructure

1. Read [`DESIGN.md`](../DESIGN.md) before changing viewer UI design.
2. Use [duckdb_schema.md](duckdb_schema.md) whenever schema, query semantics,
   score grouping, variants, or required columns change.
3. Use [huggingface_space_deploy.md](huggingface_space_deploy.md) for public
   Space, DuckDB publishing, image refresh, verification, and rollback.
4. Rebuild compiled viewer CSS from `hakari_bench/viewer/assets/app.tailwind.css`
   instead of hand-editing `hakari_bench/viewer/assets/app.css`.

## Artifact Map

| Artifact | Usually committed? | Source of truth / workflow |
| --- | --- | --- |
| Library code under `hakari_bench/` | Yes | Keep changes within module boundaries described in AGENTS.md. |
| Dataset YAML under `config/datasets/` and `config/dataset_collections/` | Yes | [create_nano_datasets.md](create_nano_datasets.md), [dataset_citation_metadata.md](dataset_citation_metadata.md). |
| Model cards under `config/model_cards/` | Yes | [model_cards.md](model_cards.md), [new_model_results_workflow.md](new_model_results_workflow.md). |
| Viewer config under `config/viewer/` | Yes | [duckdb_schema.md](duckdb_schema.md) and [`DESIGN.md`](../DESIGN.md) when UI behavior changes. |
| Tailwind source `app.tailwind.css` and compiled `app.css` | Yes, together | Rebuild with `scripts/build_viewer_css.py`; never hand-edit compiled CSS. |
| Per-task result JSON `.json.xz` | No in this repo | Submit to the results dataset workflow in [contributing_results.md](contributing_results.md). |
| DuckDB files, viewer caches, local reports | No | Rebuild through [evaluation_runbook.md](evaluation_runbook.md) or deployment docs. |
| Generated Nano dataset artifacts under `output/` | No unless explicitly requested | Keep generated large artifacts out of the repo by default. |
| Local progress checklists and scratch work under `tmp/` | No | Use for long-running audits or benchmark waves only. |

## Before Editing

- For behavioral code changes, add or update focused tests first when practical.
- For documentation changes, keep reusable project workflows under `docs/`;
  skill files may point to docs, but they should not be the only source.
- For benchmark evaluation changes, update both runnable examples and policy
  text when the expected behavior changes.
- For viewer schema or query changes, keep [duckdb_schema.md](duckdb_schema.md)
  in sync.
- For public docs or dataset metadata, avoid local-only paths and do not invent
  citations, sources, or human verification status.
