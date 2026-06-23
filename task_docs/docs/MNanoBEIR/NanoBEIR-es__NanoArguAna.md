# MNanoBEIR / NanoBEIR-es / NanoArguAna

## Overview

This task is the Spanish NanoBEIR version of ArguAna, an argument retrieval benchmark where the query is an argument and the relevant document is its counterargument. The original ArguAna task studies retrieval of the best counterargument without assuming prior topic knowledge, using debate-portal argument pairs where relevant documents often discuss the same issue while taking the opposite stance. In this NanoBEIR slice, long Spanish translated arguments must retrieve Spanish translated counterarguments from 3,635 candidate documents. There are 50 queries and 50 positive relevance judgments, with exactly one positive per query. The task is a compact diagnostic for stance-aware retrieval: models must recognize topic continuity, shared argumentative aspects, and rebuttal relation, not just ordinary semantic similarity.

## Details

### What the Original Data Measures

ArguAna measures counterargument retrieval. A good result should answer an argument with an opposing argument that targets the same issue or premise. This differs from standard topical retrieval because a document that agrees with the query can be lexically and semantically close while still being irrelevant. The task therefore tests whether a retriever can separate same-topic support from same-topic rebuttal, using long argumentative passages with premises, conclusions, examples, and cited evidence.

### Observed Data Profile

The Spanish Nano task has 50 queries, 3,635 documents, and 50 positives. Every query has one positive counterargument. Queries are very long, averaging about 1,220 characters, and documents average about 1,111 characters. The examples cover reform of the House of Lords, Heathrow expansion, excessive consumer choice, cyberattacks by non-state actors, and limits on religiously motivated speech. Both query and positive passages are translated debate arguments rather than short questions or factual statements.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.413, Hit@10 of 0.700, and Recall@100 of 0.940. This shows that sparse retrieval is effective at candidate discovery because counterarguments usually reuse the same topic vocabulary, named institutions, policy terms, and debate-specific language. However, BM25 is weaker at top ranking because lexical overlap does not distinguish rebuttal from support. A same-topic pro argument can look highly relevant to a sparse model even when the true positive is the opposing stance.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline gives the best top-10 ranking, with nDCG@10 of 0.481, Hit@10 of 0.860, and Recall@100 of 0.900. Dense retrieval can capture broader argumentative fit and paraphrased premise relations, which helps it rank counterarguments above simple lexical matches. Its Recall@100 is slightly lower than BM25, suggesting that exact topic terms still matter for broad candidate coverage. The dense profile is nevertheless the strongest direct retrieval signal for this Spanish slice because it better handles long-passage semantic relation.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.436, Hit@10 of 0.740, and Recall@100 of 0.980, with one safeguard row at 101 candidates. It has the best Recall@100 but does not beat dense retrieval in top-10 ranking. This is a typical pattern for stance-aware retrieval: hybrid search is valuable for ensuring the counterargument appears in the candidate set, but dense ranking may be better at ordering the correct rebuttal above other same-topic passages. The hybrid result is most useful as a reranking pool.

### Metric Interpretation for Model Researchers

Because each query has exactly one positive, Recall@100 directly measures whether the correct counterargument is available for reranking. nDCG@10 and Hit@10 measure whether the model can place that counterargument where a user would see it. The gap between hybrid recall and dense nDCG suggests a two-stage opportunity: use hybrid retrieval for coverage, then apply a stance-aware reranker to separate rebuttal from topical similarity.

### Query and Relevance Type Tendencies

Queries are long arguments that include claims, supporting reasons, and examples. Relevant documents are counterarguments that share the same controversial issue but reverse the stance or challenge the premise. Many hard negatives are likely to discuss the same topic and even use similar evidence, so relevance depends on argumentative role and opposition, not merely topical overlap.

### Representative Failure Modes

BM25 can retrieve supporting arguments because they repeat many of the same words. Dense retrieval can retrieve conceptually close arguments that do not actually rebut the query. Hybrid retrieval can include the positive but rank a same-side argument above it. Failure analysis should inspect the stance relation: does the retrieved document challenge the query's core claim, or does it simply discuss the issue?

### Training and Leakage Considerations

Training should exclude ArguAna, BEIR, NanoBEIR, and translated debate records likely to overlap with the evaluation arguments. Useful non-overlapping data includes argument-counterargument pairs, stance-aware retrieval datasets, debate portal argument pairs, claim rebuttal data, and Spanish or multilingual argument mining corpora. Synthetic data should create paired pro and con arguments for the same issue with explicit stance reversal and same-topic hard negatives.

### Model Improvement Signals

Strong models should improve stance-sensitive ranking while preserving topic coverage. Useful training signals include long-passage contrastive examples, premise-targeted rebuttals, pro/con hard negatives, and multilingual argument mining data. Hybrid systems should use BM25 for reliable issue matching and dense or cross-encoder scoring for the counterargument relation.

## Example Data

| Query | Positive document |
| --- | --- |
| El público es apático ante la reforma. Es discutible si la reforma de la Cámara de los Lores debería... [100 / 572 chars] | La campaña de voto alternativo no puede compararse con una reforma del sistema político. Además, no se debe confundir a un público mal informado debido a la manipulación política con apatía. A menudo,... [200 / 462 chars] |
| La expansión de Heathrow es vital para la economía. La expansión de Heathrow garantizaría muchos de... [100 / 1,285 chars] | La comunidad empresarial está lejos de estar unida en su supuesto apoyo a una tercera pista. Las encuestas sugieren que muchos negocios influyentes, en realidad, no apoyan la expansión. Una carta expr... [200 / 1,438 chars] |
| Las personas tienen demasiadas opciones, lo que las hace menos felices. La publicidad lleva a muchas... [100 / 989 chars] | Las personas están descontentas porque no pueden tenerlo todo, no porque se les ofrezca demasiadas opciones y eso les resulte estresante. De hecho, los anuncios juegan un papel crucial al asegurar que... [200 / 983 chars] |
| Los ataques cibernéticos a menudo son perpetrados por actores no estatales, como ciberterroristas o... [100 / 1,067 chars] | En caso de un ataque de actores no estatales, muchos expertos en derecho internacional coinciden en que el estado puede aún retaliar en defensa propia si otro estado es 'incapaz o no está dispuesto a... [200 / 599 chars] |
| Porque la religión promueve la certeza de la creencia, el odio divino es fácil de utilizar para just... [100 / 1,473 chars] | Nadie está siendo obligado a cometer actos de violencia por las palabras de otra persona; es su elección hacerlo. Igualmente, hay muchas personas que podrían tener opiniones que se considerarían homof... [200 / 680 chars] |

## Public Sources

- [ArguAna paper](https://aclanthology.org/P18-1023/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| ArguAna paper (https://aclanthology.org/P18-1023/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
