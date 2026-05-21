# NanoMIRACL / th

## Overview

MIRACL's Thai task is monolingual Wikipedia passage retrieval: Thai questions
search Thai passages, using native-language judgments rather than translation.
The Nano split keeps a compact, single-positive version of that benchmark. The
observed questions vary widely in form and include spouse, year, founder,
location, true/false-style, and definition requests, with Thai year expressions
such as `พ.ศ.` appearing often. Retrieval therefore depends on exact entity and
attribute matching across media, sports, biology, history, politics,
technology, countries, religion, and named people.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Thai queries retrieve Thai
Wikipedia passages, so the task measures same-language retrieval rather than
cross-lingual search. The paper states that MIRACL uses well-formed questions
and native-speaker relevance judgments over passage-level corpora.

Thai is one of the MIRACL languages inherited from Mr. TyDi and TyDi QA. The
paper explains that, for these languages, MIRACL aligns with the Mr. TyDi split
structure while adding denser passage-level annotations and fixing corpus
segmentation issues. This makes the task a retrieval benchmark over Thai
Wikipedia passages, not answer extraction from a single selected article.

MIRACL annotators generated questions from Wikipedia prompts and judged
candidate passages returned by an ensemble of BM25, mDPR, and mColBERT. For
Thai, the MIRACL overview reports development-set BM25 nDCG@10 of 0.484 and
hybrid BM25+mDPR nDCG@10 of 0.599. The paper also uses a Thai query-passage pair
as its running example, emphasizing the benchmark's same-language Wikipedia
passage retrieval setting.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,897 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 43.61
characters. Openings vary widely, but the sample includes question forms around
spouses, years, founders, locations, whether a statement is true, and what a
term means. Thai year expressions such as `พ.ศ.` and entity-heavy queries are
common.

Documents average 595.21 characters and usually begin with a Thai Wikipedia
article title. The observed positives cover Fate/stay night, UEFA Europa League
qualification, the human olfactory system, Paul Cezanne, Matou Sakura, East
Germany and World War II, China area, mobile phones, Thai sitcoms, stainless
steel, Thaksin Shinawatra's premiership, and Thai royal biography. The language
detection metadata marks both queries and documents as Thai.

The task often requires the model to bind a named entity to a specific
attribute: release year, number of teams, anatomical location, birth date,
relationship, country area, first use, office holder, or place of death. Thai
word segmentation and long named entities create lexical challenges even when
the topic is recognizable.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6475
and hit@10 = 0.9150 on this Nano split. BM25 places 84 of 200 positives at rank
1 and 183 of 200 positives in the top 10. This is one of the stronger BM25
profiles among the inspected NanoMIRACL splits, but 17 positives are still
outside the top 10.

The failures show that the remaining difficulty is mostly passage selection
inside the correct broad topic. For the UEFA Europa League 2018-19 query, BM25
retrieves season and group-stage pages before the qualifying/playoff passage
that states the number of participating clubs. For "สาธารณรัฐประชาชนจีนมีขนาด
พื้นที่ประเทศเท่าไหร่?", related China administrative pages outrank the country
passage with the area statement. For the stainless-steel first-use query, other
stainless-steel sections rank above the passage that narrates the 1911-1913
commercial adoption. For a long Thai royal place-of-death question, near
sections from the same or related articles outrank the passage about the
medical treatment and death context.

Because this Nano split is single-positive, hit@10 measures whether the labeled
evidence passage appears at all. nDCG@10 is still important because many
positives are present but below topically similar passages from the same article
or event.

### Training Data That May Help

Non-overlapping Thai MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should
preferably be excluded from training. Other useful data includes Thai Wikipedia
question-to-passage retrieval pairs, Thai open-domain QA evidence retrieval, and
hard negatives from same-article Thai Wikipedia sections.

Training should focus on Thai passage-level evidence selection. The model needs
to rank the section that contains the requested number, date, relation, office,
or location above other sections with the same entity name.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Thai Wikipedia-style
passages and generate Thai questions grounded in one selected passage. Useful
question forms include `ใคร`, `เมื่อไหร่`, `ปีใด`, `กี่`, `ที่ใด`, `คืออะไร`,
and statement-verification forms such as `ใช่หรือไม่`, with Thai Buddhist-era
and Common Era date variants when appropriate.

For joint document-and-question generation, create Thai encyclopedia-style
passages with article titles, aliases, dates, titles, locations, competitions,
anatomical terms, cultural works, and political offices, then generate
answerable Thai questions. Do not seed generation with Nano evaluation queries
or positive passages. Include near-duplicate distractors from the same article
family or event so the model learns passage-level discrimination.

## Example Data

| Query | Positive document |
| --- | --- |
| ชาวนอร์มันหมายถึงอะไร? (22 chars) | นอร์มัน นอร์มัน () คือกลุ่มชนผู้ให้นามแก่ดินแดนนอร์ม็องดีซึ่งเป็นบริเวณทางตอนเหนือของฝรั่งเศส ชนนอร์มันสืบเชื้อสายมาจากไวกิงผู้ได้รับชัยชนะต่อผู้ตั้งถิ่นฐานอยู่แต่เดิมที่เป็นชนแฟรงค์ (Franks) และกอลล์-โรมัน (Gallo-Roman) ความ ... [truncated 225 chars](602 chars) |
| คอเคลียเต็มไปด้วยน้ำที่เรียกว่าอะไร? (36 chars) | หูชั้นในรูปหอยโข่ง คอเคลียเต็มไปด้วยน้ำที่เรียกว่า perilymph ซึ่งไหวไปตามแรงสั่นสะเทือนที่มาจากหูชั้นกลางโดยผ่านช่องรูปไข่ (oval window) เมื่อน้ำในคอเคลียเคลื่อน ท่อคอเคลีย (cochlear duct/partition) ที่อยู่ตรงกลาง ซึ่งรวมเยื่ ... [truncated 225 chars](623 chars) |
| สไปรูไลนามีโปรตีนอยู่ราวเท่าไหร่? (33 chars) | สไปรูลินา (ผลิตภัณฑ์เสริมอาหาร) สไปรูไลนามีโปรตีนอยู่ราว 60% (51-71%) ในสไปรูไลนามีโปรตีนที่มีกรดอะมิโนจำเป็นทุกชนิด แม้ว่าจะมีปริมาณเมไทโอนีน ซีสเตอีนและไลซีนเมื่อเทียบกับโปรตีนที่ได้จากเนื้อสัตว์ ไข่และนม อย่างไรก็ตาม สไปรู ... [truncated 225 chars](516 chars) |
| พระราชวังบวรสถานมงคล ถูกสร้างขึ้นเมื่อไหร่? (43 chars) | พระราชวังบวรสถานมงคล พระราชวังบวรสถานมงคล หรือ พระบวรราชวัง ตั้งอยู่ที่เขตพระนคร กรุงเทพมหานคร เป็นพระราชวังที่ประทับของกรมพระราชวังบวรสถานมงคลหรือวังหน้า สมเด็จพระบวรราชเจ้ามหาสุรสิงหนาทซึ่งทรงดำรงพระอิสริยยศกรมพระราชวังบวรส ... [truncated 225 chars](767 chars) |
| การแข่งขัน ยูฟ่ายูโรปาลีก ฤดูกาล 2018–19 มีกี่สโมสรที่ลงแข่งขัน? (64 chars) | ยูฟ่ายูโรปาลีก ฤดูกาล 2018–19 รอบคัดเลือกและรอบเพลย์ออฟ ทั้งหมด 178 ทีมที่เข้าร่วมในระบบการคัดเลือกของ ยูฟ่ายูโรปาลีก ฤดูกาล 2018–19, ประกอบไป้วยรอบคัดเลือกและรอบเพลย์ออฟ, กับ 35 ทีมในเส้นทางแชมเปียนส์และ 143 ทีมในเส้นทางหลัก ... [truncated 225 chars](476 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | th |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | th |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,897 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6475 |
| BM25 hit@10 | 0.9150 |
| Query length avg chars | 43.61 |
| Document length avg chars | 595.21 |

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
  task_name: th
  split_name: th
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/th.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1897
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 43.61
    document_mean: 595.210332
  bm25:
    ndcg_at_10: 0.6475204605
    hit_at_10: 0.915
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Thai train split data
      - Thai Wikipedia question-to-passage retrieval pairs
      - Thai open-domain QA evidence retrieval datasets
      - same-article Thai Wikipedia hard negatives
    synthetic_data:
      document_generation: Thai Wikipedia-style passages with titles, aliases, dates, locations, competitions, anatomical terms, cultural works, and political offices
      question_generation: Thai fact questions using who, when, which year, how many, where, what-is, and yes/no statement forms with Buddhist-era and Common Era date variants
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
