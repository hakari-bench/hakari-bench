# MNanoBEIR / NanoBEIR-vi / NanoNQ

## Overview

NanoNQ in the Vietnamese NanoBEIR slice is an open-domain question answering retrieval task derived from Natural Questions. The queries are Vietnamese translated search questions, and the corpus contains Vietnamese translated Wikipedia-style passages. The retrieval goal is to find passages that answer real information-seeking questions. This makes the task useful for evaluating Vietnamese natural-question understanding, answer-bearing passage ranking, and semantic retrieval over encyclopedic text.

## Details

### What the Original Data Measures

Natural Questions was created from real Google search questions paired with Wikipedia evidence. In retrieval form, a model must map a natural user question to a passage that contains the answer. The questions are usually concise but can ask for locations, people, dates, reasons, definitions, or whether a proposition is true.

The Vietnamese translated version preserves the open-domain character of the task. Named entities and titles may remain in English, while the question structure and surrounding passage text are Vietnamese. A strong retriever must handle translated question wording, entity grounding, and answer-type inference.

### Observed Data Profile

The task contains 50 queries, 5,035 documents, and 57 relevance judgments. Most queries have one positive passage, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 2, and 7 queries are multi-positive, or 14.0% of the set.

Queries average 47.88 characters, while documents average 540.97 characters. This is a compact open-domain QA retrieval setting: questions are short enough that answer intent must be inferred, while documents are long enough to contain background context as well as the needed answer.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3848, hit@10 of 0.6200, and recall@100 of 0.8421 using the top-500 BM25 candidate subset. Lexical matching is useful because many questions include entity names, titles, or distinctive phrases. BM25 can often place the answer passage somewhere within the top 100.

The top-10 metrics are more limited. A passage may share the same entity or phrase while answering a different relation, and translated natural questions often do not reuse the exact wording found in the answer passage. BM25 is therefore a reasonable candidate generator but not the strongest direct ranker.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5939, hit@10 of 0.7800, and recall@100 of 0.9649. Dense retrieval is the strongest profile across all three reported metrics. It substantially improves top-10 ranking and candidate coverage over BM25.

This shows that embedding similarity is highly valuable for Vietnamese Natural Questions-style retrieval. Dense retrieval can connect the question's intent to answer passages even when the exact terms differ. It is especially useful for why, where, who, and whether-style questions, where the relation between query and passage matters more than raw word overlap.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5351, hit@10 of 0.7200, and recall@100 of 0.9298. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 3 safeguard rows, candidate counts from 100 to 101, and a mean of 100.06 candidates.

The hybrid profile is stronger than BM25 but weaker than dense retrieval on this task. It still provides a strong candidate pool by combining exact entity anchors with semantic matching, but the dense signal appears to dominate for direct ranking. For reranking, reranking_hybrid remains useful because it preserves broad coverage while reducing dependence on a single retrieval signal.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 measures whether the answer passage is visible to a user or RAG pipeline, while nDCG@10 measures how early it appears. recall@100 is a candidate-generation metric for downstream rerankers. Dense retrieval leading all three metrics indicates that this task is primarily semantic rather than purely lexical.

The comparison separates the retrieval behavior clearly: BM25 uses names and surface phrases effectively, dense retrieval captures answer intent, and reranking_hybrid provides a balanced but not best direct ranking. This task is useful for testing whether a model understands natural Vietnamese search questions.

### Query and Relevance Type Tendencies

Queries ask questions such as where the Final Four is held this year, whether The Nightmare Before Christmas was originally a Disney film, why the Angel of the North is there, where the Three-Fifths Compromise appears in the Constitution, and who sang "Somebody's Watching Me" with Michael Jackson. Relevant passages usually provide a direct answer inside broader encyclopedic context.

The task rewards answer-type recognition and relation matching. A model must know whether the query asks for a place, person, explanation, constitutional location, or media attribution, then rank the passage that resolves that specific need.

### Representative Failure Modes

Likely failures include retrieving a passage about the same entity but not the asked relation, missing answers because the question is phrased differently from the passage, confusing media titles or historical references, and ranking broad background pages above answer-bearing passages. BM25 is vulnerable to same-entity distractors, while dense retrieval may still confuse semantically adjacent facts.

### Training Data That May Help

Useful training data includes Vietnamese open-domain QA, multilingual Wikipedia passage retrieval, translated Natural Questions-style pairs, and hard negatives that share the entity but answer a different relation. Synthetic data should preserve natural short-question style rather than turning each query into a keyword list.

### Model Improvement Notes

A model targeting this task should improve semantic answer matching while keeping entity recall high. Sparse systems need query expansion and title normalization. Dense systems are the strongest baseline and can improve further with answer-aware hard negatives. Hybrid systems may be most useful as reranking candidate pools when exact entity matching and semantic coverage must both be preserved.

## Example Data

### Public Sources

The original task is based on Natural Questions, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Natural Questions](https://aclanthology.org/Q19-1026/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-vi dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |

Representative query and positive answer snippets:

| Query | Positive document snippet |
| --- | --- |
| Nam nay, vong chung ket bon duoc to chuc o dau | Giai bong ro NCAA Division I nam 2018 la mot giai dau loai truc tiep 68 doi... |
| Lieu Nightmare Before Christmas ban dau co phai la mot bo phim cua Disney khong | Ac Mong Truoc Giang Sinh bat nguon tu mot bai tho duoc viet boi Tim Burton... |
| tai sao thien than phia bac lai o do | Theo Gormley, y nghia cua mot thien than co ba khia canh... |
| noi nao thoa thuan 3/5 duoc neu ra trong hien phap | Thoa thuan Ba Nam Phan duoc tim thay trong Dieu 1, Muc 2, Khoan 3... |
| ai hat bai somebody's watching me voi michael jackson | "Somebody's Watching Me" la mot bai hat cua ca si nguoi My Rockwell... |
