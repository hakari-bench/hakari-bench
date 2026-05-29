# NanoMTEB-Korean / squad_kor_v1

## Overview

`squad_kor_v1` is the Korean SQuAD/KorQuAD-style retrieval split in
`NanoMTEB-Korean`. Queries are Korean extractive-QA questions, and documents are
Korean Wikipedia passages. The retriever must find the passage that contains the
answer span.

## Details

### What the Original Data Measures

[KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension](https://arxiv.org/abs/1909.07005)
introduces a large Korean extractive machine-reading dataset built from Korean
Wikipedia. The paper says KorQuAD1.0 follows the SQuAD1.0 data-creation process
but uses human-generated Korean questions over Korean Wikipedia articles. It
also emphasizes Korean-specific evaluation details and lexical diversity in
question writing.

The [yjoonjang/squad_kor_v1](https://huggingface.co/datasets/yjoonjang/squad_kor_v1)
dataset card is minimal, but the `NanoMTEB-Korean` metadata describes it as a
Korean translation or adaptation of SQuAD v1.0 for retrieval based on Korean
Wikipedia articles. In the Nano task, the question is the query and the
answer-bearing passage is the positive document.

### Observed Data Profile

The Nano split has 200 queries, 960 documents, and 200 positive qrels. Every
query has one positive. Queries average 35.77 characters and are direct Korean
fact questions. Documents average 545.20 characters and are Korean Wikipedia
passages with title prefixes.

The sampled positives ask about Western philosophy, Ban Ki-moon, Alexander
Haig, and Korean security-policy history. Several queries share the same
document, which is typical for reading-comprehension datasets where multiple
questions are written for a passage.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8812 and hit@10 = 0.9450. This is one of the easiest Korean splits for BM25:
165 positives are ranked first and the median best rank is 1.

The remaining misses show the retrieval challenge left after lexical matching.
For example, the query about Ban Ki-moon's first Korean-held office has its
positive at rank 27, likely because many passages mention names and offices.
Better retrievers need answer-specific matching, not only entity overlap.

### Training Data That May Help

Useful training data includes non-overlapping KorQuAD/SQuADKor train pairs,
Korean Wikipedia question-passage retrieval data, and native Korean QA
reformulations. Training should exclude the source test split, Nano queries,
qrels, and positive passages likely to overlap with this evaluation.

Since each query has one positive, focused question-to-passage retrieval
training is adequate, but hard negatives from the same article help avoid
ranking adjacent context too highly.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Korean Wikipedia
passages and generate Korean questions whose answer span is explicitly present.
For joint generation, create encyclopedic Korean paragraphs and questions over
dates, names, offices, locations, numbers, and definitions.

Hard negatives should come from the same article or related entity pages. Do not
use Nano evaluation questions or positive passages as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| '행보가 비서 본연의 역할을 벗어난다', '장관들과 내각이 소외되고 대통령비서실의 권한이 너무 크다'는 의견이 제기된 대표적인 예는? (74 chars) | 임종석 "내각과 장관들이 소외되고 대통령비서실의 권한이 너무 크다", "행보가 비서 본연의 역할을 벗어난다"는 의견이 제기되었다. 대표적인 예가 10차 개헌안 발표이다. 원로 헌법학자인 허영 경희대 석좌교수는 정부의 헌법개정안 준비 과정에 대해 "청와대 비서실이 아닌 국무회의 중심으로 이뤄졌어야 했다"고 지적했다. '국무회의의 심의를 거쳐야 한다'(제89조)는 헌법 규정에 충실하지 않았다는 것이다. ... [truncated 225 chars](480 chars) |
| 임종석이 1989년 2월 15일에 지명수배 받은 혐의는 어떤 시위를 주도했다는 것인가? (48 chars) | 임종석 1989년 2월 15일 여의도 농민 폭력 시위를 주도한 혐의(폭력행위등처벌에관한법률위반)으로 지명수배되었다. 1989년 3월 12일 서울지방검찰청 공안부는 임종석의 사전구속영장을 발부받았다. 같은 해 6월 30일 평양축전에 임수경을 대표로 파견하여 국가보안법위반 혐의가 추가되었다. 경찰은 12월 18일~20일 사이 서울 경희대학교에서 임종석이 성명 발표를 추진하고 있다는 첩보를 입수했고, 12 ... [truncated 225 chars](482 chars) |
| 유사지질학자들이 노아의 홍수를 증명하기 위해 성경 이외에 근거라고 주장한 것들은? (45 chars) | 노아의_방주 역사학과 과학의 발달이 더뎠던 고대사회에서는, 성경이 단순한 교리적인 부분 뿐 아니라 역사책으로서의 권위도 높았기에 노아의 방주를 역사적인 존재로서 다루고 있었다. 이는 제칠일안식교에서 비롯된 의사과학의 한 종류인 유사지질학인 홍수지질학과 같은 것에 영향을 주었으며, 과거 신학에서는 이러한 근본주의적 해석을 받아들여 역사와 사회적인 모든 부분에 있어 성경을 교과서로 채택할 것을 촉구했다. ... [truncated 225 chars](588 chars) |
| 반기문이 유엔 차기 사무총장 선거에 공식적으로 출마 선언을 한 날짜는? (39 chars) | 반기문 2006년 2월 14일에 유엔 차기 사무총장 선거에 공식적으로 출마 선언을 하여 선거운동을 시작했다. 반기문은 대한민국의 외교통상부 장관으로서 유엔 안전보장 이사회의 모든 나라를 순방할 수 있었다. 2006년 10월 14일에 한국인으로서는 최초로 유엔 사무총장에 당선되었다. 그러나 그가 출마를 선언했을 당시엔 그의 당선을 예상한 외신은 그다지 많지 않았다. 반기문은 아시아에 돌아갈 차례였던 당 ... [truncated 225 chars](551 chars) |
| 중화민국 수립 후 임세영은 자신의 스승이었던 누구를 재조명하는 작업에 착수하였는가? (46 chars) | 린스룽 임세영은 자신의 제자들과 연극을 구경하러 갔다가 우연히 깡패들과 시비가 붙었는데 깡패들이 임세영의 무공이 고강한 것을 알고 물러갔으나 임세영이 홀로 있을 때 몰래 기습을 해왔다. 그러자 임세영은 그들의 무리수가 많아 방어만 하기에는 곤란한 것을 깨닫고 할 수 없이 공격을 하여 깡패들을 쓰러뜨렸으나 결국 광주 전역에 임세영을 체포한다는 수배령이 내려졌다. 그러자 임세영은 몸을 피해 다른 지역으로 ... [truncated 225 chars](460 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Korean |
| Backing dataset | NanoMTEB-Korean |
| Task / split | squad_kor_v1 |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean) |
| Language | ko |
| Category | natural_language |
| Queries | 200 |
| Documents | 960 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.9618 |
| BM25 hit@10 | 0.9850 |
| BM25 Recall@100 | 0.9950 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9158 |
| Dense hit@10 | 1.0000 |
| Dense Recall@100 | 1.0000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9585 |
| Reranking hybrid hit@10 | 0.9950 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 35.77 |
| Document length avg chars | 545.20 |

### Public Sources

- [KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension](https://arxiv.org/abs/1909.07005); 2019; Lim Seungyoung et al.
- [yjoonjang/squad_kor_v1 dataset card](https://huggingface.co/datasets/yjoonjang/squad_kor_v1).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean)
- Source dataset: [yjoonjang/squad_kor_v1](https://huggingface.co/datasets/yjoonjang/squad_kor_v1)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension | 2019 | arXiv paper | https://arxiv.org/abs/1909.07005 |
| yjoonjang/squad_kor_v1 | 2025 | dataset card | https://huggingface.co/datasets/yjoonjang/squad_kor_v1 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Korean
  backing_dataset: NanoMTEB-Korean
  dataset_id: hakari-bench/NanoMTEB-Korean
  task_name: squad_kor_v1
  split_name: squad_kor_v1
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Korean/squad_kor_v1.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/1909.07005
    additional_source_urls:
    - https://huggingface.co/datasets/yjoonjang/squad_kor_v1
  counts:
    queries: 200
    documents: 960
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 35.77
    document_mean: 545.1958333333
  bm25:
    ndcg_at_10: 0.9618395415129224
    hit_at_10: 0.985
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude source test data, Nano queries, qrels, and positive Korean
      Wikipedia passages likely to overlap with the evaluation split
    useful_training_data:
    - non-overlapping KorQuAD or SQuADKor train pairs
    - Korean Wikipedia question-to-passage retrieval data
    - native Korean QA reformulations
    - same-article hard negatives
    synthetic_data:
      document_generation: Korean Wikipedia-style paragraphs with titles, named entities,
        dates, offices, locations, and numeric facts
      question_generation: Korean extractive QA questions whose answer span is explicit
        in the passage
      answerability: each positive passage should contain the answer span and enough
        local context
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean
    source_urls:
    - label: KorQuAD1.0 arXiv
      url: https://arxiv.org/abs/1909.07005
    - label: yjoonjang/squad_kor_v1
      url: https://huggingface.co/datasets/yjoonjang/squad_kor_v1
    source_notes: []
  references:
  - title: 'KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension'
    url: https://arxiv.org/abs/1909.07005
    year: 2019
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9618395415
      hit_at_10: 0.985
      recall_at_100: 0.995
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.995
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9157974005
      hit_at_10: 1.0
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.958510434
      hit_at_10: 0.995
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
