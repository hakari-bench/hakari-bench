# NanoMIRACL / id

## Overview

MIRACL includes Indonesian as a TyDi-derived same-language retrieval setting:
Indonesian questions search Indonesian Wikipedia passages with native relevance
judgments. The Nano split preserves that monolingual passage task in a compact
single-positive form. Observed queries are short Indonesian fact questions with
case variation and starts such as `Apa`, `Apakah`, `Kapan`, `Berapa`,
`Siapakah`, and `dimanakah`, so retrieval hinges on matching country, history,
religion, science, film, politics, geography, biology, and definition requests
to the answer-bearing passage.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. Indonesian queries retrieve
Indonesian Wikipedia passages, so the task measures same-language retrieval
rather than translation. The paper states that MIRACL uses native-speaker
questions and relevance judgments over passage-level Wikipedia corpora.

Indonesian is one of the MIRACL languages inherited from Mr. TyDi and TyDi QA.
The paper explains that for these languages, MIRACL aligns with the Mr. TyDi
split structure but provides denser passage annotations over a consistently
segmented Wikipedia corpus. It also adds newly generated questions with the same
annotation methodology. This makes the Indonesian task a retrieval benchmark
over answer-bearing passages, not a reading-comprehension task over a fixed
article.

MIRACL annotators generated questions from Wikipedia prompts and then judged
candidate passages retrieved by an ensemble of BM25, mDPR, and mColBERT. For
Indonesian, the MIRACL overview reports development-set BM25 nDCG@10 of 0.449.
The same paper reports stronger hybrid BM25+mDPR performance on many languages,
showing that lexical matching is an important baseline but not a complete
solution.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,520 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 38.51
characters. The most common openings are `Apa`, `Apakah`, `Kapan`, lowercase
`apakah`, `Berapa`, `berapakah`, `kapankah`, `Siapakah`, and `dimanakah`.
This visible case variation is part of the query style rather than a formatting
error to normalize away in the documentation.

Documents average 676.16 characters and are Indonesian Wikipedia passages. The
observed positives cover the Boshin War, ethanol production, Tallinn as
Estonia's capital, bishops, Hayao Miyazaki's first film, biological cells,
hydrated salts, Soeharto's fall, Hindu caste, Quran surahs, Indonesian
demographics, Bohemia, plant tumors, Riau, and national anthems.

The config language detection reports mostly Indonesian with a small amount of
Malay and other languages, which is plausible for short Indonesian/Malay-like
text and named-entity-heavy snippets. The actual inspected examples are
Indonesian Wikipedia passages and Indonesian questions. Retrieval difficulty
comes less from language identification and more from matching the exact
relation requested by short question forms.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5705
and hit@10 = 0.8350 on this Nano split. BM25 places 66 of 200 positives at rank
1 and 167 of 200 positives in the top 10. It performs well when the query
contains distinctive names such as `Hayao Miyazaki`, `Perang Boshin`, or
`Tallinn`, but it still misses 33 positives from the top 10.

The misses show common sparse-retrieval confusions. For "apakah nama ibukota
Estonia?", BM25 ranks other capital-city passages before the Tallinn passage.
For "Apakah nama lagu kebangsaan Kanada?", it retrieves pages about national
anthems of other countries before the Canadian evidence passage. For the
question about the 41st surah of the Quran, the exact `Surah Fussilat` passage
is ranked first but the labeled positive is a different Surah Ibrahim passage
that mentions ayat 35 to 41, exposing a label/query ambiguity that a benchmark
reader should notice. For Riau and Bohemia location questions, geographically
related or capital-city pages outrank the target passage.

Because every query has one positive qrel, hit@10 measures whether BM25 finds
the labeled evidence passage at all. nDCG@10 captures whether that passage is
ranked above related but non-answering material. A strong model should preserve
Indonesian entity matching while improving relation selection for capital,
population, definition, first-work, and yes/no questions.

### Training Data That May Help

Non-overlapping Indonesian MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries,
qrels, and positive passages likely to overlap with NanoMIRACL should preferably
be excluded from training. Other useful data includes Indonesian Wikipedia
question-to-passage retrieval pairs, Indonesian QA evidence retrieval datasets,
and entity-attribute supervision for places, dates, populations, religion,
science, government, and media.

Training should emphasize evidence retrieval. The model needs to retrieve the
passage that contains the requested fact, not just a related page with similar
question words or a neighboring entity.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Indonesian
Wikipedia-style passages and generate Indonesian questions grounded in one
selected passage. Useful forms include `Apa`, `Apakah`, `Kapan`, `Berapa`,
`Berapakah`, `Siapa`, `Siapakah`, `Dimana`, and `Dimanakah`, with realistic
case variation, named entities, country names, dates, counts, definitions, and
capital-city relations.

For joint document-and-question generation, create Indonesian encyclopedia-style
passages with titles, aliases, locations, dates, populations, religious terms,
scientific terms, and concise factual statements, then generate answerable
questions. Do not seed generation with Nano evaluation queries or positive
passages. Include related-entity distractors such as other capitals, other
national anthems, or neighboring administrative regions.

## Example Data

| Query | Positive document |
| --- | --- |
| berapakah jumlah karakter huruf dalam bahasa Indonesia? (55 chars) | Layanan pesan singkat Maksud dari 7 bit alphabet adalah standard untuk karakter huruf inggris (UK) termasuk yang dipakai Indonesia. Dan panjang karakter maksimal per SMS adalah 160 karakter (semua karakter termasuk spasi). Se ... [truncated 225 chars](797 chars) |
| dimanakah Mesin cetak pertama kali diciptakan? (46 chars) | Alkitab Sebelum adanya mesin cetak, bagian-bagian Alkitab disalin dengan tangan oleh para penganutnya dengan tingkat ketelitian yang tinggi. Terbukti dari salinan-salinan yang ditemukan sampai sekarang (paling tua dari abad k ... [truncated 225 chars](789 chars) |
| Apa itu Acta Sanctorum? (23 chars) | Acta Sanctorum Acta Sanctorum diterbitkan bulan Januari tahun 1643 dalam dua volume. Sebanyak 53 volume Acta Sanctorum telah diterbitkan dari tahun 1643 hingga 1794 yang memuat riwayat hidup orang beriman. Saat Acta Sanctoriu ... [truncated 225 chars](588 chars) |
| Apakah yang dimaksud dengan frekuensi audio? (44 chars) | Modulasi amplitudo Modulasi amplitudo (AM) adalah proses memodulasi sinyal frekuensi rendah pada gelombang frekuensi tinggi dengan mengubah-ubah amplitudo gelombang frekuensi tinggi tanpa mengubah frekuensinya. Frekuensi rend ... [truncated 225 chars](1131 chars) |
| Dimana James Hepburn meninggal? (31 chars) | James Curtis Hepburn Ia meninggal pada 21 September 1911 di East Orange, New Jersey, saat usia 96 tahun. (104 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | id |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | id |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,520 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5705 |
| BM25 hit@10 | 0.8350 |
| Query length avg chars | 38.51 |
| Document length avg chars | 676.16 |

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
  task_name: id
  split_name: id
  language: id
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/id.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1520
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 38.51
    document_mean: 676.163816
  bm25:
    ndcg_at_10: 0.5704678149
    hit_at_10: 0.835
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Indonesian train split data
      - Indonesian Wikipedia question-to-passage retrieval pairs
      - Indonesian entity-attribute QA evidence retrieval pairs
    synthetic_data:
      document_generation: Indonesian Wikipedia-style passages with titles, aliases, locations, dates, populations, religious terms, scientific terms, and factual evidence
      question_generation: Indonesian fact questions using varied Apa, Apakah, Kapan, Berapa, Berapakah, Siapa, Siapakah, Dimana, and Dimanakah forms with realistic case variation
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
