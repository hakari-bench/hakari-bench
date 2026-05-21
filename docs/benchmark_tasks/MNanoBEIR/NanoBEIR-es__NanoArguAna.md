# MNanoBEIR / NanoBEIR-es / NanoArguAna

## Overview

ArguAna is an argument retrieval benchmark where the query is an argument and
the relevant document is a counterargument. `NanoBEIR-es__NanoArguAna` is the
Spanish MNanoBEIR version: long Spanish translated arguments must retrieve
Spanish translated counterarguments with an opposing stance. The task tests
argumentative fit and stance reversal.

## Details

### What the Original Data Measures

[Retrieval of the Best Counterargument without Prior Topic
Knowledge](https://aclanthology.org/P18-1023/) studies the task of finding the
best counterargument for a given argument. The paper argues that good
counterarguments often invoke the same aspects while taking the opposite stance,
and builds argument-counterargument pairs from debate portal data.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes ArguAna as an
argument retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 50 queries, 3,635 documents, and 50 positive
qrel rows. Every query has one positive counterargument. The average query
length is 1,219.96 characters, and the average document length is 1,110.85
characters.

The inspected examples cover gender roles in work, Democratic versus Republican
economic outcomes, reparations, intervention in Syria, and free higher
education. Both queries and positives are long Spanish translated arguments with
premises, conclusions, and cited evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4291 and hit@10 = 0.6800. BM25 ranks the positive first for 9 queries, and
the median first-positive rank is 4.

Lexical overlap is only partly useful because counterarguments discuss the same
topic while opposing the stance. A sparse model may retrieve same-topic support
instead of the actual rebuttal. Strong models should capture stance, premise
target, and argumentative opposition.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs,
stance-aware retrieval datasets, debate portal argument pairs, claim rebuttal
data, and Spanish or multilingual argument mining corpora.

Training should exclude ArguAna, BEIR, NanoBEIR, or translated debate records
likely to overlap with these evaluation arguments.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation counterarguments
and generate opposing arguments that share the same issue and aspect. Synthetic
queries should include enough premise detail to make stance matching necessary.

For joint generation, create paired pro and con arguments for controversial
topics, with explicit stance reversal and same-topic hard negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| El público es apático ante la reforma. Es discutible si la reforma de la Cámara de los Lores debería ser una prioridad en el actual clima económico, ya no digamos si un gobierno de coalición podría iniciar e implementar tales ... [truncated 225 chars](572 chars) | La campaña de voto alternativo no puede compararse con una reforma del sistema político. Además, no se debe confundir a un público mal informado debido a la manipulación política con apatía. A menudo, los votantes expresan qu ... [truncated 225 chars](462 chars) |
| La expansión de Heathrow es vital para la economía. La expansión de Heathrow garantizaría muchos de los empleos actuales y crearía nuevos. Actualmente, Heathrow sostiene aproximadamente 250,000 empleos. Además, cientos de mil ... [truncated 225 chars](1285 chars) | La comunidad empresarial está lejos de estar unida en su supuesto apoyo a una tercera pista. Las encuestas sugieren que muchos negocios influyentes, en realidad, no apoyan la expansión. Una carta expresando preocupación fue f ... [truncated 225 chars](1438 chars) |
| Las personas tienen demasiadas opciones, lo que las hace menos felices. La publicidad lleva a muchas personas a sentirse abrumadas por la necesidad interminable de decidir entre demandas competitivas de su atención – esto se ... [truncated 225 chars](989 chars) | Las personas están descontentas porque no pueden tenerlo todo, no porque se les ofrezca demasiadas opciones y eso les resulte estresante. De hecho, los anuncios juegan un papel crucial al asegurar que el dinero que las person ... [truncated 225 chars](983 chars) |
| Los ataques cibernéticos a menudo son perpetrados por actores no estatales, como ciberterroristas o hacktivistas (activistas sociales que hackean), sin ninguna implicación del estado real. Por ejemplo, en 2007, un ataque cibe ... [truncated 225 chars](1067 chars) | En caso de un ataque de actores no estatales, muchos expertos en derecho internacional coinciden en que el estado puede aún retaliar en defensa propia si otro estado es 'incapaz o no está dispuesto a tomar medidas efectivas' ... [truncated 225 chars](599 chars) |
| Porque la religión promueve la certeza de la creencia, el odio divino es fácil de utilizar para justificar y promover acciones violentas y prácticas discriminatorias. La libertad de expresión debe ceder cuando existe el poten ... [truncated 225 chars](1473 chars) | Nadie está siendo obligado a cometer actos de violencia por las palabras de otra persona; es su elección hacerlo. Igualmente, hay muchas personas que podrían tener opiniones que se considerarían homofóbicas, pero se horroriza ... [truncated 225 chars](680 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.4291 |
| BM25 hit@10 | 0.6800 |
| Query length avg chars | 1,219.96 |
| Document length avg chars | 1,110.85 |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/); 2018; Henning Wachsmuth, Shahbaz Syed, Benno Stein; DOI: `10.18653/v1/P18-1023`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | task paper | https://aclanthology.org/P18-1023/ |
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
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoArguAna.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3635
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1219.96
    document_mean: 1110.847318
  bm25:
    ndcg_at_10: 0.4290547157
    hit_at_10: 0.68
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding ArguAna, BEIR, or NanoBEIR records likely to overlap with these evaluation arguments
    useful_training_data:
      - non-overlapping argument-counterargument pairs
      - stance-aware retrieval datasets
      - debate portal argument pairs
      - Spanish or multilingual argument mining corpora
    synthetic_data:
      document_generation: Spanish counterarguments with explicit premises, conclusion, and controversial issue context
      question_generation: opposing Spanish arguments that share the same aspect while reversing stance
      answerability: positives should rebut the query argument, not simply discuss the same topic
    multi_positive_training: not_required_for_this_sample
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
      - label: ArguAna paper
        url: https://aclanthology.org/P18-1023/
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - Spanish task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: Retrieval of the Best Counterargument without Prior Topic Knowledge
      url: https://aclanthology.org/P18-1023/
      year: 2018
      doi: 10.18653/v1/P18-1023
      is_paper: true
      source_confidence: definitive_paper_link
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
