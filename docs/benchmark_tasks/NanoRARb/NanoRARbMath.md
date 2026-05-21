# NanoRARb / NanoRARbMath

## Overview

`NanoRARbMath` retrieves mathematical answers or worked solutions for math
problems. Queries are math word problems or formal problems, and the positive
document is the corresponding solution text.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
constructs a pooled numerical reasoning retrieval task from MATH and GSM8K
evaluation questions, with MetaMathQA answer material used to enlarge the
corpus. The related sources include [Training Verifiers to Solve Math Word
Problems](https://arxiv.org/abs/2110.14168), [Measuring Mathematical Problem
Solving With the MATH Dataset](https://arxiv.org/abs/2103.03874), and
[MetaMath](https://arxiv.org/abs/2309.12284).

This task tests whether retrievers can connect a problem statement to its
solution among many mathematical texts.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels.
Queries average 201.33 characters, while solution documents average 481.33
characters.

Observed examples include trigonometric simplification, vector scalar triple
products, and geometry with diagrams encoded as text.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5348
and hit@10 = 0.6600. It ranks 86 positives first.

BM25 is much stronger here than on many RAR-b tasks because the solution often
repeats equations, symbols, or named quantities from the problem.

### Training Data That May Help

Helpful data includes math problem-to-solution retrieval, GSM8K/MATH-style
reasoning pairs outside the evaluation examples, verifier data, and synthetic
worked solutions with hard distractors.

### Synthetic Data Guidance

Generate problems with full worked solutions and near-miss solutions that share
symbols but make a different transformation or solve a different quantity.
Preserve equations and final answers so answerability is explicit.

## Example Data

| Query | Positive document |
| --- | --- |
| Problem: Let $ABC$ be a triangle with $\angle A = 45^\circ$. Let $P$ be a point on side $\overline{BC}$ with $PB = 3$ and $PC = 5$. Let $O$ be the circumcenter of triangle $ABC$. Determine the length $OP$. (205 chars) | Using the extended Sine law, we find the circumradius of $ABC$ to be $R = \frac{BC}{2\sin A} = 4\sqrt 2$. [asy] unitsize(0.8 cm); pair A, B, C, O, P; A = (0,0); B = (2,2); C = (5,0); P = interp(B,C,3/8); O = circumcenter(A,B, ... [truncated 225 chars](557 chars) |
| Problem: Find the matrix that corresponds to rotating about the origin by an angle of $45^\circ$ clockwise. (107 chars) | The transformation that rotates about the origin by an angle of $45^\circ$ clockwise takes $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$ to $\begin{pmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{pmatrix}$ and $\begin{pmatrix} 0 \\ 1 \end{p ... [truncated 225 chars](406 chars) |
| Problem: Compute $\sin^{-1} (\sin 3) + \sin^{-1} (\sin 4) + \sin^{-1} (\sin 5).$ All functions are in radians. (111 chars) | Since $\sin (\pi - 3) = \sin 3$ and $-\frac{\pi}{2} \le \pi - 3 \le \frac{\pi}{2},$ \[\sin^{-1} (\sin 3) = \pi - 3.\]Since $\sin (\pi - 4) = \sin 4$ and $-\frac{\pi}{2} \le \pi - 4 \le \frac{\pi}{2},$ \[\sin^{-1} (\sin 4) = \ ... [truncated 225 chars](484 chars) |
| Problem: Find the degree measure of the least positive angle $\theta$ for which \[\tan \theta = \frac{\cos 5^\circ \cos 20^\circ + \cos 35^\circ \cos 50^\circ - \sin 5^\circ \sin 20^\circ - \sin 35^\circ \sin 50^\circ}{\sin 5 ... [truncated 225 chars](338 chars) | From the angle addition formula, the numerator is \begin{align*} &(\cos 5^\circ \cos 20^\circ - \sin 5^\circ \sin 20^\circ) + (\cos 35^\circ \cos 50^\circ - \sin 35^\circ \sin 50^\circ) \\ &= \cos (5^\circ + 20^\circ) + \cos ... [truncated 225 chars](1061 chars) |
| Problem: In triangle $ABC,$ \[a^4 + b^4 + c^4 = 2c^2 (a^2 + b^2).\]Enter the possible values of $\angle C,$ in degrees, separated by commas. (140 chars) | From the Law of Cosines, \[a^2 + b^2 - c^2 = 2ab \cos C.\]Squaring this equation, we get \[a^4 + b^4 + c^4 + 2a^2 b^2 - 2a^2 c^2 - 2b^2 c^2 = 4a^2 b^2 \cos^2 C.\]From the given equation, $a^4 + b^4 + c^4 = 2a^2 c^2 + 2b^2 c^2 ... [truncated 225 chars](615 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoRARbMath |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5348 |
| BM25 hit@10 | 0.6600 |
| Query length avg chars | 201.33 |
| Document length avg chars | 481.33 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168).
- [Measuring Mathematical Problem Solving With the MATH Dataset](https://arxiv.org/abs/2103.03874).
- [MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models](https://arxiv.org/abs/2309.12284).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| Training Verifiers to Solve Math Word Problems | 2021 | arXiv paper | https://arxiv.org/abs/2110.14168 |
| Measuring Mathematical Problem Solving With the MATH Dataset | 2021 | arXiv paper | https://arxiv.org/abs/2103.03874 |
| MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models | 2023 | arXiv paper | https://arxiv.org/abs/2309.12284 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoRARbMath
  split_name: NanoRARbMath
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoRARbMath.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 201.325
    document_mean: 481.3339
  bm25:
    ndcg_at_10: 0.5348
    hit_at_10: 0.66
    source: dataset_bm25_column
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
      - label: RAR-b arXiv
        url: https://arxiv.org/abs/2404.06347
      - label: GSM8K arXiv
        url: https://arxiv.org/abs/2110.14168
      - label: MATH arXiv
        url: https://arxiv.org/abs/2103.03874
      - label: MetaMath arXiv
        url: https://arxiv.org/abs/2309.12284
  references:
    - title: "RAR-b: Reasoning as Retrieval Benchmark"
      url: https://arxiv.org/abs/2404.06347
      year: 2024
      is_paper: true
    - title: "Training Verifiers to Solve Math Word Problems"
      url: https://arxiv.org/abs/2110.14168
      year: 2021
      is_paper: true
    - title: "Measuring Mathematical Problem Solving With the MATH Dataset"
      url: https://arxiv.org/abs/2103.03874
      year: 2021
      is_paper: true
    - title: "MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models"
      url: https://arxiv.org/abs/2309.12284
      year: 2023
      is_paper: true
```
