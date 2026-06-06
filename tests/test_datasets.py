from __future__ import annotations

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
    assert registry.get_dataset("NanoJMTEB-v2").dataset_id == "hakari-bench/NanoJMTEB-v2"
    assert registry.get_dataset("NanoRTEB").dataset_id == "hakari-bench/NanoRTEB"
    assert registry.get_dataset("NanoMTEB-v2").dataset_id == "hakari-bench/NanoMTEB-v2"
    assert registry.get_dataset("NanoMMTEB-v2").dataset_id == "hakari-bench/NanoMMTEB-v2"
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
    assert registry.get_dataset("NanoFaMTEB-v2").dataset_id == "hakari-bench/NanoFaMTEB-v2"
    assert registry.get_dataset("NanoIndicQA").dataset_id == "hakari-bench/NanoIndicQA"
    assert registry.get_dataset("NanoMuPLeR").dataset_id == "hakari-bench/NanoMuPLeR"
    assert registry.get_dataset("NanoMTEB-Dutch").dataset_id == "hakari-bench/NanoMTEB-Dutch"
    assert registry.get_dataset("NanoMTEB-Misc").dataset_id == "hakari-bench/NanoMTEB-Misc"
    assert registry.get_dataset("NanoMTEB-Polish").dataset_id == "hakari-bench/NanoMTEB-Polish"
    assert len(registry.get_collection("MNanoBEIR").datasets) == 14
    with pytest.raises(KeyError):
        registry.get_collection("NanoMTEB_Family")


def test_builtin_config_lives_in_repo_config() -> None:
    config_root = Path("config")

    assert config_root.joinpath("datasets", "nanobeir_en.yaml").is_file()
    assert config_root.joinpath("dataset_collections", "mnanobeir.yaml").is_file()
    assert not config_root.joinpath("dataset_collections", "nanomteb_family.yaml").exists()
    assert config_root.joinpath("viewer", "benchmarks.yaml").is_file()


def test_builtin_registry_is_cached() -> None:
    assert DatasetRegistry.load_builtin() is DatasetRegistry.load_builtin()


def test_resolve_eval_tasks_for_builtin_nanomteb_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoMTEB-v2"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoMTEB-v2", "argu_ana"),
        ("NanoMTEB-v2", "climate_fever"),
        ("NanoMTEB-v2", "cqadupstack_gaming"),
        ("NanoMTEB-v2", "cqadupstack_unix"),
        ("NanoMTEB-v2", "fever"),
        ("NanoMTEB-v2", "fi_qa2018"),
        ("NanoMTEB-v2", "hotpot_qa"),
        ("NanoMTEB-v2", "scidocs"),
        ("NanoMTEB-v2", "touche2020_v3"),
        ("NanoMTEB-v2", "treccovid"),
    ]


def test_resolve_eval_tasks_for_builtin_nanommteb_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoMMTEB-v2"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoMMTEB-v2", "ailastatutes"),
        ("NanoMMTEB-v2", "argu_ana"),
        ("NanoMMTEB-v2", "belebele"),
        ("NanoMMTEB-v2", "covid"),
        ("NanoMMTEB-v2", "hagrid"),
        ("NanoMMTEB-v2", "legal_bench_corporate_lobbying"),
        ("NanoMMTEB-v2", "lembpasskey"),
        ("NanoMMTEB-v2", "miracl"),
        ("NanoMMTEB-v2", "mlqa"),
        ("NanoMMTEB-v2", "scidocs"),
        ("NanoMMTEB-v2", "spart_qa"),
        ("NanoMMTEB-v2", "stack_overflow_qa"),
        ("NanoMMTEB-v2", "statcan_dialogue_dataset"),
        ("NanoMMTEB-v2", "temp_reason_l1"),
        ("NanoMMTEB-v2", "treccovid"),
        ("NanoMMTEB-v2", "twitter_hjerne"),
        ("NanoMMTEB-v2", "wikipedia_multilingual"),
        ("NanoMMTEB-v2", "wino_grande"),
    ]


def test_resolve_eval_tasks_for_builtin_nanomteb_chinese_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoCMTEB"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoCMTEB", "cmedqa"),
        ("NanoCMTEB", "covid"),
        ("NanoCMTEB", "du"),
        ("NanoCMTEB", "ecom"),
        ("NanoCMTEB", "medical"),
        ("NanoCMTEB", "mmarco"),
        ("NanoCMTEB", "t2"),
        ("NanoCMTEB", "video"),
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


def test_resolve_eval_tasks_for_builtin_nanomteb_japanese_uses_declared_splits() -> None:
    registry = DatasetRegistry.load_builtin()

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoJMTEB-v2"], collection_values=[], split_values=[])

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoJMTEB-v2", "ja_cwir"),
        ("NanoJMTEB-v2", "ja_gov_faqs"),
        ("NanoJMTEB-v2", "jaqket"),
        ("NanoJMTEB-v2", "mintaka_ja"),
        ("NanoJMTEB-v2", "miracl_ja"),
        ("NanoJMTEB-v2", "mr_tidy_japanese"),
        ("NanoJMTEB-v2", "multi_long_doc_ja"),
        ("NanoJMTEB-v2", "nlpjournal_abs_article"),
        ("NanoJMTEB-v2", "nlpjournal_abs_intro"),
        ("NanoJMTEB-v2", "nlpjournal_title_abs"),
        ("NanoJMTEB-v2", "nlpjournal_title_intro"),
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


def test_resolve_eval_tasks_for_builtin_nanodapfam_excludes_fulltext_by_default() -> None:
    registry = DatasetRegistry.load_builtin()

    standard_tasks = resolve_eval_tasks(registry=registry, dataset_values=["NanoDAPFAM"], collection_values=[], split_values=[])
    all_tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=["NanoDAPFAM"],
        collection_values=[],
        split_values=[],
        evaluation_scope="all",
    )

    assert len(standard_tasks) == 12
    assert len(all_tasks) == 18
    assert all("ToFullText" not in task.split_name for task in standard_tasks)
    fulltext_tasks = [task for task in all_tasks if task.split_name.endswith("ToFullText")]
    assert len(fulltext_tasks) == 6
    assert all(not task.evaluation_scope.include_by_default for task in fulltext_tasks)


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
            "NanoGerDaLIRSmall",
            "NanoLeCaRDv2",
            "NanoLegalBenchConsumerContractsQA",
            "NanoLegalBenchCorporateLobbying",
            "NanoLegalQuAD",
            "NanoLegalSummarization",
        ],
        "NanoMedical": [
            "NanoCMedQAv2reranking",
            "NanoCUREv1",
            "NanoCmedqa",
            "NanoMedicalQA",
            "NanoNFCorpus",
            "NanoPublicHealthQA",
            "NanoSciFact",
            "NanoSciFactPL",
            "NanoTRECCOVID",
            "NanoTRECCOVIDPL",
        ],
        "NanoRARb": [
            "NanoARCChallenge",
            "NanoAlphaNLI",
            "NanoHellaSwag",
            "NanoPIQA",
            "NanoQuail",
            "NanoRARbCode",
            "NanoRARbMath",
            "NanoSIQA",
            "NanoSpartQA",
            "NanoTempReasonL1",
            "NanoTempReasonL2Context",
            "NanoTempReasonL2Fact",
            "NanoTempReasonL2Pure",
            "NanoTempReasonL3Context",
            "NanoTempReasonL3Fact",
            "NanoTempReasonL3Pure",
            "NanoWinoGrande",
        ],
        "NanoBRIGHT": [
            "NanoBrightAops",
            "NanoBrightBiology",
            "NanoBrightBiologyLong",
            "NanoBrightEarthScience",
            "NanoBrightEarthScienceLong",
            "NanoBrightEconomics",
            "NanoBrightEconomicsLong",
            "NanoBrightLeetcode",
            "NanoBrightPony",
            "NanoBrightPonyLong",
            "NanoBrightPsychology",
            "NanoBrightPsychologyLong",
            "NanoBrightRobotics",
            "NanoBrightRoboticsLong",
            "NanoBrightStackoverflow",
            "NanoBrightStackoverflowLong",
            "NanoBrightSustainableLiving",
            "NanoBrightSustainableLivingLong",
            "NanoBrightTheoremQAQuestions",
            "NanoBrightTheoremQATheorems",
        ],
        "NanoCodeRAG": [
            "NanoCodeRAGLibraryDocumentationSolutions",
            "NanoCodeRAGOnlineTutorials",
            "NanoCodeRAGProgrammingSolutions",
            "NanoCodeRAGStackoverflowPosts",
        ],
        "NanoChemTEB": ["NanoChemHotpotQA", "NanoChemNQ", "NanoChemRxiv"],
        "NanoR2MED": [
            "NanoR2MEDBioinformatics",
            "NanoR2MEDBiology",
            "NanoR2MEDIIYiClinical",
            "NanoR2MEDMedQADiag",
            "NanoR2MEDMedXpertQAExam",
            "NanoR2MEDMedicalSciences",
            "NanoR2MEDPMCClinical",
            "NanoR2MEDPMCTreatment",
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
        dataset_values=["example/NanoToy"],
        collection_values=[],
        split_values=[],
    )

    assert [(task.dataset_name, task.split_name) for task in tasks] == [
        ("NanoToy", "ja"),
        ("NanoToy", "en"),
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


def test_resolve_eval_tasks_excludes_non_default_tasks_from_standard_scope(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
splits: [short, long]
task_evaluation_scope:
  long:
    include_by_default: false
    tags: [long_context, expensive]
    reason: Long-context task is evaluated only when explicitly requested.
""".strip(),
        encoding="utf-8",
    )
    registry = DatasetRegistry.load_from_root(tmp_path)

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["Toy"], collection_values=[], split_values=[])

    assert [(task.split_name, task.evaluation_scope.include_by_default) for task in tasks] == [("short", True)]


def test_resolve_eval_tasks_all_scope_includes_non_default_tasks(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
splits: [short, long]
task_evaluation_scope:
  long:
    include_by_default: false
    tags: [long_context, expensive]
    reason: Long-context task is evaluated only when explicitly requested.
""".strip(),
        encoding="utf-8",
    )
    registry = DatasetRegistry.load_from_root(tmp_path)

    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=["Toy"],
        collection_values=[],
        split_values=[],
        evaluation_scope="all",
    )

    assert [(task.split_name, task.evaluation_scope.include_by_default) for task in tasks] == [
        ("short", True),
        ("long", False),
    ]
    assert tasks[1].evaluation_scope.tags == ["long_context", "expensive"]


def test_resolve_eval_tasks_explicit_split_bypasses_standard_scope_filter(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
splits: [short, long]
task_evaluation_scope:
  long:
    include_by_default: false
    tags: [long_context]
""".strip(),
        encoding="utf-8",
    )
    registry = DatasetRegistry.load_from_root(tmp_path)

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["Toy"], collection_values=[], split_values=["long"])

    assert [(task.split_name, task.evaluation_scope.include_by_default) for task in tasks] == [("long", False)]


def test_resolve_eval_tasks_dataset_scope_is_inherited_by_tasks(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
splits: [heldout, standard]
evaluation_scope:
  include_by_default: false
  tags: [heldout]
task_evaluation_scope:
  standard:
    include_by_default: true
""".strip(),
        encoding="utf-8",
    )
    registry = DatasetRegistry.load_from_root(tmp_path)

    tasks = resolve_eval_tasks(registry=registry, dataset_values=["Toy"], collection_values=[], split_values=[])

    assert [(task.split_name, task.evaluation_scope.include_by_default) for task in tasks] == [("standard", True)]


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


def test_metadata_validation_accepts_language_detection_fields() -> None:
    spec = NanoDatasetSpec(
        name="Toy",
        dataset_id="local/toy",
        metadata={
            "language": "unknown",
            "languages": ["en", "ja"],
            "category": "natural_language",
            "short_description": "Toy metadata.",
            "description": "Toy metadata with detected language distributions.",
            "language_detection": {
                "detector": "fast-langdetect",
                "min_language_percent": 0.5,
                "main_language_percent": 10.0,
                "query": {"sample_count": 10, "languages": {"ja": 80.0, "en": 20.0}},
                "document": {"sample_count": 100, "languages": {"en": 81.0, "ja": 19.0}},
            },
        },
    )

    assert spec.validate_metadata() == []


def test_metadata_validation_rejects_invalid_language_detection_fields() -> None:
    spec = NanoDatasetSpec(
        name="Toy",
        dataset_id="local/toy",
        metadata={
            "language": "en",
            "languages": ["english"],
            "category": "natural_language",
            "short_description": "Toy metadata.",
            "description": "Toy metadata with invalid language detection.",
            "language_detection": {
                "detector": 1,
                "min_language_percent": "0.5",
                "main_language_percent": 10.0,
                "query": {"sample_count": 10, "languages": {"engl": 100.0}},
                "document": {"sample_count": "100", "languages": {"en": "100"}},
            },
        },
    )

    assert spec.validate_metadata() == [
        "Toy metadata has invalid languages[0] 'english'.",
        "Toy metadata language_detection.detector must be string.",
        "Toy metadata language_detection.min_language_percent must be numeric.",
        "Toy metadata has invalid language_detection.query.languages key 'engl'.",
        "Toy metadata language_detection.document.sample_count must be integer.",
        "Toy metadata language_detection.document.languages['en'] must be numeric.",
    ]


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
