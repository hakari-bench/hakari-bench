# NanoJMTEB-v2 / ja_cwir

## Overview

`NanoJMTEB-v2 / ja_cwir` is the Nano split for JaCWIR, a Japanese web
information-retrieval task. Short Japanese questions must retrieve web-page title
and description snippets collected from varied Hatena Bookmark-style web content.
The task tests broad-domain Japanese web search behavior rather than encyclopedic
or FAQ matching.

## Details

### What the Original Data Measures

The JaCWIR dataset card describes JaCWIR as a casual Japanese web IR dataset:
web-page titles and meta descriptions are collected across many genres, and
question texts are generated with ChatGPT-3.5 from one of the pages. The linked
page is then treated as the positive document for the generated question. The
JMTEB card says the retrieval version reformats this data as a Japanese embedding
retrieval task.

This provenance matters because the task is not a human query log and not a
carefully controlled question-answering benchmark. It measures whether a model
can recover the source web page behind a synthetic Japanese question from noisy,
short web snippets. Titles, news snippets, blog summaries, page boilerplate, and
partially mismatched descriptions all appear in the corpus.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive document. Queries average 33.80 characters, while
documents average 189.04 characters. The sampled queries are broad web-search
questions about business news, lifestyle articles, sports/news headlines,
technology, entertainment, and explanatory blog posts.

The positive documents are compact title-plus-description strings. Some examples
are clean direct matches, but others have noisy page descriptions whose first
sentences do not fully answer the generated question. This makes the task
different from passage QA: the model must often use title cues and topical
alignment rather than answer extraction.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2431
and hit@10 = 0.2750. BM25 ranks 42 of 200 positives at rank 1 and 55 of 200 in
the top 10. Every positive appears somewhere in the top 100, so the Nano
candidate column is complete for recall but shallow lexical ranking is weak.

The hard cases are mostly web-noise and intent-paraphrase failures. For example,
the query about government lending systems for unemployed people maps to a page
whose description begins with unrelated beauty-clinic text. BM25 then prefers
other pages with more exact surface overlap, even when the positive title is the
semantic target.

### Training Data That May Help

Helpful training data would include Japanese web search pairs, title/description
retrieval pairs, and synthetic question-to-page supervision over noisy snippets.
Models should see broad-domain Japanese titles and page descriptions, not only
Wikipedia passages or FAQ answers. Data generated from evaluation queries or the
JaCWIR Nano positives should be excluded.

### Synthetic Data Guidance

For synthetic data, sample non-evaluation Japanese web snippets and generate
natural search questions that target the page title or main description. Preserve
noise: page boilerplate, partial summaries, date/headline fragments, and genre
variety. Avoid making all positives clean answer paragraphs; the real task often
requires matching a question to a page summary rather than reading an explicit
answer.

## Example Data

| Query | Positive document |
| --- | --- |
| 米国で成人男性が労働市場にとどまれない理由は何ですか？ (27 chars) | 米国で成人男性が労働市場にとどまれない理由とは: 米連邦司法統計局の最新のまとめによると、収監中もしくは保護観察中、仮釈放中の男性は2013年、560万人に上った。米紙ニューヨーク・タイムズなどが今年初めに行った調査によれば、25~54歳で無職の男性の約34%が犯罪歴を持っている。 障害を持つ人々にも厳しい雇用環境が迫る。金融危機の間には、 (171 chars) |
| マンガ好きがTPPに注目する理由は何ですか？ (22 chars) | マンガ好きもTPPに注目...「創作活動を萎縮」 : 経済 : 読売新聞(YOMIURI ONLINE): 環太平洋経済連携協定(TPP)交渉で、著作権を巡る議論がアニメやマンガの同人誌を作る愛好家の注目を集めている。 参加12か国は著作権の侵害について、警察が独自の判断で取り締まることができるようにする方向で検討している。愛好家にとってはこのことが「自由な創作活動を萎縮させる」というのだ。 (197 chars) |
| UXの本質について何が重要だと考えられますか？ (23 chars) | UXの本質について: ※本コラムは、長谷川のブログ「underconcept」からの転載です。 ユーザー体験(ユーザーエクスペリエンス/User Experience: UX)という言葉が広く聞かれるようになってきた。半ばバズワードのように、特にウェブデザインやマーケティングの記事などの中では、この言葉を見ない日はない。しかしながら、多くの場合、 (174 chars) |
| ビットコインの採掘とは何をしているのか? (20 chars) | ビットコインの「採掘」に関する基礎知識: ビットコインの採掘とは何をしているのか?という質問が多い。これに関しては、なかなか説明するのが難しく、ちゃんと説明しようとするとテクニカルになって長くなってしまうし、簡単に説明しようとするとイマイチなものになる。 下記の文章は、テクニカルな部分を極力おさえつつ、 (152 chars) |
| 電子契約において、なぜハンコの印影が法的に不要とされるのか？ (30 chars) | 電子契約ではハンコの印影(押印)が法的に不要となるのはなぜか—押印による二段の推定と比較して解説 \| クラウドサイン: 電子契約は、朱肉とハンコを使って押印することで二段の推定が成立する紙の契約書と違って、印影がないものが普通です。しかし、押印による印影がないと、契約として有効に成立しているのか不安という方も少なくありません。この記事では、なぜ電子契約では押印による印影が不要なのか、 (193 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | ja_cwir |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.9181 |
| BM25 hit@10 | 0.9750 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8367 |
| Dense hit@10 | 0.9100 |
| Dense Recall@100 | 0.9550 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8810 |
| Reranking hybrid hit@10 | 0.9550 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 33.80 |
| Document length avg chars | 189.04 |

### Public Sources

- [hotchpotch/JaCWIR](https://huggingface.co/datasets/hotchpotch/JaCWIR), dataset card for the Japanese Casual Web IR dataset.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), Japanese embedding benchmark card.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/JaCWIRRetrieval](https://huggingface.co/datasets/mteb/JaCWIRRetrieval)
- Upstream source dataset: [hotchpotch/JaCWIR](https://huggingface.co/datasets/hotchpotch/JaCWIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| hotchpotch/JaCWIR |  | dataset card | https://huggingface.co/datasets/hotchpotch/JaCWIR |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoJMTEB-v2
  backing_dataset: NanoJMTEB-v2
  dataset_id: hakari-bench/NanoJMTEB-v2
  task_name: ja_cwir
  split_name: ja_cwir
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/ja_cwir.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone JaCWIR paper was confirmed; dataset card and JMTEB
      card were checked.
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
    query_mean: 33.795
    document_mean: 189.0404
  bm25:
    ndcg_at_10: 0.9180507786994767
    hit_at_10: 0.975
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9180507787
      hit_at_10: 0.975
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8367277007
      hit_at_10: 0.91
      recall_at_100: 0.955
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.955
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8810210097
      hit_at_10: 0.955
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
