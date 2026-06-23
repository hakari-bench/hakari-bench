from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from html import escape
from pathlib import Path
import re
from urllib.parse import quote, urlparse

from pydantic import ValidationError

from hakari_bench.task_docs import TaskMetadata, load_task_metadata


HAKARI_BENCH_PAPER_TITLE = (
    "HAKARI-Bench: A Lightweight Benchmark for Comparing Retrieval Architectures "
    "and Efficiency Settings under Unified Conditions"
)
HAKARI_BENCH_PAPER_URL = "http://arxiv.org/abs/2606.22778"


@dataclass(frozen=True)
class BenchmarkDoc:
    title: str
    description: str
    url: str
    markdown: str


@dataclass(frozen=True)
class DocsPageChrome:
    """Shared head/header assets so documentation pages match the leaderboard.

    ``header_html`` is a pre-rendered, trusted HTML fragment built by the app;
    the URL fields already include cache-busting query strings. ``viewer_js_url``
    loads the shared script that applies the stored theme and binds the toggle.
    """

    css_url: str
    viewer_js_url: str
    favicon_svg_url: str
    favicon_png_url: str
    header_html: str


class BenchmarkDocs:
    def __init__(self, docs_dir: Path, *, metadata_dir: Path | None = None) -> None:
        self.docs_dir = docs_dir
        self.metadata_dir = metadata_dir

    def group_docs(self) -> list[BenchmarkDoc]:
        if not self.docs_dir.is_dir():
            return []
        docs: list[BenchmarkDoc] = []
        for path in sorted(self.docs_dir.glob("*/index.md")):
            if not _is_relative_to(path, self.docs_dir):
                continue
            doc = self._doc_from_path(path, url_parts=(path.parent.name,))
            if doc is not None:
                docs.append(doc)
        return sorted(docs, key=lambda doc: doc.title.lower())

    def group_doc(self, view_name: str) -> BenchmarkDoc | None:
        return self._doc_from_path(self.docs_dir / _safe_segment(view_name) / "index.md", url_parts=(view_name,))

    def task_doc(self, *, view_name: str, metric_column: str) -> BenchmarkDoc | None:
        path = self._task_doc_path(view_name=view_name, metric_column=metric_column)
        if path is None:
            return None
        return self._doc_from_path(path, url_parts=(path.parent.name, path.stem))

    def route_doc(self, *, benchmark: str, task: str | None = None) -> BenchmarkDoc | None:
        benchmark_segment = _safe_segment(benchmark)
        if task is None:
            return self._doc_from_path(self.docs_dir / benchmark_segment / "index.md", url_parts=(benchmark_segment,))
        task_segment = _safe_segment(task)
        return self._doc_from_path(self.docs_dir / benchmark_segment / f"{task_segment}.md", url_parts=(benchmark_segment, task_segment))

    def _task_doc_path(self, *, view_name: str, metric_column: str) -> Path | None:
        benchmark = _safe_segment(view_name)
        parts = metric_column.split("::")
        candidates: list[str] = []
        if len(parts) >= 3:
            benchmark = _safe_segment(parts[0] or view_name)
            dataset = _safe_segment(parts[-2].rsplit("/", 1)[-1])
            task = _safe_segment(parts[-1])
            candidates.extend([f"{dataset}__{task}", task])
        elif len(parts) == 2:
            benchmark = _safe_segment(parts[0] or view_name)
            candidates.append(_safe_segment(parts[1]))
        else:
            candidates.append(_safe_segment(metric_column))
        for candidate in candidates:
            path = self._matching_task_doc_path(benchmark=benchmark, candidate=candidate)
            if path is not None:
                return path
        return None

    def _matching_task_doc_path(self, *, benchmark: str, candidate: str) -> Path | None:
        benchmark_dir = self.docs_dir / benchmark
        exact_path = benchmark_dir / f"{candidate}.md"
        if exact_path.is_file():
            return exact_path
        if not benchmark_dir.is_dir():
            return None
        candidate_dataset, candidate_task = _split_dataset_task_stem(candidate)
        candidate_task_key = _normalize_doc_key(candidate_task)
        candidate_task_keys = {candidate_task_key, _normalize_doc_key(f"Nano{candidate_task}")}
        candidate_dataset_key = _normalize_doc_key(candidate_dataset)
        for path in sorted(benchmark_dir.glob("*.md")):
            if path.name == "index.md":
                continue
            doc_dataset, doc_task = _split_dataset_task_stem(path.stem)
            if candidate_dataset_key and _normalize_doc_key(doc_dataset) != candidate_dataset_key:
                continue
            if _normalize_doc_key(doc_task) in candidate_task_keys:
                return path
        return None

    def _doc_from_path(self, path: Path, *, url_parts: tuple[str, ...]) -> BenchmarkDoc | None:
        if not _is_relative_to(path, self.docs_dir) or not path.is_file():
            return None
        markdown = _read_markdown(path)
        markdown = self._markdown_with_metadata(path=path, markdown=markdown)
        return BenchmarkDoc(
            title=_extract_title(markdown) or path.stem,
            description=_extract_overview(markdown),
            url=_doc_url(url_parts),
            markdown=markdown,
        )

    def _markdown_with_metadata(self, *, path: Path, markdown: str) -> str:
        if self.metadata_dir is None:
            return markdown
        if path.name == "index.md":
            task_metadata = self._group_task_metadata(path.parent)
            if not task_metadata or "## Metadata Summary" in markdown:
                return markdown
            return f"{markdown.rstrip()}\n\n{_render_group_metadata_markdown(group_dir=path.parent, task_metadata=task_metadata)}\n"
        metadata = self._load_metadata(path)
        if metadata is None or "## Dataset Information" in markdown:
            return markdown
        rendered = markdown.rstrip()
        examples = _examples_markdown(metadata)
        if examples and "## Example Data" not in markdown:
            rendered = f"{rendered}\n\n{examples}"
        return f"{rendered}\n\n{_render_task_metadata_markdown(metadata)}\n"

    def _group_task_metadata(self, group_dir: Path) -> list[tuple[Path, TaskMetadata]]:
        items: list[tuple[Path, TaskMetadata]] = []
        for path in sorted(group_dir.glob("*.md")):
            if path.name == "index.md":
                continue
            metadata = self._load_metadata(path)
            if metadata is not None:
                items.append((path, metadata))
        return items

    def _load_metadata(self, path: Path) -> TaskMetadata | None:
        if self.metadata_dir is None:
            return None
        try:
            return load_task_metadata(path, docs_root=self.docs_dir, metadata_root=self.metadata_dir)
        except (OSError, ValidationError, ValueError):
            return None


def _render_docs_document(*, chrome: DocsPageChrome, title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="{chrome.css_url}">
  <link rel="icon" type="image/svg+xml" href="{chrome.favicon_svg_url}">
  <link rel="icon" type="image/png" href="{chrome.favicon_png_url}">
  <script src="{chrome.viewer_js_url}" defer></script>
</head>
<body class="bg-zinc-50 text-zinc-950">
  <main class="mx-auto max-w-4xl px-4 py-6 sm:px-6">
    {chrome.header_html}
    {body_html}
  </main>
</body>
</html>"""


def render_markdown_page(*, doc: BenchmarkDoc, chrome: DocsPageChrome) -> str:
    breadcrumb = _render_doc_breadcrumb(doc.url)
    body = f"""{breadcrumb}
    <article class="benchmark-doc border border-zinc-200 bg-white px-5 py-6 sm:px-7">
      {render_markdown_to_html(doc.markdown, base_url=doc.url)}
    </article>"""
    return _render_docs_document(chrome=chrome, title=f"{doc.title} - HAKARI-Bench docs", body_html=body)


def render_docs_index_page(*, docs: list[BenchmarkDoc], chrome: DocsPageChrome) -> str:
    items = "\n".join(
        f"""<li class="doc-card px-4 py-3.5">
          <a class="doc-card-link doc-card-title font-semibold underline-offset-2 hover:underline" href="{escape(doc.url, quote=True)}">{escape(doc.title)}</a>
          <p class="doc-card-description mt-1.5 text-sm leading-snug">{escape(doc.description)}</p>
        </li>"""
        for doc in docs
    )
    body = f"""<nav class="doc-breadcrumb mb-3 text-sm text-zinc-600" aria-label="Breadcrumb">
      <ol class="flex flex-wrap items-center gap-y-1">
        <li><a class="underline underline-offset-2" href="/">Top</a></li>
        <li><span class="px-1 text-zinc-400" aria-hidden="true">&gt;</span></li>
        <li><span aria-current="page">Benchmark documentation</span></li>
      </ol>
    </nav>
    <section class="mb-4">
      <h2 class="text-lg font-semibold text-zinc-950">Paper</h2>
      <p class="mt-1 text-sm text-zinc-600">
        <a class="underline underline-offset-2" href="{escape(HAKARI_BENCH_PAPER_URL, quote=True)}">{escape(HAKARI_BENCH_PAPER_TITLE)}</a>
      </p>
    </section>
    <header class="mb-4">
      <h1 class="text-lg font-semibold text-zinc-950">Benchmark documentation</h1>
      <p class="mt-1 text-sm text-zinc-600">Dataset and benchmark task group descriptions used by the leaderboard viewer.</p>
    </header>
    <ul class="doc-card-grid">
      {items}
    </ul>"""
    return _render_docs_document(chrome=chrome, title="Benchmark documentation - HAKARI-Bench docs", body_html=body)


def _render_task_metadata_markdown(metadata: TaskMetadata) -> str:
    rows = [
        ("Nano set", metadata.nano_set),
        ("Backing dataset", metadata.backing_dataset),
        ("Task / split", _task_split_label(metadata)),
        ("Hugging Face dataset", _dataset_link(metadata)),
        ("Language", metadata.language),
        ("Category", metadata.category),
        ("Queries", _format_int(metadata.counts.queries)),
        ("Documents", _format_int(metadata.counts.documents)),
        ("Positive qrels", _format_int(metadata.counts.positive_qrels)),
        ("Positives / query avg", _format_float(metadata.positives_per_query.average)),
        ("Positives / query min", _format_int(metadata.positives_per_query.min)),
        ("Positives / query median", _format_float(metadata.positives_per_query.median)),
        ("Positives / query max", _format_int(metadata.positives_per_query.max)),
        ("Multi-positive queries", _multi_positive_label(metadata)),
        ("Query length avg chars", _format_float(metadata.text_stats_chars.query_mean)),
        ("Document length avg chars", _format_float(metadata.text_stats_chars.document_mean)),
    ]
    info_table = _markdown_table(["Field", "Value"], [[label, value] for label, value in rows if value])
    sections = [
        "## Dataset Information",
        "",
        info_table,
    ]
    candidate_table = _candidate_subsets_table(metadata)
    if candidate_table:
        sections.extend(["", "### Candidate Subsets", "", candidate_table])
    learning = _learning_markdown(metadata)
    if learning:
        sections.extend(["", "### Training and Leakage Metadata", "", learning])
    links = _links_markdown(metadata)
    if links:
        sections.extend(["", "### Hugging Face Links", "", links])
    references = _references_table(metadata)
    if references:
        sections.extend(["", "### Source Reference Table", "", references])
    return "\n".join(sections)


def _render_group_metadata_markdown(*, group_dir: Path, task_metadata: list[tuple[Path, TaskMetadata]]) -> str:
    metadata = [item for _, item in task_metadata]
    languages = sorted({item.language for item in metadata})
    categories = sorted({item.category for item in metadata})
    query_count = sum(item.counts.queries for item in metadata)
    document_count = sum(item.counts.documents for item in metadata)
    positive_count = sum(item.counts.positive_qrels for item in metadata)
    overview_table = _markdown_table(
        ["Field", "Value"],
        [
            ["Task pages", _format_int(len(metadata))],
            ["Queries", _format_int(query_count)],
            ["Split-local documents", _format_int(document_count)],
            ["Positive qrels", _format_int(positive_count)],
            ["Languages", ", ".join(languages)],
            ["Categories", ", ".join(categories)],
            ["Positives / query avg", _format_float(positive_count / query_count) if query_count else ""],
        ],
    )
    task_rows = []
    for path, item in sorted(task_metadata, key=lambda entry: (entry[1].task_name.lower(), entry[0].name.lower())):
        scores = _profile_scores(item)
        task_rows.append(
            [
                f"[{item.task_name}]({path.relative_to(group_dir).as_posix()})",
                item.backing_dataset,
                item.language,
                item.category,
                _format_int(item.counts.queries),
                _format_int(item.counts.documents),
                _format_int(item.counts.positive_qrels),
                _format_optional_score(scores.get("BM25")),
                _format_optional_score(scores.get("Dense")),
                _format_optional_score(scores.get("Reranking hybrid")),
                _best_profile_label(scores),
            ]
        )
    task_table = _markdown_table(
        [
            "Task",
            "Backing dataset",
            "Lang",
            "Category",
            "Queries",
            "Docs",
            "Positives",
            "BM25 nDCG@10",
            "Dense nDCG@10",
            "Reranking hybrid nDCG@10",
            "Best profile",
        ],
        task_rows,
    )
    return "\n".join(
        [
            "## Metadata Summary",
            "",
            overview_table,
            "",
            "### Task Metadata Summary",
            "",
            task_table,
        ]
    )


def _task_split_label(metadata: TaskMetadata) -> str:
    if metadata.task_name == metadata.split_name:
        return metadata.task_name
    return f"{metadata.task_name} / {metadata.split_name}"


def _dataset_link(metadata: TaskMetadata) -> str:
    url = metadata.links.nano_dataset if metadata.links is not None else f"https://huggingface.co/datasets/{metadata.dataset_id}"
    return f"[{metadata.dataset_id}]({url})"


def _multi_positive_label(metadata: TaskMetadata) -> str:
    value = _format_int(metadata.positives_per_query.multi_positive_queries)
    percent = metadata.positives_per_query.multi_positive_query_percent
    if percent is None:
        return value
    return f"{value} ({_format_float(percent)}%)"


def _candidate_subsets_table(metadata: TaskMetadata) -> str:
    subsets = metadata.candidate_subsets
    rows: list[list[str]] = []
    for key in ("bm25", "dense", "reranking_hybrid"):
        subset = getattr(subsets, key) if subsets is not None else None
        if subset is None:
            continue
        rows.append(
            [
                subset.label,
                f"`{subset.config}`",
                _format_score(subset.ndcg_at_10),
                _format_score(subset.hit_at_10),
                _format_score(subset.recall_at_100),
                f"top-{_format_int(subset.top_k)}",
            ]
        )
    if not rows and metadata.bm25 is not None:
        rows.append(["BM25", "`bm25`", _format_score(metadata.bm25.ndcg_at_10), _format_score(metadata.bm25.hit_at_10), "", ""])
    return _markdown_table(["Profile", "Config", "nDCG@10", "Hit@10", "Recall@100", "Candidates"], rows) if rows else ""


def _examples_markdown(metadata: TaskMetadata) -> str:
    if not metadata.examples:
        return ""
    rows = [
        [
            _format_example_text(example.query.text, example.query.full_chars, example.query.limit_chars, example.query.truncated),
            _format_example_text(
                example.positive_document.text,
                example.positive_document.full_chars,
                example.positive_document.limit_chars,
                example.positive_document.truncated,
            ),
        ]
        for example in metadata.examples
    ]
    return "\n".join(["## Example Data", "", _markdown_table(["Query", "Positive document"], rows)])


def _format_example_text(text: str, full_chars: int, limit_chars: int, truncated: bool) -> str:
    if truncated:
        return f"{text}... [{_format_int(limit_chars)} / {_format_int(full_chars)} chars]"
    return f"{text} [{_format_int(full_chars)} chars]"


def _profile_scores(metadata: TaskMetadata) -> dict[str, float]:
    subsets = metadata.candidate_subsets
    if subsets is None:
        return {"BM25": metadata.bm25.ndcg_at_10}
    scores: dict[str, float] = {}
    for key in ("bm25", "dense", "reranking_hybrid"):
        subset = getattr(subsets, key)
        if subset is not None:
            scores[subset.label] = subset.ndcg_at_10
    if "BM25" not in scores:
        scores["BM25"] = metadata.bm25.ndcg_at_10
    return scores


def _best_profile_label(scores: dict[str, float]) -> str:
    if not scores:
        return ""
    return max(scores.items(), key=lambda item: item[1])[0]


def _learning_markdown(metadata: TaskMetadata) -> str:
    learning = metadata.learning
    if learning is None:
        return ""
    rows = [
        ("Original train split", learning.original_train_split),
        ("Evaluation split origin", learning.evaluation_split_origin),
        ("Train/eval overlap audit", learning.train_eval_overlap_audit),
        ("Leakage note", learning.leakage_note),
        ("Multi-positive training", learning.multi_positive_training),
    ]
    lines = [f"- {label}: {value}" for label, value in rows if value]
    if learning.useful_training_data:
        lines.append(f"- Useful training data: {', '.join(learning.useful_training_data)}")
    return "\n".join(lines)


def _links_markdown(metadata: TaskMetadata) -> str:
    if metadata.links is None:
        return f"- Nano dataset: [{metadata.dataset_id}](https://huggingface.co/datasets/{metadata.dataset_id})"
    lines = [f"- Nano dataset: [{metadata.dataset_id}]({metadata.links.nano_dataset})"]
    lines.extend(f"- {item.label}: [{item.url}]({item.url})" for item in metadata.links.source_urls)
    return "\n".join(lines)


def _references_table(metadata: TaskMetadata) -> str:
    if not metadata.references:
        return ""
    rows = [
        [
            reference.title,
            str(reference.year) if reference.year is not None else "",
            "paper" if reference.is_paper else "dataset page",
            f"[{reference.url}]({reference.url})",
        ]
        for reference in metadata.references
    ]
    return _markdown_table(["Title", "Year", "Type", "URL"], rows)


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return ""
    alignments = ["---"] * len(headers)
    lines = [
        "| " + " | ".join(_escape_table_cell(header) for header in headers) + " |",
        "| " + " | ".join(alignments) + " |",
    ]
    for row in rows:
        padded = [*row, *([""] * (len(headers) - len(row)))]
        lines.append("| " + " | ".join(_escape_table_cell(cell) for cell in padded[: len(headers)]) + " |")
    return "\n".join(lines)


def _escape_table_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _format_int(value: int) -> str:
    return f"{value:,}"


def _format_float(value: float) -> str:
    return f"{value:,.2f}"


def _format_score(value: float) -> str:
    return f"{value:.4f}"


def _format_optional_score(value: float | None) -> str:
    return "" if value is None else _format_score(value)


def render_markdown_to_html(markdown: str, *, base_url: str = "") -> str:
    lines = markdown.splitlines()
    html: list[str] = []
    paragraph: list[str] = []
    in_list = False
    in_code = False
    code_lines: list[str] = []
    in_table = False
    details_level: int | None = None

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            html.append(f"<p>{_inline_markdown(' '.join(line.strip() for line in paragraph), base_url=base_url)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            html.append("</ul>")
            in_list = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            html.append("</tbody></table></div>")
            in_table = False

    def close_details() -> None:
        nonlocal details_level
        if details_level is not None:
            html.append("</details>")
            details_level = None

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                html.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                close_list()
                close_table()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            flush_paragraph()
            close_list()
            close_table()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            close_list()
            close_table()
            level = len(heading.group(1))
            heading_text = heading.group(2).strip()
            if details_level is not None and level <= details_level:
                close_details()
            if heading_text.lower() == "machine-readable metadata":
                html.append(
                    '<details class="machine-readable-metadata mt-6 border border-zinc-200 bg-zinc-50 px-3 py-2">'
                    '<summary class="cursor-pointer text-sm font-semibold text-zinc-800">'
                    f"{_inline_markdown(heading_text, base_url=base_url)}"
                    "</summary>"
                )
                details_level = level
                continue
            html.append(f"<h{level}>{_inline_markdown(heading_text, base_url=base_url)}</h{level}>")
            continue
        if line.startswith(">"):
            flush_paragraph()
            close_list()
            close_table()
            html.append(f"<blockquote>{_inline_markdown(line.lstrip('> ').strip(), base_url=base_url)}</blockquote>")
            continue
        if line.startswith("- "):
            flush_paragraph()
            close_table()
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{_inline_markdown(line[2:].strip(), base_url=base_url)}</li>")
            continue
        if _is_table_row(line):
            flush_paragraph()
            close_list()
            if _is_table_separator(line):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            row_html = "".join(f"<td>{_inline_markdown(cell, base_url=base_url)}</td>" for cell in cells)
            if not in_table:
                html.append('<div class="overflow-x-auto"><table><tbody>')
                in_table = True
            html.append(f"<tr>{row_html}</tr>")
            continue
        close_table()
        paragraph.append(line)
    flush_paragraph()
    close_list()
    close_table()
    if in_code:
        html.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
    close_details()
    return "\n".join(html)


def _render_doc_breadcrumb(url: str) -> str:
    parts = _doc_url_parts(url)
    if not parts:
        return ""
    crumbs = [
        '<a class="underline underline-offset-2" href="/">Top</a>',
        '<a class="underline underline-offset-2" href="/docs/benchmark-tasks">Benchmark documentation</a>',
    ]
    if len(parts) == 1:
        crumbs.append(f'<span aria-current="page">{escape(parts[0])}</span>')
    else:
        group = parts[0]
        crumbs.append(f'<a class="underline underline-offset-2" href="/docs/benchmark-tasks/{quote(group, safe="")}">{escape(group)}</a>')
        crumbs.append(f'<span aria-current="page">{escape(parts[-1])}</span>')
    separator = '<span class="px-1 text-zinc-400" aria-hidden="true">&gt;</span>'
    return f"""<nav class="doc-breadcrumb mb-3 text-sm text-zinc-600" aria-label="Breadcrumb">
      <ol class="flex flex-wrap items-center gap-y-1">
        <li>{f'</li><li>{separator}</li><li>'.join(crumbs)}</li>
      </ol>
    </nav>"""


def _doc_url_parts(url: str) -> list[str]:
    prefix = "/docs/benchmark-tasks/"
    if not url.startswith(prefix):
        return []
    return [part for part in url[len(prefix) :].strip("/").split("/") if part]


def _read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@lru_cache(maxsize=1024)
def _extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


@lru_cache(maxsize=1024)
def _extract_overview(markdown: str) -> str:
    lines = markdown.splitlines()
    overview: list[str] = []
    in_overview = False
    for line in lines:
        if line.startswith("## "):
            if in_overview:
                break
            in_overview = line.strip().lower() == "## overview"
            continue
        if in_overview:
            if line.startswith("#"):
                break
            if line.startswith(">"):
                continue
            overview.append(line)
    text = _plain_markdown("\n".join(overview)).strip()
    return re.sub(r"\s+", " ", text)


def _plain_markdown(markdown: str) -> str:
    text = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_#>|-]", " ", text)
    return text


def _inline_markdown(text: str, *, base_url: str = "") -> str:
    code_tokens: dict[str, str] = {}

    def code_replacement(match: re.Match[str]) -> str:
        token = f"\x00CODE{len(code_tokens)}\x00"
        code_tokens[token] = f"<code>{escape(match.group(1))}</code>"
        return token

    text_without_code = re.sub(r"`([^`]+)`", code_replacement, text)
    escaped = escape(text_without_code)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda match: _link_replacement(match, base_url=base_url), escaped)
    escaped = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", escaped)
    for token, code_html in code_tokens.items():
        escaped = escaped.replace(token, code_html)
    return escaped


def _link_replacement(match: re.Match[str], *, base_url: str = "") -> str:
    label = match.group(1)
    url = match.group(2)
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label}</a>'
    local_href = _local_doc_href(url, base_url=base_url)
    if local_href is None:
        return label
    return f'<a href="{escape(local_href, quote=True)}">{label}</a>'


def _local_doc_href(url: str, *, base_url: str) -> str | None:
    if not base_url:
        return None
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or parsed.query:
        return None
    path = parsed.path
    if "\\" in path or path.startswith("/"):
        return None
    parts = path.split("/")
    if len(parts) != 1 or parts[0] in {"", ".", ".."}:
        return None
    filename = parts[0]
    if not filename.endswith(".md"):
        return None
    stem = filename[:-3]
    if not stem or _safe_segment(stem) != stem:
        return None
    href = f"{base_url.rstrip('/')}/{quote(stem, safe='')}"
    if parsed.fragment:
        href = f"{href}#{quote(parsed.fragment, safe='-_.:')}"
    return href


def _is_table_row(line: str) -> bool:
    return line.startswith("|") and line.endswith("|") and "|" in line[1:-1]


def _is_table_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|", line))


def _safe_segment(value: str) -> str:
    segment = value.strip().strip("/").replace("/", "__")
    return re.sub(r"[^A-Za-z0-9_.:-]", "_", segment)


def _split_dataset_task_stem(stem: str) -> tuple[str, str]:
    if "__" not in stem:
        return "", stem
    dataset, task = stem.rsplit("__", 1)
    return dataset, task


def _normalize_doc_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _doc_url(parts: tuple[str, ...]) -> str:
    encoded = "/".join(quote(_safe_segment(part), safe="") for part in parts)
    return f"/docs/benchmark-tasks/{encoded}"


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True
