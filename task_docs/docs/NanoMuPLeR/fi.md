# NanoMuPLeR / fi

## Overview

`NanoMuPLeR / fi` is the Finnish split of MuPLeR-retrieval. It uses synthetic Finnish legal questions and Finnish DGT-Acquis-derived EU legal passages. Each query has one positive passage that contains the legal condition or factual detail required by the question. The split is useful for evaluating retrieval in a morphologically rich language where long Finnish compounds, case inflection, EU institutional terms, and legal formulae all affect matching. Compared with other MuPLeR languages, Finnish has especially long queries in this Nano sample, making it a good test of robust legal term and condition matching.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures multilingual parallel legal retrieval using DGT-Acquis passages and synthetic queries. The source dataset card describes 10,000 human-translated EU legal passages and 200 synthetic queries per language.

For the Finnish split, retrieval is same-language. The model must find the passage that answers the legal question, not merely a passage in the same EU policy area.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 160.16 characters, while documents average 683.64 characters.

Examples include maritime labor conventions, telecommunications market dominance, vocational training indicators, human-resource planning, and intelligent transport systems. Documents are formal Finnish EU legal or administrative passages.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8230, hit@10 of 0.9050, and recall@100 of 0.9400. BM25 is very strong despite Finnish morphology because many queries contain distinctive legal terms, dates, institutions, and topic-specific vocabulary.

Its recall@100 is lower than dense retrieval's, suggesting that exact term overlap sometimes misses the positive when Finnish inflection or paraphrase changes surface forms.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7955, hit@10 of 0.8850, and recall@100 of 0.9600. Dense retrieval has better recall@100 than BM25 but weaker top-rank quality.

This pattern suggests that dense retrieval broadens candidate coverage under Finnish variation, while BM25's exact legal anchors often place the right passage higher when it finds it.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with four queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.8682, hit@10 of 0.9250, and recall@100 of 0.9800. This is the strongest profile across the candidate types.

Hybrid retrieval is therefore well suited for Finnish legal retrieval because it combines exact EU terminology with semantic matching across inflection and paraphrase.

### Metric Interpretation for Model Researchers

This is single-positive retrieval, so top-rank metrics directly indicate exact passage grounding. Recall@100 shows candidate coverage for reranking. The split is especially useful for comparing sparse and dense behavior in a morphologically rich legal language.

BM25's high top-rank quality and dense retrieval's higher recall suggest that reranking over hybrid candidates is the most informative evaluation setup.

### Query and Relevance Type Tendencies

Queries are long Finnish legal questions. Relevant documents are Finnish EU legal passages. The questions often ask which body, framework, indicator, plan, or system satisfies a specified condition.

The relevance relation is exact legal answerability. Same-domain legal text is insufficient if it does not satisfy the query condition.

### Representative Failure Modes

Common failures include missing inflected variants, matching legal terms without the correct condition, confusing similar EU advisory or regulatory bodies, and over-ranking passages with shared policy vocabulary. Dense systems may retrieve broad legal-semantic matches; sparse systems may be brittle to morphology.

### Training Data That May Help

Useful training data includes non-overlapping Finnish EU legal retrieval pairs, Finnish legal QA, EUR-Lex passages, multilingual parallel legal data, and hard negatives from nearby legal provisions. MuPLeR evaluation query-passage pairs and near-duplicate aligned passages should be excluded.

### Model Improvement Notes

Models should handle Finnish morphology, compounds, legal terminology, and exact institutional references. Hybrid retrieval is particularly attractive because it balances exact matching with semantic coverage. Hard negatives should be legally adjacent but fail the specific condition in the query.

## Example Data

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Mikä EU:n neuvoa-antava elin ilmoitti tervetulleeksi työnantajien ja työntekijöiden sopimuksen sisällyttää vuoden 2006 merityön yleissopimus yhteisön lainsäädäntöön? | A Finnish passage about the EESC welcoming a social-partner agreement to include the 2006 Maritime Labour Convention in Community law. |
| Mikä sääntelykehys salli viranomaisten nimetä yrityksiä dominoiviksi noin 25 prosentin markkinaosuuden ja asiakasyhteyksien sekä rahoitusvoiman perusteella? | A passage explaining the 1998 telecommunications regulatory framework and market designation criteria. |
| Mikä ehdotettu valittavissa oleva mittaristo tukee kansallisen ammatillisen koulutuksen laatua eroten neuvoston 25. toukokuuta 2007 päätelmiistä? | A passage about reference indicators for evaluating and improving vocational education quality. |
| Miten henkilöstöresurssien suunnittelijat suosittelevat kohdentamaan koulutusohjelmia työllisyysennusteisiin, käyttäen Etelä-Koreaa valaisevana esimerkkinä? | A passage about human-resource development, training, and aligning education with employment needs. |
| Mikä järjestelmätyyppi edellyttää pitkän aikavälin suunnittelua sekä suurten tietomäärien laajamittaista käsittelyä tunnistettavissa olevien henkilöiden tietojen osalta alueellisten oikeudellis‑teknisten säädösten alaisena? | A passage about intelligent transport systems and the large-scale use of data under legal and technical rules. |
