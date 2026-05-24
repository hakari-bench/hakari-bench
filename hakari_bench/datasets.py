from __future__ import annotations

import importlib
import importlib.resources
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import yaml

from hakari_bench.config_schema import DatasetCollectionConfigModel, DatasetConfigFileModel, DatasetConfigModel
from hakari_bench.defaults import DEFAULT_CANDIDATE_RANKING

try:
    HfApi: Any = getattr(importlib.import_module("huggingface_hub"), "HfApi")
except Exception:  # pragma: no cover
    HfApi = None

try:
    from datasets import get_dataset_split_names
except Exception:  # pragma: no cover

    def get_dataset_split_names(dataset_id: str, subset: str) -> list[str]:
        raise RuntimeError("datasets is required to discover Nano benchmark splits.")


NANOBEIR_SPLIT_MAPPING: dict[str, str] = {
    "climatefever": "NanoClimateFEVER",
    "dbpedia": "NanoDBPedia",
    "fever": "NanoFEVER",
    "fiqa2018": "NanoFiQA2018",
    "hotpotqa": "NanoHotpotQA",
    "msmarco": "NanoMSMARCO",
    "nfcorpus": "NanoNFCorpus",
    "nq": "NanoNQ",
    "quoraretrieval": "NanoQuoraRetrieval",
    "scidocs": "NanoSCIDOCS",
    "arguana": "NanoArguAna",
    "scifact": "NanoSciFact",
    "touche2020": "NanoTouche2020",
}

VALID_METADATA_CATEGORIES = {"natural_language", "code"}
REQUIRED_METADATA_FIELDS = {"language", "category", "short_description", "description"}
TEXT_STATS_FIELDS = {"count", "min_chars", "max_chars", "mean_chars", "median_chars"}
LANGUAGE_DETECTION_SIDES = ("query", "document")
REFERENCE_SOURCE_CONFIDENCE_LABELS = {
    "source_uncertain": (
        "The source may be relevant, but the citation-to-task relationship is not established well enough "
        "to rely on without further review."
    ),
    "probably_correct": (
        "The source appears to be the right task or dataset source based on upstream metadata, local MTEB data, "
        "dataset cards, or web search, but some uncertainty remains."
    ),
    "definitive_paper_link": (
        "The source is a paper, official proceedings page, DOI landing page, arXiv page, or comparable scholarly "
        "record that clearly corresponds to the task or dataset."
    ),
    "human_verified": (
        "A human reviewer explicitly checked and approved the source. AI agents must not assign this label."
    ),
}
VALID_REFERENCE_SOURCE_CONFIDENCE = set(REFERENCE_SOURCE_CONFIDENCE_LABELS)


@dataclass(frozen=True)
class NanoDatasetSpec:
    name: str
    dataset_id: str
    corpus_config: str = "corpus"
    queries_config: str = "queries"
    qrels_config: str = "qrels"
    candidate_config: str | None = DEFAULT_CANDIDATE_RANKING
    benchmark_kind: str = "nano"
    splits: list[str] | None = None
    split_mapping: dict[str, str] | None = None
    metadata: dict[str, Any] | None = None
    task_metadata: dict[str, dict[str, Any]] | None = None

    @property
    def effective_split_mapping(self) -> dict[str, str] | None:
        if self.split_mapping is not None:
            return dict(self.split_mapping)
        if self.benchmark_kind == "nanobeir":
            return dict(NANOBEIR_SPLIT_MAPPING)
        return None

    def metadata_for_task(self, *, split_name: str, task_name: str) -> dict[str, Any]:
        metadata = dict(self.metadata or {})
        task_metadata = self.task_metadata or {}
        selected = task_metadata.get(task_name) or task_metadata.get(split_name) or {}
        metadata.update(selected)
        return metadata

    def validate_metadata(self) -> list[str]:
        errors = _validate_metadata_mapping(self.metadata or {}, context=f"{self.name} metadata")
        for task_name, metadata in sorted((self.task_metadata or {}).items()):
            errors.extend(_validate_metadata_mapping(metadata, context=f"{self.name}/{task_name} metadata"))
        return errors


@dataclass(frozen=True)
class DatasetCollectionSpec:
    name: str
    datasets: list[str]
    metadata: dict[str, Any] | None = None

    def validate_metadata(self) -> list[str]:
        return _validate_metadata_mapping(self.metadata or {}, context=f"{self.name} collection metadata")


@dataclass(frozen=True)
class EvalTask:
    dataset: NanoDatasetSpec
    split_name: str
    task_name: str

    @property
    def dataset_id(self) -> str:
        return self.dataset.dataset_id

    @property
    def dataset_name(self) -> str:
        return self.dataset.name

    @property
    def evaluator_name(self) -> str:
        return f"{self.dataset.name}_{self.task_name}"

    @property
    def metadata(self) -> dict[str, Any]:
        return self.dataset.metadata_for_task(split_name=self.split_name, task_name=self.task_name)


def _normalize_key(value: str) -> str:
    return value.strip().lower()


def _repo_name(dataset_id: str) -> str:
    return dataset_id.rstrip("/").split("/")[-1]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


def _dataset_from_config(config: DatasetConfigModel) -> NanoDatasetSpec:
    return NanoDatasetSpec(
        name=config.name,
        dataset_id=config.dataset_id,
        corpus_config=config.corpus_config,
        queries_config=config.queries_config,
        qrels_config=config.qrels_config,
        candidate_config=config.candidate_config,
        benchmark_kind=config.benchmark_kind,
        splits=list(config.splits) if config.splits is not None else None,
        split_mapping=dict(config.split_mapping) if config.split_mapping else None,
        metadata=dict(config.metadata) if config.metadata is not None else None,
        task_metadata=(
            {task_name: dict(metadata) for task_name, metadata in config.task_metadata.items()}
            if config.task_metadata is not None
            else None
        ),
    )


def _dataset_from_mapping(data: dict[str, Any], *, source: str) -> NanoDatasetSpec:
    try:
        config = DatasetConfigModel.model_validate(data)
    except Exception as exc:
        raise ValueError(f"Dataset spec {source} is invalid: {exc}") from exc
    return _dataset_from_config(config)


def _collection_from_config(
    config: DatasetCollectionConfigModel,
    *,
    registry: DatasetRegistry,
) -> DatasetCollectionSpec:
    dataset_names: list[str] = []
    for raw in config.datasets:
        if isinstance(raw, str):
            dataset_names.append(raw)
            continue
        dataset = _dataset_from_config(raw)
        registry.add_dataset(dataset)
        dataset_names.append(dataset.name)
    return DatasetCollectionSpec(
        name=config.name,
        datasets=dataset_names,
        metadata=dict(config.metadata) if config.metadata is not None else None,
    )


def _collection_from_mapping(data: dict[str, Any], *, registry: DatasetRegistry, source: str) -> DatasetCollectionSpec:
    try:
        config = DatasetCollectionConfigModel.model_validate(data)
    except Exception as exc:
        raise ValueError(f"Collection spec {source} is invalid: {exc}") from exc
    return _collection_from_config(config, registry=registry)


class DatasetRegistry:
    def __init__(
        self,
        datasets: list[NanoDatasetSpec] | None = None,
        collections: list[DatasetCollectionSpec] | None = None,
    ) -> None:
        self._datasets_by_key: dict[str, NanoDatasetSpec] = {}
        self._collections_by_key: dict[str, DatasetCollectionSpec] = {}
        for dataset in datasets or []:
            self.add_dataset(dataset)
        for collection in collections or []:
            self.add_collection(collection)

    @classmethod
    def load_builtin(cls) -> DatasetRegistry:
        local_config_root = Path("config")
        if local_config_root.exists():
            return cls.load_from_root(local_config_root)
        try:
            config_resources = importlib.resources.files("config")
        except ModuleNotFoundError as exc:
            raise FileNotFoundError("Built-in HAKARI dataset config was not found.") from exc
        with importlib.resources.as_file(config_resources) as config_root:
            return cls.load_from_root(config_root)

    @classmethod
    def load_from_root(cls, root: Path) -> DatasetRegistry:
        registry = cls()
        dataset_dir = root / "datasets"
        if dataset_dir.exists():
            for path in sorted(dataset_dir.glob("*.yaml")):
                data = _load_yaml(path)
                if "datasets" in data:
                    try:
                        config_file = DatasetConfigFileModel.model_validate(data)
                    except Exception as exc:
                        raise ValueError(f"Dataset config file {path} is invalid: {exc}") from exc
                    for raw in config_file.datasets:
                        registry.add_dataset(_dataset_from_config(raw))
                else:
                    registry.add_dataset(_dataset_from_mapping(data, source=str(path)))

        collection_dir = root / "dataset_collections"
        if collection_dir.exists():
            for path in sorted(collection_dir.glob("*.yaml")):
                registry.add_collection(_collection_from_mapping(_load_yaml(path), registry=registry, source=str(path)))
        return registry

    def add_dataset(self, dataset: NanoDatasetSpec) -> None:
        self._datasets_by_key[_normalize_key(dataset.name)] = dataset
        self._datasets_by_key[_normalize_key(dataset.dataset_id)] = dataset

    def add_collection(self, collection: DatasetCollectionSpec) -> None:
        self._collections_by_key[_normalize_key(collection.name)] = collection

    def dataset_names(self) -> list[str]:
        datasets = {dataset.dataset_id: dataset for dataset in self._datasets_by_key.values()}
        return [dataset.name for dataset in sorted(datasets.values(), key=lambda item: item.name.lower())]

    def get_dataset(self, value: str) -> NanoDatasetSpec:
        dataset = self._datasets_by_key.get(_normalize_key(value))
        if dataset is not None:
            return dataset
        if "/" in value:
            return infer_dataset_spec(value)
        raise KeyError(f"Unknown dataset '{value}'.")

    def get_collection(self, value: str) -> DatasetCollectionSpec:
        collection = self._collections_by_key.get(_normalize_key(value))
        if collection is None:
            raise KeyError(f"Unknown dataset collection '{value}'.")
        return collection


def infer_dataset_spec(dataset_id: str) -> NanoDatasetSpec:
    name = _repo_name(dataset_id)
    benchmark_kind = "nanobeir" if name.lower().startswith("nanobeir-") else "nano"
    return NanoDatasetSpec(name=name, dataset_id=dataset_id, benchmark_kind=benchmark_kind)


def _validate_metadata_mapping(metadata: dict[str, Any], *, context: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_METADATA_FIELDS - set(metadata))
    if missing:
        errors.append(f"{context} is missing required fields: {missing}.")

    language = metadata.get("language")
    if isinstance(language, str):
        if language not in {"multilingual", "unknown"} and len(language) != 2:
            errors.append(f"{context} has invalid language '{language}'.")
    elif language is not None or "language" in metadata:
        errors.append(f"{context} has invalid language {language!r}.")

    languages = metadata.get("languages")
    if languages is not None:
        if not isinstance(languages, list) or not languages:
            errors.append(f"{context} has invalid languages; expected non-empty list.")
        else:
            for index, detected_language in enumerate(languages):
                if not isinstance(detected_language, str):
                    errors.append(f"{context} languages[{index}] must be string.")
                elif not _is_valid_language_code(detected_language):
                    errors.append(f"{context} has invalid languages[{index}] '{detected_language}'.")

    category = metadata.get("category")
    if isinstance(category, str):
        if category not in VALID_METADATA_CATEGORIES:
            errors.append(f"{context} has invalid category '{category}'.")
    elif category is not None or "category" in metadata:
        errors.append(f"{context} has invalid category {category!r}.")

    short_description = metadata.get("short_description")
    if isinstance(short_description, str):
        if len(short_description) > 140:
            errors.append(f"{context} short_description exceeds 140 characters.")
    elif short_description is not None or "short_description" in metadata:
        errors.append(f"{context} has invalid short_description {short_description!r}.")

    description = metadata.get("description")
    if not isinstance(description, str) and (description is not None or "description" in metadata):
        errors.append(f"{context} has invalid description {description!r}.")

    references = metadata.get("references")
    if references is not None:
        if not isinstance(references, list):
            errors.append(f"{context} has invalid references; expected list.")
        else:
            for index, reference in enumerate(references):
                if not isinstance(reference, dict):
                    errors.append(f"{context} references[{index}] must be a mapping.")
                    continue
                reference_mapping = cast(dict[str, Any], reference)
                if "is_paper" not in reference_mapping:
                    errors.append(f"{context} references[{index}] is missing is_paper.")
                elif not isinstance(reference_mapping["is_paper"], bool):
                    errors.append(f"{context} references[{index}].is_paper must be boolean.")
                source_confidence = reference_mapping.get("source_confidence")
                if "source_confidence" not in reference_mapping:
                    errors.append(f"{context} references[{index}] is missing source_confidence.")
                elif not isinstance(source_confidence, str):
                    errors.append(f"{context} references[{index}].source_confidence must be string.")
                elif source_confidence not in VALID_REFERENCE_SOURCE_CONFIDENCE:
                    errors.append(
                        f"{context} references[{index}].source_confidence has invalid label "
                        f"{source_confidence!r}."
                    )

    for stats_key in ("query_text_stats", "document_text_stats"):
        stats = metadata.get(stats_key)
        if stats is None:
            continue
        if not isinstance(stats, dict):
            errors.append(f"{context} has invalid {stats_key}; expected mapping.")
            continue
        missing_stats = sorted(TEXT_STATS_FIELDS - set(stats))
        if missing_stats:
            errors.append(f"{context} {stats_key} is missing fields: {missing_stats}.")
        for key in TEXT_STATS_FIELDS & set(stats):
            if not isinstance(stats[key], int | float):
                errors.append(f"{context} {stats_key}.{key} must be numeric.")

    language_detection = metadata.get("language_detection")
    if language_detection is not None:
        errors.extend(_validate_language_detection(language_detection, context=context))
    return errors


def _validate_language_detection(language_detection: Any, *, context: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(language_detection, dict):
        return [f"{context} has invalid language_detection; expected mapping."]
    detector = language_detection.get("detector")
    if not isinstance(detector, str):
        errors.append(f"{context} language_detection.detector must be string.")
    for threshold_key in ("min_language_percent", "main_language_percent"):
        value = language_detection.get(threshold_key)
        if not isinstance(value, int | float):
            errors.append(f"{context} language_detection.{threshold_key} must be numeric.")
    for side in LANGUAGE_DETECTION_SIDES:
        side_value = language_detection.get(side)
        if not isinstance(side_value, dict):
            errors.append(f"{context} language_detection.{side} must be mapping.")
            continue
        sample_count = side_value.get("sample_count")
        if not isinstance(sample_count, int):
            errors.append(f"{context} language_detection.{side}.sample_count must be integer.")
        detected_languages = side_value.get("languages")
        if not isinstance(detected_languages, dict) or not detected_languages:
            errors.append(f"{context} language_detection.{side}.languages must be non-empty mapping.")
            continue
        for language, percent in detected_languages.items():
            if not isinstance(language, str):
                errors.append(f"{context} language_detection.{side}.languages key must be string.")
            elif not _is_valid_language_code(language):
                errors.append(f"{context} has invalid language_detection.{side}.languages key '{language}'.")
            if not isinstance(percent, int | float):
                errors.append(f"{context} language_detection.{side}.languages[{language!r}] must be numeric.")
    return errors


def _is_valid_language_code(language: str) -> bool:
    return language == "unknown" or 2 <= len(language) <= 3


def validate_builtin_metadata() -> list[str]:
    registry = DatasetRegistry.load_builtin()
    errors: list[str] = []
    datasets = sorted({id(dataset): dataset for dataset in registry._datasets_by_key.values()}.values(), key=lambda item: item.name)
    collections = sorted(
        {id(collection): collection for collection in registry._collections_by_key.values()}.values(),
        key=lambda item: item.name,
    )
    for dataset in datasets:
        errors.extend(dataset.validate_metadata())
        task_metadata = dataset.task_metadata or {}
        for split_name in dataset.splits or list((dataset.effective_split_mapping or {}).values()):
            task_name = _task_name_for_split(dataset, split_name)
            if task_name not in task_metadata and split_name not in task_metadata:
                errors.append(f"{dataset.name}/{task_name} metadata is missing.")
    for collection in collections:
        errors.extend(collection.validate_metadata())
    return errors


def resolve_dataset_splits(spec: NanoDatasetSpec) -> list[str]:
    if spec.splits is not None:
        return list(spec.splits)
    mapping = spec.effective_split_mapping
    if mapping is not None:
        return list(mapping.values())
    return list(get_dataset_split_names(spec.dataset_id, spec.queries_config))


@lru_cache(maxsize=512)
def resolve_dataset_revision(dataset_id: str, requested_revision: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "requested": requested_revision,
        "resolved": None,
        "source": "huggingface_hub",
    }
    if HfApi is None:
        payload["error"] = "huggingface_hub is not installed."
        return payload
    try:
        info = HfApi().dataset_info(repo_id=dataset_id, revision=requested_revision)
    except Exception as exc:
        payload["error"] = f"{type(exc).__name__}: {exc}"
        return payload

    sha = getattr(info, "sha", None)
    if sha is None:
        payload["error"] = "Dataset revision SHA was not returned by Hugging Face Hub."
    else:
        payload["resolved"] = str(sha)
    return payload


def _resolve_selected_split(spec: NanoDatasetSpec, value: str) -> tuple[str, str]:
    mapping = spec.effective_split_mapping
    if mapping is None:
        return value, value

    lowered = value.lower()
    if lowered in mapping:
        return mapping[lowered], lowered
    for logical_name, split_name in mapping.items():
        if value == split_name or value.lower() == split_name.lower():
            return split_name, logical_name
    raise ValueError(f"Unknown split '{value}' for dataset '{spec.name}'. Available: {sorted(mapping)}")


def _task_name_for_split(spec: NanoDatasetSpec, split_name: str) -> str:
    mapping = spec.effective_split_mapping
    if mapping is not None:
        for logical_name, mapped_split in mapping.items():
            if split_name == mapped_split:
                return logical_name
    return split_name


def parse_csv_values(values: list[str] | None) -> list[str]:
    parsed: list[str] = []
    for value in values or []:
        parsed.extend(item.strip() for item in value.split(",") if item.strip())

    seen: set[str] = set()
    deduped: list[str] = []
    for value in parsed:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def resolve_eval_tasks(
    *,
    registry: DatasetRegistry,
    dataset_values: list[str],
    collection_values: list[str],
    split_values: list[str] | None,
) -> list[EvalTask]:
    dataset_specs: list[NanoDatasetSpec] = []
    for collection_name in parse_csv_values(collection_values):
        collection = registry.get_collection(collection_name)
        dataset_specs.extend(registry.get_dataset(dataset_name) for dataset_name in collection.datasets)
    dataset_specs.extend(registry.get_dataset(dataset_name) for dataset_name in parse_csv_values(dataset_values))

    selected_splits = parse_csv_values(split_values)
    tasks: list[EvalTask] = []
    for spec in dataset_specs:
        if selected_splits:
            split_pairs = [_resolve_selected_split(spec, value) for value in selected_splits]
        else:
            split_pairs = [(split_name, _task_name_for_split(spec, split_name)) for split_name in resolve_dataset_splits(spec)]
        for split_name, task_name in split_pairs:
            tasks.append(EvalTask(dataset=spec, split_name=split_name, task_name=task_name))

    deduped: list[EvalTask] = []
    seen: set[tuple[str, str]] = set()
    for task in tasks:
        key = (task.dataset_id, task.split_name)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(task)
    if not deduped:
        raise ValueError("No evaluation tasks were resolved.")
    return deduped
