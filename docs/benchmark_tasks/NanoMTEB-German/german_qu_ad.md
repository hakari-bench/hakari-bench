# NanoMTEB-German / german_qu_ad

## Overview

`german_qu_ad` is the GermanQuAD-Retrieval split in `NanoMTEB-German`. Queries
are German extractive-QA questions, and documents are German Wikipedia
paragraphs. The retriever must select the context paragraph that contains the
answer, so the task tests high-precision German evidence retrieval.

## Details

### What the Original Data Measures

[GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://arxiv.org/abs/2104.12741)
introduces GermanQuAD as a hand-annotated German extractive QA dataset inspired
by SQuAD but built from German Wikipedia. The paper says passages are extracted
from German counterparts of SQuAD articles, short or low-quality passages are
filtered, and annotators are asked to write self-sufficient questions with lower
lexical overlap where possible.

The retrieval version turns the QA setup into context retrieval: the question is
the query and the answer-bearing German Wikipedia paragraph is the positive
document. This directly measures whether an embedding model can map native
German information needs to the paragraph that supports the answer.

### Observed Data Profile

The Nano split has 200 queries, 474 documents, and 200 positive qrels. Each
query has one positive. Queries average 54.88 characters and are short, natural
German questions. Documents average 1,937.65 characters, with page-title prefixes
and section-like text from Wikipedia.

The sampled questions ask about USB support, tuberculosis surgery history, U.S.
state admission, the molecular structure of ice, and Sichuan agriculture. They
are more direct than GerDaLIR and less open-domain than GermanDPR because the
corpus is only 474 documents in this Nano split.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.9042 and hit@10 = 0.9750. This is an easy lexical-retrieval split compared
with the other German tasks: 165 positives are ranked first.

The remaining misses show where semantic retrieval still matters. A question
such as "Wie kann die USA einen neuen Bundesstaat aufnehmen?" has the positive
at rank 12 in the sampled BM25 ranking, despite being topically obvious. Models
that understand paraphrase and answer-bearing context can improve on pure term
matching in these few cases.

### Training Data That May Help

The original GermanQuAD train split is relevant training data when allowed, but
the GermanQuAD test split and this Nano split should be excluded. Useful data
includes GermanQuAD train question-context pairs, German Wikipedia QA retrieval
pairs, and native German paraphrased questions with hard negatives from the same
article or section.

Machine-translated English QA can add coverage, but the source paper warns that
translated training data does not fully substitute hand-annotated target-language
data. Native German supervision is therefore preferable.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation German Wikipedia
paragraphs and generate answerable, self-sufficient German questions. Preserve
titles, section context, named entities, dates, quantities, and definitions.

For joint generation, create compact encyclopedic passages and questions with
explicit answer spans. Hard negatives should come from related pages or nearby
sections so the model learns fine-grained evidence selection. Do not use Nano
evaluation questions or positives as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Was versuchen die Umweltorganisationen wie CSE in Indien zu verbessern? (71 chars) | Rajasthan === Umweltorganisationen fördern traditionelles Sammeln von Regenwasser === Umweltorganisationen in Indien, wie das Centre for Science and Environment (CSE), haben vor über 20 Jahren damit begonnen, die alten tradit ... [truncated 225 chars](1933 chars) |
| Wann muss man die Zieletage in seillosen Aufzügen auswählen? (60 chars) | Aufzugsanlage === Seilloser Aufzug === An der RWTH Aachen im Institut für Elektrische Maschinen wurde ein seilloser Aufzug entwickelt und ein Prototyp aufgebaut. Die Kabine wird hierbei durch zwei elektromagnetische Synchron- ... [truncated 225 chars](1766 chars) |
| Warum sind Schwarze aus Überseegebieten in Frankreich tendenziell besser integriert als Schwarze aus Schwarzafrika? (115 chars) | Schwarze ==== Frankreich ==== Die Bevölkerung Frankreichs setzt sich aus zahlreichen Ethnien zusammen, darunter sind 2,5 bis 5 Millionen schwarze Menschen. Die meisten von ihnen sind Einwanderer oder deren Nachkommen aus den ... [truncated 225 chars](3198 chars) |
| In welcher Klimazone liegt Oklahoma City? (41 chars) | Oklahoma_City === Klima === Die Stadt befindet sich nach Köppen in der feucht-subtropischen Klimazone (Cfa). Dieses liegt in der Form des Ostseitenklimas vor. Das Klima ist ganzjährig humid mit einem Niederschlagsmaximum im J ... [truncated 225 chars](1293 chars) |
| In welcher Jahreszeit wird auf die Sommerzeit umgestellt? (57 chars) | Sommerzeit Frühling: Umstellung von Normalzeit auf Sommerzeit – die Uhr wird um eine Stunde ''vor''gestellt. Herbst: Umstellung von Sommerzeit auf Normalzeit – die Uhr wird um eine Stunde ''zurück''gestellt. Als Sommerzeit wi ... [truncated 225 chars](830 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-German |
| Backing dataset | NanoMTEB-German |
| Task / split | german_qu_ad |
| Hugging Face dataset | [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German) |
| Language | de |
| Category | natural_language |
| Queries | 200 |
| Documents | 474 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.9458 |
| BM25 hit@10 | 0.9950 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9321 |
| Dense hit@10 | 0.9550 |
| Dense Recall@100 | 0.9600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9427 |
| Reranking hybrid hit@10 | 0.9650 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 54.88 |
| Document length avg chars | 1,937.65 |

### Public Sources

- [GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://arxiv.org/abs/2104.12741); 2021; Timo Möller, Julian Risch, and Malte Pietsch; DOI: `10.48550/arXiv.2104.12741`.
- [ACL Anthology record for GermanQuAD and GermanDPR](https://aclanthology.org/2021.mrqa-1.4/); DOI: `10.18653/v1/2021.mrqa-1.4`.
- [mteb/germanquad-retrieval dataset card](https://huggingface.co/datasets/mteb/germanquad-retrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-German](https://huggingface.co/datasets/hakari-bench/NanoMTEB-German)
- Source dataset: [mteb/germanquad-retrieval](https://huggingface.co/datasets/mteb/germanquad-retrieval)
- Original source dataset: [deepset/germanquad](https://huggingface.co/datasets/deepset/germanquad)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval | 2021 | arXiv paper | https://arxiv.org/abs/2104.12741 |
| GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval | 2021 | proceedings paper | https://aclanthology.org/2021.mrqa-1.4/ |
| mteb/germanquad-retrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/germanquad-retrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-German
  backing_dataset: NanoMTEB-German
  dataset_id: hakari-bench/NanoMTEB-German
  task_name: german_qu_ad
  split_name: german_qu_ad
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-German/german_qu_ad.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2104.12741
    additional_source_urls:
    - https://aclanthology.org/2021.mrqa-1.4/
    - https://huggingface.co/datasets/mteb/germanquad-retrieval
    - https://huggingface.co/datasets/deepset/germanquad
  counts:
    queries: 200
    documents: 474
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 54.88
    document_mean: 1937.64557
  bm25:
    ndcg_at_10: 0.9458416423805717
    hit_at_10: 0.995
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude GermanQuAD test data, Nano queries, qrels, and positive
      passages likely to overlap with the evaluation split
    useful_training_data:
    - non-overlapping GermanQuAD train question-context pairs
    - German Wikipedia question-to-passage retrieval pairs
    - native German paraphrase and reformulation data for QA questions
    - hard negatives from related Wikipedia pages and sections
    synthetic_data:
      document_generation: German Wikipedia-style paragraphs with titles, sections,
        entities, dates, definitions, and numeric facts
      question_generation: self-contained German QA questions with answer evidence
        in the paragraph
      answerability: each positive paragraph should contain explicit evidence for
        the question
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-German
    source_urls:
    - label: GermanQuAD/GermanDPR arXiv
      url: https://arxiv.org/abs/2104.12741
    - label: ACL Anthology record
      url: https://aclanthology.org/2021.mrqa-1.4/
    - label: mteb/germanquad-retrieval
      url: https://huggingface.co/datasets/mteb/germanquad-retrieval
    - label: deepset/germanquad
      url: https://huggingface.co/datasets/deepset/germanquad
    source_notes: []
  references:
  - title: 'GermanQuAD and GermanDPR: Improving Non-English Question Answering and
      Passage Retrieval'
    url: https://arxiv.org/abs/2104.12741
    year: 2021
    doi: 10.48550/arXiv.2104.12741
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9458416424
      hit_at_10: 0.995
      recall_at_100: 1.0
      candidate_count_min: 474
      candidate_count_max: 474
      candidate_count_mean: 474.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9321433473
      hit_at_10: 0.955
      recall_at_100: 0.96
      candidate_count_min: 474
      candidate_count_max: 474
      candidate_count_mean: 474.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9427479421
      hit_at_10: 0.965
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```

