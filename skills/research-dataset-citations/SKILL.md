---
name: research-dataset-citations
description: Research and apply paper, dataset, blog, and source citation metadata for NanoIR dataset YAML definitions. Use when Codex needs to add, audit, or repair references, BibTeX, source confidence labels, language/category metadata, descriptions, or query/document text statistics for benchmark groups and task-level dataset definitions.
---

# Research Dataset Citations

## Goal

Use this skill to make benchmark dataset metadata suitable for paper writing and reproducible dataset documentation. Prefer task-specific citations over broad benchmark citations, and distinguish scholarly papers from dataset cards, blog posts, project pages, and Hugging Face or Zenodo records.

## Core Workflow

1. Inspect the repository guidance, dataset YAML shape, metadata validation code, and existing examples under `config/datasets/` and `config/dataset_collections/`.
2. Build an inventory of every group and task that needs metadata. Include collection-level metadata, dataset-level `metadata`, and per-task `task_metadata`.
3. For each group or task, identify candidate sources from the dataset YAML, Hugging Face dataset card, dataset README, paper title in the data source, and upstream benchmark implementations such as the MTEB GitHub repository: `https://github.com/embeddings-benchmark/mteb`.
4. Verify candidates against primary or near-primary sources. Prefer ACL Anthology, arXiv, DOI landing pages, official proceedings, CEUR, TREC/IR Anthology, publisher pages, official project pages, Zenodo records, and Hugging Face dataset cards over search snippets or secondary blogs.
5. Decide whether each source is a paper. Set `is_paper: true` only for scholarly papers, proceedings papers, preprints, technical reports, or comparable academic records. Set `is_paper: false` for blogs, dataset cards, Hugging Face pages, GitHub repositories, Zenodo dataset records, and project pages unless the record is explicitly a paper.
6. Assign `source_confidence` for every reference. Use the strongest label justified by the evidence, and never assign `human_verified` unless a human reviewer explicitly did the check.
7. Update YAML with structured references, citation keys, BibTeX, language, category, short descriptions, long descriptions, and text statistics when requested.
8. Validate mechanically, then review manually for copy-paste errors such as duplicated citation keys, duplicated authors, stale arXiv links when final proceedings exist, incorrect author order, or mismatched dataset/source titles.

## Source Priority

Use sources in this order when available:

1. Task-specific paper or official proceedings page.
2. Dataset paper, shared-task overview paper, or benchmark paper that directly introduced the dataset.
3. Official dataset record, dataset card, project page, or Zenodo record.
4. Upstream benchmark metadata, including MTEB GitHub source files and dataset cards.
5. Blog posts or repository pages, only when no stronger source exists or when they are the benchmark's canonical announcement.

If a task appears in MTEB, use MTEB as an evidence source, not as the only authority. Confirm the paper URL, authors, year, DOI, and task relationship with a primary source whenever possible.

## Metadata Fields

Use these fields for collection, dataset, and task metadata when the repository supports them:

```yaml
metadata:
  language: en
  category: natural_language
  short_description: Compact description under 140 characters.
  description: Longer benchmark overview.
  citation_keys:
  - example2024dataset
  references:
  - title: Example Dataset Paper
    authors:
    - First Author
    - Second Author
    year: 2024
    url: https://arxiv.org/abs/2401.00000
    is_paper: true
    source_confidence: definitive_paper_link
    doi: 10.48550/arXiv.2401.00000
  bibtex: |
    @article{example2024dataset,
      title = {Example Dataset Paper},
      author = {Author, First and Author, Second},
      year = {2024},
      url = {https://arxiv.org/abs/2401.00000}
    }
```

For task-level metadata, place the same shape under `task_metadata.<TaskName>`. Include `query_text_stats` and `document_text_stats` when text statistics are part of the task:

```yaml
query_text_stats:
  count: 200
  min_chars: 12
  max_chars: 420
  mean_chars: 84.35
  median_chars: 71.0
document_text_stats:
  count: 10000
  min_chars: 4
  max_chars: 12000
  mean_chars: 735.2
  median_chars: 540.0
```

## Language And Category

Set `language` to an ISO 639-1 two-character code such as `en`, `ja`, `zh`, `fr`, or to `multilingual` when the task intentionally spans multiple languages.

Set `category` to one of:

- `natural_language` for ordinary text retrieval, QA, fact checking, legal, medical, scientific, multilingual, or web/document retrieval tasks.
- `code` for code search, code RAG, text-to-SQL, programming, or source-code-centered retrieval tasks.

## Source Confidence Labels

Use the repository's labels consistently:

- `source_uncertain`: The source may be relevant, but the task-to-source relationship is not reliable enough for citation without further review.
- `probably_correct`: The source appears to be correct based on upstream metadata, dataset cards, MTEB source, or web research, but it is not a definitive paper/source page or some uncertainty remains.
- `definitive_paper_link`: The source is a paper, official proceedings page, DOI landing page, arXiv page, or comparable scholarly record that clearly corresponds to the task or dataset.
- `human_verified`: A human reviewer explicitly checked and approved the source. AI agents must not assign this label.

Prefer `definitive_paper_link` only when the URL and bibliographic data clearly match the task. Use `probably_correct` for Hugging Face dataset cards, GitHub pages, dataset-only Zenodo records, blog posts, or paper candidates that remain plausible but not fully established.

## Citation Policy

For benchmark groups, cite the benchmark paper or canonical announcement for the group. For sub tasks, also cite the underlying dataset or task paper when it exists. A group-level citation is not a substitute for a task-level citation when the task comes from an external dataset.

When a task has no paper, cite the strongest non-paper source and mark it with `is_paper: false` and `source_confidence: probably_correct`. Do not force a weak or unrelated paper into the metadata just to avoid a non-paper reference.

When a source exists both as an arXiv preprint and final proceedings paper, prefer the final proceedings URL and DOI unless the dataset explicitly asks to cite the preprint. Keep the BibTeX consistent with the chosen URL.

## Audit Checklist

For every changed YAML file:

- Confirm all references have `title`, `authors`, `year`, `url`, `is_paper`, and `source_confidence`.
- Confirm `citation_keys` are unique within the metadata block and match the BibTeX keys.
- Confirm author names are not duplicated and match the chosen source spelling.
- Confirm DOI and URL point to the same work.
- Confirm `is_paper` is false for blog, Hugging Face, GitHub, project-page, and dataset-record sources.
- Confirm no AI-only audit assigns `human_verified`.
- Confirm every task listed in `splits` has task metadata.
- Confirm stats fields are numeric and use `count`, `min_chars`, `max_chars`, `mean_chars`, and `median_chars`.
- Run the repository metadata validation and tests required by `AGENTS.md`.

## Long Audits

For large dataset sweeps, keep an ignored progress checklist under `tmp/`. Split work by dataset family when using subagents, but require each reviewer to list source URLs checked, unresolved uncertainties, and exact YAML changes needed. After merging findings, perform one parent pass over all files to catch cross-file inconsistencies and copy-paste mistakes.
