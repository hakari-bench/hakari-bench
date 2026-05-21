# NanoMTEB-Dutch / b_bsardnl

## Overview

`b_bsardnl` is the Dutch bBSARD statutory article retrieval task. Queries are
plain-language legal questions, and documents are Dutch Belgian statutory
articles. The retriever must find the law article or articles that support an
answer to the user's legal question.

## Details

### What the Original Data Measures

[Bilingual BSARD: Extending Statutory Article Retrieval to Dutch](https://arxiv.org/abs/2412.07462)
introduces bBSARD as a bilingual extension of the Belgian Statutory Article
Retrieval Dataset. The paper says the corpus was built by scraping parallel
French and Dutch Belgian statutory articles from the Justel portal and by
translating the BSARD legal questions into Dutch. It reports that 22,417 of
22,633 articles were available in both languages, and that the original BSARD
question set contains 1,108 citizen legal questions split into 886 train and 222
test questions.

[MTEB-NL and E5-NL](https://arxiv.org/abs/2509.12340) includes bBSARDNLRetrieval
as the Dutch subset of this bilingual legal retrieval resource. In MTEB-NL, it
is one of the main native Dutch retrieval tasks rather than a generic translated
BEIR task.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 923 positive qrel rows.
Queries average 93.84 characters and look like short citizen questions about
rent, legal aid, court procedure, bankruptcy, and Belgian regional housing law.
Documents average 863.16 characters but vary substantially, from short articles
to long statutory provisions.

This is a multi-positive legal retrieval task. The average query has 4.62
positive articles, the median is 2, and one query has 57 positives. The sampled
positive documents are article texts with section numbers, paragraph markers,
and legal conditions, so models need to connect lay wording to statutory
phrasing and sometimes retrieve several supporting provisions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1249
and hit@10 = 0.2950. This is low despite the shared language because legal
questions use everyday wording while statutory articles use formal terminology,
article numbers, definitions, and cross-references.

The bBSARD paper reports that lexical approaches remain important baselines for
legal retrieval, but the observed Nano sample shows why sparse matching is
fragile: terms such as "studentenhuurcontract", "juridische bijstand", or
"huur indexeren" may need to map to specific article titles and procedural
conditions rather than exact phrasal overlap alone.

### Training Data That May Help

Useful training data includes the non-overlapping bBSARD training split, BSARD
French-Dutch parallel legal pairs, Dutch statutory article retrieval data,
legal-aid question-answer pairs, and multilingual legal retrieval examples. The
evaluation test questions, positive article IDs, and article texts used by this
Nano split should be excluded from training and synthetic seed material.

Because many queries have multiple positives, training should preserve the set
of relevant articles rather than reducing the task to a single best article.
Cross-lingual legal training can help when it uses the same Belgian legal
concepts but does not leak the test questions.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation Dutch statutory articles
and generate layperson legal questions that paraphrase the legal conditions in
ordinary language. Include cases where a question depends on definitions,
exceptions, dates, jurisdiction, or procedure.

For joint generation, create coherent groups of related Dutch legal articles and
generate one question with several relevant articles. Add hard negatives from
nearby article numbers or the same legal code so that training rewards
article-level legal grounding.

## Example Data

| Query | Positive document |
| --- | --- |
| Ik huur het hele jaar door een caravan op een camping. Welke regels zijn van toepassing op mijn huurcontract in Brussel? (120 chars) | Art. 234. - Beginselen Dit hoofdstuk is van toepassing op huurovereenkomsten betreffende een woning die de huurder, met uitdrukkelijke of stilzwijgende toestemming van de verhuurder, vanaf de ingenottreding tot zijn hoofdverb ... [truncated 225 chars](1287 chars) |
| Ik heb een testament gemaakt. Kan ik het wijzigen? (50 chars) | Art. 969. Een testament kan eigenhandig, of bij openbare akte of in de vorm van het internationaal testament, gemaakt worden. (125 chars) |
| Moet ik de gerechtskosten betalen als ik een beslissing van een sociale zekerheidsinstelling betwist? (101 chars) | Art. 1017. Tenzij bijzondere wetten anders bepalen, verwijst ieder eindvonnis, zelfs ambtshalve, de in het ongelijk gestelde partij in de kosten, onverminderd de overeenkomst tussen partijen, die het eventueel bekrachtigt. Ni ... [truncated 225 chars](1690 chars) |
| Kan ik in Brussel de nodige reparaties zelf uitvoeren als mijn verhuurder deze niet doet? (89 chars) | Art. 223. - Herstellingen en onderhoud § 1. De huurder is gehouden tot de huurherstellingen, met uitzondering van die veroorzaakt door ouderdom of overmacht, en van de geringe herstellingen tot onderhoud. De huurherstellingen ... [truncated 225 chars](632 chars) |
| Hoe lees en begrijp ik mijn waterfactuur in Wallonië? (53 chars) | Art. R270bis8. Overlegging van de factuur De jaarlijkse regularisatiefactuur vermeldt hoe dan ook : - de naam en het adres van de bestemmeling; - de plaats van levering; - een historiek van het verbruik, met een histogram van ... [truncated 225 chars](1242 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | b_bsardnl |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/mteb-nl-bbsard](https://huggingface.co/datasets/clips/mteb-nl-bbsard) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 923 |
| Avg positives / query | 4.62 |
| Positives per query (min / median / max) | 1 / 2 / 57 |
| Queries with multiple positives | 125 (62.50%) |
| BM25 nDCG@10 | 0.1249 |
| BM25 hit@10 | 0.2950 |
| Query length avg chars | 93.84 |
| Document length avg chars | 863.16 |

### Public Sources

- [Bilingual BSARD: Extending Statutory Article Retrieval to Dutch](https://arxiv.org/abs/2412.07462), 2025.
- [ACL Anthology record for Bilingual BSARD](https://aclanthology.org/2025.regnlp-1.3/).
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.
- [clips/mteb-nl-bbsard](https://huggingface.co/datasets/clips/mteb-nl-bbsard), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/mteb-nl-bbsard](https://huggingface.co/datasets/clips/mteb-nl-bbsard)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Bilingual BSARD: Extending Statutory Article Retrieval to Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2412.07462 |
| Bilingual BSARD: Extending Statutory Article Retrieval to Dutch | 2025 | proceedings page | https://aclanthology.org/2025.regnlp-1.3/ |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |
| clips/mteb-nl-bbsard |  | dataset card | https://huggingface.co/datasets/clips/mteb-nl-bbsard |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: b_bsardnl
  split_name: b_bsardnl
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/b_bsardnl.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2412.07462
    additional_source_urls:
      - https://aclanthology.org/2025.regnlp-1.3/
      - https://arxiv.org/abs/2509.12340
      - https://huggingface.co/datasets/clips/mteb-nl-bbsard
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 923
  positives_per_query:
    average: 4.615
    min: 1
    median: 2.0
    max: 57
    multi_positive_queries: 125
    multi_positive_query_percent: 62.5
  text_stats_chars:
    query_mean: 93.845
    document_mean: 863.1596
  bm25:
    ndcg_at_10: 0.1249128833
    hit_at_10: 0.295
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "bBSARDNLRetrieval test split from clips/mteb-nl-bbsard"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude bBSARD Dutch test questions, qrels, and positive statutory articles used by this Nano split."
    useful_training_data:
      - non-overlapping bBSARD train retrieval pairs
      - Dutch statutory article retrieval data
      - Belgian legal QA and legal-aid question-answer pairs
      - French-Dutch parallel legal retrieval data with overlap removed
    synthetic_data:
      document_generation: "Dutch Belgian statutory articles or article-like legal provisions outside the evaluation set."
      question_generation: "Layperson Dutch legal questions that paraphrase article conditions, exceptions, and procedures."
      answerability: "Questions should be answerable from one or more explicit statutory articles."
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
      - label: bBSARD arXiv
        url: https://arxiv.org/abs/2412.07462
      - label: bBSARD ACL Anthology
        url: https://aclanthology.org/2025.regnlp-1.3/
      - label: MTEB-NL arXiv
        url: https://arxiv.org/abs/2509.12340
      - label: clips/mteb-nl-bbsard
        url: https://huggingface.co/datasets/clips/mteb-nl-bbsard
    source_notes: []
  references:
    - title: "Bilingual BSARD: Extending Statutory Article Retrieval to Dutch"
      url: https://arxiv.org/abs/2412.07462
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch"
      url: https://arxiv.org/abs/2509.12340
      year: 2025
      doi: 10.48550/arXiv.2509.12340
      is_paper: true
      source_confidence: definitive_paper_link
    - title: clips/mteb-nl-bbsard
      url: https://huggingface.co/datasets/clips/mteb-nl-bbsard
      year: null
      is_paper: false
      source_confidence: probably_correct
  example_count: 5
```
