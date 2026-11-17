"""Convert a Qwen3-Reranker CausalLM checkpoint into a vLLM-servable SequenceClassification checkpoint.

The original model scores a pair with ``logit("yes") - logit("no")`` at the
last position, which is what the SentenceTransformers ``LogitScore`` module
returns. Because ``logits = norm(h) @ lm_head.T``, a one-label score head whose
weight is ``lm_head["yes"] - lm_head["no"]`` returns the same value from the
same final hidden state. The converted checkpoint can therefore be served by
vLLM as a last-token pooling classifier without changing scores.

Usage:

    python scripts/convert_qwen3_reranker_seqcls.py Qwen/Qwen3-Reranker-4B \
        output/models/Qwen3-Reranker-4B-seqcls --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

import torch
from transformers import AutoModelForCausalLM, AutoModelForSequenceClassification, AutoTokenizer

YES_TOKEN = "yes"
NO_TOKEN = "no"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a Qwen3-Reranker checkpoint into a vLLM-servable SeqCls checkpoint.")
    parser.add_argument("model", help="Hugging Face model ID or local path of the original Qwen3-Reranker.")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--revision", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    tokenizer = cast(Any, AutoTokenizer).from_pretrained(args.model, revision=args.revision)
    yes_id = tokenizer.convert_tokens_to_ids(YES_TOKEN)
    no_id = tokenizer.convert_tokens_to_ids(NO_TOKEN)

    causal = AutoModelForCausalLM.from_pretrained(args.model, revision=args.revision, dtype=torch.bfloat16)
    # Read lm_head instead of the input embedding so untied checkpoints (Qwen3-Reranker-8B) convert correctly.
    lm_head = causal.get_output_embeddings().weight.detach()
    score_weight = (lm_head[yes_id].float() - lm_head[no_id].float())[None].to(torch.bfloat16)
    del causal

    model = AutoModelForSequenceClassification.from_pretrained(
        args.model, revision=args.revision, num_labels=1, dtype=torch.bfloat16
    )
    model.score.weight.data.copy_(score_weight)
    model.config.pad_token_id = tokenizer.pad_token_id
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    (args.output_dir / "hakari_conversion.json").write_text(
        json.dumps(
            {
                "source": args.model,
                "revision": args.revision,
                "score": "logit(yes) - logit(no) at the last token",
                "yes_token_id": yes_id,
                "no_token_id": no_id,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"saved {args.output_dir}")


if __name__ == "__main__":
    main()
