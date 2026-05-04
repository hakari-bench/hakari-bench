from __future__ import annotations

import json
import importlib
import random
import re
import time
from collections.abc import Callable, Iterable
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Sequence, cast

import numpy as np

from hakari_bench.datasets import EvalTask, resolve_dataset_revision
from hakari_bench.metrics import compute_ir_metrics

BM25Tokenizer = Literal[
    "regex",
    "whitespace",
    "transformer",
    "stemmer",
    "english_regex",
    "english_porter",
    "english_porter_stop",
    "wordseg",
]
BM25EvaluationSource = Literal["dataset_candidate_subset", "computed_bm25s"]

_BM25_ALGORITHM_NAME = "okapi"
_BM25S_OKAPI_METHOD = "robertson"
_TOKEN_PATTERN = re.compile(r"\b\w+\b", flags=re.UNICODE)
_ENGLISH_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")
_DEFAULT_TRANSFORMER_TOKENIZER = "Qwen/Qwen3-0.6B"
_MAX_TOKENIZER_CHUNK_CHARS = 4000
WORD_SEGMENTATION_TOKENIZER_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "ja": ("fugashi", "unidic_lite"),
    "zh": ("jieba",),
    "th": ("pythainlp.tokenize",),
    "ko": ("kiwipiepy",),
    "vi": ("pyvi.ViTokenizer",),
}
_ENGLISH_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "being",
        "but",
        "by",
        "for",
        "from",
        "had",
        "has",
        "have",
        "he",
        "her",
        "hers",
        "him",
        "his",
        "i",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "me",
        "my",
        "myself",
        "of",
        "on",
        "or",
        "our",
        "ours",
        "ourselves",
        "she",
        "so",
        "than",
        "that",
        "the",
        "their",
        "theirs",
        "them",
        "themselves",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "to",
        "too",
        "up",
        "very",
        "was",
        "we",
        "were",
        "what",
        "when",
        "where",
        "which",
        "who",
        "whom",
        "why",
        "will",
        "with",
        "you",
        "your",
        "yours",
        "yourself",
        "yourselves",
    }
)


@dataclass(frozen=True)
class BM25Config:
    tokenizer: str | None = None
    tokenizer_name: str | None = None
    stemmer_algorithm: str = "english"
    top_k: int = 100
    k1: float = 1.5
    b: float = 0.75
    show_progress: bool = False
    auto_selected: bool = False
    auto_detected_language: str | None = None
    auto_detection_language_counts: dict[str, int] | None = None
    auto_detection_sample_size: int | None = None


@dataclass(frozen=True)
class BM25BuildResult:
    task: EvalTask
    cache_hit: bool
    output_path: Path
    payload: dict[str, Any]


def bm25_config_from_args(args: Any) -> BM25Config:
    return BM25Config(
        tokenizer=args.bm25_tokenizer,
        tokenizer_name=args.bm25_tokenizer_name,
        stemmer_algorithm=args.bm25_stemmer_algorithm,
        top_k=args.top_k,
        k1=args.bm25_k1,
        b=args.bm25_b,
        show_progress=args.show_progress,
    )


def bm25_config_name(config: BM25Config) -> str:
    tokenizer = config.tokenizer or "auto"
    parts = ["bm25s", _BM25_ALGORITHM_NAME, tokenizer]
    if config.tokenizer in {"transformer", "wordseg"} and config.tokenizer_name:
        parts.append(config.tokenizer_name)
    if config.tokenizer == "stemmer":
        parts.append(config.stemmer_algorithm)
    return "-".join(parts)


def bm25_config_payload(
    config: BM25Config,
    *,
    source: str = "computed_bm25s",
    candidate_subset_name: str | None = None,
) -> dict[str, Any]:
    payload = {
        "backend": "bm25s" if source == "computed_bm25s" else "dataset",
        "algorithm": _BM25_ALGORITHM_NAME if source == "computed_bm25s" else "bm25",
        "source": source,
        **asdict(config),
    }
    if candidate_subset_name is not None:
        payload["candidate_ranking"] = candidate_subset_name
    return payload


def collect_bm25_metadata(
    args: Any,
    *,
    config: BM25Config | None = None,
    source: str = "computed_bm25s",
    candidate_subset_name: str | None = None,
) -> dict[str, Any]:
    config = config or bm25_config_from_args(args)
    return {
        "method": "bm25",
        "id": getattr(args, "model_id", args.model),
        "source": getattr(args, "model_source", {"type": "bm25", "name": args.model}),
        "backend_library": "bm25s" if source == "computed_bm25s" else "dataset",
        "bm25": bm25_config_payload(config, source=source, candidate_subset_name=candidate_subset_name),
        "total_parameters": 0,
        "trainable_parameters": 0,
        "transformer_parameters": 0,
        "active_parameters": 0,
    }


def evaluate_bm25_task(
    *,
    dataset: Any,
    config: BM25Config,
    source: BM25EvaluationSource = "dataset_candidate_subset",
) -> Any:
    from hakari_bench.evaluation import TaskEvaluation

    score_start = time.perf_counter()
    if source == "dataset_candidate_subset":
        if dataset.candidates is None:
            raise ValueError(
                "BM25 dataset-source evaluation requires a candidate subset such as bm25. "
                "Use --bm25-source computed to recompute BM25 locally with bm25s."
            )
        rankings = rank_dataset_candidates(
            queries=dataset.queries,
            corpus=dataset.corpus,
            candidates=dataset.candidates,
            top_k=config.top_k,
        )
        score_name = "bm25_dataset_subset"
    elif source == "computed_bm25s":
        rankings = rank_bm25_candidates(corpus=dataset.corpus, queries=dataset.queries, config=config)
        score_name = "bm25_bm25s_okapi"
    else:
        raise ValueError(f"Unsupported BM25 evaluation source: {source!r}.")
    score_seconds = time.perf_counter() - score_start

    metric_start = time.perf_counter()
    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=dataset.qrels,
        evaluator_name=dataset.evaluator_name,
        score_name=score_name,
    )
    metric_seconds = time.perf_counter() - metric_start
    return TaskEvaluation(
        metrics=metrics,
        timing={
            "query_embedding_seconds": 0.0,
            "corpus_embedding_seconds": 0.0,
            "score_and_topk_seconds": float(score_seconds),
            "metric_compute_seconds": float(metric_seconds),
            "pure_compute_seconds": float(score_seconds + metric_seconds),
        },
    )


def rank_dataset_candidates(
    *,
    queries: dict[str, str],
    corpus: dict[str, str],
    candidates: dict[str, list[str]],
    top_k: int,
) -> dict[str, list[str]]:
    if top_k <= 0:
        raise ValueError("top_k must be positive.")
    return {
        query_id: [doc_id for doc_id in candidates.get(query_id, []) if doc_id in corpus][:top_k]
        for query_id in queries
    }


def rank_bm25_candidates(
    *,
    corpus: dict[str, str],
    queries: dict[str, str],
    config: BM25Config,
) -> dict[str, list[str]]:
    import bm25s

    if not corpus:
        raise ValueError("corpus is empty.")
    if not queries:
        raise ValueError("queries is empty.")
    config = resolve_bm25_config_for_queries(config, queries)
    _validate_config(config)

    corpus_ids = list(corpus)
    query_ids = list(queries)
    corpus_tokens = tokenize_texts(
        [corpus[corpus_id] for corpus_id in corpus_ids],
        tokenizer=cast(BM25Tokenizer, config.tokenizer),
        tokenizer_name=config.tokenizer_name,
        stemmer_algorithm=config.stemmer_algorithm,
    )
    query_tokens = tokenize_texts(
        [queries[query_id] for query_id in query_ids],
        tokenizer=cast(BM25Tokenizer, config.tokenizer),
        tokenizer_name=config.tokenizer_name,
        stemmer_algorithm=config.stemmer_algorithm,
    )
    if not any(corpus_tokens):
        raise ValueError("corpus produced no BM25 tokens.")

    top_k = max(1, min(config.top_k, len(corpus_ids)))
    retriever = bm25s.BM25(k1=config.k1, b=config.b, method=_BM25S_OKAPI_METHOD)
    retriever.index(corpus_tokens, show_progress=config.show_progress, leave_progress=False)
    ranked_indices, _scores = retriever.retrieve(
        query_tokens,
        k=top_k,
        show_progress=config.show_progress,
        leave_progress=False,
        return_as="tuple",
    )
    return {
        query_id: [corpus_ids[int(index)] for index in np.asarray(row).reshape(-1).tolist()]
        for query_id, row in zip(query_ids, ranked_indices)
    }


def tokenize_texts(
    texts: Sequence[str],
    *,
    tokenizer: BM25Tokenizer,
    tokenizer_name: str | None = None,
    stemmer_algorithm: str = "english",
) -> list[list[str]]:
    if tokenizer == "whitespace":
        return [[token for token in text.lower().split() if token] for text in texts]
    if tokenizer == "regex":
        return [_regex_tokens(text) for text in texts]
    if tokenizer == "english_regex":
        return [_english_regex_tokens(text) for text in texts]
    if tokenizer == "english_porter":
        return [_porter_stem_tokens(_english_regex_tokens(text)) for text in texts]
    if tokenizer == "english_porter_stop":
        return [
            _porter_stem_tokens([token for token in _english_regex_tokens(text) if token not in _ENGLISH_STOPWORDS])
            for text in texts
        ]
    if tokenizer == "stemmer":
        return [_pystemmer_tokens(_regex_tokens(text), stemmer_algorithm=stemmer_algorithm) for text in texts]
    if tokenizer == "transformer":
        return _tokenize_with_transformer(texts, tokenizer_name or _DEFAULT_TRANSFORMER_TOKENIZER)
    if tokenizer == "wordseg":
        return _tokenize_with_wordseg(texts, tokenizer_name)
    raise ValueError(f"Unsupported BM25 tokenizer: {tokenizer}")


def resolve_bm25_config_for_queries(
    config: BM25Config,
    queries: dict[str, str],
    *,
    detector: Callable[[str], Any] | None = None,
) -> BM25Config:
    if config.tokenizer is not None:
        return config

    sampled_queries = _sample_query_texts(queries, sample_size=10)
    detections = [_normalize_detect_result((detector or _detect_language)(text)) for text in sampled_queries]
    languages = [language for language, _score in detections if language]
    language_counts = dict(Counter(languages))
    detected_language = _select_detected_language(detections)

    if detected_language in WORD_SEGMENTATION_TOKENIZER_DEPENDENCIES:
        tokenizer = "wordseg"
        tokenizer_name = detected_language
    else:
        tokenizer = "regex"
        tokenizer_name = None

    return BM25Config(
        tokenizer=tokenizer,
        tokenizer_name=tokenizer_name,
        stemmer_algorithm=config.stemmer_algorithm,
        top_k=config.top_k,
        k1=config.k1,
        b=config.b,
        show_progress=config.show_progress,
        auto_selected=True,
        auto_detected_language=detected_language,
        auto_detection_language_counts=language_counts,
        auto_detection_sample_size=len(sampled_queries),
    )


def rankings_to_candidate_rows(rankings: dict[str, list[str]]) -> list[dict[str, Any]]:
    return [{"query-id": query_id, "corpus-ids": corpus_ids} for query_id, corpus_ids in rankings.items()]


def candidate_rows_to_rankings(rows: Sequence[dict[str, Any]]) -> dict[str, list[str]]:
    return {str(row["query-id"]): [str(corpus_id) for corpus_id in row["corpus-ids"]] for row in rows}


def bm25_candidate_path_for_task(*, output_dir: Path, task: EvalTask, config: BM25Config) -> Path:
    from hakari_bench.results import safe_path_part

    return output_dir / safe_path_part(bm25_config_name(config)) / safe_path_part(task.dataset_id) / f"{safe_path_part(task.task_name)}.json"


def run_or_load_bm25_task(
    *,
    task: EvalTask,
    dataset: Any,
    args: Any,
    config: BM25Config,
) -> BM25BuildResult:
    resolved_config = resolve_bm25_config_for_queries(config, dataset.queries)
    output_path = bm25_candidate_path_for_task(output_dir=Path(args.output_dir), task=task, config=resolved_config)
    if output_path.exists() and not args.override:
        return BM25BuildResult(
            task=task,
            cache_hit=True,
            output_path=output_path,
            payload=json.loads(output_path.read_text(encoding="utf-8")),
        )

    started_at = datetime.now(timezone.utc)
    start = time.perf_counter()
    rankings = rank_bm25_candidates(corpus=dataset.corpus, queries=dataset.queries, config=resolved_config)
    elapsed = time.perf_counter() - start
    rows = rankings_to_candidate_rows(rankings)
    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=dataset.qrels,
        evaluator_name=dataset.evaluator_name,
        score_name="bm25_bm25s_okapi",
    )
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": {
            "dataset_name": task.dataset_name,
            "dataset_id": task.dataset_id,
            "dataset_revision": resolve_dataset_revision(
                task.dataset_id,
                requested_revision=getattr(args, "dataset_revision", None),
            ),
            "split_name": task.split_name,
            "task_name": task.task_name,
            "corpus_config": task.dataset.corpus_config,
            "queries_config": task.dataset.queries_config,
            "qrels_config": task.dataset.qrels_config,
        },
        "config": bm25_config_payload(resolved_config),
        "evaluation": {
            "started_at_utc": started_at.isoformat(),
            "finished_at_utc": datetime.now(timezone.utc).isoformat(),
            "wall_seconds": float(elapsed),
            "cache_hit": False,
        },
        "metrics": metrics,
        "rows": rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return BM25BuildResult(task=task, cache_hit=False, output_path=output_path, payload=payload)


def _validate_config(config: BM25Config) -> None:
    if config.tokenizer not in {
        "whitespace",
        "regex",
        "transformer",
        "stemmer",
        "english_regex",
        "english_porter",
        "english_porter_stop",
        "wordseg",
    }:
        raise ValueError(f"Unsupported BM25 tokenizer: {config.tokenizer}")
    if config.top_k <= 0:
        raise ValueError("top_k must be positive.")
    if config.k1 <= 0.0:
        raise ValueError("k1 must be positive.")
    if not 0.0 <= config.b <= 1.0:
        raise ValueError("b must be between 0 and 1.")


def _regex_tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in _TOKEN_PATTERN.finditer(text)]


def _english_regex_tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in _ENGLISH_TOKEN_PATTERN.finditer(text)]


def _porter_stem_tokens(tokens: list[str]) -> list[str]:
    from nltk.stem import PorterStemmer

    stemmer = PorterStemmer()
    return [str(stemmer.stem(token)) for token in tokens]


def _pystemmer_tokens(tokens: list[str], *, stemmer_algorithm: str) -> list[str]:
    stemmer_module = importlib.import_module("Stemmer")
    stemmer_cls = getattr(stemmer_module, "Stemmer")
    stemmer = stemmer_cls(stemmer_algorithm)
    return [str(stemmer.stemWord(token)) for token in tokens]


def _sample_query_texts(queries: dict[str, str], *, sample_size: int) -> list[str]:
    texts = [text for text in queries.values() if text]
    if len(texts) <= sample_size:
        return texts
    return random.Random(0).sample(texts, sample_size)


def _detect_language(text: str) -> Any:
    fast_langdetect_module = importlib.import_module("fast_langdetect")
    detect_fn = getattr(fast_langdetect_module, "detect")
    return detect_fn(text)


def _normalize_detect_result(result: Any) -> tuple[str | None, float]:
    candidate = result[0] if isinstance(result, list) and result else result
    if isinstance(candidate, dict):
        language = candidate.get("lang") or candidate.get("language")
        score = candidate.get("score") or candidate.get("probability") or 0.0
        return (_normalize_language_code(str(language)) if language else None, float(score))
    if isinstance(candidate, str):
        return _normalize_language_code(candidate), 1.0
    return None, 0.0


def _normalize_language_code(language: str) -> str:
    return language.lower().replace("_", "-").split("-")[0]


def _select_detected_language(detections: list[tuple[str | None, float]]) -> str | None:
    scores: dict[str, float] = {}
    counts: Counter[str] = Counter()
    for language, score in detections:
        if language is None:
            continue
        counts[language] += 1
        scores[language] = scores.get(language, 0.0) + score
    if not counts:
        return None
    return sorted(counts, key=lambda language: (-counts[language], -scores[language], language))[0]


def _tokenize_with_transformer(texts: Sequence[str], tokenizer_name: str) -> list[list[str]]:
    from transformers import AutoTokenizer

    transformer_tokenizer: Any = AutoTokenizer.from_pretrained(tokenizer_name)
    tokenized_texts: list[list[str]] = []
    for text in texts:
        tokens: list[str] = []
        for chunk in _chunk_text(text, max_chunk_chars=_MAX_TOKENIZER_CHUNK_CHARS):
            tokenize_fn = getattr(transformer_tokenizer, "tokenize")
            raw_tokens = tokenize_fn(chunk, add_special_tokens=False)
            if isinstance(raw_tokens, str):
                tokens.append(raw_tokens)
            else:
                tokens.extend(str(token) for token in raw_tokens)
        tokenized_texts.append(tokens)
    return tokenized_texts


def _tokenize_with_wordseg(texts: Sequence[str], language: str | None) -> list[list[str]]:
    if language is None:
        raise ValueError(
            "wordseg tokenizer requires --bm25-wordseg-language with one of "
            f"{sorted(WORD_SEGMENTATION_TOKENIZER_DEPENDENCIES)}."
        )
    splitter = _build_wordseg_splitter(_normalize_wordseg_language(language))
    return [splitter(text) for text in texts]


def _normalize_wordseg_language(language: str) -> str:
    return language.lower().replace("_", "-").split("-")[0]


def _build_wordseg_splitter(
    language: str,
    *,
    module_loader: Callable[[str], Any] = importlib.import_module,
) -> Callable[[str], list[str]]:
    language = _normalize_wordseg_language(language)
    if language == "ja":
        fugashi_module = _load_wordseg_module("fugashi", language=language, module_loader=module_loader)
        _load_wordseg_module("unidic_lite", language=language, module_loader=module_loader)
        tagger_cls = getattr(fugashi_module, "Tagger")
        tagger = tagger_cls()

        def splitter(text: str) -> list[str]:
            return _tokenize_chunked(
                text,
                lambda chunk: [str(word.surface) for word in tagger(chunk) if str(word.surface)],
            )

        return splitter

    if language == "zh":
        jieba_module = _load_wordseg_module("jieba", language=language, module_loader=module_loader)
        cut_fn = cast(Callable[[str], Iterable[str]], getattr(jieba_module, "cut"))

        def splitter(text: str) -> list[str]:
            return _tokenize_chunked(text, lambda chunk: [str(token) for token in cut_fn(chunk) if str(token)])

        return splitter

    if language == "th":
        pythainlp_tokenize_module = _load_wordseg_module(
            "pythainlp.tokenize",
            language=language,
            module_loader=module_loader,
        )
        word_tokenize_fn = cast(Callable[..., list[str]], getattr(pythainlp_tokenize_module, "word_tokenize"))

        def splitter(text: str) -> list[str]:
            return _tokenize_chunked(
                text,
                lambda chunk: [str(token) for token in word_tokenize_fn(chunk, engine="newmm") if str(token)],
            )

        return splitter

    if language == "ko":
        kiwipiepy_module = _load_wordseg_module("kiwipiepy", language=language, module_loader=module_loader)
        kiwi_cls = getattr(kiwipiepy_module, "Kiwi")
        kiwi = kiwi_cls()

        def splitter(text: str) -> list[str]:
            return _tokenize_chunked(
                text,
                lambda chunk: [str(token.form) for token in kiwi.tokenize(chunk) if str(token.form)],
            )

        return splitter

    if language == "vi":
        pyvi_tokenizer_module = _load_wordseg_module(
            "pyvi.ViTokenizer",
            language=language,
            module_loader=module_loader,
        )
        raw_tokenize_fn = getattr(pyvi_tokenizer_module, "tokenize", None)
        if raw_tokenize_fn is None:
            raw_tokenize_fn = getattr(getattr(pyvi_tokenizer_module, "ViTokenizer"), "tokenize")
        tokenize_fn = cast(Callable[[str], str], raw_tokenize_fn)

        def splitter(text: str) -> list[str]:
            return _tokenize_chunked(
                text,
                lambda chunk: [
                    token.lower()
                    for token in str(tokenize_fn(chunk)).split()
                    if token and _has_token_text(token)
                ],
            )

        return splitter

    raise ValueError(
        f"wordseg tokenizer does not support language '{language}'. "
        f"Supported languages: {sorted(WORD_SEGMENTATION_TOKENIZER_DEPENDENCIES)}"
    )


def _load_wordseg_module(
    module_name: str,
    *,
    language: str,
    module_loader: Callable[[str], Any],
) -> Any:
    try:
        return module_loader(module_name)
    except ImportError as exc:
        dependencies = WORD_SEGMENTATION_TOKENIZER_DEPENDENCIES.get(language, ())
        raise RuntimeError(
            f"Missing dependencies for wordseg language '{language}': {dependencies}. "
            "Install them with `uv sync --extra wordseg` or install the matching optional packages."
        ) from exc


def _has_token_text(token: str) -> bool:
    return any(char.isalnum() for char in token)


def _tokenize_chunked(text: str, tokenize_chunk: Callable[[str], list[str]]) -> list[str]:
    tokens: list[str] = []
    for text_chunk in _chunk_text(text, max_chunk_chars=_MAX_TOKENIZER_CHUNK_CHARS):
        tokens.extend(tokenize_chunk(text_chunk))
    return tokens


def _chunk_text(text: str, *, max_chunk_chars: int) -> list[str]:
    if max_chunk_chars <= 0:
        raise ValueError("max_chunk_chars must be positive.")
    if len(text) <= max_chunk_chars:
        return [text]
    return [text[index : index + max_chunk_chars] for index in range(0, len(text), max_chunk_chars)]
