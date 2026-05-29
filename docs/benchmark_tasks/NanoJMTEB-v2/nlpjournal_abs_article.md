# NanoJMTEB-v2 / nlpjournal_abs_article

## Overview

`NanoJMTEB-v2 / nlpjournal_abs_article` is a Japanese academic-paper retrieval
task built from the NLP Journal LaTeX Corpus. Given a paper abstract, the model
must retrieve the corresponding full article text.

## Details

### What the Original Data Measures

The JMTEB card describes the NLP Journal V2 retrieval tasks as datasets created
from the Japanese NLP Journal LaTeX Corpus. Titles, abstracts, introductions,
and full articles are shuffled; each task asks a model to recover the matching
paper component. In this split, the query is the abstract and the document is
the full article.

This task measures long academic-document matching within Japanese NLP papers.
It is not open-domain web search: all documents come from the same academic
publication domain, with LaTeX commands, citations, section labels, and technical
terminology retained in the text.

### Observed Data Profile

The Nano split has 200 queries, 637 documents, and 200 positive qrel rows. Each
query has one positive article. Queries are long abstracts averaging 494.52
characters, while documents are full papers averaging 28,330.39 characters.

The examples show Japanese NLP abstracts about machine translation, writing
support, lexical knowledge acquisition, example-based translation, and dialogue
systems. Positives are full LaTeX-like article texts beginning near the
introduction. The shared domain and long-document format make this more like
academic paper linking than ordinary passage retrieval.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8267
and hit@10 = 0.8900. It ranks 153 positives at rank 1 and 178 in the top 10.
All positives appear within the top 100.

This is the easiest NanoJMTEB-v2 task for BM25 because abstracts and full
articles share technical terms, method names, and LaTeX vocabulary. Remaining
errors happen when papers in the same research area share many terms, so the
model must still distinguish the exact article.

### Training Data That May Help

Academic retrieval data, paper abstract-to-full-text matching, Japanese NLP
paper corpora, and document-level contrastive training are useful. Training
should preserve technical terminology and LaTeX artifacts. Avoid using the same
NLP Journal corpus records from this evaluation.

### Synthetic Data Guidance

Create synthetic Japanese academic abstracts and full-paper introductions or
articles within NLP-like domains. Keep method names, datasets, evaluation
metrics, citations, and section markers. Generate hard negatives from papers in
the same subfield so the model learns exact paper matching, not just topic
matching.

## Example Data

| Query | Positive document |
| --- | --- |
| 機械翻訳などの多言語間自然言語処理で用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には一貫性・網羅性などの点で限界があることから対訳コーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳関係の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．素性関数として共起情報を用いるモデルと品詞情報を用いるモデルを定義した．共起情 ... [truncated 225 chars](423 chars) | \section{はじめに} \label{sec:intro}機械翻訳などの多言語間システムの構築において対訳辞書は必要不可欠であり，その品質がシステム全体の性能を左右する．これらに用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には限界があり，品質を向上するためには膨大な労力が必要であること，辞書の記述の一貫性を保つことが困難であることが問題となる．このことからコーパスから自動的に対訳辞書を作成しようとする研 ... [truncated 225 chars](16801 chars) |
| 日本語ニュースを局所的要約する際に必要となる要約知識を，コーパスから自動獲得する手法について述べる．局所的要約とは注目個所の近傍の情報（局所的情報）を用いて行なう要約をいう．局所的情報には注目個所そのものやその前後の単語列などがある．本手法では要約知識として置換規則と置換条件を用い，これらを原文−要約文コーパスから自動獲得する．はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間の距離を計算し，ＤＰマッチングによって最適な単語対 ... [truncated 225 chars](392 chars) | \section{はじめに} \label{sec:sec1}インターネットの普及も手伝って，最近は電子化されたテキスト情報を簡単にかつ大量に手にいれることが可能となってきている．このような状況の中で，必要な情報だけを得るための技術として文章要約は重要であり，計算機によって要約を自動的に行なうこと，すなわち自動要約が望まれる．自動要約を実現するためには本来，人間が文章を要約するのと同様に，原文を理解する過程が当然必要となる．しかし，計算機が言語理 ... [truncated 225 chars](19372 chars) |
| 近年の高度情報化の流れにより，自動車にも種々の情報機器が搭載されるようになり，その中で音声認識・合成の必要性が高まっている．本研究は音声合成を行うための日本語解析の中で基本となる，文節まとめあげに関する研究報告である．従来の文節まとめあげは，人手規則による手法と機械学習による手法の二つに大きく分けられる．前者は，長年の努力により非常に高い精度を得られているが，入力データ形式が固定であるために柔軟性に欠け，人手で規則を作成・保守管理するため多大な労 ... [truncated 225 chars](589 chars) | \section{はじめに} 近年の高度情報化の流れにより，種々の情報機器が自動車にも搭載されるようになり，さまざまな情報通信サービスが広がりつつある．このような車載情報機器は，自動車に搭載するためにCPUの速度やRAM，ROMなどのメモリ容量の制約が非常に厳しく，また，開発期間がより短いことや保守管理の労力の低減も同時に求められている．自動車内で提供される情報通信サービスには，交通情報，観光情報，電子メール，一般情報(例えばニュース)などが含ま ... [truncated 225 chars](19030 chars) |
| 本論文で提案する{\em関連用語収集問題}は，与えられた専門用語に対し，それと強く関連する用語集合を求める問題である．この問題を解くためには，ある用語が専門用語であり，かつ，入力用語と強く関連するかどうかを判定する方法が必要となる．本研究では，ウェブのサーチエンジンのヒット数から計算したJaccard係数もしくは$\chi^2$統計量を用いて，この判定を行なう．作成した関連用語収集システムは，候補語収集モジュールと関連用語選択モジュールの2つのモ ... [truncated 225 chars](425 chars) | \section{はじめに} 「ある用語を知る」ということは，その用語が何を意味し，どのような概念を表すかを知ることである．それと同時に，その用語が他のどのような用語と関連があるのかを知ることは非常に重要である．特定の専門分野で使われる用語---{\bf専門用語}---は，その分野内で孤立した用語として存在することはない．その分野で使われる他の用語に支えられ，その関連を土台として，はじめて意味を持つ．それらの用語間の関連を把握することは，「その専 ... [truncated 225 chars](47297 chars) |
| 統計情報に基づく自然言語処理が盛んになる中で，訓練データとしてのコーパスの影響は非常に大きい．生コーパスをそのまま利用する場合には，コーパスの取得が容易であるため，目的に合ったドメインのコーパスを大量に入手できるという利点がある．しかし，生コーパスは人間の言語の性質上，未登録語や未知の言い回し，非文とされるような文の出現等を多く含むことがほとんどであり，これらが処理の精度の低下を招くという問題がある．特に，口語表現の処理は，電子メールでの利用等利 ... [truncated 225 chars](496 chars) | \section{はじめに} 統計情報に基づく自然言語処理では，訓練データとしてのコーパスの影響は非常に大きい．形態素情報や品詞情報等の情報を付加したコーパスを利用することで処理の精度の向上や処理の簡略化等が期待できるが，情報を付加する段階での労力が大きく，その精度に結果が大きく左右されるという問題がある．生コーパスをそのまま利用する場合には，コーパスの取得が容易であるため，目的に合ったドメインのコーパスを大量に入手できるという利点がある．しかし ... [truncated 225 chars](21603 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Task / split | nlpjournal_abs_article |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Queries | 200 |
| Documents | 637 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.9982 |
| BM25 hit@10 | 1.0000 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9763 |
| Dense hit@10 | 0.9850 |
| Dense Recall@100 | 0.9900 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9863 |
| Reranking hybrid hit@10 | 0.9900 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 494.52 |
| Document length avg chars | 28,330.39 |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB), source card for the NLP Journal retrieval tasks.
- [言語処理学会論文誌 LaTeX コーパス](https://github.com/jenio/nlp-journal-latex-corpus), upstream corpus repository.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source task dataset: [mteb/NLPJournalAbsArticleRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalAbsArticleRetrieval.V2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| 言語処理学会論文誌 LaTeX コーパス |  | repository | https://github.com/jenio/nlp-journal-latex-corpus |
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
  task_name: nlpjournal_abs_article
  split_name: nlpjournal_abs_article
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/nlpjournal_abs_article.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone paper for this retrieval task was confirmed; JMTEB
      card and upstream corpus repository were checked.
  counts:
    queries: 200
    documents: 637
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 494.52
    document_mean: 28330.390895
  bm25:
    ndcg_at_10: 0.9981546487678572
    hit_at_10: 1.0
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9981546488
      hit_at_10: 1.0
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
      ndcg_at_10: 0.9763092975
      hit_at_10: 0.985
      recall_at_100: 0.99
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9863092975
      hit_at_10: 0.99
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
