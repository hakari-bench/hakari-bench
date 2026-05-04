from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from hakari_bench.datasets import DatasetRegistry, resolve_dataset_splits
from hakari_bench.metadata import text_stats


StatsByTask = dict[tuple[str, str], dict[str, dict[str, int | float]]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Update query/document character statistics in dataset YAML metadata.")
    parser.add_argument("--config-root", type=Path, default=Path("config"))
    parser.add_argument("--dataset", default=None, help="Optional dataset name or id to update.")
    parser.add_argument("--task", default=None, help="Optional split/task name to update.")
    parser.add_argument("--dataset-revision", default=None)
    args = parser.parse_args()

    registry = DatasetRegistry.load_from_root(args.config_root)
    datasets = [registry.get_dataset(args.dataset)] if args.dataset else sorted(
        {id(dataset): dataset for dataset in registry._datasets_by_key.values()}.values(),
        key=lambda item: item.name,
    )
    stats: StatsByTask = {}
    for dataset in datasets:
        split_names = resolve_dataset_splits(dataset)
        for split_name in split_names:
            task_name = _task_name_for_split(dataset, split_name)
            if args.task and args.task not in {split_name, task_name}:
                continue
            try:
                stats[(dataset.dataset_id, split_name)] = load_text_stats(
                    dataset_id=dataset.dataset_id,
                    corpus_config=dataset.corpus_config,
                    queries_config=dataset.queries_config,
                    split_name=split_name,
                    revision=args.dataset_revision,
                )
            except Exception as exc:  # pragma: no cover - exercised manually against remote datasets
                print(f"warning: failed to load {dataset.dataset_id}/{split_name}: {type(exc).__name__}: {exc}")

    for path in sorted((args.config_root / "datasets").glob("*.yaml")):
        update_stats_in_file(path, stats)
    for path in sorted((args.config_root / "dataset_collections").glob("*.yaml")):
        update_stats_in_file(path, stats)


def load_text_stats(
    *,
    dataset_id: str,
    corpus_config: str,
    queries_config: str,
    split_name: str,
    revision: str | None,
) -> dict[str, dict[str, int | float]]:
    from datasets import load_dataset

    queries = load_dataset(dataset_id, queries_config, split=split_name, revision=revision)
    corpus = load_dataset(dataset_id, corpus_config, split=split_name, revision=revision)
    return {
        "query_text_stats": text_stats([str(text) for text in queries["text"] if str(text)]),
        "document_text_stats": text_stats([str(text) for text in corpus["text"] if str(text)]),
    }


def update_stats_in_file(path: Path, stats: StatsByTask) -> bool:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return False
    changed = _update_stats_for_mapping(data, stats)
    raw_datasets = data.get("datasets")
    if isinstance(raw_datasets, list):
        for raw_dataset in raw_datasets:
            if isinstance(raw_dataset, dict):
                changed = _update_stats_for_mapping(raw_dataset, stats) or changed
    if changed:
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return changed


def _update_stats_for_mapping(data: dict[str, Any], stats: StatsByTask) -> bool:
    dataset_id = str(data.get("dataset_id", ""))
    task_metadata = data.get("task_metadata")
    if not isinstance(task_metadata, dict):
        return False
    changed = False
    for task_name, metadata in task_metadata.items():
        if not isinstance(metadata, dict):
            continue
        task_stats = stats.get((dataset_id, str(task_name)))
        if task_stats is None:
            continue
        metadata.update(task_stats)
        changed = True
    return changed


def _task_name_for_split(dataset: Any, split_name: str) -> str:
    mapping = dataset.effective_split_mapping
    if mapping is not None:
        for logical_name, mapped_split in mapping.items():
            if split_name == mapped_split:
                return logical_name
    return split_name


if __name__ == "__main__":
    main()
