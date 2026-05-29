# NanoVNMTEB / cqadupstack_tex_vn

## Overview

The TeX split is VN-MTEB's Vietnamese translation of CQADupStack duplicate
retrieval for LaTeX and TeX questions. Relevance comes from manual duplicate
links, so a translated title must retrieve earlier threads solving the same
typesetting issue rather than broadly related LaTeX content. The observed data
includes multi-line sums, cover-relation symbols, renaming document elements,
undefined citation warnings, TeXLive installation, packages, layout, symbols,
bibliographies, and long code-heavy documents.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) uses manually flagged
StackExchange duplicate links to evaluate retrieval of earlier questions that
should answer a new question. The paper notes that this real-time duplicate
detection setting differs from generic related-question retrieval: related
questions are not the same as manually identified duplicates.

[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates the source
benchmark into Vietnamese and filters the translations with language,
embedding-similarity, and LLM-based quality checks. TeX is a difficult case for
translation because commands, package names, code snippets, and mathematical
notation must stay semantically intact.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 743 positive qrel rows.
The average is 3.715 positives per query; 86 queries have multiple positives and
the maximum is 100. Queries average 47.79 characters. Documents average
1,090.56 characters, with a very long tail: the longest observed document is
56,546 characters.

Examples include multi-line sums, cover-relation symbols, renaming document
elements, undefined citation warnings, and TeXLive installation. Documents often
mix Vietnamese prose with LaTeX commands, package names, quoted warning text,
and short code blocks.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2923
and hit@10 = 0.4900. Exact command names and warning strings are strong lexical
cues, but many duplicates are conceptual TeX questions where different command
paths solve the same formatting problem.

The large multi-positive clusters make ranking quality important: finding one
duplicate helps, but a useful retriever should rank several equivalent TeX
solutions above same-package but different-problem negatives.

### Training Data That May Help

Useful training data includes non-overlapping TeX StackExchange duplicate pairs,
Vietnamese technical writing QA, LaTeX documentation retrieval pairs, and
translated CQADupStack training splits after overlap removal. The translated
test questions, qrels, documents, and duplicate clusters used by this Nano split
should be excluded.

Training should preserve code and markup tokens exactly; normalizing away
backslashes, package names, or warning strings would remove important evidence.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation TeX QA threads and create
Vietnamese duplicate titles that ask for the same LaTeX behavior with different
wording. Preserve commands, package names, bibliography styles, warning text,
and mathematical notation.

For joint generation, create clusters around one TeX problem such as symbol
selection, page layout, citations, package conflicts, or installation. Include
hard negatives that share a package or command but solve a different formatting
intent.

## Example Data

| Query | Positive document |
| --- | --- |
| Vẽ cung tròn trong Tikz khi trung tâm của đường tròn được chỉ định (66 chars) | vị trí cung so với vòng tròn > **Có thể là trùng lặp:** > Vẽ cung trong Tikz khi tâm của vòng tròn được chỉ định một câu hỏi rất đơn giản nhưng tôi không thể làm được! Xin lỗi nhưng tôi thấy tọa độ gây nhầm lẫn. Tôi muốn vẽ m ... [truncated 225 chars](868 chars) |
| Cách trích dẫn tài liệu pháp lý đúng cách là gì? (48 chars) | Làm thế nào để trích dẫn các vụ kiện pháp lý trong BibTeX > **Có thể trùng lặp:** > Cách trích dẫn văn bản pháp lý đúng cách là gì? Ai biết cách định dạng trích dẫn một vụ án pháp lý trong BibTeX không? Giả sử tôi muốn trích ... [truncated 225 chars](297 chars) |
| Sử dụng ERT trong LyX (21 chars) | Bảng TeX của LyX quá lớn Tôi đang chèn một tập tin TeX vào tài liệu LyX bằng cách sử dụng Chèn -> Tài liệu con. Bảng trông ổn trên màn hình của LyX nhưng khi tôi xem trước PDF thì nó lớn gấp 10 lần. Không biết làm thế nào để ... [truncated 225 chars](1052 chars) |
| Làm thế nào để sửa lỗi "ruby.exe seems not to be installed" trong Windows 7 khi cả Miktex 2.9 và Ruby đều đã được cài đặt? (122 chars) | TexLive không thể tìm thấy Ruby.exe > **Có thể trùng lặp:** > Làm thế nào để sửa lỗi "ruby.exe dường như không được cài đặt" trên Windows 7 nơi cả Miktex 2.9 và Ruby đã được cài đặt? Tôi vừa cài đặt TexLive 2010 trên một máy ... [truncated 225 chars](372 chars) |
| Định dạng hàng đầu tiên của bảng khác nhau (42 chars) | \newcommand \multispan không được đặt đúng vị trí. Tôi đang cố gắng xây dựng một công thức nấu ăn của riêng mình, có một macro thành phần. Đôi khi các thành phần nên được tách ra và có tiêu đề, vì vậy tôi đã thử với một đối s ... [truncated 225 chars](692 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | cqadupstack_tex_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/cqadupstack-tex-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 743 |
| Avg positives / query | 3.71 |
| Positives per query (min / median / max) | 1 / 1 / 100 |
| Queries with multiple positives | 86 (43.00%) |
| BM25 nDCG@10 | 0.2843 |
| BM25 hit@10 | 0.4700 |
| BM25 Recall@100 | 0.3997 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2927 |
| Dense hit@10 | 0.5000 |
| Dense Recall@100 | 0.4576 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3163 |
| Reranking hybrid hit@10 | 0.5000 |
| Reranking hybrid Recall@100 | 0.4980 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 38 |
| Query length avg chars | 47.79 |
| Document length avg chars | 1,090.56 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/cqadupstack-tex-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/cqadupstack-tex-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | https://doi.org/10.1145/2838931.2838934 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/cqadupstack-tex-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: cqadupstack_tex_vn
  split_name: cqadupstack_tex_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/cqadupstack_tex_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 743
  positives_per_query:
    average: 3.715
    min: 1
    median: 1.0
    max: 100
    multi_positive_queries: 86
    multi_positive_query_percent: 43.0
  text_stats_chars:
    query_mean: 47.79
    document_mean: 1090.556
  bm25:
    ndcg_at_10: 0.28430487181297953
    hit_at_10: 0.47
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB CQADupStack TeX test split from GreenNode/cqadupstack-tex-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated TeX test questions, documents, qrels, and duplicate
      clusters used by this Nano split.
    useful_training_data:
    - non-overlapping TeX StackExchange duplicate-question pairs
    - Vietnamese technical writing and LaTeX QA
    - LaTeX documentation retrieval pairs
    - translated CQADupStack training splits with overlap removed
    synthetic_data:
      document_generation: Vietnamese TeX QA threads preserving commands, package
        names, warnings, and mathematical notation.
      question_generation: Short Vietnamese duplicate titles asking the same TeX formatting
        or installation problem.
      answerability: Each query should match duplicate TeX behavior, with same-package
        but different-problem negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: CQADupStack DOI
      url: https://doi.org/10.1145/2838931.2838934
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/cqadupstack-tex-vn
      url: https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn
    source_notes: []
  references:
  - title: 'CQADupStack: A Benchmark Data Set for Community Question-Answering Research'
    url: https://doi.org/10.1145/2838931.2838934
    year: 2015
    doi: 10.1145/2838931.2838934
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'VN-MTEB: Vietnamese Massive Text Embedding Benchmark'
    url: https://aclanthology.org/2026.findings-eacl.86/
    year: 2026
    doi: 10.18653/v1/2026.findings-eacl.86
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  - title: GreenNode/cqadupstack-tex-vn
    url: https://huggingface.co/datasets/GreenNode/cqadupstack-tex-vn
    year: null
    doi: null
    is_paper: false
    source_confidence: probably_correct
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2843048718
      hit_at_10: 0.47
      recall_at_100: 0.399730821
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.399730821
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2927496014
      hit_at_10: 0.5
      recall_at_100: 0.4576043069
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4576043069
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3162843275
      hit_at_10: 0.5
      recall_at_100: 0.4979811575
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.19
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4979811575
      safeguard_positive_rows: 38
      rows_with_101_candidates: 38
```
