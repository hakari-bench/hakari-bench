from __future__ import annotations

import argparse
import importlib
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import pyarrow.parquet as pq
import yaml
from huggingface_hub import hf_hub_download, list_repo_files

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from hakari_bench.bm25 import BM25Config, BM25Tokenizer  # noqa: E402
from hakari_bench.nano_dataset_builder import build_nano_dataset_from_rows  # noqa: E402
from hakari_bench.nano_dataset_builder import _write_readme as write_nano_readme  # noqa: E402
from scripts.build_nanomteb_family_datasets import (  # noqa: E402
    DIRECT_SOURCE_BY_TARGET,
    FAMILY_DATASETS,
    MISC_SOURCE_CANDIDATES,
    SOURCE_DATASET_IDS,
)
from scripts.migrate_nanomteb_family_results import SPLIT_MOVES_TO_MISC  # noqa: E402


CONFIGS = ("bm25", "corpus", "qrels", "queries")
DEFAULT_QUERY_LIMIT = 200
DEFAULT_DOC_LIMIT = 10_000
DEFAULT_TOP_K = 100
MANUAL_TASK_NAMES = {
    "NanoCQADupstackGaming": "CQADupstackGamingRetrieval",
    "NanoCQADupstackUnix": "CQADupstackUnixRetrieval",
    "NanoFiQA2018": "FiQA2018",
    "NanoSCIDOCS": "SCIDOCS",
    "NanoTouche2020": "Touche2020Retrieval.v3",
    "NanoClimateFEVERHardNegatives": "ClimateFEVERHardNegatives.v2",
    "NanoFEVERHardNegatives": "FEVERHardNegatives.v2",
    "NanoHotpotQAHardNegatives": "HotpotQAHardNegatives.v2",
    "NanoNews21Instruction": "News21InstructionRetrieval",
}
LANGUAGE_TO_MTEB_CODE = {
    "ar": "ara",
    "as": "asm",
    "bn": "ben",
    "cs": "ces",
    "da": "dan",
    "de": "deu",
    "el": "ell",
    "en": "eng",
    "es": "spa",
    "fa": "fas",
    "fi": "fin",
    "fr": "fra",
    "gu": "guj",
    "hi": "hin",
    "it": "ita",
    "ja": "jpn",
    "kn": "kan",
    "ko": "kor",
    "lt": "lit",
    "lv": "lav",
    "ml": "mal",
    "mr": "mar",
    "nl": "nld",
    "no": "nor",
    "or": "ory",
    "pa": "pan",
    "pl": "pol",
    "pt": "por",
    "ru": "rus",
    "sk": "slk",
    "sl": "slv",
    "sv": "swe",
    "ta": "tam",
    "te": "tel",
    "th": "tha",
    "vi": "vie",
    "zh": "zho",
}


@dataclass(frozen=True)
class SplitPlan:
    dataset_name: str
    split_name: str
    task_name: str
    old_source_dataset_name: str | None
    source_subsets: tuple[str, ...] | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recreate canonical NanoMTEB-family datasets from upstream MTEB task sources."
    )
    parser.add_argument("--output-root", type=Path, default=Path("output/nano_datasets"))
    parser.add_argument("--config-root", type=Path, default=Path("config"))
    parser.add_argument("--datasets", default=None, help="Comma-separated dataset names to recreate.")
    parser.add_argument("--splits", default=None, help="Comma-separated split names to recreate.")
    parser.add_argument("--query-limit", type=int, default=DEFAULT_QUERY_LIMIT)
    parser.add_argument("--doc-limit", type=int, default=DEFAULT_DOC_LIMIT)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--bm25-tokenizer", default="regex")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected_datasets = _parse_csv(args.datasets)
    selected_splits = _parse_csv(args.splits)
    plans = build_plan(config_root=args.config_root, selected_datasets=selected_datasets, selected_splits=selected_splits)
    if args.clean:
        _clean_output(output_root=args.output_root, dataset_names=sorted({plan.dataset_name for plan in plans}))
    args.output_root.mkdir(parents=True, exist_ok=True)

    bm25_config = BM25Config(
        tokenizer=cast(BM25Tokenizer, args.bm25_tokenizer),
        top_k=args.top_k,
    )
    for index, plan in enumerate(plans, start=1):
        if not args.overwrite and _split_output_exists(output_root=args.output_root, plan=plan):
            print(f"[{index}/{len(plans)}] skip existing {plan.dataset_name}/{plan.split_name}", flush=True)
            continue
        print(f"[{index}/{len(plans)}] {plan.dataset_name}/{plan.split_name} <- {plan.task_name}", flush=True)
        build_split_from_mteb(
            plan=plan,
            output_root=args.output_root,
            config_root=args.config_root,
            query_limit=args.query_limit,
            doc_limit=args.doc_limit,
            bm25_config=bm25_config,
        )

    for dataset_name in sorted({plan.dataset_name for plan in plans}):
        dataset_dir = args.output_root / dataset_name
        dataset_config = _dataset_config(config_root=args.config_root, dataset_name=dataset_name)
        metadata = _dataset_readme_metadata(dataset_config)
        write_nano_readme(
            output_dir=dataset_dir,
            dataset_name=dataset_name,
            dataset_id=f"hakari-bench/{dataset_name}",
            metadata=metadata,
        )
        audit = validate_dataset_dir(dataset_dir=dataset_dir)
        (dataset_dir / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"[audit] {dataset_name}: splits={len(audit['splits'])} "
            f"issues={len(audit['issues'])} missing_forced={audit['missing_positive_doc_count_after_forcing']}",
            flush=True,
        )


def build_split_from_mteb(
    *,
    plan: SplitPlan,
    output_root: Path,
    config_root: Path,
    query_limit: int,
    doc_limit: int,
    bm25_config: BM25Config,
) -> None:
    mteb = _mteb_module()
    task = mteb.get_tasks(tasks=[plan.task_name])[0]
    eval_split = _eval_split(task)
    source = _load_mteb_source(
        task=task,
        eval_split=eval_split,
        split_name=plan.split_name,
        source_subsets=plan.source_subsets,
    )
    dataset_config = _dataset_config(config_root=config_root, dataset_name=plan.dataset_name)
    metadata = _split_metadata(
        dataset_config=dataset_config,
        task=task,
        subset=source["source_subset"],
        eval_split=eval_split,
        old_source_dataset_name=plan.old_source_dataset_name,
    )
    build_nano_dataset_from_rows(
        output_dir=output_root / plan.dataset_name,
        dataset_name=plan.dataset_name,
        dataset_id=f"hakari-bench/{plan.dataset_name}",
        split_name=plan.split_name,
        corpus_rows=source["corpus_rows"],
        query_rows=source["query_rows"],
        qrels_rows=source["qrels_rows"],
        query_limit=query_limit,
        doc_limit=doc_limit,
        bm25_config=bm25_config,
        metadata=metadata,
    )


def _load_mteb_source(
    *,
    task: Any,
    eval_split: str,
    split_name: str,
    source_subsets: tuple[str, ...] | None,
) -> dict[str, Any]:
    if str(task.metadata.name) == "BelebeleRetrieval":
        containers = _load_belebele_containers(task=task, eval_split=eval_split)
        if source_subsets is not None:
            containers = [(subset, container) for subset, container in containers if subset in source_subsets]
    elif _has_component_configs(task, source_subsets=source_subsets):
        containers = _load_component_containers(task=task, eval_split=eval_split, source_subsets=source_subsets)
    else:
        task.load_data(eval_splits=[eval_split])
        containers = _containers_from_loaded_task(task=task, eval_split=eval_split, source_subsets=source_subsets)
    if not containers:
        raise ValueError(f"MTEB task {task.metadata.name} did not load split {eval_split}.")
    if len(containers) == 1:
        subset, container = containers[0]
        relevant_docs = cast(dict[str, dict[str, int | float]], container["relevant_docs"])
        qrels_rows = [
            {"query-id": str(query_id), "corpus-id": str(corpus_id), "score": score}
            for query_id, docs in relevant_docs.items()
            for corpus_id, score in docs.items()
        ]
        return {
            "source_subset": subset,
            "corpus_rows": _prefixed_rows(rows=container["corpus"], prefix="", row_kind="corpus"),
            "query_rows": _prefixed_rows(rows=container["queries"], prefix="", row_kind="query"),
            "qrels_rows": qrels_rows,
        }
    return {
        "source_subset": "combined",
        "corpus_rows": _prefixed_corpus_rows(containers=containers, split_name=split_name),
        "query_rows": _prefixed_query_rows(containers=containers, split_name=split_name),
        "qrels_rows": _prefixed_qrels_rows(containers=containers, split_name=split_name),
    }


def _loaded_subsets(task: Any) -> list[str]:
    preferred = [str(subset) for subset in getattr(task, "hf_subsets", []) or []]
    loaded = [str(subset) for subset in task.dataset]
    ordered = [subset for subset in preferred if subset in task.dataset]
    ordered.extend(subset for subset in loaded if subset not in ordered)
    return ordered


def _containers_from_loaded_task(
    *,
    task: Any,
    eval_split: str,
    source_subsets: tuple[str, ...] | None,
) -> list[tuple[str, dict[str, Any]]]:
    if getattr(task, "dataset", None) is not None:
        if eval_split in task.dataset:
            container = task.dataset[eval_split]
            if isinstance(container, dict) and all(key in container for key in ("corpus", "queries", "relevant_docs")):
                if source_subsets is not None and "default" not in source_subsets:
                    return []
                return [("default", container)]
        containers = [
            (str(subset), task.dataset[subset][eval_split])
            for subset in _loaded_subsets(task)
            if isinstance(task.dataset[subset], dict)
            and eval_split in task.dataset[subset]
            and (source_subsets is None or str(subset) in source_subsets)
        ]
        if containers:
            return containers

    corpus = getattr(task, "corpus", None)
    queries = getattr(task, "queries", None)
    relevant_docs = getattr(task, "relevant_docs", None)
    if isinstance(corpus, dict) and isinstance(queries, dict) and isinstance(relevant_docs, dict) and eval_split in corpus:
        if source_subsets is not None and "default" not in source_subsets:
            return []
        return [
            (
                "default",
                {
                    "corpus": corpus[eval_split],
                    "queries": queries[eval_split],
                    "relevant_docs": relevant_docs[eval_split],
                },
            )
        ]
    if isinstance(corpus, dict) and isinstance(queries, dict) and isinstance(relevant_docs, dict):
        subsets = [str(subset) for subset in getattr(task, "hf_subsets", []) or []]
        if source_subsets is not None:
            subsets = [subset for subset in subsets if subset in source_subsets]
        return [
            (
                subset,
                {
                    "corpus": corpus[subset][eval_split],
                    "queries": queries[subset][eval_split],
                    "relevant_docs": relevant_docs[subset][eval_split],
                },
            )
            for subset in subsets
            if subset in corpus
            and subset in queries
            and subset in relevant_docs
            and isinstance(corpus[subset], dict)
            and isinstance(queries[subset], dict)
            and isinstance(relevant_docs[subset], dict)
            and eval_split in corpus[subset]
            and eval_split in queries[subset]
            and eval_split in relevant_docs[subset]
        ]
    return []


def _prefixed_corpus_rows(*, containers: list[tuple[str, dict[str, Any]]], split_name: str) -> Any:
    for subset, container in containers:
        prefix = f"{split_name}__{subset}::d::"
        yield from _prefixed_rows(rows=container["corpus"], prefix=prefix, row_kind="corpus")


def _prefixed_query_rows(*, containers: list[tuple[str, dict[str, Any]]], split_name: str) -> Any:
    rows_by_subset = []
    for subset, container in containers:
        prefix = f"{split_name}__{subset}::q::"
        rows_by_subset.append(list(_prefixed_rows(rows=container["queries"], prefix=prefix, row_kind="query")))
    max_rows = max((len(rows) for rows in rows_by_subset), default=0)
    for index in range(max_rows):
        for rows in rows_by_subset:
            if index < len(rows):
                yield rows[index]


def _prefixed_qrels_rows(*, containers: list[tuple[str, dict[str, Any]]], split_name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    query_ids_by_subset: list[tuple[str, list[str], dict[str, dict[str, int | float]]]] = []
    for subset, container in containers:
        query_ids = [str(row["_id"]) for row in _prefixed_rows(rows=container["queries"], prefix="", row_kind="query")]
        relevant_docs = cast(dict[str, dict[str, int | float]], container["relevant_docs"])
        query_ids_by_subset.append((subset, query_ids, relevant_docs))
    max_queries = max((len(query_ids) for _, query_ids, _ in query_ids_by_subset), default=0)
    for index in range(max_queries):
        for subset, query_ids, relevant_docs in query_ids_by_subset:
            if index >= len(query_ids):
                continue
            query_id = query_ids[index]
            if query_id not in relevant_docs:
                continue
            query_prefix = f"{split_name}__{subset}::q::"
            corpus_prefix = f"{split_name}__{subset}::d::"
            rows.extend(
                {"query-id": f"{query_prefix}{query_id}", "corpus-id": f"{corpus_prefix}{corpus_id}", "score": score}
                for corpus_id, score in relevant_docs[query_id].items()
            )
    return rows

def _prefixed_rows(*, rows: Any, prefix: str, row_kind: str) -> Any:
    if isinstance(rows, dict):
        for row_id, value in rows.items():
            if isinstance(value, dict):
                row = dict(value)
                row["_id"] = f"{prefix}{row_id}"
                yield row
            else:
                yield {"_id": f"{prefix}{row_id}", "text": str(value)}
        return
    for row in rows:
        row_dict = dict(row)
        raw_id = row_dict.get("id") or row_dict.get("_id")
        if raw_id is None:
            raise ValueError(f"{row_kind} row is missing id: {row_dict}")
        row_dict["_id"] = f"{prefix}{raw_id}"
        row_dict.pop("id", None)
        yield row_dict


def _load_belebele_containers(*, task: Any, eval_split: str) -> list[tuple[str, dict[str, Any]]]:
    from datasets import load_dataset

    dataset_path = task.metadata.dataset["path"]
    revision = task.metadata.dataset["revision"]
    language_cache: dict[str, Any] = {}
    containers: list[tuple[str, dict[str, Any]]] = []
    for subset in task.hf_subsets:
        languages = task.metadata.eval_langs[subset]
        corpus_lang = languages[0].replace("-", "_")
        query_lang = languages[1].replace("-", "_")
        if corpus_lang not in language_cache:
            language_cache[corpus_lang] = load_dataset(dataset_path, corpus_lang, revision=revision)[eval_split]
        if query_lang not in language_cache:
            language_cache[query_lang] = load_dataset(dataset_path, query_lang, revision=revision)[eval_split]
        corpus_ds = language_cache[corpus_lang]
        query_ds = language_cache[query_lang]
        question_ids: dict[str, int] = {}
        for row in query_ds:
            question = str(row["question"])
            if question not in question_ids:
                question_ids[question] = len(question_ids)
        link_to_context_id: dict[str, str] = {}
        corpus: dict[str, dict[str, str]] = {}
        for row in corpus_ds:
            link = str(row["link"])
            if link in link_to_context_id:
                continue
            context_id = f"C{len(link_to_context_id)}"
            link_to_context_id[link] = context_id
            corpus[context_id] = {"title": "", "text": str(row["flores_passage"])}
        queries: dict[str, str] = {}
        relevant_docs: dict[str, dict[str, int]] = {}
        for row in query_ds:
            question = str(row["question"])
            query_id = f"Q{question_ids[question]}"
            queries[query_id] = question
            context_id = link_to_context_id[str(row["link"])]
            relevant_docs.setdefault(query_id, {})[context_id] = 1
        containers.append((str(subset), {"corpus": corpus, "queries": queries, "relevant_docs": relevant_docs}))
    return containers


def _has_component_configs(task: Any, *, source_subsets: tuple[str, ...] | None) -> bool:
    from datasets import get_dataset_config_names

    subsets = list(source_subsets or tuple(str(subset) for subset in getattr(task, "hf_subsets", []) or []))
    if not subsets:
        return False
    dataset_info = task.metadata.dataset
    dataset_path = str(dataset_info.get("path") or "")
    revision = str(dataset_info.get("revision") or "")
    if not dataset_path:
        return False
    try:
        config_names = set(get_dataset_config_names(dataset_path, revision=revision or None))
    except Exception:
        return False
    return all(f"{subset}-{kind}" in config_names for subset in subsets for kind in ("corpus", "queries", "qrels"))


def _load_component_containers(
    *,
    task: Any,
    eval_split: str,
    source_subsets: tuple[str, ...] | None,
) -> list[tuple[str, dict[str, Any]]]:
    from datasets import load_dataset

    dataset_info = task.metadata.dataset
    dataset_path = str(dataset_info["path"])
    revision = str(dataset_info.get("revision") or "")
    containers: list[tuple[str, dict[str, Any]]] = []
    subsets = list(source_subsets or tuple(str(subset) for subset in getattr(task, "hf_subsets", []) or []))
    print(f"  loading component datasets: {len(subsets)} subsets", flush=True)
    for index, subset in enumerate(subsets, start=1):
        print(f"  [{index}/{len(subsets)}] {subset}", flush=True)
        corpus = load_dataset(dataset_path, f"{subset}-corpus", split=eval_split, revision=revision or None)
        queries = load_dataset(dataset_path, f"{subset}-queries", split=eval_split, revision=revision or None)
        qrels_rows = load_dataset(dataset_path, f"{subset}-qrels", split=eval_split, revision=revision or None)
        relevant_docs: dict[str, dict[str, int | float]] = {}
        for row in qrels_rows:
            relevant_docs.setdefault(str(row["query-id"]), {})[str(row["corpus-id"])] = cast(int | float, row["score"])
        containers.append((subset, {"corpus": corpus, "queries": queries, "relevant_docs": relevant_docs}))
    return containers


def build_plan(*, config_root: Path, selected_datasets: set[str], selected_splits: set[str]) -> list[SplitPlan]:
    old_repo_files = _old_repo_files()
    plans: list[SplitPlan] = []
    for dataset_name in FAMILY_DATASETS:
        if selected_datasets and dataset_name not in selected_datasets:
            continue
        dataset_config = _dataset_config(config_root=config_root, dataset_name=dataset_name)
        splits = cast(list[str], dataset_config["splits"])
        for split_name in splits:
            if selected_splits and split_name not in selected_splits:
                continue
            old_source = _old_source_dataset_name(
                dataset_name=dataset_name,
                split_name=split_name,
                old_repo_files=old_repo_files,
            )
            old_metadata = _old_split_metadata(old_source, split_name, old_repo_files=old_repo_files)
            task_name = _resolve_task_name(split_name=split_name, old_metadata=old_metadata)
            source_subsets = _resolve_source_subsets(
                dataset_name=dataset_name,
                split_name=split_name,
                dataset_config=dataset_config,
                task_name=task_name,
            )
            plans.append(
                SplitPlan(
                    dataset_name=dataset_name,
                    split_name=split_name,
                    task_name=task_name,
                    old_source_dataset_name=old_source,
                    source_subsets=source_subsets,
                )
            )
    return plans


def _resolve_task_name(*, split_name: str, old_metadata: dict[str, Any]) -> str:
    mteb = _mteb_module()
    candidates = []
    for key in ("task_name", "source_task", "requested_source_task"):
        value = old_metadata.get(key)
        if isinstance(value, str) and value:
            candidates.append(value)
    base = split_name.removeprefix("Nano")
    candidates.extend(
        [
            MANUAL_TASK_NAMES.get(split_name, ""),
            base,
            f"{base}Retrieval",
        ]
    )
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            if mteb.get_tasks(tasks=[candidate]):
                return candidate
        except Exception:
            continue
    raise ValueError(f"Could not resolve MTEB task for split {split_name}; tried {candidates}")


def _resolve_source_subsets(
    *,
    dataset_name: str,
    split_name: str,
    dataset_config: dict[str, Any],
    task_name: str,
) -> tuple[str, ...] | None:
    if dataset_name == "NanoMMTEB":
        return None
    mteb = _mteb_module()
    task = mteb.get_tasks(tasks=[task_name])[0]
    subsets = [str(subset) for subset in getattr(task, "hf_subsets", []) or []]
    if len(subsets) < 2:
        return None

    split_metadata = cast(dict[str, Any], cast(dict[str, Any], dataset_config.get("task_metadata") or {}).get(split_name) or {})
    language_values = split_metadata.get("languages") or split_metadata.get("language")
    if language_values is None:
        language_values = cast(dict[str, Any], dataset_config.get("metadata") or {}).get("language")
    target_codes = _language_codes(language_values)
    if not target_codes:
        return None

    eval_langs = task.metadata.eval_langs
    directional_subset = _directional_subset_from_split(split_name)
    if directional_subset in subsets:
        return (directional_subset,)

    matched: list[str] = []
    for subset in subsets:
        subset_langs = _subset_language_codes(eval_langs, subset)
        subset_code = LANGUAGE_TO_MTEB_CODE.get(subset.lower(), subset.lower())
        if subset_code == target_codes[0]:
            matched.append(subset)
        elif set(target_codes).issubset(set(subset_langs)):
            matched.append(subset)
    if not matched:
        raise ValueError(
            f"Could not resolve source subset for {dataset_name}/{split_name} from languages "
            f"{sorted(target_codes)} and task subsets {subsets}"
        )
    return tuple(matched)


def _directional_subset_from_split(split_name: str) -> str | None:
    if split_name.endswith("DeFr"):
        return "deu-fra"
    if split_name.endswith("FrDe"):
        return "fra-deu"
    return None


def _language_codes(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list):
        values = [str(item) for item in value]
    else:
        return tuple()
    codes: list[str] = []
    for raw_value in values:
        language = raw_value.split("-", maxsplit=1)[0].lower()
        if language == "multilingual":
            continue
        codes.append(LANGUAGE_TO_MTEB_CODE.get(language, language))
    return tuple(dict.fromkeys(codes))


def _subset_language_codes(eval_langs: Any, subset: str) -> tuple[str, ...]:
    if isinstance(eval_langs, dict):
        raw_values = eval_langs.get(subset) or []
    else:
        raw_values = eval_langs or []
    if isinstance(raw_values, str):
        raw_values = [raw_values]
    return _language_codes(list(raw_values))


def _eval_split(task: Any) -> str:
    splits = list(task.metadata.eval_splits)
    if not splits:
        raise ValueError(f"MTEB task {task.metadata.name} has no eval splits.")
    return str(splits[0])


def _dataset_subset(task: Any) -> str:
    subsets = list(getattr(task, "hf_subsets", []) or [])
    if subsets:
        return str(subsets[0])
    keys = list(task.dataset)
    if not keys:
        raise ValueError(f"MTEB task {task.metadata.name} loaded no dataset subsets.")
    return str(keys[0])


def _split_metadata(
    *,
    dataset_config: dict[str, Any],
    task: Any,
    subset: str,
    eval_split: str,
    old_source_dataset_name: str | None,
) -> dict[str, Any]:
    metadata = dict(cast(dict[str, Any], dataset_config.get("metadata") or {}))
    dataset_info = dict(task.metadata.dataset)
    source_dataset_id = str(dataset_info.get("path") or "")
    source_revision = str(dataset_info.get("revision") or "")
    metadata.update(
        {
            "source_benchmark_name": "MTEB task registry",
            "source_task": str(task.metadata.name),
            "source_dataset_id": source_dataset_id,
            "source_dataset_revision": source_revision,
            "source_dataset_subset": subset,
            "source_eval_split": eval_split,
            "source_dataset_location": f"{source_dataset_id} ({subset}/{eval_split})",
            "source_split_policy": f"MTEB eval split `{eval_split}` from subset `{subset}`",
            "source_links": [
                f"https://huggingface.co/datasets/{source_dataset_id}",
                "https://github.com/embeddings-benchmark/mteb",
            ],
            "source_hard_negative_note": (
                "Source relevance rows with score <= 0 are used as hard-negative corpus candidates when present; "
                "otherwise corpus fill follows source corpus order after qrels-positive documents."
            ),
            "upstream_license_target": "the upstream MTEB task sources and their original datasets",
        }
    )
    if old_source_dataset_name is not None:
        metadata["historical_nano_dataset_name"] = old_source_dataset_name
    return metadata


def validate_dataset_dir(*, dataset_dir: Path) -> dict[str, Any]:
    split_sets = {
        config: {path.stem for path in (dataset_dir / config).glob("*.parquet")}
        for config in CONFIGS
    }
    all_splits = sorted(set().union(*split_sets.values()))
    issues: list[str] = []
    for config, splits in split_sets.items():
        if splits != set(all_splits):
            issues.append(f"{config} split set differs: {sorted(splits)}")

    missing_after = 0
    counts: list[dict[str, Any]] = []
    for split in all_splits:
        queries = _read_parquet(dataset_dir / "queries" / f"{split}.parquet")
        corpus = _read_parquet(dataset_dir / "corpus" / f"{split}.parquet")
        qrels = _read_parquet(dataset_dir / "qrels" / f"{split}.parquet")
        bm25 = _read_parquet(dataset_dir / "bm25" / f"{split}.parquet")
        query_ids = [str(row["_id"]) for row in queries]
        corpus_ids = [str(row["_id"]) for row in corpus]
        if len(query_ids) != len(set(query_ids)):
            issues.append(f"{split}: duplicate query ids")
        if len(corpus_ids) != len(set(corpus_ids)):
            issues.append(f"{split}: duplicate corpus ids")
        query_id_set = set(query_ids)
        corpus_id_set = set(corpus_ids)
        for row in qrels:
            if "score" in row:
                issues.append(f"{split}: qrels contains score column")
                break
            if str(row["query-id"]) not in query_id_set or str(row["corpus-id"]) not in corpus_id_set:
                issues.append(f"{split}: qrels references missing ids")
                break
        for row in bm25:
            ids = [str(value) for value in row["corpus-ids"]]
            if str(row["query-id"]) not in query_id_set:
                issues.append(f"{split}: bm25 references missing query id")
                break
            if len(ids) != len(set(ids)):
                issues.append(f"{split}: bm25 row has duplicate corpus ids")
                break
            if any(corpus_id not in corpus_id_set for corpus_id in ids):
                issues.append(f"{split}: bm25 references missing corpus id")
                break
        metadata = _read_optional_json(dataset_dir / "metadata" / f"{split}.json")
        raw_bm25_metadata = metadata.get("bm25")
        bm25_metadata = raw_bm25_metadata if isinstance(raw_bm25_metadata, dict) else {}
        missing_after += int(bm25_metadata.get("missing_positive_doc_count_after_forcing") or 0)
        counts.append(
            {
                "split_name": split,
                "queries": len(queries),
                "corpus": len(corpus),
                "qrels": len(qrels),
                "bm25": len(bm25),
            }
        )
    return {
        "dataset_dir": str(dataset_dir),
        "splits": all_splits,
        "counts": counts,
        "missing_positive_doc_count_after_forcing": missing_after,
        "issues": issues,
    }


def _dataset_readme_metadata(dataset_config: dict[str, Any]) -> dict[str, Any]:
    metadata = dict(cast(dict[str, Any], dataset_config.get("metadata") or {}))
    metadata.update(
        {
            "source_benchmark_name": "MTEB task registry",
            "source_dataset_location": "the per-split upstream MTEB task datasets listed in the Split Mapping table",
            "source_split_policy": "each split uses the first MTEB eval split declared by the task",
            "source_links": [
                "https://github.com/embeddings-benchmark/mteb",
                "https://huggingface.co/mteb",
            ],
            "upstream_license_target": "the upstream MTEB task sources and their original datasets",
        }
    )
    return metadata


def _old_repo_files() -> dict[str, set[str]]:
    source_names = set(DIRECT_SOURCE_BY_TARGET.values()) | set(MISC_SOURCE_CANDIDATES) | set(SPLIT_MOVES_TO_MISC)
    files: dict[str, set[str]] = {}
    for source_name in sorted(source_names):
        dataset_id = SOURCE_DATASET_IDS[source_name]
        try:
            files[dataset_id] = set(list_repo_files(dataset_id, repo_type="dataset"))
        except Exception:
            files[dataset_id] = set()
    return files


def _old_source_dataset_name(
    *,
    dataset_name: str,
    split_name: str,
    old_repo_files: dict[str, set[str]],
) -> str | None:
    if dataset_name != "NanoMTEB-Misc":
        return DIRECT_SOURCE_BY_TARGET[dataset_name]
    for source_name, moved_splits in SPLIT_MOVES_TO_MISC.items():
        if split_name in moved_splits:
            return source_name
    for source_name in MISC_SOURCE_CANDIDATES:
        dataset_id = SOURCE_DATASET_IDS[source_name]
        files = old_repo_files.get(dataset_id, set())
        if any(
            candidate in files
            for candidate in (
                f"queries/{split_name}.parquet",
                f"queries/{split_name}-00000-of-00001.parquet",
                f"{split_name}/queries/test.parquet",
            )
        ):
            return source_name
    return None


def _old_split_metadata(
    old_source_dataset_name: str | None,
    split_name: str,
    *,
    old_repo_files: dict[str, set[str]],
) -> dict[str, Any]:
    if old_source_dataset_name is None:
        return {}
    dataset_id = SOURCE_DATASET_IDS[old_source_dataset_name]
    files = old_repo_files.get(dataset_id, set())
    for filename in (f"metadata/{split_name}.json", f"{split_name}/metadata/test.json"):
        if filename not in files:
            continue
        try:
            path = Path(hf_hub_download(dataset_id, filename, repo_type="dataset"))
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
        return data if isinstance(data, dict) else {}
    return {}


def _dataset_config(*, config_root: Path, dataset_name: str) -> dict[str, Any]:
    for path in sorted((config_root / "datasets").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("name") == dataset_name:
            return data
    raise FileNotFoundError(f"Could not find dataset config for {dataset_name}")


def _clean_output(*, output_root: Path, dataset_names: list[str]) -> None:
    for dataset_name in dataset_names:
        path = output_root / dataset_name
        if path.exists():
            shutil.rmtree(path)


def _split_output_exists(*, output_root: Path, plan: SplitPlan) -> bool:
    dataset_dir = output_root / plan.dataset_name
    return all((dataset_dir / config / f"{plan.split_name}.parquet").exists() for config in CONFIGS)


def _read_parquet(path: Path) -> list[dict[str, Any]]:
    return [dict(row) for row in pq.read_table(path).to_pylist()]


def _read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _parse_csv(value: str | None) -> set[str]:
    if value is None or not value.strip():
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def _mteb_module() -> Any:
    try:
        return importlib.import_module("mteb")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "The mteb package is required for this script. Run it as "
            "`uv run --with mteb python scripts/recreate_nanomteb_datasets_from_mteb.py ...`."
        ) from exc


if __name__ == "__main__":
    main()
