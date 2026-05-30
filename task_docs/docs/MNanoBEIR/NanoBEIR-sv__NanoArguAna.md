# MNanoBEIR / NanoBEIR-sv / NanoArguAna

## Overview

NanoArguAna in the Swedish NanoBEIR slice is an argument-counterargument retrieval task derived from ArguAna. The queries and documents are Swedish translated argumentative passages, and each query has a paired relevant passage that responds to it. The benchmark measures whether a retriever can identify argumentative relation and response fit between long texts, rather than simply matching topics. It is a compact but demanding diagnostic for stance-aware and discourse-aware multilingual retrieval.

## Details

### What the Original Data Measures

ArguAna is used in BEIR as an argument retrieval benchmark where relevance depends on the relationship between an argument and a counterargument. The relevant document often discusses the same issue but takes a different position, responds to a specific premise, or challenges the reasoning in the query. This makes the task harder than retrieving a document on the same topic.

In the Swedish translated version, both queries and documents are long argumentative passages. The model must compare claims, reasons, stance, and response structure across translated text. Lexical overlap can be helpful because the paired texts often discuss the same topic, but too much reliance on overlap can retrieve same-topic distractors that do not actually answer or counter the argument.

### Observed Data Profile

The task contains 50 queries, 3,635 documents, and 50 relevance judgments. Every query has exactly one positive document: the average, minimum, median, and maximum positives per query are all 1.0, and there are no multi-positive queries. This makes the benchmark a precise single-target retrieval task.

The text units are long. Queries average 1,096.22 characters, and documents average 1,006.23 characters. Unlike short-query passage retrieval, both sides contain substantial argumentative context. A strong model must use the whole passage structure, not just a few shared topic words.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3185, hit@10 of 0.5600, and recall@100 of 0.8600 using the top-500 BM25 candidate subset. This profile shows that lexical overlap is useful for candidate generation: the relevant counterargument is usually somewhere in the first 100 ranks. However, BM25 is much weaker at placing the paired response in the top 10.

The gap between recall@100 and top-10 quality reflects the nature of ArguAna. Many distractors may share the same topic vocabulary, especially in long debate passages. BM25 can locate the debate area, but it does not model stance, rebuttal structure, or whether the passage responds to the query's specific claim.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4108, hit@10 of 0.7600, and recall@100 of 0.9400. Dense retrieval is clearly stronger than BM25 in top-rank quality and candidate coverage. This indicates that embedding similarity captures response fit and argumentative relatedness better than exact term matching alone.

The dense advantage is important because the task is long-text and discourse-heavy. The relevant passage may not be the document with the most repeated words; it may be the one that challenges the premise or addresses the same argument from the opposite side. Dense retrieval appears better aligned with this kind of semantic and pragmatic relation, though the single-positive format still leaves little room for partial credit when a near miss is ranked high.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3784, hit@10 of 0.7200, and recall@100 of 0.9600. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 2 safeguard rows and a mean of 100.04 candidates. The hybrid pool has the best recall@100, while dense retrieval has the best top-10 ranking.

This means hybrid search improves coverage by combining lexical and dense evidence, but its first-stage ordering is not as strong as dense retrieval alone. For Swedish ArguAna, the relevant document is often present in the hybrid candidate pool, making it useful for reranking. The top rank, however, benefits from the denser semantic signal that better reflects argument-response relation.

### Metric Interpretation for Model Researchers

Because there is exactly one positive per query, hit@10 and nDCG@10 are closely tied to whether the model places the paired response in a usable position. recall@100 is a candidate-generation measure: it tells whether a later reranker has a chance to recover the positive. A model can have high recall@100 and still feel poor in direct search if many same-topic distractors appear above the true response.

The pattern across methods is instructive. BM25 is a useful lexical candidate generator but weak at response ranking. Dense retrieval is strongest for immediate ranking quality. reranking_hybrid provides the broadest candidate coverage. This makes the task valuable for evaluating whether a system's second stage can exploit a high-recall candidate set.

### Query and Relevance Type Tendencies

Queries are long arguments about topics such as public indifference to reform, Heathrow expansion, choice overload and happiness, cyberattacks by non-state actors, and the tension between religion, hate speech, and free expression. Positives are response passages that often challenge, qualify, or counter the original argument.

The task therefore requires more than topic detection. A relevant passage may share the same policy issue but differ in stance or address a specific premise. Models need to capture claim structure, argument target, and discourse relation. Long translated Swedish passages also create opportunities for retrieval systems to over-focus on repeated nouns while ignoring the argumentative role of the text.

### Representative Failure Modes

Likely failures include retrieving a passage on the same debate topic that does not answer the query, confusing supportive and counterargument relations, overvaluing repeated policy vocabulary, and missing the paired response when it uses different framing. Dense models may sometimes retrieve semantically close but stance-mismatched passages, while BM25 may rank long same-topic distractors above the true counterargument.

### Training Data That May Help

Useful training data includes argument-counterargument pairs, stance-aware retrieval data, debate passage ranking, multilingual argument mining, and hard negatives from the same topic with different stance or response targets. Swedish argumentative data can help with discourse markers and translation-specific phrasing. For rerankers, the most useful negatives are passages that are topically close but fail to respond to the query's specific claim.

### Model Improvement Notes

A model targeting this task should improve response-relation modeling for long argumentative text. Dense retrievers are the best starting point, but they need hard-negative training against same-topic non-responses. Sparse systems need more than token overlap, possibly using stance-aware expansion or passage segmentation. Hybrid systems should use their strong recall as a candidate source, then rely on a reranker that can compare claim, stance, and counterargument structure.

## Example Data

### Public Sources

The original task is based on ArguAna argument retrieval, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [ArguAna](https://aclanthology.org/P18-1023/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive response snippets:

| Query | Positive document snippet |
| --- | --- |
| Allmänheten är likgiltig inför reformer. Om reform av Overhuset bör vara en högsta prioritet... | AV-kampanjen kan inte jämföras med reformer av överhuset. Man bör inte förväxla en missinformerad allmänhet... |
| Utbyggnaden av Heathrow är avgörande för ekonomin. En utbyggnad av Heathrow skulle säkra många befintliga jobb... | Affärsvärlden är långt ifrån enad i sitt påstådda stöd för en tredje start- och landningsbana... |
| Människor får för många valmöjligheter, vilket gör dem mindre lyckliga. | Människor är missnöjda för att de inte kan ha allt, inte för att de får för många val... |
| Cyberattacker utförs ofta av icke-statliga aktörer, såsom cyberterrorister eller hacktivister... | Vid attacker från icke-statliga aktörer är det en allmän uppfattning bland praktiker inom internationell rätt... |
| Eftersom religion främjar säkerhet i tro, är gudomligt inspirerad hat lätt att använda för att rättfärdiga... | Ingen tvingas utföra våldshandlingar på grund av andras ord; det är deras eget val... |
