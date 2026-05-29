# NanoMIRACL / yo

## Overview

The MIRACL TACL release includes Yoruba as a same-language Wikipedia retrieval
setting, but the Nano sample visibly contains spelling, diacritic, English, and
code-mixed variation. The task remains question-to-passage retrieval with one
positive per query, yet the model must be robust to forms such as `Odun`,
`Ọdún`, `ọdún`, `Ki`, `Kí`, `Omo`, and `Ọmọ`. The content is mostly short
factual retrieval about countries, capitals, years, Nigerian history, people,
cultural topics, food, states, and institutions.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) introduced MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. The later TACL version,
[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse
Languages](https://aclanthology.org/2023.tacl-1.63/), identifies Yoruba as one
of the 18 released languages. Yoruba queries retrieve Yoruba Wikipedia passages,
so the task is intended to measure same-language retrieval rather than
cross-lingual search.

Yoruba has a special role in MIRACL. The TACL paper's dataset table lists
Yoruba as one of the two WSDM Cup surprise languages, with development and
test-B data but no training split. The paper explains that surprise-language
identities were hidden until shortly before the competition deadline and that no
training splits were provided for them, specifically to evaluate retrieval under
limited data and time conditions. After the competition, the paper states that
the surprise-versus-known distinction is no longer relevant, but the no-train
setup remains important for interpreting Yoruba results.

The MIRACL construction process follows the same retrieval-first design across
languages: native speakers generated well-formed questions from Wikipedia
prompts, then judged candidate passages produced by an ensemble baseline
retrieval system. The paper states that the ensemble included BM25, mDPR, and
mColBERT, and that the corpus was built from Wikipedia passages rather than
answer snippets. For Yoruba, the TACL baseline table reports development-set
BM25 nDCG@10 of 0.406, hybrid BM25+mDPR nDCG@10 of 0.374, and mColBERT
nDCG@10 of 0.561.

### Observed Data Profile

The sampled Nano task has 119 queries, 921 documents, and 119 positive qrel
rows. Every query has exactly one positive passage. Queries average 37.69
characters. Common starts include `Odun`, `Ọdún`, `ọdún`, `Ki`, `Kí`, `Omo`,
`Ọmọ`, `Orile`, `Ilu`, `Awon`, and `Ta`, often without full Yoruba diacritics.

Documents average 397.16 characters and usually begin with a Wikipedia article
title. The observed positives cover the Nigerian Civil War, Helsinki, Nigerian
independence, Osun State, Anne Kansiime, Haiti's capital, Tam David-West,
Kamaru Usman, Ghadames, William Onyeabor, fura, Christmas, and Nouakchott. The
repository metadata labels the split as `multilingual` and lists `yo`, `en`,
and `sw`; language detection is noisy because the text is short, diacritics are
inconsistent, and many pages include English names, country names, or code-mixed
phrases.

The task rewards exact entity matching and relation matching in a low-resource
Wikipedia setting. Many questions are short and formulaic, asking for a capital,
country, year, school, nationality, month, or what something is. Relevant
passages may be very short, but distractors with the same generic phrase such as
`oluilu orile-ede` or `omo orile ede` are common.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5323
and hit@10 = 0.7227 on this Nano split. BM25 places 40 of 119 positives at rank
1 and 86 of 119 positives in the top 10. It works well for exact titles and
very short capital questions, but it misses 33 positives from the top 10.

The failures show phrase-template confusion. For "kí ni oluilu orile-ede
Haiti?", BM25 retrieves other capital pages such as Tbilisi, Hanoi, and
Helsinki before Port-au-Prince. For "Omo orile ede wo ni Kamaru Usman?", pages
about other Nigerian people outrank the Kamaru Usman passage. For "Orile ede wo
ni ilu Ghadames wa?", generic capital/country pages and unrelated country
mentions outrank the Ghadames passage. For the Christmas month query, pages that
contain month names in unrelated contexts rank above the Christmas passage.

Because this Nano split is single-positive, hit@10 measures whether the labeled
evidence passage appears at all. nDCG@10 is still important because short
Yoruba questions can produce many near-identical lexical matches; the model
must rank the exact entity and requested relation above template-like
distractors.

### Training Data That May Help

Yoruba MIRACL has no original training split according to the TACL paper, so
training should rely on non-overlapping external data or carefully generated
synthetic data. Useful sources include Yoruba Wikipedia question-to-passage
retrieval pairs built from non-evaluation pages, Yoruba open-domain QA evidence
retrieval, Nigerian geography and biography retrieval data, and multilingual
African-language retrieval data where the evidence passage is in Yoruba.

Any training pipeline should explicitly avoid NanoMIRACL evaluation queries and
positive passages. Because the split is small and single-positive, even a small
amount of overlap would materially distort scores.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Yoruba Wikipedia-style
passages and generate Yoruba questions grounded in one selected passage. Useful
forms include `Kí ni`, `Ta ni`, `Ilu wo`, `Orile ede wo`, `Ọmọ orile ede wo`,
`ọdún wo`, `Oṣù wo`, and `nibo`, with both diacritic-rich and plain ASCII-like
orthographic variants because the observed queries contain both.

For joint document-and-question generation, create Yoruba encyclopedia-style
passages with article titles, capitals, countries, years, biographies,
institutions, food descriptions, and Nigerian history facts, then generate
answerable questions. Do not seed generation with Nano evaluation queries or
positive passages. Include hard negatives that share generic Yoruba templates
but differ in the named entity or requested attribute.

## Example Data

| Query | Positive document |
| --- | --- |
| ilé iṣẹ iroyin wo ni Eugenia Abu bá ṣiṣe? (41 chars) | Eugenia Abu Eugenia Abu (bíi ni ọjọ́ mọ́kàndinlógún oṣù kẹwàá ọdún 1961) jẹ́ oniroyin, agbóhùnsáfẹ́fẹ́, akọ̀wé àti akéwì. Òun ni atọkun ètò ìròyìn tẹ́lẹ̀ fún Nigerian Television Authority (NTA) . Ó ṣe atọkun ètò lórí NTA fún ... [truncated 225 chars](245 chars) |
| Awon orile ede wo lo yika Austria? (34 chars) | Austríà Austríà ( tabi ; ), lonibise bi Orileominira ile Austria (German: "Republik Österreich"), je orile-ede atimo ile to ni awon eniyan bi egbegberun 8.8 to wa ni Aringbongan Europe. O ni bode mo Orileominira Tseki ati Jem ... [truncated 225 chars](684 chars) |
| ẹgbẹ wo ni Huey Newton da silẹ? (31 chars) | Huey P. Newton Huey Percy Newton (February 17, 1942 – August 22, 1989) je omo ile Amerika. Newton je oludasile ati olori egbe oselu Black Panther Party. (152 chars) |
| Odun wo ni Stella Obasanjo s'alaisi? (36 chars) | Stella Obasanjo Stella Obasanjo (14 November 1945 – 23 October 2005) ni Iyaafin Akoko ile Naijiria lati 1999 titi di ojo iku re ni 23 osu kewa, 2005. Ohun ni iyawo aare totikoja Olusegun Obasanjo. (196 chars) |
| Orukọ wo ni a n pe orile-ede Botswana ki wọn to yi pada? (56 chars) | Bòtswánà Ni orundun 19k, ogun sele larin awon Tswana ti won ti ungbe Botswana ati awon eya Ndebele ti won sese unko bo si agbegbe yi lati ariwa-ilaorun. Bakanna rogbodiyan sele pelu awon ateludo Boer lati Transvaal ni ilaorun ... [truncated 225 chars](660 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | yo |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | multilingual (primarily yo; config also lists en and sw) |
| Category | natural_language |
| Queries | 119 |
| Documents | 921 |
| Positive qrels | 119 |
| BM25 nDCG@10 | 0.5816 |
| BM25 hit@10 | 0.8151 |
| BM25 Recall@100 | 0.9167 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8416 |
| Dense hit@10 | 0.9496 |
| Dense Recall@100 | 0.9653 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7651 |
| Reranking hybrid hit@10 | 0.9412 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 37.69 |
| Document length avg chars | 397.16 |

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
  task_name: yo
  split_name: yo
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/yo.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 119
    documents: 921
    positive_qrels: 119
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 37.689076
    document_mean: 397.161781
  bm25:
    ndcg_at_10: 0.5816424741595791
    hit_at_10: 0.8151260504201681
    source: dataset_candidate_subset
  learning:
    original_train_split: unavailable
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: Yoruba MIRACL has no original train split; avoid NanoMIRACL evaluation
      queries and positive passages when building external or synthetic training data
    useful_training_data:
    - Yoruba Wikipedia question-to-passage retrieval pairs from non-evaluation pages
    - Yoruba open-domain QA evidence retrieval datasets
    - Nigerian geography and biography retrieval data with Yoruba evidence passages
    - multilingual African-language retrieval data with Yoruba evidence passages
    synthetic_data:
      document_generation: Yoruba Wikipedia-style passages with titles, capitals,
        countries, years, biographies, institutions, food descriptions, and Nigerian
        history facts
      question_generation: Yoruba fact questions using Ki ni, Ta ni, Ilu wo, Orile
        ede wo, Omo orile ede wo, odun wo, Osu wo, and nibo forms with diacritic-rich
        and plain variants
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
    source_notes:
    - repository metadata labels this split as multilingual and lists yo, en, and
      sw; observed data is Yoruba-centered with English names and code-mixed text
    - the TACL paper identifies Yoruba as a WSDM Cup surprise language with no original
      training split
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
  - title: MIRACL GitHub repository
    url: https://github.com/project-miracl/miracl
    year: null
    doi: null
    is_paper: false
    source_confidence: official_project_repository
  - title: MIRACL corpus dataset
    url: https://huggingface.co/datasets/miracl/miracl-corpus
    year: null
    doi: null
    is_paper: false
    source_confidence: official_dataset_card
  - title: MIRACL source queries and qrels
    url: https://huggingface.co/datasets/miracl/miracl
    year: null
    doi: null
    is_paper: false
    source_confidence: official_dataset_card
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5816424742
      hit_at_10: 0.8151260504
      recall_at_100: 0.9166666667
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 119
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9166666667
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8416263978
      hit_at_10: 0.9495798319
      recall_at_100: 0.9652777778
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 119
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9652777778
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7651054659
      hit_at_10: 0.9411764706
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 119
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
