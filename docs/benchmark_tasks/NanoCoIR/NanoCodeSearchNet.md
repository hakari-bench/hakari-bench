# NanoCoIR / NanoCodeSearchNet

## Overview

CoIR reverses the usual CodeSearchNet search direction: source code from
open-source GitHub functions becomes the query, and the retriever must find the
matching docstring or natural-language summary. The task probes whether code
structure, identifiers, and API usage can be mapped back to concise
documentation across languages such as Java, JavaScript, and Go, where the
positive text may omit much of the implementation detail.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) reverses the usual CodeSearchNet
semantic code search direction for this split: code is the query and the
docstring or summary is the target document. The [CodeSearchNet paper](https://arxiv.org/abs/1909.09436)
describes a corpus of functions from open-source GitHub repositories paired with
documentation across Go, Java, JavaScript, PHP, Python, and Ruby. CoIR uses this
resource to test whether retrievers can recover natural-language descriptions
from code.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has one positive. Queries average 636.26 characters and include Java,
JavaScript, and Go examples in the observed sample. Documents average only
86.07 characters and are short docstrings or API comments.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6471 and hit@10 = 0.7700. It ranks 104 positives first and 154 in the top 10.
BM25 benefits from function names and identifier overlap, but code often encodes
behavior through syntax and structure not repeated verbatim in documentation.

### Training Data That May Help

CodeSearchNet-style code-docstring pairs, API documentation retrieval, identifier
splitting, and hard negatives from the same library or language should help.

### Synthetic Data Guidance

Generate realistic functions and concise docstrings. Negatives should be short
descriptions from similar APIs so models cannot rely only on language or library
names.

### Benchmark Information Leakage

CoIR adapts CodeSearchNet with roughly 905k train queries, 41k dev queries, and
53k test queries over a 1M-document corpus. This Nano split is derived from the
CoIR CodeSearchNet test side, where source code is the query and the docstring
or summary is the document. Training on CodeSearchNet test rows, or on a public
CodeSearchNet export that does not preserve the upstream split, can leak exact
code-docstring pairs.

Training should use train-side CodeSearchNet-style pairs or non-overlapping
code-summary data, then remove any row whose code, docstring, function name, or
token fingerprint matches NanoCodeSearchNet. A model trained on unfiltered
test-derived pairs may get high scores by memorizing function summaries rather
than learning robust code-to-text retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| def _get_field(self, field_name, default=None): """ Fetches a field from extras, and returns it. This is some Airflow magic. The grpc hook type adds custom UI elements to the hook page, which allow admins to specify scopes, c ... [truncated 225 chars](532 chars) | Fetches a field from extras, and returns it. This is some Airflow magic. The grpc hook type adds custom UI elements to the hook page, which allow admins to specify scopes, credential pem files, etc. They get formatted as show ... [truncated 225 chars](257 chars) |
| func (in *inflights) freeTo(to uint64) { if in.count == 0 \|\| to < in.buffer[in.start] { // out of the left side of the window return } idx := in.start var i int for i = 0; i < in.count; i++ { if to < in.buffer[idx] { // found ... [truncated 225 chars](595 chars) | // freeTo frees the inflights smaller or equal to the given `to` flight. (72 chars) |
| func NewCertPool(CAFiles []string) (*x509.CertPool, error) { certPool := x509.NewCertPool() for _, CAFile := range CAFiles { pemByte, err := ioutil.ReadFile(CAFile) if err != nil { return nil, err } for { var block *pem.Block ... [truncated 225 chars](473 chars) | // NewCertPool creates x509 certPool with provided CA files. (60 chars) |
| def build_for(packages) metadata = packages.first.metadata name = metadata[:name] # Attempt to load the version manifest data from the packages metadata manifest = if version_manifest = metadata[:version_manifest] Manifest.fr ... [truncated 225 chars](1985 chars) | The build object that corresponds to this package. @param [Array<Package>] packages the packages to create the build from @return [Artifactory::Resource::Build] (167 chars) |
| function isArrayBufferView(val) { var result; if ((typeof ArrayBuffer !== 'undefined') && (ArrayBuffer.isView)) { result = ArrayBuffer.isView(val); } else { result = (val) && (val.buffer) && (val.buffer instanceof ArrayBuffer ... [truncated 225 chars](264 chars) | Determine if a value is a view on an ArrayBuffer @param {Object} val The value to test @returns {boolean} True if value is a view on an ArrayBuffer, otherwise false (165 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoCodeSearchNet |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6099 |
| BM25 hit@10 | 0.7300 |
| BM25 Recall@100 | 0.9050 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9687 |
| Dense hit@10 | 1.0000 |
| Dense Recall@100 | 1.0000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8678 |
| Reranking hybrid hit@10 | 0.9650 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 636.26 |
| Document length avg chars | 86.07 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [CodeSearchNet Challenge](https://arxiv.org/abs/1909.09436); 2019; Hamel Husain et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [code-search-net/code_search_net](https://huggingface.co/datasets/code-search-net/code_search_net)

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
  task_name: NanoCodeSearchNet
  split_name: NanoCodeSearchNet
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoCodeSearchNet.md
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
    query_mean: 636.265
    document_mean: 86.072
  bm25:
    ndcg_at_10: 0.6099066372318422
    hit_at_10: 0.73
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR CodeSearchNet test-derived retrieval split
    train_eval_overlap_audit: not_audited_split_filtering_required
    leakage_note: exclude NanoCodeSearchNet code-docstring pairs; do not train on
      CodeSearchNet test-derived rows
    leakage_risk:
      source_dataset: CodeSearchNet
      source_train_queries_reported_by_coir: 905000
      source_dev_queries_reported_by_coir: 41000
      source_test_queries_reported_by_coir: 53000
      risk: upstream CodeSearchNet test code-docstring pairs can overlap with NanoCodeSearchNet
        evaluation rows
      recommended_filter: train-side only plus normalized code, docstring, function-name,
        and token-fingerprint exclusion
    useful_training_data:
    - CodeSearchNet code-docstring pairs
    - API documentation retrieval examples
    - same-library short-docstring hard negatives
    synthetic_data:
      document_generation: concise function summaries and docstrings
      question_generation: source code snippets as queries
      answerability: positive text must describe the code behavior
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
    - label: CoIR arXiv
      url: https://arxiv.org/abs/2407.02883
    - label: CodeSearchNet arXiv
      url: https://arxiv.org/abs/1909.09436
    - label: code-search-net/code_search_net
      url: https://huggingface.co/datasets/code-search-net/code_search_net
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
      ndcg_at_10: 0.6099066372
      hit_at_10: 0.73
      recall_at_100: 0.905
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.905
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9687349467
      hit_at_10: 1.0
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8678369433
      hit_at_10: 0.965
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
