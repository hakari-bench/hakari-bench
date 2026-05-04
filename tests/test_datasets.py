from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import pytest

from hakari_bench.datasets import (
    DatasetRegistry,
    NanoDatasetSpec,
    REFERENCE_SOURCE_CONFIDENCE_LABELS,
    validate_builtin_metadata,
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
    assert registry.get_dataset("NanoBIRCO").dataset_id == "hakari-bench/NanoBIRCO"
    assert registry.get_dataset("NanoDAPFAM").dataset_id == "hakari-bench/NanoDAPFAM"
    assert registry.get_dataset("NanoMTEB-Dutch").dataset_id == "hakari-bench/NanoMTEB-Dutch"
    assert registry.get_dataset("NanoMTEB-Xlingual").dataset_id == "hakari-bench/NanoMTEB-Xlingual"
    assert len(registry.get_collection("MNanoBEIR").datasets) == 14


def test_builtin_config_is_packaged_with_library() -> None:
    config_root = files("hakari_bench").joinpath("config")

    assert config_root.joinpath("datasets", "nanobeir_en.yaml").is_file()
    assert config_root.joinpath("dataset_collections", "mnanobeir.yaml").is_file()
    assert config_root.joinpath("viewer", "benchmarks.yaml").is_file()


def test_packaged_builtin_config_matches_repo_config() -> None:
    repo_config = Path("config")
    packaged_config = Path("hakari_bench/config")

    assert sorted(path.relative_to(repo_config) for path in repo_config.rglob("*.yaml")) == sorted(
        path.relative_to(packaged_config) for path in packaged_config.rglob("*.yaml")
    )
    for repo_path in repo_config.rglob("*.yaml"):
        packaged_path = packaged_config / repo_path.relative_to(repo_config)
        assert packaged_path.read_text(encoding="utf-8") == repo_path.read_text(encoding="utf-8")


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
        ("NanoJMTEB", "NanoMIRACL"),
        ("NanoJMTEB", "NanoMintaka"),
        ("NanoJMTEB", "NanoMrTidy"),
        ("NanoJMTEB", "NanoMultiLongDoc"),
        ("NanoJMTEB", "NanoNLPJournalAbsArticle"),
        ("NanoJMTEB", "NanoNLPJournalAbsIntro"),
        ("NanoJMTEB", "NanoNLPJournalTitleAbs"),
        ("NanoJMTEB", "NanoNLPJournalTitleIntro"),
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
        "hakari_bench.datasets.get_dataset_split_names",
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
    monkeypatch.setattr("hakari_bench.datasets.HfApi", FakeHfApi)

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
    monkeypatch.setattr("hakari_bench.datasets.HfApi", FakeHfApi)

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


def test_registry_rejects_unknown_dataset_config_keys(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
unknown_key: value
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unknown_key"):
        DatasetRegistry.load_from_root(tmp_path)


def test_registry_preserves_dataset_and_task_metadata(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "dataset_collections").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
metadata:
  language: en
  category: natural_language
  short_description: Toy retrieval group.
  description: Toy dataset used to verify metadata loading.
  references:
    - title: Toy Paper
      authors: [Ada Example]
      year: 2024
      url: https://example.com/toy
  citation_keys: [toy2024]
  bibtex: |
    @misc{toy2024,
      title = {Toy Paper},
      year = {2024}
    }
splits: [a]
task_metadata:
  a:
    language: en
    category: natural_language
    short_description: Toy split.
    description: Toy split metadata survives loading and task resolution.
    query_text_stats:
      count: 2
      min_chars: 3
      max_chars: 5
      mean_chars: 4.0
      median_chars: 4.0
    document_text_stats:
      count: 3
      min_chars: 8
      max_chars: 10
      mean_chars: 9.0
      median_chars: 9.0
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "dataset_collections" / "toy_collection.yaml").write_text(
        """
name: ToyCollection
metadata:
  language: en
  category: natural_language
  short_description: Toy collection.
  description: Toy collection metadata survives loading.
datasets:
  - Toy
  - name: InlineToy
    dataset_id: local/inline-toy
    metadata:
      language: en
      category: natural_language
      short_description: Inline toy.
      description: Inline dataset metadata survives collection loading.
    splits: [inline]
    task_metadata:
      inline:
        language: en
        category: natural_language
        short_description: Inline toy split.
        description: Inline toy task metadata survives loading.
""".strip(),
        encoding="utf-8",
    )

    registry = DatasetRegistry.load_from_root(tmp_path)
    toy = registry.get_dataset("Toy")
    inline = registry.get_dataset("InlineToy")
    collection = registry.get_collection("ToyCollection")
    tasks = resolve_eval_tasks(registry=registry, dataset_values=["Toy"], collection_values=[], split_values=[])

    assert toy.metadata is not None
    assert toy.task_metadata is not None
    assert inline.metadata is not None
    assert collection.metadata is not None
    assert toy.metadata["citation_keys"] == ["toy2024"]
    assert toy.task_metadata["a"]["query_text_stats"]["median_chars"] == 4.0
    assert inline.metadata["short_description"] == "Inline toy."
    assert collection.metadata["short_description"] == "Toy collection."
    assert tasks[0].metadata["short_description"] == "Toy split."


def test_builtin_metadata_is_complete_and_valid() -> None:
    errors = validate_builtin_metadata()

    assert errors == []


def test_metadata_validation_rejects_unknown_category() -> None:
    spec = NanoDatasetSpec(
        name="Toy",
        dataset_id="local/toy",
        metadata={
            "language": "en",
            "category": "other",
            "short_description": "Toy.",
            "description": "Toy metadata with an invalid category.",
        },
    )

    errors = spec.validate_metadata()

    assert errors == ["Toy metadata has invalid category 'other'."]


def test_metadata_validation_requires_reference_is_paper_boolean() -> None:
    spec = NanoDatasetSpec(
        name="Toy",
        dataset_id="local/toy",
        metadata={
            "language": "en",
            "category": "natural_language",
            "short_description": "Toy.",
            "description": "Toy metadata with references.",
            "references": [
                {
                    "title": "Toy Paper",
                    "authors": ["A. Author"],
                    "year": 2024,
                    "url": "https://example.com/paper",
                    "source_confidence": "probably_correct",
                },
                {
                    "title": "Toy Blog",
                    "authors": ["B. Author"],
                    "year": 2024,
                    "url": "https://example.com/blog",
                    "is_paper": "no",
                    "source_confidence": "probably_correct",
                },
            ],
        },
    )

    errors = spec.validate_metadata()

    assert errors == [
        "Toy metadata references[0] is missing is_paper.",
        "Toy metadata references[1].is_paper must be boolean.",
    ]


def test_metadata_validation_requires_reference_source_confidence_label() -> None:
    spec = NanoDatasetSpec(
        name="Toy",
        dataset_id="local/toy",
        metadata={
            "language": "en",
            "category": "natural_language",
            "short_description": "Toy.",
            "description": "Toy metadata with references.",
            "references": [
                {
                    "title": "Toy Paper",
                    "authors": ["A. Author"],
                    "year": 2024,
                    "url": "https://example.com/paper",
                    "is_paper": True,
                },
                {
                    "title": "Toy Blog",
                    "authors": ["B. Author"],
                    "year": 2024,
                    "url": "https://example.com/blog",
                    "is_paper": False,
                    "source_confidence": "unchecked",
                },
            ],
        },
    )

    errors = spec.validate_metadata()

    assert errors == [
        "Toy metadata references[0] is missing source_confidence.",
        "Toy metadata references[1].source_confidence has invalid label 'unchecked'.",
    ]


def test_reference_source_confidence_labels_are_documented() -> None:
    assert set(REFERENCE_SOURCE_CONFIDENCE_LABELS) == {
        "source_uncertain",
        "probably_correct",
        "definitive_paper_link",
        "human_verified",
    }
    assert "AI agents must not assign this label" in REFERENCE_SOURCE_CONFIDENCE_LABELS["human_verified"]
