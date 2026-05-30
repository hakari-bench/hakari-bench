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

Representative queries include abstracts about bilingual dictionary extraction,
local summarization, Japanese bunsetsu grouping for speech synthesis,
related-term collection, and corpus effects in statistical NLP. The positive
documents are the corresponding introduction sections, which motivate the same
research problems and introduce the paper's core technical setting.

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
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| 言語処理学会論文誌 LaTeX コーパス |  | repository | https://github.com/jenio/nlp-journal-latex-corpus |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| An abstract about extracting bilingual word pairs from parallel corpora. | An introduction motivating bilingual dictionaries and corpus-based extraction. |
| An abstract about automatically acquiring local summarization knowledge. | An introduction discussing information overload and automatic summarization. |
| An abstract about bunsetsu grouping for speech synthesis in vehicle information systems. | An introduction describing constraints and needs for in-vehicle language processing. |
| An abstract proposing a related-term collection problem. | An introduction explaining why knowing relations among specialized terms matters. |
| An abstract about raw corpora and colloquial expressions in statistical NLP. | An introduction discussing corpus quality, annotation cost, and raw-corpus advantages. |
