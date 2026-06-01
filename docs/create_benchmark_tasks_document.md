# Creating Benchmark Task Documents

This document defines the policy and template for reader-facing benchmark task
documentation under `task_docs/docs/`, plus the group index pages that summarize
each Nano set.

## Purpose

Each task page should let a reader understand what the retrieval task measures
before looking at leaderboard scores. A page should explain the source benchmark,
the concrete query and document shapes, the domain, the language, the BM25,
dense, and reranking-hybrid retrieval signals, representative examples from the
actual Nano tables, and the kind of training data likely to improve the task
without leaking evaluation answers.

The pages are public GitHub Markdown. Do not include local paper paths, local
Obsidian links, local filesystem paths, private notes, or machine-specific URLs.

## Output Location

Write task documents under:

```text
task_docs/docs/{Nano-set name}/{task name}.md
```

For collection-level samples where the backing Nano dataset is different from
the collection name, include the backing dataset in the file name, for example:

```text
task_docs/docs/MNanoBEIR/NanoBEIR-ja__NanoMSMARCO.md
```

Reader-facing task prose should be authored under `task_docs/docs/`. The
matching JSON metadata remains under `task_docs/metadata/`.

## Source Policy

Prefer task-level source metadata from `config/datasets/*.yaml` and
`config/dataset_collections/*.yaml`. If task-level metadata is absent, fall back
to dataset-level metadata, then to the Hugging Face dataset README, then to
upstream benchmark metadata.

For papers, check whether the original paper has an arXiv page. Use the arXiv
URL as the first source URL when it exists, even if an ACL Anthology, DOI,
publisher, OpenReview, or project page also exists. Still include the DOI or
official proceedings URL as secondary metadata when it is useful for citation
accuracy. When a paper exists, read the paper PDF or HTML, not only the abstract,
and use the paper's dataset construction, related work, limitations, retrieval
source, annotation policy, train/dev/test split, and baseline analysis to improve
the task explanation.

Source priority:

1. arXiv page for the original task or benchmark paper.
2. Official proceedings, DOI, OpenReview, publisher, or ACL Anthology page when
   no arXiv page exists, or as a secondary URL.
3. Official dataset card, project page, GitHub repository, or Hugging Face
   dataset.
4. Upstream benchmark source metadata.
5. Blog posts only when they are the canonical source and no stronger source is
   available.

For benchmark collections such as BEIR, MTEB, MIRACL, BIRCO, CodeRAG-Bench, or
domain-specific benchmark suites, distinguish three paper levels:

- `task_paper`: a paper primarily introducing the exact source task or dataset.
- `benchmark_paper`: a paper introducing the benchmark that includes this task
  and discusses its construction, split policy, table statistics, task category,
  evaluation setting, or limitations.
- `related_paper`: a paper about the general task family that does not define the
  evaluated dataset.

If no standalone task paper is found but a benchmark paper includes a section,
appendix entry, dataset table, or construction note for the task, treat that
benchmark paper as a source that must be read and reflected in the Details
section. Do not write "no paper was confirmed" in a way that implies no paper was
used; instead say that no standalone task paper was confirmed and cite the
benchmark paper for the available construction details. For example, Quora in
BEIR should use the BEIR paper's duplicate-question retrieval category, Quora
statistics, split construction, and overlap-removal notes, even though the Quora
Question Pairs record is the dataset source.

Do not invent a source paper just to make a task look citable. If only a dataset
card or project page is known, list it as a source URL and make that limitation
visible. In that case, explicitly say that no task or benchmark paper was
confirmed and that the interpretation is based on the official dataset card,
Hugging Face dataset, project page, technical article, and observed sample data.

When a paper is used in prose, cite it explicitly in the sentence that relies on
it, for example: `[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse
Languages](https://arxiv.org/abs/2210.09984) states that ...`. Do not hide paper
usage only in the source list.

When using a benchmark paper, inspect more than the abstract. Look for the task
overview figure, dataset statistics table, appendix entry for the task, split
construction, overlap or leakage mitigation, evaluation metric discussion,
baseline discussion, and limitations. Mention whichever of those items materially
changes the interpretation of the Nano task.

OB Wiki Search can be used as background research, but local wiki or paper-note
paths must not be written into generated Markdown or into task metadata JSON.

## Task Metadata JSON

Keep benchmark statistics and other structured task metadata outside the
reader-facing Markdown. Store one Pydantic-validated JSON file for each task at:

```text
task_docs/metadata/{Nano-set name}/{task file stem}.json
```

The JSON path mirrors the Markdown path. For example:

```text
task_docs/docs/NanoMIRACL/ja.md
task_docs/metadata/NanoMIRACL/ja.json
```

The metadata JSON should include at least:

- Nano set name.
- Backing dataset name.
- Backing Hugging Face dataset id.
- Task or split name.
- Language and category.
- Query count, document count, and positive qrels row count.
- BM25 nDCG@10, hit@10, and Recall@100 computed from the dataset's `bm25`
  top-500 candidate subset and positive qrels.
- Dense nDCG@10, hit@10, and Recall@100 computed from the dataset's
  `harrier_oss_v1_270m` top-500 candidate subset.
- Reranking hybrid nDCG@10, hit@10, and Recall@100 computed from the dataset's
  `reranking_hybrid` candidate subset. This subset is top-100 plus an optional
  rank-101 safeguard positive when the top-100 contains no qrels positive.
- Average query length and document length in characters.

Do not hand-maintain these statistics in Markdown prose. Generate or refresh
them from the Nano dataset tables with:

```bash
uv run python scripts/build_task_metadata_json.py task_docs/docs/{Nano-set name}/{task}.md
```

The Markdown source should contain the narrative task explanation only. Public
web pages may render a statistics table by combining Markdown with the matching
JSON metadata, but the authored Markdown should not duplicate the JSON values as
a manually maintained table.

Character averages are sufficient for the current version. Compute them from the
Nano `queries` and `corpus` tables so the JSON reflects the exact task split.
Repository-maintained `query_text_stats` and `document_text_stats` can be used
as an audit signal, but should not replace the generated task metadata.

## Required Page Structure

Use this structure unless a task needs a clearly better variant:

1. `# {Nano set} / {task}` title.
2. `## Overview`: a public web-page lead of about 120-180 English words, or
   roughly 500 Japanese characters when translated. Start from the source paper
   or source benchmark when one exists, then explain the concrete Nano task:
   what the model retrieves, query shape, document shape, language, domain,
   query/document/qrel scale, single-positive or multi-positive nature, main
   retrieval difficulty, and one sentence on what BM25, dense, and reranking
   hybrid reveal. Keep sampling and candidate-generation mechanics out of this
   section.
3. `## Details`: longer interpretive prose with the subheadings defined in
   `Interpretation Policy`. The Details section should explain what the task
   measures and how model researchers should read it, not how the Nano files
   were built.
4. `## Example Data`: random query-positive examples from the actual Nano split.
5. `### Public Sources`: source papers, official pages, and dataset records.
6. `### Hugging Face Links`: the Nano dataset and source Hugging Face datasets
   when known.
7. `### Source Reference Table`: structured source title, year, type, URL.

Do not include an LLM-generated-content note in the authored Markdown. Do not
embed machine-readable YAML metadata blocks or raw `Dataset Information` tables
in the task prose; keep structured values in the matching JSON metadata.

## Example Policy

Show five query-positive examples when possible. Select five queries by
deterministic random sampling, not by taking the head of the query table. For
each sampled query, use a positive qrel with matching query and corpus records.
Use the repository script so regenerated pages stay stable:

```bash
uv run python scripts/extract_benchmark_task_examples.py hakari-bench/NanoMMTEB-v2 argu_ana
```

For bulk refreshes, replace only the `## Example Data` sections with:

```bash
uv run python scripts/extract_benchmark_task_examples.py --update-docs task_docs/docs
```

Use a Markdown table with exactly two columns by default: `Query` and
`Positive document`. The visible table should focus on the actual query and
positive document text. Omit query/doc IDs, BM25 ranks, and extra count columns
unless a task specifically needs them. Append full character counts inline.
Truncate long content to the configured visible character limit and show the
full pre-truncation length with the compact marker
`[truncated 225 chars](1258 chars)`.

```markdown
| Query | Positive document |
| --- | --- |
| What is ...? (12 chars) | The answer-bearing passage ... [truncated 225 chars](1800 chars) |
```

For extremely long-context, legal, patent, medical, code, or documentation tasks,
use a vertical sample-block format only when the table would be unreadable on
GitHub:

```markdown
### Sample 1

| Field | Value |
| --- | --- |
| Query ID | `q1` |
| Positive Doc ID | `d1` |

**Query**

> Truncated query text ... [truncated from 2400 chars]

**Positive document**

> Truncated positive document text ... [truncated from 18000 chars]
```

Do not summarize samples. Show the actual query and positive document text from
the Nano tables. Long query or document text must be truncated to a readable
length, with the original character count visible, for example `[truncated from
20442 chars]`. Even when text is truncated, the reader should be able to tell the full
query and positive-document character counts.

## Interpretation Policy

The `Details` section should explain the data itself. Do not spend the section
explaining that this is a Nano subset or that the Nano format has query, corpus,
qrels, and BM25 tables. Mention Nano sampling only when the observed sampled
data changes how readers should interpret the task.

Use these subheadings inside `## Details`:

```markdown
### What the Original Data Measures

### Observed Data Profile

### BM25 Evaluation Profile

### Dense Evaluation Profile

### Reranking Hybrid Evaluation Profile

### Metric Interpretation for Model Researchers

### Query and Relevance Type Tendencies

### Representative Failure Modes

### Language- or Domain-Specific Notes

### Training and Leakage Notes

### Model Improvement Hints

### Training Data That May Help

### Synthetic Data Guidance
```

Discuss:

- what the task asks the model to retrieve,
- what the original paper or official dataset source says the dataset was built
  to evaluate,
- what the source paper says about dataset construction, annotation, split
  design, related benchmarks, baseline behavior, limitations, or intended use,
- what the actual Nano data looks like: query style, document genre, document
  length, positives per query, language, and domain,
- whether lexical matching, embedding similarity, or hybrid retrieval is likely
  to be strong,
- whether the task is multilingual, domain-specific, code-oriented,
  long-document-oriented, or fact/evidence-oriented,
- whether qrels are mostly single-positive or multi-positive,
- how BM25, dense, and reranking hybrid nDCG@10, hit@10, and Recall@100 should
  be read for this task,
- which query and relevance types define the task,
- which failure modes are likely to matter for model development,
- which language-specific or domain-specific quirks affect retrieval,
- what improvements would help first-stage retrievers and rerankers,
- what existing non-evaluation training data may help,
- what synthetic source documents and synthetic questions would be useful.

Avoid generic filler. Each final task page should include at least one
task-specific paragraph grounded in the original paper, dataset card, or
benchmark source.

If a source paper exists, cite it in prose. Good detail text should read like:

```markdown
[CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497)
reports that the benchmark aggregates programming solutions, online tutorials,
library documentation, StackOverflow posts, and GitHub repositories as retrieval
sources. This matters for this task because ...
```

If no source paper is confirmed, say so plainly:

```markdown
No source paper was confirmed for this task. The interpretation below is based
on the official Hugging Face dataset card, project metadata, and observed sample
queries and positives.
```

### Search Signal Subsections

Keep the BM25, Dense, and Reranking Hybrid subsections short. Each subsection
should be about 40-80 English words and include:

- nDCG@10, hit@10, and Recall@100.
- What this retrieval view captures for the task.
- One main limitation or failure tendency.

Do not put all metric interpretation in these subsections. Use
`### Metric Interpretation for Model Researchers` for the broader reading of
nDCG@10 versus Recall@100, first-stage candidate coverage, and reranker
evidence ordering.

### Metric Interpretation for Model Researchers

This subsection should explain how to read the visible scores for this specific
task. Cover:

- Whether nDCG@10 or Recall@100 is the more important signal for this task.
- Whether the task primarily tests top-rank ordering, candidate coverage,
  evidence selection, or all of them.
- What it means when BM25, dense, or reranking hybrid is strongest.
- For multi-positive tasks, explain that Recall@100 can remain low even when a
  candidate list is useful, because many judged positives may exist per query.
- For reranker-oriented tasks, explain whether top-100 candidate loss is still a
  main issue or whether the remaining challenge is ordering plausible evidence.

### Query and Relevance Type Tendencies

This subsection should describe the main query and relevance patterns. Cover:

- Main query categories and document genres.
- What counts as relevant.
- Which query types are lexical-heavy.
- Which query types require semantic matching.
- Which query types benefit from hybrid retrieval.
- Domain-specific forms such as entity facts, health phrases, legal questions,
  patent prior art, code intent, claims, argument topics, citation families, or
  long-document cited sources.

### Representative Failure Modes

This subsection should explain task-level mistakes that a model researcher would
want to diagnose. Cover 2-4 concrete patterns, such as:

- near-entity confusion,
- near-topic or domain-neighbor retrieval,
- wrong relation or wrong attribute,
- wrong evidence span inside a long document,
- code semantic mismatch despite identifier overlap,
- citation-family ambiguity,
- translation or normalization artifacts.

Use real query examples when available. Avoid describing only one model's
idiosyncratic errors; focus on failures implied by the task.

### Language- or Domain-Specific Notes

Use the generic heading when no narrower title is better, or adapt it to the
task:

- `### Japanese-Specific Notes`
- `### Code-Specific Notes`
- `### Legal-Specific Notes`
- `### Biomedical-Specific Notes`
- `### Patent-Specific Notes`
- `### Long-Document Notes`
- `### Multilingual Notes`

Cover tokenization, normalization, script, transliteration, spelling,
punctuation, date/number formats, domain terminology, long-document structure,
code/API semantics, or other task-specific matching problems. Say whether exact
terms must be preserved and whether dense retrieval helps bridge paraphrase or
translation artifacts.

### Training and Leakage Notes

This subsection should say what not to train on and what training exposure must
be disclosed. Cover:

- Evaluation queries, qrels, positive passages/documents, and source rows that
  should be excluded.
- Upstream train/dev/test split risks.
- Public benchmark overlap risks, especially for common sources such as MS
  MARCO, NQ, FEVER, CodeSearchNet, HumanEval, MIRACL, NFCorpus, SciFact,
  SCIDOCS, legal datasets, patent datasets, and BRIGHT source documents.
- What a model report should disclose, such as whether the model saw the source
  benchmark, source corpus, translated evaluation text, or synthetic data derived
  from evaluation positives.

### Model Improvement Hints

This subsection should translate the task analysis into concrete modeling
directions. Cover:

- First-stage retriever improvements, such as lexical-semantic fusion,
  long-document chunking, code-aware encoding, entity grounding, or domain term
  preservation.
- Reranker improvements, such as relation-aware reranking, evidence-span
  selection, multi-positive/listwise training, or long-context evidence
  selection.
- Hard negative design, such as same entity but wrong relation, same statute but
  wrong legal issue, same API family but wrong behavior, same biomedical term
  but wrong outcome, or same patent topic but different mechanism.
- Synthetic data directions that teach the task-specific behavior without
  seeding from evaluation queries or positives.

### Training Data That May Help

This subsection should answer which existing datasets or supervised pairs could
teach the domain without using evaluation answers.

Cover these cases:

- If the original dataset provides a train split or official training data,
  state that it is the first source to inspect. Do not assume it may be used for
  a leaderboard unless the benchmark rules allow it.
- Always check split provenance. If the Nano task is derived from an upstream
  dev or test split, say that data likely to overlap with the benchmark, such as
  the same upstream dev/test split, should preferably be excluded from training.
  Recommend upstream train splits or other source data that are unlikely to
  overlap with the evaluation task.
- For public datasets, warn in practical terms that obvious overlap with the
  benchmark should be avoided. Detailed ID or text overlap audits are useful for
  production-quality training pipelines, but the reader-facing guidance should
  not make the first-pass task brief feel like an implementation checklist.
- State that learning the evaluation queries, qrels, or positive passages can
  inflate benchmark scores. For retrieval tasks, memorizing the answer passage is
  not the same as learning retrieval behavior.
- For code tasks, recommend source-aligned data such as documentation retrieval,
  DocPrompting-style NL-intent-to-doc pairs, StackOverflow QA, tutorials,
  migration guides, docstrings, issue-to-fix pairs, and API examples.
- For multilingual tasks, recommend native-language supervised pairs and
  same-language corpora rather than translated English-only pairs.
- Keep this subsection concise and technical. It should list the data types that
  help, not re-explain the entire benchmark.

### Synthetic Data Guidance

This subsection should explain what synthetic documents and questions to create.
It should be separate from `Training Data That May Help`.

Cover these cases:

- If synthetic data is recommended, specify the document genre, document
  contents, question style, question intent, and how the generated question
  should be answerable from the generated or selected document.
- Distinguish document-to-question generation from joint document-and-question
  generation. Document-to-question generation should use non-evaluation source
  documents. Joint generation should create both realistic source-style
  documents and questions with explicit answer grounding.
- Do not use evaluation split queries or positive passages as seeds for
  synthetic generation. For example, if a Nano task is derived from MIRACL dev,
  use MIRACL train or non-overlapping Wikipedia passages, not MIRACL dev/test
  positives.
- For multilingual tasks, prefer native-language synthetic queries and
  documents over translated English-only data.
- For code tasks, synthetic data should preserve executable/API semantics,
  identifiers, version constraints, stack traces, and realistic developer
  tasks.
- For legal, patent, medical, finance, or scientific tasks, synthetic documents
  should use realistic domain structure, terminology, citations, measurements,
  entities, and evidential wording.
- For multi-positive tasks, train with multi-positive objectives or listwise /
  distillation signals rather than reducing the task to one positive per query.

## External Metadata JSON

Each task page should have a matching metadata JSON file instead of an embedded
YAML metadata block. The Markdown file should end after the reader-facing
sections, usually after `### Source Reference Table`.

The JSON file must validate against `TaskMetadataDocument` in
`hakari_bench/task_docs.py`. It should use the top-level key `task_metadata` and
live at the mirrored path under `task_docs/metadata/`.

Minimal shape:

```json
{
  "task_metadata": {
    "schema_version": 1,
    "document_status": "first_pass",
    "nano_set": "NanoMIRACL",
    "backing_dataset": "NanoMIRACL",
    "dataset_id": "hakari-bench/NanoMIRACL",
    "task_name": "ja",
    "split_name": "ja",
    "language": "ja",
    "category": "natural_language",
    "document_path": "task_docs/docs/NanoMIRACL/ja.md",
    "source_research": {
      "primary_source_type": "task_paper",
      "paper_pdf_or_html_checked": true,
      "no_paper_note": null
    },
    "counts": {
      "queries": 200,
      "documents": 10000,
      "positive_qrels": 373
    },
    "positives_per_query": {
      "average": 1.865,
      "min": 1,
      "median": 1.0,
      "max": 8,
      "multi_positive_queries": 78,
      "multi_positive_query_percent": 39.0
    },
    "text_stats_chars": {
      "query_mean": 17.5,
      "document_mean": 173.3871
    },
    "bm25": {
      "ndcg_at_10": 0.6600634301,
      "hit_at_10": 0.935,
      "source": "dataset_candidate_subset"
    }
  }
}
```

Field guidance:

- `schema_version`: increment only for incompatible schema changes.
- `document_status`: use `first_pass`, `reviewed`, or `needs_review`.
- `document_path`: repository-relative Markdown path only.
- `source_research.primary_source_type`: use `task_paper`, `benchmark_paper`,
  `dataset_card`, `project_page`, `technical_article`, or `sample_inference`.
- `bm25.source`: must be `dataset_candidate_subset` for the current Nano set
  unless the task explicitly uses a different source.
- `candidate_subsets`: records `bm25`, `dense`, and `reranking_hybrid`
  candidate metrics. `bm25` and `dense` are top-500 candidate subsets.
  `reranking_hybrid` is top-100 plus optional rank-101 safeguard.
- `learning.*`, `links.*`, and `references[]`: optional structured support
  material for index pages, public rendering, and doc generation. Keep public
  URLs only; do not store local research paths.

## Document Template

Use this template for new pages:

````markdown
# {Nano set} / {task name}

## Overview

{120-180 English words. Write the public web-page lead. Include source paper or
benchmark lineage when available, what the model retrieves, query shape,
document shape, language, domain, query/document/qrel scale, single-positive or
multi-positive nature, the main retrieval difficulty, and one sentence on what
BM25, dense, and reranking hybrid reveal. Avoid implementation details, Nano
build procedure, and candidate-generation mechanics.}

## Details

### What the Original Data Measures

{Explain the original data or benchmark from the source paper, official dataset
card, or project page. Focus on what retrieval behavior is being tested, not on
Nano packaging. If a paper was used, cite it directly in prose, e.g.
`[Paper Title](url) reports that ...`. If no paper was confirmed, state that the
interpretation is based on public dataset cards, project pages, and sample data.}

### Observed Data Profile

{Summarize the actual sampled task with useful interpretation, not only counts:
query and document styles, recurring intents, multi-positive clusters, visible
data quirks, and what those imply for retrieval.}

### BM25 Evaluation Profile

{40-80 English words. Include BM25 nDCG@10, hit@10, and Recall@100. Say what
BM25 captures for this task and name one main limitation.}

### Dense Evaluation Profile

{40-80 English words. Include dense nDCG@10, hit@10, and Recall@100 from
`harrier_oss_v1_270m`. Say what embedding similarity captures for this task and
name one main limitation.}

### Reranking Hybrid Evaluation Profile

{40-80 English words. Include reranking hybrid nDCG@10, hit@10, and Recall@100.
Say whether hybrid is best for top-rank quality, candidate coverage, or both,
and what this implies for reranker evaluation.}

### Metric Interpretation for Model Researchers

{100-170 English words. Explain how to read nDCG@10 versus Recall@100 for this
task. Say whether the task primarily tests top-rank ordering, candidate
coverage, evidence selection, or all of them. Explain what it means if BM25,
dense, or hybrid is strongest. For multi-positive tasks, explain how the number
of positives changes Recall@100 interpretation.}

### Query and Relevance Type Tendencies

{100-170 English words. Describe main query categories, document genres, and
what counts as relevant. Say which query types are lexical-heavy, which require
semantic matching, and which benefit from hybrid retrieval. Use task-specific
categories such as entity facts, legal questions, code intent, biomedical
phrases, claims, arguments, citations, or long-document sources.}

### Representative Failure Modes

{100-180 English words. Describe 2-4 task-level failure patterns. Use real query
examples when available. Explain whether errors are near-entity confusions,
near-topic/domain-neighbor misses, wrong-relation errors, evidence-selection
errors, code semantic mismatches, citation-family ambiguity, long-document
dilution, or translation artifacts.}

### {Language- or Domain-Specific Notes}

{80-150 English words. Replace the heading with a specific title when useful,
such as `Japanese-Specific Notes`, `Code-Specific Notes`, `Legal-Specific
Notes`, `Biomedical-Specific Notes`, `Patent-Specific Notes`,
`Long-Document Notes`, or `Multilingual Notes`. Discuss tokenization,
normalization, scripts, transliteration, spelling, punctuation, dates/numbers,
domain terminology, long-document structure, code/API semantics, and whether
exact terms must be preserved.}

### Training and Leakage Notes

{80-150 English words. Say which evaluation queries, qrels, positives, source
rows, or upstream splits should be excluded. Mention benchmark overlap risks and
what training exposure should be disclosed when reporting model scores.}

### Model Improvement Hints

{80-150 English words. Translate the task analysis into modeling directions:
first-stage retriever improvements, reranker improvements, hard negative design,
and synthetic data directions. Keep the advice specific to this task.}

### Training Data That May Help

{List concise, technical existing-data recommendations. Mention the official
train split when available, but warn that upstream dev/test sets, or other data
likely to overlap with the benchmark, should preferably be excluded. Keep
detailed overlap-audit mechanics in metadata or implementation notes rather than
the main prose unless the task specifically needs them.}

### Synthetic Data Guidance

{Describe what synthetic source-style documents and questions to create. Separate
document-to-question generation from generating both documents and questions.
State that evaluation split queries and positive passages should not be used as
seeds.}

### Optional: Qrels Semantics

{Use this section only when relevance labels are multi-positive, graded,
citation-based, claim-evidence based, argument-based, or otherwise non-obvious.
Explain what a positive qrel means and how that affects metric interpretation.}

### Optional: Task Boundary Notes

{Use this section only when the task is easily confused with another task type,
such as QA versus retrieval, duplicate retrieval versus topical retrieval,
generation benchmark versus retrieval adaptation, or code search direction.}

### Optional: Long-Document Retrieval Notes

{Use this section for BRIGHT, legal, patent, long-context, full-document, or
documentation tasks where evidence may be buried inside a long document.}

### Optional: Benchmark Information Leakage

{Use this section for CodeSearchNet, HumanEval, public QA, public legal,
medical, benchmark-derived, or otherwise leakage-prone tasks with known
train/test or source-corpus overlap risks.}

### Optional: Comparison With Source Task

{Use this section only when the Nano task differs materially from the full
source task in corpus size, qrels semantics, language, document granularity,
translation, or retrieval direction.}

### Optional: Known Artifacts

{Use this section only when translation, OCR, synthetic generation, HTML
boilerplate, code formatting, source formatting, or candidate-pool artifacts are
visible enough to affect interpretation.}

## Example Data

{Five deterministic random query-positive examples. Generate with
`scripts/extract_benchmark_task_examples.py`. Use a two-column Markdown table,
include full character counts inline, and visibly truncate long content with
`[truncated 225 chars](N chars)`.}

### Public Sources

- [{Primary paper title, preferably arXiv when available}]({primary_public_url}); {year}; {authors}; DOI: `{doi}`.
- [{Dataset card or project page}]({public_url}).

### Hugging Face Links

- Nano dataset: [{dataset_id}](https://huggingface.co/datasets/{dataset_id})
- Source dataset: [{source_dataset_id}](https://huggingface.co/datasets/{source_dataset_id})

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| {title} | {year} | paper | {url} |
````

## Group Index Pages

Collection-level index pages should not use the full task template. They should
summarize the Nano set as a public entry point and then link to task pages. Use:

```text
task_docs/docs/{Nano-set name}/index.md
```

Use this reader-facing structure:

1. `# {Nano set}` title.
2. `## Overview`: about 150-250 English words explaining the benchmark group,
   source benchmark or paper, language/domain coverage, and what kind of
   retrieval behavior the group measures.
3. `## What This Group Measures`: the shared retrieval semantics of the group:
   single-evidence retrieval, multi-positive retrieval, duplicate-question
   retrieval, argument retrieval, scientific or biomedical retrieval, entity
   retrieval, monolingual/multilingual/cross-lingual behavior, and whether the
   group is native or translated.
4. `## Task Families`: bullets by task family, language family, domain, or
   retrieval setting. This section should make heterogeneous Nano sets easy to
   scan.
5. `## Dataset Shape`: task count, query/document/qrel totals, multi-positive
   distribution, task-family differences, document length differences, and
   language/domain caveats. Explain that document totals are split-local sums
   when that is how the metadata is aggregated.
6. `## Retrieval Behavior`: group-level BM25, dense, and reranking hybrid
   patterns. Include `### BM25 Profile`, `### Dense Profile`, and
   `### Reranking Hybrid Profile` when the group has enough tasks for those
   comparisons to be meaningful.
7. `## Task Summary`: navigation table linking to task pages. For multilingual
   or strongly heterogeneous groups, add `## Language Summary`, `## Task Family
   Summary`, or `## Outlier Tasks` before or after the task table when useful.
8. `## Interpretation Notes for Model Researchers`: how to compare languages,
   task families, domains, model families, and reranking versus retrieval
   behavior. Call out hit@10 saturation, multi-positive recall, lexical bias,
   and cases where dense or hybrid retrieval changes the interpretation.
9. `## Training and Leakage Notes`: group-level training suggestions and overlap
   cautions. Treat direct translations, upstream train/dev/test splits, and
   common benchmark mixtures as possible leakage sources.
10. `## Public Sources`: group-level source papers, official pages, dataset
    cards, and a compact source reference table.

Do not include machine-readable group metadata in the authored index page. The
index should read as a public web page, not as a metadata dump.

Build index pages from the task metadata JSON files. Each group index
summary table should include:

- task name and document link,
- language and category,
- query/document/qrels counts,
- positives-per-query summary only when it adds signal,
- BM25, dense, and reranking hybrid nDCG@10,
- the best nDCG@10 profile (`BM25`, `Dense`, `Reranking hybrid`, or `Mixed`),
- average query/document character lengths,
- source status and primary paper title when available.

Avoid oversized tables in the index. Put full metric payloads, candidate counts,
safeguard rows, and document status in `task_docs/metadata/`, not in the
reader-facing group table.

Group index pages should be authored one Nano set at a time. Use the metadata
JSON files and the task pages in `task_docs/docs/` as references, but write the
group prose manually. Do not bulk-generate these index pages from a template
script.

## Maintenance Checklist

Before publishing a batch:

1. Confirm every generated page has a Nano dataset link and at least one public
   source or a visible note that source metadata is missing.
2. Confirm arXiv was checked for every paper source and is used as the first URL
   when available.
3. Confirm that every cited paper was checked beyond the abstract when possible:
   use the PDF or HTML to inspect dataset construction, source data, splits,
   related work, baselines, limitations, and task-specific discussion.
4. If no source paper is confirmed, confirm the page says so and explains that
   the interpretation is based on official dataset cards, project pages,
   technical articles, Hugging Face metadata, and observed samples.
5. Confirm train/dev/test provenance. If the Nano task comes from an upstream
   dev/test split, the page must warn against training on that split and should
   recommend only non-overlapping train or source-corpus data.
6. Confirm BM25, dense, and reranking hybrid metrics were computed from the Nano
   candidate subset tables: `bm25` top-500, `harrier_oss_v1_270m` top-500, and
   `reranking_hybrid` top-100 plus optional rank-101 safeguard. Do not replace
   dataset-provided BM25 with a fresh local BM25 run.
7. Confirm positives-per-query statistics were computed from qrels.
8. Confirm exactly five random examples come from the selected Nano split when
   at least five qrel pairs are available.
9. Confirm sample data shows actual query and positive document text, not a
   summary, and that long samples are visibly truncated with original character
   count.
10. Confirm the matching task metadata JSON validates successfully.
11. Confirm no generated benchmark outputs, caches, local paper paths, local wiki
   paths, or private scratch artifacts are committed.

## Final Prose Quality Review

After generating a task page, do a final pass specifically for writing quality
and usefulness. The page should not feel like a statistics dump. It should help a
reader understand what kind of retrieval behavior the task rewards, why the task
is difficult, and what data would plausibly teach the domain.

Use this checklist before considering a generated task page ready:

1. The overview explains the original benchmark or source dataset first, then
   explains the concrete Nano task. It describes the task itself, not the
   Markdown file or the Nano packaging.
2. The source discussion cites the paper, benchmark paper, dataset card, or
   project page in the sentences that depend on that source. When no paper was
   confirmed, the page says so plainly and does not pretend that a paper-backed
   interpretation exists.
3. The details section includes at least one paragraph grounded in the source
   paper or official dataset card: dataset construction, annotation workflow,
   source corpus, split design, benchmark purpose, or known limitations.
4. The observed data profile goes beyond counts. It names visible query types,
   document genres, recurring domains, language-specific issues, entity or
   terminology patterns, multi-positive clusters when present, and any quirks
   that affect retrieval.
5. The search signal sections are concise. BM25, dense, and reranking hybrid
   each state the visible metrics, what signal the candidate view captures, and
   one limitation. They should not become long essays.
6. The metric interpretation section explains how to read nDCG@10, hit@10, and
   Recall@100 for this task. It should distinguish top-rank ordering, candidate
   coverage, evidence selection, and multi-positive relevance when applicable.
7. The task-specific difficulty is explicit. For example, debate tasks should
   discuss stance and counterargument matching; duplicate-question tasks should
   discuss intent equivalence and paraphrase clusters; Wikipedia QA retrieval
   should discuss short fact queries and passage evidence; public-health FAQ
   retrieval should discuss procedural guidance and action-specific matching.
8. Query and relevance type tendencies are concrete. They should name the
   recurring query forms and explain what counts as relevant, rather than only
   saying that the task requires semantic understanding.
9. Representative failure modes are useful for model debugging. They should name
   near-entity, near-topic, wrong-relation, long-document, code, legal, patent,
   biomedical, translation, or citation-style errors as appropriate.
10. The language/domain-specific section explains the practical matching issues:
    tokenization, normalization, scripts, domain terminology, long documents,
    code/API semantics, or other task-specific constraints.
11. The training-data section is concise and technical. It recommends existing
   data types that teach the domain without using likely evaluation answers, and
   it includes a practical overlap warning for public train/dev/test data.
12. The synthetic-data section focuses on what documents and questions to
   generate. It should specify document genre, question style, answerability, and
   domain details. Hard negatives can be mentioned when they are central to the
   task.
13. The examples are actual query-positive text from the Nano split. They should
   be readable on GitHub, include full character counts, and show truncation
   clearly when content is shortened.
14. The page avoids generic filler. Replace broad statements such as "this task
    requires semantic understanding" with task-specific statements about the
    exact relation being retrieved.
15. The writing separates evidence from inference. If a claim comes from a
    paper, say so with a link. If it comes from inspecting the sampled Nano data,
    make that clear through wording such as "the sampled data shows" or "the
    observed BM25 ranking suggests".
16. The final page has a coherent reader flow: warning note, overview, details,
    samples, public sources, Hugging Face links, and source references. A user
    should understand the task before reaching the source lists.
