# NanoCoIR / NanoCodeSearchNetCCR

## Overview

CoIR constructs CodeSearchNet-CCR by splitting CodeSearchNet functions into a
prefix and a continuation, turning code completion context into retrieval. The
query is the beginning of a real function and the positive document is the
remaining segment from the same function. Because identifiers, formatting, and
local control flow often continue across the split, the task is a strong probe
of code continuity as well as an unusually lexical code-to-code retrieval case.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) creates CodeSearchNet-CCR from
CodeSearchNet by splitting each function into an initial query segment and a
remaining target segment. The [CodeSearchNet paper](https://arxiv.org/abs/1909.09436)
provides the underlying open-source function corpus. CoIR's adaptation turns the
resource into a code-to-code retrieval task for completion-oriented context
matching.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has one positive. Queries average 372.82 characters and documents average
158.42 characters. Observed examples include JavaScript UI helpers, Ruby health
checks, and partial cryptographic utility functions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8922 and hit@10 = 0.9700. It ranks 163 positives first and 194 positives in
the top 10. Lexical continuity is very strong because the continuation often
shares the same function name, local identifiers, comments, and formatting.

### Training Data That May Help

Code completion retrieval data, function-prefix-to-suffix pairs, CodeSearchNet
code splits, and hard negatives from the same repository or function family
should help.

### Synthetic Data Guidance

Generate realistic partial functions and matching continuations. To avoid an
overly lexical task, include hard negatives with the same identifier names but a
different control-flow or return behavior.

### Benchmark Information Leakage

CoIR constructs CodeSearchNet-CCR from CodeSearchNet by splitting functions into
prefix queries and continuation documents, using the same broad split sizes as
CodeSearchNet: roughly 905k train queries, 41k dev queries, and 53k test queries
over a 1M-document corpus. This Nano split is derived from the CoIR
CodeSearchNet-CCR test side. Training on the corresponding test functions or
prefix-continuation pairs can leak the exact continuation target.

Training should use train-side function completion pairs or synthetic
repository-local continuations, then remove any row whose prefix, continuation,
full function, repository-local identifier pattern, or token fingerprint matches
NanoCodeSearchNetCCR. Because this task is highly lexical, memorized
prefix-continuation pairs can produce high scores without improving general code
retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| def _get_field(self, field_name, default=None): """ Fetches a field from extras, and returns it. This is some Airflow magic. The grpc hook type adds custom UI elements to the hook page, which allow admins to specify scopes, c ... [truncated 225 chars](337 chars) | GrpcHook._get_field full_field_name = 'extra__grpc__{}'.format(field_name) if full_field_name in self.extras: return self.extras[full_field_name] else: return default (206 chars) |
| func (in *inflights) freeTo(to uint64) { if in.count == 0 \|\| to < in.buffer[in.start] { // out of the left side of the window return } idx := in.start var i int for i = 0; i < in.count; i++ { if to < in.buffer[idx] { // found ... [truncated 225 chars](364 chars) | freeTo -= size } } // free i inflights and set new start index in.count -= i in.start = idx if in.count == 0 { // inflights is empty, reset the start index so that we don't grow the // buffer unnecessarily. in.start = 0 } } (237 chars) |
| func NewCertPool(CAFiles []string) (*x509.CertPool, error) { certPool := x509.NewCertPool() for _, CAFile := range CAFiles { pemByte, err := ioutil.ReadFile(CAFile) if err != nil { return nil, err } for { var block *pem.Block ... [truncated 225 chars](304 chars) | NewCertPool break } cert, err := x509.ParseCertificate(block.Bytes) if err != nil { return nil, err } certPool.AddCert(cert) } } return certPool, nil } (176 chars) |
| def build_for(packages) metadata = packages.first.metadata name = metadata[:name] # Attempt to load the version manifest data from the packages metadata manifest = if version_manifest = metadata[:version_manifest] Manifest.fr ... [truncated 225 chars](843 chars) | Omnibus.ArtifactoryPublisher.build_for name: name, number: manifest.build_version, vcs_revision: manifest.build_git_revision, build_agent: { name: "omnibus", version: Omnibus::VERSION, }, modules: [ { # com.getchef:chef-serve ... [truncated 225 chars](1172 chars) |
| function isArrayBufferView(val) { var result; if ((typeof ArrayBuffer !== 'undefined') && (ArrayBuffer.isView)) { result = ArrayBuffer.isView(val); } else { result (177 chars) | isArrayBufferView = (val) && (val.buffer) && (val.buffer instanceof ArrayBuffer); } return result; } (104 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoCodeSearchNetCCR |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8834 |
| BM25 hit@10 | 0.9700 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8519 |
| Dense hit@10 | 0.9350 |
| Dense Recall@100 | 0.9400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9073 |
| Reranking hybrid hit@10 | 0.9850 |
| Reranking hybrid Recall@100 | 0.9950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 372.82 |
| Document length avg chars | 158.42 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [CodeSearchNet Challenge](https://arxiv.org/abs/1909.09436); 2019; Hamel Husain et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [CoIR-Retrieval/CodeSearchNet-ccr](https://huggingface.co/datasets/CoIR-Retrieval/CodeSearchNet-ccr)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| CodeSearchNet Challenge: Evaluating the State of Semantic Code Search | 2019 | source task paper | https://arxiv.org/abs/1909.09436 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoCodeSearchNetCCR
  split_name: NanoCodeSearchNetCCR
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoCodeSearchNetCCR.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 372.82
    document_mean: 158.4226
  bm25:
    ndcg_at_10: 0.8833612093631618
    hit_at_10: 0.97
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR CodeSearchNet-CCR test-derived retrieval split
    train_eval_overlap_audit: not_audited_split_filtering_required
    leakage_note: exclude NanoCodeSearchNetCCR prefix-continuation pairs; do not train
      on CodeSearchNet-CCR test-derived rows
    leakage_risk:
      source_dataset: CodeSearchNet-derived prefix-continuation pairs
      source_train_queries_reported_by_coir: 905000
      source_dev_queries_reported_by_coir: 41000
      source_test_queries_reported_by_coir: 53000
      risk: upstream CodeSearchNet test functions can overlap with NanoCodeSearchNetCCR
        evaluation prefix-continuation rows
      recommended_filter: train-side only plus normalized prefix, continuation, full-function,
        and token-fingerprint exclusion
    useful_training_data:
    - function prefix-to-continuation retrieval data
    - CodeSearchNet code splits
    - same-repository code hard negatives
    synthetic_data:
      document_generation: function continuations preserving control flow and identifiers
      question_generation: partial function prefixes
      answerability: positive continuation must complete the source function
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
    - label: CoIR arXiv
      url: https://arxiv.org/abs/2407.02883
    - label: CodeSearchNet arXiv
      url: https://arxiv.org/abs/1909.09436
    - label: CoIR-Retrieval/CodeSearchNet-ccr
      url: https://huggingface.co/datasets/CoIR-Retrieval/CodeSearchNet-ccr
    source_notes: []
  references:
  - title: 'CoIR: A Comprehensive Benchmark for Code Information Retrieval Models'
    url: https://arxiv.org/abs/2407.02883
    year: 2025
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'CodeSearchNet Challenge: Evaluating the State of Semantic Code Search'
    url: https://arxiv.org/abs/1909.09436
    year: 2019
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8833612094
      hit_at_10: 0.97
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.851869594
      hit_at_10: 0.935
      recall_at_100: 0.94
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9073268177
      hit_at_10: 0.985
      recall_at_100: 0.995
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.995
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
