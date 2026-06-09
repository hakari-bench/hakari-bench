from __future__ import annotations

import argparse
import json
import re
import tempfile
from collections.abc import Collection
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi, hf_hub_download

CONFIG_ORDER = ("corpus", "queries", "qrels", "bm25", "harrier_oss_v1_270m", "reranking_hybrid")


@dataclass(frozen=True)
class DatasetTarget:
    dataset_dir: Path
    repo_id: str


def main() -> None:
    parser = argparse.ArgumentParser(description="Push local reranking_hybrid Nano datasets to Hugging Face.")
    parser.add_argument("--output-root", type=Path, default=Path("output/nano_reranking_hybrid_20260525"))
    parser.add_argument("--only", action="append", default=[], help="Dataset directory name or repo id to push.")
    parser.add_argument("--resume-after", default=None, help="Skip datasets until this dataset directory name has passed.")
    parser.add_argument("--log-path", type=Path, default=Path("tmp/push_reranking_hybrid_nano_datasets_20260526.jsonl"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--readme-only", action="store_true", help="Only upload corrected README metadata.")
    args = parser.parse_args()

    targets = discover_targets(args.output_root)
    if args.only:
        only = set(args.only)
        targets = [target for target in targets if target.dataset_dir.name in only or target.repo_id in only]
    if args.resume_after:
        targets = skip_until_after(targets, args.resume_after)

    args.log_path.parent.mkdir(parents=True, exist_ok=True)
    for index, target in enumerate(targets, start=1):
        print(f"[{index}/{len(targets)}] {target.repo_id}", flush=True)
        if args.dry_run:
            log_event(args.log_path, target=target, status="dry_run")
            continue
        try:
            push_dataset(target, readme_only=args.readme_only)
        except Exception as exc:
            log_event(args.log_path, target=target, status="error", error=f"{type(exc).__name__}: {exc}")
            raise
        log_event(args.log_path, target=target, status="readme_ok" if args.readme_only else "ok")


def discover_targets(output_root: Path) -> list[DatasetTarget]:
    targets: list[DatasetTarget] = []
    for dataset_dir in sorted(path for path in output_root.iterdir() if path.is_dir()):
        metadata_path = dataset_dir / "reranking_hybrid_metadata.json"
        if not metadata_path.exists():
            continue
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        repo_id = str(metadata.get("source_dataset") or f"hakari-bench/{dataset_dir.name}")
        targets.append(DatasetTarget(dataset_dir=dataset_dir, repo_id=repo_id))
    return targets


def skip_until_after(targets: list[DatasetTarget], marker: str) -> list[DatasetTarget]:
    skipped = True
    remaining: list[DatasetTarget] = []
    for target in targets:
        if skipped:
            skipped = target.dataset_dir.name != marker and target.repo_id != marker
            continue
        remaining.append(target)
    return remaining


def push_dataset(target: DatasetTarget, *, readme_only: bool = False) -> None:
    api = HfApi()
    if not readme_only:
        for config_name in CONFIG_ORDER:
            config_dir = target.dataset_dir / config_name
            if not config_dir.exists():
                continue
            dataset_dict = dataset_dict_from_config(config_dir)
            dataset_dict.push_to_hub(
                target.repo_id,
                config_name=config_name,
                set_default=True if config_name == "queries" else None,
                commit_message=f"Update {config_name} for reranking_hybrid candidates",
            )

        api.upload_file(
            repo_id=target.repo_id,
            repo_type="dataset",
            path_or_fileobj=str(target.dataset_dir / "reranking_hybrid_metadata.json"),
            path_in_repo="reranking_hybrid_metadata.json",
            commit_message="Add reranking_hybrid metadata",
        )
    remote_files = api.list_repo_files(repo_id=target.repo_id, repo_type="dataset")
    readme = merged_readme_with_remote_frontmatter(target, remote_files=remote_files)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
        handle.write(readme)
        readme_path = Path(handle.name)
    try:
        api.upload_file(
            repo_id=target.repo_id,
            repo_type="dataset",
            path_or_fileobj=str(readme_path),
            path_in_repo="README.md",
            commit_message="Update dataset README for reranking_hybrid candidates",
        )
    finally:
        readme_path.unlink(missing_ok=True)


def dataset_dict_from_config(config_dir: Path) -> DatasetDict:
    dataset_dict = DatasetDict()
    for parquet_path in sorted(config_dir.glob("*.parquet")):
        dataset_dict[parquet_path.stem] = Dataset.from_parquet(str(parquet_path))
    return dataset_dict


def merged_readme_with_remote_frontmatter(
    target: DatasetTarget,
    *,
    remote_files: Collection[str] | None = None,
) -> str:
    local_text = (target.dataset_dir / "README.md").read_text(encoding="utf-8")
    local_body = split_card(local_text)[1]
    remote_text = download_remote_readme(target.repo_id)
    remote_frontmatter, _remote_body = split_card(remote_text)
    local_frontmatter, _ = split_card(local_text)
    if remote_files is None:
        remote_files = HfApi().list_repo_files(repo_id=target.repo_id, repo_type="dataset")
    merged = merge_frontmatter(remote_frontmatter, local_frontmatter, remote_files=remote_files)
    return "---\n" + yaml.safe_dump(merged, sort_keys=False, allow_unicode=True).rstrip() + "\n---\n" + local_body


def download_remote_readme(repo_id: str) -> str:
    path = hf_hub_download(repo_id=repo_id, repo_type="dataset", filename="README.md")
    return Path(path).read_text(encoding="utf-8")


def split_card(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", maxsplit=2)
    if len(parts) != 3:
        return {}, text
    parsed = yaml.safe_load(parts[1]) or {}
    frontmatter = parsed if isinstance(parsed, dict) else {}
    return frontmatter, parts[2].lstrip()


def merge_frontmatter(
    remote: dict[str, Any],
    local: dict[str, Any],
    *,
    remote_files: Collection[str] | None = None,
) -> dict[str, Any]:
    merged = dict(remote)
    for key in ("configs", "language", "tags"):
        if key in local:
            merged[key] = local[key]
    if "configs" in merged:
        merged = rewrite_data_file_paths_for_push_to_hub(merged, remote_files=remote_files)
    return merged


def rewrite_data_file_paths_for_push_to_hub(
    frontmatter: dict[str, Any],
    *,
    remote_files: Collection[str] | None = None,
) -> dict[str, Any]:
    rewritten = dict(frontmatter)
    configs = frontmatter.get("configs")
    if not isinstance(configs, list):
        return rewritten

    rewritten_configs: list[Any] = []
    for config in configs:
        if not isinstance(config, dict):
            rewritten_configs.append(config)
            continue
        rewritten_config = dict(config)
        data_files = config.get("data_files")
        if isinstance(data_files, list):
            rewritten_config["data_files"] = [
                _rewrite_data_file_entry_for_push_to_hub(entry, remote_files=remote_files) for entry in data_files
            ]
        rewritten_configs.append(rewritten_config)
    rewritten["configs"] = rewritten_configs
    return rewritten


def _rewrite_data_file_entry_for_push_to_hub(
    entry: Any,
    *,
    remote_files: Collection[str] | None,
) -> Any:
    if not isinstance(entry, dict):
        return entry
    path = entry.get("path")
    if not isinstance(path, str) or not path.endswith(".parquet"):
        return dict(entry)
    path_obj = Path(path)
    if remote_files is not None:
        matches = _remote_shard_paths(path_obj, remote_files)
        if matches:
            rewritten = dict(entry)
            rewritten["path"] = matches[0] if len(matches) == 1 else matches
            return rewritten
    if _SHARD_SUFFIX_RE.search(path_obj.stem):
        return dict(entry)
    rewritten = dict(entry)
    rewritten["path"] = str(path_obj.with_name(f"{path_obj.stem}-00000-of-00001{path_obj.suffix}"))
    return rewritten


_SHARD_SUFFIX_RE = re.compile(r"-\d{5}-of-\d{5}$")


def _remote_shard_paths(path: Path, remote_files: Collection[str]) -> list[str]:
    stem = _SHARD_SUFFIX_RE.sub("", path.stem)
    prefix = f"{path.parent.as_posix()}/{stem}-"
    return sorted(
        remote_path
        for remote_path in remote_files
        if remote_path.startswith(prefix)
        and remote_path.endswith(path.suffix)
        and _SHARD_SUFFIX_RE.search(Path(remote_path).stem)
    )


def log_event(log_path: Path, *, target: DatasetTarget, status: str, error: str | None = None) -> None:
    event = {"dataset": target.dataset_dir.name, "repo_id": target.repo_id, "status": status}
    if error is not None:
        event["error"] = error
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
