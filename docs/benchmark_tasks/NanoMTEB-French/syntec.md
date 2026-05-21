# NanoMTEB-French / syntec

## Overview

`syntec` is a French retrieval task built from the Syntec collective bargaining
agreement. Queries are natural-language employment questions, and documents are
articles from the collective agreement. The retriever must find the article
that governs the labor-law or workplace-policy question.

## Details

### What the Original Data Measures

[MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468)
introduces SyntecRetrieval as a new French retrieval dataset. The paper
describes scraping the Syntec collective bargaining agreement, using its
articles as documents, and writing queries for retrieval evaluation. It notes
that Syntec is legal/workplace text, but the language is less specialized than
some statutory legal datasets.

### Observed Data Profile

The Nano split has 100 French queries, 90 documents, and 100 positive qrels.
Every query has one positive. Queries average 72.80 characters, while documents
average 1,226.27 characters. Sampled questions ask about illness and seniority,
unpaid leave, `IC`, Sunday work, and family travel during foreign assignments.

Documents are article-level provisions with article numbers, modification
notices, and structured subsections. The small corpus makes the task compact,
but many article texts are long enough to require finding the relevant clause.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6906 and hit@10 = 0.8700. The median best rank is 1. BM25 is strong because
queries often reuse legal terms from the article titles, but abbreviations and
policy paraphrases can still push positives below rank 1.

### Training Data That May Help

Useful training data includes French collective-agreement QA, labor-law FAQ to
article retrieval pairs, and non-overlapping Syntec-style article questions.
Training should avoid Nano queries, qrels, and Syntec article positives used in
the evaluation.

### Synthetic Data Guidance

Generate French workplace-policy articles and employee questions about leave,
seniority, Sunday work, travel, classifications, and termination. Documents
should preserve article numbering and clause structure; questions should be
natural employee wording.

## Example Data

| Query | Positive document |
| --- | --- |
| Puis-je justifier d'une indemnité de licenciement si cela fait-il plus de 2 ans que je suis dans cette entreprise ? (115 chars) | Article 18 : Indemnité de licenciement – Conditions d’attribution Modification Avenant n° 7 du 5/07/1991 Il est attribué à tout salarié licencié justifiant d’au moins 2 années d’ancienneté une indemnité de licenciement distin ... [truncated 225 chars](690 chars) |
| Mon entreprise a déposé un brevet sur mon invention. A quoi ai-je droit ? (73 chars) | Article 75 : Invention des salariés dans le cadre des activités professionnelles Dispositions générales : Les règles relatives aux inventions des salariés sont fixées par la loi n° 78-742 du 13 juillet 1978 modifiant et compl ... [truncated 225 chars](3628 chars) |
| Quelle est la période de prise de congés ? (42 chars) | Article 25 : Période de congés Les droits à congé s’acquièrent du 1er juin de l’année précédente au 31 mai de l’année en cours. La période de prise de ces congés, dans tous les cas, est de treize mois au maximum. Aucun report ... [truncated 225 chars](753 chars) |
| J'ai le droit de faire combien d'heures supplémentaires sans avoir l'accord de l'inspecteur du travail ? (104 chars) | Article 33 : Heures supplémentaires [En vigueur] ETAM hors CE : A. – Rémunération des heures supplémentaires : Les heures supplémentaires de travail contrôlées, effectuées par le personnel ETAM, sont payées avec les majoratio ... [truncated 225 chars](465 chars) |
| Y a-t-il un examen médical obligatoire au retour d'un déplacement à l'étranger ? (80 chars) | Article 73 : Contrôle médical En cas de séjour prolongé à l’étranger, le salarié est tenu, à la demande de l’employeur avant son départ et dans le mois qui suit son retour à son domicile, de subir, lui et éventuellement les m ... [truncated 225 chars](513 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Task / split | syntec |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Language | fr |
| Category | natural_language |
| Queries | 100 |
| Documents | 90 |
| Positive qrels | 100 |
| BM25 nDCG@10 | 0.6906 |
| BM25 hit@10 | 0.8700 |
| Query length avg chars | 72.80 |
| Document length avg chars | 1226.27 |

### Public Sources

- [MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468); 2024; Mathieu Ciancone et al.
- [lyon-nlp/mteb-fr-retrieval-syntec-s2p dataset card](https://huggingface.co/datasets/lyon-nlp/mteb-fr-retrieval-syntec-s2p).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French)
- Source dataset: [lyon-nlp/mteb-fr-retrieval-syntec-s2p](https://huggingface.co/datasets/lyon-nlp/mteb-fr-retrieval-syntec-s2p)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis | 2024 | arXiv paper | https://arxiv.org/abs/2405.20468 |
| lyon-nlp/mteb-fr-retrieval-syntec-s2p | 2024 | dataset card | https://huggingface.co/datasets/lyon-nlp/mteb-fr-retrieval-syntec-s2p |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-French
  backing_dataset: NanoMTEB-French
  dataset_id: hakari-bench/NanoMTEB-French
  task_name: syntec
  split_name: syntec
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/syntec.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 100
    documents: 90
    positive_qrels: 100
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 72.8
    document_mean: 1226.2666666666667
  bm25:
    ndcg_at_10: 0.6906106408
    hit_at_10: 0.87
    source: dataset_bm25_column
  learning:
    original_train_split: not_found
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Nano queries, qrels, and Syntec article positives used in this evaluation
    useful_training_data:
      - French collective-agreement QA pairs
      - French labor-law FAQ to article retrieval data
      - non-overlapping employment policy question-article pairs
      - hard negatives from adjacent agreement articles
    synthetic_data:
      document_generation: French workplace-policy articles with article numbers, clauses, exceptions, and modification notes
      question_generation: employee questions about leave, seniority, Sunday work, travel, classifications, and termination
      answerability: each positive article should include the clause that resolves the employee question
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-French
    source_urls:
      - label: MTEB-French arXiv
        url: https://arxiv.org/abs/2405.20468
      - label: lyon-nlp/mteb-fr-retrieval-syntec-s2p
        url: https://huggingface.co/datasets/lyon-nlp/mteb-fr-retrieval-syntec-s2p
    source_notes: []
  references:
    - title: "MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis"
      url: https://arxiv.org/abs/2405.20468
      year: 2024
      doi: 10.48550/arXiv.2405.20468
      is_paper: true
      source_confidence: definitive_paper_link
```
