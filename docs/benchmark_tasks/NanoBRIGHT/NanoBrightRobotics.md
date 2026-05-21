# NanoBRIGHT / NanoBrightRobotics

## Overview

`NanoBrightRobotics` is the Robotics StackExchange slice of BRIGHT. Queries are
long robotics troubleshooting posts, often about ROS, Gazebo, controllers, or
simulation; relevant documents are cited passages that help resolve the issue.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) includes Robotics as one of its
knowledge-intensive StackExchange domains. The paper states that StackExchange
queries often have long technical descriptions and that positives are web
passages linked from accepted or high-vote answers, while annotators add
topically similar negatives. For Robotics, the retrieval problem is usually to
connect a concrete system failure to a relevant documentation or issue passage.

### Observed Data Profile

The split has 101 queries, 10,000 documents, and 518 positive qrels. Queries
average 2179.45 characters, the longest of this NanoBRIGHT batch, and often
contain code snippets, ROS version details, XML, controller configuration, and
error descriptions. Documents average 382.35 characters and are short passages
from documentation, GitHub issues, or API references. Positives average 5.13 per
query, with a median of 2.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0888 and hit@10 = 0.2376. It ranks only 4 queries with a positive first, and
the median best positive rank is 92. The long queries contain many distracting
technical tokens, so lexical matching can overfit to incidental ROS or XML terms
instead of the actual cause or relevant interface.

### Training Data That May Help

Useful data includes non-overlapping Robotics StackExchange posts with cited
sources, ROS/Gazebo documentation search data, issue-to-document pairs, and
hard negatives from the same package or controller but a different failure mode.

### Synthetic Data Guidance

Generate robotics troubleshooting posts with realistic versions, snippets,
configuration files, and symptoms. Positives should be documentation or issue
passages that explain the relevant interface, plugin, controller, or message
type. Hard negatives should share the same framework but not solve the failure.

## Example Data

| Query | Positive document |
| --- | --- |
| ROS2 Map not received when using nav2_bringup I'm currently using the TurtleBot2 on Ubuntu 22.04 Humble and successfully generated a map with ros2 launch nav2_bringup navigation_launch.py. I was able to use the command ros2 l ... [truncated 225 chars](1101 chars) | ## MapIO library `MapIO` library contains following API functions declared in `map_io.hpp` to work with OccupancyGrid maps: - loadMapYaml(): Load and parse the given YAML file - loadMapFromFile(): Load the image from map file ... [truncated 225 chars](1367 chars) |
| Custom hardware interface type I would like to write a controller that needs all joint states to update a single joint. My idea was to create a class MyStateInterface which inherits from hardware_interface::StateInterface and ... [truncated 225 chars](2560 chars) | \| \| // END: for backward compatibility Copy link Member ### ![@saikishor](https://avatars.githubusercontent.com/u/10082428?s=48&v=4) **[ saikishor ](/saikishor) ** Mar 17, 2024 There was a problem hiding this comment. ### Cho ... [truncated 225 chars](1633 chars) |
| Add files to be loaded when ROS node is launched Rosanswers logo Hello ROS community, I have a python code for a hardware device (radar) that uses a parameters.cfg file for hardware settings (independantly of ROS). In the sam ... [truncated 225 chars](1169 chars) | # Python In Python, you can use the ` RosPack ` class in the [ rospkg ](http://docs.ros.org/independent/api/rospkg/html/) library to get information about ROS packages. For example: 1 import rospkg 2 3 # get an instance of Ro ... [truncated 225 chars](631 chars) |
| Rosdep installing python dependencies as root seems to break the installation I started with ROS2 for robotic development. As far as I understand one must specify the dependencies of the code in package.xml (for example all p ... [truncated 225 chars](3039 chars) | def main(args=None): rclpy.init(args=args) sensor = Vl53l1x_publisher() rclpy.on_shutdown(Vl53l1x_publisher.stop) rclpy.spin(sensor) # Destroy the node explicitly # (optional - otherwise it will be done automatically # when t ... [truncated 225 chars](1120 chars) |
| ldlidar ros 2, colcon build error, pthread mutex init/lock/unlock not declared So i am trying to use the LD19 Lidar from ldrobot with ros2_iron. I am following this tutorial: https://github.com/ldrobotSensorTeam/ldlidar_stl_r ... [truncated 225 chars](2759 chars) | > > > #include <[pthread.h](pthread.h.html)> > > int pthread_mutex_init(pthread_mutex_t * _mutex_ , > const pthread_mutexattr_t * _attr_ ); > int pthread_mutex_destroy(pthread_mutex_t * _mutex_ ); > pthread_mutex_t _mutex_ = ... [truncated 225 chars](285 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightRobotics |
| Source task | Robotics StackExchange |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 101 |
| Documents | 10000 |
| Positive qrels | 518 |
| Positives per query | avg 5.13, min 1, median 2, max 33 |
| Multi-positive queries | 65 (64.36%) |
| BM25 nDCG@10 | 0.0888 |
| BM25 hit@10 | 0.2376 |
| Query length avg chars | 2179.45 |
| Document length avg chars | 382.35 |

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
  task_name: NanoBrightRobotics
  split_name: NanoBrightRobotics
  source_task: Robotics StackExchange
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightRobotics.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 101
    documents: 10000
    positive_qrels: 518
  positives_per_query:
    average: 5.128712871287129
    min: 1
    median: 2
    max: 33
    multi_positive_queries: 65
    multi_positive_query_percent: 64.35643564356435
  text_stats_chars:
    query_mean: 2179.4455445544554
    document_mean: 382.3519
  bm25:
    ndcg_at_10: 0.08879149656934751
    hit_at_10: 0.2376237623762376
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Robotics StackExchange evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT Robotics queries, cited positives, and linked answer pages
    useful_training_data:
      - non-overlapping Robotics StackExchange posts with cited sources
      - ROS and Gazebo documentation search data
      - issue-to-document troubleshooting pairs
    synthetic_data:
      document_generation: ROS, Gazebo, controller, and robotics API passages
      question_generation: long robotics troubleshooting posts with versions and snippets
      answerability: positives should explain the relevant interface, plugin, controller, or message type
    multi_positive_training: multi_positive_objective
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
    - title: "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval"
      url: https://arxiv.org/abs/2407.12883
      year: 2024
      doi: 10.48550/arXiv.2407.12883
      is_paper: true
      source_confidence: definitive_paper_link
```
