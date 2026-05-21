# NanoMTEB-v2 / fever

## Overview

`fever` is a claim-to-evidence retrieval task derived from FEVER. Queries are
short factual claims, and relevant documents are Wikipedia passages that
support or refute the claim.

## Details

### What the Original Data Measures

[FEVER](https://arxiv.org/abs/1803.05355) was introduced for fact extraction
and verification: systems must retrieve evidence from Wikipedia and then decide
whether a claim is supported, refuted, or unverifiable. The MTEB retrieval
version uses the evidence-retrieval component, with hard negatives in this Nano
split supplied by the source MTEB dataset.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 229 positive qrels. Queries
average 50.56 characters and are concise factual claims. Documents average
565.98 characters and usually contain a Wikipedia title followed by a passage.
Most queries have one positive, with an average of 1.15 positives per query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8951 and hit@10 = 0.9950. It ranks 164 queries with a positive first, and the
median best positive rank is 1. The task is highly lexical in this Nano sample
because claims often include entity names that also appear in the evidence.

### Training Data That May Help

Useful data includes FEVER claim-evidence pairs, Wikipedia entity retrieval
pairs, fact-checking evidence datasets, and hard negatives with the same named
entities but different predicates.

### Synthetic Data Guidance

Generate claims from Wikipedia passages by changing relation, date, location,
occupation, or membership facts. Include negatives about the same entity so the
model must match the exact evidence, not only the entity name.

## Example Data

| Query | Positive document |
| --- | --- |
| One Flew Over the Cuckoo's Nest only won one Academy Award. (59 chars) | One Flew Over the Cuckoo's Nest (film) One Flew Over the Cuckoo 's Nest is a 1975 American comedy-drama film directed by Miloš Forman , based on the 1962 novel One Flew Over the Cuckoo 's Nest by Ken Kesey . The film stars Ja ... [truncated 225 chars](1023 chars) |
| Salt River Valley is on the Mississippi River. (46 chars) | Salt River Valley The Salt River Valley is an extensive valley on the Salt River in central Arizona , which contains the Phoenix Metropolitan Area . Although this geographic term still identifies the area , the name `` Valley ... [truncated 225 chars](525 chars) |
| Sky UK is a British telecommunications company. (47 chars) | United Kingdom The United Kingdom of Great Britain and Northern Ireland , commonly known as the United Kingdom ( UK ) or Britain , is a sovereign country in western Europe . Lying off the north-western coast of the European m ... [truncated 225 chars](5000 chars) |
| Kaya Scodelario is a director. (30 chars) | Kaya Scodelario Kaya Scodelario-Davis ( born Kaya Rose Humphrey ; March 13 , 1992 ) is an English actress . She made her acting debut as Effy Stonem on the E4 teen drama Skins ( 2007-2010 ) , for which she received recognitio ... [truncated 225 chars](1626 chars) |
| A fellow Protestant murdered King Henry III of France. (54 chars) | Henry III of France Henry III ( 19 September 1551 -- 2 August 1589 ; born Alexandre Édouard de France , Henryk Walezy , Henrikas Valua ) was a monarch of the House of Valois who was elected the monarch of the Polish-Lithuania ... [truncated 225 chars](2522 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | fever |
| Source task | FEVERHardNegatives |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Source dataset | [mteb/FEVER_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 229 |
| Positives per query | avg 1.15, min 1, median 1, max 4 |
| Multi-positive queries | 25 (12.50%) |
| BM25 nDCG@10 | 0.8951 |
| BM25 hit@10 | 0.9950 |
| Query length avg chars | 50.56 |
| Document length avg chars | 565.98 |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/FEVER_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/FEVER_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | source task paper | https://arxiv.org/abs/1803.05355 |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/FEVER_test_top_250_only_w_correct-v2 | 2024 | dataset card | https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: fever
  split_name: fever
  source_task: FEVERHardNegatives
  source_dataset_id: mteb/FEVER_test_top_250_only_w_correct-v2
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/fever.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 229
  positives_per_query:
    average: 1.145
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 25
    multi_positive_query_percent: 12.5
  text_stats_chars:
    query_mean: 50.565
    document_mean: 565.9753
  bm25:
    ndcg_at_10: 0.8951263986829078
    hit_at_10: 0.995
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB FEVER hard-negative test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 fever claims and evidence pages
    useful_training_data:
      - FEVER claim-evidence pairs
      - Wikipedia evidence retrieval data
      - fact-checking hard negatives
    synthetic_data:
      document_generation: Wikipedia-style passages with explicit factual evidence
      question_generation: short factual claims about entities and relations
      answerability: positive document should contain evidence for or against the claim
    multi_positive_training: optional
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
      - label: FEVER arXiv
        url: https://arxiv.org/abs/1803.05355
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/FEVER_test_top_250_only_w_correct-v2
        url: https://huggingface.co/datasets/mteb/FEVER_test_top_250_only_w_correct-v2
    source_notes: []
  references:
    - title: "FEVER: a Large-scale Dataset for Fact Extraction and VERification"
      url: https://arxiv.org/abs/1803.05355
      year: 2018
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
