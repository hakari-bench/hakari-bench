# NanoMLDR / ja

## Overview

`NanoMLDR / ja` is the Japanese split of NanoMLDR, a multilingual
long-document retrieval benchmark derived from MLDR. Japanese paragraph-grounded
questions retrieve full Japanese articles, where the answer-bearing paragraph is
embedded inside a longer document. The Nano split has 148 queries, 3,112
documents, and 148 positive qrel rows, with exactly one positive document per
query. Current diagnostics show BM25 as the strongest profile, dense retrieval
as substantially weaker, and `reranking_hybrid` as recovering much of the BM25
coverage while not matching BM25 top-rank quality.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The retrieval target is the full article containing the answer-bearing
paragraph.

For Japanese, this evaluates whether a retrieval model can connect a detailed
Japanese question to the correct full article rather than only to a short
passage. The relevant evidence can be local, while the indexed document is long
and may cover many adjacent topics.

### Observed Data Profile

The Nano split contains 148 queries, 3,112 documents, and 148 positive qrel
rows. Every query has exactly one positive document. Queries average 51.70
characters, while documents average 5,384.62 characters.

Observed examples include questions about teacher license renewal, military
aircraft development, Umayyad taxation, juvenile novels, game music, climbing,
tanks, criminal justice, television programs, and military organization. The
positive documents are Japanese long articles containing the paragraph that
generated each question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7589, hit@10 = 0.8446, and recall@100 = 0.9189. BM25 is
the strongest observed retrieval profile for this split. Many Japanese
questions preserve distinctive article terms, title fragments, names, works,
institutions, or technical expressions from the answer-bearing paragraph.

This makes lexical matching highly useful despite the long-document setting.
Japanese tokenization still matters: terms may be segmented differently, and
shared named entities can create hard negatives. Even with those constraints,
the BM25 ranking places the single positive near the top for a large majority
of queries.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.5014, hit@10 = 0.5946, and recall@100 = 0.7838.
Dense retrieval is much weaker than BM25 here. It captures broad embedding
similarity, but the task often depends on a specific paragraph inside a full
article.

For Japanese long documents, a single dense representation can dilute the
answer-bearing clue. Articles about the same historical period, literary work,
military technology, education system, or cultural product may be semantically
close, while only one article contains the paragraph that generated the query.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 14 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.6452, hit@10 = 0.7432, and recall@100 = 0.9054. Hybrid retrieval improves
substantially over dense retrieval and nearly recovers BM25 recall@100, but it
still remains below BM25 for top-rank quality.

This suggests that the hybrid candidate pool is useful for reranking pipelines:
it combines lexical and embedding evidence and keeps most positives available.
However, the sparse signal is strong enough that blending dense candidates can
move the positive lower than BM25 alone for some queries.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the positive document's exact rank, and recall@100 measures
whether the positive remains available to a downstream reranker.

The Japanese profile is a lexical-anchor-heavy long-document task. A model that
performs well should preserve exact Japanese terms and named entities while
also handling paraphrase across the query and answer paragraph. Dense results
should be interpreted against the strong BM25 baseline, not in isolation.

### Query and Relevance Type Tendencies

Queries are Japanese paragraph-grounded questions about education, history,
military systems, literature, games, entertainment, law, sports, and public
institutions. They often contain a specific condition, title, organization, or
named entity that points to a particular paragraph.

Relevant documents are full Japanese articles. The answer-bearing paragraph may
be a small part of the document, so good retrieval requires both document-level
coverage and paragraph-level evidence recognition.

### Representative Failure Modes

Dense retrieval can return an article that is topically related but lacks the
exact answer-bearing paragraph. This is likely when multiple Japanese articles
share the same period, work, institution, aircraft, legal concept, or cultural
topic. BM25 can fail when tokenization splits important Japanese terms poorly or
when several documents share the same rare title or entity.

Hybrid retrieval can keep the positive in the candidate pool but rank a related
article above it. Rerankers should therefore inspect the local paragraph
evidence rather than relying only on a full-document embedding or title-level
similarity.

### Training Data That May Help

Useful training data includes Japanese long-document QA retrieval pairs,
Japanese Wikipedia article retrieval, multilingual MLDR training data outside
this Nano split, and Japanese hard negatives that share titles, named entities,
or domain vocabulary. Training should include cases where the positive is a
full article selected because one paragraph answers the question.

Synthetic data can help when it samples paragraphs from long Japanese
encyclopedic articles, generates grounded Japanese questions, and uses the full
article as the positive. Negatives should be neighboring Japanese articles that
share entities or topic labels but do not contain the answer paragraph.

### Model Improvement Notes

Dense retrievers should consider chunked indexing, late interaction,
paragraph-aware pooling, or multi-vector document representations so that local
evidence is not lost in a full-document vector. Sparse systems should preserve
Japanese lexical anchors and use robust tokenization. Rerankers should be
validated against BM25 because the lexical baseline is the strongest observed
top-rank signal.

For hybrid systems, `NanoMLDR / ja` is a useful check that hybrid search
improves dense-only retrieval while preserving BM25-style exact-match strength.
The current `reranking_hybrid` profile is close to BM25 in recall but still
leaves room for better top-rank reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| 員免許更新制の廃止により、教育における免許状の効力がどのように変化するのかについて、雇用者が評価を上げる方針をとる場合、人物面の評価においてプラスの評価をする理由は何ですか？ [87 chars] | 日本における教育職員免許状（きょういくしょくいんめんきょじょう）とは、就学前教育・初等教育・中等教育などにかかわる教育職員に就くための資格要件とされている、教育職員免許法に基づく免許状のことである。「教員免許」「免状」「教免」「教状」などと略して呼ばれることがある。 現代の日本においては、学校教員の職に必要な免許状のみがあり、学校教員の免許状は、教員免許状（きょういんめんきょじょう）とも呼ばれる。... [200 / 10,839 chars] |
| 軍はなぜ零戦の後継機である烈風の試作途中段階に留まっていたのか、その理由は何ですか？ [42 chars] | 紫電改（しでんかい）は、太平洋戦争期における大日本帝国海軍の戦闘機である。紫電（N1K1-J）の二一型以降が紫電改と呼称される。この項では紫電改と紫電をまとめて紹介する。 局地戦闘機紫電は、水上戦闘機「強風」を陸上戦闘機化したもので、紫電二一型は強風にちなんだ中翼配置の紫電を低翼に再設計した機体であり、紫電改は新機軸の設計（自動空戦フラップ、層流翼）が特徴であった。この機体は後述するように日本海軍... [200 / 10,836 chars] |
| ましたが、南北アラブの対立が税収の減少につながった理由は何ですか？ [33 chars] | ウマイヤ朝（ウマイヤちょう、、al-Dawla al-Umawiyya）は、イスラム史上最初の世襲イスラム王朝である。大食（唐での呼称）、またはカリフ帝国やアラブ帝国と呼ばれる体制の王朝のひとつであり、イスラム帝国のひとつでもある。 イスラームの預言者ムハンマドと父祖を同じくするクライシュ族の名門で、メッカの指導層であったウマイヤ家による世襲王朝である。第4代正統カリフであるアリーとの抗争において... [200 / 11,106 chars] |
| 『時をかける少女』以来のジュブナイル小説を発表することに戻った理由は何ですか？ [39 chars] | は、日本の小説家・劇作家・俳優である。ホリプロ所属。身長166cm。兵庫県神戸市垂水区在住。 大阪市に生まれた。天王寺動物園長だった父の影響を受け、幼い頃から博物的な世界に憧れを持つ。同志社大学に入学し、美学・美術史を専攻。 1965年に東京に転居し、本格的な作家活動を展開、第一短編集『東海道戦争』（1965年）を刊行した。同年、『時をかける少女』『48億の妄想』では、現実と非現実をつなぐ幻想のリ... [200 / 11,047 chars] |
| 「Love Song 探して」のBGMでは、ポルタメントが多用されていますか？ [39 chars] | 『ドラゴンクエストII 悪霊の神々』（ドラゴンクエストツー あくりょうのかみがみ）は、1987年1月26日に株式会社エニックス（現：株式会社スクウェア・エニックス）より発売されたファミリーコンピュータ用ロールプレイングゲーム。 ドラゴンクエストシリーズの第2作目。前作『ドラゴンクエスト』（1986年発売）から100年後、邪教の教祖によって破られた世界の平和を、勇者ロトの血を引く前作の主人公の子孫3... [200 / 10,767 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Japanese question about teacher license renewal and evaluation. | A long article about Japanese education staff licenses. |
| A question about why a fighter aircraft successor remained in prototype development. | A long article about a Japanese military aircraft. |
| A question about taxation and Arab political conflict. | A long article about the Umayyad Caliphate. |
| A question about returning to juvenile fiction after a particular work. | A long article about a Japanese writer or cultural figure. |
| A question about portamento in a game music track. | A long article about a Japanese role-playing game. |
