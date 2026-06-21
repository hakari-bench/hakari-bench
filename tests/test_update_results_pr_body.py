from __future__ import annotations

from pathlib import Path

from scripts import update_results_pr_body as script


def test_update_results_pr_body_writes_generated_output(tmp_path: Path, monkeypatch) -> None:
    result_dir = tmp_path / "results"
    output_path = tmp_path / "body.md"
    calls = {}

    def fake_generate_pr_template(**kwargs):
        calls.update(kwargs)
        return "generated body"

    monkeypatch.setattr(script, "generate_pr_template", fake_generate_pr_template)

    exit_code = script.main(
        [
            str(result_dir),
            "--repo-path",
            "hakari-results/model",
            "--comparison-duckdb-path",
            str(tmp_path / "results.duckdb"),
            "--comparison-model",
            "model/a",
            "--comparison-model",
            "model/b",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8") == "generated body"
    assert calls["result_dir"] == result_dir
    assert calls["repo_path"] == "hakari-results/model"
    assert calls["comparison_duckdb_path"] == tmp_path / "results.duckdb"
    assert calls["comparison_models"] == ["model/a", "model/b"]


def test_update_results_pr_body_edits_first_discussion_comment(tmp_path: Path, monkeypatch) -> None:
    result_dir = tmp_path / "results"
    edits = {}

    def fake_generate_pr_template(**kwargs):
        return "generated body"

    class FakeEvent:
        type = "comment"
        id = "comment-1"

    class FakeDiscussion:
        events = [FakeEvent()]

    class FakeHfApi:
        def get_discussion_details(self, **kwargs):
            edits["details_kwargs"] = kwargs
            return FakeDiscussion()

        def edit_discussion_comment(self, **kwargs):
            edits["edit_kwargs"] = kwargs
            return object()

    monkeypatch.setattr(script, "generate_pr_template", fake_generate_pr_template)
    monkeypatch.setattr(script, "HfApi", FakeHfApi)

    exit_code = script.main(
        [
            str(result_dir),
            "--discussion-num",
            "10",
            "--repo-id",
            "hakari-bench/results",
        ]
    )

    assert exit_code == 0
    assert edits["details_kwargs"] == {
        "repo_id": "hakari-bench/results",
        "repo_type": "dataset",
        "discussion_num": 10,
    }
    assert edits["edit_kwargs"]["comment_id"] == "comment-1"
    assert edits["edit_kwargs"]["new_content"] == "generated body"


def test_update_results_pr_body_defaults_to_remote_latest_cache_path(tmp_path: Path, monkeypatch) -> None:
    result_dir = tmp_path / "results"
    duckdb_path = tmp_path / "remote_latest.duckdb"
    calls = {}

    def fake_generate_pr_template(**kwargs):
        calls.update(kwargs)
        return "generated body"

    monkeypatch.setenv(script.REMOTE_LATEST_DUCKDB_PATH_ENV, str(duckdb_path))
    monkeypatch.setattr(script, "generate_pr_template", fake_generate_pr_template)

    exit_code = script.main([str(result_dir), "--output", str(tmp_path / "body.md")])

    assert exit_code == 0
    assert calls["comparison_duckdb_path"] == duckdb_path
