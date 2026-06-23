# NanoMTEB-Spanish / spanish_passage_s2_s

## Overview

`spanish_passage_s2_s` is the passage-level version of the Spanish Passage Retrieval health dataset. The same Spanish consumer-health questions are used as queries, but the documents are concise answer-bearing passages rather than full web pages. This makes the task closer to direct answer-passage retrieval for Spanish health information needs about baby care, vaccination, breastfeeding, emergencies, and low back pain.

The Nano split contains 167 queries, 250 passage documents, and 1,228 positive relevance judgments. Queries average about 68 characters, while passages average about 442 characters. Almost every query is multi-positive: 165 of 167 queries have more than one relevant passage, with an average of 7.35 positives and a maximum of 20. Compared with S2P, this variant removes much of the full-page noise and asks the model to rank short passages that explicitly answer the question.

## Details

### What the Original Data Measures

The Spanish Passage Retrieval collection provides manually assessed passage-level relevance for Spanish health questions. The S2S variant uses those passages as the retrieval units. This means the positive document should directly answer the user's information need, rather than merely contain an answer somewhere inside a longer page.

The task is still multi-positive. Several passages can answer the same question, sometimes with different wording, levels of detail, or source pages. A good retriever should recover multiple valid answer passages.

### Observed Data Profile

The passages are short health explanations written for lay readers. Examples discuss the benefits of breastfeeding, when to introduce complementary foods, how frequently a newborn should feed, which vaccines are publicly financed, and how vaccines prevent infectious disease. Other passages cover lumbago, back injury causes, pediatric checkups, and newborn weight.

Because the corpus is small and answer-focused, exact answer terms are more concentrated than in S2P. At the same time, paraphrase still matters: `darle el pecho`, `amamantar`, `lactancia materna`, and related expressions may refer to the same need.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5458, hit@10 of 0.9401, and recall@100 of 0.9438. The lexical baseline is strong because passages are short and often contain the key health terms from the query. With less long-document noise, BM25 can match question terms to answer passages more reliably than in full-page retrieval.

The remaining limitation is paraphrase and consumer-medical style mismatch. A user may ask in everyday language, while the passage uses a more formal phrase. BM25 can also over-rank passages that share a topic term but answer a different subquestion.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest for top-10 ranking, with nDCG@10 of 0.6398, hit@10 of 0.9701, and recall@100 of 0.9902. Dense retrieval benefits from the shorter answer-passage unit: the embedding can focus on the actual answer rather than a full web page with mixed content.

This profile shows that semantic matching is valuable in Spanish health QA. Dense retrieval can connect layperson questions with concise answer passages even when wording differs. It also preserves nearly all positives within the top 100.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.6333, hit@10 of 0.9701, and recall@100 of 0.9919. Candidate lists contain exactly 100 items with no safeguard rows. Hybrid retrieval is essentially tied with dense at hit@10, slightly below dense in nDCG@10, and slightly above dense in recall@100.

This makes S2S a balanced dense/hybrid task. Dense is marginally better for final top ordering, while hybrid is marginally better for preserving positives. Because the corpus is small and answer-focused, both semantic and lexical signals work well.

### Metric Interpretation for Model Researchers

This split is dense-favorable for nDCG@10 and hybrid-favorable by a very small margin for recall@100. BM25 is strong but clearly behind the semantic profiles. The contrast with S2P is important: when the retrieval unit is the answer passage rather than the full page, dense retrieval becomes much more effective.

The task has many positives per query, so top-10 ranking should be interpreted as ranking a set of valid passages. Hit@10 is high for all methods, but nDCG@10 reveals whether the better passages are ranked earlier and whether several positives appear near the top.

### Query and Relevance Type Tendencies

Representative queries ask about breast milk benefits, the timing of complementary foods, breastfeeding frequency, free vaccines, and vaccination for infectious disease prevention. Relevant passages directly answer the question in one or a few paragraphs. Many are written in educational or public-health language.

The model should understand both medical vocabulary and layperson phrasing. It should also retrieve multiple passages when the same question has several valid explanatory answers.

### Representative Failure Modes

BM25 may miss paraphrased answer passages or retrieve a passage from the same health topic that answers a different question. Dense retrieval may retrieve a semantically related health passage that is not specific enough. Hybrid retrieval can include both lexical and semantic near misses, although the small corpus limits the damage.

Another failure mode is under-ranking secondary positives. Since many queries have more than five positives, a model may retrieve one excellent passage but miss other valid answers that use different wording or focus on a different detail.

### Training Data That May Help

Useful training data includes Spanish medical FAQ passage retrieval pairs, consumer-health question-answer sentence pairs, multi-positive Spanish health retrieval examples, and paraphrase-rich data about baby care, vaccination, and low back pain. Training should exclude PRES evaluation questions, qrels, and overlapping passage text.

Hard negatives should be passages from the same health topic that answer a different subquestion. These are essential for teaching the model to distinguish broad topical relevance from direct answer relevance.

### Model Improvement Notes

Dense models can improve by focusing on Spanish health paraphrases, layperson-to-medical wording, and multi-positive passage ranking. Sparse systems benefit from the short passage unit but need synonym and morphology handling to close the gap. Hybrid systems are robust for candidate preservation, while dense retrieval is slightly better for final top ordering.

For downstream use, S2S is a good benchmark for answer-passage retrieval in consumer health. The best models should retrieve concise, directly useful passages rather than broad health pages.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Cuáles son los beneficios de la leche materna? [47 chars] | En la misma se reconoce que la lactancia materna es el mejor modo de proporcionar al recién nacido los nutrientes que necesita durante los primeros meses de vida. [162 chars] |
| ¿Cuándo debo introducir alimentos complementarios aparte de la lactancia materna? [81 chars] | Durante los primeros 6 meses de vida el bebé solamente necesita tomar leche materna. Es recomendable utilizar la edad corregida para comenzar a introducir el resto de alimentos, individualizando según las necesidades. No es conveniente introducir alimentación complementaria antes de los 4 meses de edad corregida. [314 chars] |
| ¿Tendría que darle el pecho a mi bebé siempre que me lo pida? [61 chars] | Durante el primer mes de vida, su recién nacido debería alimentarse entre ocho y 12 veces al día. [97 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| ECIR paper | Original Spanish health retrieval test collection. |
| Project page | Passage-level relevance and topic description. |
| Source dataset card | Public dataset packaging. |
| MTEB task card | S2S retrieval formulation. |

### Representative Snippets

- A query asks about breast milk benefits; a relevant passage states that breastfeeding provides newborns with needed nutrients.
- A query asks when to introduce complementary foods; relevant passages discuss the first six months and corrected age for premature infants.
- A query asks whether to breastfeed on demand; a relevant passage says newborns should feed eight to twelve times daily during the first month.
- A query asks which vaccines are free; relevant passages describe publicly financed systematic vaccines.
- A query asks about vaccination for preventing infectious disease; relevant passages describe routine childhood vaccination against multiple diseases.
