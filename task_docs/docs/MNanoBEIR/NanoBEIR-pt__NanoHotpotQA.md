# MNanoBEIR / NanoBEIR-pt / NanoHotpotQA

## Overview

NanoBEIR-pt NanoHotpotQA is a Portuguese multi-hop question answering
retrieval task derived from HotpotQA. Queries are translated questions, and
documents are translated Wikipedia passages that provide supporting evidence.
Every query in this Nano subset has exactly two positive passages, so the task
is not finished when a model finds one obvious entity page. A strong retriever
must recover both pieces of evidence needed for a multi-hop answer. This makes
the task a compact benchmark for bridge-entity retrieval, comparison, and
multi-positive evidence coverage in Portuguese.

## Details

### What the Original Data Measures

HotpotQA was designed for explainable multi-hop question answering with
supporting facts. In BEIR, the retrieval task measures whether systems can find
the passages required to answer a question. The MNanoBEIR Portuguese version
keeps this evidence-retrieval objective after translation. It measures whether
models can follow question constraints across entities and retrieve multiple
supporting passages, including the bridge passage and the answer-bearing
passage.

### Observed Data Profile

This Nano subset contains 50 queries, 5,090 documents, and 100 positive qrels.
Every query has exactly two positives, so the average, median, minimum, and
maximum positives per query are all 2.00. All queries are multi-positive.
Queries average 91.12 characters, and documents are short Wikipedia passages
averaging 377.51 characters. This fixed two-positive structure makes recall
and evidence-set retrieval especially important: a model may look successful
with one hit while still missing the second support.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.7604,
hit@10 0.9600, and recall@100 0.9300. This strong lexical baseline reflects
the entity-heavy nature of HotpotQA questions. Names, titles, dates, and places
often appear in at least one support passage, letting BM25 retrieve an obvious
hop. The limitation is complete multi-hop coverage: lexical overlap can favor
the most explicit entity while under-ranking the second passage needed to
answer the question.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.7948, hit@10 0.9800, and recall@100 0.9600, improving over
BM25 across the reported metrics. Dense retrieval helps connect question
semantics to supporting passages even when the bridge relation is not a simple
word match. It can better represent paraphrased titles, roles, and relations
across the two-hop chain. The remaining errors likely come from partial-match
distractors, where a passage mentions one entity from the question but does
not provide the needed bridge or final answer evidence.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.8145, hit@10 1.0000, and
recall@100 0.9600, making it the strongest top-rank profile. The hybrid result
shows that Portuguese HotpotQA benefits from combining lexical entity anchors
with dense semantic matching. BM25 helps preserve exact names and titles,
while dense retrieval captures the relationship implied by the question. The
combined pool gives perfect first-page query coverage and the best nDCG@10.

### Metric Interpretation for Model Researchers

Because every query has two positives, hit@10 only confirms that at least one
support passage was found. Recall@100 is more important for whether a reranker
or QA system can access both pieces of evidence. nDCG@10 shows whether support
passages appear early enough to be useful. The observed scores show that dense
and hybrid retrieval improve on BM25, with reranking hybrid giving the best
early ordering. Researchers should evaluate evidence-set recovery rather than
single-passage success.

### Query and Relevance Type Tendencies

Queries are natural-language questions that often require following a bridge
entity, identifying a work or person, then retrieving another fact. Examples
include a sitcom actor connection, a sword made by the founder of a school, a
film written and directed by a specific person, a college football game date,
and a music collection tied to a band's alternate performance name. Relevant
documents are short Wikipedia passages that each contain part of the evidence
chain.

### Representative Failure Modes

BM25 may retrieve the passage with the clearest entity overlap but miss the
second support. Dense models may retrieve semantically related passages around
the same entity cluster while overlooking a specific bridge constraint. Hybrid
retrieval reduces these failures but still needs reranking that values
complementary evidence rather than repeated variants of one hop. Translation
can also affect titles, roles, and relation wording in Portuguese.

### Training Data That May Help

Helpful training data includes non-overlapping multi-hop QA retrieval,
Portuguese Wikipedia question generation, bridge-entity retrieval, comparison
questions, and multi-positive passage ranking. Hard negatives should mention
one entity from the question but omit the bridge fact or final answer. Training
should exclude HotpotQA, BEIR, NanoBEIR, and translated evaluation questions
or supporting passages.

### Model Improvement Notes

NanoHotpotQA-pt is a strong diagnostic for multi-hop retrieval systems.
Reranking hybrid is the best profile because it combines exact entity matching
with semantic relation matching. Improvements should focus on preserving
question constraints, retrieving complementary support passages, and reranking
for evidence-set completeness. For downstream QA, the most important behavior
is not just first-hit success but whether both supporting passages are present
and highly ranked.

## Example Data

| Query | Positive document |
| --- | --- |
| Em qual sitcom de televisão Penny Rae Bridges participou com qual outro ator? | Penny Rae Bridges é uma atriz americana. Seu trabalho na televisão inclui papéis em "For Your Love", "Family Law"... |
| Quem entregou a Kaganoi Shigemochi uma espada feita pelo fundador da escola Muramasa? | Kaganoi Shigemochi foi um samurai japonês do período Azuchi-Momoyama, que serviu ao clã Oda... |
| Qual é o filme escrito e dirigido por Joby Harold com música de Samuel Sim? | Samuel Sim é um compositor de cinema e televisão. Ganhou reconhecimento com a trilha sonora premiada da série "Dunkirk"... |
| Qual é a data deste jogo de futebol universitário no Sun Life Stadium em Miami Gardens, Flórida, onde a Clemson derrotou os Oklahoma Sooners por 37-17? | A equipe de futebol americano dos Clemson Tigers de 2015 representou a Universidade de Clemson na temporada de 2015... |
| Comida do Diabo é uma coletânea de singles de uma banda de rock and roll americana que também é conhecida por tocar shows de country sob qual nome? | Devil's Food é uma coletânea de singles da banda americana de rock and roll Supersuckers, lançada em abril de 2005... |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
