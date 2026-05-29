# NanoCodeRAG

## Overview

NanoCodeRAG is the compact CodeRAG-Bench group for code retrieval-augmented
generation. It evaluates whether a retriever can find useful programming
context before a code-generation model answers a developer request. The group
covers four source genres: Python library documentation, online tutorials,
compact programming solutions, and Stack Overflow-style posts.

The tasks are all English code retrieval tasks, but they do not have the same
retrieval shape. Documentation and tutorials are long explanatory documents,
Stack Overflow posts mix problem statements with answers and discussion, and
programming solutions are short snippets whose semantics may not repeat the
query wording. This makes NanoCodeRAG a source-genre benchmark as much as a code
benchmark.

## Details

### What the Original Group Measures

[CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://aclanthology.org/2025.findings-naacl.176/)
studies retrieval sources for code-generation tasks, asking whether retrieved
programming context can improve generation. NanoCodeRAG packages compact
retrieval tasks from that setting. The query is a code-related information need,
and the positive document is the library documentation, tutorial, programming
solution, or Stack Overflow post that should help answer it.

The group measures practical developer retrieval behavior. A good retriever
should find API documentation for library usage, tutorials for procedural tasks,
posts for error-oriented or Q&A-style problems, and compact code solutions for
implementation prompts.

### Subtask Coverage

- **NanoCodeRAGLibraryDocumentationSolutions:** API names or short API
  descriptions retrieve Python library documentation entries.
- **NanoCodeRAGOnlineTutorials:** short tutorial or programming-problem titles
  retrieve long tutorial articles.
- **NanoCodeRAGProgrammingSolutions:** natural-language Python prompts retrieve
  compact solution snippets.
- **NanoCodeRAGStackoverflowPosts:** programming questions retrieve
  Stack Overflow-style posts containing answers, snippets, and discussion.

All four subtasks are single-positive in the current Nano qrels.

### Observed Group Profile

The task pages report 800 queries, 800 positive qrels, and 29,664 split-local
candidate documents. Queries average 184.36 characters when weighted by query
count. `NanoCodeRAGLibraryDocumentationSolutions` has the longest average query
length because some queries include detailed API descriptions, while
`NanoCodeRAGOnlineTutorials` has short title-like queries.

Documents are much longer than in many code retrieval benchmarks: the
split-local document-weighted average is 4,129.84 characters. Online tutorials
and Stack Overflow posts dominate this length, while ProgrammingSolutions uses
short snippets averaging 189.13 characters. This contrast is central to the
group: retrieval over long prose-plus-code resources behaves differently from
retrieval over compact solution code.

### BM25 Difficulty

Using the dataset-provided BM25 candidate columns, NanoCodeRAG has
query-weighted BM25 nDCG@10 = 0.4198 and hit@10 = 0.5100. The strongest lexical
task is `NanoCodeRAGOnlineTutorials` (nDCG@10 = 0.7472, hit@10 = 0.8400),
followed by `NanoCodeRAGStackoverflowPosts` (0.6902, 0.7950). Long documents
often repeat query terms, API names, and error or topic words.

The weakest task is `NanoCodeRAGProgrammingSolutions` (nDCG@10 = 0.0138,
hit@10 = 0.0250). Short solution snippets may contain little of the natural
language prompt, so BM25 rarely finds the correct implementation. Library
documentation sits between these extremes: API names help, but documentation
entries can be long, nested, or phrased differently from the query.

### Training Data That May Help

Useful training data includes non-overlapping CodeRAG-Bench retrieval pairs,
API-documentation search pairs, tutorial title-to-article pairs, Stack Overflow
question-answer retrieval pairs, and natural-language prompt-to-code solution
pairs. Training should preserve source genre, because a single pooled code
retrieval objective can overfit to long prose documents and underperform on
short implementation snippets.

Training should exclude NanoCodeRAG evaluation queries, qrels, and positive
documents. Public Stack Overflow, tutorial, or documentation data should be
deduplicated against the evaluation positives when used for supervised training.

### Synthetic Data Guidance

Synthetic data should generate both developer requests and source documents in
the correct genre. For documentation retrieval, use API signatures, parameter
descriptions, examples, and version constraints. For tutorials, generate longer
step-by-step articles with code examples. For Stack Overflow-style data, include
titles, errors, failed attempts, answers, and accepted-solution cues. For
programming-solution retrieval, generate concise prompts paired with correct
short implementations.

Do not seed generation with NanoCodeRAG evaluation queries or positive
documents. Negatives should share language, APIs, or task type while failing to
answer the request or solve the implementation.

### Benchmark Information Leakage

CodeRAG-Bench builds retrieval datastores and then samples evaluation tasks from
those sources. The public CodeRAG-Bench source datasets should therefore not be
treated as ordinary safe training splits. In particular, the library
documentation source contains about 34k documentation entries, the online
tutorial source about 79.4k tutorial documents, the programming-solutions source
about 1.1k prompt-solution entries, and the Stack Overflow source about 23.5M
posts. NanoCodeRAG positives are sampled from these source genres, so unfiltered
training on `code-rag-bench/*` can leak exact positive documents.

Training should prefer non-overlapping sources that mimic the same genre, or it
should remove any row whose query, document, API path, title, URL, prompt,
solution, post id, code block, or token fingerprint matches NanoCodeRAG
evaluation data. Reported high scores from models trained on unfiltered
CodeRAG-Bench source datastores should be treated as potentially contaminated
until a positive-document and near-duplicate audit is available.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [NanoCodeRAGLibraryDocumentationSolutions](NanoCodeRAGLibraryDocumentationSolutions.md) | API or library query to documentation | 200 | 8,683 | 200 | 0.2279 | 0.3800 | 397.43 | 2,045.70 |
| [NanoCodeRAGOnlineTutorials](NanoCodeRAGOnlineTutorials.md) | tutorial title to tutorial article | 200 | 9,997 | 200 | 0.7472 | 0.8400 | 51.91 | 5,722.55 |
| [NanoCodeRAGProgrammingSolutions](NanoCodeRAGProgrammingSolutions.md) | programming prompt to solution snippet | 200 | 984 | 200 | 0.0138 | 0.0250 | 78.28 | 189.13 |
| [NanoCodeRAGStackoverflowPosts](NanoCodeRAGStackoverflowPosts.md) | programming question to Stack Overflow post | 200 | 10,000 | 200 | 0.6902 | 0.7950 | 209.83 | 4,735.02 |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCodeRAG |
| Backing dataset | NanoCodeRAG |
| Hugging Face dataset | [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG) |
| Language | en |
| Category | code |
| Subtasks | 4 |
| Total queries | 800 |
| Split-local documents | 29,664 |
| Positive qrels | 800 |
| Positives per query | exactly 1.00 for every subtask |
| Query-weighted BM25 nDCG@10 | 0.5823 |
| Query-weighted BM25 hit@10 | 0.6787 |
| Query-weighted BM25 Recall@100 | 0.8050 |
| Query-weighted Dense nDCG@10 | 0.8296 |
| Query-weighted Dense hit@10 | 0.9175 |
| Query-weighted Dense Recall@100 | 0.9513 |
| Query-weighted Reranking hybrid nDCG@10 | 0.6685 |
| Query-weighted Reranking hybrid hit@10 | 0.7800 |
| Query-weighted Reranking hybrid Recall@100 | 0.9775 |
| Mean query length | 184.36 chars, weighted by query count |
| Mean document length | 4,129.84 chars, weighted by split-local document count |

### Public Sources

- [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://aclanthology.org/2025.findings-naacl.176/); 2025; DOI: `10.18653/v1/2025.findings-naacl.176`.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CodeRAG-Bench: Can Retrieval Augment Code Generation? | 2025 | benchmark paper | https://aclanthology.org/2025.findings-naacl.176/ |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoCodeRAG
  backing_dataset: NanoCodeRAG
  dataset_id: hakari-bench/NanoCodeRAG
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCodeRAG/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 4
    queries: 800
    split_local_documents: 29664
    positive_qrels: 800
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_tasks: 0
    multi_positive_queries: 0
  text_stats_chars:
    query_mean_weighted_by_queries: 184.3625
    document_mean_weighted_by_documents: 4129.841626299554
  bm25:
    ndcg_at_10_query_weighted: 0.5822803815
    hit_at_10_query_weighted: 0.67875
    source: dataset_candidate_subset
    strongest_task_by_ndcg_at_10: NanoCodeRAGOnlineTutorials
    weakest_task_by_ndcg_at_10: NanoCodeRAGProgrammingSolutions
  tasks:
  - name: NanoCodeRAGLibraryDocumentationSolutions
    path: docs/benchmark_tasks/NanoCodeRAG/NanoCodeRAGLibraryDocumentationSolutions.md
    retrieval_focus: api_or_library_query_to_documentation
    queries: 200
    documents: 8683
    positive_qrels: 200
    bm25_ndcg_at_10: 0.2279
    bm25_hit_at_10: 0.38
  - name: NanoCodeRAGOnlineTutorials
    path: docs/benchmark_tasks/NanoCodeRAG/NanoCodeRAGOnlineTutorials.md
    retrieval_focus: tutorial_title_to_tutorial_article
    queries: 200
    documents: 9997
    positive_qrels: 200
    bm25_ndcg_at_10: 0.7472
    bm25_hit_at_10: 0.84
  - name: NanoCodeRAGProgrammingSolutions
    path: docs/benchmark_tasks/NanoCodeRAG/NanoCodeRAGProgrammingSolutions.md
    retrieval_focus: programming_prompt_to_solution_snippet
    queries: 200
    documents: 984
    positive_qrels: 200
    bm25_ndcg_at_10: 0.0138
    bm25_hit_at_10: 0.025
  - name: NanoCodeRAGStackoverflowPosts
    path: docs/benchmark_tasks/NanoCodeRAG/NanoCodeRAGStackoverflowPosts.md
    retrieval_focus: programming_question_to_stackoverflow_post
    queries: 200
    documents: 10000
    positive_qrels: 200
    bm25_ndcg_at_10: 0.6902
    bm25_hit_at_10: 0.795
  learning:
    leakage_note: exclude NanoCodeRAG evaluation queries, qrels, and positive documents;
      do not train on unfiltered CodeRAG-Bench source datastores
    leakage_risk:
      library_documentation:
        source_dataset: code-rag-bench/library-documentation
        source_corpus_size_reported_by_coderag_bench: 34000
        risk: source datastore can contain NanoCodeRAG library-documentation positives
      online_tutorials:
        source_dataset: code-rag-bench/online-tutorials
        source_corpus_size_reported_by_coderag_bench: 79400
        risk: source datastore can contain NanoCodeRAG tutorial positives
      programming_solutions:
        source_dataset: code-rag-bench/programming-solutions
        source_corpus_size_reported_by_coderag_bench: 1100
        risk: small source datastore can overlap heavily with NanoCodeRAG programming-solution
          positives
      stackoverflow_posts:
        source_dataset: code-rag-bench/stackoverflow-posts
        source_corpus_size_reported_by_coderag_bench: 23500000
        risk: source datastore can contain NanoCodeRAG Stack Overflow positives
      recommended_filter: remove matching queries, positive documents, URLs, ids,
        prompts, code blocks, and token fingerprints before training
    useful_training_data:
    - CodeRAG-Bench retrieval pairs
    - API documentation search pairs
    - tutorial title-to-article pairs
    - Stack Overflow question-answer retrieval pairs
    - natural-language prompt-to-code solution pairs
    synthetic_data:
      document_generation: documentation pages, tutorials, Stack Overflow posts, and
        compact solution snippets with realistic APIs and code
      question_generation: developer requests, API queries, tutorial titles, errors,
        and implementation prompts grounded in the source document
      answerability: positives must help solve the programming request or supply the
        needed code context
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCodeRAG
    source_urls:
    - label: CodeRAG-Bench ACL Anthology
      url: https://aclanthology.org/2025.findings-naacl.176/
  references:
  - title: 'CodeRAG-Bench: Can Retrieval Augment Code Generation?'
    url: https://aclanthology.org/2025.findings-naacl.176/
    year: 2025
    doi: 10.18653/v1/2025.findings-naacl.176
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      query_weighted_ndcg_at_10: 0.5822803815
      query_weighted_hit_at_10: 0.67875
      query_weighted_recall_at_100: 0.805
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.8296015191
      query_weighted_hit_at_10: 0.9175
      query_weighted_recall_at_100: 0.95125
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.6685249316
      query_weighted_hit_at_10: 0.78
      query_weighted_recall_at_100: 0.9775
      source: dataset_candidate_subset
```
