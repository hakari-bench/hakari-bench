from __future__ import annotations

import argparse
import random
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


EXAMPLE_SECTION_RE = re.compile(r"(## Example Data\n\n).*?(?=\n## Dataset Information)", re.DOTALL)
METADATA_RE = re.compile(r"<!-- benchmark-task-metadata:v1 -->\s*```yaml\n(.*?)\n```", re.DOTALL)
DEFAULT_TEXT_LIMIT = 225
DEFAULT_SAMPLE_SIZE = 5
DEFAULT_SEED = 42


@dataclass(frozen=True)
class TaskReference:
    dataset_id: str
    split_name: str


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _first_present(row: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    raise KeyError(f"none of the expected keys are present: {', '.join(keys)}")


def _row_id(row: Mapping[str, Any]) -> str:
    return _as_text(_first_present(row, ("_id", "id", "query-id", "query_id", "corpus-id", "corpus_id")))


def _row_text(row: Mapping[str, Any]) -> str:
    text = _as_text(
        _first_present(
            row,
            (
                "text",
                "query",
                "question",
                "contents",
                "content",
                "document",
                "passage",
                "answer",
            ),
        )
    ).strip()
    title = _as_text(row.get("title")).strip()
    if title and text and not text.startswith(title):
        return f"{title}\n\n{text}"
    if title and not text:
        return title
    return text


def _qrel_query_id(row: Mapping[str, Any]) -> str:
    return _as_text(_first_present(row, ("query-id", "query_id", "qid", "query", "_id"))).strip()


def _qrel_corpus_id(row: Mapping[str, Any]) -> str:
    return _as_text(_first_present(row, ("corpus-id", "corpus_id", "docid", "document_id", "doc_id"))).strip()


def _is_positive_qrel(row: Mapping[str, Any]) -> bool:
    if "score" not in row or row["score"] is None:
        return True
    try:
        return float(row["score"]) > 0
    except (TypeError, ValueError):
        return True


def _normalize_visible_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _escape_markdown_cell(text: str) -> str:
    return text.replace("|", r"\|")


def format_example_text(text: str, *, text_limit: int = DEFAULT_TEXT_LIMIT) -> str:
    stripped = text.strip()
    full_chars = len(stripped)
    visible = _normalize_visible_text(stripped)
    if len(visible) > text_limit:
        visible = visible[:text_limit].rstrip()
        return _escape_markdown_cell(f"{visible} ... [truncated {text_limit} chars]({full_chars} chars)")
    return _escape_markdown_cell(f"{visible} ({full_chars} chars)")


def _materialize_by_id(rows: Iterable[Mapping[str, Any]]) -> dict[str, str]:
    return {_row_id(row): _row_text(row) for row in rows}


def _positive_docs_by_query(rows: Iterable[Mapping[str, Any]]) -> dict[str, list[str]]:
    positives: dict[str, list[str]] = {}
    for row in rows:
        if not _is_positive_qrel(row):
            continue
        positives.setdefault(_qrel_query_id(row), []).append(_qrel_corpus_id(row))
    return positives


def build_example_table(
    *,
    queries: Iterable[Mapping[str, Any]],
    corpus: Iterable[Mapping[str, Any]],
    qrels: Iterable[Mapping[str, Any]],
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    seed: int = DEFAULT_SEED,
    text_limit: int = DEFAULT_TEXT_LIMIT,
) -> str:
    queries_by_id = _materialize_by_id(queries)
    corpus_by_id = _materialize_by_id(corpus)
    positives_by_query = _positive_docs_by_query(qrels)
    eligible_query_ids = sorted(
        query_id
        for query_id, corpus_ids in positives_by_query.items()
        if query_id in queries_by_id and any(corpus_id in corpus_by_id for corpus_id in corpus_ids)
    )
    if not eligible_query_ids:
        raise ValueError("no query-positive pairs with matching query and corpus records were found")

    rng = random.Random(seed)
    selected_query_ids = rng.sample(eligible_query_ids, k=min(sample_size, len(eligible_query_ids)))

    lines = [
        "| Query | Positive document |",
        "| --- | --- |",
    ]
    for query_id in selected_query_ids:
        corpus_id = next(corpus_id for corpus_id in positives_by_query[query_id] if corpus_id in corpus_by_id)
        query_text = format_example_text(queries_by_id[query_id], text_limit=text_limit)
        document_text = format_example_text(corpus_by_id[corpus_id], text_limit=text_limit)
        lines.append(f"| {query_text} | {document_text} |")
    return "\n".join(lines)


def load_example_table(
    *,
    dataset_id: str,
    split_name: str,
    queries_config: str = "queries",
    corpus_config: str = "corpus",
    qrels_config: str = "qrels",
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    seed: int = DEFAULT_SEED,
    text_limit: int = DEFAULT_TEXT_LIMIT,
) -> str:
    queries = _load_dataset_split(dataset_id, queries_config, split_name)
    corpus = _load_dataset_split(dataset_id, corpus_config, split_name)
    qrels = _load_dataset_split(dataset_id, qrels_config, split_name)
    return build_example_table(
        queries=queries,
        corpus=corpus,
        qrels=qrels,
        sample_size=sample_size,
        seed=seed,
        text_limit=text_limit,
    )


@lru_cache(maxsize=None)
def _load_dataset_config(dataset_id: str, config_name: str) -> Any:
    from datasets import load_dataset

    return load_dataset(dataset_id, config_name)


def _load_dataset_split(dataset_id: str, config_name: str, split_name: str) -> Any:
    dataset = _load_dataset_config(dataset_id, config_name)
    try:
        return dataset[split_name]
    except KeyError as exc:
        available = ", ".join(str(split) for split in getattr(dataset, "keys", lambda: [])())
        raise KeyError(f"{dataset_id}/{config_name} does not contain split {split_name!r}; available: {available}") from exc


def _task_reference_from_doc(path: Path) -> TaskReference:
    text = path.read_text(encoding="utf-8")
    match = METADATA_RE.search(text)
    if not match:
        raise ValueError(f"missing benchmark task metadata: {path}")
    metadata = yaml.safe_load(match.group(1))
    task_metadata = metadata.get("benchmark_task_metadata") if isinstance(metadata, dict) else None
    if not isinstance(task_metadata, dict):
        raise ValueError(f"invalid benchmark task metadata: {path}")
    dataset_id = task_metadata.get("dataset_id")
    split_name = task_metadata.get("split_name") or task_metadata.get("task_name")
    if not dataset_id or not split_name:
        raise ValueError(f"metadata must include dataset_id and split_name: {path}")
    return TaskReference(dataset_id=str(dataset_id), split_name=str(split_name))


def _replace_example_section(text: str, table: str) -> str:
    updated, count = EXAMPLE_SECTION_RE.subn(lambda match: f"{match.group(1)}{table}\n", text, count=1)
    if count != 1:
        raise ValueError("expected exactly one Example Data section followed by Dataset Information")
    return updated


def update_docs(
    *,
    docs_root: Path,
    sample_size: int,
    seed: int,
    text_limit: int,
    dry_run: bool,
) -> list[Path]:
    changed: list[Path] = []
    task_docs = sorted(path for path in docs_root.rglob("*.md") if path.name != "index.md")
    for path in task_docs:
        text = path.read_text(encoding="utf-8")
        if "## Example Data" not in text:
            continue
        reference = _task_reference_from_doc(path)
        table = load_example_table(
            dataset_id=reference.dataset_id,
            split_name=reference.split_name,
            sample_size=sample_size,
            seed=seed,
            text_limit=text_limit,
        )
        updated = _replace_example_section(text, table)
        if updated == text:
            continue
        changed.append(path)
        if not dry_run:
            path.write_text(updated, encoding="utf-8")
    return changed


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract deterministic random query-positive examples from Nano benchmark datasets."
    )
    parser.add_argument("dataset_id", nargs="?", help="Hugging Face dataset id, such as hakari-bench/NanoMMTEB-v2.")
    parser.add_argument("split_name", nargs="?", help="Dataset split/task name, such as argu_ana.")
    parser.add_argument("--queries-config", default="queries")
    parser.add_argument("--corpus-config", default="corpus")
    parser.add_argument("--qrels-config", default="qrels")
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--text-limit", type=int, default=DEFAULT_TEXT_LIMIT)
    parser.add_argument("--update-docs", type=Path, help="Replace Example Data sections below this docs root.")
    parser.add_argument("--dry-run", action="store_true", help="Report changed files without writing them.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.sample_size <= 0:
        raise SystemExit("--sample-size must be positive")
    if args.text_limit <= 0:
        raise SystemExit("--text-limit must be positive")

    if args.update_docs:
        changed = update_docs(
            docs_root=args.update_docs,
            sample_size=args.sample_size,
            seed=args.seed,
            text_limit=args.text_limit,
            dry_run=args.dry_run,
        )
        action = "Would update" if args.dry_run else "Updated"
        for path in changed:
            print(path)
        print(f"{action} {len(changed)} files.", file=sys.stderr)
        return 0

    if not args.dataset_id or not args.split_name:
        raise SystemExit("dataset_id and split_name are required unless --update-docs is used")
    print(
        load_example_table(
            dataset_id=args.dataset_id,
            split_name=args.split_name,
            queries_config=args.queries_config,
            corpus_config=args.corpus_config,
            qrels_config=args.qrels_config,
            sample_size=args.sample_size,
            seed=args.seed,
            text_limit=args.text_limit,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
