# NanoMMTEB-v2 / treccovid

## Overview

`NanoMMTEB-v2 / treccovid` is an English biomedical ad-hoc retrieval task from
the TREC-COVID challenge. Queries are COVID-19 information needs, and documents
are scientific article titles and abstracts from pandemic literature. The Nano
split has 50 queries, 10,000 documents, and 4,527 positive qrel rows. Every
query is heavily multi-positive, averaging 90.54 relevant articles. Current
diagnostics show `reranking_hybrid` as the strongest profile, dense retrieval
second, and BM25 third. All methods find at least one relevant article for most
queries, but ranking many relevant biomedical articles remains difficult.

## Details

### What the Original Data Measures

TREC-COVID constructed an information retrieval test collection over CORD-19
literature during the COVID-19 pandemic. It used evolving search topics, pooled
systems, and relevance judgments from biomedical assessors. The task reflects
real pandemic information needs where terminology, evidence, and literature
coverage changed quickly.

This retrieval task measures biomedical literature search. A model must return
articles addressing questions about treatments, transmission, testing,
serology, biomarkers, epidemiology, social distancing, or clinical outcomes.

### Observed Data Profile

The Nano split contains 50 queries, 10,000 documents, and 4,527 positive qrel
rows. Every query has multiple positives: the average is 90.54 positives per
query, with a minimum of 22, median of 100, and maximum of 100. Queries average
69.24 characters, while documents average 1,321.57 characters.

Documents are biomedical title/abstract records. Example topics ask about
dexamethasone treatment, coronavirus stability on surfaces, social distancing,
serological tests, and biomarkers predicting severe clinical course.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.3627, hit@10 = 0.9200, and recall@100 = 0.2319. BM25 is a
useful biomedical baseline because disease names, drug names, mechanistic
terms, and exact topic wording often appear in article abstracts.

However, BM25 is the weakest of the three provided profiles. Many relevant
articles discuss the same biomedical evidence need using different terminology,
abbreviations, or clinical framing. Ranking among dozens of relevant articles
requires more than term frequency.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.4266, hit@10 = 0.9400, and recall@100 = 0.2576.
Dense retrieval improves over BM25 across all reported metrics.

This suggests that embedding similarity helps connect information needs to
biomedical abstracts when wording differs. Dense retrieval can capture
relationships among interventions, outcomes, pathogens, evidence types, and
clinical mechanisms, though recall@100 remains limited because each query has
many positives.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 candidates per query and
achieves nDCG@10 = 0.4505, hit@10 = 0.9800, and recall@100 = 0.2761. Hybrid
retrieval is the strongest observed profile across the reported metrics.

This is a clear hybrid-search success case. BM25 contributes exact biomedical
terms, while dense retrieval contributes semantic evidence matching. The hybrid
pool still covers only a minority of all positives because there are many
relevant articles, but it ranks strong evidence near the top more effectively
than either component alone.

### Metric Interpretation for Model Researchers

This is an extremely multi-positive task. Hit@10 is easy to satisfy because most
queries have many relevant documents. nDCG@10 is more informative because it
rewards putting relevant biomedical evidence early. Recall@100 should be read
relative to the large positive set; even 100 candidates cannot cover all
relevant articles for many topics.

Researchers should focus on top-rank evidence quality and diversity, not only
whether any relevant article is found.

### Query and Relevance Type Tendencies

Queries are English biomedical information needs about COVID-19. They mention
treatments, virus stability, distancing, antibody tests, biomarkers, clinical
course, transmission, prevention, and public-health measures. Relevant
documents are article titles and abstracts that address the evidence need.

The task rewards both exact biomedical terminology and semantic understanding
of populations, interventions, outcomes, mechanisms, and evidence type.

### Representative Failure Modes

BM25 can over-rank articles that share disease terms but address a different
clinical question. Dense retrieval can retrieve broadly related COVID-19 papers
without matching the specific intervention, outcome, or population. Hybrid
retrieval can still miss relevant diversity when many articles satisfy the same
topic.

Rerankers should distinguish clinical intervention, mechanistic evidence,
observational findings, diagnostics, and epidemiological claims.

### Training Data That May Help

Useful training data includes biomedical literature retrieval, CORD-19 and
PubMed title-abstract retrieval, TREC-style judged biomedical topics outside
this split, and disease or drug matched hard negatives. The Nano split's
TREC-COVID topics, qrels, and judged article records should be excluded from
training.

Synthetic data can generate biomedical titles and abstracts with clinical and
mechanistic evidence. Questions should ask COVID-19 information needs about
populations, interventions, outcomes, and mechanisms. Hard negatives should
share SARS-CoV-2 terminology but differ in clinical or mechanistic focus.

### Model Improvement Notes

Dense retrievers should improve biomedical synonymy, abbreviation handling, and
evidence-type discrimination. Sparse systems should preserve exact disease,
drug, and outcome terms. Rerankers should evaluate whether the article
addresses the specific PICO-style evidence need.

For hybrid systems, `NanoMMTEB-v2 / treccovid` is a strong positive case:
`reranking_hybrid` gives the best nDCG@10, hit@10, and recall@100. The next
challenge is ranking diverse high-quality evidence among many relevant
articles.

## Example Data

| Query | Positive document |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? [69 chars] | Targeting inflammation and cytokine storm in COVID-19 [53 chars] |
| how long does coronavirus remain stable on surfaces? [53 chars] | Body fluids may contribute to human-to-human transmission of severe acute respiratory syndrome coronavirus 2: evidence and practical experience BACKGROUND: In December 2019, an unbelievable outbreak o... [200 / 1,172 chars] |
| has social distancing had an impact on slowing the spread of COVID-19? [70 chars] | A first study on the impact of current and future control measures on the spread of COVID-19 in Germany The novel coronavirus (SARS-CoV-2), identified in China at the end of December 2019 and causing... [200 / 948 chars] |
| are there serological tests that detect antibodies to coronavirus? [66 chars] | Serodiagnostics for Severe Acute Respiratory Syndrome-Related Coronavirus-2: A Narrative Review Accurate serologic tests to detect host antibodies to severe acute respiratory syndrome-related coronavi... [200 / 1,429 chars] |
| which biomarkers predict the severe clinical course of 2019-nCOV infection? [75 chars] | Clinical Features and Predictors for Patients with Severe SARS-CoV-2 Pneumonia: a retrospective multicenter cohort study Objectives: This study was performed to investigate clinical features of patien... [200 / 1,518 chars] |

### Public Sources

- [TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection](https://arxiv.org/abs/2005.04474),
  2020.
- [NIST TREC-COVID challenge page](https://ir.nist.gov/covidSubmit/index.html).
- [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection | 2020 | task paper | [https://arxiv.org/abs/2005.04474](https://arxiv.org/abs/2005.04474) |
| NIST TREC-COVID challenge page | 2020 | challenge page | [https://ir.nist.gov/covidSubmit/index.html](https://ir.nist.gov/covidSubmit/index.html) |
| mteb/trec-covid | 2024 | dataset card | [https://huggingface.co/datasets/mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A question asking for evidence on dexamethasone as COVID-19 treatment. | An article title about inflammation and cytokine storm in COVID-19. |
| A question about coronavirus stability on surfaces. | An abstract discussing SARS-CoV-2 transmission and practical evidence. |
| A question about social distancing and slowing spread. | An article about control measures and COVID-19 spread in Germany. |
| A question about serological tests for coronavirus antibodies. | A review of serodiagnostics for SARS-CoV-2. |
| A question about biomarkers predicting severe infection. | A clinical study of severe SARS-CoV-2 pneumonia predictors. |
