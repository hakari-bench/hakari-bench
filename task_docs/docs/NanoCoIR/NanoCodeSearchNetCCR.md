# NanoCoIR / NanoCodeSearchNetCCR

## Overview

NanoCodeSearchNetCCR is an English code-to-code retrieval task in NanoCoIR. It is derived from CodeSearchNet through CoIR by splitting real functions into a prefix and a continuation. The query is the beginning of a function, and the positive document is the remaining segment from the same source function.

The task is a retrieval version of code continuation. It evaluates whether a model can identify the continuation that matches local identifiers, formatting, control flow, object state, and return behavior. Unlike code-to-docstring retrieval, this split has strong lexical continuity because the prefix and continuation often share the same local vocabulary.

## Details

### What the Original Data Measures

CoIR constructs CodeSearchNet-CCR from the CodeSearchNet function corpus. Each source function is divided into an initial query segment and a target continuation segment. The model must retrieve the matching continuation from a corpus of candidate code fragments.

This measures code-context continuity. The positive continuation should complete the specific function represented by the prefix, not merely implement a similar operation. Matching can depend on variable names, open control-flow structures, comments, indentation, object fields, and the partially established computation.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive continuation. Queries average 372.82 characters, and documents average 158.42 characters. Both sides are relatively short code fragments, making local lexical and syntactic evidence very important.

Observed examples include Python connection helpers, Go in-flight buffer management, Go certificate-pool construction, Ruby package build construction, and JavaScript ArrayBuffer-view checks. The continuation frequently reuses identifiers introduced in the prefix, such as local variables, receiver names, or object fields.

### BM25 Evaluation Profile

BM25 is very strong on NanoCodeSearchNetCCR. It reaches nDCG@10 of 0.8834, hit@10 of 0.9700, and recall@100 of 1.0000 with a top-500 candidate pool. This reflects the strong lexical continuity between prefixes and continuations.

For this task, term frequency is not just a shallow signal. Shared variable names, function names, receiver names, string literals, and comments often identify the correct continuation. BM25 can recover every positive by rank 100 because the target fragment usually carries code tokens established in the query. The main BM25 risk is over-ranking a fragment from a similar function that shares names but diverges in control flow or return behavior.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.8519, hit@10 of 0.9350, and recall@100 of 0.9400. Dense retrieval is strong, but it is below BM25 and reranking_hybrid. This indicates that embedding similarity captures broad continuation compatibility, while exact local code tokens remain crucial.

Dense retrieval can recognize that a prefix about certificate parsing should continue with certificate parsing logic, or that a JavaScript predicate should finish with a boolean return. However, it may miss the exact continuation when many fragments have similar semantics. Local identifier matching and syntactic continuity are more decisive here than broad embedding similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset is the strongest top-rank profile, with nDCG@10 of 0.9073, hit@10 of 0.9850, and recall@100 of 0.9950. It uses top-100 candidates with optional rank-101 safeguards; one query has 101 candidates and one safeguard-positive row is recorded.

This result shows that combining lexical and dense evidence improves top ranking over either signal alone. BM25 supplies exact continuation anchors, while dense retrieval helps when the continuation is semantically compatible but shares fewer tokens. The slight recall@100 drop relative to BM25 means BM25 alone is the most complete top-100 source, but reranking_hybrid gives the best top-10 ordering.

### Metric Interpretation for Model Researchers

NanoCodeSearchNetCCR is a lexical-continuity-heavy code retrieval task. Unlike NanoCodeSearchNet, where dense retrieval dominates code-to-text mapping, CCR rewards exact local code matching. Strong models should preserve identifiers and control-flow state while also representing the semantics of the continuation.

The metric pattern is useful: BM25 has perfect recall@100, dense is lower, and reranking_hybrid has the best nDCG@10. This means candidate generation can rely heavily on lexical code continuity, while final ranking benefits from semantic compatibility checks. A model that ignores exact identifiers may lose candidates that are easy for BM25.

### Query and Relevance Type Tendencies

Queries are partial function prefixes. They may include signatures, comments, local variable initialization, an open loop or conditional, or a partially constructed object. Documents are short continuation fragments that finish the same logic.

Relevance is source-continuation identity. The positive fragment must complete the exact source function. A fragment from the same repository, language, or API may still be wrong if it does not continue the established variables and control flow.

### Representative Failure Modes

BM25 may retrieve a continuation with matching identifiers but incompatible control flow. Dense retrieval may retrieve a semantically related fragment that uses different variable names or belongs to a different function. Hybrid retrieval can still be confused when several continuations share both local tokens and broad purpose.

Another failure mode is treating code continuation as generic code similarity. The correct answer is not just a fragment that performs the same operation; it must fit the prefix's partially built state. Models need sensitivity to open scopes, accumulator variables, object fields, and return expectations.

### Training Data That May Help

Useful training data includes function prefix-to-continuation retrieval pairs, CodeSearchNet code splits, and hard negatives from the same repository or function family. Hard negatives should reuse identifiers or APIs where possible so that models must learn actual continuation compatibility.

Leakage filtering is required because this split is derived from CodeSearchNet test-side functions. Training should exclude NanoCodeSearchNetCCR prefix-continuation pairs and should not train on CodeSearchNet-CCR test-derived rows. Filters should cover normalized prefix text, continuation text, full-function text, repository-local identifier patterns, and token fingerprints.

### Model Improvement Notes

Improving this task requires precise code-context representation. Models should encode local variables, receiver objects, control-flow structures, and partially completed expressions. Identifier-preserving tokenization and code-aware pretraining are likely important.

For reranking research, NanoCodeSearchNetCCR is a good case where lexical candidate generation is already very strong. The challenge is to use semantic and syntactic compatibility to rank the exact continuation above fragments that merely share names.

## Example Data

| Query | Positive document |
| --- | --- |
| def _get_field(self, field_name, default=None): """ Fetches a field from extras, and returns it. Thi... [100 / 337 chars] | GrpcHook._get_field full_field_name = 'extra__grpc__{}'.format(field_name) if full_field_name in self.extras: return self.extras[full_field_name] else: return default [206 chars] |
| func (in *inflights) freeTo(to uint64) { if in.count == 0 \|\| to < in.buffer[in.start] { // out of th... [100 / 364 chars] | freeTo -= size } } // free i inflights and set new start index in.count -= i in.start = idx if in.count == 0 { // inflights is empty, reset the start index so that we don't grow the // buffer unnecess... [200 / 237 chars] |
| func NewCertPool(CAFiles []string) (*x509.CertPool, error) { certPool := x509.NewCertPool() for _, C... [100 / 304 chars] | NewCertPool break } cert, err := x509.ParseCertificate(block.Bytes) if err != nil { return nil, err } certPool.AddCert(cert) } } return certPool, nil } [176 chars] |
| def build_for(packages) metadata = packages.first.metadata name = metadata[:name] # Attempt to load... [100 / 843 chars] | Omnibus.ArtifactoryPublisher.build_for name: name, number: manifest.build_version, vcs_revision: manifest.build_git_revision, build_agent: { name: "omnibus", version: Omnibus::VERSION, }, modules: [ {... [200 / 1,172 chars] |
| function isArrayBufferView(val) { var result; if ((typeof ArrayBuffer !== 'undefined') && (ArrayBuff... [100 / 177 chars] | isArrayBufferView = (val) && (val.buffer) && (val.buffer instanceof ArrayBuffer); } return result; } [104 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [CodeSearchNet Challenge: Evaluating the State of Semantic Code Search](https://arxiv.org/abs/1909.09436) | Source task paper for the underlying function corpus. |
| [CoIR-Retrieval/CodeSearchNet-ccr](https://huggingface.co/datasets/CoIR-Retrieval/CodeSearchNet-ccr) | Public source dataset card for prefix-continuation retrieval. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Python helper begins fetching a field from connection extras. | The continuation builds the full extra-field name and returns either the stored value or the default. |
| A Go method starts freeing in-flight buffer entries up to a target value. | The continuation updates counters and resets the start index when the buffer becomes empty. |
| A Go function starts reading CA files into an x509 certificate pool. | The continuation parses PEM blocks into certificates and adds them to the pool. |
| A Ruby package build helper begins constructing metadata from a manifest. | The continuation fills the build object with name, version, revision, agent, and module fields. |
| A JavaScript predicate begins checking ArrayBuffer view support. | The continuation completes the fallback check and returns the boolean result. |
