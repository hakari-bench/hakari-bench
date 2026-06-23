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
| 1950年代に日本の映画業界で使われた宣伝文句がその語源である、毎年4月末から5月にわたる大型連休の通称は何でしょう? [59 chars] | ゴールデンウィーク ゴールデンウィーク、ゴールデンウイーク（和製英語: Golden Week, GW）とは、日本では毎年4月末から5月初めにかけての休日が多い期間のこと。大型連休（おおがたれんきゅう）、黄金週間（おうごんしゅうかん）ともいう。 本来は5月3日から5月5日までの3日間を指すが、一般的には4月29日から5月5日までとされる。また直前・直後に土曜日・日曜日・振替休日がある場合、それらを... [200 / 8,186 chars] |
| 美しい景観から「ドナウ川の真珠」とも呼ばれる、ハンガリーの首都はどこでしょう? [39 chars] | ブダペスト ブダペストまたはブダペシュト（ハンガリー語: Budapest, 英語:[ˈbuːdəpɛst], [ˈbuːdəpɛʃt] or [ˈbʊdəpɛst]; ハンガリー語発音: [ˈbudɒpɛʃt] ( 音声ファイル)）は、ハンガリーの首都であり、同国最大の都市である。 「ブダペスト」として一つの市でドナウ川の両岸を占めるようになったのは1873年11月17日に西岸のブダとオーブダ、... [200 / 23,581 chars] |
| 日本では有明海と八代海のみに生息するハゼ科の魚で、作家・畑正憲の愛称にもなっているのは何でしょう? [49 chars] | ムツゴロウ ムツゴロウ（鯥五郎、学名 Boleophthalmus pectinirostris ）は、スズキ目・ハゼ科に属する魚の一種。潮が引いた干潟の上で生活する魚として知られ、有明海・八代海を含む東アジアに分布する。有明海沿岸ではムツ、ホンムツなどと呼ばれる。 英語ではこれらを総称し"Mudskipper"（マッドスキッパー）と呼ぶ。 成魚は全長15センチ・メートル、最大で20センチ・メート... [200 / 2,354 chars] |
| 人類学者の増田義郎によって命名された、ヨーロッパ人が船でアジアやアメリカに次々と進出した15~17世紀の時代を指す言葉は何でしょう? [66 chars] | 大航海時代 大航海時代（だいこうかいじだい）とは、ヨーロッパ人がアフリカ・アジア・アメリカ大陸への大規模な航海を行い、"発見"した土地で略奪や搾取の限りを尽くした時代。15世紀半ばから17世紀半ばまで続き、主にポルトガルとスペインにより行われた。 「大航海時代」の名称は、1963年岩波書店にて「大航海時代叢書」を企画していた際、それまでの「地理上の発見」、「大発見時代」（Age of Discov... [200 / 9,243 chars] |
| シャフトと呼ばれる横棒にプレートと呼ばれる円盤状の重りを付けた、重量挙げに使われる器具は何でしょう? [50 chars] | バーベル バーベル（英: barbell）は、重量挙げ、パワーリフティング、ウエイトトレーニング等に用いられる、シャフトと呼ばれる横棒の両端に、プレートと呼ばれる円盤形の重りを付け、固定したスポーツ器具である。 プレートはシャフトに着脱可能になっており、種々の重量のプレートを取り換えることにより、全体の重量を調整して使用する。2つのプレートの間隔は肩幅よりやや広くされており、シャフトを両手で握って... [200 / 683 chars] |

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
