# MNanoBEIR / NanoBEIR-de / NanoSCIDOCS

## Overview

This task is the German NanoBEIR version of SCIDOCS, a scientific document retrieval benchmark derived from scholarly relatedness signals. The original SCIDOCS benchmark was introduced with SPECTER to evaluate whether document representations capture citation-informed relatedness between scientific papers. In this NanoBEIR slice, German translated scientific titles or short paper descriptions are used as queries, and the system must retrieve German translated related scientific documents. The task contains 50 queries, 2,210 documents, and 244 positive relevance judgments. Every query has multiple positives, usually five. This makes the task a focused diagnostic for scholarly retrieval: models must go beyond title keyword overlap and identify related research through methods, domains, citation-like proximity, and scientific problem framing.

## Details

### What the Original Data Measures

SCIDOCS measures document-level scientific relatedness rather than direct question answering. Relevance can reflect citation prediction, recommendation, or other scholarly neighborhood signals. A related paper may share a method, dataset, application, theoretical framing, or citation context without using the same surface words. In BEIR and NanoBEIR, this becomes a retrieval task where the query is a scientific document representation and the positives are other documents that should be ranked as scholarly related.

### Observed Data Profile

The German Nano task has 50 queries, 2,210 documents, and 244 positives. Every query is multi-positive, with three to five relevant documents and an average of 4.88 positives per query. Queries average about 82 characters, while documents average about 1,071 characters. The examples include scientific titles about power converters, Gaussian Markov fields, texture synthesis, RFID antennas, and digital heart-rate monitors. Documents are translated scientific abstracts or paper summaries, sometimes with noisy translation artifacts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.191, Hit@10 of 0.580, and Recall@100 of 0.480. This is a weak-to-moderate sparse profile and reflects the difficulty of citation-style relatedness. Lexical matching helps when a query and relevant paper share distinctive technical terms, but many positives are related by method, application area, or citation context rather than exact wording. BM25 can also be distracted by documents that repeat a technical term but are not among the target related papers.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is substantially stronger, with nDCG@10 of 0.371, Hit@10 of 0.820, and Recall@100 of 0.660. This is the expected pattern for scholarly relatedness: embedding similarity can capture conceptual proximity across terminology differences and can represent paper-level topics better than raw term frequency. Dense retrieval is especially helpful when related papers share research intent, architecture class, or domain context without sharing many title words. The remaining recall gap shows that generic multilingual embeddings still do not fully model citation-informed scientific neighborhoods.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.300, Hit@10 of 0.780, and Recall@100 of 0.656, with exactly 100 candidates per query and no safeguard rows. It is close to dense on Recall@100 but below dense on top-10 ranking. This indicates that the hybrid candidate pool successfully recovers many dense-discovered positives, but lexical signals do not consistently improve ordering for this task. In scientific relatedness, exact terminology is useful but can be misleading; the strongest signal in this sample is dense document-level similarity.

### Metric Interpretation for Model Researchers

Because all queries have multiple positives, Hit@10 alone is insufficient. A model can hit one related paper while missing most of the relevant neighborhood. nDCG@10 measures how many related papers appear early and how well they are ordered. Recall@100 is also important because downstream recommendation or reranking systems often depend on a broad candidate set. The dense and hybrid recall values show that candidate coverage is materially better than BM25, but ranking quality still favors dense retrieval.

### Query and Relevance Type Tendencies

Queries resemble paper titles or compressed scientific descriptions. Relevant documents are longer abstracts or paper descriptions. The relation between query and positive may be topical, methodological, citation-like, or application-based. This makes the task sensitive to scientific terminology, domain clustering, noisy translated abstracts, and the ability to distinguish truly related work from papers that only share a term.

### Representative Failure Modes

BM25 can over-rank papers with the same keyword but a different research problem. Dense retrieval can retrieve broadly similar scientific documents that lack the specific scholarly relation used by SCIDOCS. Hybrid retrieval can preserve lexical candidates that are not citation-neighborhood positives, lowering nDCG even when recall is strong. Failures should be analyzed at the document-cluster level, not only by checking whether one retrieved paper looks topical.

### Training and Leakage Considerations

Training should exclude SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, and translated scientific records likely to overlap with the evaluation documents. Useful non-overlapping supervision includes citation prediction pairs, paper recommendation data, co-citation or co-viewed paper pairs, S2ORC-style abstracts, and German or multilingual scholarly retrieval data. Multi-positive training is required because every query is meant to retrieve a related set.

### Model Improvement Signals

Strong performance should come from scientific-document pretraining, citation-informed contrastive learning, and hard negatives from the same research area. Models should learn relatedness beyond title overlap: shared method, citation role, application domain, and experimental framing all matter. Hybrid systems should preserve exact terminology for candidate discovery while allowing dense representations to dominate final relatedness ordering when lexical overlap is not reliable.

## Example Data

| Query | Positive document |
| --- | --- |
| Neuartiger Gleichstrom-Gleichstrom-Mehrstufen-Aufwärtswandler [61 chars] | Mehrstufige Spannungsquellenwandler (Multilevel Voltage Source Converters) etablieren sich als neue Optionen für leistungsstarke Anwendungen. Diese Wandler erzeugen in der Regel eine treppenförmige Spannungswelle aus mehreren Stufen von Gleichspannungskondensatoren. Eine der Hauptbeschränkungen der mehrstufigen Wandler ist die Spannungsungleichgewicht zwischen den verschiedenen Stufen. Die Techniken zur Spannungsausgleichung zwischen den verschiedenen Stufen umfassen in der Regel Spannungsklemmung oder Kondensatorladungssteuerung. Es gibt mehrere Methoden zur Implementierung des Spannungsausgleichs in mehrstufigen Wandlern. Ohne die traditionellen magnetisch gekoppelten Wandler zu berücksichtigen, stellt dieser Artikel drei kürzlich entwickelte mehrstufige Spannungsquellenwandler vor: 1) Dioden-geklemmt, 2) Fliegende Kondensatoren und 3) Kaskadierte Wechselrichter mit separaten Gleichspannungsquellen. Die Betriebsprinzipien, Merkmale, Einschränkungen und potenziellen Anwendungen dieser... [1,000 / 1,027 chars] |
| Schnelles Lernen von sparsen Gaußschen Markov-Feldern basierend auf Cholesky-Zerlegung [86 chars] | Sure, please provide the English document text that you need translated into German. [84 chars] |
| Textursynthese mit Convolutional Neural Networks [48 chars] | In dieser Arbeit untersuchen wir den Einfluss der Tiefe von Faltungsnetzwerken auf deren Genauigkeit in der groß angelegten Bilderkennung. Unser Hauptbeitrag ist eine gründliche Bewertung von Netzwerken zunehmender Tiefe, die zeigt, dass eine erhebliche Verbesserung gegenüber den bisherigen Konfigurationen erreicht werden kann, indem die Tiefe auf 16–19 Gewichtsschichten erhöht wird. Diese Erkenntnisse bildeten die Grundlage für unseren Beitrag zum ImageNet Challenge 2014, bei dem unser Team den ersten und zweiten Platz in den Kategorien Lokalisierung und Klassifizierung belegte. Wir zeigen auch, dass sich unsere Darstellungen gut auf andere Datensätze übertragen, wobei wir Spitzenleistungen erzielen. Wichtig ist, dass wir unsere beiden besten ConvNet-Modelle öffentlich zugänglich gemacht haben, um weitere Forschung über die Nutzung tiefer visueller Darstellungen in der Computer Vision zu fördern. [910 chars] |

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
