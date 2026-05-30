# NanoCoIR / NanoCosQA

## Overview

NanoCosQA is an English code-retrieval task in NanoCoIR, adapted from CoSQA through CoIR. The query is a short web-search-style natural-language request, and the target document is a Python function that satisfies the search intent. The task reflects practical code search where users type sparse phrases such as "token to id python" or "python 3 tkinter open file dialog" rather than complete specifications.

This benchmark is useful because it tests intent recovery from very little text. The query may be short, incomplete, informal, or mildly ungrammatical, while the relevant function may express the answer through identifiers, docstrings, and implementation details. A good retrieval model must connect user search language to concrete Python utility behavior.

## Details

### What the Original Data Measures

CoIR uses CoSQA as a web-query-to-code retrieval task. CoSQA contains web queries paired with Python functions from CodeSearchNet, with human relevance annotation for whether the function satisfies the query. In the CoIR retrieval formulation, the natural-language query must retrieve the relevant Python code from a candidate corpus.

The original data measures code search under realistic search-query conditions. Relevance depends on whether the function performs the requested operation, not whether the words happen to match exactly. Since CoSQA queries come from search-log style text, many examples lack detailed constraints and require interpretation.

### Observed Data Profile

This Nano split contains 200 queries, 6,267 documents, and 200 positive qrels. Each query has exactly one positive Python function. Queries are extremely short, averaging 36.10 characters, while documents average 307.61 characters.

Observed queries ask for operations such as converting tokens to IDs, opening a Tkinter file dialog, calculating page alignment, splitting list elements while retaining spaces, and changing file extensions. Documents are compact Python functions, often with docstrings and clear utility-style names.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3049, hit@10 of 0.4650, and recall@100 of 0.7400 with a top-500 candidate pool. This modest result reflects the sparse lexical signal in short queries. If the query contains an exact API name such as Tkinter or a distinctive term such as file extension, BM25 can help. When the query is vague, synonym-heavy, or colloquial, lexical retrieval loses rank precision.

The task shows a typical web-code-search weakness for BM25: the relevant function may use identifiers or docstrings that do not mirror the query phrase. Common terms such as Python, list, date, string, file, or ID appear in many candidates. BM25 can therefore retrieve functions that share search words but implement a different operation.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest, with nDCG@10 of 0.6733, hit@10 of 0.8750, and recall@100 of 0.9800. Dense retrieval substantially outperforms BM25 because it can map short user phrases to broader code behavior.

Dense similarity is especially valuable when the query describes intent rather than exact implementation terms. It can connect "python calc page align" to a function computing byte-boundary alignment, or "how to separate list elements by white space" to a string-splitting helper. The remaining errors likely involve underspecified queries where many Python functions are plausible.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4792, hit@10 of 0.6600, and recall@100 of 0.9650. It uses top-100 candidates with optional rank-101 safeguards; seven rows contain 101 candidates and seven safeguard-positive rows are recorded. The hybrid profile improves over BM25 but remains well below dense retrieval for top ranking.

This result suggests that BM25 contributes useful exact API matches, but the dominant signal for this task is semantic intent. Adding lexical candidates can improve coverage relative to BM25 alone, yet can also introduce high-overlap wrong functions. Dense retrieval is the cleaner first-stage candidate source for short web-query code search.

### Metric Interpretation for Model Researchers

NanoCosQA is a dense-favored short-query code search task. It is a useful contrast to code tasks with long instructions or code-to-code continuity. Here, the query is often too short for reliable term-frequency matching, so a model must infer intent from sparse text and align it with Python behavior.

Recall@100 separates the profiles clearly: dense reaches 0.9800, reranking_hybrid reaches 0.9650, and BM25 reaches 0.7400. If a system uses BM25-only candidates for reranking, it will miss too many positives before reranking begins. Improvements should focus on short query understanding and code behavior representation.

### Query and Relevance Type Tendencies

Queries are short search phrases, often without full grammar. They may include a language name, an API name, a desired transformation, or a rough description of a utility. Documents are Python functions with docstrings, signatures, and implementation code.

Relevance is function-level satisfaction. The positive function should perform the operation implied by the search query. A function that shares words but performs a different transformation is non-relevant.

### Representative Failure Modes

BM25 often retrieves functions that share generic words such as list, file, Python, token, string, or ID but do not satisfy the requested operation. Dense retrieval can fail when the query is too terse to identify the desired function uniquely.

Another failure mode is API ambiguity. A query such as an open-file-dialog request may match several GUI helpers, while only one candidate implements the exact requested behavior. Strong models need both semantic intent matching and enough exact API sensitivity.

### Training Data That May Help

Useful training data includes CoSQA query-code pairs, CodeSearchNet Python functions and docstrings, and search-log-style code queries. Hard negatives should share common query terms or Python utility names while implementing a different function.

Leakage filtering is required. The Nano split is derived from CoIR CoSQA test-side data. Training should exclude NanoCosQA queries and positive Python functions, and should not train on CoSQA test-derived rows. Filters should cover normalized query text, code text, and token fingerprints.

### Model Improvement Notes

Improving NanoCosQA requires better alignment between short natural-language search phrases and executable function behavior. Identifier splitting, docstring-code alignment, and training on realistic short queries are likely important.

A strong model should not require polished requirements. It should interpret incomplete phrases, map them to likely operations, and distinguish functions that share common words but differ in behavior.

## Example Data

### Public Sources

NanoCosQA is documented through CoIR and the CoSQA paper. The CoIR-Retrieval/cosqa dataset card is the source-specific public reference for the retrieval adaptation.

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [CoSQA: 20,000+ Web Queries for Code Search and Question Answering](https://arxiv.org/abs/2105.13239) | Source task paper for web-query code search. |
| [CoIR-Retrieval/cosqa](https://huggingface.co/datasets/CoIR-Retrieval/cosqa) | Public source dataset card. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| "token to id python" | A Python helper converts a sequence of string token IDs into integer IDs. |
| "python 3 tkinter open file dialog" | A function opens a Tkinter file dialog and returns the selected filename. |
| "python calc page align" | A function computes page-boundary alignment for a content length. |
| "how to separate list elements by white space python" | A helper splits strings in a list while preserving spaces for later rejoining. |
| "python how to change file extension" | A function rewrites a file path with a normalized lowercase extension. |
