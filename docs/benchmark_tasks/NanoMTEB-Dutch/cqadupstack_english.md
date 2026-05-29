# NanoMTEB-Dutch / cqadupstack_english

## Overview

`cqadupstack_english` is the Dutch-translated English Language & Usage subforum
split of CQADupStack. Queries are language-usage questions and positive
documents are older duplicate questions. The task measures whether a retriever
can identify semantically equivalent questions about grammar, usage, wording,
and idioms after translation into Dutch.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
defines CQADupStack as duplicate-question retrieval and classification data from
twelve StackExchange subforums. The paper emphasizes manually flagged duplicate
links, chronological retrieval splits, and standardized evaluation for community
question answering. [BEIR](https://arxiv.org/abs/2104.08663) later repackaged
CQADupStack as one of its heterogeneous zero-shot retrieval datasets.

[BEIR-NL](https://aclanthology.org/2025.bucc-1.5/) automatically translates
public BEIR datasets into Dutch. For this subforum, the underlying topic is
English-language usage, but the benchmark text itself is Dutch-translated, so
retrievers see Dutch questions about English grammar and phrasing.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Every query has one positive. Queries average 49.65 characters and documents
average 521.67 characters. The examples ask about compound nouns, infinitive
ordering, plural notation, "lean in", and differences among purpose phrases.

This split contains many quoted English expressions embedded in Dutch text. That
mix makes the task different from general Dutch retrieval: exact English strings
can help, but the duplicate relation often depends on grammatical intent rather
than surface wording.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2769
and hit@10 = 0.3550. Quoted phrases and grammar terms support lexical matching,
but paraphrases such as "woordafscheider" versus token-list terminology still
require semantic alignment.

### Training Data That May Help

Useful training data includes non-overlapping CQADupStack English duplicate
pairs, Dutch-translated grammar help pairs, multilingual duplicate-question
data, and forum QA pairs with quoted expressions preserved. Exclude this Nano
test split and its positives from training.

### Synthetic Data Guidance

Generate Dutch questions about English usage from non-evaluation grammar posts,
including quoted English phrases. Create duplicate paraphrases that ask the same
grammatical question with different wording, and include hard negatives about
nearby but distinct usage issues.

## Example Data

| Query | Positive document |
| --- | --- |
| Het algemene 'het (17 chars) | Waar verwijst 'het' naar in dit voorbeeld? **Mogelijk duplicaat:** > Het regent. Wat dan? 'Het regent.' Waar verwijst 'het' naar? Ik weet dat sommige mensen 'het weer' zouden zeggen, maar je zou niet zeggen: 'Het weer regent. ... [truncated 225 chars](301 chars) |
| Hoe moet je een bereik van getallen met een koppelteken interpunctiëren? (72 chars) | Wat is het verschil tussen - en -- in een zin? **Mogelijke dubbel:** > Wanneer moet ik een em-dash, een en-dash en een koppelteken gebruiken? Wanneer plaats ik een - in een zin? Is het een sterkere komma? Met een langere pauz ... [truncated 225 chars](229 chars) |
| Kiezen tussen "experimenteren met" en "waarmee te experimenteren (64 chars) | Waar moet het voorzetsel van "goedkeuren" staan? **Mogelijke dubbel:** > Wanneer is het gepast om een zin met een voorzetsel te eindigen? In dit antwoord schreef ik > [Je kunt het gebruiken] om foto's te maken van een film in ... [truncated 225 chars](660 chars) |
| Hoofdletterregels voor "the (27 chars) | De hoofdletter in bepaalde lidwoorden in namen Toen ik jonger was, een aantal _mumble-mumble-mumble_ decennia geleden, leerde ik dat in namen van personen, plaatsen en dingen met het bepaalde lidwoord _the_, het lidwoord niet ... [truncated 225 chars](862 chars) |
| Wat is het verschil tussen 'part of' en 'a part of'? (52 chars) | Verschil tussen 'part' en 'a part'? Deze vraag lijkt misschien heel simpel, maar ik raak er altijd in de war wanneer ik wil spreken. Ik las een boek getiteld "re-start your English", en zag een zin. > dit is een been. het is ... [truncated 225 chars](517 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_english |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2769 |
| BM25 hit@10 | 0.3550 |
| BM25 Recall@100 | 0.4950 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3587 |
| Dense hit@10 | 0.5150 |
| Dense Recall@100 | 0.6500 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3248 |
| Reranking hybrid hit@10 | 0.4250 |
| Reranking hybrid Recall@100 | 0.6850 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 63 |
| Query length avg chars | 49.65 |
| Document length avg chars | 521.67 |

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
  task_name: cqadupstack_english
  split_name: cqadupstack_english
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_english.md
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
    query_mean: 49.65
    document_mean: 521.6717
  bm25:
    ndcg_at_10: 0.2768966576105474
    hit_at_10: 0.355
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CQADupstackEnglish-NL test split from clips/beir-nl-cqadupstack
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated CQADupStack English subforum test queries and
      duplicate positives used by this Nano split.
    useful_training_data:
    - non-overlapping CQADupStack English duplicate-question pairs
    - Dutch-translated grammar and usage duplicate questions
    - multilingual duplicate-question retrieval data with quoted phrases preserved
    synthetic_data:
      document_generation: Dutch-translated English usage forum questions outside
        the evaluation set.
      question_generation: Paraphrased duplicate grammar and wording questions.
      answerability: Each synthetic query should duplicate one prior usage question,
        with near-topic hard negatives.
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: CQADupStack DOI
      url: https://doi.org/10.1145/2838931.2838934
    - label: BEIR-NL ACL Anthology
      url: https://aclanthology.org/2025.bucc-1.5/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: clips/beir-nl-cqadupstack
      url: https://huggingface.co/datasets/clips/beir-nl-cqadupstack
    source_notes: []
  references:
  - title: 'CQADupStack: A Benchmark Data Set for Community Question-Answering Research'
    url: https://doi.org/10.1145/2838931.2838934
    year: 2015
    doi: 10.1145/2838931.2838934
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language'
    url: https://aclanthology.org/2025.bucc-1.5/
    year: 2025
    is_paper: true
    source_confidence: definitive_paper_link
  - title: clips/beir-nl-cqadupstack
    url: https://huggingface.co/datasets/clips/beir-nl-cqadupstack
    year: null
    is_paper: false
    source_confidence: probably_correct
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2768966576
      hit_at_10: 0.355
      recall_at_100: 0.495
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.495
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3586537072
      hit_at_10: 0.515
      recall_at_100: 0.65
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.65
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3248057175
      hit_at_10: 0.425
      recall_at_100: 0.685
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.315
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.685
      safeguard_positive_rows: 63
      rows_with_101_candidates: 63
```
