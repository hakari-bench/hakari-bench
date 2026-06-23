# MNanoBEIR / NanoBEIR-es / NanoSciFact

## Overview

This task is the Spanish NanoBEIR version of SciFact, a scientific claim verification retrieval benchmark. The original SciFact dataset contains expert-written scientific claims paired with evidence-containing abstracts labeled as supporting or refuting the claim. In this NanoBEIR slice, Spanish translated scientific claims must retrieve Spanish translated scientific abstracts from 2,919 candidate documents. The task contains 50 queries and 56 positive relevance judgments. Most claims have one positive abstract, while four have multiple positives. It is a compact diagnostic for evidence retrieval in scientific literature, where models must connect terminology-rich claims to abstracts that provide the needed evidence before any separate support/refute classification step.

## Details

### What the Original Data Measures

SciFact measures scientific claim evidence retrieval and verification. Claims are declarative assertions about research findings, mechanisms, interventions, or biological effects. In retrieval form, a positive document is an abstract that contains evidence for or against the claim. The retriever must therefore find the evidence-bearing abstract, not merely a paper that belongs to the same scientific area.

### Observed Data Profile

The Spanish Nano task has 50 queries, 2,919 documents, and 56 positives. Positives per query average 1.12, with a maximum of four. Queries are relatively long, averaging about 114 characters, while documents average about 1,644 characters. The examples include claims about Ly49Q and neutrophil migration, antiretroviral therapy and tuberculosis, interferon-induced genes in West Nile virus infection, HPV cervical cancer screening, and TDP-43 interactions in neuronal damage. Positive documents are long scientific abstracts.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.718, Hit@10 of 0.860, and Recall@100 of 0.929. Scientific claims often reuse distinctive biomedical terms, genes, diseases, proteins, interventions, and measurements from the evidence abstracts. These rare terms give sparse retrieval strong signals. The main BM25 risk is over-ranking abstracts that share terminology but do not contain the specific finding needed to verify the claim.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.648, Hit@10 of 0.760, and Recall@100 of 0.893. Dense retrieval is useful for paraphrased scientific findings, but it trails BM25 in this Spanish sample. That suggests exact biomedical terminology and rare-token anchoring are particularly important here. Dense models may retrieve conceptually related abstracts that lack the specific evidential relation or result.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest, with nDCG@10 of 0.728, Hit@10 of 0.860, and Recall@100 of 0.929, with four safeguard rows at 101 candidates. It slightly improves nDCG over BM25 while matching BM25's strong coverage. This is a useful hybrid-search case: sparse retrieval protects rare scientific terms, while dense similarity can adjust ordering when the abstract expresses the claim relation in different wording.

### Metric Interpretation for Model Researchers

Because most queries have one positive, Hit@10 and Recall@100 directly measure evidence discovery. nDCG@10 is the best signal for whether the evidence appears early enough for a practical fact-checking pipeline. Retrieval should be interpreted separately from the final verification label: a refuting abstract is still a positive retrieval target if it contains the relevant evidence.

### Query and Relevance Type Tendencies

Queries are atomic scientific claims rather than questions. They often contain biomedical entities, causal statements, comparative claims, and experimental outcomes. Relevant documents are abstracts with methods, context, and results. Hard negatives can mention the same disease, gene, or intervention while reporting a different finding.

### Representative Failure Modes

BM25 can retrieve abstracts with the same technical terms but no evidence for the claim. Dense retrieval can retrieve abstracts in the same scientific neighborhood but miss the exact finding. Hybrid retrieval improves ordering but can still fail when the key evidence is expressed through subtle experimental context. Failure analysis should check whether the abstract verifies the claim, not only whether it shares terminology.

### Training and Leakage Considerations

Training should exclude SciFact, BEIR, NanoBEIR, and translated abstracts or claims likely to overlap with this evaluation slice. Useful non-overlapping data includes scientific claim-evidence pairs, biomedical abstract retrieval data, CORD-19-style claim retrieval, and Spanish or multilingual scientific NLI and evidence selection data. Synthetic data should generate atomic Spanish claims from non-evaluation abstracts and include hard negatives with shared biomedical entities.

### Model Improvement Signals

Strong models should combine exact scientific term matching with claim-evidence semantics. Useful improvements include biomedical entity normalization, abbreviation handling, relation-aware hard negatives, and evidence selection objectives. Hybrid systems should retain sparse term recall while using dense scoring to improve cases where the evidence relation is paraphrased.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q dirige la migración de los neutrófilos hacia áreas inflamadas regulando las funciones de las b... [100 / 116 chars] | Los neutrófilos rápidamente sufren polarización y movimiento direccional para infiltrarse en los sitios de infección e inflamación. Aquí mostramos que un receptor inhibidor de MHC I, Ly49Q, fue crucia... [200 / 1,125 chars] |
| La terapia antirretroviral reduce las tasas de tuberculosis en diferentes niveles de CD4. [89 chars] | ANTECEDENTES La infección por el virus de la inmunodeficiencia humana (VIH) es el factor de riesgo más fuerte para desarrollar tuberculosis y ha impulsado su resurgimiento, especialmente en el África... [200 / 2,420 chars] |
| Aumento rápido y mayor expresión basal de genes inducidos por interferón reducen la supervivencia de... [100 / 176 chars] | Aunque la susceptibilidad de las neuronas del cerebro a la infección microbiana es un determinante mayor del resultado clínico, se sabe poco sobre los factores moleculares que gobiernan esta vulnerabi... [200 / 1,284 chars] |
| El cribado primario de cáncer cervical con detección de VPH tiene mayor sensibilidad longitudinal qu... [100 / 184 chars] | ANTECEDENTES La detección de cáncer cervical basada en la prueba del virus del papiloma humano (VPH) aumenta la sensibilidad para detectar neoplasia intraepitelial cervical de alto grado (grado 2 o 3)... [200 / 2,540 chars] |
| Bloquear la interacción entre TDP-43 y las proteínas del complejo respiratorio I ND3 y ND6 resulta e... [100 / 156 chars] | Las mutaciones genéticas en la proteína TAR DNA-binding protein 43 (TARDBP, también conocida como TDP-43) causan esclerosis lateral amiotrófica (ELA), y un aumento en la presencia de TDP-43 (codificad... [200 / 1,483 chars] |

## Public Sources

- [SciFact paper](https://arxiv.org/abs/2004.14974)
- [SciFact repository](https://github.com/allenai/scifact)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| SciFact paper (https://arxiv.org/abs/2004.14974) |
| SciFact repository (https://github.com/allenai/scifact) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
