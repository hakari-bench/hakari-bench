# NanoRTEB / NanoApps

## Overview

`NanoApps` is an English code retrieval task from NanoRTEB. The query is a long natural-language programming challenge statement from APPS, and the relevant document is a Python solution. Each query has one positive solution among 8,754 candidate code documents. The task measures problem-to-code matching rather than code generation. BM25 is almost ineffective because problem statements and solutions share little surface text, while dense retrieval is the strongest profile and `reranking_hybrid` is useful but weaker.

## Details

### What the Original Data Measures

APPS was introduced as a benchmark for measuring coding challenge competence. The original task asks models to synthesize programs from competitive-programming and interview-style problem statements.

RTEB repurposes APPS as retrieval. A system must retrieve the solution code that corresponds to a problem statement. This changes the problem from generation to matching algorithmic intent, constraints, input-output behavior, and code structure.

### Observed Data Profile

The Nano split contains 200 queries, 8,754 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 1,675.42 characters, while Python solution documents average 573.12 characters.

Example queries include grid or path problems, contest archive validation, monster battle calculations, stick length optimization, and digit-removal tasks for divisibility. Positive documents are complete Python submissions rather than short function descriptions.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0084, hit@10 of 0.0150, and recall@100 of 0.0750. This is a near-failure lexical baseline.

The result is expected for problem-to-code retrieval. A natural-language statement describes goals, constraints, and examples, while the solution code contains variables, loops, imports, and implementation details. Shared words are sparse and often not discriminative.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.2528, hit@10 of 0.3500, and recall@100 of 0.6700. Dense retrieval is clearly the strongest first-stage profile.

This indicates that embedding similarity can connect problem semantics to solution structure better than term frequency. The remaining gap is large because many competitive-programming tasks share broad themes but require different algorithms, edge cases, or arithmetic.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 92 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.1655, hit@10 of 0.2750, and recall@100 of 0.5400. Hybrid retrieval is much stronger than BM25 but weaker than dense retrieval.

Sparse evidence can help when problem statements and code share tokens such as input symbols, constants, or domain words, but it also introduces misleading overlap. For this split, dense semantic matching is the primary useful signal.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the exact solution appears, hit@10 measures whether the solution is in the first ten candidates, and recall@100 measures whether a reranker can access it.

For `NanoApps`, recall@100 is especially important because a code-aware reranker may need to inspect candidates for algorithmic equivalence. Low BM25 recall means sparse-only candidate generation is a poor foundation for this task.

### Query and Relevance Type Tendencies

Queries are long programming problem statements with narratives, constraints, input-output formats, and examples. Relevant documents are Python submissions that implement the required algorithm.

Relevance is task-solution correspondence. A solution for a similar topic is wrong if it solves a different constraint set or output condition.

### Representative Failure Modes

Common failures include retrieving code for a same-topic but different contest problem, matching on variable names or numeric constants, confusing similar greedy or dynamic programming tasks, and ranking generic template-heavy submissions. BM25 is harmed by cross-modal vocabulary mismatch; dense retrieval can still overvalue broad algorithmic similarity.

### Training Data That May Help

Useful training data includes problem-statement-to-solution retrieval, competitive-programming submissions, code search over contest tasks, and hard negatives from problems with similar topics but different algorithms. Evaluation problem statements, solutions, and qrels should be excluded.

### Model Improvement Notes

Models should represent constraints, input-output behavior, and algorithmic requirements rather than only text similarity. Hard negatives should share tags such as greedy, dynamic programming, graph search, or number theory while requiring a different implementation. Dense retrieval is the strongest first-stage profile for this task.

## Example Data

| Query | Positive document |
| --- | --- |
| On the way to Rio de Janeiro Ostap kills time playing with a grasshopper he took with him in a special box. Ostap builds a line of length n such that some cells of this line are empty and some contain obstacles. Then, he places his grasshopper to one of the empty cells and a small insect in another empty cell. The grasshopper wants to eat the insect. Ostap knows that grasshopper is able to jump to any empty cell that is exactly k cells away from the current (to the left or to the right). Note th... [500 / 2,427 chars] | from math import * from sys import * from queue import * from decimal import * n,k=(int(z) for z in input().split()) s=input() i=0 while i<len(s) and s[i] not in ["G","T"]: i+=1 i+=k while i<len(s) and s[i] not in ["G","T","#"]: i+=k if i>=len(s) or s[i]=="#": print("NO") else: print("YES") [300 chars] |
| The All-Berland National Olympiad in Informatics has just ended! Now Vladimir wants to upload the contest from the Olympiad as a gym to a popular Codehorses website. Unfortunately, the archive with Olympiad's data is a mess. For example, the files with tests are named arbitrary without any logic. Vladimir wants to rename the files with tests so that their names are distinct integers starting from 1 without any gaps, namely, "1", "2", ..., "n', where n is the total number of tests. Some of the fi... [500 / 2,762 chars] | n = int(input()) t = [1] + [0] * n b, a = d = [], [] h, s = [], [] for i in range(n): f, k = input().split() d[int(k)].append(f) m = len(a) for i in a: if i.isdigit() and i[0] != '0': j = int(i) if 0 < j <= m: t[j] = 1 elif m < j <= n: t[j] = -1 else: s.append(i) else: s.append(i) for i in b: if i.isdigit() and i[0] != '0': j = int(i) if m < j <= n: t[j] = 1 elif 0 < j <= m: t[j] = -1 else: s.append(i) else: s.append(i) x = [j for j in range(1, m + 1) if t[j] < 0] y = [j for j in range(m + 1, n + 1) if t[j] < 0] u = [j for j in range(1, m + 1) if not t[j]] v = [j for j in range(m + 1, n + 1) if not t[j]] if not s and (x or y): s = ['0'] if y: i = y.pop() v.append(i) else: i = x.pop() u.append(i) h.append(str(i) + ' 0') t[i] = 0 while x or y: if v and x: i = x.pop() j = v.pop() t[j] = 1 h.append(str(i) + ' ' + str(j)) u.append(i) else: u, v, x, y = v, u, y, x k = 1 for j in s: while t[k] == 1: k += 1 h.append(j + ' ' + str(k)) k += 1 d = '\nmove ' print(str(len(h)) + d + d.join(h) if h... [1,000 / 1,311 chars] |
| You are fighting with Zmei Gorynich — a ferocious monster from Slavic myths, a huge dragon-like reptile with multiple heads! $m$ Initially Zmei Gorynich has $x$ heads. You can deal $n$ types of blows. If you deal a blow of the $i$-th type, you decrease the number of Gorynich's heads by $min(d_i, curX)$, there $curX$ is the current number of heads. But if after this blow Zmei Gorynich has at least one head, he grows $h_i$ new heads. If $curX = 0$ then Gorynich is defeated. You can deal each blow... [500 / 2,047 chars] | for _ in range(int(input())): n, x = list(map(int, input().split())) A = [] for _1 in range(n): d, h = list(map(int, input().split())) A.append([d, h]) A.sort(reverse=True) if A[0][0] >= x: print(1) else: x -= A[0][0] mz = 0 for d, h in A: mz = max(mz, d - h) if mz: print((x + mz - 1) // mz + 1) else: print(-1) [434 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Measuring Coding Challenge Competence With APPS | 2021 | task paper | [https://arxiv.org/abs/2105.09938](https://arxiv.org/abs/2105.09938) |
| codeparrot/apps |  | dataset card | [https://huggingface.co/datasets/codeparrot/apps](https://huggingface.co/datasets/codeparrot/apps) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A contest problem describes a line with obstacles and asks whether a grasshopper can move between marked cells using a fixed step. | Python code scans the string by step size and checks whether an obstacle blocks the path. |
| A programming statement describes validating contest archive metadata for an online gym upload. | Python code parses entries and tracks which numbered files or names are valid. |
| A monster battle problem gives attack and healing values and asks for the minimum number of blows. | Python code selects the strongest first blow and computes repeated net damage. |
| A stick-length optimization problem asks for a target length minimizing adjustment cost. | Python code searches candidate target lengths and computes the minimum cost. |
| A digit-removal problem asks how many digits to remove to make a number divisible by a power of ten. | Python code counts trailing zeros from the end and handles insufficient-zero cases. |
