from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import yaml
from huggingface_hub import hf_hub_download, list_repo_files

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.migrate_nanomteb_family_results import SPLIT_MOVES_TO_MISC


CONFIGS = ("bm25", "corpus", "qrels", "queries")

FAMILY_DATASETS = (
    "NanoMTEB",
    "NanoMMTEB",
    "NanoCMTEB",
    "NanoMTEB-Dutch",
    "NanoMTEB-French",
    "NanoMTEB-German",
    "NanoJMTEB",
    "NanoMTEB-Korean",
    "NanoFaMTEB",
    "NanoRuMTEB",
    "NanoMTEB-Scandinavian",
    "NanoMTEB-Spanish",
    "NanoMTEB-Thai",
    "NanoVNMTEB",
    "NanoMTEB-Misc",
)

SOURCE_DATASET_IDS = {
    "NanoMTEB": "hakari-bench/NanoMTEB",
    "NanoMMTEB": "hakari-bench/NanoMMTEB",
    "NanoMTEB-Chinese": "hakari-bench/NanoMTEB-Chinese",
    "NanoMTEB-Dutch": "hakari-bench/NanoMTEB-Dutch",
    "NanoMTEB-French": "hakari-bench/NanoMTEB-French",
    "NanoMTEB-German": "hakari-bench/NanoMTEB-German",
    "NanoMTEB-Japanese": "hakari-bench/NanoMTEB-Japanese",
    "NanoMTEB-Korean": "hakari-bench/NanoMTEB-Korean",
    "NanoMTEB-Persian": "hakari-bench/NanoMTEB-Persian",
    "NanoMTEB-Polish": "hakari-bench/NanoMTEB-Polish",
    "NanoMTEB-Russian": "hakari-bench/NanoMTEB-Russian",
    "NanoMTEB-Scandinavian": "hakari-bench/NanoMTEB-Scandinavian",
    "NanoMTEB-Spanish": "hakari-bench/NanoMTEB-Spanish",
    "NanoMTEB-Thai": "hakari-bench/NanoMTEB-Thai",
    "NanoMTEB-Vietnamese": "hakari-bench/NanoMTEB-Vietnamese",
    "NanoMTEB-Xlingual": "hakari-bench/NanoMTEB-Xlingual",
}

DIRECT_SOURCE_BY_TARGET = {
    "NanoMTEB": "NanoMTEB",
    "NanoMMTEB": "NanoMMTEB",
    "NanoCMTEB": "NanoMTEB-Chinese",
    "NanoMTEB-Dutch": "NanoMTEB-Dutch",
    "NanoMTEB-French": "NanoMTEB-French",
    "NanoMTEB-German": "NanoMTEB-German",
    "NanoJMTEB": "NanoMTEB-Japanese",
    "NanoMTEB-Korean": "NanoMTEB-Korean",
    "NanoFaMTEB": "NanoMTEB-Persian",
    "NanoRuMTEB": "NanoMTEB-Russian",
    "NanoMTEB-Scandinavian": "NanoMTEB-Scandinavian",
    "NanoMTEB-Spanish": "NanoMTEB-Spanish",
    "NanoMTEB-Thai": "NanoMTEB-Thai",
    "NanoVNMTEB": "NanoMTEB-Vietnamese",
}

MISC_SOURCE_CANDIDATES = (
    "NanoMTEB-Xlingual",
    "NanoMTEB-Polish",
    "NanoMTEB-Dutch",
    "NanoMTEB-French",
    "NanoMTEB-German",
    "NanoMTEB-Korean",
    "NanoMTEB-Persian",
    "NanoMTEB-Russian",
    "NanoMTEB-Vietnamese",
)


@dataclass(frozen=True)
class SplitSource:
    target_dataset: str
    split_name: str
    source_dataset_name: str
    source_dataset_id: str


def build_plan(*, config_root: Path) -> dict[str, list[SplitSource]]:
    files_by_source: dict[str, set[str]] = {}
    plan: dict[str, list[SplitSource]] = {}
    for target_dataset in FAMILY_DATASETS:
        splits = _dataset_splits(config_root=config_root, dataset_name=target_dataset)
        if target_dataset == "NanoMTEB-Misc":
            plan[target_dataset] = [
                _find_misc_source(split, files_by_source=files_by_source) for split in splits
            ]
            continue
        source_name = DIRECT_SOURCE_BY_TARGET[target_dataset]
        source_id = SOURCE_DATASET_IDS[source_name]
        plan[target_dataset] = [
            SplitSource(
                target_dataset=target_dataset,
                split_name=split,
                source_dataset_name=source_name,
                source_dataset_id=source_id,
            )
            for split in splits
        ]
    return plan


def build_datasets(*, output_root: Path, config_root: Path, clean: bool = False) -> None:
    plan = build_plan(config_root=config_root)
    if clean and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    for dataset_name, splits in plan.items():
        dataset_dir = output_root / dataset_name
        if clean and dataset_dir.exists():
            shutil.rmtree(dataset_dir)
        dataset_dir.mkdir(parents=True, exist_ok=True)
        _write_lfs_attributes(dataset_dir)
        copied = _copy_dataset_files(dataset_dir=dataset_dir, splits=splits)
        _write_metadata_files(
            dataset_dir=dataset_dir,
            dataset_name=dataset_name,
            splits=splits,
            copied=copied,
            config_root=config_root,
        )


def _copy_dataset_files(*, dataset_dir: Path, splits: list[SplitSource]) -> dict[str, dict[str, str]]:
    files_by_repo = {
        source.source_dataset_id: set(list_repo_files(source.source_dataset_id, repo_type="dataset"))
        for source in sorted(set(splits), key=lambda source: source.source_dataset_id)
    }
    copied: dict[str, dict[str, str]] = {}
    for source in splits:
        copied[source.split_name] = {}
        for config in CONFIGS:
            source_file = _select_parquet_file(
                files=files_by_repo[source.source_dataset_id],
                config=config,
                split_name=source.split_name,
                dataset_id=source.source_dataset_id,
            )
            local_file = hf_hub_download(source.source_dataset_id, source_file, repo_type="dataset")
            dest = dataset_dir / config / f"{source.split_name}.parquet"
            dest.parent.mkdir(parents=True, exist_ok=True)
            _copy_parquet_file(local_file=Path(local_file), dest=dest, config=config)
            copied[source.split_name][config] = str(dest.relative_to(dataset_dir))

        metadata_file = _select_metadata_file(
            files=files_by_repo[source.source_dataset_id],
            split_name=source.split_name,
        )
        if metadata_file is not None:
            local_metadata = hf_hub_download(source.source_dataset_id, metadata_file, repo_type="dataset")
            dest = dataset_dir / "metadata" / f"{source.split_name}.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(local_metadata, dest)
            _patch_split_metadata_counts(dataset_dir=dataset_dir, source=source)
        else:
            _write_generated_split_metadata(dataset_dir=dataset_dir, source=source)
    return copied


def _write_metadata_files(
    *,
    dataset_dir: Path,
    dataset_name: str,
    splits: list[SplitSource],
    copied: dict[str, dict[str, str]],
    config_root: Path,
) -> None:
    dataset_config = _dataset_config(config_root=config_root, dataset_name=dataset_name)
    manifest = _build_manifest(dataset_name=dataset_name, splits=splits, dataset_dir=dataset_dir)
    (dataset_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    bm25_config = _build_bm25_subset_config(dataset_name=dataset_name, splits=splits)
    (dataset_dir / "nano_bm25_subset_config.json").write_text(
        json.dumps(bm25_config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (dataset_dir / "README.md").write_text(
        _build_readme(dataset_name=dataset_name, dataset_config=dataset_config, copied=copied, splits=splits),
        encoding="utf-8",
    )


def _build_manifest(*, dataset_name: str, splits: list[SplitSource], dataset_dir: Path) -> dict[str, Any]:
    source_datasets = _source_dataset_payloads(splits)
    split_mapping: list[dict[str, Any]] = []
    counts: list[dict[str, Any]] = []
    for source in splits:
        metadata = _read_optional_json(dataset_dir / "metadata" / f"{source.split_name}.json")
        mapping: dict[str, Any] = {
            "split_name": source.split_name,
            "source_dataset_name": source.source_dataset_name,
            "source_dataset_id": source.source_dataset_id,
        }
        for key in (
            "task_name",
            "source_query_config",
            "source_query_split",
            "source_corpus_config",
            "source_corpus_split",
        ):
            if key in metadata:
                mapping[key] = metadata[key]
        split_mapping.append(mapping)
        count = {"split_name": source.split_name}
        for key in ("queries", "corpus", "qrels", "candidate_queries"):
            if key in metadata:
                count[key] = metadata[key]
        counts.append(count)
    return {
        "dataset_name": dataset_name,
        "dataset_id": f"hakari-bench/{dataset_name}",
        "output_root": str(dataset_dir),
        "source_datasets": source_datasets,
        "split_mapping": split_mapping,
        "counts": counts,
    }


def _build_bm25_subset_config(*, dataset_name: str, splits: list[SplitSource]) -> dict[str, Any]:
    entries_by_split: dict[str, dict[str, Any]] = {}
    for source in sorted(set(splits), key=lambda item: item.source_dataset_id):
        source_config = _download_optional_json(source.source_dataset_id, "nano_bm25_subset_config.json")
        for entry in source_config.get("splits", []):
            if isinstance(entry, dict) and isinstance(entry.get("split_name"), str):
                entry = dict(entry)
                entry["source_dataset_name"] = source.source_dataset_name
                entry["source_dataset_id"] = source.source_dataset_id
                entries_by_split[entry["split_name"]] = entry
    return {
        "dataset": dataset_name,
        "dataset_id": f"hakari-bench/{dataset_name}",
        "source_datasets": _source_dataset_payloads(splits),
        "bm25_top_k": 100,
        "candidate_policy": (
            "Rank each selected split corpus with BM25, keep up to top-100 candidates, "
            "and force qrels-positive documents into the final candidate list when missing."
        ),
        "splits": [entries_by_split.get(source.split_name, {"split_name": source.split_name}) for source in splits],
    }


def _build_readme(
    *,
    dataset_name: str,
    dataset_config: dict[str, Any],
    copied: dict[str, dict[str, str]],
    splits: list[SplitSource],
) -> str:
    front_matter: dict[str, Any] = {
        "configs": [
            {
                "config_name": config,
                "data_files": [
                    {"split": split_name, "path": copied[split_name][config]} for split_name in copied
                ],
                **({"default": True} if config == "queries" else {}),
            }
            for config in CONFIGS
        ],
        "tags": ["information-retrieval", "retrieval", "nano", "bm25", "hakari-bench"],
    }
    languages = _dataset_languages(dataset_config)
    if languages:
        front_matter["language"] = languages
    raw_metadata = dataset_config.get("metadata")
    metadata = cast("dict[str, Any]", raw_metadata) if isinstance(raw_metadata, dict) else {}
    description = str(metadata.get("description") or f"{dataset_name} is a Nano-style retrieval dataset.")
    sources = ", ".join(f"`{payload['dataset_id']}`" for payload in _source_dataset_payloads(splits))
    return (
        "---\n"
        + yaml.safe_dump(front_matter, sort_keys=False, allow_unicode=True)
        + "---\n\n"
        + f"# {dataset_name}\n\n"
        + f"{description}\n\n"
        + "This repository is a Nano-style information retrieval dataset prepared for "
        + "[HAKARI-Bench](https://github.com/hotchpotch/hakari-bench). It follows the "
        + "NanoBEIR-style Hugging Face Datasets layout with separate `corpus`, `queries`, "
        + "`qrels`, and `bm25` configs. Each config contains the same split names.\n\n"
        + f"Source historical dataset repositories: {sources}.\n\n"
        + "The canonical Hugging Face dataset id for this directory is "
        + f"`hakari-bench/{dataset_name}`. Historical broad language-bucket dataset "
        + "repositories are intended to be removed after these canonical datasets are uploaded.\n"
    )


def _find_misc_source(split_name: str, *, files_by_source: dict[str, set[str]]) -> SplitSource:
    for source_name, moved_splits in SPLIT_MOVES_TO_MISC.items():
        if split_name in moved_splits:
            return SplitSource(
                target_dataset="NanoMTEB-Misc",
                split_name=split_name,
                source_dataset_name=source_name,
                source_dataset_id=SOURCE_DATASET_IDS[source_name],
            )
    for source_name in MISC_SOURCE_CANDIDATES:
        dataset_id = SOURCE_DATASET_IDS[source_name]
        files = files_by_source.setdefault(dataset_id, set(list_repo_files(dataset_id, repo_type="dataset")))
        if _has_split(files=files, config="queries", split_name=split_name):
            return SplitSource(
                target_dataset="NanoMTEB-Misc",
                split_name=split_name,
                source_dataset_name=source_name,
                source_dataset_id=dataset_id,
            )
    raise ValueError(f"Could not locate source dataset for NanoMTEB-Misc split: {split_name}")


def _select_parquet_file(*, files: set[str], config: str, split_name: str, dataset_id: str) -> str:
    candidates = [
        f"{config}/{split_name}.parquet",
        f"{config}/{split_name}-00000-of-00001.parquet",
        f"{split_name}/{config}/test.parquet",
    ]
    for candidate in candidates:
        if candidate in files:
            return candidate
    prefix = f"{config}/{split_name}-"
    matches = sorted(file for file in files if file.startswith(prefix) and file.endswith(".parquet"))
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise ValueError(f"Split {dataset_id}/{config}/{split_name} has multiple parquet shards: {matches}")
    raise FileNotFoundError(f"Missing parquet file for {dataset_id}/{config}/{split_name}")


def _select_metadata_file(*, files: set[str], split_name: str) -> str | None:
    for candidate in (f"metadata/{split_name}.json", f"{split_name}/metadata/test.json"):
        if candidate in files:
            return candidate
    return None


def _has_split(*, files: set[str], config: str, split_name: str) -> bool:
    try:
        _select_parquet_file(files=files, config=config, split_name=split_name, dataset_id="")
    except (FileNotFoundError, ValueError):
        return False
    return True


def _dataset_splits(*, config_root: Path, dataset_name: str) -> list[str]:
    config = _dataset_config(config_root=config_root, dataset_name=dataset_name)
    splits = config.get("splits")
    if not isinstance(splits, list) or not all(isinstance(split, str) for split in splits):
        raise ValueError(f"Dataset config for {dataset_name} must declare string splits.")
    return [cast("str", split) for split in splits]


def _dataset_config(*, config_root: Path, dataset_name: str) -> dict[str, Any]:
    for path in sorted((config_root / "datasets").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("name") == dataset_name:
            return data
    raise FileNotFoundError(f"Could not find dataset config for {dataset_name}")


def _dataset_languages(dataset_config: dict[str, Any]) -> list[str]:
    metadata = dataset_config.get("metadata")
    if not isinstance(metadata, dict):
        return []
    languages = metadata.get("languages")
    if isinstance(languages, list):
        return [str(language) for language in languages if str(language) not in {"unknown", "multilingual"}]
    language = str(metadata.get("language") or "")
    if language and language not in {"unknown", "multilingual"}:
        return [language]
    return []


def _source_dataset_payloads(splits: list[SplitSource]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    payloads: list[dict[str, str]] = []
    for source in splits:
        key = (source.source_dataset_name, source.source_dataset_id)
        if key in seen:
            continue
        seen.add(key)
        payloads.append({"name": source.source_dataset_name, "dataset_id": source.source_dataset_id})
    return payloads


def _read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _download_optional_json(dataset_id: str, filename: str) -> dict[str, Any]:
    try:
        local_path = hf_hub_download(dataset_id, filename, repo_type="dataset")
    except Exception:
        return {}
    data = json.loads(Path(local_path).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _write_lfs_attributes(dataset_dir: Path) -> None:
    (dataset_dir / ".gitattributes").write_text(
        "*.parquet filter=lfs diff=lfs merge=lfs -text\n",
        encoding="utf-8",
    )


def _write_generated_split_metadata(*, dataset_dir: Path, source: SplitSource) -> None:
    metadata = {
        "split_name": source.split_name,
        "source_dataset_name": source.source_dataset_name,
        "source_dataset_id": source.source_dataset_id,
        "queries": _parquet_num_rows(dataset_dir / "queries" / f"{source.split_name}.parquet"),
        "corpus": _parquet_num_rows(dataset_dir / "corpus" / f"{source.split_name}.parquet"),
        "qrels": _parquet_num_rows(dataset_dir / "qrels" / f"{source.split_name}.parquet"),
        "candidate_queries": _parquet_num_rows(dataset_dir / "bm25" / f"{source.split_name}.parquet"),
    }
    dest = dataset_dir / "metadata" / f"{source.split_name}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _copy_parquet_file(*, local_file: Path, dest: Path, config: str) -> None:
    if config != "qrels":
        shutil.copy2(local_file, dest)
        return
    import pyarrow as pa
    import pyarrow.parquet as pq

    table = pq.read_table(local_file)
    if "score" in table.column_names:
        mask = pa.array([score > 0 for score in table.column("score").to_pylist()])
        table = table.filter(mask)
        table = table.drop(["score"])
    pq.write_table(table, dest)


def _parquet_num_rows(path: Path) -> int:
    import pyarrow.parquet as pq

    return int(pq.ParquetFile(path).metadata.num_rows)


def _patch_split_metadata_counts(*, dataset_dir: Path, source: SplitSource) -> None:
    path = dataset_dir / "metadata" / f"{source.split_name}.json"
    metadata = _read_optional_json(path)
    metadata["queries"] = _parquet_num_rows(dataset_dir / "queries" / f"{source.split_name}.parquet")
    metadata["corpus"] = _parquet_num_rows(dataset_dir / "corpus" / f"{source.split_name}.parquet")
    metadata["qrels"] = _parquet_num_rows(dataset_dir / "qrels" / f"{source.split_name}.parquet")
    metadata["candidate_queries"] = _parquet_num_rows(dataset_dir / "bm25" / f"{source.split_name}.parquet")
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build uploadable NanoMTEB family dataset directories.")
    parser.add_argument("--output-root", type=Path, default=Path("output/NanoMTEB_Family"))
    parser.add_argument("--config-root", type=Path, default=Path("config"))
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    build_datasets(output_root=args.output_root, config_root=args.config_root, clean=args.clean)


if __name__ == "__main__":
    main()
