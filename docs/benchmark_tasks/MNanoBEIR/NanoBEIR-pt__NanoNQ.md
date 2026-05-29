# MNanoBEIR / NanoBEIR-pt / NanoNQ

## Overview

Natural Questions is an answer-oriented Wikipedia retrieval benchmark.
`NanoBEIR-pt__NanoNQ` uses Portuguese translated Google-style questions to
retrieve Portuguese translated answer passages.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced naturally
occurring search questions paired with Wikipedia evidence. BEIR evaluates the
retrieval step, and MMTEB supplies the multilingual framing for the Portuguese
translation.

### Observed Data Profile

The sampled task has 50 queries, 5,035 documents, and 57 positive qrels. Most
queries have one positive, with a small two-positive tail. Queries average 51.58
characters, and documents average 549.83 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3645 and hit@10 = 0.6000. The median first-positive
rank is 6.5, so lexical overlap is useful but not enough for many Portuguese
natural questions.

### Training Data That May Help

Helpful data includes non-overlapping open-domain QA retrieval, Portuguese
Wikipedia passage search, and multilingual query-passage pairs. Exclude Natural
Questions, BEIR, NanoBEIR, and translated evaluation examples.

### Synthetic Data Guidance

Generate Portuguese natural questions from encyclopedia passages. The positive
document should contain the answer span or answer-bearing context; hard
negatives should share entities without answering the question.

## Example Data

| Query | Positive document |
| --- | --- |
| Onde vai ser realizado o Final Four este ano? (45 chars) | O Torneio de Basquetebol Masculino da Divisão I da NCAA de 2018 foi um torneio de eliminação simples com 68 equipes para determinar o campeão nacional de basquetebol universitário da NCAA para a temporada 2017-18. A 80ª ediçã ... [truncated 225 chars](355 chars) |
| O "O Estranho Mundo de Jack" é um filme original da Disney? (59 chars) | O Pesadelo Antes do Natal surgiu de um poema escrito por Tim Burton em 1982, enquanto ele trabalhava como animador na Walt Disney Feature Animation. Com o sucesso de Vincent no mesmo ano, os Estúdios Walt Disney começaram a c ... [truncated 225 chars](668 chars) |
| Por que existe o Anjo do Norte? (31 chars) | De acordo com Gormley, o significado de um anjo era tríplice: primeiro, para significar que, sob o local de sua construção, mineiros de carvão trabalharam por dois séculos; segundo, para compreender a transição de uma era ind ... [truncated 225 chars](351 chars) |
| Onde foi originalmente mencionado o Compromisso dos Três Quintos na Constituição? (81 chars) | O Compromisso dos Três Quintos está no Artigo 1, Seção 2, Cláusula 3 da Constituição dos Estados Unidos, que diz: (113 chars) |
| Quem canta "Someone's Watching Me" com Michael Jackson? (55 chars) | "Somebody's Watching Me" é uma música do cantor americano Rockwell de seu álbum de estreia Somebody's Watching Me (1984). Foi lançada como o primeiro single e single principal do álbum em 14 de janeiro de 1984, pela Motown. C ... [truncated 225 chars](362 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Positives per query avg | 1.14 |
| Positives per query min / median / max | 1 / 1.0 / 2 |
| Multi-positive queries | 7 (14.00%) |
| BM25 nDCG@10 | 0.3645 |
| BM25 hit@10 | 0.6000 |
| BM25 Recall@100 | 0.8070 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5103 |
| Dense hit@10 | 0.6600 |
| Dense Recall@100 | 0.8421 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4522 |
| Reranking hybrid hit@10 | 0.6600 |
| Reranking hybrid Recall@100 | 0.8772 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 5 |
| Query length avg chars | 51.58 |
| Document length avg chars | 549.83 |

### Public Sources

- [Natural Questions: a Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: a Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
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
  task_name: NanoNQ
  split_name: NanoNQ
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoNQ.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5035
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 7
    multi_positive_query_percent: 14.0
  text_stats_chars:
    query_mean: 51.58
    document_mean: 549.828401
  bm25:
    ndcg_at_10: 0.36454612694411226
    hit_at_10: 0.6
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3645461269
      hit_at_10: 0.6
      recall_at_100: 0.8070175439
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8070175439
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5102629612
      hit_at_10: 0.66
      recall_at_100: 0.8421052632
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8421052632
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4522082362
      hit_at_10: 0.66
      recall_at_100: 0.8771929825
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.1
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8771929825
      safeguard_positive_rows: 5
      rows_with_101_candidates: 5
```
