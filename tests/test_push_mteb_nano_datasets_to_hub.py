from __future__ import annotations

from scripts import push_mteb_nano_datasets_to_hub as script


def test_confirm_deletion_returns_true_for_empty_list() -> None:
    assert script._confirm_deletion([], assume_yes=False, input_func=_unexpected_input) is True


def test_confirm_deletion_skips_prompt_when_assume_yes() -> None:
    assert (
        script._confirm_deletion(
            ["hakari-bench/NanoFoo"], assume_yes=True, input_func=_unexpected_input
        )
        is True
    )


def test_confirm_deletion_accepts_explicit_yes() -> None:
    assert (
        script._confirm_deletion(
            ["hakari-bench/NanoFoo"], assume_yes=False, input_func=lambda _prompt: "yes"
        )
        is True
    )


def test_confirm_deletion_rejects_other_input() -> None:
    assert (
        script._confirm_deletion(
            ["hakari-bench/NanoFoo"], assume_yes=False, input_func=lambda _prompt: "y"
        )
        is False
    )
    assert (
        script._confirm_deletion(
            ["hakari-bench/NanoFoo"], assume_yes=False, input_func=lambda _prompt: ""
        )
        is False
    )


def _unexpected_input(_prompt: str) -> str:
    raise AssertionError("input should not be called")
