# NanoMTEB-Dutch / cqadupstack_webmasters

## Overview

`cqadupstack_webmasters` is the Dutch-translated Webmasters subforum split of
CQADupStack. Queries ask about SEO, site administration, malware, spam, and web
publishing. Positive documents are earlier questions marked as duplicates.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) evaluates retrieval of
duplicate questions in community QA. The paper highlights that StackExchange
duplicates are manually flagged and that retrieval splits are chronological,
which mirrors the practical setting of finding an already answered question for
a newly posted one.

This Dutch version comes from [BEIR-NL](https://aclanthology.org/2025.bucc-1.5/),
which translated BEIR datasets to Dutch. The underlying domain remains
webmaster support, but the query/document wording is translated.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 58.83 characters and documents
average 761.20 characters. Examples cover `rel="next"` and `rel="prev"`,
malware cleanup, anti-spam forms, cross-linking, and WordPress/CMS SEO.

Documents often include quoted markup, URLs, search-engine terminology, and
site-administration context. The same topic can produce many near-duplicate
questions that differ in framing or platform.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2307
and hit@10 = 0.2850. Terms such as SEO, WordPress, malware, and `rel` help, but
translation and broad webmaster vocabulary make exact matching unreliable.

### Training Data That May Help

Useful training data includes non-overlapping Webmasters Stack Exchange
duplicate pairs, Dutch web-admin support QA, SEO question paraphrases, and
technical support duplicate-question data. Exclude this Nano test split and
positive documents.

### Synthetic Data Guidance

Generate Dutch webmaster questions from non-evaluation support posts. Include
duplicate paraphrases for SEO tags, indexing, malware warnings, forms, and CMS
configuration. Add hard negatives from the same site-management topic.

## Example Data

| Query | Positive document |
| --- | --- |
| vind-nieuwe/berichten&recent=1 als homepage: wat met SEO? (57 chars) | Best practice URL-structuur voor paginering Is een van deze formaten voor paginering beter voor SEO? * www.example.com/list/1 * www.example.com/list?page=1 Welke overwegingen of factoren moeten worden meegenomen bij het kieze ... [truncated 225 chars](332 chars) |
| Het voorkomen dat robots een specifiek gedeelte van een pagina crawlen (70 chars) | Voorkom dat zoekmachines specifieke content op uw site indexeren **Mogelijk duplicaat:** > Voorkomen dat robots een specifiek gedeelte van een pagina crawlen Ik heb een nogal vreemd scenario waar ik me afvroeg of iemand me me ... [truncated 225 chars](1067 chars) |
| SEO-voorkeur voor WWW of HTTP:// protocolredirectie? Ranken www-websites beter dan niet-www? (92 chars) | Wat is de beste werkwijze voor het kiezen van een standaarddomein - www.example.com of example.com? **Mogelijk duplicaat:** > SEO-voorkeur voor WWW of HTTP:// protocolredirectie? Ranken www-websites > beter dan niet-www websi ... [truncated 225 chars](458 chars) |
| Wat betekenen dubbele slashes in URL\'s? (40 chars) | Is er een probleem met het gebruik van twee slashes in het midden van een URL? **Mogelijke dubbel: (99 chars) |
| Waarom werken Google Rich Snippets voor de ene site-auteur wel en voor de andere niet? (86 chars) | Rich snippets genegeerd door Google **Mogelijk duplicaat:** Waarom werken Google Rich Snippets voor de ene site-auteur wel en voor de andere niet? Ik loop tegen een probleem aan. Ik heb rich snippets – microdata – voor de web ... [truncated 225 chars](764 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_webmasters |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2307 |
| BM25 hit@10 | 0.2850 |
| BM25 Recall@100 | 0.5550 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2947 |
| Dense hit@10 | 0.4450 |
| Dense Recall@100 | 0.6700 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2968 |
| Reranking hybrid hit@10 | 0.4200 |
| Reranking hybrid Recall@100 | 0.7250 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 55 |
| Query length avg chars | 58.83 |
| Document length avg chars | 761.20 |

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
  task_name: cqadupstack_webmasters
  split_name: cqadupstack_webmasters
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_webmasters.md
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
    query_mean: 58.825
    document_mean: 761.2033
  bm25:
    ndcg_at_10: 0.23069243882907045
    hit_at_10: 0.285
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CQADupstackWebmasters-NL test split from clips/beir-nl-cqadupstack
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated CQADupStack Webmasters test queries and duplicate
      positives used by this Nano split.
    useful_training_data:
    - non-overlapping Webmasters Stack Exchange duplicate-question pairs
    - Dutch web-admin support QA
    - SEO and CMS duplicate-question pairs with overlap removed
    synthetic_data:
      document_generation: Dutch webmaster support questions outside the evaluation
        set.
      question_generation: Paraphrased duplicate SEO, site-admin, and CMS troubleshooting
        questions.
      answerability: Each query should duplicate one prior webmaster question, with
        same-topic hard negatives.
    multi_positive_training: single_positive
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2306924388
      hit_at_10: 0.285
      recall_at_100: 0.555
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.555
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2947360296
      hit_at_10: 0.445
      recall_at_100: 0.67
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.67
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2968084248
      hit_at_10: 0.42
      recall_at_100: 0.725
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.275
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.725
      safeguard_positive_rows: 55
      rows_with_101_candidates: 55
```
