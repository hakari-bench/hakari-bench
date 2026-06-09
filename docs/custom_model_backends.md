# Custom Model Backends

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

Late-interaction backends must expose:

```python
def encode(self, sentences, *, is_query: bool, **kwargs): ...
```

Late-interaction embeddings should follow the PyLate/ColBERT-compatible shape
already used by HAKARI-Bench: one token-embedding matrix per input text.

These are structural interfaces. Backends do not need to inherit from a HAKARI
base class.

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

## Dummy Backend Example

`examples/custom_backends/dummy_backend.py` is a minimal reference
implementation. It is intentionally simple, but it demonstrates the extension
shape:

```bash
uv run hakari-bench evaluate dense \
  --model dummy/model \
  --model-loader examples.custom_backends.dummy_backend:load_model \
  --model-loader-kwargs-json '{"scale":1.0}' \
  --dataset hakari-bench/NanoBEIR-en \
  --split NanoNQ \
  --no-default-embedding-variants
```

Use it as a template for wrapping hosted embedding APIs, internal model serving
clients, or non-SentenceTransformers Python libraries.
