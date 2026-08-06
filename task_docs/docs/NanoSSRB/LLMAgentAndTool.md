# NanoSSRB / LLMAgentAndTool

## Overview

LLMAgentAndTool evaluates retrieval over JSON records describing agents, tools,
capabilities, model outputs, API requests, sessions, security events, and tool
usage. Its 200 English queries search 10,000 documents with 600 positive qrels.
Requests combine exact endpoints, model names, users, thresholds, status codes,
or runtime settings with semantic capabilities such as summarization, sentiment
analysis, or safe tool choice. The task measures whether a retriever understands
software-like constraints without reducing records to bag-of-words matches.

## Details

### What the Original Data Measures

The SSRB formulation targets complex querying across heterogeneous schemas.
This domain connects that problem to agentic and RAG systems, where retrieving
the wrong tool or execution record can cause an incorrect downstream action.

### Observed Data Profile

Queries average 362 characters and documents 590 characters, with three
positives per query. Examples use model names, confidence ranges, temperature,
endpoint latency, response size, user identity, and capability descriptions.

### BM25 Evaluation Profile

BM25 reaches 0.3582 nDCG@10, 0.6700 hit@10, and 0.8617 Recall@100. Endpoint,
model, parameter, and capability tokens are powerful anchors, but lexical
search cannot consistently enforce ranges or infer equivalent capabilities.

### Dense Evaluation Profile

Dense retrieval reaches 0.4171 nDCG@10, 0.7300 hit@10, and 0.8367 Recall@100.
It improves top-rank semantic matching but loses some exact-token coverage,
especially for identifiers and configuration values.

### Reranking Hybrid Evaluation Profile

Hybrid is strongest at 0.4727 nDCG@10, 0.7750 hit@10, and 0.9067 Recall@100.
The complementary gain indicates that tool and agent retrieval needs both exact
software anchors and semantic capability understanding.

### Metric Interpretation for Model Researchers

High Recall@100 matters for tool availability; nDCG@10 matters when an agent
will act on the first few results. Hybrid gains are evidence that endpoint and
model tokens should not be discarded. Inspect whether errors violate runtime
bounds, choose the wrong capability, or confuse a request record with a tool
definition.

### Query and Relevance Type Tendencies

Queries cover tool discovery, execution-log search, generation settings,
latency and size filtering, model-output analysis, access control, and security
events. Relevance requires the correct record type plus all requested values.

### Representative Failure Modes

Common mistakes include selecting a semantically suitable tool with the wrong
endpoint, ignoring latency or token limits, conflating confidence with sentiment
score, or matching the right user in the wrong session. Version and case
normalization can also merge distinct software identifiers.

### Agent-and-Tool Notes

Preserve paths, model IDs, parameter names, status codes, timestamps, and
units. Semantic similarity should bridge capability paraphrases while keeping
operational fields distinct; `/summarize` is not interchangeable with a record
that merely mentions summaries.

### Training and Leakage Notes

Exclude NanoSSRB test records and disclose Struct-IR exposure. Avoid generating
training pairs from evaluation tool definitions or logs, even with superficial
renaming.

### Model Improvement Hints

Use schema-aware serialization, identifier-preserving tokenization, range-aware
features, and negatives with one wrong endpoint, model, user, status, or runtime
value. Capability-aware reranking should verify every constraint.

### Training Data That May Help

Independent API catalogs, tool-use traces, developer documentation retrieval,
and synthetic execution logs can teach this behavior without benchmark overlap.

### Synthetic Data Guidance

Generate fictional tools and execution records with grounded natural-language
requests. Include close alternatives differing in endpoint, permission, latency,
model, or parameter; do not seed from evaluation data.

### Public Sources

- [SSRB: Direct Natural Language Querying to Massive Heterogeneous Semi-Structured Data](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html), 2025.
- [vec-ai/struct-ir](https://huggingface.co/datasets/vec-ai/struct-ir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoSSRB](https://huggingface.co/datasets/hakari-bench/NanoSSRB)
- Source dataset: [vec-ai/struct-ir](https://huggingface.co/datasets/vec-ai/struct-ir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SSRB: Direct Natural Language Querying to Massive Heterogeneous Semi-Structured Data | 2025 | benchmark paper | [NeurIPS](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html) |
| vec-ai/struct-ir | 2025 | source dataset | [Hugging Face](https://huggingface.co/datasets/vec-ai/struct-ir) |

## Example Data

| Query | Positive document |
| --- | --- |
| Find sentiment analysis results from the 'roberta-large' model with a confidence score greater than 0.8 and a sentiment score between 0.5 and 1.0, specifically looking for positive sentiments. [192 chars] | { "analysis_id": "a123b456c789", "text_content": "This new feature is absolutely amazing! I've been waiting for this for ages and it's exceeded my expectations. RoBERTa-large really nailed the positive sentiment here.", "sentiment_score": 0.95, "sentiment_label": "positive", "analysis_timestamp": "2024-02-15T10:30:00Z", "model_used": "RoBERTa-large", "confidence_score": 0.98 } [407 chars] |
| Find content generations created by user 'user123' that had a temperature setting greater than 0.7. [99 chars] | { "generation_id": "gen-789012", "user_id": "user123", "prompt": "Short test prompt", "generated_content": "This is a short response generated with high temperature.", "temperature": 0.9, "max_tokens": 100, "generation_timestamp": "2024-01-08T14:30:00Z" } [283 chars] |
| Find API requests made to the '/summarize' endpoint with a response time between 200 and 500 milliseconds. I am interested in requests that processed a relatively small amount of data, so exclude requests where the response size exceeds 1000 bytes. [248 chars] | { "api_key_id": "key-12345", "request_id": "req-67890", "endpoint": "/summarize", "request_timestamp": "2024-01-26T10:00:00Z", "response_time": 350.5, "request_size": 150, "response_size": 500, "status_code": 200 } [246 chars] |
