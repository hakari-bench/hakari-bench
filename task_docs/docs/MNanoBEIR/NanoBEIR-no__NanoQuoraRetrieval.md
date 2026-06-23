# MNanoBEIR / NanoBEIR-no / NanoQuoraRetrieval

## Overview

NanoBEIR-no NanoQuoraRetrieval is a Norwegian duplicate-question retrieval task
derived from the Quora Question Pairs data as adapted in BEIR. Queries and
documents are both translated questions, and the goal is to retrieve questions
that express the same or nearly the same information need. The task is compact
but important for retrieval research because it isolates paraphrase matching:
unlike passage retrieval, the relevant document is not an answer, evidence
paragraph, or article summary, but another short question with equivalent
intent.

## Details

### What the Original Data Measures

The Quora Question Pairs dataset was designed to identify duplicate questions.
BEIR adapts it as a retrieval task in which each query should retrieve
semantically equivalent questions from a corpus. The MNanoBEIR Norwegian
version keeps that duplicate-question objective after translation. It measures
whether retrieval models can match meaning across short questions, including
cases where two questions share only part of their wording or express the same
intent with different phrasing.

### Observed Data Profile

This Nano subset contains 50 queries, 5,046 documents, and 70 positive qrels.
Most queries have one positive, but 10 queries have multiple positives. The
average positives per query is 1.40, with a minimum of 1, median of 1.00, and
maximum of 6. Queries average 50.62 characters, and documents average 57.87
characters. Because both sides are short questions, there is little surrounding
context. Models must infer semantic equivalence from concise phrasing,
question form, and topic constraints.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.6347,
hit@10 0.7800, and recall@100 0.8857. This is a strong lexical baseline.
Duplicate questions often share important words, entities, or constructions,
so term frequency is highly informative. However, BM25 still misses or
under-ranks paraphrases that express the same intent with different word
choices, and it can over-rank questions that share topic words but ask for
different information. The high recall means BM25 is a useful candidate
generator, but semantic ranking remains necessary for robust duplicate
retrieval.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.7829, hit@10 0.8800, and recall@100 0.9714, outperforming BM25
on all reported metrics. This is the expected behavior for a duplicate-question
task: embedding similarity captures paraphrase and intent better than lexical
overlap alone. Dense retrieval is especially valuable when one question uses a
more natural phrasing and the other uses a different synonym, word order, or
expanded formulation. The remaining errors likely involve same-topic
non-duplicates, vague questions, or cases where translation makes two
questions appear closer or farther than their original intent.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.6988, hit@10 0.8200, and
recall@100 1.0000. The hybrid profile achieves complete relevant coverage at
100 candidates, exceeding both BM25 and dense recall. Its early ranking,
however, remains below dense retrieval. This indicates that lexical and dense
signals are complementary for candidate generation: BM25 captures exact shared
terms, while dense retrieval captures paraphrases. A reranker has an ideal
opportunity here, because the candidate pool contains all positives but still
needs better ordering by true duplicate intent.

### Metric Interpretation for Model Researchers

Because some queries have multiple duplicate questions, recall@100 indicates
how well the retrieval stage covers the equivalent-question set. Hit@10 is a
coarse first-page measure, and nDCG@10 is the best signal for early ordering.
The dense profile is strongest for ranking, while the hybrid profile is best
for complete candidate coverage. This separation is useful: researchers can
use this task to test whether a reranker can improve on a high-recall hybrid
pool, and whether an encoder distinguishes duplicate intent from same-topic
question similarity.

### Query and Relevance Type Tendencies

Queries and documents are short natural-language questions. Relevant pairs may
be near-identical, lightly rephrased, or semantically equivalent despite
different wording. Examples include questions about laughing at one's own
jokes, clever lies, Quora feed behavior, physical strength, and quantum
satellites. The task favors models that preserve question intent, scope, and
requested information, rather than simply matching topic words.

### Representative Failure Modes

BM25 may retrieve questions that share several words but ask a different thing.
Dense models may retrieve semantically related questions that are not true
duplicates, especially when broad topics such as politics, health, or
technology dominate the embedding. Hybrid systems may include all relevant
questions but still mix them with strong distractors. Translation can also
compress or normalize phrasing, making some non-duplicates look more similar
than they should.

### Training Data That May Help

Helpful training data includes non-overlapping duplicate-question pairs,
paraphrase retrieval, semantic textual similarity, multilingual question
matching, and Norwegian short-question pairs. Hard negatives should share
entities or topic words but request different information. Training should
avoid Quora Question Pairs, BEIR, NanoBEIR, and overlapping translated
questions.

### Model Improvement Notes

NanoQuoraRetrieval-no is a direct test of short-text semantic equivalence.
Dense retrieval is the strongest single ranking profile, while reranking
hybrid provides full top-100 coverage and is therefore an excellent reranker
input. Improvements should focus on intent preservation, paraphrase robustness,
and hard-negative discrimination between duplicates and same-topic
non-duplicates. For production duplicate detection, the most useful system
would combine high-recall hybrid candidate generation with a reranker trained
specifically on question equivalence.

## Example Data

| Query | Positive document |
| --- | --- |
| Er det greit å le av egne vitser? [33 chars] | Er det rart å le av mine egne vitser? [37 chars] |
| Hva er den mest geniale løgn du noen gang har fortalt? [54 chars] | Hva er den mest gjennomtenkte løgnen du noen gang har fortalt? [62 chars] |
| Hvorfor fremmer Quora ofte svar i min feed som kritiserer Donald Trump? [71 chars] | Hvorfor virker det som om Quora bare har subjektive og partiske svar på spørsmål om Donald Trump? [97 chars] |
| Hvordan kan jeg bli sterkere fysisk? [36 chars] | Hvordan blir jeg fysisk sterk? [30 chars] |
| Hvordan fungerer en kvantum-satellitt? [38 chars] | Hvordan fungerer en Quantum-satellitt, og hva er noen av dens hovedbruk? [72 chars] |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset page | [https://kaggle.com/competitions/quora-question-pairs](https://kaggle.com/competitions/quora-question-pairs) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
