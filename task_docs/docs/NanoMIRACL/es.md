# NanoMIRACL / es

## Overview

`NanoMIRACL / es` is the Spanish split of the MIRACL-style multilingual
monolingual retrieval benchmark. Spanish queries retrieve Spanish Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 934 positive qrel rows. It is highly multi-positive: most
queries have several judged answer-bearing passages. Current diagnostics show
dense retrieval as the strongest nDCG@10 profile, BM25 as a very strong lexical
baseline for finding at least one positive, and `reranking_hybrid` as the
strongest recall profile with complete observed recall@100 coverage.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Spanish queries retrieve Spanish
passages from Spanish Wikipedia. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Spanish belongs to the MIRACL languages built beyond the earlier Mr. TyDi/TyDi
QA sources. The task should therefore be read as Spanish Wikipedia passage
retrieval created in the MIRACL framework, not as an English benchmark
translated into Spanish. The relevant item is an evidence-bearing passage that
supports the question, not a direct answer string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 934 positive qrel
rows. Positives per query average 4.67, with a minimum of 1, a median of 4, and
a maximum of 10. There are 172 multi-positive queries, representing 86.0 percent
of the split. Queries average 47.65 characters, while documents average 453.21
characters.

The examples are natural Spanish questions using forms such as `¿Qué`,
`¿Cuál`, `¿Cómo`, `¿Por qué`, `¿Cuáles`, `¿Quién`, `¿Cuándo`, `¿Dónde`, and
`¿Cuántos`. Topics include history, geography, religion, politics, science,
definitions, alphabets, universities, mythology, music, media, skyscrapers,
regions, and cultural works.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6861, hit@10 = 0.9900, and recall@100 = 0.9807. BM25 is
very strong because Spanish queries often contain distinctive names, places,
titles, numbers, and domain terms that recur in relevant Wikipedia passages.
This includes phrases such as alphabet names, religious terms, proper nouns,
geographic entities, and media titles.

The limitation is not whether BM25 can find Spanish evidence at all; it usually
can. The limitation is ranking the best passage among many related positives
and distractors. For questions asking what something is called, why a place has
its name, which entities belong to a set, or where a historical fact comes from,
lexical overlap can place topically close but non-answering passages above the
most direct evidence.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7793, hit@10 = 0.9350, and recall@100 = 0.9133.
Dense retrieval is the strongest observed profile by nDCG@10. It ranks
answer-bearing passages higher when the important signal is the semantic
relation requested by the Spanish question rather than exact term overlap.

The tradeoff is that dense retrieval has lower hit@10 and recall@100 than BM25
and hybrid retrieval. This means it is good at ordering the positives it finds
but less complete as a candidate generator. For a highly multi-positive task
like Spanish MIRACL, this distinction matters: top-rank quality and positive
set coverage are different system properties.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.7478, hit@10 = 0.9900,
and recall@100 = 1.0000. Hybrid retrieval is slightly below dense retrieval by
nDCG@10, but it matches BM25's strong hit@10 and preserves every judged positive
within the observed top-100 candidate set.

This is the clearest Spanish signal: hybrid search is the best candidate
generation strategy. BM25 contributes exact Spanish surface forms, while dense
retrieval contributes semantic relation matching. The combined result has both
high top-10 usefulness and complete positive coverage for downstream reranking.

### Metric Interpretation for Model Researchers

This task is heavily multi-positive: 86.0 percent of queries have more than one
positive passage. Hit@10 measures whether at least one relevant passage appears
near the top. nDCG@10 rewards ranking relevant passages high, and recall@100
measures how much of the judged positive set remains available for reranking.

The observed profile separates ranking from coverage. Dense retrieval is best
for top-rank ordering, BM25 is extremely strong at retrieving at least one
positive, and `reranking_hybrid` is strongest for complete candidate coverage.
For Spanish retrieval research, this task is especially useful for evaluating
whether a model can improve top ranking without sacrificing the broad positive
set.

### Query and Relevance Type Tendencies

Queries are concise Spanish information needs about names, definitions, causes,
locations, counts, historical facts, institutional facts, cultural works, and
entity membership. They often contain a clear topic anchor, but relevance
depends on the requested relation: what something is called, why it has a name,
where an event occurred, how many items exist, or who is associated with an
entity.

Relevant documents are Spanish Wikipedia passages with article-title context and
answer-bearing prose. The task rewards systems that distinguish direct evidence
from related topic passages and that handle Spanish interrogative forms,
accented terms, named entities, and inflection.

### Representative Failure Modes

BM25 can over-rank passages that share numbers or topic words but do not answer
the question. A question about the ten tallest skyscrapers in Malaysia can
retrieve unrelated pages containing `10` and building vocabulary before the
specific skyscraper passage. A question asking why the Iberian Peninsula is
called that can retrieve nearby peninsula or Iberian pages before the passage
that explains the name. A question asking what Jews call the Pentateuch can
retrieve broad Jewish-history pages before the passage that states the Torah
relation.

Dense retrieval can fail by preferring a semantically plausible Spanish passage
that lacks the exact answer statement. Hybrid retrieval reduces missing
positives, but a reranker still has to choose the passage with the most direct
evidence among many relevant or near-relevant candidates.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Spanish training data,
Spanish Wikipedia question-to-passage retrieval pairs, Spanish open-domain QA
evidence retrieval datasets, and Spanish entity-attribute supervision for
history, geography, religion, politics, media, organizations, and definitions.
Hard negatives should include related Spanish Wikipedia passages that share
entities but lack the requested relation.

Synthetic data can help when it creates Spanish Wikipedia-style passages with
titles, aliases, dates, locations, lists, definitions, and factual evidence.
Generated questions should use varied `qué`, `cuál`, `cómo`, `por qué`,
`quién`, `cuándo`, `dónde`, and `cuántos` forms. Comparable evaluation should
exclude upstream development/test data or other MIRACL-derived examples likely
to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their semantic top-rank advantage while
recovering BM25's strong lexical coverage. Sparse systems benefit from better
weighting of Spanish question intent and from recognizing when exact topic
overlap is not enough. Rerankers should combine exact names, numbers, and terms
with relation-level evidence matching.

For hybrid systems, `NanoMIRACL / es` strongly supports `reranking_hybrid` as a
candidate stage: it achieves complete recall@100 while keeping high hit@10 and
near-dense nDCG@10. The next improvement target is reranking those candidates so
the most direct evidence passages are consistently placed first.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Cómo es la arquitectura del caravasar de Orbelián? [51 chars] | Caravasar de Orbelian El caravasar está construido con bloques de basalto. [75 chars] |
| ¿Cómo llaman los judíos al Pentateuco? [38 chars] | Pentateuco Se corresponde con los que en la tradición hebrea forman la "Torá" —La Ley—, núcleo de la religión judía. Los cinco libros que lo componen son:Está contenido a su vez en el "Tanaj", el cual es considerado sagrado por todas las religiones abrahámicas (judaísmo, cristianismo e islam). No obstante lo anterior y que es uno de sus tres textos sagrados, los musulmanes creen que el texto sufrió corrupción ("tahrif") por los escribas judíos y cristianos por lo que no confían del todo en él. Mientras que los hebreos los nombran por la primera palabra significativa de cada uno, los cristianos han seguido tradicionalmente la nomenclatura de la versión griega de los LXX. [679 chars] |
| ¿Cuándo recibió Daniel Harold Rolling la inyección letal de su condenación? [75 chars] | Daniel Harold Rolling Rolling fue ejecutado por inyección letal en prisión estatal de Florida el 25 de octubre de 2006, después de que la Corte Suprema de Estados Unidos rechazó una última apelación. Fue declarado fallecido a las 18:13 EDT. [241 chars] |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984),
  2022.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/),
  2023.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus),
  source corpus dataset.
- [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | [https://aclanthology.org/2023.tacl-1.63/](https://aclanthology.org/2023.tacl-1.63/) |
| MIRACL GitHub repository |  | project repository | [https://github.com/project-miracl/miracl](https://github.com/project-miracl/miracl) |
| miracl/miracl-corpus |  | dataset card | [https://huggingface.co/datasets/miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Spanish question asking what the first women's university in Japan was. | A passage about the institution and its founding context. |
| A question asking what Jews call the Pentateuch. | A passage stating the relation between the Pentateuch and the Torah. |
| A question asking how a place name is pronounced. | A passage with pronunciation or naming information for the place. |
| A question asking which cities or places are most touristic. | A passage about tourism in the relevant country or region. |
| A question asking what a historical or literary figure died of. | A biographical passage containing the death-related evidence. |
