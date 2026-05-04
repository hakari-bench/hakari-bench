from __future__ import annotations

import re
import shlex
from pathlib import Path

from hakari_bench.cli import parse_args


def test_readme_hakari_bench_commands_parse() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    commands = [
        command
        for block in re.findall(r"```bash\n(.*?)\n```", readme, flags=re.DOTALL)
        if (command := _normalize_shell_command(block)).startswith("uv run hakari-bench ")
    ]

    assert commands
    for command in commands:
        tokens = shlex.split(command)
        assert tokens[:3] == ["uv", "run", "hakari-bench"]
        parse_args(tokens[3:])


def _normalize_shell_command(block: str) -> str:
    return " ".join(line.rstrip("\\").strip() for line in block.splitlines()).strip()
