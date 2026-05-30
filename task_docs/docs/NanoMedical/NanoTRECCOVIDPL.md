# NanoMedical / NanoTRECCOVIDPL

## Overview

`NanoMedical / NanoTRECCOVIDPL` is the Polish BEIR-PL adaptation of TREC-COVID. Queries are Polish translations of COVID-19 information needs, and documents are Polish translations of CORD-19 scientific article records. The underlying retrieval task comes from TREC-COVID, while BEIR-PL adds the Polish translation layer. This Nano split contains 50 single-positive queries over 10,000 documents. It is useful for evaluating multilingual biomedical retrieval under machine-translated scientific text, where models must handle Polish morphology, translated pandemic terminology, and exact information-need matching.

## Details

### What the Original Data Measures

TREC-COVID measures retrieval over COVID-19 scientific literature. BEIR-PL translates BEIR-style datasets into Polish to evaluate zero-shot Polish retrieval. This task combines both: it keeps the COVID-19 information needs and evidence-document structure, but presents queries and documents in Polish.

The target is a scientific article record that answers or addresses the specific information need. General COVID-19 topicality is not enough.

### Observed Data Profile

The Nano split contains 50 queries, 10,000 documents, and 50 positive qrel rows. Each query has exactly one positive document. Queries average 69.42 characters, while documents average 1,251.91 characters.

The examples ask about dexamethasone treatment, surface stability, social distancing, serological antibody tests, and biomarkers for severe clinical course. Documents are translated title-plus-abstract records, often retaining names such as SARS-CoV-2, COVID-19, biomarkers, remdesivir, dexamethasone, and antibody terminology.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3266, hit@10 of 0.4400, and recall@100 of 0.7000. BM25 is weaker than in the English NanoTRECCOVID split. Polish inflection, translated phrasing, and biomedical terminology variation reduce exact overlap, even when the underlying topic is the same.

Sparse retrieval still helps when drug names, virus names, or technical terms are preserved. It struggles when the question and translated abstract express the same evidence relation with different Polish wording.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3585, hit@10 of 0.5200, and recall@100 of 0.8600. Dense retrieval improves over BM25 across all reported metrics, especially recall@100.

This shows that semantic retrieval is important for translated Polish biomedical search. The model must bridge inflected and translated forms while preserving the specific intervention, population, outcome, or test in the information need.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with two queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.3864, hit@10 of 0.5400, and recall@100 of 0.9600. This is the strongest profile across the candidate types.

Hybrid retrieval is therefore the best candidate-generation strategy for this task. It combines exact preserved biomedical terms from BM25 with dense matching across Polish translation variation.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 and hit@10 directly measure whether the sampled positive appears early. Recall@100 measures candidate availability for reranking. Comparing this task with English NanoTRECCOVID is useful for identifying the added cost of translation and Polish retrieval.

The hybrid advantage suggests that multilingual biomedical systems should retain sparse exact-term behavior while using dense semantic matching.

### Query and Relevance Type Tendencies

Queries are Polish clinical, biological, or public-health COVID-19 information needs. Relevant documents are translated scientific article records.

The relevance relation is evidence responsiveness to the translated question. A document must address the specific treatment, test, intervention, risk factor, or mechanism.

### Representative Failure Modes

Common failures include matching generic COVID-19 passages, missing translated drug or test names, confusing older coronavirus literature with SARS-CoV-2 evidence, and failing on Polish inflection or phrasing changes. Sparse systems underperform when surface forms diverge; dense systems can still retrieve broad topic matches with the wrong evidence type.

### Training Data That May Help

Useful training data includes non-overlapping Polish COVID-19 literature retrieval data, translated biomedical ad hoc retrieval data, Polish public-health QA and medical retrieval data, and multilingual CORD-19 retrieval with hard negatives. BEIR-PL TREC-COVID test examples, translated positives, and translated duplicates of English TREC-COVID evaluation topics should be excluded.

### Model Improvement Notes

Models should preserve biomedical entity names while supporting Polish morphology and translation variation. Hard negatives should share COVID-19 vocabulary but differ in population, intervention, outcome, or evidence type. Hybrid candidate generation is the most useful setup for reranking experiments on this split.

## Example Data

### Public Sources

- [BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language](https://arxiv.org/abs/2305.19840), 2024.
- [BEIR-PL ACL Anthology record](https://aclanthology.org/2024.lrec-main.194/).
- [Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID](https://arxiv.org/abs/2104.09632), 2021.
- [TREC-COVID data archive](https://ir.nist.gov/trec-covid/).
- [clarin-knext Hugging Face](https://huggingface.co/clarin-knext).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | arXiv paper | https://arxiv.org/abs/2305.19840 |
| BEIR-PL: Zero Shot Information Retrieval Benchmark for the Polish Language | 2024 | ACL Anthology paper | https://aclanthology.org/2024.lrec-main.194/ |
| Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID | 2021 | arXiv paper | https://arxiv.org/abs/2104.09632 |
| TREC-COVID data archive | 2020 | benchmark archive | https://ir.nist.gov/trec-covid/ |
| clarin-knext |  | Hugging Face publisher | https://huggingface.co/clarin-knext |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| jakie są dowody na to, że deksametazon może być stosowany w leczeniu COVID-19? | A Polish translated article record about tocilizumab, methylprednisolone, lung recruitment, and mechanically ventilated COVID-19 patients. |
| jak długo koronawirus pozostaje stabilny na powierzchniach? | A translated abstract about SARS-CoV-2 transmission evidence and practical experience. |
| czy dystans społeczny miał wpływ na spowolnienie rozprzestrzeniania się COVID-19? | A translated abstract about increased detection, social distancing, health planning, and stochastic simulation of COVID-19 burden. |
| czy istnieją testy serologiczne wykrywające przeciwciała przeciwko koronawirusowi? | A translated narrative review on serodiagnostics and host antibody testing for SARS-CoV-2. |
| które biomarkery przewidują ciężki przebieg kliniczny zakażenia 2019-nCOV? | A translated retrospective cohort study about severe SARS-CoV-2 pneumonia and clinical predictors. |
