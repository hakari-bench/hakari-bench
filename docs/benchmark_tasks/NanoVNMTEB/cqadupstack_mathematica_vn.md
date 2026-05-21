# NanoVNMTEB / cqadupstack_mathematica_vn

## Overview

VN-MTEB translates CQADupStack's Mathematica duplicate-question retrieval into
Vietnamese, preserving the source task's emphasis on finding previously asked
equivalent StackExchange questions. Queries are short translated Mathematica
titles, while documents are longer threads with code fragments, pattern syntax,
plotting calls, and held expressions. The observed topics include decimal
formatting, array construction with prescribed density, `ListPlot` data
preparation, and kernel behavior, so retrieval must connect Wolfram Language
operations across translated descriptions and code.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) targets duplicate
question retrieval in community QA, using StackExchange subforums with
predefined chronological retrieval splits. The paper reports that duplicate
questions often have low lexical overlap, making the task more than simple title
matching.

[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates the source
datasets into Vietnamese using an LLM-based translation and filtering pipeline.
For Mathematica, this means natural language is translated while code tokens and
Wolfram-specific syntax often remain in the documents.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 424 positive qrel rows.
The average is 2.12 positives per query; 71 queries have multiple positives and
the maximum is 56. Queries average 49.35 characters. Documents average 1,045.79
characters and frequently include code fragments such as function definitions,
pattern syntax, plotting functions, or held expressions.

The examples cover decimal formatting, constructing arrays with prescribed
density, preparing data for `ListVectorPlot[]`, numeric evaluation with `N@`,
and evaluating one step of an expression. Duplicate intent depends on both
Vietnamese prose and code semantics.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2114
and hit@10 = 0.3700. This is hard for lexical retrieval. Mathematica questions
can be short, code tokens may be sparse, and translated explanations can differ
while describing the same programming operation.

Dense models need to preserve both technical identifiers and the semantic role
of code constructs. Pure paraphrase matching is not enough when the duplicate
depends on evaluation behavior or data structure shape.

### Training Data That May Help

Useful training data includes non-overlapping Mathematica duplicate-question
pairs, Wolfram Language QA, translated CQADupStack training data with overlap
removed, and programming-question paraphrase data that preserves code. Exclude
the translated Mathematica test questions, qrels, documents, and duplicate
clusters used in this Nano split.

Hard negatives should share functions or syntax but ask a different computation
or evaluation behavior.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation Mathematica support threads
and generate short Vietnamese duplicate titles. Keep code identifiers, brackets,
patterns, and function names intact.

For joint generation, create clusters of Vietnamese Mathematica questions around
the same Wolfram Language task, with duplicate variants and hard negatives using
similar functions for different outcomes.

## Example Data

| Query | Positive document |
| --- | --- |
| nguồn giao nhau giữa hai đường cong trong Mathematica (53 chars) | Giao điểm của hai đường cong bậc hai Tôi có một tập hợp các tập hợp điểm, mỗi tập hợp xác định phân đoạn của một đường cong (đẹp) trên cầu đơn vị $S^2 \subset \mathbb {R}^3$. Các điểm được tính toán bằng số học. Tôi bây giờ m ... [truncated 225 chars](2327 chars) |
| Mathematica và Python tích hợp? (31 chars) | Có cách nào để chạy Python từ Mathematica không? Tôi biết có một số hỗ trợ cho việc chạy _Mathematica_ từ Python, nhưng có cách nào để làm ngược lại không? Ví dụ như nhập một vài lớp Python và sử dụng chúng trong _Mathematica ... [truncated 225 chars](228 chars) |
| Cách tránh lỗi NIntegrate::slwcon (33 chars) | Làm thế nào để tính tích phân số học của một hàm, mà kết quả phải là 0? Tôi muốn tích phân số học hàm 'berrycur' theo kx và ky. Định nghĩa của 'berrycur' được đưa ra ở cuối câu hỏi. Đồ thị của 'berrycur[kx,ky,1]' được hiển th ... [truncated 225 chars](3054 chars) |
| Truyền hàm hoặc công thức như là tham số của hàm (48 chars) | Truyền một hàm như một tham số của một hàm khác > **Có thể trùng lặp:** > Pass hàm hoặc công thức như tham số hàm Tôi đang cố gắng thực hiện một hàm Plot[] giống nhau, với bản tóm tắt tương tự; lần thử đầu tiên (và duy nhất c ... [truncated 225 chars](909 chars) |
| Có cách nào để thêm các mũi tên dọc theo một đường cong tham số bên trong một hàm thao tác (Mathematica)? (105 chars) | Vẽ đồ thị của một tập hợp các đường cong (không phải là trường vectơ) trong không gian 3 chiều Hãy xem xét một tập hợp các quỹ đạo trong không gian 3D, có thể hội tụ. Bằng cách trực quan hóa các quỹ đạo như mũi tên kết quả sẽ ... [truncated 225 chars](3641 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | cqadupstack_mathematica_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/cqadupstack-mathematica-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 424 |
| Avg positives / query | 2.12 |
| Positives per query (min / median / max) | 1 / 1 / 56 |
| Queries with multiple positives | 71 (35.50%) |
| BM25 nDCG@10 | 0.2114 |
| BM25 hit@10 | 0.3700 |
| Query length avg chars | 49.35 |
| Document length avg chars | 1,045.79 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/cqadupstack-mathematica-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/cqadupstack-mathematica-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | https://doi.org/10.1145/2838931.2838934 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/cqadupstack-mathematica-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: cqadupstack_mathematica_vn
  split_name: cqadupstack_mathematica_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/cqadupstack_mathematica_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
      - https://aclanthology.org/2026.findings-eacl.86/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 424
  positives_per_query:
    average: 2.12
    min: 1
    median: 1.0
    max: 56
    multi_positive_queries: 71
    multi_positive_query_percent: 35.5
  text_stats_chars:
    query_mean: 49.345
    document_mean: 1045.7923
  bm25:
    ndcg_at_10: 0.211379253
    hit_at_10: 0.37
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "translated VN-MTEB CQADupStack Mathematica test split from GreenNode/cqadupstack-mathematica-vn"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated Mathematica test questions, documents, qrels, and duplicate clusters used by this Nano split."
    useful_training_data:
      - non-overlapping Mathematica duplicate-question pairs
      - Wolfram Language QA and documentation retrieval data
      - translated CQADupStack training splits with overlap removed
      - code-aware paraphrase pairs with identifiers preserved
    synthetic_data:
      document_generation: "Vietnamese Mathematica support threads with Wolfram Language code and explanation."
      question_generation: "Short Vietnamese duplicate titles preserving functions, symbols, and code syntax."
      answerability: "Each query should match duplicate programming intent, with same-function hard negatives."
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
      - label: GreenNode/cqadupstack-mathematica-vn
        url: https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn
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
    - title: GreenNode/cqadupstack-mathematica-vn
      url: https://huggingface.co/datasets/GreenNode/cqadupstack-mathematica-vn
      year: null
      doi: null
      is_paper: false
      source_confidence: probably_correct
```
