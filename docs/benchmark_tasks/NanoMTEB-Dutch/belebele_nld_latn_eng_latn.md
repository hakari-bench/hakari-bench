# NanoMTEB-Dutch / belebele_nld_latn_eng_latn

## Overview

`belebele_nld_latn_eng_latn` is the Dutch-to-English Belebele retrieval split:
English questions retrieve Dutch passages. It tests whether a retriever can map
English reading-comprehension questions onto Dutch answer-bearing passages.

## Details

### What the Original Data Measures

[The Belebele Benchmark](https://arxiv.org/abs/2308.16884) was built as a
parallel reading-comprehension benchmark over FLORES-200 passages, with 900
unique questions and four answer choices across 122 language variants. The paper
emphasizes that questions were curated to be answerable from the passage while
not being trivially solved by lexical heuristics.

[MTEB-NL and E5-NL](https://arxiv.org/abs/2509.12340) lists BelebeleRetrieval as
part of MTEB-NL's retrieval coverage and says the Dutch portion was used without
extra preprocessing. This split reverses the language direction of
`belebele_eng_latn_nld_latn`: the query is English and the relevant passage is
Dutch.

### Observed Data Profile

The Nano split has 200 queries, 488 documents, and 200 positive qrel rows. Each
query has one positive. Queries average 81.31 characters and are English
questions; documents average 529.14 characters and are Dutch passages. Examples
include questions about organizational history, animal anatomy, mutations,
Maori history, and the temple of Artemis.

The Dutch passages are longer than the English-document direction on average,
and the English questions often contain generic phrases such as "according to
the passage". The retriever needs to align English question semantics to Dutch
evidence without relying on shared content words.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1226
and hit@10 = 0.1950. This is difficult for BM25 because the query is entirely
English and the documents are Dutch, leaving only names, numbers, and occasional
cognates as lexical anchors.

Compared with the Dutch-query English-document direction, the observed sparse
baseline is much weaker. The samples show why: English terms such as "mutation",
"offspring", or "arsonist" must map to Dutch wording such as "mutaties",
"erfelijk", or "in brand gestoken".

### Training Data That May Help

Useful training data includes English-to-Dutch parallel QA retrieval,
cross-lingual sentence and passage retrieval, translated reading-comprehension
tasks, and multilingual dense-retrieval data with Dutch documents. Do not train
on the Belebele test items used by this split.

Because the document side is Dutch, models with strong Dutch passage encoders
and English query alignment are likely to help. Hard negatives should include
Dutch passages that share entities or themes but answer a different question.

### Synthetic Data Guidance

For document-to-query generation, use Dutch passages outside the evaluation set
and generate English questions that target explicit facts in those passages.
Include entity-heavy and relation-heavy questions, not only direct keyword
questions.

For joint generation, create Dutch short passages paired with English
comprehension questions, plus Dutch hard negatives from nearby topics. The
generated question should be answerable from the Dutch passage alone.

## Example Data

| Query | Positive document |
| --- | --- |
| Which of the changes prompted by The French Revolution had a significant impact on working class citizens? (106 chars) | De Revolutie heeft grote sociale en politieke gevolgen gehad, zoals het gebruik van het metrieke stelsel, een verschuiving van de absolute monarchie naar republicanisme, nationalisme en de opvatting dat het land aan zijn inwo ... [truncated 225 chars](650 chars) |
| According to the passage, who may have started an agriculture society? (70 chars) | Voor een groot deel van de negentiende en twintigste eeuw geloofde men dat de vroegste inwoners van Nieuw-Zeeland de Maori waren, die jacht maakten die op enorme vogels genaamd moa's. De theorie leidde tot het idee dat het Ma ... [truncated 225 chars](774 chars) |
| Which of the following accurately describes the practice of subsistence agriculture? (84 chars) | Zelfvoorzienende landbouw is landbouw waarbij voldoende voedsel wordt geproduceerd om aan de behoeften van de boer en zijn gezin te voldoen. Landbouw met als doel levensonderhoud is een simpel systeem dat meestal biologisch i ... [truncated 225 chars](552 chars) |
| According to the passage, which of the following was one of China’s most violent eras? (86 chars) | Het oude China had een unieke manier om verschillende tijdsperiodes weer te geven; iedere fase van China of iedere regerende familie had een onderscheidende dynastie. Ook tussen de verschillende dynastieën was er een onstabie ... [truncated 225 chars](710 chars) |
| When did King Tutankhamun gain notoriety? (41 chars) | Ja! Koning Toetanchamon is vandaag de dag een van de bekendste koningen van het oude Egypte. In de oudheid werd hij echter niet als belangrijk beschouwd en hij is niet opgenomen in de meeste lijsten met koningen uit de oudhei ... [truncated 225 chars](525 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | belebele_nld_latn_eng_latn |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [mteb/belebele](https://huggingface.co/datasets/mteb/belebele) |
| Language | en query, nl document |
| Category | natural_language |
| Queries | 200 |
| Documents | 488 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3288 |
| BM25 hit@10 | 0.3800 |
| BM25 Recall@100 | 0.4400 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9306 |
| Dense hit@10 | 0.9850 |
| Dense Recall@100 | 0.9850 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4456 |
| Reranking hybrid hit@10 | 0.5200 |
| Reranking hybrid Recall@100 | 0.9900 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 81.31 |
| Document length avg chars | 529.14 |

### Public Sources

- [The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884), 2023.
- [facebookresearch/belebele](https://github.com/facebookresearch/belebele), source repository.
- [mteb/belebele](https://huggingface.co/datasets/mteb/belebele), MTEB dataset card.
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [mteb/belebele](https://huggingface.co/datasets/mteb/belebele)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | arXiv paper | https://arxiv.org/abs/2308.16884 |
| facebookresearch/belebele | 2023 | repository | https://github.com/facebookresearch/belebele |
| mteb/belebele |  | dataset card | https://huggingface.co/datasets/mteb/belebele |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: belebele_nld_latn_eng_latn
  split_name: belebele_nld_latn_eng_latn
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/belebele_nld_latn_eng_latn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2308.16884
    additional_source_urls:
    - https://github.com/facebookresearch/belebele
    - https://huggingface.co/datasets/mteb/belebele
    - https://arxiv.org/abs/2509.12340
  counts:
    queries: 200
    documents: 488
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 81.305
    document_mean: 529.143443
  bm25:
    ndcg_at_10: 0.3287836985129981
    hit_at_10: 0.38
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: mteb/belebele nld_Latn-eng_Latn test split
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude Belebele test questions and passages used by this Nano split.
    useful_training_data:
    - English-to-Dutch parallel QA retrieval pairs
    - multilingual dense retrieval data with Dutch documents
    - translated reading-comprehension examples with English queries
    - Dutch passage retrieval hard negatives with overlap removed
    synthetic_data:
      document_generation: Short Dutch passages outside the evaluation set.
      question_generation: English comprehension questions grounded in the Dutch passage.
      answerability: Each generated English query should be answerable from one Dutch
        passage.
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: Belebele arXiv
      url: https://arxiv.org/abs/2308.16884
    - label: Belebele repository
      url: https://github.com/facebookresearch/belebele
    - label: mteb/belebele
      url: https://huggingface.co/datasets/mteb/belebele
    - label: MTEB-NL arXiv
      url: https://arxiv.org/abs/2509.12340
    source_notes: []
  references:
  - title: 'The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122
      Language Variants'
    url: https://arxiv.org/abs/2308.16884
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch'
    url: https://arxiv.org/abs/2509.12340
    year: 2025
    doi: 10.48550/arXiv.2509.12340
    is_paper: true
    source_confidence: definitive_paper_link
  - title: mteb/belebele
    url: https://huggingface.co/datasets/mteb/belebele
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
      ndcg_at_10: 0.3287836985
      hit_at_10: 0.38
      recall_at_100: 0.44
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.44
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9305889891
      hit_at_10: 0.985
      recall_at_100: 0.985
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.985
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.445551701
      hit_at_10: 0.52
      recall_at_100: 0.99
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.01
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
