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
    breadcrumb = _render_doc_breadcrumb(doc.url)
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
    {breadcrumb}
    <article class="benchmark-doc border border-zinc-200 bg-white px-4 py-5">
      {render_markdown_to_html(doc.markdown, base_url=doc.url)}
    </article>
  </main>
</body>
</html>"""


def render_docs_index_page(*, docs: list[BenchmarkDoc], css_version: str) -> str:
    items = "\n".join(
        f"""<li class="border border-zinc-200 bg-white px-4 py-3">
          <a class="font-semibold text-cyan-700 underline underline-offset-2" href="{escape(doc.url, quote=True)}">{escape(doc.title)}</a>
          <p class="mt-1 text-sm leading-snug text-zinc-700">{escape(doc.description)}</p>
        </li>"""
        for doc in docs
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Benchmark documentation - HAKARI-bench docs</title>
  <link rel="stylesheet" href="/assets/app.css?v={escape(css_version, quote=True)}">
</head>
<body class="bg-zinc-50 text-zinc-950">
  <main class="mx-auto max-w-4xl px-4 py-6 sm:px-6">
    <nav class="doc-breadcrumb mb-3 text-sm text-zinc-600" aria-label="Breadcrumb">
      <ol class="flex flex-wrap items-center gap-y-1">
        <li><a class="underline underline-offset-2" href="/">Top</a></li>
        <li><span class="px-1 text-zinc-400" aria-hidden="true">&gt;</span></li>
        <li><span aria-current="page">Benchmark documentation</span></li>
      </ol>
    </nav>
    <header class="mb-4">
      <h1 class="text-2xl font-semibold text-zinc-950">Benchmark documentation</h1>
      <p class="mt-1 text-sm text-zinc-600">Dataset and benchmark task group descriptions used by the leaderboard viewer.</p>
    </header>
    <ul class="space-y-2">
      {items}
    </ul>
  </main>
</body>
</html>"""


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
