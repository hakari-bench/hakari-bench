# NanoMIRACL / fi

## Overview

MIRACL reuses Finnish from the TyDi/Mr. TyDi lineage as monolingual retrieval:
Finnish questions are answered by Finnish Wikipedia passages with
native-language judgments. In the Nano split, every query has one labeled
positive passage. The inspected queries are compact Finnish fact questions with
starts such as `Milloin`, `Mikä`, `Kuka`, `Onko`, `Mitä`, and `Missä`, so the
task focuses on exact same-language evidence retrieval for science, history,
places, philosophy, films, food, religion, and definitions.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a monolingual
ad hoc retrieval benchmark over Wikipedia passages. The query and corpus
language are the same, so Finnish queries retrieve Finnish Wikipedia passages.
The paper states that MIRACL uses natural-language questions, passage-level
Wikipedia corpora, and native-speaker relevance judgments.

Finnish is one of the MIRACL languages inherited from Mr. TyDi and TyDi QA. The
paper explains that for these languages, MIRACL aligns with the existing Mr.
TyDi splits but adds denser positive and negative annotations over a
consistently segmented Wikipedia passage corpus. That makes this task a
passage-retrieval benchmark rather than an answer extraction task over a
preselected article.

MIRACL's annotation workflow also matters. Annotators generated well-formed
questions from Wikipedia prompts and then judged candidate passages returned by
an ensemble of BM25, mDPR, and mColBERT. For Finnish, the original paper reports
development-set BM25 nDCG@10 of 0.551 and hybrid BM25+mDPR nDCG@10 of 0.672,
which suggests that lexical matching is strong but still leaves room for better
semantic passage selection.

### Observed Data Profile

The sampled Nano task has 200 queries, 1,828 documents, and 200 positive qrel
rows. Every query has exactly one positive passage. Queries average 37.34
characters and are compact Finnish questions. The most frequent openings are
`Milloin`, `Mikä`, `Kuka`, `Onko`, `Mitä`, and `Missä`, followed by forms such
as `Mistä`, `Miten`, `Kuinka`, and `Mihin`.

Documents average 653.42 characters and are Finnish Wikipedia passages that
usually begin with the article title. The observed positives cover scientific
definitions such as phosphorescence and hydrology, historical rulers, Christian
reformation topics, philosophy, film direction, places, food, geography, horse
colors, and mental-health terminology. Many queries ask for definitions or a
single factual relation, and the relevant passage may be a subsection of a
broader article rather than the obvious title page.

Finnish morphology makes evidence retrieval more than string matching. Query
forms such as `sijaitsee`, `tarkoittaa`, `tutkii`, and case-marked entity names
need to be matched to inflected or compound-heavy Wikipedia text. A useful
retriever should identify the answer-bearing relation, not simply the closest
surface overlap.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6240
and hit@10 = 0.8950 on this Nano split. BM25 places 72 of 200 positives at rank
1 and 179 of 200 positives in the top 10. This is a strong sparse baseline: many
queries include distinctive Finnish terms such as `fosforesenssi`,
`hydrologia`, `Sääksmäki`, or `Kordillieerit`.

The failure cases show where lexical matching still breaks. For "Onko
uskonpuhdistus sama kuin reformaatio?", BM25 retrieves several Uskonpuhdistus
passages but the labeled passage in a broader Renaissance philosophy article is
rank 13. For "Kuka on ohjannut Black Panther elokuvan?", top passages about
music and release details outrank the passage that names the director. For
"Mitä on stoalaisuus?" and "Mitä on altruismi?", abstract `Mitä on` queries are
distracted by generic philosophy and psychology passages. For location
questions such as "Missä sijaitsee Kronstadt?" and "Missä sijaitsee
Sääksmäki?", BM25's top hits can be unrelated Finnish-place or map-like passages
while the obvious positive article appears far lower.

Because this Nano split is single-positive, hit@10 measures whether the labeled
evidence passage is retrieved at all, while nDCG@10 captures whether it is ranked
near the top. A strong model should keep BM25's rare-term advantage and improve
inflection-aware relation matching for definitions, locations, and creator or
role questions.

### Training Data That May Help

Non-overlapping Finnish MIRACL training data is the first source to inspect.
Because this task is MIRACL-derived, upstream development or test queries, qrels,
and positive passages likely to overlap with NanoMIRACL should preferably be
excluded from training. Other useful data includes Finnish Wikipedia
question-to-passage retrieval pairs, Finnish QA evidence retrieval datasets, and
entity-attribute examples covering places, definitions, dates, creators, and
scientific concepts.

Training should emphasize passage evidence rather than short-answer generation.
The model needs to retrieve the passage that supports the answer, even when a
same-title page, a broader concept article, or an inflected form creates strong
lexical overlap.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Finnish Wikipedia-style
passages and generate Finnish questions grounded in one selected passage. Useful
forms include `Mikä`, `Mitä`, `Milloin`, `Missä`, `Kuka`, `Onko`, `Kuinka`,
`Mistä`, and `Miten`, with inflected names, compounds, dates, locations, and
definition sentences.

For joint document-and-question generation, create Finnish encyclopedia-style
passages with titles, aliases, dates, places, role descriptions, and concise
factual statements, then generate answerable Finnish questions. Do not seed
generation with Nano evaluation queries or positive passages. Synthetic data is
most useful when it includes related but non-answering passages so the model
learns to rank evidence over topic overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| Mistä nimitys markka tulee? (27 chars) | Suomen markka Markka otettiin käyttöön vuonna 1860, mutta sen kurssi oli sidottu ruplan arvoon: yksi markka vastasi ruplaa, jota sitäkin Venäjällä epäiltiin liian suureksi yksiköksi. Rahan nimi valittiin kilpailulla. Markan j ... [truncated 225 chars](634 chars) |
| Minkälaisia arimaa-pelin nappulat ovat? (39 chars) | Arimaa (peli) Arimaata pelataan shakkilaudan kaltaisella 8×8 ruudun laudalla, jonka neljä ruutua, c3, f3, c6 ja f6 ovat "ansaruutuja". Kummallakin pelaajalla, kullalla ja hopealla, on kuusitoista nappulaa. Vahvimmasta heikoim ... [truncated 225 chars](476 chars) |
| Onko Uranuksella kuita? (23 chars) | Uranus Uranuksella on 27 tunnettua kuuta. Kaksi suurinta kuuta, Titanian ja Oberonin, löysi Herschel 13. maaliskuuta 1787. William Lassell löysi Arielin ja Umbrielin vuonna 1851. William Herschelin poika John nimesi vuotta my ... [truncated 225 chars](908 chars) |
| Onko Unelmien talli -kirjasarjan kirjoissa yhteinen juoni? (58 chars) | Unelmien talli Unelmien talli on kirjailija Tiina Lehtinevan luoma kirjasarja. Siihen kuuluu viisi osaa: "Unelmien painajainen" (Aikamedia, 2005), "Unelmien laukka" (Aikamedia, 2007), "Unelmien tahdon" (Aikamedia, 2008), "Une ... [truncated 225 chars](561 chars) |
| Missä Angleseyn saari sijaitsee? (32 chars) | Anglesey Anglesey () on Irlanninmeren saari Walesin luoteisrannikolla. Anglesey on Walesin ja Englannin suurin saari ja sen pinta-ala on 676 km². Hallinnollisesti Anglesey muodostaa Isle of Angleseyn (kymriksi "Ynys Môn") kre ... [truncated 225 chars](348 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Task / split | fi |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | fi |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,828 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6240 |
| BM25 hit@10 | 0.8950 |
| Query length avg chars | 37.34 |
| Document length avg chars | 653.42 |

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
  task_name: fi
  split_name: fi
  language: fi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/fi.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1828
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 37.335
    document_mean: 653.41849
  bm25:
    ndcg_at_10: 0.6240408593
    hit_at_10: 0.895
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream development/test data or other MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions and passages
    useful_training_data:
      - non-overlapping MIRACL Finnish train split data
      - Finnish Wikipedia question-to-passage retrieval pairs
      - Finnish entity-attribute QA evidence retrieval pairs
    synthetic_data:
      document_generation: Finnish Wikipedia-style passages with titles, aliases, dates, locations, definitions, roles, and factual evidence
      question_generation: Finnish fact questions using varied Mikä, Mitä, Milloin, Missä, Kuka, Onko, Kuinka, Mistä, and Miten forms with realistic inflection
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
