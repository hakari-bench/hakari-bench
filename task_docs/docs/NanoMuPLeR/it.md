# NanoMuPLeR / it

## Overview

`NanoMuPLeR / it` is the Italian split of MuPLeR-retrieval, a multilingual legal retrieval benchmark based on European Union legal passages. Queries are synthetic Italian legal questions, and documents are Italian DGT-Acquis passages. Each query has one relevant passage, so the task focuses on exact passage identification rather than broad topical matching. The split is useful for testing whether retrieval models can connect formal Italian legal questions to the correct EU passage when many candidates share institutions, regulations, products, or legal terminology.

## Details

### What the Original Data Measures

MuPLeR-retrieval evaluates multilingual parallel legal retrieval using DGT-Acquis passages and synthetic parallel queries. The source dataset card describes a 10,000-passage corpus with 200 queries per language. The broader DGT-Acquis resource is part of the European Union's multilingual legal corpus infrastructure.

In this Italian split, both queries and documents are in Italian. The retrieval system must find the one passage that grounds the answer, even when competing passages discuss a similar legal field or reuse the same institutional vocabulary.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 140.77 characters, while documents average 726.14 characters.

Examples include EU trademark opposition, etymology and specification of a cured meat product, mental-health prevention frameworks, salmonella-control expenditure notifications, and milk-lamb breed definitions. The task therefore mixes legal procedure, agricultural product specifications, public-health policy, and administrative reporting.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.7920, hit@10 of 0.8750, and recall@100 of 0.9500. BM25 performs well because Italian EU legal passages contain distinctive names, product labels, regulation numbers, institutional terms, and formal phrases that are often echoed in the queries.

The moderate gap to dense and hybrid retrieval shows that sparse matching is not enough for all questions. Some queries use compressed paraphrases of longer legal language, and several passages can share the same legal domain while differing in the exact requested condition.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8257, hit@10 of 0.9200, and recall@100 of 0.9750. Dense retrieval is stronger than BM25 on every reported metric, indicating that semantic similarity captures many Italian legal paraphrases and definitional questions better than term frequency alone.

This profile is especially useful for model researchers because it shows a split where embedding retrieval is the better standalone first-stage ranker. A strong dense model must still preserve fine distinctions among similar EU provisions, products, and procedural descriptions.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with one row receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.8422, hit@10 of 0.9250, and recall@100 of 0.9950. The hybrid profile is the strongest overall, improving candidate coverage and early ranking beyond the dense-only subset.

This means Italian MuPLeR is a good case for hybrid search: BM25 contributes exact legal and product terminology, while dense retrieval contributes paraphrase sensitivity. A reranker should benefit from seeing the combined candidate pool rather than either standalone retrieval list.

### Metric Interpretation for Model Researchers

With one positive per query, hit@10 is the proportion of questions whose answer passage is available near the top, while nDCG@10 rewards placing that passage earlier. Recall@100 measures whether the candidate-generation stage gives a reranker access to the positive.

For this split, dense retrieval clearly improves over BM25, and hybrid retrieval improves further. The ordering suggests that Italian legal retrieval depends heavily on semantic matching, but exact lexical anchors remain valuable for robust coverage.

### Query and Relevance Type Tendencies

Queries are formal Italian questions that often ask for a named product, regulatory fact, disease-control measure, EU legal procedure, or breed/specification detail. Relevant documents are formal EU legal and administrative passages with long sentences and dense terminology.

Relevance is narrow. A passage from the same regulation, policy area, or product domain is not enough unless it answers the exact question.

### Representative Failure Modes

Failures can arise from retrieving a passage with the correct institution but wrong proceeding, confusing similar protected product descriptions, matching a disease-control topic without the requested notification fact, or treating a related agricultural specification as interchangeable. Sparse systems can miss paraphrases; dense systems can overgeneralize among adjacent legal passages.

### Training Data That May Help

Useful training data includes non-overlapping Italian EUR-Lex retrieval pairs, Italian legal QA, multilingual legal alignment data, and hard negatives from related EU provisions. Evaluation queries and exact positives should be excluded from training.

### Model Improvement Notes

Models should learn both Italian legal paraphrase and exact handling of names, regulation references, product labels, dates, and administrative actors. Hard-negative construction should keep near passages from the same legal area while changing the requested fact. The hybrid results indicate that reranking over a combined sparse-dense pool is the most appropriate setting for this split.

## Example Data

| Query | Positive document |
| --- | --- |
| Quale opposizione UE in spagnolo riguardò diniego per somiglianza tra segno figurativo di due letter... [100 / 129 chars] | «Marchio comunitario Procedura di opposizione Marchio comunitario figurativo anteriore contenente la combinazione di lettere “NL”Domande di marchi comunitari figurativi contenenti i termini “NLSPORT”,... [200 / 553 chars] |
| Quale salume il cui nome etimologicamente deriva da termini per cacciatori e indica razioni portatil... [100 / 124 chars] | Il nome kiełbasa myśliwska indica la natura specifica del prodotto. Il carattere specifico del prodotto è testimoniato dall'etimologia del nome che deriva da myśliwy (cacciatore), myślistwo (caccia) e... [200 / 635 chars] |
| Quale schema d'intervento a tre livelli è proposto insieme a promuovere benessere psicologico, mante... [100 / 144 chars] | Da questo punto di vista va posto l'accento sulla prevenzione, o sulla sua componente primaria, secondaria e terziaria più adatta al settore interessato. Devono essere sviluppati gli interventi di pro... [200 / 600 chars] |
| Quando è stata notificata alla Commissione europea la spesa cofinanziata per il controllo di patogen... [100 / 132 chars] | L’obiettivo dell’aiuto è l’attuazione del programma di controllo della salmonella negli allevamenti di polli da carne, in conformità alle disposizioni della normativa comunitaria [regolamento (CE) n.... [200 / 683 chars] |
| Quali razze ovine pure da latte di montagna forniscono il ceppo materno per l'agnello da latte legat... [100 / 124 chars] | L'agnello da latte dei Pirenei nasce da tre razze locali da latte. Le madri sono di pura razza basco-bearnese, Manech testa nera o Manech testa rossa. Grazie alla loro conformazione fisica e morfologi... [200 / 617 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0) |
| DGT-Acquis |  | source corpus | [https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which Spanish EU opposition concerned refusal based on similarity between a two-letter figurative sign and clothing marks? | A passage about Community trademark opposition involving figurative marks containing `NL` combinations and related clothing marks. |
| Which cured meat has a name etymologically derived from terms for hunters and portable long-keeping rations? | A passage explaining the specific nature and etymology of `kielbasa mysliwska` and its link to hunting use. |
| Which three-level intervention framework is proposed together with psychological well-being, healthy lifestyles, and supportive contexts? | A passage stressing prevention and primary, secondary, and tertiary health-promotion interventions for mental health. |
| When was co-financed expenditure for controlling food-borne pathogens in broiler chickens notified to the European Commission? | A passage about a salmonella-control program for broiler farms and notification of related co-financed expenditure. |
| Which pure mountain dairy sheep breeds provide the maternal stock for a milk-fed lamb tied to seasonal pasture? | A passage describing the Pyrenean milk-fed lamb and the Basco-Bearnaise and Manech dairy breeds used as mothers. |
