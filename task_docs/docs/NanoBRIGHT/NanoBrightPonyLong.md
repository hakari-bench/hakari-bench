# NanoBRIGHT / NanoBrightPonyLong

## Overview

NanoBrightPonyLong is the long-document Pony programming-language retrieval slice of NanoBRIGHT. Queries are Pony coding tasks, and relevant documents are longer manual pages or documentation sections that contain the language constructs needed for implementation. The task measures whether retrieval systems can map a programming task to the correct documentation page when the answer is embedded among broader syntax, control-flow, or library material.

## Details

### What the Original Data Measures

BRIGHT's Pony task targets rare-language programming assistance. The long-document version changes the retrieval unit from short manual passages to larger documentation pages. A query may describe an array, string, numeric, or game-style programming problem, while the positive page may be a control-structure page, operator page, primitive-type page, or library page.

This setting tests source-page discovery rather than fine-grained passage search. It is easier to find a broad documentation page than a single short paragraph, but relevance still requires inferring which language features the code solution needs.

### Observed Data Profile

The task contains 112 queries, 577 documents, and 769 relevance judgments. It remains highly multi-positive, with 6.87 positives per query on average, a minimum of 1, a median of 7.0, a maximum of 12, and 111 multi-positive queries, or 99.11% of the set.

Queries average 388.97 characters, while documents average 3,553.13 characters. Documents are much longer than in the passage-level Pony task but shorter than the long StackExchange pages. Each positive page can cover multiple relevant constructs, which explains the lower positive count compared with the short-passage version.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2244, hit@10 of 0.8304, and recall@100 of 0.8765 using the top-500 BM25 candidate subset. This is much stronger than BM25 on the short-passage Pony task. Page-level documents aggregate many related terms, so exact matches from templates, operators, arrays, strings, and control-flow words are more likely to land on a useful page.

The remaining weakness is top-rank precision. A documentation page can include many related constructs, and BM25 may rank a broad but less central page above the page that best supports the implementation need. Term overlap is effective for candidate coverage but not always for ordering.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.0767, hit@10 of 0.4554, and recall@100 of 0.4174. Dense retrieval remains much weaker than BM25. The model struggles to bridge the gap between algorithmic problem descriptions and rare-language documentation pages.

This suggests that general embedding similarity is not enough for Pony documentation retrieval, even when documents are longer and contain broader context. The embedding may match general programming semantics but fail to identify the exact manual page needed by the template and language constructs.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2871, hit@10 of 0.8661, and recall@100 of 0.7750. It uses exactly 100 candidates per query in this slice, with no rank-101 safeguard rows.

The hybrid profile is best for nDCG@10 and hit@10, while BM25 is best for recall@100. This is an important pattern: adding dense evidence helps reorder the first page, but the dense component does not improve the broader relevant-page coverage. For reranking experiments, reranking_hybrid is attractive for top-rank quality, while BM25 remains important for high-recall candidate generation.

### Metric Interpretation for Model Researchers

The long Pony task shows that document granularity can change the apparent difficulty. BM25 becomes much stronger because relevant manual pages contain many possible lexical anchors. Dense retrieval remains weak because the query-document relation is still task-to-documentation, not ordinary semantic similarity.

Researchers should treat this as a documentation-grounded programming benchmark. A model must infer implementation requirements and then retrieve pages that describe those language constructs. The best current profile is hybrid at top ranks, but broader coverage still favors sparse lexical retrieval.

### Query and Relevance Type Tendencies

Queries describe small algorithmic tasks in Pony: array aggregation, digit arithmetic, string character checks, pair counting, and similar problems. Relevant pages often describe control structures, local variables, operators, primitive types, strings, iterators, collections, or error behavior.

The relevance relation is page-level functional support. A page is relevant because it contains manual sections needed to implement the task, even if much of the page is not directly about the specific problem.

### Representative Failure Modes

Likely failures include retrieving a documentation page for a nearby but unnecessary construct, ranking a broad page above the specific construct page, missing common features that are implicit in the task, and confusing algorithmic similarity with language-documentation relevance.

BM25 can over-rank pages with repeated template terms. Dense retrieval can under-rank the correct manual page because the wording does not resemble the problem statement. Hybrid retrieval improves the top page but may lose some of BM25's broader recall.

### Training Data That May Help

Useful training data includes document-level programming manual retrieval, rare-language coding tasks aligned to manual pages, API-documentation search, and synthetic tasks labeled with the language constructs required for implementation.

Synthetic data should create Pony tasks that require specific constructs such as loops, conditionals, primitives, iterators, errors, numeric operators, and collection operations. Positives should be complete manual pages containing those constructs. Hard negatives should be adjacent pages that look plausible but omit the required feature.

### Model Improvement Notes

Strong models should use task decomposition. First infer the needed implementation operations, then retrieve documentation for those operations. Sparse matching is strong for this task because manual pages include construct names and examples. Dense models need training on rare-language documentation alignment rather than generic programming similarity.

The observed metrics suggest using reranking_hybrid for top-10 quality and BM25 when recall@100 is the priority. A reranker that reasons over required constructs could improve the hybrid ordering while preserving BM25's wide coverage.

## Example Data

### Public Sources

The original task is based on BRIGHT's reasoning-intensive retrieval benchmark, with NanoBRIGHT providing the compact dataset packaging and long-document split.

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
| Implement a stone-smashing array problem in Pony. | A long control-structures manual page explains decisions, iteration, and repeated actions. |
| Return the sum of elements that appear exactly once. | A manual page covers control flow and expression patterns needed for array traversal. |
| Count good pairs in an integer array. | A documentation page describes local variables and related implementation building blocks. |
| Compute the product of digits minus the sum of digits. | A manual page explains arithmetic operators and how expressions are formed. |
| Check whether a string contains both cases for every letter. | A control-flow or string-related page provides the constructs needed for repeated checks. |
