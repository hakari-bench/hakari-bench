# MNanoBEIR / NanoBEIR-ja / NanoNQ

## Overview

`NanoBEIR-ja__NanoNQ` is the Japanese NanoBEIR version of Natural Questions, an
open-domain question answering retrieval benchmark based on real Google search
questions and Wikipedia evidence. The task uses Japanese translated questions
as queries and asks a retriever to rank Japanese translated Wikipedia passages
that contain answer evidence. The Nano split contains 50 queries, 5,035
documents, and 57 positive qrels. Most queries have one positive passage, while
7 queries have two. The task is a compact test of short question-to-evidence
retrieval, where dense semantic matching is clearly stronger for top-10 ranking
and hybrid retrieval is strongest for candidate coverage.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced a benchmark
for real information-seeking questions paired with Wikipedia answers and
annotations. BEIR uses NQ as an open-domain QA retrieval task: the system must
retrieve passages likely to contain the answer before any downstream reader or
verifier can answer the question. In this Japanese NanoBEIR version, translated
queries are matched against translated Wikipedia passages. The benchmark
therefore measures answer evidence retrieval under multilingual translation,
short question phrasing, and entity-rich Wikipedia context.

### Observed Data Profile

The task has 50 queries and 5,035 documents. It contains 57 positive qrels,
with 1.14 positives per query on average. The positives-per-query distribution
is 1 minimum, 1.00 median, and 2 maximum, with 14.0% multi-positive queries.
Queries average 42.60 characters, while documents average 243.98 characters.
The examples include event locations, film origins, landmark explanations,
constitutional clauses, and song credits. These are concise information needs
whose relevant passages often answer through surrounding context rather than
through repeated query wording.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.4473, hit@10 = 0.6400, and
Recall@100 = 0.8070. BM25 can use names, titles, and distinctive terms, but it
is limited by the shortness of the queries and by answer paraphrase. A passage
may contain the answer while not sharing many surface terms with the Japanese
translated question. BM25 therefore provides a useful entity-aware baseline but
misses many answer-bearing passages in the top 10.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.6165, hit@10 =
0.8000, and Recall@100 = 0.9298. Dense retrieval is the strongest top-10
profile for this task. The result shows that embedding similarity is well
matched to Natural Questions-style retrieval: it can connect a short question
to a passage that expresses the answer relation, even when the passage uses a
different syntax or includes extra encyclopedic context. Dense retrieval also
substantially improves top-100 coverage over BM25.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5569, hit@10 = 0.7600, and Recall@100 = 0.9649, with no rank-101
safeguard rows. Hybrid retrieval has the best top-100 coverage but is below
dense retrieval on top-10 ranking. This indicates that combining lexical and
dense signals finds more answer evidence overall, while the fused first-stage
order is not as clean as dense-only ranking near the top.

### Metric Interpretation for Model Researchers

This task is useful for separating semantic top-rank quality from candidate
coverage. BM25 underperforms because exact term matching does not capture many
question-answer relations. Dense retrieval is the best initial ranker for
nDCG@10 and hit@10. Hybrid retrieval is the strongest candidate generator for
Recall@100 and is therefore attractive for reranking systems. A model that
improves this task should state whether the gain comes from answer-aware
semantic ranking or from broader candidate recall.

### Query and Relevance Type Tendencies

The examples ask where the Final Four was held, whether a film originated at
Disney, why the Angel of the North is located where it is, where the Three-
Fifths Compromise appears in the Constitution, and who sings on "Somebody's
Watching Me". Relevant passages are short Wikipedia summaries that contain the
answer in context. The retriever must match question intent, not only the
headline entity.

### Representative Failure Modes

BM25 can rank the right entity but the wrong passage, or miss an answer passage
that uses different wording. Dense retrieval can retrieve semantically related
Wikipedia passages that do not contain the exact answer. Hybrid retrieval can
recover more positives in the candidate set while still ranking lexical
distractors above answer-bearing passages. For the few two-positive queries,
retrieving only one evidence passage is another common error.

### Training Data That May Help

Useful training data includes non-overlapping open-domain QA retrieval,
Wikipedia question-passage pairs, Japanese answer retrieval data, and
multilingual QA evidence retrieval. Hard negatives should contain related
entities but not the answer. Training should exclude Natural Questions, BEIR,
NanoBEIR, and overlapping translated Wikipedia passages from this benchmark.

### Model Improvement Notes

Strong systems should represent short Japanese questions as answer-seeking
intents while retaining enough entity sensitivity to avoid broad topical
matches. Dense retrieval is already the strongest top-10 profile, so reranking
experiments should use the hybrid pool to recover additional evidence and then
restore answer-focused ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| 今年のファイナルフォーはどこで開催されますか [22 chars] | 2018年のNCAAディビジョンI男子バスケットボール選手権は、2017–18年シーズンの全米大学体育協会（NCAA）ディビジョンI男子大学バスケットボールの全国王者を決定するための68チームによるシングルエリミネーション方式のトーナメントであった。第80回大会は2018年3月13日に始まり、4月2日にテキサス州サンアントニオのアラモドームで行われた決勝戦をもって終了した。 [188 chars] |
| 『ナイトメア・ビフォア・クリスマス』はもともとディズニーの映画だったのか？ [37 chars] | 『ナイトメア・ビフォア・クリスマス』は、1982年にティム・バートンがウォルト・ディズニー・フィーチャー・アニメーションでアニメーターとして働いていた際に書いた詩が起源である。同年に『ヴィンセント』が成功したことで、ウォルト・ディズニー・スタジオは『ナイトメア・ビフォア・クリスマス』を短編映画または30分のテレビ特別番組として制作することを検討し始めた。その後数年間、バートンは定期的にこのプロジェ... [200 / 326 chars] |
| なぜ「北の天使」はそこに存在するのか [18 chars] | ゴームリーによれば、天使の意義は三つある。第一に、その建造地の地下で炭鉱労働者が2世紀にわたり働いていたことを象徴すること。第二に、産業時代から情報時代への移行を捉えること。第三に、私たちの変化する希望と恐怖の焦点となることである。[2] [119 chars] |
| 3分の5妥協は、アメリカ合衆国憲法の第1条第2節第3項に最初に記述されています。 [40 chars] | 三人のうち五分の三の妥協は、アメリカ合衆国憲法第1条第2項第3項に記載されており、その内容は以下の通りである： [55 chars] |
| 「Somebody's Watching Me」でマイケル・ジャクソンが参加しているのは、ロッキー・ローランド（Rockwell）です。マイケル・ジャクソンはこの曲のバックボーカルを務めています。 [98 chars] | 「Somebody's Watching Me」は、アメリカの歌手ロクウェルが自身のデビュースタジオアルバム『Somebody's Watching Me』（1984年）から発表した楽曲である。この曲は1984年1月14日にモータウンから、ロクウェルのデビューシングルおよびアルバムのリードシングルとしてリリースされた。曲には元ジャクソン5のメンバーであるマイケル・ジャクソン（コーラスでのボーカル）... [200 / 235 chars] |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | [https://aclanthology.org/Q19-1026/](https://aclanthology.org/Q19-1026/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
