# NanoVNMTEB / climate_fever_vn

## Overview

`climate_fever_vn` is the Vietnamese Climate-FEVER retrieval task from VN-MTEB.
Queries are translated real-world climate claims, and documents are translated
Wikipedia evidence passages. The task tests evidence retrieval for climate
fact-checking, where relevant passages may support, refute, or otherwise inform
the claim.

## Details

### What the Original Data Measures

[CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614)
collects 1,535 real-world climate claims from the web and annotates 7,675
claim-evidence pairs. The paper adapts the FEVER methodology to climate
misinformation and emphasizes that real climate claims are subtler than
artificial FEVER claims, sometimes producing disputed evidence.

[BEIR](https://arxiv.org/abs/2104.08663) uses Climate-FEVER as a fact-checking
retrieval task with claims as queries and Wikipedia evidence as documents.
[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates and
filters the source data into Vietnamese, so this task evaluates translated
Vietnamese climate evidence retrieval.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 635 positive qrel rows.
It is highly multi-positive: the average is 3.17 positives per query, the median
is 3, and 93% of queries have multiple positives. Queries average 129.97
characters and are complete climate claims. Documents average 407.08 characters
and are Wikipedia-style evidence passages, sometimes with page-title prefixes.

The sampled positives include broad climate and science entities such as Gulf
Stream, climate models, greenhouse gases, Oxford, and sea level. Some positives
look topically indirect, reflecting the original task's evidence-retrieval
framing and the difficulty of climate claims that require context.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2780
and hit@10 = 0.6700. The hit rate is moderate, but nDCG is low for a task with
several positives per query. Lexical overlap helps when claims name a climate
term, but evidence often uses different phrasing, background pages, or related
scientific concepts.

Models need to retrieve multiple relevant evidence passages and not just the
nearest climate-related page. Translation artifacts can also weaken exact term
matching.

### Training Data That May Help

Useful training data includes the official Climate-FEVER training material where
permitted, FEVER-style claim-evidence data, Vietnamese scientific or climate
fact-checking pairs, and translated climate evidence data with overlap removed.
The translated VN-MTEB test queries, qrels, and positive evidence passages should
not be used for training.

Because most queries have multiple positives, multi-positive training or listwise
distillation is more appropriate than treating each claim as a single answer.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation Vietnamese climate
or encyclopedia passages and generate claims that are explicitly supported or
refuted by the evidence. Include numeric claims, causal claims, and claims about
sea level, emissions, temperature, ice, and climate models.

For joint generation, create small evidence sets around a climate claim, with
supporting, refuting, and insufficient-evidence passages. Hard negatives should
share climate terminology but fail to validate the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Ở Alaska, gấu nâu đang thay đổi thói quen ăn uống của chúng để ăn quả mâm xôi chín sớm hơn. (91 chars) | Gấu nâu Gấu nâu (Ursus arctos) là một loài gấu lớn với sự phân bố rộng nhất trong số các loài gấu còn sinh tồn. Loài này được tìm thấy ở hầu hết các vùng phía bắc của châu Âu và Bắc Mỹ. Đây là một trong hai loài ăn thịt lớn n ... [truncated 225 chars](1643 chars) |
| Chúng ta sẽ phải đối mặt với nhiệt độ cực cao, nhưng ở mức độ dễ chịu hơn rất nhiều so với nếu chúng ta không làm gì để ngăn chặn biến đổi khí hậu. (147 chars) | Thay đổi khí hậu và giới tính Thay đổi khí hậu và giới tính liên quan đến sự khác biệt về giới trong bối cảnh thay đổi khí hậu và các mối quan hệ quyền lực phức tạp, đan xen phát sinh từ đó. Bằng cách thay đổi hệ sinh thái củ ... [truncated 225 chars](1439 chars) |
| Họ nói với chúng ta rằng chúng ta là những lực lượng chính điều khiển nhiệt độ trên Trái Đất bằng cách đốt cháy nhiên liệu hóa thạch và giải phóng khí carbon dioxide ra môi trường. (180 chars) | Khí cacbonic Khí cacbonic ( công thức hóa học: CO2) là một khí vô màu với mật độ cao hơn khoảng 60% so với không khí (1,225 g/L), ở nồng độ thông thường nó không có mùi. Khí cacbonic bao gồm một nguyên tử cacbon liên kết đôi ... [truncated 225 chars](1882 chars) |
| Nhai nhổ bọt của bò gây tác hại đến khí hậu hơn tất cả những chiếc xe hơi trên hành tinh này. (93 chars) | Trái Đất Trái Đất ( từ Eorðe -LSB- Γαῖα , Gaia -RSB- Terra ) , còn được gọi là Thế giới hay Trái cầu, là hành tinh thứ ba tính từ Mặt Trời và là vật thể duy nhất trong vũ trụ được biết đến có sự sống. Đây là hành tinh có khối ... [truncated 225 chars](978 chars) |
| Ngoài ra [mô hình khí hậu] bỏ qua thực tế là việc làm giàu khí quyển với CO2 có lợi. (84 chars) | Giảm nhẹ biến đổi khí hậu Giảm nhẹ biến đổi khí hậu bao gồm các hành động nhằm hạn chế mức độ hoặc tốc độ của biến đổi khí hậu trong dài hạn. Giảm nhẹ biến đổi khí hậu nói chung liên quan đến việc giảm phát thải khí nhà kính ... [truncated 225 chars](2205 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | climate_fever_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/climate-fever-vn](https://huggingface.co/datasets/GreenNode/climate-fever-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 635 |
| Avg positives / query | 3.17 |
| Positives per query (min / median / max) | 1 / 3 / 5 |
| Queries with multiple positives | 186 (93.00%) |
| BM25 nDCG@10 | 0.2780 |
| BM25 hit@10 | 0.6700 |
| Query length avg chars | 129.97 |
| Document length avg chars | 407.08 |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614), 2020.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/climate-fever-vn](https://huggingface.co/datasets/GreenNode/climate-fever-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/climate-fever-vn](https://huggingface.co/datasets/GreenNode/climate-fever-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | arXiv paper | https://arxiv.org/abs/2012.00614 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/climate-fever-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/climate-fever-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: climate_fever_vn
  split_name: climate_fever_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/climate_fever_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2012.00614
    additional_source_urls:
      - https://aclanthology.org/2026.findings-eacl.86/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/GreenNode/climate-fever-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 635
  positives_per_query:
    average: 3.175
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 186
    multi_positive_query_percent: 93.0
  text_stats_chars:
    query_mean: 129.965
    document_mean: 407.0829
  bm25:
    ndcg_at_10: 0.278029502
    hit_at_10: 0.67
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: "translated VN-MTEB ClimateFEVER test split from GreenNode/climate-fever-vn"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated ClimateFEVER-VN test claims, qrels, and positive evidence passages used by this Nano split."
    useful_training_data:
      - official Climate-FEVER claim-evidence data with overlap removed
      - FEVER-style claim verification retrieval pairs
      - Vietnamese climate and science fact-checking data
      - multilingual climate evidence retrieval pairs
    synthetic_data:
      document_generation: "Vietnamese climate evidence passages with scientific entities, numbers, and causal statements."
      question_generation: "Vietnamese climate claims that require retrieving supporting or refuting evidence."
      answerability: "Claims should have multiple explicit evidence positives and climate-topic hard negatives."
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
      - label: CLIMATE-FEVER arXiv
        url: https://arxiv.org/abs/2012.00614
      - label: VN-MTEB ACL Anthology
        url: https://aclanthology.org/2026.findings-eacl.86/
      - label: BEIR arXiv
        url: https://arxiv.org/abs/2104.08663
      - label: GreenNode/climate-fever-vn
        url: https://huggingface.co/datasets/GreenNode/climate-fever-vn
    source_notes: []
  references:
    - title: "CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims"
      url: https://arxiv.org/abs/2012.00614
      year: 2020
      doi: 10.48550/arXiv.2012.00614
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
    - title: GreenNode/climate-fever-vn
      url: https://huggingface.co/datasets/GreenNode/climate-fever-vn
      year: null
      doi: null
      is_paper: false
      source_confidence: probably_correct
```
