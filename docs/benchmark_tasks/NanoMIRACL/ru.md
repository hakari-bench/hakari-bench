# NanoMIRACL / ru

## Overview

MIRACL defines Russian as monolingual ad hoc retrieval over Russian Wikipedia,
with well-formed questions and native-speaker relevance judgments. This Nano
task keeps a compact single-positive version of that setting. The queries are
Russian fact questions commonly beginning with `Когда`, `Сколько`, `Кто`, `В`,
`Как`, or `Где`, so the retriever must find passages stating the requested
history, geography, ruler, legal, technology, religious, biographical,
infrastructure, or definition fact.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Russian queries retrieve
Russian Wikipedia passages, so the task measures same-language retrieval rather
than cross-lingual search. The paper states that MIRACL uses well-formed
questions and native-speaker relevance judgments over passage-level corpora.

Russian is one of the MIRACL languages inherited from Mr. TyDi and TyDi QA. The
paper explains that, for these languages, MIRACL aligns with the Mr. TyDi split
structure while adding denser passage-level annotations and fixing corpus
segmentation issues. This makes the task a retrieval benchmark over Russian
Wikipedia passages, not answer extraction from a single selected article.

MIRACL annotators generated questions from Wikipedia prompts and judged
candidate passages returned by an ensemble of BM25, mDPR, and mColBERT. For
Russian, the MIRACL overview reports development-set BM25 nDCG@10 of 0.334 and
hybrid BM25+mDPR nDCG@10 of 0.532. That gap is important for this split because
lexical matching often finds related Russian pages, but the answer-bearing
passage may still be lower in the ranking.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,727 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 45.54
characters. The most common starts are `Когда`, `Сколько`, `Кто`, `В`, `Как`,
and `Где`, with additional forms such as `Какой`, `Что`, `Какая`, and `Можно`.

Documents average 783.43 characters and are Russian Wikipedia passages that
usually begin with an article title. The observed positives cover Moldavian
religious history, Valentina Tereshkova's spacecraft, the Colosseum,
Khrushchevka housing, Sapsan trains, capital punishment, Olga of Kiev, Anna
Ioannovna, Cappadocia, Soviet tanks, Herod the Great, Constantinople/Istanbul,
coming out, Kaluga rivers, Kadyrov, women's suffrage, and Marilyn Monroe.

The task often asks for a precise temporal, legal, or biographical relation.
Russian inflection and long noun phrases mean that relevant passages may not
share the exact same surface form as the query. At the same time, many near
topic pages share strong lexical overlap, so the model must choose the passage
that actually contains the requested evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4457
and hit@10 = 0.6750 on this Nano split. BM25 places 51 of 200 positives at rank
1 and 135 of 200 positives in the top 10. It works when distinctive names or
terms dominate the query, such as `Сапсан`, `Колизей`, or `Терешкова`, but it
misses 65 positives from the top 10.

The failures show relation and morphology issues. For "Когда была отменена
смертная казнь в Российской Федерации?", BM25 ranks pages about capital
punishment in Norway and Germany before the Russian capital-punishment passage.
For "Каким именем крестили Ольгу, мать князя Владимира?", Byzantine and church
pages outrank the Olga passage that names her baptismal name. For "В каком году
Константинополь стал называться Стамбулом?", related Mehmed II and Istanbul
history passages appear above the passage that directly discusses the name. For
"Когда женщины в России получили право голосовать?", generic women's suffrage
pages and Saudi Arabia pages outrank the universal-suffrage passage with the
Russia-specific claim.

Because this Nano split is single-positive, hit@10 measures whether the labeled
evidence passage appears at all. nDCG@10 is still important because many
positives are present but below near-topic distractors. A strong retriever
should preserve Russian named-entity matching while improving relation-aware
ranking for dates, names, legal status, causes, and historical sequence.

### Training Data That May Help

Non-overlapping Russian MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should preferably
be excluded from training. Other useful data includes Russian Wikipedia
question-to-passage retrieval pairs, Russian open-domain QA evidence retrieval,
and entity-attribute supervision for rulers, places, dates, laws, historical
events, and definitions.

Training should focus on evidence passage retrieval. The model needs to rank a
passage that contains the requested fact above related pages that share many
Russian words but answer a different date, person, or institution.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Russian
Wikipedia-style passages and generate Russian questions grounded in one selected
passage. Useful forms include `Когда`, `Кто`, `Где`, `Сколько`, `Какой`,
`Какая`, `Что`, `В каком году`, and `При каком`, with realistic inflection,
dates, offices, titles, places, and named entities.

For joint document-and-question generation, create Russian encyclopedia-style
passages with article titles, aliases, dates, offices, legal claims, locations,
and historical-event descriptions, then generate answerable Russian questions.
Do not seed generation with Nano evaluation queries or positive passages.
Include related but non-answering distractors around the same country, ruler,
law, or event.

## Example Data

| Query | Positive document |
| --- | --- |
| В честь кого назван ЭВС «Сапсан»? (33 chars) | Сапсан (электропоезд) ЭВС «Сапсан» ("Velaro RUS") — высокоскоростные электропоезда из семейства электропоездов Velaro производства компании Siemens, приобретённые ОАО «РЖД» для эксплуатации на российских скоростных железных д ... [truncated 225 chars](428 chars) |
| Когда Тимофе́й Па́влович Мозго́в стал игроком команды НБА «Орландо Мэджик»? (75 chars) | Мозгов, Тимофей Павлович Тимофе́й Па́влович Мозго́в (16 июля 1986, Ленинград) — российский профессиональный баскетболист, выступающий за команду НБА «Орландо Мэджик». Играет на позиции центрового. Первые шаги в баскетболе Моз ... [truncated 225 chars](573 chars) |
| Вавилон был центром держави Александра Македонского? (52 chars) | История Вавилона В октябре 331 г до н. э. Александр Македонский торжественно вступил в Вавилон, принёс жертву Белу и был провозглашён "«царём Вавилона и четырёх сторон света»". Македонское войско пребывало в городе около меся ... [truncated 225 chars](1160 chars) |
| Как умер последний царь России Николай Второй? (46 chars) | Николай II Николай II отрёкся от престола в ходе Февральской революции 1917 года, после чего находился вместе с семьёй под домашним арестом в Александровском дворце Царского Села. Летом 1917 года по решению Временного правите ... [truncated 225 chars](458 chars) |
| Где построили первую кирпичную церковь на Руси? (47 chars) | Советское (Саратовская область) В XVIII веке колония имела сначала молитвенный дом, а затем небольшую деревянную кирху Вознесения пресвятой девы Марии. Первая кирпичная церковь была построена в 1800 году. Однако и она вскоре ... [truncated 225 chars](697 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | ru |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | ru |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,727 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5887 |
| BM25 hit@10 | 0.8650 |
| BM25 Recall@100 | 0.9333 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7693 |
| Dense hit@10 | 0.9250 |
| Dense Recall@100 | 0.9495 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6816 |
| Reranking hybrid hit@10 | 0.9100 |
| Reranking hybrid Recall@100 | 0.9928 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 45.54 |
| Document length avg chars | 783.43 |

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
  task_name: ru
  split_name: ru
  language: ru
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/ru.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1727
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 45.535
    document_mean: 783.427331
  bm25:
    ndcg_at_10: 0.5887311199870267
    hit_at_10: 0.865
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived
      data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
    - non-overlapping MIRACL Russian train split data
    - Russian Wikipedia question-to-passage retrieval pairs
    - Russian open-domain QA evidence retrieval datasets
    synthetic_data:
      document_generation: Russian Wikipedia-style passages with titles, aliases,
        dates, offices, laws, locations, definitions, and factual evidence
      question_generation: Russian fact questions using varied Когда, Кто, Где, Сколько,
        Какой, Какая, Что, В каком году, and При каком forms with realistic inflection
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
      ndcg_at_10: 0.58873112
      hit_at_10: 0.865
      recall_at_100: 0.9333333333
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9333333333
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7693149116
      hit_at_10: 0.925
      recall_at_100: 0.9495495495
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9495495495
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6816431633
      hit_at_10: 0.91
      recall_at_100: 0.9927927928
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.015
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9927927928
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
