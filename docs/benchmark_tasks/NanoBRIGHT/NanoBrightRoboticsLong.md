# NanoBRIGHT / NanoBrightRoboticsLong

## Overview

`NanoBrightRoboticsLong` is the long-document version of the Robotics
StackExchange BRIGHT task. Queries are long ROS or robotics troubleshooting
posts, and relevant documents are full cited pages such as GitHub issues,
documentation pages, or message definitions.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) reports that long-context variants
retrieve from unsplit web pages, making the retrieval pool smaller but the
documents much longer. For Robotics, this tests whether a model can identify
the right full documentation or issue page for a specific ROS2, Gazebo,
controller, or interface problem.

### Observed Data Profile

The split has 101 queries, 505 documents, and 106 positive qrels. Queries
average 2179.45 characters. Documents average 35,895.20 characters and include
long GitHub pages, ROS interface pages, source files, and project
documentation. Only 5 queries have multiple positives; most have one relevant
full document.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2193 and hit@10 = 0.3465. It ranks 10 queries with a positive first, and the
median best positive rank is 60. Full pages contain large amounts of boilerplate
and repeated framework vocabulary, which makes lexical ranking brittle for
precise troubleshooting intent.

### Training Data That May Help

Useful data includes document-level robotics documentation retrieval, ROS issue
or Q&A posts linked to source pages, and troubleshooting datasets aligned to
manual pages. Avoid using this split's exact posts or cited full pages for
training.

### Synthetic Data Guidance

Generate long ROS or robotics documentation pages and issue pages, then write
specific troubleshooting posts that require one page. Hard negatives should use
the same ROS package, message family, or simulator but address a different
interface or failure.

## Example Data

| Query | Positive document |
| --- | --- |
| ROS2 Map not received when using nav2_bringup I'm currently using the TurtleBot2 on Ubuntu 22.04 Humble and successfully generated a map with ros2 launch nav2_bringup navigation_launch.py. I was able to use the command ros2 l ... [truncated 225 chars](1101 chars) | # Map Server The `Map Server` provides maps to the rest of the Nav2 system using both topic and service interfaces. Map server will expose maps on the node bringup, but can also change maps using a `load_map` service during r ... [truncated 225 chars](5260 chars) |
| Custom hardware interface type I would like to write a controller that needs all joint states to update a single joint. My idea was to create a class MyStateInterface which inherits from hardware_interface::StateInterface and ... [truncated 225 chars](2560 chars) | Skip to content Toggle navigation [ ](https://github.com/) [ Sign in ](/login?return_to=https%3A%2F%2Fgithub.com%2Fros- controls%2Fros2_control%2Fpull%2F1240) * Product * [ Actions Automate any workflow ](/features/actions) * ... [truncated 225 chars](75706 chars) |
| Add files to be loaded when ROS node is launched Rosanswers logo Hello ROS community, I have a python code for a hardware device (radar) that uses a parameters.cfg file for hardware settings (independantly of ROS). In the sam ... [truncated 225 chars](1169 chars) | [ ![ros.org](/custom/images/ros_org.png) ](/) \| [ About ](http://www.ros.org/about-ros) \| [ Support ](/Support) \| [ Discussion Forum ](http://discourse.ros.org/) \| [ Index ](http://index.ros.org/) \| [ Service Status ](http:// ... [truncated 225 chars](7029 chars) |
| Rosdep installing python dependencies as root seems to break the installation I started with ROS2 for robotic development. As far as I understand one must specify the dependencies of the code in package.xml (for example all p ... [truncated 225 chars](3039 chars) | Skip to content Toggle navigation [ ](https://github.com/) [ Sign in ](/login?return_to=https%3A%2F%2Fgithub.com%2Fros2%2Fros2%2Fissues%2F1478) * Product * [ Actions Automate any workflow ](/features/actions) * [ Packages Hos ... [truncated 225 chars](14000 chars) |
| ldlidar ros 2, colcon build error, pthread mutex init/lock/unlock not declared So i am trying to use the LD19 Lidar from ldrobot with ros2_iron. I am following this tutorial: https://github.com/ldrobotSensorTeam/ldlidar_stl_r ... [truncated 225 chars](2759 chars) | The Single UNIX ® Specification, Version 2 Copyright © 1997 The Open Group * * * #### NAME > pthread_mutex_init, pthread_mutex_destroy - initialise or destroy a mutex #### SYNOPSIS > > > #include <[pthread.h](pthread.h.html)> ... [truncated 225 chars](4377 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightRoboticsLong |
| Source task | Robotics StackExchange long-document |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 101 |
| Documents | 505 |
| Positive qrels | 106 |
| Positives per query | avg 1.05, min 1, median 1, max 2 |
| Multi-positive queries | 5 (4.95%) |
| BM25 nDCG@10 | 0.2490 |
| BM25 hit@10 | 0.4257 |
| BM25 Recall@100 | 0.8019 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2851 |
| Dense hit@10 | 0.4950 |
| Dense Recall@100 | 0.8868 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2866 |
| Reranking hybrid hit@10 | 0.5347 |
| Reranking hybrid Recall@100 | 0.8774 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 12 |
| Query length avg chars | 2179.45 |
| Document length avg chars | 35895.20 |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).
- [BRIGHT project page](https://brightbenchmark.github.io/).
- [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT)
- Source dataset: [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT)
- MTEB dataset record: [mteb/BRIGHT](https://huggingface.co/datasets/mteb/BRIGHT)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | benchmark paper | https://arxiv.org/abs/2407.12883 |
| BRIGHT project page | 2024 | project page | https://brightbenchmark.github.io/ |
| xlangai/BRIGHT | 2024 | dataset card | https://huggingface.co/datasets/xlangai/BRIGHT |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  task_name: NanoBrightRoboticsLong
  split_name: NanoBrightRoboticsLong
  source_task: Robotics StackExchange long-document
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightRoboticsLong.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 101
    documents: 505
    positive_qrels: 106
  positives_per_query:
    average: 1.0495049504950495
    min: 1
    median: 1
    max: 2
    multi_positive_queries: 5
    multi_positive_query_percent: 4.9504950495049505
  text_stats_chars:
    query_mean: 2179.4455445544554
    document_mean: 35895.2
  bm25:
    ndcg_at_10: 0.2489505233164181
    hit_at_10: 0.42574257425742573
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Robotics long-document evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT RoboticsLong queries and full cited source pages
    useful_training_data:
    - document-level robotics documentation retrieval
    - ROS issue or Q&A posts linked to source pages
    - troubleshooting datasets aligned to manual pages
    synthetic_data:
      document_generation: long ROS, Gazebo, controller, or robotics issue pages
      question_generation: specific robotics troubleshooting posts with configuration
        details
      answerability: positive full document should solve the interface or failure
        mode
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
    - label: BRIGHT arXiv
      url: https://arxiv.org/abs/2407.12883
    - label: BRIGHT project
      url: https://brightbenchmark.github.io/
    - label: xlangai/BRIGHT
      url: https://huggingface.co/datasets/xlangai/BRIGHT
    source_notes: []
  references:
  - title: 'BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive
      Retrieval'
    url: https://arxiv.org/abs/2407.12883
    year: 2024
    doi: 10.48550/arXiv.2407.12883
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2489505233
      hit_at_10: 0.4257425743
      recall_at_100: 0.8018867925
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 101
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8018867925
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2850816873
      hit_at_10: 0.495049505
      recall_at_100: 0.8867924528
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 101
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8867924528
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2865678197
      hit_at_10: 0.5346534653
      recall_at_100: 0.8773584906
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.118812
      query_count: 101
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8773584906
      safeguard_positive_rows: 12
      rows_with_101_candidates: 12
```
