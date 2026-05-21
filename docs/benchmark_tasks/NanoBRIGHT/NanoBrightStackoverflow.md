# NanoBRIGHT / NanoBrightStackoverflow

## Overview

`NanoBrightStackoverflow` is the Stack Overflow slice of BRIGHT. Queries are
developer questions with code or configuration context, and relevant documents
are cited web passages such as documentation, blog posts, or API references.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) includes "coding in Stack Overflow"
among the StackExchange-derived tasks. Its construction uses accepted or
high-vote answers with URL links, then validates cited passages as useful
supporting documents. For Stack Overflow, the retrieval behavior being tested is
not simply matching a code token; it is finding the document that explains the
API, environment behavior, or language feature needed to resolve the issue.

### Observed Data Profile

The split has 117 queries, 10,000 documents, and 478 positive qrels. Queries
average 1292.97 characters and include programming context, SQL, PowerShell,
Spring Boot, Redux Toolkit, and other code snippets. Documents average 1120.63
characters and are passage chunks from API docs, blog posts, and technical
reference pages. Positives average 4.09 per query, with a maximum of 59.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2043 and hit@10 = 0.3932. It ranks 22 queries with a positive first, and the
median best positive rank is 28. Lexical matching helps when exact API names
repeat, but many queries require connecting a symptom to a documentation concept
such as descriptors, Snowflake random functions, Spring property binding, or
PowerShell launch flags.

### Training Data That May Help

Useful data includes non-overlapping Stack Overflow questions with cited links,
documentation retrieval pairs, API usage examples, issue-to-doc pairs, and hard
negatives from the same library or framework but a different failure mode.

### Synthetic Data Guidance

Generate developer questions with realistic code snippets, environment details,
and symptoms, then pair them with documentation or technical-blog passages that
explain the needed API behavior. Hard negatives should share library names and
syntax but not solve the actual issue.

## Example Data

| Query | Positive document |
| --- | --- |
| Sort tbody list which is populated with Javascript getList? I have a router with a DHCP page which is not sorted by the internal IP number, instead it is fully random. I have full access to the html and javascript, and I can ... [truncated 225 chars](12432 chars) | ` 0 ` or have opposite signs. * _Transitive_ : If ` compareFn(a, b) ` and ` compareFn(b, c) ` are both positive, zero, or negative, then ` compareFn(a, c) ` has the same positivity as the previous two. A comparator conforming ... [truncated 225 chars](3998 chars) |
| Copy and delete files from SFTP folder I have to pick (remove) the files with file mask `FileName_A_*` and `FileName_B_*` from SFTP location and place them in an sharedrive. I tried using WinSCP. I have created an `HourlyFile ... [truncated 225 chars](1125 chars) | Menu Toggle search [ ![](https://winscp- static-746341.c.cdn77.org/assets/images/logos/logo.png?v=7032) WinSCP Free SFTP, SCP, S3 and FTP client for Windows ](https://winscp.net/) * [ Home ](/eng/index.php) * [ News ](/eng/ne ... [truncated 225 chars](4000 chars) |
| DAX RLS Function using LOOKUPVALUE Parsing but not working I have a table that I'm trying to implement RLS on using a secondary table with a structure below: EmployeeTable ``` EmployeeID EmployeeEmail 1 1234@email.com 2 4567@ ... [truncated 225 chars](1525 chars) | Skip to main content This browser is no longer supported. Upgrade to Microsoft Edge to take advantage of the latest features, security updates, and technical support. [ Download Microsoft Edge ](https://go.microsoft.com/fwlin ... [truncated 225 chars](3997 chars) |
| How can I get LLM to only respond in JSON strings? This is how I am defining the executor ``` const executor = await initializeAgentExecutorWithOptions(tools, model, { agentType: 'chat-conversational-react-description', verbo ... [truncated 225 chars](1063 chars) | which covers methods to improve model reasoning, reduce the likelihood of model hallucinations, and more. You can also find many useful resources including code samples in the OpenAI Cookbook. FAQ How should I set the tempera ... [truncated 225 chars](1699 chars) |
| How can I initialise a constexpr array with values using std::generate For example, if I wanted a constexpr std::array<int,100> initialised with all the multiples of 3 from 1-300 at compile time how can I do this? My first th ... [truncated 225 chars](565 chars) | ##### [ cppreference.com ](/) [ Log in ](/mwiki/index.php?title=Special:UserLogin&returnto=cpp%2Futility%2Finteger+sequence "You are encouraged to log in; however, it is not mandatory \[o\]") ##### Namespaces * [ Page ](/w/cp ... [truncated 225 chars](4000 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightStackoverflow |
| Source task | Stack Overflow |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 117 |
| Documents | 10000 |
| Positive qrels | 478 |
| Positives per query | avg 4.09, min 1, median 2, max 59 |
| Multi-positive queries | 81 (69.23%) |
| BM25 nDCG@10 | 0.2043 |
| BM25 hit@10 | 0.3932 |
| Query length avg chars | 1292.97 |
| Document length avg chars | 1120.63 |

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
  task_name: NanoBrightStackoverflow
  split_name: NanoBrightStackoverflow
  source_task: Stack Overflow
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightStackoverflow.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 117
    documents: 10000
    positive_qrels: 478
  positives_per_query:
    average: 4.085470085470085
    min: 1
    median: 2
    max: 59
    multi_positive_queries: 81
    multi_positive_query_percent: 69.23076923076923
  text_stats_chars:
    query_mean: 1292.965811965812
    document_mean: 1120.6261
  bm25:
    ndcg_at_10: 0.2043421382260914
    hit_at_10: 0.39316239316239315
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Stack Overflow evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT Stackoverflow queries, cited positives, and linked answer pages
    useful_training_data:
      - non-overlapping Stack Overflow questions with cited links
      - documentation retrieval and API usage examples
      - issue-to-doc troubleshooting pairs
    synthetic_data:
      document_generation: API docs, technical blog passages, and framework reference snippets
      question_generation: developer questions with code snippets, environment details, and symptoms
      answerability: positives should explain the API behavior or configuration needed to solve the issue
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
    - title: "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval"
      url: https://arxiv.org/abs/2407.12883
      year: 2024
      doi: 10.48550/arXiv.2407.12883
      is_paper: true
      source_confidence: definitive_paper_link
```
