from __future__ import annotations

from pathlib import Path

import yaml

from hakari_bench.metadata import export_bibtex, export_citation_catalog, export_latex_citations, text_stats
from scripts.update_dataset_language_detection import (
    _task_name_for_split,
    build_language_detection_metadata,
    detect_language_distribution,
    select_main_languages,
    update_languages_in_file,
)
from scripts.update_dataset_metadata_stats import update_stats_in_file


def test_text_stats_calculates_character_distribution() -> None:
    assert text_stats(["abc", "abcde", "abcdefg"]) == {
        "count": 3,
        "min_chars": 3,
        "max_chars": 7,
        "mean_chars": 5.0,
        "median_chars": 5.0,
    }


def test_export_citations_from_registry_metadata(tmp_path: Path) -> None:
    (tmp_path / "datasets").mkdir()
    (tmp_path / "datasets" / "toy.yaml").write_text(
        """
name: Toy
dataset_id: local/toy
metadata:
  language: en
  category: natural_language
  short_description: Toy dataset.
  description: Toy dataset metadata.
  citation_keys: [toy2024]
  bibtex: |
    @misc{toy2024,
      title = {Toy Paper},
      year = {2024}
    }
splits: [test]
task_metadata:
  test:
    language: en
    category: natural_language
    short_description: Toy task.
    description: Toy task metadata.
    citation_keys: [toy2024]
""".strip(),
        encoding="utf-8",
    )

    catalog = export_citation_catalog(config_root=tmp_path)

    assert catalog["datasets"][0]["name"] == "Toy"
    assert catalog["datasets"][0]["tasks"][0]["citations_latex"] == ["\\cite{toy2024}"]
    assert "@misc{toy2024" in export_bibtex(config_root=tmp_path)
    assert "Toy/test: \\cite{toy2024}" in export_latex_citations(config_root=tmp_path)


def test_update_stats_in_file_writes_query_and_document_stats(tmp_path: Path) -> None:
    path = tmp_path / "toy.yaml"
    path.write_text(
        """
name: Toy
dataset_id: local/toy
splits: [test]
task_metadata:
  test:
    language: en
    category: natural_language
    short_description: Toy task.
    description: Toy task metadata.
""".strip(),
        encoding="utf-8",
    )

    update_stats_in_file(
        path,
        {
            ("local/toy", "test"): {
                "query_text_stats": text_stats(["q1", "query two"]),
                "document_text_stats": text_stats(["doc one", "doc two two"]),
            }
        },
    )

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["task_metadata"]["test"]["query_text_stats"]["median_chars"] == 5.5
    assert data["task_metadata"]["test"]["document_text_stats"]["max_chars"] == 11


def test_detect_language_distribution_keeps_languages_above_half_percent() -> None:
    texts = ["en"] * 198 + ["ja"] + ["fr"]

    result = detect_language_distribution(texts, detector=lambda text: text)

    assert result["sample_count"] == 200
    assert result["ratios"] == {"en": 0.99, "fr": 0.005, "ja": 0.005}


def test_select_main_languages_uses_query_or_document_threshold_and_orders_by_usage() -> None:
    languages = select_main_languages(
        {"ja": 0.80, "en": 0.20},
        {"en": 0.81, "ja": 0.19},
    )

    assert languages == ["en", "ja"]


def test_build_language_detection_metadata_records_query_and_document_percentages() -> None:
    result = build_language_detection_metadata(
        query_texts=["ja"] * 8 + ["en"] * 2,
        document_texts=["en"] * 81 + ["ja"] * 19,
        detector=lambda text: text,
    )

    assert result["languages"] == ["en", "ja"]
    assert result["language_detection"]["detector"] == "fast-langdetect"
    assert result["language_detection"]["query"]["languages"] == {"ja": 80.0, "en": 20.0}
    assert result["language_detection"]["document"]["languages"] == {"en": 81.0, "ja": 19.0}


def test_update_languages_in_file_writes_task_language_detection(tmp_path: Path) -> None:
    path = tmp_path / "toy.yaml"
    path.write_text(
        """
name: Toy
dataset_id: local/toy
splits: [test]
task_metadata:
  test:
    language: en
    category: natural_language
    short_description: Toy task.
    description: Toy task metadata.
""".strip(),
        encoding="utf-8",
    )

    update_languages_in_file(
        path,
        {
            ("local/toy", "test"): {
                "languages": ["en"],
                "language_detection": {
                    "detector": "fast-langdetect",
                    "min_language_percent": 0.5,
                    "main_language_percent": 10.0,
                    "query": {"sample_count": 2, "languages": {"en": 100.0}},
                    "document": {"sample_count": 3, "languages": {"en": 100.0}},
                },
            }
        },
    )

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    metadata = data["task_metadata"]["test"]
    assert metadata["languages"] == ["en"]
    assert metadata["language_detection"]["query"]["languages"] == {"en": 100.0}


def test_update_languages_in_file_keeps_english_as_main_language_for_code_tasks(tmp_path: Path) -> None:
    path = tmp_path / "toy.yaml"
    path.write_text(
        """
name: Toy
dataset_id: local/toy
splits: [test]
task_metadata:
  test:
    language: en
    category: code
    short_description: Toy task.
    description: Toy code task metadata.
""".strip(),
        encoding="utf-8",
    )

    update_languages_in_file(
        path,
        {
            ("local/toy", "test"): {
                "languages": ["de", "es", "en"],
                "language_detection": {
                    "detector": "fast-langdetect",
                    "min_language_percent": 0.5,
                    "main_language_percent": 10.0,
                    "query": {"sample_count": 2, "languages": {"en": 100.0}},
                    "document": {"sample_count": 3, "languages": {"de": 84.0, "es": 16.0}},
                },
            }
        },
    )

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    metadata = data["task_metadata"]["test"]
    assert metadata["languages"] == ["en"]
    assert metadata["language_detection"]["document"]["languages"] == {"de": 84.0, "es": 16.0}


def test_task_name_for_split_uses_metadata_key_from_split_mapping() -> None:
    class Dataset:
        effective_split_mapping = {"climatefever": "NanoClimateFEVER"}

    assert _task_name_for_split(Dataset(), "NanoClimateFEVER") == "NanoClimateFEVER"
    assert _task_name_for_split(Dataset(), "climatefever") == "NanoClimateFEVER"
