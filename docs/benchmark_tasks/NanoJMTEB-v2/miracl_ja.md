# NanoJMTEB-v2 / miracl_ja

## Overview

`NanoJMTEB-v2 / miracl_ja` is the Japanese MIRACL retrieval split inside
NanoJMTEB-v2. Short Japanese questions must retrieve answer-bearing Japanese
Wikipedia passages. This task evaluates compact factual search over an
encyclopedic passage corpus.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of
Languages](https://arxiv.org/abs/2210.09984) describes MIRACL as a multilingual
monolingual retrieval benchmark over Wikipedia passages. Queries and documents
are in the same language; for Japanese, Japanese questions retrieve Japanese
Wikipedia passages. MIRACL uses native-speaker relevance judgments and was built
to cover 18 languages.

The JMTEB card notes that its Japanese MIRACL retrieval task uses the Japanese
split and reformats MIRACL as a retrieval task for embedding evaluation. The task
inherits the MIRACL/Mr.TyDi style of short natural questions with one or more
relevant passages.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 373 positive qrel rows.
There are 78 multi-positive queries. Queries average 17.50 characters, while
documents average 194.29 characters. The questions ask about birthplace,
foundation/opening date, office holders, definitions, media people, sports, and
historical entities.

The documents are Japanese Wikipedia passages, often beginning with the article
title and a concise explanatory paragraph. Several queries have multiple
relevant passages for the same question, so evaluation is not always a single
answer-page lookup.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0588
and hit@10 = 0.1000. It ranks only 9 queries' positives at rank 1 and finds a
positive in the top 10 for 20 of 200 queries. All positives appear within the top
100 candidate list.

The low shallow score is partly caused by passage granularity. BM25 may retrieve
the correct article but a different passage above the judged positive, or it may
match the entity name while missing the relation asked by a short query. Good
systems need both entity anchoring and passage-level evidence selection.

### Training Data That May Help

Japanese MIRACL training data, Japanese Wikipedia question-passage retrieval, and
Mr.TyDi-style monolingual retrieval pairs are directly relevant. Useful training
should include passage-level positives and hard negatives from the same article
or topic family. Avoid training on the MIRACL Japanese development/test examples
used by the Nano split.

### Synthetic Data Guidance

Generate short Japanese questions from non-evaluation Wikipedia passages and
pair them with answer-bearing passages. Include entity-neighbor hard negatives
from the same article family. Questions should cover `いつ`, `どこ`, `誰`, `何`,
yes/no facts, and title variants, while documents should remain passage-shaped
rather than answer-only strings.

## Example Data

| Query | Positive document |
| --- | --- |
| 神戸港が開港したのはいつ (12 chars) | 神戸港: 「神戸」は当時、開港場一帯の村の名前でしかなかったが、公文書には、開港直後の1868年（慶応4年、明治元年）には「神戸港」の名称がすでに現れている。やがて外国人の手によって居留地ができ始め、西洋文化の入り口として発展して「神戸」の名が著名になっていった。1872年（明治5年）、和田岬に和田岬灯台が設置されて1892年（明治25年）に勅令により、旧生田川（現フラワーロード）河口から和田岬までの全体が「神戸港」となる。 (214 chars) |
| レーシングドライバーになるには免許が必要ですか？ (24 chars) | モータースポーツライセンス: 世界的に通用する国際ライセンスの発行は以下の団体が行っている。下記団体が開催する競技に参戦するためには、これらの団体が発行したライセンスが必要となる。ただし発給申請自体は、傘下の国内ライセンスの発行団体を通じて行えることが多い。日本の法律ではモータースポーツを行うのに資格は必要ないが、参加するモータースポーツ主催の団体（FIAやJAF等）が発行するモータースポーツライセンスが必要になる。日本国内でのみ通用する国内ライ ... [truncated 225 chars](564 chars) |
| ウェールズはどこの国に属する？ (15 chars) | ウェールズ: ウェールズ（、 カムリ）は、グレートブリテンおよび北アイルランド連合王国（イギリス）を構成する4つの「国（イギリスのカントリー）」（country）のひとつである。ウェールズはグレートブリテン島の南西に位置し、南にブリストル海峡、東にイングランド、西と北にはアイリッシュ海が存在する。 (149 chars) |
| パメラ・コールマン・スミスはいつ生まれた？ (21 chars) | パメラ・コールマン・スミス: パメラ・コールマン・スミス（Pamela Colman Smith、1878年2月16日 - 1951年9月18日）は、画家、イラストレーター、作家。ニックネームは「ピクシー」だった。スミスは、占いに使用するタロット・カードの一つ、「ウェイト＝スミス・デッキ」（ライダー＝ウェイト、あるいはライダー＝ウェイト＝スミス・デッキとも呼ばれる。）を、アーサー・エドワード・ウェイトのためにデザインしたことで最も有名である。 (223 chars) |
| マーベル・コミックのミュータントは特殊能力を持つ？ (25 chars) | マグニートー (マーベル・コミック): マグニートーは磁場を操り、幅広い種類の影響を及ぼすことができるミュータントである。彼の主要な能力は、磁力を支配し、鉄を含む金属と非鉄の金属を操ることである。彼が一度に操ることのできる量の最大値は不明で、彼は何度か、大きな小惑星を動かし、3万トンの原子力潜水艦を容易く空中に浮かせたことがある。彼は自分の力を原子レベルにまで拡張し、（電磁力が化学結合の要因である限りでは）化学構造を操り、物質を再配列できる。けれ ... [truncated 225 chars](831 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | miracl_ja |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 373 |
| BM25 nDCG@10 | 0.0588 |
| BM25 hit@10 | 0.1000 |
| Query length avg chars | 17.50 |
| Document length avg chars | 194.29 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984), 2022.
- [MIRACL project page](http://miracl.ai/).
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), Japanese embedding benchmark card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL project page |  | project page | http://miracl.ai/ |
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
  task_name: miracl_ja
  split_name: miracl_ja
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/miracl_ja.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 373
  positives_per_query:
    average: 1.865
    min: 1
    median: 1.0
    max: 6
    multi_positive_queries: 78
    multi_positive_query_percent: 39.0
  text_stats_chars:
    query_mean: 17.5
    document_mean: 194.2899
  bm25:
    ndcg_at_10: 0.0587521649
    hit_at_10: 0.1
    source: dataset_bm25_column
  example_count: 5
```
