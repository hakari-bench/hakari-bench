# MNanoBEIR / NanoBEIR-es / NanoNFCorpus

## Overview

NFCorpus is a medical information retrieval dataset built around health and
nutrition information needs linked to research articles. `NanoBEIR-es__NanoNFCorpus`
is the Spanish MNanoBEIR version: short Spanish translated health queries must
retrieve Spanish translated medical or biomedical documents. The task stresses
domain vocabulary, lay-to-technical matching, and many relevant documents per
query.

## Details

### What the Original Data Measures

[A Full-Text Learning to Rank Dataset for Medical Information
Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
describes NFCorpus as a medical learning-to-rank dataset whose queries come
from NutritionFacts.org health topics and whose relevance links connect those
queries to PubMed and medical articles at multiple relevance levels. The paper
emphasizes the lexical gap between lay health language and medical literature.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes NFCorpus as a
bio-medical retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 50 queries, 2,953 documents, and 1,651
positive qrel rows. Queries average 33.02 positives, with 47 of 50 queries
having multiple positives. The average query length is 27.10 characters, and
the average document length is 1,732.44 characters.

The inspected queries include chicken nuggets, meat purge and cola, Atkins
diet, adenovirus 36, and probiotics for common cold prevention. Documents are
long Spanish translated biomedical abstracts or scientific summaries.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3492 and hit@10 = 0.6400. BM25 ranks a positive first for 23 queries, and
the median first-positive rank is 2.

BM25 often finds at least one related document, but the large number of
positives makes ranking quality important. The task rewards models that bridge
short lay Spanish queries to biomedical mechanisms, interventions, outcomes,
and study terminology.

### Training Data That May Help

Useful training data includes non-overlapping biomedical IR datasets,
consumer-health question to biomedical abstract pairs, PubMed relevance ranking
data, and Spanish or multilingual medical retrieval supervision.

Training should exclude NFCorpus, BEIR, NanoBEIR, or translated NutritionFacts
records likely to overlap with these evaluation queries or linked articles.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation biomedical abstracts
and generate short Spanish lay questions or topic labels. Include diseases,
diets, supplements, mechanisms, and prevention questions.

For joint generation, create clusters of related biomedical passages so that
multi-positive training teaches retrieval of several valid evidence documents
for the same health topic.

## Example Data

| Query | Positive document |
| --- | --- |
| Batidos de chocolate saludables (31 chars) | Objetivo: Estudiar la relación entre el consumo de cerezas y el riesgo de ataques recurrentes de gota en individuos con gota. Métodos: Realizamos un estudio de caso-cruce para examinar las asociaciones de un conjunto de facto ... [truncated 225 chars](1865 chars) |
| ética médica (12 chars) | ANTECEDENTES: Uno de los principales problemas en el control del colesterol sérico mediante intervención dietética parece ser la necesidad de mejorar la adherencia del paciente. OBJETIVOS: Explorar las diversas preguntas sobr ... [truncated 225 chars](2091 chars) |
| habas (5 chars) | Durante los últimos 20 años, el creciente interés en la bioquímica, nutrición y farmacología de la L-arginina ha llevado a extensos estudios para explorar sus roles nutricionales y terapéuticos en el tratamiento y prevención ... [truncated 225 chars](1398 chars) |
| ¿Qué contienen los nuggets de pollo? (36 chars) | OBJETIVO: Determinar los componentes de las croquetas de pollo de 2 cadenas de comida nacionales. ANTECEDENTES: Las croquetas de pollo se han convertido en un componente importante de la dieta estadounidense. Buscamos determi ... [truncated 225 chars](852 chars) |
| grasa saturada (14 chars) | El interés por la posibilidad de que la ingesta materna de alimentos durante el embarazo pueda influir en el desarrollo de trastornos alérgicos en los niños ha aumentado. El presente estudio prospectivo examinó la asociación ... [truncated 225 chars](2263 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Avg positives / query | 33.02 |
| Positives per query (min / median / max) | 1 / 23.50 / 100 |
| Queries with multiple positives | 47 (94.0%) |
| BM25 nDCG@10 | 0.3492 |
| BM25 hit@10 | 0.6400 |
| Query length avg chars | 27.10 |
| Document length avg chars | 1,732.44 |

### Public Sources

- [A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf); 2016; Vera Boteva, Demian Gholipour Ghalandari, Artem Sokolov, Stefan Riezler; DOI: `10.1007/978-3-319-30671-1_58`.
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| NFCorpus project page |  | project page | https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-es
  dataset_id: hakari-bench/NanoBEIR-es
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoNFCorpus.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2953
    positive_qrels: 1651
  positives_per_query:
    average: 33.02
    min: 1
    median: 23.5
    max: 100
    multi_positive_queries: 47
    multi_positive_query_percent: 94.0
  text_stats_chars:
    query_mean: 27.1
    document_mean: 1732.442939
  bm25:
    ndcg_at_10: 0.3492041046
    hit_at_10: 0.64
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding NFCorpus, BEIR, or NanoBEIR records likely to overlap with these evaluation queries or linked medical documents
    useful_training_data:
      - non-overlapping biomedical information retrieval datasets
      - consumer-health question to biomedical abstract pairs
      - PubMed relevance ranking data
      - Spanish or multilingual medical retrieval supervision
    synthetic_data:
      document_generation: Spanish biomedical abstracts and health article summaries outside the evaluation set
      question_generation: short Spanish lay health questions and topic labels that bridge to biomedical terminology
      answerability: positives should be medically relevant evidence documents, not only documents sharing a disease or diet keyword
    multi_positive_training: recommended
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
      - label: NFCorpus paper
        url: https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
      - label: NFCorpus project page
        url: https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - Spanish task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: A Full-Text Learning to Rank Dataset for Medical Information Retrieval
      url: https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf
      year: 2016
      doi: 10.1007/978-3-319-30671-1_58
      is_paper: true
      source_confidence: definitive_paper_link
    - title: NFCorpus project page
      url: https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_project_page
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      doi: null
      is_paper: false
      source_confidence: dataset_collection
```
