# NanoVNMTEB / argu_ana_vn

## Overview

VN-MTEB translates ArguAna's counterargument retrieval task into Vietnamese:
each long debate argument must retrieve the best opposing argument, not a
same-stance topical neighbor. The original ArguAna paper frames this as
retrieving counterarguments without prior topic knowledge, balancing topic
match with stance opposition. In this Nano split, translated arguments about
airport expansion, BBC funding, blasphemy, organ donation, hip-hop censorship,
and meat eating require the retriever to follow the debated aspect and return a
direct counterposition.

## Details

### What the Original Data Measures

[Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/)
introduces the ArguAna Counterargs corpus, built from idebate.org debates with
6,753 argument-counterargument pairs across 1,069 debates. The paper frames the
task as retrieving the best counterargument to an argument without assuming prior
knowledge of the topic, balancing topical similarity with stance opposition.

[VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/)
translates source embedding datasets into Vietnamese using a pipeline with
language detection, Aya-23-35B translation, semantic-similarity filtering, and
LLM-as-judge quality scoring. This task is therefore a Vietnamese translated
counterargument retrieval benchmark, not a natively authored Vietnamese debate
corpus.

### Observed Data Profile

The Nano split has 199 queries, 8,674 documents, and 199 positive qrel rows.
Every query has exactly one positive. Queries are long Vietnamese translated
arguments, averaging 1,183.88 characters. Documents average 1,080.34 characters
and often begin with debate-topic metadata followed by the opposing argument.

The examples cover airport expansion, BBC funding and blasphemy, organ donation,
hip-hop censorship, and meat eating. The positive document usually shares the
broad subject with the query while taking the opposite argumentative stance.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2591
and hit@10 = 0.5678. This is a difficult lexical task. Long arguments contain
many shared topical terms, but the relevant counterargument must oppose or
undercut the query rather than simply discuss the same theme.

The single-positive qrels make near misses costly: a same-topic argument with
the wrong stance receives no credit. Vietnamese translation also introduces
occasional awkward phrasing, so models need robust argument-level semantics.

### Training Data That May Help

Useful training data includes non-overlapping Vietnamese argument-counterargument
pairs, translated ArguAna training material with test overlap removed, debate
forum data with stance labels, and multilingual argument-mining corpora adapted
to Vietnamese. Training should exclude the translated ArguAna test queries,
qrels, and positive documents used in this Nano split.

Hard negatives should be same-topic arguments with the same or ambiguous stance,
because broad topic matching alone is insufficient.

### Synthetic Data Guidance

For document-to-query generation, start from Vietnamese counterarguments and
generate long opposing arguments that the document can rebut. Keep the query as
a full argumentative paragraph with claim and premises.

For joint generation, create paired Vietnamese debate arguments and
counterarguments on policy, ethics, health, technology, and education topics.
Include stance-near hard negatives so training rewards counterargument matching,
not only topic retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| Quyền tự quyết cá nhân là quyền con người cơ bản, ngang hàng với quyền sống. Nguyên tắc cơ bản của con người là mỗi người sinh ra đều có tính chủ thể. Vì vậy chúng tôi tin rằng mọi người đều có quyền đối với cơ thể của mình v ... [truncated 225 chars](1001 chars) | triết lý y tế đạo đức nhà cho phép quyên góp các cơ quan quan trọng ngay cả chi phí Con người cũng là một sinh vật xã hội. Trong khi chúng ta có quyền đối với cơ thể của mình, chúng ta cũng có nghĩa vụ đối với những người xun ... [truncated 225 chars](818 chars) |
| Động vật thí nghiệm được đối xử tốt Động vật dùng trong nghiên cứu nói chung không bị đau khổ. Mặc dù chúng có thể bị đau, nhưng nói chung chúng được cho thuốc giảm đau, và khi chúng bị hạ sát thì việc này được thực hiện một ... [truncated 225 chars](559 chars) | thú vật khoa học khoa học đại chúng thử nghiệm trên động vật Chỉ vì một con vật được đối xử tốt khi nó được nuôi dưỡng không ngăn chặn nỗi đau rất thực tế trong khi thử nghiệm. Quy tắc nghiêm ngặt và thuốc giảm đau không giúp ... [truncated 225 chars](353 chars) |
| Việc xây dựng đường băng thứ ba sẽ gây ra vấn đề tiếng ồn và ô nhiễm. Mật độ dân cư cao trong khu vực xung quanh sân bay Heathrow cho thấy đây không phải là địa điểm lý tưởng để xây dựng một sân bay lớn hơn. Việc tăng sức chứ ... [truncated 225 chars](1302 chars) | kinh tế môi trường chung khí hậu môi trường chung ô nhiễm nhà ở Việc bổ sung đường băng không nhất thiết dẫn đến sự gia tăng đáng kể về ô nhiễm tiếng ồn, vì điều đó phụ thuộc vào vị trí đặt đường băng. Nếu đường băng được xây ... [truncated 225 chars](1124 chars) |
| Những va chạm là một phần của trò chơi. Đầu tiên, những va chạm là một phần truyền thống của bóng chày. Chúng đã tồn tại trong trò chơi từ rất lâu rồi. Người hâm mộ, cầu thủ và huấn luyện viên đều mong đợi những cú đánh vào s ... [truncated 225 chars](2102 chars) | đội thể thao tin rằng giải bóng chày nên tiếp tục cho phép va chạm Những va chạm ít xảy ra trong trò chơi hơn những gì mọi người nghĩ. Ý tưởng rằng những va chạm đã tồn tại từ lâu trong trò chơi là một quan niệm sai lầm được ... [truncated 225 chars](1659 chars) |
| Không có quyền không bị xúc phạm, việc thực thi những gì được cho là chấp nhận được để suy nghĩ hoặc nói đặt quá nhiều quyền lực vào tay nhà nước. Không thể đảm bảo rằng không ai bị xúc phạm và điều đó còn đáng nghi ngờ hơn n ... [truncated 225 chars](1230 chars) | Nhà ở khác biệt sống sẽ trừng phạt bài phát biểu thù hận tôn giáo Đây chỉ là một huyền thoại. Xã hội thường thường lập pháp để ngăn ngừa hành vi phạm tội bằng cách hạn chế những gì có thể nói hoặc làm trong phát sóng hay in ấ ... [truncated 225 chars](675 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | argu_ana_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/arguana-vn](https://huggingface.co/datasets/GreenNode/arguana-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 199 |
| Documents | 8,674 |
| Positive qrels | 199 |
| BM25 nDCG@10 | 0.2742 |
| BM25 hit@10 | 0.6030 |
| BM25 Recall@100 | 0.9548 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3698 |
| Dense hit@10 | 0.7889 |
| Dense Recall@100 | 0.9447 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3372 |
| Reranking hybrid hit@10 | 0.7387 |
| Reranking hybrid Recall@100 | 0.9799 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 1,183.88 |
| Document length avg chars | 1,080.34 |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/), 2018.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/arguana-vn](https://huggingface.co/datasets/GreenNode/arguana-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/arguana-vn](https://huggingface.co/datasets/GreenNode/arguana-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | ACL paper | https://aclanthology.org/P18-1023/ |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/arguana-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/arguana-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: argu_ana_vn
  split_name: argu_ana_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/argu_ana_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://aclanthology.org/P18-1023/
    additional_source_urls:
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/arguana-vn
    no_paper_note: null
  counts:
    queries: 199
    documents: 8674
    positive_qrels: 199
  positives_per_query:
    average: 1.0
    min: 1
    median: 1
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1183.879396985
    document_mean: 1080.336407655
  bm25:
    ndcg_at_10: 0.2742105725041169
    hit_at_10: 0.6030150753768844
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB ArguAna test split from GreenNode/arguana-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated ArguAna-VN test queries, qrels, and positive
      counterarguments used by this Nano split.
    useful_training_data:
    - non-overlapping Vietnamese argument-counterargument pairs
    - translated ArguAna training material with test overlap removed
    - Vietnamese debate or stance-labeled forum data
    - multilingual argument-mining corpora adapted to Vietnamese
    synthetic_data:
      document_generation: Vietnamese counterargument paragraphs with clear rebuttal
        targets.
      question_generation: Long Vietnamese arguments that can be answered by retrieving
        an opposing counterargument.
      answerability: Each generated query should have one explicit counterargument
        positive and same-topic hard negatives.
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: ArguAna ACL Anthology
      url: https://aclanthology.org/P18-1023/
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/arguana-vn
      url: https://huggingface.co/datasets/GreenNode/arguana-vn
    source_notes: []
  references:
  - title: Retrieval of the Best Counterargument without Prior Topic Knowledge
    url: https://aclanthology.org/P18-1023/
    year: 2018
    doi: 10.18653/v1/P18-1023
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
  - title: GreenNode/arguana-vn
    url: https://huggingface.co/datasets/GreenNode/arguana-vn
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
      ndcg_at_10: 0.2742105725
      hit_at_10: 0.6030150754
      recall_at_100: 0.9547738693
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9547738693
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3697788862
      hit_at_10: 0.7889447236
      recall_at_100: 0.9447236181
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9447236181
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3371939282
      hit_at_10: 0.7386934673
      recall_at_100: 0.9798994975
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.020101
      query_count: 199
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9798994975
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
