# NanoMIRACL / ko

## Overview

MIRACL uses Korean as a same-language Wikipedia retrieval task inherited from
the TyDi/Mr. TyDi family: Korean questions retrieve Korean passages under
native-language judgments. The Nano split is compact and single-positive, with
short queries and relatively short passages. Many Korean questions begin with
the entity or topic rather than a wh-word, such as `세상에서`, `일본의`,
`임진왜란이`, or `대한민국의`, so the retrieval problem is to infer the
requested fact from topic-led Korean phrasing across science, history,
geography, politics, entertainment, religion, technology, and definitions.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Korean queries retrieve
Korean Wikipedia passages, so the task evaluates same-language retrieval rather
than cross-lingual matching. The paper states that MIRACL uses
native-speaker-generated questions and native-speaker relevance assessments.

Korean is one of the MIRACL languages inherited from Mr. TyDi and TyDi QA. The
paper explains that for these languages, MIRACL aligns with the Mr. TyDi split
structure while adding denser positive and negative passage judgments over a
newly prepared Wikipedia corpus. The task is therefore passage retrieval over
Korean Wikipedia, not answer extraction from a single preselected article.

The annotation workflow matters because annotators judged candidate passages
retrieved by an ensemble of BM25, mDPR, and mColBERT after generating questions
from Wikipedia prompts. For Korean, the MIRACL overview reports development-set
BM25 nDCG@10 of 0.419 and hybrid BM25+mDPR nDCG@10 of 0.609. This indicates
that lexical matching is useful but leaves room for semantic ranking and better
passage selection.

### Observed Data Profile

The sampled Nano task has 200 queries, 2,419 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 21.71
characters and documents average 287.30 characters, making this split shorter
than many other NanoMIRACL language samples. The query starts are diverse
because Korean questions often begin with the entity or topic: examples include
`세상에서`, `일본의`, `임진왜란이`, `중국의`, `태양은`, `대한민국의`, and
`히틀러가`.

The observed positives cover graphene thermal conductivity, chloroplasts, the
fall of the Western Roman Empire, Iceland's capital, brackish water, Ukraine's
largest city, Joseon kings, Japanese snow records, Korean Air corporate events,
Tang-dynasty geography, Hitler conspiracy claims, PlayStation 4, Korean
universities, and Doctor Who. Several query-positive pairs are near-verbatim
yes/no or definition checks, while others ask for a concise fact such as a
capital, date, king order, or developer.

The task is sensitive to Korean morphology and general question endings. Short
questions ending in `어디인가요`, `무엇인가`, or `몇 년도` can share many generic
tokens with unrelated pages. A relevant passage may also be a subsection of a
broader article rather than the most obvious title page.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5090
and hit@10 = 0.7150 on this Nano split. BM25 places 67 of 200 positives at rank
1 and 143 of 200 positives in the top 10. The baseline works well when there is
near-verbatim overlap, such as the graphene and chloroplast examples, but it
misses 57 positives from the top 10.

The failures show how common Korean question words and related-entity passages
can dominate. For "아이슬란드 수도는 어딘가요?", BM25 ranks film pages containing
`어딘가` above the Reykjavík passage. The same pattern appears for "대한민국의 최초
대학은 어디인가요?" and "당나라는 현재의 어디인가?", where `어디`-like surface overlap pulls in
unrelated titles. For "일본에서 가장 눈이 많이 내리는 도시는 어디인가?", BM25 finds Japanese
snow-related pages but misses the Jōetsu passage just outside the top 10. For
"히틀러는 몇 년도에 자살했는가?", the top passage about Hitler's death is highly
plausible, but the labeled positive is a conspiracy-theory passage mentioning
the same event, showing that the exact qrel passage can be non-obvious.

Because every query has one positive qrel, hit@10 shows whether BM25 retrieves
the labeled evidence at all. nDCG@10 adds the ranking sensitivity needed when a
positive appears but is below more general or related passages. A strong model
should handle Korean endings and entity relations while avoiding over-weighting
generic question phrases.

### Training Data That May Help

Non-overlapping Korean MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should preferably
be excluded from training. Other useful data includes Korean Wikipedia
question-to-passage retrieval pairs, Korean open-domain QA evidence retrieval,
and entity-attribute supervision for dates, locations, historical roles,
definitions, and yes/no factual checks.

Training should emphasize passage evidence rather than only answer strings or
question paraphrases. The model needs to distinguish the passage that supports a
fact from another passage that merely repeats a topic name or common question
ending.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Korean Wikipedia-style
passages and generate Korean questions grounded in one selected passage. Useful
question forms include `무엇인가`, `언제`, `어디`, `누구`, `몇`, `인가요`, and
`있나요`, with entity-first wording, dates, capitals, definitions, and yes/no
claims.

For joint document-and-question generation, create Korean encyclopedia-style
passages with titles, aliases, dates, places, organizations, definitions, and
concise evidence sentences, then generate answerable Korean questions. Do not
seed generation with Nano evaluation queries or positive passages. Include
near-title and generic-question distractors so models learn to rank evidence
instead of surface phrase overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| 헤라클레스는 그리스 신들 중 한 명인가? (22 chars) | 그리스 신화 헤라클레스는 에트루리아와 로마의 신화 및 숭배에도 등장하며, 로마인이 쓰던 라틴어 감탄사 "mehercule"은 그리스어인 "Herakleis"에서 유래한 것이었다. 이탈리아에서는 헤라클레스를 상인의 신으로 숭배하였는데, 다른 나라에서는 그의 특징적인 재능인 행운이나 위험에서의 구조를 염원하기도 하였다. (177 chars) |
| 숙종은 몇 번째 왕인가? (13 chars) | 조선 숙종 숙종(肅宗, 1661년 10월 7일(음력 8월 15일) ~ 1720년 7월 12일(음력 6월 8일))은 조선의 제19대 왕이다. 성은 이(李), 휘는 돈(焞), 본관은 전주(全州)., 초명은 용상(龍祥), 광(爌), 자는 명보(明譜), 사후 시호는 숙종현의광륜예성영렬장문헌무경명원효대왕(肅宗顯義光倫睿聖英烈章文憲武敬明元孝大王)이며 이후 존호가 더해져 정식 시호는 숙종현의광륜예성영렬유모영운홍인준 ... [truncated 225 chars](370 chars) |
| 가톨릭교회의 교회법(CIC)은 교회의 고유한 조직과 운영, 그리고 신자들이 교회의 목적을 좇아 이루도록 합법적인 교회의 권위로 제정한 법을 말하나요? (83 chars) | 로마 가톨릭교회 가톨릭교회의 교회법(CIC)은 교회의 고유한 조직과 운영, 그리고 신자들이 교회의 목적을 좇아 이루도록 합법적인 교회의 권위로 제정한 법을 말한다. 가톨릭교회는 영신적이면서도 가시적인 형태로 존재하며, 신적인 것과 인간적인 것이 함께 존재한다. 그러므로 교회법도 자연히 신약성경과 성전 안에 나오는 신법과, 교회와 인간이 제정한 실정법으로 이루어진다. 이러한 법의 제정 및 공표는 교황만 ... [truncated 225 chars](319 chars) |
| RNA는 오탄당인 리보스를 기반으로 사슬구조를 이루나요? (31 chars) | RNA RNA는 오탄당인 리보스를 기반으로 사슬구조를 이룬다. 오른쪽 그림에서와 같이 리보스에 있는 다섯개의 탄소에 번호를 붙였을 때 1번 탄소가 핵염기와 연결되며(이 그림의 경우 구아닌) 3번과 5번은 인산에 연결된다. 1번 탄소에 연결되는 핵염기는 구아닌 이외에도 아데닌, 우라실, 시토신이 있다. 인산은 당과 당 사이를 연결하여 사슬을 이룬다. (195 chars) |
| 불교의 시작은 어느 나라인가? (16 chars) | 불교의 역사 기원전 317년경 찬드라굽타(Chandra Gupta)에 의해 인도 최초의 통일 국가인 마우리아 왕조가 성립되고 제3대 왕 아소카가 즉위한 후 불교는 비약적으로 팽창하여 캐시미르와 간다라 지방을 비롯한 인도 각 지역그리스의 식민지인 박트리아스리랑카(실론)미얀마(버마) 등 국외로까지 전파되었다. 특히 스리랑카에는 아소카 왕은 자신의 아들 마힌다(Mahinda)를 보내 불교를 전파했다. 아소 ... [truncated 225 chars](292 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | ko |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | ko |
| Category | natural_language |
| Queries | 200 |
| Documents | 2,419 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4994 |
| BM25 hit@10 | 0.8000 |
| BM25 Recall@100 | 0.9606 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6910 |
| Dense hit@10 | 0.9100 |
| Dense Recall@100 | 0.9213 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7026 |
| Reranking hybrid hit@10 | 0.9400 |
| Reranking hybrid Recall@100 | 0.9882 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 21.71 |
| Document length avg chars | 287.30 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022; Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo, Xiaoguang Li, Qun Liu, Mehdi Rezagholizadeh, Jimmy Lin; DOI: `10.48550/arXiv.2210.09984`.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/); 2023 TACL version; DOI: `10.1162/tacl_a_00595`.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [MIRACL corpus dataset card](https://huggingface.co/datasets/miracl/miracl-corpus).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)
- Source corpus: [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus)
- Source queries and qrels: [miracl/miracl](https://huggingface.co/datasets/miracl/miracl)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus |  | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |
| miracl/miracl |  | dataset card | https://huggingface.co/datasets/miracl/miracl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMIRACL
  backing_dataset: NanoMIRACL
  dataset_id: hakari-bench/NanoMIRACL
  task_name: ko
  split_name: ko
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/ko.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 2419
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 21.71
    document_mean: 287.300951
  bm25:
    ndcg_at_10: 0.49940244273255596
    hit_at_10: 0.8
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping MIRACL Korean train split data
    - Korean Wikipedia question-to-passage retrieval pairs
    - Korean open-domain QA evidence retrieval datasets
    synthetic_data:
      document_generation: Korean Wikipedia-style passages with titles, aliases, dates,
        places, organizations, definitions, and factual evidence
      question_generation: Korean fact and yes/no questions using entity-first wording
        and forms such as 무엇인가, 언제, 어디, 누구, 몇, 인가요, and 있나요
      answerability: questions should be grounded in explicit facts or relations in
        the generated or selected passage
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMIRACL
    source_urls:
    - label: MIRACL corpus dataset
      url: https://huggingface.co/datasets/miracl/miracl-corpus
    - label: MIRACL source queries and qrels
      url: https://huggingface.co/datasets/miracl/miracl
    - label: MIRACL GitHub repository
      url: https://github.com/project-miracl/miracl
    source_notes: []
  references:
  - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum
      of Languages'
    url: https://arxiv.org/abs/2210.09984
    year: 2022
    doi: 10.48550/arXiv.2210.09984
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages'
    url: https://aclanthology.org/2023.tacl-1.63/
    year: 2023
    doi: 10.1162/tacl_a_00595
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4994024427
      hit_at_10: 0.8
      recall_at_100: 0.9606299213
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9606299213
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6910020911
      hit_at_10: 0.91
      recall_at_100: 0.9212598425
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9212598425
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7026491206
      hit_at_10: 0.94
      recall_at_100: 0.9881889764
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.015
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9881889764
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
