# NanoJMTEB-v2 / multi_long_doc_ja

## Overview

`NanoJMTEB-v2 / multi_long_doc_ja` is the Japanese Nano split of
MultiLongDocRetrieval, a long-document retrieval task. Japanese generated
questions must retrieve the full long document that contains the source
evidence. This makes the benchmark very different from short passage, FAQ, or
entity-label retrieval: the query is local, but the indexed unit is a complete
article whose relevant span may be a small part of a much longer text. The Nano
split has 200 queries, 10,000 documents, and one positive document per query.
Current diagnostics show a long-document profile where BM25 is the strongest
top-10 ranker, dense retrieval is weaker, and `reranking_hybrid` improves
coverage beyond both individual profiles while remaining below BM25's top-10
ranking.

## Details

### What the Original Data Measures

The MultiLongDocRetrieval task is associated with the M3-Embedding benchmark
line and is described in JMTEB as a multilingual long-document retrieval dataset
built from sources such as Wikipedia, Wudao, and mC4. The dataset construction
samples lengthy articles, selects paragraphs, and generates questions from
those local paragraph contexts. The retrieval pair then links the generated
question to the full source article.

This construction measures whether a retriever can connect a localized
information need to an entire long document. The relevant evidence may be only
a paragraph or section, but the model must retrieve the article as a whole.
That stresses document representation, truncation policy, and the ability to
avoid being distracted by many unrelated terms inside long documents.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has one positive document, with no multi-positive queries.
Queries average 61.62 characters. Documents average 14,479.43 characters, far
longer than most Nano tasks.

The examples include generated questions about maternal and child health policy
inside a Bolivia article, turquoise production and trade, Ymobile store
operation models, legal risk around Scientology, and transit or stop-location
issues inside a Manhattan article. Several queries preserve generated-question
artifacts, such as lists of possible questions or discourse-dependent phrasing.
This reinforces that the task is not natural web search alone; it is paragraph-
conditioned question-to-full-article retrieval.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5929, hit@10 = 0.7000, and recall@100 = 0.8000. BM25 is
the strongest observed top-10 profile. Long documents contain many lexical
anchors, and generated questions often preserve terms from the source paragraph.
When the decisive phrase, entity, or technical word appears in the long article,
BM25 can locate the source document effectively.

The weakness is recall. BM25 misses one fifth of positives from the first 100
candidates. Long documents also contain many incidental terms, so sparse
matching can rank unrelated articles that share local vocabulary. The result is
still clear: for this Nano split, exact word evidence from generated questions
is highly informative, and lexical retrieval should not be dismissed for long
Japanese documents.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3956, hit@10 = 0.4900, and recall@100 = 0.6800.
Dense retrieval is substantially weaker than BM25 here. The most likely reason
is representation dilution: a single embedding for a very long document must
cover many topics, while the query is tied to a localized paragraph.

Dense retrieval can still help when the query is semantically related to the
article but does not share exact phrasing. However, the current numbers suggest
that the dense model struggles to preserve the evidence-bearing span inside
full-document representations. For model researchers, this task is a warning
that strong short-passage embeddings do not automatically transfer to long-
document retrieval.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 32 safeguard positive rows and a mean of 100.16 candidates. It
achieves nDCG@10 = 0.5008, hit@10 = 0.6250, and recall@100 = 0.8400. The hybrid
profile improves substantially over dense retrieval and gives the best observed
top-100 coverage, but it does not overtake BM25 in top-10 ranking.

This is a useful hybrid-search pattern for long documents. BM25 contributes
paragraph-level lexical anchors that remain highly predictive. Dense retrieval
adds semantically related articles and improves candidate diversity. The hybrid
set is therefore attractive for reranking because it preserves more positives,
but the final ranker must avoid letting broad semantic similarity outrank the
article with the exact source paragraph.

### Metric Interpretation for Model Researchers

Because each query has one positive document, hit@10 measures whether the
source article appears in the first ten results, and nDCG@10 rewards ranking it
near the top. Recall@100 measures whether candidate generation keeps the source
article available for a later reranker.

The metric pattern is important: BM25 is best for top-10 ranking, dense is
weakest, and hybrid is best for recall@100. This means `multi_long_doc_ja`
should be used to evaluate long-document candidate construction, not only final
embedding similarity. A model that looks good on short Japanese passages may
fail when the relevant span is buried in a long article.

### Query and Relevance Type Tendencies

Queries are generated Japanese questions based on local article paragraphs.
Some are natural short questions, while others look like generated lists or
question templates. The relevant document is the full article, not the paragraph
alone. As a result, the positive can contain thousands of characters of context
that are unrelated to the query.

This setup rewards systems that can index long documents in a way that retains
local evidence. Chunking, late interaction, multi-vector document
representations, or paragraph-aware aggregation may be more appropriate than
simple single-vector document embeddings.

### Representative Failure Modes

BM25 can fail when many long documents contain the same local term or named
entity, or when generated wording does not appear cleanly in the article. Dense
retrieval can fail when the full-document embedding is dominated by the
article's broad topic rather than the paragraph that generated the query.
Hybrid retrieval can include both the exact lexical match and several
semantically related long articles, leaving a difficult ranking decision.

Other likely errors include truncating away the evidence-bearing paragraph,
overweighting introductory sections, and confusing full articles that share
entities but differ in the relevant local detail.

### Training Data That May Help

Helpful training data includes Japanese long-document retrieval,
paragraph-generated question to article retrieval, Wikipedia long-article
retrieval, and hard negatives from articles with overlapping entities or
section-level vocabulary. Training should include cases where the relevant span
is not near the beginning of the document.

Comparable benchmark reporting should avoid training on the same
MultiLongDocRetrieval examples used in this Nano split. Synthetic data can help
when generated from non-evaluation long Japanese articles, especially if it
keeps some noisy or discourse-dependent generated questions.

### Model Improvement Notes

Dense retrievers need better long-document representation. Options include
chunk-level retrieval with article aggregation, late-interaction scoring,
multi-vector indexing, long-context encoders, or training objectives that force
the model to retain localized evidence. Sparse systems should preserve Japanese
terms, named entities, and technical phrases because they are strong signals in
this task. Rerankers should inspect the candidate document at a finer granularity
than a single global summary.

For hybrid systems, `multi_long_doc_ja` argues for using BM25 as a serious
component rather than a fallback. Lexical evidence remains powerful when
generated questions inherit source-paragraph wording, while dense evidence is
useful mainly for broadening candidate coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| 国家母子保健政策の具体的な内容は何ですか？ [21 chars] | ボリビア多民族国（ボリビアたみんぞくこく、、、）、通称ボリビアは、南アメリカ大陸西部にある立憲共和制国家。憲法上の首都はスクレだが、ラパスが実質的な首都機能を担っており、議会をはじめとした政府主要機関が所在する。ラパスは標高3600メートルで、世界で最も高所にある首都となっている。 太平洋戦争 (1879年-1884年)で敗れてチリに太平洋海岸部の領土を奪われて以降は内陸国となっており、南西はチリ... [200 / 10,747 chars] |
| トルコ石製品の生産と取引が繁栄した地域について、以下のような質問が考えられます: - トルコ石製品の生産と取引が繁栄した理由は何ですか？ - トルコ石製品の生産と取引が繁栄した地域では、どのような特別... [100 / 418 chars] | トルコ石（トルコいし、turquoise、ターコイズ）は青色から緑色の色を持つ不透明な鉱物。化学的には水酸化銅アルミニウム燐酸塩であり、化学式では CuAl6(PO4)4(OH)8·4H2O と表される。良質のものは貴重であり、宝石とみなされる。 その色合いのために、数千年の昔から装飾品とされてきた。近年では他の多くの不透明の宝石と同様に、表面処理されたものや模造品・合成品が市場に出回っていて問題... [200 / 11,470 chars] |
| ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルについて、以下の質問が考えられます: 1. ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルの違いは何ですか？ 2. ワイモバイルとウィ... [100 / 540 chars] | ワイモバイル株式会社（Ymobile Corporation）は、かつて存在した、日本の電気通信事業者。 2014年7月1日付けでイー・アクセス株式会社から商号変更した。 主にADSL回線の卸売、及びY!mobileのブランド名で移動体通信およびPHSサービスを提供している。2013年1月1日付で一度ソフトバンクの完全子会社となったが、議決権付株式の売却により、同年1月17日から持分法適用関連会社... [200 / 13,385 chars] |
| ジー教会との関係を持つことは、どのような法的リスクを伴いますか？ [32 chars] | サイエントロジー（）は、アメリカの作家L・ロン・ハバードによって考案された一連の信条と実践、および関連する運動である。 概要. カルト、ビジネス、新宗教運動など、さまざまな定義がある。最新の国勢調査によると、アメリカには約25,000人（2008年）、イギリスには約2,300人（2011年）、カナダ（2011年）とオーストラリア（2016年）にはそれぞれ約1,700人のフォロワー がいるとされてい... [200 / 10,635 chars] |
| マンハッタン内部の停留所の設置や案内不足による問題が発生している可能性がありますか？ [42 chars] | マンハッタン（Manhattan、）は、アメリカ合衆国ニューヨーク州ニューヨーク市の地区。 ハドソン川河口部の中州であるマンハッタン島 (Manhattan Island)、あるいは、マンハッタン島が大部分を占めるマンハッタン区 (Manhattan Borough) のことである。ニューヨーク州のニューヨーク郡 (New York County) の郡域もマンハッタン区と同じである。マンハッタン... [200 / 12,229 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval),
  source dataset card.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  Japanese embedding benchmark card.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| mteb/MultiLongDocRetrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval) |
| sbintuitions/JMTEB | 2024 | dataset card | [https://huggingface.co/datasets/sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A generated question asking about national maternal and child health policy. | A full long article about Bolivia where the relevant health-policy material is embedded inside broader country information. |
| A long generated list of possible questions about turquoise production and trade. | A full article about turquoise, including mineral, historical, and trade-related sections. |
| A generated question about Ymobile and Willcom Okinawa store operation models. | A long article about the former Ymobile corporation and related mobile-communication business history. |
| A question about legal risk from a relationship with Scientology. | A long article describing Scientology, its movement, public status, and controversies. |
| A question about stop placement or insufficient guidance inside Manhattan. | A full article about Manhattan containing many sections beyond the local transit-related evidence. |
