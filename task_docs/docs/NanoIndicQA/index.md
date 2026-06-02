# NanoIndicQA

## Overview

NanoIndicQA is a language-specific Nano benchmark for IndicQA retrieval. It
covers eleven Indic language splits: Assamese, Bengali, Gujarati, Hindi,
Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu. Each split turns
an IndicQA reading-comprehension example into retrieval: the query is a
question in the target language, and the positive document is the context
paragraph containing the evidence needed to answer it.

The group is useful as a controlled multilingual passage-selection benchmark.
All languages share the same retrieval shape, so differences mainly reflect
script, morphology, paragraph length, named entities, and model coverage for
Indic languages. BM25 shows how far exact same-language term matching goes,
dense retrieval tests cross-script semantic passage matching, and
`reranking_hybrid` shows whether sparse and dense candidates complement each
other in small paragraph pools.

## What This Group Measures

[Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409)
introduces IndicXTREME and includes IndicQA as a manually curated
reading-comprehension benchmark for Indic languages. The retrieval version uses
each question as a query and the original context paragraph as the relevant
document. NanoIndicQA keeps this setup in compact per-language corpora.

The group measures same-language evidence paragraph retrieval. It is not
answer-string extraction and not cross-lingual retrieval. A model must retrieve
the supporting paragraph in the same Indic language as the query.

## Task Families

- **Same-language QA evidence retrieval:** all 11 tasks use question-to-context
  paragraph retrieval.
- **Eastern Indo-Aryan scripts:** Assamese, Bengali, and Odia test related but
  distinct scripts and orthographic conventions.
- **Western and northern Indo-Aryan scripts:** Gujarati, Hindi, Marathi, and
  Punjabi test different scripts, morphology, and named-entity patterns.
- **Dravidian scripts:** Kannada, Malayalam, Tamil, and Telugu test non-Indo-
  Aryan languages with longer paragraph evidence in several splits.

## Dataset Shape

NanoIndicQA contains 11 task pages, 2,200 queries, 2,759 split-local documents,
and 2,205 positive qrel rows. Every language has exactly 200 queries. The
document pools are small, roughly 241 to 261 context paragraphs per language.
The group is nearly single-positive: most queries have exactly one positive
paragraph, and only a few splits include one query with two positives.

Query and document length vary by language. Malayalam has the longest average
query length, while Telugu and Hindi have especially long context paragraphs.
Odia and Kannada have shorter average documents. Because the document pools are
small, top-rank ordering is often more informative than broad candidate recall.

## Retrieval Behavior

### BM25 Profile

BM25 is strong when the question repeats distinctive names, places, dates,
titles, or entity phrases from the evidence paragraph. Telugu, Bengali,
Malayalam, Assamese, Gujarati, Odia, and Punjabi all show useful sparse signal
in the current metadata. This reflects the same-language design: there is no
translation step, and exact terms can point directly to the paragraph.

BM25 is weaker for Tamil, Hindi, Kannada, and Marathi in the current metadata.
These failures often arise when the question wording differs from the paragraph
or when a short question does not provide enough exact anchors. Sparse retrieval
can also be affected by tokenizer quality for each script.

### Dense Profile

Dense retrieval is the best profile for most NanoIndicQA languages. It improves
paragraph matching when the question and evidence express the same fact with
different wording. This is especially visible for Tamil, Kannada, Hindi,
Marathi, Bengali, Gujarati, Odia, and Malayalam.

Dense retrieval should still be evaluated per language. A model may have strong
general Indic representation for one script but weaker coverage for another.
Dense gains are most meaningful when they improve semantic matching without
losing named entities and local script forms.

### Reranking Hybrid Profile

`reranking_hybrid` is rarely the best nDCG@10 profile in this group, but it is
often close to dense. Punjabi is the main hybrid-led split in the current
metadata. The hybrid view is useful when exact entity anchors and semantic
paragraph matching recover different candidates, but the small document pools
mean dense retrieval often has enough coverage by itself.

For reranking, this group is a clean same-language passage benchmark: the key
question is whether first-stage retrieval places the evidence paragraph near
the top, not whether it searches a huge web-scale corpus.

## Language Summary

| Language | Task | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Assamese | [as](as.md) | 200 | 250 | 200 | 0.6111 | 0.7416 | 0.7283 | Dense |
| Bengali | [bn](bn.md) | 200 | 250 | 201 | 0.6971 | 0.7773 | 0.7460 | Dense |
| Gujarati | [gu](gu.md) | 200 | 248 | 201 | 0.6060 | 0.7487 | 0.7207 | Dense |
| Hindi | [hi](hi.md) | 200 | 261 | 201 | 0.4545 | 0.6511 | 0.5738 | Dense |
| Kannada | [kn](kn.md) | 200 | 257 | 200 | 0.4730 | 0.7037 | 0.6111 | Dense |
| Malayalam | [ml](ml.md) | 200 | 247 | 200 | 0.6528 | 0.8214 | 0.7807 | Dense |
| Marathi | [mr](mr.md) | 200 | 250 | 200 | 0.4612 | 0.6720 | 0.5916 | Dense |
| Odia | [or](or.md) | 200 | 252 | 201 | 0.6041 | 0.7605 | 0.7033 | Dense |
| Punjabi | [pa](pa.md) | 200 | 241 | 200 | 0.5983 | 0.6445 | 0.6885 | Reranking hybrid |
| Tamil | [ta](ta.md) | 200 | 253 | 201 | 0.2932 | 0.6415 | 0.4551 | Dense |
| Telugu | [te](te.md) | 200 | 250 | 200 | 0.7674 | 0.7186 | 0.7582 | BM25 |

## Interpretation Notes for Model Researchers

NanoIndicQA is a controlled way to compare Indic-language passage retrieval
because all tasks share the same basic structure. Language-level differences
should therefore be interpreted through script coverage, tokenizer behavior,
paragraph length, and training data availability rather than task-family
differences.

The dense-versus-BM25 profile is especially important. Dense-led splits show
where semantic passage matching helps beyond repeated terms. BM25-led or
BM25-competitive splits show where exact names and local orthography remain
central. Tamil is a useful stress case because dense retrieval greatly improves
over BM25 in the current metadata.

## Training and Leakage Notes

Useful training data includes non-overlapping IndicQA-style question-context
pairs, same-language Wikipedia passage retrieval, extractive QA in each
language, and hard negatives from related biographies, places, events, or
cultural topics. Training should keep the target as the full evidence paragraph,
not only the answer span.

Exclude NanoIndicQA evaluation questions, positive paragraphs, qrels, and
direct translations or paraphrases of them. Upstream IndicQA and MTEB retrieval
splits should be audited for overlap before training.

## Public Sources

- [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409), 2022.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Leaving No Indic Language Behind | 2022 | paper | https://arxiv.org/abs/2212.05409 |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | https://arxiv.org/abs/2210.07316 |
