# MNanoBEIR / NanoBEIR-it / NanoQuoraRetrieval

## Overview

`NanoBEIR-it__NanoQuoraRetrieval` is the Italian NanoBEIR version of Quora
duplicate-question retrieval. The task uses Italian translated questions as
queries and asks a retriever to find Italian translated questions that express
the same or nearly the same information need. The Nano split contains 50
queries, 5,046 documents, and 70 positive qrels. Most queries have one positive,
but 10 queries have multiple positives, and the maximum is 6 positives for one
query. Because both queries and documents are short questions, this benchmark is
a direct test of paraphrase retrieval, duplicate intent matching, and semantic
similarity rather than document understanding over long passages.

## Details

### What the Original Data Measures

The Quora Question Pairs dataset was released as a duplicate-question detection
benchmark. BEIR adapts it into a retrieval task: given one question, rank a pool
of candidate questions so that duplicates or semantic equivalents appear near
the top. The Italian NanoBEIR task preserves this duplicate-question retrieval
setting after translation. A relevant result can be nearly identical to the
query, a lightly reworded version, or a question that asks the same thing with
different syntax. This makes the task especially informative for sentence-level
embedding models and rerankers.

### Observed Data Profile

The task contains 50 queries and 5,046 candidate questions. There are 70
positive qrels, with 1.40 positives per query on average. The positives-per-
query distribution is 1 minimum, 1.00 median, and 6 maximum, and 20.0% of
queries have multiple positives. Query length averages 52.82 characters, while
document length averages 64.45 characters. Since both sides are short, a model
has little surrounding context to use. Small changes in wording can preserve or
change intent, so the benchmark rewards precise semantic equivalence rather
than broad topical matching.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.7130, hit@10 = 0.8800, and
Recall@100 = 0.9429. This is a strong lexical baseline because duplicate
questions often reuse distinctive words, entity names, or phrasing. Exact term
overlap can identify many near-duplicates quickly. However, BM25 is still well
below dense retrieval on all main metrics, which shows the limit of word
frequency when duplicates are expressed through paraphrase, reordered
constructions, or different function words.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.8699, hit@10 =
0.9800, and Recall@100 = 0.9857. Dense retrieval is the strongest top-rank
profile for this task. The result matches the task structure: duplicate-question
retrieval is close to a sentence embedding similarity problem, and relevant
pairs often share intent even when wording changes. The high hit@10 shows that
semantic similarity usually places at least one duplicate near the top, while
the high nDCG@10 indicates that dense ranking is also good at ordering multiple
valid duplicates.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.8038, hit@10 = 0.9400, and Recall@100 = 1.0000, with no rank-101
safeguard rows. Hybrid retrieval has perfect top-100 relevant coverage, which
means it is an excellent candidate pool for downstream reranking. Its top-10
ranking, however, is below dense retrieval. This suggests that lexical signals
add coverage and protect exact-overlap duplicates, but they can also promote
questions that share words while asking something different. For this task,
hybrid search is strongest as a recall-oriented first stage.

### Metric Interpretation for Model Researchers

This task is a clean example of dense retrieval winning on top-rank semantic
quality while hybrid retrieval wins on candidate coverage. BM25 is already
strong because duplicate questions often overlap lexically, but dense retrieval
handles paraphrase and intent equivalence better. The hybrid profile shows that
combining lexical and dense retrieval can capture every positive within the
candidate set, but a reranker is needed to recover dense-like precision at the
top. Researchers should inspect whether improvements come from paraphrase
understanding, exact duplicate handling, or avoiding topical false positives.

### Query and Relevance Type Tendencies

Examples include questions about laughing at one's own jokes, clever lies,
Quora's political answer recommendations, physical strength, and quantum
satellites. Some positives are almost identical to the query, while others add
or remove detail but preserve the core information need. This makes the task
sensitive to distinctions between duplicate intent and merely related topic. A
question that shares "Donald Trump" or "satellite" terms can be a hard negative
if it asks a different thing.

### Representative Failure Modes

BM25 can over-rank questions that share many terms but differ in intent. Dense
retrieval can overmerge related questions, especially when broad topics dominate
the sentence representation. Hybrid retrieval can improve coverage but may
inherit both error types: lexical distractors from BM25 and semantic near-misses
from dense retrieval. Multiple-positive queries can also expose ranking errors
where one obvious duplicate is found but less literal paraphrases are ranked too
low.

### Training Data That May Help

Useful training data includes non-overlapping duplicate-question pairs,
paraphrase retrieval, Italian question matching, multilingual semantic
similarity data, and hard negatives that share topic words while asking a
different question. Training should exclude Quora Question Pairs, BEIR,
NanoBEIR, and overlapping translated pairs from this benchmark.

### Model Improvement Notes

Strong models for this task should represent question intent at sentence level
while preserving enough lexical detail to avoid false duplicates. Good hard
negatives are critical: they should be topically close and lexically similar but
not interchangeable as questions. A hybrid pipeline can use lexical retrieval to
guarantee coverage, but final ranking should emphasize semantic equivalence.

## Example Data

| Query | Positive document |
| --- | --- |
| Si può ridere delle proprie battute? | È strano ridere delle proprie battute? |
| Qual è la bugia più ingegnosa che hai mai raccontato? | Qual è la bugia più elaborata che tu abbia mai raccontato? |
| Perché Quora suggerisce spesso risposte nel mio feed che criticano Donald Trump? | Perché su Quora sembrano esserci solo risposte soggettive e di parte riguardo alle domande su Donald Trump? |
| Come posso diventare più forte fisicamente? | Come posso diventare più forte fisicamente? |
| Come funziona un satellite quantistico? | Come funziona un satellite quantistico e quali potrebbero essere i suoi principali utilizzi? |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset page | https://kaggle.com/competitions/quora-question-pairs |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
