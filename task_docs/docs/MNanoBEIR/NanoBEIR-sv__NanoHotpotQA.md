# MNanoBEIR / NanoBEIR-sv / NanoHotpotQA

## Overview

NanoHotpotQA in the Swedish NanoBEIR slice is a multi-hop Wikipedia retrieval task derived from HotpotQA. The queries are Swedish translated questions, and the corpus contains Swedish translated supporting passages. Each query requires two relevant passages, so the benchmark measures whether a retriever can recover the connected evidence needed for explainable question answering. It is a compact diagnostic for bridge-entity retrieval, multi-positive ranking, and multilingual question-to-passage matching.

## Details

### What the Original Data Measures

HotpotQA was designed for diverse and explainable multi-hop question answering. In retrieval form, the system must find supporting passages that together answer a question. One passage may identify an entity, while the second supplies the answer or completes the reasoning chain. Relevance is therefore not only about topical similarity; it is about retrieving both pieces of evidence needed for the multi-hop path.

The Swedish translated version tests whether a model can preserve entity links and question structure across translated text. Queries often mention one entity and ask for a property that is found through another related entity. A strong retriever must use both lexical clues and semantic bridging rather than stopping at the first obvious passage.

### Observed Data Profile

The task contains 50 queries, 5,090 documents, and 100 relevance judgments. Every query has exactly two positives: the average, minimum, median, and maximum positives per query are all 2.0, and all 50 queries are multi-positive. This makes the task structurally different from single-answer retrieval; retrieving only one support passage is incomplete.

Queries average 86.34 characters, while documents average 349.52 characters. The queries are moderately long because they often contain a bridge description, a named entity, and the final information need. The documents are concise Wikipedia-style passages, which makes exact entity and relation matching visible in the ranking metrics.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7413, hit@10 of 0.9800, and recall@100 of 0.9100 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Many HotpotQA questions contain named entities, titles, dates, or other distinctive words that also appear in the supporting passages, allowing BM25 to recover at least one positive for nearly every query.

The recall@100 value shows that BM25 still misses some supporting passages. Multi-hop retrieval is stricter than ordinary answer retrieval because both positives matter. BM25 may retrieve the entity mentioned in the query but fail to retrieve the second bridge passage, or it may over-rank passages with shared names that do not complete the reasoning chain.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.7617, hit@10 of 0.9400, and recall@100 of 0.9500. Dense retrieval improves nDCG@10 and recall@100 over BM25, while BM25 has slightly higher hit@10. This indicates that embedding similarity is better at covering both supporting passages, even when one support is less lexically obvious.

The dense profile is well aligned with the multi-hop nature of the task. It can connect related entities and question intent beyond exact word overlap. The slightly lower hit@10 suggests that lexical entity anchors remain useful for ensuring at least one positive appears early, but dense retrieval is stronger for recovering the full support set.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.8233, hit@10 of 1.0000, and recall@100 of 0.9400. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. This is the strongest top-rank profile among the three modes and achieves a positive in the top 10 for every query.

The hybrid result fits the task well. BM25 contributes precise entity matching, while dense retrieval contributes bridge and semantic matching. The combined signal improves top-10 ordering, even though dense retrieval has slightly higher recall@100. For a practical multi-hop QA pipeline, reranking_hybrid is attractive because it puts supporting evidence high in the first page.

### Metric Interpretation for Model Researchers

hit@10 is useful but incomplete here. Since each query has two positives, a system can hit@10 by retrieving only one supporting passage and still fail as a multi-hop evidence retriever. nDCG@10 and recall@100 are more informative because they reward recovering and ranking the relevant set. recall@100 indicates whether a second-stage reader or reranker has access to both supports.

The method comparison shows that all three modes are strong, but for different reasons. BM25 excels at visible entity anchors. Dense retrieval improves support-set coverage. reranking_hybrid gives the best top-10 ordering and perfect hit@10. This makes NanoHotpotQA-sv useful for evaluating whether a model can combine entity precision with bridge reasoning.

### Query and Relevance Type Tendencies

Queries ask multi-hop questions such as which actor appeared with Penny Rae Bridges in a sitcom, who gave Kaganoi Shigemochi a sword made by the founder of the Muramasa school, which film was written and directed by Joby Harold and scored by Samuel Sim, or when a particular Clemson-Oklahoma football game took place. Positives are supporting passages that together resolve the entity chain.

The task rewards models that track named entities, works, people, organizations, events, and their relationships. A passage about the named query entity may be relevant, but the second support passage is often needed to complete the answer. This is the core retrieval challenge.

### Representative Failure Modes

Likely failures include retrieving only one of the two supports, ranking same-name distractors above the bridge passage, missing a support when it uses a different description, and confusing works, people, or events with similar titles. BM25 may over-focus on explicit names, while dense retrieval may retrieve semantically related but incomplete evidence. Hybrid systems can reduce these failures when the final ranking preserves both lexical and semantic clues.

### Training Data That May Help

Useful training data includes multi-hop QA retrieval, Wikipedia bridge-question data, paired supporting-passage ranking, multilingual QA, and hard negatives that mention one bridge entity but do not complete the reasoning chain. Swedish Wikipedia data can help with translated entity descriptions. For rerankers, examples where only one of two supports is present are especially useful hard negatives.

### Model Improvement Notes

A model targeting this task should optimize for complete support recovery, not just first positive discovery. Sparse systems should preserve exact entity and title matching. Dense systems should strengthen relation and bridge-entity matching. Hybrid systems are well suited to the benchmark, but a downstream reranker should explicitly favor rankings that include both required supports.

## Example Data

### Public Sources

The original task is based on HotpotQA, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [HotpotQA](https://arxiv.org/abs/1809.09600) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive supporting-passage snippets:

| Query | Positive document snippet |
| --- | --- |
| Med vilken annan skådespelare medverkade Penny Rae Bridges i en TV-sitcom? | Penny Rae Bridges är en amerikansk skådespelerska. Hon har medverkat i TV-serier som "For Your Love"... |
| Vem gav Kaganoi Shigemochi ett svärd som tillverkades av den som grundade Muramasa-skolan? | Kaganoi Shigemochi var en japansk samuraj under Azuchi-Momoyama-perioden... |
| Vilken film är skriven och regisserad av Joby Harold och har musik av Samuel Sim? | Samuel Sim är en film- och TV-kompositör. Han fick först uppmärksamhet med sin prisbelönta musik... |
| När spelades denna college football-match på Sun Life Stadium i Miami Gardens, Florida, där Clemson slog de fjärdeplacerade Oklahoma Sooners med 37-17? | Clemson Tigers fotbollslaget 2015 representerade Clemson University i 2015 års NCAA Division I FBS fotbollssäsong... |
| Devil's Food är en samling med singlar av ett amerikanskt rock and roll-band som också är känt för att spela country-konserter under vilket namn? | Devil's Food är en samling av singlar av det amerikanska rock'n'roll-bandet Supersuckers... |
