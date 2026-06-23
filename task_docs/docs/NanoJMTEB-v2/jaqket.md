# NanoJMTEB-v2 / jaqket

## Overview

`NanoJMTEB-v2 / jaqket` is the Nano split of JAQKET, a Japanese quiz-question
to Wikipedia entity retrieval task. A query is a Japanese quiz clue, and the
correct document is the Wikipedia-style entity page that answers the clue. This
is different from ordinary web search or FAQ retrieval: the model must infer an
entity from attributes, aliases, definitions, dates, roles, or descriptions,
then retrieve a long entity document. The Nano split has 200 queries, 10,000
documents, and exactly one positive qrel per query. The current retrieval
profile is balanced: BM25 and dense retrieval are nearly tied at nDCG@10 and
hit@10, while the `reranking_hybrid` candidate set gives the strongest observed
top-10 and top-100 coverage.

## Details

### What the Original Data Measures

JAQKET, "Japanese Questions on Knowledge of Entities", was introduced as a
Japanese question answering dataset built around quiz questions. In the
retrieval formulation used by MTEB and JMTEB, a quiz-style Japanese question is
used as the query, and the relevant document is the Wikipedia passage or entity
page corresponding to the answer.

The original task therefore measures entity retrieval from clue text. The query
may not name the answer directly. Instead, it can describe an origin, a
geographical nickname, a work, a sports object, a historical period, an alias,
or a property. A strong retrieval model must map those clues to the answer
entity and remain robust to long document text that contains far more
information than the query mentions.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has one positive document, with no multi-positive queries.
Queries average 52.98 characters. Documents are much longer than in most Nano
retrieval tasks, averaging 5,363.14 characters, because positives are
Wikipedia-like entity pages rather than short passages.

Representative questions ask for entities such as Golden Week, Budapest, the
mudskipper known in Japanese as "mutsugoro", the Age of Discovery, and the
barbell. These queries often include enough lexical evidence for exact matching,
but the main task is answer-entity identification. The correct document may be
found through a distinctive phrase in the clue, through semantic inference, or
through recognizing an alias or defining property.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7837, hit@10 = 0.8650, and recall@100 = 0.9450. BM25 is
strong on this task because quiz clues often include rare and informative terms:
place nicknames, historical periods, named people, technical object parts,
geographic references, or distinctive descriptions. When those words also occur
in the entity page, lexical matching can rank the positive highly.

The limitation is that BM25 cannot fully solve entity inference. If the query
describes the answer without naming it, or if the decisive clue is expressed
through an alias or indirect property, surface overlap may point to related
entities instead. The long documents also increase distractor risk: many entity
pages contain broad contextual words, and a related but wrong page can share
several clue terms.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset also has 500 candidates per
query. It reaches nDCG@10 = 0.7830, hit@10 = 0.8650, and recall@100 = 0.9300.
Top-10 dense retrieval is nearly identical to BM25 by these metrics, indicating
that semantic entity matching is helpful but does not dominate the lexical
signals in this Nano split.

Dense retrieval is useful when the query describes a concept rather than
repeating the title or answer name. It can connect "the Hungarian capital called
the Pearl of the Danube" to the Budapest page, or a definition of a sports
object to the correct entity. Its lower recall@100 suggests that some positives
are still best preserved by exact words, aliases, or Japanese surface forms
that dense embeddings may blur among related entities.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 7 safeguard positive rows and a mean of 100.035 candidates. It
achieves nDCG@10 = 0.7876, hit@10 = 0.8750, and recall@100 = 0.9650. The gains
over BM25 and dense retrieval are modest but consistent across the reported
metrics.

This is a classic hybrid entity-retrieval pattern. BM25 contributes rare clue
terms and exact Japanese aliases. Dense retrieval contributes semantic mapping
from clue descriptions to entity pages. The hybrid set is not a dramatic
top-10 breakthrough, but it provides the best candidate coverage and slightly
better rank quality. For reranking experiments, this means the task rewards a
model that can combine clue-word precision with entity-level semantic
recognition.

### Metric Interpretation for Model Researchers

Because every query has one positive document, hit@10 measures whether the
answer entity page appears in the first ten results, and nDCG@10 measures how
high it is ranked within those results. Recall@100 matters for reranking
pipelines because it tells whether the positive entity survives candidate
generation.

The key interpretation is that `jaqket` is not strongly dominated by one
retrieval family. BM25 and dense retrieval are essentially tied in top-10
quality, while hybrid retrieval provides the most complete candidate pool. This
makes the task a useful diagnostic for Japanese models that must handle both
exact clue terms and conceptual entity inference.

### Query and Relevance Type Tendencies

Queries are quiz-style Japanese questions. They often end with a phrase such as
"what is it?" or "where is it?", and they may mention enough properties to
identify an entity without giving the answer name. The relevant document is a
long entity page, so the match is between a compact clue and a broad
encyclopedic document.

This setup rewards models that can identify answer entities, handle aliases and
descriptive names, and compare a short clue to long document context. It also
tests whether long-document embeddings or rerankers can focus on the relevant
parts of an entity page instead of being diluted by unrelated sections.

### Representative Failure Modes

BM25 can fail when a clue's distinctive words also appear in related entity
pages, or when the answer is implied by properties rather than named. Dense
retrieval can fail by retrieving a semantically related entity in the same
category, such as another city, period, object, animal, or person. Hybrid
retrieval reduces these errors but still requires reranking that can resolve the
exact answer from the clue.

Long documents introduce another failure mode: the positive page may contain the
right evidence, but it is surrounded by thousands of characters of unrelated
context. Models that average document meaning too coarsely may miss the decisive
snippet, while models that overfocus on sparse terms may confuse related pages.

### Training Data That May Help

Helpful training data includes Japanese quiz QA, entity linking, question-to-
Wikipedia-page retrieval, alias-aware entity matching, and hard negatives from
neighboring entity categories. Training pairs should include questions that
describe entities indirectly rather than always naming them. Long positive
documents are useful because the benchmark itself uses long entity pages.

Comparable benchmark reporting should avoid training on the same JAQKET
validation or test questions, Nano examples, or exact positive entity passages.
Synthetic data can be useful if it is generated from non-evaluation Wikipedia
pages and includes clue styles similar to real quiz questions.

### Model Improvement Notes

Dense retrievers can improve by learning Japanese entity aliases, definitions,
and property-to-entity mappings while preserving rare clue terms. Sparse systems
benefit from good tokenization of Japanese names, katakana terms, compounds, and
foreign-language aliases. Rerankers should be trained to compare the clue
against the most relevant portions of a long entity page, not just to score the
global topical similarity of the page.

For hybrid search systems, `jaqket` suggests that lexical and dense evidence are
both necessary. The best candidate set is the one that keeps exact clue matches
while also admitting semantically inferred answer entities.

## Example Data

| Query | Positive document |
| --- | --- |
| 1950年代に日本の映画業界で使われた宣伝文句がその語源である、毎年4月末から5月にわたる大型連休の通称は何でしょう? [59 chars] | ゴールデンウィーク ゴールデンウィーク、ゴールデンウイーク（和製英語: Golden Week, GW）とは、日本では毎年4月末から5月初めにかけての休日が多い期間のこと。大型連休（おおがたれんきゅう）、黄金週間（おうごんしゅうかん）ともいう。 本来は5月3日から5月5日までの3日間を指すが、一般的には4月29日から5月5日までとされる。また直前・直後に土曜日・日曜日・振替休日がある場合、それらを含めて呼ぶことが多い。この場合は、その直前・直後の土日との間に挟まれる平日の日数が、一般的な平日の連続日数である5日の半数未満の場合つまり2日以内の場合はその土日もゴールデンウィークに含まれるが、半数を超える場合つまり3日以上平日が挟まれる場合はその土日はゴールデンウィークには含めない。この期間、4月29日（昭和の日、1988年（昭和63年）までは天皇誕生日、2006年（平成18年）まではみどりの日）・5月3日（憲法記念日）・5月4日（みどりの日、1988年（昭和63年）から2006年（平成18年）までは日曜日・月曜日以外なら国民の休日）・5月5日（こどもの日）が国民の祝日（2006年〈平成18年〉までの5月4日を除く）であり、5月1日がメーデーのため休日になる会社（人）も少なくないことから、間の平日を休みにすることで長期連休にしやすい。 以前は休日が飛び飛びになることが多かったことから「飛石連休」という言い方がされたが、1985年（昭和60年）の「国民の祝日に関する法律」（以下「祝日法」という。）の改正で5月4日が日曜日や振替休日でなくても「国民の休日」になってからは、この言い回しは少なくなった。 2005年（平成17年）に行われた祝日法の改正により、休日の名称および振替休日の規定が変更されたため、憲法記念日やみどりの日が日曜日と重なった場合、「こどもの日」の翌日が振替休日になり、その分ゴールデンウィークが延びることとなり、5月4日が日曜日となる2008年（平成20年）に最初に適用され、振替休日が初めて月曜日以外の火曜日となった。続く2009年（平成21年）も振替休日が初めて水曜日となった。 「ゴールデンウィーク」の名称は、映画会社の大映が松竹と競作して1951年（昭和26年）に同時上映となった獅子文六原作の『自由学校』が大映創設以来（当時）最高の売上を記録し、正月映画や... [1,000 / 8,186 chars] |
| 美しい景観から「ドナウ川の真珠」とも呼ばれる、ハンガリーの首都はどこでしょう? [39 chars] | ブダペスト ブダペストまたはブダペシュト（ハンガリー語: Budapest, 英語:[ˈbuːdəpɛst], [ˈbuːdəpɛʃt] or [ˈbʊdəpɛst]; ハンガリー語発音: [ˈbudɒpɛʃt] ( 音声ファイル)）は、ハンガリーの首都であり、同国最大の都市である。 「ブダペスト」として一つの市でドナウ川の両岸を占めるようになったのは1873年11月17日に西岸のブダとオーブダ、東岸のペストが合併してからである。 ドナウ川河畔に位置し、ハンガリーの政治、文化、商業、産業、交通の一大中心都市で、東・中央ヨーロッパ (en) では最大、欧州連合の市域人口では8番目に大きな都市である。しばしばハンガリーのプライメイトシティとも表現される。 ブダペストの市域面積は525km2 (202.7 sq mi)で、2011年の国勢調査によるブダペストの人口は174万人、ピークであった1989年の210万人より減少している。これは、ブダペスト周辺部の郊外化によるものである。ブダペスト都市圏（通勤圏）の人口は330万人である。 ブダペストの歴史の始まりはローマ帝国のアクインクムとしてで、もともとはケルト人の集落であった。アクインクムは古代ローマの低パンノニア属州の首府となっている。マジャル人がブダペスト周辺にやって来たのは9世紀頃である。最初の集落は1241年から1242年にかけてモンゴルの襲来 (en) により略奪された。15世紀に町が再建されるとブダペストはルネサンス期の人文主義者文化の中心となった。続いてモハーチの戦いが起こり、オスマン帝国による150年間の支配が続き、18世紀、19世紀に新しい時代に入ると町は発展し繁栄する。ブダペストは1873年にドナウ川を挟んだ都市の合併が行われると、世界都市となる。また、1848年から1918年の第一次世界大戦勃発まで列強に含まれたオーストリア＝ハンガリー帝国のウィーンに続く第二の首都であった。1920年のトリアノン条約によりハンガリーは国土の72%を失い、ハンガリーの文化や経済をブダペストがすべてを占めるようになった。ブダペストはその大きさや人口で圧倒的に優位に立ち、ハンガリーの他の都市を小さく見せていた。ブダペストはハンガリー革命 (1848年)や1919年のハンガリー評議会共和国、1944年のパンツァーファウスト作戦... [1,000 / 23,581 chars] |
| 日本では有明海と八代海のみに生息するハゼ科の魚で、作家・畑正憲の愛称にもなっているのは何でしょう? [49 chars] | ムツゴロウ ムツゴロウ（鯥五郎、学名 Boleophthalmus pectinirostris ）は、スズキ目・ハゼ科に属する魚の一種。潮が引いた干潟の上で生活する魚として知られ、有明海・八代海を含む東アジアに分布する。有明海沿岸ではムツ、ホンムツなどと呼ばれる。 英語ではこれらを総称し"Mudskipper"（マッドスキッパー）と呼ぶ。 成魚は全長15センチ・メートル、最大で20センチ・メートルに達する。同様に干潟上で見られるトビハゼの倍くらいの大きさになる。体色は褐色から暗緑色で、全身に白か青の斑点がある。両目は頭の一番高いところに突き出ていて、周囲を広く見渡せる。また、威嚇や求愛のときには二つの背鰭を大きく広げ、よく目立つ。 軟泥干潟に1メートルほどの巣穴を掘って生活する。満潮時・夜間・敵に追われたときなどは巣穴に隠れるが、昼間の干潮時には巣穴から這い出て活動する。干潟では胸びれで這ったり、全身で飛び跳ねて移動する。干潟の上で生活できるのは、皮膚と口の中に溜めた水で呼吸するためといわれる。陸上生活ができるとはいえ皮膚が乾くと生きることができず、ときにゴロリと転がって体を濡らす行動がみられる。直径2メートルほどの縄張りを持ち、同種だけでなく同じ餌を食べるヤマトオサガニなども激しく攻撃して追い払う。反対に、肉食性のトビハゼとは餌の競合はしないが、なわばりに入ってきたトビハゼに対しては、攻撃して追い払う。 植物食性で、干潟の泥の表面に付着している珪藻などの底生藻類を食べる。口は大きく、上顎にはとがった歯が生えているが、下顎の歯はシャベル状で前方を向いている。口を地面に押し付け、頭を左右に振りながら下顎の歯で泥の表面に繁殖した藻類を泥と一緒に薄く削り取って食べる。 1年のうちで最も活発に活動するのは初夏で、ムツゴロウ漁もこの時期に行われる。この時期にはオスがピョンピョンと跳ねて求愛したり、なわばり内に侵入した他のオスと背びれを立てて威嚇しあったり、猛獣のように激しく戦ったりする姿が見られる。メスは巣穴の横穴部分の天井に産卵し、オスが孵化するまで卵を守る。孵化した稚魚は巣穴から泳ぎだし、しばらく水中で遊泳生活を送るが、全長2センチ・メートルほどになると海岸に定着し干潟生活を始める。 日本・朝鮮半島・中国・台湾に分布するが、日本での分布域は有明海と八代海に限られる。氷河... [1,000 / 2,354 chars] |

### Public Sources

- [JAQKET: クイズを題材にした日本語 QA データセットの構築](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf),
  2020.
- [mteb/jaqket](https://huggingface.co/datasets/mteb/jaqket), MTEB dataset
  card.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  Japanese embedding benchmark card.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| JAQKET: クイズを題材にした日本語 QA データセットの構築 | 2020 | paper | [https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf) |
| mteb/jaqket |  | dataset card | [https://huggingface.co/datasets/mteb/jaqket](https://huggingface.co/datasets/mteb/jaqket) |
| sbintuitions/JMTEB | 2024 | dataset card | [https://huggingface.co/datasets/sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A quiz clue about a Japanese holiday period whose name originated as a 1950s film-industry promotion term. | The Wikipedia-style page for Golden Week, including alternate names and the late-April to early-May holiday period. |
| A clue asking for the Hungarian capital called the Pearl of the Danube. | The Budapest entity page, including its Hungarian name and history as a city on both sides of the Danube. |
| A clue about a goby-family fish living in the Ariake and Yatsushiro Seas and linked to a writer's nickname. | The mutsugoro entity page describing the mudskipper species, distribution, and Japanese names. |
| A clue about the 15th to 17th century when Europeans expanded by ship into Asia and the Americas. | The Age of Discovery entity page describing European voyages and the historical period. |
| A clue about weightlifting equipment made from a shaft and plate weights. | The barbell entity page describing the shaft, plates, and weight-training use. |
