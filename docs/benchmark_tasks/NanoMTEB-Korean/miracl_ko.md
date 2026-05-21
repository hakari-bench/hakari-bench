# NanoMTEB-Korean / miracl_ko

## Overview

`miracl_ko` is the Korean MIRACL retrieval split in `NanoMTEB-Korean`.
Queries are Korean information needs, and documents are Korean Wikipedia
passages. The retriever must rank answer-bearing passages in the same language,
often with several relevant passages for one query.

## Details

### What the Original Data Measures

[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://arxiv.org/abs/2210.09984)
states that MIRACL provides human-annotated passage-level relevance judgments
over Wikipedia in 18 languages, including Korean. Queries and passages are in
the same language, and annotations are denser than earlier multilingual
retrieval resources.

For Korean, MIRACL builds on the Mr. TyDi / TyDi QA lineage for the existing
language set and uses Korean Wikipedia passages. The source paper describes
native-speaker annotation, BM25/mDPR/mColBERT candidate pools, training/dev/test
splits, and release of training and development sets. The Nano task uses the
Korean dev split through the MTEB MIRACL retrieval packaging.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 508 positive qrels.
Queries average 2.54 positives, the median is 2, and 51.5% of queries have more
than one positive. Queries average 21.70 characters and are compact Korean fact
questions. Documents average 192.21 characters and are short Korean Wikipedia
passages with title prefixes.

The sampled positives include geography and history questions, such as capitals
of Bulgaria, Iceland, and Lebanon, the founder of Gojoseon, and a Greek
mythology question. Some sampled positives are related but not direct answer
passages, which reflects the multi-positive and passage-segmentation nature of
MIRACL.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4132 and hit@10 = 0.7050. BM25 ranks 70 positives first and finds a positive
in the top 10 for 141 of 200 queries, but sampled positives also appear at ranks
13, 21, and 24.

Lexical matching helps with named entities and country/capital patterns, but
Korean morphology, aliases, and passage segmentation make exact matching
fragile. Multi-positive ranking also matters: retrieving one related passage is
not the same as ranking all useful evidence well.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Korean training data,
Mr. TyDi Korean retrieval pairs, Korean Wikipedia question-passage pairs, and
native Korean hard negatives. Training should exclude MIRACL Korean dev/test
queries, qrels, and positives that overlap with the Nano evaluation split.

Because many queries have multiple positives, multi-positive objectives or
listwise losses are better aligned than single-positive training alone.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Korean Wikipedia
passages and generate Korean fact questions grounded in one or more passages.
For joint generation, create short Korean encyclopedia passages with titles,
aliases, dates, countries, organizations, and definitions, then create
answerable questions.

Synthetic data should preserve Korean morphology and common question forms such
as `어디`, `누구`, `언제`, and `무엇`. Do not use Nano evaluation queries or
positive passages as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| 헤라클레스는 그리스 신들 중 한 명인가? (22 chars) | 그리스 신화 헤라클레스는 에트루리아와 로마의 신화 및 숭배에도 등장하며, 로마인이 쓰던 라틴어 감탄사 "mehercule"은 그리스어인 "Herakleis"에서 유래한 것이었다. 이탈리아에서는 헤라클레스를 상인의 신으로 숭배하였는데, 다른 나라에서는 그의 특징적인 재능인 행운이나 위험에서의 구조를 염원하기도 하였다. (178 chars) |
| 숙종은 몇 번째 왕인가? (13 chars) | 조선 숙종 숙종(肅宗, 1661년 10월 7일(음력 8월 15일) ~ 1720년 7월 12일(음력 6월 8일))은 조선의 제19대 왕이다. 성은 이(李), 휘는 돈(焞), 본관은 전주(全州)., 초명은 용상(龍祥), 광(爌), 자는 명보(明譜), 사후 시호는 숙종현의광륜예성영렬장문헌무경명원효대왕(肅宗顯義光倫睿聖英烈章文憲武敬明元孝大王)이며 이후 존호가 더해져 정식 시호는 숙종현의광륜예성영렬유모영운홍인준 ... [truncated 225 chars](371 chars) |
| 가톨릭교회의 교회법(CIC)은 교회의 고유한 조직과 운영, 그리고 신자들이 교회의 목적을 좇아 이루도록 합법적인 교회의 권위로 제정한 법을 말하나요? (83 chars) | 로마 가톨릭교회 가톨릭교회의 교회법(CIC)은 교회의 고유한 조직과 운영, 그리고 신자들이 교회의 목적을 좇아 이루도록 합법적인 교회의 권위로 제정한 법을 말한다. 가톨릭교회는 영신적이면서도 가시적인 형태로 존재하며, 신적인 것과 인간적인 것이 함께 존재한다. 그러므로 교회법도 자연히 신약성경과 성전 안에 나오는 신법과, 교회와 인간이 제정한 실정법으로 이루어진다. 이러한 법의 제정 및 공표는 교황만 ... [truncated 225 chars](320 chars) |
| RNA는 오탄당인 리보스를 기반으로 사슬구조를 이루나요? (31 chars) | RNA RNA는 오탄당인 리보스를 기반으로 사슬구조를 이룬다. 오른쪽 그림에서와 같이 리보스에 있는 다섯개의 탄소에 번호를 붙였을 때 1번 탄소가 핵염기와 연결되며(이 그림의 경우 구아닌) 3번과 5번은 인산에 연결된다. 1번 탄소에 연결되는 핵염기는 구아닌 이외에도 아데닌, 우라실, 시토신이 있다. 인산은 당과 당 사이를 연결하여 사슬을 이룬다. (196 chars) |
| 불교의 시작은 어느 나라인가? (16 chars) | 불교의 역사 기원전 317년경 찬드라굽타(Chandra Gupta)에 의해 인도 최초의 통일 국가인 마우리아 왕조가 성립되고 제3대 왕 아소카가 즉위한 후 불교는 비약적으로 팽창하여 캐시미르와 간다라 지방을 비롯한 인도 각 지역그리스의 식민지인 박트리아스리랑카(실론)미얀마(버마) 등 국외로까지 전파되었다. 특히 스리랑카에는 아소카 왕은 자신의 아들 마힌다(Mahinda)를 보내 불교를 전파했다. 아소 ... [truncated 225 chars](293 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Korean |
| Backing dataset | NanoMTEB-Korean |
| Task / split | miracl_ko |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean) |
| Language | ko |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 508 |
| Avg positives / query | 2.54 |
| Positives per query (min / median / max) | 1 / 2.0 / 12 |
| Queries with multiple positives | 103 (51.5%) |
| BM25 nDCG@10 | 0.4132 |
| BM25 hit@10 | 0.7050 |
| Query length avg chars | 21.70 |
| Document length avg chars | 192.21 |

### Public Sources

- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://arxiv.org/abs/2210.09984); 2023; Xueguang Ma et al.; DOI: `10.1162/tacl_a_00595`.
- [MIRACL project page](http://miracl.ai/).
- [mteb/MIRACLRetrieval dataset card](https://huggingface.co/datasets/mteb/MIRACLRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean)
- Source dataset: [mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | arXiv paper | https://arxiv.org/abs/2210.09984 |
| MIRACL project page | 2023 | project page | http://miracl.ai/ |
| mteb/MIRACLRetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/MIRACLRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Korean
  backing_dataset: NanoMTEB-Korean
  dataset_id: hakari-bench/NanoMTEB-Korean
  task_name: miracl_ko
  split_name: miracl_ko
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Korean/miracl_ko.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2210.09984
    additional_source_urls:
      - http://miracl.ai/
      - https://huggingface.co/datasets/mteb/MIRACLRetrieval
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 508
  positives_per_query:
    average: 2.54
    min: 1
    median: 2.0
    max: 12
    multi_positive_queries: 103
    multi_positive_query_percent: 51.5
  text_stats_chars:
    query_mean: 21.705
    document_mean: 192.2093
  bm25:
    ndcg_at_10: 0.4132083896
    hit_at_10: 0.705
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude MIRACL Korean dev/test queries, qrels, and positive passages likely to overlap with the Nano split
    useful_training_data:
      - non-overlapping MIRACL Korean train pairs
      - Mr. TyDi Korean retrieval pairs
      - Korean Wikipedia question-to-passage retrieval pairs
      - native Korean hard negatives from the same Wikipedia topic
    synthetic_data:
      document_generation: Korean Wikipedia-style passages with titles, aliases, dates, places, organizations, and definitions
      question_generation: Korean fact questions grounded in one or more source passages
      answerability: positives should contain answer-bearing evidence or necessary context for the query
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean
    source_urls:
      - label: MIRACL arXiv
        url: https://arxiv.org/abs/2210.09984
      - label: MIRACL project page
        url: http://miracl.ai/
      - label: mteb/MIRACLRetrieval
        url: https://huggingface.co/datasets/mteb/MIRACLRetrieval
    source_notes: []
  references:
    - title: "MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages"
      url: https://arxiv.org/abs/2210.09984
      year: 2023
      doi: 10.1162/tacl_a_00595
      is_paper: true
      source_confidence: definitive_paper_link
```

