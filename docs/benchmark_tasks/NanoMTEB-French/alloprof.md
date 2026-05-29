# NanoMTEB-French / alloprof

## Overview

`alloprof` is a French educational retrieval task built from Alloprof, a
Quebec educational help resource. Queries are student questions in French, and
documents are long educational explanations. The retriever must find the lesson
or resource that answers the student's school-subject question.

## Details

### What the Original Data Measures

[MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468)
includes AlloprofRetrieval as one of the French retrieval tasks and describes
Alloprof as an existing French dataset used to evaluate retrieval and reranking.
The Nano metadata identifies the source as Alloprof, an organization in Quebec
that provides teacher-curated resources and a help forum for primary and
secondary school students.

No standalone Alloprof retrieval paper was confirmed in this pass. The
interpretation below is based on MTEB-French, the public dataset cards, and the
observed Nano examples.

### Observed Data Profile

The Nano split has 200 French queries, 2,556 documents, and 200 positive qrels.
Every query has one positive. Queries average 179.23 characters, but the range
is wide: some are short concept questions, while others are long student forum
messages with spelling errors and context. Documents average 3,504.53
characters and are explanatory lessons.

The sampled data covers Quebec history, conclusion writing, modalization,
probability, and algebraic expressions. Documents often include pedagogical
definitions, examples, and formulas, so the task rewards school-domain
question-to-resource retrieval rather than generic web search.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3390 and hit@10 = 0.4750. The median best rank is 13.5. Lexical matching
works for distinctive terms such as `Maurice Duplessis` or `probabilité`, but
long informal student questions often include noise that dilutes the core
information need.

### Training Data That May Help

Useful training data includes non-overlapping French educational forum
questions, lesson-resource retrieval pairs, and school-subject QA in Quebec or
general French. Training should exclude Alloprof test examples, Nano queries,
qrels, and positive lesson documents likely to overlap with this evaluation.

### Synthetic Data Guidance

Generate French student questions with realistic spelling variation,
politeness, partial attempts, and school-subject vocabulary. Pair them with
lesson-style documents covering mathematics, grammar, history, science, and
writing. Do not use Nano evaluation questions or positives as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Bonjour, j'ai de la difficulté à comprendre les différences entre le simple past et le past progressive. Avez-vous des trucs pour savoir quand les utiliser svp? MERCI!!! (169 chars) | Was he playing soccer when his mom arrived? They were watching a movie while their parents were preparing dinner. The past continuous is used to describe two types of actions happening in the past. One action that was happeni ... [truncated 225 chars](768 chars) |
| Bonjour! Je suis en 5e année du primaire et je voudrais des trucs pour mémoriser les fractions irréductible et équivalente. ps: Y a t'il des jeux ou des exercises dans alloprof pour m'aider?? Merci Chevalmagnifique2012 (218 chars) | Les fractions équivalentes sont des fractions qui représentent le même nombre, la même proportion. Pour passer d'une fraction à une autre fraction équivalente, on peut multiplier ou diviser cette fraction par une fraction-uni ... [truncated 225 chars](3529 chars) |
| bonjour, on comence a voir les cirquit électrique en science. ma question sais a quoi serve les Résisteur. (106 chars) | La résistance électrique est une propriété physique d'un matériau qui limite le passage du courant électrique dans un circuit. Les composantes qui possèdent cette propriété servent à limiter le passage des électrons dans un c ... [truncated 225 chars](2507 chars) |
| bonjour, l'eau est un PH7, alors le papier tournesol rouge et bleu ne réagient pas? merci (89 chars) | Il existe quatre façons de déterminer la nature d'une substance. Le papier tournesol est imbibé de teinture de tournesol ou d'extrait de poudre de lichen. Il sert d'indicateur coloré pour déterminer la nature acide, basique o ... [truncated 225 chars](4326 chars) |
| C'est quoi une somme (20 chars) | L'addition est une opération qui consiste à ajouter un nombre (ou plusieurs nombres) à un autre nombre. Les nombres qui composent l'addition se nomment les termes. La somme désigne le résultat de cette opération. Les mots sui ... [truncated 225 chars](774 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Task / split | alloprof |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Language | fr |
| Category | natural_language |
| Queries | 200 |
| Documents | 2556 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3447 |
| BM25 hit@10 | 0.4850 |
| BM25 Recall@100 | 0.7900 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5139 |
| Dense hit@10 | 0.6750 |
| Dense Recall@100 | 0.8950 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5214 |
| Reranking hybrid hit@10 | 0.7000 |
| Reranking hybrid Recall@100 | 0.9150 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 17 |
| Query length avg chars | 179.23 |
| Document length avg chars | 3504.53 |

### Public Sources

- [MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468); 2024; Mathieu Ciancone et al.
- [mteb/AlloprofRetrieval dataset card](https://huggingface.co/datasets/mteb/AlloprofRetrieval).
- [antoinelb7/alloprof dataset card](https://huggingface.co/datasets/antoinelb7/alloprof).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French)
- Source dataset: [mteb/AlloprofRetrieval](https://huggingface.co/datasets/mteb/AlloprofRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis | 2024 | arXiv paper | https://arxiv.org/abs/2405.20468 |
| mteb/AlloprofRetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/AlloprofRetrieval |
| antoinelb7/alloprof | 2025 | dataset card | https://huggingface.co/datasets/antoinelb7/alloprof |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-French
  backing_dataset: NanoMTEB-French
  dataset_id: hakari-bench/NanoMTEB-French
  task_name: alloprof
  split_name: alloprof
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/alloprof.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Alloprof retrieval paper was confirmed in this pass;
      interpretation uses MTEB-French, dataset cards, and observed data
  counts:
    queries: 200
    documents: 2556
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 179.23
    document_mean: 3504.527386541471
  bm25:
    ndcg_at_10: 0.3446844140578008
    hit_at_10: 0.485
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Alloprof test examples, Nano queries, qrels, and positive
      lesson documents likely to overlap with this evaluation
    useful_training_data:
    - French educational forum question-resource pairs
    - Quebec school-subject QA and lesson retrieval data
    - French pedagogical explanations with student questions
    - hard negatives from the same school subject
    synthetic_data:
      document_generation: French lesson-style documents for mathematics, grammar,
        history, science, and writing
      question_generation: French student questions with realistic spelling variation,
        partial attempts, and school vocabulary
      answerability: each positive lesson should directly explain the concept or procedure
        needed by the student
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-French
    source_urls:
    - label: MTEB-French arXiv
      url: https://arxiv.org/abs/2405.20468
    - label: mteb/AlloprofRetrieval
      url: https://huggingface.co/datasets/mteb/AlloprofRetrieval
    - label: antoinelb7/alloprof
      url: https://huggingface.co/datasets/antoinelb7/alloprof
    source_notes: []
  references:
  - title: 'MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis'
    url: https://arxiv.org/abs/2405.20468
    year: 2024
    doi: 10.48550/arXiv.2405.20468
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3446844141
      hit_at_10: 0.485
      recall_at_100: 0.79
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.79
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5138589735
      hit_at_10: 0.675
      recall_at_100: 0.895
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.895
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5214433188
      hit_at_10: 0.7
      recall_at_100: 0.915
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.085
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.915
      safeguard_positive_rows: 17
      rows_with_101_candidates: 17
```
