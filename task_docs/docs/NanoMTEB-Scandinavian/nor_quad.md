# NanoMTEB-Scandinavian / nor_quad

## Overview

`nor_quad` is the Norwegian NanoMTEB-Scandinavian retrieval adaptation of NorQuAD. NorQuAD was introduced as a Norwegian extractive machine-reading dataset built from Bokmal Wikipedia and news passages. In the retrieval form used here, a Norwegian question is the query and the relevant document is a concise answer string or answer-bearing snippet. This makes the task closer to answer selection than ordinary passage retrieval.

The Nano split contains 196 queries, 1,048 documents, and 291 positive relevance judgments. Queries average about 49 characters, while documents average about 214 characters. About 48.47% of queries have two positives, and no query has more than two. Many positives are short names, places, dates, quantities, or phrases, such as `I 1999`, `Bibelen`, `Romersk Britannia`, or a short description of tone. The task is difficult because the correct answer may share little lexical overlap with the full question.

## Details

### What the Original Data Measures

NorQuAD was designed for Norwegian extractive question answering. The original data asks a reader model to answer questions from a passage. The Scandinavian retrieval adaptation separates the question from possible answer strings or snippets and asks the retrieval model to rank the correct answer document.

This conversion makes relevance very different from factoid passage retrieval. The target can be a very short answer rather than a passage with repeated question context. A query like "When was the euro introduced?" should retrieve `I 1999`; a lexical model receives almost no shared terms between query and answer.

### Observed Data Profile

The corpus is compact, but the answer documents are often too short to support normal term-overlap retrieval. Nearly half the queries have two valid positives, which may reflect alternative answer strings or answer-bearing snippets. The task includes person, place, date, number, reason, and description answers.

The examples show the central challenge. Some positives are short strings, while others are longer snippets from news or Wikipedia-like text. A model must infer the answer type and map the question to a compatible answer, rather than matching question words to a passage.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.1118, hit@10 of 0.2143, and recall@100 of 0.2131. This is expected for short-answer retrieval. A correct answer such as `I 1999` or `Romersk Britannia` may not repeat any words from the question. Term frequency gives little signal unless the answer string contains an entity from the query.

This split is therefore one of the least favorable settings for pure lexical retrieval. BM25 can retrieve some positives when names or topic words overlap, but many queries require semantic answer-type matching.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is the strongest profile, with nDCG@10 of 0.2378, hit@10 of 0.3724, and recall@100 of 0.4536. These scores are still modest, but the gain over BM25 is large. Dense retrieval is better at mapping a question to a concise answer because it can use semantic compatibility and answer type.

The task remains hard for dense retrieval because the answer documents may be extremely short. A standalone answer string has little context for an embedding model to represent. Dense models must infer that a year, person, place, or phrase answers the question from minimal text.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.1301, hit@10 of 0.2296, and recall@100 of 0.4261. Candidate lists contain 100 to 101 items, and 89 rows use the positive safeguard. Hybrid recall is close to dense recall, but top-10 ranking remains much lower than dense.

This result shows that adding lexical candidates does not help the final ranking much in short-answer retrieval. The hybrid pool can preserve many positives for reranking diagnostics, but the ranking still needs a model that understands question-answer compatibility. A reranker trained for answer selection would likely be more useful than lexical fusion alone.

### Metric Interpretation for Model Researchers

This split is dense-favorable, but it is difficult for all first-stage methods. BM25's poor performance highlights how little term overlap exists between questions and concise answers. Dense retrieval roughly doubles BM25's top-rank quality, yet absolute scores remain low.

Researchers should treat `nor_quad` as an answer-selection stress test. It does not primarily measure passage retrieval or duplicate-question matching. It measures whether a model can connect a full Norwegian question to a short answer text. Recall@100 also matters because many positives need to be kept for a downstream reranker.

### Query and Relevance Type Tendencies

Representative queries ask when the euro was introduced, which book most Britons lie about reading, which Eastern European country first got a non-communist prime minister, what Romans called the province made from today's England and Wales, and what Botnan's tone was after a race. Relevant answers can be years, titles, historical names, countries, or short descriptive phrases.

The key signal is answer type. The query often implies the kind of document that should be retrieved: a date, title, place, person, quantity, or phrase. A good model must represent this compatibility even when lexical overlap is absent.

### Representative Failure Modes

BM25 fails when the answer string contains none of the question's words. Dense retrieval can fail by retrieving a semantically plausible answer of the wrong type or a related snippet that does not answer the question. Hybrid retrieval may include the answer somewhere in the candidate set but still rank lexical distractors above it.

Another failure mode is ambiguity among same-type answers. If many candidate documents are dates, names, or short place names, a model must use fine-grained semantic context to choose the right one. Short answer strings provide little disambiguating evidence.

### Training Data That May Help

Useful training data includes non-overlapping NorQuAD training question-answer pairs, Norwegian Wikipedia and news extractive QA pairs, and answer-selection datasets with short answers. Synthetic data can be built by generating Norwegian wh-questions from passages and using concise extractive answers as positives.

Hard negatives should be plausible answers of the same type: nearby dates, related persons, same-domain place names, or entities from the same source article. These negatives teach the model to select the exact answer rather than a compatible answer type.

### Model Improvement Notes

Dense models can improve by representing question focus and answer type in Norwegian. Models trained only on passage retrieval may underperform because answer strings lack context. Adding answer-selection or extractive-QA supervision should help. Sparse systems have limited upside unless the answer contains query terms.

For reranking, this task calls for cross-encoders or late-interaction models that can compare the question and answer candidate directly. A good first-stage retriever should maximize recall@100, but final quality depends on answer-compatibility ranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Når ble euroen innført? [23 chars] | I 1999 [6 chars] |
| Hvilken bok lyver flest briter om at de har lest? [49 chars] | «Bibelen» [9 chars] |
| Hvilket land i Øst-Europa var det første til å få en ikke-kommunistisk statsminister? [85 chars] | 30 år uten Berlinmur Berlinmuren falt ikke, den ble revet av mennesker som ikke lenger ville leve bak stengsler. FOTO: GERARD MALLE/NTB SCANPIX Det heter at muren falt. Som om den tumlet over ende av... [200 / 1,948 chars] |
| Hva kalte romerne provinsen de lagde ut av dagens England og Wales? [67 chars] | Romersk Britannia [17 chars] |
| Hvordan var tonen til Botnan etter løpet? [41 chars] | litt mer spøkefull [18 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Scandinavian Embedding Benchmarks | Benchmark framing for Scandinavian retrieval tasks. |
| NorQuAD paper | Original Norwegian extractive QA dataset description. |
| NorQuAD retrieval dataset card | Retrieval adaptation and dataset access. |

### Representative Snippets

- A query asks when the euro was introduced; the relevant answer is `I 1999`.
- A query asks which book most Britons lie about having read; the relevant answer is `Bibelen`.
- A query asks which Eastern European country first got a non-communist prime minister; a relevant snippet discusses the Berlin Wall period.
- A query asks what Romans called the province made from today's England and Wales; the relevant answer is `Romersk Britannia`.
- A query asks what Botnan's tone was after the race; the relevant answer is a short phrase meaning a more joking tone.
