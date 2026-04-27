from __future__ import annotations

from pathlib import Path

import pytest

from nano_ir_benchmark.datasets import (
    DatasetRegistry,
    NanoDatasetSpec,
    resolve_dataset_splits,
    resolve_eval_tasks,
)


def test_builtin_registry_contains_requested_benchmarks() -> None:
    registry = DatasetRegistry.load_builtin()

    assert registry.get_dataset("NanoBEIR-en").dataset_id == "sentence-transformers/NanoBEIR-en"
    assert registry.get_dataset("NanoMIRACL").dataset_id == "hotchpotch/NanoMIRACL"
    assert registry.get_dataset("NanoMLDR").dataset_id == "hotchpotch/NanoMLDR"
    assert registry.get_dataset("NanoJMTEB").dataset_id == "hotchpotch/NanoJMTEB"
    assert registry.get_dataset("NanoRTEB").dataset_id == "hotchpotch/NanoRTEB"
    assert registry.get_dataset("NanoCodeSearchNet").dataset_id == "hotchpotch/NanoCodeSearchNet"
    assert len(registry.get_collection("MNanoBEIR").datasets) == 14


def test_resolve_eval_tasks_for_builtin_nanorteb_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoRTEB"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoRTEB", "NanoAILACasedocs"),
        ("NanoRTEB", "NanoAILAStatutes"),
        ("NanoRTEB", "NanoLegalSummarization"),
        ("NanoRTEB", "NanoFinanceBench"),
        ("NanoRTEB", "NanoHC3Finance"),
        ("NanoRTEB", "NanoFinQA"),
        ("NanoRTEB", "NanoApps"),
        ("NanoRTEB", "NanoDS1000"),
        ("NanoRTEB", "NanoHumanEval"),
        ("NanoRTEB", "NanoMBPP"),
        ("NanoRTEB", "NanoWikiSQL"),
        ("NanoRTEB", "NanoFreshStack"),
        ("NanoRTEB", "NanoChatDoctor"),
        ("NanoRTEB", "NanoCUREv1"),
    ]


def test_resolve_eval_tasks_for_builtin_nanojmteb_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoJMTEB"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoJMTEB", "NanoJaCWIR"),
        ("NanoJMTEB", "NanoJaGovFaqs"),
        ("NanoJMTEB", "NanoJaqket"),
        ("NanoJMTEB", "NanoJaMIRACL"),
        ("NanoJMTEB", "NanoJaMintaka"),
        ("NanoJMTEB", "NanoJaMrTidy"),
        ("NanoJMTEB", "NanoJaMultiLongDoc"),
        ("NanoJMTEB", "NanoJaNLPJournalAbsArticle"),
        ("NanoJMTEB", "NanoJaNLPJournalAbsIntro"),
        ("NanoJMTEB", "NanoJaNLPJournalTitleAbs"),
        ("NanoJMTEB", "NanoJaNLPJournalTitleIntro"),
    ]


def test_resolve_eval_tasks_for_builtin_nanomldr_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoMLDR"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoMLDR", "ar"),
        ("NanoMLDR", "de"),
        ("NanoMLDR", "en"),
        ("NanoMLDR", "es"),
        ("NanoMLDR", "fr"),
        ("NanoMLDR", "hi"),
        ("NanoMLDR", "it"),
        ("NanoMLDR", "ja"),
        ("NanoMLDR", "ko"),
        ("NanoMLDR", "pt"),
        ("NanoMLDR", "ru"),
        ("NanoMLDR", "th"),
        ("NanoMLDR", "zh"),
    ]


def test_resolve_eval_tasks_expands_mnanobeir_collection() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=[], collection_values=["MNanoBEIR"], split_values=["msmarco"])

    assert len(tasks) == 14
    assert tasks[0].dataset_id == "sentence-transformers/NanoBEIR-en"
    assert tasks[0].split_name == "NanoMSMARCO"
    assert tasks[0].task_name == "msmarco"


def test_resolve_eval_tasks_accepts_direct_dataset_id(monkeypatch: pytest.MonkeyPatch) -> None:
    registry = DatasetRegistry.load_builtin()
    monkeypatch.setattr(
        "nano_ir_benchmark.datasets.get_dataset_split_names",
        lambda dataset_id, subset: ["ja", "en"],
    )

    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=["hotchpotch/NanoMIRACL"],
        collection_values=[],
        split_values=[],
    )

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoMIRACL", "ja"),
        ("NanoMIRACL", "en"),
    ]


def test_resolve_dataset_splits_uses_yaml_splits_without_network() -> None:
    spec = NanoDatasetSpec(
        name="Toy",
        dataset_id="local/toy",
        corpus_config="corpus",
        queries_config="queries",
        qrels_config="qrels",
        candidate_config="bm25",
        splits=["a", "b"],
    )

    assert resolve_dataset_splits(spec) == ["a", "b"]


def test_registry_loads_yaml_files(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "dataset_collections").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
corpus_config: corpus
queries_config: queries
qrels_config: qrels
candidate_config: bm25
splits: [a]
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "dataset_collections" / "toy_collection.yaml").write_text(
        """
name: ToyCollection
datasets:
  - Toy
""".strip(),
        encoding="utf-8",
    )

    registry = DatasetRegistry.load_from_root(tmp_path)

    assert registry.get_dataset("Toy").dataset_id == "local/toy"
    assert registry.get_collection("ToyCollection").datasets == ["Toy"]
