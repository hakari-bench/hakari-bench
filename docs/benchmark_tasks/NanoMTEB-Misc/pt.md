# NanoMTEB-Misc / pt

## Overview

`NanoMTEB-Misc / pt` is the Portuguese split of EuroPIRQ retrieval. Portuguese
synthetic questions retrieve Portuguese EU legal and administrative passages
derived from DGT-Acquis.

## Details

### What the Original Data Measures

The [EuroPIRQ dataset card](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval)
describes a dataset built from DGT-Acquis paragraph-level chunks in English,
Finnish, and Portuguese. The construction includes text cleaning, sentence
chunking, language detection, cross-lingual alignment checks, and synthetic
query generation.

[MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
gives the broader multilingual benchmark setting. No standalone task paper was
confirmed for EuroPIRQ; task interpretation is based on the public dataset card
and observed examples.

### Observed Data Profile

The split has 100 queries, 9,517 documents, and 100 positive qrel rows. Every
query has one positive. Queries average 149.75 characters and documents average
583.83 characters. The examples are Portuguese versions of EU committee,
competition, court, and governance passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.9189 and hit@10 = 0.9800. It ranks 86 positives at rank 1 and 98 in the top
10.

The task is lexically friendly because synthetic questions reuse names,
institutions, and legal terms from the relevant passage. Errors mostly arise
when multiple passages share legal boilerplate or a very similar institutional
frame.

### Training Data That May Help

Portuguese legal retrieval, EU-domain passage retrieval, multilingual
DGT-Acquis parallel corpora, and synthetic question-passage pairs are useful.
Hard negatives should be passages with the same legal basis, institution, or
administrative domain.

### Synthetic Data Guidance

Generate Portuguese questions from non-evaluation EU passages. Keep a mix of
entity-heavy questions and paraphrased questions. For hard negatives, sample
nearby legal passages with similar directives, committee language, and court
formulas.

## Example Data

| Query | Positive document |
| --- | --- |
| Por que a Comissão acredita que o insucesso empresarial deve ser visto como uma oportunidade para um novo arranque? (115 chars) | O CESE subscreve a importância atribuída pela Comissão à necessidade de superar o estigma do insucesso empresarial. A Comissão está certa em afirmar que a criação de empresas e o êxito e o insucesso empresariais são inerentes ... [truncated 225 chars](562 chars) |
| Como o Conselho propõe aliviar a sobrecarga das PME em relação ao regulamento REACH? (84 chars) | Nesta base, a posição comum não integra algumas das alterações adoptadas pelo Parlamento Europeu em primeira leitura (alterações 169 e 726). No que se refere à alteração 169, que introduziria um procedimento menos pesado para ... [truncated 225 chars](554 chars) |
| O que é necessário para o processo contínuo de construção e operação de um mercado integrado? (93 chars) | Finalmente, a construção de um mercado totalmente integrado não é uma tarefa definida e com um fim finito, mas antes um processo permanente que requer um esforço, vigilância e actualização constantes. Há sempre novos desafios ... [truncated 225 chars](561 chars) |
| Quais medidas as autoridades gregas não implementaram para proteger o sítio e evitar a deterioração dos habitats e as perturbações das espécies? (144 chars) | Em contrapartida, verifica-se que as autoridades gregas não tomaram as medidas necessárias para estabelecer um regime de protecção adequada do sítio e evitar a deterioração dos habitats e as perturbações significativas das es ... [truncated 225 chars](552 chars) |
| Que tipo de produtos a Comissão está considerando promover através de um instrumento comunitário, e por que esses produtos são considerados valiosos? (149 chars) | A Comissão prossegue as suas reflexões sobre esta matéria e tenciona realizar trabalhos preparatórios para avaliar a viabilidade de um instrumento comunitário de valorização e promoção dos produtos típicos — não agrícolas — d ... [truncated 225 chars](545 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Task / split | pt |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Source dataset | [eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval) |
| Language | pt |
| Category | natural_language |
| Queries | 100 |
| Documents | 9,517 |
| Positive qrels | 100 |
| BM25 nDCG@10 | 0.9186 |
| BM25 hit@10 | 0.9800 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8623 |
| Dense hit@10 | 0.9300 |
| Dense Recall@100 | 0.9600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8901 |
| Reranking hybrid hit@10 | 0.9400 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 149.75 |
| Document length avg chars | 583.83 |

### Public Sources

- [EuroPIRQ-retrieval dataset card](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval), construction and data-field description.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), benchmark context.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), original benchmark framework.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)
- Source task dataset: [eherra/EuroPIRQ-retrieval](https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| EuroPIRQ-retrieval | 2025 | dataset card | https://huggingface.co/datasets/eherra/EuroPIRQ-retrieval |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Misc
  backing_dataset: NanoMTEB-Misc
  dataset_id: hakari-bench/NanoMTEB-Misc
  task_name: pt
  split_name: pt
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/pt.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone EuroPIRQ task paper was confirmed; dataset card and
      MMTEB/MTEB sources were checked.
  counts:
    queries: 100
    documents: 9517
    positive_qrels: 100
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 149.75
    document_mean: 583.83
  bm25:
    ndcg_at_10: 0.9186487477261229
    hit_at_10: 0.98
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9186487477
      hit_at_10: 0.98
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8622553921
      hit_at_10: 0.93
      recall_at_100: 0.96
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8900774325
      hit_at_10: 0.94
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
