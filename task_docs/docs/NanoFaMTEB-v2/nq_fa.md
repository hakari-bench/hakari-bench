# NanoFaMTEB-v2 / nq_fa

## Overview

`nq_fa` is a Persian Natural Questions-style passage retrieval task in NanoFaMTEB-v2. The queries are short factual questions, and the documents are Persian encyclopedia-style passages.

This task evaluates open-domain factual retrieval in Persian. Compared with many-positive web passage tasks, `nq_fa` usually has only one positive passage per query, so the model must identify the specific passage that answers the question rather than relying on broad topical coverage.

## Details

### What the Original Data Measures

FaMTEB includes translated and Persian retrieval datasets to evaluate text embeddings beyond English. `nq_fa` uses `MCINext/NQ_FA_test_top_250_only_w_correct-v2`, a Persian Natural Questions-style hard-negative dataset under the MTEB retrieval setup.

Natural Questions-style retrieval measures whether a system can find answer-bearing passages for factual questions derived from real search behavior. In this Persian split, the target documents are compact encyclopedia passages, and hard negatives often share entities or topical vocabulary with the correct answer.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 251 positive qrels. Queries have 1.25 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 3. There are 48 multi-positive queries, or 24.0% of the split. Queries average 46.72 characters, and documents average 556.82 characters.

Observed examples ask about television show judges, release timing, amusement-park ride closure dates, actors in a sitcom, and the number of national parks in India. Positive documents are concise passages about the relevant program, attraction, actor, list, or entity.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4470, hit@10 of 0.7000, and recall@100 of 0.9363 with a top-500 candidate pool. This profile shows strong lexical candidate coverage but weaker top-10 ordering.

Named entities, titles, dates, and distinctive nouns help BM25 include positives in the broader candidate set. The challenge is that many hard negatives repeat the same entity name or topic. BM25 can retrieve a passage about the right show, location, or country while missing the exact answer-bearing passage at the top.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.5817, hit@10 of 0.8350, and recall@100 of 0.9163. Dense retrieval is the strongest first-stage top-ranking profile for this task.

The improvement over BM25 suggests that embedding similarity helps connect the factual intent of the question to the answer passage. Dense retrieval can handle paraphrase, translated phrasing, and answer descriptions that do not repeat every query term. Its recall@100 is slightly below BM25, so lexical matching still contributes useful breadth.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5274, hit@10 of 0.7900, and recall@100 of 0.9841. It uses 100 candidates per query, with four rank-101 safeguard positives.

Hybrid retrieval is best for candidate coverage. It does not outperform dense retrieval on nDCG@10, but it gives a reranker a more complete pool of answer-bearing passages. For a task with mostly one positive per query, this high recall is important because a missing candidate cannot be recovered by downstream reranking.

### Metric Interpretation for Model Researchers

`nq_fa` separates exact-answer ranking from broad candidate recall. Dense retrieval is the best direct ranker, BM25 is a strong lexical recall source, and reranking_hybrid provides the most complete top-100 candidate set.

nDCG@10 and hit@10 are especially important because most queries have only one relevant passage. Recall@100 is still useful for diagnosing whether a candidate generator supplies the answer passage to a reranker. The four safeguard rows indicate that a small number of positives needed the optional rank-101 inclusion in the hybrid pool.

### Query and Relevance Type Tendencies

Queries are Persian factual questions, often asking "who", "when", "how many", or "which" questions. They frequently mention a title, person, place, or organization. Relevant documents are encyclopedia-like passages that contain the answer and enough context to identify the entity.

The relevance relation is narrow. A passage about the same subject is not enough if it does not answer the requested fact.

### Representative Failure Modes

BM25 may over-rank passages that share the entity name but discuss a different property. Dense retrieval may retrieve a semantically close passage that answers a related question. Hybrid retrieval reduces candidate misses but still needs a reranker to distinguish the exact answer span from nearby entity descriptions.

Date and list questions can be difficult when many passages contain numbers. Actor, episode, or release questions can also confuse models if several names from the same franchise or show appear in the corpus.

### Training Data That May Help

Useful training data includes Persian open-domain QA retrieval, translated Natural Questions examples, Persian Wikipedia passage retrieval, and hard negatives that share the same entity but answer a different fact. Training should include narrowly answerable questions with single or few positives.

Training should exclude source test rows included in this Nano split.

### Model Improvement Notes

Improving this task requires precise question-passage alignment. Models should preserve entity names and dates while also representing the relation asked by the question. Persian-aware tokenization and training on translated QA retrieval can help with both exact names and paraphrased answer contexts.

For reranking, the most valuable behavior is rejecting topically related passages that do not contain the requested fact. A reranker should focus on answer sufficiency, not only subject similarity.

## Example Data

### Public Sources

This task is documented through the FaMTEB paper and the `MCINext/NQ_FA_test_top_250_only_w_correct-v2` dataset card. MTEB provides the broader retrieval evaluation framework.

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/NQ_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/NQ_FA_test_top_250_only_w_correct-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian question asking who judged a season of a skating television program. | A passage about the program season and the returning hosts, coaches, and judges. |
| A question asking when the fifth season of RWBY was released. | A passage about the animated web series and its episode or release history. |
| A question asking when a log flume ride at Alton Towers closed. | A passage about the ride's opening, redesign, sponsorship, and closure context. |
| A question asking who played Professor Proton in The Big Bang Theory. | A biographical passage about Bob Newhart and his television roles. |
| A question asking how many national parks India has. | A list-style passage giving the number of national parks and their protected area coverage. |
