# MNanoBEIR / NanoBEIR-ko / NanoTouche2020

## Overview

Touché 2020 is an argument retrieval benchmark for controversial questions.
`NanoBEIR-ko__NanoTouche2020` uses Korean translated controversial questions to
retrieve Korean translated debate-style arguments.

## Details

### What the Original Data Measures

[Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26)
describes the CLEF Touché argument retrieval task, where relevance depends on
both topic match and argumentative content. BEIR includes Touché 2020 as an
argument retrieval task, and MMTEB supplies the multilingual context.

### Observed Data Profile

The sampled task has 49 queries, 5,745 documents, and 932 positive qrels. Every
query is multi-positive, averaging 19.02 positives. Queries are short Korean
controversial questions averaging 21.73 characters, while documents are long
debate arguments averaging 1,032.84 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5034 and hit@10 = 0.9796. Topic terms and many
positives make at least one relevant argument easy to find, but ranking still
needs to prioritize substantive arguments over topical mentions.

### Training Data That May Help

Useful data includes non-overlapping Touché argument retrieval, debate portal
argument collections, pro/con retrieval pairs, and Korean or multilingual
argument quality data. Training should exclude Touché 2020, BEIR, NanoBEIR, and
overlapping translated arguments.

### Synthetic Data Guidance

Generate Korean controversial questions from non-evaluation debate documents.
For joint generation, create multiple pro and con arguments per topic so
multi-positive training rewards broad coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| 숙제는 유익한가요? (10 chars) | 첫째, 숙제가 훌륭하며 현대 학교에서 계속되어야 할 세 가지 이유가 있다. 1. 숙제는 실천을 통해 배우는 학습자에게 도움이 된다. 일반적으로 세 가지 유형의 학습자가 있다. 듣고 배우는 사람, 보고 배우는 사람, 그리고 실천을 통해 배우는 사람이 그것이다. 많은 사람들이 특정 과목을 듣거나 보는 것으로 학습에 만족하지만, 일부는 실제로 해보아야 이해할 수 있다. 따라서 숙제는 후자 그룹에게 유익하다 ... [truncated 225 chars](1872 chars) |
| 처방약을 소비자에게 직접 광고하는 것이 타당한가? (27 chars) | 많은 광고들은 약물의 효과에 대한 충분한 정보를 제공하지 않는다. 예를 들어, 루네스타(Lunesta)는 평화롭게 잠자는 사람 위로 침실 창문을 통해 날아드는 나방의 이미지로 광고된다. 실제로 루네스타는 6개월 치료 후 환자들이 15분 더 빨리 잠들게 하고, 밤에 평균 37분 더 잠을 자게 한다. 대부분의 광고는 감정적 호소에 기반하지만, 질환의 원인, 위험 요인, 중요한 생활 습관 변화에 대한 정보 ... [truncated 225 chars](936 chars) |
| 아이들에게 어떤 백신이라도 의무화되어야 할까요? (26 chars) | 아직 완전한 주장은 아니다. 단지 내가 정리한 몇 가지 사항들이다. 정부는 부모가 자녀의 건강 문제에 대해 내리는 결정에 개입할 권리를 가져서는 안 된다. 미시간 대학교의 2010년 조사에 따르면, 자녀에게 의무화된 학교 입학 백신 접종을 거부할 권리가 있어야 한다고 생각하는 부모는 31%에 달한다. 많은 부모들이 백신 접종에 반대하는 종교적 신념을 가지고 있다. 이러한 부모들에게 백신 접종을 강요하 ... [truncated 225 chars](2132 chars) |
| 낙태는 합법이어야 하나요? (14 chars) | 낙태는 태아가 생존 가능해지거나 출생한 후에 인간으로서의 인격이 시작되므로, 수정 시점이 아니라 그 이후에 합법화되어야 한다. 미국 대법원에 따르면, 인간은 산모의 자궁 밖으로 나와 산소를 호흡하기 시작할 때 나이를 가지게 되며, 이때부터 0세로 시작하여 결국 1세까지 성장하게 된다. (159 chars) |
| 표준화된 시험이 교육을 향상시키는가? (20 chars) | 해결됨: SAT, ACT 및 기타 표준화된 시험은 고교 성적(GPA)보다 엘리트 대학 및 대학교에서의 교육 준비 상태에 대해 더 많은 통찰을 제공하므로 입학 심사 과정에서 더 큰 비중을 차지해야 한다. 논의를 위해, 지원자의 15% 미만만을 받아들이는 모든 대학이나 대학교는 엘리트로 간주될 수 있다. 이는 더 높은 비율의 지원자를 받아들이는 엘리트 대학이 존재하지 않는다는 의미는 아니지만, 상대방이 ... [truncated 225 chars](2102 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Avg positives / query | 19.02 |
| Positives per query (min / median / max) | 6 / 19.00 / 32 |
| Queries with multiple positives | 49 (100.0%) |
| BM25 nDCG@10 | 0.5034 |
| BM25 hit@10 | 0.9796 |
| Query length avg chars | 21.73 |
| Document length avg chars | 1,032.84 |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | https://doi.org/10.5281/zenodo.6862281 |
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
  backing_dataset: NanoBEIR-ko
  dataset_id: hakari-bench/NanoBEIR-ko
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoTouche2020.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 49
    documents: 5745
    positive_qrels: 932
  positives_per_query:
    average: 19.020408
    min: 6
    median: 19.0
    max: 32
    multi_positive_queries: 49
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 21.734694
    document_mean: 1032.83725
  bm25:
    ndcg_at_10: 0.5033791223
    hit_at_10: 0.9795918367
    source: dataset_bm25_column
```
