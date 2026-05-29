# NanoVNMTEB / sci_fact_vn

## Overview

VN-MTEB translates SciFact's scientific claim-verification retrieval problem
into Vietnamese. The source SciFact paper defines claims that must be supported
or refuted by scientific abstracts with rationale evidence; this Nano task uses
the retrieval part, with translated scientific claims as queries and translated
abstracts as documents. The sampled claims concern molecular mechanisms,
histone demethylase recruitment, KRAS-mutant tumors, and biomedical
associations, so retrieval must preserve scientific directionality and evidence
semantics across translation.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduces SciFact as a scientific claim verification task. The paper describes
1,409 expert-written scientific claims verified against a corpus of 5,183
abstracts, with evidence abstracts labeled as supporting or refuting claims and
with rationale sentences annotated.

[BEIR](https://arxiv.org/abs/2104.08663) uses SciFact as a scientific
fact-checking retrieval task. [VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/)
translates and filters the source data into Vietnamese, so this split evaluates
scientific evidence retrieval under translation.

### Observed Data Profile

The Nano split has 134 queries, 5,183 documents, and 155 positive qrel rows.
Most claims have one positive abstract; 13 claims have multiple positives and
the maximum is 5. Queries average 90.64 characters and are formal scientific
claims. Documents average 1,518.84 characters and are long biomedical or life
science abstracts.

Observed examples include claims about aPKCz and glutamine metabolism, histone
demethylase recruitment, PI3K/MEK inhibition for KRAS-mutant tumors, ALDH1 and
breast cancer prognosis, and lysine acetylation. Retrieval requires scientific
terminology and relation matching.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5954
and hit@10 = 0.7463. Domain terms such as KRAS, ALDH1, acetylation, and
glutamine help lexical retrieval, but scientific claims often require matching a
directional finding or experimental conclusion.

The median first relevant BM25 rank is 2, so lexical retrieval is useful but not
sufficient for robust evidence ranking.

### Training Data That May Help

Useful training data includes official SciFact training claims and abstracts
where permitted, biomedical claim-evidence retrieval pairs, scientific NLI or
fact-verification data, and translated scientific retrieval data with overlap
removed. The translated test claims, qrels, and positive abstracts used by this
Nano split should be excluded.

Hard negatives should share entities or interventions while contradicting or
omitting the claimed relation.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation scientific abstracts and
generate Vietnamese claims about explicit findings, interventions, biomarkers,
or biological mechanisms in the abstract.

For joint generation, create abstracts and support/refute claims with rationale
sentences. Preserve gene names, proteins, disease names, directions of effect,
measurements, and experimental context.

## Example Data

| Query | Positive document |
| --- | --- |
| Mức độ nghiêm trọng của bệnh tim liên quan đến amyloidosis có thể được mô tả bằng mức độ xuyên thành của sự tăng cường gadolinium muộn trong MRI. (145 chars) | Giá trị tiên lượng của quá trình tăng cường muộn gadolinium của cộng hưởng từ tim mạch trong bệnh tim amyloidosis BỐN MẠT LÝ NHIỆM: Dự đoán và điều trị 2 loại bệnh Amyloidosis tim chính, chuỗi nhẹ của immunoglobulin (AL) và A ... [truncated 225 chars](2127 chars) |
| Sildenafil cải thiện chức năng cương dương ở những người đàn ông bị rối loạn cương dương do sử dụng thuốc chống trầm cảm SSRI. (126 chars) | Điều trị rối loạn chức năng tình dục liên quan đến thuốc chống trầm cảm với sildenafil: một thử nghiệm có đối chứng. Bất lực là tác dụng phụ phổ biến của thuốc chống trầm cảm thường gây nên tình trạng không tuân thủ điều trị. ... [truncated 225 chars](2203 chars) |
| Căng thẳng ethanol làm giảm biểu hiện của IBP trong vi khuẩn. (61 chars) | Sự điều chỉnh và chuyển mạch trao hóa trong quá trình tiến hóa trong phòng thí nghiệm của độ dung nạp cồn ở E. coli Hiểu được cơ sở di truyền của sự thích nghi là một vấn đề trung tâm trong sinh học. Tuy nhiên, việc chỉ ra cá ... [truncated 225 chars](1545 chars) |
| Sự giao tiếp giữa tế bào dendritic (DCs) và tế bào bạch cầu lympho bản chất (ILCs) đóng vai trò quan trọng trong điều hòa cân bằng nội môi đường ruột. (150 chars) | Yếu tố phiên mã T-bet điều tiết viêm ruột được trung gian bởi tế bào lympho bẩm sinh thụ thể interleukin-7+ Chuột thiếu yếu tố phiên mã T-bet trong hệ miễn dịch bẩm sinh phát triển viêm đại tràng phụ thuộc vào vi khuẩn đường ... [truncated 225 chars](1347 chars) |
| Các tế bào đang trải qua hạn chế methionine có thể kích hoạt miRNAs. (68 chars) | microRNAs: Một biện pháp bảo vệ chống lại sự hỗn loạn? Dữ liệu gần đây cho thấy rằng microRNAs (miRNAs) đóng vai trò quan trọng trong các phản ứng căng thẳng ngoài vai trò được công nhận hơn của chúng trong quá trình phát tri ... [truncated 225 chars](554 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | sci_fact_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/scifact-vn](https://huggingface.co/datasets/GreenNode/scifact-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 134 |
| Documents | 5,183 |
| Positive qrels | 155 |
| Avg positives / query | 1.16 |
| Positives per query (min / median / max) | 1 / 1 / 5 |
| Queries with multiple positives | 13 (9.70%) |
| BM25 nDCG@10 | 0.6158 |
| BM25 hit@10 | 0.7537 |
| BM25 Recall@100 | 0.8774 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6636 |
| Dense hit@10 | 0.7836 |
| Dense Recall@100 | 0.9097 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6485 |
| Reranking hybrid hit@10 | 0.7612 |
| Reranking hybrid Recall@100 | 0.9290 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 10 |
| Query length avg chars | 90.64 |
| Document length avg chars | 1,518.84 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974), 2020.
- [SciFact GitHub repository](https://github.com/allenai/scifact), official dataset repository.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/scifact-vn](https://huggingface.co/datasets/GreenNode/scifact-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/scifact-vn](https://huggingface.co/datasets/GreenNode/scifact-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | arXiv paper | https://arxiv.org/abs/2004.14974 |
| SciFact GitHub repository |  | project page | https://github.com/allenai/scifact |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/scifact-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/scifact-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: sci_fact_vn
  split_name: sci_fact_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/sci_fact_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2004.14974
    additional_source_urls:
    - https://github.com/allenai/scifact
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/scifact-vn
    no_paper_note: null
  counts:
    queries: 134
    documents: 5183
    positive_qrels: 155
  positives_per_query:
    average: 1.157
    min: 1
    median: 1.0
    max: 5
    multi_positive_queries: 13
    multi_positive_query_percent: 9.701
  text_stats_chars:
    query_mean: 90.642
    document_mean: 1518.84
  bm25:
    ndcg_at_10: 0.6157620166338039
    hit_at_10: 0.753731343283582
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB SciFact test split from GreenNode/scifact-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated SciFact-VN test claims, qrels, and positive abstracts
      used by this Nano split.
    useful_training_data:
    - official SciFact training claims and abstracts with overlap removed
    - biomedical claim-evidence retrieval pairs
    - scientific NLI and fact-verification data
    - translated scientific retrieval data with overlap removed
    synthetic_data:
      document_generation: Vietnamese scientific abstracts preserving genes, proteins,
        disease names, measurements, and experimental context.
      question_generation: Vietnamese scientific claims about explicit findings, mechanisms,
        interventions, or biomarkers.
      answerability: Claims should be supported or refuted by rationale-bearing abstracts
        with entity-sharing hard negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: SciFact arXiv
      url: https://arxiv.org/abs/2004.14974
    - label: SciFact GitHub
      url: https://github.com/allenai/scifact
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/scifact-vn
      url: https://huggingface.co/datasets/GreenNode/scifact-vn
    source_notes: []
  references:
  - title: 'Fact or Fiction: Verifying Scientific Claims'
    url: https://arxiv.org/abs/2004.14974
    year: 2020
    doi: 10.48550/arXiv.2004.14974
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
  - title: GreenNode/scifact-vn
    url: https://huggingface.co/datasets/GreenNode/scifact-vn
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
      ndcg_at_10: 0.6157620166
      hit_at_10: 0.7537313433
      recall_at_100: 0.8774193548
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 134
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8774193548
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6635889042
      hit_at_10: 0.7835820896
      recall_at_100: 0.9096774194
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 134
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9096774194
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6485360114
      hit_at_10: 0.7611940299
      recall_at_100: 0.9290322581
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.074627
      query_count: 134
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9290322581
      safeguard_positive_rows: 10
      rows_with_101_candidates: 10
```
