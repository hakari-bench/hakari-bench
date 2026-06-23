# NanoMLDR / fr

## Overview

`NanoMLDR / fr` is the French split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. French paragraph-grounded questions
retrieve full French documents, where the answer-bearing paragraph may be only
one small part of a long article. The Nano split has 152 queries, 3,059
documents, and 152 positive qrel rows, with exactly one positive document per
query. Current diagnostics show BM25 as the strongest top-rank profile,
`reranking_hybrid` as matching BM25 on recall@100, and dense retrieval as useful
but weaker than lexical retrieval.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The positive is the full document containing the answer-bearing paragraph.

For French, this means the task is paragraph-to-document retrieval over long
French articles. A system must identify the containing article even when the
question targets a local fact in one section rather than the main title or
overall article theme.

### Observed Data Profile

The Nano split contains 152 queries, 3,059 documents, and 152 positive qrel
rows. Every query has exactly one positive document. Queries average 119.92
characters, while documents average 11,534.15 characters.

Observed examples include French questions about sports results, X-Men character
interpretation, ferry crossing time, a footballer's loss of a national-team
place, Formula 1 car modifications, charitable orders, theater, comics, and
Jewish community history. The questions are usually specific and retain
distinctive terms from the answer paragraph.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9125, hit@10 = 0.9408, and recall@100 = 0.9868. BM25 is
the strongest observed top-rank profile. The long French questions often
include names, events, titles, organizations, or technical terms that also occur
in the positive article.

This split demonstrates how strong lexical retrieval can be for generated
long-document questions. Even though the positive document is long, article-
specific vocabulary gives BM25 enough evidence to rank the correct document
highly.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7706, hit@10 = 0.8421, and recall@100 = 0.9211.
Dense retrieval is useful but weaker than BM25. It captures broad semantic
similarity but can miss the exact long document when several French articles
share the same cultural, sports, historical, or technical topic.

The core problem is granularity. The question is grounded in one paragraph, but
the dense representation summarizes the full document. Local evidence can be
diluted by the rest of the article.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.8421, hit@10 = 0.9145, and recall@100 = 0.9868. Hybrid retrieval matches BM25
on recall@100 but remains below BM25 on nDCG@10 and hit@10.

This means hybrid search is useful as a robust candidate source, but BM25 is
still the best observed ranker. Dense candidates help maintain coverage, while
exact French lexical evidence remains the most reliable top-rank signal.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether the positive appears near the top. nDCG@10 is
sensitive to the positive's rank, and recall@100 measures whether it remains in
the reranking candidate pool.

The French MLDR profile rewards systems that preserve paragraph-derived lexical
anchors inside long documents. Dense retrieval should be evaluated against a
strong BM25 baseline, and hybrid systems should avoid degrading BM25's high
top-rank precision.

### Query and Relevance Type Tendencies

Queries are long French questions about sports events, films and comics,
transport routes, biographies, car engineering, community history, theater, and
cultural institutions. They often mention multiple named entities or a detailed
condition from the source paragraph.

Relevant documents are long French articles containing the answer-bearing
paragraph. The task rewards exact named-entity matching, long-document indexing,
and paragraph-level evidence recognition inside full documents.

### Representative Failure Modes

Dense retrieval can return a thematically related article but miss the exact
document containing the paragraph. Long articles about the same film, sports
season, port, athlete, or racing car can be semantically close. BM25 can fail
when a detailed question shares names with several articles or when the answer
paragraph is phrased differently.

Hybrid retrieval can preserve the positive in the candidate pool but still rank
a near-topic article too high. Rerankers should examine chunks or paragraphs,
not just full-document summaries.

### Training Data That May Help

Useful training data includes French long-document QA retrieval pairs, French
Wikipedia article retrieval, multilingual MLDR training data outside this Nano
split, and same-entity French article hard negatives. Training should include
full documents where a local paragraph determines relevance.

Synthetic data can help when it samples paragraphs from long French
encyclopedic articles, generates paragraph-grounded French questions, and uses
the full article as the positive. Negatives should be full articles in the same
topical area but missing the answer paragraph.

### Model Improvement Notes

Dense retrievers should use chunked indexing, paragraph-aware aggregation, late
interaction, or multi-vector document representations to avoid losing local
answer evidence. Sparse systems should retain exact French terms and names
while improving robustness to paraphrase and inflection. Rerankers should
validate against BM25 because lexical retrieval is very strong here.

For hybrid systems, `NanoMLDR / fr` supports BM25-first candidate generation
with dense retrieval as a recall supplement. The current hybrid profile matches
BM25 recall but does not surpass BM25 ranking quality.

## Example Data

| Query | Positive document |
| --- | --- |
| Quels sont les résultats des huitièmes de finale de la Coupe de France et de la Coupe UEFA ? [92 chars] | Cette page concerne l'actualité sportive du mois de . Mardi mars Football : surprises à l'occasion des huitièmes de finale de la Coupe de France. Clermont Foot, modeste seizième en Ligue 2, sort l'Olympique lyonnais, leader de Ligue 1, aux tirs au but après un match nul 1-1 arraché dans les arrêts de jeu par Sylvain Wiltord. Nîmes Olympique (National) poursuit également sa route en éliminant un troisième sociétaire de Ligue 1 : OGC Nice. Le score est sans appel, 4-0! Troisième match au programme ce soir : Sedan (L1) élimine logiquement l'US Quevilly (CFA) par 2-0. Le match US Boulogne - FC Nantes est reporté en raisons des mauvaises conditions météo. Suite du programme demain avec notamment le choc Auxerre – Paris Saint-Germain. Mercredi 2 mars Football : suite des huitièmes de finale de la Coupe de France. Monaco élimine Rennes (0-1 après prolongation) et Sochaux s'impose logiquement à Albi (0-3). Surprise à Lille avec la victoire du sociétaire de Ligue 2, Grenoble : 1-3! Le choc Auxe... [1,000 / 24,419 chars] |
| Quel est le lien entre les personnages Xavier et Magnéto et les figures historiques de Martin Luther King et Malcolm X dans le projet proposé par Bryan Singer et Tom DeSanto à la Fox en 1998? [191 chars] | X-Men est un film américain réalisé par Bryan Singer, sorti en 2000. C'est le premier film de la série X-Men mettant en scène les personnages de la série de comics X-Men de Marvel Comics, créés par le scénariste Stan Lee et le dessinateur Jack Kirby. Le film marque le début de la saga cinématographique X-Men. Résumé Pologne, 1944. Un groupe de prisonniers juifs est conduit vers un camp nazi où une sinistre sélection met d'un côté un jeune adolescent et de l'autre le restant de sa famille. Comprenant leur funeste destin, le garçon, agissant par instinct, veut rejoindre ses parents mais les gardes ne peuvent l'emmener, son corps étant bloqué par l'attraction magnétique qui le lie aux portes du camp de la mort. Ce n'est qu'une fois assommé que le garçon est emmené alors que ses proches sont exterminés. Des années plus tard, aux États-Unis, un vieil homme quitte en colère une assemblée où le sénateur Robert Kelly prône une loi pour l'identification et l'enfermement des mutants dont l'exist... [1,000 / 22,611 chars] |
| Quel est le temps de traversée entre Ouistreham et Portsmouth en utilisant la ligne de ferry de Brittany Ferries ? [114 chars] | Le port de Caen-Ouistreham est un port de commerce, un port passager et un port de plaisance français s'étendant sur le canal de Caen à la mer depuis l'embouchure de l'Orne à Ouistreham jusqu'à la ville de Caen, dans le département du Calvados et la région Normandie. Il reste aussi un port de pêche artisanale et côtière. Histoire Du Moyen Âge à l'époque moderne Au , un vicus se constitue sur les bords de l'Odon à l'emplacement de l'actuelle abbaye aux Hommes. Des fouilles menées dans les années 1970 ont montré qu'après l'échec d'une première tentative pour stabiliser les berges de la rivière un canal a été creusé d'est en ouest à travers le bourg. Ce canal avait pour but d'assainir le terrain, mais il est probable que les berges aménagées de ce canal tenaient également lieu d'installations portuaires sommaires. Le cabotage jusqu'à l'Orne assuré par des barques à fond plat devaient permettre l'échange de produits locaux. Les différents bourgs dispersés dans la vallée de l'Orne connaisse... [1,000 / 22,300 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A French question about sports round-of-16 results. | A long sports-news or monthly-sports article. |
| A question about X-Men characters and historical figures. | A long article about the X-Men film. |
| A question about ferry crossing time. | A long article about the Caen-Ouistreham port. |
| A question about why a footballer lost his national-team place. | A long biography of Bernard Lama. |
| A question about Formula 1 car modifications. | A long article about the Lola T97/30. |
