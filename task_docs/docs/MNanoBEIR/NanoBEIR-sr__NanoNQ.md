# MNanoBEIR / NanoBEIR-sr / NanoNQ

## Overview

NanoNQ in the Serbian NanoBEIR slice is a compact answer-passage retrieval task derived from Natural Questions and represented through the BEIR-style retrieval format. The queries are Serbian translations of information-seeking questions, and the corpus consists of Serbian translated Wikipedia passages that may contain the answer. The task asks a model to retrieve the passage that supports answering the question, not merely a passage that repeats the same surface terms. In this Nano version, the benchmark is small enough for rapid diagnostics while preserving the core difficulty of open-domain question answering: entity grounding, paraphrase, answer-bearing context, and short queries whose decisive evidence may appear in a longer passage.

## Details

### What the Original Data Measures

Natural Questions was designed around real search questions and Wikipedia evidence, so this task measures whether a retriever can connect a user question to an answer-bearing passage. The query usually names an entity, event, title, person, or concept, while the relevant passage often contains surrounding explanatory text rather than a sentence copied from the query. In the Serbian translated setting, the model must also handle translated names, inflection, transliteration choices, and cases where English-origin titles or proper nouns remain partly unchanged.

This makes NanoNQ different from duplicate-question retrieval or short-title matching. A strong result requires more than high lexical overlap: the model must find passages where the answer relation is expressed in context. At the same time, lexical grounding remains important because many queries contain distinctive named entities or quoted titles that can strongly narrow the candidate set.

### Observed Data Profile

The task contains 50 queries, 5,035 corpus documents, and 57 relevance judgments. Each query has at least one positive passage, with an average of 1.14 positives per query. The median number of positives is 1, the maximum is 2, and 7 queries have multiple positives, or 14.0% of the query set. This is therefore a mostly single-answer benchmark, where top-rank precision is often more important than broad recall across many acceptable documents.

The average query length is 45.60 characters, while the average document length is 514.47 characters. The large gap between short questions and longer passages matters for retrieval behavior. Query terms are sparse and highly selective, but relevant passages may contain additional context that changes the lexical distribution. A model that only keys on repeated words can still succeed on entity-heavy questions, but it may miss passages where the answer is described indirectly.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2624, hit@10 of 0.4800, and recall@100 of 0.7368 using the top-500 BM25 candidate subset. This profile suggests that lexical matching finds many relevant passages somewhere in the first 100 ranks, but it is much weaker at placing the correct passage in the top 10. That is consistent with a Natural Questions style task: distinctive words and names help candidate discovery, while answer-bearing evidence often depends on context that BM25 does not model directly.

The relatively high recall@100 compared with the low nDCG@10 is useful diagnostically. BM25 is not failing to see the task completely; rather, it often ranks several lexical distractors above the true evidence passage. For model researchers, this makes the task a good place to inspect whether a reranker or dense retriever can promote passages that answer the question instead of passages that merely share rare terms.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5343, hit@10 of 0.7200, and recall@100 of 0.8772. Dense retrieval is clearly stronger than BM25 on this task, especially at the top of the ranking. The gain indicates that embedding similarity is capturing question-answer semantics, paraphrase, and passage-level context beyond exact term overlap.

This is the expected pattern for many Natural Questions style tasks. The query asks for a fact or relation, and the relevant passage may express the answer with wording that is not a direct lexical restatement. Dense retrieval can connect semantically compatible formulations, and it is less dependent on the exact translated surface form. The remaining errors are likely to involve fine-grained entity ambiguity, very similar Wikipedia passages, or questions whose answer hinges on a small phrase rather than broad topical similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4228, hit@10 of 0.6800, and recall@100 of 0.9123. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 3 safeguard rows and a mean of 100.06 candidates. Its recall@100 is the strongest among the three profiles, while its top-10 ranking is weaker than the dense run.

This indicates that the hybrid candidate pool is doing what it is meant to do: it broadens coverage by combining lexical and dense evidence. However, for NanoNQ in Serbian, the final ordering implied by the hybrid setup does not outperform dense retrieval at the top ranks. Researchers should read this as a candidate-generation advantage rather than a complete ranking advantage. The hybrid pool is valuable when a later reranker can use the combined candidate set, but the dense retriever alone is the stronger first-stage ranker for top-10 quality here.

### Metric Interpretation for Model Researchers

nDCG@10 is the most direct signal for whether a model places answer-bearing passages where a downstream QA or RAG system would actually use them. hit@10 measures whether at least one relevant passage appears in the practical inspection window, and recall@100 measures whether the relevant passage is available for reranking. In this task, the difference between BM25 recall@100 and BM25 nDCG@10 is especially informative: lexical retrieval often finds a plausible candidate set but needs semantic reranking.

The dense profile shows that embedding similarity is well aligned with this benchmark. The reranking_hybrid profile shows that combining lexical and dense sources improves coverage, but researchers should not assume that wider coverage automatically means better top-rank ordering. NanoNQ-sr is therefore useful for separating candidate recall from first-page ranking quality.

### Query and Relevance Type Tendencies

Queries tend to be direct fact-seeking questions such as where an event is held, whether a film was originally released by a particular company, why a monument exists, where a constitutional compromise appears, or who sings on a song. Relevant documents are answer-bearing explanatory passages, often containing named entities, dates, titles, and compact factual statements.

The Serbian translation adds realistic multilingual retrieval issues. Some named entities and cultural titles may remain close to English, while surrounding grammar and function words follow Serbian. A model that handles only lexical overlap may overvalue repeated names and miss the answer relation. A model that handles only broad semantic similarity may retrieve topically related passages that do not contain the exact fact.

### Representative Failure Modes

Likely failures include retrieving a Wikipedia passage about the same entity but not the requested fact, confusing related events or works with similar names, ranking definitional background above the answer-bearing passage, and missing a positive passage when Serbian morphology changes the lexical form of key terms. Dense models may also over-rank passages with the right topic but insufficient evidence, while BM25 may over-rank passages that repeat quoted titles or proper nouns without answering the question.

### Training Data That May Help

Useful training data includes multilingual question-answer retrieval pairs, Wikipedia passage retrieval examples, translated open-domain QA data, and hard negatives built from passages sharing entities with the query but lacking the answer. Serbian and related South Slavic data can help with morphology and word order, while multilingual alignment data can help with translated titles and proper names. For rerankers, hard negatives from the BM25 and dense candidate pools are particularly valuable because the errors are often plausible rather than random.

### Model Improvement Notes

A model targeting this task should preserve entity precision while improving answer-relation matching. For dense retrievers, the main improvement area is distinguishing answer-bearing passages from merely topical passages. For sparse or lexical systems, Serbian tokenization, normalization, and morphology-aware matching may improve candidate quality. For hybrid systems, the high recall@100 suggests that reranking is the natural place to focus: the combined pool contains strong candidates, but the final top ranks need better evidence-sensitive ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| Gde se održava Final Four ove godine? [37 chars] | NCAA Divizija I muški košarkaški turnir 2018. bio je turnir sa 68 timova po sistemu direktnog ispadanja, održan kako bi se odredio nacionalni šampion u muškoj koledž košarci NCAA Divizije I za sezonu... [200 / 353 chars] |
| Da li je "Noćna mora pre Božića" originalno bio Diznijev film? [62 chars] | "Pakao pre Božića" nastao je iz pesme koju je Tim Burton napisao 1982. godine, dok je radio kao animator u studiju Walt Disney Feature Animation. Uz uspeh filma "Vinsent" iste godine, studijo Walt Dis... [200 / 616 chars] |
| Zašto je anđeo severa tu? [25 chars] | Prema Gormliju, značaj anđela je bio trostruk: prvo, da označi da su ispod mesta njegove izgradnje rudari uglja radili dva veka; drugo, da obuhvati prelazak iz industrijskog u informaciono doba, i tre... [200 / 264 chars] |
| Gde je kompromis 3/5 prvobitno naveden u ustavu? [48 chars] | Kompromis o tri petine nalazi se u Članu 1, Odeljku 2, Stav 3 Ustava Sjedinjenih Država, koji glasi: [100 chars] |
| Ko peva pesmu "Somebody's Watching Me" sa Majklom Džeksonom? [60 chars] | "Somebody's Watching Me" je pesma američkog pevača Rokvela sa njegovog debitantskog studijskog albuma Somebody's Watching Me (1984). Objavljena je kao Rokvelov debitanski singl i vodeći singl sa album... [200 / 358 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Natural Questions](https://aclanthology.org/Q19-1026/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sr dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |

Representative query and positive passage snippets:

| Query | Positive passage snippet |
| --- | --- |
| Gde se održava Final Four ove godine? | NCAA Divizija I muški košarkaški turnir 2018. bio je turnir sa 68 timova... |
| Da li je "Noćna mora pre Božića" originalno bio Diznijev film? | "Pakao pre Božića" nastao je iz pesme koju je Tim Burton napisao 1982... |
| Zašto je anđeo severa tu? | Prema Gormliju, značaj anđela je bio trostruk... |
| Gde je kompromis 3/5 prvobitno naveden u ustavu? | Kompromis o tri petine nalazi se u Članu 1, Odeljku 2, Stav 3 Ustava Sjedinjenih Država... |
| Ko peva pesmu "Somebody's Watching Me" sa Majklom Džeksonom? | "Somebody's Watching Me" je pesma američkog pevača Rokvela... |
