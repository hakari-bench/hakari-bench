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

Representative queries include titles about extracting bilingual word pairs
with maximum entropy, acquiring local summarization knowledge, applying
multiple decision lists for bunsetsu grouping, collecting related terms, and
extracting colloquial strings from character statistics. The positive documents
are the corresponding introduction sections from Japanese NLP Journal papers.

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
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| 言語処理学会論文誌 LaTeX コーパス |  | repository | https://github.com/jenio/nlp-journal-latex-corpus |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A title about maximum entropy extraction of bilingual word pairs. | An introduction about bilingual dictionaries, multilingual systems, and corpus-based extraction. |
| A title about automatic acquisition of local summarization knowledge. | An introduction motivating automatic summarization for large electronic text collections. |
| A title about sequential application of multiple decision lists for bunsetsu grouping. | An introduction about in-vehicle information systems and Japanese analysis for speech synthesis. |
| A title about a related-term collection problem and solution. | An introduction explaining specialized terms and the importance of relationships among them. |
| A title about automatic extraction of colloquial strings using character statistics. | An introduction discussing corpus use, annotation cost, and problems in raw-corpus processing. |
