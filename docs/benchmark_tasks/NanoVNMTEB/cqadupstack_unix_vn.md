# NanoVNMTEB / cqadupstack_unix_vn

## Overview

VN-MTEB translates CQADupStack's Unix duplicate-question retrieval split into
Vietnamese. The query is a short Unix or Linux title, and the target is a longer
archived system-administration thread that asks the same problem. Observed
documents contain command snippets, terminal output, paths, and configuration
context, with examples such as launching applications from a terminal, tilde
suffixes on filenames, read-only ISO mounts, and reacting when files change.
The task tests equivalent command-line intent across shells, filesystems,
signals, networking, mounting, and process handling.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) presents a benchmark for
retrieving duplicate community questions from StackExchange. It keeps the task
close to real duplicate detection by ranking previously asked questions and by
using manual duplicate flags rather than generic related-question links.

[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates such
English benchmark data into Vietnamese with automatic translation and quality
filtering. For Unix, translation quality matters because command names,
filenames, signals, mount options, package names, and error messages are part of
the retrieval signal.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 434 positive qrel rows.
The average is 2.17 positives per query; 80 queries have multiple positives and
the maximum is 16. Queries average 52.80 characters. Documents average 875.77
characters and commonly include command snippets, terminal output, paths, and
system configuration context.

Observed examples include launching applications from a terminal, tilde suffixes
on filenames, read-only ISO mounts, reacting when files appear in a directory,
and resolving hostnames on a LAN. The same operational problem may be described
as a command question, an error-message question, or a workflow question.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3816
and hit@10 = 0.5750. Unix command names and error strings are strong lexical
signals, and the median first relevant BM25 rank is 7, the best among this
six-task batch.

Even so, many duplicates require mapping a symptom to an underlying Unix
concept, such as SIGHUP behavior, filesystem mount modes, or local DNS name
resolution. A model must use technical equivalence, not only shared command
tokens.

### Training Data That May Help

Useful training data includes non-overlapping Unix StackExchange duplicate
pairs, Vietnamese Linux administration QA, man-page or documentation retrieval
pairs, shell-command troubleshooting data, and translated CQADupStack training
splits after overlap removal. The translated test questions, qrels, documents,
and duplicate clusters used by this Nano split should be excluded.

Hard negatives should share command names or error text but differ in operating
system behavior or configuration cause.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation Unix QA threads and create
Vietnamese duplicate titles that ask the same command-line or administration
problem in another form. Preserve commands, paths, flags, signals, package
names, and error messages.

For joint generation, create clusters around one system behavior, with
equivalent symptom descriptions and hard negatives from the same command family.
Do not use evaluation split queries or positive documents as synthetic seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Tập tin đặc biệt gây ra lỗi I/O (31 chars) | Tạo ra lỗi đọc lặp đi lặp lại để thử nghiệm? Tôi đang cố gắng thử nghiệm xử lý lỗi trong một số phần mềm, đặc biệt là những gì xảy ra khi có lỗi xảy ra khi đọc từ một tập tin hoặc đường ống. Có cách nào đơn giản để gửi một lư ... [truncated 225 chars](457 chars) |
| Xác định gen từ một danh sách các gen (37 chars) | So sánh hai tập tin để tìm các dòng trùng khớp và lưu kết quả dương tính Tôi có 2 file. ### File 1: A0001 C001 B0003 C896 A0024 C234 . B1542 C231 . tới 28412 dòng như thế này ### File 2: A0001 A0024 B1542 . . và 12000 dòng nh ... [truncated 225 chars](568 chars) |
| Làm thế nào để tôi chỉnh sửa một tập tin như là root? (53 chars) | Cách để chỉnh sửa fstab ở Debian Tôi muốn thay đổi tập tin fstab để có thể giải quyết "lỗi đính kèm" (tôi đã thử xóa dòng cuối của tập tin fstab) # /etc/fstab: thông tin hệ thống tập tin tĩnh. # # Sử dụng 'blkid' để in định d ... [truncated 225 chars](1069 chars) |
| Làm thế nào để có được hỗ trợ 256 màu trong một TTY đăng nhập? (62 chars) | 256 màu trong thực tế console Tôi có trong .bashrc của tôi xuất ra biến môi trường TERM = xterm-256color, nhưng điều này gây ra nhấp nháy tất cả các văn bản màu sắc (ls -- màu sắc, trong vim, v.v.) trên console thực tế (CTRL ... [truncated 225 chars](636 chars) |
| Cách làm cho một máy tính có thể truy cập được từ LAN sử dụng tên máy chủ (73 chars) | định địa chỉ đơn giản trên LAN Tôi đọc câu hỏi này Làm thế nào để tạo một máy tính có thể truy cập từ mạng cục bộ sử dụng tên máy chủ. Cách đơn giản nhất để cho phép các máy chủ Linux trên LAN xác định nhau bằng tên máy chủ l ... [truncated 225 chars](449 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | cqadupstack_unix_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/cqadupstack-unix-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-unix-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 434 |
| Avg positives / query | 2.17 |
| Positives per query (min / median / max) | 1 / 1 / 16 |
| Queries with multiple positives | 80 (40.00%) |
| BM25 nDCG@10 | 0.3816 |
| BM25 hit@10 | 0.5750 |
| Query length avg chars | 52.80 |
| Document length avg chars | 875.77 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/cqadupstack-unix-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-unix-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/cqadupstack-unix-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-unix-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | https://doi.org/10.1145/2838931.2838934 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/cqadupstack-unix-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/cqadupstack-unix-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: cqadupstack_unix_vn
  split_name: cqadupstack_unix_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/cqadupstack_unix_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
      - https://aclanthology.org/2026.findings-eacl.86/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/GreenNode/cqadupstack-unix-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 434
  positives_per_query:
    average: 2.17
    min: 1
    median: 1.0
    max: 16
    multi_positive_queries: 80
    multi_positive_query_percent: 40.0
  text_stats_chars:
    query_mean: 52.795
    document_mean: 875.765
  bm25:
    ndcg_at_10: 0.381628513
    hit_at_10: 0.575
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "translated VN-MTEB CQADupStack Unix test split from GreenNode/cqadupstack-unix-vn"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated Unix test questions, documents, qrels, and duplicate clusters used by this Nano split."
    useful_training_data:
      - non-overlapping Unix StackExchange duplicate-question pairs
      - Vietnamese Linux and system-administration QA
      - man-page and documentation retrieval pairs
      - translated CQADupStack training splits with overlap removed
    synthetic_data:
      document_generation: "Vietnamese Unix QA threads preserving commands, paths, flags, signals, and error messages."
      question_generation: "Short Vietnamese duplicate titles asking the same command-line or administration problem."
      answerability: "Each query should match the same system behavior, with same-command but different-cause negatives."
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
      - label: GreenNode/cqadupstack-unix-vn
        url: https://huggingface.co/datasets/GreenNode/cqadupstack-unix-vn
    source_notes: []
  references:
    - title: "CQADupStack: A Benchmark Data Set for Community Question-Answering Research"
      url: https://doi.org/10.1145/2838931.2838934
      year: 2015
      doi: 10.1145/2838931.2838934
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "VN-MTEB: Vietnamese Massive Text Embedding Benchmark"
      url: https://aclanthology.org/2026.findings-eacl.86/
      year: 2026
      doi: 10.18653/v1/2026.findings-eacl.86
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: definitive_paper_link
    - title: GreenNode/cqadupstack-unix-vn
      url: https://huggingface.co/datasets/GreenNode/cqadupstack-unix-vn
      year: null
      doi: null
      is_paper: false
      source_confidence: probably_correct
```
