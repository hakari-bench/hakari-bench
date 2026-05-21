# MNanoBEIR

## Overview

MNanoBEIR is the multilingual NanoBEIR retrieval group. It contains compact
BEIR-style retrieval tasks for thirteen non-English language variants: Arabic,
German, Spanish, French, Italian, Japanese, Korean, Norwegian, Portuguese,
Serbian, Swedish, Thai, and Vietnamese. Each language variant contains the same
thirteen NanoBEIR source tasks, covering argument retrieval, fact-checking,
entity search, finance QA, multi-hop QA, web passage retrieval, biomedical
retrieval, duplicate question retrieval, scientific-paper retrieval, and debate
argument retrieval.

This group is useful because it separates two hard problems that are often
mixed together: the BEIR source-task relation and multilingual retrieval. A
model must understand whether the task wants a counterargument, a duplicate
question, a Wikipedia evidence passage, a scientific paper, or a biomedical
document, while also handling translated or localized text in scripts ranging
from Arabic and Thai to Japanese, Korean, Cyrillic Serbian, and Latin-script
European languages.

## Details

### What the Original Group Measures

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)
introduced a broad retrieval benchmark spanning multiple task families rather
than a single passage-retrieval setting. The BEIR paper emphasizes diversity in
task type, domain, query length, document length, annotation strategy, and
lexical bias. The MNanoBEIR group inherits that BEIR framing through compact
NanoBEIR tasks, then extends it across multiple languages.

The [NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)
packages smaller BEIR subsets with 50 queries and up to 10,000 documents per
task. [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
describes the larger multilingual evaluation setting that motivates language
coverage and cost-aware retrieval subsets. In MNanoBEIR, the result is a
regular grid: thirteen languages by thirteen compact BEIR-derived retrieval
tasks.

### Subtask Coverage

The thirteen base tasks cover these retrieval families:

- **Argument retrieval:** `NanoArguAna` retrieves counterarguments, while
  `NanoTouche2020` retrieves debate-style argument passages.
- **Fact-checking evidence retrieval:** `NanoFEVER`, `NanoClimateFEVER`, and
  `NanoSciFact` retrieve Wikipedia or scientific evidence for factual or
  scientific claims.
- **Question answering and web retrieval:** `NanoMSMARCO`, `NanoNQ`, and
  `NanoHotpotQA` retrieve answer-bearing passages for web search, natural
  questions, and multi-hop questions.
- **Duplicate and entity retrieval:** `NanoQuoraRetrieval` retrieves duplicate
  questions, and `NanoDBPedia` retrieves entity pages.
- **Domain-specific retrieval:** `NanoFiQA2018` covers finance answers,
  `NanoNFCorpus` covers biomedical and nutrition evidence, and `NanoSCIDOCS`
  covers scientific related-paper retrieval.

All thirteen languages use the same source-task grid. That makes language-level
comparisons cleaner than groups where each language has a different task mix.
The English NanoBEIR group is documented separately as `NanoBEIR-en`; this page
summarizes the multilingual MNanoBEIR task documents under the `MNanoBEIR`
directory.

### Observed Group Profile

Across the 169 MNanoBEIR task pages, the group contains 8,437 queries, 61,048
positive qrels, and 737,399 split-local candidate documents. The document count
is a sum over split-local pools, not a deduplicated multilingual corpus size.
Most tasks have 50 queries; `NanoTouche2020` has 49 queries per language, so
each language totals 649 queries.

The group average is 7.24 positives per query, but the distribution is driven by
multi-positive tasks. `NanoArguAna` and `NanoMSMARCO` are single-positive in
this Nano grid. `NanoDBPedia`, `NanoNFCorpus`, and `NanoTouche2020` contribute
many positives per query, and `NanoTouche2020` retains a high hit rate because
each debate topic has many acceptable argument passages. Query length is also
task-dependent: `NanoArguAna` has long translated arguments averaging 1,024.72
characters across languages, while `NanoNFCorpus` has short medical queries
averaging 23.33 characters. Document length ranges from very short Quora
question documents to long argument, medical, and scientific passages.

### BM25 Difficulty

The query-weighted BM25 nDCG@10 across MNanoBEIR is 0.4502, with query-weighted
hit@10 of 0.7272. BM25 is strongest on tasks with preserved named entities,
titles, or many acceptable positives. `NanoFEVER`, `NanoHotpotQA`,
`NanoQuoraRetrieval`, and `NanoSciFact` have high task-level averages. The
highest single split by nDCG@10 is Portuguese `NanoFEVER`, where entity and
claim wording often lead BM25 directly to evidence.

The hardest task families are `NanoFiQA2018`, `NanoClimateFEVER`, and
`NanoSCIDOCS`. Finance questions often need semantically matching advice rather
than exact words. Climate claims can require evidence with different scientific
phrasing. SCIDOCS asks for related papers, so the query title and positive paper
may share topic but not obvious lexical strings. The lowest single split by
nDCG@10 is Swedish `NanoFiQA2018`.

Language also matters, but not as a simple script effect. French, Italian,
Portuguese, and Spanish have the highest language-level BM25 nDCG averages in
this snapshot, while Serbian and Arabic are lower. Japanese and Korean have
shorter observed character counts, so character averages are not directly
comparable with Latin-script languages.

### Training Data That May Help

Useful training data should mix multilingual coverage with task-specific
supervision. For the QA and web-search tasks, multilingual MS MARCO-style
query-passage pairs, Natural Questions-style Wikipedia retrieval, and multi-hop
QA evidence retrieval are relevant. For fact-checking tasks, multilingual
claim-evidence data and scientific-claim retrieval pairs help. For argument
tasks, counterargument and debate passage data with stance-aware hard negatives
are important. For scientific and biomedical tasks, paper-title retrieval,
citation-context retrieval, medical search, and biomedical QA pairs are useful.

Training must exclude the exact MNanoBEIR queries, positives, qrels, and
translated candidate documents. Because the source tasks are common in retrieval
training pipelines, overlap audits are important for MS MARCO, NQ, FEVER,
Quora, NFCorpus, SCIDOCS, SciFact, and Touche-style argument data. Cross-lingual
training should also avoid using direct translations of the evaluation queries
as synthetic seeds.

### Synthetic Data Guidance

Synthetic data for MNanoBEIR should preserve both the source-task relation and
the target language surface. A generated duplicate question should be a true
duplicate, not just a same-topic question. A generated fact-checking query must
retrieve evidence that supports or refutes the claim. A generated SCIDOCS pair
should reflect scientific relatedness, not merely word overlap. For Arabic,
Japanese, Korean, Thai, Vietnamese, Serbian, and European languages, preserve
script, named entities, numbers, citations, biomedical terms, and code-like
fragments when present.

Hard negatives should be task-aware: same entity but wrong attribute for
DBPedia or FEVER, same topic but wrong stance for argument retrieval, same
medical term but wrong intervention for NFCorpus, and same paper topic but
unrelated contribution for SCIDOCS. Synthetic examples should not be generated
from MNanoBEIR evaluation query or positive text.

## Language Summary

| Language | Tasks | Queries | Docs | Qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ar` | 13 | 649 | 56,723 | 4,696 | 0.4042 | 0.6965 | 118.92 | 787.30 |
| `de` | 13 | 649 | 56,723 | 4,696 | 0.4285 | 0.6965 | 160.35 | 1009.80 |
| `es` | 13 | 649 | 56,723 | 4,696 | 0.4791 | 0.7519 | 158.51 | 991.68 |
| `fr` | 13 | 649 | 56,723 | 4,696 | 0.4877 | 0.7596 | 167.00 | 1031.91 |
| `it` | 13 | 649 | 56,723 | 4,696 | 0.4874 | 0.7535 | 156.57 | 985.00 |
| `ja` | 13 | 649 | 56,723 | 4,696 | 0.4714 | 0.7442 | 72.60 | 404.76 |
| `ko` | 13 | 649 | 56,723 | 4,696 | 0.4534 | 0.7427 | 76.68 | 455.63 |
| `no` | 13 | 649 | 56,723 | 4,696 | 0.4246 | 0.6888 | 140.06 | 879.95 |
| `pt` | 13 | 649 | 56,723 | 4,696 | 0.4866 | 0.7658 | 151.39 | 950.15 |
| `sr` | 13 | 649 | 56,723 | 4,696 | 0.3983 | 0.6795 | 149.21 | 885.38 |
| `sv` | 13 | 649 | 56,723 | 4,696 | 0.4232 | 0.7011 | 140.11 | 887.92 |
| `th` | 13 | 649 | 56,723 | 4,696 | 0.4416 | 0.7227 | 115.69 | 752.22 |
| `vi` | 13 | 649 | 56,723 | 4,696 | 0.4663 | 0.7504 | 134.96 | 869.21 |

## Task Family Summary

| Base task | Languages | Queries | Docs | Qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `NanoArguAna` | 13 | 650 | 47,255 | 650 | 0.3629 | 0.6338 | 1024.72 | 942.58 |
| `NanoClimateFEVER` | 13 | 650 | 44,304 | 1,924 | 0.2512 | 0.6138 | 126.73 | 1475.28 |
| `NanoDBPedia` | 13 | 650 | 78,585 | 15,054 | 0.5030 | 0.9092 | 34.46 | 321.23 |
| `NanoFEVER` | 13 | 650 | 64,948 | 741 | 0.7099 | 0.8508 | 44.89 | 1122.37 |
| `NanoFiQA2018` | 13 | 650 | 59,774 | 1,599 | 0.2504 | 0.4723 | 61.36 | 867.41 |
| `NanoHotpotQA` | 13 | 650 | 66,170 | 1,300 | 0.6793 | 0.9246 | 82.74 | 343.37 |
| `NanoMSMARCO` | 13 | 650 | 65,559 | 650 | 0.3369 | 0.5108 | 35.24 | 308.18 |
| `NanoNFCorpus` | 13 | 650 | 38,389 | 21,463 | 0.3132 | 0.6231 | 23.33 | 1456.31 |
| `NanoNQ` | 13 | 650 | 65,455 | 741 | 0.3512 | 0.5492 | 47.22 | 493.84 |
| `NanoQuoraRetrieval` | 13 | 650 | 65,598 | 910 | 0.6884 | 0.8477 | 48.53 | 56.96 |
| `NanoSCIDOCS` | 13 | 650 | 28,730 | 3,172 | 0.2601 | 0.7369 | 71.96 | 894.15 |
| `NanoSciFact` | 13 | 650 | 37,947 | 728 | 0.6483 | 0.8046 | 93.78 | 1382.83 |
| `NanoTouche2020` | 13 | 637 | 74,685 | 12,116 | 0.4985 | 0.9812 | 45.32 | 1939.08 |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing datasets | NanoBEIR language variants under MNanoBEIR |
| Hugging Face dataset pattern | `hakari-bench/NanoBEIR-{language}` |
| Languages | ar, de, es, fr, it, ja, ko, no, pt, sr, sv, th, vi |
| Category | natural_language |
| Subtasks | 169 |
| Base tasks | 13 |
| Total queries | 8,437 |
| Split-local documents | 737,399 |
| Positive qrels | 61,048 |
| Positives per query | avg 7.24, min 1, max 100 |
| Multi-positive queries | 4,459 |
| Query-weighted BM25 nDCG@10 | 0.4502 |
| Query-weighted BM25 hit@10 | 0.7272 |
| Mean query length | 134.00 chars, weighted by query count |
| Mean document length | 837.76 chars, weighted by split-local document count |

### Public Sources

- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur et al.; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen et al.; DOI: `10.48550/arXiv.2502.13595`.
- [NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir); 2024; Zeta Alpha.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.

### Hugging Face Links

- NanoBEIR collection: [zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)
- Example MNanoBEIR datasets:
  [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar),
  [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja),
  [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- MTEB repository: [embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: MNanoBEIR
  backing_dataset: MNanoBEIR
  dataset_id: hakari-bench/NanoBEIR-{language}
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 169
    base_tasks: 13
    languages: 13
    queries: 8437
    split_local_documents: 737399
    positive_qrels: 61048
  positives_per_query:
    average: 7.2357473035439135
    min: 1
    max: 100
    multi_positive_tasks: 143
    multi_positive_queries: 4459
  text_stats_chars:
    query_mean_weighted_by_queries: 134.00367429678798
    document_mean_weighted_by_documents: 837.7634889414416
  bm25:
    ndcg_at_10_query_weighted: 0.4501844200621074
    hit_at_10_query_weighted: 0.7271542017292165
    ndcg_at_10_unweighted_task_mean: 0.4502587566337278
    hit_at_10_unweighted_task_mean: 0.7275449824887574
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: NanoBEIR-pt__NanoFEVER
    hardest_task_by_ndcg_at_10: NanoBEIR-sv__NanoFiQA2018
  languages:
    - ar
    - de
    - es
    - fr
    - it
    - ja
    - ko
    - "no"
    - pt
    - sr
    - sv
    - th
    - vi
  base_tasks:
    - NanoArguAna
    - NanoClimateFEVER
    - NanoDBPedia
    - NanoFEVER
    - NanoFiQA2018
    - NanoHotpotQA
    - NanoMSMARCO
    - NanoNFCorpus
    - NanoNQ
    - NanoQuoraRetrieval
    - NanoSCIDOCS
    - NanoSciFact
    - NanoTouche2020
  tasks:
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-it__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoTouche2020.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoArguAna.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoClimateFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoDBPedia.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoFEVER.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoFiQA2018.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoHotpotQA.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoMSMARCO.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoNFCorpus.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoNQ.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoQuoraRetrieval.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoSCIDOCS.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoSciFact.md
    - path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoTouche2020.md
  learning:
    leakage_note: exclude MNanoBEIR evaluation queries, qrels, positive documents, translated candidate pools, and direct translations of evaluation items; audit source BEIR and multilingual training data before use
    useful_training_data:
      - multilingual question-passage retrieval pairs
      - multilingual claim-evidence and scientific-claim retrieval data
      - argument, counterargument, and debate passage retrieval data
      - duplicate-question and paraphrase retrieval clusters
      - biomedical, finance, entity, and scientific-paper retrieval pairs
      - language-specific hard negatives for each base task
    synthetic_data:
      document_generation: multilingual passages, claims, entity descriptions, scientific abstracts, medical documents, finance answers, duplicate questions, and debate arguments with preserved task relations
      question_generation: target-language search queries, claims, topic prompts, paper titles, counterarguments, duplicate-question variants, and medical or finance questions grounded in the selected document
      answerability: positives must satisfy the BEIR source-task relation in the target language, not only share translated keywords
    multi_positive_training: mixed_single_and_multi_positive_multilingual_retrieval_objective
  links:
    nano_dataset_pattern: https://huggingface.co/datasets/hakari-bench/NanoBEIR-{language}
    source_urls:
      - label: BEIR arXiv
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB arXiv
        url: https://arxiv.org/abs/2502.13595
      - label: NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
    source_notes: []
  references:
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      is_paper: false
      source_confidence: probably_correct
```
