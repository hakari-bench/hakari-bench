# MNanoBEIR / NanoBEIR-ja / NanoHotpotQA

## Overview

`NanoBEIR-ja__NanoHotpotQA` is the Japanese NanoBEIR version of HotpotQA, a
multi-hop question answering benchmark. The task uses Japanese translated
questions and asks a retriever to rank Japanese translated Wikipedia paragraphs
that contain the supporting evidence. The Nano split contains 50 queries, 5,090
documents, and 100 positive qrels. Every query has exactly two positives. This
fixed two-support structure makes the task useful for studying whether a model
can retrieve both evidence pieces needed for a multi-hop answer rather than
only the passage with the most obvious entity overlap.

## Details

### What the Original Data Measures

[HotpotQA](https://arxiv.org/abs/1809.09600) was designed for explainable
multi-hop question answering with supporting facts. BEIR treats it as evidence
retrieval: the model receives a question and must rank Wikipedia passages that
contain the supporting information. In this Japanese NanoBEIR version, the
retrieval task is exposed through translated questions and translated passages.
The benchmark measures whether a retriever can connect named entities,
relations, and bridge facts across multiple passages.

### Observed Data Profile

The task has 50 queries and 5,090 documents. It contains 100 positive qrels, and
each query has exactly two positives. Query length averages 46.56 characters,
while documents are short Wikipedia-style paragraphs averaging 184.71
characters. The examples include actors and sitcoms, historical figures and
objects, film creators and composers, sports events, and music groups. Because
documents are short, a relevant support passage can be missed if the retriever
locks onto only one entity in the question.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5296, hit@10 = 0.7600, and
Recall@100 = 0.8200. BM25 benefits from named entities, titles, and distinctive
surface forms in the question, but it is the weakest of the three profiles. The
multi-hop structure makes exact term frequency fragile: the first support may
share many words with the query, while the second support may be connected by a
relationship or bridge entity that is less lexically explicit. Japanese
translation and transliteration variation can further reduce exact overlap.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.6885, hit@10 =
0.9400, and Recall@100 = 0.9000. Dense retrieval is the strongest top-10
profile for this task. The large gap over BM25 indicates that embedding
similarity is helpful for mapping multi-hop questions to passages that express
the answer relation without repeating all query terms. Dense retrieval is
particularly strong at finding at least one relevant support near the top, and
its nDCG@10 suggests that it orders the best evidence more effectively than
lexical matching alone.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.6354, hit@10 = 0.9000, and Recall@100 = 0.9500. One query uses the
rank-101 safeguard. Hybrid retrieval has the best top-100 coverage, while dense
retrieval remains best for top-10 ranking. This means the hybrid candidate pool
is especially valuable for downstream reranking because it recovers more of the
two-support evidence set, even if the fused initial order is not as strong as
dense alone.

### Metric Interpretation for Model Researchers

This task highlights a useful split between semantic ranking and evidence
coverage. Dense retrieval is best when judging the initial top 10, showing that
semantic representations are critical for Japanese multi-hop QA retrieval.
Hybrid retrieval is best at Recall@100, showing that lexical and dense signals
together recover more supporting passages. BM25 is still informative as a
named-entity baseline, but it underperforms when evidence depends on a bridge
relation. Researchers should check whether a model retrieves both positives,
not just whether it finds one answer-bearing passage.

### Query and Relevance Type Tendencies

The examples ask for linked facts: which actor appeared with Penny Rae Bridges,
who gave a Muramasa sword to Kaganoi Shigemochi, which film connects Joby
Harold and Samuel Sim, when a specific college football game occurred, and what
name a rock band uses for country shows. These questions contain surface
anchors, but the answer often depends on a second passage. Relevance is
therefore relational, not merely topical.

### Representative Failure Modes

BM25 can retrieve the most obvious entity page and miss the second support.
Dense retrieval can retrieve semantically related pages that explain the topic
but omit one required fact. Hybrid retrieval can recover more positives but may
still rank only one support high enough for practical use. For analysis, errors
should be separated into missing-first-hop, missing-second-hop, and near-miss
semantic distractor cases.

### Training Data That May Help

Useful training data includes non-overlapping multi-hop QA retrieval pairs,
Wikipedia evidence selection, Japanese question-to-passage retrieval, and
multilingual multi-hop evidence data. Hard negatives should include one-hop
partial matches that mention one entity but do not complete the reasoning
chain. Training should exclude HotpotQA, BEIR, NanoBEIR, and overlapping
translated support paragraphs.

### Model Improvement Notes

Strong systems should combine entity anchoring with relation-aware semantic
matching. Candidate generation should be judged by whether both positives are
available, while reranking should prioritize complete evidence chains. Dense
models that already perform well at top-10 ranking can still improve by
increasing second-support coverage, where hybrid candidate generation currently
has the advantage.

## Example Data

| Query | Positive document |
| --- | --- |
| Penny Rae Bridgesは、どの他の俳優と共演してテレビのシットコムに出演しましたか？ [48 chars] | ペニー・レイ・ブリッジズ（1990年7月29日生まれ）はアメリカの女優である。テレビ番組では、「フォア・ユア・ラブ」、「ファミリー・ロー」、「ボーイ・ミーツ・ワールド」、「ザ・ペアレント・フッド」などに出演している。彼女は「ハーフ＆ハーフ」で若いモナを演じた役で最も知られている。 [140 chars] |
| 誰が村正派を創設した人物が作った刀を加賀野井重持に授けたのか？ [31 chars] | 加賀井重望（かがのい しげもち、1561年 - 慶長5年8月27日（1600年8月27日））は、安土桃山時代の日本の武士で、織田氏に仕えた。加賀井城を治めた。小牧・長久手の戦いでは、父重宗の配下として織田信雄の軍勢に属して戦った。その後間もなく、加賀井城は豊臣秀吉の軍勢に包囲され、重宗は降伏。重望は秀吉に召し抱えられ、使者として仕え、1万石の知行を賜った。また、1598年に秀吉から名刀村正を下賜されている。 [205 chars] |
| ジョビー・ハロルドが脚本と監督を担当し、サミュエル・シムが音楽を手掛けた映画はどれですか？ [45 chars] | サミュエル・シムは、映画およびテレビの作曲家である。彼はBBCドラマシリーズ『ダンケルク』の受賞歴を持つ楽曲で初めて注目を集めた。以来、さまざまな映画やテレビ番組の音楽を手がけており、最近では、ザ・ワインスタイン・カンパニーの映画『目覚めの時』や、BBC／HBO共同制作のドラマシリーズ『サダムの一族』の音楽を担当した。彼の最新の称賛された作品は、テレビシリーズ『ホーム・ファイアーズ』のサウンドトラックである。『ホーム・ファイアーズ（テレビシリーズ音楽）』は2016年5月6日、ソニー・クラシカル・レコードから発売された。 [262 chars] |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | [https://arxiv.org/abs/1809.09600](https://arxiv.org/abs/1809.09600) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
