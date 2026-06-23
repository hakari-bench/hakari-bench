# NanoCoIR / NanoCodeFeedbackMT

## Overview

NanoCodeFeedbackMT is an English code-retrieval task in NanoCoIR, adapted from CoIR's CodeFeedback-MT setting. The query is a multi-turn programming dialogue that may include user instructions, code, execution feedback, intermediate assistant attempts, and repair requests. The target document is the final assistant response for that dialogue.

The task measures whether a retriever can preserve dialogue state across long code-assistant interactions. It is not enough to match a standalone programming question to a generic answer. The model must identify which response is appropriate after the accumulated context, including earlier mistakes, corrections, requested formatting, and code-refinement intent.

## Details

### What the Original Data Measures

CoIR defines CodeFeedback-MT as a multi-turn code retrieval task. The source data comes from OpenCodeInterpreter-style Code-Feedback interactions, where code generation is combined with execution feedback and iterative refinement. CoIR turns the dialogue prefix into a query and treats the final assistant response as the item to retrieve.

The original task therefore measures stateful assistant-response retrieval. The relevant document is not merely topically related to the first user request; it must be the next or final response that fits the entire interaction history. This makes the benchmark sensitive to long-context encoding, instruction tracking, and distinctions between answers for earlier and later turns.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive response. Queries are very long, averaging 4,468.62 characters, because they include multi-turn dialogue histories. Documents average 1,468.16 characters and often combine explanatory prose with code blocks or revised code.

Observed examples include SQL query refinement, string-processing functions, number-theory reasoning, Django architecture and middleware discussion, and timestamp conversion. The target response may be a corrected implementation, an apology and clarification, a formatted explanation, or a result after simulated execution. The long query length is a defining feature of this split.

### BM25 Evaluation Profile

BM25 is strong on NanoCodeFeedbackMT. It reaches nDCG@10 of 0.7403, hit@10 of 0.8100, and recall@100 of 0.9050 with a top-500 candidate pool. This indicates that many final responses share substantial lexical material with the dialogue history, including function names, error messages, code fragments, libraries, table names, or mathematical expressions.

The BM25 behavior is different from problem-to-solution retrieval tasks such as NanoApps. Here, dialogue context and final response are often linguistically connected. Exact terms from the user request and earlier assistant attempts may reappear in the final answer. However, BM25 can still over-rank responses that match an earlier turn rather than the final requested state, especially when the conversation contains several related versions of the same code.

### Dense Evaluation Profile

The dense harrier-oss-270m candidate subset is the best top-rank profile for this task, with nDCG@10 of 0.9177, hit@10 of 0.9400, and recall@100 of 0.9450. This shows that embedding similarity is very effective at connecting the full dialogue state to the correct final response.

Dense retrieval likely benefits from modeling intent across the whole conversation. It can recognize that a final answer is not just about SQL, Django, or string processing in general, but about the specific repair or refinement requested after previous messages. The remaining errors probably come from near-duplicate dialogue states, similar assistant responses, or long contexts where an important late-turn correction is diluted by earlier material.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8035, hit@10 of 0.8900, and recall@100 of 0.9950. It uses top-100 candidates with optional rank-101 safeguards; only one query uses 101 candidates, and one safeguard positive row is recorded. The hybrid profile has the best recall@100 but weaker top-rank ordering than dense retrieval.

This result suggests that lexical and dense candidates are complementary for coverage. BM25 contributes exact code and dialogue-token overlap, while dense retrieval captures the stateful response relation. Yet the top-10 ordering is better in dense-only results, so adding lexical evidence can introduce plausible but stale responses from adjacent turns. For reranking experiments, this task is a good example where hybrid candidates are useful, but final ranking must be dialogue-state aware.

### Metric Interpretation for Model Researchers

NanoCodeFeedbackMT is a high-scoring but still informative retrieval task. BM25, dense, and hybrid all recover many positives, but their strengths differ. BM25 confirms that exact code and dialogue tokens are useful. Dense retrieval shows the strongest nDCG@10, meaning semantic dialogue-state matching is critical for top placement. Reranking_hybrid confirms that combined candidates improve near-complete coverage.

The most important distinction is between top-rank precision and candidate recall. Dense is best when the question is "which response should be ranked first?", while reranking_hybrid is best when the question is "can the positive response be made available to a downstream reranker?" Models that improve this task should be inspected for whether they distinguish the final required turn from earlier valid-but-outdated answers.

### Query and Relevance Type Tendencies

Queries are multi-turn code-assistant histories. They may contain user requests, assistant explanations, code blocks, execution output, feedback, and revisions. Documents are final assistant responses that may include prose, code, formatting changes, or acknowledgments of earlier mistakes.

Relevance depends on the entire history. A document that answers the original user instruction may be non-relevant if the final turn requests a correction, different style, execution result, or additional explanation. This favors retrievers that can encode turn order and late-context changes rather than averaging all dialogue text.

### Representative Failure Modes

A common failure mode is retrieving a response that matches the initial user request but ignores later feedback. Another is retrieving a response from a similar coding conversation with the same library, function name, or error pattern. BM25 is especially vulnerable when long query text repeats code snippets that also appear in many candidate responses.

Dense systems can fail when several candidate responses are semantically close, such as multiple corrections for the same function or multiple explanations of the same programming concept. Hybrid systems may recover the correct response in the candidate pool but rank an earlier or more lexically similar response above it.

### Training Data That May Help

Useful training data includes multi-turn code assistant conversations, execution-feedback repair traces, and hard negatives from adjacent code-feedback turns. Good negatives should include earlier assistant responses from the same conversation, responses to similar bugs, and final answers for related but distinct instructions.

Leakage control is unusually important. The metadata records an audit of `m-a-p/Code-Feedback` in which 66,383 source train rows were scanned. All 200 Nano queries had normalized exact query matches, all 200 positives had normalized exact positive matches, 200 high-shingle query matches were found, and 199 high-shingle positive matches were found. Raw public Code-Feedback train rows therefore contain direct benchmark leakage for this split and must be filtered before training.

### Model Improvement Notes

Improvements should focus on long-dialogue representation and final-turn grounding. A strong model should preserve the difference between earlier context and the current retrieval target, especially when the conversation includes several code versions.

For candidate generation, dense retrieval is already highly effective, while reranking_hybrid gives stronger top-100 coverage. The most promising research direction is a reranker or embedding model that uses turn structure, code-block boundaries, execution feedback, and final instruction changes to choose the response that fits the latest state.

## Example Data

| Query | Positive document |
| --- | --- |
| 'user': Write a SQL query to list customers who have placed orders for more than $100 in the past mo... [100 / 3,249 chars] | To adhere to standard SQL formatting, keywords are written in uppercase, while database, table, and column names in lowercase. Indentation is used to show the structure of SQL statements clearly, and... [200 / 2,115 chars] |
| 'user': Design a programming function that integrates underscores in place of spaces that separate w... [100 / 2,357 chars] | The function `underscore_punctuation` has been successfully defined without any syntactical errors. Now we can use this function to replace spaces with underscores in string words, ending with punctua... [200 / 557 chars] |
| 'user': A divisor $d$ of a number $n$ is deemed unitary if it possesses the characteristic $\gcd(d,... [100 / 7,649 chars] | I apologize for any confusion caused earlier. Calculating $S(100,000,000!)$ directly is not feasible due to the size of the numbers involved. In mathematics, problems like this often require a deep un... [200 / 777 chars] |
| 'user': Write a detailed explanation of the Model-View-Controller (MVC) architecture pattern and its... [100 / 11,785 chars] | Apologies for the confusion, but as an AI, I can't execute Django code. However, I can indeed enhance the middleware code with comments and improved formatting for better readability: For the threadin... [200 / 2,136 chars] |
| 'user': Write a Python code that takes a Unix timestamp as input, converts it to date and time, and... [100 / 3,514 chars] | The provided Unix timestamp, 1594102055, has been successfully converted into a date and time. The year extracted from this conversion was 2020, and based on that, the program has returned the message... [200 / 429 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement](https://arxiv.org/abs/2402.14658) | Source task paper describing execution and refinement data. |
| [m-a-p/Code-Feedback](https://huggingface.co/datasets/m-a-p/Code-Feedback) | Public source dataset card for the multi-turn code feedback data. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A multi-turn SQL request about customers, order totals, order counts, exclusions, and formatting requirements. | The final response provides a formatted SQL-oriented answer that follows the accumulated constraints. |
| A dialogue asking for a string function that replaces spaces after punctuation-ending words. | The target response confirms or provides the corrected function behavior and explains the result. |
| A long number-theory request involving unitary divisors and infeasible direct computation. | The response clarifies the computational difficulty and redirects toward mathematical reasoning. |
| A discussion of Django MVC concepts, form validation, database transactions, and middleware examples. | The final answer supplies revised explanatory text or code after acknowledging earlier confusion. |
| A timestamp conversion request that asks for extracted date elements and leap-year evaluation. | The target response reports the converted date context and the leap-year conclusion for the requested timestamp. |
