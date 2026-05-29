# NanoBRIGHT / NanoBrightStackoverflowLong

## Overview

`NanoBrightStackoverflowLong` is the long-document version of the Stack Overflow
BRIGHT task. Queries are developer questions with code or configuration context,
and relevant documents are full cited source pages such as MDN, Microsoft Learn,
RFC-style specifications, or technical reference pages.

## Details

### What the Original Data Measures

[BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883)
converts StackExchange tasks to long-context retrieval by using complete web
pages rather than split passages. The paper notes that this creates a smaller
document pool but much longer documents, and that long-context reasoning remains
difficult even with fewer candidates. For Stack Overflow, the retriever must
identify the full source page that explains the relevant API, language behavior,
or platform feature.

### Observed Data Profile

The split has 117 queries, 1,846 documents, and 129 positive qrels. Queries
average 1292.97 characters and include JavaScript, iCalendar, WebView2, .NET,
and C# examples. Documents average 77,578.44 characters, with some very large
reference pages. Most queries have one positive full document; 12 queries have
two positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3084 and hit@10 = 0.5214. It ranks 16 queries with a positive first, and the
median best positive rank is 8. Exact API names and specification terms can help
BM25, but long pages contain large amounts of boilerplate and unrelated
reference material.

### Training Data That May Help

Useful data includes document-level API documentation retrieval, Stack Overflow
questions with cited links, issue-to-doc pairs, and long technical-reference QA.
Avoid training on the exact posts and full cited documents in this Nano split.

### Synthetic Data Guidance

Generate developer questions with concrete code and environment context, then
pair them with full documentation pages where a specific section explains the
behavior. Hard negatives should be long pages from the same platform or API
family that do not resolve the issue.

## Example Data

| Query | Positive document |
| --- | --- |
| Sort tbody list which is populated with Javascript getList? I have a router with a DHCP page which is not sorted by the internal IP number, instead it is fully random. I have full access to the html and javascript, and I can ... [truncated 225 chars](12432 chars) | * Skip to main content * Skip to search * Skip to select language [ MDN Web Docs ](/en-US/) Open main menu * References [ References ](/en-US/docs/Web) * [ Overview / Web Technology Web technology reference for developers ](/ ... [truncated 225 chars](951658 chars) |
| Copy and delete files from SFTP folder I have to pick (remove) the files with file mask `FileName_A_*` and `FileName_B_*` from SFTP location and place them in an sharedrive. I tried using WinSCP. I have created an `HourlyFile ... [truncated 225 chars](1125 chars) | Menu Toggle search [ ![](https://winscp- static-746341.c.cdn77.org/assets/images/logos/logo.png?v=7032) WinSCP Free SFTP, SCP, S3 and FTP client for Windows ](https://winscp.net/) * [ Home ](/eng/index.php) * [ News ](/eng/ne ... [truncated 225 chars](190917 chars) |
| DAX RLS Function using LOOKUPVALUE Parsing but not working I have a table that I'm trying to implement RLS on using a secondary table with a structure below: EmployeeTable ``` EmployeeID EmployeeEmail 1 1234@email.com 2 4567@ ... [truncated 225 chars](1525 chars) | Skip to main content This browser is no longer supported. Upgrade to Microsoft Edge to take advantage of the latest features, security updates, and technical support. [ Download Microsoft Edge ](https://go.microsoft.com/fwlin ... [truncated 225 chars](42606 chars) |
| How can I get LLM to only respond in JSON strings? This is how I am defining the executor ``` const executor = await initializeAgentExecutorWithOptions(tools, model, { agentType: 'chat-conversational-react-description', verbo ... [truncated 225 chars](1063 chars) | Text generation models OpenAI's text generation models (often called generative pre-trained transformers or large language models) have been trained to understand natural language, code, and images. The models provide text ou ... [truncated 225 chars](67273 chars) |
| How can I initialise a constexpr array with values using std::generate For example, if I wanted a constexpr std::array<int,100> initialised with all the multiples of 3 from 1-300 at compile time how can I do this? My first th ... [truncated 225 chars](565 chars) | ##### [ cppreference.com ](/) [ Log in ](/mwiki/index.php?title=Special:UserLogin&returnto=cpp%2Futility%2Fpair "You are encouraged to log in; however, it is not mandatory \[o\]") ##### Namespaces * [ Page ](/w/cpp/utility/pa ... [truncated 225 chars](128018 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightStackoverflowLong |
| Source task | Stack Overflow long-document |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 117 |
| Documents | 1846 |
| Positive qrels | 129 |
| Positives per query | avg 1.10, min 1, median 1, max 2 |
| Multi-positive queries | 12 (10.26%) |
| BM25 nDCG@10 | 0.4440 |
| BM25 hit@10 | 0.7009 |
| BM25 Recall@100 | 0.9225 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3894 |
| Dense hit@10 | 0.6581 |
| Dense Recall@100 | 0.9070 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4744 |
| Reranking hybrid hit@10 | 0.8376 |
| Reranking hybrid Recall@100 | 0.9767 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 1292.97 |
| Document length avg chars | 77578.44 |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).
- [BRIGHT project page](https://brightbenchmark.github.io/).
- [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT)
- Source dataset: [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT)
- MTEB dataset record: [mteb/BRIGHT](https://huggingface.co/datasets/mteb/BRIGHT)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | benchmark paper | https://arxiv.org/abs/2407.12883 |
| BRIGHT project page | 2024 | project page | https://brightbenchmark.github.io/ |
| xlangai/BRIGHT | 2024 | dataset card | https://huggingface.co/datasets/xlangai/BRIGHT |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  task_name: NanoBrightStackoverflowLong
  split_name: NanoBrightStackoverflowLong
  source_task: Stack Overflow long-document
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightStackoverflowLong.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 117
    documents: 1846
    positive_qrels: 129
  positives_per_query:
    average: 1.1025641025641026
    min: 1
    median: 1
    max: 2
    multi_positive_queries: 12
    multi_positive_query_percent: 10.256410256410257
  text_stats_chars:
    query_mean: 1292.965811965812
    document_mean: 77578.43770314193
  bm25:
    ndcg_at_10: 0.44401084662537865
    hit_at_10: 0.7008547008547008
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Stack Overflow long-document evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT StackoverflowLong queries and full cited source
      pages
    useful_training_data:
    - document-level API documentation retrieval
    - Stack Overflow questions with cited links
    - long technical-reference QA
    synthetic_data:
      document_generation: full API documentation or specification pages with many
        sections
      question_generation: developer questions with code and environment context
      answerability: positive full document should contain the API behavior or feature
        needed to solve the issue
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
    - label: BRIGHT arXiv
      url: https://arxiv.org/abs/2407.12883
    - label: BRIGHT project
      url: https://brightbenchmark.github.io/
    - label: xlangai/BRIGHT
      url: https://huggingface.co/datasets/xlangai/BRIGHT
    source_notes: []
  references:
  - title: 'BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive
      Retrieval'
    url: https://arxiv.org/abs/2407.12883
    year: 2024
    doi: 10.48550/arXiv.2407.12883
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4440108466
      hit_at_10: 0.7008547009
      recall_at_100: 0.9224806202
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 117
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9224806202
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3894004556
      hit_at_10: 0.6581196581
      recall_at_100: 0.9069767442
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 117
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9069767442
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4743933597
      hit_at_10: 0.8376068376
      recall_at_100: 0.976744186
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.025641
      query_count: 117
      query_coverage: 1.0
      relevant_coverage_at_100: 0.976744186
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
