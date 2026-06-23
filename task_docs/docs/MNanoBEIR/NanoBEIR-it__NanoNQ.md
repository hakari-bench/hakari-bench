# MNanoBEIR / NanoBEIR-it / NanoNQ

## Overview

`NanoBEIR-it__NanoNQ` is the Italian NanoBEIR version of Natural Questions, an
open-domain question answering retrieval benchmark based on real Google search
questions and Wikipedia evidence. The task uses Italian translated questions to
retrieve Italian translated Wikipedia passages that contain answer evidence. The
Nano split contains 50 queries, 5,035 documents, and 57 positive qrels. Most
queries have one positive passage, while 7 queries have two. This makes the task
a compact test of short question-to-Wikipedia passage retrieval, where semantic
answer matching is usually more important than matching only the visible query
terms.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced a benchmark
for real information-seeking questions paired with Wikipedia answers and
annotations. In BEIR, NQ is used as an open-domain QA retrieval task: a system
must rank passages likely to contain the answer to a natural question. The
Italian NanoBEIR version preserves the same retrieval behavior in a multilingual
setting. Questions are often direct, but the relevant passage may express the
answer through surrounding context, dates, titles, or explanatory prose rather
than repeating the question wording.

### Observed Data Profile

The task contains 50 queries and 5,035 documents. It has 57 positive qrels, with
an average of 1.14 positives per query. The positives-per-query distribution is
1 minimum, 1.00 median, and 2 maximum, and 14.0% of queries are multi-positive.
Queries average 54.32 characters, while documents average 575.90 characters.
Compared with MS MARCO, the documents are longer and more encyclopedia-like; the
questions remain short but frequently depend on the retriever recognizing the
answer context rather than just the named entity.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3750, hit@10 = 0.4800, and
Recall@100 = 0.7895. BM25 finds many relevant passages somewhere in the first
100 candidates, but it struggles in the top 10. This suggests that exact Italian
term overlap is useful for entity names, titles, and event references, yet not
sufficient to rank the answer passage reliably. Short natural questions often
contain function words and broad entity references, while the supporting
Wikipedia passage may answer indirectly through a description, date, or
relationship.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.5133, hit@10 =
0.7000, and Recall@100 = 0.8772. Dense retrieval is the strongest top-10
profile for this task. The improvement over BM25 indicates that embedding
similarity is better suited to mapping question intent to answer context, even
when the passage does not repeat the full query. This is a typical Natural
Questions signal: the model needs to connect a question such as where an event
was held, why a landmark is located somewhere, or who performed a song with the
passage that contains the answer-bearing explanation.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4545, hit@10 = 0.6600, and Recall@100 = 0.8947. Four queries use the
rank-101 safeguard. Hybrid retrieval has the best top-100 relevant coverage, but
its top-10 ranking is below dense retrieval. This means that combining lexical
and dense candidates helps keep more positives available for reranking, while
the fused candidate order is not always as semantically focused as dense alone
near the top. For this task, hybrid search is most valuable as a candidate pool
for a stronger reranker.

### Metric Interpretation for Model Researchers

The main pattern is dense top-rank strength with hybrid coverage strength. BM25
is weaker at placing positives in the first 10, even though it retrieves many of
them within the top 100. Dense retrieval gives the best nDCG@10 and hit@10,
showing that semantic question-answer matching is central. Hybrid retrieval
gives the best Recall@100, which matters when downstream reranking can reorder a
candidate set. A model that claims progress on this task should show whether it
improves semantic answer ranking, candidate coverage, or both, because those are
different retrieval capabilities.

### Query and Relevance Type Tendencies

The examples include questions about a sports event location, the production
origin of a film, the meaning of a landmark's location, a constitutional clause,
and a song performer. Relevant passages are Wikipedia-style paragraphs that
contain the fact in context. Some queries include explicit named entities, but
others rely on relation words such as "where", "why", or "who". Effective
retrieval therefore needs both entity anchoring and relation-aware semantic
matching.

### Representative Failure Modes

BM25 can rank a page mentioning the main entity above the passage that actually
answers the question. Dense retrieval can retrieve semantically related
Wikipedia passages that discuss the event, film, song, or concept but omit the
specific answer. Hybrid retrieval can include the positive in the candidate set
while still placing lexical distractors above it. For the few two-positive
queries, another error mode is retrieving only one of the answer-bearing
passages.

### Training Data That May Help

Useful training data includes non-overlapping open-domain QA retrieval,
Wikipedia question-passage pairs, Italian question answering, and multilingual
answer retrieval data. Hard negatives should contain related entities or
article-level topical overlap without the answer sentence. Training should
exclude Natural Questions, BEIR, NanoBEIR, and overlapping translated Wikipedia
passages from this benchmark.

### Model Improvement Notes

This task rewards models that understand short questions as answer-seeking
intents rather than bags of terms. Improvements should focus on answer evidence
selection, relation matching, and distinguishing answer-bearing passages from
topic-only passages. Hybrid candidate generation can improve coverage, but the
final ranker must be able to recover the dense semantic signal to maximize
nDCG@10.

## Example Data

| Query | Positive document |
| --- | --- |
| Dove si terrà la Final Four quest'anno? [39 chars] | L'80ª edizione del Torneo di Pallacanestro Maschile della Divisione I della NCAA 2018 è stato un torneo a eliminazione diretta con 68 squadre per determinare il campione nazionale di pallacanestro della Divisione I della NCAA per la stagione 2017-18. Il torneo è iniziato il 13 marzo 2018 e si è concluso con la finale il 2 aprile all'Alamodome di San Antonio, Texas. [367 chars] |
| L'incubo prima di Natale è stato originariamente un film Disney? [64 chars] | Il film "Nightmare Before Christmas" ha avuto origine da una poesia scritta da Tim Burton nel 1982, mentre lavorava come animatore presso la Walt Disney Feature Animation. Grazie al successo di "Vincent" nello stesso anno, la Walt Disney Studios iniziò a considerare la possibilità di sviluppare "Nightmare Before Christmas" come cortometraggio o speciale televisivo di 30 minuti. Nel corso degli anni, Burton tornò più volte a questo progetto, e nel 1990, strinse un accordo di sviluppo con Disney. La produzione iniziò a luglio 1991 a San Francisco; Disney distribuì il film sotto l'etichetta Touchstone Pictures, poiché lo studio riteneva che il film fosse "troppo oscuro e spaventoso per i bambini".[4] [706 chars] |
| Perché l'Angelo del Nord si trova lì? [37 chars] | Secondo Gormley, il significato dell'angelo era triplice: innanzitutto, per indicare che sotto il sito della sua costruzione, i minatori di carbone avevano lavorato per due secoli; in secondo luogo, per comprendere la transizione dall'era industriale a quella dell'informazione, e infine, per fungere da punto di riferimento per le nostre speranze e paure in evoluzione. [370 chars] |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | [https://aclanthology.org/Q19-1026/](https://aclanthology.org/Q19-1026/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
