# Custom Model Backends

This document explains how to evaluate non-standard dense, sparse, reranker, or late-interaction models in HAKARI-Bench by supplying a custom Python loader instead of the built-in SentenceTransformers, SparseEncoder, CrossEncoder, or PyLate loaders. It defines the duck-typed loader contract, method-specific encode or score interfaces, backend kwargs, params JSON usage, metadata expectations, secrets handling, pre-quantized SentenceTransformers artifact support, and a dummy backend example. Coding agents should use this file when searching for `--model-loader`, hosted embedding APIs, custom reranker wrappers, backend kwargs, parameter metadata, remote providers, or non-SentenceTransformers model integration.

HAKARI-Bench can evaluate model objects that are not implemented with
SentenceTransformers, as long as they provide the small duck-typed interface
needed by the selected evaluation method.

The default behavior is unchanged:

- `evaluate dense` loads `sentence_transformers.SentenceTransformer`.
- `evaluate sparse` loads `sentence_transformers.sparse_encoder.SparseEncoder`.
- `evaluate reranker` loads `sentence_transformers.CrossEncoder`.
- `evaluate late-interaction` loads PyLate `ColBERT`.

Use a custom loader only when the model should be created by another Python
library, an internal wrapper, or a hosted embedding/reranker API.

## Loader Contract

The built-in `--model-loader typesafe` integrates hosted Jev reranking. Use
`--typesafe-mode pointwise` for one request per query/document pair, or `listwise` for
all candidates in one shared state, with recorded mmBERT-guided splitting and
score merging when estimated budgets or API token limits are exceeded. The
tokenizer is configurable; mmBERT is the default. See
[TypeSafe reranker evaluation](typesafe_reranker_evaluation.md) for commands,
limits, comparison policy, and runtime metadata.

Pass a loader with `--model-loader module:function`. The callable receives a
`hakari_bench.models.ModelLoadConfig` and returns any Python object matching the
method interface.

```python
from hakari_bench.models import ModelLoadConfig


def load_model(config: ModelLoadConfig):
    kwargs = config.model_loader_kwargs or {}
    return MyEmbeddingApiClient(**kwargs)
```

Runtime dependencies for the custom loader must be importable in the same
Python environment used to run `hakari-bench`.

## Method Interfaces

Dense and sparse embedding backends must expose either role-aware methods:

```python
def encode_query(self, sentences, **kwargs): ...
def encode_document(self, sentences, **kwargs): ...
```

or a generic encoder:

```python
def encode(self, sentences, **kwargs): ...
```

Reranker backends must expose at least one of:

```python
def rank(self, query, documents, **kwargs): ...
def predict(self, pairs, **kwargs): ...
def __call__(self, pairs, **kwargs): ...
```

For rerankers exposing `predict` or a callable scoring interface, HAKARI groups
pairs by query and sends up to `--batch-size` pairs per call (default 32, with no
fixed upper cap). For example, `--batch-size 128 --rerank-top-k 100` sends all
100 selected candidates for each query in one call. The backend still determines
whether it scores those candidates jointly or independently. Smaller batches
change the available context for listwise scoring, so scores from separate
chunks must be comparable. Rank-only backends receive all selected documents
for each query in one `rank` call and manage their own internal batching.

Late-interaction backends must expose:

```python
def encode(self, sentences, *, is_query: bool, **kwargs): ...
```

Late-interaction embeddings should follow the PyLate/ColBERT-compatible shape
already used by HAKARI-Bench: one token-embedding matrix per input text.

These are structural interfaces. Backends do not need to inherit from a HAKARI
base class.

## Selecting the Reranker `rank` Path

The evaluator selects the interface automatically. A callable `predict` method
or a callable model object takes precedence over `rank`, even when both exist.
There is no CLI flag to force `rank`. The standard CrossEncoder therefore uses
the pair-scoring path. To select `rank`, return an object with a `rank` method
but no callable `predict` or `__call__` from your custom loader.

### Adapting a Listwise Reranker

Use the rank-only interface for listwise rerankers that compare candidates in a
shared context. If your model already satisfies this contract, the loader can
return it directly. Otherwise, write an adapter that exposes only `rank` and
translates between the model's native interface and HAKARI's ranking format.
Increasing `--batch-size` on the `predict` path is not a robust substitute:
queries with more candidates than the batch size would still be split by the
evaluator, changing the context available to the model.

The adapter should:

- Accept one query and all selected documents in `rank(query, documents)`.
  `--rerank-top-k` controls candidate selection before this call; `rank` receives
  the selected candidates, not the full corpus.
- Keep candidate identities tied to their positions in the input list, including
  when documents contain identical text. Return every input position exactly
  once as an integer `corpus_id`.
- Return entries in ranked order without `score` when the model produces a
  permutation. If returning numeric scores, make them comparable across all
  candidates; HAKARI sorts them in descending order. Omit scores to preserve an
  adapter-defined tie order.
- Handle context limits internally when necessary. Define any splitting,
  overlapping windows, and ranking or score merging explicitly. A rank-only
  interface avoids evaluator-side splitting but does not guarantee that all
  candidates fit in one model request.
- Record model settings, context limits, splitting, and merging choices through
  `metadata()` so the result explains how the ranking was produced. See
  [Metadata and Secrets](#metadata-and-secrets).

Avoid exposing `predict` or forwarding it through a generic `__getattr__` on
the adapter, and do not make the adapter callable: either would select the
pair-scoring path instead. A `rank` signature accepting only `query` and
`documents` is sufficient; HAKARI filters unsupported keyword arguments.

The built-in `TypeSafeRerankerAdapter` in `hakari_bench/models.py` demonstrates
this design for Jev. It exposes only `rank`, constructs shared candidate context
in listwise mode, manages token-budget splitting and score merging internally,
and returns ordered `corpus_id` entries without scores to preserve its tie order.
Its metadata records the splitting policy and query-level diagnostics. These
are Jev-specific implementation choices; other listwise adapters should use
policies appropriate to their model. See
[TypeSafe Jev reranker evaluation](typesafe_reranker_evaluation.md).

### Wrapping an Existing `rank` Method

For example, save this wrapper as `rank_backend.py` in the repository root to
call the built-in CrossEncoder through its `rank` interface:

```python
from dataclasses import replace

from hakari_bench.models import ModelLoadConfig, load_model as load_builtin_model


class RankOnlyBackend:
    def __init__(self, model):
        self.model = model

    def rank(self, query, documents, **kwargs):
        return self.model.rank(query, documents, **kwargs)


def load_model(config: ModelLoadConfig):
    model = load_builtin_model(
        replace(config, model_loader=None, model_loader_kwargs=None)
    )
    return RankOnlyBackend(model)
```

Run it with your model ID:

```bash
PYTHONPATH="$PWD" uv run hakari-bench evaluate reranker \
  --model YOUR_CROSS_ENCODER_MODEL \
  --model-loader rank_backend:load_model \
  --dataset NanoBEIR-en --split NanoHotpotQA \
  --rerank-top-k 100 --batch-size 128 \
  --results-dir output/rank-interface
```

HAKARI passes the selected, deterministically shuffled documents together to
`rank`, forwarding supported kwargs including `batch_size`, `top_k=None`, and
`return_documents=False`. A backend may still batch internally. Calling
CrossEncoder's `rank` does not turn a pairwise model into a listwise model.
For a custom listwise model, implement the joint ranking inside `rank` instead.

Return one entry per document with an integer `corpus_id` indexing the input
`documents`. Entries with numeric `score` values are sorted by descending score;
without scores, return entries in the desired ranking order. When invoking
`evaluate_reranker_task` directly from Python, pass the same rank-only object as
`model` to select this path.

The built-in TypeSafe adapter already exposes only `rank`; use
`--model-loader typesafe --typesafe-mode listwise` to select its listwise mode.
See [the TypeSafe commands](typesafe_reranker_evaluation.md#commands).

## Passing Backend Kwargs

Loader kwargs are available on `ModelLoadConfig.model_loader_kwargs`:

```bash
uv run hakari-bench evaluate dense \
  --model api/embed-v1 \
  --model-loader my_pkg.hakari_loader:load_model \
  --model-loader-kwargs-json '{"endpoint":"https://example.test","model":"embed-v1"}'
```

Extra encode kwargs can be passed to both query and document encoding:

```bash
uv run hakari-bench evaluate dense \
  --model api/embed-v1 \
  --model-loader my_pkg.hakari_loader:load_model \
  --encode-kwargs-json '{"dimensions":1024}'
```

Role-specific kwargs override common encode kwargs:

```bash
uv run hakari-bench evaluate dense \
  --model api/embed-v1 \
  --model-loader my_pkg.hakari_loader:load_model \
  --encode-kwargs-json '{"dimensions":1024}' \
  --query-encode-kwargs-json '{"input_type":"query"}' \
  --document-encode-kwargs-json '{"input_type":"document"}'
```

The evaluator calls encode methods with signature-aware kwargs. Arguments that
are not accepted by a backend method are omitted, so a hosted API wrapper does
not need to accept SentenceTransformers-specific options such as
`convert_to_numpy`.

For rerankers, keep using `--reranker-inference-kwargs-json`; those kwargs are
passed to `rank`, `predict`, or the callable backend.

## Params JSON

The same configuration is available through `--params-json`:

```json
{
  "model": {
    "source": "api/embed-v1",
    "loader": "my_pkg.hakari_loader:load_model",
    "loader_kwargs": {
      "endpoint": "https://example.test",
      "model": "embed-v1"
    }
  },
  "prompts": {
    "encode_kwargs": {
      "dimensions": 1024
    },
    "query_encode_kwargs": {
      "input_type": "query"
    },
    "document_encode_kwargs": {
      "input_type": "document"
    }
  }
}
```

## Metadata and Secrets

If the backend object has a `metadata()` method returning a dictionary, the
result JSON records it under `model.backend_metadata`. A
`backend_library` value in that metadata is also used as the top-level
`model.backend_library`.

Loader kwargs are recorded in result JSON after redacting keys whose names look
secret-bearing, including `api_key`, `token`, `secret`, `password`, and
`credential`. Prefer passing real secrets through environment variables rather
than JSON.

## Pre-Quantized SentenceTransformers Artifacts

SentenceTransformers can load already-exported ONNX and OpenVINO artifacts when
the model repository contains them. Use this path when the quantization has
already been done outside HAKARI-Bench and you want to evaluate that artifact
directly, for example an ONNX Runtime qint8 model or an OpenVINO INT8 IR model.

This is different from HAKARI's dense embedding variants such as `int8`,
`binary`, `rescore:int8`, and `rescore:binary`. Those variants quantize or
rescore the embeddings after model inference. A pre-quantized ONNX/OpenVINO
backend changes the model inference itself. You can use both together, but keep
the distinction clear when comparing results.

`examples/custom_backends/quantized_sentence_transformers.py` is a small loader
that forwards to `SentenceTransformer(..., backend=..., model_kwargs=...)` and
records the selected backend and artifact path in result JSON metadata. Because
`examples/` is not installed as a package, run these examples from the repository
checkout with `PYTHONPATH=$PWD`.

Install the backend runtime dependencies in the command environment. For a
one-off run, `uv run --with` is usually enough:

```bash
PYTHONPATH=$PWD uv run --with 'sentence-transformers[onnx,openvino]>=5.4' \
  hakari-bench evaluate dense \
    --model hotchpotch/bekko-embedding-v1-a8m \
    --model-alias hotchpotch/bekko-embedding-v1-a8m-onnx-qint8-avx512-cpu \
    --model-loader examples.custom_backends.quantized_sentence_transformers:load_model \
    --model-loader-kwargs-json '{"backend":"onnx","model_kwargs":{"file_name":"onnx/model_qint8_avx512.onnx","provider":"CPUExecutionProvider"}}' \
    --dataset hakari-bench/NanoBEIR-en \
    --split NanoNQ \
    --device cpu \
    --dtype fp32 \
    --retrieval-score-device cpu
```

For OpenVINO CPU inference, point the loader at the quantized IR artifact and
pass OpenVINO's CPU device through `model_kwargs`:

```bash
PYTHONPATH=$PWD uv run --with 'sentence-transformers[onnx,openvino]>=5.4' \
  hakari-bench evaluate dense \
    --model hotchpotch/bekko-embedding-v1-a8m \
    --model-alias hotchpotch/bekko-embedding-v1-a8m-openvino-qint8-cpu \
    --model-loader examples.custom_backends.quantized_sentence_transformers:load_model \
    --model-loader-kwargs-json '{"backend":"openvino","model_kwargs":{"file_name":"openvino/openvino_model_qint8_quantized.xml","device":"CPU"}}' \
    --dataset hakari-bench/NanoBEIR-en \
    --split NanoNQ \
    --device cpu \
    --dtype fp32 \
    --retrieval-score-device cpu
```

Run the original non-quantized model as a separate logical model name, then
compare the result JSON or rebuild the DuckDB viewer database:

```bash
uv run hakari-bench evaluate dense \
  --model hotchpotch/bekko-embedding-v1-a8m \
  --dataset hakari-bench/NanoBEIR-en \
  --split NanoNQ \
  --dtype bf16 \
  --device cuda:0
```

Using distinct `--model-alias` values for the quantized backends keeps the
original, ONNX, and OpenVINO rows separate in result JSON and DuckDB. This makes
the quality delta visible for the same task, such as base nDCG@10 for the
original model versus the pre-quantized ONNX and OpenVINO CPU inference paths.

## Dummy Backend Example

`examples/custom_backends/dummy_backend.py` is a minimal reference
implementation. It is intentionally simple, but it demonstrates the extension
shape:

```bash
PYTHONPATH=$PWD uv run hakari-bench evaluate dense \
  --model dummy/model \
  --model-loader examples.custom_backends.dummy_backend:load_model \
  --model-loader-kwargs-json '{"scale":1.0}' \
  --dataset hakari-bench/NanoBEIR-en \
  --split NanoNQ \
  --no-default-embedding-variants
```

Use it as a template for wrapping hosted embedding APIs, internal model serving
clients, or non-SentenceTransformers Python libraries.
