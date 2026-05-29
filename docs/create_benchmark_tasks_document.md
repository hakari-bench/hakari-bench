# Creating Benchmark Task Documents

This document defines the policy and template for task-level benchmark
documentation under `docs/benchmark_tasks/`.

## Purpose

Each task page should let a reader understand what the retrieval task measures
before looking at leaderboard scores. A page should explain the source benchmark,
the concrete query and document shapes, the domain, the language, the BM25
baseline behavior, representative examples from the actual Nano tables, and the
kind of training data likely to improve the task without leaking evaluation
answers.

The pages are public GitHub Markdown. Do not include local paper paths, local
Obsidian links, local filesystem paths, private notes, or machine-specific URLs.

## Output Location

Write task documents under:

```text
docs/benchmark_tasks/{Nano-set name}/{task name}.md
```

For collection-level samples where the backing Nano dataset is different from
the collection name, include the backing dataset in the file name, for example:

```text
docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoMSMARCO.md
```

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
paths must not be written into generated Markdown or into the machine-readable
metadata block.

## Structured Fields

Place structured reference material after `## Example Data` and before
`## Machine-Readable Metadata`. This keeps the reader-facing flow focused on the
task first: overview, interpretation, then examples. The information table
should include at least:

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

Include positives-per-query rows in the visible information table only when they
add signal: for example, when the average is not exactly `1.00`, when the
minimum/maximum differ from `1`, or when any query has multiple positives. If
every query has exactly one positive qrel, omit the visible distribution rows.
Still keep the full positives-per-query statistics in the final YAML metadata
block so index builders and audits can use them.

Character averages are sufficient for the current version. Prefer
repository-maintained `query_text_stats` and `document_text_stats` when present.
If they are missing, compute them from the Nano `queries` and `corpus` tables.

## Required Page Structure

Use this structure unless a task needs a clearly better variant:

1. `# {Nano set} / {task}` title.
2. GitHub note, placed immediately after the title, warning that the page was
   generated by an LLM from source papers, dataset cards, repository metadata,
   and sampled data, and that it may contain mistakes. Keep it simple and
   reader-facing:

   ```markdown
   > [!NOTE]
   > This page was generated by an LLM using source papers, dataset cards,
   > repository metadata, and sampled benchmark data. It may contain mistakes;
   > please treat it as a reference aid rather than a definitive source.
   ```

3. `## Overview`: a paper-centered summary of what the benchmark task is. Start
   from the source paper when one exists: what retrieval problem the paper
   introduced, how the source data is framed, and what the concrete task asks a
   model to retrieve. If no source paper is available, summarize the benchmark
   task itself from the dataset card, official project page, and sampled data.
   The Overview should be task-specific prose, not a reusable sentence pattern
   such as "`{Task}` evaluates ... Queries are ...". Mention Nano packaging only
   when it changes how the source task is interpreted.
4. `## Details`: longer interpretive prose about the original task/data,
   source-paper findings, observed Nano data tendencies, BM25 difficulty, and
   why the benchmark differs from adjacent benchmarks.
5. `## Example Data`: random query-positive examples from the actual Nano split.
6. `## Dataset Information`: a Markdown table for structured facts.
7. `### Public Sources`: source papers, official pages, and dataset records.
8. `### Hugging Face Links`: the Nano dataset and source Hugging Face datasets
   when known.
9. `### Source Reference Table`: structured source title, year, type, URL.
10. `## Machine-Readable Metadata`: final YAML block for index generation.

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
uv run python scripts/extract_benchmark_task_examples.py --update-docs docs/benchmark_tasks
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

### BM25 Difficulty

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
- whether lexical matching is likely to be strong,
- whether the task is multilingual, domain-specific, code-oriented,
  long-document-oriented, or fact/evidence-oriented,
- whether qrels are mostly single-positive or multi-positive,
- how BM25 nDCG@10 and hit@10 should be read for this task,
- how dense and reranking hybrid candidate metrics should be read when they are
  available,
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

## Machine-Readable Metadata

Each task page must end with a fenced YAML block. This block is for future index
page generation and should be easy to parse without reading prose.

Use this marker immediately before the YAML block:

```markdown
<!-- benchmark-task-metadata:v1 -->
```

The block must be the final content in the Markdown file:

````markdown
## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMIRACL
  backing_dataset: NanoMIRACL
  dataset_id: hakari-bench/NanoMIRACL
  task_name: ja
  split_name: ja
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/ja.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1846
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 17.47
    document_mean: 297.912784
  bm25:
    ndcg_at_10: 0.5956231823
    hit_at_10: 0.94
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on upstream dev/test queries, qrels, or positive passages
    useful_training_data:
      - official non-overlapping train split
      - native-language question-to-passage retrieval pairs
      - non-overlapping source-corpus passage QA pairs
    synthetic_data:
      document_generation: native-language answer-bearing passages from the source collection style
      question_generation: native-language information needs answerable from those passages
      answerability: questions should be grounded in explicit facts, entities, or relations in the document
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMIRACL
    source_urls:
      - label: MIRACL unified source dataset
        url: https://huggingface.co/datasets/hotchpotch/miracl-hf-unified
    source_notes: []
  references:
    - title: "MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages"
      url: https://arxiv.org/abs/2210.09984
      year: 2023
      doi: 10.1162/tacl_a_00595
      is_paper: true
      source_confidence: definitive_paper_link
```
````

Metadata field guidance:

- `schema_version`: increment only for incompatible schema changes.
- `document_status`: use `first_pass`, `reviewed`, or `needs_review`.
- `document_path`: repository-relative path only.
- `source_research.primary_source_type`: use `task_paper`, `benchmark_paper`,
  `dataset_card`, `project_page`, `technical_article`, or `sample_inference`.
  Use `benchmark_paper` when the strongest paper source is the benchmark paper
  that includes the task, even if no standalone task paper was confirmed.
- `source_research.paper_pdf_or_html_checked`: boolean. Set `true` only when
  the paper PDF or HTML was inspected beyond title/abstract metadata.
- `source_research.no_paper_note`: short public note when no paper was
  confirmed, otherwise `null`.
- `bm25.source`: must be `dataset_candidate_subset` for the current Nano set
  unless the task explicitly uses a different source.
- `candidate_subsets`: records `bm25`, `dense`, and `reranking_hybrid`
  candidate metrics. `bm25` and `dense` are top-500 candidate subsets.
  `reranking_hybrid` is top-100 plus optional rank-101 safeguard.
- `learning.original_train_split`: use `available`, `not_found`, or `unknown`.
  Leave this as `unknown` unless the original source split was explicitly
  audited.
- `learning.evaluation_split_origin`: record the upstream split if known, such
  as `train`, `dev`, `test`, `validation`, or `unknown`.
- `learning.train_eval_overlap_audit`: use `passed`, `failed`,
  `not_applicable`, or `not_audited`. Use `not_audited` until query IDs,
  document IDs, source titles, and positive text overlap were checked.
- `learning.leakage_note`: short public warning about what not to train on.
- `learning.useful_training_data`: concise machine-readable list of existing
  data types that may teach the domain without using evaluation answers.
- `learning.synthetic_data`: concise machine-readable hints for what synthetic
  documents and questions to generate. These are for index/filter pages and
  should mirror the prose in `### Synthetic Data Guidance`.
- `learning.multi_positive_training`: use `multi_positive_objective` when the
  qrels contain multiple positives for a meaningful share of queries, otherwise
  `single_positive_question_document_focus`.
- `references[].url`: use the arXiv URL first when one exists.
- `links.source_urls`: structured `{label, url}` objects with public URLs only.
  These may include Hugging Face datasets, project pages, or source repositories.
- `links.source_notes`: optional non-URL source notes from README metadata.

## Document Template

Use this template for new pages:

````markdown
# {Nano set} / {task name}

> [!NOTE]
> This page was generated by an LLM using source papers, dataset cards,
> repository metadata, and sampled benchmark data. It may contain mistakes;
> please treat it as a reference aid rather than a definitive source.

## Overview

{About 500 English characters summarizing what this benchmark task is. When a
paper exists, ground the overview in the paper: what problem the paper introduced,
how the data was constructed or adapted, what the query and document sides
represent, and what retrieval behavior is being tested. When no paper exists,
summarize the task from the dataset card, official page, repository metadata, and
sampled data. Avoid a fill-in-the-blank pattern such as "`{Task}` evaluates ...
Queries are ..."; the paragraph should contain details that would not fit most
other tasks in the same group.}

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

### BM25 Difficulty

{Explain BM25 nDCG@10 and hit@10 for this task. Include concrete patterns from
the Nano BM25 candidate ranking when useful, such as cases where lexical matching
finds the topic but misses intent equivalence.}

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

## Example Data

{Five deterministic random query-positive examples. Generate with
`scripts/extract_benchmark_task_examples.py`. Use a two-column Markdown table,
include full character counts inline, and visibly truncate long content with
`[truncated 225 chars](N chars)`.}

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | {Nano set} |
| Backing dataset | {Backing dataset} |
| Task / split | {Task or split} |
| Hugging Face dataset | [{dataset_id}](https://huggingface.co/datasets/{dataset_id}) |
| Language | {language} |
| Category | {natural_language or code} |
| Queries | {query_count} |
| Documents | {document_count} |
| Positive qrels | {qrel_count} |
| Avg positives / query | {avg_positives_per_query; omit this row when all queries have exactly one positive} |
| Positives per query (min / median / max) | {min} / {median} / {max; omit this row when all queries have exactly one positive} |
| Queries with multiple positives | {count} ({percent}%; omit this row when all queries have exactly one positive} |
| BM25 nDCG@10 | {bm25_ndcg_at_10} |
| BM25 hit@10 | {bm25_hit_at_10} |
| BM25 Recall@100 | {bm25_recall_at_100} |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | {dense_ndcg_at_10} |
| Dense hit@10 | {dense_hit_at_10} |
| Dense Recall@100 | {dense_recall_at_100} |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | {reranking_hybrid_ndcg_at_10} |
| Reranking hybrid hit@10 | {reranking_hybrid_hit_at_10} |
| Reranking hybrid Recall@100 | {reranking_hybrid_recall_at_100} |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | {100 or 100-101} |
| Reranking hybrid safeguard rows | {safeguard_positive_rows} |
| Query length avg chars | {query_mean_chars} |
| Document length avg chars | {document_mean_chars} |

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

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: {Nano set}
  backing_dataset: {Backing dataset}
  dataset_id: {dataset_id}
  task_name: {task_name}
  split_name: {split_name}
  language: {language}
  category: {category}
  document_path: docs/benchmark_tasks/{Nano-set name}/{task name}.md
  source_research:
    primary_source_type: {task_paper|benchmark_paper|dataset_card|project_page|technical_article|sample_inference}
    paper_pdf_or_html_checked: {true|false}
    no_paper_note: {null or public note}
  counts:
    queries: {query_count}
    documents: {document_count}
    positive_qrels: {qrel_count}
  positives_per_query:
    average: {avg_positives_per_query}
    min: {min_positives}
    median: {median_positives}
    max: {max_positives}
    multi_positive_queries: {multi_positive_query_count}
    multi_positive_query_percent: {multi_positive_query_percent}
  text_stats_chars:
    query_mean: {query_mean_chars}
    document_mean: {document_mean_chars}
  bm25:
    ndcg_at_10: {bm25_ndcg_at_10}
    hit_at_10: {bm25_hit_at_10}
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: {bm25_ndcg_at_10}
      hit_at_10: {bm25_hit_at_10}
      recall_at_100: {bm25_recall_at_100}
      candidate_count_min: {bm25_candidate_count_min}
      candidate_count_max: {bm25_candidate_count_max}
      candidate_count_mean: {bm25_candidate_count_mean}
      query_count: {query_count}
      query_coverage: {bm25_query_coverage}
      relevant_coverage_at_100: {bm25_relevant_coverage_at_100}
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: {dense_ndcg_at_10}
      hit_at_10: {dense_hit_at_10}
      recall_at_100: {dense_recall_at_100}
      candidate_count_min: {dense_candidate_count_min}
      candidate_count_max: {dense_candidate_count_max}
      candidate_count_mean: {dense_candidate_count_mean}
      query_count: {query_count}
      query_coverage: {dense_query_coverage}
      relevant_coverage_at_100: {dense_relevant_coverage_at_100}
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: {reranking_hybrid_ndcg_at_10}
      hit_at_10: {reranking_hybrid_hit_at_10}
      recall_at_100: {reranking_hybrid_recall_at_100}
      candidate_count_min: {reranking_hybrid_candidate_count_min}
      candidate_count_max: {reranking_hybrid_candidate_count_max}
      candidate_count_mean: {reranking_hybrid_candidate_count_mean}
      query_count: {query_count}
      query_coverage: {reranking_hybrid_query_coverage}
      relevant_coverage_at_100: {reranking_hybrid_relevant_coverage_at_100}
      safeguard_positive_rows: {reranking_hybrid_safeguard_positive_rows}
      rows_with_101_candidates: {reranking_hybrid_rows_with_101_candidates}
  learning:
    original_train_split: unknown
    evaluation_split_origin: {train|dev|test|validation|unknown}
    train_eval_overlap_audit: not_audited
    leakage_note: {short leakage warning}
    useful_training_data:
      - {existing_training_data_type}
    synthetic_data:
      document_generation: {synthetic_document_generation}
      question_generation: {synthetic_question_generation}
      answerability: {synthetic_answerability}
    multi_positive_training: {multi_positive_training}
  links:
    nano_dataset: https://huggingface.co/datasets/{dataset_id}
    source_urls:
      - label: {source_label}
        url: {source_url}
    source_notes: []
  references:
    - title: {title}
      url: {public_url}
      year: {year}
      doi: {doi}
      is_paper: true
      source_confidence: {source_confidence}
```
````

## Group Index Pages

Before scaling to all 500+ tasks, add group index pages such as:

```text
docs/benchmark_tasks/{Nano-set name}/index.md
```

Build index pages from the machine-readable metadata blocks. Each group index
should include:

- task name and document link,
- language and category,
- query/document/qrels counts,
- positives-per-query summary only when the task is not exactly one-positive per
  query,
- BM25 nDCG@10, hit@10, and Recall@100,
- Dense top-500 nDCG@10, hit@10, and Recall@100,
- Reranking hybrid top-100/top-101 nDCG@10, hit@10, Recall@100, candidate
  count range, and safeguard row count,
- average query/document character lengths,
- source status and primary paper title,
- document status.

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
6. Confirm BM25 nDCG@10 was computed from the Nano `bm25` top-500 table, not
   from a fresh local BM25 run.
7. Confirm positives-per-query statistics were computed from qrels.
8. Confirm exactly five random examples come from the selected Nano split when
   at least five qrel pairs are available.
9. Confirm sample data shows actual query and positive document text, not a
   summary, and that long samples are visibly truncated with original character
   count.
10. Confirm the final YAML metadata block parses successfully.
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
5. The BM25 section interprets the score. It should explain what BM25 is doing
   well, what it fails to distinguish, and include concrete patterns from the
   dataset-provided BM25 ranking when those patterns are informative.
6. The task-specific difficulty is explicit. For example, debate tasks should
   discuss stance and counterargument matching; duplicate-question tasks should
   discuss intent equivalence and paraphrase clusters; Wikipedia QA retrieval
   should discuss short fact queries and passage evidence; public-health FAQ
   retrieval should discuss procedural guidance and action-specific matching.
7. The training-data section is concise and technical. It recommends existing
   data types that teach the domain without using likely evaluation answers, and
   it includes a practical overlap warning for public train/dev/test data.
8. The synthetic-data section focuses on what documents and questions to
   generate. It should specify document genre, question style, answerability, and
   domain details. Do not spend this section on hard negatives.
9. The examples are actual query-positive text from the Nano split. They should
   be readable on GitHub, include full character counts, and show truncation
   clearly when content is shortened.
10. The page avoids generic filler. Replace broad statements such as "this task
    requires semantic understanding" with task-specific statements about the
    exact relation being retrieved.
11. The writing separates evidence from inference. If a claim comes from a
    paper, say so with a link. If it comes from inspecting the sampled Nano data,
    make that clear through wording such as "the sampled data shows" or "the
    observed BM25 ranking suggests".
12. The final page has a coherent reader flow: warning note, overview, details,
    samples, dataset information, public sources, and machine-readable metadata.
    A user should understand the task before reaching the tables and source
    lists.
