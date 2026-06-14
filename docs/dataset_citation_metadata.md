# Dataset Citation Metadata

This document is the canonical repository guidance for writing and auditing
paper/source citation metadata for NanoIR dataset definition files. Do not rely
on skill-local citation instructions as the source of truth. Skill files may
point here, but citation policy and metadata workflow should be maintained in
this document.

## Purpose

Dataset metadata should help benchmark users understand what each dataset group and task measures, which language and category it belongs to, and which sources should be cited when writing papers. Task-level citations matter because many Nano-set benchmark groups are assembled from external datasets. A group paper such as MTEB, MIRACL, RTEB, or a Nano benchmark paper may explain the benchmark wrapper, but it may not be the correct source for an individual task.

The citation metadata must therefore distinguish between:

- the benchmark group source,
- the underlying task or dataset paper,
- non-paper sources such as blogs, Hugging Face dataset cards, GitHub repositories, project pages, and Zenodo dataset records,
- the confidence level that the source is the correct one for the task.

## Where Metadata Lives

Built-in dataset definitions live under `config/datasets/`. Collection definitions live under `config/dataset_collections/`.

Use dataset-level `metadata` for the dataset group as a whole:

```yaml
metadata:
  language: en
  category: natural_language
  short_description: Compact MTEB English retrieval benchmark.
  description: NanoMTEB is a compact English retrieval benchmark aligned with the MTEB retrieval evaluation suite.
  languages:
  - en
  language_detection:
    detector: fast-langdetect
    min_language_percent: 0.5
    main_language_percent: 10.0
    query:
      sample_count: 200
      languages:
        en: 100.0
    document:
      sample_count: 10000
      languages:
        en: 99.8
  citation_keys:
  - muennighoff2023mteb
  references:
  - title: 'MTEB: Massive Text Embedding Benchmark'
    authors:
    - Niklas Muennighoff
    - Nouamane Tazi
    - Loic Magne
    - Nils Reimers
    year: 2023
    url: https://arxiv.org/abs/2210.07316
    is_paper: true
    source_confidence: definitive_paper_link
    doi: 10.48550/arXiv.2210.07316
  bibtex: |
    @inproceedings{muennighoff2023mteb,
      title = {{MTEB}: Massive Text Embedding Benchmark},
      author = {Muennighoff, Niklas and Tazi, Nouamane and Magne, Loic and Reimers, Nils},
      year = {2023},
      url = {https://arxiv.org/abs/2210.07316},
      doi = {10.48550/arXiv.2210.07316}
    }
```

Use task-level `task_metadata` for each split or task:

```yaml
task_metadata:
  NanoArguAna:
    language: en
    category: natural_language
    short_description: Argument retrieval over counterargument pairs.
    description: A compact ArguAna split where each query is an argument and relevant documents are strong counterarguments.
    languages:
    - en
    language_detection:
      detector: fast-langdetect
      min_language_percent: 0.5
      main_language_percent: 10.0
      query:
        sample_count: 200
        languages:
          en: 100.0
      document:
        sample_count: 8626
        languages:
          en: 100.0
    citation_keys:
    - wachsmuth2018arguana
    references:
    - title: Retrieval of the Best Counterargument without Prior Topic Knowledge
      authors:
      - Henning Wachsmuth
      - Shahbaz Syed
      - Benno Stein
      year: 2018
      url: https://aclanthology.org/P18-1023/
      is_paper: true
      source_confidence: definitive_paper_link
      doi: 10.18653/v1/P18-1023
    bibtex: |
      @inproceedings{wachsmuth2018arguana,
        title = {Retrieval of the Best Counterargument without Prior Topic Knowledge},
        author = {Wachsmuth, Henning and Syed, Shahbaz and Stein, Benno},
        booktitle = {Proceedings of ACL},
        year = {2018},
        url = {https://aclanthology.org/P18-1023/},
        doi = {10.18653/v1/P18-1023}
      }
```

## Field Types

### Group And Task Metadata

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `language` | string | yes | ISO 639-1 two-character code, or `multilingual`. |
| `primary_languages` | list of strings | required for language-axis Nano-sets | Canonical language routing for leaderboard language pages. Use one code for a language-specific Nano-set such as `vi`, up to two codes for bitext/cross-lingual tasks such as `[de, fr]`, or only `[multilingual]` when the task is inherently mixed across many languages. |
| `languages` | list of strings | recommended | Main detected languages for the task. Include languages that account for at least 10% of either query or document texts, ordered by detected usage. Use `unknown` when detection cannot establish a language. |
| `language_detection` | mapping | recommended | `fast-langdetect` query/document language percentages. Include languages at or above 0.5% for each side. |
| `category` | string | yes | `natural_language` or `code`. |
| `short_description` | string | yes | 140 characters or fewer. |
| `description` | string | yes | Human-readable benchmark/task overview. Prefer concise prose for YAML maintainability. |
| `citation_keys` | list of strings | recommended | Keys used by `bibtex` and downstream citation rendering. Keep unique within the metadata block. |
| `references` | list of reference objects | recommended | Structured source records. Each reference must include `is_paper` and `source_confidence`. |
| `bibtex` | string | recommended | BibTeX entries for the citation keys. Keep entries consistent with `references`. |
| `query_text_stats` | text stats object | task-level when available | Character-count summary for queries. |
| `document_text_stats` | text stats object | task-level when available | Character-count summary for corpus documents. |

### Reference Object

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `title` | string | recommended | Source title exactly enough to identify the work. |
| `authors` | list of strings | recommended | Use structured author names, not `et al.` when practical. |
| `year` | integer | recommended | Publication or source year. |
| `url` | string | recommended | Prefer DOI, ACL Anthology, arXiv, proceedings, official dataset, or dataset-card URL. |
| `doi` | string | optional | Include when known and consistent with `url`. |
| `is_paper` | boolean | yes | `true` for scholarly papers/preprints/proceedings; `false` for blog, dataset card, GitHub, Hugging Face, project page, or dataset-only Zenodo records. |
| `source_confidence` | string | yes | One of the labels below. |

### Text Stats Object

| Field | Type | Required |
| --- | --- | --- |
| `count` | integer or float | yes |
| `min_chars` | integer or float | yes |
| `max_chars` | integer or float | yes |
| `mean_chars` | integer or float | yes |
| `median_chars` | integer or float | yes |

### Language Detection Object

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `detector` | string | yes | Currently `fast-langdetect`. |
| `min_language_percent` | integer or float | yes | Minimum side percentage reported under `query.languages` and `document.languages`; normally `0.5`. |
| `main_language_percent` | integer or float | yes | Threshold for inclusion in top-level `languages`; normally `10.0`. |
| `query.sample_count` | integer | yes | Number of non-empty query texts passed to the detector. |
| `query.languages` | mapping | yes | Detected query-language percentages, ordered descending. |
| `document.sample_count` | integer | yes | Number of non-empty document texts passed to the detector. |
| `document.languages` | mapping | yes | Detected document-language percentages, ordered descending. |

For code retrieval tasks whose natural-language surface is primarily English, keep top-level `languages` as `["en"]` even when code snippets cause `fast-langdetect` to assign programming tokens to unrelated natural languages. Preserve those raw detector percentages in `language_detection` rather than hiding them.

## Source Confidence Labels

Use these labels exactly:

| Label | Meaning |
| --- | --- |
| `source_uncertain` | The source may be relevant, but the citation-to-task relationship is not established well enough to rely on without further review. |
| `probably_correct` | The source appears to be the right task or dataset source based on upstream metadata, MTEB GitHub source, dataset cards, or web research, but some uncertainty remains or the source is non-paper. |
| `definitive_paper_link` | The source is a paper, official proceedings page, DOI landing page, arXiv page, or comparable scholarly record that clearly corresponds to the task or dataset. |
| `human_verified` | A human reviewer explicitly checked and approved the source. AI agents must not assign this label. |

## Research Guidance

Start with the dataset YAML and Hugging Face dataset card, then compare against upstream benchmark source repositories such as [MTEB](https://github.com/embeddings-benchmark/mteb). Treat upstream benchmark metadata as evidence, not as final authority. Confirm the citation with primary or near-primary sources when possible.

Prefer sources in this order:

1. Task-specific paper or official proceedings page.
2. Dataset paper, shared-task overview paper, or benchmark paper that introduced the task.
3. Official dataset record, dataset card, project page, or Zenodo record.
4. Upstream benchmark source metadata.
5. Blog post or repository page when it is the canonical source and no stronger paper exists.

When a final ACL, EMNLP, NAACL, SIGIR, LREC, CEUR, TREC, DOI, or publisher page exists, prefer it over an older arXiv URL unless the source explicitly asks users to cite the preprint. Keep the year, title, authors, DOI, and BibTeX synchronized with the selected source.

## Citation Usability

A task is ready for paper bibliography use when it has at least one `references` entry with `is_paper: true` and `source_confidence: definitive_paper_link`. A task with only `is_paper: false` and `probably_correct` sources can still be documented, but it should normally be cited as a dataset/source URL rather than as a scholarly paper.

Do not attach an unrelated paper just to make a task look more citable. If the best available source is a dataset card or blog, keep it as non-paper metadata and make that limitation explicit through `is_paper: false` and `source_confidence: probably_correct`.

## Validation Checklist

Before committing metadata changes:

1. Confirm every split/task has `task_metadata`.
2. Confirm every metadata block has `language`, `category`, `short_description`, and `description`.
3. Confirm `languages` contains the main detected languages and `language_detection` records query/document percentages when language detection has been run.
4. Confirm every reference has boolean `is_paper` and valid `source_confidence`.
5. Confirm no AI audit assigns `human_verified`.
6. Confirm duplicated citation keys and duplicated authors are removed.
7. Confirm BibTeX keys match `citation_keys`.
8. Confirm source URLs, DOI values, years, and author lists refer to the same work.
9. Confirm text stats are numeric and use the required five fields.
10. Run the repository checks required by `AGENTS.md`, normally `uv run tox` before committing.

## Long Audits

For large dataset metadata sweeps, keep an ignored progress checklist under
`tmp/`. Split work by dataset family when parallel review is useful, but require
each reviewer to list source URLs checked, unresolved uncertainties, and exact
YAML changes needed. After merging findings, perform one parent pass over all
files to catch cross-file inconsistencies, duplicated citation keys, duplicated
authors, stale source URLs, and copy-paste mistakes.
