"""Reranker backend that scores pairs through a vLLM pooling server.

The server hosts a ``*ForSequenceClassification`` checkpoint whose one-label
head reproduces the original model score, for example a Qwen3-Reranker
converted with ``scripts/convert_qwen3_reranker_seqcls.py``. The client renders
each pair with the original model's SentenceTransformers chat template and
default prompt, tokenizes it locally, and sends token IDs to ``/classify``, so
the server never re-templates or re-truncates the input.

Pairs that fit ``max_seq_length`` are token-identical to the
SentenceTransformers CrossEncoder. Longer pairs differ on purpose: CrossEncoder
truncates the rendered template from the right, which removes the final
assistant prompt that the yes/no score is read from. This client keeps the
template prefix, the query, and the template suffix, and truncates only the
document, as the official Qwen3-Reranker recipe does.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Protocol

import numpy as np
import orjson
import urllib3

from hakari_bench.models import ModelLoadConfig

DOCUMENT_MARKER = "HAKARI_DOCUMENT_PLACEHOLDER_3f9a1c"
# Documents longer than this many characters per allowed token are pre-cut
# before tokenization; the cut is only used when it still overflows the budget.
PRE_CUT_CHARS_PER_TOKEN = 12
PRE_CUT_SAFETY_TOKENS = 64
CONNECTION_RETRIES = 3


class _HttpClient(Protocol):
    def request(self, method: str, url: str, *, body: bytes, headers: dict[str, str], timeout: float) -> Any: ...


class VllmRerankerClient:
    def __init__(
        self,
        *,
        endpoint: str,
        served_model: str,
        tokenizer: Any,
        max_seq_length: int,
        prompts: dict[str, str] | None = None,
        default_prompt_name: str | None = None,
        max_request_tokens: int = 262144,
        concurrency: int = 4,
        timeout: float = 3600.0,
        server_metadata: dict[str, Any] | None = None,
        parameter_model: Any | None = None,
        http: _HttpClient | None = None,
    ) -> None:
        if not endpoint:
            raise ValueError("vLLM endpoint is required.")
        if max_seq_length <= 0 or max_request_tokens <= 0 or concurrency <= 0:
            raise ValueError("max_seq_length, max_request_tokens, and concurrency must be positive.")
        self.endpoint = endpoint.rstrip("/")
        self.served_model = served_model
        self.tokenizer = tokenizer
        self.max_seq_length = int(max_seq_length)
        self.prompts = dict(prompts or {})
        self.default_prompt_name = default_prompt_name
        self.max_request_tokens = int(max_request_tokens)
        self.concurrency = int(concurrency)
        self.timeout = float(timeout)
        self.server_metadata = dict(server_metadata or {})
        # A meta-device skeleton of the original model, used only for parameter counts.
        self.model = parameter_model
        self._http = http or urllib3.PoolManager(maxsize=self.concurrency)
        self.reset_task_statistics()

    def reset_task_statistics(self) -> None:
        self.scored_pairs = 0
        self.truncated_pairs = 0
        self.truncated_queries = 0
        self.max_input_tokens = 0

    def predict(
        self,
        pairs: Sequence[Sequence[str]],
        *,
        batch_size: int = 32,
        prompt: str | None = None,
        prompt_name: str | None = None,
        show_progress_bar: bool = False,
        **_: Any,
    ) -> np.ndarray:
        instruction = self._resolve_prompt(prompt=prompt, prompt_name=prompt_name)
        encoded = [self.prepare_pair(query, document, instruction=instruction) for query, document in pairs]
        scores = np.empty(len(encoded), dtype=np.float32)
        requests = list(self._request_batches(encoded))
        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            for indices, values in zip(requests, executor.map(lambda idx: self._classify([encoded[i] for i in idx]), requests)):
                scores[indices] = values
        if not np.isfinite(scores).all():
            raise ValueError("vLLM reranker returned non-finite scores.")
        self.scored_pairs += len(encoded)
        return scores

    def prepare_pair(self, query: str, document: str, *, instruction: str | None) -> list[int]:
        ids = self._encode(self._render(query, document, instruction), self.max_seq_length + 1)
        if len(ids) > self.max_seq_length:
            ids = self._truncate_document(query, document, instruction)
        self.max_input_tokens = max(self.max_input_tokens, len(ids))
        return ids

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "vllm",
            "api": "vllm_classify",
            "endpoint": self.endpoint,
            "served_model": self.served_model,
            "score": "raw last-token classifier logit (no activation)",
            "input": "token ids rendered locally with the SentenceTransformers chat template",
            "truncation": "keep template prefix, query, and suffix; truncate the document tail",
            "max_seq_length": self.max_seq_length,
            "prompts": self.prompts,
            "default_prompt_name": self.default_prompt_name,
            "max_request_tokens": self.max_request_tokens,
            "concurrency": self.concurrency,
            "server": self.server_metadata,
            "scored_pairs": self.scored_pairs,
            "truncated_pairs": self.truncated_pairs,
            "truncated_queries": self.truncated_queries,
            "max_input_tokens": self.max_input_tokens,
        }

    def _resolve_prompt(self, *, prompt: str | None, prompt_name: str | None) -> str | None:
        if prompt is not None:
            return prompt
        name = prompt_name if prompt_name is not None else self.default_prompt_name
        return self.prompts.get(name) if name is not None else None

    def _render(self, query: str, document: str, instruction: str | None) -> str:
        # Same message layout as SentenceTransformers' flat message format with a prompt.
        messages = [{"role": "query", "content": query}, {"role": "document", "content": document}]
        if instruction:
            messages.insert(0, {"role": "system", "content": instruction})
        return self.tokenizer.apply_chat_template(messages, tokenize=False)

    def _encode(self, text: str, limit: int | None = None) -> list[int]:
        kwargs = {} if limit is None else {"truncation": True, "max_length": limit}
        return list(self.tokenizer(text, add_special_tokens=False, **kwargs)["input_ids"])

    def _truncate_document(self, query: str, document: str, instruction: str | None) -> list[int]:
        self.truncated_pairs += 1
        template_length = len(self._encode(self._render("", "", instruction)))
        query_budget = (self.max_seq_length - template_length) * 3 // 4
        query_ids = self._encode(query, query_budget + 1)
        if len(query_ids) > query_budget:
            self.truncated_queries += 1
            query = self.tokenizer.decode(query_ids[:query_budget], skip_special_tokens=False)
        head, tail = self._render(query, DOCUMENT_MARKER, instruction).split(DOCUMENT_MARKER)
        # Keep the separator space with the document so it tokenizes as in the joint text.
        separator = head[len(head.rstrip(" ")) :]
        head_ids = self._encode(head[: len(head) - len(separator)])
        tail_ids = self._encode(tail)
        budget = self.max_seq_length - len(head_ids) - len(tail_ids)
        if budget <= 0:
            raise ValueError("Model context is too short for the reranker template.")
        return head_ids + self._encode_document_prefix(separator + document, budget) + tail_ids

    def _encode_document_prefix(self, text: str, budget: int) -> list[int]:
        cut = budget * PRE_CUT_CHARS_PER_TOKEN
        if len(text) > cut:
            ids = self._encode(text[:cut])
            # Tokens far before the cut are unaffected by it, so a cut that still overflows is exact.
            if len(ids) >= budget + PRE_CUT_SAFETY_TOKENS:
                return ids[:budget]
        return self._encode(text, budget)

    def _request_batches(self, encoded: list[list[int]]) -> Iterable[list[int]]:
        order = sorted(range(len(encoded)), key=lambda index: len(encoded[index]), reverse=True)
        batch: list[int] = []
        tokens = 0
        for index in order:
            length = len(encoded[index])
            if batch and tokens + length > self.max_request_tokens:
                yield batch
                batch, tokens = [], 0
            batch.append(index)
            tokens += length
        if batch:
            yield batch

    def _classify(self, inputs: list[list[int]]) -> list[float]:
        payload = orjson.dumps({"model": self.served_model, "input": inputs, "use_activation": False})
        for attempt in range(CONNECTION_RETRIES + 1):
            try:
                response = self._http.request(
                    "POST",
                    f"{self.endpoint}/classify",
                    body=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=self.timeout,
                )
                break
            except urllib3.exceptions.ProtocolError:
                # Tokenizing very long documents can leave a pooled connection idle past the
                # server keep-alive timeout; scoring is side-effect free, so resend it.
                if attempt == CONNECTION_RETRIES:
                    raise
        status = int(getattr(response, "status", 0))
        data = bytes(getattr(response, "data", b""))
        if status >= 400:
            raise RuntimeError(f"vLLM classify request failed with HTTP {status}: {data[:500].decode(errors='replace')}")
        rows = orjson.loads(data).get("data")
        if not isinstance(rows, list) or len(rows) != len(inputs):
            raise RuntimeError("vLLM classify response did not contain one row per input.")
        scores = [0.0] * len(inputs)
        for row in rows:
            probs = row["probs"]
            if len(probs) != 1:
                raise RuntimeError(f"Expected a one-label classifier, got {len(probs)} labels.")
            scores[int(row["index"])] = float(probs[0])
        return scores


def load_model(config: ModelLoadConfig) -> VllmRerankerClient:
    """Load the client; ``config.model_name_or_path`` is the original model, used for the tokenizer and prompts."""
    if config.model_type != "reranker":
        raise ValueError("The vLLM reranker backend supports reranker evaluation only.")
    kwargs = dict(config.model_loader_kwargs or {})
    endpoint = str(kwargs.pop("endpoint", ""))
    served_model = str(kwargs.pop("served_model", config.model_name_or_path))
    client_kwargs = {key: kwargs.pop(key) for key in ("max_request_tokens", "concurrency", "timeout") if key in kwargs}
    # The server cannot report its quantization or pooling flags, so the caller records them here.
    server_launch = kwargs.pop("server_launch", None)
    if kwargs:
        raise ValueError(f"Unsupported vLLM reranker loader kwargs: {', '.join(sorted(kwargs))}")

    from huggingface_hub import hf_hub_download
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

    source = config.model_name_or_path
    tokenizer = AutoTokenizer.from_pretrained(
        source, revision=config.model_revision, trust_remote_code=config.trust_remote_code
    )
    st_config = json.loads(
        open(hf_hub_download(source, "config_sentence_transformers.json", revision=config.model_revision)).read()
    )
    model_config = AutoConfig.from_pretrained(
        source, revision=config.model_revision, trust_remote_code=config.trust_remote_code
    )
    max_seq_length = config.max_seq_length or int(model_config.max_position_embeddings)
    import torch

    with torch.device("meta"):
        parameter_model = AutoModelForCausalLM.from_config(model_config)
    return VllmRerankerClient(
        endpoint=endpoint,
        served_model=served_model,
        tokenizer=tokenizer,
        max_seq_length=max_seq_length,
        prompts=st_config.get("prompts") or {},
        default_prompt_name=st_config.get("default_prompt_name"),
        server_metadata={**_server_metadata(endpoint, served_model), "launch": server_launch},
        parameter_model=parameter_model,
        **client_kwargs,
    )


def _server_metadata(endpoint: str, served_model: str) -> dict[str, Any]:
    """Record what the server reports about itself; the launch flags are documented separately."""
    http = urllib3.PoolManager()
    metadata: dict[str, Any] = {}
    for path, key in (("/version", "version"), ("/v1/models", "models")):
        response = http.request("GET", f"{endpoint.rstrip('/')}{path}", timeout=30.0)
        if int(response.status) >= 400:
            raise RuntimeError(f"vLLM server {endpoint} did not answer {path}: HTTP {response.status}")
        metadata[key] = orjson.loads(response.data)
    served = [row.get("id") for row in metadata["models"].get("data", [])]
    if served_model not in served:
        raise RuntimeError(f"vLLM server {endpoint} serves {served}, not {served_model!r}.")
    models = [{key: row.get(key) for key in ("id", "root", "max_model_len")} for row in metadata["models"].get("data", [])]
    return {"version": metadata["version"].get("version"), "models": models}
