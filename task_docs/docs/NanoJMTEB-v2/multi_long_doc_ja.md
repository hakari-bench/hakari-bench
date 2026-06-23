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
| 国家母子保健政策の具体的な内容は何ですか？ [21 chars] | ボリビア多民族国（ボリビアたみんぞくこく、、、）、通称ボリビアは、南アメリカ大陸西部にある立憲共和制国家。憲法上の首都はスクレだが、ラパスが実質的な首都機能を担っており、議会をはじめとした政府主要機関が所在する。ラパスは標高3600メートルで、世界で最も高所にある首都となっている。 太平洋戦争 (1879年-1884年)で敗れてチリに太平洋海岸部の領土を奪われて以降は内陸国となっており、南西はチリ、北西はペルー、北東はブラジル、南東はパラグアイ、南はアルゼンチンと国境を接する。 概要. 国土面積は約110万平方キロメートルで、日本の約3.3倍。アメリカ大陸では8番目に、ラテンアメリカでは6番目に、世界的には27番目に大きい国であるが、上記のように領土を隣国に奪われる前はさらに広かった。ボリビアは太平洋岸領土の奪還を諦めておらず、チチカカ湖や河川で活動するボリビア海軍（兵力4800人）を保持しているほか、3月23日を海の日 (ボリビア)と定め、国際司法裁判所に提訴（2018年に「チリは交渉に応じる義務はないが、善隣の精神に基づいた対話継続を妨げない」との判断が示された）するなどしている。 南半球にあり、晴れていれば南十字星が見える。 かつて「黄金の玉座に座る乞食」と形容されたように、豊かな天然資源を持つにもかかわらず実際には貧しい状態が続いており、現在もラテンアメリカ貧国の一つである。推定1万4000人の日系ボリビア人がおり、日本人町もある。 国名. 公用語による正式名称は、スペイン語で 。公式のケチュア語表記は , 公式のアイマラ語表記は である。通称は 。 2009年3月18日に、それまでの（ボリビア共和国）から現国名へ変更した。 公式の英語表記は 。通称は となっている。 日本語の表記は、ボリビア多民族国。通称は、ボリビア。また、ボリヴィアとも表記される。また公式ではないが、漢字表記としては、「暮利比亜」「保里備屋」「玻里非」「波力斐」などが使われる。漢字一文字の略称では「暮国」が使われることが多い。 国家の独立前はアルト・ペルー（上ペルー、高地ペルー）と呼ばれていたが、独立に際してラテンアメリカの解放者として知られるシモン・ボリバル将軍と、アントニオ・ホセ・デ・スクレ将軍に解放されたことを称えて、国名をボリビア、首都名をスクレ（旧チャルカス）と定めた。 政治.... [1,000 / 10,747 chars] |
| トルコ石製品の生産と取引が繁栄した地域について、以下のような質問が考えられます: - トルコ石製品の生産と取引が繁栄した理由は何ですか？ - トルコ石製品の生産と取引が繁栄した地域では、どのような特別な技術や資源が利用されていましたか？ - トルコ石製品の生産と取引が繁栄した地域の経済にどのような影響を与えましたか？ - ヨーロッパの影響が現れた1880年頃以降、トルコ石製品の生産と取引はどのように変化しましたか？ - ナバホや他の南西アメリカインディアンの種族が銀の宝飾品の生産を開始した背景には何があったのでしょうか？ - 銀の宝飾品が現代になってから開発された理由は何ですか？ - ナバホや他の南西アメリカインディアンの種族が銀の宝飾品の生産においてヨーロッパの影響をどのように取り入れましたか？ - ナバホや他の南西アメリカインディアンの種族が銀の宝飾品の生産を始めた後、地域の経済や文化にどのような変化が見られましたか？ [418 chars] | トルコ石（トルコいし、turquoise、ターコイズ）は青色から緑色の色を持つ不透明な鉱物。化学的には水酸化銅アルミニウム燐酸塩であり、化学式では CuAl6(PO4)4(OH)8·4H2O と表される。良質のものは貴重であり、宝石とみなされる。 その色合いのために、数千年の昔から装飾品とされてきた。近年では他の多くの不透明の宝石と同様に、表面処理されたものや模造品・合成品が市場に出回っていて問題となっている。専門家でもその鑑定は難しい。宝石学者ジョージ・フレデリック・クンツによれば、大プリニウスの『博物誌』に「カッライス（callais）」として登場する宝石が現在のトルコ石の古名に当たるが、当時から盛んに模造品が作られていたという。 語源. 英語では turquoise （ターコイズ）と言い、フランス語の pierre turquoise （トルコの石）に由来する。十字軍（東方の文物が西ヨーロッパに到来するきっかけ）の時代にヨーロッパに広まったため、この石が「トルコの石」と呼ばれるようになったばかりか、もとは古フランス語で「トルコの｣を表す形容詞だった"turquoise"と言う語が、青の色みの一つを表すようにもなった。 後述のとおり、かつてペルシアと呼ばれた現在のイラン周辺は、少なくとも2000年来トルコ石の主要な産地として知られ、9世紀以来トルコ系王朝が興亡を繰り返したホラーサーンには最も古い鉱脈があった。つまり最初にヨーロッパに認識された「トルコ石」がトルコ人の国のものであったというのが、トルコ石と呼ばれる所以である。 なお、これは幾分かの誤解を含んでおり、トルコでトルコ石が産出されたわけではなく、アトラス山脈周辺の砂漠で産出されたものが貿易でトルコを経由してヨーロッパへ広がったのちになじみの深い宝石になり、「トルコ石」と呼ばれるようになったという説が存在する。現在のトルコからトルコ石の産出はない。 性質. トルコ石は良質のものでもやや脆い。モース硬度では6以下。 トルコ石は単結晶を作ることがほとんどない隠微晶質鉱物なので、性質は変異に富む。X線回折によると、結晶系は三斜晶系である。硬度と同様に比重も小さく、 2.60 – 2.90 である。また多孔質である（これらの性質は結晶の粒度に左右される）。 トルコ石は一般に不溶性だが、熱した塩酸には溶ける。条痕は薄... [1,000 / 11,470 chars] |
| ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルについて、以下の質問が考えられます: 1. ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルの違いは何ですか？ 2. ワイモバイルとウィルコム沖縄の直営店と代理店の運営比率はどのようになっていますか？ 3. ソフトバンクのショップ店とワイモバイルのショップ店が同一地で運営されている拠点はありますか？ 4. ワイモバイルのソフトバンクモバイルへの吸収合併後、直営店と代理店の数に変化はありましたか？ 5. ワイモバイルとウィルコム沖縄の直営店は、どのような地域に設けられていますか？ 6. ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルは、なぜこのようになっているのですか？ 7. 直営店と代理店の運営モデルの違いによる利点やデメリットはありますか？ 8. ソフトバンクのショップ店とワイモバイルのショップ店が同一地で運営されている拠点では、どのようにブランドの差別化が行われていますか？ 9. ワイモバイルとウィルコム沖縄の直営店と代理店の運営モデルは、顧客にどのような影響を与えていますか？ 10. ワイモバイルとウィルコ... [500 / 540 chars] | ワイモバイル株式会社（Ymobile Corporation）は、かつて存在した、日本の電気通信事業者。 2014年7月1日付けでイー・アクセス株式会社から商号変更した。 主にADSL回線の卸売、及びY!mobileのブランド名で移動体通信およびPHSサービスを提供している。2013年1月1日付で一度ソフトバンクの完全子会社となったが、議決権付株式の売却により、同年1月17日から持分法適用関連会社となった。 2015年4月1日、ソフトバンクモバイル株式会社（同年7月1日付でソフトバンク株式会社に商号変更）に吸収合併され、解散した。 概要. 1999年（平成11年）に、インターネット・サービス・プロバイダとADSL回線の契約を一括で提供するホールセール（卸売）を行う企業として設立。 当時の商号は、「イー・アクセス株式会社」である。 2000年（平成12年）4月28日、東京の青山局で無料試験サービス(下り最大512kbps、上り最大256kbps)を開始した後、同年10月1日に正式にサービスを開始した。 2002年（平成14年）6月には、当時の日本テレコム（事業上はのちのソフトバンクテレコム、会社組織上は同ソフトバンクモバイル、現：ソフトバンク）からADSL事業（J-DSL）を約55億円で譲り受け。同時に日本テレコムが筆頭株主となった。 2004年（平成16年）7月1日、AOLジャパンから日本国内に於けるAOL事業を約21億円で譲り受け、ISP事業へ参入した。 2005年（平成17年）に、移動体通信事業会社としてイー・モバイル株式会社を設立。サービス開始は、2007年（平成19年）(データ通信)、2008年（平成20年）(音声通話)である。 2005年（平成17年）11月9日、総務省電波監理審議会 の答申により、BBモバイル（ソフトバンクグループ）及びアイピーモバイルと同時に事業計画の認定が発表された。これにより、事業認可と電波免許の交付（1.7GHz帯）が行われた。コアネットワークは、エリクソン、基地局は、エリクソン（東名阪地域）と華為技術（その他地域）の製品を用いた。 2011年（平成23年）3月31日に、親会社イー・アクセスに吸収合併され法人は解散。イー・モバイルのブランド名はモバイル事業部門のブランドとして、Y!mobileに変更されるまで継続使用された。 20... [1,000 / 13,385 chars] |

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
