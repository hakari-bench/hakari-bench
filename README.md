# ⚖️ HAKARI-Bench

> A Lightweight Benchmark for Comparing Retrieval Architectures and Efficiency
> Settings under Unified Conditions

<p align="left">
  📊 <a href="https://huggingface.co/spaces/hakari-bench/leaderboard">🤗 Leaderboard</a> | 
  📄 Paper [WIP]
</p>

HAKARI-Bench is a lightweight IR benchmark that rebuilds retrieval tasks as
small Nano-sets, making model selection, regression checks, quantization,
truncation, and reranking comparisons practical under the same conditions.

The name HAKARI refers to `⚖️ 秤` (hakari), the Japanese word for a weighing
scale.

## ✨ Highlights

- 🌍 **Broad coverage, fast iteration.** Run compact retrieval evaluations over
  35+ benchmark groups, 551+ tasks, and 43+ languages without the cost of full
  benchmark sweeps.
- 📈 **A high-fidelity ranking proxy.** Nano-set rankings reproduce official
  MTEB retrieval v2, MMTEB v2 retrieval, and English BEIR full rankings at
  Spearman > 0.97 on intersecting models and tasks.
- ⚙️ **Production settings are first-class.** Compare Matryoshka-style
  truncation, int8 and binary quantization, and float rescoring under unified
  conditions, not as one-off model-card anecdotes.
- 🧭 **One view across retrieval families.** Evaluate BM25, dense embeddings,
  sparse/SPLADE-style encoders, ColBERT-style late interaction models, and
  CrossEncoder or LLM-style rerankers with the same task format and metrics.
- 🔁 **Rerankers can be tested at benchmark scale.** Fixed candidate sets make
  reranker quality comparable across hundreds of multilingual and domain-heavy
  retrieval tasks.

## 🚀 Quick Start

Start with [docs/quickstart.md](docs/quickstart.md) for the shortest path from
installation to a local leaderboard:

- evaluate a SentenceTransformers-compatible dense model
- run BM25, sparse, late-interaction, or reranker evaluation
- rebuild a DuckDB results database
- open the local viewer
- prepare results for official submission

The full command reference and operational details live in the
[evaluation runbook](docs/evaluation_runbook.md).

## 📚 Documentation

- [Documentation map](docs/index.md): source-of-truth map, workflow routes, and
  artifact boundaries.
- [Quick start](docs/quickstart.md): install, evaluate, build DuckDB, and open
  the viewer.
- [Evaluation policy](docs/evaluation_policy.md): prompts, dtype, attention,
  variants, reranking, and coverage audits.
- [New model results workflow](docs/new_model_results_workflow.md): model
  research, validation, full evaluation, and result submission.
- [Benchmark scope](docs/benchmark_scope.md): task format, coverage, dataset
  locations, and intended use.
- [Custom model backends](docs/custom_model_backends.md): local wrappers and
  hosted dense, sparse, reranker, and late-interaction models.
- [Leaderboard metrics](docs/leaderboard_metrics.md): visible metrics and
  quality-efficiency score interpretation.
- [DuckDB schema](docs/duckdb_schema.md): result warehouse tables, viewer SQL,
  score targets, and variant handling.

## 🛠️ Development

Use Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group all
uv run --group all pytest -q
uv run ruff check .
uv run --group all ty check
```

Run `uv run tox` before submitting larger changes.

## 🙏 Acknowledgements

HAKARI-Bench builds on the lightweight evaluation idea behind
[NanoBEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir) and
the unified retrieval benchmark methodology established by BEIR, MTEB, and
MMTEB. It also relies on the broader retrieval ecosystem around
[Sentence Transformers](https://github.com/huggingface/sentence-transformers)
and [PyLate](https://github.com/lightonai/pylate).

## ⚠️ Disclaimer

HAKARI-Bench results are provided for informational and comparative purposes
only. Scores may be incomplete, inaccurate, or affected by dataset sampling,
upstream dataset changes, model or runtime configuration, library versions,
hardware, or implementation issues.

HAKARI-Bench, its maintainers, and contributors provide the software,
leaderboard data, and benchmark results "as is", without warranty of any kind.
To the maximum extent permitted by applicable law, they are not liable for any
loss, damage, or other consequence arising from use of, reliance on, or
interpretation of HAKARI-Bench results.

## 📄 License

The HAKARI-Bench software is released under the MIT License. See
[LICENSE](LICENSE). Nano-set datasets are derived from upstream datasets and
retain their respective license, terms, and attribution requirements.

## 👤 Main Author

Yuichi Tateno ([@hotchpotch](https://github.com/hotchpotch))
