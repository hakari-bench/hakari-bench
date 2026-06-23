# MNanoBEIR / NanoBEIR-it / NanoHotpotQA

## Overview

`NanoBEIR-it__NanoHotpotQA` is the Italian NanoBEIR version of HotpotQA, a
multi-hop question answering benchmark introduced to test whether systems can
find the facts needed to answer questions that are not usually resolved by a
single sentence. In BEIR-style retrieval, the task is converted into evidence
search: each query is an Italian question, and the retriever must rank translated
Wikipedia passages that contain the supporting evidence. The Nano split contains
50 queries, 5,090 candidate documents, and 100 positive qrels, with exactly two
positive documents for every query. That fixed two-support structure makes the
task especially useful for studying whether a model can retrieve both sides of a
bridge or comparison rather than only the passage with the most obvious entity
overlap.

## Details

### What the Original Data Measures

[HotpotQA](https://arxiv.org/abs/1809.09600) was designed around diverse,
explainable multi-hop question answering over Wikipedia. Its questions often
combine a named entity with a second condition, such as an actor and a sitcom, a
person and a related work, or a historical figure and an associated object. BEIR
uses the dataset as an information retrieval benchmark by asking systems to
retrieve the passages that support the answer. In this Italian NanoBEIR task,
the same retrieval problem is exposed through translated queries and translated
passages, so the benchmark tests multilingual lexical matching, semantic
matching, and cross-sentence evidence discovery inside compact Wikipedia-style
paragraphs.

### Observed Data Profile

The task has 50 queries and 5,090 documents. There are 100 positive qrels, and
the positives-per-query distribution is unusually regular: the minimum, median,
and maximum are all 2, so every query requires two supporting passages. The
average query length is 93.38 characters, while the average document length is
378.28 characters. The queries are long enough to include multiple constraints,
but the documents are still short Wikipedia passages rather than full articles.
This creates a retrieval setting where entity names, titles, and explicit
descriptions matter, yet ranking only the first entity match is insufficient.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.7275, hit@10 = 0.9800, and
Recall@100 = 0.9300. This is a strong lexical profile: nearly every query has at
least one relevant passage in the top 10, which reflects the heavy presence of
named entities, titles, dates, and concrete nouns in HotpotQA-style questions.
However, the Recall@100 value shows that BM25 still misses some supporting
passages across the two-positive queries. A passage that contains the second hop
may share fewer surface terms with the question than the bridge passage does, so
term frequency and exact Italian token overlap can over-favor the more explicit
entity page.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.7540, hit@10 =
0.9200, and Recall@100 = 0.9200. Dense retrieval is slightly better than BM25 on
nDCG@10, suggesting that embedding similarity helps place semantically related
support passages higher when the query and evidence do not share all important
terms. At the same time, dense hit@10 and Recall@100 are lower than BM25. For
this task, semantic similarity helps ordering within the top ranks, but it can
also drift toward passages that are topically close without being one of the two
annotated supports. This is an important distinction for researchers: better
semantic ranking does not automatically imply better support coverage in
multi-hop retrieval.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.7762, hit@10 = 0.9600, and Recall@100 = 0.9700, with no rank-101
safeguard rows. It is the best configuration on both nDCG@10 and Recall@100,
while its hit@10 sits between BM25 and dense. This pattern is consistent with a
hybrid search effect: lexical retrieval contributes reliable entity and title
coverage, and dense retrieval contributes passages that are semantically aligned
even when the surface forms differ. Because every query has exactly two
positives, the hybrid advantage is especially meaningful here. It indicates that
combining lexical and dense evidence can recover the second support passage more
often than either single retrieval family.

### Metric Interpretation for Model Researchers

For this task, BM25-only retrieval is not a weak baseline. It is excellent at
finding at least one relevant support quickly, and its hit@10 is the highest of
the three profiles. Dense retrieval provides the strongest single-method
nDCG@10, which means it can improve the relative order of relevant evidence when
semantic paraphrase or translated wording matters. The hybrid profile is the
most useful diagnostic for end-to-end retrieval systems because it has the best
top-10 ranking quality and the best top-100 support coverage together. A model
that improves this task should therefore be judged not only by whether it finds
one answer-bearing page, but also by whether it retrieves both annotated support
passages with stable rank positions.

### Query and Relevance Type Tendencies

The sample queries ask for linked facts: a television actor and sitcom, a sword
and its donor, a film connected to a composer, a college football game, or a
music collection and performer identity. Many questions include proper nouns
that strongly guide lexical retrieval, but the required evidence often depends
on a second relation that is less directly expressed in the query. The positive
documents are compact encyclopedia paragraphs, so relevant evidence is usually
localized. This favors models that can combine exact entity anchoring with
semantic relation matching.

### Representative Failure Modes

BM25 can over-rank the first-hop entity page and under-rank the second support
when the latter uses different wording. Dense models can retrieve passages about
the same topic, work, person, or event that are plausible but not annotated as
supporting facts. Hybrid systems can still fail if both lexical and dense
signals agree on a popular distractor, especially when a query contains multiple
entities that appear across many Wikipedia passages. For evaluation, inspect
whether errors are one-support failures, bridge-entity failures, or near-miss
semantic distractors.

### Training Data That May Help

Useful training data includes non-overlapping multi-hop QA retrieval pairs,
Wikipedia evidence selection data, multilingual question-to-passage retrieval,
and hard negatives built from one-hop partial matches. Italian translated data
or multilingual supervision can help with surface-form variation, but training
should avoid overlap with HotpotQA, BEIR, NanoBEIR, and translated support
paragraphs used by this benchmark.

### Model Improvement Notes

This task rewards a retriever that keeps lexical anchors while expanding toward
the second relation implied by the question. Strong systems should combine
entity-sensitive candidate generation, semantic ranking, and hard-negative
training against passages that mention only one side of the multi-hop chain.
Evaluation beyond aggregate nDCG should check whether both positives appear in
the candidate set, because a single high-ranked support can hide a failure to
retrieve the complete evidence pair.

## Example Data

| Query | Positive document |
| --- | --- |
| In quale sitcom televisiva Penny Rae Bridges ha recitato insieme a quale altro attore? [86 chars] | Penny Rae Bridges (nata il 29 luglio 1990) è un'attrice americana. Ha recitato in "For Your Love", "Family Law", "Boy Meets World" e "The Parent 'Hood". È famosa per il suo ruolo in "Half & Half", nel ruolo della giovane Mona. [226 chars] |
| Chi ha donato a Kaganoi Shigemochi una spada forgiata dal fondatore della scuola Muramasa? [90 chars] | Kaganoi Shigemochi (加賀井 重望, 1561 – 27 agosto 1600) fu un samurai giapponese durante il periodo Azuchi-Momoyama, al servizio del clan Oda. Governava il castello di Kaganoi. Durante la battaglia di Komaki e Nagakute, Shigemochi combatté sotto il padre Shigemune, che era al servizio delle forze di Oda Nobukatsu. Poco dopo, il castello di Kaganoi fu circondato dalle forze di Toyotomi Hideyoshi; Shigemune si arrese, e Shigemochi fu assunto da Hideyoshi come messaggero, ricevendo uno stipendio di 10.000 "koku". Possedeva inoltre una spada forgiata da Muramasa, che Hideyoshi gli conferì nel 1598. [596 chars] |
| Quale film è stato scritto e diretto da Joby Harold con la musica di Samuel Sim? [80 chars] | Samuel Sim è un compositore di film e televisione. Ha ottenuto il primo riconoscimento con la colonna sonora premiata della serie drammatica della BBC "Dunkirk". Da allora ha composto la musica per una vasta gamma di produzioni cinematografiche e televisive, tra cui più recentemente la colonna sonora del film "Awake" per The Weinstein Company e la serie drammatica BBC/HBO "House of Saddam". La sua musica più recente e acclamata è la colonna sonora di Home Fires. Home Fires (Musiche della Serie Televisiva) è stato pubblicato il 6 maggio 2016 da Sony Classical Records. [573 chars] |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | [https://arxiv.org/abs/1809.09600](https://arxiv.org/abs/1809.09600) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
