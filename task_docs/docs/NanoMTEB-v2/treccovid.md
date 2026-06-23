# NanoMTEB-v2 / treccovid

## Overview

`NanoMTEB-v2 / treccovid` is a biomedical ad hoc retrieval task from the TREC-COVID challenge. Queries are COVID-19 information needs, and relevant documents are scientific article records from pandemic literature, typically titles plus abstracts. TREC-COVID was built as a rapidly developed information retrieval test collection over COVID-19 research, with relevance judgments coordinated across multiple rounds. This Nano split contains only 50 queries but has 4,584 positive qrels, so every query is highly multi-positive. It is useful for evaluating biomedical retrieval, scientific terminology, and the difference between first-hit success and broad relevant-document coverage.

## Details

### What the Original Data Measures

TREC-COVID measures retrieval over COVID-19 scientific literature. Topics ask about clinical, epidemiological, virological, and public-health information needs. Relevant documents are research articles or abstracts that address the need.

The task differs from ordinary web QA because many documents can be relevant to a single topic, and relevance depends on biomedical specificity: population, intervention, outcome, disease mechanism, study type, or evidence target.

### Observed Data Profile

The Nano split contains 50 queries, 10,000 documents, and 4,584 positive qrel rows. Queries have 91.68 positives on average, with a median of 100 and a maximum of 100. Every query is multi-positive. Queries average 69.24 characters, while documents average 1,326.60 characters.

The examples ask about dexamethasone treatment, coronavirus stability on surfaces, social distancing, antibody tests, and biomarkers for severe clinical course. Documents are biomedical title-abstract records and often contain dense scientific terminology.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3893, hit@10 of 0.9200, and recall@100 of 0.2319. BM25 frequently finds at least one relevant article because COVID-19 topics share exact biomedical terms with abstracts. However, recall@100 is low relative to the very large number of positives per query.

This means sparse retrieval is useful for first-hit discovery but limited for broad evidence gathering. It may over-rank articles with matching disease or drug terms while missing relevant studies that use different clinical phrasing.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.4177, hit@10 of 0.9200, and recall@100 of 0.2716. Dense retrieval improves both nDCG@10 and recall@100 over BM25, showing that semantic matching helps with biomedical information needs.

The gain is moderate rather than overwhelming because biomedical terminology is highly lexical and exact terms matter. Dense retrieval helps bridge wording differences between topic statements and article abstracts, but biomedical domain specialization remains important.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard positives. It reaches nDCG@10 of 0.4521, hit@10 of 0.9800, and recall@100 of 0.2860. This is the strongest profile across the three candidate types. Hybrid retrieval combines exact biomedical term matching with semantic matching and improves both top-rank relevance and candidate coverage.

The recall numbers remain low because each query has many judged positives. The hybrid pool is best among the available candidates, but it still represents only a fraction of the relevant literature for broad biomedical review.

### Metric Interpretation for Model Researchers

Hit@10 is not enough for this task. With dozens of positives per query, a system can easily retrieve one relevant article while missing most of the relevant set. nDCG@10 captures the quality of the first page of results, while recall@100 captures evidence coverage.

The hybrid profile is the strongest candidate-generation signal. For downstream systematic review or evidence synthesis, broader recall and diversification may be more important than first-hit success.

### Query and Relevance Type Tendencies

Queries are concise biomedical information needs about COVID-19, SARS-CoV-2, treatments, diagnostics, transmission, risk factors, and clinical outcomes. Relevant documents are title-abstract records from the scientific literature.

The relevance relation is biomedical topical and evidential relevance. A document should address the information need, not merely mention COVID-19.

### Representative Failure Modes

Common failures include retrieving articles that mention the same drug or disease but answer a different clinical question, confusing diagnostic-test topics with antibody biology, missing population or outcome constraints, and over-ranking generic COVID-19 abstracts. Dense systems may retrieve broad semantic matches; sparse systems may rely too heavily on exact biomedical keywords.

### Training Data That May Help

Useful training data includes biomedical literature retrieval pairs, CORD-19 or PubMed title-abstract retrieval data, TREC-COVID topics and qrels outside this Nano split, and hard negatives that share disease or drug terms while differing in population, intervention, outcome, or evidence type. Multi-positive training is required.

### Model Improvement Notes

Models should preserve biomedical exactness while improving semantic recall. Domain-specific encoders, MeSH or entity-aware training, and hard negatives by clinical facet are likely helpful. Rerankers should prioritize whether an abstract addresses the topic's specific evidence need rather than only sharing COVID-19 vocabulary.

## Example Data

| Query | Positive document |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? [69 chars] | The Combination of Tocilizumab and Methylprednisolone Along With Initial Lung Recruitment Strategy in Coronavirus Disease 2019 Patients Requiring Mechanical Ventilation: A Series of 21 Consecutive Cas... [200 / 1,757 chars] |
| how long does coronavirus remain stable on surfaces? [53 chars] | Body fluids may contribute to human-to-human transmission of severe acute respiratory syndrome coronavirus 2: evidence and practical experience BACKGROUND: In December 2019, an unbelievable outbreak o... [200 / 1,172 chars] |
| has social distancing had an impact on slowing the spread of COVID-19? [70 chars] | Increased Detection coupled with Social Distancing and Health Capacity Planning Reduce the Burden of COVID-19 Cases and Fatalities: A Proof of Concept Study using a Stochastic Computational Simulation... [200 / 1,576 chars] |
| are there serological tests that detect antibodies to coronavirus? [66 chars] | A Guide to COVID‐19: a global pandemic caused by the novel coronavirus SARS‐CoV‐2 The emergence of the SARS‐CoV‐2 strain of the human coronavirus has thrown the world into the midst of a new pandemic.... [200 / 1,084 chars] |
| which biomarkers predict the severe clinical course of 2019-nCOV infection? [75 chars] | Clinical course and outcome of 107 patients infected with the novel coronavirus, SARS-CoV-2, discharged from two hospitals in Wuhan, China BACKGROUND: In December 2019, coronavirus disease 2019 (COVID... [200 / 1,932 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection | 2020 | source task paper | [https://arxiv.org/abs/2005.04474](https://arxiv.org/abs/2005.04474) |
| NIST TREC-COVID | 2020 | challenge page | [https://ir.nist.gov/covidSubmit/index.html](https://ir.nist.gov/covidSubmit/index.html) |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/trec-covid |  | dataset card | [https://huggingface.co/datasets/mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? | A biomedical abstract about immunomodulatory treatment and mechanical ventilation in COVID-19 patients. |
| how long does coronavirus remain stable on surfaces? | An abstract discussing SARS-CoV-2 transmission evidence and practical experience. |
| has social distancing had an impact on slowing the spread of COVID-19? | An abstract about increased detection, social distancing, health capacity planning, and simulation of COVID-19 cases. |
| are there serological tests that detect antibodies to coronavirus? | A guide-style abstract about COVID-19, SARS-CoV-2, and immune response concepts. |
| which biomarkers predict the severe clinical course of 2019-nCOV infection? | A clinical abstract about patients infected with SARS-CoV-2 and their outcomes. |
