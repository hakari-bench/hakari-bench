# Creating Nano Datasets From MTEB

This document defines the rules for creating Nano-style retrieval datasets from
the MTEB task registry and MTEB-compatible Hugging Face sources.

It complements `docs/create_nano_datasets.md`, which describes the generic Nano
dataset shape, qrels policy, corpus sampling, and BM25 generation. Use this
document when the source task is selected through MTEB, or when reorganizing the
NanoMTEB-family datasets.

## Goals

MTEB-derived Nano datasets should:

- follow the official MTEB benchmark grouping when one exists;
- avoid duplicate task weighting when a base task and a hard-negative task share
  the same underlying dataset;
- keep public Hugging Face dataset configs stable and source-oriented;
- preserve upstream source provenance in README and metadata;
- minimize `NanoMTEB-Misc` by placing tasks into benchmark, source-family, or
  language-family groups whenever there is a defensible grouping.

## Source Of Truth

Use the installed MTEB package as the authoritative source for task metadata.

The normal discovery flow is:

```bash
uv run --with mteb python - <<'PY'
import mteb

for benchmark in mteb.get_benchmarks():
    retrieval_tasks = [
        task.metadata.name
        for task in benchmark.tasks
        if task.metadata.type == "Retrieval"
    ]
    if retrieval_tasks:
        print(benchmark.name, len(retrieval_tasks), retrieval_tasks)
PY
```

For a specific task, inspect:

- `task.metadata.name`
- `task.metadata.dataset["path"]`
- `task.metadata.dataset["revision"]`
- `task.metadata.eval_splits`
- `task.metadata.hf_subsets`
- `task.metadata.languages`
- `task.metadata.reference`
- benchmark membership from `mteb.get_benchmarks()`

Dataset YAML files under `config/datasets/` are the local registry, but they
should not override MTEB registry metadata when recreating MTEB-derived Nano
datasets.

## Group Naming

The public Nano dataset name is the task group. Choose the group in this order.

1. Official MTEB benchmark family.
2. Independent benchmark or source-family collection.
3. Language-family collection with enough task volume.
4. `NanoMTEB-Misc` only as a final fallback.

### Official MTEB Families

If a retrieval task set can be extracted from `MTEB(name, vN)` or another
official MTEB benchmark name, use that benchmark as the primary grouping.

When the MTEB benchmark name explicitly includes v2 or a later version, include
that version in the Nano dataset name.

Examples:

| MTEB benchmark | Nano dataset |
|---|---|
| `MTEB(eng, v2)` | `NanoMTEB-v2` |
| `MTEB(Multilingual, v2)` | `NanoMMTEB-v2` |
| `MTEB(fas, v2)` | `NanoFaMTEB-v2` |
| `JMTEB(v2)` | `NanoJMTEB-v2` |
| `MTEB(cmn, v1)` | `NanoCMTEB` |
| `MTEB(rus, v1.1)` | `NanoRuMTEB` |
| `VN-MTEB (vie, v1)` | `NanoVNMTEB` |

For v1 families, the existing non-versioned names may remain for compatibility
unless a migration explicitly decides to version every family.

### Independent Source Families

Use a dedicated Nano dataset when the tasks form a clear benchmark or source
family with enough coverage to justify a standalone group even if they are not
exposed as an official `MTEB(name, vN)` benchmark.

Examples:

| Source family | Nano dataset |
|---|---|
| MuPLeR retrieval | `NanoMuPLeR` |
| IndicQA retrieval | `NanoIndicQA` |

Small source families should stay under `NanoMTEB-Misc` with source-based
configs instead of becoming standalone Nano datasets. This currently includes
EuroPIRQ retrieval, NeuCLIR 2022 retrieval, Cross-Lingual Semantic
Discrimination over WMT19/WMT21, and RuSciBench citation/cocitation retrieval.

### Language Families

Use `NanoMTEB-{Language}` when there is enough retrieval coverage in that
language but no official MTEB benchmark family fully captures the relevant
tasks.

This is appropriate for language collections such as Polish, because
`MTEB(pol, v1)` currently does not provide retrieval tasks even though there are
multiple Polish retrieval sources.

Language collections may include BEIR-derived translated datasets. `NanoBEIR`
itself is not recreated in this flow, but translated or adapted BEIR-derived
sources may still belong to language-specific groups.

Examples:

- `NanoMTEB-Polish`
- `NanoMTEB-Dutch`
- `NanoMTEB-Korean`

## Public Dataset Configs

In the uploaded Hugging Face dataset, configs are source groups, not MTEB task
subsets.

Use these config names:

- `mteb` for datasets under the official `mteb/` Hugging Face namespace;
- `{org_or_user}__{dataset_name}` for any other Hugging Face namespace.

Examples:

| Source dataset | Public config |
|---|---|
| `mteb/Quora-PLHardNegatives` | `mteb` |
| `mteb/MuPLeR-retrieval` | `mteb` |
| `clips/beir-nl-cqadupstack` | `clips__beir-nl-cqadupstack` |
| `clarin-pl/PUGG_IR` | `clarin-pl__PUGG_IR` |
| `GreenNode/nq-vn` | `GreenNode__nq-vn` |
| `eherra/EuroPIRQ-retrieval` | `eherra__EuroPIRQ-retrieval` |

Do not expose upstream MTEB `hf_subsets` as public Nano configs unless the
source dataset itself is a distinct data source. Put upstream source subsets,
language slices, and direction slices into split names and metadata.

## Split Naming

Splits are the evaluation tasks inside a source config.

Split names should be concise, stable, and source-local. They should encode the
source slice needed to distinguish tasks inside the same public config.

Examples:

| Group | Config | Split |
|---|---|---|
| `NanoMTEB-Polish` | `mteb` | `quora` |
| `NanoMTEB-Polish` | `mteb` | `nq` |
| `NanoMTEB-Polish` | `mteb` | `cqadupstack-android` |
| `NanoMuPLeR` | `mteb` | `pl` |
| `NanoMTEB-Misc` | `eherra__EuroPIRQ-retrieval` | `fi` |
| `NanoMTEB-Misc` | `mteb` | `2022-fa` |
| `NanoMTEB-Misc` | `Andrianos__clsd_wmt19_21` | `wmt19-de-fr` |
| `NanoMTEB-Misc` | `mlsa-iai-msu-lab__ru_sci_bench_cite_retrieval` | `cite-ru` |

The README and per-split metadata must record:

- MTEB task name;
- source dataset id and revision;
- upstream source subset or slice;
- source evaluation split;
- original reference and license target when known.

## Hard-Negative Consolidation

When a base task and a `HardNegatives` task use the same underlying dataset, do
not publish both as separate Nano tasks.

Instead:

1. Publish one Nano split.
2. Prefer the `HardNegatives` source for Nano creation.
3. Keep the base source in README or metadata as related provenance.
4. Do not include `HardNegatives` in the public split name unless it is needed
   to distinguish genuinely different tasks.

Examples:

| Base task | Hard-negative task | Nano group/config/split |
|---|---|---|
| `Quora-PL` | `Quora-PLHardNegatives` | `NanoMTEB-Polish` / `mteb` / `quora` |
| `NQ-PL` | `NQ-PLHardNegatives` | `NanoMTEB-Polish` / `mteb` / `nq` |
| `NeuCLIR2022Retrieval` | `NeuCLIR2022RetrievalHardNegatives` | `NanoNeuCLIR` / `mteb` / `2022-{lang}` |
| `NeuCLIR2023Retrieval` | `NeuCLIR2023RetrievalHardNegatives` | `NanoFaMTEB-v2` / `mteb` / `neuclir-2023` |

Treat the base and hard-negative tasks as separate only when MTEB metadata or
source inspection shows that the evaluation target is not the same underlying
dataset.

## `NanoMTEB-Misc` Policy

`NanoMTEB-Misc` is a last-resort group.

Do not place a task in `NanoMTEB-Misc` when any of the following is true:

- it belongs to an official MTEB benchmark family;
- it belongs to a recognizable source-family collection;
- it is one of several tasks in the same language and can fit a
  `NanoMTEB-{Language}` group;
- it is a BEIR-derived translated task that can fit a language group.

Examples of preferred placements:

| Task family | Preferred placement |
|---|---|
| Polish Quora/NQ/CQADupStack/FiQA/PUGG | `NanoMTEB-Polish` |
| Dutch BEIR-NL translated tasks | `NanoMTEB-Dutch` |
| Korean AutoRAG/LawIR/SQuADKorV1 | `NanoMTEB-Korean` addon sources |
| French FQuAD retrieval | `NanoMTEB-French` addon source |
| German government-service QA retrieval | `NanoMTEB-German` addon source |
| EuroPIRQ, NeuCLIR2022, CLSD-WMT, and RuSciBench sparse families | `NanoMTEB-Misc` |
| MuPLeR retrieval slices | `NanoMuPLeR` |

If a task remains in `NanoMTEB-Misc`, document why no benchmark, source-family,
or language-family grouping is appropriate.

## Creation Workflow

1. Inspect MTEB benchmarks with `mteb.get_benchmarks()`.
2. Select retrieval tasks from the intended official benchmark or source family.
3. Resolve source dataset id, revision, eval split, and source subset from MTEB
   metadata.
4. Apply hard-negative consolidation before counting planned Nano tasks.
5. Assign each planned row to:
   - group: public Nano dataset;
   - config: public source config;
   - split: source-local evaluation task;
   - source slice: upstream `hf_subset` or equivalent provenance.
6. Recreate the Nano dataset using the qrels, corpus sampling, and BM25 rules in
   `docs/create_nano_datasets.md`.
7. Verify that:
   - qrels are positive-only;
   - every qrel query and document exists in the selected Nano tables;
   - BM25 candidate lists include every positive document after forcing;
   - README and metadata record upstream source provenance.
8. Update `config/datasets/` and `config/dataset_collections/` to match the new
   public group/config/split layout.

## Reporting Planned Tasks

Before recreating or publishing a large regrouping, produce a table with these
columns:

- group;
- public config;
- split;
- MTEB/source task;
- source dataset;
- source revision;
- source slice;
- source eval split;
- status, such as `official`, `addon-regrouped`, or `historical-addon`;
- notes about hard-negative consolidation or overlap risks.

This report should be reviewed before writing upload-ready output directories.

## Overlap And Duplication Checks

Check for these cases before finalizing a group:

- base and `HardNegatives` variants from the same dataset;
- full benchmark tasks duplicated by historical Nano-only task-level variants;
- translated BEIR tasks already represented in another language group;
- multilingual source tasks where only one language slice should be selected for
  a language-specific group;
- source families that should remain together rather than being split only by
  language.

When in doubt, keep the grouping that best preserves benchmark provenance and
avoids double-counting the same retrieval problem.
