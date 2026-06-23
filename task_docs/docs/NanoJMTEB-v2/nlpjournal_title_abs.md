# NanoJMTEB-v2 / nlpjournal_title_abs

## Overview

`NanoJMTEB-v2 / nlpjournal_title_abs` is a Japanese academic retrieval task built
from the NLP Journal LaTeX Corpus. The query is a paper title, and the document
to retrieve is the corresponding abstract. This makes the task a compact
technical-title to abstract matching benchmark: the query is short, but it often
contains the method name, target phenomenon, or task phrase that defines the
paper. The Nano split has 200 queries, 637 documents, and one positive abstract
per query. Current diagnostics show that BM25 remains the strongest observed
ranker despite the short query length, dense retrieval is close but lower, and
`reranking_hybrid` improves over dense but does not surpass the sparse profile.

## Details

### What the Original Data Measures

The JMTEB card describes the NLP Journal V2 tasks as retrieval views built from
the Japanese NLP Journal LaTeX Corpus. Paper titles, abstracts, introductions,
and full articles are shuffled, and each task asks a model to recover the
matching paper component. In this split, titles are used as queries and
abstracts are used as documents.

This measures academic component matching under a short-query condition. A
title is usually much shorter than an abstract, but it is a high-information
field: it may include a method name, problem name, resource type, language
phenomenon, or modeling approach. The task tests whether a model can map that
compact technical phrase to the full abstract among many Japanese NLP papers in
the same publication domain.

### Observed Data Profile

The Nano split contains 200 queries, 637 documents, and 200 positive qrel rows.
Each query has one positive abstract, with no multi-positive queries. Titles
average 27.02 characters, while abstract documents average 461.52 characters.

Representative titles include work on maximum entropy extraction of bilingual
word pairs, automatic acquisition of local summarization knowledge, sequential
application of multiple decision lists for bunsetsu grouping, related-term
collection, and automatic extraction of colloquial strings from character
statistics. These titles are concise but technically dense, and their core
terms often reappear in the matching abstracts.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9526, hit@10 = 0.9850, and recall@100 = 1.0000. This is a
very strong sparse profile. Even though queries are short, Japanese academic
titles often contain distinctive technical terms that are repeated in the
abstract: method names, problem labels, task names, and key domain expressions.

The result is important because short queries do not automatically imply a
semantic-only task. Here, exact terminology carries much of the paper identity.
BM25's perfect top-100 coverage also makes it an excellent candidate generator.
Most remaining difficulty is distinguishing papers in similar subfields rather
than finding the correct abstract at all.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.9290, hit@10 = 0.9600, and recall@100 = 0.9700.
Dense retrieval is strong, but it trails BM25. It can connect compact title
phrases to longer abstract descriptions, which is useful when the abstract
expands the title with different wording. However, semantic similarity alone
can confuse papers in the same NLP area.

The dense gap suggests that exact technical vocabulary remains decisive. If a
title contains a specific method or coined problem name, a model must preserve
that lexical signal instead of smoothing it into a broad topic representation.
This is especially true in a small academic corpus where many abstracts discuss
related language-processing problems.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 1 safeguard positive row and a mean of 100.005 candidates. It
achieves nDCG@10 = 0.9428, hit@10 = 0.9700, and recall@100 = 0.9950. The hybrid
profile improves over dense retrieval in top-10 quality and coverage, but it
does not match BM25's nDCG@10, hit@10, or recall@100.

This is a case where hybrid search is helpful but not dominant. Dense evidence
adds some semantic title-abstract matches, while BM25 provides the strongest
paper-specific lexical anchors. For reranking experiments, the hybrid set is a
good source of close academic negatives, but the final ranker must not
overweight broad topic similarity over exact title terminology.

### Metric Interpretation for Model Researchers

With one positive abstract per title, hit@10 measures whether the matching
abstract appears in the first ten results, while nDCG@10 rewards placing it
near rank 1. Recall@100 measures whether candidate generation keeps the
matching abstract available for reranking.

The metric pattern is high-performing but still diagnostic. BM25 is best,
hybrid is second, and dense is close behind. This indicates that the task
primarily tests technical lexical precision under short-query conditions, with
semantic matching serving as a useful complement rather than the main signal.

### Query and Relevance Type Tendencies

Queries are Japanese paper titles. They are short, noun-heavy, and often
contain technical compounds. Relevant documents are abstracts that describe the
paper's motivation, proposed method, and evaluation. The abstract usually
expands the title's core phrase into a fuller research description.

The task rewards models that can handle compact Japanese academic titles,
technical terms, method names, and same-domain hard negatives. It is less about
general question answering and more about recovering the correct paper identity
from a concise scholarly label.

### Representative Failure Modes

BM25 can fail when several titles and abstracts share the same common NLP
terminology, or when a title is very general and the abstract's distinctive
terms do not overlap strongly. Dense retrieval can fail by ranking a topically
similar abstract above the exact matching paper. Hybrid retrieval can include
both, leaving the reranker to identify the abstract that actually belongs to
the title.

Common error sources include overmatching general words such as translation,
summarization, corpus, or analysis while underweighting the specific method,
problem formulation, or data type named in the title.

### Training Data That May Help

Helpful training data includes Japanese title-abstract retrieval pairs,
academic paper search, metadata-to-abstract matching, and hard negatives from
the same NLP subfield. Training should include short technical titles and
abstracts that share broad vocabulary but differ in method or contribution.

Comparable benchmark reporting should avoid using the same NLP Journal records
from this evaluation. Synthetic data can help when it creates compact Japanese
technical titles and matching abstracts with realistic same-field negatives.

### Model Improvement Notes

Dense retrievers can improve by preserving exact Japanese technical compounds
inside title embeddings and by learning title-to-abstract expansion without
losing method-specific detail. Sparse systems are already very strong, but
tokenization of Japanese compounds, Roman letters, formulas, and LaTeX-related
strings remains important. Rerankers should compare title terms against the
abstract's contribution and method statements, not just the broad research
topic.

For hybrid systems, `nlpjournal_title_abs` is a useful calibration task: hybrid
search should help when titles are under-specified, but exact academic
terminology should usually remain a high-weight signal.

## Example Data

| Query | Positive document |
| --- | --- |
| 最大エントロピー法を用いた対訳単語対の抽出 [21 chars] | 機械翻訳などの多言語間自然言語処理で用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には一貫性・網羅性などの点で限界があることから対訳コーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳関係の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．素性関数として共起情報を用い... [200 / 423 chars] |
| 局所的要約知識の自動獲得手法 [14 chars] | 日本語ニュースを局所的要約する際に必要となる要約知識を，コーパスから自動獲得する手法について述べる．局所的要約とは注目個所の近傍の情報（局所的情報）を用いて行なう要約をいう．局所的情報には注目個所そのものやその前後の単語列などがある．本手法では要約知識として置換規則と置換条件を用い，これらを原文−要約文コーパスから自動獲得する．はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間... [200 / 392 chars] |
| 複数決定リストの順次適用による文節まとめあげ [22 chars] | 近年の高度情報化の流れにより，自動車にも種々の情報機器が搭載されるようになり，その中で音声認識・合成の必要性が高まっている．本研究は音声合成を行うための日本語解析の中で基本となる，文節まとめあげに関する研究報告である．従来の文節まとめあげは，人手規則による手法と機械学習による手法の二つに大きく分けられる．前者は，長年の努力により非常に高い精度を得られているが，入力データ形式が固定であるために柔軟性... [200 / 589 chars] |
| 関連用語収集問題とその解法 [13 chars] | 本論文で提案する{\em関連用語収集問題}は，与えられた専門用語に対し，それと強く関連する用語集合を求める問題である．この問題を解くためには，ある用語が専門用語であり，かつ，入力用語と強く関連するかどうかを判定する方法が必要となる．本研究では，ウェブのサーチエンジンのヒット数から計算したJaccard係数もしくは$\chi^2$統計量を用いて，この判定を行なう．作成した関連用語収集システムは，候補... [200 / 425 chars] |
| 文字間統計情報に基づく口語文字列の自動抽出 [21 chars] | 統計情報に基づく自然言語処理が盛んになる中で，訓練データとしてのコーパスの影響は非常に大きい．生コーパスをそのまま利用する場合には，コーパスの取得が容易であるため，目的に合ったドメインのコーパスを大量に入手できるという利点がある．しかし，生コーパスは人間の言語の性質上，未登録語や未知の言い回し，非文とされるような文の出現等を多く含むことがほとんどであり，これらが処理の精度の低下を招くという問題があ... [200 / 496 chars] |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  source card for the NLP Journal retrieval tasks.
- [言語処理学会論文誌 LaTeX コーパス](https://github.com/jenio/nlp-journal-latex-corpus),
  upstream corpus repository.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2022.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/NLPJournalTitleAbsRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalTitleAbsRetrieval.V2),
  source task dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| sbintuitions/JMTEB | 2024 | dataset card | [https://huggingface.co/datasets/sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB) |
| 言語処理学会論文誌 LaTeX コーパス |  | repository | [https://github.com/jenio/nlp-journal-latex-corpus](https://github.com/jenio/nlp-journal-latex-corpus) |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A compact title about extracting bilingual word pairs using maximum entropy. | An abstract describing automatic bilingual dictionary construction from parallel corpora. |
| A title about automatic acquisition of local summarization knowledge. | An abstract explaining local summarization, replacement rules, and corpus-based acquisition. |
| A title about sequential application of multiple decision lists for bunsetsu grouping. | An abstract about Japanese analysis for speech synthesis and machine-learning approaches to bunsetsu grouping. |
| A title about a related-term collection problem and its solution. | An abstract defining related-term collection and using web-search statistics for selection. |
| A title about automatic extraction of colloquial strings from character statistics. | An abstract discussing raw corpora, unknown expressions, and colloquial expression processing. |
