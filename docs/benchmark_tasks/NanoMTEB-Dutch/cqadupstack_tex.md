# NanoMTEB-Dutch / cqadupstack_tex

## Overview

`cqadupstack_tex` is the Dutch-translated TeX / LaTeX subforum split of
CQADupStack. Queries are typesetting questions and positives are older duplicate
questions. The task measures retrieval over LaTeX tooling, Beamer, TeXstudio,
TikZ, fonts, and compilation workflows.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) provides duplicate
question retrieval data from StackExchange subforums, including TeX. It uses
manually flagged duplicate links and chronological retrieval splits. The task is
to find the earlier question that resolves the same user need.

[BEIR-NL](https://aclanthology.org/2025.bucc-1.5/) automatically translates
public BEIR datasets into Dutch. In this split, TeX commands, package names, and
code fragments often remain in their original form while explanatory text is
translated.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 53.53 characters. Documents average
1,211.75 characters, the longest among the inspected CQADupStack Dutch
subforums. Examples include live LaTeX preview, TeXstudio shortcuts, Beamer
navigation dots, identifying a font, and TikZ externalization with pgfplots.

Duplicate matching often depends on commands and package names, but long MWE-like
documents and translated prose can obscure the core intent.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2106
and hit@10 = 0.2850. Exact commands help, but many questions are short and the
documents are long, so sparse retrieval can over-rank posts that share packages
without solving the same problem.

### Training Data That May Help

Useful training data includes non-overlapping TeX Stack Exchange duplicate pairs,
LaTeX support QA, code-aware duplicate retrieval data, and Dutch-translated
technical forum pairs. Exclude this Nano test split and positives.

### Synthetic Data Guidance

Generate Dutch LaTeX questions from non-evaluation posts while preserving
commands, package names, and minimal examples. Create duplicates with different
wording but the same desired rendering or compilation behavior.

## Example Data

| Query | Positive document |
| --- | --- |
| BibLaTeX: primaire en secundaire bibliografieën (47 chars) | Bibliografie met verschillende namen en gesorteerd op naam Ik wil graag twee bibliografieën maken met twee verschillende namen. Mijn twee bibliografieën zijn books.bib en articles.bib. Door \renewcommand{\refname}{Referenties ... [truncated 225 chars](559 chars) |
| Hoe kan ik het compileren van een document met meerdere afbeeldingen versnellen? (80 chars) | Het verwerken van alle afbeeldingen onderdrukken Ik probeer een concept te maken door LaTeX te dwingen alle afbeeldingen te negeren. Hoe kan ik LaTeX vertellen alle afbeeldingsbestandsnamen (in de `\includegraphics`-opdracht) ... [truncated 225 chars](420 chars) |
| Lege regels in align-omgeving (29 chars) | Waarom geeft een extra regel witruimte voor \end{align} een foutmelding? Ik voeg vaak extra witruimte toe aan mijn TeX-bestand voor betere leesbaarheid, en ik krijg deze foutmelding steeds wanneer er een lege regel voor `\end ... [truncated 225 chars](312 chars) |
| alternatief voor slashbox (25 chars) | Geavanceerde tabellen maken ![voer hier een afbeeldingbeschrijving in](http://i.stack.imgur.com/PX4Jn.png) Ik probeer tabellen te genereren zoals de bovenstaande die ik in een leerboek in LaTeX heb gevonden. In het bijzonder ... [truncated 225 chars](456 chars) |
| Een ander plaatje plaatsen in elke paginahoek (45 chars) | Bladerboek in masterproef Ik schrijf momenteel mijn masterproef in de informatica over een visualisatieonderwerp. Aangezien de kern van mijn scriptie een complexe 3D-visualisatie is die zijn boodschap alleen goed overbrengt v ... [truncated 225 chars](2990 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_tex |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2106 |
| BM25 hit@10 | 0.2850 |
| BM25 Recall@100 | 0.5650 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2611 |
| Dense hit@10 | 0.3800 |
| Dense Recall@100 | 0.6400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2926 |
| Reranking hybrid hit@10 | 0.4100 |
| Reranking hybrid Recall@100 | 0.6750 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 65 |
| Query length avg chars | 53.53 |
| Document length avg chars | 1,211.75 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: cqadupstack_tex
  split_name: cqadupstack_tex
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_tex.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
    - https://eltimster.github.io/www/pubs/adcs2015.pdf
    - https://aclanthology.org/2025.bucc-1.5/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/clips/beir-nl-cqadupstack
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
    query_mean: 53.53
    document_mean: 1211.7541
  bm25:
    ndcg_at_10: 0.21058258509758204
    hit_at_10: 0.285
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CQADupstackTex-NL test split from clips/beir-nl-cqadupstack
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated CQADupStack TeX test queries and duplicate positives
      used by this Nano split.
    useful_training_data:
    - non-overlapping TeX Stack Exchange duplicate-question pairs
    - LaTeX support QA pairs
    - code-aware technical duplicate retrieval data
    synthetic_data:
      document_generation: Dutch LaTeX support posts with commands and minimal examples
        preserved.
      question_generation: Paraphrased duplicate TeX questions about the same rendering
        or compilation issue.
      answerability: Each query should duplicate one prior TeX question, with package-near
        hard negatives.
    multi_positive_training: single_positive
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2105825851
      hit_at_10: 0.285
      recall_at_100: 0.565
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.565
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2610955367
      hit_at_10: 0.38
      recall_at_100: 0.64
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.64
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2925875899
      hit_at_10: 0.41
      recall_at_100: 0.675
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.325
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.675
      safeguard_positive_rows: 65
      rows_with_101_candidates: 65
```
