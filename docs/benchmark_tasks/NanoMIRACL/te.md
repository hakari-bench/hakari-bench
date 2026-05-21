# NanoMIRACL / te

## Overview

MIRACL includes Telugu as a native same-language Wikipedia retrieval task from
the TyDi/Mr. TyDi lineage. This Nano split is smaller than most other MIRACL
languages, with 84 single-positive queries, but it preserves the same
question-to-passage objective. The sampled Telugu questions are heavily
entity- and census-oriented, often involving village names, years such as
`2011`, population or area attributes, places, people, institutions, religious
sites, and definitions, so the model must distinguish repeated census-style
passages and exact local entities.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Telugu queries retrieve
Telugu Wikipedia passages, so the task measures same-language retrieval rather
than cross-lingual search. The paper states that MIRACL uses well-formed
questions and native-speaker relevance judgments over passage-level corpora.

Telugu is one of the MIRACL languages inherited from Mr. TyDi and TyDi QA. The
paper explains that, for these languages, MIRACL aligns with the Mr. TyDi split
structure while adding denser passage-level annotations and fixing corpus
segmentation issues. This makes the task a retrieval benchmark over Telugu
Wikipedia passages, not answer extraction from a single selected article.

MIRACL annotators generated questions from Wikipedia prompts and judged
candidate passages returned by an ensemble of BM25, mDPR, and mColBERT. For
Telugu, the MIRACL overview reports development-set BM25 nDCG@10 of 0.494 and
hybrid BM25+mDPR nDCG@10 of 0.602. That gap matters here because many Telugu
Wikipedia village pages have nearly identical census language; lexical matching
can retrieve the right page family but still confuse the requested village or
attribute.

### Observed Data Profile

The sampled Nano task has 84 queries, 754 documents, and 84 positive qrel rows.
Every query has exactly one positive passage. Queries average 38.46 characters.
The most common start is `2011`, which appears in many census-style questions,
followed by village or entity names such as `సూళ్ళూరు`, `చక్కపల్లి`,
`గుమ్మడికాయ`, `ఇస్రో`, and `రామోజీ`.

Documents average 787.54 characters and usually begin with a Telugu Wikipedia
article title. The observed positives cover Falaknuma Palace, village area,
village population, male/female counts, pin codes, scientific names, ISRO,
Ramayana authorship, religious sites, and biographies. Many documents have a
highly repetitive structure: settlement location, distance from nearby towns,
2011 Indian census counts, area in hectares, male/female population,
Scheduled Caste and Scheduled Tribe counts, census location code, pin code, and
nearby public services.

The task therefore mixes general encyclopedia retrieval with a dense cluster of
structured village-statistic retrieval. A strong model must preserve exact
Telugu entity matching and also bind the query to the requested attribute:
area, population, male count, number of houses, pin code, founder, birthplace,
or scientific name.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6044
and hit@10 = 0.8452 on this Nano split. BM25 places 32 of 84 positives at rank
1 and 71 of 84 positives in the top 10. It is strong for exact village names
and repeated census phrasing, but it still misses 13 positives from the top 10.

The failures are concentrated in formulaic pages. For the pumpkin scientific
name query, BM25 retrieves other plant pages with `శాస్త్రీయ నామం` before the
pumpkin passage. For the Gamhiraopet pin-code query, nearby or similarly
formatted village pages outrank the exact `గంభీరావుపేట్` page. For several
village-area questions, passages with the same `గ్రామ విస్తీర్ణం` census
phrasing rank above the target village. The ISRO founder and Ramayana author
queries show a different problem: the positive passage contains the answer, but
related organization or cultural pages share enough vocabulary to push it down.

Because this Nano split is single-positive and small, each miss has a visible
effect on the aggregate score. nDCG@10 is especially sensitive to whether the
model can rank the exact village or entity page above near-duplicate template
pages with the same attribute words.

### Training Data That May Help

Non-overlapping Telugu MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should
preferably be excluded from training. Other useful data includes Telugu
Wikipedia question-to-passage retrieval pairs, Telugu open-domain QA evidence
retrieval, and synthetic village-statistic retrieval pairs built from
non-evaluation pages.

Training should emphasize exact entity disambiguation in Telugu script and
attribute binding in repeated census templates. The model needs to distinguish
`విస్తీర్ణం`, `జనాభా`, `పురుషుల సంఖ్య`, `ఇళ్ల`, and `పిన్ కోడ్` questions even
when many candidate passages share the same boilerplate.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Telugu
Wikipedia-style passages and generate Telugu questions grounded in one selected
passage. Useful forms include `2011 జనగణన ప్రకారం`, `గ్రామ విస్తీర్ణం ఎంత`,
`పురుషుల సంఖ్య ఎంత`, `పిన్ కోడ్ ఏంటి`, `ఎవరు`, `ఎక్కడ`, and `శాస్త్రీయ నామం
ఏంటి`, with exact village and entity names copied faithfully.

For joint document-and-question generation, create Telugu encyclopedia-style
passages with article titles, aliases, census tables written in prose, areas,
population counts, pin codes, founders, birthplaces, scientific names, and
religious or institutional descriptions, then generate answerable questions. Do
not seed generation with Nano evaluation queries or positive passages. Include
near-duplicate distractors that differ only in village name or requested
attribute.

## Example Data

| Query | Positive document |
| --- | --- |
| లబదపుత్తు గ్రామ వైశాల్యం ఎంత? (29 chars) | లబదపుత్తు లబదపుత్తు, విశాఖపట్నం జిల్లా, ముంచంగిపుట్టు మండలానికి చెందిన గ్రామము. లబాడపుట్టు ఆంధ్ర ప్రదేశ్ రాష్ట్రం, విశాఖపట్నం జిల్లా, ముంచింగిపుట్టు మండలంలోని గ్రామం. ఇది మండల కేంద్రమైన ముంచింగిపుట్టు నుండి 17 కి. మీ. దూరం లో ... [truncated 225 chars](6166 chars) |
| తక్కెళ్ళపాడు గ్రామ విస్తీర్ణం ఎంత? (34 chars) | తక్కెళ్ళపాడు (ఫిరంగిపురం) తక్కెళ్ళపాడు (ఫిరంగిపురం), గుంటూరు జిల్లా, ఫిరంగిపురం మండలానికి చెందిన గ్రామము. పిన్ కోడ్:522 438. ఇది మండల కేంద్రమైన ఫిరంగిపురం నుండి 8 కి. మీ. దూరం లోను, సమీప పట్టణమైన సత్తెనపల్లి నుండి 10 కి. మీ. ... [truncated 225 chars](807 chars) |
| గుమ్మడికాయ యొక్క శాస్త్రీయ నామం ఏంటి? (37 chars) | గుమ్మడి గుమ్మడి లేదా తియ్య గుమ్మడి దీని శాస్త్రీయ నామము "cucurbita pepo లేదా cucuebita mixta ", Pumpkin Cucurbita moschata, N.O. cucurbitaceae.గుమ్మడి ఆంధ్రులకు ప్రీతికరమైన శుభప్రథమైన తరచూ వాడబడు కూర.ఇది ప్రపంచములో అన్ని దేశా ... [truncated 225 chars](591 chars) |
| భారతదేశంలో జరిగిన మొదటి యుద్ధం ఏది ? (36 chars) | మొదటి భారత స్వాతంత్ర్య యుద్ధం మొదటి భారత స్వాతంత్ర్య యుద్ధం : 1857–-58 మధ్యకాలంలో ఉత్తర, మధ్య భారతదేశంలో బ్రిటిష్ వారికి వ్యతిరేకంగా జరిగిన తిరుగుబాట్లని మొదటి భారత స్వాతంత్ర్య యుద్ధం అనీ, 1857 సిపాయిల తిరుగుబాటు అనీ పరిగణిస్ ... [truncated 225 chars](575 chars) |
| అశ్వఘోషుడు తల్లి పేరేమిటి? (26 chars) | అశ్వఘోషుడు క్రీ. శ. 1, 2 శతాబ్దాలకు చెందిన మహాకవి అశ్వఘోషుని జీవిత విశేషాలు కొద్దిగా మాత్రమే తెలుస్తున్నాయి. ఇతని సౌందరనందం కావ్యం చివర 18 వ సర్గలో " ఆర్య సువర్ణాక్షీపుత్రస్య సాకేతకస్య భిక్షోరాచార్యస్య భదంతాశ్వఘోషస్య మహాకవేర్ ... [truncated 225 chars](965 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | te |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | te |
| Category | natural_language |
| Queries | 84 |
| Documents | 754 |
| Positive qrels | 84 |
| BM25 nDCG@10 | 0.6044 |
| BM25 hit@10 | 0.8452 |
| Query length avg chars | 38.46 |
| Document length avg chars | 787.54 |

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
  task_name: te
  split_name: te
  language: te
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/te.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 84
    documents: 754
    positive_qrels: 84
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 38.464286
    document_mean: 787.543767
  bm25:
    ndcg_at_10: 0.6044209131
    hit_at_10: 0.8452380952
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Telugu train split data
      - Telugu Wikipedia question-to-passage retrieval pairs
      - Telugu open-domain QA evidence retrieval datasets
      - synthetic village-statistic retrieval pairs from non-evaluation Telugu pages
    synthetic_data:
      document_generation: Telugu Wikipedia-style passages with titles, aliases, census prose, areas, population counts, pin codes, founders, birthplaces, scientific names, and institutional descriptions
      question_generation: Telugu fact questions using 2011 census, village area, male count, number of houses, pin code, who, where, and scientific-name forms with exact entity names
      answerability: questions should be grounded in explicit facts or relations in the generated or selected passage
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
    - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages'
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
```
