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

Representative queries include abstracts about extracting bilingual word pairs
with maximum entropy models, acquiring local summarization rules from corpora,
Japanese bunsetsu grouping for speech synthesis, collecting related technical
terms using web statistics, and the influence of corpora in statistical NLP.
The positive documents are the corresponding full paper texts from the NLP
Journal LaTeX Corpus.

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
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| 言語処理学会論文誌 LaTeX コーパス |  | repository | https://github.com/jenio/nlp-journal-latex-corpus |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| An abstract about extracting bilingual dictionary entries from parallel corpora using maximum entropy models. | The full paper beginning with an introduction on bilingual dictionaries for multilingual NLP systems. |
| An abstract about acquiring local summarization knowledge from Japanese news corpora. | The full article discussing automatic summarization and replacement rules. |
| An abstract about bunsetsu grouping for Japanese analysis in speech synthesis. | The corresponding full article on vehicle information systems and Japanese text analysis for speech synthesis. |
| An abstract introducing a related-term collection problem using web search statistics. | The full paper discussing specialized terms, relation measures, and candidate term collection. |
| An abstract about the effect of raw corpora and colloquial expressions in statistical NLP. | The full paper introducing corpus-related problems and statistical language processing motivation. |
