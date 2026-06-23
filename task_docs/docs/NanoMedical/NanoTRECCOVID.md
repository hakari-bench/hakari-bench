# NanoMedical / NanoTRECCOVID

## Overview

`NanoMedical / NanoTRECCOVID` is an English COVID-19 scientific literature retrieval task derived from TREC-COVID. Queries are pandemic information needs about SARS-CoV-2 origin, transmission, testing, treatments, vaccines, public-health interventions, and clinical outcomes. Documents are CORD-19-style scientific article records, usually represented by title and abstract. The original TREC-COVID benchmark was built during the pandemic to evaluate retrieval over rapidly changing biomedical literature. This Nano split reduces the task to 50 question-style queries with one positive document per query, making it a compact test of exact evidence retrieval for COVID-19 scientific search.

## Details

### What the Original Data Measures

TREC-COVID measures ad hoc retrieval over COVID-19 and coronavirus literature. Topics were designed as biomedical and public-health information needs, with judgments over CORD-19 documents. The original task included many relevance judgments per topic, but this Nano split is a single-positive retrieval setup sampled from that larger evidence-search surface.

The task is not general pandemic FAQ retrieval. It asks whether a system can retrieve a scientific article record that is responsive to a specific research or clinical question.

### Observed Data Profile

The Nano split contains 50 queries, 10,000 documents, and 50 positive qrel rows. Each query has exactly one positive document. Queries average 69.24 characters, while documents average 1,208.78 characters.

The examples ask about dexamethasone, coronavirus stability on surfaces, social distancing, serological antibody tests, and biomarkers for severe clinical course. Documents are biomedical article-title plus abstract passages, although some records may be shorter or title-like.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3983, hit@10 of 0.5200, and recall@100 of 0.8000. BM25 is moderately effective because many queries contain exact biomedical terms such as drug names, antibody, serological, coronavirus, COVID-19, or biomarkers.

Its weaknesses come from the density of shared pandemic vocabulary. Many documents mention COVID-19 and related terms, so lexical overlap can retrieve topically related papers that do not answer the specific information need. BM25 has the best standalone recall@100, but only around half of positives appear in the top 10.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3875, hit@10 of 0.5200, and recall@100 of 0.7000. Dense retrieval is close to BM25 in top-rank quality but lower in recall@100.

This suggests that general semantic matching helps with biomedical intent, but exact terminology and article-specific evidence remain important. Dense retrieval may retrieve broadly relevant COVID-19 abstracts while missing the specific positive selected for the Nano split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with two queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.3193, hit@10 of 0.4400, and recall@100 of 0.9600. The hybrid pool has the best recall@100 by a large margin, but its top-rank quality is lower than BM25 and dense retrieval.

This is an important separation between coverage and ordering. Hybrid retrieval is the best candidate pool for downstream reranking, but the first-stage hybrid order itself should not be treated as the final ranking.

### Metric Interpretation for Model Researchers

This Nano split has one positive per query, unlike the broader TREC-COVID collection where topics have many judged relevant documents. nDCG@10 therefore mostly reflects whether the sampled positive document is ranked early. Recall@100 is especially important for reranking because the hybrid pool recovers nearly all positives.

The task should be read as compact evidence-document retrieval, not as full systematic-review coverage.

### Query and Relevance Type Tendencies

Queries are concise English biomedical or public-health questions about COVID-19. Relevant documents are scientific article title-abstract records that address the question.

The relevance relation is evidence responsiveness. A paper about COVID-19 in general is not enough if it does not answer the intervention, mechanism, test, population, or outcome asked about.

### Representative Failure Modes

Common failures include retrieving papers with the same pandemic terms but the wrong intervention or outcome, confusing coronavirus family evidence with SARS-CoV-2 evidence, missing title-only positives, and over-ranking broad overview papers. Dense systems may match general semantic topic; sparse systems may over-weight exact COVID vocabulary.

### Training Data That May Help

Useful training data includes non-overlapping COVID-19 literature retrieval judgments, biomedical ad hoc retrieval data, clinical and public-health question-to-abstract data, and hard negatives from coronavirus or influenza literature. TREC-COVID complete qrels for the evaluation topics and exact positive documents from this split should be excluded for clean zero-shot evaluation.

### Model Improvement Notes

Models should combine exact biomedical term handling with semantic information-need matching. Hard negatives should share COVID-19 vocabulary but differ in intervention, population, outcome, or virus family. Rerankers should be evaluated on the hybrid pool because it provides the broadest candidate coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? [69 chars] | The Combination of Tocilizumab and Methylprednisolone Along With Initial Lung Recruitment Strategy in Coronavirus Disease 2019 Patients Requiring Mechanical Ventilation: A Series of 21 Consecutive Cases OBJECTIVE: To describe the outcomes with use of a combination of tocilizumab and methylprednisolone administered around the time of endotracheal intubation in patients with confirmed coronavirus disease 2019-associated hypoxemic respiratory failure requiring mechanical ventilation. DATA SOURCES: Retrospective chart review. STUDY SELECTION/DATA EXTRACTION: Twenty-one consecutive patients with confirmed coronavirus disease 2019-associated hypoxemic respiratory failure requiring mechanical ventilation. Initial ventilator parameters were positive end-expiratory pressure 14 cm H(2)o and target plateau pressure 29 cm H(2)o to maximize lung recruitment. Methylprednisolone (125 mg every 6hr for 24 hr with tapering to 60 mg every 12 hr) was administered shortly after patients were intubated (med... [1,000 / 1,756 chars] |
| how long does coronavirus remain stable on surfaces? [53 chars] | Body fluids may contribute to human-to-human transmission of severe acute respiratory syndrome coronavirus 2: evidence and practical experience BACKGROUND: In December 2019, an unbelievable outbreak of pneumonia associated with coronavirus was reported in the city of Wuhan, Hubei Province. This virus was called severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). Although much effort has been spent on clarifying the transmission route of SARS-CoV-2, but, very little evidence is available regarding the relationship between human body fluids and transmission of SARS-CoV-2 virus. Considerable evidence from hospital in Wuhan indicates that strict rules to avoid occupational exposure to patients’ body fluids in healthcare settings, particularly among every medical staff, limited person-to-person transmission of nosocomial infections by direct or indirect contact. CONCLUSION: We tried to provide important information for understanding the possible transmission routes of SARS-CoV-2 v... [1,000 / 1,171 chars] |
| has social distancing had an impact on slowing the spread of COVID-19? [70 chars] | Increased Detection coupled with Social Distancing and Health Capacity Planning Reduce the Burden of COVID-19 Cases and Fatalities: A Proof of Concept Study using a Stochastic Computational Simulation Model Objective: In absence of any vaccine, the Corona Virus Disease 2019 (COVID-19) pandemic is being contained through a non-pharmaceutical measure termed Social Distancing (SD). However, whether SD alone is enough to flatten the epidemic curve is debatable. Using a Stochastic Computational Simulation Model, we investigated the impact of increasing SD, hospital beds and COVID-19 detection rates in preventing COVID-19 cases and fatalities. Research Design and Methods: The Stochastic Simulation Model was built using the EpiModel package in R. As a proof of concept study, we ran the simulation on Kasaragod, the most affected district in Kerala. We added 3 compartments to the SEIR model to obtain a SEIQHRF (Susceptible-Exposed-Infectious-Quarantined-Hospitalised-Recovered-Fatal) model. Resu... [1,000 / 1,575 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID | 2021 | arXiv paper | [https://arxiv.org/abs/2104.09632](https://arxiv.org/abs/2104.09632) |
| TREC-COVID data archive | 2020 | benchmark archive | [https://ir.nist.gov/trec-covid/](https://ir.nist.gov/trec-covid/) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? | An article record about tocilizumab, methylprednisolone, lung recruitment strategy, and mechanically ventilated COVID-19 patients. |
| how long does coronavirus remain stable on surfaces? | An abstract discussing SARS-CoV-2 transmission evidence and practical experience with body fluids. |
| has social distancing had an impact on slowing the spread of COVID-19? | An abstract about increased detection, social distancing, health capacity planning, and stochastic simulation of COVID-19 burden. |
| are there serological tests that detect antibodies to coronavirus? | A narrative review on serodiagnostics for SARS-CoV-2 and host antibody testing. |
| which biomarkers predict the severe clinical course of 2019-nCOV infection? | A retrospective multicenter cohort study about severe SARS-CoV-2 pneumonia and clinical predictors. |
