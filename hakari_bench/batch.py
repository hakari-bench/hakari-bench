from __future__ import annotations

import importlib
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np

from hakari_bench.datasets import EvalTask, resolve_dataset_revision
from hakari_bench.evaluation import LoadedIrDataset
from hakari_bench.models import OpenAIEmbeddingAdapter, _load_dotenv_file
from hakari_bench.results import safe_path_part

OPENAI_EMBEDDINGS_BATCH_ENDPOINT = "/v1/embeddings"
DEFAULT_BATCH_WORKSPACE_ROOT = "tmp/batch_workspace"
DEFAULT_BATCH_COMPLETION_WINDOW = "24h"
TERMINAL_BATCH_STATUSES = {"completed", "failed", "cancelled", "expired"}


@dataclass(frozen=True)
class BatchMetadata:
    schema_version: int
    provider: str
    model_type: str
    model: str
    target: str
    workspace_path: Path
    metadata_path: Path
    input_file_path: Path
    output_file_path: Path
    error_file_path: Path
    requests: list[dict[str, Any]]
    tasks: list[dict[str, Any]]
    request_count: int
    embedding_input_count: int
    status: str
    batch_id: str | None = None
    input_file_id: str | None = None
    output_file_id: str | None = None
    error_file_id: str | None = None
    dataset_revision: str | None = None
    config: dict[str, Any] | None = None
    api: dict[str, Any] | None = None

    @classmethod
    def from_path(cls, path: Path) -> BatchMetadata:
        payload = json.loads(path.read_text(encoding="utf-8"))
        workspace_path = Path(payload["workspace_path"])
        return cls(
            schema_version=int(payload["schema_version"]),
            provider=str(payload["provider"]),
            model_type=str(payload["model_type"]),
            model=str(payload["model"]),
            target=str(payload["target"]),
            workspace_path=workspace_path,
            metadata_path=Path(payload.get("metadata_path") or path),
            input_file_path=Path(payload["input_file_path"]),
            output_file_path=Path(payload["output_file_path"]),
            error_file_path=Path(payload["error_file_path"]),
            requests=list(payload["requests"]),
            tasks=list(payload["tasks"]),
            request_count=int(payload["request_count"]),
            embedding_input_count=int(payload["embedding_input_count"]),
            status=str(payload["status"]),
            batch_id=payload.get("batch_id"),
            input_file_id=payload.get("input_file_id"),
            output_file_id=payload.get("output_file_id"),
            error_file_id=payload.get("error_file_id"),
            dataset_revision=payload.get("dataset_revision"),
            config=payload.get("config"),
            api=payload.get("api"),
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "provider": self.provider,
            "model_type": self.model_type,
            "model": self.model,
            "target": self.target,
            "workspace_path": str(self.workspace_path),
            "metadata_path": str(self.metadata_path),
            "input_file_path": str(self.input_file_path),
            "output_file_path": str(self.output_file_path),
            "error_file_path": str(self.error_file_path),
            "requests": self.requests,
            "tasks": self.tasks,
            "request_count": self.request_count,
            "embedding_input_count": self.embedding_input_count,
            "status": self.status,
            "batch_id": self.batch_id,
            "input_file_id": self.input_file_id,
            "output_file_id": self.output_file_id,
            "error_file_id": self.error_file_id,
            "dataset_revision": self.dataset_revision,
            "config": self.config or {},
            "api": self.api or {},
        }

    def write(self) -> None:
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.write_text(json.dumps(self.to_payload(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def replace(self, **changes: Any) -> BatchMetadata:
        payload = self.to_payload()
        payload.update(changes)
        self.metadata_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return BatchMetadata.from_path(self.metadata_path)


class PrecomputedDenseEmbeddingModel:
    similarity_fn_name = "cosine"
    default_prompt_name = None
    prompts = None

    def __init__(
        self,
        *,
        query_embeddings: np.ndarray,
        corpus_embeddings: np.ndarray,
        model_name: str,
        max_seq_length: int | None,
        backend_metadata: dict[str, Any] | None = None,
    ) -> None:
        self.query_embeddings = np.asarray(query_embeddings, dtype=np.float32)
        self.corpus_embeddings = np.asarray(corpus_embeddings, dtype=np.float32)
        self.model_name_or_path = model_name
        self.model_name = model_name
        self.max_seq_length = max_seq_length
        self._backend_metadata = dict(backend_metadata or {})

    def encode_query(self, sentences: list[str], **_: Any) -> np.ndarray:
        if len(sentences) != len(self.query_embeddings):
            raise ValueError(
                f"Precomputed query embedding count mismatch: got {len(sentences)} texts, "
                f"but {len(self.query_embeddings)} embeddings are available."
            )
        return self.query_embeddings

    def encode_document(self, sentences: list[str], **_: Any) -> np.ndarray:
        if len(sentences) != len(self.corpus_embeddings):
            raise ValueError(
                f"Precomputed document embedding count mismatch: got {len(sentences)} texts, "
                f"but {len(self.corpus_embeddings)} embeddings are available."
            )
        return self.corpus_embeddings

    def encode(self, sentences: list[str], **kwargs: Any) -> np.ndarray:
        del kwargs
        if len(sentences) == len(self.query_embeddings):
            return self.query_embeddings
        if len(sentences) == len(self.corpus_embeddings):
            return self.corpus_embeddings
        raise ValueError("Precomputed dense model cannot infer role from text count.")

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "batch-precomputed",
            "batch_materialized": True,
            **self._backend_metadata,
        }


def batch_metadata_path(*, target: str, workspace_root: Path | str = DEFAULT_BATCH_WORKSPACE_ROOT) -> Path:
    return Path(workspace_root) / safe_path_part(target) / "batch_metadata.json"


def load_batch_metadata(*, target: str, workspace_root: Path | str = DEFAULT_BATCH_WORKSPACE_ROOT) -> BatchMetadata:
    return BatchMetadata.from_path(batch_metadata_path(target=target, workspace_root=workspace_root))


def write_openai_embedding_batch_files(
    *,
    target: str,
    workspace_root: Path,
    model: str,
    tasks: list[EvalTask],
    dataset_loader: Callable[[EvalTask], LoadedIrDataset],
    encoding: Any,
    batch_size: int,
    max_input_tokens: int,
    max_request_tokens: int,
    max_embedding_inputs: int | None = None,
    query_prompt: str | None,
    document_prompt: str | None,
    dataset_revision: str | None,
    overwrite: bool = False,
) -> BatchMetadata:
    workspace_path = workspace_root / safe_path_part(target)
    input_file_path = workspace_path / "requests.jsonl"
    output_file_path = workspace_path / "output.jsonl"
    error_file_path = workspace_path / "errors.jsonl"
    metadata_path = workspace_path / "batch_metadata.json"
    if metadata_path.exists() and not overwrite:
        raise FileExistsError(f"Batch metadata already exists: {metadata_path}. Use --overwrite to replace it.")
    workspace_path.mkdir(parents=True, exist_ok=True)

    requests: list[dict[str, Any]] = []
    task_payloads: list[dict[str, Any]] = []
    request_lines: list[str] = []
    embedding_input_count = 0
    for task in tasks:
        dataset = dataset_loader(task)
        task_key = _task_key(task)
        task_payloads.append(
            {
                "dataset_name": task.dataset_name,
                "dataset_id": task.dataset_id,
                "split_name": task.split_name,
                "task_name": task.task_name,
                "task_key": task_key,
                "query_count": len(dataset.queries),
                "corpus_count": len(dataset.corpus),
                "dataset_revision": resolve_dataset_revision(task.dataset_id, requested_revision=dataset_revision),
            }
        )
        request_lines.extend(
            _openai_embedding_request_lines_for_role(
                model=model,
                task=task,
                task_key=task_key,
                role="query",
                ids=list(dataset.queries),
                texts=list(dataset.queries.values()),
                prompt=query_prompt,
                encoding=encoding,
                batch_size=batch_size,
                max_input_tokens=max_input_tokens,
                max_request_tokens=max_request_tokens,
                requests=requests,
            )
        )
        request_lines.extend(
            _openai_embedding_request_lines_for_role(
                model=model,
                task=task,
                task_key=task_key,
                role="document",
                ids=list(dataset.corpus),
                texts=[dataset.corpus[corpus_id] for corpus_id in dataset.corpus],
                prompt=document_prompt,
                encoding=encoding,
                batch_size=batch_size,
                max_input_tokens=max_input_tokens,
                max_request_tokens=max_request_tokens,
                requests=requests,
            )
        )
    embedding_input_count = sum(len(request["ids"]) for request in requests)
    if max_embedding_inputs is not None and embedding_input_count > max_embedding_inputs:
        raise ValueError(
            f"OpenAI embeddings batch has {embedding_input_count:,} inputs, exceeding the "
            f"{max_embedding_inputs:,} input limit. Register fewer tasks or splits for this target."
        )
    input_file_path.write_text("\n".join(request_lines) + ("\n" if request_lines else ""), encoding="utf-8")
    metadata = BatchMetadata(
        schema_version=1,
        provider="openai",
        model_type="dense",
        model=model,
        target=target,
        workspace_path=workspace_path,
        metadata_path=metadata_path,
        input_file_path=input_file_path,
        output_file_path=output_file_path,
        error_file_path=error_file_path,
        requests=requests,
        tasks=task_payloads,
        request_count=len(requests),
        embedding_input_count=embedding_input_count,
        status="prepared",
        dataset_revision=dataset_revision,
        config={
            "batch_size": batch_size,
            "max_input_tokens": max_input_tokens,
            "max_request_tokens": max_request_tokens,
            "max_embedding_inputs": max_embedding_inputs,
            "query_prompt": query_prompt,
            "document_prompt": document_prompt,
            "dimension_reduction": "full_embedding_prefix_l2_normalize",
        },
        api={
            "endpoint": OPENAI_EMBEDDINGS_BATCH_ENDPOINT,
            "completion_window": DEFAULT_BATCH_COMPLETION_WINDOW,
            "input_purpose": "batch",
        },
    )
    metadata.write()
    return metadata


def register_openai_embedding_batch(
    *,
    target: str,
    workspace_root: Path,
    model: str,
    tasks: list[EvalTask],
    dataset_loader: Callable[[EvalTask], LoadedIrDataset],
    batch_size: int,
    max_input_tokens: int,
    max_request_tokens: int,
    max_embedding_inputs: int | None,
    query_prompt: str | None,
    document_prompt: str | None,
    dataset_revision: str | None,
    dotenv_path: str | None,
    api_key_env: str,
    base_url: str | None,
    organization: str | None,
    project: str | None,
    overwrite: bool = False,
) -> BatchMetadata:
    adapter = OpenAIEmbeddingAdapter(
        model_name=model,
        dotenv_path=dotenv_path,
        api_key_env=api_key_env,
        base_url=base_url,
        organization=organization,
        project=project,
        max_input_tokens=max_input_tokens,
        max_request_tokens=max_request_tokens,
    )
    metadata = write_openai_embedding_batch_files(
        target=target,
        workspace_root=workspace_root,
        model=model,
        tasks=tasks,
        dataset_loader=dataset_loader,
        encoding=adapter._tokenizer(),
        batch_size=batch_size,
        max_input_tokens=max_input_tokens,
        max_request_tokens=max_request_tokens,
        max_embedding_inputs=max_embedding_inputs,
        query_prompt=query_prompt,
        document_prompt=document_prompt,
        dataset_revision=dataset_revision,
        overwrite=overwrite,
    )
    client = _openai_client(
        dotenv_path=dotenv_path,
        api_key_env=api_key_env,
        base_url=base_url,
        organization=organization,
        project=project,
    )
    with metadata.input_file_path.open("rb") as file:
        input_file = client.files.create(file=file, purpose="batch")
    batch = client.batches.create(
        input_file_id=_object_id(input_file),
        endpoint=OPENAI_EMBEDDINGS_BATCH_ENDPOINT,
        completion_window=DEFAULT_BATCH_COMPLETION_WINDOW,
        metadata={
            "hakari_target": target[:512],
            "hakari_model_type": "dense",
            "hakari_provider": "openai",
        },
    )
    return metadata.replace(
        status=str(getattr(batch, "status", "submitted")),
        input_file_id=_object_id(input_file),
        batch_id=_object_id(batch),
    )


def refresh_openai_batch_files(
    *,
    metadata: BatchMetadata,
    dotenv_path: str | None,
    api_key_env: str,
    base_url: str | None,
    organization: str | None,
    project: str | None,
) -> BatchMetadata:
    if metadata.batch_id is None:
        raise ValueError("Batch metadata does not contain batch_id.")
    client = _openai_client(
        dotenv_path=dotenv_path,
        api_key_env=api_key_env,
        base_url=base_url,
        organization=organization,
        project=project,
    )
    batch = client.batches.retrieve(metadata.batch_id)
    output_file_id = getattr(batch, "output_file_id", None)
    error_file_id = getattr(batch, "error_file_id", None)
    if output_file_id and not metadata.output_file_path.exists():
        _download_openai_file(client, output_file_id, metadata.output_file_path)
    if error_file_id and not metadata.error_file_path.exists():
        _download_openai_file(client, error_file_id, metadata.error_file_path)
    return metadata.replace(
        status=str(getattr(batch, "status", metadata.status)),
        output_file_id=output_file_id,
        error_file_id=error_file_id,
    )


def wait_for_openai_batch(
    *,
    metadata: BatchMetadata,
    poll_seconds: int,
    dotenv_path: str | None,
    api_key_env: str,
    base_url: str | None,
    organization: str | None,
    project: str | None,
) -> BatchMetadata:
    current = metadata
    while current.status not in TERMINAL_BATCH_STATUSES:
        current = refresh_openai_batch_files(
            metadata=current,
            dotenv_path=dotenv_path,
            api_key_env=api_key_env,
            base_url=base_url,
            organization=organization,
            project=project,
        )
        print(
            json.dumps(
                {
                    "target": current.target,
                    "batch_id": current.batch_id,
                    "status": current.status,
                    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        if current.status in TERMINAL_BATCH_STATUSES:
            break
        time.sleep(poll_seconds)
    return current


def collect_openai_batch_embeddings(*, metadata: BatchMetadata, output_path: Path | None = None) -> dict[str, dict[str, Any]]:
    path = output_path or metadata.output_file_path
    if not path.exists():
        raise FileNotFoundError(f"Batch output file does not exist: {path}")
    request_by_custom_id = {str(request["custom_id"]): request for request in metadata.requests}
    values: dict[str, dict[str, dict[str, list[float]]]] = {}
    with path.open("rt", encoding="utf-8") as file:
        lines = enumerate(file, 1)
        for line_number, line in lines:
            if not line.strip():
                continue
            _collect_openai_batch_output_line(
                line=line,
                line_number=line_number,
                request_by_custom_id=request_by_custom_id,
                values=values,
            )

    results: dict[str, dict[str, Any]] = {}
    for task in metadata.tasks:
        task_key = str(task["task_key"])
        query_requests = [request for request in metadata.requests if request["task_key"] == task_key and request["role"] == "query"]
        doc_requests = [request for request in metadata.requests if request["task_key"] == task_key and request["role"] == "document"]
        query_ids = [str(item) for request in query_requests for item in request["ids"]]
        corpus_ids = [str(item) for request in doc_requests for item in request["ids"]]
        missing_queries = [query_id for query_id in query_ids if query_id not in values.get(task_key, {}).get("query", {})]
        missing_docs = [doc_id for doc_id in corpus_ids if doc_id not in values.get(task_key, {}).get("document", {})]
        if missing_queries or missing_docs:
            raise ValueError(
                f"Batch output is incomplete for {task_key}: "
                f"missing_queries={len(missing_queries)}, missing_docs={len(missing_docs)}"
            )
        results[task_key] = {
            "query_ids": query_ids,
            "corpus_ids": corpus_ids,
            "query_embeddings": np.asarray([values[task_key]["query"][query_id] for query_id in query_ids], dtype=np.float32),
            "corpus_embeddings": np.asarray([values[task_key]["document"][doc_id] for doc_id in corpus_ids], dtype=np.float32),
        }
    return results


def _collect_openai_batch_output_line(
    *,
    line: str,
    line_number: int,
    request_by_custom_id: dict[str, dict[str, Any]],
    values: dict[str, dict[str, dict[str, list[float]]]],
) -> None:
    if not line.strip():
        return
    row = json.loads(line)
    custom_id = str(row.get("custom_id"))
    request = request_by_custom_id.get(custom_id)
    if request is None:
        raise ValueError(f"Batch output line {line_number} has unknown custom_id: {custom_id}")
    error = row.get("error")
    if error is not None:
        raise ValueError(f"Batch output line {line_number} failed for {custom_id}: {error}")
    response = row.get("response")
    if not isinstance(response, dict) or int(response.get("status_code", 0)) >= 400:
        raise ValueError(f"Batch output line {line_number} has non-success response for {custom_id}: {response}")
    body = response.get("body")
    if not isinstance(body, dict):
        raise ValueError(f"Batch output line {line_number} has no response body for {custom_id}.")
    data = body.get("data")
    if not isinstance(data, list):
        raise ValueError(f"Batch output line {line_number} response body has no data list for {custom_id}.")
    ids = [str(item) for item in request["ids"]]
    task_key = str(request["task_key"])
    role = str(request["role"])
    values.setdefault(task_key, {}).setdefault(role, {})
    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f"Batch output line {line_number} has invalid embedding item for {custom_id}.")
        index = int(item.get("index", 0))
        if index < 0 or index >= len(ids):
            raise ValueError(f"Batch output line {line_number} has invalid item index {index} for {custom_id}.")
        values[task_key][role][ids[index]] = [float(value) for value in item["embedding"]]


def _openai_embedding_request_lines_for_role(
    *,
    model: str,
    task: EvalTask,
    task_key: str,
    role: str,
    ids: list[str],
    texts: list[str],
    prompt: str | None,
    encoding: Any,
    batch_size: int,
    max_input_tokens: int,
    max_request_tokens: int,
    requests: list[dict[str, Any]],
) -> list[str]:
    if prompt is not None:
        texts = [f"{prompt}{text}" for text in texts]
    prepared = [_prepare_openai_text(text, encoding=encoding, max_input_tokens=max_input_tokens) for text in texts]
    ranges = _request_ranges(prepared, batch_size=batch_size, max_request_tokens=max_request_tokens)
    lines: list[str] = []
    for start, end in ranges:
        custom_id = f"{safe_path_part(task.dataset_name)}__{safe_path_part(task.split_name)}__{role}__{start:06d}"
        chunk_ids = ids[start:end]
        chunk_prepared = prepared[start:end]
        requests.append(
            {
                "custom_id": custom_id,
                "dataset_id": task.dataset_id,
                "dataset_name": task.dataset_name,
                "split_name": task.split_name,
                "task_name": task.task_name,
                "task_key": task_key,
                "role": role,
                "start": start,
                "end": end,
                "ids": chunk_ids,
                "token_counts": [token_count for _text, token_count in chunk_prepared],
            }
        )
        lines.append(
            json.dumps(
                {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": OPENAI_EMBEDDINGS_BATCH_ENDPOINT,
                    "body": {
                        "model": model,
                        "input": [text for text, _token_count in chunk_prepared],
                        "encoding_format": "float",
                    },
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
    return lines


def _prepare_openai_text(text: str, *, encoding: Any, max_input_tokens: int) -> tuple[str, int]:
    tokens = encoding.encode(str(text), disallowed_special=())
    if len(tokens) > max_input_tokens:
        tokens = tokens[:max_input_tokens]
        text = str(encoding.decode(tokens))
    return str(text), len(tokens)


def _request_ranges(
    prepared: list[tuple[str, int]],
    *,
    batch_size: int,
    max_request_tokens: int,
) -> list[tuple[int, int]]:
    if batch_size <= 0:
        raise ValueError("Batch size must be positive.")
    if max_request_tokens <= 0:
        raise ValueError("OpenAI max_request_tokens must be positive.")
    ranges: list[tuple[int, int]] = []
    start = 0
    while start < len(prepared):
        token_total = 0
        end = start
        while end < len(prepared) and end - start < batch_size:
            next_tokens = prepared[end][1]
            if end > start and token_total + next_tokens > max_request_tokens:
                break
            token_total += next_tokens
            end += 1
        ranges.append((start, end))
        start = end
    return ranges


def _openai_client(
    *,
    dotenv_path: str | None,
    api_key_env: str,
    base_url: str | None,
    organization: str | None,
    project: str | None,
) -> Any:
    if dotenv_path:
        _load_dotenv_file(Path(dotenv_path))
    kwargs: dict[str, Any] = {}
    import os

    api_key = os.environ.get(api_key_env)
    if api_key:
        kwargs["api_key"] = api_key
    if base_url is not None:
        kwargs["base_url"] = base_url
    if organization is not None:
        kwargs["organization"] = organization
    if project is not None:
        kwargs["project"] = project
    return getattr(importlib.import_module("openai"), "OpenAI")(**kwargs)


def _download_openai_file(client: Any, file_id: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp")
    if tmp_path.exists():
        tmp_path.unlink()
    streaming = getattr(getattr(client.files, "with_streaming_response", None), "content", None)
    if callable(streaming):
        with streaming(file_id) as response:
            response.stream_to_file(tmp_path)
        tmp_path.replace(path)
        return
    content = client.files.content(file_id)
    write_to_file = getattr(content, "write_to_file", None)
    if callable(write_to_file):
        write_to_file(tmp_path)
        tmp_path.replace(path)
        return
    data = getattr(content, "content", None)
    if isinstance(data, bytes):
        tmp_path.write_bytes(data)
        tmp_path.replace(path)
        return
    text = getattr(content, "text", None)
    if isinstance(text, str):
        tmp_path.write_text(text, encoding="utf-8")
        tmp_path.replace(path)
        return
    if isinstance(content, bytes):
        tmp_path.write_bytes(content)
        tmp_path.replace(path)
        return
    tmp_path.write_text(str(content), encoding="utf-8")
    tmp_path.replace(path)


def _object_id(value: Any) -> str:
    object_id = getattr(value, "id", None)
    if object_id is None and isinstance(value, dict):
        object_id = value.get("id")
    if object_id is None:
        raise ValueError(f"OpenAI object did not include an id: {value!r}")
    return str(object_id)


def _task_key(task: EvalTask) -> str:
    return f"{task.dataset_id}::{task.split_name}"
