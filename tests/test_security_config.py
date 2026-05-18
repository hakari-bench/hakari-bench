from __future__ import annotations

from pathlib import Path


def test_space_dockerfile_pins_images_and_runs_as_non_root() -> None:
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")

    assert "FROM python:3.12-slim@sha256:" in dockerfile
    assert "COPY --from=ghcr.io/astral-sh/uv:0.9.18@sha256:" in dockerfile
    assert "useradd" in dockerfile
    assert "USER hakari" in dockerfile
