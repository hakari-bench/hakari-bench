# NanoCodeRAG / NanoCodeRAGOnlineTutorials

## Overview

NanoCodeRAGOnlineTutorials is an English code-retrieval task in NanoCodeRAG, sampled from the online-tutorial retrieval source of CodeRAG-Bench. The query is usually a short tutorial title, how-to phrase, or programming-problem title. The target document is a long tutorial page containing prose, code snippets, examples, steps, and explanations.

This task tests whether a retrieval model can connect a concise developer need to the article that explains it. The documents are much longer than the queries and often contain boilerplate, multiple examples, timestamps, headings, and unrelated tokens. A good model must identify the central tutorial topic rather than match incidental code words inside a long page.

## Details

### What the Original Data Measures

CodeRAG-Bench includes online tutorials as one of its retrieval sources for retrieval-augmented code generation. The benchmark paper describes tutorial pages collected from programming tutorial sites such as GeeksforGeeks, W3Schools, Tutorialspoint, and Towards Data Science through ClueWeb22. These pages contain code snippets and explanatory text for programming concepts, APIs, algorithms, and practical tasks.

This Nano task isolates tutorial retrieval. The correct document should be the tutorial that explains the requested API, language feature, algorithm, or programming procedure. It measures title-to-article and short-query-to-long-document retrieval.

### Observed Data Profile

This Nano split contains 200 queries, 9,997 documents, and 200 positive qrels. Each query has exactly one positive tutorial page. Queries average 51.91 characters, while documents average 5,722.55 characters. This large length gap is central to the task.

Observed queries include Android screen control, secure file deletion on Linux, C++ access modifiers, Python superscript and subscript printing, and GeeksforGeeks practice problems. Documents are article-like pages with dates, explanations, examples, and sometimes long code-heavy sections.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.8175, hit@10 of 0.9200, and recall@100 of 0.9700 using a top-500 candidate pool. Tutorial titles and article bodies often share exact phrases, language names, method names, and problem titles, so term frequency is a powerful signal.

BM25 still has weaknesses. Generic titles, repeated site boilerplate, and common programming terms can distract lexical ranking. A query such as a standard-library method example or a broad STL concept may retrieve a closely related page instead of the intended overview. Long documents also contain many incidental words that can create false lexical matches.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is the strongest by nDCG@10, reaching 0.9027, with hit@10 of 0.9400 and recall@100 of 0.9550. Dense retrieval improves top-rank ordering by matching the central tutorial meaning rather than only exact title words.

Dense similarity helps when a short query describes a task and the tutorial explains it with different wording. It can connect "turn Android device screen on and off programmatically" to a page with setup steps and code, or a practice problem title to the article that states the problem and solution. Its recall@100 is slightly lower than BM25, suggesting that exact title matching still recovers some positives dense retrieval misses.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8673, hit@10 of 0.9550, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard-positive rows. Hybrid retrieval gives the best hit@10 and perfect top-100 coverage, although dense retrieval has the best nDCG@10.

This is a classic hybrid-friendly pattern. BM25 contributes exact title and phrase matching, while dense retrieval captures article-topic similarity. The combined pool ensures that every positive is available for downstream reranking. The final ranker still needs to decide which long article is most directly about the query.

### Metric Interpretation for Model Researchers

NanoCodeRAGOnlineTutorials is a strong retrieval task for studying short-query to long-document matching. BM25, dense, and hybrid all perform well, but for different reasons. BM25 uses exact title and phrase overlap, dense retrieval gives the best top-rank quality, and reranking_hybrid gives full top-100 coverage.

The metric pattern suggests that candidate generation should not discard lexical signals. A dense-only system may rank positives best on average, but BM25 recovers some title-driven pages. A hybrid candidate pool is a strong base for reranking tutorial search.

### Query and Relevance Type Tendencies

Queries are concise title-like strings. They may name a platform, language, API, algorithm, or practice problem. Documents are long tutorials with prose explanations, code snippets, examples, and headings.

Relevance is page-level topical match. The positive document should be the tutorial that explains the requested task. A page from the same language or site is non-relevant if it covers a neighboring method, operator, or problem.

### Representative Failure Modes

BM25 may over-rank pages with similar titles or repeated site boilerplate. Dense retrieval may choose a semantically nearby tutorial that explains a related concept but not the exact requested one. Hybrid retrieval can recover the positive but still needs reranking to distinguish overview pages from method-specific pages.

Long documents introduce another failure mode: incidental code snippets or footer text can match query terms even when the main article topic differs. Models should learn to focus on title, headings, and central explanation.

### Training Data That May Help

Useful training data includes non-overlapping programming tutorial title-to-page pairs, developer search logs over tutorials and documentation, Stack Overflow question-to-tutorial citation pairs, and code-example retrieval with long tutorial hard negatives. Hard negatives should come from the same language or topic but solve a different task.

Leakage filtering is required. CodeRAG-Bench reports about 79,400 online-tutorial documents, and this Nano split is sampled from that source. Training should exclude NanoCodeRAG tutorial queries, qrels, positive tutorial pages, matching titles, URLs, article bodies, code snippets, and token fingerprints.

### Model Improvement Notes

Improving this task requires robust long-document retrieval. Models should recognize the page's main tutorial topic and avoid being misled by boilerplate or incidental examples. Title and heading signals are important, but semantic alignment to the requested procedure also matters.

For reranking, useful features include title match, heading match, language or framework match, code-example relevance, and whether the article explains the requested procedure directly. A good ranker should prefer the tutorial that solves the exact task over a broader related article.

## Example Data

| Query | Positive document |
| --- | --- |
| How to turn Android device screen on and off programmatically? [62 chars] | This example demonstrate about How to turn Android device screen on and off programmatically. Step 1 − Create a new project in Android Studio, go to File ⇒ New Project and fill all required details to... [200 / 6,654 chars] |
| Tools to Securely Delete Files from Linux - GeeksforGeeks [57 chars] | 16 Feb, 2021 Every time you delete a file from your Linux system using the shift + delete or rm command, it doesn’t actually permanently and securely delete the file from the hard disk. When you delet... [200 / 3,940 chars] |
| Difference between Private and Protected in C++ with Example - GeeksforGeeks [76 chars] | 03 Jan, 2022 Protected Protected access modifier is similar to that of private access modifiers, the difference is that the class member declared as Protected are inaccessible outside the class but th... [200 / 2,559 chars] |
| How to print Superscript and Subscript in Python? - GeeksforGeeks [65 chars] | 24 Jan, 2021 Whenever we are working with formulas there may be a need of writing the given formula in a given format which may require subscripts or superscripts. There are several methods available... [200 / 2,336 chars] |
| Maximum Difference \| Practice \| GeeksforGeeks [45 chars] | Given array A[] of integers, the task is to complete the function findMaxDiff which finds the maximum absolute difference between nearest left and right smaller element of every element in array.If th... [200 / 12,706 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497) | Benchmark paper describing the retrieval sources and code-generation setting. |
| [CodeRAG-Bench project page](https://code-rag-bench.github.io/) | Project page for the benchmark. |
| [CodeRAG-Bench GitHub](https://github.com/code-rag-bench/code-rag-bench) | Repository for benchmark resources. |
| [code-rag-bench/online-tutorials](https://huggingface.co/datasets/code-rag-bench/online-tutorials) | Public source dataset card. |
| [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| "How to turn Android device screen on and off programmatically?" | A tutorial page explains Android project setup and code steps for controlling the screen state. |
| "Tools to Securely Delete Files from Linux" | The article explains why normal deletion is insufficient and describes secure deletion tools. |
| "Difference between Private and Protected in C++ with Example" | The tutorial compares access modifiers and gives C++ examples. |
| "How to print Superscript and Subscript in Python?" | The page explains methods for formatting superscript and subscript text in Python. |
| "Maximum Difference" practice problem | The article states the array problem and describes a solution for nearest smaller elements. |
