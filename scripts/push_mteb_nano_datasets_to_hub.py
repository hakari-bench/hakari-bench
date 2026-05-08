from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path

from huggingface_hub import HfApi


COMPONENTS = ("corpus", "queries", "qrels", "bm25")

OLD_REPLACED_REPOS = {
    "hakari-bench/NanoMMTEB",
    "hakari-bench/NanoMTEB",
    "hakari-bench/NanoMTEB-Chinese",
    "hakari-bench/NanoMTEB-Dutch",
    "hakari-bench/NanoMTEB-French",
    "hakari-bench/NanoMTEB-German",
    "hakari-bench/NanoMTEB-Japanese",
    "hakari-bench/NanoMTEB-Korean",
    "hakari-bench/NanoMTEB-Persian",
    "hakari-bench/NanoMTEB-Polish",
    "hakari-bench/NanoMTEB-Russian",
    "hakari-bench/NanoMTEB-Scandinavian",
    "hakari-bench/NanoMTEB-Spanish",
    "hakari-bench/NanoMTEB-Thai",
    "hakari-bench/NanoMTEB-Vietnamese",
    "hakari-bench/NanoMTEB-Xlingual",
}

EXCLUDED_REPOS = {
    "hakari-bench/NanoBEIR-ar",
    "hakari-bench/NanoBEIR-de",
    "hakari-bench/NanoBEIR-en",
    "hakari-bench/NanoBEIR-es",
    "hakari-bench/NanoBEIR-fr",
    "hakari-bench/NanoBEIR-it",
    "hakari-bench/NanoBEIR-ja",
    "hakari-bench/NanoBEIR-ko",
    "hakari-bench/NanoBEIR-no",
    "hakari-bench/NanoBEIR-pt",
    "hakari-bench/NanoBEIR-sr",
    "hakari-bench/NanoBEIR-sv",
    "hakari-bench/NanoBEIR-th",
    "hakari-bench/NanoBEIR-vi",
    "hakari-bench/NanoMIRACL",
    "hakari-bench/NanoMLDR",
    "hakari-bench/NanoRTEB",
    "hakari-bench/NanoCoIR",
    "hakari-bench/NanoLongEmbed",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replace regrouped NanoMTEB-family datasets on Hugging Face Hub.")
    parser.add_argument("--output-root", type=Path, default=Path("output/nano_datasets"))
    parser.add_argument("--org", default="hakari-bench")
    parser.add_argument("--delete", action="store_true", help="Delete replaced Hub datasets before uploading.")
    parser.add_argument("--upload", action="store_true", help="Upload regenerated datasets as private repos.")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned actions without mutating the Hub.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api = HfApi()
    groups = sorted(path.name for path in args.output_root.iterdir() if path.is_dir() and path.name.startswith("Nano"))
    target_repos = {f"{args.org}/{group}" for group in groups}
    delete_repos = sorted((target_repos | OLD_REPLACED_REPOS) - EXCLUDED_REPOS)

    print("target upload repos:")
    for repo_id in sorted(target_repos):
        print(f"  {repo_id}")
    print("delete repos:")
    for repo_id in delete_repos:
        print(f"  {repo_id}")

    if args.dry_run:
        return
    if args.delete:
        for repo_id in delete_repos:
            print(f"[delete] {repo_id}", flush=True)
            api.delete_repo(repo_id=repo_id, repo_type="dataset", missing_ok=True)
    if args.upload:
        for group in groups:
            repo_id = f"{args.org}/{group}"
            print(f"[create] {repo_id}", flush=True)
            api.create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True)
            _push_group(
                api=api,
                group_dir=args.output_root / group,
                repo_id=repo_id,
            )


def _push_group(*, api: HfApi, group_dir: Path, repo_id: str) -> None:
    split_index = _split_index(group_dir)
    hub_splits = _hub_split_mapping(split_index)
    with tempfile.TemporaryDirectory(prefix=f"{group_dir.name}-hub-metadata-") as tmp:
        staging = Path(tmp)
        for component in COMPONENTS:
            component_dir = staging / component
            component_dir.mkdir(parents=True, exist_ok=True)
            for split, components in sorted(split_index.items()):
                hub_split = hub_splits[split]
                shutil.copy2(components[component], component_dir / f"{hub_split}-00000-of-00001.parquet")
        _write_hub_readme(
            staging / "README.md",
            group_dir=group_dir,
            repo_id=repo_id,
            split_index=split_index,
            hub_splits=hub_splits,
        )
        _write_flat_metadata(staging / "metadata", split_index=split_index, hub_splits=hub_splits)
        for filename in ("audit.json",):
            source = group_dir / filename
            if source.exists():
                shutil.copy2(source, staging / filename)
        print(f"[push] {repo_id} files={sum(1 for path in staging.rglob('*') if path.is_file())}", flush=True)
        api.upload_folder(
            folder_path=staging,
            repo_id=repo_id,
            repo_type="dataset",
            commit_message=f"Upload regenerated {group_dir.name}",
        )


def _split_index(group_dir: Path) -> dict[str, dict[str, Path]]:
    index: dict[str, dict[str, Path]] = defaultdict(dict)
    for subset_dir in sorted(path for path in group_dir.iterdir() if path.is_dir()):
        for component in (*COMPONENTS, "metadata"):
            component_dir = subset_dir / component
            if not component_dir.exists():
                continue
            suffix = ".json" if component == "metadata" else ".parquet"
            for path in sorted(component_dir.glob(f"*{suffix}")):
                index[path.stem][component] = path
    missing = [
        (split, component)
        for split, components in sorted(index.items())
        for component in (*COMPONENTS, "metadata")
        if component not in components
    ]
    if missing:
        raise ValueError(f"Missing component files under {group_dir}: {missing[:20]}")
    return dict(index)


def _hub_split_mapping(split_index: dict[str, dict[str, Path]]) -> dict[str, str]:
    mapping = {split: re.sub(r"\W", "_", split) for split in split_index}
    reverse: dict[str, str] = {}
    collisions: list[tuple[str, str, str]] = []
    for original, hub_split in mapping.items():
        previous = reverse.setdefault(hub_split, original)
        if previous != original:
            collisions.append((hub_split, previous, original))
    if collisions:
        raise ValueError(f"Hub split name collisions after sanitization: {collisions[:20]}")
    return mapping


def _write_flat_metadata(
    metadata_dir: Path,
    *,
    split_index: dict[str, dict[str, Path]],
    hub_splits: dict[str, str],
) -> None:
    metadata_dir.mkdir(parents=True, exist_ok=True)
    for split, components in sorted(split_index.items()):
        metadata = json.loads(components["metadata"].read_text(encoding="utf-8"))
        metadata["original_nano_split"] = split
        metadata["hub_split"] = hub_splits[split]
        (metadata_dir / f"{hub_splits[split]}.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def _write_hub_readme(
    path: Path,
    *,
    group_dir: Path,
    repo_id: str,
    split_index: dict[str, dict[str, Path]],
    hub_splits: dict[str, str],
) -> None:
    rows = []
    source_links: list[str] = []
    for split, components in sorted(split_index.items()):
        metadata = json.loads(components["metadata"].read_text(encoding="utf-8"))
        source_dataset_id = str(metadata.get("source_dataset_id") or "")
        source_task = str(metadata.get("source_task") or split)
        queries = int(metadata.get("queries") or 0)
        corpus = int(metadata.get("corpus") or 0)
        qrels = int(metadata.get("qrels") or 0)
        source_link = _hf_dataset_link(source_dataset_id)
        if source_dataset_id:
            source_links.append(source_link)
        rows.append(
            f"| {hub_splits[split]} | {split} | {source_task} | {source_link} | {queries} | {corpus} | {qrels} |"
        )

    configs = []
    for component in COMPONENTS:
        files = [
            {"split": hub_splits[split], "path": f"{component}/{hub_splits[split]}-00000-of-00001.parquet"}
            for split in sorted(split_index)
        ]
        configs.append({"config_name": component, "data_files": files, **({"default": True} if component == "queries" else {})})

    frontmatter = {
        "configs": configs,
        "tags": ["information-retrieval", "retrieval", "nano", "bm25", "hakari-bench"],
    }
    source_links = list(dict.fromkeys(source_links))
    source_link_lines = "\n".join(f"- {link}" for link in source_links)
    split_rows = "\n".join(rows)
    group = group_dir.name
    path.write_text(
        "---\n"
        + json.dumps(frontmatter, ensure_ascii=False, indent=2)
        + "\n---\n\n"
        + f"# {group}\n\n"
        + "This is a private regenerated Nano-style retrieval dataset for HAKARI-Bench.\n\n"
        + "## Source Links\n\n"
        + source_link_lines
        + "\n\n"
        + "## Data Layout\n\n"
        + "The dataset uses four Hugging Face Datasets configs: `corpus`, `queries`, `qrels`, and `bm25`. "
        + "Each config contains the same Hub split names. Hub split names replace unsupported characters in "
        + "the original Nano split names with underscores; the original split names are listed below and stored "
        + "in `metadata/{hub_split}.json`.\n\n"
        + "## Split Mapping\n\n"
        + "| Hub split | Original Nano split | Source task | Source dataset | Queries | Corpus | Qrels |\n"
        + "|---|---|---|---|---:|---:|---:|\n"
        + split_rows
        + "\n\n"
        + "## License\n\n"
        + f"{group} is a derived dataset. Users must comply with the licenses, terms, "
        + "and attribution requirements of the upstream MTEB task sources and their original datasets.\n",
        encoding="utf-8",
    )


def _hf_dataset_link(dataset_id: str) -> str:
    if not dataset_id:
        return "unknown"
    return f"[{dataset_id}](https://huggingface.co/datasets/{dataset_id})"


if __name__ == "__main__":
    main()
