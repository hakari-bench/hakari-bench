# NanoBEIR-en / NanoHotpotQA

## Overview

HotpotQA is a multi-hop question answering benchmark built from Wikipedia.
`NanoHotpotQA` is the compact English NanoBEIR retrieval task: each query is a
question whose answer depends on evidence from two Wikipedia pages, and the
system must retrieve both supporting documents. The task tests bridge-entity
and comparison-style retrieval, where finding one relevant page is often not
enough because the question is designed to require connecting facts across
multiple pages.

## Details

### What the Original Data Measures

[HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question
Answering](https://arxiv.org/abs/1809.09600) introduces HotpotQA as a
Wikipedia-based QA dataset designed to require reasoning over multiple
supporting documents. The paper reports 113K question-answer pairs and
emphasizes four properties: questions require multiple documents, are diverse
and not constrained by a fixed knowledge-base schema, include sentence-level
supporting facts, and include comparison questions that test whether systems can
extract and compare facts across entities.

The paper's data collection pipeline uses the Wikipedia hyperlink graph to
construct bridge questions. Crowd workers see paragraph pairs connected through
a bridge entity and write questions requiring both paragraphs. The paper also
adds comparison questions by sampling two similar entities from curated lists,
then asking workers to write questions that compare shared properties. This
design is directly relevant for retrieval: the system must often find both a
bridge page and a target page, or both compared entity pages, before an answer
can be produced.

HotpotQA was created partly because earlier QA datasets often allowed
single-paragraph matching and did not provide strong supervision for the
reasoning path. HotpotQA's supporting facts make the evidence path explicit.
[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes HotpotQA as a
question-answering retrieval task, where the retriever is evaluated on whether
it can surface the supporting Wikipedia documents.

### Observed Data Profile

The sampled Nano task has 50 queries, 5,090 documents, and 100 positive qrel
rows. Every query has exactly two positive documents. This is a strong signal:
unlike single-answer passage retrieval, the intended retrieval unit is a pair of
supporting pages. The average query length is 88.34 characters, and the average
document length is 349.63 characters.

The queries are longer and more compositional than typical factoid questions.
Examples include `Alice David is the voice of Lara Croft in a video game
developed by which company ?`, `Who was born first Doug Liman or Saul
Metzstein?`, and `Do Czeslaw Milosz and Nathalie Sarraute have the same
nationality?`. Many questions mention two entities, a work and a person, or a
relation that must be resolved through another page.

The documents are short Wikipedia entity descriptions. Positives often form an
explicit reasoning chain: one page identifies the intermediate entity, and the
other page supplies the requested attribute. For comparison questions, both
positive pages describe the entities being compared, such as two people whose
birth dates or nationalities must be compared. This makes the task a retrieval
problem for explainable multi-hop QA rather than ordinary answer passage search.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8176
and hit@10 = 1.0000. BM25 finds at least one positive in the top 10 for every
query, and 43 of 50 queries have a positive ranked first. However, because every
query has two positives, the more important question is whether both supporting
documents are ranked high. A model that retrieves only the most lexically
obvious page can still fail the evidence-pair objective.

The inspected rankings show the main difficulty. For `What occupations do both
Ian Hunter and Rob Thomas have?`, BM25 first retrieves Ian Hunter songs and
other Ian Hunter pages before the two singer-songwriter biographies. For `Who
was the head promotor of the singer of "For The Good Times"?`, lexical overlap
with the song title retrieves unrelated albums and singers before the evidence
chain involving Kris Kristofferson and the relevant festival/promoter page. For
comparison questions, BM25 often finds one entity page quickly but may place the
other entity page lower.

The task is therefore lexically approachable but structurally demanding. Strong
retrieval needs to identify all required entities, not just the first salient
title. It also needs to understand bridge clues, shared attributes, and
comparison framing so that both evidence pages are available to a downstream QA
or reasoning model.

### Training Data That May Help

Useful non-synthetic training data includes HotpotQA training examples with
supporting facts, other multi-hop QA retrieval datasets, Wikipedia hyperlink
graph retrieval pairs, and question-to-supporting-document supervision where
each query has multiple positives. Single-hop QA retrieval data can help with
entity matching, but it does not fully teach the model to retrieve a complete
evidence set.

Training should preferably exclude upstream dev/test data, BEIR-derived
evaluation records, and HotpotQA examples likely to overlap with the NanoBEIR
evaluation questions or supporting pages. Multi-positive training objectives
are especially appropriate because every query in this Nano sample has two
positives.

### Synthetic Data Guidance

For document-to-question generation, start from pairs of non-evaluation
Wikipedia passages connected by a hyperlink or shared entity type, then generate
questions that require both passages. Bridge questions should require resolving
an intermediate entity before asking for an attribute. Comparison questions
should ask which entity has a larger value, earlier date, same nationality,
shared occupation, or similar property.

For joint document-and-question generation, create paired entity descriptions
with explicit links, dates, locations, occupations, creators, or membership
relations, then write questions whose positives are both documents. The
synthetic data should preserve the requirement that both passages are needed;
questions answerable from one passage alone are less useful for this benchmark.

## Example Data

| Query | Positive document |
| --- | --- |
| Penny Rae Bridges starred in a television sitcom with what other actor? (71 chars) | Penny Rae Bridges (born July 29, 1990) is an American actress. Her television work has included roles in "For Your Love", "Family Law", "Boy Meets World" and "The Parent 'Hood". She is best known for her role in "Half & Half" ... [truncated 225 chars](245 chars) |
| Who bestowed Kaganoi Shigemochi with a blade made by the person that founded the Muramasa school? (97 chars) | Kaganoi Shigemochi (加賀井 重望 , 1561 – August 27, 1600) was a Japanese samurai of the Azuchi-Momoyama period, who served the Oda clan. He ruled Kaganoi Castle. During the Battle of Komaki and Nagakute, Shigemochi fought under hi ... [truncated 225 chars](575 chars) |
| What film was written and directed by Joby Harold with music written by Samuel Sim? (83 chars) | Samuel Sim is a film and television composer. He first gained recognition with his award winning score for the BBC drama series "Dunkirk". Since then he has written the music for a wide variety of film and television producti ... [truncated 225 chars](502 chars) |
| What is the date played of this college football game at Sun Life Stadium in Miami Gardens, Florida, where Clemson defeated the No. 4 Oklahoma Sooners, 37-17? (158 chars) | The 2015 Clemson Tigers football team represented Clemson University in the 2015 NCAA Division I FBS football season. The Tigers were led by head coach Dabo Swinney in his seventh full year and eighth overall since taking ove ... [truncated 225 chars](1019 chars) |
| Devil's Food is a singles compilation by an American rock and roll band that has also been known to play country shows under what? (130 chars) | Devil's Food is a singles compilation by the American rock and roll band Supersuckers, released in April 2005 on Mid-Fi records. (128 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Task / split | NanoHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,090 |
| Positive qrels | 100 |
| Avg positives / query | 2.00 |
| Positives per query (min / median / max) | 2 / 2.00 / 2 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.8270 |
| BM25 hit@10 | 1.0000 |
| BM25 Recall@100 | 0.9600 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8043 |
| Dense hit@10 | 0.9400 |
| Dense Recall@100 | 0.9100 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8325 |
| Reranking hybrid hit@10 | 0.9600 |
| Reranking hybrid Recall@100 | 0.9700 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 88.34 |
| Document length avg chars | 349.63 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600); 2018; Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, Christopher D. Manning; DOI: `10.18653/v1/D18-1259`.
- [HotpotQA official site](https://hotpotqa.github.io/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | paper | https://arxiv.org/abs/1809.09600 |
| HotpotQA official site |  | project page | https://hotpotqa.github.io/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBEIR-en
  backing_dataset: NanoBEIR-en
  dataset_id: hakari-bench/NanoBEIR-en
  task_name: NanoHotpotQA
  split_name: NanoHotpotQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/NanoHotpotQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5090
    positive_qrels: 100
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 88.34
    document_mean: 349.634971
  bm25:
    ndcg_at_10: 0.8270114821048032
    hit_at_10: 1.0
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream dev/test data or other HotpotQA/BEIR-derived
      records likely to overlap with the NanoBEIR evaluation questions and supporting
      pages
    useful_training_data:
    - non-overlapping HotpotQA training examples with supporting facts
    - multi-hop QA retrieval datasets
    - Wikipedia hyperlink graph retrieval pairs
    - question-to-multiple-supporting-document supervision
    synthetic_data:
      document_generation: paired Wikipedia-style entity passages connected by hyperlinks,
        shared types, dates, locations, occupations, creators, or memberships
      question_generation: bridge and comparison questions that require both generated
        passages
      answerability: positives should be both documents needed for the reasoning path,
        not a single answer-bearing passage
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
    - label: HotpotQA official site
      url: https://hotpotqa.github.io/
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes: []
  references:
  - title: 'HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering'
    url: https://arxiv.org/abs/1809.09600
    year: 2018
    doi: 10.18653/v1/D18-1259
    is_paper: true
    source_confidence: definitive_paper_link
  - title: HotpotQA official site
    url: https://hotpotqa.github.io/
    year: null
    doi: null
    is_paper: false
    source_confidence: definitive_project_page
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8270114821
      hit_at_10: 1.0
      recall_at_100: 0.96
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8042763454
      hit_at_10: 0.94
      recall_at_100: 0.91
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.91
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8325190637
      hit_at_10: 0.96
      recall_at_100: 0.97
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
