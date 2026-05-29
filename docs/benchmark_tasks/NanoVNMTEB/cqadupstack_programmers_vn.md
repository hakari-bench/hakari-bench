# NanoVNMTEB / cqadupstack_programmers_vn

## Overview

CQADupStack defines this source family as retrieval of earlier StackExchange
questions manually flagged as duplicates; VN-MTEB translates and filters those
examples into Vietnamese. In the Programmers split, short translated software
engineering titles retrieve longer archived threads. The observed data covers
keeping up with tools, data structures and algorithms, internships, software
process, design, career choices, and programming practice, so the task asks for
duplicate intent matching over long engineering discussions rather than code
snippet retrieval.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) was built from twelve
StackExchange communities to evaluate duplicate-question retrieval in community
QA. The paper emphasizes that the retrieval setting should return earlier
questions that were manually flagged as duplicates, and that duplicate and
non-duplicate pairs have heavily overlapping lexical-similarity distributions.

[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates source
benchmark samples into Vietnamese with LLM translation, language filtering,
semantic-similarity filtering, and LLM-as-judge checks. In this split, software
engineering terminology is translated while product names, APIs, and program
identifiers may remain in English.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 490 positive qrel rows.
The average is 2.45 positives per query; 74 queries have multiple positives and
the maximum is 32. Queries average 58.73 characters. Documents average 1,070.56
characters and often read like full StackExchange posts with background,
constraints, code or tool names, and career context.

Observed examples cover keeping up with new tools, whether to invest in data
structures and algorithms, internships and Google Summer of Code, leaving a job,
and boolean parameters that change behavior. This is not only API lookup: many
queries ask for equivalent software-engineering judgments expressed with
different framing.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3438
and hit@10 = 0.5550. Lexical retrieval can use terms such as Selenium, GSoC,
algorithm, or boolean, but it often has to distinguish duplicate intent from
nearby programming discussion.

The median first relevant BM25 rank is 8, so a lexical baseline often finds at
least one duplicate in the top ranks but leaves substantial room for semantic
matching across paraphrased design and career questions.

### Training Data That May Help

Useful training data includes non-overlapping Programmers or Software
Engineering StackExchange duplicate pairs, Vietnamese developer QA, translated
CQADupStack training splits after overlap removal, and hard negatives from the
same topic but a different design decision. The translated test questions,
qrels, documents, and duplicate clusters used by this Nano split should be
excluded.

Training should preserve multi-positive supervision rather than reducing each
query to one duplicate, because more than one third of queries have multiple
positives.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation software-engineering QA
threads and create Vietnamese duplicate titles that ask the same engineering
decision in shorter or differently framed language. Preserve product names,
code identifiers, licensing terms, and project constraints.

For joint generation, create clusters of Vietnamese software-engineering
questions around one decision, plus hard negatives that share tools or keywords
but ask a different intent. Do not seed generation from this evaluation split's
queries or positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| Thư viện so với khung so với API? (33 chars) | Sự khác biệt giữa API, thư viện, runtime và khung làm việc là gì? > **Có thể trùng lặp:** > Thư viện so với framework so với API? Tôi đang gặp khó khăn trong việc hiểu những khái niệm này thực sự có nghĩa là gì. "Stack phần m ... [truncated 225 chars](523 chars) |
| Điều kiện tiên quyết để trở thành kiến trúc sư kỹ thuật (55 chars) | Những điều cần thiết để trở thành kiến trúc sư kỹ thuật tốt là gì? Tôi chỉ tò mò muốn biết làm thế nào để trở thành một kiến trúc sư kỹ thuật tốt. Hoặc những điều gì tạo nên một nhà phát triển kiến trúc tốt. Hãy chia sẻ ý kiế ... [truncated 225 chars](248 chars) |
| Java phát triển giải pháp server-client (39 chars) | Tôi nên tiếp cận phát triển ứng dụng client-server dựa trên Java như thế nào? Tôi đã được yêu cầu phát triển một ứng dụng khách hàng-máy chủ (yêu cầu cơ sở dữ liệu) cho một công ty. Tôi rất thành thạo Java và muốn sử dụng nó. ... [truncated 225 chars](1358 chars) |
| Nếu tôi sử dụng .NET Framework cho ứng dụng của mình, tôi có phải trả tiền cho Microsoft không? (95 chars) | Tôi muốn bán phần mềm của tôi [ứng dụng C # trên máy tính để bàn] nhưng tôi bị kẹt trong giấy phép > **Có thể trùng lặp:** > nếu tôi sử dụng .NET Framework cho ứng dụng của tôi, tôi có phải trả tiền gì cho Microsoft không? Tô ... [truncated 225 chars](1258 chars) |
| Về cách sử dụng của các khẳng định (34 chars) | Sử dụng những khẳng định so với ném ngoại lệ? Khi viết một hàm thường tôi muốn chắc rằng đầu vào cho nó là hợp lệ để phát hiện các lỗi càng sớm càng tốt (tôi nghĩ những điều này được gọi là tiền điều kiện). Khi một tiền điều ... [truncated 225 chars](497 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | cqadupstack_programmers_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/cqadupstack-programmers-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-programmers-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 490 |
| Avg positives / query | 2.45 |
| Positives per query (min / median / max) | 1 / 1 / 32 |
| Queries with multiple positives | 74 (37.00%) |
| BM25 nDCG@10 | 0.3568 |
| BM25 hit@10 | 0.5500 |
| BM25 Recall@100 | 0.5388 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4294 |
| Dense hit@10 | 0.6400 |
| Dense Recall@100 | 0.6306 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4229 |
| Reranking hybrid hit@10 | 0.6350 |
| Reranking hybrid Recall@100 | 0.6388 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 27 |
| Query length avg chars | 58.73 |
| Document length avg chars | 1,070.56 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/cqadupstack-programmers-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-programmers-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/cqadupstack-programmers-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-programmers-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | https://doi.org/10.1145/2838931.2838934 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/cqadupstack-programmers-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/cqadupstack-programmers-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: cqadupstack_programmers_vn
  split_name: cqadupstack_programmers_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/cqadupstack_programmers_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/cqadupstack-programmers-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 490
  positives_per_query:
    average: 2.45
    min: 1
    median: 1.0
    max: 32
    multi_positive_queries: 74
    multi_positive_query_percent: 37.0
  text_stats_chars:
    query_mean: 58.73
    document_mean: 1070.557
  bm25:
    ndcg_at_10: 0.35680960307366844
    hit_at_10: 0.55
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB CQADupStack Programmers test split
      from GreenNode/cqadupstack-programmers-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated Programmers test questions, documents, qrels,
      and duplicate clusters used by this Nano split.
    useful_training_data:
    - non-overlapping Programmers StackExchange duplicate-question pairs
    - Vietnamese software-engineering QA
    - translated CQADupStack training splits with overlap removed
    - same-topic software-design hard negatives
    synthetic_data:
      document_generation: Vietnamese software-engineering QA threads with tools,
        APIs, design constraints, and career context.
      question_generation: Short Vietnamese duplicate titles asking the same software-engineering
        decision.
      answerability: Each query should match the duplicate engineering intent, with
        same-tool but different-intent negatives.
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
    - label: GreenNode/cqadupstack-programmers-vn
      url: https://huggingface.co/datasets/GreenNode/cqadupstack-programmers-vn
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
  - title: GreenNode/cqadupstack-programmers-vn
    url: https://huggingface.co/datasets/GreenNode/cqadupstack-programmers-vn
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
      ndcg_at_10: 0.3568096031
      hit_at_10: 0.55
      recall_at_100: 0.5387755102
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5387755102
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4294210014
      hit_at_10: 0.64
      recall_at_100: 0.6306122449
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6306122449
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4229354048
      hit_at_10: 0.635
      recall_at_100: 0.6387755102
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.135
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6387755102
      safeguard_positive_rows: 27
      rows_with_101_candidates: 27
```
