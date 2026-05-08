from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
import yaml
from datasets import Dataset, load_dataset

from hakari_bench.bm25 import BM25Config, bm25_config_payload, rank_bm25_candidates, rankings_to_candidate_rows
from hakari_bench.metrics import compute_ir_metrics


DEFAULT_QUERY_LIMIT = 200
DEFAULT_DOC_LIMIT = 10_000
DEFAULT_BM25_TOP_K = 100
NANO_CONFIGS = ("bm25", "corpus", "qrels", "queries")
_README_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "docs" / "NanoREADME.template.md"

_CORPUS_ID_COLUMNS = ("_id", "id", "docid", "doc_id", "corpus-id", "corpus_id", "document_id")
_QUERY_ID_COLUMNS = ("_id", "id", "qid", "query-id", "query_id")
_QRELS_QUERY_ID_COLUMNS = ("query-id", "query_id", "qid", "query")
_QRELS_CORPUS_ID_COLUMNS = ("corpus-id", "corpus_id", "doc-id", "doc_id", "docid", "document_id")
_QUERY_TEXT_COLUMNS = ("text", "query", "question")
_CORPUS_TEXT_COLUMNS = ("text", "document", "contents", "content", "body", "passage")
_SCORE_COLUMNS = ("score", "relevance", "label")


@dataclass(frozen=True)
class SourceTables:
    corpus_rows: list[dict[str, Any]]
    query_rows: list[dict[str, Any]]
    qrels_rows: list[dict[str, Any]]


@dataclass(frozen=True)
class NanoBuildResult:
    dataset_name: str
    dataset_id: str
    split_name: str
    output_dir: Path
    dataset_config_path: Path | None
    queries: int
    corpus: int
    qrels: int
    source_positive_qrels: int
    source_non_positive_qrels: int
    forced_queries: int
    forced_doc_count: int
    missing_positive_doc_count_after_forcing: int
    bm25_ndcg_at_10: float


def _first_present(row: Mapping[str, Any], columns: Iterable[str], *, row_name: str) -> Any:
    for column in columns:
        if column in row and row[column] is not None:
            return row[column]
    raise ValueError(f"{row_name} row is missing one of columns {list(columns)}: {row}")


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _corpus_text(row: Mapping[str, Any]) -> str:
    title = _clean_text(row.get("title"))
    body = ""
    for column in _CORPUS_TEXT_COLUMNS:
        if column in row:
            body = _clean_text(row[column])
            break
    if title and body and title != body:
        return f"{title}\n\n{body}"
    return body or title


def _query_text(row: Mapping[str, Any]) -> str:
    for column in _QUERY_TEXT_COLUMNS:
        if column in row:
            text = _clean_text(row[column])
            if text:
                return text
    raise ValueError(f"query row is missing a usable text column: {row}")


def _score(row: Mapping[str, Any]) -> float:
    for column in _SCORE_COLUMNS:
        if column in row and row[column] is not None:
            return float(row[column])
    return 1.0


def normalize_corpus_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for row in rows:
        corpus_id = str(_first_present(row, _CORPUS_ID_COLUMNS, row_name="corpus"))
        text = _corpus_text(row)
        if corpus_id and text:
            normalized.append({"_id": corpus_id, "text": text})
    return normalized


def normalize_query_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for row in rows:
        query_id = str(_first_present(row, _QUERY_ID_COLUMNS, row_name="query"))
        text = _query_text(row)
        if query_id and text:
            normalized.append({"_id": query_id, "text": text})
    return normalized


def normalize_qrels_rows(rows: Iterable[Mapping[str, Any]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    positives: list[dict[str, str]] = []
    non_positives: list[dict[str, str]] = []
    seen_positives: set[tuple[str, str]] = set()
    seen_non_positives: set[tuple[str, str]] = set()
    for row in rows:
        query_id = str(_first_present(row, _QRELS_QUERY_ID_COLUMNS, row_name="qrels"))
        corpus_id = str(_first_present(row, _QRELS_CORPUS_ID_COLUMNS, row_name="qrels"))
        key = (query_id, corpus_id)
        if _score(row) > 0:
            if key not in seen_positives:
                seen_positives.add(key)
                positives.append({"query-id": query_id, "corpus-id": corpus_id})
        elif key not in seen_non_positives:
            seen_non_positives.add(key)
            non_positives.append({"query-id": query_id, "corpus-id": corpus_id})
    return positives, non_positives


def _rows_by_id(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["_id"]: row for row in rows}


def _select_queries(
    *,
    queries: list[dict[str, str]],
    positive_qrels: list[dict[str, str]],
    corpus_by_id: Mapping[str, dict[str, str]],
    query_limit: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    positive_by_query: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in positive_qrels:
        if row["corpus-id"] in corpus_by_id:
            positive_by_query[row["query-id"]].append(row)

    selected_queries: list[dict[str, str]] = []
    selected_qids: set[str] = set()
    seen_query_texts: set[str] = set()
    skipped_without_qrels = 0
    skipped_duplicate_text = 0
    for row in queries:
        query_id = row["_id"]
        if query_id not in positive_by_query:
            skipped_without_qrels += 1
            continue
        if row["text"] in seen_query_texts:
            skipped_duplicate_text += 1
            continue
        selected_queries.append(row)
        selected_qids.add(query_id)
        seen_query_texts.add(row["text"])
        if len(selected_queries) >= query_limit:
            break

    selected_qrels = [row for row in positive_qrels if row["query-id"] in selected_qids]
    return selected_queries, selected_qrels, {
        "skipped_queries_without_positive_qrels": skipped_without_qrels,
        "skipped_duplicate_query_texts": skipped_duplicate_text,
    }


def _round_robin_hard_negative_ids(rows: list[dict[str, str]], *, selected_qids: set[str]) -> list[str]:
    by_query: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        query_id = row["query-id"]
        if query_id not in selected_qids:
            continue
        corpus_id = row["corpus-id"]
        if corpus_id not in by_query[query_id]:
            by_query[query_id].append(corpus_id)

    output: list[str] = []
    index = 0
    query_ids = sorted(by_query)
    while True:
        added = False
        for query_id in query_ids:
            values = by_query[query_id]
            if index < len(values):
                output.append(values[index])
                added = True
        if not added:
            break
        index += 1
    return output


def _select_corpus(
    *,
    corpus: list[dict[str, str]],
    selected_qrels: list[dict[str, str]],
    non_positive_qrels: list[dict[str, str]],
    doc_limit: int,
) -> tuple[list[dict[str, str]], dict[str, int | str]]:
    corpus_by_id = _rows_by_id(corpus)
    selected_qids = {row["query-id"] for row in selected_qrels}
    positive_doc_ids = [row["corpus-id"] for row in selected_qrels]
    hard_negative_doc_ids = _round_robin_hard_negative_ids(non_positive_qrels, selected_qids=selected_qids)

    selected: list[dict[str, str]] = []
    selected_ids: set[str] = set()
    seen_texts: set[str] = set()
    duplicate_doc_texts_removed = 0
    kept_hard_negatives = 0

    def add_doc(doc_id: str, *, hard_negative: bool = False) -> None:
        nonlocal duplicate_doc_texts_removed, kept_hard_negatives
        if len(selected) >= doc_limit or doc_id in selected_ids:
            return
        row = corpus_by_id.get(doc_id)
        if row is None:
            return
        text = row["text"]
        if text in seen_texts:
            duplicate_doc_texts_removed += 1
            return
        selected.append(row)
        selected_ids.add(doc_id)
        seen_texts.add(text)
        if hard_negative:
            kept_hard_negatives += 1

    for doc_id in positive_doc_ids:
        add_doc(doc_id)
    for doc_id in hard_negative_doc_ids:
        add_doc(doc_id, hard_negative=True)
    for row in corpus:
        add_doc(row["_id"])

    return selected, {
        "positive_doc_count": len(set(positive_doc_ids)),
        "source_hard_negative_doc_candidates": len(set(hard_negative_doc_ids)),
        "kept_hard_negative_docs": kept_hard_negatives,
        "duplicate_doc_texts_removed": duplicate_doc_texts_removed,
        "hard_negative_sampling_policy": "query_round_robin",
    }


def force_qrels_positives_into_rankings(
    *,
    rankings: dict[str, list[str]],
    qrels: dict[str, set[str]],
    top_k: int,
) -> tuple[dict[str, list[str]], dict[str, int]]:
    forced_queries = 0
    forced_doc_count = 0
    output: dict[str, list[str]] = {}
    for query_id, candidates in rankings.items():
        positives = list(qrels.get(query_id, set()))
        current = [doc_id for doc_id in candidates[:top_k]]
        seen = set(current)
        missing = [doc_id for doc_id in positives if doc_id not in seen]
        if missing:
            forced_queries += 1
            forced_doc_count += len(missing)
        for doc_id in missing:
            replaced = False
            for index in range(len(current) - 1, -1, -1):
                if current[index] not in positives:
                    seen.discard(current[index])
                    current[index] = doc_id
                    seen.add(doc_id)
                    replaced = True
                    break
            if not replaced and len(current) < top_k:
                current.append(doc_id)
                seen.add(doc_id)
        if len(current) != len(set(current)):
            raise RuntimeError(f"duplicate BM25 candidates for query {query_id}")
        output[query_id] = current[:top_k]

    missing_after = 0
    for query_id, positives in qrels.items():
        candidate_set = set(output.get(query_id, []))
        missing_after += sum(1 for doc_id in positives if doc_id not in candidate_set)
    return output, {
        "forced_queries": forced_queries,
        "forced_doc_count": forced_doc_count,
        "missing_positive_doc_count_after_forcing": missing_after,
    }


def build_nano_dataset_from_rows(
    *,
    output_dir: Path,
    dataset_name: str,
    dataset_id: str,
    split_name: str,
    corpus_rows: Iterable[Mapping[str, Any]],
    query_rows: Iterable[Mapping[str, Any]],
    qrels_rows: Iterable[Mapping[str, Any]],
    dataset_config_dir: Path | None = None,
    query_limit: int = DEFAULT_QUERY_LIMIT,
    doc_limit: int = DEFAULT_DOC_LIMIT,
    bm25_config: BM25Config | None = None,
    metadata: dict[str, Any] | None = None,
) -> NanoBuildResult:
    if query_limit <= 0:
        raise ValueError("query_limit must be positive.")
    if doc_limit <= 0:
        raise ValueError("doc_limit must be positive.")

    corpus = normalize_corpus_rows(corpus_rows)
    queries = normalize_query_rows(query_rows)
    positive_qrels, non_positive_qrels = normalize_qrels_rows(qrels_rows)
    selected_queries, selected_qrels, query_metadata = _select_queries(
        queries=queries,
        positive_qrels=positive_qrels,
        corpus_by_id=_rows_by_id(corpus),
        query_limit=query_limit,
    )
    selected_corpus, corpus_metadata = _select_corpus(
        corpus=corpus,
        selected_qrels=selected_qrels,
        non_positive_qrels=non_positive_qrels,
        doc_limit=doc_limit,
    )
    selected_query_ids = {row["_id"] for row in selected_queries}
    selected_doc_ids = {row["_id"] for row in selected_corpus}
    selected_qrels = [
        row for row in selected_qrels if row["query-id"] in selected_query_ids and row["corpus-id"] in selected_doc_ids
    ]
    if not selected_queries or not selected_corpus or not selected_qrels:
        raise ValueError("selected Nano split must contain queries, corpus, and positive qrels.")

    query_map = {row["_id"]: row["text"] for row in selected_queries}
    corpus_map = {row["_id"]: row["text"] for row in selected_corpus}
    qrels_map = _qrels_mapping(selected_qrels)
    resolved_bm25 = bm25_config or BM25Config(tokenizer="regex", top_k=DEFAULT_BM25_TOP_K)
    raw_rankings = rank_bm25_candidates(corpus=corpus_map, queries=query_map, config=resolved_bm25)
    rankings, forcing_metadata = force_qrels_positives_into_rankings(
        rankings=raw_rankings,
        qrels=qrels_map,
        top_k=resolved_bm25.top_k,
    )
    bm25_rows = rankings_to_candidate_rows(rankings)
    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=qrels_map,
        evaluator_name=split_name,
        score_name="bm25_bm25s_okapi",
    )
    ndcg_key = f"{split_name}_bm25_bm25s_okapi_ndcg@10"
    bm25_ndcg_at_10 = float(metrics.get(ndcg_key, 0.0))

    _write_split_parquet(output_dir=output_dir, split_name=split_name, corpus=selected_corpus, queries=selected_queries, qrels=selected_qrels, bm25_rows=bm25_rows)
    split_metadata = {
        "split_name": split_name,
        "queries": len(selected_queries),
        "corpus": len(selected_corpus),
        "qrels": len(selected_qrels),
        "source_positive_qrels": len(positive_qrels),
        "source_non_positive_qrels": len(non_positive_qrels),
        "query_limit": query_limit,
        "doc_limit": doc_limit,
        "qrels_score_policy": "score > 0 kept as qrels; score <= 0 excluded and used as hard-negative corpus candidates",
        "query_selection": query_metadata,
        "corpus_selection": corpus_metadata,
        "bm25": {
            "config": bm25_config_payload(resolved_bm25),
            "ndcg_at_10": bm25_ndcg_at_10,
            **forcing_metadata,
        },
    }
    _write_json(output_dir / "metadata" / f"{split_name}.json", split_metadata)
    _upsert_manifest(output_dir=output_dir, dataset_name=dataset_name, dataset_id=dataset_id, split_metadata=split_metadata)
    _write_readme(output_dir=output_dir, dataset_name=dataset_name, dataset_id=dataset_id, metadata=metadata)

    dataset_config_path = None
    if dataset_config_dir is not None:
        dataset_config_path = upsert_dataset_config_yaml(
            dataset_config_dir=dataset_config_dir,
            dataset_name=dataset_name,
            dataset_id=dataset_id,
            split_name=split_name,
            metadata=metadata,
        )

    return NanoBuildResult(
        dataset_name=dataset_name,
        dataset_id=dataset_id,
        split_name=split_name,
        output_dir=output_dir,
        dataset_config_path=dataset_config_path,
        queries=len(selected_queries),
        corpus=len(selected_corpus),
        qrels=len(selected_qrels),
        source_positive_qrels=len(positive_qrels),
        source_non_positive_qrels=len(non_positive_qrels),
        forced_queries=int(forcing_metadata["forced_queries"]),
        forced_doc_count=int(forcing_metadata["forced_doc_count"]),
        missing_positive_doc_count_after_forcing=int(forcing_metadata["missing_positive_doc_count_after_forcing"]),
        bm25_ndcg_at_10=bm25_ndcg_at_10,
    )


def _qrels_mapping(qrels: list[dict[str, str]]) -> dict[str, set[str]]:
    output: dict[str, set[str]] = {}
    for row in qrels:
        output.setdefault(row["query-id"], set()).add(row["corpus-id"])
    return output


def _write_split_parquet(
    *,
    output_dir: Path,
    split_name: str,
    corpus: list[dict[str, str]],
    queries: list[dict[str, str]],
    qrels: list[dict[str, str]],
    bm25_rows: list[dict[str, Any]],
) -> None:
    for config in NANO_CONFIGS + ("metadata",):
        (output_dir / config).mkdir(parents=True, exist_ok=True)
    Dataset.from_list(corpus).to_parquet(str(output_dir / "corpus" / f"{split_name}.parquet"))
    Dataset.from_list(queries).to_parquet(str(output_dir / "queries" / f"{split_name}.parquet"))
    Dataset.from_list(qrels).to_parquet(str(output_dir / "qrels" / f"{split_name}.parquet"))
    Dataset.from_list(bm25_rows).to_parquet(str(output_dir / "bm25" / f"{split_name}.parquet"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _upsert_manifest(
    *,
    output_dir: Path,
    dataset_name: str,
    dataset_id: str,
    split_metadata: dict[str, Any],
) -> None:
    path = output_dir / "manifest.json"
    if path.exists():
        manifest = json.loads(path.read_text(encoding="utf-8"))
    else:
        manifest = {"dataset_name": dataset_name, "dataset_id": dataset_id, "splits": []}
    splits = [
        item
        for item in manifest.get("splits", [])
        if isinstance(item, dict) and item.get("split_name") != split_metadata["split_name"]
    ]
    splits.append(
        {
            "split_name": split_metadata["split_name"],
            "queries": split_metadata["queries"],
            "corpus": split_metadata["corpus"],
            "qrels": split_metadata["qrels"],
            "source_positive_qrels": split_metadata["source_positive_qrels"],
            "source_non_positive_qrels": split_metadata["source_non_positive_qrels"],
            "forced_doc_count": split_metadata["bm25"]["forced_doc_count"],
            "bm25_ndcg_at_10": split_metadata["bm25"]["ndcg_at_10"],
        }
    )
    manifest["splits"] = sorted(splits, key=lambda item: str(item["split_name"]))
    _write_json(path, manifest)


def _write_readme(
    *,
    output_dir: Path,
    dataset_name: str,
    dataset_id: str,
    metadata: dict[str, Any] | None,
) -> None:
    template = _read_readme_template()
    context = _readme_context(
        output_dir=output_dir,
        dataset_name=dataset_name,
        dataset_id=dataset_id,
        metadata=metadata or {},
    )
    text = _drop_template_checklist(_replace_template_placeholders(template, context))
    (output_dir / "README.md").write_text(text.strip() + "\n", encoding="utf-8")


def _read_readme_template() -> str:
    if _README_TEMPLATE_PATH.exists():
        return _README_TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        "# {{DATASET_NAME}}\n\n"
        "This dataset is a Nano-style retrieval dataset. Nano-series evaluation can "
        "be run easily with [HAKARI-Bench](https://github.com/hotchpotch/hakari-bench).\n\n"
        "## Split Statistics\n\n"
        "{{SPLIT_STATISTICS_ROWS}}\n\n"
        "## BM25 nDCG@10\n\n"
        "{{BM25_SCORE_ROWS}}\n"
    )


def _replace_template_placeholders(template: str, context: Mapping[str, str]) -> str:
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def _drop_template_checklist(text: str) -> str:
    marker = "\n## Template Fill Checklist\n"
    if marker not in text:
        return text
    return text.split(marker, maxsplit=1)[0]


def _readme_context(
    *,
    output_dir: Path,
    dataset_name: str,
    dataset_id: str,
    metadata: Mapping[str, Any],
) -> dict[str, str]:
    splits = _readme_splits(output_dir)
    max_query_limit = _max_split_metadata_value(output_dir, splits, "query_limit", DEFAULT_QUERY_LIMIT)
    max_doc_limit = _max_split_metadata_value(output_dir, splits, "doc_limit", DEFAULT_DOC_LIMIT)
    bm25_top_k = _max_bm25_top_k(output_dir, splits)
    tokenizer_policy = _default_tokenizer_policy(output_dir, splits)
    return {
        "CONFIG_BM25_DATA_FILES": _data_files_yaml("bm25", splits),
        "CONFIG_CORPUS_DATA_FILES": _data_files_yaml("corpus", splits),
        "CONFIG_QRELS_DATA_FILES": _data_files_yaml("qrels", splits),
        "CONFIG_QUERIES_DATA_FILES": _data_files_yaml("queries", splits),
        "LANGUAGE_LIST": _language_list_yaml(metadata),
        "TAG_LIST": _tag_list_yaml(metadata),
        "DATASET_NAME": dataset_name,
        "SOURCE_BENCHMARK_NAME": _metadata_text(metadata, "source_benchmark_name", "the upstream retrieval sources"),
        "DATASET_OVERVIEW_PARAGRAPH": _metadata_text(
            metadata,
            "description",
            f"{dataset_name} is a Nano-style retrieval dataset.",
        ),
        "NAMING_NOTE_SECTION": _metadata_text(metadata, "naming_note", ""),
        "SOURCE_LINKS_LIST": _source_links_list(metadata, dataset_id),
        "SOURCE_DATASET_LOCATION": _metadata_text(
            metadata,
            "source_dataset_location",
            "the source dataset tables passed to the converter",
        ),
        "SOURCE_SPLIT_POLICY": _metadata_text(metadata, "source_split_policy", "the documented source evaluation split"),
        "MAX_QUERIES_PER_SPLIT": str(max_query_limit),
        "MAX_CORPUS_DOCUMENTS": str(max_doc_limit),
        "CORPUS_FILL_POLICY": _metadata_text(
            metadata,
            "corpus_fill_policy",
            "selected positives, source score <= 0 hard negatives, then source corpus order",
        ),
        "QRELS_DUPLICATE_POLICY": _metadata_text(metadata, "qrels_duplicate_policy", "the qrels row was removed"),
        "CORPUS_TEXT_POLICY": _metadata_text(metadata, "corpus_text_policy", "`title` plus body text when available"),
        "BM25_TOP_K": str(bm25_top_k),
        "BM25_TOKENIZER_POLICY": tokenizer_policy,
        "QRELS_SCORE_POLICY_NOTE": _metadata_text(
            metadata,
            "qrels_score_policy_note",
            "Source relevance scores are collapsed to binary positive qrels in the published Nano layout.",
        ),
        "SOURCE_HARD_NEGATIVE_NOTE": _metadata_text(
            metadata,
            "source_hard_negative_note",
            "Source rows with `score <= 0` are used as hard-negative corpus candidates when available.",
        ),
        "QRELS_CAPPING_NOTE": _metadata_text(metadata, "qrels_capping_note", ""),
        "SPLIT_STATISTICS_ROWS": _split_statistics_rows(output_dir, splits),
        "SPLIT_MAPPING_NOTES": _metadata_text(
            metadata,
            "split_mapping_notes",
            "Each Nano split maps to one source retrieval task unless noted otherwise.",
        ),
        "SPLIT_MAPPING_ROWS": _split_mapping_rows(output_dir, splits, metadata, dataset_id),
        "BM25_SCORE_NOTES": _metadata_text(
            metadata,
            "bm25_score_notes",
            "Scores are reported for the included BM25 candidate subset after forced-positive insertion.",
        ),
        "BM25_SCORE_ROWS": _bm25_score_rows(output_dir, splits),
        "SKIPPED_TASKS_SECTION": _skipped_tasks_section(metadata),
        "UPSTREAM_LICENSE_TARGET": _metadata_text(metadata, "upstream_license_target", "the upstream source datasets"),
    }


def _readme_splits(output_dir: Path) -> list[str]:
    split_names: set[str] = set()
    for config in NANO_CONFIGS:
        config_dir = output_dir / config
        if config_dir.exists():
            split_names.update(path.stem for path in config_dir.glob("*.parquet"))
    return sorted(split_names)


def _data_files_yaml(config: str, splits: list[str]) -> str:
    rows = [{"split": split, "path": f"{config}/{split}.parquet"} for split in splits]
    return _indent(yaml.safe_dump(rows, sort_keys=False, allow_unicode=True).rstrip(), spaces=2)


def _language_list_yaml(metadata: Mapping[str, Any]) -> str:
    languages = _metadata_sequence(metadata, "languages")
    if not languages and isinstance(metadata.get("language"), str):
        languages = [str(metadata["language"])]
    return yaml.safe_dump(languages or ["unknown"], sort_keys=False, allow_unicode=True).rstrip()


def _tag_list_yaml(metadata: Mapping[str, Any]) -> str:
    tags = _metadata_sequence(metadata, "tags") or ["information-retrieval", "retrieval", "nano", "bm25", "hakari-bench"]
    return yaml.safe_dump(tags, sort_keys=False, allow_unicode=True).rstrip()


def _source_links_list(metadata: Mapping[str, Any], dataset_id: str) -> str:
    raw_links = metadata.get("source_links")
    if isinstance(raw_links, list):
        links = [str(link) for link in raw_links if str(link).strip()]
        if links:
            return "\n".join(f"- {link}" for link in links)
    return f"- Final dataset: [`{dataset_id}`](https://huggingface.co/datasets/{dataset_id})"


def _split_statistics_rows(output_dir: Path, splits: list[str]) -> str:
    rows: list[str] = []
    for split in splits:
        queries = _read_optional_parquet(output_dir / "queries" / f"{split}.parquet")
        corpus = _read_optional_parquet(output_dir / "corpus" / f"{split}.parquet")
        qrels = _read_optional_parquet(output_dir / "qrels" / f"{split}.parquet")
        query_stats = _length_stats(row.get("text") for row in queries)
        doc_stats = _length_stats(row.get("text") for row in corpus)
        rows.append(
            "| "
            + " | ".join(
                [
                    split,
                    str(len(queries)),
                    str(len(corpus)),
                    str(len(qrels)),
                    *_format_stats(query_stats),
                    *_format_stats(doc_stats),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def _split_mapping_rows(
    output_dir: Path,
    splits: list[str],
    metadata: Mapping[str, Any],
    dataset_id: str,
) -> str:
    source_dataset = _metadata_text(metadata, "source_dataset_id", dataset_id)
    rows: list[str] = []
    for split in splits:
        queries = len(_read_optional_parquet(output_dir / "queries" / f"{split}.parquet"))
        corpus = len(_read_optional_parquet(output_dir / "corpus" / f"{split}.parquet"))
        qrels = len(_read_optional_parquet(output_dir / "qrels" / f"{split}.parquet"))
        source_task = _split_metadata_text(output_dir, split, "source_task", split)
        rows.append(f"| {split} | {source_task} | `{source_dataset}` | {queries} | {corpus} | {qrels} |")
    return "\n".join(rows)


def _bm25_score_rows(output_dir: Path, splits: list[str]) -> str:
    rows: list[str] = []
    for split in splits:
        split_metadata = _read_optional_json(output_dir / "metadata" / f"{split}.json")
        bm25 = split_metadata.get("bm25")
        bm25 = bm25 if isinstance(bm25, dict) else {}
        config = bm25.get("config")
        config = config if isinstance(config, dict) else {}
        tokenizer = str(config.get("tokenizer") or "auto")
        tokenizer_name = config.get("tokenizer_name")
        if isinstance(tokenizer_name, str) and tokenizer_name:
            tokenizer = f"{tokenizer}:{tokenizer_name}"
        forced = int(bm25.get("forced_doc_count") or 0)
        ndcg = float(bm25.get("ndcg_at_10") or 0.0)
        rows.append(f"| {split} | {tokenizer} | {forced} | {ndcg:.4f} |")
    return "\n".join(rows)


def _read_optional_parquet(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [dict(row) for row in pq.read_table(path).to_pylist()]


def _read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    parsed = json.loads(path.read_text(encoding="utf-8"))
    return parsed if isinstance(parsed, dict) else {}


def _length_stats(values: Iterable[Any]) -> dict[str, float]:
    lengths = sorted(float(len(str(value))) for value in values if value is not None)
    if not lengths:
        return {"avg": 0.0, "std": 0.0, "median": 0.0, "p25": 0.0, "p75": 0.0}
    avg = sum(lengths) / len(lengths)
    variance = sum((value - avg) ** 2 for value in lengths) / len(lengths)
    return {
        "avg": avg,
        "std": math.sqrt(variance),
        "median": _percentile(lengths, 0.50),
        "p25": _percentile(lengths, 0.25),
        "p75": _percentile(lengths, 0.75),
    }


def _percentile(sorted_values: list[float], q: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def _format_stats(stats: Mapping[str, float]) -> list[str]:
    return [
        f"{stats['avg']:.1f}",
        f"{stats['std']:.1f}",
        f"{stats['median']:.1f}",
        f"{stats['p25']:.1f}",
        f"{stats['p75']:.1f}",
    ]


def _metadata_sequence(metadata: Mapping[str, Any], key: str) -> list[str]:
    value = metadata.get(key)
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item) for item in value if str(item).strip()]
    return []


def _metadata_text(metadata: Mapping[str, Any], key: str, default: str) -> str:
    value = metadata.get(key)
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _split_metadata_text(output_dir: Path, split: str, key: str, default: str) -> str:
    value = _read_optional_json(output_dir / "metadata" / f"{split}.json").get(key)
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _max_split_metadata_value(output_dir: Path, splits: list[str], key: str, default: int) -> int:
    values: list[int] = []
    for split in splits:
        value = _read_optional_json(output_dir / "metadata" / f"{split}.json").get(key)
        if isinstance(value, int):
            values.append(value)
    return max(values, default=default)


def _max_bm25_top_k(output_dir: Path, splits: list[str]) -> int:
    values: list[int] = []
    for split in splits:
        bm25 = _read_optional_json(output_dir / "metadata" / f"{split}.json").get("bm25")
        if not isinstance(bm25, dict):
            continue
        config = bm25.get("config")
        if isinstance(config, dict) and isinstance(config.get("top_k"), int):
            values.append(config["top_k"])
    return max(values, default=DEFAULT_BM25_TOP_K)


def _default_tokenizer_policy(output_dir: Path, splits: list[str]) -> str:
    tokenizers = {_bm25_tokenizer_for_split(output_dir, split) for split in splits}
    tokenizers.discard("")
    if len(tokenizers) == 1:
        return next(iter(tokenizers))
    if tokenizers:
        return "split-specific BM25"
    return "regex"


def _bm25_tokenizer_for_split(output_dir: Path, split: str) -> str:
    bm25 = _read_optional_json(output_dir / "metadata" / f"{split}.json").get("bm25")
    if not isinstance(bm25, dict):
        return ""
    config = bm25.get("config")
    if not isinstance(config, dict):
        return ""
    tokenizer = str(config.get("tokenizer") or "auto")
    tokenizer_name = config.get("tokenizer_name")
    if isinstance(tokenizer_name, str) and tokenizer_name:
        return f"{tokenizer}:{tokenizer_name}"
    return tokenizer


def _skipped_tasks_section(metadata: Mapping[str, Any]) -> str:
    skipped = metadata.get("skipped_tasks")
    if isinstance(skipped, list) and skipped:
        return "\n".join(f"- {item}" for item in skipped)
    return "No source tasks were skipped."


def _indent(text: str, *, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" if line else line for line in text.splitlines())


def upsert_dataset_config_yaml(
    *,
    dataset_config_dir: Path,
    dataset_name: str,
    dataset_id: str,
    split_name: str,
    metadata: dict[str, Any] | None = None,
) -> Path:
    dataset_config_dir.mkdir(parents=True, exist_ok=True)
    path = dataset_config_dir / f"{_dataset_config_filename(dataset_name)}.yaml"
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"dataset config YAML must contain a mapping: {path}")
    else:
        data = {
            "name": dataset_name,
            "dataset_id": dataset_id,
            "benchmark_kind": "nano",
            "corpus_config": "corpus",
            "queries_config": "queries",
            "qrels_config": "qrels",
            "candidate_config": "bm25",
            "splits": [],
            "metadata": _default_dataset_metadata(dataset_name, metadata),
        }
    splits = [str(split) for split in data.get("splits", []) if isinstance(split, str)]
    if split_name not in splits:
        splits.append(split_name)
    data["splits"] = splits
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def _dataset_config_filename(dataset_name: str) -> str:
    return "".join(char.lower() for char in dataset_name if char.isalnum() or char in {"_", "-"}).replace("-", "_")


def _default_dataset_metadata(dataset_name: str, metadata: dict[str, Any] | None) -> dict[str, Any]:
    if metadata is not None:
        return dict(metadata)
    return {
        "language": "unknown",
        "category": "natural_language",
        "short_description": f"{dataset_name} Nano retrieval dataset.",
        "description": f"{dataset_name} is a Nano-style retrieval dataset generated from retrieval source tables.",
    }


def load_local_source_tables(*, source_dir: Path, source_split_name: str) -> SourceTables:
    return SourceTables(
        corpus_rows=pq.read_table(_local_source_path(source_dir, "corpus", source_split_name)).to_pylist(),
        query_rows=pq.read_table(_local_source_path(source_dir, "queries", source_split_name)).to_pylist(),
        qrels_rows=pq.read_table(_local_source_path(source_dir, "qrels", source_split_name)).to_pylist(),
    )


def _local_source_path(source_dir: Path, config: str, source_split_name: str) -> Path:
    candidates = [
        source_dir / source_split_name / config / "test.parquet",
        source_dir / config / f"{source_split_name}.parquet",
        source_dir / config / "test.parquet",
        source_dir / config / f"{config}.parquet",
    ]
    if config == "qrels":
        candidates.extend(
            [
                source_dir / "default" / f"{source_split_name}.parquet",
                source_dir / "default" / "test.parquet",
            ]
        )
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"Missing local source parquet for {config}/{source_split_name} under {source_dir}.")


def build_nano_dataset_from_local_source(
    *,
    source_dir: Path,
    output_dir: Path,
    dataset_name: str,
    dataset_id: str,
    source_split_name: str,
    split_name: str | None = None,
    dataset_config_dir: Path | None = None,
    query_limit: int = DEFAULT_QUERY_LIMIT,
    doc_limit: int = DEFAULT_DOC_LIMIT,
    bm25_config: BM25Config | None = None,
    metadata: dict[str, Any] | None = None,
) -> NanoBuildResult:
    tables = load_local_source_tables(source_dir=source_dir, source_split_name=source_split_name)
    return build_nano_dataset_from_rows(
        output_dir=output_dir,
        dataset_name=dataset_name,
        dataset_id=dataset_id,
        split_name=split_name or source_split_name,
        corpus_rows=tables.corpus_rows,
        query_rows=tables.query_rows,
        qrels_rows=tables.qrels_rows,
        dataset_config_dir=dataset_config_dir,
        query_limit=query_limit,
        doc_limit=doc_limit,
        bm25_config=bm25_config,
        metadata=metadata,
    )


def load_hf_mteb_source_tables(
    *,
    dataset_id: str,
    corpus_config: str = "corpus",
    queries_config: str = "queries",
    qrels_config: str = "default",
    corpus_split: str = "corpus",
    queries_split: str = "queries",
    qrels_split: str = "test",
    revision: str | None = None,
) -> SourceTables:
    corpus = load_dataset(dataset_id, name=corpus_config, split=corpus_split, revision=revision)
    queries = load_dataset(dataset_id, name=queries_config, split=queries_split, revision=revision)
    qrels = load_dataset(dataset_id, name=qrels_config, split=qrels_split, revision=revision)
    return SourceTables(
        corpus_rows=[dict(row) for row in corpus],
        query_rows=[dict(row) for row in queries],
        qrels_rows=[dict(row) for row in qrels],
    )


def build_nano_dataset_from_hf_mteb(
    *,
    source_dataset_id: str,
    output_dir: Path,
    dataset_name: str,
    dataset_id: str,
    split_name: str,
    dataset_config_dir: Path | None = None,
    corpus_config: str = "corpus",
    queries_config: str = "queries",
    qrels_config: str = "default",
    corpus_split: str = "corpus",
    queries_split: str = "queries",
    qrels_split: str = "test",
    revision: str | None = None,
    query_limit: int = DEFAULT_QUERY_LIMIT,
    doc_limit: int = DEFAULT_DOC_LIMIT,
    bm25_config: BM25Config | None = None,
    metadata: dict[str, Any] | None = None,
) -> NanoBuildResult:
    tables = load_hf_mteb_source_tables(
        dataset_id=source_dataset_id,
        corpus_config=corpus_config,
        queries_config=queries_config,
        qrels_config=qrels_config,
        corpus_split=corpus_split,
        queries_split=queries_split,
        qrels_split=qrels_split,
        revision=revision,
    )
    return build_nano_dataset_from_rows(
        output_dir=output_dir,
        dataset_name=dataset_name,
        dataset_id=dataset_id,
        split_name=split_name,
        corpus_rows=tables.corpus_rows,
        query_rows=tables.query_rows,
        qrels_rows=tables.qrels_rows,
        dataset_config_dir=dataset_config_dir,
        query_limit=query_limit,
        doc_limit=doc_limit,
        bm25_config=bm25_config,
        metadata=metadata,
    )
