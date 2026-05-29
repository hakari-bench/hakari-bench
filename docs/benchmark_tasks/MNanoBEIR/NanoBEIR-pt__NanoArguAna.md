# MNanoBEIR / NanoBEIR-pt / NanoArguAna

## Overview

ArguAna is an argument-counterargument retrieval benchmark. `NanoBEIR-pt__NanoArguAna`
uses Portuguese translated argumentative passages as queries and retrieves
Portuguese translated counterarguments or closely paired arguments.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) is used in BEIR as an argument
retrieval task where relevance depends on argumentative relation, stance, and
response suitability rather than only topical similarity. MMTEB provides the
multilingual context for the Portuguese translation.

### Observed Data Profile

The sampled task has 50 queries, 3,635 documents, and 50 positive qrels. Every
query has exactly one positive. Queries are long translated argumentative
passages averaging 1,158.52 characters, while documents average 1,064.28
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4131 and hit@10 = 0.7000. Long text gives BM25 many
lexical anchors, but matching the correct counterargument still requires stance
and argument-structure understanding.

### Training Data That May Help

Useful data includes non-overlapping argument retrieval, debate counterargument
pairs, stance-aware retrieval, and Portuguese or multilingual argument mining
data. Training should exclude ArguAna, BEIR, NanoBEIR, and translated argument
records likely to overlap.

### Synthetic Data Guidance

Generate Portuguese claims and counterarguments from non-evaluation debate text.
Hard negatives should address the same topic while taking a different stance or
responding to a different premise.

## Example Data

| Query | Positive document |
| --- | --- |
| O público é indiferente às reformas. É discutível se a reforma da Câmara dos Lordes deve ser uma prioridade máxima no atual clima econômico, sem falar se um governo de coalizão conseguiria iniciar e implementar tais medidas. ... [truncated 225 chars](566 chars) | A campanha de voto alternativo não pode ser comparada a uma reforma do sistema político. Além disso, não se deve confundir um público mal informado devido à manipulação política com indiferença. Muitas vezes, os eleitores diz ... [truncated 225 chars](436 chars) |
| A expansão do Heathrow é vital para a economia. A expansão do Heathrow garantiria muitos empregos atuais e criaria novos. Atualmente, o Heathrow sustenta cerca de 250.000 empregos. Além disso, centenas de milhares de pessoas ... [truncated 225 chars](1228 chars) | A comunidade empresarial está longe de estar unida no suposto apoio a uma terceira pista. Pesquisas indicam que muitas empresas influentes, na verdade, não apoiam a expansão. Uma carta expressando preocupação foi assinada por ... [truncated 225 chars](1369 chars) |
| As pessoas têm muitas opções, o que as deixa menos felizes. A publicidade faz com que muitas pessoas se sintam sobrecarregadas pela necessidade constante de decidir entre várias demandas de atenção – isso é conhecido como a t ... [truncated 225 chars](975 chars) | As pessoas ficam infelizes porque não podem ter tudo, e não porque têm muitas opções e acham isso estressante. Na verdade, os anúncios desempenham um papel crucial ao garantir que o dinheiro que as pessoas têm seja gasto no p ... [truncated 225 chars](933 chars) |
| Ataques cibernéticos são frequentemente realizados por atores não estatais, como ciberterroristas ou hacktivistas (ativistas sociais que hackeiam), sem qualquer envolvimento do estado em questão. Por exemplo, em 2007, um gran ... [truncated 225 chars](1069 chars) | Em caso de ataque de atores não estatais, muitos praticantes do direito internacional concordam que o estado pode ainda retaliar em legítima defesa se outro estado é 'relutante ou incapaz de tomar medidas eficazes' para lidar ... [truncated 225 chars](565 chars) |
| Porque a religião promove a certeza de crença, o ódio inspirado por Deus é facilmente utilizado para justificar e promover ações violentas e práticas discriminatórias. A liberdade de expressão deve ser secundária quando há ri ... [truncated 225 chars](1347 chars) | Ninguém é obrigado a cometer atos de violência pelas palavras de outra pessoa; é uma escolha deles fazer isso. Da mesma forma, há muitas pessoas que podem ter opiniões que poderiam ser consideradas homofóbicas, mas ficariam h ... [truncated 225 chars](685 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.4131 |
| BM25 hit@10 | 0.7000 |
| BM25 Recall@100 | 0.8800 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4918 |
| Dense hit@10 | 0.8800 |
| Dense Recall@100 | 0.9600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4474 |
| Reranking hybrid hit@10 | 0.7800 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 1,158.52 |
| Document length avg chars | 1,064.28 |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
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
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoArguAna.md
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
    query_mean: 1158.52
    document_mean: 1064.275928
  bm25:
    ndcg_at_10: 0.41312404006862136
    hit_at_10: 0.7
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4131240401
      hit_at_10: 0.7
      recall_at_100: 0.88
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.88
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4918230114
      hit_at_10: 0.88
      recall_at_100: 0.96
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4473500883
      hit_at_10: 0.78
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
