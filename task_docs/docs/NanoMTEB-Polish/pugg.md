# NanoMTEB-Polish / pugg

## Overview

`pugg` is the Polish NanoMTEB version of the PUGG information-retrieval task. PUGG was developed as a Polish dataset for knowledge-base question answering, machine reading comprehension, and information retrieval. In this IR split, each short natural Polish question is paired with one Wikipedia-derived passage that contains the answer. The task is therefore a compact Polish open-domain QA retrieval benchmark, not a translated English dataset.

The Nano split contains 200 queries, 10,000 documents, and exactly 200 positive relevance judgments. Each query has one positive passage. Queries are short, averaging about 36 characters, while documents average about 850 characters. The observed questions involve Polish literature, historical declarations, biblical concepts, fictional characters, physical traits, definitions, borders, sports, and popular culture. This makes the task a precise test of whether a model can map a short Polish factoid question to an answer-bearing encyclopedic passage.

## Details

### What the Original Data Measures

The PUGG paper introduces a modern Polish dataset construction pipeline for KBQA, MRC, and IR. The IR view uses natural questions and Wikipedia-derived passages segmented into shorter windows. Relevance means that the document contains the answer to the question, not that it is merely topically related.

This setup differs from duplicate-question retrieval. A relevant passage may not repeat the question wording; it must include the answer entity, relation, definition, event, or fact. The task is also Polish-native in topic and language, which makes it useful for evaluating retrieval over Polish encyclopedic content.

### Observed Data Profile

The queries are short and often entity- or relation-focused. Documents are longer Wikipedia-like passages with descriptive context. Because each query has exactly one positive, ranking precision is critical. If the answer-bearing passage is not near the top, there is no second positive to compensate.

The examples include questions such as who wrote `Balladyna`, what was promised to Poles in the Act of 5 November, what lessons come from the biblical creation story, whom Tadeusz became engaged to, and what percentage of people have blond hair. Many queries contain strong lexical clues, but the model still has to retrieve the passage that states the answer.

### BM25 Evaluation Profile

BM25 is strong on this split, with nDCG@10 of 0.6390, hit@10 of 0.7950, and recall@100 of 0.8750. Short Polish factoid questions often share names or key nouns with the correct Wikipedia passage. Lexical overlap on titles, people, works, and historical terms gives BM25 a high baseline.

However, BM25 is not sufficient. Some questions are phrased through relations or definitions rather than exact passage titles. A question may ask for an author, a promise, a family relation, or a percentage, while the relevant passage contains the answer in surrounding prose. Exact matching can retrieve related pages but miss the answer-bearing one.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest at top ranks, with nDCG@10 of 0.7817, hit@10 of 0.8850, and recall@100 of 0.9300. Dense retrieval improves over BM25 by connecting question intent to answer passages even when the wording is not identical. It can better represent the relation between the question and the fact expressed in the passage.

This strong dense profile reflects the open-domain QA nature of PUGG. The model must match "who wrote", "what was promised", or "how many" to passages that contain the corresponding answer. Embedding similarity is better than term frequency at recognizing these question-to-evidence relations.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.7146, hit@10 of 0.8300, and recall@100 of 0.9800. Candidate lists contain 100 to 101 items, and only 4 rows use the positive safeguard. Hybrid retrieval has the best recall@100 but lower top-10 quality than dense retrieval.

This means hybrid search is excellent for candidate generation in PUGG. It almost always preserves the single positive somewhere in the top 100. But the final top ordering is less accurate than dense retrieval, likely because lexical candidates can include related Wikipedia passages that share terms without answering the question.

### Metric Interpretation for Model Researchers

This split is dense-favorable for direct ranking and hybrid-favorable for recall. BM25 is unusually strong because the questions are short and entity-rich, but dense retrieval still improves substantially. Hybrid retrieval should be considered when the output feeds a reranker or reader model that can select the answer-bearing passage from a broad candidate pool.

Because every query has exactly one positive, metrics are easy to interpret. Hit@10 indicates whether the answer passage is visible in the first page, nDCG@10 rewards higher placement, and recall@100 measures first-stage preservation. There is no multi-positive ambiguity.

### Query and Relevance Type Tendencies

Representative queries ask who wrote `Balladyna`, what the Act of 5 November promised Poles, what lessons follow from the biblical creation story, whom Tadeusz became engaged to, and what percentage of people have blond hair. The answer-bearing passages are descriptive and encyclopedic.

The task tends to reward models that identify the expected answer type. A "who" question should retrieve a passage with a person; a "what was promised" question should retrieve a historical statement; a "what percentage" question should retrieve a numeric fact.

### Representative Failure Modes

BM25 may retrieve a related page that shares an entity but lacks the requested answer. Dense retrieval may retrieve a semantically related encyclopedic passage that discusses the topic but not the specific fact. Hybrid retrieval can include both, improving recall but requiring a reranker to place the answer passage first.

Another failure mode is relation confusion. A model may find a passage about Tadeusz or `Balladyna` but miss the specific relation being asked, such as engagement or authorship. Correct retrieval requires matching the question relation, not only the entity.

### Training Data That May Help

Useful training data includes non-overlapping PUGG training records, Polish Wikipedia QA retrieval pairs, Polish KBQA and MRC data, and hard negatives from related Wikipedia entities. Synthetic or mined examples should keep the answer passage explicit and pair it with related non-answer passages.

Hard negatives are important: pages about the same work, person, event, or category that do not answer the query help teach the model to retrieve evidence rather than topic matches.

### Model Improvement Notes

Dense models can improve by representing Polish question focus, answer type, and encyclopedic evidence. Sparse systems can improve through entity normalization and Polish morphology handling, but dense retrieval is already the stronger direct ranking baseline. Hybrid systems are valuable when high recall is needed before reranking.

For downstream QA systems, this split is useful because the retrieved passage must support an answer. Retrieval improvements should be judged by whether the answer-bearing document appears high enough for a reader or reranker to use.

## Example Data

### Public Sources

- PUGG paper: https://aclanthology.org/2024.findings-acl.652/
- Source dataset card: https://huggingface.co/datasets/clarin-pl/PUGG_IR
- PUGG repository: https://github.com/CLARIN-PL/PUGG

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| PUGG paper | Original Polish KBQA, MRC, and IR dataset description. |
| PUGG dataset card | Source IR dataset packaging. |
| PUGG repository | Implementation and dataset-construction context. |

### Representative Snippets

- A query asks who wrote `Balladyna`; the relevant passage states that it was written by Juliusz Slowacki.
- A query asks what Poles were promised in the Act of 5 November; the relevant passage describes the promise of a Polish kingdom.
- A query asks what lessons come from the biblical creation story; the relevant passage explains the creation-world concept.
- A query asks whom Tadeusz became engaged to; the relevant passage describes Tadeusz Soplica and his relation to Zosia.
- A query asks what percentage of people have blond hair; the relevant passage describes blond hair and prevalence.
