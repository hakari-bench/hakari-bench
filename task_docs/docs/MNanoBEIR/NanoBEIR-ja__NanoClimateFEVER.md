# MNanoBEIR / NanoBEIR-ja / NanoClimateFEVER

## Overview

`NanoBEIR-ja__NanoClimateFEVER` is the Japanese NanoBEIR version of
CLIMATE-FEVER, a climate-science fact-checking retrieval benchmark. The task
uses Japanese translated climate claims as queries and asks a retriever to rank
Japanese translated evidence passages. The Nano split contains 50 queries,
3,408 documents, and 148 positive qrels. Most queries have multiple evidence
passages: the average is 2.96 positives per query, and 44 of 50 queries are
multi-positive. This makes the task a compact test of claim-to-evidence
retrieval in climate science, where lexical terms are useful but scientific
context and paraphrase are necessary for robust ranking.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) extends the FEVER-style claim
verification setting to climate change claims. The original task links claims to
evidence passages that support, refute, or provide relevant context for the
claim. BEIR uses it as a fact-checking retrieval task, and the Japanese NanoBEIR
version preserves the retrieval problem after translation. A system must find
evidence for climate claims involving temperature trends, sea level, ice melt,
extreme weather, methane release, renewable energy, or attribution.

### Observed Data Profile

The task has 50 queries and 3,408 documents. It contains 148 positive qrels,
with positives per query ranging from 1 to 5 and a median of 3.00. Query length
averages 57.50 characters, while documents average 665.96 characters. The
queries are shorter than the evidence passages and often state a claim in a
compressed form. The positive documents are explanatory encyclopedia-style
passages or scientific summaries. This means the retriever has to bridge from a
claim to evidence-bearing context rather than simply match a question to a
direct answer.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.2672, hit@10 = 0.6800, and
Recall@100 = 0.5338. BM25 benefits when climate terms, named phenomena, dates,
or technical phrases are preserved in both claim and evidence. However, the
score profile shows that exact term overlap is not enough. Climate claims can
be paraphrased, evidence passages may discuss a broader scientific mechanism,
and translated Japanese wording can differ between the claim and the passage.
BM25 finds some evidence, but it often fails to cover all relevant passages for
multi-positive claims.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.2839, hit@10 =
0.6800, and Recall@100 = 0.5878. Dense retrieval improves ranking quality and
top-100 coverage over BM25 while matching BM25 on hit@10. This suggests that
embedding similarity helps with climate-science paraphrase and broader evidence
matching, especially when a passage explains the same phenomenon with different
surface wording. The dense advantage is moderate rather than overwhelming,
which indicates that precise scientific terms still carry important signal.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.3100, hit@10 = 0.7400, and Recall@100 = 0.6149. Three queries use
the rank-101 safeguard. Hybrid retrieval is strongest across all three reported
metrics. This is the expected pattern for climate fact-checking retrieval:
lexical matching keeps important terms such as sea level, methane, ice, or
specific events grounded, while dense retrieval adds evidence that is
semantically related but lexically different. The hybrid profile is therefore
the best proxy for a practical first-stage retrieval pool.

### Metric Interpretation for Model Researchers

This task shows a clear hybrid advantage. BM25 alone is limited by paraphrase
and evidence-context mismatch, while dense retrieval alone improves coverage but
does not fully replace term-sensitive matching. `reranking_hybrid` provides the
best top-10 ranking and the best top-100 evidence coverage. Researchers should
interpret improvements in this task as evidence that a model can combine
scientific terminology with claim-level semantic matching. Since most queries
have multiple positives, coverage across evidence variants is as important as
finding one obvious passage.

### Query and Relevance Type Tendencies

The examples include claims about historical warming periods, statistically
significant trends, local sea-level variability, hurricane impacts, and CERN
CLOUD claims about cosmic rays. Relevant passages may not explicitly repeat the
claim; they may describe the underlying climate mechanism, summarize the
scientific consensus, or provide context that supports or refutes the claim.
This makes evidence retrieval sensitive to both factual specificity and topic
scope.

### Representative Failure Modes

BM25 can over-rank passages that repeat a climate term but do not address the
claim's specific assertion. Dense retrieval can find broad climate-change
passages that are topically related but not valid evidence for the claim.
Hybrid retrieval can still fail when both signals favor a general topic page
over a narrower evidence passage. Multi-positive queries also expose coverage
failures when a system retrieves only one type of evidence and misses other
supporting or contextual passages.

### Training Data That May Help

Useful training data includes non-overlapping climate claim-evidence pairs,
scientific fact-checking retrieval, environmental science QA, and multilingual
claim verification data. Hard negatives should share climate terminology but
fail to support or refute the exact claim. Training should exclude
CLIMATE-FEVER, BEIR, NanoBEIR, and overlapping translated evidence passages from
this benchmark.

### Model Improvement Notes

Strong systems should combine climate terminology, claim decomposition, and
evidence-context matching. Candidate generation should preserve exact matches
for technical terms and events, while ranking should recognize when a passage
actually bears on the claim. For reranking experiments, this task is useful for
testing whether hybrid candidates can be reordered into evidence-focused
results rather than broad climate-topic results.

## Example Data

| Query | Positive document |
| --- | --- |
| 1970年から1998年まで、約0.7°Fの温度上昇をもたらした温暖化期間があり、これが地球温暖化懸念派の運動の発展を後押しした。 [65 chars] | ペレオセーン（-LSB- 発音：ˈpæliəˌsiːn、_ ˈpæ -、_ -lɪoʊ - -RSB-）またはパレオセーン（「古き新生」）は、約から続いた地質時代の区分である。これは、新生代の現代的な古第三紀における最初の世である。多くの地質時代と同様に、この世の始まりと終わりを定義する地層は明確に特定されているが、正確な年代は依然として不確実である。 ペレオセーン世は地球の歴史における2つの主要... [200 / 508 chars] |
| 実際、統計的に有意ではないが、傾向は下方に向かっている。 [28 chars] | 太陽周期または太陽磁気活動周期とは、太陽の活動（太陽放射量や太陽物質の放出レベルの変化）および外観（太陽黒点の数や大きさ、太陽フレア、その他の現象の変化）におけるほぼ周期的な11年周期の変動を指す。これらの変動は、太陽の外観の変化や地球上で観測されるオーロラなどの現象を通じて、何世紀にもわたって観測されてきた。太陽の変化は、宇宙空間、大気、および地球表面にさまざまな影響を及ぼす。太陽活動における主... [200 / 228 chars] |
| 局所的および地域的な海面レベルは、引き続き典型的な自然変動を示しており、ある場所では上昇し、他の場所では下降している。 [59 chars] | 平均海面（MSL）（単に「海面」と略されることもある）とは、地球の海洋の表面の平均的なレベルであり、標高などの高さを測定する基準となるものである。MSLは、垂直方向のデatum（垂直デatum）の一種であり、地図作成や海洋航法における図法基準面（チャートデatum）や、航空分野において大気圧を測定して高度を較正し、結果として航空機の飛行高度を決定するための標準海面として用いられる。ある特定の地点に... [200 / 418 chars] |
| [気候科学者ら]は、ハービー台風の事例のいくつかの側面が、地球温暖化が悪い状況をさらに悪化させていることを示唆していると述べている。 [66 chars] | 地球温暖化の影響とは、温室効果ガスの人為的排出によって（直接的または間接的に）引き起こされる環境的および社会的変化を指す。気候変動が実際に進行しており、その主な原因が人間の活動であるという点については、科学的な合意が存在する。すでに観測されている気候変動の影響には、氷河の後退、季節イベントの時期の変化（例：植物の開花時期の前倒し）、農業生産性の変化などがある。 気候変動の将来の影響は、気候変動政策... [200 / 507 chars] |
| CERNのCLOUD実験は、宇宙線が地球温暖化の原因であるとするために必要な4つの条件のうち、4つのうち1つだけの3分の1しか検証しておらず、残りの条件のうち2つはすでに否定されている。 [93 chars] | 最近の気候変動の原因究明とは、地球上で見られる最近の気候変動、いわゆる「地球温暖化」の背後にある仕組みを科学的に明らかにしようとする試みである。この取り組みは、記録が最も信頼できる観測温度記録期間、特に過去50年間に注目している。この期間は人間活動が急速に拡大した時期であり、対流圏の観測データが得られるようになった時期でもある。主要な仕組みは人為的、すなわち人間の活動に起因するものであり、以下の通... [200 / 813 chars] |

### Public Sources

- [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER | 2020 | task paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
