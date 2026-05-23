# NanoCodeRAG / NanoCodeRAGStackoverflowPosts

## Overview

CodeRAG-Bench treats Stack Overflow posts as developer knowledge that can
augment code generation, using question-answer posts from the StackExchange
portion of RedPajama-1T as retrievable documents. In this Nano split, a
programming question, usually beginning with a title and short problem
description, must retrieve a long post containing answers, code examples,
caveats, and discussion. The observed topics include Photoshop automation,
locked files in C#, concurrent database editing, MySQL triggers, and IIS
bandwidth behavior, so relevance is a practical fix or design answer rather
than a generic topic match.

## Details

### What the Original Data Measures

[CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497)
collects Stack Overflow posts as one of its five developer retrieval sources,
using the StackExchange split of RedPajama-1T. The paper treats each post as a
retrievable document with a question, code responses, and textual explanations.
Its open retrieval analysis reports that Stack Overflow posts can improve
general programming generation, because retrieved posts may contain the same
programming problem, code, and detailed explanations.

This Nano split focuses on retrieving those community Q&A documents directly.
The source is less formal than documentation: posts include multiple answers,
partial fixes, warnings, tool recommendations, and conversational text.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Every query has one positive. Queries average 209.84 characters and often begin
with `Q:` followed by a title and problem details. Documents average 4,735.05
characters and may contain several answers, code examples, caveats, and links.

The sampled queries include Mac font lookup from Photoshop automation, deleting
a locked file in C#, concurrent database editing, MySQL trigger errors, and IIS
bandwidth throttling. The positives are practical answer threads, not polished
reference pages, so relevance may depend on matching the exact error condition
or development environment.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6902
and hit@10 = 0.7950. It ranks 115 positives first and finds 159 positives in the
top 10. Lexical matching is often strong because the query text is copied from
the post's question and the answer thread repeats product names, languages, and
error phrases.

The misses are usually near-neighbor Q&A failures. For TortoiseSVN branching,
BM25 retrieves another version-control discussion before the positive. For SQL
Server's equivalent of MySQL `REPLACE INTO`, it retrieves a database hosting
cost discussion. The retriever must distinguish the requested operation,
platform, and tool from other posts with similar technology words.

### Training Data That May Help

Useful training data includes non-overlapping Stack Overflow question-to-answer
thread retrieval, duplicate-question retrieval, issue-to-fix pairs, API usage
Q&A, and documentation-linked Q&A. Training should exclude the NanoCodeRAG Stack
Overflow evaluation queries, qrels, and positive posts.

Community Q&A data benefits from negatives that share tags or error messages but
answer a different problem. Models should learn to use both the question title
and body, because the title alone may be too broad.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Q&A posts and generate
developer questions that preserve the language, framework, error, environment,
and desired operation. The selected post should contain a usable answer, warning,
or workaround.

For joint generation, create realistic Stack Overflow-style threads with a
question, accepted answer, alternative answers, code snippets, and caveats. Hard
negatives should share the same tags or tool names but solve a different
failure mode. Do not use Nano evaluation queries or positive posts as seeds.

### Benchmark Information Leakage

CodeRAG-Bench uses a Stack Overflow retrieval source of about 23.5M posts from
the RedPajama StackExchange split, and this Nano split is sampled from that
source. The `code-rag-bench/stackoverflow-posts` data should be treated as an
evaluation-source datastore unless Nano positives and near duplicates have been
removed. Training on the unfiltered source can leak the exact posts used by
NanoCodeRAG.

Training should use non-overlapping Q&A corpora or remove every row whose
question title, body, answer, post id, URL, code block, or token fingerprint
matches NanoCodeRAG Stack Overflow queries and positives. Models trained on
leaked posts may score highly by memorizing community answers rather than
learning robust developer-Q&A retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| Q: How can I find the full path to a font from its display name on a Mac? I am using the Photoshop's javascript API to find the fonts in a given PSD. (149 chars) | Given a font name returned by the API, I want to find the actual physical font file that font name corresponds to on the disc. This is all happening in a python program running on OSX so I guess I'm looking for one of: * *Som ... [truncated 225 chars](5076 chars) |
| Q: How do I delete a file which is locked by another process in C#? I'm looking for a way to delete a file which is locked by another process using C#. I suspect the method must be able to find which process is locking the fi ... [truncated 225 chars](396 chars) | A: If you want to do it programmatically. I'm not sure... and I'd really recommend against it. If you're just troubleshooting stuff on your own machine, SysInternals Process Explorer can help you Run it, use the Find Handle c ... [truncated 225 chars](13199 chars) |
| Q: Editing database records by multiple users I have designed database tables (normalised, on an MS SQL server) and created a standalone windows front end for an application that will be used by a handful of users to add and ... [truncated 225 chars](334 chars) | I am concerned that if two users start editing the same record then the last to commit the update would be the 'winner' and important information may be lost. A number of solutions come to mind but I'm not sure if I am going ... [truncated 225 chars](4026 chars) |
| Q: Throw an error preventing a table update in a MySQL trigger If I have a trigger before the update on a table, how can I throw an error that prevents the update on that table? (177 chars) | A: CREATE TRIGGER sample_trigger_msg BEFORE INSERT FOR EACH ROW BEGIN IF(NEW.important_value) < (1*2) THEN DECLARE dummy INT; SELECT Enter your Message Here!!! INTO dummy FROM mytable WHERE mytable.id=new.id END IF; END; A: H ... [truncated 225 chars](5314 chars) |
| Q: Bandwith throttling in IIS 6 by IP Address I am writing an application that downloads large files in the background. All clients are logged in locally, or through a VPN. When they are logged in locally, I do not want to th ... [truncated 225 chars](391 chars) | Since this is an AIR Application, I figure I will throttle via server-side since I can do it from either the server itself (IIS 6) or the web service (asp.net / C#). Throttling through IIS 6 seems to work fine, but it seems l ... [truncated 225 chars](922 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCodeRAG |
| Backing dataset | NanoCodeRAG |
| Task / split | NanoCodeRAGStackoverflowPosts |
| Hugging Face dataset | [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6902 |
| BM25 hit@10 | 0.7950 |
| Query length avg chars | 209.84 |
| Document length avg chars | 4,735.05 |

### Public Sources

- [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497); 2025; Zora Zhiruo Wang, Akari Asai, Xinyan Velocity Yu, Frank F. Xu, Yiqing Xie, Graham Neubig, and Daniel Fried; DOI: `10.18653/v1/2025.findings-naacl.176`.
- [CodeRAG-Bench project page](https://code-rag-bench.github.io/).
- [CodeRAG-Bench GitHub repository](https://github.com/code-rag-bench/code-rag-bench).
- [code-rag-bench/stackoverflow-posts dataset card](https://huggingface.co/datasets/code-rag-bench/stackoverflow-posts).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG)
- Source dataset: [code-rag-bench/stackoverflow-posts](https://huggingface.co/datasets/code-rag-bench/stackoverflow-posts)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CodeRAG-Bench: Can Retrieval Augment Code Generation? | 2025 | arXiv paper | https://arxiv.org/abs/2406.14497 |
| CodeRAG-Bench project page | 2025 | project page | https://code-rag-bench.github.io/ |
| code-rag-bench/stackoverflow-posts | 2024 | dataset card | https://huggingface.co/datasets/code-rag-bench/stackoverflow-posts |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCodeRAG
  backing_dataset: NanoCodeRAG
  dataset_id: hakari-bench/NanoCodeRAG
  task_name: NanoCodeRAGStackoverflowPosts
  split_name: NanoCodeRAGStackoverflowPosts
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCodeRAG/NanoCodeRAGStackoverflowPosts.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2406.14497
    additional_source_urls:
      - https://aclanthology.org/2025.findings-naacl.176/
      - https://code-rag-bench.github.io/
      - https://github.com/code-rag-bench/code-rag-bench
      - https://huggingface.co/datasets/code-rag-bench/stackoverflow-posts
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
    query_mean: 209.835
    document_mean: 4735.0462
  bm25:
    ndcg_at_10: 0.6901992074
    hit_at_10: 0.795
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: CodeRAG-Bench Stack Overflow posts retrieval source sampled into NanoCodeRAG
    train_eval_overlap_audit: not_audited_source_datastore_filtering_required
    leakage_note: exclude NanoCodeRAG Stack Overflow queries, qrels, and positive posts; do not train on unfiltered code-rag-bench/stackoverflow-posts rows
    leakage_risk:
      source_dataset: code-rag-bench/stackoverflow-posts
      source_corpus_size_reported_by_coderag_bench: 23500000
      risk: CodeRAG-Bench Stack Overflow source datastore can contain NanoCodeRAG evaluation positives
      recommended_filter: remove matching titles, bodies, answers, post ids, URLs, code blocks, and token fingerprints
    useful_training_data:
      - non-overlapping Stack Overflow question-to-answer thread retrieval
      - duplicate-question and related-question retrieval pairs
      - issue-to-fix and API usage Q&A pairs
      - documentation-linked Q&A with tag-matched hard negatives
    synthetic_data:
      document_generation: realistic Stack Overflow-style threads with question, accepted answer, alternative answers, code snippets, caveats, and environment details
      question_generation: developer questions preserving language, framework, error message, and desired operation
      answerability: the selected post should contain a usable answer, workaround, warning, or API usage pattern
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCodeRAG
    source_urls:
      - label: CodeRAG-Bench arXiv
        url: https://arxiv.org/abs/2406.14497
      - label: CodeRAG-Bench project page
        url: https://code-rag-bench.github.io/
      - label: CodeRAG-Bench GitHub
        url: https://github.com/code-rag-bench/code-rag-bench
      - label: code-rag-bench/stackoverflow-posts
        url: https://huggingface.co/datasets/code-rag-bench/stackoverflow-posts
    source_notes: []
  references:
    - title: "CodeRAG-Bench: Can Retrieval Augment Code Generation?"
      url: https://arxiv.org/abs/2406.14497
      year: 2025
      doi: 10.18653/v1/2025.findings-naacl.176
      is_paper: true
      source_confidence: definitive_paper_link
```
