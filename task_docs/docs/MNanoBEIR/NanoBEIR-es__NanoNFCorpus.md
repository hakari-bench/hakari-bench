# MNanoBEIR / NanoBEIR-es / NanoNFCorpus

## Overview

This task is the Spanish NanoBEIR version of NFCorpus, a medical information retrieval benchmark built from consumer health and nutrition information needs linked to biomedical articles. The original NFCorpus collection was designed as a learning-to-rank dataset where short lay health queries connect to PubMed and medical evidence documents. In this NanoBEIR slice, short Spanish translated health queries must retrieve Spanish translated medical or biomedical documents from 2,953 candidates. The task contains 50 queries and 1,651 positive relevance judgments, with an average of 33.02 positives per query. It is therefore a dense many-positive benchmark for lay-to-technical medical retrieval, where models must recover multiple relevant evidence documents for the same health topic.

## Details

### What the Original Data Measures

NFCorpus measures the gap between consumer health language and biomedical literature. A query may be a short topic label such as a food, diet, supplement, disease, or health concern, while relevant documents may describe mechanisms, interventions, cohorts, outcomes, or study designs in technical language. The retrieval task is not to find a single answer passage; it is to rank a set of medically relevant evidence documents.

### Observed Data Profile

The Spanish Nano task has 50 queries, 2,953 documents, and 1,651 positives. Positives per query average 33.02, with a median of 23.5 and a maximum of 100. Forty-seven queries are multi-positive. Queries are very short, averaging about 27 characters, while documents are long, averaging about 1,732 characters. Examples include healthy chocolate shakes, medical ethics, fava beans, chicken nuggets, and saturated fat. Documents are translated biomedical abstracts or scientific summaries.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.272, Hit@10 of 0.600, and Recall@100 of 0.164. Sparse retrieval can find at least one relevant document when a query term directly appears in a biomedical abstract, but its recall is low relative to the large number of positives. Short lay queries often do not share terminology with scientific documents, and even exact food or disease words may appear in many partially related abstracts. BM25 therefore under-recovers the evidence set.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is slightly stronger, with nDCG@10 of 0.276, Hit@10 of 0.680, and Recall@100 of 0.209. Dense retrieval improves first-page hits and recall by bridging consumer terms to biomedical concepts. However, the improvement is modest, which shows that generic embedding similarity still struggles with domain-specific medical evidence. The task requires recognizing interventions, outcomes, mechanisms, and article-level relevance, not only broad topical similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.284, Hit@10 of 0.620, and Recall@100 of 0.204, with seven safeguard rows at 101 candidates. It gives the best nDCG@10 but does not beat dense retrieval on Hit@10 or Recall@100. This means hybrid search slightly improves early graded ranking while preserving similar evidence coverage to dense retrieval. BM25 contributes exact medical or food terms, while dense retrieval provides lay-to-technical matching; neither signal alone is sufficient for broad evidence recall.

### Metric Interpretation for Model Researchers

NFCorpus must be read as a many-positive retrieval task. Hit@10 only indicates whether at least one relevant document appears and hides the difficulty of retrieving dozens of evidence documents. Recall@100 is low for all profiles, showing that candidate generation remains hard. nDCG@10 is useful for top-rank quality, but researchers should also inspect whether the retrieved documents cover the range of relevant biomedical evidence for a health topic.

### Query and Relevance Type Tendencies

Queries are short Spanish health topics or lay questions. Relevant documents are long biomedical abstracts and medical summaries. A single query may have positives spanning different studies, mechanisms, populations, and outcomes. Hard negatives often share a disease or diet term while studying a different outcome or intervention. This makes the task sensitive to medical domain knowledge and lay-to-scientific vocabulary mapping.

### Representative Failure Modes

BM25 can miss documents that discuss the concept using technical terminology. Dense retrieval can retrieve medically adjacent abstracts that are not relevant to the specific health topic. Hybrid retrieval can improve ranking but still miss most positives because the evidence set is large and diverse. Failure analysis should look at missing evidence clusters, not only the first retrieved positive.

### Training and Leakage Considerations

Training should exclude NFCorpus, BEIR, NanoBEIR, and translated NutritionFacts records likely to overlap with these queries or linked medical documents. Useful non-overlapping data includes biomedical IR datasets, consumer-health QA to abstract pairs, PubMed ranking data, and Spanish or multilingual medical retrieval supervision. Multi-positive training is recommended because most queries require many valid evidence documents.

### Model Improvement Signals

Strong models should improve medical terminology bridging and evidence-set recall. Useful training signals include lay health queries paired with abstracts, hard negatives sharing disease or diet terms, biomedical synonym and mechanism mapping, and cluster-level positives for the same topic. Hybrid systems should preserve exact terms while dense representations expand toward scientific paraphrases and related mechanisms.

## Example Data

| Query | Positive Document |
|---|---|
| Batidos de chocolate saludables | Objetivo: Estudiar la relación entre el consumo de cerezas y el riesgo de ataques recurrentes de gota... |
| ética médica | ANTECEDENTES: Uno de los principales problemas en el control del colesterol sérico mediante intervención dietética parece ser la necesidad de mejorar... |
| habas | Durante los últimos 20 años, el creciente interés en la bioquímica, nutrición y farmacología de la L-arginina... |
| ¿Qué contienen los nuggets de pollo? | OBJETIVO: Determinar los componentes de las croquetas de pollo de 2 cadenas de comida nacionales... |
| grasa saturada | El interés por la posibilidad de que la ingesta materna de alimentos durante el embarazo pueda influir en el desarrollo de trastornos alérgicos... |

## Public Sources

- [NFCorpus paper](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| NFCorpus paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| NFCorpus project page | https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/ |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
