# NanoCodeRAG

## Overview

NanoCodeRAG is the compact Nano set for CodeRAG-Bench, a benchmark for
retrieval-augmented code generation. The group evaluates whether a retriever can
find programming context that would help a generation model answer a developer
request. It covers four source genres: Python library documentation, online
tutorials, compact programming solutions, and Stack Overflow-style posts.

The tasks are all English code retrieval tasks, but their retrieval shapes are
very different. Documentation and tutorials are long explanatory resources,
Stack Overflow posts mix problem statements, answers, and code, while
programming solutions are short snippets whose semantics may not repeat the
query wording. BM25 exposes source genres where exact API names or topic words
dominate; dense retrieval tests whether developer intent can be connected to
code or long prose; `reranking_hybrid` shows when exact code tokens and semantic
matching form a better candidate pool.

## What This Group Measures

[CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://aclanthology.org/2025.findings-naacl.176/)
studies retrieval sources for code-generation tasks. NanoCodeRAG packages
compact retrieval splits from that setting. The query is a code-related
information need, and the positive document is the documentation page,
tutorial, programming solution, or Stack Overflow post that should help solve
it.

This group measures practical developer retrieval. A useful retriever should
find API documentation for library usage, tutorial context for procedural
tasks, solution snippets for implementation prompts, and Q&A posts for
error-oriented or usage-oriented problems. It therefore evaluates source-genre
matching as much as generic code search.

## Task Families

- **Library documentation retrieval:** `NanoCodeRAGLibraryDocumentationSolutions`
  maps API or library requests to documentation entries.
- **Tutorial retrieval:** `NanoCodeRAGOnlineTutorials` retrieves long online
  tutorial articles from short title-like or task-like queries.
- **Programming solution retrieval:** `NanoCodeRAGProgrammingSolutions` maps
  natural-language programming prompts to compact code snippets.
- **Stack Overflow retrieval:** `NanoCodeRAGStackoverflowPosts` retrieves posts
  that combine developer questions, answers, discussion, and code blocks.

## Dataset Shape

NanoCodeRAG contains 4 task pages, 800 queries, 29,664 split-local documents,
and 800 positive qrel rows. Every task is single-positive in the current
metadata. Each split has 200 queries, but document pools and document lengths
vary substantially.

The document-weighted average length is dominated by tutorials and Stack
Overflow posts, both of which are long prose-plus-code documents. Programming
solutions are much shorter, averaging under 200 characters. Query length also
varies: library documentation queries can include detailed API descriptions,
while tutorial and solution queries are much shorter. This makes the group a
useful test of retrieval across source genres.

## Retrieval Behavior

### BM25 Profile

BM25 works well when long documents repeat API names, topic words, error
phrases, or tutorial titles. It is strong on online tutorials and Stack
Overflow posts, and reasonably strong on library documentation. These tasks
often preserve the exact strings a developer would search for.

BM25 nearly fails on `NanoCodeRAGProgrammingSolutions`. The query describes a
programming task in natural language, while the positive document is a compact
solution snippet. The relevant code may contain little literal overlap with the
prompt, so sparse retrieval misses the implementation even when the intent is
clear.

### Dense Profile

Dense retrieval is the best profile for all four NanoCodeRAG tasks in the
current metadata. It is especially important for programming-solution retrieval,
where it raises nDCG@10 far above BM25 by connecting task descriptions to code
semantics. It also improves documentation, tutorial, and Stack Overflow
retrieval by matching developer intent beyond exact phrase overlap.

Dense retrieval still has to preserve code-specific details. A semantically
near document that uses the wrong API, version, library, argument, or
implementation pattern may not help code generation. Dense gains are most
meaningful when they keep exact programming anchors while improving intent
matching.

### Reranking Hybrid Profile

`reranking_hybrid` is competitive but usually below dense in this group. That
pattern is informative: dense retrieval is the strongest first-stage ranker
overall, but sparse signals still recover useful candidates in documentation,
tutorial, and Stack Overflow tasks. Hybrid is weaker for ProgrammingSolutions
because BM25 contributes little to a prompt-to-code snippet task.

For reranker experiments, the hybrid pool is still useful when the source genre
has exact API or error tokens. It is less useful when the task is mainly
semantic program retrieval with little lexical overlap.

## Task Summary

| Task | Retrieval focus | Queries | Docs | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoCodeRAGLibraryDocumentationSolutions](NanoCodeRAGLibraryDocumentationSolutions.md) | API query to documentation | 200 | 8,683 | 0.6867 | 0.7645 | 0.7544 | Dense |
| [NanoCodeRAGOnlineTutorials](NanoCodeRAGOnlineTutorials.md) | tutorial query to article | 200 | 9,997 | 0.8175 | 0.9027 | 0.8673 | Dense |
| [NanoCodeRAGProgrammingSolutions](NanoCodeRAGProgrammingSolutions.md) | prompt to solution snippet | 200 | 984 | 0.0512 | 0.7646 | 0.2151 | Dense |
| [NanoCodeRAGStackoverflowPosts](NanoCodeRAGStackoverflowPosts.md) | developer question to Stack Overflow post | 200 | 10,000 | 0.7737 | 0.8865 | 0.8373 | Dense |

## Interpretation Notes for Model Researchers

NanoCodeRAG should be read by source genre. Long tutorial and Stack Overflow
documents make lexical retrieval easier because query terms often reappear.
Short programming-solution snippets make lexical retrieval much harder because
the code may only express the intent operationally. A model that does well on
tutorials is not necessarily strong at prompt-to-code retrieval.

The ProgrammingSolutions split is the clearest diagnostic for semantic code
retrieval in this group. The documentation and Stack Overflow splits are better
diagnostics for exact API, version, library, error-message, and prose-code
alignment. Compare BM25 and dense task by task before interpreting a group
average.

## Training and Leakage Notes

Useful training data includes non-overlapping CodeRAG-Bench-style retrieval
pairs, API documentation search pairs, tutorial title-to-article pairs, Stack
Overflow question-answer retrieval, and prompt-to-code solution data. Training
should preserve source genre rather than pooling every source into one generic
code retrieval objective.

Exclude NanoCodeRAG evaluation queries, positives, qrels, documentation pages,
tutorials, Stack Overflow posts, and solution snippets. Public CodeRAG-Bench
source datastores should be treated as potential leakage sources unless exact
and near-duplicate positives have been removed.

## Public Sources

- [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://aclanthology.org/2025.findings-naacl.176/), 2025.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| CodeRAG-Bench: Can Retrieval Augment Code Generation? | 2025 | paper | [https://aclanthology.org/2025.findings-naacl.176/](https://aclanthology.org/2025.findings-naacl.176/) |
