# NanoMTEB-Dutch / vabb

## Overview

`vabb` is a Dutch and Flemish academic-bibliography retrieval task from
MTEB-NL. Queries are publication titles, and documents are bibliographic
records or abstract-like descriptions from the Flemish Academic Bibliography
for the Social Sciences and Humanities. The Nano split contains 200 queries,
9,123 documents, and 200 positive qrel rows, with exactly one positive record
per query.

The task measures exact publication retrieval in humanities and social-science
metadata. BM25 is strong because titles often share keywords with the
bibliographic record, but dense retrieval with `harrier_oss_v1_270m` is
stronger in nDCG@10, hit@10, and recall@100. `reranking_hybrid` has the highest
recall@100 but a weaker top order than dense. The task is useful for evaluating
academic title-to-record retrieval where titles can be metaphorical,
multilingual, or much shorter than the description.

## Details

### What the Original Data Measures

The [VABB-SHW Zenodo record](https://zenodo.org/records/14214806) describes the
Flemish Academic Bibliography for the Social Sciences and Humanities as a
database of approved publications by researchers affiliated with Flemish
universities. MTEB-NL uses this source to build a retrieval task by matching
publication titles to corresponding abstracts or bibliographic descriptions.
No standalone retrieval paper for this exact task was confirmed.

This is not question answering or claim verification. It is bibliographic
record retrieval: given a title, find the matching publication record among
academic metadata and abstract-like descriptions.

### Observed Data Profile

The split contains 200 title queries over 9,123 documents. Queries average
74.47 characters, and documents average 837.89 characters. Titles may be in
Dutch, English, French, Latin, or mixed academic style. Documents may include
authors, publication year, discipline, abstract text, or descriptive metadata.

Representative examples cover administrative-law principles, punishment theory,
social-law codes, the filmmaker Raoul Servais, and museum policy reactions.
Some positive documents are concise records, while others are long descriptive
entries. The retrieval target is one exact record.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.6952, hit@10 = 0.7850, and recall@100 = 0.8650 over
top-500 candidate lists. This is a strong lexical baseline. Many publication
titles repeat important disciplinary terms that appear in the record, and
named entities or book titles can be highly distinctive.

BM25's weakness appears when titles are metaphorical, abbreviated, multilingual,
or conceptually broader than the record description. Humanities and social
science titles can be expressive rather than literal. BM25 may also confuse
records from the same author, discipline, or keyword neighborhood.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.7804, hit@10 =
0.8500, and recall@100 = 0.9000. Dense retrieval is the strongest top-ranked
candidate source. It improves over BM25 by matching title meaning to abstract
or metadata descriptions even when exact wording differs.

Dense retrieval is useful for title-to-abstract semantics, but it still has to
distinguish exact records from same-discipline neighbors. The single-positive
setup makes near misses costly: a related publication is not relevant unless it
is the exact title's record.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.7540, hit@10 =
0.8350, and recall@100 = 0.9200, with 100 to 101 candidates per query and 16
rank-101 safeguard rows. Hybrid retrieval has the best recall@100, while dense
retrieval has the best top order.

This pattern suggests that lexical and dense signals are complementary for
candidate generation. BM25 can preserve exact title words and names; dense
retrieval can connect title semantics to abstract descriptions. A reranker can
then select the exact publication record.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 directly reflects the rank of the
matching bibliographic record. Hit@10 approximates whether the user sees the
right record quickly, and recall@100 measures candidate coverage. Dense
retrieval is the best first-stage ranker, but hybrid search is a better
candidate source for reranking.

The task is a useful check on title-to-document semantics in academic metadata,
especially for humanities titles that are less keyword-like than STEM paper
titles.

### Query and Relevance Type Tendencies

Queries are publication titles. Relevant documents are exact matching records
or abstract-like descriptions. The corpus includes humanities and social
science material, where titles may include proper names, legal terms,
historical periods, or discipline-specific phrases.

Relevance is record identity. A document about the same author, topic, or
discipline is not enough unless it is the matching publication.

### Representative Failure Modes

BM25 can fail on metaphorical or multilingual titles. Dense retrieval can fail
by retrieving a semantically related academic record that is not the exact
publication. Hybrid retrieval can include similar-title or same-discipline
records that require reranking.

Hard negatives should come from the same author, discipline, publication year,
or title keyword cluster. These are the realistic confusions in bibliographic
search.

### Training Data That May Help

Useful training data includes non-overlapping title-to-abstract academic
bibliography pairs, Dutch and Flemish library or publication metadata retrieval
data, citation and publication recommendation pairs, and same-discipline hard
negatives. Training should exclude VABB evaluation titles, bibliographic
records, abstracts, and qrels used by this Nano split.

Synthetic data can be created from academic bibliographic records with authors,
year, discipline, and abstract-like descriptions. Use the publication title as
the query and include similar-title or same-discipline negatives.

### Model Improvement Notes

Improving this task requires exact-record retrieval with semantic title
understanding. Dense models should learn to connect titles to abstracts while
preserving bibliographic identity. Rerankers should compare title, author,
topic, and description to avoid selecting a nearby but different publication.

Hybrid search is useful for reranking, but dense retrieval currently gives the
best initial top ranking.

## Example Data

| Query | Positive document |
| --- | --- |
| De polsstokwerking van de beginselen van behoorlijk bestuur: export en reflexwerking? [85 chars] | Deze bijdrage omvat een analyse van de toepassing van de beginselen van behoorlijk bestuur op het privaatrechtelijk handelen van de overheid, bekeken vanuit het perspectief van publicisten. [189 chars] |
| Het leedprincipe, het strafbegrip en de schuld zonder straf. De fixatie op leedtoevoegende straffen... [100 / 117 chars] | Volgens velen kenmerkt het strafrecht zich door het feit dat het leidt tot het opleggen van een straf. Vanuit dit oogpunt wordt het strafrecht te snel en te gemakkelijk gereduceerd tot straffen, en du... [200 / 1,499 chars] |
| Bamacodex 4 Sociaalrecht 2009-10 [32 chars] | De Bamacodex 4 "Sociaalrecht" biedt een selectie aan, met zorg uitgevoerd, van de belangrijkste en geupdated wetten en besluiten in de domeinen van het arbeidsrecht en het socialezekerheidsrecht. Onde... [200 / 270 chars] |
| Raoul Servais. De Tovenaar van Oostende [39 chars] | Context Raoul Servais, revolutionaire animatiecineast. Engagement, contestatie en erkenning Schrijven over de filmkunst van Raoul Servais is geen gemakkelijke taak. In het hierna volgende interview wo... [200 / 7,551 chars] |
| Museumstrijd. Reacties van de conservatoren [43 chars] | Naar aanleiding van onderzoek naar het beleid van erfgoedmusea in Vlaanderen aan de UGent, werden in dit artikel reacties van de conservatoren verzameld. [153 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| VABB-SHW: Dataset of Flemish Academic Bibliography for the Social Sciences and Humanities (edition 14) | 2024 | Zenodo dataset | [https://zenodo.org/records/14214806](https://zenodo.org/records/14214806) |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |
| clips/mteb-nl-vabb-ret |  | dataset card | [https://huggingface.co/datasets/clips/mteb-nl-vabb-ret](https://huggingface.co/datasets/clips/mteb-nl-vabb-ret) |
| MTEB project repository |  | repository | [https://github.com/embeddings-benchmark/mteb](https://github.com/embeddings-benchmark/mteb) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| De polsstokwerking van de beginselen van behoorlijk bestuur: export en reflexwerking? | A bibliographic description analyzes application of principles of good administration to private-law government action. |
| Het leedprincipe, het strafbegrip en de schuld zonder straf. | A description discusses how criminal law is often reduced too quickly to punishment and added suffering. |
| Bamacodex 4 Sociaalrecht 2009-10 | A record describes a curated selection of updated laws and decrees in labor and social-security law. |
| Raoul Servais. De Tovenaar van Oostende | A long record gives context on Raoul Servais as a revolutionary animation filmmaker. |
| Museumstrijd. Reacties van de conservatoren | A record describes conservators' reactions following research into Flemish heritage-museum policy. |
