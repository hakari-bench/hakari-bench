# NanoBEIR-en / NanoNQ

## Overview

NanoNQ is the compact English NanoBEIR version of Natural Questions, an open-domain question answering retrieval task built from real Google search queries and Wikipedia evidence. Each query is a natural information-seeking question, and the corpus contains Wikipedia-style passages that can answer it. The retrieval goal is to find the answer-bearing evidence passage, not merely a page that shares entity terms. This makes the task useful for evaluating natural question understanding, relation-aware passage retrieval, and first-stage evidence selection for QA.

## Details

### What the Original Data Measures

Natural Questions was designed around real user queries rather than questions written after reading a paragraph. In the original QA task, annotators identify long and short answers in Wikipedia pages. In retrieval form, the benchmark asks whether a system can retrieve the passage that contains the answer evidence.

The BEIR version places NQ in the question answering group, and the NanoBEIR version keeps a compact English sample. A strong retriever must understand the requested relation, such as who, where, when, why, or what, while also preserving entity and title recall.

### Observed Data Profile

The task contains 50 queries, 5,035 documents, and 57 relevance judgments. Most queries have one positive passage, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 2, and 7 queries are multi-positive, or 14.0% of the set.

Queries average 47.04 characters, while documents average 525.60 characters. Queries are concise search-style questions, and the documents are paragraph-like evidence passages. The task is less multi-hop than HotpotQA and less paraphrase-oriented than Quora; its center is answer-bearing Wikipedia passage retrieval.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5140, hit@10 of 0.8000, and recall@100 of 0.9123 using the top-500 BM25 candidate subset. Lexical matching is effective when a query contains distinctive names, titles, dates, or phrases that identify the relevant page.

The remaining gap comes from relation selection. BM25 may retrieve a passage about the same entity while missing the paragraph that answers the requested why, where, who, or when relation. It is a useful candidate generator but not the strongest direct ranker for natural question intent.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6726, hit@10 of 0.8600, and recall@100 of 1.0000. Dense retrieval is the strongest overall profile by nDCG@10 and recall@100. It improves substantially over BM25, showing that embedding similarity captures answer intent beyond surface overlap.

This is especially valuable for questions where the passage uses different wording from the query. Dense retrieval can connect a natural question to a passage that expresses the answer relation indirectly. Its full recall@100 also makes it a strong candidate source for reranking.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6584, hit@10 of 0.8800, and recall@100 of 0.9649. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.02 candidates. The hybrid profile has the best hit@10, while dense retrieval has better nDCG@10 and recall@100.

This suggests that hybrid search is a strong practical candidate pool but not the best direct ranking profile in this slice. BM25 contributes exact entity and title matches, while dense retrieval contributes relation-aware matching. The tradeoff is that combining signals can slightly reduce the complete coverage that dense achieves alone.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 measures whether an answer passage is visible, and nDCG@10 measures how early it appears. recall@100 is important for reranking and QA pipelines because a reader cannot answer if the evidence is missing from the candidate set.

The comparison shows that BM25 is useful for entity anchoring, dense retrieval is best for semantic answer evidence, and reranking_hybrid provides a high-hit candidate pool. This task is a useful diagnostic for whether a model understands natural user questions rather than only matching Wikipedia titles.

### Query and Relevance Type Tendencies

Queries ask about where the Final Four is held, whether The Nightmare Before Christmas was originally a Disney movie, why the Angel of the North is there, where the Three-Fifths Compromise appears in the Constitution, and who sings "Somebody's Watching Me" with Michael Jackson. Positive passages contain the corresponding Wikipedia evidence.

The task rewards answer-type recognition and entity grounding. A passage can mention the right film, song, person, or event while failing to answer the exact question. Relation-specific hard negatives are therefore important.

### Representative Failure Modes

Likely failures include retrieving a same-entity passage that does not answer the question, confusing related titles or events, missing explanatory passages for why questions, and ranking broad background pages above answer-bearing evidence. BM25 may be too literal, while dense retrieval may occasionally retrieve semantically close but incomplete passages.

### Training Data That May Help

Useful training data includes non-overlapping Natural Questions training examples, open-domain QA retrieval pairs over Wikipedia, answer-span to passage retrieval supervision, and KILT-style question-to-Wikipedia evidence pairs. Hard negatives should share the entity or topic but lack the requested answer relation.

### Model Improvement Notes

A model targeting this task should improve relation-aware answer passage ranking while preserving exact entity recall. Sparse systems need query expansion and title handling. Dense systems are the strongest baseline and can improve with answer-aware contrastive training. Hybrid systems are useful when exact entity matching and semantic evidence matching both need to be retained.

## Example Data

### Public Sources

The original task is based on Natural Questions, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact English dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [Natural Questions](https://aclanthology.org/Q19-1026/) |
| Project page | [Google Research Natural Questions page](https://research.google/pubs/natural-questions-a-benchmark-for-question-answering-research/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Source dataset card | [BeIR/nq](https://huggingface.co/datasets/BeIR/nq) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| where is final four being held this year | The 2018 NCAA Division I Men's Basketball Tournament was a 68-team tournament. |
| was nightmare before christmas originally a disney movie | The Nightmare Before Christmas originated in a poem by Tim Burton while he worked at Disney. |
| why is the angel of the north there | The angel signifies coal miners, industrial transition, and human hopes and fears. |
| where was the 3/5 compromise originally stated in the constitution | The Three-Fifths Compromise is found in Article 1, Section 2, Clause 3. |
| who sings somebody's watching me with michael jackson | "Somebody's Watching Me" is a song by American singer Rockwell. |
