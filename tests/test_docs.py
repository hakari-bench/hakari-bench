from __future__ import annotations

import re
import shlex
from pathlib import Path

from hakari_bench.task_docs import (
    TaskMetadataDocument,
    load_task_metadata,
    task_metadata_json_path,
    validate_task_docs,
)
from hakari_bench.cli import parse_args
from scripts.extract_benchmark_task_examples import build_example_metadata, render_example_table


def test_documented_hakari_bench_commands_parse() -> None:
    docs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            Path("README.md"),
            Path("docs/evaluation_runbook.md"),
            Path("docs/evaluation_policy.md"),
        ]
    )
    commands = [
        command
        for block in re.findall(r"```bash\n(.*?)\n```", docs, flags=re.DOTALL)
        if (command := _normalize_shell_command(block)).startswith("uv run hakari-bench ")
    ]

    assert commands
    for command in commands:
        tokens = shlex.split(command)
        assert tokens[:3] == ["uv", "run", "hakari-bench"]
        parse_args(tokens[3:])


def test_nano_readme_template_documents_fill_requirements() -> None:
    template = Path("docs/NanoREADME.template.md")

    assert template.exists()
    text = template.read_text(encoding="utf-8")
    assert "[HAKARI-Bench](https://github.com/hakari-bench/hakari-bench)" in text
    assert "[NanoBEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir)" in text
    assert "{{SPLIT_STATISTICS_ROWS}}" in text
    assert "{{CANDIDATE_SCORE_ROWS}}" in text
    assert "BM25 nDCG@10 | Dense nDCG@10 | Hybrid nDCG@10" in text
    assert "Dense means `microsoft/harrier-oss-v1-270m`" in text
    assert "Do not include this checklist in the actual dataset README." in text
    assert "- [ ] every config lists the same Nano splits" in text


def test_task_metadata_schema_parses_yaml_boolean_language() -> None:
    metadata = load_task_metadata(Path("task_docs/docs/NanoMTEB-Scandinavian/nor_quad.md"))

    assert metadata.language == "no"


def test_task_metadata_prefers_external_json(tmp_path: Path) -> None:
    docs_root = tmp_path / "docs"
    metadata_root = tmp_path / "metadata"
    doc_path = docs_root / "NanoMIRACL" / "ja.md"
    doc_path.parent.mkdir(parents=True)
    doc_path.write_text("# NanoMIRACL / ja\n", encoding="utf-8")

    source_metadata = load_task_metadata(Path("task_docs/docs/NanoMIRACL/ja.md"))
    updated_metadata = source_metadata.model_copy(update={"document_path": doc_path.as_posix()})
    document = TaskMetadataDocument(task_metadata=updated_metadata)
    metadata_path = task_metadata_json_path(
        doc_path,
        docs_root=docs_root,
        metadata_root=metadata_root,
    )
    metadata_path.parent.mkdir(parents=True)
    metadata_path.write_text(document.model_dump_json(indent=2) + "\n", encoding="utf-8")

    metadata, issues = validate_task_docs([doc_path], docs_root=docs_root, metadata_root=metadata_root)

    assert not issues
    assert [item.task_name for item in metadata] == ["ja"]


def test_task_metadata_examples_store_truncated_text_and_full_lengths() -> None:
    source_metadata = load_task_metadata(Path("task_docs/docs/NanoMIRACL/ja.md"))
    payload = source_metadata.model_dump()
    payload["examples"] = [
        {
            "query_id": "q1",
            "document_id": "d1",
            "query": {
                "text": "short query",
                "full_chars": 11,
                "limit_chars": 500,
                "truncated": False,
            },
            "positive_document": {
                "text": "long document preview",
                "full_chars": 2200,
                "limit_chars": 1000,
                "truncated": True,
            },
        }
    ]

    document = TaskMetadataDocument.model_validate({"task_metadata": payload})

    assert document.task_metadata.examples is not None
    example = document.task_metadata.examples[0]
    assert example.query.text == "short query"
    assert example.query.full_chars == 11
    assert example.query.limit_chars == 500
    assert not example.query.truncated
    assert example.positive_document.text == "long document preview"
    assert example.positive_document.full_chars == 2200
    assert example.positive_document.limit_chars == 1000
    assert example.positive_document.truncated


def test_task_metadata_references_require_valid_source_confidence() -> None:
    source_metadata = load_task_metadata(Path("task_docs/docs/NanoMIRACL/ja.md"))
    payload = source_metadata.model_dump()
    payload["references"] = [
        {
            "title": "Unchecked Source",
            "url": "https://example.com/source",
            "is_paper": False,
            "source_confidence": "unchecked",
        }
    ]

    metadata, issues = validate_task_docs()
    assert not issues

    try:
        TaskMetadataDocument.model_validate({"task_metadata": payload})
    except ValueError as exc:
        assert "source_confidence has invalid label 'unchecked'" in str(exc)
    else:
        raise AssertionError("invalid source_confidence label should fail validation")


def test_build_example_metadata_uses_separate_query_and_document_limits() -> None:
    examples = build_example_metadata(
        queries=[{"_id": "q1", "text": "query " + "x" * 520}],
        corpus=[{"_id": "d1", "text": "document " + "y" * 1040}],
        qrels=[{"query-id": "q1", "corpus-id": "d1", "score": 1}],
        sample_size=3,
        seed=42,
        query_text_limit=500,
        document_text_limit=1000,
    )

    assert len(examples) == 1
    assert examples[0]["query_id"] == "q1"
    assert examples[0]["document_id"] == "d1"
    assert examples[0]["query"]["full_chars"] == 526
    assert examples[0]["query"]["limit_chars"] == 500
    assert examples[0]["query"]["truncated"] is True
    assert len(examples[0]["query"]["text"]) == 500
    assert examples[0]["positive_document"]["full_chars"] == 1049
    assert examples[0]["positive_document"]["limit_chars"] == 1000
    assert examples[0]["positive_document"]["truncated"] is True
    assert len(examples[0]["positive_document"]["text"]) == 1000

    table = render_example_table(examples)

    assert "| Query | Positive document |" in table
    assert "... [500 / 526 chars]" in table
    assert "... [1,000 / 1,049 chars]" in table


def test_task_docs_metadata_validate() -> None:
    metadata, issues = validate_task_docs()

    assert not issues
    assert len(metadata) > 500
    for item in metadata:
        assert item.examples is not None, item.document_path
        assert len(item.examples) == 3, item.document_path
        assert item.example_count == 3, item.document_path
        for example in item.examples:
            assert example.query_id
            assert example.document_id
            assert len(example.query.text) <= example.query.limit_chars
            assert len(example.positive_document.text) <= example.positive_document.limit_chars
            assert example.query.limit_chars == 500
            assert example.positive_document.limit_chars == 1000


def _normalize_shell_command(block: str) -> str:
    return " ".join(line.rstrip("\\").strip() for line in block.splitlines()).strip()
