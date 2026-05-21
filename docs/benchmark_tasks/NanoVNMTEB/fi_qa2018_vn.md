# NanoVNMTEB / fi_qa2018_vn

## Overview

`fi_qa2018_vn` is the Vietnamese FiQA 2018 retrieval task from VN-MTEB. Queries
are translated financial questions, and documents are translated answer posts or
financial discussion snippets. The task tests retrieval for investor-oriented
questions involving funds, transfers, taxation, real estate, equity returns, and
practical personal-finance decisions.

## Details

### What the Original Data Measures

[WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301)
defines FiQA tasks for aspect-based financial sentiment and opinion-based
question answering. For Task 2, the paper describes natural-language financial
questions over a knowledge base of 57,640 answer posts, with 17,110
question-answer pairs for training and 531 pairs for testing.

[BEIR](https://arxiv.org/abs/2104.08663) includes FiQA as a financial retrieval
task. [VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates and
filters the source data into Vietnamese, so the task evaluates finance-domain
Vietnamese retrieval rather than generic web QA.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 549 positive qrel rows.
The average is 2.745 positives per query; 129 queries have multiple positives
and the maximum is 15. Queries average 69.43 characters. Documents average
811.03 characters and are often longer, opinionated answers with caveats,
jurisdictional assumptions, and investment reasoning.

Observed examples include Vanguard ETFs versus mutual funds, sending money from
Australia to the UK while abroad, whether a company director can invoice their
own company, foreign real-estate investment in China, and the meaning of a
shareholder return headline. These require financial interpretation, not only
keyword matching.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3112
and hit@10 = 0.5650. Lexical cues such as ETF, Vanguard, director, China, or
shareholder return help, but relevant answers often use explanatory language
instead of repeating the exact question wording.

The median first relevant BM25 rank is 6. The task rewards retrievers that can
match the financial situation, jurisdiction, and instrument type while avoiding
same-topic but advice-incompatible answers.

### Training Data That May Help

Useful training data includes the official non-overlapping FiQA training pairs,
finance-domain QA, Vietnamese personal-finance and investment QA, financial
forum answer ranking data, and translated finance retrieval data with overlap
removed. The translated test questions, qrels, and positive answers used by this
Nano split should be excluded.

Financial data should be filtered carefully for stale, jurisdiction-specific, or
advice-like content when used outside benchmarking.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation financial answer posts and
generate Vietnamese questions about the same decision, product, tax situation,
or transfer scenario. Preserve currencies, account types, jurisdictions,
company roles, and investment products.

For joint generation, create realistic financial Q&A pairs with explicit
assumptions and caveats. Include hard negatives that share the same product or
country but answer a different financial decision.

## Example Data

| Query | Positive document |
| --- | --- |
| "Sell on ask", "sell on bid" trong chứng khoán là gì? (53 chars) | Giá mua (bid) và giá bán (ask) là mức giá cao nhất để mua và thấp nhất để bán trên thị trường, điều đó không có nghĩa là bạn chỉ nên mua/bán ở mức giá này. Tuy nhiên bạn có thể mua/bán theo mức giá mà bạn muốn mặc dù việc thự ... [truncated 225 chars](489 chars) |
| Giải thích chi phí sinh viên - Để khai thuế cho năm tiếp theo (61 chars) | Giả sử ở đây bạn đang nói về việc khấu trừ học phí của bạn như một khoản khấu trừ dưới mức cơ bản như một chi phí kinh doanh hoặc tương tự, sau đó nó phụ thuộc. Theo 1.162-5, nếu giáo dục: Sau đó nó được coi là một chi phí ki ... [truncated 225 chars](966 chars) |
| Điều gì xảy ra với "người mua dài" của một cổ phiếu khi người bán ngắn khác thất bại (đó là, thua lỗ không giới hạn phá sản người bán ngắn) (139 chars) | Nếu không có gì tinh tế mà tôi bỏ lỡ, chẳng có gì xảy ra với người mua. Giả sử Alice muốn bán khống 1000 cổ phiếu XYZ ở mức $5. Cô ta vay cổ phiếu từ Bob và bán chúng cho Charlie. Bây giờ Charlie thực sự sở hữu cổ phiếu; chún ... [truncated 225 chars](1159 chars) |
| Tôi có nên thay thế trái phiếu trong một chiến lược đầu tư thụ động không? (74 chars) | "Trái phiếu vẫn chắc chắn có một chỗ đứng trong nhiều danh mục đầu tư thụ động. Mặc dù đúng là lãi suất đã ở mức thấp bất thường, nhưng lợi suất trên các khoản đầu tư trái phiếu thụ động hợp lý vẫn dao động từ 2-4%. Đây là mứ ... [truncated 225 chars](2213 chars) |
| 28 tuổi vừa thừa kế một số tiền lớn và bất động sản - không biết làm gì với nó (78 chars) | Chúng tôi không có một câu trả lời tốt cho việc bắt đầu đầu tư ở Ba Lan. Chúng tôi đã có những câu trả lời tốt cho trường hợp nói chung, mà cũng nên áp dụng ở Ba Lan. Ví dụ: Cách tốt nhất để bắt đầu đầu tư, đối với một người ... [truncated 225 chars](4316 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | fi_qa2018_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/fiqa-vn](https://huggingface.co/datasets/GreenNode/fiqa-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 549 |
| Avg positives / query | 2.75 |
| Positives per query (min / median / max) | 1 / 2 / 15 |
| Queries with multiple positives | 129 (64.50%) |
| BM25 nDCG@10 | 0.3112 |
| BM25 hit@10 | 0.5650 |
| Query length avg chars | 69.43 |
| Document length avg chars | 811.03 |

### Public Sources

- [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301), 2018.
- [FiQA project page](https://sites.google.com/view/fiqa/), official challenge page.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/fiqa-vn](https://huggingface.co/datasets/GreenNode/fiqa-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/fiqa-vn](https://huggingface.co/datasets/GreenNode/fiqa-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WWW'18 Open Challenge: Financial Opinion Mining and Question Answering | 2018 | ACM paper | https://doi.org/10.1145/3184558.3192301 |
| FiQA project page |  | project page | https://sites.google.com/view/fiqa/ |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/fiqa-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/fiqa-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: fi_qa2018_vn
  split_name: fi_qa2018_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/fi_qa2018_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/3184558.3192301
    additional_source_urls:
      - https://sites.google.com/view/fiqa/
      - https://aclanthology.org/2026.findings-eacl.86/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/GreenNode/fiqa-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 549
  positives_per_query:
    average: 2.745
    min: 1
    median: 2.0
    max: 15
    multi_positive_queries: 129
    multi_positive_query_percent: 64.5
  text_stats_chars:
    query_mean: 69.43
    document_mean: 811.031
  bm25:
    ndcg_at_10: 0.311195336
    hit_at_10: 0.565
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "translated VN-MTEB FiQA2018 test split from GreenNode/fiqa-vn"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated FiQA-VN test questions, qrels, and positive answers used by this Nano split."
    useful_training_data:
      - official FiQA training question-answer pairs with overlap removed
      - Vietnamese personal-finance and investment QA
      - finance-domain forum answer ranking data
      - translated financial QA data with overlap removed
    synthetic_data:
      document_generation: "Vietnamese financial answer posts with currencies, jurisdictions, account types, and product names."
      question_generation: "Vietnamese investor or personal-finance questions answerable from those posts."
      answerability: "Questions should require the same financial decision context, with same-product but different-advice negatives."
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
      - label: FiQA DOI
        url: https://doi.org/10.1145/3184558.3192301
      - label: FiQA project page
        url: https://sites.google.com/view/fiqa/
      - label: VN-MTEB ACL Anthology
        url: https://aclanthology.org/2026.findings-eacl.86/
      - label: BEIR arXiv
        url: https://arxiv.org/abs/2104.08663
      - label: GreenNode/fiqa-vn
        url: https://huggingface.co/datasets/GreenNode/fiqa-vn
    source_notes: []
  references:
    - title: "WWW'18 Open Challenge: Financial Opinion Mining and Question Answering"
      url: https://doi.org/10.1145/3184558.3192301
      year: 2018
      doi: 10.1145/3184558.3192301
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
    - title: GreenNode/fiqa-vn
      url: https://huggingface.co/datasets/GreenNode/fiqa-vn
      year: null
      doi: null
      is_paper: false
      source_confidence: probably_correct
```
