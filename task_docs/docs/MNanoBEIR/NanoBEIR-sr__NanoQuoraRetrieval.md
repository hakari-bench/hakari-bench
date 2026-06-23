# MNanoBEIR / NanoBEIR-sr / NanoQuoraRetrieval

## Overview

NanoQuoraRetrieval in the Serbian NanoBEIR slice is a duplicate-question retrieval task derived from Quora Question Pairs and represented in a BEIR-style search format. Each query is a Serbian translated question, and the corpus contains Serbian translated questions that may ask the same thing in another way. The benchmark measures whether a retriever can identify semantic equivalence between short user questions rather than retrieve long explanatory documents. It is especially useful for studying paraphrase sensitivity, question intent, and the difference between lexical overlap and meaning-preserving reformulation.

## Details

### What the Original Data Measures

Quora Question Pairs was created to identify whether two user-written questions are duplicates. In retrieval form, this becomes a task where the query question must retrieve another question with the same intent. The relevant item may share many words with the query, but it may also use a different construction, different modifiers, or a more specific phrasing. Because both query and document are short questions, there is little extra context to average over.

In the Serbian translated version, the benchmark additionally tests robustness to translated question wording, inflection, and named-entity spelling. The model must compare intent at the sentence level. A near match that changes the target, sentiment, or requested explanation should not be treated as equivalent merely because it shares many words.

### Observed Data Profile

The task contains 50 queries, 5,046 corpus documents, and 70 relevance judgments. Each query has at least one positive question, with an average of 1.40 positives per query. The median is 1, the maximum is 6, and 10 queries have multiple positives, or 20.0% of the query set. This gives the task more alternative positives than many answer-passage NanoBEIR tasks, while still keeping most queries focused on a single duplicate target.

The average query length is 49.26 characters, and the average document length is 58.05 characters. Query and document lengths are therefore closely matched. This short-text structure makes the benchmark sensitive to small wording changes: a few tokens can determine whether two questions are duplicates or only topically related.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5837, hit@10 of 0.7800, and recall@100 of 0.9143 using the top-500 BM25 candidate subset. This is a strong lexical profile compared with longer passage tasks. Duplicate questions often repeat key nouns, verbs, or entities, so term frequency and exact token overlap can be a powerful signal.

The metrics also show the limitation of lexical matching. BM25 has high recall@100, meaning that it usually brings at least one duplicate candidate into the reranking window, but it does not match the dense run at top-10 ranking. In duplicate-question retrieval, lexical overlap can be misleading when a question is phrased similarly but asks a different thing, and it can be insufficient when two duplicate questions use different wording.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8100, hit@10 of 0.9200, and recall@100 of 0.9714. This is the strongest profile on the task. The large top-rank gain over BM25 indicates that embedding similarity is well suited to Serbian translated duplicate-question retrieval, where the goal is to compare question intent rather than document topicality.

Dense retrieval benefits from the short and symmetric structure of the data. Both sides are questions, and the semantic unit is compact. This reduces the risk that a long document contains multiple unrelated topics, and it lets embeddings focus on intent equivalence. Remaining errors are likely to involve subtle meaning changes, highly generic questions, or cases where duplicate status depends on pragmatic interpretation rather than surface semantics.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7129, hit@10 of 0.9200, and recall@100 of 0.9714. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 1 safeguard row and a mean of 100.02 candidates. Its hit@10 and recall@100 match the dense run, while nDCG@10 remains lower.

This pattern suggests that the hybrid pool preserves the major candidate coverage advantages of dense retrieval and also incorporates lexical evidence. However, the final top ordering is not as strong as dense retrieval alone. For this task, dense semantic similarity is the most aligned first-stage signal, while the hybrid pool is still useful as a broad candidate source for later reranking or diagnostics.

### Metric Interpretation for Model Researchers

nDCG@10 is the most important ranking metric here because duplicate-question systems typically need the best matches first. hit@10 indicates whether a user-facing or downstream system would see at least one duplicate candidate, and recall@100 indicates whether a later reranker has enough coverage to work with. The combination of high BM25 recall@100 and higher dense nDCG@10 shows that lexical retrieval is a strong candidate generator but less reliable as the final ranker.

The dense and reranking_hybrid recall values are identical at 0.9714, and their hit@10 values are also identical at 0.9200. The difference is primarily ordering quality inside the top 10. That makes NanoQuoraRetrieval-sr a useful diagnostic for models that already retrieve the right candidates but need better fine-grained ranking of paraphrases.

### Query and Relevance Type Tendencies

Queries are short user questions, often asking for advice, explanations, opinions, or how something works. Positives are duplicate or near-duplicate questions, not passages. Examples include matching whether laughing at one's own jokes is strange, identifying the same request for the best lie someone has told, and matching closely related formulations of how to become physically strong.

Because the text units are short, the task emphasizes sentence-level intent. Exact overlap can be very helpful when the duplicate wording is nearly identical, but it is not sufficient. A good model must recognize reformulations such as word-order changes, synonym use, added specificity, and equivalent question framing while rejecting questions that share a topic but ask a different thing.

### Representative Failure Modes

Likely failures include over-ranking questions that share many words but differ in intent, missing duplicates that use different vocabulary, confusing a broad question with a narrower one, and treating opinion questions with different stances as equivalent. Dense models may sometimes overgeneralize semantic similarity, while BM25 may overvalue repeated nouns or named entities. Hybrid systems can inherit both error types if the final ordering does not explicitly model duplicate status.

### Training Data That May Help

Useful training data includes multilingual duplicate-question pairs, paraphrase identification data, natural question rewrites, and hard negatives built from high-overlap non-duplicates. Serbian and related-language paraphrase data can help with morphology and translated phrasing. For rerankers, contrastive examples where two questions share many words but ask different things are especially valuable because they directly target the main lexical failure mode.

### Model Improvement Notes

A model targeting this task should prioritize fine-grained question intent matching. Dense retrievers already perform strongly, so improvements may come from better multilingual paraphrase alignment, stronger treatment of negation and scope, and hard-negative training on near-duplicate but non-equivalent questions. BM25-style systems can remain useful for candidate recall, but the final ranking should be guided by semantic equivalence rather than raw overlap. Hybrid systems should preserve lexical anchors without letting them dominate when intent diverges.

## Example Data

| Query | Positive document |
| --- | --- |
| Da li je u redu da se smeješ svojim šalama? [43 chars] | Je li čudno da se smejem svojim šalama? [39 chars] |
| Koja je najbolja laž koju ste ikada ispricali? [46 chars] | Koja je najbolje osmišljena laž koju ste ikada ispričali? [57 chars] |
| Zašto Quora često predlaže odgovore u mom feedu koji omalovažavaju Donalda Trumpa? [82 chars] | Zašto se čini da Quora ima samo subjektivne, pristrasne odgovore na pitanja o Donaldu Trampu? [93 chars] |
| Kako mogu da postanem fizički jak? [34 chars] | Kako da postanem fizički jak? [29 chars] |
| Kako će raditi kvantni satelit? [31 chars] | Kako funkcioniše kvantni satelit i koje bi bile njegove osnovne primene? [72 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sr dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |

Representative query and positive question snippets:

| Query | Positive question |
| --- | --- |
| Da li je u redu da se smeješ svojim šalama? | Je li čudno da se smejem svojim šalama? |
| Koja je najbolja laž koju ste ikada ispricali? | Koja je najbolje osmišljena laž koju ste ikada ispričali? |
| Zašto Quora često predlaže odgovore u mom feedu koji omalovažavaju Donalda Trumpa? | Zašto se čini da Quora ima samo subjektivne, pristrasne odgovore na pitanja o Donaldu Trampu? |
| Kako mogu da postanem fizički jak? | Kako da postanem fizički jak? |
| Kako će raditi kvantni satelit? | Kako funkcioniše kvantni satelit i koje bi bile njegove osnovne primene? |
