# NanoCodeRAG / NanoCodeRAGLibraryDocumentationSolutions

## Overview

NanoCodeRAGLibraryDocumentationSolutions is an English code-retrieval task in NanoCodeRAG, sampled from the library-documentation retrieval source of CodeRAG-Bench. The query is an API name, usage intent, or short reference-style description, and the target document is the documentation entry that contains the needed API behavior, signature, arguments, aliases, examples, or migration notes.

The task is useful for studying retrieval-augmented code generation because library documentation is often the missing context for correct API use. A model must preserve exact identifiers such as dotted module paths and function names, while also matching semantic clues about the API's purpose. The documents are long enough to include generic boilerplate, so the retriever must find the exact reference page rather than any page from the same library.

## Details

### What the Original Data Measures

CodeRAG-Bench evaluates whether retrieval can support code generation. It defines several retrieval sources, including programming solutions, online tutorials, Python library documentation, Stack Overflow posts, and GitHub files. The library-documentation source is built from official Python library references, including documentation collected through devdocs.io.

This Nano task isolates the documentation source. The relevant document should contain the API behavior, signature, argument details, aliases, examples, or version-specific notes needed by the query. The task therefore measures API-reference retrieval, not general web search.

### Observed Data Profile

This Nano split contains 200 queries, 8,683 documents, and 200 positive qrels. Each query has exactly one positive documentation entry. Queries average 397.43 characters, and documents average 2,045.70 characters. The long document length reflects full reference entries rather than short summaries.

Observed examples are dominated by TensorFlow-style API documentation, including entries such as forward-mode autodiff accumulators, random datasets, confusion matrices, batch-to-space operations, and distribution strategies. The relevant documents contain signatures, aliases, parameter descriptions, examples, deprecation notices, and migration guidance.

### BM25 Evaluation Profile

BM25 is strong on this task, with nDCG@10 of 0.6867, hit@10 of 0.8150, and recall@100 of 0.9200 using a top-500 candidate pool. Exact API paths, function names, class names, and argument names give lexical retrieval meaningful anchors. When the query contains a dotted TensorFlow path, BM25 can often find the matching documentation entry.

The difficulty is that documentation pages share large amounts of boilerplate: alias sections, migration guide text, parameter templates, and generic phrases appear across many entries. BM25 can over-rank nearby APIs in the same namespace when they share common text but describe a different function. Exact identifier preservation matters, but it is not sufficient by itself.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is the best top-rank result, with nDCG@10 of 0.7645, hit@10 of 0.8900, and recall@100 of 0.9250. Dense retrieval improves over BM25 by using semantic clues in the API summary and query text, not just exact identifier overlap.

Dense similarity can connect a query about Jacobian-vector products to forward-mode autodiff documentation, or a query about reshaping batch dimensions to a batch-to-space operation. It still faces ambiguity among neighboring API pages, especially when many documents share the same library namespace and boilerplate structure.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7544, hit@10 of 0.8850, and recall@100 of 0.9450. It uses top-100 candidates with optional rank-101 safeguards; 11 rows contain 101 candidates and 11 safeguard-positive rows are recorded. Hybrid retrieval has the best top-100 coverage but is slightly below dense retrieval for nDCG@10.

This pattern shows that lexical and dense signals are complementary. BM25 helps with exact API paths and argument names, while dense retrieval helps with purpose and usage descriptions. The hybrid pool is attractive for downstream reranking because it recovers more positives by rank 100, but final ranking still needs to choose the exact documentation entry among similar API pages.

### Metric Interpretation for Model Researchers

NanoCodeRAGLibraryDocumentationSolutions is an API-documentation retrieval task where both exact terms and semantic similarity matter. Dense retrieval is strongest at the top, reranking_hybrid is strongest for coverage, and BM25 remains competitive because API identifiers are decisive.

Researchers should inspect whether a model preserves namespace structure and identifier tokens. A model that smooths all TensorFlow documentation into a broad semantic cluster may retrieve the right topic but wrong page. Conversely, a purely lexical model may overvalue boilerplate and alias text.

### Query and Relevance Type Tendencies

Queries are API-name or usage-intent strings. They may contain a dotted path, class or function name, short description, inheritance note, or alias cue. Documents are reference entries with signatures, attributes, examples, arguments, returns, warnings, and version notes.

Relevance is exact documentation grounding. The positive document should be the page or entry that contains the requested API's behavior or signature. A page from the same namespace is non-relevant if it documents a different operation.

### Representative Failure Modes

BM25 may confuse entries that share `tf.compat.v1`, alias boilerplate, or migration guide text. Dense retrieval may confuse APIs with related purposes, such as neighboring tensor-shape operations or similar dataset classes.

Hybrid retrieval can recover the positive while still ranking a nearby API page above it. These errors are especially likely when the query and candidate documents share broad TensorFlow documentation language but differ in the final namespace component or argument behavior.

### Training Data That May Help

Useful training data includes non-overlapping Python API documentation retrieval pairs, DocPrompting-style natural-language intent to documentation pairs, docstring and example-code to reference-page retrieval, and library search logs with overlap removed. Training should preserve dotted paths, argument names, aliases, and version notes.

Leakage filtering is required. CodeRAG-Bench reports a library-documentation source corpus of about 34,000 entries, and this Nano split is sampled from that source. Training should exclude NanoCodeRAG library-documentation queries, qrels, positive documentation entries, matching API paths, section text, and token fingerprints.

### Model Improvement Notes

Improving this task requires combining identifier-sensitive retrieval with semantic API understanding. Tokenization should preserve module paths, class names, function names, and argument names. At the same time, the model should understand short descriptions such as "computes a confusion matrix" or "distribution strategy for a single device."

For reranking, useful features include namespace match, signature match, argument compatibility, and whether the document contains the exact behavior requested by the query. Boilerplate sections should be down-weighted.

## Example Data

### Public Sources

NanoCodeRAGLibraryDocumentationSolutions is documented through CodeRAG-Bench and its public project resources. The source-specific dataset card is `code-rag-bench/library-documentation`.

### Source Reference Table

| Source | Role |
| --- | --- |
| [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497) | Benchmark paper describing the retrieval sources and code-generation setting. |
| [CodeRAG-Bench project page](https://code-rag-bench.github.io/) | Project page for the benchmark. |
| [CodeRAG-Bench GitHub](https://github.com/code-rag-bench/code-rag-bench) | Repository for benchmark resources. |
| [code-rag-bench/library-documentation](https://huggingface.co/datasets/code-rag-bench/library-documentation) | Public source dataset card. |
| [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| `tf.autodiff.ForwardAccumulator` and a short description of Jacobian-vector products. | The documentation entry gives the constructor signature and explains forward-mode autodiff behavior. |
| `tf.compat.v1.data.experimental.RandomDataset` as a pseudorandom-value dataset. | The reference page documents the dataset constructor and inherited dataset behavior. |
| `tf.compat.v1.confusion_matrix` with a confusion-matrix description. | The target entry gives aliases, signature, and details for labels, predictions, classes, dtype, and weights. |
| `tf.compat.v1.batch_to_space_nd` as an N-dimensional batch-to-space operation. | The documentation explains the reshape operation, block shape, crops, and migration aliases. |
| `tf.compat.v1.distribute.OneDeviceStrategy` for single-device distribution. | The reference entry describes variable placement and input distribution for one device. |
