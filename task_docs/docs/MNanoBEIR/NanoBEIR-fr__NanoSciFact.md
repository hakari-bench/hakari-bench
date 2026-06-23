# MNanoBEIR / NanoBEIR-fr / NanoSciFact

## Overview

This task is the French NanoBEIR version of SciFact, a scientific claim verification retrieval benchmark. The original SciFact dataset contains expert-written scientific claims paired with abstracts annotated as supporting or refuting the claim. In this NanoBEIR slice, French translated scientific claims must retrieve French translated scientific abstracts from 2,919 candidate documents. The task contains 50 queries and 56 positive relevance judgments. Most claims have one positive abstract, while four have multiple positives. It is a compact diagnostic for scientific evidence retrieval, where models must connect terminology-rich claims to evidence-bearing abstracts before any separate support/refute classification step.

## Details

### What the Original Data Measures

SciFact measures scientific claim verification over research abstracts. In retrieval form, the model must find the abstract that contains evidence for or against a claim. The claim may describe a biological mechanism, medical intervention, cellular process, disease relationship, or experimental finding. Relevance requires evidential support, not only membership in the same scientific topic.

### Observed Data Profile

The French Nano task has 50 queries, 2,919 documents, and 56 positives. Positives per query average 1.12, with a maximum of four. Queries are long, averaging about 119 characters, while documents average about 1,711 characters. Examples include claims about Ly49Q and neutrophil migration, antiretroviral therapy and tuberculosis, interferon-induced genes in West Nile virus infection, HPV cervical cancer screening, and TDP-43 neuronal damage. Positive documents are long scientific abstracts.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.718, Hit@10 of 0.860, and Recall@100 of 0.946. This reflects the importance of exact biomedical terminology. Claims often repeat rare entities, proteins, diseases, interventions, and measurement terms from the evidence abstract. BM25 can still fail when an abstract expresses the finding through abbreviations, different phrasing, or experimental context rather than repeating the claim wording.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.697, Hit@10 of 0.840, and Recall@100 of 0.929. Dense retrieval is helpful for semantic evidence matching, but it trails BM25 in this French sample. This suggests that exact technical term anchoring is especially important. Dense models may retrieve abstracts that are scientifically related but do not contain the specific evidence needed to verify the claim.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest, with nDCG@10 of 0.734, Hit@10 of 0.900, and Recall@100 of 0.964, with two safeguard rows at 101 candidates. Hybrid search combines BM25's rare-term precision with dense retrieval's ability to handle phrasing differences. It improves both top-10 ranking and candidate coverage, making it the best first-stage profile for this French SciFact slice.

### Metric Interpretation for Model Researchers

Because most queries have one positive, Hit@10 and Recall@100 are direct measures of evidence discovery. nDCG@10 indicates how early the evidence abstract appears. Retrieval should be separated from the verification label: an abstract that refutes the claim is still a correct retrieval target. The hybrid advantage suggests that scientific claim retrieval needs both term precision and semantic evidence matching.

### Query and Relevance Type Tendencies

Queries are declarative scientific claims with biomedical entities, mechanisms, and outcomes. Relevant documents are abstracts containing methods, background, and findings. Hard negatives often share disease or protein terminology but report a different result. The task is sensitive to abbreviation handling, entity normalization, and relation-specific evidence matching.

### Representative Failure Modes

BM25 can over-rank abstracts that share rare terms but lack the verifying finding. Dense retrieval can retrieve abstracts in the same scientific area but miss the exact claim relation. Hybrid retrieval reduces both risks but can still fail when evidence depends on subtle experimental context. Failure analysis should ask whether the abstract verifies the claim, not only whether it is topically related.

### Training and Leakage Considerations

Training should exclude SciFact, BEIR, NanoBEIR, and translated records likely to overlap with these claims or abstracts. Useful non-overlapping data includes SciFact-style claim-evidence pairs, scientific fact verification data, biomedical abstract retrieval pairs, and French or multilingual scientific NLI and evidence selection data. Synthetic data should generate atomic French claims from non-evaluation abstracts and include hard negatives sharing terminology.

### Model Improvement Signals

Strong models should combine exact biomedical term recall with claim-evidence semantics. Useful signals include abbreviation expansion, biomedical entity linking, same-entity hard negatives, and evidence selection objectives. Hybrid systems should preserve sparse rare-term matching while dense scoring improves paraphrased evidence relations.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q dirige l'organisation de la migration des neutrophiles vers les sites d'inflammation en régulant les fonctions des rafts membranaires. [140 chars] | Les neutrophiles subissent rapidement une polarisation et un mouvement directionnel pour infiltrer les sites d'infection et d'inflammation. Nous démontrons ici que le récepteur inhibiteur MHC I, Ly49Q, est crucial pour la polarisation rapide et l'infiltration tissulaire des neutrophiles. En état stable, Ly49Q inhibe l'adhésion des neutrophiles en empêchant la formation de complexes focaux, probablement en inhibant les kinases Src et PI3. Cependant, en présence de stimuli inflammatoires, Ly49Q médiatise la polarisation rapide et l'infiltration tissulaire des neutrophiles de manière dépendante du domaine ITIM. Ces fonctions opposées semblent être médiées par l'utilisation distincte des phosphatases effectrices SHP-1 et SHP-2. La polarisation et la migration dépendantes de Ly49Q sont influencées par la régulation des fonctions des radeaux membranaires par Ly49Q. Nous proposons que Ly49Q est pivotale pour permettre aux neutrophiles de passer à une morphologie polarisée et à une migration r... [1,000 / 1,134 chars] |
| La thérapie antirétrovirale réduit les taux de tuberculose chez les patients ayant différents niveaux de CD4. [109 chars] | CONTEXTE L'infection par le virus de l'immunodéficience humaine (VIH) est le principal facteur de risque de développement de la tuberculose et a contribué à sa résurgence, notamment en Afrique subsaharienne. En 2010, on estimait à 1,1 million le nombre de nouveaux cas de tuberculose parmi les 34 millions de personnes vivant avec le VIH dans le monde. La thérapie antirétrovirale a un potentiel considérable pour prévenir la tuberculose associée au VIH. Nous avons réalisé une revue systématique des études analysant l'impact de la thérapie antirétrovirale sur l'incidence de la tuberculose chez les adultes infectés par le VIH. MÉTHODES ET RÉSULTATS Nous avons systématiquement recherché dans PubMed, Embase, African Index Medicus, LILACS et les registres d'essais cliniques. Les essais randomisés contrôlés, les études de cohortes prospectives et rétrospectives ont été inclus s'ils comparaient l'incidence de la tuberculose en fonction du statut de thérapie antirétrovirale chez les adultes infec... [1,000 / 2,452 chars] |
| La régulation rapide et l'expression basale plus élevée des gènes induits par les interférons diminuent la survie des neurones des cellules granulaires infectés par le virus du Nil occidental. [192 chars] | Bien que la sensibilité des neurones du cerveau aux infections microbiennes soit un facteur déterminant majeur des résultats cliniques, peu de choses sont connues sur les facteurs moléculaires régissant cette vulnérabilité. Ici, nous montrons que deux types de neurones provenant de régions cérébrales distinctes présentent une permissivité différentielle à la réplication de plusieurs virus à ARN à brin positif. Les neurones granulaires du cervelet et les neurones corticaux du cortex cérébral possèdent des programmes immunitaires innés uniques qui confèrent une sensibilité différentielle à l'infection virale ex vivo et in vivo. En transduisant des neurones corticaux avec des gènes exprimés de manière plus élevée dans les neurones granulaires, nous avons identifié trois gènes stimulés par l'interféron (ISGs; Ifi27, Irg1 et Rsad2 (également connu sous le nom de Viperin)) qui médient les effets antiviraux contre différents virus neurotropes. De plus, nous avons constaté que l'état épigénéti... [1,000 / 1,344 chars] |

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
