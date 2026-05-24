from __future__ import annotations

import sys
import types
from collections.abc import Iterable

import pytest

from hakari_bench.bm25 import (
    BM25Config,
    _build_wordseg_splitter,
    evaluate_bm25_task,
    rank_bm25_candidates,
    rankings_to_candidate_rows,
    resolve_bm25_config_for_queries,
    tokenize_texts,
)
from hakari_bench.evaluation import LoadedIrDataset


def test_rank_bm25_candidates_uses_bm25s_okapi() -> None:
    corpus = {
        "d1": "red orchard fruit",
        "d2": "blue car engine",
        "d3": "apple pie recipe",
    }
    queries = {"q1": "orchard"}

    rankings = rank_bm25_candidates(
        corpus=corpus,
        queries=queries,
        config=BM25Config(
            tokenizer="regex",
            top_k=1,
            show_progress=False,
        ),
    )

    assert rankings["q1"] == ["d1"]


def test_rank_bm25_candidates_uses_bm25s_robertson_for_okapi(monkeypatch: pytest.MonkeyPatch) -> None:
    methods: list[str | None] = []

    class _FakeBM25:
        def __init__(self, *, k1: float, b: float, method: str) -> None:
            _ = (k1, b)
            methods.append(method)

        def index(self, corpus_tokens: list[list[str]], **kwargs: object) -> None:
            _ = (corpus_tokens, kwargs)

        def retrieve(self, query_tokens: list[list[str]], **kwargs: object) -> tuple[list[list[int]], None]:
            _ = (query_tokens, kwargs)
            return [[0]], None

    monkeypatch.setitem(sys.modules, "bm25s", types.SimpleNamespace(BM25=_FakeBM25))

    rankings = rank_bm25_candidates(
        corpus={"d1": "red apple"},
        queries={"q1": "apple"},
        config=BM25Config(tokenizer="regex", top_k=1),
    )

    assert rankings == {"q1": ["d1"]}
    assert methods == ["robertson"]


def test_resolve_bm25_config_auto_selects_wordseg_for_supported_language() -> None:
    calls: list[str] = []

    def detector(text: str) -> dict[str, object]:
        calls.append(text)
        return {"lang": "ja", "score": 0.99}

    config = resolve_bm25_config_for_queries(
        BM25Config(tokenizer=None),
        {f"q{i}": f"query {i}" for i in range(20)},
        detector=detector,
    )

    assert len(calls) == 10
    assert config.tokenizer == "wordseg"
    assert config.tokenizer_name == "ja"
    assert config.auto_selected is True
    assert config.auto_detected_language == "ja"
    assert config.auto_detection_sample_size == 10
    assert config.auto_detection_language_counts == {"ja": 10}


def test_resolve_bm25_config_auto_selects_wordseg_for_vietnamese() -> None:
    config = resolve_bm25_config_for_queries(
        BM25Config(tokenizer=None),
        {"q1": "thành phố hồ chí minh", "q2": "truy xuất thông tin"},
        detector=lambda _: {"lang": "vi", "score": 0.99},
    )

    assert config.tokenizer == "wordseg"
    assert config.tokenizer_name == "vi"
    assert config.auto_detected_language == "vi"


def test_resolve_bm25_config_auto_selects_regex_for_other_languages() -> None:
    config = resolve_bm25_config_for_queries(
        BM25Config(tokenizer=None),
        {"q1": "what is bm25", "q2": "retrieval benchmark"},
        detector=lambda _: {"lang": "en", "score": 0.98},
    )

    assert config.tokenizer == "regex"
    assert config.tokenizer_name is None
    assert config.auto_selected is True
    assert config.auto_detected_language == "en"


def test_resolve_bm25_config_keeps_explicit_tokenizer() -> None:
    config = resolve_bm25_config_for_queries(
        BM25Config(tokenizer="english_porter_stop"),
        {"q1": "what is bm25"},
        detector=lambda _: {"lang": "ja", "score": 0.99},
    )

    assert config.tokenizer == "english_porter_stop"
    assert config.auto_selected is False
    assert config.auto_detected_language is None


def test_tokenize_texts_supports_basic_tokenizers() -> None:
    assert tokenize_texts(["BM25-based retrieval works."], tokenizer="regex") == [
        ["bm25", "based", "retrieval", "works"]
    ]
    assert tokenize_texts(["BM25-based retrieval works."], tokenizer="whitespace") == [
        ["bm25-based", "retrieval", "works."]
    ]
    assert tokenize_texts(["BM25-based retrieval works."], tokenizer="english_regex") == [
        ["bm25", "based", "retrieval", "works"]
    ]


def test_tokenize_texts_supports_english_porter_stop() -> None:
    assert tokenize_texts(["The running runners run in the park."], tokenizer="english_porter_stop") == [
        ["run", "runner", "run", "park"]
    ]


def test_tokenize_texts_supports_pystemmer() -> None:
    assert tokenize_texts(["running runners"], tokenizer="stemmer", stemmer_algorithm="english") == [
        ["run", "runner"]
    ]


def test_tokenize_texts_supports_wordseg_japanese_with_lazy_loader() -> None:
    class _Word:
        def __init__(self, surface: str) -> None:
            self.surface = surface

    class _FugashiModule:
        class Tagger:
            def __call__(self, text: str) -> list[_Word]:
                _ = text
                return [_Word("東京"), _Word("タワー")]

    def module_loader(module_name: str) -> object:
        if module_name == "fugashi":
            return _FugashiModule()
        if module_name == "unidic_lite":
            return types.SimpleNamespace()
        raise AssertionError(module_name)

    splitter = _build_wordseg_splitter("ja", module_loader=module_loader)

    assert splitter("東京タワー") == ["東京", "タワー"]


def test_tokenize_texts_supports_wordseg_chinese_with_lazy_loader() -> None:
    def module_loader(module_name: str) -> object:
        if module_name == "jieba":
            return types.SimpleNamespace(cut=lambda text: ["北京", "大学"])
        raise AssertionError(module_name)

    splitter = _build_wordseg_splitter("zh", module_loader=module_loader)

    assert splitter("北京大学") == ["北京", "大学"]


def test_tokenize_texts_supports_wordseg_thai_with_lazy_loader() -> None:
    engines: list[str] = []

    def word_tokenize(text: str, *, engine: str) -> list[str]:
        _ = text
        engines.append(engine)
        return ["ภาษา", "ไทย"]

    def module_loader(module_name: str) -> object:
        if module_name == "pythainlp.tokenize":
            return types.SimpleNamespace(word_tokenize=word_tokenize)
        raise AssertionError(module_name)

    splitter = _build_wordseg_splitter("th", module_loader=module_loader)

    assert splitter("ภาษาไทย") == ["ภาษา", "ไทย"]
    assert engines == ["newmm"]


def test_tokenize_texts_supports_wordseg_korean_with_lazy_loader() -> None:
    class _Token:
        def __init__(self, form: str) -> None:
            self.form = form

    class _Kiwi:
        def tokenize(self, text: str) -> Iterable[_Token]:
            _ = text
            return [_Token("한국"), _Token("어")]

    def module_loader(module_name: str) -> object:
        if module_name == "kiwipiepy":
            return types.SimpleNamespace(Kiwi=lambda: _Kiwi())
        raise AssertionError(module_name)

    splitter = _build_wordseg_splitter("ko", module_loader=module_loader)

    assert splitter("한국어") == ["한국", "어"]


def test_tokenize_texts_supports_wordseg_vietnamese_with_lazy_loader() -> None:
    class _PyviTokenizerModule:
        @staticmethod
        def tokenize(text: str) -> str:
            _ = text
            return "xin_chao THÀNH_PHỐ !"

    def module_loader(module_name: str) -> object:
        if module_name == "pyvi.ViTokenizer":
            return _PyviTokenizerModule()
        raise AssertionError(module_name)

    splitter = _build_wordseg_splitter("vi", module_loader=module_loader)

    assert splitter("xin chao thanh pho") == ["xin_chao", "thành_phố"]


def test_tokenize_texts_requires_wordseg_language() -> None:
    with pytest.raises(ValueError, match="requires --bm25-wordseg-language"):
        tokenize_texts(["東京タワー"], tokenizer="wordseg")


def test_tokenize_texts_reports_missing_wordseg_dependency() -> None:
    def module_loader(module_name: str) -> object:
        raise ImportError(module_name)

    with pytest.raises(RuntimeError, match="Missing dependencies for wordseg language 'ja'"):
        _build_wordseg_splitter("ja", module_loader=module_loader)


def test_rankings_to_candidate_rows_preserves_query_ids() -> None:
    rows = rankings_to_candidate_rows({"q1": ["d2", "d1"]})

    assert rows == [{"query-id": "q1", "corpus-ids": ["d2", "d1"]}]


def test_evaluate_bm25_task_returns_ir_metrics() -> None:
    dataset = LoadedIrDataset(
        queries={"q1": "cat fish", "q2": "dog bone"},
        corpus={"d1": "cat likes fish", "d2": "dog likes bone", "d3": "other"},
        qrels={"q1": {"d1"}, "q2": {"d2"}},
        candidates=None,
        evaluator_name="Toy",
    )

    result = evaluate_bm25_task(
        dataset=dataset,
        config=BM25Config(tokenizer="regex", top_k=3, show_progress=False),
        source="computed_bm25s",
    )

    assert result.metrics["Toy_bm25_bm25s_okapi_ndcg@10"] == pytest.approx(1.0)
    assert result.metrics["Toy_bm25_bm25s_okapi_acc@100"] == pytest.approx(1.0)
    assert set(result.metrics) == {"Toy_bm25_bm25s_okapi_ndcg@10", "Toy_bm25_bm25s_okapi_acc@100"}
    assert result.timing["score_and_topk_seconds"] >= 0.0


def test_evaluate_bm25_task_uses_dataset_candidate_subset_without_bm25s(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FailingBM25:
        def __init__(self, **kwargs: object) -> None:
            _ = kwargs
            raise AssertionError("bm25s should not be used when dataset candidates are available")

    monkeypatch.setitem(sys.modules, "bm25s", types.SimpleNamespace(BM25=_FailingBM25))
    dataset = LoadedIrDataset(
        queries={"q1": "cat fish", "q2": "dog bone"},
        corpus={"d1": "cat likes fish", "d2": "dog likes bone", "d3": "other"},
        qrels={"q1": {"d1"}, "q2": {"d2"}},
        candidates={"q1": ["d1", "d3"], "q2": ["d2", "d1"]},
        evaluator_name="Toy",
    )

    result = evaluate_bm25_task(
        dataset=dataset,
        config=BM25Config(tokenizer=None, top_k=1, show_progress=False),
    )

    assert result.metrics["Toy_bm25_dataset_subset_ndcg@10"] == pytest.approx(1.0)
    assert result.metrics["Toy_bm25_dataset_subset_acc@100"] == pytest.approx(1.0)
    assert result.timing["score_and_topk_seconds"] >= 0.0


def test_evaluate_bm25_task_requires_dataset_candidates_by_default() -> None:
    dataset = LoadedIrDataset(
        queries={"q1": "cat fish"},
        corpus={"d1": "cat likes fish"},
        qrels={"q1": {"d1"}},
        candidates=None,
        evaluator_name="Toy",
    )

    with pytest.raises(ValueError, match="--bm25-source computed"):
        evaluate_bm25_task(
            dataset=dataset,
            config=BM25Config(tokenizer="regex", top_k=1, show_progress=False),
        )
