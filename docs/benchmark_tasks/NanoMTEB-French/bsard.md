# NanoMTEB-French / bsard

## Overview

`bsard` is the Belgian Statutory Article Retrieval Dataset in French. Queries
are lay legal questions, often with category labels, and documents are Belgian
statutory articles. The retriever must find the law article relevant to a
citizen's legal issue.

## Details

### What the Original Data Measures

[A Statutory Article Retrieval Dataset in French](https://arxiv.org/abs/2108.11792)
introduces BSARD as more than 1,100 French legal questions labeled by
experienced jurists with relevant articles from a corpus of over 22,600 Belgian
law articles. The paper emphasizes the mismatch between ordinary citizens'
language and statutory language, plus the hierarchical structure of legal
codes.

### Observed Data Profile

The Nano split has 200 French queries, 10,000 law-article documents, and 200
positive qrels. Every query has one positive in this compact split. Queries
average 144.97 characters, and documents average 793.01 characters. Sampled
queries cover debt mediation, rental inventory in Brussels, criminal fines,
lease termination, and legal aid income conditions.

Documents are formal statutory text with article sections, enumerated clauses,
and dense legal terminology. The positive article may not repeat the lay
question wording directly.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1708 and hit@10 = 0.2850. Only 14 positives are ranked first, and the median
best rank is 66. This is one of the harder French splits for lexical retrieval
because query language and statute language often diverge.

### Training Data That May Help

Useful training data includes non-overlapping BSARD train examples, French
legal question-to-statute retrieval pairs, legal FAQ-to-code mappings, and hard
negatives from the same legal code. Training should avoid BSARD test questions,
Nano queries, qrels, and positive statute text likely to overlap.

### Synthetic Data Guidance

Generate French lay legal questions and formal Belgian-style statutory
articles. Include rental law, debt, family law, legal aid, procedure, and
administrative benefits. Synthetic questions should use non-expert wording
while positives use legal article style, with explicit statutory grounding.

## Example Data

| Query | Positive document |
| --- | --- |
| Je loue une caravane dans un camping à l'année. Quelles règles s'appliquent à mon bail à Bruxelles ? Bail de résidence principale (Bruxelles), Champ d'application (162 chars) | PrincipesLe présent chapitre s'applique aux baux portant sur le logement que le preneur, avec l'accord exprès ou tacite du bailleur, affecte dès l'entrée en jouissance à sa résidence principale. Est réputée non écrite la clau ... [truncated 225 chars](1082 chars) |
| J’ai fait un testament. Puis-je le modifier ? Démarches avant décès, Donation et testament, Testament (101 chars) | Le testament par acte public est celui qui est reçu par un notaire. Le testament par acte public est celui qui est reçu par un notaire, en présence de deux témoins, ou par deux notaires. (186 chars) |
| Dois-je payer les frais de justice si je conteste une décision d’un organisme de sécurité sociale ? (99 chars) | L'indemnité de procédure est une intervention forfaitaire dans les frais et honoraires d'avocat de la partie ayant obtenu gain de cause.Après avoir pris l'avis de l'Ordre des barreaux francophones et germanophone et de l'Orde ... [truncated 225 chars](2341 chars) |
| Mon propriétaire ne fait pas les réparations nécessaires, puis-je faire les réparations à sa place à Bruxelles ? Bail de résidence principale (Bruxelles), Réparations, entretiens et travaux, Inaction du propriétaire (215 chars) | Réparations et entretien§ 1er. Le preneur est tenu des réparations locatives, à l'exception de celles qui sont occasionnées par la vétusté ou la force majeure, et des travaux de menu entretien.Les réparations locatives et de ... [truncated 225 chars](555 chars) |
| Comment lire et comprendre ma facture d'eau en Wallonie ? Dettes liées à la fourniture d'eau, En Wallonie (105 chars) | Une facture annuelle est établie par le distributeur. De plus, des acomptes ou des factures intermédiaires au minimum trimestriels seront établis.En cas de changement d'usager ainsi qu'en cas de modification de la période de ... [truncated 225 chars](530 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Task / split | bsard |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Language | fr |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.1708 |
| BM25 hit@10 | 0.2850 |
| Query length avg chars | 144.97 |
| Document length avg chars | 793.01 |

### Public Sources

- [A Statutory Article Retrieval Dataset in French](https://arxiv.org/abs/2108.11792); 2022; Antoine Louis and Gerasimos Spanakis.
- [mteb/BSARDRetrieval dataset card](https://huggingface.co/datasets/mteb/BSARDRetrieval).
- [MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468); 2024; Mathieu Ciancone et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French)
- Source dataset: [mteb/BSARDRetrieval](https://huggingface.co/datasets/mteb/BSARDRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Statutory Article Retrieval Dataset in French | 2022 | arXiv paper | https://arxiv.org/abs/2108.11792 |
| MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis | 2024 | arXiv paper | https://arxiv.org/abs/2405.20468 |
| mteb/BSARDRetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/BSARDRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-French
  backing_dataset: NanoMTEB-French
  dataset_id: hakari-bench/NanoMTEB-French
  task_name: bsard
  split_name: bsard
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/bsard.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 144.965
    document_mean: 793.0132
  bm25:
    ndcg_at_10: 0.1707572164
    hit_at_10: 0.285
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude BSARD test questions, Nano queries, qrels, and positive Belgian law articles likely to overlap with this evaluation
    useful_training_data:
      - non-overlapping BSARD train examples
      - French legal question-to-statute retrieval pairs
      - legal FAQ to code article mappings
      - hard negatives from the same Belgian code or legal topic
    synthetic_data:
      document_generation: formal French Belgian-style statutory articles with sections, clauses, and legal terminology
      question_generation: lay French legal questions about debt, rental law, family law, legal aid, procedure, and benefits
      answerability: each positive article should provide the statutory basis needed to address the lay question
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-French
    source_urls:
      - label: BSARD arXiv
        url: https://arxiv.org/abs/2108.11792
      - label: mteb/BSARDRetrieval
        url: https://huggingface.co/datasets/mteb/BSARDRetrieval
      - label: MTEB-French arXiv
        url: https://arxiv.org/abs/2405.20468
    source_notes: []
  references:
    - title: "A Statutory Article Retrieval Dataset in French"
      url: https://arxiv.org/abs/2108.11792
      year: 2022
      doi: 10.18653/v1/2022.acl-long.468
      is_paper: true
      source_confidence: definitive_paper_link
```
