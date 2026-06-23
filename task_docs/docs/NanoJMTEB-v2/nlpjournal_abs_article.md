# NanoJMTEB-v2 / nlpjournal_abs_article

## Overview

`NanoJMTEB-v2 / nlpjournal_abs_article` is a Japanese academic-document
retrieval task built from the NLP Journal LaTeX Corpus. The query is a paper
abstract, and the target document is the corresponding full article text. This
is a within-paper component matching task rather than open-domain search: the
query and positive document come from the same Japanese NLP paper and share
technical vocabulary, method descriptions, data names, and LaTeX-like writing
style. The Nano split has 200 queries, 637 documents, and one positive article
per query. Current diagnostics are near ceiling: BM25 is almost perfect,
`reranking_hybrid` also reaches full top-100 coverage, and dense retrieval is
very strong but slightly below the sparse and hybrid profiles.

## Details

### What the Original Data Measures

The JMTEB card describes the NLP Journal V2 retrieval tasks as datasets created
from the Japanese NLP Journal LaTeX Corpus. Titles, abstracts, introductions,
and full articles are shuffled into different retrieval views. In this split,
the abstract is the query and the full article is the document to retrieve.

The task measures academic paper linking inside a narrow technical domain. It
does not test broad web search, answer extraction, or multilingual transfer.
Instead, it tests whether a model can match two components of the same
Japanese NLP paper, with LaTeX commands, section markers, citations, technical
terms, and research-topic vocabulary still present in the text.

### Observed Data Profile

The Nano split contains 200 queries, 637 documents, and 200 positive qrel rows.
Every query has one positive article, with no multi-positive queries. Abstract
queries are long, averaging 494.52 characters. Full-article documents average
28,330.39 characters, making this one of the longest-document tasks in the Nano
set.

Representative examples cover machine translation and bilingual dictionary
extraction, local summarization for Japanese news, bunsetsu grouping for speech
synthesis, related-term collection from the web, and corpus effects in
statistical NLP. The positive documents are full LaTeX-like article texts that
typically begin around the introduction and repeat much of the abstract's
method, task, terminology, and motivation.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9982, hit@10 = 1.0000, and recall@100 = 1.0000. This is
essentially a ceiling sparse-retrieval result. Abstracts and full articles share
many exact terms: method names, task names, linguistic phenomena, mathematical
expressions, datasets, evaluation terms, and domain-specific Japanese NLP
vocabulary.

For researchers, the implication is clear. This task is not difficult because
of paraphrase or sparse lexical mismatch. BM25 almost always finds the exact
article because the abstract is a dense lexical summary of the same paper. The
remaining difficulty is fine-grained discrimination among papers in the same
subfield, where multiple articles can discuss similar methods or terminology.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.9763, hit@10 = 0.9850, and recall@100 = 0.9900.
Dense retrieval is very strong, but it is still slightly below BM25. This is
expected for abstract-to-article matching: dense embeddings capture the
research topic, but exact technical terms and repeated phrasing provide a
particularly strong sparse signal.

Dense retrieval's small gap can arise when several papers are semantically
nearby, such as multiple NLP papers about translation, summarization, corpus
processing, or dialogue. A dense model may rank a topically similar paper above
the exact source article if it does not preserve enough paper-specific lexical
detail.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.9863, hit@10 = 0.9900,
and recall@100 = 1.0000. The hybrid profile improves over dense retrieval and
matches BM25's full top-100 coverage, but it does not surpass BM25's nearly
perfect top-10 ranking.

This profile shows that hybrid search is robust but not necessary to solve most
queries in this split. Lexical evidence already identifies the article in
nearly every case. The hybrid set is still useful for reranking experiments
because it provides complete positive coverage while adding semantically
related alternatives from the same academic domain.

### Metric Interpretation for Model Researchers

With one positive article per abstract, hit@10 measures whether the exact full
paper appears in the first ten results, and nDCG@10 rewards ranking it near
rank 1. Recall@100 measures whether candidate generation keeps the exact paper
available for reranking.

The metric pattern marks this as a high-ceiling, low-mismatch task. BM25 is the
best observed top-10 ranker, dense retrieval is very close, and hybrid retrieval
is a reliable candidate pool. Improvements on this task are likely to be small
in absolute terms, so it is most useful for detecting regressions in Japanese
technical-term handling or long academic document matching.

### Query and Relevance Type Tendencies

Queries are full Japanese abstracts. They are much longer than typical web
queries and contain problem statements, proposed methods, feature descriptions,
and evaluation summaries. Relevant documents are full papers, often tens of
thousands of characters long. The match is document-identity matching between
two components of the same paper.

The task rewards models that preserve Japanese technical terminology,
mathematical or LaTeX artifacts, citation-style text, and domain-specific NLP
expressions. It is less sensitive to broad semantic world knowledge because the
abstract itself contains rich lexical evidence.

### Representative Failure Modes

BM25 may fail only in rare cases where several papers share nearly identical
terminology or where the decisive terms are spread across a long article.
Dense retrieval may confuse papers in the same subfield, especially when
abstracts discuss similar tasks or methods. Hybrid retrieval can include the
right article but still require a reranker to separate exact paper identity from
close topical similarity.

Long documents introduce another possible issue: if a model truncates the full
article poorly, it may lose sections that mirror the abstract. Sparse retrieval
is less affected because many abstract terms appear throughout introductions,
method sections, and related work.

### Training Data That May Help

Helpful training data includes academic paper retrieval, abstract-to-full-text
matching, Japanese NLP paper corpora, citation-aware document matching, and
hard negatives from papers in the same research subfield. Training should
preserve LaTeX commands, formulas, section labels, and technical expressions
because they are meaningful retrieval signals here.

Comparable benchmark reporting should avoid using the same NLP Journal corpus
records from this evaluation. Synthetic data can help if it creates realistic
Japanese NLP abstracts and matching long articles, along with hard negatives
from the same topic area rather than random documents.

### Model Improvement Notes

Dense retrievers can improve by preserving fine-grained technical terms in
long-document representations and by distinguishing exact paper identity from
topic similarity. Sparse systems already perform near ceiling, but Japanese
tokenization of technical compounds, Roman letters, mathematical expressions,
and LaTeX artifacts remains important. Rerankers should compare the abstract
against article sections that restate the contribution, method, and evaluation.

For hybrid search systems, this task is mainly a regression and calibration
check. If a system performs poorly here, it likely mishandles long Japanese
academic text or exact technical vocabulary.

## Example Data

| Query | Positive document |
| --- | --- |
| 機械翻訳などの多言語間自然言語処理で用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には一貫性・網羅性などの点で限界があることから対訳コーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳関係の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．素性関数として共起情報を用いるモデルと品詞情報を用いるモデルを定義した．共起情報により対訳関係にある単語の意味を制約し，品詞情報により対訳関係にある単語の品詞を制約する．本手法の有効性を示すために日英対訳コーパスを用いた対訳単語対の抽出実験を行い，本論文で提案した手法が従来の手法よりも精度・再現率において優れた結果となり，また，テストコーパスによる実験では学習コーパスに出現しなかった単語対に関しても学習データに現れたものとほぼ同等の精度・再現率で抽出できることを示した． [423 chars] | \section{はじめに} \label{sec:intro}機械翻訳などの多言語間システムの構築において対訳辞書は必要不可欠であり，その品質がシステム全体の性能を左右する．これらに用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には限界があり，品質を向上するためには膨大な労力が必要であること，辞書の記述の一貫性を保つことが困難であることが問題となる．このことからコーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている\cite{gale_91,kaji_96,kitamura_96,fung_97,melamed_97}．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳単語対の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．本論文では対訳関係にある単語の組を対訳単語対と呼ぶ．最大エントロピー法は，与えられた制約の中でエントロピーを最大化するようなモデルを推定するという最大エントロピー原理に基づいており，未知データに対しても確率値をなるべく一様に配分するため，自然言語処理においてしばしば問題となるデータスパースネスに比較的強いという特徴を持っている．このため，構文解析\cite{ratnaparkhi_97,wojciech_98,uchimoto_99}，文境界の同定\cite{reynar_97}，動詞の下位範疇化モデル\cite{utsuro_97b}などに応用されている．また我々の手法は，既存の対訳辞書を必要とせず，文対応の付いた対訳コーパスさえあれば，対訳コーパスの分野を限定することなく対訳単語対を抽出できるという特徴を持つ．本論文の構成は以下の通りである．\ref{sec:ME_method}節では最大エントロピー法について説明し，\ref{sec:MEdict}節では最大エントロピー法を用いて対訳単語対を抽出する手法を述べる．\ref{sec:experiment_discussion}節では我々が提案した手法の有効性を示すために行った実験の結果とそれに対する考察を述べ，関連研究との比較を行う．\ref{sec:future}節でまとめを述べる． \section{最大エントロピー法} \label{sec:ME_method}一般に確率モデルは，履歴とその時の出力の関係を... [1,000 / 16,801 chars] |
| 日本語ニュースを局所的要約する際に必要となる要約知識を，コーパスから自動獲得する手法について述べる．局所的要約とは注目個所の近傍の情報（局所的情報）を用いて行なう要約をいう．局所的情報には注目個所そのものやその前後の単語列などがある．本手法では要約知識として置換規則と置換条件を用い，これらを原文−要約文コーパスから自動獲得する．はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間の距離を計算し，ＤＰマッチングによって最適な単語対応を求める．その結果より，置換規則は単語対応上で不一致となる単語列として獲得する．一方，置換条件は置換規則の前後ｎグラムの単語列として獲得する．原文と要約文にそれぞれＮＨＫニュース原稿とＮＨＫ文字放送の原稿を使って実際に要約知識を自動獲得し，得られた要約知識を評価する実験を行った．その結果，妥当な要約知識が獲得できることを確認した． [392 chars] | \section{はじめに} \label{sec:sec1}インターネットの普及も手伝って，最近は電子化されたテキスト情報を簡単にかつ大量に手にいれることが可能となってきている．このような状況の中で，必要な情報だけを得るための技術として文章要約は重要であり，計算機によって要約を自動的に行なうこと，すなわち自動要約が望まれる．自動要約を実現するためには本来，人間が文章を要約するのと同様に，原文を理解する過程が当然必要となる．しかし，計算機が言語理解を行うことは現在のところ非常に困難である．実際，広範囲の対象に対して言語理解を扱っている自然言語処理システムはなく，ドメインを絞ったトイシステムにとどまっている．一方では言語理解に踏み込まずともある程度実現されている自然言語処理技術もある．例えば，かな漢字変換や機械翻訳は，人間が適切に介在することにより広く利用されている．自動要約の技術でも言語理解を導入せずに，表層情報に基づいたさまざまな手法が提案されている．これらの手法による要約は用いる情報の範囲により大きく２つに分けることができる．本論文では文章全体にわたる広範な情報を主に用いて行なう要約を{\gt大域的要約}，注目個所の近傍の情報を用いて行なう要約を{\gt局所的要約}と呼ぶ．我々は字幕作成への適用も視野に入れ，現在，局所的要約に重点を置き研究している．局所的要約を実現するには，後述する要約知識が必須であり，これをどのようにして獲得するかがシステムを構築する際のポイントとなる．本論文ではこのような要約知識（置換規則と置換条件）を，コーパス（原文−要約文コーパス）から自動的に獲得する手法について述べる．本手法では，はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間の距離を計算し，ＤＰマッチングによって最適な単語対応を求める．その結果から置換規則は単語対応上で不一致となる単語列として得られる．一方，置換条件は置換規則の前後ｎグラムの単語列として得られる．ＮＨＫニュースを使って局所的要約知識の自動獲得実験を行い，その有効性を検証する実験を行ったのでその結果についても述べる．以下，~\ref{sec:sec2}~章では自動要約に関して{\gt大域的要約}と{\gt局所的要約}について説明をする．~\ref{sec:sec3}~章では要約知識を自動獲得する... [1,000 / 19,372 chars] |
| 近年の高度情報化の流れにより，自動車にも種々の情報機器が搭載されるようになり，その中で音声認識・合成の必要性が高まっている．本研究は音声合成を行うための日本語解析の中で基本となる，文節まとめあげに関する研究報告である．従来の文節まとめあげは，人手規則による手法と機械学習による手法の二つに大きく分けられる．前者は，長年の努力により非常に高い精度を得られているが，入力データ形式が固定であるために柔軟性に欠け，人手で規則を作成・保守管理するため多大な労力を要し，車載情報機器へ実装するには問題が大きい．また後者は，それらの問題に柔軟に対処できるが，精度を向上させるためにアルゴリズムが複雑化しており，その結果開発期間が延長するなどの問題が生じ，車載情報機器には不向きである．そこで本研究は，決定リストを用いる手法を発展させ，複数の決定リストを順に適用するだけという非常に簡明な文節まとめあげの手法を提案する．決定リストの手法は非常に単純であるが，それだけでは高い精度が得られない．そこで，決定リストを一つではなく複数作成し，それぞれのリストを最適な順序に並べて利用することにより精度向上を図った．この結... [500 / 589 chars] | \section{はじめに} 近年の高度情報化の流れにより，種々の情報機器が自動車にも搭載されるようになり，さまざまな情報通信サービスが広がりつつある．このような車載情報機器は，自動車に搭載するためにCPUの速度やRAM，ROMなどのメモリ容量の制約が非常に厳しく，また，開発期間がより短いことや保守管理の労力の低減も同時に求められている．自動車内で提供される情報通信サービスには，交通情報，観光情報，電子メール，一般情報(例えばニュース)などが含まれるが，このような情報はディスプレイ上に文字で表示するよりも，音声により提供する方が望ましいとされている．文字情報を音声に変換する技術の研究開発は進んでいるが，その合成音声の韻律は不自然という問題がある．その原因として大きな割合を占めるものはポーズ位置の誤りであり，これを改善することにより韻律の改善が可能となる．ポーズ位置を制御する手法として，係り受け解析を利用する方法が研究されている\cite{Suzuki1995,Umiki1996,Sato1999,Shimizu1999}．これらの手法の中で，海木ら\cite{Umiki1996}や清水ら\cite{Shimizu1999}の手法は係り受けの距離が2以上の文節の後にポーズを挿入するという方法であり，その有効性がすでに示されている．そしてこの手法を実現するためには，高精度な係り受け解析が必要となる．文節まとめあげは図\ref{fig:文節まとめあげ}のように，形態素解析された日本語文を文節にまとめあげる処理のことをいう．この処理は，日本語文の係り受け解析に重要となるものであるため，文節まとめあげの精度が高いことが望まれる\footnote{形態素解析の精度は，既に十分高い精度を得られている．}．本研究はこのように，係り受け解析にとって重要な位置を占めている文節まとめあげに関する研究報告である．\begin{figure}\begin{center}\begin{tabular}{cl}\fbox{日本語文}&うまく日本語文を解析する．\\$\downarrow$&$\downarrow$\\\fbox{形態素解析}&うまく,日本語,文,を,解析,する,．\\$\downarrow$&$\downarrow$\\\fbox{\bold文節まとめあげ}&うまく｜日本語文を｜... [1,000 / 19,030 chars] |

### Public Sources

- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  source card for the NLP Journal retrieval tasks.
- [言語処理学会論文誌 LaTeX コーパス](https://github.com/jenio/nlp-journal-latex-corpus),
  upstream corpus repository.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2022.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/NLPJournalAbsArticleRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalAbsArticleRetrieval.V2),
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
| An abstract about extracting bilingual dictionary entries from parallel corpora using maximum entropy models. | The full paper beginning with an introduction on bilingual dictionaries for multilingual NLP systems. |
| An abstract about acquiring local summarization knowledge from Japanese news corpora. | The full article discussing automatic summarization and replacement rules. |
| An abstract about bunsetsu grouping for Japanese analysis in speech synthesis. | The corresponding full article on vehicle information systems and Japanese text analysis for speech synthesis. |
| An abstract introducing a related-term collection problem using web search statistics. | The full paper discussing specialized terms, relation measures, and candidate term collection. |
| An abstract about the effect of raw corpora and colloquial expressions in statistical NLP. | The full paper introducing corpus-related problems and statistical language processing motivation. |
