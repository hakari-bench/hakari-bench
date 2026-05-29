# MNanoBEIR / NanoBEIR-es / NanoFEVER

## Overview

FEVER is a Wikipedia fact verification benchmark. `NanoBEIR-es__NanoFEVER` is
the Spanish MNanoBEIR version: Spanish translated claims must retrieve Spanish
translated Wikipedia evidence pages. The task tests fact-checking evidence
retrieval for short claims across broad encyclopedic topics.

## Details

### What the Original Data Measures

[FEVER: a Large-scale Dataset for Fact Extraction and
VERification](https://arxiv.org/abs/1803.05355) introduces claims generated from
Wikipedia and annotated with evidence supporting or refuting the claim. For the
retrieval view used in BEIR, the first-stage problem is to find the evidence
documents that allow verification.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes FEVER as a
fact-checking retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 50 queries, 4,996 documents, and 57 positive
qrel rows. Most queries have one positive document, while 6 queries have
multiple positives. The average query length is 49.56 characters, and the
average document length is 1,301.14 characters.

The inspected claims concern Vic Mensa, Doctor Who, Menace II Society, Alex
Jones, and The Man in the Iron Mask. Documents are Spanish translated
Wikipedia-style pages that contain entity facts needed to verify the claim.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7776 and hit@10 = 0.9200. BM25 ranks a positive first for 33 queries, and the
median first-positive rank is 1.

BM25 is strong because claims often contain explicit entity names. The remaining
difficulty is verifying claims where the relevant evidence is not the most
obvious lexical match, where a claim is false, or where relation details such as
dates, roles, and directors must be found.

### Training Data That May Help

Useful training data includes non-overlapping FEVER evidence retrieval pairs,
Spanish or multilingual Wikipedia claim verification data, entity-centric
question-answer evidence pairs, and hard negatives from similar entity pages.

Training should exclude FEVER, BEIR, NanoBEIR, or translated Wikipedia claim
records likely to overlap with these evaluation claims or pages.

### Synthetic Data Guidance

For document-to-query generation, start from Spanish Wikipedia-style passages
and generate short factual claims. Include both supported and contradicted
claims about dates, occupations, works, memberships, and locations.

For joint generation, create multiple related entity pages and claims that
require selecting the correct evidence page rather than the page with the most
overlapping name.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux conocía a los Grateful Dead (42 chars) | La Grateful Dead fue una banda de rock estadounidense formada en 1965 en Palo Alto, California. Conformada por entre cinco y siete miembros, la banda es conocida por su estilo único y ecléctico, que fusionaba elementos de roc ... [truncated 225 chars](3117 chars) |
| Taarak Mehta Ka Ooltah Chashmah es una comedia de situación (59 chars) | Taarak Mehta Ka Ooltah Chashmah (en inglés: La Perspectiva Diferente de Taarak Mehta) es la sitcom más longeva de la India, producida por Neela Tele Films Private Limited. La serie se estrenó el 28 de julio de 2008. Se emite ... [truncated 225 chars](606 chars) |
| Aviones de alta tecnología y secretos se fabricaron en Burbank, California. (75 chars) | Burbank es una ciudad en el condado de Los Ángeles, en el sur de California, Estados Unidos, a 12 millas al noroeste del centro de Los Ángeles. Según el censo de 2010, su población era de 103,340 habitantes. Conocida como la ... [truncated 225 chars](1475 chars) |
| Nero es una persona (19 chars) | La dinastía Julio-Claudia se refiere a los primeros cinco emperadores romanos —Augusto, Tiberio, Calígula, Claudio y Nerón— o a la familia a la que pertenecían. Gobernaron el Imperio Romano desde su formación bajo Augusto a f ... [truncated 225 chars](2075 chars) |
| Scream 2 es una película exclusivamente alemana. (48 chars) | Scream 2 es una película de terror estadounidense de 1997 dirigida por Wes Craven y escrita por Kevin Williamson. Protagonizada por David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Jamie Kennedy, Laurie Me ... [truncated 225 chars](2742 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,996 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 3 |
| Queries with multiple positives | 6 (12.0%) |
| BM25 nDCG@10 | 0.7803 |
| BM25 hit@10 | 0.9200 |
| BM25 Recall@100 | 0.9649 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8427 |
| Dense hit@10 | 0.9400 |
| Dense Recall@100 | 0.9474 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8029 |
| Reranking hybrid hit@10 | 0.9600 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 49.56 |
| Document length avg chars | 1,301.14 |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355); 2018; James Thorne, Andreas Vlachos, Christos Christodoulopoulos, Arpit Mittal; DOI: `10.18653/v1/N18-1074`.
- [FEVER shared task site](https://fever.ai/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
| FEVER shared task site |  | project page | https://fever.ai/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-es
  dataset_id: hakari-bench/NanoBEIR-es
  task_name: NanoFEVER
  split_name: NanoFEVER
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4996
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 6
    multi_positive_query_percent: 12.0
  text_stats_chars:
    query_mean: 49.56
    document_mean: 1301.139712
  bm25:
    ndcg_at_10: 0.7803465129746283
    hit_at_10: 0.92
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding FEVER, BEIR, or NanoBEIR records likely to overlap
      with these evaluation claims or evidence pages
    useful_training_data:
    - non-overlapping FEVER evidence retrieval pairs
    - Spanish or multilingual Wikipedia claim verification data
    - entity-centric question-answer evidence pairs
    - hard negatives from similar entity pages
    synthetic_data:
      document_generation: Spanish Wikipedia-style entity and event passages outside
        the evaluation set
      question_generation: short factual Spanish claims, including supported and contradicted
        variants
      answerability: positives should contain evidence needed to verify the claim
    multi_positive_training: useful_but_not_central
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
    - label: FEVER paper
      url: https://arxiv.org/abs/1803.05355
    - label: FEVER shared task
      url: https://fever.ai/
    - label: BEIR paper
      url: https://arxiv.org/abs/2104.08663
    - label: MMTEB paper
      url: https://arxiv.org/abs/2502.13595
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
    - Spanish task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
  references:
  - title: 'FEVER: a Large-scale Dataset for Fact Extraction and VERification'
    url: https://arxiv.org/abs/1803.05355
    year: 2018
    doi: 10.18653/v1/N18-1074
    is_paper: true
    source_confidence: definitive_paper_link
  - title: FEVER shared task site
    url: https://fever.ai/
    year: null
    doi: null
    is_paper: false
    source_confidence: definitive_project_page
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    doi: 10.48550/arXiv.2502.13595
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'NanoBEIR: Smaller BEIR dataset subsets'
    url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    year: 2024
    doi: null
    is_paper: false
    source_confidence: dataset_collection
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.780346513
      hit_at_10: 0.92
      recall_at_100: 0.9649122807
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9649122807
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8426965873
      hit_at_10: 0.94
      recall_at_100: 0.9473684211
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9473684211
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8028559403
      hit_at_10: 0.96
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
