# MNanoBEIR / NanoBEIR-no / NanoFiQA2018

## Overview

NanoBEIR-no NanoFiQA2018 is a Norwegian financial question-answer retrieval
task derived from FiQA 2018. Queries are translated personal-finance questions,
and documents are translated answer passages from finance-oriented forum data.
The task is useful because it combines short practical questions with long,
domain-specific answers. Unlike encyclopedic fact retrieval, relevance often
depends on understanding the decision being asked about, such as taxes,
investment returns, credit cards, freelancing, contracts, or trading volume.
This makes the task a compact test of finance-domain semantics in multilingual
retrieval.

## Details

### What the Original Data Measures

FiQA 2018 was built around financial opinion, question answering, and
domain-specific information needs. In BEIR, the retrieval version evaluates
whether systems can retrieve answer passages for finance questions. The
MNanoBEIR Norwegian version keeps that question-to-answer structure after
translation. It measures whether retrieval models can match a short Norwegian
finance question to the answer that addresses the same financial concept,
procedure, risk, or jurisdictional issue.

### Observed Data Profile

This Nano subset contains 50 queries, 4,598 documents, and 123 positive qrels.
It is moderately multi-positive: the average is 2.46 positives per query, with
a minimum of 1, median of 2.00, and maximum of 15. There are 28 multi-positive
queries, covering 56.0% of the task. Queries average 64.68 characters and are
usually practical finance questions. Documents average 910.83 characters and
often contain explanatory forum answers, caveats, and examples. The task
therefore requires answer matching rather than simple topic retrieval.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.1955,
hit@10 0.4200, and recall@100 0.5528. This is a hard lexical setting. Finance
questions can use broad terms such as "tax," "volume," "returns," or "credit
card," but relevant answers may explain the issue with different wording or
with jurisdiction-specific details. BM25 can recover candidates when the same
technical phrase appears in both query and answer, but it often over-ranks
documents that share finance vocabulary while answering a different practical
question. The moderate recall also means a lexical-only first stage may exclude
many valid answer passages from later reranking.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.4205, hit@10 0.6800, and recall@100 0.7236, clearly
outperforming BM25. This result fits the task: embedding similarity is better
at connecting a short question with an explanatory answer when the answer does
not repeat the exact query terms. Dense retrieval also helps with conceptual
matching, such as linking a question about freelancing to tax-status
explanations or a question about volume to trading-volume definitions. The
remaining misses likely reflect finance-specific ambiguity, jurisdictional
differences, and answers that require more precise decision context than a
general embedding can represent.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.08 and 4 safeguard rows. It reaches nDCG@10 0.3330, hit@10 0.5800,
and recall@100 0.7154. The hybrid profile substantially improves over BM25 and
nearly matches dense recall@100, but it trails dense on early ranking and
hit@10. This indicates that the hybrid pool collects many useful answer
candidates by combining lexical and semantic evidence, while dense ordering is
better at placing the most relevant finance answer high. A strong reranker
should be able to exploit the hybrid pool by checking whether the answer
actually resolves the financial question.

### Metric Interpretation for Model Researchers

Because more than half of the queries have multiple positives, recall@100
reflects answer coverage, while hit@10 reflects whether at least one useful
answer reaches the first page. nDCG@10 is the key early-ranking signal. The
large gap between BM25 and dense shows that exact word overlap is a weak proxy
for relevance in finance QA. The smaller gap between dense and reranking hybrid
on recall suggests that hybrid search is still useful for candidate generation,
especially when rare finance terms or numbers matter. For model comparison,
this task highlights whether a retriever understands the intent of a finance
question rather than merely matching domain vocabulary.

### Query and Relevance Type Tendencies

Queries are short, practical questions that ask what something means, how to
handle a tax situation, how a financial product behaves, or how to account for
a business expense. Relevant documents are forum-style answers that may include
definitions, examples, legal caveats, or personal-finance reasoning. The
answers often address the same decision using longer explanations rather than
restating the question. This favors models that can represent intent,
financial-domain concepts, and answer utility.

### Representative Failure Modes

BM25 may retrieve passages that share terms like "tax," "return," or "credit"
but discuss another financial action. Dense systems may retrieve generally
related financial advice that does not answer the exact question or applies to
a different jurisdiction. Hybrid systems may broaden the candidate pool while
still needing a reranker to separate true answers from same-topic advice.
Translation can also reduce surface overlap when domain terminology is
rendered in different Norwegian phrases across question and answer.

### Training Data That May Help

Helpful training data includes non-overlapping financial QA, personal-finance
forum retrieval, tax and investment question-answer pairs, multilingual finance
retrieval, and domain-specific hard-negative training. Hard negatives should
share finance terms but answer a different decision, country, product, or
accounting condition. Training should exclude FiQA, BEIR, NanoBEIR, and
translated answer passages likely to overlap with this benchmark.

### Model Improvement Notes

NanoFiQA2018-no is a strong diagnostic for answer-aware retrieval in a domain
where terminology alone is not enough. Dense retrieval is the strongest single
profile, while reranking hybrid offers nearly the same candidate coverage and a
broader mix of lexical and semantic signals. Improvements should focus on
finance-domain pretraining, jurisdiction and condition sensitivity, and
rerankers that compare question intent with answer content. A practical system
would likely use hybrid candidates, then rerank with a model trained on
financial QA relevance rather than generic passage similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Hvilken type avkastning gir Vanguard? [37 chars] | Fra Vanguards side - Dette virket som den enkleste siden S&P-data er lett å finne. Jeg bruker MoneyChimp for å bekrefte at Vanguards side tilbyr CAGR, ikke aritmetisk gjennomsnitt. Merk: Vanguard oppgir 'For amerikanske aksjemarkedets avkastning, bruker vi Standard & Poor's 90 fra 1926 til 3. mars 1957,' mens MoneyChimp bruker data fra Nobelprisvinneren Robert Shillers nettsted. [381 chars] |
| Hva er skattekonsekvensene av å frilanse? [41 chars] | Hvis du har inntekt i USA, må du betale amerikansk inntektsskatt på det, med mindre det finnes en avtale mellom ditt land og USA som sier noe annet. [148 chars] |
| Hva betyr høy eller lav volum? [30 chars] | Den daglige volumet sammenlignes vanligvis med gjennomsnittlig daglig volum over de siste 50 dagene for en aksje. Høyt volum regnes vanligvis som 2 eller flere ganger gjennomsnittlig daglig volum over de siste 50 dagene for den aktuelle aksjen. Noen håndlere kan imidlertid sette kriteriet til 3x eller 4x gjennomsnittlig daglig volum (ADV) for å bekrefte et bestemt mønster eller hendelse. Volumet sammenlignes med ADV for den aktuelle aksjen, da sammenligning med volumet til andre aksjer ville være som å sammenligne epler med pærer. Forskjellige selskaper vil ha forskjellige antall aksjer i omløp, forskjellige nivåer av likviditet og forskjellige nivåer av volatilitet, noe som alle kan påvirke volumet som handles hver dag. [730 chars] |

### Public Sources

- [FiQA 2018](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA 2018 | 2018 | task paper | [https://doi.org/10.1145/3184558.3192301](https://doi.org/10.1145/3184558.3192301) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
