# MNanoBEIR / NanoBEIR-es / NanoHotpotQA

## Overview

This task is the Spanish NanoBEIR version of HotpotQA, a multi-hop question answering retrieval benchmark built from Wikipedia. The original HotpotQA dataset was designed to require reasoning over multiple supporting documents, especially bridge questions and comparison questions. In this NanoBEIR slice, Spanish translated multi-hop questions must retrieve Spanish translated supporting Wikipedia passages from 5,090 candidates. The task contains 50 queries and 100 positive relevance judgments, with exactly two positives for every query. It is useful for diagnosing whether retrieval models can surface both pieces of evidence needed for multi-hop reasoning, rather than only the most lexically obvious entity page.

## Details

### What the Original Data Measures

HotpotQA measures explainable multi-hop QA. In retrieval form, the important step is recovering the supporting passages that make the reasoning path possible. A question may name one entity but require another linked entity, or compare two entities using attributes that appear in separate passages. A retriever must therefore find complementary evidence, not only a single answer-like paragraph.

### Observed Data Profile

The Spanish Nano task has 50 queries, 5,090 documents, and 100 positives. Every query has two relevant passages. Query length averages about 93 characters, and documents average about 391 characters. The examples include questions about Penny Rae Bridges, Kaganoi Shigemochi, Joby Harold and Samuel Sim, a Clemson football game, and the Supersuckers compilation Devil's Food. Documents are short Wikipedia-style entity descriptions and event passages.

### BM25 Evaluation Profile

BM25 is strongest by top-10 ranking, with nDCG@10 of 0.747, Hit@10 of 0.960, and Recall@100 of 0.900. This reflects the entity-heavy structure of the task. Many queries contain names, titles, locations, or dates that appear directly in one of the supporting passages. Sparse retrieval is especially effective at finding the most obvious entity page. The remaining challenge is retrieving the second support passage, which may be connected by a bridge relation and may not repeat all query terms.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.710, Hit@10 of 0.900, and Recall@100 of 0.860. Dense retrieval helps with semantic bridge relations and paraphrased context, but it trails BM25 on this Spanish slice. This suggests that exact entity and title matching are highly important here. Dense models can over-rank semantically related Wikipedia passages that are not one of the two gold supports, especially when a broad topic or entity neighborhood contains many plausible distractors.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.721, Hit@10 of 0.940, and Recall@100 of 0.940. It has the best Recall@100, while BM25 has the best nDCG@10. This means hybrid search is best at ensuring both support passages appear in the candidate pool, but BM25's exact lexical ordering remains very competitive at the top. For multi-hop QA pipelines, the hybrid candidate pool may be more useful than a slightly higher first-page lexical ranking because missing the second evidence passage breaks answerability.

### Metric Interpretation for Model Researchers

Because every query has exactly two positives, metrics should be interpreted as evidence-chain retrieval measures. Hit@10 can be high even if only one support passage is retrieved, so nDCG@10 and Recall@100 are more informative. Recall@100 is especially important for downstream multi-hop readers, which need both evidence pieces. A model that retrieves one obvious entity page but misses the bridge passage is incomplete for this task.

### Query and Relevance Type Tendencies

Queries are natural Spanish multi-hop questions involving people, films, sports events, music, and historical entities. Relevant documents are paired evidence passages. One positive is often directly lexical, while the other may be connected through a relation such as actor, composer, founder, event date, or publication. This makes the task sensitive to entity linking, aliases, and bridge relation understanding.

### Representative Failure Modes

BM25 can retrieve the direct entity page while missing the bridge or answer-bearing page. Dense retrieval can retrieve a semantically related page from the same entity neighborhood but not the gold support. Hybrid retrieval improves coverage but can still rank one support high and bury the other. Failure analysis should check whether both positives are retrieved and whether they jointly support the answer.

### Training and Leakage Considerations

Training should exclude HotpotQA, BEIR, NanoBEIR, and translated records likely to overlap with these questions or supporting pages. Useful non-overlapping data includes multi-hop QA retrieval examples, Wikipedia hyperlink graph pairs, Spanish or multilingual question-to-multiple-document supervision, and bridge/comparison question generation. Multi-positive training is required because every query needs two evidence documents.

### Model Improvement Signals

Strong models should preserve exact entity matching while improving retrieval of the second support passage. Useful training signals include paired evidence supervision, bridge-entity hard negatives, comparison questions, and relation-aware dense retrieval. Hybrid systems should use BM25 for names and titles while dense retrieval expands candidates to semantically linked supports.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Con qué otro actor participó Penny Rae Bridges en una sitcom de televisión? [76 chars] | Penny Rae Bridges (nacida el 29 de julio de 1990) es una actriz estadounidense. Su trabajo en televisión incluye papeles en "For Your Love", "Family Law", "Boy Meets World" y "The Parent 'Hood". Es más conocida por su papel en "Half & Half", interpretando a la joven Mona. [272 chars] |
| ¿Quién otorgó a Kaganoi Shigemochi una espada fabricada por el fundador de la escuela Muramasa? [95 chars] | Kaganoi Shigemochi (加賀井 重望, 1561 – 27 de agosto de 1600) fue un samurái japonés del período Azuchi-Momoyama que sirvió al clan Oda. Gobernó el Castillo Kaganoi. Durante la Batalla de Komaki y Nagakute, Shigemochi luchó bajo las órdenes de su padre, Shigemune, quien estaba adscrito a las fuerzas de Oda Nobukatsu. Poco después, el Castillo Kaganoi fue rodeado por las tropas de Toyotomi Hideyoshi; Shigemune se rindió, y Shigemochi fue empleado por Hideyoshi como mensajero, recibiendo un estipendio de 10,000 'koku'. También poseía una espada forjada por Muramasa, que Hideyoshi le otorgó en 1598. [598 chars] |
| ¿Qué película fue escrita y dirigida por Joby Harold y tiene música de Samuel Sim? [82 chars] | Samuel Sim es un compositor de cine y televisión. Alcanzó reconocimiento con su premiada banda sonora para la serie dramática de la BBC "Dunkirk". Desde entonces, ha compuesto la música para una amplia variedad de producciones cinematográficas y televisivas, más recientemente la película "Awake" para The Weinstein Company y la serie dramática de la BBC/HBO "House of Saddam". Su música más reciente y reconocida es la banda sonora de "Home Fires". "Home Fires (Música de la Serie de Televisión)" fue lanzado el 6 de mayo de 2016 por Sony Classical Records. [558 chars] |

## Public Sources

- [HotpotQA paper](https://arxiv.org/abs/1809.09600)
- [HotpotQA official site](https://hotpotqa.github.io/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| HotpotQA paper (https://arxiv.org/abs/1809.09600) |
| HotpotQA official site (https://hotpotqa.github.io/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
