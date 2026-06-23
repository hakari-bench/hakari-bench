# NanoCodeRAG / NanoCodeRAGStackoverflowPosts

## Overview

NanoCodeRAGStackoverflowPosts is an English developer-Q&A retrieval task in NanoCodeRAG, sampled from the Stack Overflow post retrieval source of CodeRAG-Bench. The query is a programming question, often beginning with a title and short problem description. The target document is a long Stack Overflow-style post containing answers, code examples, warnings, caveats, and discussion.

The task evaluates practical developer knowledge retrieval. A relevant post should contain a usable answer, workaround, warning, or API usage pattern for the question. The model must distinguish the exact problem from nearby posts with the same language, framework, error message, or tool name.

## Details

### What the Original Data Measures

CodeRAG-Bench treats Stack Overflow posts as one of its retrieval sources for code-generation support. The benchmark paper describes using StackExchange data as retrievable developer knowledge, where posts can contain questions, answers, code snippets, and explanations.

This Nano task isolates Stack Overflow post retrieval. Unlike formal documentation, posts are conversational and may contain multiple answers or partial fixes. Relevance depends on whether the post helps solve the specific developer problem in the query.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive post. Queries average 209.84 characters, while documents average 4,735.05 characters. The documents are long community threads rather than concise answers.

Observed topics include finding a font file path from a display name on macOS, deleting a locked file in C#, handling concurrent database edits, throwing an error from a MySQL trigger, and throttling bandwidth in IIS. These examples require matching environment, tool, and failure mode.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.7737, hit@10 of 0.9000, and recall@100 of 0.9650 using a top-500 candidate pool. The query often shares title words, product names, language names, error phrases, and code tokens with the positive post. That makes lexical retrieval a good candidate generator.

BM25 can still fail on near-neighbor posts. Many Stack Overflow questions share tags and terminology but ask different things. A version-control question, database operation, or server configuration issue may retrieve another post with the same tool name but a different requested fix.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is the best top-rank result, with nDCG@10 of 0.8865, hit@10 of 0.9500, and recall@100 of 0.9600. Dense retrieval improves over BM25 by matching the problem and answer semantics rather than only shared words.

Dense similarity helps when the answer thread uses different wording from the question or when the relevant post contains a workaround rather than a direct phrase match. It can connect a question about locked files to a post recommending handle inspection tools, or a question about MySQL trigger errors to a post with trigger-specific error behavior.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8373, hit@10 of 0.9250, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard-positive rows. Hybrid retrieval has the best top-100 coverage, while dense retrieval has the best top-10 ranking.

This is a good reranking setup. BM25 contributes exact titles, tags, errors, and code tokens. Dense retrieval contributes semantic problem matching. The combined pool includes every positive by rank 100, but the final ranker must suppress same-tag or same-tool distractors.

### Metric Interpretation for Model Researchers

NanoCodeRAGStackoverflowPosts is a strong hybrid developer-Q&A task. BM25 is useful, dense retrieval is stronger at the top, and reranking_hybrid gives complete candidate coverage. This makes it a good benchmark for separating candidate generation from final answer-thread ranking.

For model researchers, the task tests whether a model understands developer intent in noisy community text. High scores require handling titles, body context, code snippets, error messages, accepted-answer language, and post-level discussion structure.

### Query and Relevance Type Tendencies

Queries are concise developer questions, often with a title and short context. Documents are long Stack Overflow-style threads containing answers, code, caveats, and conversational explanation. The relevant evidence may be in an accepted answer, an alternative answer, or a warning inside the thread.

Relevance is post usefulness. A candidate should answer the same problem, in the same environment or tool context, with a usable fix or explanation. A post from the same tag is not enough if it addresses a different failure mode.

### Representative Failure Modes

BM25 may retrieve posts with the same language, framework, or error token but a different issue. Dense retrieval may retrieve a conceptually similar post that does not contain the needed workaround. Hybrid retrieval can include the positive but rank a same-tag distractor higher.

Long posts also create incidental-match failures. A document may mention many APIs, operating systems, or tools in comments and alternative answers, even though its main solution is unrelated to the query.

### Training Data That May Help

Useful training data includes non-overlapping Stack Overflow question-to-answer thread retrieval, duplicate-question and related-question retrieval pairs, issue-to-fix pairs, API usage Q&A, and documentation-linked Q&A with tag-matched hard negatives.

Leakage filtering is required. CodeRAG-Bench reports a Stack Overflow source corpus of about 23.5 million posts, and this Nano split is sampled from that source. Training should exclude NanoCodeRAG Stack Overflow queries, qrels, positive posts, matching titles, bodies, answers, post IDs, URLs, code blocks, and token fingerprints.

### Model Improvement Notes

Improving this task requires ranking whole developer threads by problem-solving value. Models should use title and body text, preserve code and error tokens, and recognize whether the answer actually addresses the requested operation.

For reranking, useful signals include exact tool or framework match, error-message match, answer specificity, code-block relevance, and whether the post contains a practical fix rather than a generic discussion.

## Example Data

| Query | Positive document |
| --- | --- |
| Q: How can I find the full path to a font from its display name on a Mac? I am using the Photoshop's... [100 / 149 chars] | Given a font name returned by the API, I want to find the actual physical font file that font name corresponds to on the disc. This is all happening in a python program running on OSX so I guess I'm l... [200 / 5,076 chars] |
| Q: How do I delete a file which is locked by another process in C#? I'm looking for a way to delete... [100 / 396 chars] | A: If you want to do it programmatically. I'm not sure... and I'd really recommend against it. If you're just troubleshooting stuff on your own machine, SysInternals Process Explorer can help you Run... [200 / 13,199 chars] |
| Q: Editing database records by multiple users I have designed database tables (normalised, on an MS... [100 / 334 chars] | I am concerned that if two users start editing the same record then the last to commit the update would be the 'winner' and important information may be lost. A number of solutions come to mind but I'... [200 / 4,026 chars] |
| Q: Throw an error preventing a table update in a MySQL trigger If I have a trigger before the update... [100 / 177 chars] | A: CREATE TRIGGER sample_trigger_msg BEFORE INSERT FOR EACH ROW BEGIN IF(NEW.important_value) < (1*2) THEN DECLARE dummy INT; SELECT Enter your Message Here!!! INTO dummy FROM mytable WHERE mytable.id... [200 / 5,314 chars] |
| Q: Bandwith throttling in IIS 6 by IP Address I am writing an application that downloads large files... [100 / 391 chars] | Since this is an AIR Application, I figure I will throttle via server-side since I can do it from either the server itself (IIS 6) or the web service (asp.net / C#). Throttling through IIS 6 seems to... [200 / 922 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497) | Benchmark paper describing the retrieval sources and code-generation setting. |
| [CodeRAG-Bench project page](https://code-rag-bench.github.io/) | Project page for the benchmark. |
| [CodeRAG-Bench GitHub](https://github.com/code-rag-bench/code-rag-bench) | Repository for benchmark resources. |
| [code-rag-bench/stackoverflow-posts](https://huggingface.co/datasets/code-rag-bench/stackoverflow-posts) | Public source dataset card. |
| [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| Asks how to find the full font-file path from a display name on macOS while using Photoshop automation. | The thread discusses mapping displayed font names to physical font files in an OS X workflow. |
| Asks how to delete a file locked by another process in C#. | The answer recommends cautious handling and tools or methods for identifying the locking process. |
| Asks how multiple users should edit the same database records safely. | The post discusses concurrency, update conflicts, and design choices for database editing. |
| Asks how to throw an error from a MySQL trigger to prevent an update. | The answer gives trigger logic or workaround patterns for causing an error condition. |
| Asks about bandwidth throttling in IIS 6 by IP address. | The thread discusses server-side throttling behavior and limitations for the requested environment. |
