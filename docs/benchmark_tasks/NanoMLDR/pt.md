# NanoMLDR / pt

## Overview

`pt` is the Portuguese split of NanoMLDR. It evaluates retrieval of long
Portuguese articles for paragraph-grounded Portuguese questions.

## Details

### What the Original Data Measures

[M3-Embedding](https://arxiv.org/abs/2402.03216) evaluates MLDR as a
multilingual long-document retrieval benchmark. The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR)
lists Portuguese as Wikipedia-sourced and describes generated questions paired
with full long articles.

### Observed Data Profile

The Nano split has 141 queries, 3,028 documents, and 141 positive qrels. Each
query has one positive. Queries average 110.99 characters and documents average
14,744.68 characters. The examples cover municipalities, amphibians, U.S. state
economics, Windows Vista, and John Adams.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.9210 and hit@10 = 0.9716, the strongest observed NanoMLDR BM25 result in this
batch. The generated questions usually preserve very distinctive terms from the
target Portuguese article.

### Training Data That May Help

Useful training data includes Portuguese Wikipedia retrieval, Portuguese
long-document QA, multilingual MLDR training data, and hard negatives from
related articles with overlapping names, dates, or institutions.

### Synthetic Data Guidance

Synthetic data should generate Portuguese paragraph-grounded questions from
long articles. Hard negatives should be long Portuguese articles in the same
topic area but lacking the relevant paragraph.

## Example Data

| Query | Positive document |
| --- | --- |
| Qual é a relação entre as fórmulas formula_99, formula_94 e formula_47 para resolver a equação mencionada? (106 chars) | Cinemática A cinemática (do grego "κινημα", movimento) é o ramo da física que se ocupa da descrição dos movimentos de pontos, corpos ou sistemas de corpos (grupos de objetos), sem se preocupar com a análise de suas causas. Co ... [truncated 225 chars](31375 chars) |
| Quais foram as ocasiões em que Haydn, Mozart e Beethoven redescobriram a forma fugal e a utilizaram frequentemente em suas obras durante a era Clássica? (152 chars) | Fuga Fuga em música, é um estilo de composição contrapontista, polifônica e imitativa, de um tema principal, com sua origem na música barroca. Na composição musical o tema é repetido por outras vozes que entram sucessivamente ... [truncated 225 chars](30207 chars) |
| O que é necessário para obter o ajuste de luminosidade em um tubo de raios catódicos (CRT)? (91 chars) | Osciloscópio O osciloscópio é um instrumento de medida de sinais elétricos/eletrônicos que apresenta gráficos a duas dimensões de um ou mais sinais elétricos (de acordo com a quantidade de canais de entrada). O eixo vertical ... [truncated 225 chars](26731 chars) |
| Qual é a importância da PR-16 para o município de Curiúva e como ela contribui para a conexão com outras cidades dos estados do Paraná e São Paulo? (147 chars) | Curiúva Curiúva é um município brasileiro localizado no interior do estado do Paraná. Pertence à Região Geográfica Intermediária de Ponta Grossa e à Imediata de Telêmaco Borba e localiza-se a noroeste da capital do estado, di ... [truncated 225 chars](26810 chars) |
| Qual foi o impacto da disponibilidade de jogos falsificados a preços mais acessíveis na popularidade do console Saturn no Brasil? (129 chars) | Sega Saturn O Sega Saturn é um console de jogos eletrônicos de quinta geração, lançado pela empresa Sega em 22 de Novembro de 1994 no Japão, 11 de Maio de 1995 na América do Norte, 30 de agosto de 1995 no Brasil e 8 de Julho ... [truncated 225 chars](32800 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | pt |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | pt |
| Category | natural_language |
| Queries | 141 |
| Documents | 3028 |
| Positive qrels | 141 |
| BM25 nDCG@10 | 0.9210 |
| BM25 hit@10 | 0.9716 |
| Query length avg chars | 110.99 |
| Document length avg chars | 14744.68 |

### Public Sources

- [M3-Embedding](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
- [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR)
- Source dataset: [Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMLDR
  backing_dataset: NanoMLDR
  dataset_id: hakari-bench/NanoMLDR
  task_name: pt
  split_name: pt
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/pt.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 141
    documents: 3028
    positive_qrels: 141
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 110.99290780141844
    document_mean: 14744.681307793924
  bm25:
    ndcg_at_10: 0.9210128865930197
    hit_at_10: 0.9716312056737588
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR Portuguese split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR pt queries, qrels, and positive documents
    useful_training_data:
      - Portuguese long-document QA retrieval pairs
      - Portuguese Wikipedia article retrieval
      - multilingual MLDR training data outside this Nano split
      - same-entity Portuguese hard negatives
    synthetic_data:
      document_generation: long Portuguese encyclopedic articles
      question_generation: paragraph-grounded Portuguese questions
      answerability: positives should be full articles containing the answer-bearing paragraph
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
      - label: M3-Embedding arXiv
        url: https://arxiv.org/abs/2402.03216
      - label: Shitao/MLDR
        url: https://huggingface.co/datasets/Shitao/MLDR
    source_notes: []
  references:
    - title: "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
      url: https://arxiv.org/abs/2402.03216
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
```
