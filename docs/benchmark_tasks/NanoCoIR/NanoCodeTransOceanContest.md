# NanoCoIR / NanoCodeTransOceanContest

## Overview

CoIR adapts CodeTransOcean contest examples from code translation into
cross-language code retrieval. The query side contains Python programs for
algorithmic tasks, while the target side contains semantically equivalent C++
solutions. This task asks a retriever to recognize program equivalence across
syntax, standard-library idioms, and implementation choices, not just shared
problem titles or comments.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) adapts CodeTransOcean's contest data
for code-to-code retrieval: Python code is used as the query and equivalent C++
code is retrieved from the corpus. [CodeTransOcean](https://arxiv.org/abs/2310.04951)
introduces multilingual code translation datasets, including MultilingualTrans
from Rosetta Code, to evaluate program-level translation across programming
languages. In CoIR, this becomes a retrieval test for semantic equivalence
rather than generation.

### Observed Data Profile

The Nano split has 200 queries, 1,008 documents, and 200 positive qrels. Each
query has one positive. Queries average 1,009.56 characters and documents
average 1,528.72 characters. The examples are algorithms such as permutations,
powerful numbers, ASCII diagrams, and string or dictionary processing.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5361 and hit@10 = 0.6850. It ranks 84 positives first, with median best
positive rank 3. Lexical matching helps when names or comments overlap, but the
main challenge is recognizing equivalent behavior across Python and C++.

### Training Data That May Help

Parallel code corpora, Rosetta Code pairs, multilingual programming contest
solutions, and hard negatives from the same algorithmic family should help.

### Synthetic Data Guidance

Generate equivalent implementations in different languages and include
distractors that share identifiers or algorithm names but implement a different
variant. Positives should be behaviorally equivalent, not merely topically
similar.

### Benchmark Information Leakage

CoIR adapts CodeTransOcean contest data with roughly 561 train queries, 226 dev
queries, and 446 test queries over a 1k-document corpus. This Nano split is
derived from the CoIR CodeTransOcean-Contest test side. Training on unfiltered
test pairs can leak the exact cross-language program pairs used for evaluation.

Training should use train-side or non-overlapping parallel code pairs, then
remove any row whose source program, target program, task name, or token
fingerprint matches NanoCodeTransOceanContest. A model trained on leaked contest
pairs may score highly by memorizing known Python-to-C++ equivalents rather than
learning general cross-language code retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| import mpmath as mp with mp.workdps(72): def integer_term(n): p = 532 * n * n + 126 * n + 9 return (p * 2**5 * mp.factorial(6 * n)) / (3 * mp.factorial(n)**6) def exponent_term(n): return -(mp.mpf("6.0") * n + 3) def nthterm( ... [truncated 225 chars](904 chars) | Almkvist-Giullera formula for pi #include <boost/multiprecision/cpp_dec_float.hpp> #include <boost/multiprecision/gmp.hpp> #include <iomanip> #include <iostream> namespace mp = boost::multiprecision; using big_int = mp::mpz_i ... [truncated 225 chars](1331 chars) |
| a1 = [0, 1403580, -810728] m1 = 2**32 - 209 a2 = [527612, 0, -1370589] m2 = 2**32 - 22853 d = m1 + 1 class MRG32k3a(): def __init__(self, seed_state=123): self.seed(seed_state) def seed(self, seed_state): assert 0 <seed_state ... [truncated 225 chars](1166 chars) | Pseudo-random numbers_Combined recursive generator MRG32k3a #include <array> #include <iostream> int64_t mod(int64_t x, int64_t y) { int64_t m = x % y; if (m < 0) { if (y < 0) { return m - y; } else { return m + y; } } return ... [truncated 225 chars](1793 chars) |
| def water_collected(tower): N = len(tower) highest_left = [0] + [max(tower[:n]) for n in range(1,N)] highest_right = [max(tower[n:N]) for n in range(1,N)] + [0] water_level = [max(min(highest_left[n], highest_right[n]) - towe ... [truncated 225 chars](770 chars) | Water collected between towers #include <iostream> #include <vector> #include <algorithm> enum { EMPTY, WALL, WATER }; auto fill(const std::vector<int> b) { auto water = 0; const auto rows = *std::max_element(std::begin(b), s ... [truncated 225 chars](1488 chars) |
| from fractions import Fraction def harmonic_series(): n, h = Fraction(1), Fraction(1) while True: yield h h += 1 / (n + 1) n += 1 if __name__ == '__main__': from itertools import islice for n, d in (h.as_integer_ratio() for h ... [truncated 225 chars](328 chars) | Harmonic series #include <iomanip> #include <iostream> #include <boost/rational.hpp> #include <boost/multiprecision/gmp.hpp> using integer = boost::multiprecision::mpz_int; using rational = boost::rational<integer>; class har ... [truncated 225 chars](1031 chars) |
| "Generate a short Superpermutation of n characters A... as a string using various algorithms." from __future__ import print_function, division from itertools import permutations from math import factorial import string import ... [truncated 225 chars](3528 chars) | Superpermutation minimisation #include <array> #include <iostream> #include <vector> constexpr int MAX = 12; static std::vector<char> sp; static std::array<int, MAX> count; static int pos = 0; int factSum(int n) { int s = 0; ... [truncated 225 chars](1027 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoCodeTransOceanContest |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 1008 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5361 |
| BM25 hit@10 | 0.6850 |
| Query length avg chars | 1009.56 |
| Document length avg chars | 1528.72 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [CodeTransOcean](https://arxiv.org/abs/2310.04951); 2023; Weixiang Yan et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [WeixiangYan/CodeTransOcean](https://huggingface.co/datasets/WeixiangYan/CodeTransOcean)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation | 2023 | source task paper | https://arxiv.org/abs/2310.04951 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoCodeTransOceanContest
  split_name: NanoCodeTransOceanContest
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoCodeTransOceanContest.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1008
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1009.56
    document_mean: 1528.720238095238
  bm25:
    ndcg_at_10: 0.5361361353193328
    hit_at_10: 0.685
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR CodeTransOcean-Contest test-derived retrieval split
    train_eval_overlap_audit: not_audited_split_filtering_required
    leakage_note: exclude NanoCodeTransOceanContest code pairs; do not train on CodeTransOcean-Contest test-derived rows
    leakage_risk:
      source_dataset: WeixiangYan/CodeTransOcean contest data
      source_train_queries_reported_by_coir: 561
      source_dev_queries_reported_by_coir: 226
      source_test_queries_reported_by_coir: 446
      risk: upstream CodeTransOcean contest test pairs can overlap with NanoCodeTransOceanContest evaluation rows
      recommended_filter: train-side only plus normalized source-code, target-code, task-name, and token-fingerprint exclusion
    useful_training_data:
      - multilingual equivalent-code pairs
      - Rosetta Code style program pairs
      - contest solutions with cross-language hard negatives
    synthetic_data:
      document_generation: C++ implementations equivalent to Python queries
      question_generation: source-language implementations of algorithmic tasks
      answerability: positive code must implement the same behavior
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
      - label: CoIR arXiv
        url: https://arxiv.org/abs/2407.02883
      - label: CodeTransOcean arXiv
        url: https://arxiv.org/abs/2310.04951
      - label: WeixiangYan/CodeTransOcean
        url: https://huggingface.co/datasets/WeixiangYan/CodeTransOcean
    source_notes: []
  references:
    - title: "CoIR: A Comprehensive Benchmark for Code Information Retrieval Models"
      url: https://arxiv.org/abs/2407.02883
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation"
      url: https://arxiv.org/abs/2310.04951
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
