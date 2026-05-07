from __future__ import annotations

import argparse
import importlib
from collections import Counter
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

import yaml

from hakari_bench.datasets import DatasetRegistry, resolve_dataset_splits


DetectionByTask = dict[tuple[str, str], dict[str, Any]]
Detector = Callable[[str], Any]


DEFAULT_MIN_LANGUAGE_RATIO = 0.005
DEFAULT_MAIN_LANGUAGE_RATIO = 0.10


def main() -> None:
    parser = argparse.ArgumentParser(description="Update query/document language detection in dataset YAML metadata.")
    parser.add_argument("--config-root", type=Path, default=Path("config"))
    parser.add_argument("--dataset", default=None, help="Optional dataset name or id to update.")
    parser.add_argument("--task", default=None, help="Optional split/task name to update.")
    parser.add_argument("--dataset-revision", default=None)
    parser.add_argument("--min-language-ratio", type=float, default=DEFAULT_MIN_LANGUAGE_RATIO)
    parser.add_argument("--main-language-ratio", type=float, default=DEFAULT_MAIN_LANGUAGE_RATIO)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    registry = DatasetRegistry.load_from_root(args.config_root)
    datasets = [registry.get_dataset(args.dataset)] if args.dataset else sorted(
        {id(dataset): dataset for dataset in registry._datasets_by_key.values()}.values(),
        key=lambda item: item.name,
    )
    detections: DetectionByTask = {}
    for dataset in datasets:
        split_names = resolve_dataset_splits(dataset)
        for split_name in split_names:
            task_name = _task_name_for_split(dataset, split_name)
            if args.task and args.task not in {split_name, task_name}:
                continue
            try:
                detection = load_language_detection(
                    dataset_id=dataset.dataset_id,
                    corpus_config=dataset.corpus_config,
                    queries_config=dataset.queries_config,
                    split_name=split_name,
                    revision=args.dataset_revision,
                    min_language_ratio=args.min_language_ratio,
                    main_language_ratio=args.main_language_ratio,
                )
            except Exception as exc:  # pragma: no cover - exercised manually against remote datasets
                print(f"warning: failed to load {dataset.dataset_id}/{split_name}: {type(exc).__name__}: {exc}")
                continue
            detections[(dataset.dataset_id, task_name)] = detection
            print(
                f"{dataset.name}/{task_name}: languages={detection['languages']} "
                f"query={detection['language_detection']['query']['languages']} "
                f"document={detection['language_detection']['document']['languages']}",
                flush=True,
            )

    if args.dry_run:
        return

    for path in sorted((args.config_root / "datasets").glob("*.yaml")):
        update_languages_in_file(path, detections)
    for path in sorted((args.config_root / "dataset_collections").glob("*.yaml")):
        update_languages_in_file(path, detections)


def load_language_detection(
    *,
    dataset_id: str,
    corpus_config: str,
    queries_config: str,
    split_name: str,
    revision: str | None,
    min_language_ratio: float = DEFAULT_MIN_LANGUAGE_RATIO,
    main_language_ratio: float = DEFAULT_MAIN_LANGUAGE_RATIO,
) -> dict[str, Any]:
    from datasets import load_dataset

    queries = load_dataset(dataset_id, queries_config, split=split_name, revision=revision)
    corpus = load_dataset(dataset_id, corpus_config, split=split_name, revision=revision)
    return build_language_detection_metadata(
        query_texts=[str(text) for text in queries["text"] if str(text)],
        document_texts=[str(text) for text in corpus["text"] if str(text)],
        min_language_ratio=min_language_ratio,
        main_language_ratio=main_language_ratio,
    )


def build_language_detection_metadata(
    *,
    query_texts: Iterable[str],
    document_texts: Iterable[str],
    detector: Detector | None = None,
    min_language_ratio: float = DEFAULT_MIN_LANGUAGE_RATIO,
    main_language_ratio: float = DEFAULT_MAIN_LANGUAGE_RATIO,
) -> dict[str, Any]:
    query_detection = detect_language_distribution(
        query_texts,
        detector=detector,
        min_language_ratio=min_language_ratio,
    )
    document_detection = detect_language_distribution(
        document_texts,
        detector=detector,
        min_language_ratio=min_language_ratio,
    )
    languages = select_main_languages(
        query_detection["ratios"],
        document_detection["ratios"],
        main_language_ratio=main_language_ratio,
    )
    return {
        "languages": languages,
        "language_detection": {
            "detector": "fast-langdetect",
            "min_language_percent": round(min_language_ratio * 100, 3),
            "main_language_percent": round(main_language_ratio * 100, 3),
            "query": _language_detection_payload(query_detection),
            "document": _language_detection_payload(document_detection),
        },
    }


def detect_language_distribution(
    texts: Iterable[str],
    *,
    detector: Detector | None = None,
    min_language_ratio: float = DEFAULT_MIN_LANGUAGE_RATIO,
) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    total = 0
    detect = detector or _detect_language
    for text in texts:
        normalized = str(text).strip()
        if not normalized:
            continue
        total += 1
        language, _score = _normalize_detect_result(_safe_detect(detect, normalized))
        counts[language or "unknown"] += 1

    if total == 0:
        return {"sample_count": 0, "counts": {"unknown": 0}, "ratios": {"unknown": 1.0}}

    ratios = {language: count / total for language, count in counts.items()}
    filtered = {
        language: ratio
        for language, ratio in sorted(ratios.items(), key=lambda item: (-item[1], item[0]))
        if ratio >= min_language_ratio
    }
    if not filtered:
        filtered = {"unknown": 1.0}
    return {
        "sample_count": total,
        "counts": dict(counts),
        "ratios": filtered,
    }


def select_main_languages(
    query_ratios: dict[str, float],
    document_ratios: dict[str, float],
    *,
    main_language_ratio: float = DEFAULT_MAIN_LANGUAGE_RATIO,
) -> list[str]:
    languages = set(query_ratios) | set(document_ratios)
    selected = [
        language
        for language in languages
        if max(query_ratios.get(language, 0.0), document_ratios.get(language, 0.0)) >= main_language_ratio
    ]
    if not selected:
        return ["unknown"]
    return sorted(
        selected,
        key=lambda language: (
            -max(query_ratios.get(language, 0.0), document_ratios.get(language, 0.0)),
            -document_ratios.get(language, 0.0),
            -query_ratios.get(language, 0.0),
            language,
        ),
    )


def update_languages_in_file(path: Path, detections: DetectionByTask) -> bool:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return False
    changed = _update_languages_for_mapping(data, detections)
    raw_datasets = data.get("datasets")
    if isinstance(raw_datasets, list):
        for raw_dataset in raw_datasets:
            if isinstance(raw_dataset, dict):
                changed = _update_languages_for_mapping(raw_dataset, detections) or changed
    if changed:
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return changed


def _update_languages_for_mapping(data: dict[str, Any], detections: DetectionByTask) -> bool:
    dataset_id = str(data.get("dataset_id", ""))
    task_metadata = data.get("task_metadata")
    if not isinstance(task_metadata, dict):
        return False
    changed = False
    for task_name, metadata in task_metadata.items():
        if not isinstance(metadata, dict):
            continue
        task_detection = detections.get((dataset_id, str(task_name)))
        if task_detection is None:
            continue
        metadata["languages"] = _main_languages_for_metadata(metadata, task_detection)
        metadata["language_detection"] = task_detection["language_detection"]
        changed = True
    return changed


def _main_languages_for_metadata(metadata: dict[str, Any], task_detection: dict[str, Any]) -> list[str]:
    if metadata.get("category") == "code" and metadata.get("language") == "en":
        return ["en"]
    return list(task_detection["languages"])


def _language_detection_payload(detection: dict[str, Any]) -> dict[str, Any]:
    return {
        "sample_count": detection["sample_count"],
        "languages": {
            language: round(ratio * 100, 3)
            for language, ratio in sorted(detection["ratios"].items(), key=lambda item: (-item[1], item[0]))
        },
    }


def _safe_detect(detector: Detector, text: str) -> Any:
    try:
        return detector(text)
    except Exception:
        return None


def _detect_language(text: str) -> Any:
    fast_langdetect_module = importlib.import_module("fast_langdetect")
    detect_fn = getattr(fast_langdetect_module, "detect")
    return detect_fn(text)


def _normalize_detect_result(result: Any) -> tuple[str | None, float]:
    candidate = result[0] if isinstance(result, list) and result else result
    if isinstance(candidate, dict):
        language = candidate.get("lang") or candidate.get("language")
        score = candidate.get("score") or candidate.get("probability") or 0.0
        return (_normalize_language_code(str(language)) if language else None, float(score))
    if isinstance(candidate, str):
        return _normalize_language_code(candidate), 1.0
    return None, 0.0


def _normalize_language_code(language: str) -> str:
    return language.lower().replace("_", "-").split("-")[0]


def _task_name_for_split(dataset: Any, split_name: str) -> str:
    mapping = dataset.effective_split_mapping
    if mapping is not None:
        if split_name in mapping:
            return str(mapping[split_name])
        for _logical_name, mapped_split in mapping.items():
            if split_name == mapped_split:
                return str(mapped_split)
    return split_name


if __name__ == "__main__":
    main()
