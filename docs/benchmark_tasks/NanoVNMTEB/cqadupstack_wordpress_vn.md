# NanoVNMTEB / cqadupstack_wordpress_vn

## Overview

VN-MTEB translates CQADupStack's WordPress duplicate-question retrieval split
into Vietnamese, preserving the goal of retrieving earlier threads that ask the
same support problem. Queries are short translated WordPress titles, while
documents are longer support threads with API names, PHP snippets, theme
filenames, plugin names, and error text. The observed examples include
`start_el()` signature errors, RSS feed titles, custom post type templates
returning 404, hooks, SEO plugins, and template routing, so code and WordPress
terminology must survive translation-aware duplicate matching.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) provides StackExchange
duplicate-question retrieval data with manually flagged duplicate links. The
paper reports benchmark results with lexical methods including BM25, and it
notes that duplicate detection is hard because lexical overlap does not cleanly
separate duplicate from non-duplicate question pairs.

[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates source
benchmark data into Vietnamese and filters it for language and semantic
quality. WordPress questions retain many English identifiers, hook names, file
templates, plugin names, and PHP fragments, which the retriever must handle
alongside Vietnamese prose.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 337 positive qrel rows.
The average is 1.685 positives per query; 43 queries have multiple positives
and the maximum is 62. Queries average 52.37 characters. Documents average
1,028.81 characters and often include WordPress API names, PHP snippets, theme
filenames, plugin names, or error text.

Observed examples include `start_el()` signature errors, custom RSS feed titles,
custom post type single templates returning 404, archive pages for custom post
types, and hiding Yoast SEO meta boxes. Many duplicates depend on WordPress
routing or plugin behavior rather than a single exact keyword.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3170
and hit@10 = 0.4800. Exact identifiers such as `start_el`, `single-<post-type>`,
Yoast SEO, and RSS are useful, but relevant duplicates may use different
template names or describe the same hook behavior from another angle.

The median first relevant BM25 rank is 17, so retrieval needs semantic and
technical normalization to move duplicates into the top 10.

### Training Data That May Help

Useful training data includes non-overlapping WordPress StackExchange duplicate
pairs, Vietnamese WordPress support QA, WordPress documentation retrieval pairs,
plugin/theme troubleshooting data, and translated CQADupStack training splits
after overlap removal. The translated test questions, qrels, documents, and
duplicate clusters used by this Nano split should be excluded.

Training should keep PHP identifiers, hook names, template filenames, and plugin
names intact, since these tokens often carry the answer-bearing constraint.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation WordPress QA threads and
create Vietnamese duplicate titles that ask the same theme, plugin, hook, or
template-routing problem. Preserve PHP snippets, hook names, plugin names, file
templates, and version-specific details.

For joint generation, create clusters around one WordPress behavior, such as
custom post type archives, feed titles, metabox visibility, or template
resolution. Include hard negatives that share a plugin or hook but ask a
different implementation question.

## Example Data

| Query | Positive document |
| --- | --- |
| Các thành viên chia sẻ giữa hai cài đặt khác nhau với các cơ sở dữ liệu khác nhau wordpress (91 chars) | Cách sử dụng các bảng db từ xa trong cấu hình hiện tại? > **Có thể trùng lặp:** > Thành viên chia sẻ giữa hai cài đặt wordpress khác nhau với các cơ sở dữ liệu khác nhau Ví dụ tôi có 2 cài đặt wordpress khác nhau với các miền ... [truncated 225 chars](659 chars) |
| gán 2 $args cho một wp_query (28 chars) | pagenavi với wp_query hợp nhất Tôi cần sử dụng wp_query để thực thi bài viết từ 2 từ khóa riêng biệt sử dụng `s = từ khóa` vì vậy tôi đã tìm thấy câu trả lời này và nó rất hữu ích Kết hợp các truy vấn với các đối số khác nhau ... [truncated 225 chars](6097 chars) |
| Giúp với chức năng Walker trong Wordpress (41 chars) | Xác định xem mục điều hướng có con không Tôi đang cố gắng xác định xem một mục có mục con với độ sâu 1 hay không. Tôi không thể tìm thấy bất cứ điều gì về việc có một hàm/query nào đó mà tôi có thể viết để kiểm tra xem mục hi ... [truncated 225 chars](3671 chars) |
| Cách vô hiệu hóa WordPress từ tạo ra hình thu nhỏ? (50 chars) | Thêm hình ảnh không tạo ra hình thu nhỏ Tôi không chắc liệu yêu cầu của tôi có điên rồ hay hợp lý, nhưng tôi muốn kiểm soát cách mà hình ảnh của tôi được lưu trữ trong WordPress, tránh trường hợp một tập hợp các hình thu nhỏ ... [truncated 225 chars](346 chars) |
| Hình ảnh mặc định (logo) cho tùy chỉnh (38 chars) | wp_customize_image_control giá trị mặc định Tôi đang cố gắng tạo một chủ đề tùy chỉnh sử dụng tùy chọn tùy chỉnh trong Wordpress 3.4. Tôi muốn tạo một tùy chọn để thay đổi logo của chủ đề, nhưng tôi cũng muốn hiển thị hình ản ... [truncated 225 chars](993 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | cqadupstack_wordpress_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/cqadupstack-wordpress-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 337 |
| Avg positives / query | 1.69 |
| Positives per query (min / median / max) | 1 / 1 / 62 |
| Queries with multiple positives | 43 (21.50%) |
| BM25 nDCG@10 | 0.3170 |
| BM25 hit@10 | 0.4800 |
| Query length avg chars | 52.37 |
| Document length avg chars | 1,028.81 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/cqadupstack-wordpress-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/cqadupstack-wordpress-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | https://doi.org/10.1145/2838931.2838934 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/cqadupstack-wordpress-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: cqadupstack_wordpress_vn
  split_name: cqadupstack_wordpress_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/cqadupstack_wordpress_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
      - https://aclanthology.org/2026.findings-eacl.86/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 337
  positives_per_query:
    average: 1.685
    min: 1
    median: 1.0
    max: 62
    multi_positive_queries: 43
    multi_positive_query_percent: 21.5
  text_stats_chars:
    query_mean: 52.37
    document_mean: 1028.81
  bm25:
    ndcg_at_10: 0.316960341
    hit_at_10: 0.48
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "translated VN-MTEB CQADupStack WordPress test split from GreenNode/cqadupstack-wordpress-vn"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated WordPress test questions, documents, qrels, and duplicate clusters used by this Nano split."
    useful_training_data:
      - non-overlapping WordPress StackExchange duplicate-question pairs
      - Vietnamese WordPress support QA
      - WordPress documentation retrieval pairs
      - translated CQADupStack training splits with overlap removed
    synthetic_data:
      document_generation: "Vietnamese WordPress support threads preserving PHP snippets, hooks, template filenames, plugin names, and versions."
      question_generation: "Short Vietnamese duplicate titles asking the same WordPress theme, plugin, hook, or template-routing problem."
      answerability: "Each query should match the same WordPress behavior, with same-plugin but different-implementation negatives."
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
      - label: GreenNode/cqadupstack-wordpress-vn
        url: https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn
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
    - title: GreenNode/cqadupstack-wordpress-vn
      url: https://huggingface.co/datasets/GreenNode/cqadupstack-wordpress-vn
      year: null
      doi: null
      is_paper: false
      source_confidence: probably_correct
```
