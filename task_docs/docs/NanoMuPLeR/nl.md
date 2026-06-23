# NanoMuPLeR / nl

## Overview

`NanoMuPLeR / nl` is the Dutch split of MuPLeR-retrieval, a multilingual legal retrieval benchmark built from European Union legal passages. Queries are synthetic Dutch legal questions, and documents are Dutch DGT-Acquis passages. Each query has one relevant passage, so the task measures exact grounding of legal facts rather than broad topical relevance. This split is notable because BM25 is extremely strong, dense retrieval is also high but weaker, and the hybrid pool reaches perfect top-100 coverage with the best early-ranking metrics.

## Details

### What the Original Data Measures

MuPLeR-retrieval evaluates multilingual parallel legal retrieval over DGT-Acquis-derived passages. The source dataset card describes 10,000 passages and 200 synthetic parallel queries per language. DGT-Acquis is part of the European Union's multilingual legal corpus resources and is documented in work on EU parallel corpora.

For Dutch, retrieval is same-language and single-positive. The model must find the exact passage that answers a legal question about a transaction, consumer right, opposition procedure, treaty revision, or other EU legal condition.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 147.87 characters, while documents average 716.33 characters.

Examples include notification of a Finnish metal-coating acquisition, EU citizens' interest in travel to third countries, consumer dispute resolution and collective redress, trademark opposition involving `NL` marks, and a treaty revision that created a separate environmental chapter. The passages combine formal legal statements, advisory opinions, and administrative facts.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8909, hit@10 of 0.9400, and recall@100 of 0.9750. This is one of the clearest lexical-retrieval profiles in the MuPLeR family. Dutch queries preserve many discriminative terms, dates, institutional names, and legal phrases from the positive passage.

BM25 outperforms dense retrieval on all reported metrics. For this split, exact term occurrence is a primary signal, and a strong model must not discard the value of legal names, quoted marks, regulation references, or numeric facts.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8580, hit@10 of 0.9200, and recall@100 of 0.9500. Dense retrieval remains strong, but it is weaker than BM25. Its semantic matching helps with paraphrased questions, yet it can rank legally related passages above the exact answer when the surface anchors are decisive.

This makes the Dutch split useful for diagnosing whether embedding models over-smooth legal distinctions. Dense systems need to preserve the difference between similar EU procedures, marks, institutions, and treaty provisions.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard rows. It reaches nDCG@10 of 0.9072, hit@10 of 0.9650, and recall@100 of 1.0000. The hybrid pool is the strongest setting and recovers all positives in the top 100.

The result shows that sparse and dense signals are complementary even when BM25 is stronger. BM25 supplies exact Dutch legal anchors, while dense retrieval can add candidates for paraphrased or conceptually phrased questions. The combined pool is the right target for reranking.

### Metric Interpretation for Model Researchers

Because every query has one positive, nDCG@10 and hit@10 directly measure early placement of the correct passage. Recall@100 measures candidate availability for reranking. In this split, BM25 is the standalone baseline to beat, dense retrieval is a strong but secondary comparison, and hybrid retrieval is the best candidate-generation profile.

Researchers should interpret gains carefully: improving semantic retrieval is useful only if it preserves the very strong exact-match behavior already present in Dutch legal text.

### Query and Relevance Type Tendencies

Queries are formal Dutch legal questions that often ask for a named party, share acquisition, percentage, committee stance, trademark proceeding, treaty change, or legal basis. Relevant passages are translated EU legal and administrative texts with long sentences and dense terminology.

Relevance is exact. A passage from the same EU field is not enough unless it states the precise fact or condition requested.

### Representative Failure Modes

Failures include retrieving the right legal topic but wrong transaction, matching a similar trademark opposition without the exact mark, selecting a related treaty or policy passage, and confusing advisory-committee positions. Dense retrieval may over-rank semantically adjacent material; sparse retrieval may struggle when the query paraphrases the passage.

### Training Data That May Help

Useful training data includes non-overlapping Dutch EUR-Lex and DGT-Acquis retrieval pairs, Dutch legal QA, multilingual legal bitext, and hard negatives from related EU passages. Evaluation queries and exact positive passages should be excluded.

### Model Improvement Notes

Dutch legal retrieval models should retain exact handling of quoted terms, acronyms, dates, regulation references, and institutions while learning legal paraphrase. Hard negatives should share many legal terms but differ in the requested actor, procedure, or condition. The perfect hybrid recall@100 makes this split a strong reranking candidate-source benchmark.

## Example Data

| Query | Positive document |
| --- | --- |
| Wie heeft de Commissie op 11 oktober 2004 geïnformeerd over een aandelenverwerving die gezamenlijk zeggenschap geeft over een Finse metaalcoatonderneming? [154 chars] | Op 11 oktober 2004 ontving de Commissie een aanmelding van een voorgenomen concentratie in de zin van artikel 4 van Verordening (EG) nr. 139/2004 van de Raad waarin wordt meegedeeld dat de ondernemingen Outokumpu Wasacopper Oy (Wassacopper, Finland) die deel uitmaakt van het Outokumpu-concern (Finland), en Aurajoki Oy (Aurajoki, Finland) die onder zeggenschap staat van Cap Man Oy (Finland) in de zin van artikel 3, lid 1), sub b), van genoemde verordening gezamenlijk zeggenschap verkrijgen over de onderneming Cupru Oy, waarvan de naam zal veranderd worden in Aura Coat Oy (Aura Coat Oy, Finland), door de aankoop van aandelen. [631 chars] |
| Wat is het aandeel inwoners van de Unie dat binnen drie jaar naar een derde land wil reizen? [92 chars] | Toch wensen de burgers dat de Europese dimensie wordt versterkt. Zo is uit een recente Eurobarometer-enquête naar voren gekomen dat de burgers niet op de hoogte zijn van hun rechten en dat zij op dat gebied hoge verwachtingen koesteren ten aanzien van Europa. Bovendien gaf de helft van de personen met woonplaats in de Unie aan dat zij voornemens waren tijdens de komende drie jaar naar een derde land te reizen, terwijl slechts 23 % van de geënquêteerden verklaarde de door artikel 20 van het EG-Verdrag geboden mogelijkheden te kennen; tegelijkertijd was 17 % van mening dat het mogelijk is bij de delegaties van de Commissie om bescherming te verzoeken. [657 chars] |
| Welk EU-adviesorgaan steunde de derde optie van de Commissie en benadrukte dat buitengerechtelijke consumentenbeslechting met collectieve rechtsmiddelen moet samengaan? [168 chars] | Het EESC stelde eerder al dat … invoering van een groepsactie op EG-niveau … op generlei wijze afbreuk doet aan de stelsels voor buitengerechtelijke beslechting van consumentengeschillen. Het Comité steunt deze laatste voorbehoudloos en vindt dat de mogelijkheden ervan nog verder moeten worden uitgediept en ontwikkeld, zoals wordt voorgesteld in Optie 3 van het Groenboek van de Commissie. Immers, de maatregelen die de Commissie onder die optie voorstelt, zijn bedoeld als aanvulling op en niet als vervanging van het gerechtelijke EU-instrument zoals dat hierboven is beschreven. [583 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0) |
| DGT-Acquis |  | source corpus | [https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Who informed the Commission on 11 October 2004 about a share acquisition giving joint control over a Finnish metal-coating undertaking? | A passage about notification of a concentration under Council Regulation 139/2004 involving Outokumpu Wasacopper and related control. |
| What share of Union residents wants to travel to a third country within three years? | A passage citing a Eurobarometer survey about citizens' rights awareness and expectations regarding the European dimension. |
| Which EU advisory body supported the Commission's third option and emphasized links between out-of-court consumer settlement and collective redress? | A passage stating the EESC position that EU-level group actions should not weaken out-of-court consumer dispute systems. |
| Which Spanish EU opposition procedure concerned refusal based on likelihood of confusion between a two-letter figurative sign and marks such as NLJEANS? | A passage about a Community trademark opposition involving figurative marks containing the `NL` letter combination. |
| Which 17/28 February 1986 revision created a separate environmental chapter to fill a gap in the Treaty of Rome? | A passage discussing the constitutional and legal basis for policy development and treaty revision. |
