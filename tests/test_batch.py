from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from hakari_bench.batch import (
    BatchMetadata,
    DEFAULT_OPENAI_BATCH_MAX_INPUT_FILE_BYTES,
    PrecomputedDenseEmbeddingModel,
    cleanup_batch_download_files,
    collect_gemini_batch_task_embeddings,
    collect_openai_batch_embeddings,
    collect_openai_batch_task_embeddings,
    _download_openai_file,
    write_gemini_embedding_task_batch_files,
    register_openai_embedding_batch,
    write_openai_embedding_task_batch_files,
    write_openai_embedding_batch_files,
)
from hakari_bench.cli import parse_args
from hakari_bench.datasets import EvalTask, NanoDatasetSpec
from hakari_bench.evaluation import LoadedIrDataset


def _task() -> EvalTask:
    return EvalTask(
        dataset=NanoDatasetSpec(
            name="TinyNano",
            dataset_id="tiny/nano",
            corpus_config="corpus",
            queries_config="queries",
            qrels_config="qrels",
        ),
        split_name="TinyTask",
        task_name="tiny_task",
    )


def _dataset() -> LoadedIrDataset:
    return LoadedIrDataset(
        queries={"q1": "query one", "q2": "query two"},
        corpus={"d1": "document one", "d2": "document two", "d3": "document three"},
        qrels={"q1": {"d1"}, "q2": {"d2"}},
        candidates=None,
        evaluator_name="TinyNano_tiny_task",
    )


class _WhitespaceEncoding:
    def encode(self, text: str, **_: object) -> list[int]:
        return list(range(len(text.split())))

    def decode(self, tokens: list[int]) -> str:
        return " ".join(f"tok{token}" for token in tokens)


class _PassthroughGeminiTokenizer:
    def encode(self, text: str) -> list[str]:
        return list(text)

    def decode(self, tokens: list[str]) -> str:
        return "".join(tokens)


def _patch_gemini_tokenizer(monkeypatch) -> None:
    monkeypatch.setattr("hakari_bench.models._gemini_embedding_tokenizer", lambda: _PassthroughGeminiTokenizer())


def test_download_openai_file_retries_and_removes_partial_tmp(tmp_path: Path, monkeypatch) -> None:
    sleeps: list[float] = []

    class _StreamingResponse:
        calls = 0

        def __enter__(self):
            return self

        def __exit__(self, *_exc: object) -> None:
            return None

        def stream_to_file(self, path: Path) -> None:
            type(self).calls += 1
            if type(self).calls == 1:
                path.write_text("partial", encoding="utf-8")
                raise RuntimeError("temporary gateway timeout")
            path.write_text("complete", encoding="utf-8")

    class _StreamingFiles:
        def content(self, _file_id: str) -> _StreamingResponse:
            return _StreamingResponse()

    class _Files:
        with_streaming_response = _StreamingFiles()

    class _Client:
        files = _Files()

    monkeypatch.setattr("hakari_bench.batch.time.sleep", lambda seconds: sleeps.append(seconds))

    output_path = tmp_path / "output.jsonl"
    _download_openai_file(_Client(), "file-1", output_path)

    assert output_path.read_text(encoding="utf-8") == "complete"
    assert not output_path.with_name("output.jsonl.tmp").exists()
    assert sleeps == [5.0]


def test_write_openai_embedding_batch_files_links_custom_ids_to_task_inputs(tmp_path: Path) -> None:
    metadata = write_openai_embedding_batch_files(
        target="tiny-openai",
        workspace_root=tmp_path,
        model="text-embedding-3-small",
        tasks=[_task()],
        dataset_loader=lambda _task: _dataset(),
        encoding=_WhitespaceEncoding(),
        batch_size=2,
        max_input_tokens=8100,
        max_request_tokens=100,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
    )

    assert metadata.target == "tiny-openai"
    assert metadata.request_count == 3
    assert metadata.embedding_input_count == 5
    assert metadata.input_file_path.exists()
    assert metadata.metadata_path.exists()

    lines = [json.loads(line) for line in metadata.input_file_path.read_text(encoding="utf-8").splitlines()]
    assert [line["custom_id"] for line in lines] == [
        "TinyNano__TinyTask__query__000000",
        "TinyNano__TinyTask__document__000000",
        "TinyNano__TinyTask__document__000002",
    ]
    assert lines[0]["url"] == "/v1/embeddings"
    assert lines[0]["body"]["model"] == "text-embedding-3-small"
    assert lines[0]["body"]["input"] == ["query one", "query two"]

    stored = BatchMetadata.from_path(metadata.metadata_path)
    assert stored.requests[0]["ids"] == ["q1", "q2"]
    assert stored.tasks[0]["task_name"] == "tiny_task"


def test_collect_openai_batch_embeddings_restores_output_by_custom_id(tmp_path: Path) -> None:
    metadata = write_openai_embedding_batch_files(
        target="tiny-openai",
        workspace_root=tmp_path,
        model="text-embedding-3-small",
        tasks=[_task()],
        dataset_loader=lambda _task: _dataset(),
        encoding=_WhitespaceEncoding(),
        batch_size=2,
        max_input_tokens=8100,
        max_request_tokens=100,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
    )
    output_path = metadata.workspace_path / "output.jsonl"
    output_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "custom_id": "TinyNano__TinyTask__document__000002",
                        "response": {
                            "status_code": 200,
                            "body": {"data": [{"index": 0, "embedding": [0.0, 0.0, 1.0]}]},
                        },
                    }
                ),
                json.dumps(
                    {
                        "custom_id": "TinyNano__TinyTask__query__000000",
                        "response": {
                            "status_code": 200,
                            "body": {
                                "data": [
                                    {"index": 1, "embedding": [0.0, 1.0, 0.0]},
                                    {"index": 0, "embedding": [1.0, 0.0, 0.0]},
                                ]
                            },
                        },
                    }
                ),
                json.dumps(
                    {
                        "custom_id": "TinyNano__TinyTask__document__000000",
                        "response": {
                            "status_code": 200,
                            "body": {
                                "data": [
                                    {"index": 0, "embedding": [1.0, 0.0, 0.0]},
                                    {"index": 1, "embedding": [0.0, 1.0, 0.0]},
                                ]
                            },
                        },
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    embeddings = collect_openai_batch_embeddings(metadata=metadata, output_path=output_path)

    task_key = "tiny/nano::TinyTask"
    assert embeddings[task_key]["query_ids"] == ["q1", "q2"]
    assert embeddings[task_key]["corpus_ids"] == ["d1", "d2", "d3"]
    assert embeddings[task_key]["query_embeddings"].tolist() == [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    assert embeddings[task_key]["corpus_embeddings"].tolist() == [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]


def test_write_openai_embedding_task_batch_files_splits_large_task(tmp_path: Path) -> None:
    batches = write_openai_embedding_task_batch_files(
        target="tiny-openai",
        workspace_root=tmp_path,
        model="text-embedding-3-small",
        task=_task(),
        dataset=_dataset(),
        encoding=_WhitespaceEncoding(),
        batch_size=2,
        max_input_tokens=8100,
        max_request_tokens=100,
        max_embedding_inputs=3,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
    )

    assert [metadata.target for metadata in batches] == [
        "tiny-openai__TinyNano__TinyTask__part000",
        "tiny-openai__TinyNano__TinyTask__part001",
    ]
    assert [metadata.embedding_input_count for metadata in batches] == [2, 3]
    assert all(len(metadata.tasks) == 1 for metadata in batches)
    custom_ids = [request["custom_id"] for metadata in batches for request in metadata.requests]
    assert custom_ids == [
        "TinyNano__TinyTask__query__000000",
        "TinyNano__TinyTask__document__000000",
        "TinyNano__TinyTask__document__000002",
    ]


def test_write_openai_embedding_task_batch_files_splits_large_task_by_input_file_bytes(tmp_path: Path) -> None:
    dataset = LoadedIrDataset(
        queries={"q1": "query one"},
        corpus={
            "d1": "document " + ("alpha " * 20),
            "d2": "document " + ("beta " * 20),
            "d3": "document " + ("gamma " * 20),
        },
        qrels={"q1": {"d1"}},
        candidates=None,
        evaluator_name="TinyNano_tiny_task",
    )

    batches = write_openai_embedding_task_batch_files(
        target="tiny-openai",
        workspace_root=tmp_path,
        model="text-embedding-3-small",
        task=_task(),
        dataset=dataset,
        encoding=_WhitespaceEncoding(),
        batch_size=1,
        max_input_tokens=8100,
        max_request_tokens=100,
        max_embedding_inputs=100,
        max_input_file_bytes=700,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
    )

    assert len(batches) > 1
    assert sum(metadata.embedding_input_count for metadata in batches) == 4
    assert all(metadata.input_file_path.stat().st_size <= 700 for metadata in batches)
    assert [request["custom_id"] for metadata in batches for request in metadata.requests] == [
        "TinyNano__TinyTask__query__000000",
        "TinyNano__TinyTask__document__000000",
        "TinyNano__TinyTask__document__000001",
        "TinyNano__TinyTask__document__000002",
    ]


def test_write_openai_embedding_task_batch_files_rejects_single_request_over_input_file_bytes(tmp_path: Path) -> None:
    dataset = LoadedIrDataset(
        queries={"q1": "query one"},
        corpus={"d1": "document " + ("alpha " * 100)},
        qrels={"q1": {"d1"}},
        candidates=None,
        evaluator_name="TinyNano_tiny_task",
    )

    try:
        write_openai_embedding_task_batch_files(
            target="tiny-openai",
            workspace_root=tmp_path,
            model="text-embedding-3-small",
            task=_task(),
            dataset=dataset,
            encoding=_WhitespaceEncoding(),
            batch_size=1,
            max_input_tokens=8100,
            max_request_tokens=100,
            max_embedding_inputs=100,
            max_input_file_bytes=100,
            query_prompt=None,
            document_prompt=None,
            dataset_revision=None,
        )
    except ValueError as exc:
        assert "input file byte limit" in str(exc)
    else:
        raise AssertionError("Expected oversized OpenAI batch request line to be rejected.")


def test_collect_openai_batch_task_embeddings_restores_split_task(tmp_path: Path) -> None:
    batches = write_openai_embedding_task_batch_files(
        target="tiny-openai",
        workspace_root=tmp_path,
        model="text-embedding-3-small",
        task=_task(),
        dataset=_dataset(),
        encoding=_WhitespaceEncoding(),
        batch_size=2,
        max_input_tokens=8100,
        max_request_tokens=100,
        max_embedding_inputs=3,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
    )
    batches[0].output_file_path.write_text(
        json.dumps(
            {
                "custom_id": "TinyNano__TinyTask__query__000000",
                "response": {
                    "status_code": 200,
                    "body": {
                        "data": [
                            {"index": 0, "embedding": [1.0, 0.0]},
                            {"index": 1, "embedding": [0.0, 1.0]},
                        ]
                    },
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    batches[1].output_file_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "custom_id": "TinyNano__TinyTask__document__000000",
                        "response": {
                            "status_code": 200,
                            "body": {
                                "data": [
                                    {"index": 0, "embedding": [1.0, 1.0]},
                                    {"index": 1, "embedding": [2.0, 2.0]},
                                ]
                            },
                        },
                    }
                ),
                json.dumps(
                    {
                        "custom_id": "TinyNano__TinyTask__document__000002",
                        "response": {
                            "status_code": 200,
                            "body": {"data": [{"index": 0, "embedding": [3.0, 3.0]}]},
                        },
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    embeddings = collect_openai_batch_task_embeddings(batches)

    task_key = "tiny/nano::TinyTask"
    assert embeddings["task_key"] == task_key
    assert embeddings["query_ids"] == ["q1", "q2"]
    assert embeddings["corpus_ids"] == ["d1", "d2", "d3"]
    assert embeddings["query_embeddings"].tolist() == [[1.0, 0.0], [0.0, 1.0]]
    assert embeddings["corpus_embeddings"].tolist() == [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]


def test_write_gemini_embedding_task_batch_files_writes_gcs_jsonl(tmp_path: Path, monkeypatch) -> None:
    _patch_gemini_tokenizer(monkeypatch)

    batches = write_gemini_embedding_task_batch_files(
        target="tiny-gemini",
        workspace_root=tmp_path,
        model="gemini-embedding-2",
        task=_task(),
        dataset=_dataset(),
        max_input_tokens=8100,
        max_embedding_inputs=3,
        query_prompt="query: ",
        document_prompt="document: ",
        dataset_revision=None,
        project="ml-sandbox-309804",
        location="global",
        api_version="v1",
        gcs_uri_prefix="gs://bucket/hakari",
    )

    assert [metadata.provider for metadata in batches] == ["gemini", "gemini"]
    assert [metadata.embedding_input_count for metadata in batches] == [3, 2]
    first_lines = [json.loads(line) for line in batches[0].input_file_path.read_text(encoding="utf-8").splitlines()]
    assert first_lines == [
        {
            "key": "TinyNano__TinyTask__query__000000",
            "request": {"content": {"parts": [{"text": "query: query one"}]}},
        },
        {
            "key": "TinyNano__TinyTask__query__000001",
            "request": {"content": {"parts": [{"text": "query: query two"}]}},
        },
        {
            "key": "TinyNano__TinyTask__document__000000",
            "request": {"content": {"parts": [{"text": "document: document one"}]}},
        },
    ]
    api = batches[0].api
    assert api is not None
    assert api["gcs_input_uri"] == "gs://bucket/hakari/tiny-gemini__TinyNano__TinyTask__part000/requests.jsonl"
    assert api["gcs_output_uri"] == "gs://bucket/hakari/tiny-gemini__TinyNano__TinyTask__part000/output"


def test_collect_gemini_batch_task_embeddings_restores_split_task(tmp_path: Path, monkeypatch) -> None:
    _patch_gemini_tokenizer(monkeypatch)

    batches = write_gemini_embedding_task_batch_files(
        target="tiny-gemini",
        workspace_root=tmp_path,
        model="gemini-embedding-2",
        task=_task(),
        dataset=_dataset(),
        max_input_tokens=8100,
        max_embedding_inputs=3,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
        project="ml-sandbox-309804",
        location="global",
        api_version="v1",
        gcs_uri_prefix="gs://bucket/hakari",
    )
    batches[0].output_file_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "instance": {"content": "query one", "custom_id": "TinyNano__TinyTask__query__000000"},
                        "predictions": [{"embeddings": {"values": [1.0, 0.0]}}],
                        "status": "",
                    }
                ),
                json.dumps(
                    {
                        "instance": {"content": "query two", "custom_id": "TinyNano__TinyTask__query__000001"},
                        "predictions": [{"embeddings": {"values": [0.0, 1.0]}}],
                        "status": "",
                    }
                ),
                json.dumps(
                    {
                        "instance": {"content": "document one", "custom_id": "TinyNano__TinyTask__document__000000"},
                        "predictions": [{"embeddings": {"values": [1.0, 1.0]}}],
                        "status": "",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    batches[1].output_file_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "instance": {"content": "document two", "custom_id": "TinyNano__TinyTask__document__000001"},
                        "predictions": [{"embeddings": {"values": [2.0, 2.0]}}],
                        "status": "",
                    }
                ),
                json.dumps(
                    {
                        "instance": {"content": "document three", "custom_id": "TinyNano__TinyTask__document__000002"},
                        "predictions": [{"embeddings": {"values": [3.0, 3.0]}}],
                        "status": "",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    embeddings = collect_gemini_batch_task_embeddings(batches)

    assert embeddings["task_key"] == "tiny/nano::TinyTask"
    assert embeddings["query_ids"] == ["q1", "q2"]
    assert embeddings["corpus_ids"] == ["d1", "d2", "d3"]
    assert embeddings["query_embeddings"].tolist() == [[1.0, 0.0], [0.0, 1.0]]
    assert embeddings["corpus_embeddings"].tolist() == [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]


def test_collect_gemini_batch_task_embeddings_accepts_developer_api_output(tmp_path: Path, monkeypatch) -> None:
    _patch_gemini_tokenizer(monkeypatch)

    batches = write_gemini_embedding_task_batch_files(
        target="tiny-gemini",
        workspace_root=tmp_path,
        model="gemini-embedding-2",
        task=_task(),
        dataset=_dataset(),
        max_input_tokens=8100,
        max_embedding_inputs=3,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
        project="ml-sandbox-309804",
        location="global",
        api_version="v1",
        gcs_uri_prefix="gs://bucket/hakari",
    )
    batches[0].output_file_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "key": "TinyNano__TinyTask__query__000000",
                        "response": {"embedding": {"values": [1.0, 0.0]}},
                    }
                ),
                json.dumps(
                    {
                        "key": "TinyNano__TinyTask__query__000001",
                        "response": {"embedding": {"values": [0.0, 1.0]}},
                    }
                ),
                json.dumps(
                    {
                        "key": "TinyNano__TinyTask__document__000000",
                        "response": {"embedding": {"values": [1.0, 1.0]}},
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    batches[1].output_file_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "key": "TinyNano__TinyTask__document__000001",
                        "response": {"embedding": {"values": [2.0, 2.0]}},
                    }
                ),
                json.dumps(
                    {
                        "key": "TinyNano__TinyTask__document__000002",
                        "response": {"embedding": {"values": [3.0, 3.0]}},
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    embeddings = collect_gemini_batch_task_embeddings(batches)

    assert embeddings["query_ids"] == ["q1", "q2"]
    assert embeddings["corpus_ids"] == ["d1", "d2", "d3"]
    assert embeddings["query_embeddings"].tolist() == [[1.0, 0.0], [0.0, 1.0]]
    assert embeddings["corpus_embeddings"].tolist() == [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]


def test_collect_gemini_batch_task_embeddings_uses_retry_output_after_transient_line_error(
    tmp_path: Path, monkeypatch
) -> None:
    _patch_gemini_tokenizer(monkeypatch)

    batches = write_gemini_embedding_task_batch_files(
        target="tiny-gemini",
        workspace_root=tmp_path,
        model="gemini-embedding-2",
        task=_task(),
        dataset=_dataset(),
        max_input_tokens=8100,
        max_embedding_inputs=3,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
        project="ml-sandbox-309804",
        location="global",
        api_version="v1",
        gcs_uri_prefix="gs://bucket/hakari",
    )
    batches[0].output_file_path.write_text(
        "\n".join(
            [
                json.dumps({"key": "TinyNano__TinyTask__query__000000", "response": {"embedding": {"values": [1.0, 0.0]}}}),
                json.dumps({"key": "TinyNano__TinyTask__query__000001", "response": {"embedding": {"values": [0.0, 1.0]}}}),
                json.dumps({"key": "TinyNano__TinyTask__document__000000", "response": {"embedding": {"values": [1.0, 1.0]}}}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    batches[1].output_file_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "key": "TinyNano__TinyTask__document__000001",
                        "response": {"error": {"code": 4, "message": "Deadline expired before operation could complete."}},
                    }
                ),
                json.dumps({"key": "TinyNano__TinyTask__document__000001", "response": {"embedding": {"values": [2.0, 2.0]}}}),
                json.dumps({"key": "TinyNano__TinyTask__document__000002", "response": {"embedding": {"values": [3.0, 3.0]}}}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    embeddings = collect_gemini_batch_task_embeddings(batches)

    assert embeddings["corpus_embeddings"].tolist() == [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]


def test_cleanup_batch_download_files_removes_large_provider_outputs(tmp_path: Path) -> None:
    metadata = write_openai_embedding_batch_files(
        target="tiny-openai",
        workspace_root=tmp_path,
        model="text-embedding-3-small",
        tasks=[_task()],
        dataset_loader=lambda _task: _dataset(),
        encoding=_WhitespaceEncoding(),
        batch_size=2,
        max_input_tokens=8100,
        max_request_tokens=100,
        query_prompt=None,
        document_prompt=None,
        dataset_revision=None,
    )
    metadata.output_file_path.write_text("{}\n", encoding="utf-8")
    metadata.error_file_path.write_text("{}\n", encoding="utf-8")
    tmp_output = metadata.output_file_path.with_name(f"{metadata.output_file_path.name}.tmp")
    tmp_output.write_text("partial", encoding="utf-8")
    gemini_output = metadata.output_file_path.parent / "gemini_output"
    gemini_output.mkdir()
    (gemini_output / "predictions.jsonl").write_text("{}\n", encoding="utf-8")

    removed = cleanup_batch_download_files(metadata)

    assert sorted(path.name for path in removed) == ["errors.jsonl", "gemini_output", "output.jsonl", "output.jsonl.tmp"]
    assert not metadata.output_file_path.exists()
    assert not metadata.error_file_path.exists()
    assert not tmp_output.exists()
    assert not gemini_output.exists()


def test_register_openai_embedding_batch_enforces_embedding_input_limit(
    monkeypatch,
    tmp_path: Path,
) -> None:
    class FakeAdapter:
        def __init__(self, **_: object) -> None:
            pass

        def _tokenizer(self) -> _WhitespaceEncoding:
            return _WhitespaceEncoding()

    def fail_openai_client(**_: object) -> object:
        raise AssertionError("OpenAI client should not be created after local limit failure.")

    monkeypatch.setattr("hakari_bench.batch.OpenAIEmbeddingAdapter", FakeAdapter)
    monkeypatch.setattr("hakari_bench.batch._openai_client", fail_openai_client)

    try:
        register_openai_embedding_batch(
            target="tiny-openai",
            workspace_root=tmp_path,
            model="text-embedding-3-small",
            tasks=[_task()],
            dataset_loader=lambda _task: _dataset(),
            batch_size=2,
            max_input_tokens=8100,
            max_request_tokens=100,
            max_embedding_inputs=4,
            query_prompt=None,
            document_prompt=None,
            dataset_revision=None,
            dotenv_path=None,
            api_key_env="OPENAI_API_KEY",
            base_url=None,
            organization=None,
            project=None,
        )
    except ValueError as exc:
        assert "exceeding the 4 input limit" in str(exc)
    else:
        raise AssertionError("Expected max_embedding_inputs to be enforced.")


def test_precomputed_dense_embedding_model_returns_role_embeddings() -> None:
    model = PrecomputedDenseEmbeddingModel(
        query_embeddings=np.asarray([[1.0, 0.0]], dtype=np.float32),
        corpus_embeddings=np.asarray([[0.0, 1.0], [1.0, 1.0]], dtype=np.float32),
        model_name="text-embedding-3-small",
        max_seq_length=8100,
        backend_metadata={"provider": "openai"},
    )

    assert model.similarity_fn_name == "cosine"
    assert model.encode_query(["q"]).tolist() == [[1.0, 0.0]]
    assert model.encode_document(["d1", "d2"]).tolist() == [[0.0, 1.0], [1.0, 1.0]]
    assert model.metadata()["backend_library"] == "batch-precomputed"
    assert model.metadata()["provider"] == "openai"


def test_parse_args_accepts_dense_batch_commands() -> None:
    register = parse_args(
        [
            "batch",
            "dense",
            "register",
            "--provider",
            "openai",
            "--target",
            "openai-small-nanobeir",
            "--model",
            "text-embedding-3-small",
            "--dataset",
            "hakari-bench/NanoBEIR-ja",
        ]
    )
    assert register.command == "batch"
    assert register.batch_model_type == "dense"
    assert register.batch_action == "register"
    assert register.provider == "openai"
    assert register.target == "openai-small-nanobeir"
    assert register.max_input_file_bytes == DEFAULT_OPENAI_BATCH_MAX_INPUT_FILE_BYTES

    register_with_file_limit = parse_args(
        [
            "batch",
            "dense",
            "register",
            "--provider",
            "openai",
            "--target",
            "openai-small-nanobeir",
            "--model",
            "text-embedding-3-small",
            "--dataset",
            "hakari-bench/NanoBEIR-ja",
            "--max-input-file-bytes",
            "1000000",
        ]
    )
    assert register_with_file_limit.max_input_file_bytes == 1_000_000

    gemini_register = parse_args(
        [
            "batch",
            "dense",
            "register",
            "--provider",
            "gemini",
            "--target",
            "gemini-nanobeir",
            "--model",
            "gemini-embedding-2",
            "--model-alias",
            "google/gemini-embedding-2",
            "--dataset",
            "hakari-bench/NanoBEIR-en",
            "--gemini-project",
            "ml-sandbox-309804",
            "--gcs-uri-prefix",
            "gs://bucket/hakari",
        ]
    )
    assert gemini_register.provider == "gemini"
    assert gemini_register.model_alias == "google/gemini-embedding-2"
    assert gemini_register.gemini_location == "global"
    assert gemini_register.gcs_uri_prefix == "gs://bucket/hakari"

    materialize = parse_args(
        [
            "batch",
            "dense",
            "process",
            "--target",
            "openai-small-nanobeir",
            "--embedding-variant",
            "truncate:256",
            "--keep-downloaded-batch-files",
        ]
    )
    assert materialize.batch_action == "process"
    assert materialize.keep_downloaded_batch_files is True
    assert [variant["name"] for variant in materialize.embedding_variants[:2]] == [
        "truncate_dim_256",
        "int8",
    ]
