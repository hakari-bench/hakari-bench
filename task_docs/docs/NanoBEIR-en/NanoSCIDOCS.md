# NanoBEIR-en / NanoSCIDOCS

## Overview

NanoSCIDOCS is the compact English NanoBEIR version of SCIDOCS, a scientific related-document retrieval task introduced in the SPECTER evaluation setting. Each query is a scientific paper title, and relevant documents are related scientific papers represented by title-and-abstract text. The retrieval goal is not answer extraction; it is scholarly relatedness. This makes the task useful for evaluating scientific document embeddings, related-work retrieval, citation-style recommendation, and multi-positive ranking over academic text.

## Details

### What the Original Data Measures

SCIDOCS evaluates scientific document representations over tasks connected to citation prediction, user activity, document classification, and recommendation. In BEIR-style retrieval, the task is related-paper retrieval: a paper title should retrieve scientifically related documents. Relevance can reflect topic, method, citation neighborhood, or academic recommendation signals.

The NanoBEIR version keeps this structure in a compact English sample. A strong retriever must compare scientific topics and methods, not merely match a question to an answer. The task rewards document-level scholarly similarity from short titles to longer abstracts.

### Observed Data Profile

The task contains 50 queries, 2,210 documents, and 244 relevance judgments. Every query is multi-positive, with an average of 4.88 positives per query. The minimum is 3, the median is 5.0, the maximum is 5, and all 50 queries are multi-positive.

Queries average 72.78 characters, while documents average 923.57 characters. Queries are paper-title-like, and documents are scientific abstracts or title-and-abstract records. Some records may be sparse or contain metadata artifacts, so a retriever must handle both rich abstracts and less informative entries.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3294, hit@10 of 0.8400, and recall@100 of 0.6148 using the top-500 BM25 candidate subset. Lexical matching works when related papers reuse specialized terms, method names, or application phrases. It can often find at least one related paper.

The lower recall and nDCG show that exact term overlap is not enough. Related scientific papers may use different terminology while sharing a method, task, dataset, or citation context. BM25 can also over-rank papers that share keywords but differ in contribution.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4392, hit@10 of 0.9200, and recall@100 of 0.8115. Dense retrieval is the strongest profile across all reported metrics. It substantially improves both first-page quality and candidate coverage over BM25.

This is the expected behavior for scholarly relatedness. Embedding similarity can capture method and topic relationships that do not rely on exact title words. Dense retrieval is especially valuable when the positive set reflects academic neighborhood rather than direct lexical equivalence.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3962, hit@10 of 0.8800, and recall@100 of 0.7090. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.02 candidates. The hybrid profile improves over BM25 but remains below dense retrieval.

This suggests that dense semantic relatedness is the primary signal for this task. BM25 adds exact terminology coverage, but combining it with dense retrieval does not surpass the dense-only profile here. For reranking, reranking_hybrid is still a useful pool, but dense candidates appear strongest.

### Metric Interpretation for Model Researchers

Because every query has several positives, hit@10 is less informative than nDCG@10 and recall@100. A system can find one related paper while missing most of the related set. nDCG@10 measures whether the top list is useful for related-work browsing, and recall@100 measures whether a reranker can access the broader relevant set.

The comparison shows that BM25 captures technical terms, dense retrieval captures scholarly relatedness best, and reranking_hybrid provides a middle ground. This task is a strong diagnostic for scientific embedding quality.

### Query and Relevance Type Tendencies

Queries include topics such as multilevel DC-DC boost converters, sparse Gaussian Markov random fields, texture synthesis with convolutional neural networks, circularly polarized RFID antennas, and digital heartbeat monitors. Relevant documents are papers related by method, application, field, or citation-style context.

The task rewards matching research contribution and academic neighborhood. A paper can share a common term but be irrelevant, while a positive may use different terminology for the same method family or application domain.

### Representative Failure Modes

Likely failures include over-ranking keyword neighbors, missing related papers that use different terminology, confusing broad fields with specific methods, and under-covering the multi-positive related set. BM25 may be too narrow, while dense retrieval can still fail on sparse metadata or very technical abbreviations.

### Training Data That May Help

Useful training data includes non-overlapping scientific citation pairs, co-citation pairs, related-paper recommendation logs, Semantic Scholar-style title/abstract/citation triples, and hard negatives from nearby venues or topics. Multi-positive and listwise objectives are appropriate because each query has several related papers.

### Model Improvement Notes

A model targeting this task should optimize for document-level scientific relatedness. Sparse systems need field-aware indexing for titles, abstracts, and method terms. Dense systems are the strongest baseline and should use citation-informed or recommendation-informed training. Hybrid systems can help with rare terminology but should not dilute the dense scientific relation signal.

## Example Data

| Query | Positive document |
| --- | --- |
| Novel DC-DC Multilevel Boost Converter [38 chars] | AbstructMultilevel voltage source converters are emerging as a new breed of power converter options for high-power applications. The multilevel voltage source converters typically synthesize the staircase voltage wave from several levels of dc capacitor voltages. One of the major limitations of the multilevel converters is the voltage unbalance between different levels. The techniques to balance the voltage between different levels normally involve voltage clamping or capacitor charge control. There are several ways of implementing voltage balance in multilevel converters. Without considering the traditional magnetic coupled converters, this paper presents three recently developed multilevel voltage source converters: 1) diode-clamp, 2) flyingcapacitors, and 3) cascaded-inverters with separate dc sources. The operating principle, features, constraints, and potential applications of these converters will be discussed. [930 chars] |
| Fast Sparse Gaussian Markov Random Fields Learning Based on Cholesky Factorization [82 chars] |  [0 chars] |
| Texture Synthesis Using Convolutional Neural Networks [53 chars] | In this work we investigate the effect of the convolutional n etwork depth on its accuracy in the large-scale image recognition setting. Our main contribution is a thorough evaluation of networks of increasing depth, which shows that a significant improvement on the prior-art configurations can be achi eved by pushing the depth to 16–19 weight layers. These findings were the basis of our ImageNet Challenge 2014 submission, where our team secured the first a nd he second places in the localisation and classification tracks respec tively. We also show that our representations generalise well to other datasets, whe re t y achieve the stateof-the-art results. Importantly, we have made our two bestp rforming ConvNet models publicly available to facilitate further research o n the use of deep visual representations in computer vision. [840 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original evaluation context | [SPECTER](https://arxiv.org/abs/2004.07180) |
| Proceedings page | [SPECTER ACL Anthology page](https://aclanthology.org/2020.acl-main.207/) |
| Project repository | [SCIDOCS GitHub repository](https://github.com/allenai/scidocs) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Source dataset card | [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs) |

Representative query and positive document snippets:

| Query | Positive document snippet |
| --- | --- |
| Novel DC-DC Multilevel Boost Converter | Multilevel voltage source converters are emerging as power converter options for high-power applications. |
| Fast Sparse Gaussian Markov Random Fields Learning Based on Cholesky Factorization | A sparse metadata record appears as a related scientific document. |
| Texture Synthesis Using Convolutional Neural Networks | A paper investigates the effect of convolutional network depth on large-scale image recognition accuracy. |
| Planar broadband annular-ring antenna with circular polarization for RFID system | A horizontally meandered strip feed technique is proposed for a circularly polarized stacked patch antenna. |
| Design of advanced digital heartbeat monitor using basic electronic components | A paper presents an integrated device for measuring heart rate using a fingertip. |
