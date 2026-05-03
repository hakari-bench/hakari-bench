from __future__ import annotations

from pathlib import Path
from statistics import mean, median
from typing import Any

from nano_ir_benchmark.datasets import DatasetRegistry


def text_stats(texts: list[str]) -> dict[str, int | float]:
    lengths = [len(text) for text in texts]
    if not lengths:
        return {
            "count": 0,
            "min_chars": 0,
            "max_chars": 0,
            "mean_chars": 0.0,
            "median_chars": 0.0,
        }
    return {
        "count": len(lengths),
        "min_chars": min(lengths),
        "max_chars": max(lengths),
        "mean_chars": float(mean(lengths)),
        "median_chars": float(median(lengths)),
    }


def export_citation_catalog(*, config_root: Path | None = None) -> dict[str, Any]:
    registry = _load_registry(config_root)
    datasets = sorted({id(dataset): dataset for dataset in registry._datasets_by_key.values()}.values(), key=lambda item: item.name)
    payload: dict[str, Any] = {"datasets": []}
    for dataset in datasets:
        tasks: list[dict[str, Any]] = []
        split_names = dataset.splits or list((dataset.effective_split_mapping or {}).values())
        if not split_names:
            split_names = sorted((dataset.task_metadata or {}).keys())
        for split_name in split_names:
            task_name = _task_name(dataset, split_name)
            metadata = dataset.metadata_for_task(split_name=split_name, task_name=task_name)
            tasks.append(
                {
                    "split_name": split_name,
                    "task_name": task_name,
                    "language": metadata.get("language"),
                    "category": metadata.get("category"),
                    "short_description": metadata.get("short_description"),
                    "references": metadata.get("references", []),
                    "citation_keys": metadata.get("citation_keys", []),
                    "citations_latex": [_latex_cite(key) for key in metadata.get("citation_keys", [])],
                }
            )
        payload["datasets"].append(
            {
                "name": dataset.name,
                "dataset_id": dataset.dataset_id,
                "metadata": dataset.metadata or {},
                "tasks": tasks,
            }
        )
    return payload


def export_bibtex(*, config_root: Path | None = None) -> str:
    registry = _load_registry(config_root)
    entries: dict[str, str] = {}
    datasets = sorted({id(dataset): dataset for dataset in registry._datasets_by_key.values()}.values(), key=lambda item: item.name)
    for dataset in datasets:
        _collect_bibtex(entries, dataset.metadata or {})
        for metadata in (dataset.task_metadata or {}).values():
            _collect_bibtex(entries, metadata)
    return "\n\n".join(entries[key].strip() for key in sorted(entries)) + ("\n" if entries else "")


def export_latex_citations(*, config_root: Path | None = None) -> str:
    catalog = export_citation_catalog(config_root=config_root)
    lines: list[str] = []
    for dataset in catalog["datasets"]:
        for task in dataset["tasks"]:
            citations = task["citations_latex"]
            if citations:
                lines.append(f"{dataset['name']}/{task['task_name']}: {', '.join(citations)}")
    return "\n".join(lines) + ("\n" if lines else "")


def _load_registry(config_root: Path | None) -> DatasetRegistry:
    return DatasetRegistry.load_from_root(config_root) if config_root is not None else DatasetRegistry.load_builtin()


def _task_name(dataset: Any, split_name: str) -> str:
    mapping = dataset.effective_split_mapping
    if mapping is not None:
        for logical_name, mapped_split in mapping.items():
            if split_name == mapped_split:
                return logical_name
    return split_name


def _latex_cite(key: str) -> str:
    return f"\\cite{{{key}}}"


def _collect_bibtex(entries: dict[str, str], metadata: dict[str, Any]) -> None:
    bibtex = metadata.get("bibtex")
    keys = metadata.get("citation_keys") or []
    if isinstance(bibtex, str) and bibtex.strip():
        key = str(keys[0]) if keys else bibtex.split("{", maxsplit=1)[-1].split(",", maxsplit=1)[0]
        entries.setdefault(key, bibtex)
