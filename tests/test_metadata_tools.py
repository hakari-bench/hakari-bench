from __future__ import annotations

from pathlib import Path

import yaml

from hakari_bench.metadata import export_bibtex, export_citation_catalog, export_latex_citations, text_stats
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
