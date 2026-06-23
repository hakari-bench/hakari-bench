# NanoCoIR / NanoCodeTransOceanDL

## Overview

NanoCodeTransOceanDL is an English code-to-code retrieval task in NanoCoIR, adapted from CodeTransOcean-DL through CoIR. It treats deep-learning code translation as retrieval: a code snippet written for one framework must retrieve the equivalent implementation in another framework, such as PyTorch, TensorFlow, MXNet, or Paddle.

The task evaluates whether a model can recognize equivalent tensor operations, model blocks, optimization utilities, plotting helpers, and training code despite framework-specific APIs. This is different from general algorithmic translation because many candidates share neural-network vocabulary, tensor shapes, and notebook-style boilerplate.

## Details

### What the Original Data Measures

CodeTransOcean introduces multilingual and cross-framework code translation data. Its DLTrans component focuses on deep-learning framework conversion. CoIR adapts that resource into retrieval by using framework-specific source snippets as queries and equivalent snippets in another framework as documents.

The original data measures cross-framework semantic equivalence. A relevant document should perform the same tensor operation, model construction, training utility, or visualization step as the query, even if the APIs and object classes differ.

### Observed Data Profile

This Nano split contains 50 queries, 266 documents, and 50 positive qrels. Each query has exactly one positive document. Queries average 2,153.80 characters, and documents average 1,644.99 characters. It is a small split, so individual ranking changes can visibly affect aggregate metrics.

Observed examples include discount-factor plotting, matrix multiplication timing, multi-head attention setup, convolutional network training utilities, and position-wise feed-forward layers. Many snippets resemble notebook code from deep-learning teaching material, with imports, framework setup, tensor creation, and plotting calls.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5581, hit@10 of 0.9800, and recall@100 of 1.0000. Because the corpus has only 266 documents, the top-500 candidate subset effectively covers the whole document set. BM25 therefore has excellent hit and recall coverage, but its nDCG@10 shows weaker top-rank ordering.

Lexical retrieval benefits from shared mathematical notation, variable names, comments, function names, and framework-neutral terms such as attention, gamma, timer, or model. At the same time, framework-specific API names differ substantially. PyTorch, TensorFlow, MXNet, and Paddle express similar operations with different class names and tensor methods, which limits BM25 rank precision.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by nDCG@10, reaching 0.6327, with hit@10 of 0.9800 and recall@100 of 0.9800. Dense retrieval improves the top-rank ordering over BM25 by recognizing cross-framework semantic similarity, although it misses one positive by rank 100.

Dense retrieval is well suited to matching equivalent model components and tensor operations across APIs. It can connect an MXNet plotting snippet to a PyTorch plotting snippet, or a TensorFlow attention example to a Paddle equivalent. The small split and highly similar notebook style mean that many candidates remain close, so rank ordering is still difficult.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5956, hit@10 of 0.9800, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard-positive rows. It sits between BM25 and dense retrieval for nDCG while matching BM25's top-100 coverage.

This profile shows that lexical and dense signals are complementary. BM25 ensures coverage in a small corpus and captures shared variable names and comments. Dense similarity better captures framework equivalence. Hybrid retrieval preserves full candidate coverage but still needs a ranker that can distinguish the exact operation from nearby deep-learning snippets.

### Metric Interpretation for Model Researchers

NanoCodeTransOceanDL is a small, cross-framework code retrieval task where hit@10 is not very discriminative because all three candidate profiles reach 0.9800. nDCG@10 is more informative: dense retrieval ranks positives best, reranking_hybrid is second, and BM25 is third.

The task should be interpreted as a framework-equivalence benchmark rather than a broad code search task. Strong models should understand that `torch.arange`, TensorFlow tensor creation, Paddle layers, and MXNet blocks may express comparable operations under different APIs. At the same time, exact tensor shapes, layer parameters, and model structure still matter.

### Query and Relevance Type Tendencies

Queries are long deep-learning code snippets. They may include imports, notebook magic, framework setup, tensor operations, layer definitions, plotting commands, training loops, and utility classes. Documents are equivalent snippets in another framework.

Relevance is operation-level equivalence. The target should implement the same computation or model block, not merely use the same framework category. A candidate that also defines attention or a convolutional network can still be wrong if the shape, layer arrangement, or demonstrated operation differs.

### Representative Failure Modes

BM25 may retrieve snippets with the same variable names or tutorial comments but a different model component. Dense retrieval may retrieve a semantically close deep-learning example that uses the same framework pair but implements a different tensor operation.

Hybrid retrieval can recover the positive while ranking a nearby notebook cell higher. This is likely when examples share imports, plotting setup, `d2l` helper calls, or common layer names. Fine-grained operation matching is required for top-rank improvements.

### Training Data That May Help

Useful training data includes cross-framework deep-learning code pairs, notebook translation examples, and framework migration hard negatives. Good negatives should share mathematical structure or framework APIs while implementing a different operation or model block.

Leakage filtering is required. The Nano split is derived from CoIR CodeTransOcean-DL test-side data. Training should exclude NanoCodeTransOceanDL cross-framework code pairs and should not use CodeTransOcean-DL test-derived rows. Filters should remove normalized source code, target code, framework-pair labels, notebook context, and token fingerprints.

### Model Improvement Notes

Improving this task requires models that understand framework-specific APIs as equivalent operations. Representations should align tensor creation, matrix multiplication, layer construction, optimization schedules, and plotting utilities across libraries.

Because the corpus is small and recall is already high, the main research target is ranking precision. A useful reranker should compare shapes, parameters, layer order, and operation intent, not only framework names or tutorial boilerplate.

## Example Data

| Query | Positive document |
| --- | --- |
| %matplotlib inline import math from mxnet import np, npx from d2l import mxnet as d2l npx.set_np() d2l.set_figsize() gammas = [0.95, 0.9, 0.8, 0.7] for gamma in gammas: x = np.arange(40).asnumpy() d2l.plt.plot(x, (1-gamma) * gamma ** x, label=f'gamma = {gamma:.2f}') d2l.plt.xlabel('time'); def init_rmsprop_states(feature_dim): s_w = np.zeros((feature_dim, 1)) s_b = np.zeros(1) return (s_w, s_b) def rmsprop(params, states, hyperparams): gamma, eps = hyperparams['gamma'], 1e-6 for p, s in zip(para... [500 / 746 chars] | import math import torch from d2l import torch as d2l d2l.set_figsize() gammas = [0.95, 0.9, 0.8, 0.7] for gamma in gammas: x = torch.arange(40).detach().numpy() d2l.plt.plot(x, (1-gamma) * gamma ** x, label=f'gamma = {gamma:.2f}') d2l.plt.xlabel('time'); def init_rmsprop_states(feature_dim): s_w = torch.zeros((feature_dim, 1)) s_b = torch.zeros(1) return (s_w, s_b) def rmsprop(params, states, hyperparams): gamma, eps = hyperparams['gamma'], 1e-6 for p, s in zip(params, states): with torch.no_grad(): s[:] = gamma * s + (1 - gamma) * torch.square(p.grad) p[:] -= hyperparams['lr'] * p.grad / torch.sqrt(s + eps) p.grad.data.zero_() trainer = torch.optim.RMSprop d2l.train_concise_ch11(trainer, {'lr': 0.01, 'alpha': 0.9}, data_iter) [805 chars] |
| %matplotlib inline import numpy as np import tensorflow as tf from d2l import tensorflow as d2l timer = d2l.Timer() A = tf.Variable(tf.zeros((256, 256))) B = tf.Variable(tf.random.normal([256, 256], 0, 1)) C = tf.Variable(tf.random.normal([256, 256], 0, 1)) timer.start() for i in range(256): for j in range(256): A[i, j].assign(tf.tensordot(B[i, :], C[:, j], axes=1)) timer.stop() timer.start() for j in range(256): A[:, j].assign(tf.tensordot(B, C[:, j], axes=1)) timer.stop() timer.start() A.assig... [500 / 3,525 chars] | %matplotlib inline import warnings from d2l import paddle as d2l warnings.filterwarnings("ignore") import numpy as np import paddle from paddle import nn timer = d2l.Timer() A = paddle.zeros((256, 256)) B = paddle.randn((256, 256)) C = paddle.randn((256, 256)) timer.start() for i in range(256): for j in range(256): A[i, j] = paddle.dot(B[i, :], C[:, j]) timer.stop() timer.start() for j in range(256): A[:, j] = paddle.mv(B, C[:, j]) timer.stop() timer.start() A = paddle.mm(B, C) timer.stop() gigaflops = [2/i for i in timer.times] timer.start() for j in range(0, 256, 64): A[:, j:j+64] = paddle.mm(B, C[:, j:j+64]) timer.stop() d2l.DATA_HUB['airfoil'] = (d2l.DATA_URL + 'airfoil_self_noise.dat', '76e5be1548fd8222e5074cf0faae75edff8cf93f') def get_data_ch11(batch_size=10, n=1500): data = np.genfromtxt(d2l.download('airfoil'), dtype=np.float32, delimiter='\t') data = paddle.to_tensor((data - data.mean(axis=0)) / data.std(axis=0)) data_iter = d2l.load_array((data[:n, :-1], data[:n, -1]), batch... [1,000 / 3,316 chars] |
| import numpy as np import tensorflow as tf from d2l import tensorflow as d2l num_hiddens, num_heads = 100, 5 attention = d2l.MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens, num_hiddens, num_heads, 0.5) batch_size, num_queries, valid_lens = 2, 4, tf.constant([3, 2]) X = tf.ones((batch_size, num_queries, num_hiddens)) attention(X, X, X, valid_lens, training=False).shape class PositionalEncoding(tf.keras.layers.Layer): def __init__(self, num_hiddens, dropout, max_len=1000): super().__init... [500 / 1,474 chars] | import math import warnings from d2l import paddle as d2l warnings.filterwarnings("ignore") import paddle from paddle import nn num_hiddens, num_heads = 100, 5 attention = d2l.MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens, num_hiddens, num_heads, 0.5) attention.eval() batch_size, num_queries, valid_lens = 2, 4, paddle.to_tensor([3, 2]) X = paddle.ones((batch_size, num_queries, num_hiddens)) attention(X, X, X, valid_lens).shape class PositionalEncoding(nn.Layer): def __init__(self, num_hiddens, dropout, max_len=1000): super(PositionalEncoding, self).__init__() self.dropout = nn.Dropout(dropout) self.P = paddle.zeros((1, max_len, num_hiddens)) X = paddle.arange(max_len, dtype=paddle.float32).reshape( (-1, 1)) / paddle.pow(paddle.to_tensor([10000.0]), paddle.arange( 0, num_hiddens, 2, dtype=paddle.float32) / num_hiddens) self.P[:, :, 0::2] = paddle.sin(X) self.P[:, :, 1::2] = paddle.cos(X) def forward(self, X): X = X + self.P[:, :X.shape[1], :] return self.dropout(X) encoding_d... [1,000 / 1,593 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [CodeTransOcean: A Comprehensive Multilingual Benchmark for Code Translation](https://arxiv.org/abs/2310.04951) | Source task paper for multilingual and cross-framework code translation. |
| [WeixiangYan/CodeTransOcean](https://huggingface.co/datasets/WeixiangYan/CodeTransOcean) | Public source dataset card. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| An MXNet snippet plots discount-factor curves for several gamma values. | The target PyTorch snippet performs the same plotting computation with equivalent tensor creation. |
| A TensorFlow snippet times matrix operations on 256-by-256 tensors. | The target Paddle snippet constructs equivalent tensors and timing logic. |
| A TensorFlow multi-head attention setup creates inputs and valid lengths. | The target Paddle implementation sets up the same attention module and data shapes. |
| A Paddle convolutional network training utility defines layers and scheduler behavior. | The target PyTorch snippet defines the corresponding network and learning-rate schedule. |
| A Paddle position-wise feed-forward class appears in a transformer-style example. | The target MXNet snippet implements the analogous block using MXNet/Gluon classes. |
