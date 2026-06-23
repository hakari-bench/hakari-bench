# NanoBRIGHT / NanoBrightRoboticsLong

## Overview

NanoBrightRoboticsLong is the long-document Robotics StackExchange slice of NanoBRIGHT. Queries are long robotics troubleshooting posts, and relevant documents are full cited pages such as ROS documentation, GitHub issues, message definitions, source pages, or technical references. The task measures whether retrieval systems can identify the source page that solves a precise ROS, Gazebo, controller, interface, or build problem despite long queries and long documents.

## Details

### What the Original Data Measures

BRIGHT's long-document variants retrieve from full source pages rather than split passages. For Robotics, the positive document may be a complete documentation page, issue thread, repository page, or API reference. The useful evidence can be a small section explaining a parameter, service, interface, package behavior, or dependency.

The task is a source-level troubleshooting benchmark. It combines long user posts with long technical pages, so the retriever must match the actual failure mode rather than simply matching framework names or copied error text.

### Observed Data Profile

The task contains 101 queries, 505 documents, and 106 relevance judgments. It is mostly single-positive: there are 1.05 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 2, and 5 multi-positive queries, or 4.95% of the set.

Queries average 2,179.45 characters, while documents average 35,895.20 characters. This creates a double-noise retrieval setting: queries include logs and configuration details, and documents include navigation, comments, code, issue history, or broad documentation sections.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2490, hit@10 of 0.4257, and recall@100 of 0.8019 using the top-500 BM25 candidate subset. Exact matching is useful because robotics pages and queries share identifiers such as package names, message types, launch tools, and low-level function names.

However, top-rank quality is limited. Long pages contain many repeated framework terms, and a query's copied log or package name may appear in a page that does not solve the problem. BM25 is good at candidate coverage but less reliable for first-page precision.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2851, hit@10 of 0.4950, and recall@100 of 0.8868. Dense retrieval improves over BM25 on all reported metrics and has the best recall@100. This suggests that semantic context helps identify the correct source page in long-document robotics retrieval.

Dense retrieval is useful when the query describes a symptom and the relevant page explains the interface or component using different wording. It also helps when the correct page is a full issue or documentation page whose central topic matches the failure mode.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.2866, hit@10 of 0.5347, and recall@100 of 0.8774. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 12 safeguard rows, candidate counts from 100 to 101, and a mean of 100.12 candidates.

Hybrid retrieval is slightly best for nDCG@10 and clearly best for hit@10, while dense is slightly best for recall@100. The practical reading is that hybrid search gives the strongest first page, and dense contributes broad semantic coverage. Both are more effective than BM25 alone for this long-document variant.

### Metric Interpretation for Model Researchers

This task shows a different pattern from the short Robotics slice. In long-document retrieval, dense and hybrid both improve over BM25, suggesting that whole-page semantics help identify the right source. The hybrid score advantage at hit@10 indicates that exact technical identifiers still matter.

Researchers should focus on combining component-level precision with symptom-level semantics. A useful model should not merely retrieve pages that mention ROS2 or Gazebo; it should identify whether the page explains the specific map server, controller interface, dependency, or pthread failure involved.

### Query and Relevance Type Tendencies

Queries include ROS2 map server issues, custom hardware interface design, parameter file loading, rosdep dependency behavior, lidar build errors, and simulation or controller configuration problems. Positive long documents include Nav2 pages, GitHub issue pages, ROS package references, and low-level system documentation.

The relevance relation is full-page source support. The positive document contains the answer-bearing section, but the surrounding page may be much broader than the issue.

### Representative Failure Modes

Likely failures include retrieving a long issue thread for the same package but the wrong bug, over-ranking pages with repeated error terms, missing a documentation page because the query describes a symptom rather than an API name, and treating code snippets as generic text without understanding their role.

BM25 is vulnerable to boilerplate and repeated identifiers. Dense retrieval may miss exact version or interface constraints. Hybrid retrieval balances these signals, but downstream reranking must still inspect the precise failure mode.

### Training Data That May Help

Useful training data includes document-level robotics documentation retrieval, ROS issue or Q&A posts linked to source pages, troubleshooting datasets aligned to manual pages, and source-page supervision from accepted answers.

Synthetic data should generate long ROS, Gazebo, controller, or robotics issue pages and detailed troubleshooting queries with configuration snippets. Positives should solve the specific interface or failure mode. Hard negatives should use the same package, message family, or simulator but address a different issue.

### Model Improvement Notes

Strong models should preserve exact package and interface names while modeling the user's symptom and desired behavior. Dense retrieval is valuable for source-page semantics; sparse retrieval is valuable for identifiers and error fragments. Reranking_hybrid is the best observed first-page candidate source.

Long-document systems may benefit from section retrieval, issue-thread summarization, and reranking that identifies whether a page contains a concrete fix or authoritative interface explanation.

## Example Data

| Query | Positive document |
| --- | --- |
| ROS2 Map not received when using nav2_bringup I'm currently using the TurtleBot2 on Ubuntu 22.04 Hum... [100 / 1,101 chars] | # Map Server The `Map Server` provides maps to the rest of the Nav2 system using both topic and service interfaces. Map server will expose maps on the node bringup, but can also change maps using a `l... [200 / 5,260 chars] |
| Custom hardware interface type I would like to write a controller that needs all joint states to upd... [100 / 2,560 chars] | Skip to content Toggle navigation [ ](https://github.com/) [ Sign in ](/login?return_to=https%3A%2F%2Fgithub.com%2Fros- controls%2Fros2_control%2Fpull%2F1240) * Product * [ Actions Automate any workfl... [200 / 75,706 chars] |
| Add files to be loaded when ROS node is launched Rosanswers logo Hello ROS community, I have a pytho... [100 / 1,169 chars] | [ ![ros.org](/custom/images/ros_org.png) ](/) \| [ About ](http://www.ros.org/about-ros) \| [ Support ](/Support) \| [ Discussion Forum ](http://discourse.ros.org/) \| [ Index ](http://index.ros.org/) \| [... [200 / 7,029 chars] |
| Rosdep installing python dependencies as root seems to break the installation I started with ROS2 fo... [100 / 3,039 chars] | Skip to content Toggle navigation [ ](https://github.com/) [ Sign in ](/login?return_to=https%3A%2F%2Fgithub.com%2Fros2%2Fros2%2Fissues%2F1478) * Product * [ Actions Automate any workflow ](/features/... [200 / 14,000 chars] |
| ldlidar ros 2, colcon build error, pthread mutex init/lock/unlock not declared So i am trying to use... [100 / 2,759 chars] | The Single UNIX ® Specification, Version 2 Copyright © 1997 The Open Group * * * #### NAME > pthread_mutex_init, pthread_mutex_destroy - initialise or destroy a mutex #### SYNOPSIS > > > #include <[pt... [200 / 4,377 chars] |

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
| A ROS2 Nav2 setup does not receive a map after launching navigation. | A Map Server page explains map service and topic interfaces in the Nav2 system. |
| A custom hardware interface needs all joint states to update a joint. | A long ROS control pull request or issue page discusses interface behavior. |
| A ROS node needs to load a parameter file for hardware settings. | A ROS package page explains locating package resources from Python. |
| rosdep dependency installation breaks a ROS2 package. | A ROS2 issue page discusses package setup and dependency behavior. |
| A lidar package fails because pthread mutex functions are undeclared. | A long POSIX reference page documents pthread mutex functions and headers. |
