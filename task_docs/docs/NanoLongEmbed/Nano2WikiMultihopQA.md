# NanoLongEmbed / Nano2WikiMultihopQA

## Overview

`NanoLongEmbed / Nano2WikiMultihopQA` is the 2WikiMultiHopQA retrieval task in
LongEmbed. Queries are English multi-hop questions, and documents are long
bundles of Wikipedia-derived passages. The model must retrieve the bundle that
contains the entities and evidence chain needed to answer the question. The
Nano split has 200 queries, 300 documents, and one positive document per query.
Documents are very long, averaging 37,445.60 characters, but they are structured
as many short `Passage N:` encyclopedia entries. Current diagnostics show BM25
as the strongest top-10 ranker, `reranking_hybrid` as the best top-100 coverage
profile, and dense retrieval as useful but weaker than lexical entity matching.

## Details

### What the Original Data Measures

2WikiMultiHopQA was introduced as a multi-hop QA dataset built from Wikipedia
and Wikidata. It uses evidence triples and question templates to create
questions requiring comparison, inference, compositional reasoning, and bridge
or bridge-comparison reasoning. LongEmbed adapts this kind of data into a
long-context retrieval benchmark: the question is the query and the
Wikipedia-derived passage bundle is the document to retrieve.

This means the task is not merely "find a passage that contains the answer."
The positive document contains a bundle of entity passages, including bridge
entities and final-answer evidence. A retriever must identify the document that
contains the right chain, even though the document also contains many distractor
passages.

### Observed Data Profile

The Nano split contains 200 queries, 300 documents, and 200 positive qrel rows.
Every query has exactly one positive, with no multi-positive queries. Queries
average 67.52 characters. Documents average 37,445.60 characters.

Representative questions ask which film has the older director, where a
director studied, who is a queen's mother-in-law, where a spouse was born, or
where a spouse died. The documents are bundles of short encyclopedia snippets
about people, films, places, and related entities. This structure makes entity
names and relation clues highly important.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 300-document corpus and
achieves nDCG@10 = 0.9503, hit@10 = 0.9800, and recall@100 = 0.9900. BM25 is
the strongest observed top-10 ranker. The high score reflects the entity-heavy
question style: person names, film titles, family relations, and location names
often appear directly in the positive passage bundle.

This is an important nuance for researchers. Although the original QA task
requires multi-hop reasoning, the retrieval task can often be solved by finding
the bundle containing the right surface entities. BM25 does not reason through
the chain, but exact entity overlap is a very strong candidate signal.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset covers 300 documents per query
and achieves nDCG@10 = 0.8400, hit@10 = 0.9050, and recall@100 = 0.9650. Dense
retrieval is strong but clearly below BM25. A single embedding for a long bundle
can capture general topical and entity similarity, but it may blur the exact
entities and bridge relations needed for the question.

Dense retrieval can help when relation phrasing differs or when a bridge entity
is implied rather than directly repeated. Its lower top-10 performance suggests
that preserving exact names and titles is more important than broad semantic
similarity for this Nano split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.9111, hit@10 = 0.9550,
and recall@100 = 1.0000. Hybrid retrieval improves substantially over dense and
achieves full top-100 positive coverage, but it does not surpass BM25's
top-10 ranking.

The hybrid pattern is useful for long-context retrieval. BM25 contributes
entity and title exactness. Dense retrieval contributes relation-level and
semantic evidence when exact overlap is incomplete. Together they produce the
most reliable candidate pool, while final ordering still favors strong lexical
entity matching.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. Hit@10 measures whether the correct
passage bundle appears in the first ten results, nDCG@10 rewards ranking it near
the top, and recall@100 measures whether candidate generation keeps it
available for reranking.

The key metric takeaway is that this long-document multi-hop retrieval task is
lexically easy relative to other long-context tasks. BM25 is nearly saturated,
dense retrieval is lower, and hybrid retrieval is best for coverage. A system
that performs poorly here may be losing exact entity information in long
documents.

### Query and Relevance Type Tendencies

Queries are multi-hop questions involving people, films, family relations,
places, nationalities, education, death locations, or comparisons. Relevant
documents are long bundles of Wikipedia-style passages. The correct document
contains the bridge and answer evidence somewhere inside the bundle.

The task rewards models that retain entity names and relation cues across long
documents. It also rewards document representations that can focus on relevant
passages without being overwhelmed by distractors.

### Representative Failure Modes

BM25 can fail when several bundles share the same entity names or relation
words, or when the decisive bridge entity is not expressed exactly in the query.
Dense retrieval can fail by retrieving a bundle with semantically related
entities but missing the full reasoning chain. Hybrid retrieval can include the
positive but still require a reranker to verify the bridge relation.

Long-document failure modes include representation dilution and loss of exact
names in a single-vector embedding. Multi-vector or passage-aware methods may
handle these cases better.

### Training Data That May Help

Useful training data includes non-overlapping 2WikiMultiHopQA train examples,
HotpotQA-style multi-hop retrieval pairs, Wikipedia entity-linking retrieval
pairs, and hard negatives that share one bridge entity but not the full
reasoning chain. Training should include bundled passage documents with
distractors, not only isolated positive passages.

Comparable evaluation should exclude 2WikiMultiHopQA test data, Nano queries,
qrels, and positive passage bundles likely to overlap with this split.

### Model Improvement Notes

Dense retrievers should preserve exact entity identity and relation cues inside
long bundled documents. Sparse systems already perform very well, but need
robust handling of names, titles, punctuation, and case variants. Rerankers
should check that the candidate bundle supports the full multi-hop chain, not
just one entity mention.

For hybrid systems, this task supports a lexical-first candidate strategy with
dense retrieval used to fill relation-paraphrase gaps and improve recall.

## Example Data

| Query | Positive document |
| --- | --- |
| Which film has the director who is older than the other, Women'S Weapons or She Wants Me? [89 chars] | Passage 1: Scotty Fox Scott Fox is a pornographic film director who is a member of the AVN Hall of Fame. Awards 1992 AVN Award – Best Director, Video (The Cockateer) 1995 AVN Hall of Fame inductee Pas... [200 / 16,726 chars] |
| Where did the director of film Crd (Film) study? [48 chars] | Passage 1: Peter Levin Peter Levin is an American director of film, television and theatre. Career Since 1967, Levin has amassed a large number of credits directing episodic television and television... [200 / 27,463 chars] |
| Who is the mother-in-law of Queen Insun? [40 chars] | Passage 1: Maria Thins Maria Thins (c. 1593 – 27 December 1680) was the mother-in-law of Johannes Vermeer and a member of the Gouda Thins family. She was raised in a devout Dutch Catholic family with... [200 / 43,300 chars] |
| What is the place of birth of Frankie Bridge's husband? [55 chars] | Passage 1: Wayne Bridge Wayne Michael Bridge (born 5 August 1980) is an English former professional footballer who played as a left back. A graduate of the Southampton academy, he made his debut in 19... [200 / 55,577 chars] |
| Where did Elisabeth Zu Fürstenberg's husband die? [49 chars] | Passage 1: Virginia von Fürstenberg Princess Virginia Maria Clara von und zu Fürstenberg (Virginia Maria Clara Prinzessin von und zu Fürstenberg; 5 October 1974 – 10 May 2023) was an Italian artist, p... [200 / 39,248 chars] |

### Public Sources

- [Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps](https://arxiv.org/abs/2011.01060),
  2020.
- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096),
  2024.
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed), source
  dataset card.
- [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps | 2020 | arXiv paper | [https://arxiv.org/abs/2011.01060](https://arxiv.org/abs/2011.01060) |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | [https://arxiv.org/abs/2404.12096](https://arxiv.org/abs/2404.12096) |
| dwzhu/LongEmbed | 2024 | dataset card | [https://huggingface.co/datasets/dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A comparison question asking which film has the older director. | A bundled document containing passages about the two films and directors. |
| A question asking where the director of a film studied. | A bundle containing the film and director entity passages. |
| A family-relation question about Queen Insun's mother-in-law. | A bundle with related royal and family entity passages. |
| A question asking the birthplace of Frankie Bridge's husband. | A bundle containing the spouse and birthplace evidence. |
| A question asking where Elisabeth zu Fürstenberg's husband died. | A bundle with spouse, biography, and death-location evidence. |
