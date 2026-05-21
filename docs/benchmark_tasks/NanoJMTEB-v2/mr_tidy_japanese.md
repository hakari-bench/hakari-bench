# NanoJMTEB-v2 / mr_tidy_japanese

## Overview

`NanoJMTEB-v2 / mr_tidy_japanese` is the Japanese Mr. TyDi retrieval split. Short
Japanese questions must retrieve relevant Japanese documents. The task evaluates
monolingual dense retrieval over Japanese question-passage pairs derived from
the multilingual TyDi/Mr. TyDi line of benchmarks.

## Details

### What the Original Data Measures

[Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval](https://arxiv.org/abs/2108.08787)
introduces Mr. TyDi as a benchmark for monolingual retrieval in eleven
typologically diverse languages, designed to evaluate learned dense
representations beyond English. The authors report that dense representations
provide useful relevance signals when combined with sparse retrieval, even
though BM25 remains a strong baseline in their experiments.

The JMTEB card describes Mr.TyDi-ja as the Japanese split of Mr.TyDi, with the
goal of finding relevant documents for a query text. In NanoJMTEB-v2, the task
keeps the Japanese retrieval setting but reduces it to a Nano-sized evaluation.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 259 positive qrel rows.
There are 56 multi-positive queries. Queries average 18.44 characters and
documents average 233.46 characters. The examples are concise fact questions
about laws, films, scientific facts, people, and public qualifications.

Documents are short Japanese passages or entity summaries. Some positives answer
the question directly; others are supporting passages where the answer must be
inferred from context. This makes the task a compact factual retrieval benchmark
with both entity and relation matching.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0711
and hit@10 = 0.1050. It places 9 positives at rank 1 and finds a positive in the
top 10 for 21 of 200 queries. All positives are present within the top 100.

BM25 often retrieves a topic page that overlaps heavily with the question but is
not the judged answer-bearing passage. For example, a question asking who starred
in the live-action film version of `莫逆家族` can retrieve the film page above
the actor page. This is an entity-role distinction that sparse matching alone
does not resolve well.

### Training Data That May Help

Japanese Mr. TyDi training data, MIRACL-style Japanese passage retrieval, and
question-to-evidence training over Wikipedia are useful. Hard negatives should
include pages with the same entity family but the wrong relation or answer type.
Avoid overlap with the Mr. TyDi Japanese evaluation examples used here.

### Synthetic Data Guidance

Generate short Japanese factual questions from non-evaluation passages and
include hard negatives from related entities. Include birthplace/date questions,
yes/no scientific questions, media/actor role questions, legal-definition
questions, and answer passages that are not exact restatements of the query.

## Example Data

| Query | Positive document |
| --- | --- |
| ユースホステルに泊まるのに年齢制限はある？ (21 chars) | ユースホステル 元来、青少年の旅行者向けに開設された宿泊施設のため、ドイツ南部のバイエルン州では2004年まで原則満26歳までの利用とする年齢制限があった。2005年からは世界中の全ての地域・国で、利用できる年齢に上限を設けていない。 (118 chars) |
| アニー・ウッド・ベサントはいつ生まれた？ (20 chars) | アニー・ベサント アニー・ウッド・ベサント（Annie Wood Besant, ベザント</b>とも表記されるが発音は「bɛsənt」, 1847年10月1日 ロンドン、クラパム - 1933年9月20日 インド、アディヤール）は、イギリスの神智学徒、女性の権利（Women's rights）積極行動主義者、作家、演説家、アイルランドおよびインドの自治支援者、神智学協会第二代会長、英国フリーメーソンの国際組織レ・ドロワ・ユメー創設者[1]、イン ... [truncated 225 chars](242 chars) |
| サーミ人の土着信仰は何？ (12 chars) | ノアイデ ノアイデ</b><!-- ({{lang-sme\|noaidi}}, {{lang-smj\|noajdde}}, {{lang-sma\|nåejttie}}, {{lang-sms\|nōjjd}}, {{lang-sjt\|niojte}}, {{lang-sjd\|noojd/nuojd}}) -->とは、スカンジナビア北部からコラ半島にかけて居住するサーミ人の土着宗教におけるシャーマンである。当時の行政、司法からは、ノアイデの行う儀式な ... [truncated 225 chars](326 chars) |
| 市民オンブズマンは何を対象に監視していますか？ (23 chars) | 公安調査庁 また、一部の労働組合や労働争議支援団体、反戦運動・反基地運動、原子力撤廃・反核運動、市民オンブズマンなど行政監視グループ、部落解放・女性解放など人権擁護運動（アムネスティ・インターナショナル、自由法曹団、日本国民救援会、青年法律家協会等）、消費者団体（生活協同組合や産地直送運動・環境保護団体）、言論団体（日本ペンクラブ、日本ジャーナリスト会議等）などについても情報収集を行っているとされ、これらの団体から「調査・監視対象化は不当」と非難 ... [truncated 225 chars](236 chars) |
| マルティン・ルーサー・キング・ジュニアはいつ死んだ？ (26 chars) | マーティン・ルーサー・キング・ジュニア マーティン・ルーサー・キング・ジュニア（English: Martin Luther King, Jr.、1929年1月15日 - 1968年4月4日）は、アメリカ合衆国のプロテスタントバプテスト派の牧師である。 (127 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | mr_tidy_japanese |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 259 |
| BM25 nDCG@10 | 0.0711 |
| BM25 hit@10 | 0.1050 |
| Query length avg chars | 18.44 |
| Document length avg chars | 233.46 |

### Public Sources

- [Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval](https://arxiv.org/abs/2108.08787), 2021.
- [castorini/mr-tydi](https://huggingface.co/datasets/castorini/mr-tydi), source dataset card.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), Japanese embedding benchmark card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/mrtidy](https://huggingface.co/datasets/mteb/mrtidy)
- Upstream source dataset: [castorini/mr-tydi](https://huggingface.co/datasets/castorini/mr-tydi)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval | 2021 | paper | https://arxiv.org/abs/2108.08787 |
| castorini/mr-tydi |  | dataset card | https://huggingface.co/datasets/castorini/mr-tydi |
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
  task_name: mr_tidy_japanese
  split_name: mr_tidy_japanese
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/mr_tidy_japanese.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 259
  positives_per_query:
    average: 1.295
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 56
    multi_positive_query_percent: 28.0
  text_stats_chars:
    query_mean: 18.44
    document_mean: 233.4554
  bm25:
    ndcg_at_10: 0.0710585196
    hit_at_10: 0.105
    source: dataset_bm25_column
  example_count: 5
```
