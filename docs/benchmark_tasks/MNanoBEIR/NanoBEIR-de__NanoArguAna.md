# MNanoBEIR / NanoBEIR-de / NanoArguAna

## Overview

ArguAna is an argument retrieval benchmark where the query is an argument and
the relevant document is a counterargument. `NanoBEIR-de__NanoArguAna` is the
German MNanoBEIR version: long German translated arguments must retrieve German
translated counterarguments with an opposing stance. The task tests semantic
opposition and argumentative fit, not simple topical similarity.

## Details

### What the Original Data Measures

[Retrieval of the Best Counterargument without Prior Topic
Knowledge](https://aclanthology.org/P18-1023/) studies the task of finding the
best counterargument for any given argument. The paper hypothesizes that a good
counterargument invokes the same aspects as the original argument while taking
the opposite stance, and builds argument-counterargument pairs from debate
portal data.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes ArguAna as an
argument retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context for this German Nano split.

### Observed Data Profile

The sampled German Nano task has 50 queries, 3,635 documents, and 50 positive
qrel rows. Every query has one positive counterargument. The average query
length is 1,243.08 characters, and the average document length is 1,142.27
characters.

The inspected examples cover social, economic, international, and education
debates: gender roles in work, Democratic versus Republican economic outcomes,
reparations, intervention in Syria, and tuition-free higher education.
Queries and positives are long argumentative passages, often with citations or
numbered evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3079 and hit@10 = 0.5200. BM25 ranks the positive first for 6 of 50 queries,
and the median first-positive rank is 9.

Lexical overlap can be high because a counterargument discusses the same topic,
but the important relation is opposition. A sparse model may retrieve an
argument that shares entities and issue terms but supports the same side.
Strong retrieval must capture stance reversal, rebuttal structure, and the
specific aspect being contested.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs,
stance-aware retrieval datasets, debate portal argument pairs, claim rebuttal
data, and German or multilingual argument mining corpora. Hard negatives should
include same-topic arguments with the wrong stance.

Training should exclude ArguAna, BEIR, NanoBEIR, or translated debate records
likely to overlap with these evaluation arguments.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation counterarguments and
generate opposing arguments that share the same issue and aspect. Synthetic
queries should be long enough to include premises and conclusion.

For joint generation, create paired pro and con arguments for controversial
topics, with explicit stance reversal and enough shared detail to avoid trivial
topic-only retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| Die Öffentlichkeit zeigt sich reformunwillig. Ob die Reform des Oberhauses in der aktuellen wirtschaftlichen Lage Priorität haben sollte, ist umstritten, ganz zu schweigen davon, ob eine Koalitionsregierung solche Maßnahmen ü ... [truncated 225 chars](666 chars) | Die Wahlreform lässt sich nicht mit Reformen im House of Lords vergleichen. Zudem sollte man eine durch politische Rhetorik irreführte Öffentlichkeit nicht mit Gleichgültigkeit verwechseln. Oft geben Wähler an, gleichgültig z ... [truncated 225 chars](461 chars) |
| Der Ausbau von Heathrow ist für die Wirtschaft von entscheidender Bedeutung. Der Ausbau von Heathrow würde viele bestehende Arbeitsplätze sichern und gleichzeitig neue schaffen. Derzeit sichert Heathrow etwa 250.000 Arbeitspl ... [truncated 225 chars](1355 chars) | Die Geschäftswelt ist keineswegs einig in ihrer angeblichen Unterstützung für eine dritte Start- und Landebahn. Umfragen deuten darauf hin, dass viele einflussreiche Unternehmen die Erweiterung in Wirklichkeit nicht unterstüt ... [truncated 225 chars](1548 chars) |
| Menschen werden mit zu vielen Wahlmöglichkeiten konfrontiert, was sie unglücklicher macht. Werbung überfordert viele Menschen durch das endlose Bedürfnis, zwischen konkurrierenden Anforderungen an ihre Aufmerksamkeit zu entsc ... [truncated 225 chars](1218 chars) | Menschen sind unzufrieden, weil sie nicht alles haben können, nicht weil sie zu viele Wahlmöglichkeiten haben und sich dadurch gestresst fühlen. Tatsächlich spielen Werbeanzeigen eine entscheidende Rolle dabei, dass Menschen ... [truncated 225 chars](1040 chars) |
| Cyberangriffe werden häufig von nicht-staatlichen Akteuren durchgeführt, wie Cyberterroristen oder Hacktivisten (soziale Aktivisten, die hacken), ohne jede Beteiligung des tatsächlichen Staates. Zum Beispiel wurde 2007 ein ma ... [truncated 225 chars](1157 chars) | Im Falle eines Angriffs durch nicht-staatliche Akteure sind sich viele Praktiker des Völkerrechts einig, dass der Staat sich weiterhin in Selbstverteidigung wehren kann, wenn ein anderer Staat 'unwillig oder unfähig ist, effe ... [truncated 225 chars](641 chars) |
| Weil Religion die Gewissheit des Glaubens fördert, lässt sich göttlich inspirierter Hass leicht nutzen, um gewaltsame Handlungen und diskriminierende Praktiken zu rechtfertigen und zu fördern. Die Meinungsfreiheit muss zurück ... [truncated 225 chars](1247 chars) | Niemand wird durch die Worte eines anderen gezwungen, Gewaltakte zu begehen; es ist ihre eigene Entscheidung, dies zu tun. Ebenso gibt es viele Menschen, die Ansichten vertreten könnten, die als homophob betrachtet werden, ab ... [truncated 225 chars](709 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3453 |
| BM25 hit@10 | 0.5600 |
| BM25 Recall@100 | 0.9200 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4738 |
| Dense hit@10 | 0.8200 |
| Dense Recall@100 | 0.9600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4422 |
| Reranking hybrid hit@10 | 0.7400 |
| Reranking hybrid Recall@100 | 0.9800 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 1,243.08 |
| Document length avg chars | 1,142.27 |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/); 2018; Henning Wachsmuth, Shahbaz Syed, Benno Stein; DOI: `10.18653/v1/P18-1023`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
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
  backing_dataset: NanoBEIR-de
  dataset_id: hakari-bench/NanoBEIR-de
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoArguAna.md
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
    query_mean: 1243.08
    document_mean: 1142.266575
  bm25:
    ndcg_at_10: 0.3452712112570587
    hit_at_10: 0.56
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding ArguAna, BEIR, or NanoBEIR records likely to overlap
      with these evaluation arguments
    useful_training_data:
    - non-overlapping argument-counterargument pairs
    - stance-aware retrieval datasets
    - debate portal argument pairs
    - German or multilingual argument mining corpora
    synthetic_data:
      document_generation: German counterarguments with explicit premises, conclusion,
        and controversial issue context
      question_generation: opposing German arguments that share the same aspect while
        reversing stance
      answerability: positives should rebut the query argument, not simply discuss
        the same topic
    multi_positive_training: not_required_for_this_sample
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
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
    - German task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
  references:
  - title: Retrieval of the Best Counterargument without Prior Topic Knowledge
    url: https://aclanthology.org/P18-1023/
    year: 2018
    doi: 10.18653/v1/P18-1023
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    doi: 10.48550/arXiv.2502.13595
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'NanoBEIR: Smaller BEIR dataset subsets'
    url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    year: 2024
    doi: null
    is_paper: false
    source_confidence: dataset_collection
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3452712113
      hit_at_10: 0.56
      recall_at_100: 0.92
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.92
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4737603029
      hit_at_10: 0.82
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
      ndcg_at_10: 0.4422416263
      hit_at_10: 0.74
      recall_at_100: 0.98
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
