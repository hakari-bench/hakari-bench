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
| 機械翻訳などの多言語間自然言語処理で用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には一貫性・網羅性などの点で限界があることから対訳コーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳関係の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．素性関数として共起情報を用いるモデルと品詞情報を用いるモデルを定義した．共起情報により対訳関係にある単語の意味を制約し，品詞情報により対訳関係にある単語の品詞を制約する．本手法の有効性を示すために日英対訳コーパスを用いた対訳単語対の抽出実験を行い，本論文で提案した手法が従来の手法よりも精度・再現率において優れた結果となり，また，テストコーパスによる実験では学習コーパスに出現しなかった単語対に関しても学習データに現れたものとほぼ同等の精度・再現率で抽出できることを示した． [423 chars] | \label{sec:intro}機械翻訳などの多言語間システムの構築において対訳辞書は必要不可欠であり，その品質がシステム全体の性能を左右する．これらに用いられる対訳辞書は現在，人手によって作成されることが多い．しかし，人手による作成には限界があり，品質を向上するためには膨大な労力が必要であること，辞書の記述の一貫性を保つことが困難であることが問題となる．このことからコーパスから自動的に対訳辞書を作成しようとする研究が近年盛んに行われている\cite{gale_91,kaji_96,kitamura_96,fung_97,melamed_97}．本論文では，最大エントロピー法を用いて対訳コーパス上に対訳単語対の確率モデルを推定し，自動的に対訳単語対を抽出する手法を提案する．本論文では対訳関係にある単語の組を対訳単語対と呼ぶ．最大エントロピー法は，与えられた制約の中でエントロピーを最大化するようなモデルを推定するという最大エントロピー原理に基づいており，未知データに対しても確率値をなるべく一様に配分するため，自然言語処理においてしばしば問題となるデータスパースネスに比較的強いという特徴を持っている．このため，構文解析\cite{ratnaparkhi_97,wojciech_98,uchimoto_99}，文境界の同定\cite{reynar_97}，動詞の下位範疇化モデル\cite{utsuro_97b}などに応用されている．また我々の手法は，既存の対訳辞書を必要とせず，文対応の付いた対訳コーパスさえあれば，対訳コーパスの分野を限定することなく対訳単語対を抽出できるという特徴を持つ．本論文の構成は以下の通りである．\ref{sec:ME_method}節では最大エントロピー法について説明し，\ref{sec:MEdict}節では最大エントロピー法を用いて対訳単語対を抽出する手法を述べる．\ref{sec:experiment_discussion}節では我々が提案した手法の有効性を示すために行った実験の結果とそれに対する考察を述べ，関連研究との比較を行う．\ref{sec:future}節でまとめを述べる． [920 chars] |
| 日本語ニュースを局所的要約する際に必要となる要約知識を，コーパスから自動獲得する手法について述べる．局所的要約とは注目個所の近傍の情報（局所的情報）を用いて行なう要約をいう．局所的情報には注目個所そのものやその前後の単語列などがある．本手法では要約知識として置換規則と置換条件を用い，これらを原文−要約文コーパスから自動獲得する．はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間の距離を計算し，ＤＰマッチングによって最適な単語対応を求める．その結果より，置換規則は単語対応上で不一致となる単語列として獲得する．一方，置換条件は置換規則の前後ｎグラムの単語列として獲得する．原文と要約文にそれぞれＮＨＫニュース原稿とＮＨＫ文字放送の原稿を使って実際に要約知識を自動獲得し，得られた要約知識を評価する実験を行った．その結果，妥当な要約知識が獲得できることを確認した． [392 chars] | \label{sec:sec1}インターネットの普及も手伝って，最近は電子化されたテキスト情報を簡単にかつ大量に手にいれることが可能となってきている．このような状況の中で，必要な情報だけを得るための技術として文章要約は重要であり，計算機によって要約を自動的に行なうこと，すなわち自動要約が望まれる．自動要約を実現するためには本来，人間が文章を要約するのと同様に，原文を理解する過程が当然必要となる．しかし，計算機が言語理解を行うことは現在のところ非常に困難である．実際，広範囲の対象に対して言語理解を扱っている自然言語処理システムはなく，ドメインを絞ったトイシステムにとどまっている．一方では言語理解に踏み込まずともある程度実現されている自然言語処理技術もある．例えば，かな漢字変換や機械翻訳は，人間が適切に介在することにより広く利用されている．自動要約の技術でも言語理解を導入せずに，表層情報に基づいたさまざまな手法が提案されている．これらの手法による要約は用いる情報の範囲により大きく２つに分けることができる．本論文では文章全体にわたる広範な情報を主に用いて行なう要約を{\gt大域的要約}，注目個所の近傍の情報を用いて行なう要約を{\gt局所的要約}と呼ぶ．我々は字幕作成への適用も視野に入れ，現在，局所的要約に重点を置き研究している．局所的要約を実現するには，後述する要約知識が必須であり，これをどのようにして獲得するかがシステムを構築する際のポイントとなる．本論文ではこのような要約知識（置換規則と置換条件）を，コーパス（原文−要約文コーパス）から自動的に獲得する手法について述べる．本手法では，はじめに原文中の単語と要約文中の単語のすべての組み合わせに対して単語間の距離を計算し，ＤＰマッチングによって最適な単語対応を求める．その結果から置換規則は単語対応上で不一致となる単語列として得られる．一方，置換条件は置換規則の前後ｎグラムの単語列として得られる．ＮＨＫニュースを使って局所的要約知識の自動獲得実験を行い，その有効性を検証する実験を行ったのでその結果についても述べる．以下，~\ref{sec:sec2}~章では自動要約に関して{\gt大域的要約}と{\gt局所的要約}について説明をする．~\ref{sec:sec3}~章では要約知識を自動獲得する際にベースとなる，原文−要約文... [1,000 / 1,203 chars] |
| 近年の高度情報化の流れにより，自動車にも種々の情報機器が搭載されるようになり，その中で音声認識・合成の必要性が高まっている．本研究は音声合成を行うための日本語解析の中で基本となる，文節まとめあげに関する研究報告である．従来の文節まとめあげは，人手規則による手法と機械学習による手法の二つに大きく分けられる．前者は，長年の努力により非常に高い精度を得られているが，入力データ形式が固定であるために柔軟性に欠け，人手で規則を作成・保守管理するため多大な労力を要し，車載情報機器へ実装するには問題が大きい．また後者は，それらの問題に柔軟に対処できるが，精度を向上させるためにアルゴリズムが複雑化しており，その結果開発期間が延長するなどの問題が生じ，車載情報機器には不向きである．そこで本研究は，決定リストを用いる手法を発展させ，複数の決定リストを順に適用するだけという非常に簡明な文節まとめあげの手法を提案する．決定リストの手法は非常に単純であるが，それだけでは高い精度が得られない．そこで，決定リストを一つではなく複数作成し，それぞれのリストを最適な順序に並べて利用することにより精度向上を図った．この結... [500 / 589 chars] | 近年の高度情報化の流れにより，種々の情報機器が自動車にも搭載されるようになり，さまざまな情報通信サービスが広がりつつある．このような車載情報機器は，自動車に搭載するためにCPUの速度やRAM，ROMなどのメモリ容量の制約が非常に厳しく，また，開発期間がより短いことや保守管理の労力の低減も同時に求められている．自動車内で提供される情報通信サービスには，交通情報，観光情報，電子メール，一般情報(例えばニュース)などが含まれるが，このような情報はディスプレイ上に文字で表示するよりも，音声により提供する方が望ましいとされている．文字情報を音声に変換する技術の研究開発は進んでいるが，その合成音声の韻律は不自然という問題がある．その原因として大きな割合を占めるものはポーズ位置の誤りであり，これを改善することにより韻律の改善が可能となる．ポーズ位置を制御する手法として，係り受け解析を利用する方法が研究されている\cite{Suzuki1995,Umiki1996,Sato1999,Shimizu1999}．これらの手法の中で，海木ら\cite{Umiki1996}や清水ら\cite{Shimizu1999}の手法は係り受けの距離が2以上の文節の後にポーズを挿入するという方法であり，その有効性がすでに示されている．そしてこの手法を実現するためには，高精度な係り受け解析が必要となる．文節まとめあげは図\ref{fig:文節まとめあげ}のように，形態素解析された日本語文を文節にまとめあげる処理のことをいう．この処理は，日本語文の係り受け解析に重要となるものであるため，文節まとめあげの精度が高いことが望まれる\footnote{形態素解析の精度は，既に十分高い精度を得られている．}．本研究はこのように，係り受け解析にとって重要な位置を占めている文節まとめあげに関する研究報告である．\begin{figure}\begin{center}\begin{tabular}{cl}\fbox{日本語文}&うまく日本語文を解析する．\\$\downarrow$&$\downarrow$\\\fbox{形態素解析}&うまく,日本語,文,を,解析,する,．\\$\downarrow$&$\downarrow$\\\fbox{\bold文節まとめあげ}&うまく｜日本語文を｜解析する．\\$\downar... [1,000 / 1,703 chars] |

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
