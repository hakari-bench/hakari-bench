from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from hakari_bench.bm25 import BM25Config, BM25Tokenizer  # noqa: E402
from hakari_bench.nano_dataset_builder import build_nano_dataset_from_rows  # noqa: E402
from hakari_bench.nano_dataset_builder import _write_readme as write_nano_readme  # noqa: E402
from scripts.recreate_nanomteb_datasets_from_mteb import (  # noqa: E402
    CONFIGS,
    DEFAULT_DOC_LIMIT,
    DEFAULT_QUERY_LIMIT,
    DEFAULT_TOP_K,
    _eval_split,
    _load_mteb_source,
    _mteb_module,
    build_plan as build_legacy_plan,
    validate_dataset_dir,
)


OFFICIAL_BENCHMARKS: dict[str, str] = {
    "MTEB(eng, v2)": "NanoMTEB-v2",
    "MTEB(Multilingual, v2)": "NanoMMTEB-v2",
    "MTEB(cmn, v1)": "NanoCMTEB",
    "MTEB(nld, v1)": "NanoMTEB-Dutch",
    "MTEB(fra, v1)": "NanoMTEB-French",
    "MTEB(deu, v1)": "NanoMTEB-German",
    "JMTEB(v2)": "NanoJMTEB-v2",
    "MTEB(kor, v1)": "NanoMTEB-Korean",
    "MTEB(fas, v2)": "NanoFaMTEB-v2",
    "MTEB(rus, v1.1)": "NanoRuMTEB",
    "MTEB(Scandinavian, v1)": "NanoMTEB-Scandinavian",
    "MTEB(spa, v1)": "NanoMTEB-Spanish",
    "MTEB(tha, v1)": "NanoMTEB-Thai",
    "VN-MTEB (vie, v1)": "NanoVNMTEB",
}

ADDON_GROUPS = {
    "NanoIndicQA",
    "NanoMTEB-Misc",
    "NanoMuPLeR",
    "NanoMTEB-Dutch",
    "NanoMTEB-French",
    "NanoMTEB-German",
    "NanoMTEB-Korean",
    "NanoMTEB-Polish",
    "NanoVNMTEB",
}


@dataclass(frozen=True)
class PlannedTask:
    group: str
    subset: str
    split: str
    task_name: str
    source_subsets: tuple[str, ...] | None
    benchmark_name: str
    status: str
    note: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recreate regrouped NanoMTEB-family datasets from MTEB task sources."
    )
    parser.add_argument("--output-root", type=Path, default=Path("output/nano_datasets"))
    parser.add_argument("--config-root", type=Path, default=Path("config"))
    parser.add_argument("--groups", default=None, help="Comma-separated Nano groups to recreate.")
    parser.add_argument("--splits", default=None, help="Comma-separated output split names to recreate.")
    parser.add_argument("--query-limit", type=int, default=DEFAULT_QUERY_LIMIT)
    parser.add_argument("--doc-limit", type=int, default=DEFAULT_DOC_LIMIT)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--bm25-tokenizer", default="regex")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--plan-json", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected_groups = _parse_csv(args.groups)
    selected_splits = _parse_csv(args.splits)
    plans = build_plan(config_root=args.config_root)
    plans = [
        plan
        for plan in plans
        if (not selected_groups or plan.group in selected_groups)
        and (not selected_splits or plan.split in selected_splits)
    ]
    if args.plan_json is not None:
        args.plan_json.parent.mkdir(parents=True, exist_ok=True)
        args.plan_json.write_text(
            json.dumps([plan.__dict__ for plan in plans], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.clean:
        for group in sorted({plan.group for plan in plans}):
            path = args.output_root / group
            if path.exists():
                shutil.rmtree(path)
    args.output_root.mkdir(parents=True, exist_ok=True)

    bm25_config = BM25Config(
        tokenizer=cast(BM25Tokenizer, args.bm25_tokenizer),
        top_k=args.top_k,
    )
    for index, plan in enumerate(plans, start=1):
        if not args.overwrite and _task_output_exists(output_root=args.output_root, plan=plan):
            print(
                f"[{index}/{len(plans)}] skip existing {plan.group}/{plan.subset}/{plan.split}",
                flush=True,
            )
            continue
        print(
            f"[{index}/{len(plans)}] {plan.group}/{plan.subset}/{plan.split} <- {plan.task_name}",
            flush=True,
        )
        build_task(
            plan=plan,
            output_root=args.output_root,
            query_limit=args.query_limit,
            doc_limit=args.doc_limit,
            bm25_config=bm25_config,
        )

    write_group_readmes_and_audits(output_root=args.output_root, plans=plans)


def build_plan(*, config_root: Path) -> list[PlannedTask]:
    mteb = _mteb_module()
    plans: list[PlannedTask] = []
    for benchmark in mteb.get_benchmarks():
        group = OFFICIAL_BENCHMARKS.get(str(benchmark.name))
        if group is None:
            continue
        for task in benchmark.tasks:
            if str(task.metadata.type) != "Retrieval":
                continue
            plans.extend(_official_plans(group=group, benchmark_name=str(benchmark.name), task=task))

    legacy_misc = build_legacy_plan(
        config_root=config_root,
        selected_datasets={"NanoMTEB-Misc"},
        selected_splits=set(),
    )
    for legacy in legacy_misc:
        group = _misc_group(legacy.split_name)
        if group is None:
            continue
        task = mteb.get_tasks(tasks=[legacy.task_name])[0]
        subset = _source_config_name(str(task.metadata.dataset.get("path") or ""))
        split = _misc_split_name(legacy.split_name)
        plans.append(
            PlannedTask(
                group=group,
                subset=subset,
                split=split,
                task_name=str(task.metadata.name),
                source_subsets=legacy.source_subsets,
                benchmark_name="NanoMTEB-Misc regrouped source",
                status="addon-regrouped",
                note=_misc_note(legacy.split_name),
            )
        )
    return _dedupe_plans(plans)


def _official_plans(*, group: str, benchmark_name: str, task: Any) -> list[PlannedTask]:
    task_name = str(task.metadata.name)
    subset = _source_config_name(str(task.metadata.dataset.get("path") or ""))
    plans: list[PlannedTask] = []
    for source_subset in _selected_source_subsets(group=group, task=task):
        split = _official_split_name(task_name, source_subset=source_subset)
        plans.append(
            PlannedTask(
                group=group,
                subset=subset,
                split=split,
                task_name=task_name,
                source_subsets=None if source_subset == "combined" else (source_subset,),
                benchmark_name=benchmark_name,
                status="official",
                note=f"from MTEB registry benchmark {benchmark_name}",
            )
        )
    return plans


def _selected_source_subsets(*, group: str, task: Any) -> tuple[str, ...]:
    task_name = str(task.metadata.name)
    if group == "NanoMMTEB-v2":
        return ("combined",)
    if group == "NanoMTEB-Dutch":
        if task_name == "BelebeleRetrieval":
            return ("nld_Latn-nld_Latn", "nld_Latn-eng_Latn", "eng_Latn-nld_Latn")
        if task_name == "WebFAQRetrieval":
            return ("nld",)
        if task_name == "WikipediaRetrievalMultilingual":
            return ("nl",)
    if group == "NanoMTEB-French":
        if task_name == "XPQARetrieval":
            return ("fra-fra", "eng-fra", "fra-eng")
        if task_name == "MintakaRetrieval":
            return ("fr",)
    if group == "NanoMTEB-German" and task_name == "XMarket":
        return ("de",)
    if group == "NanoMTEB-Spanish":
        if task_name.startswith("MIRACLRetrieval"):
            return ("es",)
        if task_name == "MintakaRetrieval":
            return ("es",)
        if task_name == "XPQARetrieval":
            return ("spa-spa", "eng-spa", "spa-eng")
    if group == "NanoMTEB-Thai":
        if task_name == "BelebeleRetrieval":
            return ("tha_Thai-tha_Thai", "tha_Thai-eng_Latn", "eng_Latn-tha_Thai")
        if task_name.startswith("MIRACLRetrieval"):
            return ("th",)
        if task_name == "MKQARetrieval":
            return ("th",)
        if task_name == "MrTidyRetrieval":
            return ("thai",)
        if task_name == "MultiLongDocRetrieval":
            return ("th",)
        if task_name == "WebFAQRetrieval":
            return ("tha",)
        if task_name == "XQuADRetrieval":
            return ("th",)
    if group == "NanoMTEB-Korean" and task_name == "MIRACLRetrieval":
        return ("ko",)
    if group == "NanoJMTEB-v2":
        if task_name == "MrTidyRetrieval":
            return ("japanese",)
        if task_name == "MIRACLRetrieval":
            return ("ja",)
        if task_name == "MintakaRetrieval":
            return ("ja",)
        if task_name == "MultiLongDocRetrieval":
            return ("ja",)
    if group == "NanoFaMTEB-v2":
        if task_name == "WikipediaRetrievalMultilingual":
            return ("fa",)
        if task_name.startswith("MIRACLRetrieval"):
            return ("fa",)
        if task_name.startswith("NeuCLIR2023"):
            return ("fas",)
        if task_name == "WebFAQRetrieval":
            return ("fas",)
    if group == "NanoRuMTEB" and task_name.startswith("MIRACLRetrieval"):
        return ("ru",)
    return ("default",)


def build_task(
    *,
    plan: PlannedTask,
    output_root: Path,
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
        split_name=plan.split,
        source_subsets=plan.source_subsets,
    )
    metadata = _task_metadata(
        task=task,
        plan=plan,
        source_subset=str(source["source_subset"]),
        eval_split=eval_split,
    )
    build_nano_dataset_from_rows(
        output_dir=output_root / plan.group / plan.subset,
        dataset_name=plan.group,
        dataset_id=f"hakari-bench/{plan.group}",
        split_name=plan.split,
        corpus_rows=source["corpus_rows"],
        query_rows=source["query_rows"],
        qrels_rows=source["qrels_rows"],
        query_limit=query_limit,
        doc_limit=doc_limit,
        bm25_config=bm25_config,
        metadata=metadata,
    )


def _task_metadata(*, task: Any, plan: PlannedTask, source_subset: str, eval_split: str) -> dict[str, Any]:
    dataset_info = dict(task.metadata.dataset)
    source_dataset_id = str(dataset_info.get("path") or "")
    source_revision = str(dataset_info.get("revision") or "")
    return {
        "language": _metadata_language(task),
        "category": "natural_language",
        "short_description": f"{plan.group} retrieval split from {task.metadata.name}.",
        "description": str(getattr(task.metadata, "description", "") or f"{task.metadata.name} retrieval task."),
        "source_benchmark_name": plan.benchmark_name,
        "source_task": str(task.metadata.name),
        "source_dataset_id": source_dataset_id,
        "source_dataset_revision": source_revision,
        "source_dataset_subset": source_subset,
        "source_public_subset": plan.subset,
        "source_eval_split": eval_split,
        "source_dataset_location": f"{source_dataset_id} ({source_subset}/{eval_split})",
        "source_split_policy": f"MTEB eval split `{eval_split}` from source slice `{source_subset}`",
        "source_links": [
            f"https://huggingface.co/datasets/{source_dataset_id}",
            "https://github.com/embeddings-benchmark/mteb",
        ],
        "source_hard_negative_note": _hard_negative_note(plan),
        "upstream_license_target": "the upstream MTEB task sources and their original datasets",
        "mteb_regrouping_status": plan.status,
        "mteb_regrouping_note": plan.note,
    }


def _metadata_language(task: Any) -> str:
    languages = list(getattr(task.metadata, "languages", []) or [])
    if len(languages) == 1:
        return str(languages[0])
    if languages:
        return "multilingual"
    return "unknown"


def _hard_negative_note(plan: PlannedTask) -> str:
    if "HardNegatives" in plan.task_name:
        return (
            "This Nano split uses the hard-negative source variant. The corresponding base source, "
            "when present, is treated as related provenance rather than a separate Nano task."
        )
    return (
        "Source relevance rows with score <= 0 are used as hard-negative corpus candidates when present; "
        "otherwise corpus fill follows source corpus order after qrels-positive documents."
    )


def write_group_readmes_and_audits(*, output_root: Path, plans: list[PlannedTask]) -> None:
    plans_by_subset = {(plan.group, plan.subset): plan for plan in plans}
    for group in sorted({plan.group for plan in plans}):
        group_dir = output_root / group
        if not group_dir.exists():
            continue
        subset_audits: dict[str, Any] = {}
        issues: list[str] = []
        missing_after = 0
        split_count = 0
        for subset_dir in sorted(path for path in group_dir.iterdir() if path.is_dir()):
            if not all((subset_dir / config).exists() for config in CONFIGS):
                continue
            audit = validate_dataset_dir(dataset_dir=subset_dir)
            subset_audits[subset_dir.name] = audit
            issues.extend(f"{subset_dir.name}: {issue}" for issue in audit["issues"])
            missing_after += int(audit["missing_positive_doc_count_after_forcing"])
            split_count += len(audit["splits"])
            subset_plan = plans_by_subset.get((group, subset_dir.name))
            if subset_plan is not None:
                write_nano_readme(
                    output_dir=subset_dir,
                    dataset_name=group,
                    dataset_id=f"hakari-bench/{group}",
                    metadata=_readme_metadata_for_plan(subset_plan),
                )
        group_audit = {
            "dataset_dir": str(group_dir),
            "subsets": sorted(subset_audits),
            "split_count": split_count,
            "missing_positive_doc_count_after_forcing": missing_after,
            "issues": issues,
            "subset_audits": subset_audits,
        }
        (group_dir / "audit.json").write_text(
            json.dumps(group_audit, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        write_nano_readme(
            output_dir=group_dir,
            dataset_name=group,
            dataset_id=f"hakari-bench/{group}",
            metadata=_group_metadata(group=group),
        )
        print(
            f"[audit] {group}: subsets={len(subset_audits)} splits={split_count} "
            f"issues={len(issues)} missing_forced={missing_after}",
            flush=True,
        )


def _readme_metadata_for_plan(plan: PlannedTask) -> dict[str, Any]:
    mteb = _mteb_module()
    task = mteb.get_tasks(tasks=[plan.task_name])[0]
    source_subset = plan.source_subsets[0] if plan.source_subsets else "combined"
    return _task_metadata(task=task, plan=plan, source_subset=source_subset, eval_split=_eval_split(task))


def _group_metadata(*, group: str) -> dict[str, Any]:
    return {
        "language": "multilingual" if group in {"NanoMMTEB-v2", "NanoMuPLeR", "NanoEuroPIRQ"} else "unknown",
        "category": "natural_language",
        "short_description": f"{group} regrouped Nano retrieval dataset.",
        "description": (
            f"{group} is a Nano-style retrieval dataset recreated from MTEB task registry sources. "
            "Public subsets are source datasets, and splits are source-local retrieval tasks."
        ),
        "source_benchmark_name": "MTEB task registry and documented source-family groups",
        "source_dataset_location": "per-subset source datasets listed in split metadata",
        "source_split_policy": "source dataset config names are public subsets; source slices are recorded in metadata",
        "source_links": [
            "https://github.com/embeddings-benchmark/mteb",
            "https://huggingface.co/mteb",
        ],
        "upstream_license_target": "the upstream MTEB task sources and their original datasets",
    }


def _dedupe_plans(plans: list[PlannedTask]) -> list[PlannedTask]:
    selected: dict[tuple[str, str, str], PlannedTask] = {}
    for plan in plans:
        key = (plan.group, plan.subset, plan.split)
        current = selected.get(key)
        if current is None:
            selected[key] = plan
            continue
        if _plan_priority(plan) < _plan_priority(current):
            selected[key] = plan
    return sorted(selected.values(), key=lambda plan: (plan.group, plan.subset, plan.split))


def _plan_priority(plan: PlannedTask) -> tuple[int, int]:
    status_priority = 0 if plan.status == "official" else 1
    hard_negative_priority = 0 if "HardNegatives" in plan.task_name else 1
    return (status_priority, hard_negative_priority)


def _task_output_exists(*, output_root: Path, plan: PlannedTask) -> bool:
    subset_dir = output_root / plan.group / plan.subset
    return all((subset_dir / config / f"{plan.split}.parquet").exists() for config in CONFIGS)


def _source_config_name(source_dataset_id: str) -> str:
    if "/" not in source_dataset_id:
        return source_dataset_id or "unknown"
    org, dataset_name = source_dataset_id.split("/", maxsplit=1)
    if org == "mteb":
        return "mteb"
    return f"{org}__{dataset_name}"


def _official_split_name(task_name: str, *, source_subset: str) -> str:
    split = _kebab_task_name(task_name)
    if source_subset not in {"default", "combined"}:
        source_suffix = source_subset.replace("_", "-").lower()
        if source_suffix not in split:
            split = f"{split}-{source_suffix}"
    return split


def _misc_group(split_name: str) -> str | None:
    if split_name.startswith("NanoMuPLeR"):
        return "NanoMuPLeR"
    if split_name.startswith("NanoIndicQA"):
        return "NanoIndicQA"
    if split_name.startswith("NanoEuroPIRQ"):
        return "NanoMTEB-Misc"
    if split_name.startswith("NanoNeuCLIR2022"):
        return "NanoMTEB-Misc"
    if split_name.startswith("NanoWMT"):
        return "NanoMTEB-Misc"
    if split_name.startswith("NanoRuSciBench"):
        return "NanoMTEB-Misc"
    if split_name.startswith("NanoCQADupstack") and split_name.endswith("PL"):
        return "NanoMTEB-Polish"
    if split_name in {"NanoFiQAPL", "NanoNQPL", "NanoNQPLHardNegatives", "NanoPUGG", "NanoQuoraPL", "NanoQuoraPLHardNegatives"}:
        return "NanoMTEB-Polish"
    if split_name.startswith("NanoCQADupstack") and split_name.endswith("NL"):
        return "NanoMTEB-Dutch"
    if split_name in {"NanoFEVERNL", "NanoNQNL", "NanoQuoraNL"}:
        return "NanoMTEB-Dutch"
    if split_name == "NanoFQuAD":
        return "NanoMTEB-French"
    if split_name == "NanoGermanGovService":
        return "NanoMTEB-German"
    if split_name in {"NanoAutoRAG", "NanoLawIRKo", "NanoSQuADKorV1"}:
        return "NanoMTEB-Korean"
    if split_name in {"NanoNanoFEVERVN", "NanoNanoNQVN"}:
        return "NanoVNMTEB"
    return None


def _misc_split_name(split_name: str) -> str:
    if split_name.startswith("NanoMuPLeR"):
        return split_name.removeprefix("NanoMuPLeR").lower()
    if split_name.startswith("NanoIndicQA"):
        return split_name.removeprefix("NanoIndicQA").lower()
    if split_name.startswith("NanoEuroPIRQ"):
        return split_name.removeprefix("NanoEuroPIRQ").lower()
    match = re.match(r"NanoNeuCLIR(20\d\d)(Fa|Ru|Zh)", split_name)
    if match is not None:
        return f"{match.group(1)}-{match.group(2).lower()}"
    match = re.match(r"NanoWMT(\d\d)(De|Fr)(Fr|De)", split_name)
    if match is not None:
        return f"wmt{match.group(1)}-{match.group(2).lower()}-{match.group(3).lower()}"
    if split_name.startswith("NanoCQADupstack"):
        base = split_name.removeprefix("NanoCQADupstack")
        base = re.sub(r"(PL|NL)$", "", base)
        return f"cqadupstack-{_kebab_task_name(base)}"
    direct = {
        "NanoFiQAPL": "fiqa",
        "NanoNQPL": "nq",
        "NanoNQPLHardNegatives": "nq",
        "NanoPUGG": "pugg",
        "NanoQuoraPL": "quora",
        "NanoQuoraPLHardNegatives": "quora",
        "NanoFEVERNL": "fever",
        "NanoNQNL": "nq",
        "NanoQuoraNL": "quora",
        "NanoFQuAD": "fquad",
        "NanoGermanGovService": "gov-service",
        "NanoAutoRAG": "autorag",
        "NanoLawIRKo": "lawir-ko",
        "NanoSQuADKorV1": "squad-kor-v1",
        "NanoRuSciBenchCite": "cite-ru",
        "NanoRuSciBenchCocite": "cocite-ru",
        "NanoNanoFEVERVN": "nano-fever",
        "NanoNanoNQVN": "nano-nq",
    }
    return direct.get(split_name, _kebab_task_name(split_name))


def _misc_note(split_name: str) -> str:
    if split_name in {"NanoNQPLHardNegatives", "NanoQuoraPLHardNegatives"} or "NeuCLIR2022" in split_name:
        return "HardNegatives source selected; base source folded into this split"
    if split_name in {"NanoNanoFEVERVN", "NanoNanoNQVN"}:
        return "optional historical nano VN addon; check overlap with VN-MTEB official FEVER/NQ before publishing"
    return "regrouped from current NanoMTEB-Misc according to source-family and language-family rules"


def _kebab_task_name(value: str) -> str:
    value = value.removeprefix("Nano")
    value = value.replace("MIRACLRetrieval", "MIRACL")
    value = value.replace("Retrieval", "")
    value = re.sub(r"HardNegatives(?:V2)?", "", value)
    value = value.replace(".v2", "").replace(".V2", "")
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = value.replace("_", "-").replace(" ", "-")
    value = re.sub(r"-+", "-", value)
    return value.strip("-").lower()


def _parse_csv(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


if __name__ == "__main__":
    main()
