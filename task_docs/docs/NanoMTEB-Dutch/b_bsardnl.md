# NanoMTEB-Dutch / b_bsardnl

## Overview

`NanoMTEB-Dutch / b_bsardnl` is the Dutch bBSARD statutory article retrieval
task. Queries are plain-language Dutch legal questions, and documents are Dutch
Belgian statutory articles. The Nano split has 200 queries, 10,000 documents,
and 923 positive qrel rows. It is a multi-positive legal retrieval task,
averaging 4.62 relevant articles per query. Current diagnostics show dense
retrieval as the strongest top-rank profile, `reranking_hybrid` as slightly
stronger by recall@100, and BM25 as weak because lay questions rarely repeat
formal statutory wording.

## Details

### What the Original Data Measures

Bilingual BSARD extends Belgian Statutory Article Retrieval to Dutch by using
parallel French and Dutch Belgian statutory articles and Dutch translations of
citizen legal questions. MTEB-NL includes bBSARDNLRetrieval as a native Dutch
legal retrieval task.

The task measures statutory article retrieval from lay legal questions. A model
must connect everyday legal concerns to formal legal provisions, article
numbers, definitions, exceptions, and procedural requirements.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 923 positive qrel
rows. The average positives per query is 4.62, with a minimum of 1, median of
2, and maximum of 57. A total of 62.50% of queries have multiple positives.
Queries average 93.85 characters, while documents average 863.16 characters.

Queries are short citizen-style legal questions about rent, legal aid, court
costs, repairs, testament changes, Belgian regional housing law, water bills,
bankruptcy, and procedure. Documents are Dutch statutory articles with article
numbers, paragraphs, legal conditions, and cross-references.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.1249, hit@10 = 0.2950, and recall@100 = 0.3402. BM25 is
weak despite the shared Dutch language.

The weakness comes from the mismatch between lay wording and legal text.
Questions ask in ordinary language, while statutes use formal terminology,
defined concepts, article structure, and procedural phrasing. Exact token
overlap is often insufficient to find all relevant provisions.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.2749, hit@10 = 0.5350, and recall@100 = 0.4464.
Dense retrieval is the strongest observed top-rank profile.

This suggests that semantic matching helps map lay legal questions to statutory
conditions. Dense retrieval can connect concepts like tenant repairs, testament
changes, court costs, legal aid, or water invoices to formal provisions even
when terms differ.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 42 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.2234, hit@10 = 0.4500, and recall@100 = 0.4518. Hybrid retrieval slightly
exceeds dense retrieval on recall@100 but is below dense retrieval on nDCG@10
and hit@10.

This makes hybrid search useful for candidate coverage, especially when exact
legal terms identify some relevant articles. However, sparse evidence can also
pull in formal but inapplicable provisions, so top-rank ordering needs legal
semantic reranking.

### Metric Interpretation for Model Researchers

This is a multi-positive task. nDCG@10 rewards ranking several relevant
statutory articles early, while hit@10 only checks whether at least one relevant
article appears near the top. Recall@100 measures whether the legal article set
remains available to a reranker.

Because some questions have many positives, training and evaluation should
preserve the relevant article set rather than forcing a single answer article.
Low recall@100 indicates that candidate generation itself is still difficult.

### Query and Relevance Type Tendencies

Queries are plain Dutch legal questions from a citizen perspective. Relevant
documents are Belgian statutory articles in Dutch. The answer may require one
article or a group of related provisions.

The task rewards legal concept mapping, statutory terminology understanding,
and multi-article retrieval. It penalizes models that only match isolated legal
keywords.

### Representative Failure Modes

BM25 can miss articles when the query uses everyday terms and the statute uses
formal vocabulary. Dense retrieval can find the right legal theme but miss a
specific jurisdiction, exception, date, or procedure. Hybrid retrieval can
retrieve nearby articles in the same code while omitting some relevant
supporting provisions.

Rerankers should compare legal conditions, jurisdiction, actor, obligation,
exception, and procedural role against the query.

### Training Data That May Help

Useful training data includes non-overlapping bBSARD train retrieval pairs,
Dutch statutory article retrieval data, Belgian legal QA and legal-aid
question-answer pairs, and French-Dutch parallel legal retrieval data with
overlap removed. The bBSARD Dutch test questions, qrels, and positive statutory
articles used by this Nano split should be excluded from training.

Synthetic data can generate layperson Dutch legal questions from non-evaluation
statutory articles. Questions should paraphrase article conditions,
exceptions, dates, jurisdiction, and procedures. Multi-positive examples should
include coherent groups of related legal articles with hard negatives from
nearby article numbers.

### Model Improvement Notes

Dense retrievers should improve lay-to-legal semantic mapping and statutory
condition matching. Sparse systems need legal query expansion and field-aware
indexing. Rerankers should evaluate article-level legal grounding and handle
multi-positive answer sets.

For hybrid systems, `NanoMTEB-Dutch / b_bsardnl` is a mixed case: hybrid search
slightly improves recall@100, but dense retrieval gives stronger top-rank
quality. Better legal reranking is needed to use hybrid coverage effectively.

## Example Data

| Query | Positive document |
| --- | --- |
| Ik huur het hele jaar door een caravan op een camping. Welke regels zijn van toepassing op mijn huurcontract in Brussel? [120 chars] | Art. 234. - Beginselen Dit hoofdstuk is van toepassing op huurovereenkomsten betreffende een woning die de huurder, met uitdrukkelijke of stilzwijgende toestemming van de verhuurder, vanaf de ingenottreding tot zijn hoofdverblijfplaats bestemt. Het beding dat de bestemming van het goed als hoofdverblijfplaats van de huurder verbiedt en dat niet uitdrukkelijk noch ernstig kan worden gestaafd, onder meer door elementen met betrekking tot de natuurlijke bestemming van het goed, en waarin de hoofdverblijfplaats van de huurder tijdens de huurovereenkomst niet is vermeld, wordt voor niet geschreven gehouden. Dit hoofdstuk is tevens van toepassing indien de woning, met de schriftelijke toestemming van de verhuurder, in de loop van de huurovereenkomst tot hoofdverblijfplaats wordt bestemd. In dat geval, neemt de huurovereenkomst een aanvang op de dag waarop deze toestemming is verleend. Dit hoofdstuk is van toepassing op de onderverhuring aangegaan overeenkomstig artikel 230, en binnen de gren... [1,000 / 1,287 chars] |
| Ik heb een testament gemaakt. Kan ik het wijzigen? [50 chars] | Art. 969. Een testament kan eigenhandig, of bij openbare akte of in de vorm van het internationaal testament, gemaakt worden. [125 chars] |
| Moet ik de gerechtskosten betalen als ik een beslissing van een sociale zekerheidsinstelling betwist? [101 chars] | Art. 1017. Tenzij bijzondere wetten anders bepalen, verwijst ieder eindvonnis, zelfs ambtshalve, de in het ongelijk gestelde partij in de kosten, onverminderd de overeenkomst tussen partijen, die het eventueel bekrachtigt. Niettemin worden nutteloze kosten, met inbegrip van de rechtsplegingsvergoeding bedoeld in artikel 1022, zelfs ambtshalve ten laste gelegd van de partij die ze foutief heeft veroorzaakt Behalve wanneer het geding roekeloos of tergend is, wordt de overheid of de instelling belast met het toepassen van de wetten en verordeningen : 1° bedoeld in de artikelen 579, 6°, 579, 7°, 580, 581 en 582, 1° en 2°, ter zake van vorderingen ingesteld door of tegen de sociaal verzekerden persoonlijk, steeds in de kosten verwezen; 2° betreffende de sociale zekerheid van het statutair personeel van de openbare sector die gelijkwaardig zijn met de in de bepaling onder 1° bedoelde wetten en verordeningen betreffende de sociale zekerheid van werknemers, ter zake van vorderingen ingesteld d... [1,000 / 1,690 chars] |

### Public Sources

- [Bilingual BSARD: Extending Statutory Article Retrieval to Dutch](https://arxiv.org/abs/2412.07462),
  2025.
- [Bilingual BSARD ACL Anthology record](https://aclanthology.org/2025.regnlp-1.3/).
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340),
  2025.
- [clips/mteb-nl-bbsard](https://huggingface.co/datasets/clips/mteb-nl-bbsard).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Bilingual BSARD: Extending Statutory Article Retrieval to Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2412.07462](https://arxiv.org/abs/2412.07462) |
| Bilingual BSARD: Extending Statutory Article Retrieval to Dutch | 2025 | proceedings page | [https://aclanthology.org/2025.regnlp-1.3/](https://aclanthology.org/2025.regnlp-1.3/) |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |
| clips/mteb-nl-bbsard |  | dataset card | [https://huggingface.co/datasets/clips/mteb-nl-bbsard](https://huggingface.co/datasets/clips/mteb-nl-bbsard) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Dutch legal question about a year-round caravan rental in Brussels. | A statutory article about housing rental principles and scope. |
| A question asking whether a made testament can be changed. | A statutory article about forms and rules for testaments. |
| A question about court costs when contesting a social-security institution. | A procedural article about costs in judgments. |
| A Brussels tenant-repair question. | A statutory article about tenant repairs and maintenance. |
| A question about understanding a water bill in Wallonia. | A regulatory article about required invoice information. |
