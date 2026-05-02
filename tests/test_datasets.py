from __future__ import annotations

from pathlib import Path

import pytest

from nano_ir_benchmark.datasets import (
    DatasetRegistry,
    NanoDatasetSpec,
    resolve_dataset_revision,
    resolve_dataset_splits,
    resolve_eval_tasks,
)


def test_builtin_registry_contains_requested_benchmarks() -> None:
    registry = DatasetRegistry.load_builtin()

    assert registry.get_dataset("NanoBEIR-en").dataset_id == "hakari-bench/NanoBEIR-en"
    assert registry.get_dataset("NanoMIRACL").dataset_id == "hakari-bench/NanoMIRACL"
    assert registry.get_dataset("NanoMLDR").dataset_id == "hakari-bench/NanoMLDR"
    assert registry.get_dataset("NanoJMTEB").dataset_id == "hakari-bench/NanoJMTEB"
    assert registry.get_dataset("NanoRTEB").dataset_id == "hakari-bench/NanoRTEB"
    assert registry.get_dataset("NanoMTEB").dataset_id == "hakari-bench/NanoMTEB"
    assert registry.get_dataset("NanoMMTEB").dataset_id == "hakari-bench/NanoMMTEB"
    assert registry.get_dataset("NanoCMTEB").dataset_id == "hakari-bench/NanoCMTEB"
    assert registry.get_dataset("NanoLongEmbed").dataset_id == "hakari-bench/NanoLongEmbed"
    assert registry.get_dataset("NanoCoIR").dataset_id == "hakari-bench/NanoCoIR"
    assert registry.get_dataset("NanoIFIR").dataset_id == "hakari-bench/NanoIFIR"
    assert registry.get_dataset("NanoLaw").dataset_id == "hakari-bench/NanoLaw"
    assert registry.get_dataset("NanoMedical").dataset_id == "hakari-bench/NanoMedical"
    assert registry.get_dataset("NanoRARb").dataset_id == "hakari-bench/NanoRARb"
    assert registry.get_dataset("NanoBRIGHT").dataset_id == "hakari-bench/NanoBRIGHT"
    assert registry.get_dataset("NanoCodeRAG").dataset_id == "hakari-bench/NanoCodeRAG"
    assert registry.get_dataset("NanoChemTEB").dataset_id == "hakari-bench/NanoChemTEB"
    assert registry.get_dataset("NanoR2MED").dataset_id == "hakari-bench/NanoR2MED"
    assert registry.get_dataset("NanoBuiltBench").dataset_id == "hakari-bench/NanoBuiltBench"
    assert len(registry.get_collection("MNanoBEIR").datasets) == 14


def test_resolve_eval_tasks_for_builtin_nanomteb_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoMTEB"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoMTEB", "NanoArguAna"),
        ("NanoMTEB", "NanoCQADupstackGaming"),
        ("NanoMTEB", "NanoCQADupstackUnix"),
        ("NanoMTEB", "NanoClimateFEVERHardNegatives"),
        ("NanoMTEB", "NanoFEVERHardNegatives"),
        ("NanoMTEB", "NanoFiQA2018"),
        ("NanoMTEB", "NanoHotpotQAHardNegatives"),
        ("NanoMTEB", "NanoSCIDOCS"),
        ("NanoMTEB", "NanoTouche2020"),
    ]


def test_resolve_eval_tasks_for_builtin_nanommteb_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoMMTEB"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoMMTEB", "NanoStackOverflowQA"),
        ("NanoMMTEB", "NanoTwitterHjerne"),
        ("NanoMMTEB", "NanoAILAStatutes"),
        ("NanoMMTEB", "NanoArguAna"),
        ("NanoMMTEB", "NanoHagrid"),
        ("NanoMMTEB", "NanoLegalBenchCorporateLobbying"),
        ("NanoMMTEB", "NanoLEMBPasskey"),
        ("NanoMMTEB", "NanoSCIDOCS"),
        ("NanoMMTEB", "NanoSpartQA"),
        ("NanoMMTEB", "NanoTempReasonL1"),
        ("NanoMMTEB", "NanoWinoGrande"),
        ("NanoMMTEB", "NanoBelebele"),
        ("NanoMMTEB", "NanoMLQA"),
        ("NanoMMTEB", "NanoStatcanDialogueDataset"),
        ("NanoMMTEB", "NanoWikipediaRetrievalMultilingual"),
        ("NanoMMTEB", "NanoCovid"),
        ("NanoMMTEB", "NanoNews21Instruction"),
        ("NanoMMTEB", "NanoMIRACLRetrievalHardNegatives"),
    ]


def test_resolve_eval_tasks_for_builtin_nanocmteb_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoCMTEB"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoCMTEB", "NanoT2Retrieval"),
        ("NanoCMTEB", "NanoMMarcoRetrieval"),
        ("NanoCMTEB", "NanoDuRetrieval"),
        ("NanoCMTEB", "NanoCovidRetrieval"),
        ("NanoCMTEB", "NanoCmedqaRetrieval"),
        ("NanoCMTEB", "NanoEcomRetrieval"),
        ("NanoCMTEB", "NanoMedicalRetrieval"),
        ("NanoCMTEB", "NanoVideoRetrieval"),
    ]


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


def test_resolve_eval_tasks_for_builtin_nanolongembed_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoLongEmbed"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoLongEmbed", "NanoNarrativeQA"),
        ("NanoLongEmbed", "NanoSummScreenFD"),
        ("NanoLongEmbed", "NanoQMSum"),
        ("NanoLongEmbed", "Nano2WikiMultihopQA"),
        ("NanoLongEmbed", "NanoPasskey"),
        ("NanoLongEmbed", "NanoNeedle"),
    ]


def test_resolve_eval_tasks_for_builtin_nanocoir_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoCoIR"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoCoIR", "NanoApps"),
        ("NanoCoIR", "NanoCodeFeedbackMT"),
        ("NanoCoIR", "NanoCodeFeedbackST"),
        ("NanoCoIR", "NanoCodeTransOceanContest"),
        ("NanoCoIR", "NanoCodeTransOceanDL"),
        ("NanoCoIR", "NanoCosQA"),
        ("NanoCoIR", "NanoStackOverflowQA"),
        ("NanoCoIR", "NanoSyntheticText2SQL"),
        ("NanoCoIR", "NanoCodeSearchNet"),
        ("NanoCoIR", "NanoCodeSearchNetCCR"),
    ]


def test_resolve_eval_tasks_for_new_builtin_nano_datasets_use_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    expected = {
        "NanoIFIR": [
            "NanoIFIRAila",
            "NanoIFIRCds",
            "NanoIFIRFiQA",
            "NanoIFIRFire",
            "NanoIFIRNFCorpus",
            "NanoIFIRPm",
            "NanoIFIRScifact",
        ],
        "NanoLaw": [
            "NanoAILACasedocs",
            "NanoAILAStatutes",
            "NanoLegalSummarization",
            "NanoGerDaLIRSmall",
            "NanoLeCaRDv2",
            "NanoLegalBenchConsumerContractsQA",
            "NanoLegalBenchCorporateLobbying",
            "NanoLegalQuAD",
        ],
        "NanoMedical": [
            "NanoCUREv1",
            "NanoNFCorpus",
            "NanoTRECCOVID",
            "NanoTRECCOVIDPL",
            "NanoSciFact",
            "NanoSciFactPL",
            "NanoMedicalQA",
            "NanoPublicHealthQA",
            "NanoCmedqa",
            "NanoCMedQAv2reranking",
        ],
        "NanoRARb": [
            "NanoARCChallenge",
            "NanoAlphaNLI",
            "NanoHellaSwag",
            "NanoWinoGrande",
            "NanoPIQA",
            "NanoSIQA",
            "NanoQuail",
            "NanoSpartQA",
            "NanoTempReasonL1",
            "NanoTempReasonL2Pure",
            "NanoTempReasonL2Fact",
            "NanoTempReasonL2Context",
            "NanoTempReasonL3Pure",
            "NanoTempReasonL3Fact",
            "NanoTempReasonL3Context",
            "NanoRARbCode",
            "NanoRARbMath",
        ],
        "NanoBRIGHT": [
            "NanoBrightBiology",
            "NanoBrightEarthScience",
            "NanoBrightEconomics",
            "NanoBrightPsychology",
            "NanoBrightRobotics",
            "NanoBrightStackoverflow",
            "NanoBrightSustainableLiving",
            "NanoBrightPony",
            "NanoBrightLeetcode",
            "NanoBrightAops",
            "NanoBrightTheoremQATheorems",
            "NanoBrightTheoremQAQuestions",
            "NanoBrightBiologyLong",
            "NanoBrightEarthScienceLong",
            "NanoBrightEconomicsLong",
            "NanoBrightPsychologyLong",
            "NanoBrightRoboticsLong",
            "NanoBrightStackoverflowLong",
            "NanoBrightSustainableLivingLong",
            "NanoBrightPonyLong",
        ],
        "NanoCodeRAG": [
            "NanoCodeRAGLibraryDocumentationSolutions",
            "NanoCodeRAGOnlineTutorials",
            "NanoCodeRAGProgrammingSolutions",
            "NanoCodeRAGStackoverflowPosts",
        ],
        "NanoChemTEB": ["NanoChemNQ", "NanoChemHotpotQA", "NanoChemRxiv"],
        "NanoR2MED": [
            "NanoR2MEDBiology",
            "NanoR2MEDBioinformatics",
            "NanoR2MEDMedicalSciences",
            "NanoR2MEDMedXpertQAExam",
            "NanoR2MEDMedQADiag",
            "NanoR2MEDPMCTreatment",
            "NanoR2MEDPMCClinical",
            "NanoR2MEDIIYiClinical",
        ],
        "NanoBuiltBench": ["NanoBuiltBench", "NanoBuiltBenchReranking"],
    }

    for dataset_name, split_names in expected.items():
        tasks = resolve_eval_tasks(registry=registry, dataset_values=[dataset_name], collection_values=[], split_values=[])
        assert [(task.dataset_name, task.split_name) for task in tasks] == [
            (dataset_name, split_name) for split_name in split_names
        ]


def test_resolve_eval_tasks_expands_mnanobeir_collection() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=[], collection_values=["MNanoBEIR"], split_values=["msmarco"])

    assert len(tasks) == 14
    assert tasks[0].dataset_id == "hakari-bench/NanoBEIR-en"
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
        dataset_values=["hakari-bench/NanoMIRACL"],
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


def test_resolve_dataset_revision_uses_huggingface_hub_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeDatasetInfo:
        sha = "abc123"

    class FakeHfApi:
        def dataset_info(self, repo_id: str, revision: str | None = None) -> FakeDatasetInfo:
            assert repo_id == "owner/dataset"
            assert revision == "main"
            return FakeDatasetInfo()

    resolve_dataset_revision.cache_clear()
    monkeypatch.setattr("nano_ir_benchmark.datasets.HfApi", FakeHfApi)

    assert resolve_dataset_revision("owner/dataset", requested_revision="main") == {
        "requested": "main",
        "resolved": "abc123",
        "source": "huggingface_hub",
    }


def test_resolve_dataset_revision_returns_unknown_when_hub_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeHfApi:
        def dataset_info(self, repo_id: str, revision: str | None = None) -> object:
            raise RuntimeError(f"cannot resolve {repo_id}@{revision}")

    resolve_dataset_revision.cache_clear()
    monkeypatch.setattr("nano_ir_benchmark.datasets.HfApi", FakeHfApi)

    revision = resolve_dataset_revision("local/dataset", requested_revision=None)

    assert revision["requested"] is None
    assert revision["resolved"] is None
    assert revision["source"] == "huggingface_hub"
    assert revision["error"].startswith("RuntimeError:")


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
