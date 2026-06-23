# NanoBRIGHT / NanoBrightStackoverflowLong

## Overview

NanoBrightStackoverflowLong is the long-document Stack Overflow slice of NanoBRIGHT. Queries are developer questions with code, configuration, environment context, and symptoms, while relevant documents are full cited source pages such as MDN, Microsoft Learn, cppreference, API manuals, specifications, or technical documentation pages. The task measures whether a retriever can identify the source page containing the section that explains the needed API behavior or platform feature.

## Details

### What the Original Data Measures

BRIGHT's long-document StackExchange variants retrieve full source pages instead of passage chunks. For Stack Overflow, this means the positive document may be a very large reference page, documentation article, command manual, or specification. The useful explanation may be a small section inside a long page with navigation, examples, related APIs, and boilerplate.

The task is a source-page retrieval problem for programming help. Relevance depends on whether the full page contains the authoritative behavior, option, function, or language feature needed to solve the user's issue.

### Observed Data Profile

The task contains 117 queries, 1,846 documents, and 129 relevance judgments. It is mostly single-positive: there are 1.10 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 2, and 12 multi-positive queries, or 10.26% of the set.

Queries average 1,292.97 characters, while documents average 77,578.44 characters. Some source pages are extremely large, so the main challenge is not just finding a same-topic page but ranking the full page that contains the decisive API rule or reference section.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4440, hit@10 of 0.7009, and recall@100 of 0.9225 using the top-500 BM25 candidate subset. This is a strong sparse baseline. Exact API names, command names, function names, and specification terms are highly informative in programming documentation retrieval.

The weakness is that long reference pages contain many related identifiers. BM25 can rank a broad reference page highly because it shares terms with the query, even if a different page contains the exact behavior or feature needed. It is strong at coverage but not the final word on ordering.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3894, hit@10 of 0.6581, and recall@100 of 0.9070. Dense retrieval is also strong, but it trails BM25 on all reported metrics in this long-document slice.

This pattern suggests that exact identifiers are especially valuable when the relevant document is a full programming reference page. Dense retrieval can capture broad semantic similarity, but it may underweight exact function names, flags, class names, or documentation terms that uniquely identify the correct source.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4744, hit@10 of 0.8376, and recall@100 of 0.9767. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 3 safeguard rows, candidate counts from 100 to 101, and a mean of 100.03 candidates.

The hybrid profile is strongest across all reported metrics. It improves over BM25's already strong lexical signal by adding semantic evidence about the user's intended behavior or failure mode. For long Stack Overflow source retrieval, hybrid search is the best observed candidate strategy.

### Metric Interpretation for Model Researchers

This task is a high-recall hybrid-search benchmark with unusually long documents. BM25 is strong because programming references are identifier-rich. Dense retrieval is useful but weaker than BM25 in this setting. Reranking_hybrid combines exact names and semantic intent, producing the best first-page ranking and nearly complete recall@100.

Researchers should treat long-document length as a serious factor. A correct full page may be hundreds of thousands of characters, and only one section may matter. Systems that retrieve full pages should ideally include section-level reranking or evidence extraction after source-page retrieval.

### Query and Relevance Type Tendencies

Queries include JavaScript sorting, SFTP scripting, DAX row-level security, LLM JSON output, C++ constexpr initialization, iCalendar or WebView behavior, .NET APIs, and platform-specific configuration. Positive documents are often long documentation pages from major technical reference sites.

The relevance relation is full-source support. A page is positive if it contains the behavior, option, function, or rule needed to answer the Stack Overflow question. Much of the page can be unrelated.

### Representative Failure Modes

Likely failures include retrieving the wrong page from the same API family, over-ranking huge reference pages that mention many query terms, missing a source because the user describes symptoms rather than the canonical API name, and confusing examples with the authoritative rule.

BM25 may be distracted by long-page identifier density. Dense retrieval may lose exact names and version-specific details. Hybrid retrieval reduces both risks, but downstream reranking should still inspect the relevant section.

### Training Data That May Help

Useful training data includes document-level API documentation retrieval, Stack Overflow questions with cited links, long technical-reference QA, and issue-to-document pairs where the positive is a full source page.

Synthetic data should create developer questions with concrete code and environment context, then pair them with full documentation pages where one section explains the behavior. Hard negatives should be long pages from the same platform or API family that do not resolve the issue.

### Model Improvement Notes

Strong systems should combine exact identifier preservation with semantic understanding of developer intent. Candidate retrieval should use hybrid search, followed by reranking or section extraction that can locate the answer-bearing part of a large source page.

The observed metrics show that reranking_hybrid is the best pool for both top-10 visibility and downstream coverage. Further improvements should focus on distinguishing authoritative source sections from merely related reference pages.

## Example Data

| Query | Positive document |
| --- | --- |
| Sort tbody list which is populated with Javascript getList? I have a router with a DHCP page which i... [100 / 12,432 chars] | * Skip to main content * Skip to search * Skip to select language [ MDN Web Docs ](/en-US/) Open main menu * References [ References ](/en-US/docs/Web) * [ Overview / Web Technology Web technology ref... [200 / 951,658 chars] |
| Copy and delete files from SFTP folder I have to pick (remove) the files with file mask `FileName_A_... [100 / 1,125 chars] | Menu Toggle search [ ![](https://winscp- static-746341.c.cdn77.org/assets/images/logos/logo.png?v=7032) WinSCP Free SFTP, SCP, S3 and FTP client for Windows ](https://winscp.net/) * [ Home ](/eng/inde... [200 / 190,917 chars] |
| DAX RLS Function using LOOKUPVALUE Parsing but not working I have a table that I'm trying to impleme... [100 / 1,525 chars] | Skip to main content This browser is no longer supported. Upgrade to Microsoft Edge to take advantage of the latest features, security updates, and technical support. [ Download Microsoft Edge ](https... [200 / 42,606 chars] |
| How can I get LLM to only respond in JSON strings? This is how I am defining the executor ``` const... [100 / 1,063 chars] | Text generation models OpenAI's text generation models (often called generative pre-trained transformers or large language models) have been trained to understand natural language, code, and images. T... [200 / 67,273 chars] |
| How can I initialise a constexpr array with values using std::generate For example, if I wanted a co... [100 / 565 chars] | ##### [ cppreference.com ](/) [ Log in ](/mwiki/index.php?title=Special:UserLogin&returnto=cpp%2Futility%2Fpair "You are encouraged to log in; however, it is not mandatory \[o\]") ##### Namespaces * [... [200 / 128,018 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| Sort a JavaScript-populated table body by internal IP number. | A long MDN-style JavaScript reference page contains the sort and comparator behavior needed. |
| Copy and delete masked files from an SFTP folder using WinSCP. | A long WinSCP documentation page explains scripting commands and file operations. |
| Implement DAX row-level security using LOOKUPVALUE. | A Microsoft Learn page contains the relevant DAX function and security semantics. |
| Force an LLM executor to respond only with JSON strings. | A long text-generation documentation page discusses model output behavior and implementation guidance. |
| Initialize a constexpr C++ array with generated values. | A cppreference-style page contains the compile-time utility or template behavior involved. |
