# NanoLongEmbed / NanoNarrativeQA

## Overview

`NanoLongEmbed / NanoNarrativeQA` is the NarrativeQA long-document retrieval
task inside LongEmbed. Queries are short questions about stories, and documents
are whole books, plays, or movie scripts. The retrieval goal is to find the
source narrative that contains the event, motive, relationship, or fact needed
to answer the question. The Nano split has 200 queries, 355 documents, and one
positive document per query. Documents are extremely long, averaging 326,753.00
characters, and often include Project Gutenberg headers, license text, HTML, or
script-site boilerplate. Current diagnostics show BM25 as the strongest top-10
ranker, `reranking_hybrid` as the best recall@100 profile, and dense retrieval
as much weaker for this very long narrative setting.

## Details

### What the Original Data Measures

NarrativeQA was introduced as a reading-comprehension challenge over books and
movie scripts. Questions and answers were written from human summaries rather
than directly from the full text, so the questions often target story-level
events, motivations, and character relations. LongEmbed adapts this into a
long-context retrieval task by using the question as the query and the whole
source narrative as the candidate document.

The retrieval task therefore measures whether a model can identify the correct
long story source, not whether it can answer the question directly. The
answer-bearing evidence may occur far from the beginning, and the document may
contain large amounts of non-story preamble or markup.

### Observed Data Profile

The Nano split contains 200 queries, 355 documents, and 200 positive qrel rows.
Every query has exactly one positive, with no multi-positive queries. Queries
average 49.32 characters, while documents average 326,753.00 characters.

Representative questions ask why a character has not killed herself, what a
bomber leaves behind, whose hand a character takes in marriage, who Plato did
not deter from writing, or what Mrs. Lovett reveals to Todd. Positive documents
include Project Gutenberg books and IMSDb-style movie scripts. Several documents
begin with license headers, web markup, or metadata before narrative content.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 355-document corpus and
achieves nDCG@10 = 0.7619, hit@10 = 0.8450, and recall@100 = 0.9000. BM25 is
the strongest observed top-10 ranker. This shows that character names, rare
phrases, story titles, and distinctive event words are powerful signals even in
very long documents.

BM25's strength should not be mistaken for complete story understanding. It
does well when the question includes names or unusual terms that occur in the
source narrative. It is weaker when the question is short, uses pronouns, asks
about motivation, or refers to an event using language that differs from the
full text.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset covers the 355-document corpus
and achieves nDCG@10 = 0.3315, hit@10 = 0.4300, and recall@100 = 0.7500. Dense
retrieval is much weaker than BM25. A single embedding for an entire book or
screenplay is likely to dilute the small answer-bearing event, especially when
the document contains hundreds of thousands of characters.

Dense retrieval can capture broad genre or story similarity, but the task needs
source identification from a very specific question. If the model cannot retain
character names and localized events inside a long representation, it will rank
the wrong narrative above the positive.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 11 safeguard positive rows and a mean of 100.055 candidates. It
achieves nDCG@10 = 0.5120, hit@10 = 0.6550, and recall@100 = 0.9450. Hybrid
retrieval improves over dense retrieval and gives the best candidate coverage,
but it remains well below BM25 for top-10 ranking.

The hybrid result suggests that dense retrieval adds some positives that BM25
misses, especially where wording is paraphrastic, while BM25 remains the
primary ranking signal for story-source identification. A reranker using the
hybrid pool would need to inspect character and event evidence more directly to
convert the higher recall into better top ranks.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. Hit@10 measures whether the correct
book or script appears in the first ten results, nDCG@10 rewards ranking it
near the top, and recall@100 measures whether candidate generation keeps it
available for reranking.

The current metrics show a long-document failure mode for dense retrieval. BM25
is strongest, hybrid improves coverage, and dense is weakest. For long-context
embedding research, this task is useful for testing whether document
representations preserve localized narrative evidence rather than only global
topic or genre.

### Query and Relevance Type Tendencies

Queries are short story questions about motives, deaths, relationships, objects,
actions, and event consequences. Relevant documents are entire source
narratives. A question may be answerable from one scene or paragraph, but the
retrieval unit is the full book or script.

The task rewards models that preserve character names, object mentions, event
phrases, and scene-level evidence across extremely long documents. It also
tests robustness to non-content boilerplate at the beginning of documents.

### Representative Failure Modes

BM25 can fail when questions use generic words, pronouns, or paraphrases rather
than distinctive names. Dense retrieval can fail through representation
dilution: the event needed to answer the question is a tiny part of the whole
document. Hybrid retrieval can keep more positives but still rank documents
with overlapping names or genres incorrectly.

Another failure mode is over-weighting the beginning of documents. Project
Gutenberg license text or script-site HTML can consume early tokens and obscure
the narrative content if the encoder truncates or summarizes poorly.

### Training Data That May Help

Useful training data includes official non-overlapping NarrativeQA train pairs,
long-form book and screenplay question-document retrieval pairs, story-level QA
over chapters or full narratives, and hard negatives from similar stories or
shared character names. Training should preserve long-context noise such as
prefaces, scene headers, license text, and distant evidence.

Comparable evaluation should exclude NarrativeQA test data, Nano queries,
qrels, and positive long documents likely to overlap with this split.

### Model Improvement Notes

Dense retrievers need better long-document representations for localized story
events. Chunk-level retrieval, multi-vector document indexes, late interaction,
or hierarchical retrieval may be more suitable than a single global embedding.
Sparse systems should preserve character names and rare phrases. Rerankers
should search for answer-bearing scenes rather than judging the whole document
by global similarity.

For hybrid systems, `NanoNarrativeQA` suggests using BM25 for precise source
signals and dense retrieval for paraphrase coverage, followed by a passage-aware
reranker.

## Example Data

| Query | Positive document |
| --- | --- |
| Why hasn't Irena killed herself before? [39 chars] | ï»¿The Project Gutenberg EBook of When We Dead Awaken, by Henrik Ibsen This eBook is for the use of anyone anywhere at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the terms of the Project Gutenberg License included with this eBook or online at www.gutenberg.org Title: When We Dead Awaken Author: Henrik Ibsen Commentator: William Archer Translator: William Archer Release Date: December, 2003 [EBook #4782] Posting Date: February 17, 2010 Language: English *** START OF THIS PROJECT GUTENBERG EBOOK WHEN WE DEAD AWAKEN *** Produced by Sonia K WHEN WE DEAD AWAKEN By Henrik Ibsen. Introduction and translation by William Archer. INTRODUCTION. From _Pillars of Society_ to _John Gabriel Borkman_, Ibsen's plays had followed each other at regular intervals of two years, save when his indignation over the abuse heaped upon _Ghosts_ reduced to a single year the interval between that play and _An Enemy of the People_. _John Gabriel Borkman_ hav... [1,000 / 131,749 chars] |
| What does the bomber leave behind that reveals his identity? [60 chars] | <html> <head><title>Source Code Script at IMSDb.</title> <meta name="description" content="Source Code script at the Internet Movie Script Database."> <meta name="keywords" content="Source Code script, Source Code movie script, Source Code film script"> <meta name="viewport" content="width=device-width, initial-scale=1" /> <meta name="HandheldFriendly" content="true"> <meta http-equiv="content-type" content="text/html; charset=iso-8859-1"> <meta http-equiv="Content-Language" content="EN"> <meta name=objecttype CONTENT=Document> <meta name=ROBOTS CONTENT="INDEX, FOLLOW"> <meta name=Subject CONTENT="Movie scripts, Film scripts"> <meta name=rating CONTENT=General> <meta name=distribution content=Global> <meta name=revisit-after CONTENT="2 days"> <link href="/style.css" rel="stylesheet" type="text/css"> <script type="text/javascript"> var _gaq = _gaq \|\| []; _gaq.push(['_setAccount', 'UA-3785444-3']); _gaq.push(['_trackPageview']); (function() { var ga = document.createElement('script'); ga... [1,000 / 219,018 chars] |
| Whose hand does Grayes reluctantly take in marriage? [52 chars] | ï»¿The Project Gutenberg EBook of Desperate Remedies, by Thomas Hardy This eBook is for the use of anyone anywhere at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the terms of the Project Gutenberg License included with this eBook or online at www.gutenberg.org Title: Desperate Remedies Author: Thomas Hardy Release Date: November 2000 [EBook #3044] Posting Date: May 25, 2009 Language: English *** START OF THIS PROJECT GUTENBERG EBOOK DESPERATE REMEDIES *** Produced by Les Bowler DESPERATE REMEDIES By Thomas Hardy CONTENTS PREFATORY NOTE I. THE EVENTS OF THIRTY YEARS II. THE EVENTS OF A FORTNIGHT III. THE EVENTS OF EIGHT DAYS IV. THE EVENTS OF ONE DAY V. THE EVENTS OF ONE DAY VI. THE EVENTS OF TWELVE HOURS VII. THE EVENTS OF EIGHTEEN DAYS VIII. THE EVENTS OF EIGHTEEN DAYS IX. THE EVENTS OF TEN WEEKS X. THE EVENTS OF A DAY AND NIGHT XI. THE EVENTS OF FIVE DAYS XII. THE EVENTS OF TEN MONTHS XIII. THE EVENTS OF ONE DAY XIV. THE EVENTS... [1,000 / 817,284 chars] |

### Public Sources

- [The NarrativeQA Reading Comprehension Challenge](https://arxiv.org/abs/1712.07040),
  2018.
- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096),
  2024.
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed), source
  dataset card.
- [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The NarrativeQA Reading Comprehension Challenge | 2018 | arXiv paper | [https://arxiv.org/abs/1712.07040](https://arxiv.org/abs/1712.07040) |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | [https://arxiv.org/abs/2404.12096](https://arxiv.org/abs/2404.12096) |
| dwzhu/LongEmbed | 2024 | dataset card | [https://huggingface.co/datasets/dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A story question asking why Irena has not killed herself before. | A full Project Gutenberg narrative containing the relevant character and event context. |
| A question asking what a bomber leaves behind that reveals identity. | A movie-script HTML document containing the relevant scene. |
| A question asking whose hand Grayes reluctantly takes in marriage. | A long novel text where the marriage event appears far inside the narrative. |
| A question about who Plato did not deter from writing, according to Cicero. | A long classical text or translation with the relevant passage embedded inside. |
| A question asking what Mrs. Lovett revealed to Todd. | A screenplay document with script markup and the relevant dialogue. |
