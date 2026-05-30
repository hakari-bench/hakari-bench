# NanoFaMTEB-v2 / hotpot_qa_fa

## Overview

`hotpot_qa_fa` is a Persian multi-hop QA evidence retrieval task in NanoFaMTEB-v2. The query is a Persian question, and the positive documents are evidence passages. Each query has exactly two positive passages, reflecting the multi-hop nature of HotpotQA-style retrieval.

This task evaluates whether a retriever can find multiple entity-linked evidence passages for a question. Entity names make lexical retrieval strong, but the task still requires covering both supporting passages rather than only one obvious entity page.

## Details

### What the Original Data Measures

FaMTEB includes Persian retrieval data adapted from BEIR-style and MTEB-style benchmarks. `hotpot_qa_fa` uses `MCINext/HotpotQA_FA_test_top_250_only_w_correct-v2`, a Persian HotpotQA-style hard-negative dataset.

The original HotpotQA retrieval setting measures multi-hop evidence retrieval: answering the question requires connecting facts across passages. In this Persian split, the model must retrieve the relevant Persian evidence passages from a large candidate set.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 400 positive qrels. Every query has exactly two positives. Queries average 87.89 characters, and documents average 394.90 characters.

Observed examples ask about films, people, countries, lighthouses, actors, and television or movie connections. Documents are Persian encyclopedia-style passages about the entities involved in the reasoning chain.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.7735, hit@10 of 0.9650, and recall@100 of 0.9200 with a top-500 candidate pool. Entity names and titles provide powerful lexical anchors, so BM25 often finds at least one positive passage.

The limitation is multi-hop completeness. A question may mention one entity directly and require another passage for the bridge. BM25 can prioritize the obvious entity while missing or lowering the second supporting passage.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.8060, hit@10 of 0.9600, and recall@100 of 0.9275. Dense retrieval improves nDCG and recall slightly over BM25 by connecting question semantics to evidence passages beyond exact entity matching.

Dense retrieval helps when the bridge relation is expressed indirectly or when entity wording differs. It remains close to BM25 because the dataset has strong named-entity cues.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset is strongest, with nDCG@10 of 0.8366, hit@10 of 0.9950, and recall@100 of 0.9550. It uses exactly 100 candidates per query with no safeguard-positive rows. Hybrid retrieval combines lexical entity recall with dense bridge-relation matching.

This is the best profile for multi-hop evidence coverage. The absence of safeguard rows indicates that positives naturally appear in the top-100 hybrid candidate sets.

### Metric Interpretation for Model Researchers

`hotpot_qa_fa` is an entity-heavy multi-hop retrieval task. BM25, dense, and hybrid are all strong, but hybrid is best overall. The important distinction is not simply finding any relevant passage; it is recovering both positive passages and ranking them high enough for downstream QA.

Recall@100 is important because each query has two positives. nDCG@10 reflects whether both evidence passages are placed near the top.

### Query and Relevance Type Tendencies

Queries are Persian questions that often name at least one entity and ask for a linked property. Documents are short encyclopedia passages. Positives usually correspond to the two pieces of evidence needed for the multi-hop question.

### Representative Failure Modes

BM25 may retrieve only the directly named entity page. Dense retrieval may retrieve a semantically related passage but miss the exact bridge entity. Hybrid retrieval reduces these failures but may still rank one of the two positives lower.

### Training Data That May Help

Useful training data includes Persian Wikipedia QA, translated HotpotQA evidence retrieval, entity-linking retrieval, and multi-hop evidence pairs. Hard negatives should contain only one entity or answer a nearby relation.

Training should exclude this split's query and document rows from training.

### Model Improvement Notes

Improving this task requires multi-hop candidate coverage. Models should preserve entity names while also representing bridge relations and answer-supporting facts.

For reranking, passage-set coverage may be more important than individual passage similarity: the top results should jointly cover the reasoning chain.

## Example Data

### Public Sources

This task is documented through the FaMTEB paper and the `MCINext/HotpotQA_FA_test_top_250_only_w_correct-v2` dataset card. MTEB provides the broader retrieval evaluation framework.

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General benchmark framework. |
| [MCINext/HotpotQA_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/HotpotQA_FA_test_top_250_only_w_correct-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian question linking a silent film to the location where it was filmed. | Evidence passages about the film and the relevant geographic or studio location. |
| A question comparing lighthouse lamps to a lamp patented by a named inventor. | Evidence about the lighthouse lamp and the historical lamp type. |
| A question asking for the shared paternal country of two people. | Biographical evidence pages for the people involved. |
| A question about a screenwriter known for a film directed by another person. | Evidence about the writer and the film or director relation. |
| A question linking a Grey's Anatomy actor to a role in another film. | Evidence about the actor and the relevant television or film character. |
