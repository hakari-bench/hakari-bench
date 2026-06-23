# NanoRTEB / NanoDS1000

## Overview

`NanoDS1000` is an English data-science code retrieval task from NanoRTEB. The query is a natural-language programming task, often with StackOverflow-style context or code fragments, and the relevant document is a Python data-science solution snippet. Each query has one positive among 997 code documents. Unlike APPS-style contest retrieval, BM25 is fairly strong because queries often mention exact library APIs, but dense retrieval is the best top-rank profile and `reranking_hybrid` gives the best recall@100.

## Details

### What the Original Data Measures

DS-1000 was introduced as a natural and reliable benchmark for data-science code generation. It focuses on common Python data-science libraries such as NumPy, SciPy, pandas, and matplotlib, and emphasizes executable correctness.

RTEB converts this into retrieval. The query describes a data-science programming need, while the relevant document is code that solves it. The task measures whether a retriever can connect user intent, library behavior, array shapes, and API semantics to executable snippets.

### Observed Data Profile

The Nano split contains 200 queries, 997 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 1,154.15 characters, while code documents average 687.85 characters.

Example queries ask how to build sparse matrices from vectors, remove isolated cells from binary arrays, construct an optimization objective, process 2D image-like arrays, and integrate a normal distribution. Positive documents are Python snippets using libraries such as NumPy, SciPy sparse, SciPy ndimage, and SciPy optimize.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.4424, hit@10 of 0.6200, and recall@100 of 0.8750. BM25 is much stronger here than on broad problem-to-code tasks.

The reason is that data-science questions often mention concrete APIs, library names, object types, errors, or mathematical terms that also appear in code. BM25 still fails when the correct solution depends on API behavior or transformation semantics rather than shared tokens.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.6835, hit@10 of 0.8700, and recall@100 of 0.9550. Dense retrieval is the strongest top-rank profile.

This shows that embedding similarity helps map problem intent to the right library operation. It can connect phrasing such as noise removal, minimization, or distribution integration to code that uses the relevant API, even when exact terms differ.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 6 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.6053, hit@10 of 0.8450, and recall@100 of 0.9700. Hybrid retrieval has the best recall@100 but lower early ranking than dense retrieval.

This is a useful tradeoff for reranking. Sparse signals recover API-specific candidates, while dense retrieval orders semantically appropriate snippets better. A code-aware reranker should benefit from the hybrid pool because it contains slightly more positives at rank 100.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the exact solution snippet appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `NanoDS1000`, dense nDCG@10 is the main first-stage quality signal, while hybrid recall@100 indicates candidate-pool strength. Good retrieval should distinguish nearby APIs from the same library, not only retrieve same-library code.

### Query and Relevance Type Tendencies

Queries are data-science programming questions with natural language, code context, arrays, formulas, or error messages. Relevant documents are executable Python snippets, often including loading code plus a concise library operation.

Relevance is exact task-solution correspondence. Code using a similar library is wrong if it performs a different transformation, optimization, aggregation, or statistical calculation.

### Representative Failure Modes

Common failures include retrieving a nearby API from the same library, confusing array shape transformations, matching on error messages instead of solution behavior, and ranking generic boilerplate. BM25 can overvalue shared library names; dense retrieval can blur similar operations such as filtering, interpolation, and optimization.

### Training Data That May Help

Useful training data includes data-science StackOverflow question-code pairs, notebook cell retrieval, API documentation examples, and hard negatives from adjacent functions in the same library. Evaluation queries, code snippets, and qrels should be excluded.

### Model Improvement Notes

Models should encode API intent, data shape, mathematical operation, and expected output behavior. Hard negatives should use the same library and similar input types but perform a different operation. Dense retrieval is the strongest first-stage profile, while hybrid retrieval is best when the goal is a high-recall reranking pool.

## Example Data

| Query | Positive document |
| --- | --- |
| Problem: I have a list of numpy vectors of the format: [array([[-0.36314615, 0.80562619, -0.82777381... [100 / 1,055 chars] | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import numpy as np import scipy.sparse as sparse vec... [200 / 520 chars] |
| Problem: I'm trying to reduce noise in a binary python array by removing all completely isolated sin... [100 / 925 chars] | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import numpy as np import scipy.ndimage square = pic... [200 / 777 chars] |
| Problem: I am having a problem with minimization procedure. Actually, I could not create a correct o... [100 / 1,716 chars] | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import scipy.optimize import numpy as np a, x_true,... [200 / 614 chars] |
| Problem: I am working with a 2D numpy array made of 512x512=262144 values. Such values are of float... [100 / 1,020 chars] | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import numpy as np from scipy import ndimage img = p... [200 / 455 chars] |
| Problem: I'm trying to integrate X (X ~ N(u, o2)) to calculate the probability up to position `x`. H... [100 / 1,047 chars] | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import scipy.integrate import math import numpy as n... [200 / 527 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DS-1000: A Natural and Reliable Benchmark for Data Science Code Generation | 2022 | task paper | [https://arxiv.org/abs/2211.11501](https://arxiv.org/abs/2211.11501) |
| xlangai/DS-1000 |  | dataset card | [https://huggingface.co/datasets/xlangai/DS-1000](https://huggingface.co/datasets/xlangai/DS-1000) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A user asks how to build a sparse representation from a list of NumPy vectors. | Python code uses NumPy and SciPy sparse utilities to build the matrix. |
| A user wants to remove isolated single cells from a binary array. | Python code uses SciPy ndimage operations over the binary array. |
| A user needs to formulate an objective for a minimization problem. | Python code uses SciPy optimize with loaded arrays and bounds. |
| A user works with a 512-by-512 float array and coordinate-based processing. | Python code uses NumPy and SciPy ndimage for the image-like array. |
| A user asks how to integrate a normal distribution up to a point. | Python code uses SciPy integrate and math operations for the probability. |
