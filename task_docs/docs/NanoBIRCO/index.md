# NanoBIRCO

## Overview

NanoBIRCO is the compact Nano set for BIRCO, a benchmark focused on retrieval
tasks with complex objectives. The queries are often long descriptions of a
goal rather than short keyword searches: refute an argument, find matching
clinical trials for a patient, retrieve scientific abstracts for a nuanced
research need, recover a literary quotation from its surrounding context, or
identify a book from an incomplete memory.

The group is useful because topical similarity is not enough. A retrieved text
can share vocabulary with the query and still fail the objective: a clinical
trial may exclude the patient, an abstract may study a nearby but wrong problem,
a same-topic argument may agree rather than rebut, and a book description may
match the setting but not the remembered work. BM25 shows how far lexical
overlap goes on these long queries, dense retrieval tests objective-level
semantic matching, and `reranking_hybrid` indicates whether combining both
signals gives a better candidate pool.

## What This Group Measures

[BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives](https://arxiv.org/abs/2402.14151)
frames retrieval as objective satisfaction. NanoBIRCO keeps five of those
objective-heavy task families in compact English form: argument retrieval,
clinical-trial matching, DORIS-MAE scientific abstract retrieval, RELIC literary
quotation retrieval, and WhatsThatBook-style book identification.

The shared difficulty is constraint handling. The query usually contains
multiple clues or requirements, and the positive document must satisfy the
whole retrieval goal. This makes NanoBIRCO a good group for testing whether an
embedding model retrieves by intent and constraints, rather than only by topic,
genre, or repeated words.

## Task Families

- **Counterargument retrieval:** `NanoBIRCOArguAna` uses long arguments as
  queries and expects documents that directly challenge the stance.
- **Clinical-trial retrieval:** `NanoBIRCOClinicalTrial` maps patient cases to
  trial records. Inclusion and exclusion criteria matter.
- **Scientific abstract retrieval:** `NanoBIRCODorisMae` retrieves abstracts for
  detailed research needs, often with many valid positives.
- **Literary quotation retrieval:** `NanoBIRCORelic` uses context around a
  missing quotation and requires recovering the relevant literary passage.
- **Book identification:** `NanoBIRCOWTB` retrieves books from vague reader
  memories of plot, characters, setting, or atmosphere.

## Dataset Shape

NanoBIRCO contains 5 task pages, 408 queries, 18,789 split-local documents, and
2,909 positive qrel rows. Three tasks are single-positive in the observed
metadata: ArguAna, RELIC, and WTB. ClinicalTrial and DORIS-MAE are strongly
multi-positive, with average positives per query above 20.

This is one of the long-query Nano groups. Query averages range from about 497
characters in ClinicalTrial to more than 1,100 characters in ArguAna. Documents
are also substantial: clinical trial records, scientific abstracts, arguments,
and book descriptions often exceed paragraph scale. Long text alone is not the
core challenge; the harder problem is matching all constraints in the query.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest on `NanoBIRCOArguAna` and `NanoBIRCODorisMae`, where long
queries share useful topical vocabulary with counterarguments or scientific
abstracts. It is much weaker on RELIC and WTB because the important clue may be
indirect, partial, or absent from the query surface. ClinicalTrial is also hard:
medical terms overlap, but eligibility depends on inclusion and exclusion
criteria.

The BM25 results are a reminder that long queries do not automatically make
sparse retrieval easy. More words can provide more anchors, but they can also
retrieve many plausible neighbors that fail the objective.

### Dense Profile

Dense retrieval improves objective matching on several tasks, especially
ArguAna, ClinicalTrial, and DORIS-MAE. These tasks reward semantic alignment
between a complex need and a document that satisfies it. Dense retrieval is less
successful on RELIC, where the missing quotation problem often depends on
specific literary context, and it only modestly improves WTB because vague book
memories can describe many similar works.

For model researchers, this group is useful for checking whether dense
retrieval handles long, constraint-heavy queries without collapsing them into
generic topical similarity.

### Reranking Hybrid Profile

`reranking_hybrid` is the best profile for `NanoBIRCOWTB` and remains
competitive on the other tasks. It is particularly useful when a sparse match
captures a rare clue while dense retrieval captures the broader objective. In
clinical, literary, and book-identification settings, that complementarity can
matter more than either signal alone.

For reranker experiments, NanoBIRCO is a candidate-coverage stress test. A
reranker cannot fix the task if first-stage retrieval drops the one document
that satisfies the objective.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoBIRCOArguAna](NanoBIRCOArguAna.md) | argument to counterargument | 98 | 3,081 | 98 | 0.4293 | 0.5062 | 0.4932 | Dense |
| [NanoBIRCOClinicalTrial](NanoBIRCOClinicalTrial.md) | patient case to trial record | 50 | 3,375 | 1,042 | 0.1322 | 0.2152 | 0.1959 | Dense |
| [NanoBIRCODorisMae](NanoBIRCODorisMae.md) | research need to abstract | 60 | 5,544 | 1,569 | 0.3866 | 0.4140 | 0.4012 | Dense |
| [NanoBIRCORelic](NanoBIRCORelic.md) | literary context to quotation | 100 | 5,023 | 100 | 0.1314 | 0.0725 | 0.1276 | BM25 |
| [NanoBIRCOWTB](NanoBIRCOWTB.md) | vague memory to book | 100 | 1,766 | 100 | 0.2669 | 0.2714 | 0.3376 | Reranking hybrid |

## Interpretation Notes for Model Researchers

NanoBIRCO should be read as a constraint-following retrieval benchmark. Strong
performance implies more than matching topic labels: the model must retrieve a
document that satisfies the query's purpose. The most informative failures are
near misses, such as same-disease trials with wrong eligibility, same-topic
arguments with wrong stance, or similar books that do not match the remembered
details.

The group is also useful for separating long-context encoding from objective
matching. ArguAna and DORIS-MAE provide enough query text for lexical and dense
signals, while RELIC and WTB show that long or descriptive queries can still be
underspecified. Compare BM25, dense, and hybrid profiles before attributing a
score change to model size or context length alone.

## Training and Leakage Notes

Useful training data includes non-overlapping BIRCO-style objective retrieval
pairs, argument-counterargument pairs, clinical-trial eligibility matching,
scientific abstract recommendation, literary quotation retrieval, and book
description search. ClinicalTrial and DORIS-MAE should use multi-positive
training objectives where possible.

Exclude NanoBIRCO evaluation queries, positives, qrels, and direct synthetic
variants. For synthetic data, generate hard negatives that share topic or
vocabulary but fail a key requirement: wrong trial eligibility, wrong stance,
wrong literary passage, wrong abstract contribution, or wrong book identity.

## Public Sources

- [BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives](https://arxiv.org/abs/2402.14151), 2024.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives | 2024 | paper | [https://arxiv.org/abs/2402.14151](https://arxiv.org/abs/2402.14151) |
