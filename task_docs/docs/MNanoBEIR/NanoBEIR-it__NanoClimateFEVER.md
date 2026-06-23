# MNanoBEIR / NanoBEIR-it / NanoClimateFEVER

## Overview

This task is the Italian NanoBEIR version of Climate-FEVER, a climate-science claim verification retrieval benchmark. The original Climate-FEVER dataset extends FEVER-style verification to real-world climate claims and Wikipedia evidence. In this NanoBEIR slice, Italian translated climate claims must retrieve Italian translated evidence documents from 3,408 candidates. The task contains 50 queries and 148 positive relevance judgments, with an average of 2.96 positives per query. Most claims have multiple positives. It is a compact diagnostic for claim-evidence retrieval in climate science, where models must connect claim wording to scientific context, temporal framing, mechanisms, records, and broad evidence pages.

## Details

### What the Original Data Measures

Climate-FEVER measures whether systems can retrieve evidence for climate-related claims. A claim may refer to sea-level change, warming trends, carbon dioxide, solar activity, extreme weather, geological periods, or attribution studies. The retrieval step matters because verification depends on finding evidence-bearing pages, not just pages that repeat climate vocabulary.

### Observed Data Profile

The Italian Nano task has 50 queries, 3,408 documents, and 148 positives. Positives per query average 2.96, with a median of three and a maximum of five. Queries average about 152 characters, and documents average about 1,743 characters. Example claims discuss warming from 1970 to 1998, downward trends, local and regional sea-level variability, Hurricane Harvey, and the CERN CLOUD experiment. Positive documents are encyclopedia-style evidence passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.270, Hit@10 of 0.620, and Recall@100 of 0.541. Sparse retrieval helps when claims contain exact climate terms, numeric expressions, named experiments, or entities. However, it struggles when evidence appears in broader context pages or when the claim must be connected to a mechanism or scientific attribution statement. BM25 can retrieve climate-related pages without finding the specific evidence needed.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline performs best by top ranking, with nDCG@10 of 0.339, Hit@10 of 0.780, and Recall@100 of 0.608. Dense retrieval helps connect claims to evidence pages that use different wording, especially when the evidence is explanatory rather than lexical. The improvement over BM25 shows that semantic evidence matching is important for this Italian split, though recall remains moderate.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.326, Hit@10 of 0.760, and Recall@100 of 0.622, with two safeguard rows at 101 candidates. It has the best Recall@100, while dense retrieval has the best nDCG@10 and Hit@10. This means hybrid search is useful for candidate coverage, but dense ranking is better for the first page. A verification pipeline may prefer the hybrid pool because it misses fewer positives.

### Metric Interpretation for Model Researchers

Most queries have multiple positives, so Hit@10 only indicates whether at least one evidence page was found. Recall@100 matters for claim verification pipelines because several pages may capture different aspects of a claim. nDCG@10 measures whether evidence appears early enough for practical use. The dense-versus-hybrid split separates direct ranking quality from candidate coverage.

### Query and Relevance Type Tendencies

Queries are Italian declarative climate claims, often with numeric, temporal, or causal framing. Relevant documents are longer evidence passages, frequently broad encyclopedia pages. Hard negatives may share climate terms but not verify the claim. The task is sensitive to scientific terminology, time periods, named institutions, and attribution language.

### Representative Failure Modes

BM25 can retrieve pages that repeat a climate term but do not verify the claim. Dense retrieval can retrieve generally related climate pages that miss the annotated evidence. Hybrid retrieval improves recall but may still rank broader context above the most direct evidence. Failure analysis should check whether the document would actually support verification of the claim.

### Training and Leakage Considerations

Training should exclude Climate-FEVER, BEIR, NanoBEIR, and translated records likely to overlap with the evaluation evidence. Useful non-overlapping data includes climate claim-evidence pairs, scientific fact-checking retrieval data, Italian or multilingual climate science QA, and hard negatives from related climate pages. Multi-positive training is recommended because most claims have several evidence documents.

### Model Improvement Signals

Strong models should improve climate evidence recall while maintaining claim specificity. Useful signals include temporal claim variants, scientific term normalization, climate-domain hard negatives, and multilingual claim verification pairs. Hybrid systems should preserve exact scientific terms while dense retrieval recovers broader explanatory evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| Dal 1970 al 1998 c'è stato un periodo di riscaldamento che ha aumentato le temperature di circa 0,4°... [100 / 180 chars] | Il Paleocene (pronunciato /ˈpæliəˌsiːn/ o /ˈpælioʊˌsiːn/) o Paleocene, il "recentemente antico", è un'epoca geologica che si estese per circa 10 milioni di anni, dal 66 al 56 milioni di anni fa. È la... [200 / 1,167 chars] |
| In realtà, la tendenza, anche se non statisticamente significativa, è in calo. [78 chars] | Il ciclo solare o ciclo di attività magnetica solare è il ciclo quasi periodico di 11 anni che caratterizza le variazioni dell'attività solare (comprese le variazioni nei livelli di radiazione solare... [200 / 738 chars] |
| I livelli del mare locali e regionali continuano a mostrare la normale variabilità naturale, salendo... [100 / 138 chars] | Il livello medio del mare (MSL) (abbreviato semplicemente livello del mare) è il livello medio della superficie di uno o più degli oceani della Terra, rispetto al quale si misurano le altezze, come le... [200 / 1,198 chars] |
| Gli scienziati del clima dicono che alcuni elementi legati all'uragano Harvey suggeriscono che il ri... [100 / 162 chars] | Gli effetti del riscaldamento globale sono i cambiamenti ambientali e sociali causati (direttamente o indirettamente) dalle emissioni di gas serra prodotte dall'uomo. C'è un consenso scientifico che i... [200 / 1,500 chars] |
| L'esperimento CLOUD del CERN ha testato solo una delle quattro condizioni necessarie per attribuire... [100 / 198 chars] | L'attribuzione dei recenti cambiamenti climatici è lo sforzo di determinare scientificamente i meccanismi responsabili dei cambiamenti climatici osservati sulla Terra, comunemente noti come "riscaldam... [200 / 2,273 chars] |

## Public Sources

- [Climate-FEVER paper](https://arxiv.org/abs/2012.00614)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Climate-FEVER paper (https://arxiv.org/abs/2012.00614) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
