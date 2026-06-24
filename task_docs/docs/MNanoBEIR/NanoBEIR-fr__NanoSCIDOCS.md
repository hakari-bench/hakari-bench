# MNanoBEIR / NanoBEIR-fr / NanoSCIDOCS

## Overview

This task is the French NanoBEIR version of SCIDOCS, a scientific document retrieval benchmark derived from scholarly relatedness signals. The original SCIDOCS benchmark was introduced with SPECTER to evaluate whether document representations capture citation-informed relationships between scientific papers. In this NanoBEIR slice, French translated scientific paper titles or short descriptions must retrieve French translated related scientific documents from 2,210 candidates. The task contains 50 queries and 244 positive relevance judgments. Every query has multiple positives, usually five. It is a compact benchmark for scholarly retrieval, where relevance may reflect shared methods, citation neighborhoods, applications, or problem formulations rather than only title keyword overlap.

## Details

### What the Original Data Measures

SCIDOCS measures document-level scientific relatedness. In retrieval form, a query paper title or description should retrieve related papers. The relation can be topical, methodological, citation-like, or application-based. A related paper may not answer a question and may not reuse the same title words; it may instead belong to the same research neighborhood.

### Observed Data Profile

The French Nano task has 50 queries, 2,210 documents, and 244 positives. Every query is multi-positive, with three to five positives and an average of 4.88. Queries average about 93 characters, and documents average about 1,115 characters. Examples include multilevel DC-DC boost converters, sparse Gaussian Markov fields, texture synthesis with convolutional networks, RFID antennas, and digital heart-rate monitors. Documents are translated scientific abstracts or paper descriptions.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.313, Hit@10 of 0.760, and Recall@100 of 0.607. Sparse retrieval benefits from technical vocabulary overlap. Method names, hardware terms, and domain phrases can be strong lexical anchors. However, scholarly relatedness is not just title matching; BM25 can miss papers connected by citation context, shared method, or application framing when the wording differs.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline improves ranking, with nDCG@10 of 0.373, Hit@10 of 0.820, and Recall@100 of 0.615. Dense retrieval captures some scientific relatedness beyond exact words, especially when papers share research intent or method families. The recall improvement is small, which indicates that candidate coverage remains difficult and that generic dense representations only partially model citation-informed neighborhoods.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest, with nDCG@10 of 0.379, Hit@10 of 0.840, and Recall@100 of 0.664, with one safeguard row at 101 candidates. It combines technical term anchoring from BM25 with dense document-level similarity. The improvement is clearest in recall, making hybrid search the best candidate generator for this French scientific relatedness task.

### Metric Interpretation for Model Researchers

Because every query has multiple positives, Hit@10 is only a first-related-paper signal. nDCG@10 is more informative because several related documents should appear early. Recall@100 matters for recommendation or reranking systems that need a broad related-paper set. The hybrid profile's recall advantage suggests that combining lexical and semantic signals helps recover more of the scholarly neighborhood.

### Query and Relevance Type Tendencies

Queries are French translated scientific titles or compact paper descriptions. Relevant documents are longer abstracts or paper summaries. The relation may involve shared methods, citation context, application area, or problem formulation. Hard negatives can be same-field papers with overlapping terminology but no annotated relatedness relation.

### Representative Failure Modes

BM25 can retrieve papers that share keywords but target a different research problem. Dense retrieval can retrieve broadly similar papers outside the annotated related set. Hybrid retrieval improves coverage but can still misorder relatedness when lexical and conceptual signals conflict. Failure analysis should compare the scientific relationship between papers, not only topical similarity.

### Training and Leakage Considerations

Training should exclude SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, and translated scientific records likely to overlap with these documents. Useful non-overlapping data includes citation prediction pairs, scientific paper recommendation data, co-citation or co-viewed paper pairs, and French or multilingual scholarly retrieval supervision. Multi-positive training is required because every query has several related documents.

### Model Improvement Signals

Strong models should improve citation-style relatedness and scientific document representations. Useful training signals include paper-neighborhood contrastive learning, hard negatives from the same field, method and dataset normalization, and multilingual scholarly abstracts. Hybrid systems should preserve exact technical terms while dense ranking captures conceptual relatedness.

## Example Data

| Query | Positive document |
| --- | --- |
| Nouveau convertisseur élévateur multiniveau CC-CC [49 chars] | Les convertisseurs de tension à sources multiples sont en train d'émerger comme une nouvelle génération d'options de convertisseurs de puissance pour les applications à haute puissance. Les convertisseurs de tension à sources multiples synthétisent généralement une onde de tension en escalier à partir de plusieurs niveaux de tensions de condensateurs en courant continu. L'une des principales limitations des convertisseurs à niveaux multiples est le déséquilibre de tension entre les différents niveaux. Les techniques pour équilibrer la tension entre les différents niveaux impliquent généralement le clampage de tension ou le contrôle de la charge des condensateurs. Il existe plusieurs façons de mettre en œuvre l'équilibre de tension dans les convertisseurs à niveaux multiples. Sans considérer les convertisseurs traditionnels à couplage magnétique, cet article présente trois convertisseurs de tension à sources multiples récemment développés : 1) les convertisseurs à diodes de clampage, 2)... [1,000 / 1,262 chars] |
| Apprentissage accéléré des champs aléatoires de Markov gaussiens creux basé sur la décomposition de Cholesky [108 chars] | Sure, please provide the English document text that you need translated into French. [84 chars] |
| Synthèse de textures par réseaux de neurones convolutifs [56 chars] | Dans ce travail, nous examinons l'impact de la profondeur des réseaux convolutifs sur leur précision dans le contexte de la reconnaissance d'images à grande échelle. Notre principale contribution est une évaluation approfondie de réseaux de profondeur croissante, qui montre qu'une amélioration significative par rapport aux configurations de l'état de l'art peut être obtenue en augmentant la profondeur à 16–19 couches de poids. Ces résultats ont servi de base à notre soumission au concours ImageNet 2014, où notre équipe a remporté les première et deuxième places dans les catégories de localisation et de classification, respectivement. Nous démontrons également que nos représentations généralisent bien à d'autres ensembles de données, où nous obtenons des résultats à la pointe de la technologie. De plus, nous avons rendu publics nos deux meilleurs modèles de réseaux convolutifs (ConvNet) pour faciliter les recherches futures sur l'utilisation des représentations visuelles profondes en vi... [1,000 / 1,020 chars] |

## Public Sources

- [SPECTER paper](https://arxiv.org/abs/2004.07180)
- [SCIDOCS repository](https://github.com/allenai/scidocs)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| SPECTER paper (https://arxiv.org/abs/2004.07180) |
| SCIDOCS repository (https://github.com/allenai/scidocs) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
