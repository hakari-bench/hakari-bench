# MNanoBEIR / NanoBEIR-pt / NanoNFCorpus

## Overview

NFCorpus is a biomedical and nutrition information retrieval task.
`NanoBEIR-pt__NanoNFCorpus` uses Portuguese translated health queries to retrieve
Portuguese translated scientific or medical passages.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built from nutrition and health information needs with expert relevance
judgments. BEIR includes it as a domain-specific retrieval task, and MMTEB gives
the multilingual context for this Portuguese version.

### Observed Data Profile

The sampled task has 50 queries, 2,953 documents, and 1,651 positive qrels.
Nearly all queries are multi-positive, with an average of 33.02 positives and a
maximum of 100. Queries are very short, averaging 26.92 characters; documents
average 1,650.10 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3670 and hit@10 = 0.7000. Biomedical terms help lexical
retrieval, but the many positives and long scientific passages require ranking
beyond exact term overlap.

### Training Data That May Help

Useful data includes non-overlapping biomedical retrieval, Portuguese medical
question answering, scientific abstract retrieval, and multi-positive relevance
training. Exclude NFCorpus, BEIR, NanoBEIR, and overlapping translated abstracts.

### Synthetic Data Guidance

Generate Portuguese consumer-health or biomedical keyword queries from
scientific passages. Use multiple positives per query when the same condition,
intervention, or outcome is discussed by several documents.

## Example Data

| Query | Positive document |
| --- | --- |
| Batidas de chocolate saudáveis (30 chars) | Objetivo: Estudar a relação entre o consumo de cerejas e o risco de ataques recorrentes de gota em indivíduos com gota. Métodos: Realizamos um estudo caso-cruzado para examinar as associações de um conjunto de fatores de risc ... [truncated 225 chars](1752 chars) |
| ética médica (12 chars) | FUNDAMENTAÇÃO: Um dos principais problemas no controle do colesterol sérico através de intervenção dietética parece ser a necessidade de melhorar a adesão do paciente. OBJETIVOS: Explorar as diversas questões relacionadas às ... [truncated 225 chars](1978 chars) |
| favas (5 chars) | Nos últimos 20 anos, o crescente interesse pela bioquímica, nutrição e farmacologia da L-arginina levou a estudos extensivos para explorar seus papéis nutricionais e terapêuticos no tratamento e prevenção de distúrbios metabó ... [truncated 225 chars](1347 chars) |
| Do que são feitos os nuggets de frango? (39 chars) | OBJETIVO: Determinar os componentes dos nuggets de frango de 2 redes de fast food nacionais. CONTEXTO: Os nuggets de frango tornaram-se um componente importante da dieta americana. Buscamos determinar a composição atual desse ... [truncated 225 chars](790 chars) |
| gordura saturada (16 chars) | O interesse pelo possível impacto da ingestão alimentar materna durante a gravidez no desenvolvimento de doenças alérgicas em crianças tem aumentado. O presente estudo prospectivo examinou a associação entre a ingestão matern ... [truncated 225 chars](2146 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Positives per query avg | 33.02 |
| Positives per query min / median / max | 1 / 23.5 / 100 |
| Multi-positive queries | 47 (94.00%) |
| BM25 nDCG@10 | 0.2982 |
| BM25 hit@10 | 0.6600 |
| BM25 Recall@100 | 0.1581 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2966 |
| Dense hit@10 | 0.6600 |
| Dense Recall@100 | 0.1908 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3146 |
| Reranking hybrid hit@10 | 0.6200 |
| Reranking hybrid Recall@100 | 0.1987 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 5 |
| Query length avg chars | 26.92 |
| Document length avg chars | 1,650.10 |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
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
  backing_dataset: NanoBEIR-pt
  dataset_id: hakari-bench/NanoBEIR-pt
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoNFCorpus.md
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
    query_mean: 26.92
    document_mean: 1650.103962
  bm25:
    ndcg_at_10: 0.29815458115251836
    hit_at_10: 0.66
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2981545812
      hit_at_10: 0.66
      recall_at_100: 0.1580860085
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1580860085
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2966064911
      hit_at_10: 0.66
      recall_at_100: 0.1907934585
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1907934585
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3146072806
      hit_at_10: 0.62
      recall_at_100: 0.1986674743
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.1
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1986674743
      safeguard_positive_rows: 5
      rows_with_101_candidates: 5
```
