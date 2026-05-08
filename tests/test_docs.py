from __future__ import annotations

import re
import shlex
from pathlib import Path

from hakari_bench.cli import parse_args


def test_documented_hakari_bench_commands_parse() -> None:
    docs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            Path("README.md"),
            Path("docs/benchmark_evaluation.md"),
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
    assert "[HAKARI-Bench](https://github.com/hotchpotch/hakari-bench)" in text
    assert "[NanoBEIR](https://huggingface.co/blog/sionic-ai/eval-sionic-nano-beir)" in text
    assert "{{SPLIT_STATISTICS_ROWS}}" in text
    assert "{{BM25_SCORE_ROWS}}" in text
    assert "Do not include this checklist in the actual dataset README." in text
    assert "- [ ] every config lists the same Nano splits" in text


def _normalize_shell_command(block: str) -> str:
    return " ".join(line.rstrip("\\").strip() for line in block.splitlines()).strip()
