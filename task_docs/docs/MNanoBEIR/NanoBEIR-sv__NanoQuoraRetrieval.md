# MNanoBEIR / NanoBEIR-sv / NanoQuoraRetrieval

## Overview

NanoQuoraRetrieval in the Swedish NanoBEIR slice is a duplicate-question retrieval task derived from Quora Question Pairs. The queries are Swedish translated questions, and the corpus contains Swedish translated questions that may ask the same thing in another form. The retrieval goal is to identify semantic equivalence between short questions, not to retrieve long answer passages. This makes the task a compact diagnostic for paraphrase retrieval, question intent matching, and the balance between lexical overlap and embedding-based similarity.

## Details

### What the Original Data Measures

Quora Question Pairs was created to identify duplicate questions. In retrieval form, a query question should retrieve another question that expresses the same information need. Relevance can involve nearly identical wording, synonym substitution, changed word order, added specificity, or a different framing of the same intent.

The Swedish translated version tests this duplicate-question behavior across translated text. Because both sides are short questions, there is little extra context to compensate for mistakes. A model must compare intent directly. A passage that shares words with the query but asks a different question should not be ranked as a duplicate, while a differently worded paraphrase should still be retrieved.

### Observed Data Profile

The task contains 50 queries, 5,046 documents, and 70 relevance judgments. The average number of positives is 1.40 per query, with a minimum of 1, a median of 1.0, and a maximum of 6. Ten queries have multiple positives, or 20.0% of the query set. Most queries therefore have a single duplicate target, but some have small paraphrase clusters.

Queries average 48.54 characters, and documents average 57.16 characters. Query and document lengths are closely matched, which gives the task a clean short-text retrieval profile. Small lexical or semantic changes matter because there is no long passage context to dilute or clarify the question.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6474, hit@10 of 0.8000, and recall@100 of 0.8143 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Duplicate questions often repeat key words, entities, or constructions, and exact overlap can identify many pairs.

The remaining gap shows why paraphrase modeling is still necessary. BM25 can over-rank questions that share wording but differ in intent, and it can miss duplicates that use alternative phrasing. Its recall@100 is good but not complete, so lexical matching alone is not enough for reliable duplicate-question retrieval.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8274, hit@10 of 0.9600, and recall@100 of 0.9857. Dense retrieval is the strongest profile on this task. The large gain over BM25 indicates that embedding similarity is well aligned with Swedish translated duplicate-question matching.

The short and symmetric structure helps dense retrieval: both query and candidate are questions, and the main signal is intent equivalence. Dense embeddings can connect paraphrases such as a direct wording and a more expanded formulation, while avoiding some lexical traps. Remaining errors are likely to involve subtle scope changes, opinion framing, or questions that are topically close but not duplicates.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7341, hit@10 of 0.8600, and recall@100 of 0.9857. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. Its recall@100 matches dense retrieval, but dense retrieval is stronger on top-10 ranking and hit@10.

This indicates that the hybrid pool preserves the broad candidate coverage of dense retrieval while adding lexical evidence. However, the first-stage ordering is less aligned with duplicate intent than dense similarity alone. For NanoQuoraRetrieval-sv, hybrid search is useful as a candidate source, but dense retrieval is the best direct ranker among these profiles.

### Metric Interpretation for Model Researchers

Because most queries have one positive, nDCG@10 and hit@10 are direct measures of whether the duplicate question appears in a useful position. recall@100 measures candidate-pool completeness for later reranking. The dense and reranking_hybrid runs share the same recall@100, so their main difference is top-rank ordering.

The task clearly separates lexical overlap from semantic equivalence. BM25 is already strong because many duplicates are lexically similar. Dense retrieval is much stronger because it better captures paraphrase and intent. reranking_hybrid does not improve over dense at the top ranks, suggesting that lexical evidence must be handled carefully in duplicate-question ranking.

### Query and Relevance Type Tendencies

Queries ask ordinary user questions such as whether it is acceptable to laugh at one's own jokes, the best lie someone has told, why Quora suggests critical answers about Donald Trump, how to become stronger, or how a quantum satellite works. Relevant documents are duplicate or near-duplicate questions, not explanatory answers.

The task rewards models that preserve question type and intent. Two questions may be relevant even if one is more concise and the other more explicit. Conversely, two questions may share many words but differ in stance, target, or requested information. This makes fine-grained sentence-level meaning central.

### Representative Failure Modes

Likely failures include ranking same-topic non-duplicates too high, missing paraphrases that use different Swedish wording, confusing broad and narrow versions of a question, and treating subjective or politically framed questions as duplicates when the intent differs. BM25 may overvalue repeated words, while dense models may overgeneralize semantic similarity.

### Training Data That May Help

Useful training data includes Swedish paraphrase pairs, multilingual duplicate-question data, question rewrite datasets, and hard negatives that share words or entities but ask a different question. For rerankers, near-duplicate non-equivalent questions are particularly valuable because they directly target the main ambiguity in this task.

### Model Improvement Notes

A model targeting this task should improve intent-level discrimination for short questions. Dense retrieval is the strongest baseline, so improvements should focus on hard negatives, scope sensitivity, and paraphrase alignment. Sparse systems remain useful for exact duplicate candidates, but final ranking should not rely primarily on word overlap. Hybrid systems need weighting or reranking that preserves semantic duplicate status over lexical similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Är det okej att skratta åt sina egna skämt? [43 chars] | Är det konstigt att skratta åt sina egna skämt? [47 chars] |
| Vad är den bästa lögn du någonsin har berättat? [47 chars] | Vilken är den mest genomtänkta lögn du någonsin har berättat? [61 chars] |
| Varför föreslår Quora ofta svar i min flödesmatning som kritiserar Donald Trump? [80 chars] | Varför verkar Quora bara ha partiska och subjektiva svar på frågor om Donald Trump? [83 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive question snippets:

| Query | Positive question |
| --- | --- |
| Är det okej att skratta åt sina egna skämt? | Är det konstigt att skratta åt sina egna skämt? |
| Vad är den bästa lögn du någonsin har berättat? | Vilken är den mest genomtänkta lögn du någonsin har berättat? |
| Varför föreslår Quora ofta svar i min flödesmatning som kritiserar Donald Trump? | Varför verkar Quora bara ha partiska och subjektiva svar på frågor om Donald Trump? |
| Hur kan jag bli starkare? | Hur blir jag starkare fysiskt? |
| Hur fungerar en kvantsatellit? | Hur fungerar en kvantumsatellit och vad skulle några av dess huvudanvändningar vara? |
