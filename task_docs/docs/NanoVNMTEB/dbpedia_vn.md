# NanoVNMTEB / dbpedia_vn

## Overview

`dbpedia_vn` is the Vietnamese NanoVNMTEB version of the DBpedia-Entity retrieval task. DBpedia-Entity v2 was built as a test collection for entity search over DBpedia and Wikipedia-derived entity descriptions; VN-MTEB adapts the retrieval setting into Vietnamese. A query is usually a short entity-oriented request, and relevant documents are compact entity descriptions that satisfy the request.

The Nano split contains 200 queries, 10,000 candidate documents, and 5,754 positive qrels. Queries average 42.085 characters, and documents average 340.3752 characters. Unlike single-answer passage retrieval, this task is strongly multi-positive: the average query has 28.77 positives, and the median has 19. Dense retrieval is strongest on nDCG@10 and recall@100, while `reranking_hybrid` has the highest hit@10. The task is best understood as Vietnamese set-valued entity retrieval, where the model must rank many correct entities above same-category distractors.

## Details

### What the Original Data Measures

DBpedia-Entity v2 evaluates entity search over descriptions derived from DBpedia. It includes information needs from several sources, including entity-seeking and list-seeking queries. The retrieval target is not an arbitrary passage but an entity description, often identified by name, category, date, location, role, or membership in a set.

The Vietnamese version preserves this entity-search behavior. Queries may ask for Indian dishes, Star Trek captains, producers with many films, islands, countries, authors, presidents, bridges similar to a named bridge, or albums associated with an artist. Relevant documents are short entity abstracts containing titles and attributes. Retrieval must therefore combine entity-name matching, category matching, and semantic list membership.

### Observed Data Profile

The task has 5,754 positive judgments across 200 queries. The average positive count is 28.77, the median is 19, and 194 of 200 queries have more than one positive, giving a multi-positive rate of 97.0%. The maximum positive count is 100. This is one of the clearest multi-positive tasks in the NanoVNMTEB set.

Documents are short compared with forum or QA tasks, so the challenge is not long-context extraction. Instead, the difficulty lies in ranking many entities that share a category. A query may ask for a list of entities, and a model must retrieve a set rather than stop after the first plausible match. Same-category hard negatives are common because many entities look locally similar.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6137045546, hit@10 of 0.9600, and recall@100 of 0.5935001738 with a top-500 candidate set. The high hit@10 shows that lexical retrieval usually finds at least one relevant entity quickly. Entity names, categories, places, dates, and aliases provide strong sparse signals.

However, BM25 is weaker than dense retrieval on nDCG@10 and recall@100. List-style queries require ranking many relevant entities, and exact word overlap can favor a few obvious matches while missing semantically valid members of the set. BM25 may also over-rank documents that share the same category word but do not satisfy the full query constraint.

### Dense Evaluation Profile

Dense retrieval with `harrier-oss-270m` reaches nDCG@10 of 0.7640113769, hit@10 of 0.9650, and recall@100 of 0.7233229058. It is the strongest condition for nDCG@10 and recall@100. This indicates that embedding similarity captures entity-category and list-membership semantics better than exact lexical overlap alone.

Dense retrieval is particularly useful for queries that describe a class indirectly, such as entities similar to a named bridge, works associated with a person, or members of a geographic or cultural category. It can retrieve entities that do not repeat every query token but match the semantic set. Its risk is retrieving same-topic entities that are close in embedding space but fail a specific constraint such as date, nationality, role, or membership.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reaches nDCG@10 of 0.7247250643, hit@10 of 0.9900, and recall@100 of 0.7076816128. The top-100 candidate pool has exactly 100 candidates per query, with no safeguard-expanded rows. Hybrid retrieval finds at least one positive for almost every query, but its nDCG@10 and recall@100 remain below dense retrieval.

This shows that hybrid search improves first-hit reliability but does not automatically improve list ranking. Sparse evidence can add useful entity-name and category anchors, but it may also pull same-word distractors into the top ranks. For this task, dense retrieval better orders the large positive sets, while hybrid retrieval slightly improves hit coverage.

### Metric Interpretation for Model Researchers

Hit@10 is less discriminating here because both dense and hybrid are already near saturation. nDCG@10 and recall@100 are more informative: the task asks for many relevant entities, so ranking quality across the top set matters. Dense retrieval's advantage indicates that semantic list membership is central.

Researchers should treat this as a multi-positive entity retrieval benchmark, not a single-evidence task. Training and evaluation should reward retrieving multiple correct entities and ranking them above same-category non-relevant entities. Reducing each query to one positive would discard the main structure of the dataset.

### Query and Relevance Type Tendencies

Queries include list searches, entity descriptions, and category-based needs. Examples include bridges similar to Manhattan Bridge, Indian dishes, Star Trek captains, film producers, and albums involving John Lennon and Yoko Ono. Relevant documents are short entity abstracts with titles and compact descriptions.

Relevance depends on satisfying all constraints in the query. A document about a bridge may be irrelevant if it is not similar in the intended way. A person may be irrelevant if they share an occupation but not the requested role or period. Entity retrieval therefore requires matching both category and qualifiers.

### Representative Failure Modes

BM25 can over-rank entities with exact category words while missing entities that satisfy the list through paraphrase or description. Dense retrieval can over-rank entities in the same semantic neighborhood but with the wrong date, location, role, or relation. Hybrid retrieval can inherit both issues when sparse anchors and semantic similarity point to different parts of the entity space.

Another failure mode is first-hit complacency. A model may achieve high hit@10 while retrieving only one obvious positive and failing to cover the rest of the relevant set. For this benchmark, set coverage is part of the task.

### Training Data That May Help

Useful training data includes non-overlapping DBpedia-Entity queries, Vietnamese entity linking and entity retrieval pairs, Wikipedia or DBpedia question-to-entity data, and list-search supervision with overlap removed. Multi-positive training is especially important.

Synthetic data should generate Vietnamese entity-search queries over small pools of entity descriptions, with all matching entities labeled. Hard negatives should come from the same broad category but violate a specific constraint, such as wrong country, wrong date, wrong profession, or wrong fictional universe.

### Model Improvement Notes

The main improvement target is list-aware dense retrieval. Models should learn category membership, aliases, dates, locations, and role constraints. Sparse evidence remains useful for names and rare entities, but it should not dominate ranking when the query is semantic or list-based.

Error analysis should inspect whether missed positives are due to alias mismatch, category mismatch, qualifier mismatch, or insufficient multi-positive coverage. Reranking should optimize ordering across many relevant entities, not only whether any positive appears near the top.

## Example Data

### Public Sources

- [DBpedia-Entity v2 paper](https://doi.org/10.1145/3077136.3080751)
- [DBpedia-Entity project page](https://iai-group.github.io/DBpedia-Entity/)
- [VN-MTEB paper](https://aclanthology.org/2026.findings-eacl.86/)
- [BEIR paper](https://arxiv.org/abs/2104.08663)
- [GreenNode/dbpedia-vn](https://huggingface.co/datasets/GreenNode/dbpedia-vn)

### Source Reference Table

| Source | Role |
|---|---|
| DBpedia-Entity v2 | Original entity-search benchmark |
| DBpedia-Entity project page | Collection description and benchmark context |
| BEIR | Retrieval benchmark framing |
| VN-MTEB | Vietnamese benchmark collection using translated retrieval tasks |
| GreenNode dataset card | Public dataset entry for this Vietnamese split |

### Representative Snippets

- Query: `Những cây cầu nào giống như Cầu Manhattan?`
  Relevant documents include bridge entities with descriptions that satisfy a similarity or category-style need.
- Query: `John Lennon Yoko Ono album Starting Over`
  Relevant documents include music entities related to John Lennon, Yoko Ono, and the specified work.
- Query: `Món Ấn Độ`
  Relevant documents include Indian food entities such as regional dishes.
- Query: `Ai đã sản xuất được nhiều phim nhất?`
  Relevant documents include film producer entities.
- Query: `Các Thuyền trưởng Star Trek`
  Relevant documents include entities associated with Star Trek captains or related works.
