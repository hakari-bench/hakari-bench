# NanoBEIR-en / NanoArguAna

## Overview

ArguAna is an argument retrieval dataset where the query is a debate argument
and the relevant document is its best counterargument. `NanoArguAna` is the
compact English NanoBEIR version of this task. Queries and documents are long
argumentative passages from debate topics, and the retrieval target is not a
similar supporting passage but a stance-opposed response that addresses the same
aspects. The task tests argument understanding, stance opposition, and
counterargument matching.

## Details

### What the Original Data Measures

[Retrieval of the Best Counterargument without Prior Topic
Knowledge](https://aclanthology.org/P18-1023/) frames counterargument retrieval
as finding the best opposing argument for an input argument on an arbitrary
controversial topic. The paper hypothesizes that a strong counterargument should
invoke the same aspects as the original argument while taking the opposite
stance. It therefore models both similarity and dissimilarity between an
argument's premises and conclusion and a candidate counterargument.

The paper reports a corpus of 6,753 argument-counterargument pairs from 1,069
debates on idebate.org, plus false pairs derived from them. It evaluates several
retrieval settings, including ranking among opposing-stance candidates and among
all test arguments. This matters for BEIR/NanoBEIR because the task is designed
to be difficult for simple semantic similarity: the positive is related but
opposed. A retriever that returns a near-duplicate support argument is wrong if
it does not counter the query's claim.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes ArguAna as an
Argument Retrieval task and reports unusually long queries and documents
compared with most BEIR datasets. The NanoBEIR version keeps that long-form
debate structure.

### Observed Data Profile

The sampled Nano task has 50 queries, 3,635 documents, and 50 positive qrel rows.
Every query has exactly one positive counterargument. Queries are long, with an
average length of 1,201.78 characters; documents average 1,011.79 characters.
Most entries have an argument title followed by several sentences of evidence,
examples, citations, and normative claims.

The sample covers politics, education, culture, health, economy, international
relations, sport, religion, free speech, and science. The positive document is
often a direct `...a` to `...b` counterargument pair under the same debate ID.
For example, an argument that a UN standing army would be more effective is
paired with a counterargument that a multinational standing army would still
suffer from language, culture, and impartiality problems. An argument that
better nutrition improves student performance is paired with a counterargument
that incentives and subsidies, rather than coercive school-meal policy, are the
better government role.

The core retrieval problem is stance-aware topical matching. A positive usually
shares the topic and many concepts with the query, but it must attack a premise,
conclusion, expected consequence, feasibility assumption, or policy framing. This
is different from duplicate-question, QA, or fact-checking retrieval because the
right document may explicitly contradict the query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4462
and hit@10 = 0.7400. BM25 ranks 8 positives first, and 37 of 50 positives are in
the top 10. The median positive rank is 3.5. This looks strong, but the ranking
is helped by the original paired IDs and shared debate vocabulary: many
counterarguments repeat the same policy names, entities, and claims.

The harder cases reveal the stance problem. For the copyright-monitoring query,
BM25 ranks the query itself first and other same-side copyright arguments above
the positive counterargument at rank 14. For a free-speech bargaining-chip
argument, BM25 retrieves nearby free-speech or sanctions arguments while the
direct counterargument is rank 39. For a health-policy nutrition argument, BM25
finds school-performance and obesity-tax passages before the positive response
at rank 21. These are not topic failures; they are failures to rank the actual
opposing move.

Because each query has one positive, hit@10 is easy to interpret, but nDCG@10
still matters because a usable counterargument retrieval system should place the
direct response near the top. Strong models should combine long-passage topic
matching with explicit stance and attack-relation awareness.

### Training Data That May Help

Helpful training data includes non-overlapping argument-counterargument pairs,
debate portals with pro/con responses, argument attack/support relation
datasets, stance-classified arguments, and hard negatives from same-topic
same-stance arguments. The original ArguAna training material or idebate-derived
records should be audited for overlap before use with this benchmark. Upstream
test pairs and Nano evaluation arguments should not be used for training.

Generic semantic-similarity data can be actively harmful if it teaches the model
to rank supporting or duplicate arguments above counterarguments. Training should
include positives that oppose the query and negatives that are topical but do
not provide a counterargument.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation debate arguments and
generate opposing arguments that attack a premise, consequence, value judgment,
or feasibility claim while staying on the same topic. Synthetic data should
include pro/con pairs, same-topic same-stance hard negatives, and off-topic
arguments.

For joint generation, create debate topics with several long arguments on both
sides, then label the best counterargument for each query. Generated texts should
preserve argumentative structure: claim, premise, evidence, warrant, and policy
implication. Do not seed generation with Nano evaluation arguments or positives.

## Example Data

| Query | Positive document |
| --- | --- |
| The public is apathetic to reform. Whether or not reform of the House of Lords should be a top priority in the current economic climate is debateable, let alone whether or not a coalition government would be able to initiate ... [truncated 225 chars](799 chars) | The AV campaign cannot be compared to reform to the House of Lords, furthermore one should not mistake a misinformed public due to political spin, with apathy. Often voters express that they are apathetic because they feel th ... [truncated 225 chars](408 chars) |
| The expansion of Heathrow is vital for the economy Expanding Heathrow would ensure many current jobs as well as creating new ones. Currently, Heathrow supports around 250,000 jobs. [1] Added to this many hundreds of thousands ... [truncated 225 chars](1421 chars) | The business community is far from united in its supposed support of a third run-way. Surveys suggest that many influential businesses in fact do not support expansion. A letter expressing concern was signed by Justin King th ... [truncated 225 chars](1330 chars) |
| People are given too much choice, which makes them less happy. Advertising leads to many people being overwhelmed by the endless need to decide between competing demands on their attention – this is known as the tyranny of ch ... [truncated 225 chars](1031 chars) | People are unhappy because they can't have everything, not because they are given too much choice and find it stressful. In fact, advertisements play a crucial role in ensuring that what money people have, they spend on the m ... [truncated 225 chars](912 chars) |
| Cyber attacks are often carried out by non-state actors Cyber attacks are often carried out by non-state actors, such as cyberterrorists or hacktivists (social activists who hack), without any involvement of the actual state. ... [truncated 225 chars](1038 chars) | In case of non-state actors attack, many practitioners in international law agree that the state can still retaliate in self-defence if another state is 'unwilling or unable to take effective action' to deal with attacks comi ... [truncated 225 chars](547 chars) |
| Because religion promotes certainty of belief, divinely inspired hatred is easy to use to justify and promote violent actions and discriminatory practices. Free speech must come second when there is the potential for that spe ... [truncated 225 chars](1355 chars) | Nobody is being forced to perform acts of violence by the words of another; it is their choice to do so. Equally, there are plenty of people who would hold views that could be considered homophobic but would be appalled by ac ... [truncated 225 chars](636 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.4650 |
| BM25 hit@10 | 0.7600 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5787 |
| Dense hit@10 | 0.9200 |
| Dense Recall@100 | 0.9400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5422 |
| Reranking hybrid hit@10 | 0.8800 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 1,201.78 |
| Document length avg chars | 1,011.79 |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/); 2018; Henning Wachsmuth, Shahbaz Syed, Benno Stein; DOI: `10.18653/v1/P18-1023`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych.
- [ir_datasets BEIR documentation](https://ir-datasets.com/beir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- Source dataset: [mteb/arguana](https://huggingface.co/datasets/mteb/arguana)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | paper | https://aclanthology.org/P18-1023/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| mteb/arguana |  | dataset card | https://huggingface.co/datasets/mteb/arguana |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBEIR-en
  backing_dataset: NanoBEIR-en
  dataset_id: hakari-bench/NanoBEIR-en
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/NanoArguAna.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3635
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1201.78
    document_mean: 1011.791472
  bm25:
    ndcg_at_10: 0.4649518806085047
    hit_at_10: 0.76
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream ArguAna/idebate test pairs and Nano evaluation
      argument-counterargument pairs from training data
    useful_training_data:
    - non-overlapping argument-counterargument pairs
    - debate portal pro/con response pairs
    - argument attack and support relation datasets
    - stance-classified arguments with same-topic hard negatives
    synthetic_data:
      document_generation: long debate-style arguments with claims, premises, evidence,
        and policy implications
      question_generation: opposing counterarguments that address the same aspects
        while taking the opposite stance
      answerability: positives should counter the query argument, not merely support
        or paraphrase it
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
    - label: ArguAna paper
      url: https://aclanthology.org/P18-1023/
    - label: mteb/arguana
      url: https://huggingface.co/datasets/mteb/arguana
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes: []
  references:
  - title: Retrieval of the Best Counterargument without Prior Topic Knowledge
    url: https://aclanthology.org/P18-1023/
    year: 2018
    doi: 10.18653/v1/P18-1023
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4649518806
      hit_at_10: 0.76
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5787095438
      hit_at_10: 0.92
      recall_at_100: 0.94
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5422482284
      hit_at_10: 0.88
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
