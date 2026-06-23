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

| Query | Positive document |
| --- | --- |
| Batidos de chocolate saludables [31 chars] | Objetivo: Estudiar la relación entre el consumo de cerezas y el riesgo de ataques recurrentes de gota en individuos con gota. Métodos: Realizamos un estudio de caso-cruce para examinar las asociaciones de un conjunto de factores de riesgo putativos con ataques recurrentes de gota. Se reclutaron prospectivamente individuos con gota y se les siguió en línea durante un año. A los participantes se les preguntó la siguiente información al experimentar un ataque de gota: la fecha de inicio del ataque, síntomas y signos, medicamentos (incluyendo medicamentos anti-gota) y factores de riesgo potenciales (incluyendo el consumo diario de cerezas y extracto de cereza) durante el período de 2 días previo al ataque de gota. Evaluamos la misma información de exposición durante períodos de control de 2 días. Estimamos el riesgo de ataques recurrentes de gota relacionados con el consumo de cerezas utilizando regresión logística condicional. Resultados: Nuestro estudio incluyó a 633 individuos con gota.... [1,000 / 1,865 chars] |
| ética médica [12 chars] | ANTECEDENTES: Uno de los principales problemas en el control del colesterol sérico mediante intervención dietética parece ser la necesidad de mejorar la adherencia del paciente. OBJETIVOS: Explorar las diversas preguntas sobre las barreras y los motivadores para la adherencia a una dieta que reduzca el colesterol. MÉTODOS: Encuestamos las prácticas dietéticas de médicos generales franceses para pacientes con hipercolesterolemia y examinamos las actitudes de sus pacientes hacia este enfoque. RESULTADOS: Analizamos 234 cuestionarios personales de médicos y 356 cuestionarios de autoevaluación de pacientes. Las razones de los pacientes para no cumplir con la dieta prescrita incluyeron: 'ya tener hábitos alimenticios satisfactorios' (34.7%), 'rechazo a sufrir privación nutricional' (33.3%), 'dificultades para conciliar la dieta con la vida familiar' (27.8%) y 'tomar medicamentos para reducir el colesterol' (22.2%). A pesar de una comprensión generalmente buena por parte de los pacientes de... [1,000 / 2,091 chars] |
| habas [5 chars] | Durante los últimos 20 años, el creciente interés en la bioquímica, nutrición y farmacología de la L-arginina ha llevado a extensos estudios para explorar sus roles nutricionales y terapéuticos en el tratamiento y prevención de trastornos metabólicos humanos. Evidencias emergentes muestran que la suplementación dietética con L-arginina reduce la adiposidad en ratas genéticamente obesas, ratas obesas inducidas por dieta, cerdos de engorde y sujetos humanos obesos con diabetes tipo 2. Los mecanismos responsables de los efectos beneficiosos de la L-arginina son probablemente complejos, pero finalmente implican alterar el equilibrio entre la ingesta y el gasto energético a favor de la pérdida de grasa o la reducción del crecimiento del tejido adiposo blanco. Estudios recientes indican que la suplementación con L-arginina estimula la biogénesis mitocondrial y el desarrollo del tejido adiposo marrón, posiblemente a través de la síntesis mejorada de moléculas de señalización celular (por ejem... [1,000 / 1,398 chars] |

## Public Sources

- [NFCorpus paper](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| NFCorpus paper (https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| NFCorpus project page (https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
