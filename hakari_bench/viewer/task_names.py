from __future__ import annotations


def canonical_task_name(benchmark: str, task_name: str) -> str:
    return task_name


def canonical_split_name(benchmark: str, split_name: str | None) -> str:
    return split_name or ""


def canonical_task_key(*, benchmark: str, dataset_id: str, task_name: str) -> str:
    return f"{benchmark}::{dataset_id}::{task_name}"


def canonical_metric_name(benchmark: str, metric_name: str) -> str:
    return metric_name
