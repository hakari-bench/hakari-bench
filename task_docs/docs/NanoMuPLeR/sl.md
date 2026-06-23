# NanoMuPLeR / sl

## Overview

`NanoMuPLeR / sl` is the Slovenian split of MuPLeR-retrieval, a multilingual legal retrieval benchmark based on European Union legal passages. Queries are synthetic Slovenian legal questions, and documents are Slovenian DGT-Acquis passages. Each query has exactly one relevant passage. The split is useful because BM25 and dense retrieval are close and neither fully dominates, while the hybrid pool improves both early precision and candidate coverage. It tests whether models can combine exact legal terminology with semantic matching under Slovenian morphology and translated EU legal style.

## Details

### What the Original Data Measures

MuPLeR-retrieval evaluates same-language legal passage retrieval across European languages. The source dataset card describes 10,000 DGT-Acquis passages and 200 synthetic parallel queries for each language. DGT-Acquis is part of the European Union's multilingual legal corpus resources and is documented in work on highly multilingual EU parallel corpora.

For Slovenian, a model must identify the single passage that answers a specific legal, regulatory, market, or policy question, rather than merely retrieving a passage from the same broad EU topic.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 136.35 characters, while documents average 607.82 characters.

Examples include telecommunications dominance under a 1998 framework, support for limiting small denominations, beverage packaging weight share, national candy supply controlled by a franchisor, and a 2004 merger that did not create dominance or close online music markets. The content mixes competition policy, market structure, packaging systems, and regulatory interpretation.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.7455, hit@10 of 0.8350, and recall@100 of 0.9000. BM25 is moderately strong because Slovenian EU legal passages contain exact anchors such as dates, percentages, market terms, and named regulatory frameworks.

However, the sparse profile is not sufficient for the full task. The queries often describe legal consequences or market findings in paraphrased form, and many near negatives share the same market or policy vocabulary without answering the exact question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7428, hit@10 of 0.8250, and recall@100 of 0.9250. Dense retrieval is close to BM25 by nDCG@10 and hit@10, and stronger by recall@100. This indicates that embedding similarity finds additional positives at deeper ranks but does not consistently improve early ordering.

The split is therefore a balanced diagnostic. Dense retrieval helps with paraphrase and conceptual matching, while sparse retrieval keeps an advantage for exact regulatory names, numeric shares, and market-specific terms.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with five rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.7983, hit@10 of 0.8950, and recall@100 of 0.9750. Hybrid retrieval is clearly strongest.

The result shows that BM25 and dense retrieval contribute complementary evidence. The hybrid pool gives a reranker access to more positives and better top-ten placement than either standalone method, which is important for Slovenian legal retrieval where both exact terms and semantic relations matter.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the correct passage appears, hit@10 measures first-page success, and recall@100 measures candidate availability for reranking. For Slovenian MuPLeR, BM25 and dense retrieval are comparable but incomplete, while hybrid retrieval is the target candidate-generation profile.

Researchers should treat this split as a test of complementary sparse-dense behavior rather than a case where one method clearly wins.

### Query and Relevance Type Tendencies

Queries are formal Slovenian questions about market dominance, surveys, packaging categories, national supply shares, and merger effects. Relevant documents are translated EU legal, regulatory, or administrative passages with compact factual claims and formal terminology.

Relevance is exact. A passage from the same market, sector, or policy debate is a hard negative if it does not contain the requested legal finding or quantitative condition.

### Representative Failure Modes

Failures include matching a telecommunications passage with the wrong dominance criterion, retrieving packaging text without the requested beverage share, confusing national supply structure with broader market descriptions, and selecting merger discussion that lacks the specific non-dominance or foreclosure conclusion. Sparse systems miss paraphrase; dense systems can over-rank adjacent market discussions.

### Training Data That May Help

Useful training data includes non-overlapping Slovenian EUR-Lex and DGT-Acquis retrieval pairs, Slovenian legal QA, multilingual legal bitext, and hard negatives from similar EU market or policy passages. Evaluation queries and exact positives should be excluded.

### Model Improvement Notes

Models should handle Slovenian legal morphology, exact numeric expressions, market terminology, and semantic paraphrase together. Hard negatives should share the same regulatory or market domain but differ in the requested condition. The hybrid result suggests that reranking over combined sparse-dense candidates is the most informative evaluation setup.

## Example Data

| Query | Positive document |
| --- | --- |
| Kateri regulativni okvir je organom omogočal opredeliti podjetja kot prevladujoča pri 25% tržnem del... [100 / 155 chars] | V skladu z regulativnim okvirom iz leta 1998 so bila področja trga telekomunikacijskega sektorja, za katera je veljala ureditev ex ante, določena v ustreznih direktivah, vendar ti trgi niso bili opred... [200 / 775 chars] |
| Katere države so v raziskavi zabeležile približno štiri petine podpore za omejitev manjših apoenov? [99 chars] | Bankovci in kovanci. Glede zadovoljstva s sedanjimi apoeni bankovcev in kovancev, je raziskava pokazala, da pri bankovcih spremembe niso potrebne, precejšen odstotek anketirancev (od 80 % na Finskem i... [200 / 576 chars] |
| Kateri segment embalaže za pijačo v razpravah v EU predstavlja približno petino skupne embalaže po t... [100 / 104 chars] | Nacionalni sistemi za ponovno uporabo embalaže upoštevajo več vrst embalaže. Nekateri od teh sistemov delujejo zelo dobro, zlasti tisti za prevozno embalažo, kakršne so gajbe in palete, pa tudi za emb... [200 / 524 chars] |
| Kateri delež nacionalne oskrbe bonbonov trgovcem na drobno obvladuje dajalec franšize? [86 chars] | Trgovci na drobno, ki prodajajo bonbone, jih kupujejo na nacionalnem trgu pri nacionalnih proizvajalcih, ki nudijo nacionalne okuse, ali pri trgovcih na debelo, ki ob tem, da prodajajo bonbone naciona... [200 / 740 chars] |
| Katera združitev leta 2004 ni ustvarila prevladujočega nacionalnega igralca in ni zaprla trga za spl... [100 / 146 chars] | Medtem ko je bila industrija glasbenih posnetkov koncentrirana že pred združitvijo v letu 2004, tržni deleži družbe Sony BMG ostajajo nižji od vrednosti, ki bi načelno pomenile posamični prevladujoči... [200 / 620 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0) |
| DGT-Acquis |  | source corpus | [https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which regulatory framework allowed authorities to classify firms as dominant at a 25% market share, considering customer access and finances? | A passage about the 1998 telecommunications regulatory framework and ex ante market areas defined in directives. |
| Which countries in a survey recorded roughly four-fifths support for limiting smaller denominations? | A passage about banknotes and coins reporting high support levels in Finland and Germany and lower levels in other countries. |
| Which beverage-packaging segment accounts for about one-fifth of total packaging by weight in EU discussions? | A passage describing national packaging reuse systems and beverage packaging categories. |
| What share of national candy supply to retailers is controlled by the franchisor? | A passage about retailers buying candy from national producers, wholesalers, and imported suppliers in the national market. |
| Which 2004 merger did not create a dominant national player or foreclose online song sellers or device manufacturers? | A passage explaining that Sony BMG market shares remained below single-dominance levels after the 2004 merger. |
