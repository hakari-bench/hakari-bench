from __future__ import annotations

import argparse
import json
import math
import re
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
import yaml

CONFIG_ORDER = ("corpus", "queries", "qrels", "bm25", "harrier_oss_v1_270m", "reranking_hybrid")
HARRIER_CONFIG = "harrier_oss_v1_270m"
HARRIER_MODEL_ID = "microsoft/harrier-oss-v1-270m"
HYBRID_CONFIG = "reranking_hybrid"
HAKARI_LINK = "[HAKARI-bench](https://github.com/hakari-bench/hakari-bench)"
DEFAULT_TAGS = [
    "information-retrieval",
    "retrieval",
    "nano",
    "bm25",
    "dense-retrieval",
    "reranking",
    "hakari-bench",
]
NANOBEIR_ORIGINAL_SOURCE_DATASETS = {
    "NanoBEIR-ar": "lightonai/NanoBEIR-ar",
    "NanoBEIR-de": "lightonai/NanoBEIR-de",
    "NanoBEIR-en": "sentence-transformers/NanoBEIR-en",
    "NanoBEIR-es": "lightonai/NanoBEIR-es",
    "NanoBEIR-fr": "lightonai/NanoBEIR-fr",
    "NanoBEIR-it": "lightonai/NanoBEIR-it",
    "NanoBEIR-ja": "LiquidAI/NanoBEIR-ja",
    "NanoBEIR-ko": "LiquidAI/NanoBEIR-ko",
    "NanoBEIR-no": "lightonai/NanoBEIR-no",
    "NanoBEIR-pt": "lightonai/NanoBEIR-pt",
    "NanoBEIR-sr": "Serbian-AI-Society/NanoBEIR-sr",
    "NanoBEIR-sv": "lightonai/NanoBEIR-sv",
    "NanoBEIR-th": "sionic-ai/NanoBEIR-th",
    "NanoBEIR-vi": "sionic-ai/NanoBEIR-vi",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Update local reranking_hybrid Nano dataset README files.")
    parser.add_argument("--output-root", type=Path, default=Path("output/nano_reranking_hybrid_20260525"))
    parser.add_argument("--offline", action="store_true", help="Do not fetch remote Hugging Face README files.")
    args = parser.parse_args()

    updated = update_all_readmes(output_root=args.output_root, fetch_remote=not args.offline)
    print(f"updated {updated} README files under {args.output_root}")


def update_all_readmes(*, output_root: Path, fetch_remote: bool = True) -> int:
    count = 0
    for dataset_dir in sorted(path for path in output_root.iterdir() if path.is_dir()):
        metadata_path = dataset_dir / "reranking_hybrid_metadata.json"
        if not metadata_path.exists():
            continue
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        source_dataset = str(metadata.get("source_dataset") or f"hakari-bench/{dataset_dir.name}")
        remote_readme = fetch_remote_readme(source_dataset) if fetch_remote else None
        readme = render_readme(dataset_dir=dataset_dir, dataset_name=dataset_dir.name, metadata=metadata, remote_readme=remote_readme)
        (dataset_dir / "README.md").write_text(readme, encoding="utf-8")
        count += 1
    return count


def fetch_remote_readme(repo_id: str) -> str | None:
    try:
        from huggingface_hub import hf_hub_download

        path = hf_hub_download(repo_id=repo_id, repo_type="dataset", filename="README.md")
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return None


def render_readme(
    *,
    dataset_dir: Path,
    dataset_name: str,
    metadata: Mapping[str, Any],
    remote_readme: str | None,
) -> str:
    splits = sorted(str(split) for split in metadata.get("splits", {}))
    remote = parse_remote_readme(remote_readme or "")
    source_dataset = str(metadata.get("source_dataset") or f"hakari-bench/{dataset_name}")
    frontmatter = render_frontmatter(dataset_dir=dataset_dir, splits=splits, remote_frontmatter=remote.frontmatter)
    source_links = source_links_for_dataset(
        dataset_name=dataset_name,
        source_dataset=source_dataset,
        remote_source_links=remote.source_links,
    )
    overview = remote.overview or f"{dataset_name} is a Nano-style retrieval dataset."
    overview = normalize_hakari_link(overview)
    rows = [split_summary(dataset_dir=dataset_dir, split=split, split_metadata=metadata["splits"][split]) for split in splits]
    split_stat_rows = "\n".join(render_split_statistics_row(row) for row in rows)
    quality_rows = "\n".join(render_candidate_quality_row(row) for row in rows)
    mean_row = render_candidate_quality_mean_row(rows)
    safeguard_total = sum(row.safeguard_positive_count for row in rows)
    limited_total = sum(row.limited_by_corpus_size_count for row in rows)
    license_text = remote.license_text or (
        f"{dataset_name} is a derived dataset. Users must comply with the licenses, terms, "
        "and attribution requirements of the upstream source datasets."
    )

    readme = f"""---
{frontmatter}---

# {dataset_name}

This dataset is a Nano-style retrieval dataset for {HAKARI_LINK}.

{overview}

## Usage

```python
from datasets import load_dataset

dataset_id = "{source_dataset}"
split = "{splits[0] if splits else 'SPLIT_NAME'}"

queries = load_dataset(dataset_id, "queries", split=split)
corpus = load_dataset(dataset_id, "corpus", split=split)
qrels = load_dataset(dataset_id, "qrels", split=split)
reranking_candidates = load_dataset(dataset_id, "reranking_hybrid", split=split)
```

## Data Layout

This dataset uses six Hugging Face Datasets configs:

- `corpus`: documents with `_id` and `text`
- `queries`: queries with `_id` and `text`
- `qrels`: positive relevance labels with `query-id` and `corpus-id`
- `bm25`: BM25 candidate lists with `query-id` and `corpus-ids`
- `harrier_oss_v1_270m`: dense candidate lists from `{HARRIER_MODEL_ID}`
- `reranking_hybrid`: RRF candidate lists built from `bm25` and `harrier_oss_v1_270m`

Each config has the same Nano split names.

## Candidate Construction

- `bm25`: local BM25 top-500 with automatic language-aware tokenization. The resolved tokenizer is shown in the Candidate Quality table, for example `wordseg@ja`.
- `harrier_oss_v1_270m`: dense top-500 from `{HARRIER_MODEL_ID}`. In tables this is shown as `Dense`; Dense means `{HARRIER_MODEL_ID}` with the `web_search_query` prompt for queries and cosine similarity over normalized embeddings.
- `reranking_hybrid`: RRF over `bm25` and `harrier_oss_v1_270m` using `rrf_k=100`, keeping the RRF top-100.

Safeguard means rank 101 is appended only when RRF top-100 contains no qrels-positive document.

## Split Statistics

Length statistics are character counts computed with `len(str(text))`.

| Nano split | Queries | Corpus | Qrels | Query chars avg | Query chars p50 | Query chars p75 | Doc chars avg | Doc chars p50 | Doc chars p75 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{split_stat_rows}

## Candidate Quality

`nDCG@10` and `Recall@100` are computed from the included candidate rankings against the included qrels, then reported as 0-100 scores such as `52.45`. `Recall@100` uses only the top 100 candidates; an optional rank-101 safeguard positive is not counted in `Recall@100`.

Dense means `{HARRIER_MODEL_ID}` with the `web_search_query` prompt and cosine similarity.

| Nano split | BM25 tokenizer | BM25 nDCG@10 | Dense nDCG@10 | Hybrid nDCG@10 | BM25 Recall@100 | Dense Recall@100 | Hybrid Recall@100 | Hybrid candidates | Safeguard positives |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{mean_row}
{quality_rows}

## Hybrid Safeguard Summary

- Safeguard positives: {safeguard_total}
- Rows limited by corpus size: {limited_total}
- Metadata file: `reranking_hybrid_metadata.json`

## Source Links

{chr(10).join(source_links)}

## License

{license_text}
"""
    return normalize_hakari_link(readme)


def source_links_for_dataset(
    *,
    dataset_name: str,
    source_dataset: str,
    remote_source_links: Sequence[str],
) -> list[str]:
    original_dataset = NANOBEIR_ORIGINAL_SOURCE_DATASETS.get(dataset_name)
    if original_dataset is None:
        return list(remote_source_links) or [dataset_link_line(source_dataset)]

    links: list[str] = []
    original_line = dataset_link_line(original_dataset, label="Original dataset")
    if not any(original_dataset in line for line in remote_source_links):
        links.append(original_line)
    for line in remote_source_links:
        if source_dataset in line and original_dataset not in line:
            continue
        if line not in links:
            links.append(line)
    final_line = dataset_link_line(source_dataset, label="Final dataset")
    if not any(source_dataset in line for line in links):
        links.append(final_line)
    return links


def dataset_link_line(dataset_id: str, *, label: str | None = None) -> str:
    prefix = f"{label}: " if label else ""
    return f"- {prefix}[{dataset_id}](https://huggingface.co/datasets/{dataset_id})"


def render_frontmatter(*, dataset_dir: Path, splits: Sequence[str], remote_frontmatter: Mapping[str, Any]) -> str:
    configs: list[dict[str, Any]] = []
    for config in CONFIG_ORDER:
        existing_splits = [split for split in splits if (dataset_dir / config / f"{split}.parquet").exists()]
        if not existing_splits:
            continue
        item: dict[str, Any] = {
            "config_name": config,
            "data_files": [{"split": split, "path": f"{config}/{split}.parquet"} for split in existing_splits],
        }
        if config == "queries":
            item["default"] = True
        configs.append(item)
    frontmatter: dict[str, Any] = {"configs": configs}
    languages = remote_frontmatter.get("language")
    if languages:
        frontmatter["language"] = languages
    tags = list(remote_frontmatter.get("tags") or [])
    for tag in DEFAULT_TAGS:
        if tag not in tags:
            tags.append(tag)
    frontmatter["tags"] = tags
    return yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)


class RemoteReadme:
    def __init__(
        self,
        *,
        frontmatter: Mapping[str, Any],
        overview: str,
        source_links: list[str],
        license_text: str,
    ) -> None:
        self.frontmatter = frontmatter
        self.overview = overview
        self.source_links = source_links
        self.license_text = license_text


def parse_remote_readme(text: str) -> RemoteReadme:
    frontmatter: Mapping[str, Any] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", maxsplit=2)
        if len(parts) == 3:
            parsed = yaml.safe_load(parts[1]) or {}
            frontmatter = parsed if isinstance(parsed, dict) else {}
            body = parts[2]
    return RemoteReadme(
        frontmatter=frontmatter,
        overview=extract_overview(body),
        source_links=extract_list_section(body, "Source Links"),
        license_text=extract_text_section(body, "License"),
    )


def extract_overview(body: str) -> str:
    lines = [line.strip() for line in body.strip().splitlines()]
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.startswith("## "):
            break
        if line.startswith("#"):
            continue
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))
    filtered = [paragraph for paragraph in paragraphs if not is_generic_remote_overview_paragraph(paragraph)]
    return "\n\n".join(filtered[:2])


def is_generic_remote_overview_paragraph(paragraph: str) -> bool:
    checks = [
        "This dataset is a Nano-style retrieval dataset.",
        "Nano-series evaluation can be run easily",
        "HAKARI-Bench",
        "HAKARI-bench",
        "Hugging Face Datasets layout convention",
        "BM25 candidates are provided separately",
        "This is a private regenerated Nano-style retrieval dataset",
    ]
    return any(check in paragraph for check in checks)


def extract_list_section(body: str, heading: str) -> list[str]:
    section = extract_text_section(body, heading)
    return [line.strip() for line in section.splitlines() if line.strip().startswith("- ")]


def extract_text_section(body: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", body, flags=re.MULTILINE)
    if match is None:
        return ""
    start = match.end()
    next_heading = re.search(r"^## ", body[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading is not None else len(body)
    return body[start:end].strip()


def normalize_hakari_link(text: str) -> str:
    return (
        text.replace("[HAKARI-Bench](https://github.com/hotchpotch/hakari-bench)", HAKARI_LINK)
        .replace("https://github.com/hotchpotch/hakari-bench", "https://github.com/hakari-bench/hakari-bench")
        .replace("HAKARI-Bench", "HAKARI-bench")
    )


class SplitSummary:
    def __init__(
        self,
        *,
        split: str,
        queries: int,
        corpus: int,
        qrels: int,
        query_stats: Mapping[str, float],
        doc_stats: Mapping[str, float],
        tokenizer: str,
        bm25_ndcg: float,
        dense_ndcg: float,
        hybrid_ndcg: float,
        bm25_recall: float,
        dense_recall: float,
        hybrid_recall: float,
        hybrid_min: int,
        hybrid_max: int,
        safeguard_positive_count: int,
        limited_by_corpus_size_count: int,
    ) -> None:
        self.split = split
        self.queries = queries
        self.corpus = corpus
        self.qrels = qrels
        self.query_stats = query_stats
        self.doc_stats = doc_stats
        self.tokenizer = tokenizer
        self.bm25_ndcg = bm25_ndcg
        self.dense_ndcg = dense_ndcg
        self.hybrid_ndcg = hybrid_ndcg
        self.bm25_recall = bm25_recall
        self.dense_recall = dense_recall
        self.hybrid_recall = hybrid_recall
        self.hybrid_min = hybrid_min
        self.hybrid_max = hybrid_max
        self.safeguard_positive_count = safeguard_positive_count
        self.limited_by_corpus_size_count = limited_by_corpus_size_count


def split_summary(*, dataset_dir: Path, split: str, split_metadata: Mapping[str, Any]) -> SplitSummary:
    queries = read_parquet_rows(dataset_dir / "queries" / f"{split}.parquet")
    corpus = read_parquet_rows(dataset_dir / "corpus" / f"{split}.parquet")
    qrel_rows = read_parquet_rows(dataset_dir / "qrels" / f"{split}.parquet")
    qrels = qrels_by_query(qrel_rows)
    bm25 = rankings_by_query(read_parquet_rows(dataset_dir / "bm25" / f"{split}.parquet"))
    dense = rankings_by_query(read_parquet_rows(dataset_dir / HARRIER_CONFIG / f"{split}.parquet"))
    hybrid = rankings_by_query(read_parquet_rows(dataset_dir / HYBRID_CONFIG / f"{split}.parquet"))
    bm25_ndcg, bm25_recall = ranking_metrics(bm25, qrels)
    dense_ndcg, dense_recall = ranking_metrics(dense, qrels)
    hybrid_ndcg, hybrid_recall = ranking_metrics(hybrid, qrels)
    hybrid_lengths = sorted(len(ids) for ids in hybrid.values())
    hybrid_metadata = candidate_metadata(split_metadata, HYBRID_CONFIG)
    return SplitSummary(
        split=split,
        queries=len(queries),
        corpus=len(corpus),
        qrels=len(qrel_rows),
        query_stats=length_stats(row.get("text") for row in queries),
        doc_stats=length_stats(row.get("text") for row in corpus),
        tokenizer=bm25_tokenizer_label(candidate_metadata(split_metadata, "bm25")),
        bm25_ndcg=bm25_ndcg,
        dense_ndcg=dense_ndcg,
        hybrid_ndcg=hybrid_ndcg,
        bm25_recall=bm25_recall,
        dense_recall=dense_recall,
        hybrid_recall=hybrid_recall,
        hybrid_min=hybrid_lengths[0] if hybrid_lengths else 0,
        hybrid_max=hybrid_lengths[-1] if hybrid_lengths else 0,
        safeguard_positive_count=int(hybrid_metadata.get("safeguard_positive_count") or 0),
        limited_by_corpus_size_count=int(hybrid_metadata.get("limited_by_corpus_size_count") or 0),
    )


def candidate_metadata(split_metadata: Mapping[str, Any], config: str) -> Mapping[str, Any]:
    raw = split_metadata.get(config)
    return raw if isinstance(raw, dict) else {}


def bm25_tokenizer_label(metadata: Mapping[str, Any]) -> str:
    tokenizer = str(metadata.get("resolved_tokenizer") or "auto")
    language = metadata.get("auto_detected_language")
    stemmer = metadata.get("resolved_stemmer_algorithm")
    if tokenizer == "wordseg" and isinstance(language, str) and language:
        return f"wordseg@{language}"
    if tokenizer == "stemmer" and isinstance(stemmer, str) and stemmer:
        return f"stemmer@{stemmer}"
    return tokenizer


def read_parquet_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [dict(row) for row in pq.read_table(path).to_pylist()]


def qrels_by_query(rows: Iterable[Mapping[str, Any]]) -> dict[str, set[str]]:
    qrels: dict[str, set[str]] = {}
    for row in rows:
        query_id = str(row.get("query-id"))
        corpus_id = row.get("corpus-id")
        corpus_ids = row.get("corpus-ids")
        if isinstance(corpus_ids, list):
            qrels.setdefault(query_id, set()).update(str(item) for item in corpus_ids)
        elif corpus_id is not None:
            qrels.setdefault(query_id, set()).add(str(corpus_id))
    return qrels


def rankings_by_query(rows: Iterable[Mapping[str, Any]]) -> dict[str, list[str]]:
    rankings: dict[str, list[str]] = {}
    for row in rows:
        corpus_ids = row.get("corpus-ids")
        rankings[str(row.get("query-id"))] = [str(item) for item in corpus_ids] if isinstance(corpus_ids, list) else []
    return rankings


def ranking_metrics(
    rankings: Mapping[str, Sequence[str]],
    qrels: Mapping[str, set[str]],
    *,
    ndcg_k: int = 10,
    recall_k: int = 100,
) -> tuple[float, float]:
    ndcgs: list[float] = []
    recalls: list[float] = []
    for query_id, positives in qrels.items():
        if not positives:
            continue
        ranking = list(rankings.get(query_id, []))
        gains = [1.0 if corpus_id in positives else 0.0 for corpus_id in ranking[:ndcg_k]]
        ideal = [1.0] * min(len(positives), ndcg_k)
        idcg = dcg(ideal)
        ndcgs.append(dcg(gains) / idcg if idcg else 0.0)
        hits = sum(1 for corpus_id in ranking[:recall_k] if corpus_id in positives)
        recalls.append(hits / len(positives))
    if not ndcgs:
        return 0.0, 0.0
    return sum(ndcgs) / len(ndcgs), sum(recalls) / len(recalls)


def dcg(gains: Sequence[float]) -> float:
    return sum(gain / math.log2(index + 2) for index, gain in enumerate(gains))


def length_stats(values: Iterable[Any]) -> dict[str, float]:
    lengths = sorted(float(len(str(value))) for value in values if value is not None)
    if not lengths:
        return {"avg": 0.0, "p50": 0.0, "p75": 0.0}
    return {
        "avg": sum(lengths) / len(lengths),
        "p50": percentile(lengths, 0.50),
        "p75": percentile(lengths, 0.75),
    }


def percentile(sorted_values: Sequence[float], q: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def render_split_statistics_row(row: SplitSummary) -> str:
    return (
        f"| {row.split} | {row.queries} | {row.corpus} | {row.qrels} | "
        f"{row.query_stats['avg']:.1f} | {row.query_stats['p50']:.1f} | {row.query_stats['p75']:.1f} | "
        f"{row.doc_stats['avg']:.1f} | {row.doc_stats['p50']:.1f} | {row.doc_stats['p75']:.1f} |"
    )


def render_candidate_quality_row(row: SplitSummary) -> str:
    return (
        f"| {row.split} | {row.tokenizer} | "
        f"{score_100(row.bm25_ndcg)} | {score_100(row.dense_ndcg)} | {score_100(row.hybrid_ndcg)} | "
        f"{score_100(row.bm25_recall)} | {score_100(row.dense_recall)} | {score_100(row.hybrid_recall)} | "
        f"{candidate_range(row.hybrid_min, row.hybrid_max)} | {row.safeguard_positive_count} |"
    )


def render_candidate_quality_mean_row(rows: Sequence[SplitSummary]) -> str:
    if not rows:
        return "| Mean | - | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 |"

    def mean(attr: str) -> float:
        return sum(float(getattr(row, attr)) for row in rows) / len(rows)

    return (
        "| Mean | - | "
        f"{score_100(mean('bm25_ndcg'))} | {score_100(mean('dense_ndcg'))} | {score_100(mean('hybrid_ndcg'))} | "
        f"{score_100(mean('bm25_recall'))} | {score_100(mean('dense_recall'))} | {score_100(mean('hybrid_recall'))} | "
        f"- | {sum(row.safeguard_positive_count for row in rows)} |"
    )


def score_100(value: float) -> str:
    return f"{value * 100.0:.2f}"


def candidate_range(min_count: int, max_count: int) -> str:
    if min_count == max_count:
        return str(min_count)
    return f"{min_count}-{max_count}"


if __name__ == "__main__":
    main()
