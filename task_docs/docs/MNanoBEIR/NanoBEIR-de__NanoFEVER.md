# MNanoBEIR / NanoBEIR-de / NanoFEVER

## Overview

NanoBEIR-de / NanoFEVER is the German NanoBEIR version of FEVER, the
Wikipedia-based fact extraction and verification benchmark introduced in
[FEVER: a large-scale dataset for Fact Extraction and
VERification](https://arxiv.org/abs/1803.05355). Each query is a German
translated factual claim, and the retrieval target is a German translated
Wikipedia passage containing evidence needed to support or refute that claim.
The Nano task contains 50 claims, 4,996 evidence candidates, and 57 positive
qrels. Most claims have one positive, with a small multi-positive tail. BM25 is
already strong because many claims expose entity names, dense retrieval is the
best top-rank signal, and `reranking_hybrid` reaches complete Recall@100.

## Details

### What the Original Data Measures

FEVER evaluates fact verification over Wikipedia. Claims are labeled as
supported, refuted, or not enough information, and evidence sentences are
annotated for supported/refuted claims. In retrieval evaluation, the first
requirement is to retrieve the evidence passage that would allow a verifier to
judge the claim.

The German NanoBEIR version keeps this claim-to-evidence objective in
translated form. The retriever does not decide the truth label directly; it
ranks Wikipedia-style passages. A relevant passage contains the factual
relation needed for verification.

### Observed Data Profile

The metadata records 50 queries, 4,996 documents, and 57 positive qrels.
Queries average 1.14 positives; 6 queries have multiple positives. Query text
averages 52.60 characters, and documents average 1,308.21 characters. Examples
include claims about Keith Godchaux and the Grateful Dead, Taarak Mehta Ka
Ooltah Chashmah as a sitcom, aircraft manufactured in Burbank, Nero as a
person, and Scream 2 not being a purely German film.

The task is mostly entity-centered. The positive document is often a biography,
work page, place page, or organization page. However, the retriever must find
the page containing the specific fact, not merely a page that shares a name.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.7362, hit@10 = 0.9200, and
Recall@100 = 0.9825. BM25 performs well because many German translated claims
preserve entity names, titles, and key phrases from the evidence page. Exact
lexical overlap is a strong first-stage signal.

BM25's limitation is relation selection. A passage can share the same entity
but fail to contain the fact needed for verification. Claims about a date,
family relation, work type, location, or membership require more than matching
the entity string.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.8449, hit@10 = 0.9800, and Recall@100 = 0.9825. Dense retrieval is the best
top-rank signal and ties BM25 on Recall@100. This shows that embedding
similarity helps connect short German claims to the evidence passage, even
when the relevant relation is phrased differently.

Dense retrieval's risk is same-entity or same-topic drift. It can retrieve a
related page about the right entity family without containing the decisive
fact. In this sample, however, dense ordering is clearly stronger than BM25.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.8004, hit@10 =
0.9800, and Recall@100 = 1.0000. Hybrid is slightly weaker than dense on
nDCG@10 but provides complete top-100 coverage. It has exactly 100 candidates
per query and no rank-101 safeguard rows.

For reranker experiments, hybrid is the safest candidate source. It preserves
the dense top-rank advantages while ensuring every judged positive appears in
the reranking pool.

### Metric Interpretation for Model Researchers

NanoFEVER-de is a high-performing fact-evidence retrieval task. BM25 is already
strong because entity anchors are visible. Dense retrieval improves top-rank
quality substantially. Hybrid is best for candidate coverage. A model that
beats dense on nDCG@10 while preserving hybrid-like Recall@100 would be a
meaningful improvement.

Because the task is mostly single-positive, top-rank mistakes are costly.
Failures should be inspected for wrong relation, wrong entity page, or
translation-induced title mismatch.

### Query and Relevance Type Tendencies

Queries are short German factual claims. They often contain names of people,
shows, films, places, bands, offices, or historical entities. Relevant
documents are Wikipedia-style passages containing evidence for the claim.

Lexical-heavy cases involve exact names and titles. Dense-heavy cases involve
claims whose relation is expressed differently in the evidence. Hybrid
retrieval is useful when exact entity preservation and semantic relation
matching are both needed.

### Representative Failure Modes

BM25 can retrieve a page that shares the entity but lacks the target fact. Dense
retrieval can retrieve a semantically related work, person, or place but miss
the verifying relation. Both can confuse titles, alternate names, or nearby
entities. Hard negatives should come from the same entity neighborhood and
contain plausible but non-verifying facts.

### German-Specific Notes

German FEVER retrieval involves translated entity names, compound words,
foreign titles, and long evidence passages. Sparse retrieval needs to preserve
proper nouns and titles. Dense retrieval needs German encyclopedic factual
coverage. Translation variation can affect media titles and named entities, so
models should not rely on a single surface form.

### Training and Leakage Notes

Training should exclude FEVER, BEIR, or NanoBEIR records likely to overlap
with these evaluation claims or evidence passages. Useful non-overlapping data
includes FEVER claim-evidence pairs, German or multilingual fact-checking
datasets, Wikipedia claim verification retrieval, and entity-centric factual
retrieval pairs.

### Model Improvement Hints

The main improvement target is relation-aware evidence ranking. First-stage
retrievers should preserve entity anchors while using dense matching to rank
the passage that verifies the claim. Rerankers should be trained with
same-entity wrong-relation negatives.

### Training Data That May Help

Useful training data includes non-overlapping FEVER examples, German Wikipedia
fact-checking data, multilingual claim verification retrieval, entity-centric
QA evidence retrieval, and synthetic factual claims over Wikipedia-style
passages.

### Synthetic Data Guidance

Generate German factual claims from non-evaluation Wikipedia passages. Cover
dates, offices, ranks, biographies, works, family relations, nationalities, and
entity classifications. Positives should contain explicit evidence for
verification; hard negatives should mention the same entity while omitting the
target fact.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux kannte die Grateful Dead. [40 chars] | Die Grateful Dead war eine US-amerikanische Rockband, die 1965 in Palo Alto, Kalifornien, gegründet wurde. Die Besetzung variierte zwischen Quintett und Septett. Die Band ist für ihren einzigartigen und eklektischen Stil bekannt, der Elemente von Rock, Psychedelia, experimenteller Musik, Modaljazz, Country, Folk, Bluegrass, Blues, Reggae und Space Rock verband. Sie waren bekannt für ihre langen instrumentalen Jams bei Live-Auftritten und ihre treue Fangemeinde, die als „Deadheads“ bekannt ist. Ihre Musik, schreibt Lenny Kaye, „berührt Bereiche, die die meisten anderen Bands nicht einmal kennen“. Diese verschiedenen Einflüsse wurden zu einem vielfältigen und psychedelischen Ganzen destilliert, das die Grateful Dead zu den „Pionieren der Jam-Band-Welt“ machte. Das Magazin Rolling Stone setzte die Band auf Platz 57 in seiner Liste der „Greatest Artists of All Time“. Die Band wurde 1994 in die Rock and Roll Hall of Fame aufgenommen, und eine Aufnahme ihres Konzerts vom 8. Mai 1977 in der B... [1,000 / 3,134 chars] |
| Taarak Mehta Ka Ooltah Chashmah ist eine Sitcom. [48 chars] | Taarak Mehta Ka Ooltah Chashmah (englisch: Taarak Mehtas andere Perspektive) ist die am längsten laufende Sitcom-Serie in Indien, produziert von Neela Tele Films Private Limited. Die Serie wurde erstmals am 28. Juli 2008 ausgestrahlt. Sie wird von Montag bis Freitag um 20:30 Uhr gesendet, mit Wiederholungen um 23:00 Uhr und am nächsten Tag um 15:00 Uhr auf SAB TV. Die Wiederholung der Serie begann am 2. November 2015 um 16:30 Uhr und 20:00 Uhr täglich auf Sony Pal. Die Serie basiert auf der Kolumne "Duniya Ne Oondha Chashma", geschrieben von dem Kolumnisten und Journalisten Taarak Mehta für die wöchentliche Gujarati-Zeitschrift Chitralekha. [648 chars] |
| In Burbank, Kalifornien, wurden geheime, hochentwickelte Flugzeuge hergestellt. [79 chars] | Burbank ist eine Stadt im Los Angeles County in Südkalifornien, Vereinigte Staaten, etwa 12 Meilen nordwestlich des Stadtzentrums von Los Angeles. Bei der Volkszählung im Jahr 2010 betrug die Einwohnerzahl 103.340. Burbank wird als „Medienhauptstadt der Welt“ bezeichnet und liegt nur wenige Meilen nordöstlich von Hollywood. Zahlreiche Medien- und Unterhaltungsunternehmen haben hier ihren Hauptsitz oder bedeutende Produktionsstätten, darunter The Walt Disney Company, Warner Bros. Entertainment, Nickelodeon Animation Studios, NBC, Cartoon Network Studios mit dem Westküsten-Standort von Cartoon Network und Insomniac Games. Die Stadt ist auch Heimat des Bob Hope Airports. Sie war der Standort der Lockheed Skunk Works, die einige der geheimsten und technologisch fortschrittlichsten Flugzeuge produzierte, darunter die U-2-Spionageflugzeuge, die im Oktober 1962 sowjetische Raketenkomponenten in Kuba aufdeckten. Burbank besteht aus zwei unterschiedlichen Gebieten: einem Stadtzentrum/Fußhügelbe... [1,000 / 1,480 chars] |

### Public Sources

- [FEVER: a large-scale dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355), 2018.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a large-scale dataset for Fact Extraction and VERification | 2018 | task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
