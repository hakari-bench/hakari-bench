# NanoMTEB-v2 / hotpot_qa

## Overview

`NanoMTEB-v2 / hotpot_qa` is a multi-hop question-to-Wikipedia retrieval task derived from HotpotQA. Queries are natural-language questions, and each query has two relevant supporting passages. The original HotpotQA benchmark was built for explainable multi-hop question answering over Wikipedia, with annotated supporting facts that require combining evidence across pages. This Nano retrieval split evaluates whether a model can retrieve those support passages from a 10,000-document candidate pool. It is useful for studying bridge-entity retrieval, multi-positive ranking, and whether first-stage systems can find both parts of a two-hop evidence chain.

## Details

### What the Original Data Measures

HotpotQA measures question answering that often requires linking two Wikipedia entities or facts. In the retrieval version, the answer itself is not the target; the model must retrieve the supporting passages needed to answer the question. This makes the task different from ordinary single-passage QA retrieval.

Every query in this Nano split has exactly two positives. A strong retrieval system should not only find one obvious entity page, but also recover the second supporting passage that completes the reasoning chain.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 400 positive qrel rows. Each query has exactly 2 positives, so all 200 queries are multi-positive. Queries average 95.83 characters, while documents average 421.20 characters.

The examples include questions about films, lighthouse lamps, shared ancestry, screenwriters, and actors. Many questions explicitly mention one entity and ask for a relation that requires another page or linked fact. Documents are short Wikipedia-style passages with titles.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8950, hit@10 of 1.0000, and recall@100 of 0.9725. This is a very strong sparse profile. Many queries contain entity names, work titles, or distinctive phrases that appear in at least one supporting passage.

BM25 is especially good at finding the first hop when a bridge entity is stated in the query. Its remaining weakness is balanced multi-hop coverage: a system can get a hit by retrieving one support passage while still missing or under-ranking the second.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8904, hit@10 of 0.9850, and recall@100 of 0.9700. Dense retrieval is also very strong, but slightly below BM25 on this Nano sample. The result suggests that explicit entity overlap is highly informative here.

Dense retrieval remains useful because some second-hop passages may be semantically connected rather than lexically obvious. However, if the query names a bridge entity directly, sparse matching can be hard to beat.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard positives. It reaches nDCG@10 of 0.9156, hit@10 of 1.0000, and recall@100 of 0.9975. This is the strongest profile across the candidate types. The hybrid pool captures the exact-entity strengths of BM25 and the semantic bridge coverage of dense retrieval.

For reranking, this task is a good example of why hybrid search matters even when individual first-stage systems are strong. The combined pool nearly saturates supporting-passage coverage, giving a reranker the opportunity to place both positives early.

### Metric Interpretation for Model Researchers

Because every query has two positives, hit@10 alone is not enough. A system can hit with one supporting passage while still failing to retrieve the full evidence set. nDCG@10 and recall@100 should be read together: nDCG reflects whether positives are ranked high, while recall shows whether both support passages are available for downstream multi-hop reasoning.

The near-ceiling scores mean this split is not primarily a hard candidate-generation benchmark. Its value is in checking multi-hop support coverage and rank ordering under hard negatives.

### Query and Relevance Type Tendencies

Queries are English multi-hop questions, often naming one entity and asking about a related entity, location, date, role, or work. Relevant documents are short Wikipedia passages. The two positives usually correspond to the support pages required to answer the question.

The relevance relation is supporting evidence for multi-hop QA. Topical similarity is not enough unless the passage contributes to the answer chain.

### Representative Failure Modes

Common failures include retrieving only one hop, over-ranking an entity page that is mentioned in the query but not sufficient for the answer, missing the bridge page, and confusing similarly named works or people. Dense systems may retrieve semantically related pages that do not complete the reasoning chain; sparse systems may over-focus on the explicitly named entity.

### Training Data That May Help

Useful training data includes HotpotQA supporting-fact retrieval pairs, multi-hop Wikipedia QA data, entity-linking retrieval data, and hard negatives that mention one entity but lack the needed relation. Multi-positive training is required because both supporting passages matter.

### Model Improvement Notes

Models should optimize for evidence-set retrieval, not just first-hit retrieval. Candidate generation should preserve both lexical entity matches and semantic bridge candidates. Rerankers should learn to identify complementary support passages rather than ranking several passages about the same first-hop entity.

## Example Data

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600), 2018.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [mteb/HotpotQA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | source task paper | https://arxiv.org/abs/1809.09600 |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/HotpotQA_test_top_250_only_w_correct-v2 |  | dataset card | https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2 |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| The Soul of Buddha is a 1918 American silent romance film shot in a borough that is the western terminus of what? | A passage about the film `The Soul of Buddha`, including its production and filming context. |
| The lamp used in many lighthouses is similiar to this type of lamp patented in 1780 by Aimé Argand? | A passage about the Lewis lamp, a lighthouse light fixture, and its relation to earlier lamp designs. |
| What is the shared country of ancestry between Art Laboe and Scout Tufankjian? | A passage about Art Laboe describing him as an Armenian American figure. |
| Sebastian Gutierrez is known for writing the screenplay for the 2003 film directed by whom? | A passage about Sebastian Gutierrez and the films for which he wrote screenplays. |
| When did the character on Grey's Anatomy, played by the same actor who portrayed Rev James Lawson in "Lee Daniel's The Butler", debut? | A passage about Jesse Williams and his role as Dr. Jackson Avery on `Grey's Anatomy`. |
