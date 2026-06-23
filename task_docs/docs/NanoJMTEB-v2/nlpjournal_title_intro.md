# NanoJMTEB-v2 / nlpjournal_title_intro

## Overview

`NanoJMTEB-v2 / nlpjournal_title_intro` is a Japanese academic retrieval task
derived from the NLP Journal LaTeX Corpus. The query is a paper title, and the
target document is the corresponding introduction section. This is the shortest
query form in the NLP Journal retrieval family, but the target is a longer
background and motivation section rather than a compact abstract. The Nano
split has 200 queries, 637 documents, and one positive introduction per query.
Current diagnostics show that BM25 is still the strongest top-10 profile,
`reranking_hybrid` restores nearly the same top-100 coverage as BM25, and dense
retrieval is strong but lower because compact titles must be mapped to broader
introductory prose.

## Details

### What the Original Data Measures

The JMTEB card describes the NLP Journal V2 tasks as retrieval tasks over
shuffled paper titles, abstracts, introductions, and full articles from the
Japanese NLP Journal LaTeX Corpus. In this split, titles are used as queries and
introductions are used as documents.

The task measures title-to-section matching inside a narrow Japanese academic
domain. A title gives a compact label for the paper's topic or method. The
introduction explains the motivation, background, related context, and problem
setting. The retriever must connect the short technical title to that broader
introductory section among many papers from the same NLP publication domain.

### Observed Data Profile

The Nano split contains 200 queries, 637 documents, and 200 positive qrel rows.
Each query has exactly one positive introduction, with no multi-positive
queries. Titles average 27.02 characters. Introduction documents average
2,148.04 characters and often include LaTeX labels, citation commands,
technical compounds, and several paragraphs of background discussion.

Representative titles include maximum entropy extraction of bilingual word
pairs, local summarization knowledge acquisition, bunsetsu grouping with
multiple decision lists, related-term collection, and colloquial string
extraction from character statistics. The positive introductions expand these
titles into motivations and background, sometimes without repeating every
title word densely throughout the section.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9132, hit@10 = 0.9700, and recall@100 = 0.9950. BM25 is
the strongest observed top-10 ranker. Even with short titles, exact technical
terms are highly informative in this corpus. Method names, task names, and NLP
phenomena named in the title often appear in the introduction.

Compared with title-to-abstract retrieval, this split is harder because the
introduction has a different rhetorical role. It may spend more space on
background and motivation than on the title's exact method wording. Still, the
sparse score is high, showing that Japanese technical vocabulary remains a
dominant signal for this task.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.8632, hit@10 = 0.9200, and recall@100 = 0.9300.
Dense retrieval is effective, but it trails BM25 by a noticeable margin. It can
connect a compact title to the introduction's broader problem setting, yet it
can also over-rank introductions from the same general NLP area.

This is a short-query academic matching problem where the semantic space is
dense with near neighbors. Many introductions discuss similar broad themes,
such as corpora, translation, summarization, language analysis, or machine
learning. Dense models must preserve paper-specific technical detail to avoid
confusing close same-domain documents.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 1 safeguard positive row and a mean of 100.005 candidates. It
achieves nDCG@10 = 0.8704, hit@10 = 0.9200, and recall@100 = 0.9950. Hybrid
retrieval matches BM25's top-100 coverage and improves slightly over dense
nDCG@10, but it does not approach BM25's top-10 score.

The pattern suggests that hybrid search is useful for candidate coverage but
not sufficient for final ordering. BM25 already supplies strong exact title
signals. Dense evidence introduces semantically related introductions, which
may help in some cases but also adds difficult same-topic negatives. A reranker
must learn when a background section truly belongs to the title rather than
merely sharing an academic topic.

### Metric Interpretation for Model Researchers

With one positive introduction per title, hit@10 measures whether the matching
introduction appears in the first ten results, and nDCG@10 rewards ranking it
near the top. Recall@100 measures whether candidate generation keeps the
positive section available for reranking.

The observed ordering is BM25 first, hybrid second by nDCG@10, and dense close
behind. This makes `nlpjournal_title_intro` a useful test of short technical
query handling. It is more difficult than title-to-abstract matching, but it
still favors exact Japanese academic terminology over broad semantic similarity.

### Query and Relevance Type Tendencies

Queries are compact Japanese academic titles. They often contain noun phrases
and technical compounds rather than full sentences. Relevant documents are
introduction sections that motivate the topic, explain background, and place
the contribution in context. The positive may not restate the title as directly
as an abstract would.

The task rewards models that can map a short paper title to a broader research
motivation while retaining exact method and task terms. It also tests
robustness to LaTeX-style text and older Japanese academic prose.

### Representative Failure Modes

BM25 can fail when a title is too general or when several introductions contain
the same technical vocabulary. Dense retrieval can fail by selecting an
introduction from a related paper that shares the same broad research area.
Hybrid retrieval can recover the positive but still leave a ranking challenge
among many same-domain hard negatives.

Common errors include confusing papers about similar NLP methods, overweighting
general words such as corpus or translation, and missing the specific
problem-setting phrase that ties the title to the introduction.

### Training Data That May Help

Helpful training data includes Japanese academic title-to-section retrieval,
title-introduction pairs, abstract-introduction pairs, paper metadata matching,
and hard negatives from the same subfield. Training should keep citations,
LaTeX labels, method names, and technical compounds intact.

Comparable benchmark reporting should avoid using the same NLP Journal records
from this evaluation. Synthetic data can help when it creates compact titles and
longer introductions with realistic rhetorical differences and close same-topic
negative sections.

### Model Improvement Notes

Dense retrievers should improve short-title representations so that a method or
task phrase remains distinguishable after embedding. Sparse systems benefit
from robust Japanese compound tokenization and handling of mathematical or
Roman-letter terms. Rerankers should compare the title against the
introduction's problem framing, not only its broad domain.

For hybrid systems, this task suggests a conservative weighting strategy:
dense retrieval can broaden candidates, but the exact title terms are usually
the most reliable evidence for the correct introduction.

## Example Data

| Query | Positive document |
| --- | --- |
| 最大エントロピー法を用いた対訳単語対の抽出 [21 chars] | \label{sec:intro}機械翻訳などの多言語間システムの構築において対訳辞書は必要不可欠であり，その品質がシステム全体の性能を左右する．これらに用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には限界があり，品質を向上するためには膨大な労力が必要であること，辞書の記述の一貫性を保つことが困難であることが問題となる．このことからコーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている\cite{gale_91,kaji_96,kitamura_96,fung_97,melamed_97}．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳単語対の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．本論文では対訳関係にある単語の組を対訳単語対と呼ぶ．最大エントロピー法は，与えられた制約の中でエントロピーを最大化するようなモデルを推定するという最大エントロピー原理に基づいており，未知データに対しても確率値をなるべく一様に配分するため，自然言語処理においてしばしば問題となるデータスパースネスに比較的強いという特徴を持っている．このため，構文解析\cite{ratnaparkhi_97,wojciech_98,uchimoto_99}，文境界の同定\cite{reynar_97}，動詞の下位範疇化モデル\cite{utsuro_97b}などに応用されている．また我々の手法は，既存の対訳辞書を必要とせず，文対応の付いた対訳コーパスさえあれば，対訳コーパスの分野を限定することなく対訳単語対を抽出できるという特徴を持つ．本論文の構成は以下の通りである．\ref{sec:ME_method}節では最大エントロピー法について説明し，\ref{sec:MEdict}節では最大エントロピー法を用いて対訳単語対を抽出する手法を述べる．\ref{sec:experiment_discussion}節では我々が提案した手法の有効性を示すために行った実験の結果とそれに対する考察を述べ，関連研究との比較を行う．\ref{sec:future}節でまとめを述べる． [920 chars] |
| 局所的要約知識の自動獲得手法 [14 chars] | \label{sec:sec1}インターネットの普及も手伝って，最近は電子化されたテキスト情報を簡単にかつ大量に手にいれることが可能となってきている．このような状況の中で，必要な情報だけを得るための技術として文章要約は重要であり，計算機によって要約を自動的に行なうこと，すなわち自動要約が望まれる．自動要約を実現するためには本来，人間が文章を要約するのと同様に，原文を理解する過程が当然必要となる．しかし，計算機が言語理解を行うことは現在のところ非常に困難である．実際，広範囲の対象に対して言語理解を扱っている自然言語処理システムはなく，ドメインを絞ったトイシステムにとどまっている．一方では言語理解に踏み込まずともある程度実現されている自然言語処理技術もある．例えば，かな漢字変換や機械翻訳は，人間が適切に介在することにより広く利用されている．自動要約の技術でも言語理解を導入せずに，表層情報に基づいたさまざまな手法が提案されている．これらの手法による要約は用いる情報の範囲により大きく２つに分けることができる．本論文では文章全体にわたる広範な情報を主に用いて行なう要約を{\gt大域的要約}，注目個所の近傍の情報を用いて行なう要約を{\gt局所的要約}と呼ぶ．我々は字幕作成への適用も視野に入れ，現在，局所的要約に重点を置き研究している．局所的要約を実現するには，後述する要約知識が必須であり，これをどのようにして獲得するかがシステムを構築する際のポイントとなる．本論文ではこのような要約知識（置換規則と置換条件）を，コーパス（原文−要約文コーパス）から自動的に獲得する手法について述べる．本手法では，はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間の距離を計算し，ＤＰマッチングによって最適な単語対応を求める．その結果から置換規則は単語対応上で不一致となる単語列として得られる．一方，置換条件は置換規則の前後ｎグラムの単語列として得られる．ＮＨＫニュースを使って局所的要約知識の自動獲得実験を行い，その有効性を検証する実験を行ったのでその結果についても述べる．以下，~\ref{sec:sec2}~章では自動要約に関して{\gt大域的要約}と{\gt局所的要約}について説明をする．~\ref{sec:sec3}~章では要約知識を自動獲得する際にベースとなる，原文−要約文... [1,000 / 1,203 chars] |
| 複数決定リストの順次適用による文節まとめあげ [22 chars] | 近年の高度情報化の流れにより，種々の情報機器が自動車にも搭載されるようになり，さまざまな情報通信サービスが広がりつつある．このような車載情報機器は，自動車に搭載するためにCPUの速度やRAM，ROMなどのメモリ容量の制約が非常に厳しく，また，開発期間がより短いことや保守管理の労力の低減も同時に求められている．自動車内で提供される情報通信サービスには，交通情報，観光情報，電子メール，一般情報(例えばニュース)などが含まれるが，このような情報はディスプレイ上に文字で表示するよりも，音声により提供する方が望ましいとされている．文字情報を音声に変換する技術の研究開発は進んでいるが，その合成音声の韻律は不自然という問題がある．その原因として大きな割合を占めるものはポーズ位置の誤りであり，これを改善することにより韻律の改善が可能となる．ポーズ位置を制御する手法として，係り受け解析を利用する方法が研究されている\cite{Suzuki1995,Umiki1996,Sato1999,Shimizu1999}．これらの手法の中で，海木ら\cite{Umiki1996}や清水ら\cite{Shimizu1999}の手法は係り受けの距離が2以上の文節の後にポーズを挿入するという方法であり，その有効性がすでに示されている．そしてこの手法を実現するためには，高精度な係り受け解析が必要となる．文節まとめあげは図\ref{fig:文節まとめあげ}のように，形態素解析された日本語文を文節にまとめあげる処理のことをいう．この処理は，日本語文の係り受け解析に重要となるものであるため，文節まとめあげの精度が高いことが望まれる\footnote{形態素解析の精度は，既に十分高い精度を得られている．}．本研究はこのように，係り受け解析にとって重要な位置を占めている文節まとめあげに関する研究報告である．\begin{figure}\begin{center}\begin{tabular}{cl}\fbox{日本語文}&うまく日本語文を解析する．\\$\downarrow$&$\downarrow$\\\fbox{形態素解析}&うまく,日本語,文,を,解析,する,．\\$\downarrow$&$\downarrow$\\\fbox{\bold文節まとめあげ}&うまく｜日本語文を｜解析する．\\$\downar... [1,000 / 1,703 chars] |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  source card for the NLP Journal retrieval tasks.
- [言語処理学会論文誌 LaTeX コーパス](https://github.com/jenio/nlp-journal-latex-corpus),
  upstream corpus repository.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2022.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/NLPJournalTitleIntroRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalTitleIntroRetrieval.V2),
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
| A title about maximum entropy extraction of bilingual word pairs. | An introduction about bilingual dictionaries, multilingual systems, and corpus-based extraction. |
| A title about automatic acquisition of local summarization knowledge. | An introduction motivating automatic summarization for large electronic text collections. |
| A title about sequential application of multiple decision lists for bunsetsu grouping. | An introduction about in-vehicle information systems and Japanese analysis for speech synthesis. |
| A title about a related-term collection problem and solution. | An introduction explaining specialized terms and the importance of relationships among them. |
| A title about automatic extraction of colloquial strings using character statistics. | An introduction discussing corpus use, annotation cost, and problems in raw-corpus processing. |
