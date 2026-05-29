# NanoRTEB / NanoAILAStatutes

## Overview

`NanoRTEB / NanoAILAStatutes` is the AILA statute retrieval task in RTEB.
Long Indian legal situation descriptions retrieve relevant statutory provisions.

## Details

### What the Original Data Measures

[Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal
Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf) defines a statute retrieval
subtask alongside precedent retrieval. Given a legal situation, the system must
retrieve statutory provisions that help answer or analyze the scenario.

[Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb)
lists AILA statutes as an open English legal retrieval task and emphasizes
RTEB's focus on realistic enterprise retrieval. This split is therefore a
long-query-to-shorter-statute retrieval problem, not general legal QA.

### Observed Data Profile

The split has 50 queries, 82 documents, and 217 positive qrel rows. Queries are
the same long legal situations as the case-doc task and average 3,038.42
characters. Statute documents average 1,972.63 characters. Every query has
multiple positives, averaging 4.34 statutory provisions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1647 and hit@10 = 0.6200. It ranks only 6 queries at rank 1 and 31 queries
within the top 10.

This is harder for BM25 than case retrieval because statutory provisions are
compact and abstract, while queries contain long fact patterns. Exact overlap
with a statute title may be sparse even when the legal provision is relevant.

### Training Data That May Help

Helpful data includes statute retrieval, legal issue classification, Indian
statutory interpretation, and legal fact-pattern-to-provision pairs. Hard
negatives should be statutes from related legal areas that share terms but do
not control the fact pattern.

### Synthetic Data Guidance

Generate legal scenarios from non-evaluation statutes and case summaries, then
link them to applicable provisions. Include multi-positive labels when several
sections jointly apply. Do not create only title-to-title pairs; the benchmark
uses long facts against statute text.

## Example Data

| Query | Positive document |
| --- | --- |
| Appellant calls in question legality of the judgment rendered by High Court confirming his conviction for offence and sentence of imprisonment for life as awarded by the learned Sessions Judge. Background facts as unfolded du ... [truncated 225 chars](3569 chars) | Title: Attempt to murder Desc: Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty or murder, shall be punished with imprisonment of eit ... [truncated 225 chars](1973 chars) |
| This appeal, by special leave, has been preferred against the judgment and order dated 23 February 2005 of the High Court (Aurangabad Bench), by which the appeal preferred by the appellants was dismissed and their conviction ... [truncated 225 chars](3266 chars) | Title: Dowry death Desc: (1) Where the death of a woman is caused by any burns or bodily injury or occurs otherwise than under normal circumstances within seven years of her marriage and it is shown that soon before her death ... [truncated 225 chars](856 chars) |
| The appellant before us was examined as prime witness in the trial of T.R. on the file of the Special Judge against the first respondent. The trial ended in conviction against the first respondent and when the appeal filed by ... [truncated 225 chars](2857 chars) | Title: Certain laws not to be affected by this Act Desc: Nothing in this Act shall affect the provisions of any Act for punishing mutiny and desertion of officers, soldiers, sailors or airmen in the service of the Government ... [truncated 225 chars](337 chars) |
| Whether sanction is required to initiate criminal proceedings in respect of offences is the question arising for consideration in these cases. The District Registrar lodged a complaint with the Inspector of Police, CBCID on 0 ... [truncated 225 chars](1664 chars) | Title: Punishment of criminal conspiracy Desc: (1) Whoever is a party to a criminal conspiracy to commit an offence punishable with death, 1 [imprisonment for life] or rigorous imprisonment for a term of two years or upwards, ... [truncated 225 chars](742 chars) |
| These appeals involve a pure question of law as to whether an award by which residue assets of a partnership firm are distributed amongst the partners on dissolution of the partnership firm requires registration. Briefly the ... [truncated 225 chars](1668 chars) | Title: Documents of which registration is compulsory Desc: (1) The following documents shall be registered, if the property to which they relate is situate in a district in which, and if they of have been executed on or after ... [truncated 225 chars](10961 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoAILAStatutes |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 82 |
| Positive qrels | 217 |
| Positives per query | avg 4.34 / min 2 / median 4.5 / max 5 |
| Multi-positive queries | 50 |
| BM25 nDCG@10 | 0.2070 |
| BM25 hit@10 | 0.6600 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2711 |
| Dense hit@10 | 0.7600 |
| Dense Recall@100 | 1.0000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2564 |
| Reranking hybrid hit@10 | 0.7400 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 82 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 3,038.42 |
| Document length avg chars | 1,972.63 |

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf), task paper.
- [AILA 2019 Precedent & Statute Retrieval Task](https://doi.org/10.5281/zenodo.4063986), dataset record.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | task paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | dataset record | https://doi.org/10.5281/zenodo.4063986 |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRTEB
  backing_dataset: NanoRTEB
  dataset_id: hakari-bench/NanoRTEB
  task_name: NanoAILAStatutes
  split_name: NanoAILAStatutes
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoAILAStatutes.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 82
    positive_qrels: 217
  positives_per_query:
    average: 4.34
    min: 2
    median: 4.5
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 3038.42
    document_mean: 1972.63
  bm25:
    ndcg_at_10: 0.20697288076497222
    hit_at_10: 0.66
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2069728808
      hit_at_10: 0.66
      recall_at_100: 1.0
      candidate_count_min: 82
      candidate_count_max: 82
      candidate_count_mean: 82.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2710663066
      hit_at_10: 0.76
      recall_at_100: 1.0
      candidate_count_min: 82
      candidate_count_max: 82
      candidate_count_mean: 82.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2563930595
      hit_at_10: 0.74
      recall_at_100: 1.0
      candidate_count_min: 82
      candidate_count_max: 82
      candidate_count_mean: 82.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
