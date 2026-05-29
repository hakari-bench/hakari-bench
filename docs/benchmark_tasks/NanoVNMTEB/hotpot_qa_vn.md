# NanoVNMTEB / hotpot_qa_vn

## Overview

HotpotQA was designed for explainable multi-hop question answering over
Wikipedia, with supporting facts for bridge and comparison questions. VN-MTEB
translates that retrieval view into Vietnamese. This Nano split keeps exactly
two positives per query, so a translated question must retrieve both supporting
passages needed for the reasoning chain. The sampled questions connect albums,
island kingdoms, athletes' relatives, draft years, and golf records, making
coverage of both linked entities more important than finding a single answer
string.

## Details

### What the Original Data Measures

[HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600)
introduces 113k Wikipedia-based question-answer pairs requiring reasoning over
multiple documents. The paper provides sentence-level supporting facts and
distinguishes bridge-entity questions from comparison questions.

[BEIR](https://arxiv.org/abs/2104.08663) uses HotpotQA as a retrieval task in
which systems must retrieve the supporting passages for the question.
[VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/) translates and
filters the source task into Vietnamese, preserving named entities and
multi-hop question structure.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 400 positive qrel rows.
Every query has exactly two positives. Queries average 99.53 characters and
often ask a composed relation involving two entities. Documents average 445.27
characters and are compact Wikipedia-style passages.

Observed examples ask for a song author from an album clue, an island kingdom
led by Aonghus Mor, a draft-year relation involving a football player's
brother, a golf championship record holder's worldwide wins, and the predecessor
state of a short-reigning Sasanian king. These are classic two-hop retrieval
needs.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8546
and hit@10 = 0.9850. Named entities and rare titles make the first supporting
page easy to find for most queries, with a median first relevant rank of 1.

However, hit@10 hides the full multi-hop requirement. A good retriever should
retrieve both supporting documents, not just the entity page that shares the
most query words.

### Training Data That May Help

Useful training data includes official non-overlapping HotpotQA training
examples, Vietnamese multi-hop QA, Wikipedia question-to-supporting-page pairs,
and translated multi-hop retrieval data with overlap removed. The translated
test questions, qrels, and positive supporting passages used by this Nano split
should be excluded.

Training should preserve paired positives and use multi-positive or listwise
objectives so both hops are rewarded.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation Vietnamese Wikipedia
passages and generate questions that require a bridge entity or comparison
between two entities. The generated question should require retrieving both
supporting passages.

For joint generation, create pairs of linked entity passages and Vietnamese
questions whose answer depends on their relation. Include hard negatives that
share one entity but do not complete the second hop.

## Example Data

| Query | Positive document |
| --- | --- |
| Đội bóng rổ nam đại học VCU Rams 2011-12, dẫn dắt bởi huấn luyện viên trưởng năm thứ ba Shaka Smart, đại diện cho trường Đại học Virginia Commonwealth được thành lập vào năm nào? (178 chars) | Đội bóng rổ nam VCU Rams mùa 2011–12 Đội bóng rổ nam đại học VCU Rams 2011-12 đại diện cho trường Đại học Virginia Commonwealth trong giải bóng rổ NCAA Division I mùa giải 2011-12. Đây là mùa thứ 44 đội bóng rổ nam của trường ... [truncated 225 chars](856 chars) |
| Con chó mà tổ tiên gồm cả Gordon và Irish Setters là giống chó gì: Manchester Terrier hay Scotch Collie? (104 chars) | Chó Manchester Terrier Chó Manchester Terrier là một giống chó thuộc họ chó săn có lông trơn. (94 chars) |
| Bộ phim nào được viết kịch bản và đạo diễn bởi Joby Harold với nhạc nền của Samuel Sim? (87 chars) | Samuel Sim Samuel Sim là một nhạc sĩ phim và truyền hình. Anh nhận được sự công nhận đầu tiên với điểm số đoạt giải cho bộ phim truyền hình "Dunkirk" của BBC. Từ đó, anh đã viết âm nhạc cho nhiều bộ phim và chương trình truyề ... [truncated 225 chars](554 chars) |
| Năm nào thì anh trai của cầu thủ được đội Washington Redskins chọn ở lượt thứ nhất trong giải tuyển quân này mới được tuyển? (124 chars) | Ba-lê Rodney "Boss" Bailey (sinh ngày 14 tháng 10 năm 1979) là một cựu cầu thủ bóng đá Mỹ từng thi đấu ở vị trí hậu vệ trong giải bóng đá quốc gia NFL. Anh được tuyển chọn bởi đội Detroit Lions trong vòng hai của cuộc tuyển c ... [truncated 225 chars](389 chars) |
| Kịch bản gia có tác phẩm "Evolution" đã cùng viết một bộ phim mà Nicolas Cage và Téa Leoni đóng vai chính là ai? (112 chars) | David Weissman David Weissman là một biên kịch và đạo diễn. Các bộ phim của ông bao gồm "The Family Man" (năm 2000), "Evolution" (năm 2001) và ""When in Rome"" (năm 2010). (172 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | hotpot_qa_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/hotpotqa-vn](https://huggingface.co/datasets/GreenNode/hotpotqa-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 400 |
| Avg positives / query | 2.00 |
| Positives per query (min / median / max) | 2 / 2 / 2 |
| Queries with multiple positives | 200 (100.00%) |
| BM25 nDCG@10 | 0.8001 |
| BM25 hit@10 | 0.9500 |
| BM25 Recall@100 | 0.9425 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8773 |
| Dense hit@10 | 0.9800 |
| Dense Recall@100 | 0.9600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8649 |
| Reranking hybrid hit@10 | 0.9950 |
| Reranking hybrid Recall@100 | 0.9925 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 99.53 |
| Document length avg chars | 445.27 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600), 2018.
- [HotpotQA project page](https://hotpotqa.github.io/), official dataset page.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/hotpotqa-vn](https://huggingface.co/datasets/GreenNode/hotpotqa-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/hotpotqa-vn](https://huggingface.co/datasets/GreenNode/hotpotqa-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | arXiv paper | https://arxiv.org/abs/1809.09600 |
| HotpotQA project page |  | project page | https://hotpotqa.github.io/ |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/hotpotqa-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/hotpotqa-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: hotpot_qa_vn
  split_name: hotpot_qa_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/hotpot_qa_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/1809.09600
    additional_source_urls:
    - https://hotpotqa.github.io/
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/hotpotqa-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 400
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 200
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 99.525
    document_mean: 445.274
  bm25:
    ndcg_at_10: 0.8001155514812699
    hit_at_10: 0.95
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB HotpotQA test split from GreenNode/hotpotqa-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated HotpotQA-VN test questions, qrels, and positive
      supporting passages used by this Nano split.
    useful_training_data:
    - official HotpotQA train examples with overlap removed
    - Vietnamese multi-hop QA data
    - Wikipedia question-to-supporting-page retrieval pairs
    - translated multi-hop retrieval data with overlap removed
    synthetic_data:
      document_generation: Vietnamese linked Wikipedia-style entity passages for bridge
        and comparison reasoning.
      question_generation: Vietnamese multi-hop questions requiring retrieval of both
        supporting passages.
      answerability: Each query should require two labeled positives, with one-hop
        hard negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: HotpotQA arXiv
      url: https://arxiv.org/abs/1809.09600
    - label: HotpotQA project page
      url: https://hotpotqa.github.io/
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/hotpotqa-vn
      url: https://huggingface.co/datasets/GreenNode/hotpotqa-vn
    source_notes: []
  references:
  - title: 'HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering'
    url: https://arxiv.org/abs/1809.09600
    year: 2018
    doi: 10.48550/arXiv.1809.09600
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
  - title: GreenNode/hotpotqa-vn
    url: https://huggingface.co/datasets/GreenNode/hotpotqa-vn
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
      ndcg_at_10: 0.8001155515
      hit_at_10: 0.95
      recall_at_100: 0.9425
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9425
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8772754905
      hit_at_10: 0.98
      recall_at_100: 0.96
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8649405263
      hit_at_10: 0.995
      recall_at_100: 0.9925
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9925
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
