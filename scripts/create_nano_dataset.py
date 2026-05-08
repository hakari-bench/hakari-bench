from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import cast

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from hakari_bench.bm25 import BM25Config, BM25Tokenizer  # noqa: E402
from hakari_bench.nano_dataset_builder import (  # noqa: E402
    DEFAULT_BM25_TOP_K,
    DEFAULT_DOC_LIMIT,
    DEFAULT_QUERY_LIMIT,
    build_nano_dataset_from_hf_mteb,
    build_nano_dataset_from_local_source,
)


TOKENIZERS = {
    "regex",
    "whitespace",
    "transformer",
    "stemmer",
    "english_regex",
    "english_porter",
    "english_porter_stop",
    "wordseg",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a Nano-style retrieval dataset from MTEB/BEIR-style sources. "
            "The output uses corpus/queries/qrels/bm25 configs with task subsets as split names."
        )
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--source-dataset-id", help="Hugging Face MTEB/BEIR-style source dataset id.")
    source.add_argument("--source-dir", type=Path, help="Local parquet source root.")

    parser.add_argument("--dataset-name", required=True, help="Nano dataset name, e.g. NanoExample.")
    parser.add_argument("--dataset-id", required=True, help="Final Hugging Face dataset id, e.g. hakari-bench/NanoExample.")
    parser.add_argument("--split-name", required=True, help="Output Nano split/subset name.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output dataset directory.")
    parser.add_argument(
        "--dataset-config-dir",
        type=Path,
        default=None,
        help="Optional config/datasets directory where the HAKARI dataset YAML should be written.",
    )

    parser.add_argument("--source-split-name", default=None, help="Local source split/task name.")
    parser.add_argument("--corpus-config", default="corpus")
    parser.add_argument("--queries-config", default="queries")
    parser.add_argument("--qrels-config", default="default")
    parser.add_argument("--corpus-split", default="corpus")
    parser.add_argument("--queries-split", default="queries")
    parser.add_argument("--qrels-split", default="test")
    parser.add_argument("--revision", default=None)

    parser.add_argument("--query-limit", type=int, default=DEFAULT_QUERY_LIMIT)
    parser.add_argument("--doc-limit", type=int, default=DEFAULT_DOC_LIMIT)
    parser.add_argument("--top-k", type=int, default=DEFAULT_BM25_TOP_K)
    parser.add_argument("--bm25-tokenizer", choices=sorted(TOKENIZERS), default="regex")
    parser.add_argument("--bm25-tokenizer-name", default=None)
    parser.add_argument("--bm25-stemmer-algorithm", default="english")
    parser.add_argument("--bm25-k1", type=float, default=1.5)
    parser.add_argument("--bm25-b", type=float, default=0.75)
    parser.add_argument("--show-progress", action="store_true")
    parser.add_argument(
        "--metadata-json",
        default=None,
        help="Optional JSON object for the generated HAKARI dataset YAML metadata.",
    )
    return parser.parse_args(argv)


def _metadata(raw: str | None) -> dict[str, object] | None:
    if raw is None:
        return None
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("--metadata-json must be a JSON object.")
    return cast(dict[str, object], parsed)


def _bm25_config(args: argparse.Namespace) -> BM25Config:
    return BM25Config(
        tokenizer=cast(BM25Tokenizer, args.bm25_tokenizer),
        tokenizer_name=args.bm25_tokenizer_name,
        stemmer_algorithm=args.bm25_stemmer_algorithm,
        top_k=args.top_k,
        k1=args.bm25_k1,
        b=args.bm25_b,
        show_progress=args.show_progress,
    )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    metadata = _metadata(args.metadata_json)
    bm25_config = _bm25_config(args)

    if args.source_dir is not None:
        source_split_name = args.source_split_name or args.split_name
        result = build_nano_dataset_from_local_source(
            source_dir=args.source_dir,
            output_dir=args.output_dir,
            dataset_name=args.dataset_name,
            dataset_id=args.dataset_id,
            source_split_name=source_split_name,
            split_name=args.split_name,
            dataset_config_dir=args.dataset_config_dir,
            query_limit=args.query_limit,
            doc_limit=args.doc_limit,
            bm25_config=bm25_config,
            metadata=metadata,
        )
    else:
        result = build_nano_dataset_from_hf_mteb(
            source_dataset_id=args.source_dataset_id,
            output_dir=args.output_dir,
            dataset_name=args.dataset_name,
            dataset_id=args.dataset_id,
            split_name=args.split_name,
            dataset_config_dir=args.dataset_config_dir,
            corpus_config=args.corpus_config,
            queries_config=args.queries_config,
            qrels_config=args.qrels_config,
            corpus_split=args.corpus_split,
            queries_split=args.queries_split,
            qrels_split=args.qrels_split,
            revision=args.revision,
            query_limit=args.query_limit,
            doc_limit=args.doc_limit,
            bm25_config=bm25_config,
            metadata=metadata,
        )

    print(f"dataset={result.dataset_name}")
    print(f"split={result.split_name}")
    print(f"output_dir={result.output_dir}")
    print(f"queries={result.queries} corpus={result.corpus} qrels={result.qrels}")
    print(f"source_non_positive_qrels={result.source_non_positive_qrels}")
    print(f"forced_doc_count={result.forced_doc_count}")
    print(f"missing_positive_doc_count_after_forcing={result.missing_positive_doc_count_after_forcing}")
    print(f"bm25_ndcg_at_10={result.bm25_ndcg_at_10:.4f}")
    if result.dataset_config_path is not None:
        print(f"dataset_config={result.dataset_config_path}")


if __name__ == "__main__":
    main()
