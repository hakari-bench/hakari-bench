# NanoBEIR-en / NanoDBPedia

## Overview

DBpedia-Entity is an entity-search benchmark over DBpedia, the structured
knowledge-base view of Wikipedia. `NanoDBPedia` is the compact English NanoBEIR
retrieval task: a short keyword query or natural-language question is used to
retrieve relevant DBpedia entity descriptions. The task tests whether a retriever
can map concise entity-oriented information needs such as people, places,
events, products, occupations, lists, or factual questions to the correct
knowledge-base pages, often when many entities share overlapping names or types.

## Details

### What the Original Data Measures

[DBpedia-Entity v2: A Test Collection for Entity
Search](https://doi.org/10.1145/3077136.3080751) introduces DBpedia-Entity v2
as an updated and more consistent entity-retrieval test collection. The paper
explains that entity search became important because many web search needs are
centered on entities, and because knowledge repositories such as DBpedia provide
structured semantic information organized around those entities. The benchmark
therefore asks systems to return ranked DBpedia URIs for free-text user queries.

The paper reports that DBpedia-Entity v2 uses the English part of DBpedia
2015-10. Entities are required to have both a title and an abstract, which
filters out category, redirect, and disambiguation pages while retaining list
pages. The resulting knowledge base contains about 4.6 million entities. The
queries come from four sources with different search styles: SemSearch ES named
entity queries, INEX-LD keyword queries, ListSearch list-of-entities queries,
and QALD-2 natural-language questions answerable by DBpedia entities.

The v2 paper is also important for understanding relevance. DBpedia-Entity v1
combined judgments from several campaigns with different pools and annotation
standards. DBpedia-Entity v2 rebuilds the candidate pool from original qrels,
previous entity-search runs, new runs, and SPARQL answers for QALD-2. It then
collects relevance judgments under a uniform crowdsourcing setup, with expert
review for disagreement cases, using a graded scale: irrelevant, relevant, and
highly relevant. The official project page describes DBpedia-Entity as a
standard test collection for entity search over the DBpedia knowledge base.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes DBpedia-Entity as
one of its heterogeneous retrieval tasks. In the NanoBEIR version used here,
DBpedia entity descriptions are represented as corpus documents, and relevance
is evaluated with the Nano qrels. The retrieval target is therefore an entity
page description, not a long article passage and not an answer span.

### Observed Data Profile

The sampled Nano task has 50 queries, 6,045 documents, and 1,158 positive qrel
rows. This is strongly multi-positive: queries have an average of 23.16 positive
documents, 48 of 50 queries have more than one positive, and the maximum number
of positives for a single query is 81. This follows the source task design:
some queries seek a single named entity, but many ask for a class or list of
entities, such as Formula 1 drivers, Axis powers, professional surfers, Nordic
classical composers, or places where the British monarch is also head of state.

The queries are short, with an average length of 33.10 characters. They range
from terse ambiguous strings such as `carolina`, `nokia e73`, and `eloan line of
credit` to natural-language questions such as `In which programming language is
GIMP written?` or `Who are the parents of the wife of Juan Carlos I?`. This
means the task mixes entity lookup, entity disambiguation, list completion, and
simple knowledge-base question answering. A model cannot assume that every query
expects one best page.

The documents are compact DBpedia-style entity descriptions, averaging 336.31
characters. They usually begin with an entity name and a compressed encyclopedic
description. Positive documents may be direct entity matches, members of a
requested class, related events, or entities that answer a factual relation. For
example, a query about Formula 1 drivers who won the Monaco Grand Prix can have
Grand Prix race pages and driver pages as positives; a query about where the
British monarch is head of state can retrieve state or constitutional pages; and
a query about GIMP's programming language can retrieve `C`, `GTK+`, and related
software entities.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5619
and hit@10 = 0.9200. Because most queries have many positives, hit@10 is not
enough to describe ranking quality. A system may find one relevant entity but
still rank only a small fraction of the relevant entity set near the top. The
median first-positive rank is 1, which shows that sparse retrieval often finds
at least one relevant entity quickly, but the worst observed first-positive rank
is 100.

The inspected BM25 failures show why entity retrieval is not just lexical
matching. For `Which classis does the Millepede belong to?`, the relevant entity
is the millipede class `Diplopoda`, but BM25 retrieves unrelated pages whose text
happens to overlap with rare surface tokens. For `Which professional surfers
were born on the Philippines?`, top candidates are Filipino professional
athletes in other sports, while the positives require combining the profession
constraint with birthplace or nationality. For `In which programming language is
GIMP written?`, BM25 retrieves generic programming-language pages before the
specific positive entities `C`, `GTK+`, and `G'MIC`.

The task is easiest when the query contains a rare entity string that appears in
the right page title or abstract, such as `nokia e73` or a specific Grand Prix.
It is harder when the query expresses an entity type, an attribute constraint, a
relation, or a list intent. Strong retrieval needs entity typing, alias handling,
relation awareness, and a willingness to return many relevant entities rather
than a single exact lexical match.

### Training Data That May Help

Useful non-synthetic training data includes entity-search pairs from DBpedia,
Wikidata, Wikipedia title and abstract retrieval, knowledge-base question
answering data with entity answers, and list-completion or entity-set retrieval
data. Training should preferably exclude upstream dev/test data or other
DBpedia-Entity/BEIR-derived records that may overlap with the NanoBEIR
evaluation queries and judged entities.

Entity linking data can help with alias and surface-form matching, but it is not
identical to this task because DBpedia-Entity often requires returning a ranked
set of relevant entities for a broad information need. Data with graded or
multi-positive supervision is especially useful: a model should learn that some
queries have many valid answers, and that highly relevant direct entity answers
should outrank merely related entities.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation entity
descriptions and generate short entity-oriented search needs. Useful generated
queries should include direct name lookups, alias lookups, type-constrained
queries, attribute questions, relation questions, and list requests. Examples of
good patterns are "living Nordic classical composers", "companies founded in
Berlin", "who directed [film]", or "programming language used by [software]".

For joint document-and-question generation, create small clusters of
Wikipedia/DBpedia-style entity descriptions with shared types, aliases,
locations, dates, and relations, then generate queries whose positives are one
or more members of that cluster. The generated data should preserve the
multi-positive nature of entity retrieval. It should not reduce the task to
single-label entity classification or title lookup, because the benchmark
includes list, class, and relation-seeking queries.

## Example Data

| Query | Positive document |
| --- | --- |
| fitzgerald auto mall chambersburg pa (36 chars) | Fitzgerald Auto Malls is a family owned and operated auto dealership that was founded in 1966, with its first location opening in Bethesda, Maryland. As of 2014, Fitzgerald Auto Malls ranked number 59 on the list of the "Top ... [truncated 225 chars](429 chars) |
| 1994 short story collection Alice Munro is Open (47 chars) | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, née Laidlaw /ˈleɪdlɔː/; born 10 July 1931) is a Canadian author. Munro's work has been described as having revolutionized the architecture of short stories, especially in its tendency to ... [truncated 225 chars](499 chars) |
| gallo roman architecture in paris (33 chars) | Art in Paris is an article on the art culture and history in Paris, the capital of France. For centuries, Paris has attracted artists from around the world, arriving in the city to educate themselves and to seek inspiration f ... [truncated 225 chars](333 chars) |
| republics of the former Yugoslavia (34 chars) | The 1974 Yugoslav Constitution was the fourth and final constitution of the Socialist Federal Republic of Yugoslavia. It came into effect on February 21.With 406 original articles, the 1974 constitution was one of the longest ... [truncated 225 chars](436 chars) |
| films shot in Venice (20 chars) | A Little Romance is a 1979 American Technicolor and Panavision romantic comedy film directed by George Roy Hill and starring Laurence Olivier, Thelonious Bernard, and Diane Lane in her film debut. The screenplay was written b ... [truncated 225 chars](371 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Avg positives / query | 23.16 |
| Positives per query (min / median / max) | 1 / 18.00 / 81 |
| Queries with multiple positives | 48 (96.0%) |
| BM25 nDCG@10 | 0.6374 |
| BM25 hit@10 | 0.9400 |
| BM25 Recall@100 | 0.7168 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6243 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.7599 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6564 |
| Reranking hybrid hit@10 | 0.9200 |
| Reranking hybrid Recall@100 | 0.7746 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 33.10 |
| Document length avg chars | 336.31 |

### Public Sources

- [DBpedia-Entity v2: A Test Collection for Entity Search](https://doi.org/10.1145/3077136.3080751); 2017; Faegheh Hasibi, Fedor Nikolaev, Chenyan Xiong, Krisztian Balog, Svein Erik Bratsberg, Alexander Kotov, Jamie Callan; DOI: `10.1145/3077136.3080751`.
- [DBpedia-Entity official project page](https://iai-group.github.io/DBpedia-Entity/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity v2: A Test Collection for Entity Search | 2017 | paper | https://doi.org/10.1145/3077136.3080751 |
| DBpedia-Entity official project page |  | project page | https://iai-group.github.io/DBpedia-Entity/ |
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
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/NanoDBPedia.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 6045
    positive_qrels: 1158
  positives_per_query:
    average: 23.16
    min: 1
    median: 18.0
    max: 81
    multi_positive_queries: 48
    multi_positive_query_percent: 96.0
  text_stats_chars:
    query_mean: 33.1
    document_mean: 336.3067
  bm25:
    ndcg_at_10: 0.6373845172851081
    hit_at_10: 0.94
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream dev/test data or other DBpedia-Entity/BEIR-derived
      data likely to overlap with the NanoBEIR evaluation queries and judged entities
    useful_training_data:
    - non-overlapping DBpedia or Wikidata entity-search pairs
    - Wikipedia title and abstract retrieval data
    - knowledge-base question answering data with entity answers
    - list-completion and entity-set retrieval data
    synthetic_data:
      document_generation: DBpedia-style entity descriptions with titles, aliases,
        entity types, attributes, locations, dates, and relations
      question_generation: short entity-oriented queries including direct lookups,
        aliases, type constraints, relation questions, and list requests
      answerability: positives should be one or more entities satisfying the query,
        not merely pages sharing surface terms
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
    - label: DBpedia-Entity official project page
      url: https://iai-group.github.io/DBpedia-Entity/
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
    - no_arxiv_page_confirmed_for_original_task_paper
  references:
  - title: 'DBpedia-Entity v2: A Test Collection for Entity Search'
    url: https://doi.org/10.1145/3077136.3080751
    year: 2017
    doi: 10.1145/3077136.3080751
    is_paper: true
    source_confidence: definitive_paper_link
  - title: DBpedia-Entity official project page
    url: https://iai-group.github.io/DBpedia-Entity/
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
      ndcg_at_10: 0.6373845173
      hit_at_10: 0.94
      recall_at_100: 0.7167530225
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7167530225
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6243012778
      hit_at_10: 0.96
      recall_at_100: 0.7599309154
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7599309154
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6563665569
      hit_at_10: 0.92
      recall_at_100: 0.774611399
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.774611399
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
