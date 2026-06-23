# NanoBEIR-en / NanoSciFact

## Overview

NanoSciFact is the compact English NanoBEIR version of SciFact, a scientific claim evidence retrieval task. Each query is a scientific claim, and the corpus contains research abstracts that can support or refute it. The retrieval goal is to surface evidence abstracts for downstream scientific verification. This makes the task useful for evaluating biomedical evidence retrieval, scientific terminology handling, and claim-to-abstract ranking.

## Details

### What the Original Data Measures

SciFact was designed for verifying scientific claims against the research literature. The full task includes selecting evidence abstracts, identifying rationale sentences, and determining whether the evidence supports or refutes the claim. In retrieval form, the first step is evaluated: can the system retrieve the abstracts that contain the evidence?

The NanoBEIR version keeps this scientific claim-to-evidence structure. A strong retriever must match a precise claim to an abstract that addresses it, even when the abstract uses technical wording, measurements, interventions, or outcomes rather than repeating the claim verbatim.

### Observed Data Profile

The task contains 50 queries, 2,919 documents, and 56 relevance judgments. Most queries have one positive abstract, with an average of 1.12 positives per query. The minimum is 1, the median is 1.0, the maximum is 4, and 4 queries are multi-positive, or 8.0% of the set.

Queries average 95.80 characters, while documents average 1,431.23 characters. Claims are longer and more technical than ordinary web questions, and documents are long scientific abstracts. The model must align a compact claim with the study evidence that can verify it.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.7282, hit@10 of 0.8800, and recall@100 of 0.9464 using the top-500 BM25 candidate subset. This is a strong lexical baseline. Scientific claims often contain distinctive biomedical terms, abbreviations, proteins, diseases, methods, or interventions that appear in the relevant abstract.

The remaining failures occur when shared terminology is not enough to identify the verifying abstract. BM25 can retrieve abstracts about the same entity or process while missing the paper that actually supports or refutes the claim. Exact terms help, but evidence relation still matters.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.7679, hit@10 of 0.8400, and recall@100 of 0.9286. Dense retrieval has the best nDCG@10, indicating stronger top-rank ordering when it finds the evidence. It is slightly weaker than BM25 on hit@10 and recall@100.

This pattern suggests that embedding similarity helps rank scientific evidence by claim meaning, but exact biomedical anchors remain important for full candidate coverage. Dense retrieval is useful for paraphrased or relation-oriented claims, while sparse matching protects rare technical names.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.7397, hit@10 of 0.8800, and recall@100 of 0.9821. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.02 candidates. The hybrid profile has the best recall@100 and matches BM25 hit@10, while dense retrieval has the best nDCG@10.

This makes reranking_hybrid the strongest candidate pool for downstream scientific verification. It combines sparse technical-term coverage with dense semantic matching and gives a verifier the highest chance of seeing the evidence abstract within the top 100.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 measures whether the evidence abstract is visible, and nDCG@10 measures how early it is ranked. recall@100 is critical for verification pipelines because later claim classification cannot recover missing evidence.

The comparison shows a useful split: BM25 is strong for terminology, dense retrieval is strongest for direct top-rank evidence ordering, and reranking_hybrid is best for candidate completeness. This task is a good diagnostic for balancing biomedical lexical precision with scientific semantic matching.

### Query and Relevance Type Tendencies

Queries include claims about Ly49Q and neutrophil migration, antiretroviral therapy and tuberculosis, interferon-induced genes and West Nile virus, HPV screening sensitivity, and TDP-43 interactions with respiratory complex proteins. Relevant documents are scientific abstracts with background, methods, results, and conclusions.

The task rewards evidence relation matching. A passage must address the claim's biological or clinical relation, not merely mention the same disease, protein, or method. Same-entity scientific abstracts are hard negatives.

### Representative Failure Modes

Likely failures include retrieving abstracts that share terminology but test a different hypothesis, missing evidence because the wording is paraphrased, confusing direction of effect, and over-ranking broad background abstracts. BM25 may be too term-driven, while dense retrieval may underweight rare biomedical identifiers.

### Training Data That May Help

Useful training data includes non-overlapping SciFact training claims, scientific claim and evidence abstract pairs, biomedical entailment data, scientific NLI, citation-sentence-to-cited-abstract supervision, and hard negatives that share terms but do not verify the claim. Both support and refute evidence should be represented.

### Model Improvement Notes

A model targeting this task should preserve exact biomedical identifiers while improving claim-evidence relation ranking. Sparse systems need strong biomedical tokenization and acronym handling. Dense systems need scientific claim-to-abstract training. Hybrid systems are promising for reranking because they provide the highest evidence coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q directs the organization of neutrophil migration to inflammation sites by regulating membrane... [100 / 115 chars] | Neutrophils rapidly undergo polarization and directional movement to infiltrate the sites of infection and inflammation. Here, we show that an inhibitory MHC I receptor, Ly49Q, was crucial for the swi... [200 / 990 chars] |
| Antiretroviral therapy reduces rates of tuberculosis across a broad range of CD4 strata. [88 chars] | BACKGROUND Human immunodeficiency virus (HIV) infection is the strongest risk factor for developing tuberculosis and has fuelled its resurgence, especially in sub-Saharan Africa. In 2010, there were a... [200 / 2,144 chars] |
| Rapid up-regulation and higher basal expression of interferon-induced genes reduce survival of granu... [100 / 153 chars] | Although susceptibility of neurons in the brain to microbial infection is a major determinant of clinical outcome, little is known about the molecular factors governing this vulnerability. Here we sho... [200 / 1,153 chars] |
| Primary cervical cancer screening with HPV detection has higher longitudinal sensitivity than conven... [100 / 169 chars] | BACKGROUND Screening for cervical cancer based on testing for human papillomavirus (HPV) increases the sensitivity of detection of high-grade (grade 2 or 3) cervical intraepithelial neoplasia, but whe... [200 / 2,284 chars] |
| Blocking the interaction between TDP-43 and respiratory complex I proteins ND3 and ND6 leads to incr... [100 / 135 chars] | Genetic mutations in TAR DNA-binding protein 43 (TARDBP, also known as TDP-43) cause amyotrophic lateral sclerosis (ALS), and an increase in the presence of TDP-43 (encoded by TARDBP) in the cytoplasm... [200 / 1,244 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [SciFact](https://arxiv.org/abs/2004.14974) |
| Proceedings page | [SciFact EMNLP page](https://aclanthology.org/2020.emnlp-main.609/) |
| Project repository | [SciFact GitHub repository](https://github.com/allenai/scifact) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Source dataset card | [mteb/scifact](https://huggingface.co/datasets/mteb/scifact) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Ly49Q directs the organization of neutrophil migration to inflammation sites by regulating membrane raft functions. | Neutrophils rapidly undergo polarization and directional movement to infiltrate infection and inflammation sites. |
| Antiretroviral therapy reduces rates of tuberculosis across a broad range of CD4 strata. | HIV infection is the strongest risk factor for developing tuberculosis and has fueled its resurgence. |
| Rapid up-regulation and higher basal expression of interferon-induced genes reduce survival of granule cell neurons infected by West Nile virus. | The abstract discusses molecular factors governing neuronal susceptibility to microbial infection. |
| Primary cervical cancer screening with HPV detection has higher longitudinal sensitivity than conventional cytology. | HPV testing increases sensitivity for detecting high-grade cervical intraepithelial neoplasia. |
| Blocking the interaction between TDP-43 and respiratory complex I proteins ND3 and ND6 leads to increased neuronal loss. | Mutations in TAR DNA-binding protein 43 are connected to amyotrophic lateral sclerosis. |
