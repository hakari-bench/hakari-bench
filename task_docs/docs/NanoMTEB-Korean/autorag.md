# NanoMTEB-Korean / autorag

## Overview

`autorag` is a Korean RAG-oriented retrieval task built from public-document QA
data associated with the AutoRAG ecosystem. Queries are Korean questions over
finance, public-sector, legal, medical, healthcare, and commerce documents, and
the positive document is the chunk that contains the evidence needed by a RAG
system. The Nano split contains 114 queries, 720 documents, and 114 positive
qrels, with exactly one positive chunk per query. Queries average 69.61
characters, and documents average 823.60 characters. The task is a practical
test of Korean evidence retrieval from report-like chunks with numbers,
headings, policy conditions, and domain terminology.

## Details

### What the Original Data Measures

[AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline](https://arxiv.org/abs/2410.20878)
introduces AutoRAG as an open-source framework for evaluating and optimizing RAG
pipeline components, including lexical retrieval, dense retrieval, hybrid
retrieval, reranking, query expansion, and passage augmentation. The exact
`markers_bm` construction is primarily documented by dataset metadata and the
observed data rather than by a standalone task paper.

In retrieval terms, this split measures whether a Korean retriever can locate
the answer-bearing chunk for a RAG question. The target is not broad topical
similarity; the chunk should contain the specific evidence needed to answer the
query without external context.

### Observed Data Profile

The Nano split has 114 Korean queries, 720 documents, and 114 positive
judgments. Every query has one positive. Documents are public-report-like
chunks with headings, tables, percentages, dates, legal references, policy
conditions, and domain-specific terminology. Queries are often longer than
simple keyword searches because they ask for an explanation, condition, or
specific fact.

Examples include customs royalty rules, Yahoo Sports co-watching features, B2B
commerce automation, court findings about store columns, and local public
institution restructuring plans. These are realistic RAG retrieval cases where
the correct chunk may be one paragraph inside a larger report or PDF.

### BM25 Evaluation Profile

BM25 is the strongest profile, with nDCG@10 of 0.9053, hit@10 of 0.9912, and
recall@100 of 1.0000. This indicates that the task is highly favorable to
lexical matching. Queries often reuse distinctive Korean legal terms, report
phrases, named services, numerals, or policy expressions that appear in the
positive chunk.

The result is important for RAG engineering: a simple lexical retriever is a
very strong baseline for this dataset. Dense models must preserve exact Korean
domain terms and numeric anchors if they are to improve top-rank quality.

### Dense Evaluation Profile

The dense harrier-oss-270m candidates are weaker than BM25, with nDCG@10 of
0.7745, hit@10 of 0.9211, and recall@100 of 0.9561. Dense retrieval still finds
most positives, but it loses some exact evidence chunks that BM25 recovers. The
likely issue is that embedding similarity can blur report chunks that share
topic or domain while missing the exact clause, number, or named measure needed
for the answer.

For model researchers, this is a lexical-precision stress test in Korean. A
dense model that improves here must retain fine-grained terms, table-like facts,
and policy wording, not only broad semantic topic.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.8530, hit@10 of 0.9737,
and recall@100 of 1.0000. It restores complete recall like BM25 and improves
over dense retrieval, but it remains below BM25 in top-10 ordering. There are
no safeguard-positive rows, and each query has 100 hybrid candidates.

This pattern shows that hybrid search is useful as a robust RAG candidate pool:
it combines dense semantic coverage with lexical evidence and preserves full
top-100 recoverability. However, when exact Korean report terms dominate, the
BM25 ordering can still be better at the top.

### Metric Interpretation for Model Researchers

`autorag` is BM25-favorable. The main diagnostic is whether dense or hybrid
methods can avoid losing exact evidence that lexical matching captures. Since
there is exactly one positive per query, hit@10 directly measures whether the
answer chunk reaches an early result page, while recall@100 measures whether a
reranker has access to the answer at all.

The near-ceiling BM25 recall and hit rate mean that improvements should be
judged carefully. A dense model may look semantically strong but still be less
useful for RAG if it misses exact legal, financial, or policy evidence.

### Query and Relevance Type Tendencies

Queries are Korean RAG questions asking for factual explanations, quantities,
policy conditions, comparisons, or named measures. Positive documents are report
chunks that contain the needed evidence. Many chunks include mixed formats such
as headings, bullet markers, tables, and OCR-like text.

Relevance is evidence-specific. A chunk from the same report or domain is not
positive unless it contains the answer evidence. This makes same-report hard
negatives useful for training and analysis.

### Representative Failure Modes

BM25 can fail when the query paraphrases the report wording or when OCR and
tokenization artifacts alter Korean terms. Dense retrieval can fail by ranking a
topically related chunk that lacks the exact condition, percentage, or legal
clause. Hybrid retrieval can recover the positive but still rank a more
lexically attractive nearby chunk above it.

Numerical evidence is a common risk. If a question asks for a quantity or year,
the retriever must preserve the exact numeric context, not only retrieve a
related paragraph.

### Training Data That May Help

Useful training data includes non-overlapping Korean public-report RAG QA pairs,
Korean finance, government, legal, medical, and commerce document retrieval
pairs, question-to-chunk supervision from public PDFs, and hard negatives from
the same report or domain. Training should exclude `markers_bm` evaluation
queries, qrels, answers, and positive chunks likely to overlap with this Nano
split.

Synthetic data should generate Korean report chunks with headings, tables,
dates, percentages, policy conditions, and domain terminology, then create
grounded RAG questions requiring evidence from one chunk.

### Model Improvement Notes

Models should preserve Korean domain terms, numerals, and table-like evidence.
Dense encoders may need contrastive training with same-report negatives to avoid
topic-only matching. Rerankers should explicitly compare the requested fact or
condition against the candidate chunk's evidence.

## Example Data

### Public Sources

- [AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline](https://arxiv.org/abs/2410.20878)
- [AutoRAG GitHub repository](https://github.com/Marker-Inc-Korea/AutoRAG)
- [yjoonjang/markers_bm](https://huggingface.co/datasets/yjoonjang/markers_bm)
- [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline | 2024 | Paper | https://arxiv.org/abs/2410.20878 |
| AutoRAG GitHub repository | 2024 | Repository | https://github.com/Marker-Inc-Korea/AutoRAG |
| yjoonjang/markers_bm | 2025 | Dataset card | https://huggingface.co/datasets/yjoonjang/markers_bm |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| 관세법 시행령의 권리사용료 관련 조건을 묻는 질문. | A Korean legal chunk discussing intangible rights, imported materials, and royalty relevance. |
| 미국 야후가 NFL 팬들을 위해 도입한 기능을 묻는 질문. | A trend-report chunk describing Yahoo Sports Watch Together and social viewing. |
| bigin의 차별점과 이점을 묻는 질문. | An e-commerce solution chunk about marketing automation and data selection. |
| 점포 내부 기둥이 어떤 요소에 영향을 미치는지 묻는 질문. | A court-document chunk discussing store columns, visibility, size, and placement. |
| 지방공공기관 구조개혁 계획과 부채관리 기준을 묻는 질문. | A public-sector report chunk on local public institution restructuring and debt management. |
