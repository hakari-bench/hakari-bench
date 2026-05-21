# NanoVNMTEB / msmarco_vn

## Overview

`msmarco_vn` is the Vietnamese MS MARCO passage retrieval task from VN-MTEB.
Queries are translated real web-search questions, and documents are translated
short web passages. The task tests passage retrieval for everyday information
needs such as weather, films, locations, schools, people, and definitions.

## Details

### What the Original Data Measures

[MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268)
introduces questions sampled from Bing search logs, human-generated answers, and
passages extracted from web documents retrieved by Bing. The paper emphasizes
that the questions are real user queries and that the passage-ranking component
uses relevant question-passage identifier pairs.

[BEIR](https://arxiv.org/abs/2104.08663) uses MS MARCO as a passage retrieval
benchmark and treats it as a major in-domain retrieval dataset for dense
retrievers. [VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/)
translates and filters the source data into Vietnamese.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 214 positive qrel rows.
Most queries are single-positive: the average is 1.07 positives per query, and
12 queries have multiple positives. Queries average 33.40 characters, the
shortest in this batch. Documents average 306.69 characters and resemble short
web snippets or answer passages.

Observed examples include New York weather, the cast of The Emoji Movie,
monthly temperatures in Clearwater, Michael B. Jordan's role in Creed, and
colleges near Staunton, Virginia. The task is broad-domain web search rather
than a single specialized corpus.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8519
and hit@10 = 0.9000. The short queries often contain entity names or location
phrases that make lexical retrieval strong, and the median first relevant rank
is 1.

Failures are likely when translated web-search phrasing is ambiguous, when a
query is underspecified, or when the relevant passage answers the need without
repeating the same surface words.

### Training Data That May Help

Useful training data includes official MS MARCO passage-ranking train data where
permitted, Vietnamese web-search query-passage pairs, multilingual search click
or answer-passage data, and translated MS MARCO data with overlap removed. The
translated dev queries, qrels, and positive passages used by this Nano split
should be excluded.

Because MS MARCO is widely used for training retrievers, overlap auditing is
especially important before using translated or multilingual variants.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation Vietnamese web snippets and
generate short search-style questions that the snippet answers directly. Include
weather, location, entertainment, education, person, and definition intents.

For joint generation, create concise web passages and realistic short
Vietnamese search queries, with hard negatives that share entities or locations
but answer a different attribute.

## Example Data

| Query | Positive document |
| --- | --- |
| Tác dụng của việc sử dụng pedialyte (35 chars) | Ngoài ra, nếu bạn đang hướng đến việc giảm cân thì lượng calo trong Pedialyte và nước tăng lực sẽ có thể làm mất tác dụng của những bài tập vừa phải. Tuy nhiên, bù nước bằng một loại thức uống như Pedialyte cho phép cơ thể tá ... [truncated 225 chars](711 chars) |
| hiệu ứng lâu dài của ô nhiễm không khí tác động lên con người là gì? (68 chars) | Khó thở, ho, đau ngực và khó thở. ï§ Ho ra nhiều hơn hoặc nặng hơn. ï§ Tăng nguy cơ bị bệnh tim mạch. Ngoài ra, tiếp xúc lâu dài với ô nhiễm không khí có thể gây ung thư và làm tổn thương hệ miễn dịch, thần kinh, sinh sản v ... [truncated 225 chars](234 chars) |
| Quá trình tế bào nào đòi hỏi năng lượng (39 chars) | Có nhiều hơn nữa, những cái này chỉ là một vài ví dụ! [ATP (adenosine triphosphate) được dùng cho việc chuyển năng lượng trong tế bào nhưng nó không phải là hợp chất duy nhất được sử dụng. NTP, ADP, GTP & UTP để nêu ra một và ... [truncated 225 chars](474 chars) |
| Coca Cola có bao nhiêu dòng sản phẩm? (37 chars) | COCA-COLA ON SOCIAL. Coca-Cola Great Britain chịu trách nhiệm tiếp thị 20 nhãn hiệu và hơn 80 loại nước giải khát cho người tiêu dùng trên khắp Vương quốc Anh bao gồm danh mục Coca-Cola – Coca-Cola Classic, Coca-Cola Life, Co ... [truncated 225 chars](257 chars) |
| Thời tiết ở sao miguel (22 chars) | SÃ£o Miguel - Dự báo thời tiết từ Theweather.com. Điều kiện thời tiết với cập nhật về nhiệt độ, độ ẩm, tốc độ gió, tuyết, áp suất, v.v... cho SÃ£o Miguel , Coimbra Hôm nay: Trời quang đãng trong ngày hôm nay và tối trời vào b ... [truncated 225 chars](294 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | msmarco_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/msmarco-vn](https://huggingface.co/datasets/GreenNode/msmarco-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 214 |
| Avg positives / query | 1.07 |
| Positives per query (min / median / max) | 1 / 1 / 3 |
| Queries with multiple positives | 12 (6.00%) |
| BM25 nDCG@10 | 0.8519 |
| BM25 hit@10 | 0.9000 |
| Query length avg chars | 33.40 |
| Document length avg chars | 306.69 |

### Public Sources

- [MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268), 2016.
- [MS MARCO official page](https://microsoft.github.io/msmarco/), official dataset page.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/msmarco-vn](https://huggingface.co/datasets/GreenNode/msmarco-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/msmarco-vn](https://huggingface.co/datasets/GreenNode/msmarco-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | arXiv paper | https://arxiv.org/abs/1611.09268 |
| MS MARCO official page |  | project page | https://microsoft.github.io/msmarco/ |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/msmarco-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/msmarco-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: msmarco_vn
  split_name: msmarco_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/msmarco_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/1611.09268
    additional_source_urls:
      - https://microsoft.github.io/msmarco/
      - https://aclanthology.org/2026.findings-eacl.86/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/GreenNode/msmarco-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 214
  positives_per_query:
    average: 1.07
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 12
    multi_positive_query_percent: 6.0
  text_stats_chars:
    query_mean: 33.395
    document_mean: 306.69
  bm25:
    ndcg_at_10: 0.851862851
    hit_at_10: 0.9
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "translated VN-MTEB MS MARCO dev split from GreenNode/msmarco-vn"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated MS MARCO-VN dev queries, qrels, and positive passages used by this Nano split."
    useful_training_data:
      - official MS MARCO passage-ranking train data with overlap removed
      - Vietnamese web-search query-passage pairs
      - multilingual search click or answer-passage data
      - translated MS MARCO data with overlap removed
    synthetic_data:
      document_generation: "Vietnamese short web passages answering everyday search intents."
      question_generation: "Short Vietnamese web-search queries with entity, weather, location, entertainment, education, and definition intents."
      answerability: "Each query should be directly answerable from the positive passage, with same-entity different-attribute negatives."
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
      - label: MS MARCO arXiv
        url: https://arxiv.org/abs/1611.09268
      - label: MS MARCO official page
        url: https://microsoft.github.io/msmarco/
      - label: VN-MTEB ACL Anthology
        url: https://aclanthology.org/2026.findings-eacl.86/
      - label: BEIR arXiv
        url: https://arxiv.org/abs/2104.08663
      - label: GreenNode/msmarco-vn
        url: https://huggingface.co/datasets/GreenNode/msmarco-vn
    source_notes: []
  references:
    - title: "MS MARCO: A Human Generated MAchine Reading COmprehension Dataset"
      url: https://arxiv.org/abs/1611.09268
      year: 2016
      doi: 10.48550/arXiv.1611.09268
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
    - title: GreenNode/msmarco-vn
      url: https://huggingface.co/datasets/GreenNode/msmarco-vn
      year: null
      doi: null
      is_paper: false
      source_confidence: probably_correct
```
