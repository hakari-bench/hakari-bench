# MNanoBEIR / NanoBEIR-es / NanoSCIDOCS

## Overview

This task is the Spanish NanoBEIR version of SCIDOCS, a scientific document retrieval benchmark derived from scholarly relatedness signals. The original SCIDOCS benchmark was introduced with SPECTER to evaluate whether document representations capture citation-informed relationships between scientific papers. In this NanoBEIR slice, Spanish translated scientific paper titles or short descriptions are used as queries, and the system must retrieve Spanish translated related scientific documents from 2,210 candidates. The task contains 50 queries and 244 positive relevance judgments. Every query has multiple positives, usually five. It is a compact diagnostic for document-level scholarly retrieval, where relevance may depend on shared methods, application domains, citation neighborhoods, and problem formulations rather than simple title keyword overlap.

## Details

### What the Original Data Measures

SCIDOCS measures scientific relatedness at the document level. In the original setting, citation and recommendation-style signals indicate whether two papers are related. In retrieval form, a model must rank related papers for a query paper or title-like description. This differs from ordinary question answering because the relevant document may not answer a question; it may be a paper from the same research area, method family, or citation context.

### Observed Data Profile

The Spanish Nano task has 50 queries, 2,210 documents, and 244 positives. Every query is multi-positive, with three to five positives and an average of 4.88. Queries average about 88 characters, while documents average about 1,078 characters. The examples include titles about DC-DC multilevel boost converters, sparse Gaussian Markov fields, texture synthesis with convolutional networks, RFID antennas, and digital heart-rate monitoring. Documents are translated scientific abstracts or paper descriptions, including some noisy translation artifacts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.298, Hit@10 of 0.760, and Recall@100 of 0.611. Sparse retrieval benefits from technical term overlap: method names, hardware terms, and domain phrases often repeat between related papers. However, citation-style relatedness is not reducible to shared words. BM25 can over-rank papers that reuse a term while missing papers that are related by method, application setting, or scientific problem framing.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline improves the ranking, with nDCG@10 of 0.355, Hit@10 of 0.820, and Recall@100 of 0.635. This indicates that embedding similarity captures some scholarly relatedness beyond exact title terms. Dense retrieval helps when related papers share conceptual structure, task type, or research domain without using identical wording. The remaining recall gap shows that generic dense representations still only partially model citation-informed scientific neighborhoods.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is slightly strongest, with nDCG@10 of 0.355, Hit@10 of 0.820, and Recall@100 of 0.648, with one safeguard row at 101 candidates. It is nearly tied with dense retrieval on top-10 quality and improves recall modestly. This is a balanced hybrid case: lexical technical terms are useful, but dense representations are needed to capture broader scholarly relatedness. The gain is not dramatic, but hybrid search provides the best candidate coverage.

### Metric Interpretation for Model Researchers

Because every query has multiple positives, Hit@10 only indicates whether at least one related paper was found. nDCG@10 is more informative because the task expects several related documents to appear early. Recall@100 matters for recommendation and reranking pipelines, where a broad related-paper candidate set is valuable. The close dense and hybrid scores suggest that reranking quality will depend on document-level scientific representations rather than only sparse candidate generation.

### Query and Relevance Type Tendencies

Queries are Spanish translated scientific titles or compressed paper descriptions. Relevant documents are longer abstracts or summaries. The relationship may be topical, methodological, citation-like, or application-based. Same-field hard negatives can be difficult because they share technical vocabulary but do not belong to the annotated related set.

### Representative Failure Modes

BM25 can retrieve papers with the same keyword but a different research objective. Dense retrieval can retrieve broadly similar papers that are not citation-neighborhood positives. Hybrid retrieval can improve coverage but still misorder relatedness when lexical overlap conflicts with scientific context. Failure analysis should examine the relation between papers, not only whether they share a topic.

### Training and Leakage Considerations

Training should exclude SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, and translated scientific records likely to overlap with these documents. Useful non-overlapping data includes citation prediction pairs, paper recommendation data, co-citation or co-viewed pairs, S2ORC-style abstracts, and Spanish or multilingual scholarly retrieval supervision. Multi-positive training is required because every query has several related documents.

### Model Improvement Signals

Strong models should improve scientific-document representations and citation-style relatedness. Useful signals include contrastive learning over paper neighborhoods, hard negatives from the same field, method and dataset normalization, and multilingual scholarly abstracts. Hybrid systems should preserve exact technical terms while relying on dense ranking for conceptual relatedness.

## Example Data

| Query | Positive document |
| --- | --- |
| Convertidor elevador multinivel CC-CC innovador [47 chars] | Los conversores de fuente de voltaje multinivel están emergiendo como una nueva generación de opciones de conversores de potencia para aplicaciones de alta potencia. Los conversores de fuente de voltaje multinivel generalmente sintetizan la onda de voltaje en escalera a partir de varios niveles de voltajes de condensadores de corriente continua. Una de las principales limitaciones de los conversores multinivel es el desequilibrio de voltaje entre los diferentes niveles. Las técnicas para equilibrar el voltaje entre los diferentes niveles generalmente implican el clampeo de voltaje o el control de carga de condensadores. Existen varias formas de implementar el equilibrio de voltaje en los conversores multinivel. Sin considerar los conversores tradicionales acoplados magnéticamente, este artículo presenta tres conversores de fuente de voltaje multinivel desarrollados recientemente: 1) diodo-clamp, 2) condensadores voladores, y 3) inversores en cascada con fuentes de corriente continua se... [1,000 / 1,128 chars] |
| Aprendizaje rápido de campos aleatorios de Markov gaussianos esparcidos utilizando la factorización de Cholesky [111 chars] | Sure, please provide the English document text that you need translated into Spanish. [85 chars] |
| Síntesis de Texturas mediante Redes Neuronales Convolucionales [62 chars] | En este trabajo, investigamos el efecto de la profundidad de las redes convolucionales en su precisión en el contexto de reconocimiento de imágenes a gran escala. Nuestra principal contribución es una evaluación exhaustiva de redes de profundidad creciente, que demuestra que una mejora significativa sobre las configuraciones del estado del arte puede lograrse aumentando la profundidad a 16-19 capas de peso. Estos hallazgos fueron la base de nuestra participación en el ImageNet Challenge 2014, donde nuestro equipo obtuvo el primer y segundo lugar en las categorías de localización y clasificación, respectivamente. También mostramos que nuestras representaciones se generalizan bien a otros conjuntos de datos, donde obtenemos resultados de vanguardia. Es importante destacar que hemos puesto a disposición del público nuestros dos modelos ConvNet de mejor rendimiento para facilitar futuras investigaciones sobre el uso de representaciones visuales profundas en visión por computadora. [991 chars] |

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
