from __future__ import annotations

import argparse
import re
from pathlib import Path

from hakari_bench.model_cards import (
    ModelCardOverrides,
    build_model_card_from_loaded_model,
    collect_model_cards_from_results,
    load_model_cards,
    parse_truncate_dims,
    write_model_card,
)


_FULL_HF_REVISION_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate static HAKARI model-card YAML files.")
    parser.add_argument("--model", default=None, help="Hugging Face model id or local model path to load.")
    parser.add_argument("--model-id", default=None, help="Canonical model id written to the card. Defaults to --model.")
    parser.add_argument("--model-type", default="dense", choices=["dense", "sparse", "reranker", "late-interaction"])
    parser.add_argument(
        "--truncate-dims",
        nargs="+",
        default=None,
        help="Dense truncation dimensions, for example: --truncate-dims 768. Use 'none' for unsupported models.",
    )
    parser.add_argument(
        "--from-results",
        type=Path,
        default=None,
        help="Build one card per model from existing output/hakari-results JSON instead of loading a single model.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("config/model_cards"))
    parser.add_argument("--dataset", action="append", default=None, help="Dataset id/name to store in the card target.")
    parser.add_argument("--collection", action="append", default=[], help="Dataset collection to store in the card target.")
    parser.add_argument("--split", action="append", default=[], help="Split/task name to store in the card target.")
    parser.add_argument("--dataset-revision", default=None, help="Dataset revision to store in the card target.")
    parser.add_argument(
        "--existing-model-cards-path",
        type=Path,
        default=None,
        help="Existing model cards used as fallback metadata during --from-results generation. Defaults to --output-dir.",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--exclude-model", action="append", default=["bm25"], help="Model id to skip in --from-results mode.")
    parser.add_argument(
        "--exclude-model-substring",
        action="append",
        default=["bekko"],
        help="Case-insensitive model id substring to skip in --from-results mode.",
    )
    parser.add_argument("--model-revision", default=None)
    parser.add_argument("--dtype", default="bf16", choices=["bf16", "fp16", "fp32"])
    parser.add_argument("--attn-implementation", default=None)
    parser.add_argument("--flash-attn2", action="store_true")
    parser.add_argument("--device", default=None)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument(
        "--remote-code-approved",
        action="store_true",
        help="Mark trust_remote_code model cards as reviewed. Requires --trust-remote-code and a full --model-revision SHA.",
    )
    parser.add_argument("--model-max-seq-length", type=int, default=None)
    parser.add_argument("--display-name", default=None)
    parser.add_argument("--source-name", default=None)
    parser.add_argument("--source-revision", default=None)
    parser.add_argument("--source-revision-requested", default=None)
    parser.add_argument("--total-parameters", type=int, default=None)
    parser.add_argument("--trainable-parameters", type=int, default=None)
    parser.add_argument("--input-embedding-parameters", type=int, default=None)
    parser.add_argument("--active-parameters", type=int, default=None)
    parser.add_argument("--max-seq-length", type=int, default=None)
    args = parser.parse_args()

    overrides = ModelCardOverrides(
        display_name=args.display_name,
        source_name=args.source_name,
        source_revision=args.source_revision,
        source_revision_requested=args.source_revision_requested,
        total_parameters=args.total_parameters,
        trainable_parameters=args.trainable_parameters,
        input_embedding_parameters=args.input_embedding_parameters,
        active_parameters=args.active_parameters,
        max_seq_length=args.max_seq_length,
    )
    if args.from_results is not None:
        existing_cards_path = args.existing_model_cards_path or args.output_dir
        cards = collect_model_cards_from_results(
            args.from_results,
            exclude_model_substrings=args.exclude_model_substring,
            exclude_model_ids=args.exclude_model,
            existing_cards=load_model_cards(existing_cards_path),
        )
        for card in cards.values():
            output_path = write_model_card(card, output_dir=args.output_dir, overwrite=args.overwrite)
            print(output_path)
        return

    if args.model is None:
        parser.error("--model is required unless --from-results is used.")
    if args.remote_code_approved and not args.trust_remote_code:
        parser.error("--remote-code-approved requires --trust-remote-code.")
    if args.trust_remote_code and args.remote_code_approved and (
        args.model_revision is None or _FULL_HF_REVISION_SHA_RE.fullmatch(args.model_revision) is None
    ):
        parser.error("--remote-code-approved requires --model-revision to be the full reviewed Hugging Face revision SHA.")
    model_id = args.model_id or args.model
    try:
        truncate_dims = parse_truncate_dims(args.truncate_dims, model_type=args.model_type)
    except ValueError as exc:
        parser.error(str(exc))
    card = build_model_card_from_loaded_model(
        model_id=model_id,
        model_type=args.model_type,
        truncate_dims=truncate_dims,
        overrides=overrides,
        model_revision=args.model_revision,
        dtype=args.dtype,
        attn_implementation=args.attn_implementation,
        flash_attn2=args.flash_attn2,
        device=args.device,
        trust_remote_code=args.trust_remote_code,
        remote_code_approved=args.remote_code_approved,
        model_max_seq_length=args.model_max_seq_length,
        target={
            "datasets": args.dataset or [],
            "collections": args.collection,
            "splits": args.split,
            "dataset_revision": args.dataset_revision,
        },
    )
    output_path = write_model_card(card, output_dir=args.output_dir, overwrite=args.overwrite)
    print(output_path)


if __name__ == "__main__":
    main()
