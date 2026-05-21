# NanoJMTEB-v2 / jaqket

## Overview

`NanoJMTEB-v2 / jaqket` is the Nano split for JAQKET, a Japanese quiz-question
to Wikipedia-entity retrieval task. A quiz-style Japanese question must retrieve
the Wikipedia passage for the entity that answers the question.

## Details

### What the Original Data Measures

JAQKET, "Japanese Questions on Knowledge of Entities", was introduced as a
Japanese QA dataset based on quiz questions. The MTEB task card describes the
retrieval setup as quiz questions over encyclopedic, non-fiction written text,
with the relevant document being an entity description. The JMTEB card further
describes JAQKET as quiz questions paired with a Wikipedia passage corpus where
each passage describes an entity.

The original task therefore measures entity retrieval from clue-style questions.
The model must infer the answer entity from a description, often before the
entity name appears in the query. This is closer to quiz bowl or entity linking
than ordinary keyword search.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive document. Queries average 52.98 characters, and the
documents are long Wikipedia-like entity pages averaging 5,363.14 characters.

The observed questions are natural Japanese quiz prompts. They often name
attributes, works, aliases, sports rules, dates, etymology, or "what is this?"
style descriptions. Positives are full entity pages, so a retriever must identify
the entity and then tolerate much more surrounding text than the query mentions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1743
and hit@10 = 0.2100. BM25 ranks 28 positives at rank 1 and 42 in the top 10.
Every positive appears within the top 100.

BM25 helps when the clue repeats distinctive names, such as "ルスティケロ" and
"マルコ・ポーロ". It struggles when the answer is an implied concept, such as
"セットプレー", or when broad entity pages have many overlapping terms. A strong
retriever needs semantic entity resolution, not just overlap with clue words.

### Training Data That May Help

Useful data includes Japanese quiz QA, entity linking, Wikipedia question-to-page
retrieval, and training pairs that ask for an entity by properties rather than by
name. Cross-lingual entity retrieval may help if the Japanese labels and aliases
are preserved. Avoid using the same JAQKET validation/test questions as training
data.

### Synthetic Data Guidance

Generate clue-style Japanese questions from non-evaluation Wikipedia entity pages.
Questions should mention aliases, works, definitions, dates, categories, and
roles without always naming the answer. Synthetic positives should be full entity
passages or long summaries so the model learns answer-entity grounding under
long-document noise.

## Example Data

| Query | Positive document |
| --- | --- |
| 1950年代に日本の映画業界で使われた宣伝文句がその語源である、毎年4月末から5月にわたる大型連休の通称は何でしょう? (59 chars) | ゴールデンウィーク ゴールデンウィーク、ゴールデンウイーク（和製英語: Golden Week, GW）とは、日本では毎年4月末から5月初めにかけての休日が多い期間のこと。大型連休（おおがたれんきゅう）、黄金週間（おうごんしゅうかん）ともいう。 本来は5月3日から5月5日までの3日間を指すが、一般的には4月29日から5月5日までとされる。また直前・直後に土曜日・日曜日・振替休日がある場合、それらを含めて呼ぶことが多い。この場合は、その直前・直後の ... [truncated 225 chars](8186 chars) |
| 美しい景観から「ドナウ川の真珠」とも呼ばれる、ハンガリーの首都はどこでしょう? (39 chars) | ブダペスト ブダペストまたはブダペシュト（ハンガリー語: Budapest, 英語:[ˈbuːdəpɛst], [ˈbuːdəpɛʃt] or [ˈbʊdəpɛst]; ハンガリー語発音: [ˈbudɒpɛʃt] ( 音声ファイル)）は、ハンガリーの首都であり、同国最大の都市である。 「ブダペスト」として一つの市でドナウ川の両岸を占めるようになったのは1873年11月17日に西岸のブダとオーブダ、東岸のペストが合併してからである。 ドナウ川河畔に ... [truncated 225 chars](23581 chars) |
| 日本では有明海と八代海のみに生息するハゼ科の魚で、作家・畑正憲の愛称にもなっているのは何でしょう? (49 chars) | ムツゴロウ ムツゴロウ（鯥五郎、学名 Boleophthalmus pectinirostris ）は、スズキ目・ハゼ科に属する魚の一種。潮が引いた干潟の上で生活する魚として知られ、有明海・八代海を含む東アジアに分布する。有明海沿岸ではムツ、ホンムツなどと呼ばれる。 英語ではこれらを総称し"Mudskipper"（マッドスキッパー）と呼ぶ。 成魚は全長15センチ・メートル、最大で20センチ・メートルに達する。同様に干潟上で見られるトビハゼの倍くら ... [truncated 225 chars](2354 chars) |
| 人類学者の増田義郎によって命名された、ヨーロッパ人が船でアジアやアメリカに次々と進出した15~17世紀の時代を指す言葉は何でしょう? (66 chars) | 大航海時代 大航海時代（だいこうかいじだい）とは、ヨーロッパ人がアフリカ・アジア・アメリカ大陸への大規模な航海を行い、"発見"した土地で略奪や搾取の限りを尽くした時代。15世紀半ばから17世紀半ばまで続き、主にポルトガルとスペインにより行われた。 「大航海時代」の名称は、1963年岩波書店にて「大航海時代叢書」を企画していた際、それまでの「地理上の発見」、「大発見時代」（Age of Discovery / Age of Exploration） ... [truncated 225 chars](9243 chars) |
| シャフトと呼ばれる横棒にプレートと呼ばれる円盤状の重りを付けた、重量挙げに使われる器具は何でしょう? (50 chars) | バーベル バーベル（英: barbell）は、重量挙げ、パワーリフティング、ウエイトトレーニング等に用いられる、シャフトと呼ばれる横棒の両端に、プレートと呼ばれる円盤形の重りを付け、固定したスポーツ器具である。 プレートはシャフトに着脱可能になっており、種々の重量のプレートを取り換えることにより、全体の重量を調整して使用する。2つのプレートの間隔は肩幅よりやや広くされており、シャフトを両手で握って持ち上げて使用する。 持つ時の幅や持ち方は、種目に ... [truncated 225 chars](683 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | jaqket |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.1743 |
| BM25 hit@10 | 0.2100 |
| Query length avg chars | 52.98 |
| Document length avg chars | 5,363.14 |

### Public Sources

- [JAQKET: クイズを題材にした日本語 QA データセットの構築](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf), 2020.
- [mteb/jaqket](https://huggingface.co/datasets/mteb/jaqket), MTEB dataset card.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), Japanese embedding benchmark card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/jaqket](https://huggingface.co/datasets/mteb/jaqket)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| JAQKET: クイズを題材にした日本語 QA データセットの構築 | 2020 | paper | https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf |
| mteb/jaqket |  | dataset card | https://huggingface.co/datasets/mteb/jaqket |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoJMTEB-v2
  backing_dataset: NanoJMTEB-v2
  dataset_id: hakari-bench/NanoJMTEB-v2
  task_name: jaqket
  split_name: jaqket
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/jaqket.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 52.985
    document_mean: 5363.1378
  bm25:
    ndcg_at_10: 0.1743146674
    hit_at_10: 0.21
    source: dataset_bm25_column
  example_count: 5
```
