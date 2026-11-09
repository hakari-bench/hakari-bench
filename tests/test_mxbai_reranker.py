import numpy as np
import pytest
import torch

from hakari_bench.model_loaders import MxbaiRerankV2Adapter, load_mxbai_rerank_v2
from hakari_bench.models import ModelLoadConfig


class CharacterTokenizer:
    padding_side = "left"

    def apply_chat_template(self, messages, *, tokenize):
        assert not tokenize
        return f"<user>query: {messages[0]['content']}\ndocument: {messages[1]['content']}\nRelevance:<assistant>"

    def __call__(self, text, *, add_special_tokens=False, truncation=False, max_length=None):
        ids = [ord(c) for c in text]
        return {"input_ids": ids[:max_length] if truncation else ids}

    def decode(self, ids, **kwargs):
        return "".join(map(chr, ids))

    def pad(self, rows, *, padding, return_tensors):
        size = max(len(row["input_ids"]) for row in rows)
        return {
            "input_ids": torch.tensor([[0] * (size - len(row["input_ids"])) + row["input_ids"] for row in rows]),
            "attention_mask": torch.tensor([[0] * (size - len(row["input_ids"])) + [1] * len(row["input_ids"]) for row in rows]),
        }


class FakeCrossEncoder:
    tokenizer = CharacterTokenizer()
    max_seq_length = 160
    device = "cpu"

    def __init__(self, *, fail_above=None, finite=True):
        self.fail_above = fail_above
        self.finite = finite
        self.shapes = []

    def eval(self):
        return self

    def forward(self, features):
        shape = features["input_ids"].shape
        self.shapes.append(shape)
        assert features["logits_to_keep"] == 1
        assert features["use_cache"] is False
        if self.fail_above and shape[0] > self.fail_above:
            raise torch.OutOfMemoryError("test CUDA OOM")
        scores = features["input_ids"].sum(1).float()
        if not self.finite:
            scores[:] = float("nan")
        return {"scores": scores[:, None]}


def test_short_input_matches_checkpoint_template_exactly():
    encoder = FakeCrossEncoder()
    model = MxbaiRerankV2Adapter(encoder)
    pair = ["Who?", "A short document."]
    expected = encoder.tokenizer.apply_chat_template(
        [dict(role="query", content=pair[0]), dict(role="document", content=pair[1])], tokenize=False
    )
    assert encoder.tokenizer.decode(model.prepare_pair(pair)) == expected


@pytest.mark.parametrize("query,document", [("Who?", "x" * 2000), ("q" * 2000, "x" * 2000), ("q" * 2000, "x")], ids=["long-document", "both-long", "long-query"])
def test_long_input_keeps_query_document_and_relevance_suffix(query, document):
    model = MxbaiRerankV2Adapter(FakeCrossEncoder())
    ids = model.prepare_pair([query, document])
    text = model.tokenizer.decode(ids)
    assert len(ids) <= model.max_seq_length
    assert text.startswith("<user>query: ")
    assert "\ndocument: x" in text
    assert text.endswith("\nRelevance:<assistant>")
    assert text.count("Relevance:") == 1
    assert model.metadata()["truncated_pairs"] == 1
    model.reset_task_statistics()
    assert model.metadata()["truncated_pairs"] == 0


def test_token_budget_and_oom_retry_preserve_scores_and_order(monkeypatch):
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: None)
    pairs = [["A", "short"], ["B", "x" * 80], ["C", "medium"], ["D", "y" * 80]]
    expected = MxbaiRerankV2Adapter(FakeCrossEncoder()).predict(pairs, batch_size=1)
    encoder = FakeCrossEncoder(fail_above=1)
    model = MxbaiRerankV2Adapter(encoder, max_batch_tokens=250)
    actual = model.predict(pairs, batch_size=4)
    np.testing.assert_array_equal(actual, expected)
    assert model.metadata()["oom_retries"] > 0
    assert all(rows * width <= 250 for rows, width in encoder.shapes)


def test_nonfinite_scores_fail_instead_of_writing_invalid_rankings():
    with pytest.raises(ValueError, match="non-finite"):
        MxbaiRerankV2Adapter(FakeCrossEncoder(finite=False)).predict([["q", "d"]])


def test_single_pair_oom_is_not_hidden(monkeypatch):
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: None)
    encoder = FakeCrossEncoder()
    monkeypatch.setattr(encoder, "forward", lambda features: (_ for _ in ()).throw(torch.OutOfMemoryError("single")))
    with pytest.raises(torch.OutOfMemoryError, match="single"):
        MxbaiRerankV2Adapter(encoder).predict([["q", "d"]])


def test_loader_preserves_runtime_options_and_removes_recursive_loader(monkeypatch):
    configs = []

    def fake_load(config):
        configs.append(config)
        return FakeCrossEncoder()

    monkeypatch.setattr("hakari_bench.models.load_model", fake_load)
    config = ModelLoadConfig(
        model_name_or_path="mixedbread-ai/mxbai-rerank-base-v2",
        model_type="reranker",
        model_revision="a" * 40,
        dtype="bf16",
        device="cuda:0",
        attn_implementation="flash_attention_2",
        model_loader="hakari_bench.model_loaders:load_mxbai_rerank_v2",
        model_loader_kwargs={"max_batch_tokens": 8000},
    )
    model = load_mxbai_rerank_v2(config)
    assert model.max_batch_tokens == 8000
    assert configs[0].model_loader is None
    assert configs[0].model_loader_kwargs is None
    for field in ["model_revision", "dtype", "device", "attn_implementation"]:
        assert getattr(configs[0], field) == getattr(config, field)


def test_loader_rejects_wrong_method_and_unknown_options():
    with pytest.raises(ValueError, match="reranker evaluation only"):
        load_mxbai_rerank_v2(ModelLoadConfig(model_name_or_path="unused"))
    with pytest.raises(ValueError, match="Unsupported"):
        load_mxbai_rerank_v2(ModelLoadConfig(model_name_or_path="unused", model_type="reranker", model_loader_kwargs={"unknown": 1}))
