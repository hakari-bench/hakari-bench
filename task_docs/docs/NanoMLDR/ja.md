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
| 員免許更新制の廃止により、教育における免許状の効力がどのように変化するのかについて、雇用者が評価を上げる方針をとる場合、人物面の評価においてプラスの評価をする理由は何ですか？ [87 chars] | 日本における教育職員免許状（きょういくしょくいんめんきょじょう）とは、就学前教育・初等教育・中等教育などにかかわる教育職員に就くための資格要件とされている、教育職員免許法に基づく免許状のことである。「教員免許」「免状」「教免」「教状」などと略して呼ばれることがある。 現代の日本においては、学校教員の職に必要な免許状のみがあり、学校教員の免許状は、教員免許状（きょういんめんきょじょう）とも呼ばれる。教員免許（きょういんめんきょ）と略称することもある。なお、以前の教育職員免許状には、校長の免許状、教育委員会の教育長の免許状、教育委員会の事務局の職員である指導主事の免許状もあった（特に、1級または2級の普通免許状が授与されていた時代）。 日本において教員（大学・短期大学、専門学校【専修学校の専門課程】、高等専門学校および、校長・副校長・教頭および特別非常勤講師や、教員として扱われないこともある実習助手を除く）に就くには、国立学校・公立学校・私立学校を問わず、何らかの教員免許状（普通免許状＝日本国内全域で効力を有する教諭・養護教諭・栄養教諭の免許状、特別免許状＝授与された区域内で効力を有する教諭の免許状、臨時免許状＝授与された都道府県内で効力を有する助教諭・養護助教諭の免許状）が必要である。 国公立学校の教員になるためには、何らかの普通免許状が必要となる場合が多いが、私立学校においては、採用時に採用者（学校法人等）の申請を通じて特別免許状や臨時免許状の授与を受けられることもある。だが、国公私立を問わず、通常ほとんどの教員は普通免許状を所持している。 概要. 日本では、教育職員免許法（昭和24年法律第147号）に基づいて、学校教育法（昭和22年法律第26号）の第1条に定める幼稚園・小学校・中学校・高等学校・中等教育学校・特別支援学校・義務教育学校の、主幹教諭・指導教諭・教諭・助教諭・養護教諭・養護助教諭・栄養教諭・講師（講師については、特別非常勤講師を除く）の職に就いている者は、各種の免許状の授与を受けている者でなければならないとされている。ただし、教科の領域の一部に係る事項などを担任する非常勤講師については、免許状を有していなくても都道府県の教育委員会に届け出ることにより特別非常勤講師として勤務することができる。また、実習助手については、免許状を必要とされていない（ただし、... [1,000 / 10,839 chars] |
| 軍はなぜ零戦の後継機である烈風の試作途中段階に留まっていたのか、その理由は何ですか？ [42 chars] | 紫電改（しでんかい）は、太平洋戦争期における大日本帝国海軍の戦闘機である。紫電（N1K1-J）の二一型以降が紫電改と呼称される。この項では紫電改と紫電をまとめて紹介する。 局地戦闘機紫電は、水上戦闘機「強風」を陸上戦闘機化したもので、紫電二一型は強風にちなんだ中翼配置の紫電を低翼に再設計した機体であり、紫電改は新機軸の設計（自動空戦フラップ、層流翼）が特徴であった。この機体は後述するように日本海軍、ひいては日本軍の戦闘機の中で最優秀の一つとされる。精鋭が集められた第三四三海軍航空隊の通称"剣部隊"に集中配備されたこともこの機体の名声が高まった要因と言える。 昭和19年4月7日内令兵第27号「航空機の名称」では「試製紫電改」は「試製紫電の機体改造及兵装強化せるもの」として定義づけられており、昭和20年4月11日海軍航空本部「海軍飛行機略符号一覧表」における二一型以降（紫電改）は、「試製紫電改(二一型)」「試製紫電改甲(二一甲型)」「試製紫電改一(三一型)」「試製紫電改二」「試製紫電改三」「試製紫電改四」「試製紫電改五」が該当する。 名称. 「紫電改」の名称は、兵器名称付与標準に基づき兵器採用前の試製機として「試製紫電改」とされたもので、「仮称紫電二一型」とも称し、兵器採用により「紫電二一型」となった。 日本海軍の搭乗員からは「紫電」と「紫電改」の呼称の他に、紫電が「J」、紫電改が「J改」と呼称されることもあった。三四三空の戦時日記でも「紫電改」「紫電二一型」の両方の記述があり、呼称は統一されていなかった。 連合軍側のコードネームは"George"(ジョージ)。紫電改は正面から見ると低翼であることがわかるため、紫電一一型とは別機と認識され、さらに戦時中には情報不足から、疾風や零戦などの他機種と誤認報告されており、戦後になってから紫電がGeorge11、紫電改がGeorge21と分類されて呼ばれた。 開発経緯. 強風から紫電へ. 1941年（昭和16年）末、川西航空機（以下、川西）は水上機の需要減少を見込み、川西龍三社長の下、次機種制作を討議した。川西社内で二式大艇の陸上攻撃機化、新型艦上攻撃機開発、川西十五試水上戦闘機（「強風」）の陸上戦闘機化の三案を検討した結果、十五試水上戦機陸戦案が決まった。川西の菊原静男設計技師は12月28日に海軍航空本部を訪れ、技術本部長多田力... [1,000 / 10,836 chars] |
| ましたが、南北アラブの対立が税収の減少につながった理由は何ですか？ [33 chars] | ウマイヤ朝（ウマイヤちょう、、al-Dawla al-Umawiyya）は、イスラム史上最初の世襲イスラム王朝である。大食（唐での呼称）、またはカリフ帝国やアラブ帝国と呼ばれる体制の王朝のひとつであり、イスラム帝国のひとつでもある。 イスラームの預言者ムハンマドと父祖を同じくするクライシュ族の名門で、メッカの指導層であったウマイヤ家による世襲王朝である。第4代正統カリフであるアリーとの抗争において、660年自らカリフを名乗ったシリア総督ムアーウィヤが、661年のハワーリジュ派によるアリー暗殺の結果、カリフ位を認めさせて成立した王朝。首都はシリアのダマスカス。ムアーウィヤの死後、次代以降のカリフをウマイヤ家の一族によって世襲したため、ムアーウィヤ（1世）からマルワーン2世までの14人のカリフによる王朝を「ウマイヤ朝」と呼ぶ。750年にアッバース朝によって滅ぼされるが、ムアーウィヤの後裔のひとりアブド・アッラフマーン1世がイベリア半島に逃れ、後ウマイヤ朝を建てる。 非ムスリムだけでなく非アラブ人のムスリムにもズィンミー（庇護民）として人頭税（ジズヤ）と地租（ハラージュ）の納税義務を負わせる一方、ムスリムのアラブ人には免税となるアラブ至上主義を敷いた。また、ディーワーン制や駅伝制の整備、行政用語の統一やアラブ貨幣鋳造など、イスラム国家の基盤を築いた。 カリフ位の世襲制をした最初のイスラム王朝であり、アラブ人でムスリムである集団による階級的な異教異民族支配を国家の統治原理とするアラブ帝国である（アラブ・アリストクラシー）。また、ウマイヤ家がある時期まで預言者ムハンマドの宣教に抵抗してきたという事実、また後述のカルバラーの悲劇ゆえにシーア派からは複雑な感情を持たれているといった事情から、今日、非アラブを含めたムスリム全般の間での評判は必ずしも芳しくない王朝である。 歴史. ムアーウィヤによる創始. 656年、ムアーウィヤと同じウマイヤ家の長老であった第3代カリフ・ウスマーンが、イスラームの理念を政治に反映させることなどを求めた若者の一団によってマディーナの私邸で殺害された。ウスマーンの死去を受け、マディーナの古参ムスリムらに推されたアリーが第4代カリフとなったが、これにムハンマドの妻であったアーイシャなどがイラクのバスラを拠点としてアリーに反旗を翻し、第一次内乱が起こった。両... [1,000 / 11,106 chars] |

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
