from __future__ import annotations


NANOJMTEB_TASK_NAME_ALIASES = {
    "NanoJaMIRACL": "NanoMIRACL",
    "NanoJaMintaka": "NanoMintaka",
    "NanoJaMrTidy": "NanoMrTidy",
    "NanoJaMultiLongDoc": "NanoMultiLongDoc",
    "NanoJaNLPJournalAbsArticle": "NanoNLPJournalAbsArticle",
    "NanoJaNLPJournalAbsIntro": "NanoNLPJournalAbsIntro",
    "NanoJaNLPJournalTitleAbs": "NanoNLPJournalTitleAbs",
    "NanoJaNLPJournalTitleIntro": "NanoNLPJournalTitleIntro",
}


def canonical_task_name(benchmark: str, task_name: str) -> str:
    if benchmark != "NanoJMTEB":
        return task_name
    return NANOJMTEB_TASK_NAME_ALIASES.get(task_name, task_name)


def canonical_split_name(benchmark: str, split_name: str | None) -> str:
    return canonical_task_name(benchmark, split_name or "")


def canonical_task_key(*, benchmark: str, dataset_id: str, task_name: str) -> str:
    return f"{benchmark}::{dataset_id}::{canonical_task_name(benchmark, task_name)}"


def is_legacy_task_alias(benchmark: str, task_name: str) -> bool:
    return benchmark == "NanoJMTEB" and task_name in NANOJMTEB_TASK_NAME_ALIASES


def canonical_metric_name(benchmark: str, metric_name: str) -> str:
    if benchmark != "NanoJMTEB":
        return metric_name
    for legacy_name, canonical_name in NANOJMTEB_TASK_NAME_ALIASES.items():
        if metric_name == legacy_name:
            return canonical_name
        prefix = f"{legacy_name}_"
        if metric_name.startswith(prefix):
            return f"{canonical_name}_{metric_name.removeprefix(prefix)}"
    return metric_name
