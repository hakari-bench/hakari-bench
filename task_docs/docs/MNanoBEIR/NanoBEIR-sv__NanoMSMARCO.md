# MNanoBEIR / NanoBEIR-sv / NanoMSMARCO

## Overview

NanoMSMARCO in the Swedish NanoBEIR slice is a web passage retrieval task derived from MS MARCO. The queries are Swedish translated web-search questions, and the corpus contains Swedish translated answer-bearing passages. The task measures whether a retriever can connect short natural-language search queries to passages that answer them. It is a compact diagnostic for practical QA-style passage search, where wording is brief, intent may be underspecified, and the relevant passage must provide the answer rather than merely mention the topic.

## Details

### What the Original Data Measures

MS MARCO was built from real user queries and human-generated answers, making it a central benchmark for passage retrieval. In retrieval form, the model receives a short web query and must find the passage that contains the answer. The relevant passage may include definitions, explanations, names, or short factual statements.

The Swedish translated version tests multilingual web-search behavior. Queries are short and often informal, while passages are more complete and explanatory. Some entities and song titles remain in English, while the surrounding question and passage text are Swedish. A strong model must preserve exact lexical clues while also matching answer intent.

### Observed Data Profile

The task contains 50 queries, 5,043 documents, and 50 relevance judgments. Every query has exactly one positive passage, with no multi-positive queries. This makes the benchmark a strict single-answer retrieval task: ranking the one answer-bearing passage high is the central objective.

Queries average 33.60 characters, while documents average 321.19 characters. The queries are very short, often just a few words, and the passages are concise but substantially longer. This makes the task sensitive to query understanding. A single ambiguous term or named entity can determine which passage is relevant.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3777, hit@10 of 0.5400, and recall@100 of 0.7200 using the top-500 BM25 candidate subset. This indicates that lexical matching is helpful but far from sufficient. Short web questions often contain distinctive terms, but answer passages may phrase the answer differently or include context that reduces exact overlap.

BM25 is most likely to succeed on definition queries or named-entity questions where the relevant passage repeats the key term. It is weaker when the query is conversational, underspecified, or uses wording different from the answer passage. The recall@100 value shows that lexical retrieval often finds the answer candidate, but not reliably enough for a strong reranking pipeline.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4559, hit@10 of 0.6400, and recall@100 of 0.8800. Dense retrieval improves every metric over BM25. This is the expected pattern for web QA passage retrieval, where embedding similarity can connect a question to an answer-bearing passage even when the wording differs.

The dense advantage is especially strong in recall@100. It provides a much better candidate set for downstream reranking than BM25. Remaining errors likely involve ambiguity, uncommon entities, translated phrasing, or passages whose answer is only a small portion of the text. Dense similarity can still retrieve topically related passages that do not actually answer the question.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4737, hit@10 of 0.6200, and recall@100 of 0.8800. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 6 safeguard rows and a mean of 100.12 candidates. Its recall@100 matches dense retrieval, and its nDCG@10 is slightly higher, while dense has the stronger hit@10.

This suggests that hybrid search helps refine top-rank ordering for some queries by adding lexical anchors to the dense candidate signal. However, it does not increase recall beyond dense retrieval and slightly reduces hit@10. For NanoMSMARCO-sv, the hybrid pool is competitive, but dense retrieval remains the cleaner candidate generator by recall and hit rate.

### Metric Interpretation for Model Researchers

Because every query has one positive, nDCG@10 and hit@10 mostly measure whether that one answer passage appears high enough to be useful. recall@100 measures whether a later reranker has access to the answer. The method comparison shows that semantic retrieval is important: BM25 misses too many answers, while dense and reranking_hybrid recover many more.

The difference between dense and reranking_hybrid is subtle. Dense has the better hit@10, while hybrid has the better nDCG@10 with the same recall@100. This suggests that hybrid search can improve rank placement when it succeeds, but may also introduce lexical distractors for some queries. The task is useful for testing answer-intent matching in short Swedish web queries.

### Query and Relevance Type Tendencies

Queries include definitions, song or media questions, actor-role questions, geography questions, and meaning questions, such as "Vad är ruminationssyndrom?", "Vem sjöng här kommer vi igen", "Vem spelar Cameron Boyce i Liv och Maddie?", "Var förekommer jordens största öknar?", and "Vad betyder snutte?" Relevant passages are short answer-bearing texts, often with definitions or direct factual statements.

The task rewards models that infer what kind of answer is requested. "What is" queries need definitions, "who" queries need people, and "where" queries need locations. A passage can share the key term and still be wrong if it does not answer the expected question type.

### Representative Failure Modes

Likely failures include retrieving a passage that mentions the query term but lacks the answer, confusing similarly named songs or shows, missing answers when the passage uses a different wording, and over-ranking broad background passages. BM25 is vulnerable to vocabulary mismatch, while dense models may retrieve semantically related but non-answer passages. Hybrid systems must control lexical distractors introduced by short queries.

### Training Data That May Help

Useful training data includes Swedish web QA, multilingual passage retrieval, short-query answer retrieval, query-log style data, and hard negatives that share query terms but do not answer the question. Translated MS MARCO-like data can help if it does not overlap evaluation records. For rerankers, answer-type negatives are important: same topic, wrong answer form.

### Model Improvement Notes

A model targeting this task should improve short-query intent matching and answer-bearing passage discrimination. Sparse systems need query expansion and normalization for Swedish terms and translated entities. Dense systems need hard-negative training against topical non-answers. Hybrid systems can improve some top-rank placements, but should be tuned so exact overlap does not overpower answer intent.

## Example Data

| Query | Positive document |
| --- | --- |
| Vad är ruminationssyndrom? [26 chars] | Ruminationssyndrom. Ruminationssyndrom, även kallat merycism, är en ätstörning som inte passar in i andra kategorier och leder till att mat kastas upp. Även om det inte identifieras som en specifik ätstörning i DSM-IV, har vissa parametrar utarbetats för att diagnostisera störningen. [284 chars] |
| Vem sjöng här kommer vi igen [28 chars] | För andra användningar, se Here I Go Again (upplösning). Here I Go Again är en låt av det brittiska rockbandet Whitesnake. Låten släpptes ursprungligen på albumet Saints & Sinners från 1982 och spelades in på nytt för deras självbetitlade album Whitesnake från 1987. Låten spelades in på nytt samma år i en ny radiomix-version. [327 chars] |
| Vem spelar Cameron Boyce i Liv och Maddie? [42 chars] | Förbered er för några riktigt roligare skratt, ni. I en EXKLUSIV förhandsvisning av avsnittet den 19 april av Liv & Maddie som heter “Prom-A-Rooney.” Självklart. I den roligaste klippet ser vi Jessie-stjärnan Cameron Boyce dyka upp i en annan Disney-serie för att träffa Maddie (Shelby Wulfert). Hans rollfigur är, eh, lite excentrisk! [335 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [MS MARCO](https://arxiv.org/abs/1611.09268) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| Vad är ruminationssyndrom? | Ruminationssyndrom, även kallat merycism, är en ätstörning som inte passar in i andra kategorier... |
| Vem sjöng här kommer vi igen | Here I Go Again är en låt av det brittiska rockbandet Whitesnake... |
| Vem spelar Cameron Boyce i Liv och Maddie? | I en exklusiv förhandsvisning av avsnittet den 19 april av Liv & Maddie... |
| Var förekommer jordens största öknar? | De flesta av jordens öknar ligger utanför de polära områdena. Den största är Saharaöknen... |
| Vad betyder snutte? | Enligt nuvarande fynd verkar det som att ordet "copper" föregår "cop"... |
