# NanoLongEmbed

## Overview

NanoLongEmbed is the compact long-context retrieval group derived from
LongEmbed. It tests whether a retriever can select the correct long document
when evidence may be buried in books, scripts, meeting transcripts, Wikipedia
bundles, or synthetic long contexts. The group includes both real
long-document retrieval tasks and synthetic passkey or needle settings.

This group is different from ordinary passage retrieval. Documents are often
tens of thousands of characters long, and `NanoNarrativeQA` contains whole
narratives averaging more than 300,000 characters. A successful model must
retain enough signal from a long source to identify the correct document. BM25
is unusually strong because long documents contain many distinctive names and
events; dense retrieval tests long-context compression; `reranking_hybrid`
shows whether semantic candidates can recover from lexical dilution.

## What This Group Measures

[LongEmbed: Extending Embedding Models for Long Context Retrieval](https://aclanthology.org/2024.emnlp-main.47/)
introduces retrieval tasks designed for embedding long documents and long
contexts. NanoLongEmbed keeps six compact splits from that benchmark:
NarrativeQA, SummScreen, QMSum, 2WikiMultiHopQA, Passkey, and Needle.

The group measures document-level long-context retrieval. NarrativeQA,
SummScreen, QMSum, and 2WikiMultiHopQA retrieve real or dataset-derived long
sources. Passkey and Needle are synthetic probes where a small answer-bearing
statement is inserted into a long document. In all cases, the target is the
whole long document, not just a short passage.

## Task Families

- **Narrative retrieval:** `NanoNarrativeQA` retrieves books or movie scripts
  from story questions.
- **Transcript retrieval:** `NanoSummScreenFD` and `NanoQMSum` retrieve episode
  or meeting transcripts.
- **Multi-hop evidence bundle retrieval:** `Nano2WikiMultihopQA` retrieves
  concatenated Wikipedia evidence documents.
- **Synthetic long-context probes:** `NanoPasskey` and `NanoNeedle` retrieve
  long documents containing a matching inserted key or fact.

## Dataset Shape

NanoLongEmbed contains 6 task pages, 998 queries, 2,788 split-local documents,
and 998 positive qrel rows. Every task is single-positive in the current
metadata. Candidate pools are small compared with web retrieval, but documents
are extremely long.

Document length is the defining feature. `NanoNarrativeQA` averages more than
326,000 characters per document. QMSum, 2WikiMultiHopQA, Needle, Passkey, and
SummScreen also average tens of thousands of characters. Queries range from
short direct questions to long recaps and meeting requests. The challenge is not
corpus scale; it is representing enough of each long document to rank the right
source.

## Retrieval Behavior

### BM25 Profile

BM25 is the best profile for every NanoLongEmbed task in the current metadata.
This is not surprising: long documents contain many rare names, events, phrases,
and transcript terms that overlap with queries. `NanoSummScreenFD` and
`Nano2WikiMultihopQA` are especially strong because recaps, evidence bundles,
and source documents often share distinctive terms.

BM25 is still imperfect. NarrativeQA, Needle, Passkey, and QMSum can contain
many distractor terms, and the key evidence may be a small part of a very long
source. Sparse retrieval benefits from more words, but it can also over-rank
documents that share surface terms without containing the right fact.

### Dense Profile

Dense retrieval is weaker than BM25 on this group. The likely issue is
long-context compression: a single embedding must represent documents that are
much longer than ordinary passage inputs. Important evidence can be diluted by
story, meeting, or transcript context.

Dense scores are still useful diagnostically. If a model improves on
NarrativeQA, QMSum, or synthetic Needle/Passkey without losing BM25-like exact
anchors, it likely has better long-document representation rather than only
better passage semantics.

### Reranking Hybrid Profile

`reranking_hybrid` usually sits between BM25 and dense. It benefits from sparse
anchors while adding some semantic robustness, but it does not beat BM25 in the
current metadata. The hybrid profile is still relevant for reranking because it
has strong candidate coverage on single-positive long-document tasks.

For reranker experiments, the critical question is whether the correct long
document is present in the candidate pool. Once it is present, downstream
reranking or reading can focus on locating the evidence inside the document.

## Task Summary

| Task | Retrieval focus | Queries | Docs | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Nano2WikiMultihopQA](Nano2WikiMultihopQA.md) | multi-hop question to Wikipedia evidence bundle | 200 | 300 | 0.9503 | 0.8400 | 0.9111 | BM25 |
| [NanoNarrativeQA](NanoNarrativeQA.md) | story question to whole narrative document | 200 | 355 | 0.7619 | 0.3315 | 0.5120 | BM25 |
| [NanoNeedle](NanoNeedle.md) | fact query to long document with inserted needle | 98 | 800 | 0.7207 | 0.6099 | 0.6823 | BM25 |
| [NanoPasskey](NanoPasskey.md) | passkey query to long context | 100 | 800 | 0.7717 | 0.6473 | 0.7294 | BM25 |
| [NanoQMSum](NanoQMSum.md) | meeting request to transcript | 200 | 197 | 0.7440 | 0.3660 | 0.6097 | BM25 |
| [NanoSummScreenFD](NanoSummScreenFD.md) | episode recap to transcript | 200 | 336 | 0.9813 | 0.9198 | 0.9443 | BM25 |

## Interpretation Notes for Model Researchers

NanoLongEmbed should be read as a long-document representation benchmark, not
as a web-scale search benchmark. Candidate pools are small, but documents are
large. A model can fail because it cannot encode the whole source, because it
loses a small inserted fact, or because the query only references one part of a
long narrative.

The BM25 dominance is meaningful. It shows that exact rare terms remain very
powerful when documents are long. Dense models should be judged by whether they
can close the gap without losing those anchors. Improvements on NarrativeQA and
QMSum are especially informative because those tasks require selecting a whole
source from rich context.

## Training and Leakage Notes

Useful training data includes long-document QA, story and screenplay question
answering, meeting transcript retrieval, multi-hop Wikipedia retrieval, and
synthetic passkey or needle tasks with varied evidence positions. Training
should preserve full-document length or realistic truncation behavior.

Exclude NanoLongEmbed evaluation queries, positives, qrels, books, scripts,
transcripts, synthetic contexts, and direct variants. Source datasets such as
NarrativeQA, SummScreen, QMSum, and 2WikiMultiHopQA should be split-audited
before training.

## Public Sources

- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://aclanthology.org/2024.emnlp-main.47/), 2024.
- [The NarrativeQA Reading Comprehension Challenge](https://aclanthology.org/Q18-1023), 2018.
- [SummScreen: A Dataset for Abstractive Screenplay Summarization](https://aclanthology.org/2022.acl-long.589), 2022.
- [QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization](https://aclanthology.org/2021.naacl-main.472), 2021.
- [Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps](https://aclanthology.org/2020.coling-main.580), 2020.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | paper | [https://aclanthology.org/2024.emnlp-main.47/](https://aclanthology.org/2024.emnlp-main.47/) |
| The NarrativeQA Reading Comprehension Challenge | 2018 | paper | [https://aclanthology.org/Q18-1023](https://aclanthology.org/Q18-1023) |
| SummScreen: A Dataset for Abstractive Screenplay Summarization | 2022 | paper | [https://aclanthology.org/2022.acl-long.589](https://aclanthology.org/2022.acl-long.589) |
| QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization | 2021 | paper | [https://aclanthology.org/2021.naacl-main.472](https://aclanthology.org/2021.naacl-main.472) |
| Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps | 2020 | paper | [https://aclanthology.org/2020.coling-main.580](https://aclanthology.org/2020.coling-main.580) |
