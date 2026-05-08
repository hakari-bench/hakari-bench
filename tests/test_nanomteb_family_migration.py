from __future__ import annotations

import json
from pathlib import Path

from scripts.migrate_nanomteb_family_results import canonical_target_for, migrate_results


def test_canonical_target_renames_named_mteb_family_dataset() -> None:
    target = canonical_target_for(
        dataset_name="NanoMTEB-Persian",
        dataset_id="hakari-bench/NanoMTEB-Persian",
        split_name="NanoSynPerQA",
    )

    assert target.name == "NanoFaMTEB"
    assert target.dataset_id == "hakari-bench/NanoFaMTEB"


def test_canonical_target_moves_non_family_split_to_misc() -> None:
    target = canonical_target_for(
        dataset_name="NanoMTEB-Persian",
        dataset_id="hakari-bench/NanoMTEB-Persian",
        split_name="NanoNeuCLIR2023",
    )

    assert target.name == "NanoMTEB-Misc"
    assert target.dataset_id == "hakari-bench/NanoMTEB-Misc"


def test_migrate_results_rewrites_target_and_moves_file(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoMTEB-Xlingual" / "NanoWMT19DeFr.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text(
        json.dumps(
            {
                "target": {
                    "dataset_name": "NanoMTEB-Xlingual",
                    "dataset_id": "hakari-bench/NanoMTEB-Xlingual",
                    "split_name": "NanoWMT19DeFr",
                    "task_name": "NanoWMT19DeFr",
                    "metadata": {"description": "included in NanoMTEB-Xlingual"},
                },
                "evaluation": {"aggregate_metric_value": 0.1},
            }
        ),
        encoding="utf-8",
    )

    actions = migrate_results(results_dir=tmp_path)

    migrated_path = tmp_path / "model" / "hakari-bench__NanoMTEB-Misc" / "NanoWMT19DeFr.json"
    payload = json.loads(migrated_path.read_text(encoding="utf-8"))
    assert not result_path.exists()
    assert payload["target"]["dataset_name"] == "NanoMTEB-Misc"
    assert payload["target"]["dataset_id"] == "hakari-bench/NanoMTEB-Misc"
    assert payload["target"]["metadata"]["description"] == "included in NanoMTEB-Misc"
    assert any("move" in action for action in actions)
