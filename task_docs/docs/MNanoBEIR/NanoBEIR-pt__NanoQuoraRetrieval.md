# MNanoBEIR / NanoBEIR-pt / NanoQuoraRetrieval

## Overview

NanoBEIR-pt NanoQuoraRetrieval is a Portuguese duplicate-question retrieval
task derived from the Quora Question Pairs data as adapted in BEIR. Queries and
documents are both translated questions, and the target documents are duplicate
or near-duplicate questions that express the same intent. The task isolates
short-text semantic equivalence: unlike QA or evidence retrieval, the relevant
item is another question, not an answer passage. It is useful for evaluating
whether models distinguish true paraphrases from questions that merely share
topic words.

## Details

### What the Original Data Measures

The Quora Question Pairs dataset was created for duplicate-question detection.
BEIR adapts it as a retrieval task where a query question should retrieve
semantically equivalent questions from a corpus. The MNanoBEIR Portuguese
version keeps that objective after translation. It measures paraphrase
matching, intent preservation, and short-question semantic similarity in a
multilingual setting.

### Observed Data Profile

This Nano subset contains 50 queries, 5,046 documents, and 70 positive qrels.
Most queries have one positive, though 10 queries have multiple duplicates.
The average is 1.40 positives per query, with a minimum of 1, median of 1.00,
and maximum of 6. Queries average 54.20 characters, and documents average
62.53 characters. Because both sides are short, models have little extra
context and must rely on wording, intent, and semantic equivalence.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.7247,
hit@10 0.9000, and recall@100 0.9571. This is a strong lexical profile:
duplicate questions often share central words, named entities, or syntactic
patterns. BM25 is therefore highly effective at finding near-duplicates with
obvious overlap. Its limitation is paraphrase robustness. It can over-rank
same-topic questions that ask for different information and under-rank
equivalent questions that use different wording.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.8172, hit@10 0.9000, and recall@100 0.9286. Dense retrieval
has the best early ranking, indicating that embedding similarity captures
duplicate intent better than lexical overlap alone. Its recall@100 is slightly
lower than BM25, which suggests that exact word overlap still recovers some
duplicates that dense retrieval does not keep as broadly. For top-ranked
question equivalence, however, dense is the strongest single profile.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.02 and 1 safeguard row. It reaches nDCG@10 0.7634, hit@10 0.8800,
and recall@100 0.9857. The hybrid profile has the best candidate coverage but
does not match dense early ranking. This makes it useful for reranking: the
pool contains nearly all positives, but the final model must separate true
duplicates from strong same-topic distractors.

### Metric Interpretation for Model Researchers

Because some queries have multiple duplicate questions, recall@100 measures
coverage of the duplicate set, while nDCG@10 measures whether the best
duplicates appear early. Hit@10 is already high for all methods and is less
diagnostic. The dense profile is strongest for ranking, BM25 is strong for
lexical duplicate coverage, and reranking hybrid gives the broadest top-100
pool. Researchers can use this task to test whether a reranker improves a
high-recall hybrid pool without losing dense-style paraphrase sensitivity.

### Query and Relevance Type Tendencies

Queries are short Portuguese questions about personal behavior, lies, Quora
feed behavior, physical strength, and technology. Relevant documents can be
identical, lightly rephrased, or expanded versions of the same question. The
key relevance relation is intent equivalence. A question with the same topic
but a different requested fact is a hard negative, even if it shares many words
with the query.

### Representative Failure Modes

BM25 may retrieve questions that share entities or phrases but are not true
duplicates. Dense models may retrieve broadly similar questions that feel
semantically related while asking for a different answer. Hybrid retrieval may
include nearly all positives but also many strong distractors. Translation can
normalize phrasing and make some non-duplicates appear more similar than they
would in the source text.

### Training Data That May Help

Helpful training data includes non-overlapping duplicate-question retrieval,
Portuguese paraphrase pairs, semantic textual similarity data, multilingual
question matching, and hard-negative question pairs. Hard negatives should
share entities or wording but ask a different question. Training should exclude
Quora Question Pairs, BEIR, NanoBEIR, and translated duplicate records from
this split.

### Model Improvement Notes

NanoQuoraRetrieval-pt is a focused benchmark for short-question equivalence.
Dense retrieval is the best early ranker, while reranking hybrid provides the
best candidate coverage. Improvements should focus on intent preservation,
paraphrase robustness, and discrimination between duplicates and same-topic
non-duplicates. A strong production duplicate-search system would use hybrid
retrieval for recall and a duplicate-specific reranker for final ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| É normal rir das próprias piadas? [33 chars] | É estranho rir das minhas próprias piadas? [42 chars] |
| Qual é a maior mentira que você já contou? [42 chars] | Qual é a maior mentira que você já contou? [42 chars] |
| Por que o Quora frequentemente sugere respostas no meu feed que criticam Donald Trump? [86 chars] | Por que o Quora parece ter apenas respostas tendenciosas e subjetivas sobre perguntas relacionadas a Donald Trump? [114 chars] |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset competition | [https://kaggle.com/competitions/quora-question-pairs](https://kaggle.com/competitions/quora-question-pairs) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
