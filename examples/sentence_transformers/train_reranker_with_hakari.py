from __future__ import annotations

import argparse
import logging
from pathlib import Path

import torch
from datasets import Dataset, load_dataset

from hakari_bench.sentence_transformers import HakariNanoRerankerEvaluator, HakariNanoTarget
from sentence_transformers.cross_encoder import CrossEncoder, CrossEncoderModelCardData
from sentence_transformers.cross_encoder.losses import BinaryCrossEntropyLoss
from sentence_transformers.cross_encoder.trainer import CrossEncoderTrainer
from sentence_transformers.cross_encoder.training_args import CrossEncoderTrainingArguments

LOGGER = logging.getLogger(__name__)
DEFAULT_MODEL = "hotchpotch/mmBERT-L4H384-pruned"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a CrossEncoder reranker with HAKARI Nano evaluation.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--output-dir", default="output/sentence_transformers/reranker_hakari")
    parser.add_argument("--train-samples", type=int, default=50_000)
    parser.add_argument("--eval-samples", type=int, default=2_000)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--num-train-epochs", type=float, default=1.0)
    parser.add_argument("--eval-steps", type=int, default=500)
    parser.add_argument("--save-steps", type=int, default=500)
    parser.add_argument("--rerank-top-k", type=int, default=100)
    parser.add_argument("--eval-query-limit", type=int, default=None)
    parser.add_argument("--query-sample-seed", type=int, default=13)
    parser.add_argument("--bf16", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--fp16", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--smoke-train", action="store_true")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    args = parse_args()
    if args.smoke_train:
        args.train_samples = min(args.train_samples, 128)
        args.eval_samples = min(args.eval_samples, 32)
        args.batch_size = min(args.batch_size, 8)
        args.eval_steps = 2
        args.save_steps = 2
        args.num_train_epochs = 1
        args.rerank_top_k = min(args.rerank_top_k, 10)
        args.eval_query_limit = args.eval_query_limit or 3

    model_name_only = args.model.split("/")[-1]
    model = CrossEncoder(
        args.model,
        num_labels=1,
        model_card_data=CrossEncoderModelCardData(
            language="multilingual",
            license="apache-2.0",
            model_name=f"{model_name_only} reranker trained with HAKARI Nano evaluation",
        ),
    )
    train_dataset, eval_dataset = load_labeled_gooaq_pairs(
        train_samples=args.train_samples,
        eval_samples=args.eval_samples,
    )
    evaluator = build_hakari_evaluator(
        batch_size=args.batch_size,
        rerank_top_k=args.rerank_top_k,
        query_limit=args.eval_query_limit,
        query_sample_seed=args.query_sample_seed,
        smoke_train=args.smoke_train,
    )
    LOGGER.info("Evaluating the base reranker with HAKARI Nano targets")
    evaluator(model)

    training_args = CrossEncoderTrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        warmup_ratio=0.1,
        fp16=args.fp16,
        bf16=args.bf16,
        eval_strategy="steps",
        eval_steps=args.eval_steps,
        save_strategy="steps",
        save_steps=args.save_steps,
        save_total_limit=2,
        logging_steps=max(1, args.eval_steps // 5),
        logging_first_step=True,
        load_best_model_at_end=True,
        metric_for_best_model=f"eval_{evaluator.primary_metric}",
        run_name=f"{model_name_only}-hakari-reranker",
    )
    loss = BinaryCrossEntropyLoss(model=model, pos_weight=torch.tensor(1.0))
    trainer = CrossEncoderTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss=loss,
        evaluator=evaluator,
    )
    trainer.train()
    evaluator(model)
    final_output_dir = Path(args.output_dir) / "final"
    model.save_pretrained(str(final_output_dir))


def build_hakari_evaluator(
    *,
    batch_size: int,
    rerank_top_k: int,
    query_limit: int | None,
    query_sample_seed: int,
    smoke_train: bool,
) -> HakariNanoRerankerEvaluator:
    return HakariNanoRerankerEvaluator(
        targets=default_hakari_targets(),
        batch_size=batch_size,
        rerank_top_k=rerank_top_k,
        query_limit=query_limit,
        query_sample_seed=query_sample_seed,
        corpus_policy="sampled_candidates" if smoke_train else "full",
        candidate_ranking="bm25",
    )


def default_hakari_targets() -> list[HakariNanoTarget]:
    return [
        HakariNanoTarget(dataset="NanoMIRACL", splits=["en"]),
        HakariNanoTarget(dataset="NanoCoIR"),
        HakariNanoTarget(dataset="NanoMMTEB-v2"),
    ]


def load_labeled_gooaq_pairs(*, train_samples: int, eval_samples: int) -> tuple[Dataset, Dataset]:
    dataset = load_dataset("sentence-transformers/gooaq", split="train")
    dataset = _select_at_most(dataset, max(2, train_samples + eval_samples))
    split = dataset.train_test_split(test_size=min(eval_samples, max(1, len(dataset) // 5)), seed=12)
    return (
        _labeled_pairs_from_gooaq(_select_at_most(split["train"], train_samples)),
        _labeled_pairs_from_gooaq(_select_at_most(split["test"], eval_samples)),
    )


def _labeled_pairs_from_gooaq(dataset: Dataset) -> Dataset:
    questions = list(dataset["question"])
    answers = list(dataset["answer"])
    rows: list[dict[str, str | int]] = []
    for index, question in enumerate(questions):
        rows.append({"query": question, "response": answers[index], "label": 1})
        rows.append({"query": question, "response": answers[(index + 1) % len(answers)], "label": 0})
    return Dataset.from_list(rows)


def _select_at_most(dataset: Dataset, count: int) -> Dataset:
    return dataset.select(range(min(count, len(dataset))))


if __name__ == "__main__":
    main()
