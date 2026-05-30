# MNanoBEIR / NanoBEIR-no / NanoHotpotQA

## Overview

NanoBEIR-no NanoHotpotQA is a Norwegian multi-hop evidence retrieval task
derived from HotpotQA. Queries are translated questions, and documents are
translated Wikipedia paragraphs that contain supporting evidence. Each query in
this Nano subset has exactly two positive passages, so the task is not only to
find one plausible page but to recover both pieces of evidence needed for a
multi-hop answer. This makes the benchmark useful for studying whether
retrieval systems can handle bridge entities, comparisons, and partial-match
distractors in a multilingual question-answering setting.

## Details

### What the Original Data Measures

HotpotQA was designed for explainable multi-hop question answering with
supporting facts. In retrieval benchmarks such as BEIR, the task is evaluated
as evidence retrieval: systems receive a question and must retrieve paragraphs
that support the answer. The MNanoBEIR Norwegian version preserves the
question-to-supporting-paragraph structure while using translated Norwegian
queries and documents. It measures whether models can identify the linked
evidence chain behind a question, including entities that appear in only one
hop and documents that are relevant only in combination.

### Observed Data Profile

This Nano subset contains 50 queries, 5,090 documents, and 100 positive qrels.
Every query has exactly two positives, so the average, median, minimum, and
maximum positives per query are all 2.00. All queries are multi-positive.
Queries average 87.30 characters, while documents are relatively compact
Wikipedia paragraphs averaging 341.70 characters. The fixed two-positive setup
is important: a model that retrieves only the obvious paragraph may still miss
the second supporting paragraph needed for complete evidence coverage.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.7728,
hit@10 0.9600, and recall@100 0.9400. This is a strong lexical profile,
because HotpotQA questions often contain named entities, titles, dates, or
other anchors that appear in at least one supporting paragraph. However, the
task remains multi-hop: lexical matching can favor the most explicit entity
while under-ranking the bridge or comparison evidence. BM25 is therefore a
strong candidate generator for obvious hops, but it may not always balance both
supporting passages in the early ranks.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.7574, hit@10 0.9800, and recall@100 0.9400. Dense retrieval
slightly improves hit@10 over BM25 but has lower nDCG@10 with the same
recall@100. This suggests that semantic similarity is effective at finding at
least one relevant supporting passage, including paraphrased or translated
question-document matches, but the early ordering is not better than BM25 for
this subset. Dense models may cluster around the main entity or answer-bearing
paragraph and still miss the precise rank placement of the second support.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.8168, hit@10 1.0000, and
recall@100 0.9600, making it the strongest of the three candidate profiles for
this task. The result indicates that combining lexical and dense evidence is
especially useful for multi-hop retrieval. BM25 contributes entity and title
anchors, while dense retrieval contributes semantic links for bridge or
paraphrased evidence. The hybrid pool also improves coverage for the two
supporting passages, which is crucial for HotpotQA-style evaluation.

### Metric Interpretation for Model Researchers

Because every query has exactly two positives, hit@10 can be misleading if read
as complete success: it only shows that at least one supporting paragraph was
found. Recall@100 is more informative for multi-hop coverage, while nDCG@10
shows whether supporting evidence is placed early enough for downstream QA. The
reranking hybrid profile is strongest on all three practical signals, which
means this task rewards a blend of exact entity matching and semantic
connection. Researchers should inspect whether a model retrieves both support
documents, not only whether it finds the paragraph most directly tied to the
answer.

### Query and Relevance Type Tendencies

Queries are natural-language questions that often mention one entity and ask
about another connected fact. Some require a bridge relation, such as identifying
a person connected to a work, then finding another fact about that person. Others
require comparison, event, date, or title matching. Relevant documents are
Wikipedia paragraphs that each contain part of the evidence chain. This favors
retrievers that can represent named entities precisely while also following the
semantic relationship implied by the question.

### Representative Failure Modes

BM25 may retrieve the paragraph with the clearest entity overlap but miss the
second support paragraph. Dense models may retrieve semantically close
paragraphs about the same entity cluster while failing to preserve a specific
bridge constraint. Hybrid systems can reduce both errors, but the final
reranker still needs to prefer complementary evidence rather than many variants
of the same hop. Translation can add difficulty when entity names are preserved
but relations or titles are expressed differently in Norwegian.

### Training Data That May Help

Helpful training data includes non-overlapping multi-hop QA, Wikipedia
supporting-fact retrieval, bridge-entity question answering, comparison
questions, and multilingual question-to-passage retrieval. Hard negatives
should include one-hop partial matches, same-entity distractors, and passages
that answer only part of the question. Training should exclude HotpotQA, BEIR,
NanoBEIR, and overlapping translated supporting paragraphs.

### Model Improvement Notes

NanoHotpotQA-no is a compact but sharp test for retrieval systems that must
support multi-hop reasoning. The hybrid profile is strongest, indicating that
entity-level lexical cues and dense semantic cues are complementary. Model
improvements should target evidence-set retrieval, not just single-passage
similarity: query encoders should preserve bridge constraints, and rerankers
should learn to select complementary supporting paragraphs. For downstream QA,
the key question is whether both positives are available and highly ranked.

## Example Data

| Query | Positive document |
| --- | --- |
| Hvilken annen skuespiller medvirket Penny Rae Bridges i en TV-sitcom sammen med? | Penny Rae Bridges er en amerikansk skuespiller. Hun har spilt i "For Your Love", "Family Law", "Boy Meets World"... |
| Hvem ga Kaganoi Shigemochi et sverd laget av personen som grunnla Muramasa-skolen? | Kaganoi Shigemochi var en japansk samurai fra Azuchi-Momoyama-perioden som tjenestegjorde for Oda-klanen... |
| Hvilken film er skrevet og regissert av Joby Harold med musikk av Samuel Sim? | Samuel Sim er en komponist for film og fjernsyn. Han fikk først anerkjennelse for sin musikk til BBC-dramaserien "Dunkirk"... |
| Hvilken dato ble denne college football-kampen spilt på Sun Life Stadium i Miami Gardens, Florida, der Clemson slo nr. 4 Oklahoma Sooners, 37-17? | Clemson Tigers fotballaget representerte Clemson University i 2015-sesongen i NCAA Division I FBS... |
| Hva er Devil's Food? Det er en samling med singler av en amerikansk rock and roll-band som også har vært kjent for å spille country-konserter under hvilket navn? | Devil's Food er en samleplate med singler av det amerikanske rock & roll-bandet Supersuckers, utgitt i april 2005... |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
