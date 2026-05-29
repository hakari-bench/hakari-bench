# NanoMTEB-Korean / ko_strategy_qa

## Overview

`ko_strategy_qa` is the Ko-StrategyQA retrieval split in `NanoMTEB-Korean`.
Queries are short Korean questions derived from StrategyQA-style multi-hop
questions, and documents are Korean evidence passages. The retriever must find
the evidence paragraphs needed for implicit reasoning.

## Details

### What the Original Data Measures

[Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies](https://arxiv.org/abs/2101.02235)
introduces StrategyQA as a Boolean QA benchmark where the reasoning steps are
implicit in the question. The paper states that questions require decompositions
into evidence-seeking steps and that retrieving context is difficult because
there is often little lexical overlap between the original question and the
supporting evidence.

The [taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA)
dataset card says the Korean dataset is converted into BEIR format for MTEB,
groups annotator-tagged evidence documents into sets, and excludes unit
questions containing `no_evidence` or `operation`. The Nano split evaluates this
evidence-retrieval layer rather than final yes/no answering.

### Observed Data Profile

The Nano split has 200 queries, 9,251 documents, and 378 positive qrels. It is a
multi-positive task: queries average 1.89 positives, the median is 2, and 61.5%
of queries have more than one positive. Queries average 22.43 characters and are
short Korean questions. Documents average 320.25 characters and are translated
or Korean evidence passages with title prefixes.

The sampled positives include evidence about William Shakespeare, Tony Bennett,
the Chimera, guitar playing, and Heath Ledger. Several positives are not direct
answers to the query wording; they are intermediate facts needed by the
underlying reasoning chain.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3694 and hit@10 = 0.5800. BM25 ranks only 62 positives first, and sampled
positives appear as low as ranks 80 and 99.

This matches the StrategyQA paper's warning about low lexical overlap. A query
like "1번을 연주할 때 보통 몇 개의 손을 사용하나요?" can require an evidence passage about
guitars even though the surface text is indirect. A strong retriever needs
decomposition-aware semantic matching and must handle multiple evidence
paragraphs per question.

### Training Data That May Help

Useful training data includes non-overlapping Ko-StrategyQA train examples,
StrategyQA evidence retrieval pairs, Korean or translated multi-hop QA evidence
pairs, and decomposition-step retrieval supervision. Training should exclude the
Ko-StrategyQA dev examples used for Nano evaluation, their qrels, and positive
evidence passages.

Because many queries have multiple positives, pairwise single-positive training
is insufficient. Multi-positive objectives, listwise distillation, or
decomposition-step retrieval losses are better aligned with the task.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation evidence passages and
generate Korean implicit reasoning questions whose answer requires one or more
supporting facts. For joint generation, create short evidence passages plus a
strategy question that requires combining them.

Synthetic data should preserve hidden reasoning links, not merely ask direct
lookup questions. Include multi-positive evidence sets and hard negatives that
share entities but support a different reasoning step. Do not use Nano
evaluation queries or positive passages as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| 스노우다운의 연간 강수량은 얼마나 되나요? (23 chars) | Snowdon "스노우던"이라는 영어 이름은 "눈 언덕"을 의미하는 고대 영어 스노 던에서 유래되었으며, 스노우던은 종종 눈으로 덮여 있기 때문입니다. 겨울철 스노우던에 내리는 눈의 양은 매우 다양하지만, 2004년에는 1994년에 비해 55%나 적었습니다. 스노든의 경사면은 영국에서 가장 습한 기후 중 하나이며 연평균 200인치(5,100mm) 이상의 강수량을 기록합니다. (211 chars) |
| 조안 크로포드의 텔레비전 배우로서의 경력은 언제 끝났나요? (32 chars) | Joan Crawford 크로포드는 1930년대 중반까지 인기 영화 배우로서 명성을 이어갔습니다. 노 모어 레이디스(1935)는 로버트 몽고메리, 당시 남편 프랜쇼 톤과 공동 주연을 맡아 큰 성공을 거두었습니다. 크로포드는 오랫동안 MGM의 수장 루이스 B. 메이어에게 더 극적인 역할에 캐스팅해 달라고 간청했고, 메이어는 주저했지만 W.S. 반 다이크 감독의 세련된 코미디 드라마 <나는 내 인생을 산 ... [truncated 225 chars](259 chars) |
| 엘튼 존이 기사 작위를 받았나요? (18 chars) | Elton John 존은 그래미상 5회, 브릿 어워드 5회, 아카데미상 2회, 골든 글로브상 2회, 토니상, 디즈니 레전드상, 케네디 센터 아너상 등을 수상했습니다. 2004년 롤링스톤은 로큰롤 시대의 영향력 있는 뮤지션 100인 명단에서 그를 49위로 선정했습니다. 2013년 빌보드는 그를 '빌보드 핫 100 톱 올타임 아티스트'에서 가장 성공한 남성 솔로 아티스트로 선정했으며, 비틀즈와 마돈나에 ... [truncated 225 chars](490 chars) |
| 1은 어떤 식단 제한을 부과합니까? (19 chars) | Haram 하람 육류와 관련하여 무슬림은 흐르는 피를 섭취하는 것이 금지되어 있습니다. 돼지고기, 개, 고양이, 원숭이 또는 기타 하람 동물과 같이 하람으로 간주되는 고기는 사람이 굶주림에 직면하여 이 고기를 섭취함으로써 생명을 구해야 하는 긴급 상황에서만 합법적인 것으로 간주될 수 있습니다. 그러나 사회에 과잉 식량이 있는 경우에는 필요성이 존재하지 않습니다. 이슬람 공동체는 구성원을 지탱하는 하나 ... [truncated 225 chars](294 chars) |
| 소아마비 백신은 누가 만들었나요? (18 chars) | Polio vaccine 최초의 효과적인 소아마비 백신은 1952년 조나스 소크와 피츠버그 대학의 줄리어스 영너, 바이런 베넷, L. 제임스 루이스, 로레인 프리드먼 등의 연구팀에 의해 개발되었으며, 이후 수년간의 후속 테스트가 필요했습니다. 소크는 1953년 3월 26일 CBS 라디오에 출연해 소수의 성인과 어린이를 대상으로 한 실험이 성공적이었다고 보고했으며, 이틀 후 그 결과가 미국의학협회지(J ... [truncated 225 chars](369 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Korean |
| Backing dataset | NanoMTEB-Korean |
| Task / split | ko_strategy_qa |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean) |
| Language | ko |
| Category | natural_language |
| Queries | 200 |
| Documents | 9,251 |
| Positive qrels | 378 |
| Avg positives / query | 1.89 |
| Positives per query (min / median / max) | 1 / 2.0 / 5 |
| Queries with multiple positives | 123 (61.5%) |
| BM25 nDCG@10 | 0.4740 |
| BM25 hit@10 | 0.7550 |
| BM25 Recall@100 | 0.7804 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7084 |
| Dense hit@10 | 0.8350 |
| Dense Recall@100 | 0.8413 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6476 |
| Reranking hybrid hit@10 | 0.8400 |
| Reranking hybrid Recall@100 | 0.8704 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 14 |
| Query length avg chars | 22.43 |
| Document length avg chars | 320.25 |

### Public Sources

- [Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies](https://arxiv.org/abs/2101.02235); 2021; Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Berant.
- [taeminlee/Ko-StrategyQA dataset card](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean)
- Source dataset: [taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies | 2021 | arXiv paper | https://arxiv.org/abs/2101.02235 |
| taeminlee/Ko-StrategyQA | 2025 | dataset card | https://huggingface.co/datasets/taeminlee/Ko-StrategyQA |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Korean
  backing_dataset: NanoMTEB-Korean
  dataset_id: hakari-bench/NanoMTEB-Korean
  task_name: ko_strategy_qa
  split_name: ko_strategy_qa
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Korean/ko_strategy_qa.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2101.02235
    additional_source_urls:
    - https://huggingface.co/datasets/taeminlee/Ko-StrategyQA
  counts:
    queries: 200
    documents: 9251
    positive_qrels: 378
  positives_per_query:
    average: 1.89
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 123
    multi_positive_query_percent: 61.5
  text_stats_chars:
    query_mean: 22.43
    document_mean: 320.2545670738
  bm25:
    ndcg_at_10: 0.4740232370923057
    hit_at_10: 0.755
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Ko-StrategyQA dev examples, Nano queries, qrels, and positive
      evidence passages
    useful_training_data:
    - non-overlapping Ko-StrategyQA train evidence pairs
    - StrategyQA evidence retrieval and decomposition-step pairs
    - Korean multi-hop QA evidence retrieval data
    - hard negatives sharing entities but supporting different reasoning steps
    synthetic_data:
      document_generation: short Korean evidence passages about entities, dates, definitions,
        and properties
      question_generation: Korean implicit reasoning questions requiring one or more
        evidence passages
      answerability: positives should supply facts needed by the hidden decomposition,
        not just topical overlap
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean
    source_urls:
    - label: StrategyQA arXiv
      url: https://arxiv.org/abs/2101.02235
    - label: taeminlee/Ko-StrategyQA
      url: https://huggingface.co/datasets/taeminlee/Ko-StrategyQA
    source_notes: []
  references:
  - title: Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit
      Reasoning Strategies
    url: https://arxiv.org/abs/2101.02235
    year: 2021
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4740232371
      hit_at_10: 0.755
      recall_at_100: 0.7804232804
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7804232804
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7083755286
      hit_at_10: 0.835
      recall_at_100: 0.8412698413
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8412698413
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6476104044
      hit_at_10: 0.84
      recall_at_100: 0.8703703704
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.07
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8703703704
      safeguard_positive_rows: 14
      rows_with_101_candidates: 14
```
