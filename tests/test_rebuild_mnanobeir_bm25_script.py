from __future__ import annotations

import argparse

from scripts.rebuild_mnanobeir_bm25 import _bm25_config_from_args


def test_rebuild_mnanobeir_bm25_script_defaults_to_auto_tokenizer() -> None:
    config = _bm25_config_from_args(
        argparse.Namespace(
            tokenizer="auto",
            tokenizer_name=None,
            stemmer_algorithm="english",
            top_k=100,
        )
    )

    assert config.tokenizer is None
    assert config.top_k == 100


def test_rebuild_mnanobeir_bm25_script_keeps_explicit_tokenizer() -> None:
    config = _bm25_config_from_args(
        argparse.Namespace(
            tokenizer="regex",
            tokenizer_name=None,
            stemmer_algorithm="english",
            top_k=100,
        )
    )

    assert config.tokenizer == "regex"
