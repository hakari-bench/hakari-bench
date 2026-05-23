# NanoCoIR / NanoCodeTransOceanDL

## Overview

CoIR uses CodeTransOcean-DL to frame deep-learning code translation as
cross-framework retrieval. A code fragment written for one library must retrieve
the equivalent implementation in another framework such as MXNet, PyTorch,
TensorFlow, or Paddle. The task emphasizes semantic alignment of tensor
operations, model components, plotting helpers, and training utilities despite
different APIs and boilerplate.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) adapts CodeTransOcean-DL for
code-to-code retrieval, where code in one deep-learning framework retrieves
semantically equivalent code in another. [CodeTransOcean](https://arxiv.org/abs/2310.04951)
introduces DLTrans as a cross-framework code translation dataset built around
mainstream deep-learning frameworks. In retrieval form, the task tests whether
models can recognize equivalent tensor and neural-network code despite library
and API differences.

### Observed Data Profile

The Nano split has 50 queries, 266 documents, and 50 positive qrels. Each query
has one positive. Queries average 2,153.80 characters and documents average
1,644.99 characters. Examples include optimization demos, attention modules,
matrix operations, and plotting helpers from the Dive into Deep Learning style
of code.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5458 and hit@10 = 0.9400. Most positives appear in the top 10, but only 4 are
ranked first; the median best rank is 3. BM25 benefits from shared math,
function names, and comments, but cross-framework API names keep the task from
being trivial.

### Training Data That May Help

Useful training data includes cross-framework deep-learning code pairs, notebook
translation examples, framework migration diffs, and hard negatives that share
mathematical structure but implement different model components.

### Synthetic Data Guidance

Generate equivalent snippets across PyTorch, TensorFlow, MXNet, and Paddle.
Keep tensor shapes, mathematical operations, and model structure aligned, and
include negatives that use similar APIs for a different operation.

### Benchmark Information Leakage

CoIR adapts CodeTransOcean-DL with roughly 564 train queries, 72 dev queries,
and 180 test queries over an 816-document corpus. This Nano split is derived
from the CoIR CodeTransOcean-DL test side. Training on unfiltered test pairs can
leak the exact cross-framework code equivalents used for evaluation.

Training should use train-side or non-overlapping framework-conversion pairs,
then remove any row whose source snippet, target snippet, framework pair,
notebook context, or token fingerprint matches NanoCodeTransOceanDL. A model
trained on leaked pairs may score highly by memorizing known TensorFlow,
PyTorch, MXNet, or Paddle equivalents rather than learning cross-framework
retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| %matplotlib inline import math from mxnet import np, npx from d2l import mxnet as d2l npx.set_np() d2l.set_figsize() gammas = [0.95, 0.9, 0.8, 0.7] for gamma in gammas: x = np.arange(40).asnumpy() d2l.plt.plot(x, (1-gamma) * ... [truncated 225 chars](746 chars) | import math import torch from d2l import torch as d2l d2l.set_figsize() gammas = [0.95, 0.9, 0.8, 0.7] for gamma in gammas: x = torch.arange(40).detach().numpy() d2l.plt.plot(x, (1-gamma) * gamma ** x, label=f'gamma = {gamma: ... [truncated 225 chars](805 chars) |
| %matplotlib inline import numpy as np import tensorflow as tf from d2l import tensorflow as d2l timer = d2l.Timer() A = tf.Variable(tf.zeros((256, 256))) B = tf.Variable(tf.random.normal([256, 256], 0, 1)) C = tf.Variable(tf. ... [truncated 225 chars](3525 chars) | %matplotlib inline import warnings from d2l import paddle as d2l warnings.filterwarnings("ignore") import numpy as np import paddle from paddle import nn timer = d2l.Timer() A = paddle.zeros((256, 256)) B = paddle.randn((256, ... [truncated 225 chars](3316 chars) |
| import numpy as np import tensorflow as tf from d2l import tensorflow as d2l num_hiddens, num_heads = 100, 5 attention = d2l.MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens, num_hiddens, num_heads, 0.5) batch_size, n ... [truncated 225 chars](1474 chars) | import math import warnings from d2l import paddle as d2l warnings.filterwarnings("ignore") import paddle from paddle import nn num_hiddens, num_heads = 100, 5 attention = d2l.MultiHeadAttention(num_hiddens, num_hiddens, num_ ... [truncated 225 chars](1593 chars) |
| %matplotlib inline import warnings from d2l import paddle as d2l warnings.filterwarnings("ignore") import math import paddle from paddle import nn from paddle.optimizer import lr as lr_scheduler def net_fn(): model = nn.Seque ... [truncated 225 chars](4018 chars) | %matplotlib inline import math import torch from torch import nn from torch.optim import lr_scheduler from d2l import torch as d2l def net_fn(): model = nn.Sequential( nn.Conv2d(1, 6, kernel_size=5, padding=2), nn.ReLU(), nn. ... [truncated 225 chars](3912 chars) |
| import math import warnings import pandas as pd from d2l import paddle as d2l warnings.filterwarnings("ignore") import paddle from paddle import nn class PositionWiseFFN(nn.Layer): def __init__(self, ffn_num_input, ffn_num_hi ... [truncated 225 chars](8099 chars) | import math import pandas as pd from mxnet import autograd, np, npx from mxnet.gluon import nn from d2l import mxnet as d2l npx.set_np() class PositionWiseFFN(nn.Block): def __init__(self, ffn_num_hiddens, ffn_num_outputs, ** ... [truncated 225 chars](7132 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoCodeTransOceanDL |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 50 |
| Documents | 266 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.5458 |
| BM25 hit@10 | 0.9400 |
| Query length avg chars | 2153.80 |
| Document length avg chars | 1644.99 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [CodeTransOcean](https://arxiv.org/abs/2310.04951); 2023; Weixiang Yan et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [WeixiangYan/CodeTransOcean](https://huggingface.co/datasets/WeixiangYan/CodeTransOcean)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation | 2023 | source task paper | https://arxiv.org/abs/2310.04951 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoCodeTransOceanDL
  split_name: NanoCodeTransOceanDL
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoCodeTransOceanDL.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 266
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 2153.8
    document_mean: 1644.9924812030076
  bm25:
    ndcg_at_10: 0.5458308219880807
    hit_at_10: 0.94
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR CodeTransOcean-DL test-derived retrieval split
    train_eval_overlap_audit: not_audited_split_filtering_required
    leakage_note: exclude NanoCodeTransOceanDL cross-framework code pairs; do not train on CodeTransOcean-DL test-derived rows
    leakage_risk:
      source_dataset: WeixiangYan/CodeTransOcean DL data
      source_train_queries_reported_by_coir: 564
      source_dev_queries_reported_by_coir: 72
      source_test_queries_reported_by_coir: 180
      risk: upstream CodeTransOcean-DL test pairs can overlap with NanoCodeTransOceanDL evaluation rows
      recommended_filter: train-side only plus normalized source-code, target-code, framework-pair, notebook-context, and token-fingerprint exclusion
    useful_training_data:
      - cross-framework deep-learning code pairs
      - notebook translation examples
      - framework migration hard negatives
    synthetic_data:
      document_generation: equivalent implementations in another deep-learning framework
      question_generation: framework-specific source snippets
      answerability: positive code must implement the same tensor operation or model block
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
      - label: CoIR arXiv
        url: https://arxiv.org/abs/2407.02883
      - label: CodeTransOcean arXiv
        url: https://arxiv.org/abs/2310.04951
      - label: WeixiangYan/CodeTransOcean
        url: https://huggingface.co/datasets/WeixiangYan/CodeTransOcean
    source_notes: []
  references:
    - title: "CoIR: A Comprehensive Benchmark for Code Information Retrieval Models"
      url: https://arxiv.org/abs/2407.02883
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation"
      url: https://arxiv.org/abs/2310.04951
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
