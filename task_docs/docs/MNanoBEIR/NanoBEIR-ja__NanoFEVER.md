# MNanoBEIR / NanoBEIR-ja / NanoFEVER

## Overview

`NanoBEIR-ja__NanoFEVER` is the Japanese NanoBEIR version of FEVER, a fact
verification evidence retrieval benchmark. The task uses Japanese translated
claims as queries and asks a retriever to rank Japanese translated Wikipedia
passages that contain evidence for verification. The Nano split contains 50
queries, 4,996 documents, and 57 positive qrels. Most claims have one positive
evidence passage, while 6 queries have multiple positives. The task is a compact
test of claim-to-Wikipedia retrieval: exact entity and title overlap are very
useful, but the strongest top-ranking result comes from dense semantic matching.

## Details

### What the Original Data Measures

[FEVER](https://arxiv.org/abs/1803.05355) introduced a large-scale fact
extraction and verification dataset built from claims and Wikipedia evidence.
The original benchmark includes support, refute, and not-enough-information
labels, but BEIR evaluates the retrieval step: before a verifier can classify a
claim, the system must retrieve the evidence passage. In this Japanese NanoBEIR
version, translated claims are matched against translated Wikipedia passages,
so the task tests entity-aware retrieval, paraphrase robustness, and evidence
selection under multilingual translation.

### Observed Data Profile

The task has 50 queries and 4,996 documents. It contains 57 positive qrels, with
1.14 positives per query on average. The positives-per-query distribution is 1
minimum, 1.00 median, and 3 maximum, and only 12.0% of queries are
multi-positive. Queries are short claims averaging 27.72 characters, while
documents are longer Wikipedia passages averaging 581.95 characters. The
examples cover music groups, television series, locations, historical persons,
and films. Many claims contain a named entity plus a predicate that must be
checked against the evidence passage.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.6797, hit@10 = 0.8000, and
Recall@100 = 0.9298. This is a strong lexical profile. FEVER claims often
include entity names, titles, or distinctive phrases that also appear in
Wikipedia evidence, so BM25 can recover many positives in the candidate set.
However, the top-10 hit rate and nDCG leave room for semantic matching because
the evidence passage may express the claim indirectly, include translated title
variation, or require matching a predicate rather than only the entity name.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.7141, hit@10 =
0.8800, and Recall@100 = 0.8947. Dense retrieval is the best top-10 ranking
profile for this task, even though its Recall@100 is below BM25. This indicates
that embedding similarity is especially useful for placing answer-bearing
evidence higher once it is semantically aligned with the claim. The tradeoff is
that dense retrieval can miss some positives that BM25 catches through exact
entity or title overlap.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.6482, hit@10 = 0.8800, and Recall@100 = 0.9825. One query uses the
rank-101 safeguard. Hybrid retrieval is the strongest profile for top-100
coverage and ties dense retrieval on hit@10, but its nDCG@10 is lower than both
BM25 and dense. This means the hybrid candidate pool is excellent for
downstream reranking, while the fused order itself can place some relevant
evidence lower than a dense-first ranking would.

### Metric Interpretation for Model Researchers

This task separates three useful behaviors. BM25 is strong for candidate recall
because FEVER claims often name the relevant entity directly. Dense retrieval is
strong for top-rank evidence ordering because it captures the semantic relation
between claim and passage. Hybrid retrieval is best for Recall@100, making it
the safest candidate source for reranking systems. A model improvement should
therefore be described in terms of whether it improves exact entity recall,
semantic evidence ordering, or hybrid candidate reranking.

### Query and Relevance Type Tendencies

The examples include claims such as a musician knowing the Grateful Dead, a
television program being a sitcom, aircraft being built in Burbank, Nero being a
person, and a film not being exclusively German. Relevant documents are
Wikipedia-style passages that contain the entity context needed to verify the
claim. Often the evidence is not limited to a single sentence, so passage-level
retrieval must rank documents by both entity match and predicate relevance.

### Representative Failure Modes

BM25 can over-rank the right entity page when the page does not support the
specific predicate in the claim. Dense retrieval can retrieve semantically
related pages that discuss the same broad topic but miss the exact evidence.
Hybrid retrieval can recover more positives in the top 100 but still produce a
noisy order when lexical and dense signals disagree. Since most queries have a
single positive, top-rank mistakes have a large effect on nDCG@10.

### Training Data That May Help

Useful training data includes non-overlapping FEVER-style claim-evidence pairs,
Wikipedia evidence retrieval, Japanese fact-checking data, and multilingual
claim verification. Hard negatives should come from the same entity page,
nearby entities, or pages that share the title but do not verify the predicate.
Training should exclude FEVER, BEIR, NanoBEIR, and overlapping translated
Wikipedia evidence from this benchmark.

### Model Improvement Notes

Strong systems should preserve entity-name recall while learning to rank the
passage that actually verifies the claim. Dense models need hard negatives that
distinguish the right entity from the right evidence. Hybrid pipelines should
use their high candidate coverage as input to a reranker that can recover dense
semantic ordering without losing BM25's exact-match positives.

## Example Data

| Query | Positive document |
| --- | --- |
| キース・ゴドーショウはグレイトフル・デッドをよく知っていた。 [30 chars] | グレイトフル・デッドは、1965年にカリフォルニア州パロアルトで結成されたアメリカのロックバンドである。クインテットからセプテットまでメンバー数が変化したこのバンドは、ロック、サイケデリカ、実験音楽、モードジャズ、カントリー、フォーク、ブルーグラス、ブルース、レゲエ、スペース・ロックなどの要素を融合した独自で多彩なスタイル、長時間にわたるインストゥルメンタル・ジャムのライブ演奏、そして「デッドヘッ... [200 / 1,564 chars] |
| 『ターラク・メータのオルター・チャシュマ』はシットコムである。 [31 chars] | 『ターラク・メータのオルター・チャシュマー』（英語: Taarak Mehta's Different Perspective）は、ニーラ・テレ・フィルムズ・プライベート・リミテッドが制作するインドで最も長く放送されているシットコムシリーズである。この番組は2008年7月28日に初放送された。毎週月曜日から金曜日まで午後8時30分に放送され、SAB TVでは午後11時と翌日午後3時の再放送も行われ... [200 / 344 chars] |
| カリフォルニア州バーバンクでは、極秘かつ技術的に高度な飛行機が製造されていた。 [39 chars] | バーバンクは、アメリカ合衆国カリフォルニア州南部、ロサンゼルス郡にある都市で、ロサンゼルス中心部から西北西約12マイル（約19キロ）の位置にある。2010年の国勢調査では人口は103,340人であった。「世界のメディア首都」と称され、ハリウッドからわずか数マイルの北東に位置するこの都市には、ザ・ウォルト・ディズニー・カンパニー、ワーナー・ブラザース・エンターテインメント、ニコロデオン・アニメーショ... [200 / 742 chars] |
| ネロは人物です。 [8 chars] | ユリオ＝クラウディウス朝という用語は、最初の5人のローマ皇帝、すなわちアウグストゥス、ティベリウス、カリグラ、クラウディウス、ネロ、あるいは彼らが属していた家系を指す。彼らは、紀元前1世紀後半（44年／31年／27年）にアウグストゥスの下でローマ帝国が成立してから、紀元68年に最後の皇帝ネロが自殺するまで、帝国を統治した。ユリオ＝クラウディウス朝の歴史において、長子相続は顕著に見られない。アウグス... [200 / 930 chars] |
| 『スクリーム2』は独占的にドイツ映画である。 [22 chars] | 『スクリーム2』は、ウェス・クレイヴン監督、ケヴィン・ウィリアムソン脚本による1997年のアメリカのスラッシャー映画である。デヴィッド・アーキェット、ネヴ・キャンベル、コートニー・コックス、サラ・ミシェル・ゲラー、ジェイミー・ケネディ、ローリー・メトカーフ、ジェリー・オコンネル、ジャーダ・ピンケット、リーヴ・シュライバーが出演している。本作はディメンション・フィルムズにより1997年12月12日に... [200 / 1,222 chars] |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
