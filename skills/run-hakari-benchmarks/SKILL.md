---
name: run-hakari-benchmarks
description: Entry point for HAKARI-Bench evaluation work. Use when Codex is asked to benchmark or evaluate embedding models on NanoIR/Nano* datasets, choose prompt/truncate-dim/attention options, schedule GPU benchmark jobs, compare BM25, or refresh DuckDB and HTML leaderboard reports.
---

# Run HAKARI-Bench Evaluations

The canonical evaluation procedure lives in
[`docs/benchmark_evaluation.md`](../../docs/benchmark_evaluation.md).

Before running or scheduling evaluations, read that document and follow it as
the source of truth for:

- model research,
- prompt and attention choices,
- dense, sparse, late-interaction, reranker, and BM25 commands,
- embedding variant policy,
- coverage audits before reporting results,
- DuckDB/HTML viewer refresh expectations.

Do not maintain evaluation command details in this skill file. Update
`docs/benchmark_evaluation.md` instead.
