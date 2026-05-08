from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hakari_bench.results import safe_path_part


MISC_DATASET_NAME = "NanoMTEB-Misc"
MISC_DATASET_ID = "hakari-bench/NanoMTEB-Misc"

DATASET_RENAMES: dict[str, str] = {
    "NanoMTEB-Chinese": "NanoCMTEB",
    "NanoMTEB-Japanese": "NanoJMTEB",
    "NanoMTEB-Persian": "NanoFaMTEB",
    "NanoMTEB-Russian": "NanoRuMTEB",
    "NanoMTEB-Vietnamese": "NanoVNMTEB",
    "NanoMTEB-Xlingual": MISC_DATASET_NAME,
    "NanoMTEB-Polish": MISC_DATASET_NAME,
}

SPLIT_MOVES_TO_MISC: dict[str, set[str]] = {
    "NanoMTEB-Dutch": {
        "NanoCQADupstackAndroidNL",
        "NanoCQADupstackEnglishNL",
        "NanoCQADupstackGisNL",
        "NanoCQADupstackMathematicaNL",
        "NanoCQADupstackPhysicsNL",
        "NanoCQADupstackProgrammersNL",
        "NanoCQADupstackStatsNL",
        "NanoCQADupstackTexNL",
        "NanoCQADupstackWebmastersNL",
        "NanoCQADupstackWordpressNL",
        "NanoFEVERNL",
        "NanoNQNL",
        "NanoQuoraNL",
    },
    "NanoMTEB-French": {"NanoFQuAD"},
    "NanoMTEB-German": {"NanoGermanGovService"},
    "NanoMTEB-Korean": {"NanoAutoRAG", "NanoLawIRKo", "NanoSQuADKorV1"},
    "NanoMTEB-Persian": {"NanoNeuCLIR2023", "NanoNeuCLIR2023HardNegatives"},
    "NanoMTEB-Russian": {"NanoRuSciBenchCite", "NanoRuSciBenchCocite"},
    "NanoMTEB-Vietnamese": {"NanoNanoFEVERVN", "NanoNanoNQVN"},
}

@dataclass(frozen=True)
class DatasetTarget:
    name: str
    dataset_id: str


def canonical_target_for(*, dataset_name: str, dataset_id: str, split_name: str) -> DatasetTarget:
    source_name = dataset_name or _dataset_name_from_id(dataset_id)
    if split_name in SPLIT_MOVES_TO_MISC.get(source_name, set()):
        return DatasetTarget(name=MISC_DATASET_NAME, dataset_id=MISC_DATASET_ID)
    new_name = DATASET_RENAMES.get(source_name, source_name)
    return DatasetTarget(name=new_name, dataset_id=_dataset_id_for_name(new_name, fallback=dataset_id))


def migrate_results(
    *,
    results_dir: Path,
    dry_run: bool = False,
) -> list[str]:
    actions: list[str] = []
    for result_path in sorted(results_dir.glob("*/*/*.json")):
        payload = json.loads(result_path.read_text(encoding="utf-8"))
        target = payload.get("target")
        if not isinstance(target, dict):
            continue
        old_name = str(target.get("dataset_name") or "")
        old_id = str(target.get("dataset_id") or "")
        split_name = str(target.get("split_name") or target.get("task_name") or result_path.stem)
        new_target = canonical_target_for(dataset_name=old_name, dataset_id=old_id, split_name=split_name)
        if old_name != new_target.name or old_id != new_target.dataset_id:
            target["dataset_name"] = new_target.name
            target["dataset_id"] = new_target.dataset_id
            metadata = target.get("metadata")
            if isinstance(metadata, dict):
                description = metadata.get("description")
                if isinstance(description, str):
                    metadata["description"] = (
                        description.replace(old_name, new_target.name).replace(old_id, new_target.dataset_id)
                    )
            dest = result_path.parents[1] / safe_path_part(new_target.dataset_id) / result_path.name
            actions.append(f"move {result_path} -> {dest}")
            if not dry_run:
                _write_migrated_result(result_path=result_path, dest=dest, payload=payload)
    return actions


def _write_migrated_result(*, result_path: Path, dest: Path, payload: dict[str, Any]) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if dest.exists():
        existing = json.loads(dest.read_text(encoding="utf-8"))
        if existing != payload:
            raise RuntimeError(f"Refusing to overwrite divergent result: {dest}")
    dest.write_text(serialized, encoding="utf-8")
    if dest != result_path:
        result_path.unlink()
        _remove_empty_parents(result_path.parent)


def _remove_empty_parents(path: Path) -> None:
    while path.name and path.exists():
        try:
            path.rmdir()
        except OSError:
            return
        path = path.parent


def _dataset_name_from_id(dataset_id: str) -> str:
    return dataset_id.rstrip("/").split("/")[-1]


def _dataset_id_for_name(name: str, *, fallback: str) -> str:
    if name == _dataset_name_from_id(fallback):
        return fallback
    return f"hakari-bench/{name}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate NanoMTEB result JSON files to canonical dataset names.")
    parser.add_argument("--results-dir", type=Path, default=Path("output/results"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    actions = migrate_results(
        results_dir=args.results_dir,
        dry_run=args.dry_run,
    )
    for action in actions:
        print(action)


if __name__ == "__main__":
    main()
