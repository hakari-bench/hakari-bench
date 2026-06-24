# NanoCoIR / NanoCodeTransOceanContest

## Overview

NanoCodeTransOceanContest is an English code-to-code retrieval task in NanoCoIR. It is adapted from CodeTransOcean through CoIR, using algorithmic contest programs as cross-language retrieval pairs. The query side contains Python implementations, and the target side contains semantically equivalent C++ programs.

The task evaluates whether a model can recognize program equivalence across programming languages. The correct target may use different syntax, standard-library calls, numeric types, control-flow idioms, and implementation details. A retriever therefore needs more than token overlap: it must identify that two programs solve the same algorithmic problem.

## Details

### What the Original Data Measures

CodeTransOcean is a multilingual code translation benchmark. CoIR adapts its contest-style data into retrieval by treating source-language programs as queries and target-language implementations as documents. In NanoCodeTransOceanContest, the positive document must implement the same behavior as the Python query, usually in C++.

This measures cross-language semantic code retrieval. The relevant code may share a task title, comments, mathematical structure, or variable roles, but the programming-language surface can differ substantially. The benchmark is especially sensitive to whether a model can compare algorithmic behavior rather than only language-specific tokens.

### Observed Data Profile

This Nano split contains 200 queries, 1,008 documents, and 200 positive qrels. Each query has exactly one positive target program. Queries average 1,009.56 characters, and documents average 1,528.72 characters. The target side is often longer because C++ implementations include headers, namespace declarations, type aliases, and explicit data structures.

Observed examples include formulas for pi, combined recursive random-number generators, trapped-water computations, harmonic series generation, and superpermutation construction. These are program-level tasks where equivalence depends on the computation as a whole.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4869, hit@10 of 0.6350, and recall@100 of 0.8650 with a top-500 candidate pool. Lexical retrieval is helpful when programs share comments, task names, mathematical constants, or recognizable identifiers. However, the gap to dense retrieval shows that surface overlap is not enough for robust cross-language program matching.

BM25 is limited by the Python-to-C++ shift. Python library calls, syntax, and idioms may have no direct textual match in C++. Conversely, C++ boilerplate such as includes, namespaces, and type declarations can dominate term frequency without proving equivalence. BM25 can recover many positives, but it often ranks semantically related or lexically similar programs incorrectly.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest for this task, with nDCG@10 of 0.8231, hit@10 of 0.9000, and recall@100 of 0.9800. This indicates that embedding similarity captures cross-language program semantics much better than lexical matching alone.

Dense retrieval can connect algorithmic patterns such as recurrence formulas, matrix-like computations, fraction arithmetic, or list-processing logic even when the two languages use different libraries. The remaining errors likely come from tasks with similar mathematical themes or shared contest patterns, where two programs look behaviorally close but solve different variants.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7157, hit@10 of 0.8300, and recall@100 of 0.9850. It uses top-100 candidates with optional rank-101 safeguards; three queries have 101 candidates, and three safeguard-positive rows are recorded. Hybrid retrieval has the best recall@100, but dense retrieval has the best top-10 ranking.

This pattern suggests that BM25 contributes some useful exact anchors, especially task names and comments, while dense retrieval supplies the main semantic signal. Adding lexical candidates improves coverage slightly but can hurt top ranking by introducing programs that share titles, constants, or boilerplate without being equivalent.

### Metric Interpretation for Model Researchers

NanoCodeTransOceanContest is a dense-favored cross-language code retrieval task. The core difficulty is program equivalence across Python and C++, not local identifier matching. Dense retrieval outperforms BM25 by a large margin, while reranking_hybrid provides marginally higher top-100 coverage.

For model researchers, this task is a useful diagnostic for multilingual code representations. A strong result should mean that the model can encode algorithmic intent, data transformations, and numerical procedures in a language-agnostic way. Improvements should be checked against near-miss programs from the same algorithm family, not only against random negatives.

### Query and Relevance Type Tendencies

Queries are Python programs for algorithmic or mathematical tasks. Documents are C++ implementations of related tasks. Both sides may include comments, task titles, imports or includes, helper functions, loops, classes, and numerical code.

Relevance is behavioral equivalence. A target document is relevant when it implements the same task as the query. It is not enough for a candidate to mention the same topic or use a similar data structure; it must produce the same intended computation.

### Representative Failure Modes

BM25 may over-rank code that shares a task title, mathematical constant, or comment while implementing a different variant. Dense retrieval may confuse algorithms with similar high-level structure, such as different recurrence formulas, random-number generators, or sequence constructions.

Hybrid retrieval can recover more positives but may still rank a lexically attractive non-equivalent program above the correct one. This is particularly likely when contest tasks reuse common phrases or when C++ boilerplate introduces many shared tokens across candidates.

### Training Data That May Help

Useful training data includes multilingual equivalent-code pairs, Rosetta Code style program pairs, and contest solutions with cross-language hard negatives. Hard negatives should be selected from the same task family or same algorithmic pattern so the model learns equivalence rather than topic similarity.

Leakage filtering is required. The Nano split is derived from CoIR CodeTransOcean-Contest test-side data. Training should exclude NanoCodeTransOceanContest code pairs and should not use test-derived rows. Filters should remove matches by normalized source code, target code, task name, and token fingerprint.

### Model Improvement Notes

Improving this task requires language-agnostic code semantics. Models should represent control flow, mathematical operations, data structures, and algorithmic goals in a shared space across Python and C++. Identifier names can help, but they should not be the only retrieval basis.

For reranking, an effective model should compare behavioral equivalence: whether loops, formulas, state updates, and outputs correspond. Candidate recall is already high under dense and hybrid retrieval, so the main improvement target is rank ordering among topically similar programs.

## Example Data

| Query | Positive document |
| --- | --- |
| import mpmath as mp with mp.workdps(72): def integer_term(n): p = 532 * n * n + 126 * n + 9 return (p * 2**5 * mp.factorial(6 * n)) / (3 * mp.factorial(n)**6) def exponent_term(n): return -(mp.mpf("6.0") * n + 3) def nthterm(n): return integer_term(n) * mp.mpf("10.0")**exponent_term(n) for n in range(10): print("Term ", n, ' ', int(integer_term(n))) def almkvist_guillera(floatprecision): summed, nextadd = mp.mpf('0.0'), mp.mpf('0.0') for n in range(100000000): nextadd = summed + nthterm(n) if ab... [500 / 904 chars] | Almkvist-Giullera formula for pi #include <boost/multiprecision/cpp_dec_float.hpp> #include <boost/multiprecision/gmp.hpp> #include <iomanip> #include <iostream> namespace mp = boost::multiprecision; using big_int = mp::mpz_int; using big_float = mp::cpp_dec_float_100; using rational = mp::mpq_rational; big_int factorial(int n) { big_int result = 1; for (int i = 2; i <= n; ++i) result *= i; return result; } big_int almkvist_giullera(int n) { return factorial(6 * n) * 32 * (532 * n * n + 126 * n + 9) / (pow(factorial(n), 6) * 3); } int main() { std::cout << "n \| Integer portion of nth term\n" << "------------------------------------------------\n"; for (int n = 0; n < 10; ++n) std::cout << n << " \| " << std::setw(44) << almkvist_giullera(n) << '\n'; big_float epsilon(pow(big_float(10), -70)); big_float prev = 0, pi = 0; rational sum = 0; for (int n = 0;; ++n) { rational term(almkvist_giullera(n), pow(big_int(10), 6 * n + 3)); sum += term; pi = sqrt(big_float(1 / sum)); if (abs(pi - prev... [1,000 / 1,331 chars] |
| a1 = [0, 1403580, -810728] m1 = 2**32 - 209 a2 = [527612, 0, -1370589] m2 = 2**32 - 22853 d = m1 + 1 class MRG32k3a(): def __init__(self, seed_state=123): self.seed(seed_state) def seed(self, seed_state): assert 0 <seed_state < d, f"Out of Range 0 x < {d}" self.x1 = [seed_state, 0, 0] self.x2 = [seed_state, 0, 0] def next_int(self): "return random int in range 0..d" x1i = sum(aa * xx for aa, xx in zip(a1, self.x1)) % m1 x2i = sum(aa * xx for aa, xx in zip(a2, self.x2)) % m2 self.x1 = [x1i] + sel... [500 / 1,166 chars] | Pseudo-random numbers_Combined recursive generator MRG32k3a #include <array> #include <iostream> int64_t mod(int64_t x, int64_t y) { int64_t m = x % y; if (m < 0) { if (y < 0) { return m - y; } else { return m + y; } } return m; } class RNG { private: const std::array<int64_t, 3> a1{ 0, 1403580, -810728 }; const int64_t m1 = (1LL << 32) - 209; std::array<int64_t, 3> x1; const std::array<int64_t, 3> a2{ 527612, 0, -1370589 }; const int64_t m2 = (1LL << 32) - 22853; std::array<int64_t, 3> x2; const int64_t d = (1LL << 32) - 209 + 1; public: void seed(int64_t state) { x1 = { state, 0, 0 }; x2 = { state, 0, 0 }; } int64_t next_int() { int64_t x1i = mod((a1[0] * x1[0] + a1[1] * x1[1] + a1[2] * x1[2]), m1); int64_t x2i = mod((a2[0] * x2[0] + a2[1] * x2[1] + a2[2] * x2[2]), m2); int64_t z = mod(x1i - x2i, m1); x1 = { x1i, x1[0], x1[1] }; x2 = { x2i, x2[0], x2[1] }; return z + 1; } double next_float() { return static_cast<double>(next_int()) / d; } }; int main() { RNG rng; rng.seed(1234567); s... [1,000 / 1,793 chars] |
| def water_collected(tower): N = len(tower) highest_left = [0] + [max(tower[:n]) for n in range(1,N)] highest_right = [max(tower[n:N]) for n in range(1,N)] + [0] water_level = [max(min(highest_left[n], highest_right[n]) - tower[n], 0) for n in range(N)] print("highest_left: ", highest_left) print("highest_right: ", highest_right) print("water_level: ", water_level) print("tower_level: ", tower) print("total_water: ", sum(water_level)) print("") return sum(water_level) towers = [[1, 5, 3, 7, 2], [... [500 / 770 chars] | Water collected between towers #include <iostream> #include <vector> #include <algorithm> enum { EMPTY, WALL, WATER }; auto fill(const std::vector<int> b) { auto water = 0; const auto rows = *std::max_element(std::begin(b), std::end(b)); const auto cols = std::size(b); std::vector<std::vector<int>> g(rows); for (auto& r : g) { for (auto i = 0; i < cols; ++i) { r.push_back(EMPTY); } } for (auto c = 0; c < cols; ++c) { for (auto r = rows - 1u, i = 0u; i < b[c]; ++i, --r) { g[r][c] = WALL; } } for (auto c = 0; c < cols - 1; ++c) { auto start_row = rows - b[c]; while (start_row < rows) { if (g[start_row][c] == EMPTY) break; auto c2 = c + 1; bool hitWall = false; while (c2 < cols) { if (g[start_row][c2] == WALL) { hitWall = true; break; } ++c2; } if (hitWall) { for (auto i = c + 1; i < c2; ++i) { g[start_row][i] = WATER; ++water; } } ++start_row; } } return water; } int main() { std::vector<std::vector<int>> b = { { 1, 5, 3, 7, 2 }, { 5, 3, 7, 2, 6, 4, 5, 9, 1, 2 }, { 2, 6, 3, 5, 2, 8, 1, 4... [1,000 / 1,488 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation](https://arxiv.org/abs/2310.04951) | Source task paper for multilingual code translation. |
| [WeixiangYan/CodeTransOcean](https://huggingface.co/datasets/WeixiangYan/CodeTransOcean) | Public source dataset card. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Python program computes terms in an Almkvist-Giullera formula for pi. | The target C++ program implements the same formula using multiprecision numeric types. |
| A Python class implements the MRG32k3a combined recursive generator. | The C++ target implements the same pseudo-random generator state updates. |
| A Python function computes water collected between towers. | The C++ program solves the same trapped-water style computation. |
| A Python generator emits harmonic-series rational values. | The C++ target uses rational and multiprecision integer types to produce the same series. |
| A Python program constructs short superpermutations. | The C++ target implements the corresponding superpermutation minimization logic. |
