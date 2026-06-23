from __future__ import annotations

import argparse
import random
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from functools import lru_cache
from pathlib import Path
from typing import Any

from hakari_bench.task_docs import (
    TASK_METADATA_RE,
    TaskMetadataDocument,
    load_task_metadata,
    load_task_metadata_document,
    task_metadata_json_path,
)


EXAMPLE_SECTION_RE = re.compile(
    r"(## Example Data\n\n).*?(?=\n#{2,3} Public Sources|\n#{2,3} Hugging Face Links|\n#{2,3} Source Reference Table|\n## Dataset Information|\Z)",
    re.DOTALL,
)
METADATA_RE = TASK_METADATA_RE
DEFAULT_QUERY_TEXT_LIMIT = 100
DEFAULT_DOCUMENT_TEXT_LIMIT = 200
DEFAULT_SAMPLE_SIZE = 5
DEFAULT_SEED = 42


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


def truncate_example_text(text: str, *, text_limit: int) -> dict[str, Any]:
    stripped = text.strip()
    visible = _normalize_visible_text(stripped)
    truncated = len(visible) > text_limit
    if truncated:
        visible = visible[:text_limit].rstrip()
    return {
        "text": visible,
        "full_chars": len(stripped),
        "limit_chars": text_limit,
        "truncated": truncated,
    }


def format_example_text(text: str, *, text_limit: int) -> str:
    item = truncate_example_text(text, text_limit=text_limit)
    return format_example_text_metadata(item)


def format_example_text_metadata(item: Mapping[str, Any]) -> str:
    text = _as_text(item["text"])
    full_chars = int(item["full_chars"])
    limit_chars = int(item["limit_chars"])
    if item.get("truncated"):
        return _escape_markdown_cell(f"{text}... [{limit_chars:,} / {full_chars:,} chars]")
    return _escape_markdown_cell(f"{text} [{full_chars:,} chars]")


def build_example_metadata(
    *,
    queries: Iterable[Mapping[str, Any]],
    corpus: Iterable[Mapping[str, Any]],
    qrels: Iterable[Mapping[str, Any]],
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    seed: int = DEFAULT_SEED,
    query_text_limit: int = DEFAULT_QUERY_TEXT_LIMIT,
    document_text_limit: int = DEFAULT_DOCUMENT_TEXT_LIMIT,
) -> list[dict[str, Any]]:
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

    examples: list[dict[str, Any]] = []
    for query_id in selected_query_ids:
        corpus_id = next(corpus_id for corpus_id in positives_by_query[query_id] if corpus_id in corpus_by_id)
        examples.append(
            {
                "query_id": query_id,
                "document_id": corpus_id,
                "query": truncate_example_text(queries_by_id[query_id], text_limit=query_text_limit),
                "positive_document": truncate_example_text(corpus_by_id[corpus_id], text_limit=document_text_limit),
            }
        )
    return examples


def render_example_table(examples: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| Query | Positive document |",
        "| --- | --- |",
    ]
    for example in examples:
        query_text = format_example_text_metadata(example["query"])
        document_text = format_example_text_metadata(example["positive_document"])
        lines.append(f"| {query_text} | {document_text} |")
    return "\n".join(lines)


def load_example_metadata(
    *,
    dataset_id: str,
    split_name: str,
    queries_config: str = "queries",
    corpus_config: str = "corpus",
    qrels_config: str = "qrels",
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    seed: int = DEFAULT_SEED,
    query_text_limit: int = DEFAULT_QUERY_TEXT_LIMIT,
    document_text_limit: int = DEFAULT_DOCUMENT_TEXT_LIMIT,
) -> list[dict[str, Any]]:
    queries = _load_dataset_split(dataset_id, queries_config, split_name)
    corpus = _load_dataset_split(dataset_id, corpus_config, split_name)
    qrels = _load_dataset_split(dataset_id, qrels_config, split_name)
    return build_example_metadata(
        queries=queries,
        corpus=corpus,
        qrels=qrels,
        sample_size=sample_size,
        seed=seed,
        query_text_limit=query_text_limit,
        document_text_limit=document_text_limit,
    )


def _materialize_by_id(rows: Iterable[Mapping[str, Any]]) -> dict[str, str]:
    return {_row_id(row): _row_text(row) for row in rows}


def _positive_docs_by_query(rows: Iterable[Mapping[str, Any]]) -> dict[str, list[str]]:
    positives: dict[str, list[str]] = {}
    for row in rows:
        if not _is_positive_qrel(row):
            continue
        positives.setdefault(_qrel_query_id(row), []).append(_qrel_corpus_id(row))
    return positives


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


def _replace_example_section(text: str, table: str) -> str:
    updated, count = EXAMPLE_SECTION_RE.subn(lambda match: f"{match.group(1)}{table}\n", text, count=1)
    if count != 1:
        raise ValueError("expected exactly one Example Data section followed by Dataset Information")
    return updated


def update_docs(
    *,
    docs_root: Path,
    metadata_root: Path,
    sample_size: int,
    seed: int,
    query_text_limit: int,
    document_text_limit: int,
    dry_run: bool,
) -> list[Path]:
    changed: list[Path] = []
    task_docs = sorted(path for path in docs_root.rglob("*.md") if path.name != "index.md")
    for path in task_docs:
        text = path.read_text(encoding="utf-8")
        if "## Example Data" not in text:
            continue
        metadata = load_task_metadata(path, docs_root=docs_root, metadata_root=metadata_root)
        examples = [example.model_dump() for example in metadata.examples or []]
        if not examples:
            examples = load_example_metadata(
                dataset_id=metadata.dataset_id,
                split_name=metadata.split_name or metadata.task_name,
                sample_size=sample_size,
                seed=seed,
                query_text_limit=query_text_limit,
                document_text_limit=document_text_limit,
            )
        table = render_example_table(examples)
        updated = _replace_example_section(text, table)
        if updated == text:
            continue
        changed.append(path)
        if not dry_run:
            path.write_text(updated, encoding="utf-8")
    return changed


def update_metadata(
    *,
    docs_root: Path,
    metadata_root: Path,
    sample_size: int,
    seed: int,
    query_text_limit: int,
    document_text_limit: int,
    dry_run: bool,
) -> list[Path]:
    changed: list[Path] = []
    task_docs = sorted(path for path in docs_root.rglob("*.md") if path.name != "index.md")
    for path in task_docs:
        document = load_task_metadata_document(path, docs_root=docs_root, metadata_root=metadata_root)
        metadata = document.task_metadata
        examples = load_example_metadata(
            dataset_id=metadata.dataset_id,
            split_name=metadata.split_name or metadata.task_name,
            sample_size=sample_size,
            seed=seed,
            query_text_limit=query_text_limit,
            document_text_limit=document_text_limit,
        )
        metadata_payload = metadata.model_dump(mode="python", exclude_none=True)
        metadata_payload["examples"] = examples
        metadata_payload["example_count"] = len(examples)
        updated_document = TaskMetadataDocument.model_validate({"task_metadata": metadata_payload})
        output_path = task_metadata_json_path(path, docs_root=docs_root, metadata_root=metadata_root)
        payload = updated_document.model_dump_json(indent=2, exclude_none=True) + "\n"
        if output_path.exists() and output_path.read_text(encoding="utf-8") == payload:
            continue
        changed.append(output_path)
        if not dry_run:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(payload, encoding="utf-8")
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
    parser.add_argument("--query-text-limit", type=int, default=DEFAULT_QUERY_TEXT_LIMIT)
    parser.add_argument("--document-text-limit", type=int, default=DEFAULT_DOCUMENT_TEXT_LIMIT)
    parser.add_argument("--metadata-root", type=Path, default=Path("task_docs/metadata"))
    parser.add_argument("--update-metadata", type=Path, help="Refresh example metadata JSON below this docs root.")
    parser.add_argument("--update-docs", type=Path, help="Replace Example Data sections below this docs root.")
    parser.add_argument("--dry-run", action="store_true", help="Report changed files without writing them.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.sample_size <= 0:
        raise SystemExit("--sample-size must be positive")
    if args.query_text_limit <= 0:
        raise SystemExit("--query-text-limit must be positive")
    if args.document_text_limit <= 0:
        raise SystemExit("--document-text-limit must be positive")

    if args.update_metadata:
        changed = update_metadata(
            docs_root=args.update_metadata,
            metadata_root=args.metadata_root,
            sample_size=args.sample_size,
            seed=args.seed,
            query_text_limit=args.query_text_limit,
            document_text_limit=args.document_text_limit,
            dry_run=args.dry_run,
        )
        action = "Would update" if args.dry_run else "Updated"
        for path in changed:
            print(path)
        print(f"{action} {len(changed)} metadata files.", file=sys.stderr)
        return 0

    if args.update_docs:
        changed = update_docs(
            docs_root=args.update_docs,
            metadata_root=args.metadata_root,
            sample_size=args.sample_size,
            seed=args.seed,
            query_text_limit=args.query_text_limit,
            document_text_limit=args.document_text_limit,
            dry_run=args.dry_run,
        )
        action = "Would update" if args.dry_run else "Updated"
        for path in changed:
            print(path)
        print(f"{action} {len(changed)} files.", file=sys.stderr)
        return 0

    if not args.dataset_id or not args.split_name:
        raise SystemExit("dataset_id and split_name are required unless --update-metadata or --update-docs is used")
    print(
        render_example_table(
            load_example_metadata(
                dataset_id=args.dataset_id,
                split_name=args.split_name,
                queries_config=args.queries_config,
                corpus_config=args.corpus_config,
                qrels_config=args.qrels_config,
                sample_size=args.sample_size,
                seed=args.seed,
                query_text_limit=args.query_text_limit,
                document_text_limit=args.document_text_limit,
            )
        )
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
