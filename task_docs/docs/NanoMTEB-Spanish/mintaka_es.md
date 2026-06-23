# NanoMTEB-Spanish / mintaka_es

## Overview

`mintaka_es` is the Spanish NanoMTEB retrieval split derived from Mintaka, a complex multilingual question-answering dataset. Mintaka contains naturally elicited complex questions with Wikidata-style answers and translations into multiple languages, including Spanish. In this retrieval adaptation, the query is a Spanish complex question and the relevant document is a very short answer string or entity name. The task is therefore closer to entity-answer selection than passage retrieval.

The Nano split contains 200 queries, 1,693 documents, and exactly 200 positive relevance judgments. Each query has one positive answer. Queries average about 67 characters, while documents average only about 14 characters. Correct documents include short names and titles such as `Marlee Matlin`, `50 Cent`, `Pirates of the Caribbean: Dead Man's Chest`, `Lo que el viento se llevó`, and `Sting`. The model must map Spanish questions to canonical answer strings, often across multilingual entity names.

## Details

### What the Original Data Measures

Mintaka was designed for end-to-end complex question answering. It includes question types such as count, comparison, superlative, intersection, and multi-hop. The original QA task asks a system to answer questions grounded in Wikidata-style entities and relations. The retrieval version instead asks a model to retrieve the answer string from a candidate set.

This conversion creates a sharp retrieval challenge. The answer document is often just a name, number, or title. It may not contain explanatory context, and it may be in English even when the question is Spanish. Relevance depends on reasoning over the question, not matching passage text.

### Observed Data Profile

The documents are extremely short. They do not explain why they answer the query. A query may ask which Twilight film is second chronologically, which Harry Potter film was directed by Alfonso Cuaron, who is younger between two actors, or which animated film from 2007 was directed by Tim Hill. The relevant document is only the answer title or person name.

Every query has one positive, so there is no multi-positive ambiguity. The ranking problem is whether the model can connect a complex Spanish question to the correct entity among many short candidate strings.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.2502, hit@10 of 0.3150, and recall@100 of 0.3500. This is expected. The correct answer often shares few or no tokens with the question. A question may mention a director, franchise, comparison, or date, while the answer string is a film title or person name.

BM25 can work when the answer shares an entity name from the query, but many Mintaka questions require relation understanding. Term frequency alone cannot infer that the third Twilight film is `The Twilight Saga: Eclipse` or that the younger person in a comparison is Reese Witherspoon.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest, with nDCG@10 of 0.3614, hit@10 of 0.5100, and recall@100 of 0.7500. Dense retrieval is better at representing the semantic relation between the Spanish question and the answer entity. It can use learned associations between films, actors, directors, franchises, and other entity attributes.

The absolute scores remain moderate because answer strings are very short and often lack context. Even dense models have little text to embed on the document side. The task therefore tests whether the model has enough entity and relation knowledge encoded in the representation.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.2721, hit@10 of 0.3300, and recall@100 of 0.6200. Candidate lists contain 100 to 101 items, and 76 rows use the positive safeguard. Hybrid recall is better than BM25 but lower than dense, and top-10 ranking remains close to BM25.

This indicates that lexical evidence does not add much final-ranking value for this task. It may help preserve some entity candidates, but dense retrieval is the better first-stage signal. A reranker trained for question-answer compatibility or entity linking would be needed to exploit the candidate pool effectively.

### Metric Interpretation for Model Researchers

This split is dense-favorable. BM25 is disadvantaged by the short answer-string format. Hybrid retrieval does not outperform dense because lexical candidates are often based on incidental entity overlap rather than the actual answer relation. The task is a useful stress test for multilingual entity-answer retrieval.

Because every query has one positive, nDCG@10 and hit@10 directly measure whether the correct answer appears near the top. Recall@100 measures whether the answer survives candidate generation. Dense retrieval's recall advantage is especially important for downstream reranking.

### Query and Relevance Type Tendencies

Representative queries ask for the second or third Twilight film in chronological order, the Harry Potter film directed by Alfonso Cuaron, the younger person between Drew Barrymore and Reese Witherspoon, or the animated film released in 2007 and directed by Tim Hill. These require franchise ordering, director-film relations, comparison, and intersection constraints.

The relevant documents are short canonical names. A model must infer the answer from the question's relation structure, not from the answer text itself.

### Representative Failure Modes

BM25 fails when the answer string does not repeat the question's words. Dense retrieval can fail by retrieving a related entity from the same franchise, actor set, or film category. Hybrid retrieval may add lexical distractors such as a mentioned actor or franchise name rather than the actual answer.

Another failure mode is relation confusion. A model may know that two entities are related but choose the wrong member of an ordered list, comparison, or multi-hop chain. Short answers give little opportunity to correct that mistake through document context.

### Training Data That May Help

Useful training data includes non-overlapping Mintaka train examples, Spanish Wikidata entity-linking QA pairs, multilingual complex question paraphrases, and hard negatives with related entity names. Training should exclude Mintaka test examples, Nano queries, qrels, and likely-overlapping answer strings.

Hard negatives should be relation-close: other films in the same franchise, other actors in the comparison, or related titles by the same director. These teach the model to resolve the exact relation, not just the topic.

### Model Improvement Notes

Dense models can improve through multilingual entity representation, relation-aware QA retrieval, and short-answer embedding. Sparse systems have limited upside unless answer strings share query terms. Hybrid systems may help recall but need a reranker that can reason over the Spanish question and the candidate entity.

For evaluation, this task is best read as answer-entity retrieval. Improvements should focus on whether the model can retrieve the right short entity string despite minimal document context.

## Example Data

| Query | Positive document |
| --- | --- |
| En orden cronológico, ¿cuál es la segunda película de Crepúsculo? [65 chars] | The Twilight Saga: New Moon [27 chars] |
| ¿Qué película de Harry Potter es dirigida por Alfonso Cuarón? [61 chars] | Harry Potter y el prisionero de Azkaban [39 chars] |
| ¿Quién es más joven, Drew Barrymore o Reese Whiterspoon? [56 chars] | Reese Witherspoon [17 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Mintaka paper | Original complex multilingual QA dataset description. |
| MTEB paper | Retrieval benchmark framing. |
| MTEB task card | Retrieval packaging of Mintaka. |

### Representative Snippets

- A query asks for the second Twilight film chronologically; the relevant answer is `The Twilight Saga: New Moon`.
- A query asks which Harry Potter film was directed by Alfonso Cuaron; the relevant answer is `Harry Potter y el prisionero de Azkaban`.
- A query asks who is younger between Drew Barrymore and Reese Witherspoon; the relevant answer is `Reese Witherspoon`.
- A query asks which 2007 animated film was directed by Tim Hill; the relevant answer is `Alvin and the Chipmunks`.
- A query asks for the third Twilight film chronologically; the relevant answer is `The Twilight Saga: Eclipse`.
