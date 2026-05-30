# MNanoBEIR / NanoBEIR-sv / NanoFEVER

## Overview

NanoFEVER in the Swedish NanoBEIR slice is a Wikipedia evidence retrieval task derived from FEVER. The queries are Swedish translated factual claims, and the corpus contains Swedish translated evidence passages. The retrieval goal is to find passages that can verify the claim, rather than simply retrieve a page on the same topic. This compact task is useful for evaluating claim-to-evidence retrieval, entity grounding, and factual search behavior in a multilingual setting.

## Details

### What the Original Data Measures

FEVER was designed for fact extraction and verification over Wikipedia. In the retrieval step, a system receives a claim and must retrieve evidence passages that contain enough information to assess it. The relevant passage is often centered on a named entity, event, work, person, or place, but relevance depends on the claim relation as well as topic.

In the Swedish translated version, the model must handle factual claims expressed in Swedish while many named entities, media titles, and organizations may retain international forms. This makes the task a mix of exact entity matching and evidence-sensitive semantic retrieval. A strong model should retrieve the passage that resolves the claim, not just a passage where the same entity name appears.

### Observed Data Profile

The task contains 50 queries, 4,996 documents, and 57 relevance judgments. Most queries have one positive passage, with an average of 1.14 positives per query. The minimum is 1, the median is 1.0, the maximum is 3, and 6 queries have multiple positives, or 12.0% of the query set. This is therefore mostly a single-evidence retrieval task.

Queries average 44.64 characters, while documents average 1,166.66 characters. The claims are short and often contain distinctive entities or factual assertions. The relevant documents are much longer Wikipedia-style passages, so the model must locate an evidence-bearing passage inside a larger topical context.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7512, hit@10 of 0.9200, and recall@100 of 0.9649 using the top-500 BM25 candidate subset. This is a very strong lexical baseline. FEVER-style claims often contain named entities and specific wording that also appears in the evidence passage, and BM25 can exploit those anchors effectively.

The remaining gap shows that exact terms are not enough for perfect ranking. Some claims require connecting a relation or factual attribute, and there may be several passages about the same entity. BM25 can find the right neighborhood, but it may still rank a related entity passage above the one that directly verifies the claim.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8570, hit@10 of 0.9400, and recall@100 of 0.9298. Dense retrieval improves top-rank quality over BM25, although its recall@100 is slightly lower. This means embedding similarity is especially useful for ordering the most relevant evidence passages near the top.

The dense advantage likely comes from matching the factual meaning of the claim rather than only matching entity terms. It can distinguish a passage about a work, person, or location that better supports the claim from other passages with similar lexical content. The lower recall@100 suggests that exact lexical anchors still help recover some candidates that dense retrieval may miss.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.8153, hit@10 of 0.9800, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. The hybrid profile has the strongest hit@10 and complete recall@100, while dense retrieval has the strongest nDCG@10.

This is a clear case where hybrid search improves evidence coverage by combining lexical and dense sources. The full recall@100 means the relevant passages are always present in the hybrid candidate pool. However, the dense ranking places them slightly better in the top 10. For a two-stage system, reranking_hybrid is an excellent candidate source; for first-stage ranking alone, dense retrieval has the strongest graded top-10 ordering.

### Metric Interpretation for Model Researchers

Because most queries have a single positive, nDCG@10 and hit@10 directly reflect whether the evidence passage is usable without deep reranking. recall@100 indicates whether a downstream verifier or reranker has access to the evidence. In this task, all three methods are comparatively strong, but they reveal different tradeoffs.

BM25 shows that Swedish FEVER has strong lexical anchors. Dense retrieval shows that semantic ordering improves first-page quality. reranking_hybrid shows that combining the two is best for candidate completeness. A model researcher can use this task to test whether improvements come from finding missing evidence, ranking already-found evidence higher, or both.

### Query and Relevance Type Tendencies

Queries are short factual claims such as whether Keith Godchaux knew Grateful Dead, whether a TV show is a sitcom, whether advanced aircraft were made in Burbank, whether Nero is human, or whether Scream 2 is only a German film. Relevant documents are Wikipedia-style passages that provide the factual context.

The task rewards precise entity grounding. Many claims are easy to mis-handle if the model retrieves the right entity but the wrong fact. It also rewards handling of negation-like or exclusivity wording, such as "only," because the relevant passage may need to contradict or qualify the claim rather than simply repeat it.

### Representative Failure Modes

Likely failures include retrieving a passage about the correct entity that lacks the target fact, confusing similarly named works or people, over-ranking broad entity pages over specific evidence, and missing translated claim wording when entity names remain unchanged. BM25 may overvalue repeated names, while dense retrieval may occasionally miss exact lexical candidates with unusual titles or names.

### Training Data That May Help

Useful training data includes claim-evidence retrieval, Wikipedia evidence mining, multilingual fact-checking, and hard negatives that share the same entity but do not verify the claim. Swedish Wikipedia and translated fact-checking examples can improve language coverage. For rerankers, same-entity negatives are particularly valuable because the main difficulty is often factual relation, not broad topic.

### Model Improvement Notes

A model targeting this task should preserve strong named-entity recall while improving factual relation ranking. Sparse systems should maintain exact entity and title matching. Dense systems should improve coverage for rare names while keeping their strong top-rank semantic ordering. Hybrid systems are well aligned with the task, especially when followed by a verifier or reranker that can inspect the evidence relation.

## Example Data

### Public Sources

The original task is based on FEVER, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [FEVER](https://arxiv.org/abs/1803.05355) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Keith Godchaux kände till Grateful Dead | The Grateful Dead var ett amerikanskt rockband som bildades 1965 i Palo Alto, Kalifornien... |
| Taarak Mehta Ka Ooltah Chashmah är en sitcom. | Taarak Mehta Ka Ooltah Chashmah är Indiens längsta löpande sitcom... |
| Hemliga och tekniskt avancerade flygplan tillverkades i Burbank, Kalifornien. | Burbank är en stad i Los Angeles County i södra Kalifornien, USA... |
| Nero är en människa | Den julisk-claudiska dynastin syftar på de första fem romerska kejsarna... |
| Scream 2 är enbart en tysk film. | Scream 2 är en amerikansk slasherfilm från 1997, regisserad av Wes Craven... |
