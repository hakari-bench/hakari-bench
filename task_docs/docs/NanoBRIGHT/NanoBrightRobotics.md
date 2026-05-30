# NanoBRIGHT / NanoBrightRobotics

## Overview

NanoBrightRobotics is the Robotics StackExchange slice of NanoBRIGHT. Queries are long troubleshooting posts about robotics systems, often involving ROS, ROS2, Gazebo, controllers, navigation, hardware interfaces, launch files, or build errors. Relevant documents are passages from documentation, issue threads, API references, or cited resources that help resolve the specific technical problem. The task is useful for evaluating retrieval under long, noisy, implementation-heavy queries.

## Details

### What the Original Data Measures

BRIGHT's StackExchange tasks use real user posts as queries and cited or validated sources as positives. In Robotics, the query often includes environment details, command output, package names, XML or YAML snippets, hardware references, and error messages. A positive passage may explain the relevant interface, message type, plugin behavior, package dependency, or configuration rule.

The task measures troubleshooting retrieval rather than general robotics concept search. Relevance depends on whether the source helps solve the failure mode, not merely whether it names the same package or framework.

### Observed Data Profile

The task contains 101 queries, 10,000 documents, and 518 relevance judgments. It has 5.13 positives per query on average, with a minimum of 1, a median of 2.0, a maximum of 33, and 65 multi-positive queries, or 64.36% of the set.

Queries average 2,179.45 characters, making this one of the longest-query NanoBRIGHT slices. Documents average 382.35 characters and are short technical passages. The query length means many tokens are incidental: versions, paths, package names, command lines, and partial logs may or may not identify the real issue.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2607, hit@10 of 0.5149, and recall@100 of 0.4981 using the top-500 BM25 candidate subset. Lexical retrieval is useful because robotics troubleshooting contains distinctive technical identifiers such as nav2_bringup, OccupancyGrid, rosdep, pthread, controller interfaces, and ROS package names.

The limitation is that long queries contain many distracting exact tokens. BM25 can over-rank passages that match a package name or log fragment without explaining the interface or failure mode. It is a reasonable baseline but not the best candidate source.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2589, hit@10 of 0.4851, and recall@100 of 0.4865. Dense retrieval is close to BM25 in nDCG@10 but slightly worse on hit@10 and recall@100. This suggests that general semantic similarity alone does not fully capture robotics troubleshooting details.

Dense retrieval can connect broad problem descriptions to related documentation, but it may smooth over exact package names, message types, and API details that are decisive. The task therefore does not behave like a purely semantic science QA benchmark.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2976, hit@10 of 0.5248, and recall@100 of 0.5656. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 19 safeguard rows, candidate counts from 100 to 101, and a mean of 100.19 candidates.

Hybrid retrieval is the strongest profile across all reported metrics. The result is consistent with the task structure: sparse matching captures exact technical identifiers, while dense retrieval helps connect symptoms to explanatory documentation. The combined pool is the best observed input for reranking.

### Metric Interpretation for Model Researchers

This task rewards hybrid search because neither exact terms nor semantic similarity are sufficient alone. BM25 and dense are nearly tied for nDCG@10, but each misses different cases. The hybrid profile improves both ranking and recall, showing that robotics troubleshooting benefits from preserving exact names while also modeling the failure context.

Researchers should pay attention to long-query robustness. A retriever must identify the decisive part of a long technical post and avoid being dominated by irrelevant snippets. Rerankers should compare the failure mode, framework version, package, interface, and configuration details.

### Query and Relevance Type Tendencies

Queries include ROS2 map loading issues, custom hardware interfaces, launch-time parameter file loading, rosdep dependency problems, lidar build failures, Gazebo configuration, controllers, and simulation setup. Positive documents may be ROS documentation, GitHub issue comments, API pages, or system-level references.

The relevance relation is troubleshooting support. A positive passage explains the command, API, message, dependency, or interface needed to solve the user's problem.

### Representative Failure Modes

Likely failures include matching the same ROS package but the wrong failure mode, over-ranking log-token overlap, missing a relevant page because the query describes symptoms indirectly, and confusing related interfaces such as state, command, controller, and message types.

BM25 is vulnerable to incidental technical tokens. Dense retrieval is vulnerable to losing exact identifiers. Hybrid retrieval improves the balance but still needs a reranker that can reason over the specific system context.

### Training Data That May Help

Useful training data includes non-overlapping Robotics StackExchange posts with cited sources, ROS and Gazebo documentation search data, issue-to-document troubleshooting pairs, and hard negatives from the same package or controller but a different failure mode.

Synthetic data should generate robotics troubleshooting posts with realistic versions, snippets, configuration files, commands, and symptoms. Positives should explain the relevant interface, plugin, controller, dependency, or message type. Hard negatives should share the framework but not solve the failure.

### Model Improvement Notes

Strong systems should preserve exact technical identifiers while still understanding the symptom. Sparse and dense retrieval should be combined rather than treated as alternatives. Query decomposition may help: identify the framework, component, error, and desired behavior before matching sources.

The observed scores make reranking_hybrid the most useful candidate source. Further gains likely require rerankers trained on issue resolution, documentation grounding, and code/configuration-aware matching.

## Example Data

### Public Sources

The original task is based on BRIGHT's reasoning-intensive retrieval benchmark, with NanoBRIGHT providing the compact dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| A ROS2 Nav2 setup does not receive a map after launching navigation. | A map I/O passage describes APIs for loading map YAML and image files. |
| A custom hardware interface needs all joint states to update one joint. | A ROS control issue thread discusses compatibility and interface behavior. |
| A ROS node needs to load a separate parameter file at launch. | A rospkg passage explains how Python code can locate package resources. |
| rosdep installs Python dependencies in a way that breaks a ROS2 package. | A ROS2 code passage shows node initialization and shutdown behavior. |
| A lidar package fails to build because pthread mutex functions are undeclared. | A POSIX reference passage lists pthread mutex initialization and locking functions. |
