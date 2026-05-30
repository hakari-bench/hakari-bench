# NanoJMTEB-v2 / ja_cwir

## Overview

`NanoJMTEB-v2 / ja_cwir` is the Nano split of JaCWIR, a Japanese casual web
information retrieval task. Queries are short Japanese questions, and the corpus
contains compact web-page title and description snippets drawn from broad web
content. The task is useful for studying Japanese web-search behavior where the
target document is not a long answer passage, but the page that best matches a
synthetic user question. In the Nano split, the retrieval problem has 200
queries, 10,000 documents, and exactly one positive document per query. Current
candidate diagnostics show a strongly lexical task profile: BM25 is the best
direct ranker at nDCG@10, dense retrieval is still strong but lower, and the
reranking hybrid candidate set restores full top-100 positive coverage while
not surpassing BM25's top-10 ordering.

## Details

### What the Original Data Measures

The JaCWIR dataset card describes the source data as a Japanese casual web IR
collection built from web-page titles and meta descriptions. Questions were
generated from one source page, and the linked page is treated as the relevant
document. JMTEB then reformats this retrieval setting for Japanese embedding
evaluation, connecting it to the broader MTEB-style retrieval protocol.

This provenance matters for interpretation. The task is not a human query log,
not a Wikipedia passage benchmark, and not a tightly edited FAQ corpus. It
measures whether a retrieval model can recover the source page behind a
Japanese question from noisy title-plus-description snippets. Many documents are
short summaries, headlines, blog descriptions, service pages, or news-like
fragments. A model must often recognize the right page from title cues and
topic alignment rather than from an explicit answer sentence.

### Observed Data Profile

The Nano split contains 200 queries and 10,000 candidate documents. It has 200
positive qrel rows: one positive for every query, with no multi-positive
queries. Queries average 33.80 characters, while documents average 189.04
characters. This is a short-query, short-document retrieval task, but the
documents are usually longer than titles alone because they include page
descriptions.

The examples cover broad Japanese web topics: U.S. labor-market news, TPP and
manga copyright concerns, UX terminology, Bitcoin mining explanations, and
electronic-contract articles. Positives are often recognizable by exact named
entities, technical terms, and page-title phrasing. Some descriptions include
partial summaries or introductory text rather than a direct answer, so the task
also includes realistic web-page noise.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset has 500 candidates per query and
achieves nDCG@10 = 0.9181, hit@10 = 0.9750, and recall@100 = 1.0000. This is
the strongest of the three observed candidate profiles by top-10 ranking. The
result indicates that JaCWIR's Nano split has substantial lexical recoverability:
query terms, page-title words, named entities, and technical expressions often
overlap directly enough for BM25 to identify the target page.

For researchers, this means `ja_cwir` should not be read as a purely semantic
paraphrase benchmark. Japanese lexical matching is central. A model that
underweights exact words, product names, legal terms, title phrases, or topic
keywords may lose to BM25 even if it has strong embedding similarity on more
paraphrastic tasks. The perfect top-100 recall also means BM25 is an excellent
candidate generator for this task: almost all remaining difficulty is in
ordering the positive near the very top, not in surfacing it somewhere in a
large candidate pool.

### Dense Evaluation Profile

The dense profile uses the `harrier_oss_v1_270m` candidate subset with 500
candidates per query. It reaches nDCG@10 = 0.8367, hit@10 = 0.9100, and
recall@100 = 0.9550. Dense retrieval is clearly effective: it captures many
topic-level relationships between questions and web-page snippets, and it helps
when the query asks for a concept rather than repeating title words exactly.

At the same time, dense retrieval is weaker than BM25 here. The gap suggests
that embedding similarity sometimes retrieves pages that are semantically close
but not the original linked page. In a broad web corpus, many pages can share
the same general topic, while the correct page may be distinguished by a title
phrase, a named entity, or a narrow lexical signal. This is an important
diagnostic for Japanese retrieval models: strong semantic matching is necessary
but not sufficient when the benchmark rewards recovering a particular source
snippet among many plausible web documents.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query. It achieves nDCG@10 = 0.8810, hit@10 = 0.9550, and recall@100 = 1.0000,
with no rank-101 safeguard rows. This profile emulates a hybrid search setup
that combines lexical and dense evidence before reranking. Its recall matches
BM25 and exceeds dense retrieval, while its top-10 ordering improves over dense
but remains below BM25.

This pattern is informative: hybrid retrieval successfully keeps the lexical
strength of BM25 for candidate coverage while adding semantic alternatives that
dense retrieval can contribute. However, for this particular task, adding dense
evidence does not automatically improve the final top-10 ranking over BM25.
Researchers should therefore evaluate both candidate coverage and rank quality.
On `ja_cwir`, the hybrid set is useful for robust reranking experiments, but a
reranker must still learn when exact Japanese page-title evidence should win
over broader semantic similarity.

### Metric Interpretation for Model Researchers

Because every query has exactly one positive document, hit@10 and nDCG@10 are
easy to interpret. Hit@10 measures whether the target page appears in the first
ten results; nDCG@10 additionally rewards placing it closer to rank 1. Recall@100
measures whether a candidate-generation stage can keep the positive available
for later reranking.

The current values show a task where lexical candidate generation is already
near saturated. Improvements will mostly come from better top-rank ordering,
especially distinguishing the intended source page from topically related pages.
For rerankers, `ja_cwir` is a useful stress test of whether the model can use
both exact Japanese surface cues and semantic page-question compatibility.

### Query and Relevance Type Tendencies

Queries are natural Japanese questions, often asking why something happens, what
a concept means, or what an article explains. Relevance is page-level rather
than answer-span-level. The positive document usually contains a title plus a
description, so the answer may be implied by the page topic rather than stated
as a clean sentence.

The task therefore rewards models that can combine web-search intent matching,
Japanese keyword precision, and robust handling of short noisy snippets. It is
less suitable as a pure reading-comprehension task because the document selected
as relevant is the source page, not necessarily the shortest passage that
answers the question.

### Representative Failure Modes

BM25 may fail when query words appear more frequently in a related but wrong
page, or when the positive description is noisy and does not repeat the query's
main expression. Dense retrieval may fail by ranking semantically related pages
above the exact source page, especially when many documents discuss the same
topic. Hybrid retrieval can inherit both behaviors: it usually keeps the
positive available, but it still needs a reranker that can resolve fine-grained
page identity.

Other likely errors include over-reliance on common explanatory phrases, weak
handling of named entities embedded in Japanese text, and confusion between an
article title and a different page that discusses the same event or concept.

### Training Data That May Help

Helpful training data would include Japanese web search pairs, title-and-meta
description retrieval pairs, and question-to-page supervision over noisy
snippets. Synthetic data can help if it preserves realistic web-page artifacts:
partial descriptions, headlines, service-page summaries, dates, and mixed
genres. Training only on clean Wikipedia passages or FAQ answers is unlikely to
cover the full retrieval behavior tested here.

Evaluation leakage should be avoided. Data generated from the Nano split,
JaCWIR evaluation questions, or the exact positive title-description strings
should not be used for training or hard-negative mining when reporting
comparable benchmark results.

### Model Improvement Notes

For dense retrievers, the main opportunity is to preserve exact Japanese lexical
signals while still capturing paraphrase and intent. Contrastive training with
hard negatives from same-topic web pages may be especially useful. For
rerankers, the task calls for fine-grained comparison of query intent against
title and description fields, including cases where the title carries the
decisive evidence and the description is only partially helpful.

For hybrid systems, this task argues for careful weighting rather than assuming
that dense evidence should always override BM25. A strong system should keep
BM25's high-recall lexical candidates, add dense semantic coverage where useful,
and learn a final ordering rule that respects exact source-page cues.

## Example Data

Representative examples include questions about why adult men in the United
States leave the labor market, why manga fans care about TPP, what matters in
the essence of UX, what Bitcoin mining does, and why seals are legally
unnecessary for electronic contracts. Their positives are web-page
title-description snippets rather than long answer passages. The examples show
why title words and topical page identity are both important: a query may look
like a question-answering item, but the target is the source page that motivated
the question.

### Public Sources

- [hotchpotch/JaCWIR](https://huggingface.co/datasets/hotchpotch/JaCWIR),
  dataset card for the Japanese Casual Web IR dataset.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  Japanese embedding benchmark card.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2022.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/JaCWIRRetrieval](https://huggingface.co/datasets/mteb/JaCWIRRetrieval),
  source task dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| hotchpotch/JaCWIR |  | dataset card | https://huggingface.co/datasets/hotchpotch/JaCWIR |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Japanese question about why adult men in the United States cannot stay in the labor market. | A web article title and description about incarceration, probation, parole, unemployment, and difficult employment conditions. |
| A question asking why manga fans pay attention to TPP. | A news-style page about copyright enforcement, doujin activity, and concerns about chilled creative work. |
| A question about the essence of UX. | A web-design or marketing article describing user experience as a concept. |
| A question asking what Bitcoin mining does. | An explanatory article title and description about basic Bitcoin mining knowledge. |
| A question about why seal impressions are legally unnecessary in electronic contracts. | A CloudSign article explaining electronic-contract validity and comparison with paper-contract seals. |
