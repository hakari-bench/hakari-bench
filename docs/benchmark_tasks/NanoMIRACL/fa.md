# NanoMIRACL / fa

## Overview

MIRACL includes Persian as a native same-language Wikipedia retrieval setting:
Persian information needs must retrieve Persian passages, not cross-lingual
translations. The Nano split keeps a compact, single-positive version of that
setup. Many observed questions are compact or entity-first, with openings such
as `چه`, `در`, `از`, and `اولین`, which makes the task a test of Persian
attribute binding over topics such as history, geography, universities,
government, religion, infrastructure, sports, and definitions.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Persian queries retrieve
Persian passages, so the task measures native-language retrieval rather than
cross-lingual search or translation quality. The paper states that MIRACL uses
well-formed natural-language questions and native-speaker relevance judgments.

Persian is one of MIRACL's "new known languages". The paper says Hindi,
Spanish, French, Farsi, and Chinese were added beyond the languages inherited
from Mr. TyDi/TyDi QA, and that all data for those languages was generated from
scratch. This makes the Persian task a MIRACL-created retrieval collection over
Persian Wikipedia, not a relabeled version of an older Mr. TyDi split.

The annotation process is retrieval-specific. MIRACL annotators generated
questions from Wikipedia prompts and judged candidate passages returned by an
ensemble of BM25, mDPR, and mColBERT. The labeled positive is therefore an
evidence-bearing Persian Wikipedia passage. For Persian, the original paper
reports development-set BM25 nDCG@10 of 0.333 and hybrid BM25+mDPR nDCG@10 of
0.594, suggesting that lexical retrieval is useful but leaves substantial room
for semantic or hybrid ranking.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,858 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 39.99
characters and are mostly compact Persian questions or topic-first information
needs. Frequent openings include `چه`, `در`, `از`, `اولین`, `دانشگاه`, and
`چند`, but the distribution is broad because many questions begin with the
entity being asked about.

Documents average 489.71 characters and are Persian Wikipedia passages, usually
starting with an article title. The sampled positives cover air defense,
Strasbourg University, Georgian presidents, Persian calligraphy, World War I,
literary styles, Lake Van, Nader Shah memorials, Israeli prime ministers, tax
exemptions, Ali-Sadr Cave, Olympic sports, religious recognition in Iran, and
railway distances. Many questions ask for a precise attribute, such as country,
year, founder, location, number, or reason.

The data highlights Persian retrieval issues around script, spacing, and
entity-related ambiguity. Queries may include half-spaces, affixes, Persian and
Arabic letter variants, or compact forms such as `میباشد`. In the observed BM25
rankings, close article titles often appear near the top, but the correct passage
depends on whether the passage expresses the exact requested relation.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5337
and hit@10 = 0.8400 on this Nano split. BM25 places 57 of 200 positives at rank
1 and 168 of 200 positives in the top 10. This is a strong baseline when the
query has distinctive entity names such as `دانشگاه استراسبورگ`, `جنگ جهانی
اول`, or `غار علیصدر`.

The remaining failures show fine-grained passage selection problems. For "چند
نوع سبک نگارش وجود دارد؟", BM25 retrieves general scientific-writing and
Nastaliq passages before the literary-schools passage that lists Persian literary
styles. For "وسعت دریاچه وان به عنوان بزرگترین دریاچه ترکیه چقدر میباشد؟", a
Lake Van page is ranked first, but the labeled positive is a Qazvin-province
passage about Lake Ovan, showing that near-name ambiguity and dataset labels can
make the relation surprising. For two Nader Shah questions, BM25 ranks the more
familiar Mashhad `آرامگاه نادرشاه` passages above a different `آرامگاه محمد
نادرشاه` or the specific location passage. For "جنگ جهانی دوم چگونه به پایان
رسید؟", BM25 retrieves related end-of-war and Japan-war passages before the
positive World War II passage.

Because the split is single-positive, hit@10 indicates whether the labeled
evidence passage is found, while nDCG@10 shows whether it is ranked high enough.
A stronger model should keep BM25's Persian entity matching while improving
normalization, relation recognition, and disambiguation among related passages.

### Training Data That May Help

Non-overlapping Persian MIRACL training data is the first source to inspect.
Because this Nano task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with the evaluation split should
preferably be excluded from training. Other useful data includes Persian
Wikipedia question-to-passage pairs, Persian QA evidence retrieval datasets, and
native Persian entity-attribute supervision over places, universities, political
offices, dates, wars, infrastructure, and definitions.

Training should emphasize passage evidence rather than only answer generation.
The model needs to retrieve passages that contain the requested fact, even when
another related page has more lexical overlap or a more obvious title match.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Persian
Wikipedia-style passages and generate Persian questions answerable from one
selected passage. Useful question types include `چه`, `کدام`, `چند`, `در چه
سالی`, `در کجا`, `علت`, and `چه کسی` forms, with realistic names, dates,
locations, organizations, and Persian spelling variants.

For joint document-and-question generation, create Persian encyclopedia-style
passages with titles, aliases, dates, places, offices, measurements, and
definition sentences, then generate grounded Persian questions. Do not seed
generation with Nano evaluation queries or positive passages. Synthetic examples
should include near-entity and near-title distractors, because the sampled task
often requires distinguishing closely related Persian passages.

## Example Data

| Query | Positive document |
| --- | --- |
| اسرائیل با چه کشورهایی روابط دوستانه دارد؟ (42 chars) | وزارت امور خارجه اسرائیل پیش از پیروزی انقلاب ۱۳۵۷ و به قدرت رسیدن نظام جمهوری اسلامی، ایران با کشور اسرائیل روابط دوستانه و حسنه‌ای را داشت و ایران اولین کشور اسلامی در منطقه خاورمیانه بود که کشور اسرائیل را به رسمیت شناخت. ... [truncated 225 chars](409 chars) |
| وزیر کنونی فرهنگ و ارشاد اسلامی ایران چه کسی است؟ (49 chars) | محمدمهدی اسماعیلی محمدمهدی اسماعیلی (متولد ۱۳۵۴ در کبودرآهنگ) سیاستمدار ایرانی و وزیر فرهنگ و ارشاد اسلامی است. او دانش‌آموخته دکتری علوم سیاسی از پژوهشگاه علوم انسانی و مطالعات فرهنگی و عضو هیأت علمی دانشگاه تهران است. تحصیل ... [truncated 225 chars](398 chars) |
| مثلث برمودا در کجا قرار دارد؟ (29 chars) | مثلث برمودا مثلث برمودا ، همچنین به عنوان مثلث شیطان شناخته می‌شود. منطقه‌ای است در ناحیه غربی اقیانوس اطلس شمالی که گفته می‌شود تعدادی هواپیما و کشتی تحت شرایط مرموز در آن ناپدید شده‌اند. (188 chars) |
| مرکزایالت اسکوشیا کدام شهر است؟ (32 chars) | نوا اسکوشیا مرکز نوا اسکوشیا شهر هلیفکس است که بزرگ‌ترین شهر این استان نیز به حساب می‌آید و از مراکز اقتصادی منطقه است. (119 chars) |
| گیاه سرخس از سرده کدام گیاهان است؟ (34 chars) | باستان‌سرخس باستان‌سرخس سرده‌ای منقرض‌شده از گیاهی درخت‌مانند است که برگ‌هایی شبیه به سرخس داشت. (96 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | fa |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,858 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5337 |
| BM25 hit@10 | 0.8400 |
| Query length avg chars | 39.99 |
| Document length avg chars | 489.71 |

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
  task_name: fa
  split_name: fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/fa.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1858
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 39.99
    document_mean: 489.714747
  bm25:
    ndcg_at_10: 0.5337318306
    hit_at_10: 0.84
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Persian train split data
      - Persian Wikipedia question-to-passage retrieval pairs
      - Persian entity-attribute QA evidence retrieval pairs
    synthetic_data:
      document_generation: Persian Wikipedia-style passages with titles, aliases, dates, places, offices, measurements, definitions, and factual evidence
      question_generation: Persian fact questions using varied چه, کدام, چند, در چه سالی, در کجا, علت, and چه کسی forms
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
```
