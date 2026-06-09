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
    assert "[HAKARI-bench](https://github.com/hakari-bench/hakari-bench)" in text
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


def test_task_docs_metadata_validate() -> None:
    metadata, issues = validate_task_docs()

    assert not issues
    assert len(metadata) > 500


def _normalize_shell_command(block: str) -> str:
    return " ".join(line.rstrip("\\").strip() for line in block.splitlines()).strip()
