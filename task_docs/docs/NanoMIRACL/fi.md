# NanoMIRACL / fi

## Overview

`NanoMIRACL / fi` is the Finnish split of the MIRACL-style multilingual
monolingual retrieval benchmark. Finnish queries retrieve Finnish Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 328 positive qrel rows. The task combines compact fact questions,
Finnish morphology, compounds, and passage-level evidence selection. Current
diagnostics show dense retrieval as the strongest nDCG@10 profile, BM25 as a
very strong lexical baseline, and `reranking_hybrid` as the strongest hit and
recall profile.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Finnish queries retrieve Finnish
passages from Finnish Wikipedia. The benchmark emphasizes natural-language
questions, passage-level evidence, and human relevance judgments.

Finnish is one of the MIRACL languages connected to the TyDi/Mr. TyDi lineage.
The MIRACL framing adds dense passage-level judgments over a consistently
segmented Wikipedia corpus. For this split, the relevant item is the Finnish
passage that contains answer evidence, not a short answer or a translated
English passage.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 328 positive qrel
rows. Positives per query average 1.64, with a minimum of 1, a median of 1, and
a maximum of 5. There are 83 multi-positive queries, representing 41.5 percent
of the split. Queries average 37.19 characters, while documents average 393.62
characters.

The examples are compact Finnish fact questions using forms such as `Mikä`,
`Mitä`, `Milloin`, `Missä`, `Kuka`, `Onko`, `Kuinka`, `Mistä`, and `Miten`.
Topics include scientific definitions, history, rulers, Christian reformation,
philosophy, film direction, places, geography, food, horse colors, mental
health terms, and literature.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7734, hit@10 = 0.9650, and recall@100 = 0.9848. BM25 is
strong because many Finnish questions contain distinctive rare terms, names,
places, and technical words. Exact matches for terms such as scientific
concepts, place names, book titles, or geographic entities are highly useful.

The sparse profile still has limitations. Finnish inflection and compounds can
separate query forms from passage forms, and generic question words can pull in
related but non-answering passages. BM25 may retrieve the right topic family
while missing the passage that states the requested definition, location,
director, or yes/no relation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.8634, hit@10 = 0.9550, and recall@100 = 0.9512.
Dense retrieval is the strongest observed profile by nDCG@10. It appears to
rank answer-bearing Finnish passages higher by matching semantic question
intent rather than relying only on exact surface overlap.

The tradeoff is coverage. Dense retrieval is slightly weaker than BM25 and
hybrid retrieval by hit@10 and recall@100. This means it is excellent at
ordering many relevant passages but less complete as a candidate generator.
Finnish therefore offers a useful diagnostic split for separating top-rank
semantic quality from broad positive retention.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.8332, hit@10 = 0.9750,
and recall@100 = 1.0000. Hybrid retrieval is below dense retrieval by nDCG@10,
but it has the best hit@10 and complete observed top-100 positive coverage.

This profile reflects the value of combining lexical and dense retrieval. BM25
contributes exact Finnish terms, compounds, names, and rare entity strings,
while dense retrieval contributes semantic matching for relation and definition
questions. The resulting candidate set is particularly useful for downstream
rerankers.

### Metric Interpretation for Model Researchers

This task is multi-positive for 41.5 percent of queries, lower than several
other MIRACL Nano splits but still important. Hit@10 measures whether at least
one relevant passage appears near the top. nDCG@10 rewards ranking relevant
passages high, and recall@100 measures how much of the judged positive set
survives for reranking.

The observed pattern is clear: dense retrieval is best for top-rank ordering,
BM25 is a very strong sparse baseline, and `reranking_hybrid` is best for
candidate coverage. Finnish models should therefore be evaluated for both
inflection-aware exact matching and semantic passage selection.

### Query and Relevance Type Tendencies

Queries are short Finnish information needs about definitions, people, dates,
locations, authors or directors, scientific concepts, places, and yes/no
relations. Many questions contain strongly informative content words, but the
relevant passage must state the requested relation.

Relevant documents are Finnish Wikipedia passages with title context and
answer-bearing prose. The task rewards compound handling, morphology-aware
matching, entity recognition, and semantic evidence retrieval. It also tests
whether the model can avoid broad topic pages when a narrower passage contains
the answer.

### Representative Failure Modes

BM25 can retrieve related passages with strong lexical overlap but miss the
labeled evidence. A question asking whether reformation is the same as
`reformaatio` can retrieve several reformation passages while the relevant
passage is in a broader intellectual-history context. A question about who
directed `Black Panther` can retrieve music or release-detail passages before
the passage naming the director. Abstract questions such as `Mitä on
stoalaisuus?` or `Mitä on altruismi?` can attract related philosophy or
psychology passages.

Dense retrieval can fail when a semantically close Finnish passage lacks the
exact answer fact. Hybrid retrieval reduces missing positives, but a reranker
still has to choose the passage with the most direct evidence.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Finnish training data,
Finnish Wikipedia question-to-passage retrieval pairs, Finnish entity-attribute
QA evidence retrieval pairs, and hard negatives from related Finnish Wikipedia
pages. Training should include inflected names, compounds, dates, places,
definitions, creator roles, and yes/no relations.

Synthetic data can help when it creates Finnish Wikipedia-style passages with
titles, aliases, dates, locations, definitions, roles, and factual evidence.
Generated questions should use varied `Mikä`, `Mitä`, `Milloin`, `Missä`,
`Kuka`, `Onko`, `Kuinka`, `Mistä`, and `Miten` forms with realistic inflection.
Comparable evaluation should exclude upstream development/test data or other
MIRACL-derived examples likely to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their strong semantic top-rank behavior while
recovering more of BM25's recall. Sparse systems benefit from Finnish
morphology handling, compound-aware tokenization, and careful weighting of rare
terms versus generic question words. Rerankers should combine exact entity and
term evidence with relation-level answer matching.

For hybrid systems, `NanoMIRACL / fi` supports `reranking_hybrid` as a
high-recall candidate stage. The dense baseline shows that top-rank evidence
ordering can be very strong, while the hybrid profile shows that lexical Finnish
signals are still needed for complete coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Kuka perusti Ferrarin? [22 chars] | Ferrari Ferrari S.p.A. on italialainen urheiluautojen valmistaja. Ferrarin perusti Enzo Ferrari vuonna 1939 nimellä "Auto Avio Costruzioni". Ferrari on juridisesti alankomaalainen yhtiö, mutta sen pää... [200 / 425 chars] |
| Mitä tarkoittaa psykoosi? [25 chars] | Hallusinaatio Psykoosi tarkoittaa, että ihmisen todellisuudentaju on heikentynyt, eli hän ei tajua psykoosin laukaisemia kuulo- tai muita harhoja harhoiksi. Psykoosisairauttakin sairastava henkilö voi... [200 / 307 chars] |
| Onko Uranuksella kuita? [23 chars] | Uranus Uranuksella on 27 tunnettua kuuta. Kaksi suurinta kuuta, Titanian ja Oberonin, löysi Herschel 13. maaliskuuta 1787. William Lassell löysi Arielin ja Umbrielin vuonna 1851. William Herschelin po... [200 / 909 chars] |
| Mistä Suvarnabhumin lentoasema on saanut nimensä? [49 chars] | Suvarnabhumin kansainvälinen lentoasema Nimi "Suvarnabhumi" on Thaimaan kuninkaan Bhumibol Adulyadejin keksimä, ja se tarkoittaa "kultaista maata". [148 chars] |
| Mitä tuotteita Afrikka vie ulkomaille? [38 chars] | Afrikan talous Afrikan selvästi arvokkaimmat vientituotteet ovat mineraalit sekä öljy. Nämä luonnonvarat ovat keskittyneet muutaman valtion alueelle. Eteläisillä valtiolla on suuret määrät kultaa, tim... [200 / 397 chars] |

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
| A Finnish question asking where a term name comes from. | A passage about the term's history and naming. |
| A question asking what pieces in a game are like. | A passage explaining the game board, pieces, and rules. |
| A question asking whether a planet has moons. | A passage listing known moons and discovery details. |
| A question asking whether a book series has a shared plot. | A passage about the series and its volumes. |
| A question asking where an island or place is located. | A passage describing the place and its geographic context. |
