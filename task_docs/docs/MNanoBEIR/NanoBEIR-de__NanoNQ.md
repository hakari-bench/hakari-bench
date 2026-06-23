# MNanoBEIR / NanoBEIR-de / NanoNQ

## Overview

This task is the German NanoBEIR version of Natural Questions, an open-domain question answering benchmark built from real Google search questions and Wikipedia answer evidence. The original Natural Questions dataset pairs natural user queries with Wikipedia pages and annotated answer regions, making it a test of answer evidence retrieval rather than only keyword lookup. In this NanoBEIR slice, German translated questions must retrieve German translated Wikipedia passages that contain the answer. The task contains 50 queries, 5,035 documents, and 57 positive relevance judgments. Most queries have one positive passage, while seven queries have two positives. The benchmark is useful for measuring whether a retrieval model can connect naturally phrased German questions to answer-bearing encyclopedic passages, especially when the passage does not repeat the question wording exactly.

## Details

### What the Original Data Measures

Natural Questions measures open-domain QA over Wikipedia using questions that reflect real search behavior. Queries ask who, where, when, how many, why, or title-specific questions, and the answer evidence is usually a paragraph, list, table region, or other Wikipedia content span. In a retrieval benchmark, the core question is whether the answer-containing passage appears early enough for a reader, reranker, or extractive QA model to use. The task therefore rewards both entity grounding and semantic answerability.

### Observed Data Profile

The German Nano task has 50 queries, 5,035 documents, and 57 positives. Positives per query average 1.14, with a maximum of two. Average query length is about 55 characters, and average document length is about 589 characters. The inspected examples include questions about sports tournaments, Disney films, public art, constitutional clauses, and music performers. The documents are Wikipedia-style answer passages: some are short and direct, while others provide context around the answer entity or event.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.376, Hit@10 of 0.560, and Recall@100 of 0.877. The high Recall@100 compared with Hit@10 suggests that lexical retrieval often finds the answer passage somewhere in the candidate set but does not consistently rank it in the first page. BM25 is effective when the query contains a distinctive title, named entity, or phrase repeated in the passage. It is weaker when the question uses a natural wording that must be matched to answer context, such as a paraphrased reason, a location description, or a role relation.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline performs best by nDCG@10, with 0.527, Hit@10 of 0.660, and Recall@100 of 0.895. This shows that semantic question-to-answer matching is central for German NQ. Dense retrieval can connect a question to a passage that contains the answer even if the passage is not written in question form. It is especially useful for why, role, and definition-style questions where the answer relation is expressed in explanatory prose. Dense recall is only slightly above BM25, but its top-10 ordering is much stronger.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.449, Hit@10 of 0.680, and Recall@100 of 0.930, with four safeguard rows at 101 candidates. It gives the strongest Hit@10 and Recall@100, but trails dense retrieval on nDCG@10. This pattern indicates that hybrid search improves candidate coverage and first-page inclusion, while dense ranking alone may place the positive passage higher once found. For this task, hybrid search is valuable when exact entity terms and semantic answerability both matter, but the final ordering still needs careful calibration.

### Metric Interpretation for Model Researchers

Because most queries have one positive, Hit@10 and Recall@100 are informative and easy to interpret. nDCG@10 remains the better signal for top-rank quality, especially when comparing dense and hybrid profiles: hybrid retrieves more positives into the top 100, while dense places positives higher in the top 10. A model that improves Recall@100 but lowers nDCG@10 may help reranking pipelines but may not improve direct retrieval user experience.

### Query and Relevance Type Tendencies

Queries are natural questions rather than keyword-only prompts. They often mention a named entity and ask for a property, role, location, date, reason, performer, or constitutional detail. Relevant passages are answer-bearing Wikipedia text and may include the answer in a larger contextual paragraph. The task therefore requires recognizing not only the query entity but also the requested relation.

### Representative Failure Modes

BM25 can retrieve pages that share entity names but do not contain the requested answer. Dense retrieval can over-rank passages that are semantically related to the query topic but lack the precise answer span. Hybrid retrieval can find more answer-bearing passages but may still mix in strong lexical distractors. Errors should be inspected by asking whether the candidate passage actually answers the question, not merely whether it is about the same topic.

### Training and Leakage Considerations

Natural Questions is a common training source, so overlap control is important. Training should exclude Natural Questions, BEIR, NanoBEIR, and translated Wikipedia QA records likely to overlap with these evaluation questions or passages. Useful non-overlapping supervision includes German or multilingual Wikipedia QA retrieval pairs, open-domain evidence retrieval data, and real-question-to-passage datasets. Synthetic data should generate natural German questions whose answers are explicitly present in non-evaluation Wikipedia-style passages.

### Model Improvement Signals

Strong models should improve semantic answerability without losing entity precision. Useful training signals include hard negatives from the same Wikipedia entity, paraphrased question forms, and answer-bearing passages where the target fact is embedded in surrounding context. For hybrid systems, the main opportunity is to combine BM25's entity recall with dense ranking's answer-relation sensitivity.

## Example Data

| Query | Positive document |
| --- | --- |
| Wo findet dieses Jahr die Final Four statt? [43 chars] | Das NCAA Division I Men's Basketball Tournament 2018 war ein 68-Team-K.-o.-Turnier, um den nationalen Meister im Basketball der NCAA Division I für die Saison 2017/18 zu ermitteln. Die 80. Auflage des Turniers begann am 13. März 2018 und endete mit dem Finale am 2. April im Alamodome in San Antonio, Texas. [307 chars] |
| War "Die Nacht vor Weihnachten" ursprünglich ein Disney-Film? [61 chars] | Die Idee zu "The Nightmare Before Christmas" entstand 1982 in einem Gedicht, das Tim Burton schrieb, während er als Animator bei Walt Disney Feature Animation arbeitete. Nach dem Erfolg von "Vincent" im selben Jahr begann Walt Disney Studios, die Entwicklung von "The Nightmare Before Christmas" als Kurzfilm oder 30-minütige Fernsehsendung in Betracht zu ziehen. Im Laufe der Jahre kehrte Burton immer wieder zu diesem Projekt zurück, und 1990 schloss er einen Entwicklungsvertrag mit Disney ab. Die Produktion begann im Juli 1991 in San Francisco; Disney veröffentlichte den Film unter seinem Touchstone Pictures-Label, da das Studio der Meinung war, der Film sei "zu dunkel und gruselig für Kinder".[4] [705 chars] |
| Warum steht der Engel des Nordens in Gateshead? [47 chars] | Laut Gormley hatte die Bedeutung des Engels eine dreifache Bedeutung: Erstens, um darauf hinzuweisen, dass unter der Baustelle über zwei Jahrhunderte hinweg Bergleute arbeiteten; zweitens, um den Übergang von der Industrie- zur Informationsgesellschaft zu erfassen; und drittens, um als Brennpunkt für unsere sich wandelnden Hoffnungen und Ängste zu dienen. [357 chars] |

## Public Sources

- [Natural Questions paper](https://aclanthology.org/Q19-1026/)
- [Natural Questions dataset page](https://ai.google.com/research/NaturalQuestions)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Natural Questions paper (https://aclanthology.org/Q19-1026/) |
| Natural Questions dataset page (https://ai.google.com/research/NaturalQuestions) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
