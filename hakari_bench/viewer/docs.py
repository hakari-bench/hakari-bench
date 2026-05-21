from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from html import escape
from pathlib import Path
import re
from urllib.parse import quote, urlparse


@dataclass(frozen=True)
class BenchmarkDoc:
    title: str
    description: str
    url: str
    markdown: str


class BenchmarkDocs:
    def __init__(self, docs_dir: Path) -> None:
        self.docs_dir = docs_dir

    def group_doc(self, view_name: str) -> BenchmarkDoc | None:
        return self._doc_from_path(self.docs_dir / _safe_segment(view_name) / "index.md", url_parts=(view_name,))

    def task_doc(self, *, view_name: str, metric_column: str) -> BenchmarkDoc | None:
        path = self._task_doc_path(view_name=view_name, metric_column=metric_column)
        if path is None:
            return None
        return self._doc_from_path(path, url_parts=(view_name, path.stem))

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
        return BenchmarkDoc(
            title=_extract_title(markdown) or path.stem,
            description=_extract_overview(markdown),
            url=_doc_url(url_parts),
            markdown=markdown,
        )


def render_markdown_page(*, doc: BenchmarkDoc, css_version: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(doc.title)} - HAKARI-bench docs</title>
  <link rel="stylesheet" href="/assets/app.css?v={escape(css_version, quote=True)}">
</head>
<body class="bg-zinc-50 text-zinc-950">
  <main class="mx-auto max-w-4xl px-4 py-6 sm:px-6">
    <article class="benchmark-doc border border-zinc-200 bg-white px-4 py-5">
      {render_markdown_to_html(doc.markdown)}
    </article>
  </main>
</body>
</html>"""


def render_markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    html: list[str] = []
    paragraph: list[str] = []
    in_list = False
    in_code = False
    code_lines: list[str] = []
    in_table = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            html.append(f"<p>{_inline_markdown(' '.join(line.strip() for line in paragraph))}</p>")
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
            html.append(f"<h{level}>{_inline_markdown(heading.group(2).strip())}</h{level}>")
            continue
        if line.startswith(">"):
            flush_paragraph()
            close_list()
            close_table()
            html.append(f"<blockquote>{_inline_markdown(line.lstrip('> ').strip())}</blockquote>")
            continue
        if line.startswith("- "):
            flush_paragraph()
            close_table()
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{_inline_markdown(line[2:].strip())}</li>")
            continue
        if _is_table_row(line):
            flush_paragraph()
            close_list()
            if _is_table_separator(line):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            row_html = "".join(f"<td>{_inline_markdown(cell)}</td>" for cell in cells)
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
    return "\n".join(html)


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


def _inline_markdown(text: str) -> str:
    escaped = escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_replacement, escaped)
    return escaped


def _link_replacement(match: re.Match[str]) -> str:
    label = match.group(1)
    url = match.group(2)
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return label
    return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{label}</a>'


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
