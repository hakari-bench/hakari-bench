# NanoR2MED / NanoR2MEDBiology

## Overview

`NanoR2MEDBiology` is an English Q&A reference retrieval task from R2MED. Queries
are Biology StackExchange questions, and relevant documents are web or
Wikipedia-derived passages that support the accepted answer. The task evaluates
whether retrieval models can connect a natural-language biology question to the
right explanatory resource, even when the useful document is linked through an
implicit biological concept rather than repeated query wording.

## Details

### What the Original Data Measures

[R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558)
defines R2MED relevance as support for a latent reasoning answer connecting the
query to its relevant documents. Biology is part of the Q&A reference retrieval
task, where StackExchange posts are queries and cited external webpages from
answers serve as answer-supporting evidence.

The R2MED paper states that the Biology dataset is adopted from BRIGHT, while
the Bioinformatics and Medical Sciences Q&A datasets are newly built from
StackExchange communities. It then applies the same R2MED mining and assessment
pipeline: retrieve candidate documents from query, answer, and reasoning-path
views; score candidates for answer relevance and reasoning support; discard
ambiguous middle-score cases; and use expert review to improve clinical and
factual validity.

### Observed Data Profile

The Nano split has 103 queries, 10,000 documents, and 374 positive qrel rows.
Queries average 523.03 characters and often include a short biological puzzle
with a few clarifying sentences. Documents average 474.07 characters, but some
positive passages are much longer Wikipedia-derived sections.

Each query has 3.63 positives on average, with a median of 3 and a maximum of
19 positives. Sampled queries ask about long-lived proteins, kissing as a human
behavior, plant photosynthesis under monitor light, immune recognition of
tumors, and bacteriophage therapy. This makes the task broader than clinical
evidence retrieval: the model must map everyday or conceptual biology questions
to precise biological mechanisms, taxa, molecules, or evolutionary hypotheses.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2513
and hit@10 = 0.5049. It ranks 27 positives first and finds at least one positive
inside the top 10 for 52 of 103 queries. This is the strongest sparse baseline
among the Q&A reference splits inspected here, helped by clear entity terms such
as chlorophyll, phage, and kissing.

The failures are still instructive. For a nasal-cycle question, BM25 retrieves
unrelated bird-feeding text before the nasal-cycle page; for an RGB-smell
analogy, it retrieves color afterimage material before olfactory receptors; and
for a lifespan/evolution question, it retrieves vitamin C and diet passages
before antagonistic pleiotropy. The hard cases require concept selection rather
than keyword matching.

### Training Data That May Help

Useful training data includes non-overlapping Biology StackExchange answer-link
pairs, BRIGHT reasoning-intensive biology retrieval, biological concept QA,
Wikipedia section retrieval, and scientific explanation pairs with hard negatives
from adjacent concepts. Multi-positive retrieval objectives are appropriate
because most queries have more than one relevant passage.

Training should exclude the R2MED Biology evaluation posts and positive
documents. When using BRIGHT or StackExchange data, check for overlap with the
same questions, linked pages, and answer-derived passages.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation biology encyclopedia
sections, educational pages, or scientific explanations, then generate natural
questions that require identifying the concept, mechanism, organism, or
evolutionary explanation in the passage.

For joint generation, create answer-bearing biology passages and StackExchange
style questions with clarifying context and plausible misconceptions. Hard
negatives should share the same broad domain but contain a different mechanism
or entity. Do not use Nano evaluation queries or positives as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the longest-lasting protein in a human body? Protein life times are, on average, not particularly long, on a human life timescale. I was wondering, how old is the oldest protein in a human body? Just to clarify, I mea ... [truncated 225 chars](1199 chars) | Characteristics[edit] Elastin is a very long-lived protein, with a half-life of over 78 years in humans. (104 chars) |
| Is kissing a natural human activity? The word natural here is meant in contrast to it being a sociological construct. Is kissing in all its forms something natural for humans? Is it instinctively erotic? Or is it just a conve ... [truncated 225 chars](435 chars) | Biology and evolution[edit] Black-tailed prairie dogs "kissing." Prairie dogs use a nuzzle of this variety to greet their relatives. Within the natural world of other animals, there are numerous analogies to kissing, notes Cr ... [truncated 225 chars](3310 chars) |
| What types of light can't a plant photosynthesize in? I have a plant on my desk, and it got me to wondering: Can my plant use the light from my monitors to photosynthesize? If so, what light (apart from green light, to a degr ... [truncated 225 chars](509 chars) | Chlorophyll is any of several related green pigments found in cyanobacteria and in the chloroplasts of algae and plants. Its name is derived from the Greek words χλωρός, khloros ("pale green") and φύλλον, phyllon ("leaf"). Ch ... [truncated 225 chars](712 chars) |
| If Tumors have lots of mutations in them how is it the immune system can't detect them? If a cancerous tumor has a lot of mutations in them why can't the immune system detect them? If a person has cancer could this somehow al ... [truncated 225 chars](425 chars) | Antigen processing and presentation[edit] MHC class I pathway: Proteins in the cytosol are degraded by the proteasome, liberating peptides internalized by TAP channel in the endoplasmic reticulum, there associating with MHC-I ... [truncated 225 chars](3162 chars) |
| Could viruses be used as antibiotics? Could we use viruses that only affect bacteria to act as antibiotics? The more bacteria, the more times the virus divides, so the stronger it gets. Is this practical? (204 chars) | Applications[edit] Collection[edit] Phages for therapeutic use can be collected from environmental sources that likely contain high quantities of bacteria and bacteriophages, such as effluent outlets, sewage, or even soil. Th ... [truncated 225 chars](7339 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoR2MED |
| Backing dataset | NanoR2MED |
| Task / split | NanoR2MEDBiology |
| Hugging Face dataset | [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED) |
| Language | en |
| Category | natural_language |
| Queries | 103 |
| Documents | 10,000 |
| Positive qrels | 374 |
| Avg positives / query | 3.63 |
| Positives per query (min / median / max) | 1 / 3 / 19 |
| Queries with multiple positives | 93 (90.29%) |
| BM25 nDCG@10 | 0.3455 |
| BM25 hit@10 | 0.5922 |
| BM25 Recall@100 | 0.6818 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4953 |
| Dense hit@10 | 0.7573 |
| Dense Recall@100 | 0.8369 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4722 |
| Reranking hybrid hit@10 | 0.7864 |
| Reranking hybrid Recall@100 | 0.8503 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 523.03 |
| Document length avg chars | 474.07 |

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558); 2025; Xiangxu Zhang, Lei Li, Xiao Zhou, and Zheng Liu; DOI: `10.48550/arXiv.2505.14558`.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/Biology dataset card](https://huggingface.co/datasets/R2MED/Biology).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED)
- Source dataset: [R2MED/Biology](https://huggingface.co/datasets/R2MED/Biology)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/Biology | 2025 | dataset card | https://huggingface.co/datasets/R2MED/Biology |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoR2MED
  backing_dataset: NanoR2MED
  dataset_id: hakari-bench/NanoR2MED
  task_name: NanoR2MEDBiology
  split_name: NanoR2MEDBiology
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDBiology.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2505.14558
    additional_source_urls:
    - https://r2med.github.io/
    - https://github.com/R2MED/R2MED
    - https://huggingface.co/datasets/R2MED/Biology
  counts:
    queries: 103
    documents: 10000
    positive_qrels: 374
  positives_per_query:
    average: 3.6310679612
    min: 1
    median: 3.0
    max: 19
    multi_positive_queries: 93
    multi_positive_query_percent: 90.29
  text_stats_chars:
    query_mean: 523.029126
    document_mean: 474.0668
  bm25:
    ndcg_at_10: 0.3454997187149365
    hit_at_10: 0.5922330097087378
    source: dataset_candidate_subset
  learning:
    original_train_split: not_found
    evaluation_split_origin: R2MED benchmark release sampled into NanoR2MED
    train_eval_overlap_audit: not_audited
    leakage_note: exclude R2MED Biology evaluation queries, qrels, and positive passages;
      audit BRIGHT overlap before training
    useful_training_data:
    - non-overlapping Biology StackExchange answer-link retrieval
    - BRIGHT reasoning-intensive biology retrieval data without overlap
    - biological concept QA and Wikipedia section retrieval
    - hard negatives from adjacent biological mechanisms or taxa
    synthetic_data:
      document_generation: non-evaluation biology encyclopedia sections and scientific
        explanation passages
      question_generation: StackExchange-style questions that require identifying
        a mechanism, organism, molecule, or evolutionary explanation
      hard_negatives: same broad biology topic with a different mechanism or entity
      answerability: the passage should explicitly support the biological concept
        needed to answer the question
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoR2MED
    source_urls:
    - label: R2MED arXiv
      url: https://arxiv.org/abs/2505.14558
    - label: R2MED project page
      url: https://r2med.github.io/
    - label: R2MED GitHub
      url: https://github.com/R2MED/R2MED
    - label: R2MED/Biology
      url: https://huggingface.co/datasets/R2MED/Biology
    source_notes: []
  references:
  - title: 'R2MED: A Benchmark for Reasoning-Driven Medical Retrieval'
    url: https://arxiv.org/abs/2505.14558
    year: 2025
    doi: 10.48550/arXiv.2505.14558
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3454997187
      hit_at_10: 0.5922330097
      recall_at_100: 0.6818181818
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6818181818
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4953205757
      hit_at_10: 0.7572815534
      recall_at_100: 0.8368983957
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8368983957
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4721590891
      hit_at_10: 0.786407767
      recall_at_100: 0.8502673797
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.029126
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8502673797
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
