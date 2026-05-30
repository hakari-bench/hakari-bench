# NanoCoIR / NanoCodeSearchNet

## Overview

NanoCodeSearchNet is an English code-to-text retrieval task in NanoCoIR. It is based on CoIR's adaptation of CodeSearchNet, where source code is used as the query and the target document is the matching docstring or natural-language summary. This reverses the common semantic code search direction: instead of retrieving code from a text query, the model must retrieve concise documentation from code.

The task is useful for evaluating whether retrieval models can map implementation structure, identifiers, and API usage into natural-language descriptions. The positive document may be only a short function summary, while the query contains a larger code snippet. A good model must understand behavior expressed through syntax and local control flow, not only shared words.

## Details

### What the Original Data Measures

CoIR constructs this split from CodeSearchNet, a benchmark built from open-source GitHub functions paired with documentation across languages such as Go, Java, JavaScript, PHP, Python, and Ruby. In this CoIR formulation, the function body or code snippet is the query and the docstring or summary is the item to retrieve.

The original data measures code-to-documentation alignment. The relevant document should describe what the code does, even if it omits many implementation details. This creates a retrieval problem where identifiers, comments, library calls, parameter names, and return behavior all matter.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive docstring or summary. Queries average 636.27 characters, while documents average only 86.07 characters. The short document length makes ranking sensitive to concise descriptions and identifier overlap.

Observed examples include Python helper methods, Go utility functions, Ruby build-resource constructors, and JavaScript type checks. The code queries often include more information than the positive text, so the model must compress implementation behavior into a short natural-language retrieval target.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6099, hit@10 of 0.7300, and recall@100 of 0.9050 with a top-500 candidate pool. This is a solid lexical result, showing that function names, comments, parameter names, and distinctive identifiers often carry useful signal. When the docstring repeats the same key terms as the code, BM25 can rank the positive well.

However, the score is far below dense retrieval. Many relevant summaries describe behavior rather than repeating code tokens. A function may manipulate buffers, certificates, arrays, packages, or views, while the summary uses compact prose that does not mirror every identifier. BM25 can also be distracted by common library names or boilerplate syntax shared across unrelated functions.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is extremely strong on this task: nDCG@10 is 0.9687, hit@10 is 1.0000, and recall@100 is 1.0000. This indicates that embedding similarity captures code-to-description semantics very effectively for the NanoCodeSearchNet sample.

Dense retrieval is well matched to the task because the query and document are different forms of the same functional meaning. It can connect code that parses certificates to a summary about building an x509 certificate pool, or a JavaScript predicate to a description about ArrayBuffer views. The remaining ranking errors are likely cases where several short summaries are semantically close or where identifier-level evidence would choose a slightly better ordering.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8678, hit@10 of 0.9650, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard-positive rows. Hybrid retrieval preserves complete top-100 coverage, but its top-rank ordering is weaker than dense retrieval.

This suggests that lexical evidence is useful for coverage but not optimal for top ranking. BM25 may introduce docstrings that share identifiers or API words while describing a different function. Dense retrieval is the cleaner signal for the code-to-summary relation in this split, while reranking_hybrid is useful when a downstream reranker benefits from a broader candidate mix.

### Metric Interpretation for Model Researchers

NanoCodeSearchNet is a dense-favored code-to-text benchmark. BM25 is not weak in absolute terms, but dense retrieval dominates both top-10 ranking and top-100 recall. A model that improves this task should be able to infer function behavior from code and map it to short natural-language summaries.

The contrast with NanoCodeSearchNetCCR is important. Standard NanoCodeSearchNet requires cross-modal code-to-text abstraction, so dense semantics are strong. CCR uses code prefix-to-code continuation, where lexical continuity is much more powerful. Researchers should avoid treating all CodeSearchNet-derived tasks as having the same retrieval signal.

### Query and Relevance Type Tendencies

Queries are source code snippets or functions. They include signatures, control flow, library calls, comments, local variable names, and return statements. Documents are short docstrings, comments, or API-style summaries.

Relevance depends on behavioral description. The positive document should explain the code's purpose, not merely share a language or library. A short summary can be relevant even when it lacks many exact code tokens, and a lexically similar summary can be wrong if it describes a different function.

### Representative Failure Modes

BM25 can retrieve summaries from functions with similar identifiers or library names but different behavior. For example, many certificate, buffer, package, or array utilities share terms but perform different operations. Dense retrieval can fail when two summaries are extremely generic or when the code's behavior depends on subtle control-flow details.

Another failure mode is over-reliance on function names. Some names are highly descriptive, but others are abbreviated or shared across projects. Robust retrieval should combine name evidence with body semantics and return behavior.

### Training Data That May Help

Useful training data includes CodeSearchNet code-docstring pairs, API documentation retrieval examples, and hard negatives from the same library or language. Identifier splitting and code-aware tokenization are likely helpful because many useful lexical anchors are embedded inside names.

Leakage filtering is still required. The Nano split is derived from CoIR CodeSearchNet test-side data. Training should exclude NanoCodeSearchNet code-docstring pairs and should not use CodeSearchNet test-derived rows. A practical filter should remove matches by normalized code, docstring, function name, and token fingerprint.

### Model Improvement Notes

The strongest improvements should focus on code understanding and concise semantic alignment. Models need to encode what the function does, which inputs and outputs matter, and which side effects or object transformations are described by the docstring.

For reranking, the candidate pool is already complete under dense and hybrid retrieval. Future work should focus on placing the exact summary above short near-duplicate API descriptions, especially when several candidates share the same library or identifier family.

## Example Data

### Public Sources

NanoCodeSearchNet is documented through CoIR and the CodeSearchNet Challenge paper. The public CodeSearchNet dataset card provides the source data context for code-docstring pairs.

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [CodeSearchNet Challenge: Evaluating the State of Semantic Code Search](https://arxiv.org/abs/1909.09436) | Source task paper for code and documentation pairs. |
| [code-search-net/code_search_net](https://huggingface.co/datasets/code-search-net/code_search_net) | Public source dataset card. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Python helper retrieves a named field from connection extras with a default fallback. | The docstring says the method fetches a field from extras and explains the hook-specific formatting context. |
| A Go method releases in-flight entries up to a given index. | The summary states that entries smaller than or equal to the provided flight are freed. |
| A Go function reads CA files and adds parsed certificates to a pool. | The target comment describes creating an x509 certificate pool from provided CA files. |
| A Ruby build helper constructs an Artifactory build object from package metadata. | The documentation describes the build object corresponding to the package input. |
| A JavaScript predicate checks whether a value is an ArrayBuffer view. | The target summary states that the function determines whether the value is a view on an ArrayBuffer. |
