from __future__ import annotations

import importlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import yaml

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


@dataclass(frozen=True)
class NanoDatasetSpec:
    name: str
    dataset_id: str
    corpus_config: str = "corpus"
    queries_config: str = "queries"
    qrels_config: str = "qrels"
    candidate_config: str | None = "bm25"
    benchmark_kind: str = "nano"
    splits: list[str] | None = None
    split_mapping: dict[str, str] | None = None

    @property
    def effective_split_mapping(self) -> dict[str, str] | None:
        if self.split_mapping is not None:
            return dict(self.split_mapping)
        if self.benchmark_kind == "nanobeir":
            return dict(NANOBEIR_SPLIT_MAPPING)
        return None


@dataclass(frozen=True)
class DatasetCollectionSpec:
    name: str
    datasets: list[str]


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


def _normalize_key(value: str) -> str:
    return value.strip().lower()


def _repo_name(dataset_id: str) -> str:
    return dataset_id.rstrip("/").split("/")[-1]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


def _dataset_from_mapping(data: dict[str, Any], *, source: str) -> NanoDatasetSpec:
    required = {"name", "dataset_id"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"Dataset spec {source} is missing required keys: {sorted(missing)}")

    splits = data.get("splits")
    if splits is not None and not isinstance(splits, list):
        raise ValueError(f"Dataset spec {source} has invalid splits; expected list.")

    split_mapping = data.get("split_mapping")
    if split_mapping is not None and not isinstance(split_mapping, dict):
        raise ValueError(f"Dataset spec {source} has invalid split_mapping; expected mapping.")

    return NanoDatasetSpec(
        name=str(data["name"]),
        dataset_id=str(data["dataset_id"]),
        corpus_config=str(data.get("corpus_config", "corpus")),
        queries_config=str(data.get("queries_config", "queries")),
        qrels_config=str(data.get("qrels_config", "qrels")),
        candidate_config=None if data.get("candidate_config") is None else str(data.get("candidate_config", "bm25")),
        benchmark_kind=str(data.get("benchmark_kind", "nano")),
        splits=[str(split) for split in splits] if splits is not None else None,
        split_mapping={str(key): str(value) for key, value in split_mapping.items()} if split_mapping else None,
    )


def _collection_from_mapping(data: dict[str, Any], *, registry: DatasetRegistry, source: str) -> DatasetCollectionSpec:
    if "name" not in data or "datasets" not in data:
        raise ValueError(f"Collection spec {source} must include name and datasets.")
    raw_datasets = data["datasets"]
    if not isinstance(raw_datasets, list):
        raise ValueError(f"Collection spec {source} has invalid datasets; expected list.")

    dataset_names: list[str] = []
    for index, raw in enumerate(raw_datasets):
        if isinstance(raw, str):
            dataset_names.append(raw)
            continue
        if isinstance(raw, dict):
            dataset = _dataset_from_mapping(cast(dict[str, Any], raw), source=f"{source}:datasets[{index}]")
            registry.add_dataset(dataset)
            dataset_names.append(dataset.name)
            continue
        raise ValueError(f"Unsupported dataset entry in {source}: {raw!r}")
    return DatasetCollectionSpec(name=str(data["name"]), datasets=dataset_names)


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
        return cls.load_from_root(Path(__file__).resolve().parents[1] / "config")

    @classmethod
    def load_from_root(cls, root: Path) -> DatasetRegistry:
        registry = cls()
        dataset_dir = root / "datasets"
        if dataset_dir.exists():
            for path in sorted(dataset_dir.glob("*.yaml")):
                data = _load_yaml(path)
                if "datasets" in data:
                    for index, raw in enumerate(data["datasets"]):
                        if not isinstance(raw, dict):
                            raise ValueError(f"Dataset list entry in {path} must be a mapping.")
                        registry.add_dataset(_dataset_from_mapping(raw, source=f"{path}:datasets[{index}]"))
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
