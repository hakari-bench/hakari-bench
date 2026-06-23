# MNanoBEIR / NanoBEIR-ja / NanoMSMARCO

## Overview

`NanoBEIR-ja__NanoMSMARCO` is the Japanese NanoBEIR version of MS MARCO passage
retrieval, a benchmark built from real web-search questions and answer-bearing
passages. The task uses Japanese translated web queries and asks a retriever to
rank Japanese translated passages that directly answer each query. The Nano
split contains 50 queries, 5,043 documents, and 50 positive qrels, with exactly
one positive passage per query. It is a short-query, single-answer retrieval
task, and the observed results show a strong dense-retrieval advantage over
lexical and hybrid fused ranking.

## Details

### What the Original Data Measures

[MS MARCO](https://arxiv.org/abs/1611.09268) introduced large-scale real user
queries paired with answer-bearing passages. BEIR uses the passage retrieval
version as a zero-shot retrieval task: given a web-style query, a system must
rank the passage that answers it. The Japanese NanoBEIR version preserves that
setting through translated questions and passages. The task measures answer
matching for concise search queries, where the answer passage may explain the
concept without repeating the query exactly.

### Observed Data Profile

The task has 50 queries and 5,043 documents. There are 50 positive qrels, so
every query has exactly one positive. Queries are short, averaging 26.66
characters, while documents average 150.35 characters. The examples include a
definition of rumination syndrome, a song performer, a television role, desert
locations, and the meaning of "copper" for police officers. The retrieval
problem is therefore close to ordinary web QA: map a compact question to a
short passage that answers it.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3318, hit@10 = 0.4600, and
Recall@100 = 0.8600. BM25 recovers many positives somewhere in the top 100, but
it struggles to place them in the first 10. Short Japanese queries provide few
lexical anchors, and translated answer passages often use explanatory wording
instead of repeating the exact query. Entity names and quoted titles help, but
definition and meaning questions often require more than term overlap.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4748, hit@10 =
0.7000, and Recall@100 = 0.9800. Dense retrieval is the strongest profile for
this task across all main metrics. The result shows that embedding similarity is
well suited to Japanese MS MARCO-style retrieval, where question intent and
answer passage meaning are more important than exact word repetition. The high
Recall@100 also means dense retrieval is not only better at ordering but also
better at finding the single positive passage.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.3743, hit@10 = 0.5400, and Recall@100 = 0.9400. Three queries use
the rank-101 safeguard. Hybrid retrieval improves over BM25 in top-10 quality
and coverage, but it remains clearly below dense retrieval. This suggests that
lexical signals add some robustness, yet the fused candidate order can promote
surface-term matches that are less answer-bearing than the dense top results.

### Metric Interpretation for Model Researchers

This task is a clear dense-retrieval win. BM25 is useful for candidate recall
but weak for early precision, while dense retrieval provides the best top-10
ranking and the best top-100 coverage. Hybrid search does not outperform dense
here, so its role is mainly as a fallback candidate pool rather than the
preferred first-stage order. Researchers should treat this task as a diagnostic
for short Japanese question-to-answer semantic matching.

### Query and Relevance Type Tendencies

Queries are concise web questions, often asking "what is", "who", or "where".
Relevant passages are short answer snippets or encyclopedia-style statements.
The key difficulty is not broad topic matching but deciding whether the passage
answers the exact question. A passage can share a name or term with the query
and still be irrelevant if it does not provide the requested definition,
identity, or location.

### Representative Failure Modes

BM25 can miss paraphrased answer passages and over-rank documents that repeat a
query term without answering the question. Dense retrieval can retrieve
semantically related but non-answering snippets, especially for ambiguous names
or media titles. Hybrid retrieval can inherit lexical distractors from BM25 and
therefore rank below dense-only retrieval. Because each query has one positive,
small rank errors directly affect nDCG@10.

### Training Data That May Help

Useful training data includes non-overlapping web QA retrieval, Japanese search
query logs, multilingual passage retrieval, and answer-bearing passage pairs.
Hard negatives should share visible query terms but not answer the question.
Training should exclude MS MARCO, BEIR, NanoBEIR, and overlapping translated
passages from this benchmark.

### Model Improvement Notes

Strong models should represent concise Japanese questions as answer intents and
distinguish answer-bearing passages from topical snippets. Improvements should
focus on paraphrase handling, definition and entity-answer matching, and hard
negative separation. Dense retrieval is already the best first-stage profile, so
reranking work should aim to preserve dense recall while improving precision on
ambiguous queries.

## Example Data

| Query | Positive document |
| --- | --- |
| ルミネーション症候群とは何ですか [16 chars] | 反芻症候群。反芻症候群（ルミネーション症候群）は、別名マリシズムとも呼ばれ、食物の再反流を引き起こす、他の特定されていないタイプの摂食障害である。DSM-IVでは特定の摂食障害として明記されていないが、この障害を診断するための一定の基準が示されている。 [126 chars] |
| 「Here I Go Again」を歌ったのは誰ですか？ [28 chars] | 他の用法については、Here I Go Again (曖昧さ回避) を参照してください。『Here I Go Again』は、イギリスのロックバンド、ホワイトスネイクによる楽曲です。もともとは1982年のアルバム『Saints & Sinners』に収録されていましたが、1987年の同名のアルバム『Whitesnake』用に再レコーディングされました。同年に、新たにラジオミックスバージョンとして再レコーディングも行われました。 [215 chars] |
| カメロン・ボイドは『Liv and Maddie』でルーク・ロス役を演じています。 [41 chars] | 皆さんのために最高の笑いを用意しましたよ。4月19日の『リブ・アンド・マディー』のエピソード「プロム・ア・ルーニー」の独占先行映像です。もちろんね。この面白すぎるクリップでは、『ジェシー』のキャメロン・ボイドが別のディズニーショーに登場し、マディー（シェルビー・ウルファート）と出会います。彼のキャラクターは、ええと、かなり個性的なんです！ [170 chars] |

### Public Sources

- [MS MARCO: A Human Generated Machine Reading Comprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated Machine Reading Comprehension Dataset | 2016 | task paper | [https://arxiv.org/abs/1611.09268](https://arxiv.org/abs/1611.09268) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
