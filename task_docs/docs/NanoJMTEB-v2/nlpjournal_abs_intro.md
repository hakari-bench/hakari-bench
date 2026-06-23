# NanoJMTEB-v2 / nlpjournal_abs_intro

## Overview

`NanoJMTEB-v2 / nlpjournal_abs_intro` is a Japanese academic retrieval task
derived from the NLP Journal LaTeX Corpus. The query is a paper abstract, and
the document to retrieve is the corresponding introduction section from the
same paper. This is a fine-grained section-matching task: both sides describe
the same research work, but they play different rhetorical roles. Abstracts
summarize contributions and results, while introductions motivate the problem,
position prior work, and introduce the paper's setting. The Nano split has 200
queries, 637 documents, and one positive introduction per query. Current
diagnostics show very strong lexical recoverability, with BM25 near ceiling,
dense retrieval strong but lower, and `reranking_hybrid` matching BM25's
top-100 coverage while not improving the top-10 score.

## Details

### What the Original Data Measures

The JMTEB card describes the NLP Journal V2 retrieval tasks as retrieval views
constructed from the Japanese NLP Journal LaTeX Corpus. Titles, abstracts,
introductions, and full articles are shuffled, and each task asks a model to
recover the matching component from the same paper. In this split, the query is
the abstract and the corpus item is the introduction.

This task measures academic component alignment within Japanese NLP papers. It
is not broad-domain search and not answer-passage retrieval. The key question
is whether a model can link two sections of the same paper despite differences
in section function: the abstract contains compact contribution and result
statements, while the introduction contains background, motivation, citations,
and problem framing.

### Observed Data Profile

The Nano split contains 200 queries, 637 documents, and 200 positive qrel rows.
Each query has exactly one positive introduction, with no multi-positive
queries. Abstract queries average 494.52 characters. Introduction documents
average 2,148.04 characters, much shorter than full articles but still long
enough to contain multiple paragraphs of technical context.

Representative examples discuss bilingual dictionary extraction, local
summarization for Japanese news, bunsetsu grouping for speech synthesis,
related-term collection, and statistical NLP over raw corpora. The text retains
LaTeX labels, citations, technical terminology, and older Japanese academic
writing conventions. Many positives share distinctive method and task terms
with their abstracts, but introductions may omit experimental details or final
results that appear in the abstract.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9896, hit@10 = 1.0000, and recall@100 = 1.0000. BM25 is
near ceiling. Abstracts and introductions usually share core topic words,
method names, task names, and technical expressions, so exact term frequency is
enough to recover the correct introduction for almost every query.

Compared with abstract-to-full-article retrieval, this split is slightly harder
for sparse ranking because the introduction is shorter and may not repeat every
result, evaluation detail, or contribution statement. Still, the values show
that lexical overlap between abstract and introduction is the dominant signal.
This task is therefore useful as a check on Japanese academic token handling
and exact technical vocabulary retention.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.9553, hit@10 = 0.9600, and recall@100 = 0.9600.
Dense retrieval is strong but below BM25. It captures the research topic and
problem setting, but it can confuse introductions from papers in the same NLP
subfield when exact paper-specific terms are not emphasized enough.

This is an important distinction for model researchers. Semantic similarity is
not the main bottleneck; papers in the corpus are already topically close.
Precise matching of methods, resources, terminology, and contribution wording is
what separates the correct introduction from another plausible NLP paper.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.9545, hit@10 = 0.9600,
and recall@100 = 1.0000. The hybrid profile restores full top-100 coverage, but
its top-10 score is essentially the same as dense retrieval and below BM25.

The result suggests that hybrid search is reliable for keeping the positive
introduction available, but it does not improve final ordering over the strong
sparse baseline. In this task, dense evidence can add semantically related
academic sections, but those sections may be hard negatives rather than better
matches. A reranker should therefore use hybrid candidates carefully and give
substantial weight to exact paper-specific terminology.

### Metric Interpretation for Model Researchers

With one positive introduction per abstract, hit@10 measures whether the
correct section appears in the first ten results, and nDCG@10 rewards ranking
it near the top. Recall@100 measures whether candidate generation keeps the
matching introduction available for reranking.

The metric pattern is straightforward: BM25 dominates, dense and hybrid remain
high but lower, and both BM25 and hybrid have perfect top-100 coverage. This
task should be read as a high-overlap academic matching benchmark, not as a
semantic paraphrase stress test. Small drops can still reveal important
problems with Japanese technical text, LaTeX artifacts, or domain-specific
compounds.

### Query and Relevance Type Tendencies

Queries are complete Japanese abstracts. They include motivations, proposed
methods, feature descriptions, and sometimes experimental results. Relevant
documents are introduction sections, which emphasize background and problem
setup more than result summaries. This creates partial but strong overlap
between query and positive document.

The task rewards models that can align academic rhetoric across sections:
abstract contribution statements must be connected to introductory motivation,
related work, and problem definitions. It also rewards exact matching of
Japanese NLP terminology, mathematical notation, and LaTeX-style text.

### Representative Failure Modes

BM25 can fail when several introductions share the same subfield vocabulary, or
when the abstract's decisive terms are result-oriented and not repeated in the
introduction. Dense retrieval can fail by selecting a semantically similar
introduction from another paper. Hybrid retrieval can include many close
same-domain negatives and still require careful final ranking.

Another failure mode is overemphasizing general NLP words such as corpus,
translation, summarization, or analysis while missing paper-specific method
names, resources, or evaluation details.

### Training Data That May Help

Helpful training data includes Japanese academic section matching,
abstract-introduction pairs, paper component retrieval, and hard negatives from
the same research subfield. Data should preserve citations, LaTeX labels,
method names, formulas, and technical compounds rather than normalizing them
away.

Comparable benchmark reporting should avoid using the same NLP Journal corpus
records from this evaluation. Synthetic data can help when it creates paired
abstracts and introductions with different rhetorical roles and includes
near-neighbor negative introductions from similar papers.

### Model Improvement Notes

Dense retrievers should improve paper-specific discrimination, especially for
methods and resources that distinguish one Japanese NLP paper from another.
Sparse systems already perform near ceiling, but robust Japanese tokenization of
technical expressions and LaTeX fragments remains important. Rerankers should
compare abstract claims to introduction motivation and avoid treating broad
topic similarity as sufficient.

For hybrid systems, this task argues for calibration: dense evidence should help
coverage, but exact lexical evidence often deserves priority when matching
abstracts to introductions in a small academic corpus.

## Example Data

| Query | Positive document |
| --- | --- |
| 機械翻訳などの多言語間自然言語処理で用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には一貫性・網羅性などの点で限界があることから対訳コーパスから自動的に対訳辞書を作... [100 / 423 chars] | \label{sec:intro}機械翻訳などの多言語間システムの構築において対訳辞書は必要不可欠であり，その品質がシステム全体の性能を左右する．これらに用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には限界があり，品質を向上するためには膨大な労力が必要であること，辞書の記述の一貫性を保つことが困難であることが問題となる．このことからコーパスから自動的に対訳辞書... [200 / 920 chars] |
| 日本語ニュースを局所的要約する際に必要となる要約知識を，コーパスから自動獲得する手法について述べる．局所的要約とは注目個所の近傍の情報（局所的情報）を用いて行なう要約をいう．局所的情報には注目個所その... [100 / 392 chars] | \label{sec:sec1}インターネットの普及も手伝って，最近は電子化されたテキスト情報を簡単にかつ大量に手にいれることが可能となってきている．このような状況の中で，必要な情報だけを得るための技術として文章要約は重要であり，計算機によって要約を自動的に行なうこと，すなわち自動要約が望まれる．自動要約を実現するためには本来，人間が文章を要約するのと同様に，原文を理解する過程が当然必要となる．し... [200 / 1,203 chars] |
| 近年の高度情報化の流れにより，自動車にも種々の情報機器が搭載されるようになり，その中で音声認識・合成の必要性が高まっている．本研究は音声合成を行うための日本語解析の中で基本となる，文節まとめあげに関す... [100 / 589 chars] | 近年の高度情報化の流れにより，種々の情報機器が自動車にも搭載されるようになり，さまざまな情報通信サービスが広がりつつある．このような車載情報機器は，自動車に搭載するためにCPUの速度やRAM，ROMなどのメモリ容量の制約が非常に厳しく，また，開発期間がより短いことや保守管理の労力の低減も同時に求められている．自動車内で提供される情報通信サービスには，交通情報，観光情報，電子メール，一般情報(例えば... [200 / 1,703 chars] |
| 本論文で提案する{\em関連用語収集問題}は，与えられた専門用語に対し，それと強く関連する用語集合を求める問題である．この問題を解くためには，ある用語が専門用語であり，かつ，入力用語と強く関連するかど... [100 / 425 chars] | 「ある用語を知る」ということは，その用語が何を意味し，どのような概念を表すかを知ることである．それと同時に，その用語が他のどのような用語と関連があるのかを知ることは非常に重要である．特定の専門分野で使われる用語---{\bf専門用語}---は，その分野内で孤立した用語として存在することはない．その分野で使われる他の用語に支えられ，その関連を土台として，はじめて意味を持つ．それらの用語間の関連を把握... [200 / 1,510 chars] |
| 統計情報に基づく自然言語処理が盛んになる中で，訓練データとしてのコーパスの影響は非常に大きい．生コーパスをそのまま利用する場合には，コーパスの取得が容易であるため，目的に合ったドメインのコーパスを大量... [100 / 496 chars] | 統計情報に基づく自然言語処理では，訓練データとしてのコーパスの影響は非常に大きい．形態素情報や品詞情報等の情報を付加したコーパスを利用することで処理の精度の向上や処理の簡略化等が期待できるが，情報を付加する段階での労力が大きく，その精度に結果が大きく左右されるという問題がある．生コーパスをそのまま利用する場合には，コーパスの取得が容易であるため，目的に合ったドメインのコーパスを大量に入手できるとい... [200 / 600 chars] |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  source card for the NLP Journal retrieval tasks.
- [言語処理学会論文誌 LaTeX コーパス](https://github.com/jenio/nlp-journal-latex-corpus),
  upstream corpus repository.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2022.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/NLPJournalAbsIntroRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalAbsIntroRetrieval.V2),
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
| An abstract about extracting bilingual word pairs from parallel corpora. | An introduction motivating bilingual dictionaries and corpus-based extraction. |
| An abstract about automatically acquiring local summarization knowledge. | An introduction discussing information overload and automatic summarization. |
| An abstract about bunsetsu grouping for speech synthesis in vehicle information systems. | An introduction describing constraints and needs for in-vehicle language processing. |
| An abstract proposing a related-term collection problem. | An introduction explaining why knowing relations among specialized terms matters. |
| An abstract about raw corpora and colloquial expressions in statistical NLP. | An introduction discussing corpus quality, annotation cost, and raw-corpus advantages. |
