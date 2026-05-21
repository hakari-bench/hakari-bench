# NanoMTEB-Korean / lawir_ko

## Overview

`lawir_ko` is the Korean legal-information retrieval split in
`NanoMTEB-Korean`. Queries ask for the legal provision associated with a Korean
law title and article name, and documents are individual article texts from
Korean statutes and regulations. The retriever must locate the correct legal
article.

## Details

### What the Original Data Measures

No standalone task paper was confirmed for LawIRKo. The interpretation is based
on the [on-and-on/lawgov_ir-ko](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko)
dataset card, repository metadata, and observed Nano data. The dataset card says
the data was created for information-retrieval evaluation and follows Korea Law
Information Center license policies.

The `NanoMTEB-Korean` metadata describes the task as retrieval of relevant legal
articles from queries that reference specific Korean laws and provisions. Each
document represents a single article; queries are generated from law titles and
article identifiers, such as asking which article in the Building Act explains
technical standards.

### Observed Data Profile

The Nano split has 200 queries, 3,562 documents, and 200 positive qrels. Every
query has one positive. Queries average 50.62 characters and usually name a law
and a provision title. Documents average 387.21 characters and are statute
article text with enumerated clauses, cross-references, and formal legal
phrasing.

The sampled positives include the Road Traffic Act, Insurance Business Act,
Electronic Commerce Consumer Protection Act, Capital Markets Act, and Employment
Insurance Act. Query wording often paraphrases the article title, while the
document may omit the exact law title and contain many similar cross-references.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2783 and hit@10 = 0.3950. This is the hardest `NanoMTEB-Korean` split for
BM25 in this batch. It ranks only 37 positives first, and several sampled
positives appear at ranks 36, 75, or 100.

The difficulty is structural. Legal articles share formulaic wording and
cross-reference strings, while the query asks for a provision by meaning and
title. Strong models need Korean legal terminology, law-title normalization, and
article-title matching rather than broad topical similarity.

### Training Data That May Help

Useful data includes non-overlapping lawgov_ir-ko examples, Korean statute
article retrieval pairs, law-title-to-article-title mappings, and hard negatives
from the same law or adjacent provisions. Training should exclude the exact Nano
queries, qrels, and positive article texts.

Domain-specific Korean legal text is more useful than generic QA data. Models
should learn formal clause structure, cross-reference patterns, and provision
names.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Korean statute articles
and generate Korean questions that name the law and ask for the article
describing a specific provision. For joint generation, create realistic statute
articles with numbered clauses, cross-references, and article titles, then
generate matching retrieval queries.

Synthetic hard negatives should be articles from the same law with adjacent
titles or overlapping terms. Do not use Nano evaluation provisions or positive
articles as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| 금융소비자 보호에 관한 법률 상 '위원의 제척ㆍ기피 및 회피'에 대한 법규는 무엇입니까? (49 chars) | - 조정위원회 위원은 다음 각 호의 어느 하나에 해당하는 경우에는 그 분쟁조정신 청사건(이하 “사건”이라 한다)의 심의ㆍ의결에서 제척(--)된다. 1. 위원이나 그 배우자 또는 배우자였던 사람이 해당 사건의 당사자(당사자가 법인ㆍ단체 등인 경우에는 그 임원을 포함한다. 이하 이 호 및 제2호에서 같다)가 되거나 그 사건의 당사자와 공동권리자 또는 공동의무자인 경우 2. 위원이 해당 사건의 당사자와 친 ... [truncated 225 chars](645 chars) |
| '식품위생법'의 전체 내용 중 '기구 및 용기ㆍ포장에 관한 기준 및 규격'에 관한 법적 정의나 적용 사항과 범위 등을 명시한 조항이 있나요? (78 chars) | - 식품의약품안전처장은 국민보건을 위하여 필요한 경우에는 판매하 거나 영업에 사용하는 기구 및 용기ㆍ포장에 관하여 다음 각 호의 사항을 정하여 고시한다. 1. 제조 방법에 관한 기준 2. 기구 및 용기ㆍ포장과 그 원재료에 관한 규격 - 식품의약품안전처장은 제1항에 따라 기준과 규격이 고시되지 아니한 기구 및 용기ㆍ포장의 기준과 규격을 인정 받으려는 자에게 제1항 각 호의 사항을 제출하게 하여 -식품ㆍ ... [truncated 225 chars](696 chars) |
| 농수산물 유통 및 가격안정에 관한 법률에서 '대금정산조직 설립의 지원'와 관련되어 시행되고 있는 조항을 설명하시오. (64 chars) | 농림축산식품부장관, 해양수산부장관 및 도매시장 개설자는 도매시장법인ㆍ시 장도매인ㆍ중도매인 등이 다음 각 호의 대금의 정산을 위한 조합, 회사 등(이하 “대금정산조직”이라 한다)을 설립하 는 경우 그에 대한 지원을 할 수 있다. 1. 출하대금 2. 도매시장법인과 중도매인 또는 매매참가인 간의 농수산물 거래에 따른 판매대금 (180 chars) |
| 도로교통법 중 '고령운전자 표지'에 해당하는 부분이 뭐야? (32 chars) | - 국가 또는 지방자치단체는 고령운전자의 안전운전 및 교통사고 예방을 위하여 행정안전 부령으로 정하는 바에 따라 고령운전자가 운전하는 차임을 나타내는 표지(이하 “고령운전자 표지”라 한다)를 제작하 여 배부할 수 있다. - 고령운전자는 다른 차의 운전자가 쉽게 식별할 수 있도록 차에 고령운전자 표지를 부착하고 운전할 수 있다. (183 chars) |
| 개인정보 보호법에서 '자료의 요청 및 사실조사'에 관해 다루고 있는 하위 법령이 있나요? (49 chars) | - 분쟁조정위원회는 제43조제1항에 따라 분쟁조정 신청을 받았을 때에는 해당 분쟁의 조정을 위하여 필요한 자료를 분쟁당사자에게 요청할 수 있다. 이 경우 분쟁당사자는 정당한 사유가 없으면 요청에 따라야 한다. - 분쟁조정위원회는 분쟁의 조정을 위하여 사실 확인이 필요한 경우에는 분쟁조정위원회의 위원 또는 대통령령으 로 정하는 사무기구의 소속 공무원으로 하여금 사건과 관련된 장소에 출입하여 관련 자료를 ... [truncated 225 chars](526 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Korean |
| Backing dataset | NanoMTEB-Korean |
| Task / split | lawir_ko |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean) |
| Language | ko |
| Category | natural_language |
| Queries | 200 |
| Documents | 3,562 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2783 |
| BM25 hit@10 | 0.3950 |
| Query length avg chars | 50.62 |
| Document length avg chars | 387.21 |

### Public Sources

- [on-and-on/lawgov_ir-ko dataset card](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko).
- [Korea Law Information Center](https://www.law.go.kr/LSW/main.html).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean)
- Source dataset: [on-and-on/lawgov_ir-ko](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| on-and-on/lawgov_ir-ko | 2026 | dataset card | https://huggingface.co/datasets/on-and-on/lawgov_ir-ko |
| Korea Law Information Center | 2026 | public legal source | https://www.law.go.kr/LSW/main.html |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Korean
  backing_dataset: NanoMTEB-Korean
  dataset_id: hakari-bench/NanoMTEB-Korean
  task_name: lawir_ko
  split_name: lawir_ko
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Korean/lawir_ko.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone task paper was confirmed; interpretation is based on the official dataset card, MTEB metadata, and observed Nano data.
    paper_url: https://arxiv.org/abs/2210.07316
    additional_source_urls:
      - https://huggingface.co/datasets/on-and-on/lawgov_ir-ko
      - https://www.law.go.kr/LSW/main.html
  counts:
    queries: 200
    documents: 3562
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 50.62
    document_mean: 387.2071869736
  bm25:
    ndcg_at_10: 0.2782674716
    hit_at_10: 0.395
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude lawgov_ir-ko evaluation rows, Nano queries, qrels, and positive statute articles
    useful_training_data:
      - non-overlapping lawgov_ir-ko examples
      - Korean statute article retrieval pairs
      - law-title and article-title matching pairs
      - hard negatives from the same law and adjacent provisions
    synthetic_data:
      document_generation: Korean statute articles with numbered clauses, article titles, definitions, duties, and cross-references
      question_generation: Korean legal retrieval queries naming a law and asking for the article that explains a provision
      answerability: the positive article should be the provision that directly matches the queried law title and article concept
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean
    source_urls:
      - label: on-and-on/lawgov_ir-ko
        url: https://huggingface.co/datasets/on-and-on/lawgov_ir-ko
      - label: Korea Law Information Center
        url: https://www.law.go.kr/LSW/main.html
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
    source_notes: []
  references:
    - title: "on-and-on/lawgov_ir-ko"
      url: https://huggingface.co/datasets/on-and-on/lawgov_ir-ko
      year: 2026
      doi: null
      is_paper: false
      source_confidence: definitive_dataset_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      doi: 10.48550/arXiv.2210.07316
      is_paper: true
      source_confidence: definitive_paper_link
```

