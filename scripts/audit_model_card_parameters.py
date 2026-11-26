"""Audit model-card parameter counts against Hugging Face safetensors headers.

Only safetensors headers are downloaded (tensor names and shapes), not weights.
For each Hugging Face model card the script counts total, input-embedding,
non-text (vision/audio encoders and projectors, see
``hakari_bench.models.NON_TEXT_MODULE_NAMES``) and active parameters, and
compares them with ``parameters`` in the card.

``--write`` updates cards whose checkpoint bundles non-text modules, when the
header counts agree with the counts already recorded for the loaded model.
Cards with a remaining mismatch are only reported, so they can be reviewed by
loading the model. Policy: docs/model_cards.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from huggingface_hub import HfApi

from hakari_bench.model_cards import model_card_yaml_paths, replace_model_card_parameters_text
from hakari_bench.models import count_parameters_from_tensor_shapes

DEFAULT_MODEL_CARDS_PATH = Path("config/model_cards")
_ROOT_WEIGHTS_RE = re.compile(r"^model(-\d+-of-\d+)?\.safetensors$")
_MODULE_WEIGHTS_RE = re.compile(r"^\d+_[^/]+/model\.safetensors$")


def checkpoint_tensor_shapes(api: HfApi, repo_id: str, *, revision: str | None) -> dict[str, list[int]]:
    """Return tensor shapes of the root model and SentenceTransformers module weights."""
    files = api.list_repo_files(repo_id, revision=revision)
    weight_files = [name for name in files if _ROOT_WEIGHTS_RE.match(name) or _MODULE_WEIGHTS_RE.match(name)]
    shapes: dict[str, list[int]] = {}
    for filename in sorted(weight_files):
        metadata = api.parse_safetensors_file_metadata(repo_id, filename, revision=revision)
        prefix = "" if "/" not in filename else filename.rsplit("/", 1)[0] + "/"
        for tensor_name, info in metadata.tensors.items():
            shapes[prefix + tensor_name] = list(info.shape)
    return shapes


def audit_card(card: dict[str, Any], header: dict[str, Any]) -> dict[str, Any]:
    """Compare a card with header counts and propose non-text-aware parameters.

    The card's loaded-model ``total`` and ``input_embedding`` stay authoritative;
    the header only supplies the non-text count. Non-text modules are treated as
    loaded when the card total is close to the header total (within half of the
    non-text count), which excludes loaders that only build the text model.
    """
    raw_parameters = card.get("parameters")
    parameters: dict[str, Any] = raw_parameters if isinstance(raw_parameters, dict) else {}
    issues: list[str] = []
    card_total = parameters.get("total")
    card_embedding = parameters.get("input_embedding")
    non_text = header["non_text"]
    if card_total is None:
        issues.append("card has no total")
    elif card_total != header["total"]:
        issues.append(f"total differs from the checkpoint header by {card_total - header['total']}")
    if header["input_embedding"] is None:
        issues.append("no input embedding table found in the header")
    elif card_embedding is not None and card_embedding != header["input_embedding"]:
        issues.append(f"input embedding {card_embedding} differs from the header {header['input_embedding']}")
    non_text_loaded = card_total is not None and non_text > 0 and abs(card_total - header["total"]) < non_text / 2
    if non_text > 0 and card_total is not None and not non_text_loaded:
        issues.append("non-text modules are not part of the loaded model")
    proposed = None
    if non_text_loaded and card_embedding is not None and card_embedding == header["input_embedding"]:
        proposed = {
            "total": card_total,
            "trainable": parameters.get("trainable"),
            "input_embedding": card_embedding,
            "non_text": non_text,
            "active": card_total - card_embedding - non_text,
        }
    return {
        "id": card["id"],
        "card_total": card_total,
        "card_input_embedding": card_embedding,
        "card_active": parameters.get("active"),
        "header_total": header["total"],
        "header_input_embedding": header["input_embedding"],
        "header_non_text": non_text,
        "header_active": header["active"],
        "issues": issues,
        "proposed": proposed,
        "writable": proposed is not None and proposed["active"] != parameters.get("active"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--model-cards-path", type=Path, default=DEFAULT_MODEL_CARDS_PATH)
    parser.add_argument("--model", action="append", default=None, help="Only audit this model id (repeatable).")
    parser.add_argument("--write", action="store_true", help="Update cards that bundle non-text modules.")
    parser.add_argument("--json-output", type=Path, default=None)
    args = parser.parse_args()

    api = HfApi()
    rows: list[dict[str, Any]] = []
    for path in model_card_yaml_paths(args.model_cards_path):
        text = path.read_text(encoding="utf-8")
        card = yaml.safe_load(text)
        source = card.get("source") or {}
        if source.get("type") != "huggingface" or (args.model and card["id"] not in args.model):
            continue
        try:
            shapes = checkpoint_tensor_shapes(api, source["name"], revision=source.get("revision"))
        except Exception as error:  # report and keep auditing the remaining cards
            rows.append({"id": card["id"], "error": f"{type(error).__name__}: {error}"[:200]})
            continue
        if not shapes:
            rows.append({"id": card["id"], "error": "no safetensors weights"})
            continue
        row = audit_card(card, count_parameters_from_tensor_shapes(shapes))
        if args.write and row["writable"]:
            path.write_text(replace_model_card_parameters_text(text, row["proposed"]), encoding="utf-8")
            row["written"] = str(path)
        rows.append(row)
        if row["issues"] or row["header_non_text"]:
            print(json.dumps(row), file=sys.stderr)

    print("| model | card total | card active | header total | non-text | proposed active | issues |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for row in rows:
        if "error" in row:
            print(f"| {row['id']} | | | | | | {row['error']} |")
        elif row["issues"] or row["header_non_text"]:
            print(
                f"| {row['id']} | {row['card_total']} | {row['card_active']} | {row['header_total']} | "
                f"{row['header_non_text']} | {(row['proposed'] or {}).get('active', '')} | {'; '.join(row['issues'])} |"
            )
    ok = sum(1 for row in rows if "error" not in row and not row["issues"] and not row["header_non_text"])
    print(f"\n{ok} cards match their checkpoint headers and have no non-text modules.")
    if args.json_output is not None:
        args.json_output.write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
