# MNanoBEIR / NanoBEIR-pt / NanoClimateFEVER

## Overview

Climate-FEVER is an evidence retrieval task for climate-related claims.
`NanoBEIR-pt__NanoClimateFEVER` uses Portuguese translated claims to retrieve
Portuguese translated evidence passages.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) extends fact-checking to
real-world climate claims and evidence documents. BEIR includes the task as
claim-evidence retrieval, while MMTEB gives the multilingual context for this
Portuguese version.

### Observed Data Profile

The sampled task has 50 queries, 3,408 documents, and 148 positive qrels. Most
queries have several positives: the average is 2.96 positives per query, with up
to 5. Queries are translated climate claims averaging 147.80 characters, and
documents average 1,680.20 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2631 and hit@10 = 0.6400. The median first-positive
rank is 4.0, so lexical matching often finds some evidence, but the low nDCG
shows that ranking all acceptable evidence remains difficult.

### Training Data That May Help

Helpful data includes non-overlapping climate claim verification, Portuguese
scientific and policy evidence retrieval, and multilingual fact-checking data.
Training should exclude CLIMATE-FEVER, BEIR, NanoBEIR, and translated records
that overlap this evaluation split.

### Synthetic Data Guidance

Generate Portuguese climate or environmental claims from non-evaluation source
passages. Include multiple evidence passages where appropriate, and use hard
negatives that share climate terminology but do not verify the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| De 1970 até 1998 houve um período de aquecimento que elevou as temperaturas em cerca de 0,39°C, o que contribuiu para o surgimento do movimento alarmista do aquecimento global. (176 chars) | O Paleoceno (pronunciado /paleoˈsɛnu/), ou Paleoceno, o "recentemente antigo", é uma época geológica que durou aproximadamente de 66 a 56 milhões de anos atrás. É a primeira época do Período Paleogeno na Era Cenozoica moderna ... [truncated 225 chars](1128 chars) |
| De fato, a tendência, embora não seja estatisticamente significativa, é de queda. (81 chars) | O ciclo solar, ou ciclo de atividade magnética solar, é a mudança quase periódica de 11 anos na atividade do Sol, que inclui variações nos níveis de radiação solar e na ejeção de material solar, bem como alterações na sua apa ... [truncated 225 chars](641 chars) |
| Os níveis do mar locais e regionais continuam a apresentar a variabilidade natural esperada, subindo em algumas regiões e descendo em outras. (141 chars) | O nível médio do mar (NMM) (abreviado simplesmente como nível do mar) é o nível médio da superfície de um ou mais dos oceanos da Terra, a partir do qual se podem medir alturas, como elevações. O NMM é um tipo de datum vertica ... [truncated 225 chars](1098 chars) |
| Cientistas climáticos dizem que elementos do furacão Harvey sugerem que o aquecimento global está agravando uma situação já difícil. (132 chars) | As mudanças climáticas são as alterações ambientais e sociais causadas (direta ou indiretamente) pelas emissões humanas de gases de efeito estufa. Há um consenso científico de que a mudança climática está ocorrendo e que as a ... [truncated 225 chars](1416 chars) |
| O experimento CLOUD do CERN testou apenas um terço de um dos quatro requisitos necessários para culpar o aquecimento global aos raios cósmicos, e dois dos outros requisitos já foram refutados. (192 chars) | A atribuição das mudanças climáticas recentes refere-se ao esforço científico para determinar os mecanismos responsáveis pelas mudanças climáticas observadas na Terra, comumente conhecidas como "aquecimento global". Esse esfo ... [truncated 225 chars](2238 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Positives per query avg | 2.96 |
| Positives per query min / median / max | 1 / 3.0 / 5 |
| Multi-positive queries | 44 (88.00%) |
| BM25 nDCG@10 | 0.2631 |
| BM25 hit@10 | 0.6400 |
| BM25 Recall@100 | 0.5676 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2508 |
| Dense hit@10 | 0.6000 |
| Dense Recall@100 | 0.5878 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2958 |
| Reranking hybrid hit@10 | 0.7200 |
| Reranking hybrid Recall@100 | 0.6622 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 147.80 |
| Document length avg chars | 1,680.20 |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
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
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoClimateFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3408
    positive_qrels: 148
  positives_per_query:
    average: 2.96
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 44
    multi_positive_query_percent: 88.0
  text_stats_chars:
    query_mean: 147.8
    document_mean: 1680.196303
  bm25:
    ndcg_at_10: 0.26309849966413895
    hit_at_10: 0.64
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2630984997
      hit_at_10: 0.64
      recall_at_100: 0.5675675676
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5675675676
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2508474129
      hit_at_10: 0.6
      recall_at_100: 0.5878378378
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5878378378
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2958216065
      hit_at_10: 0.72
      recall_at_100: 0.6621621622
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6621621622
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
