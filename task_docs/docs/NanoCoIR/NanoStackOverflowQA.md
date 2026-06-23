# NanoCoIR / NanoStackOverflowQA

## Overview

NanoStackOverflowQA is an English code and developer-help retrieval task in NanoCoIR. It is derived from StackOverflow question-answer pairs through CoIR. The query is a developer question that may include a title, body text, code snippets, error messages, framework context, and attempted solutions. The target document is the relevant answer.

This task represents practical troubleshooting retrieval. A good model must identify the actual programming problem and retrieve an answer that diagnoses or solves it. Matching only language names, library names, or stack-trace tokens is not enough, because many questions in the same framework share similar vocabulary while requiring different fixes.

## Details

### What the Original Data Measures

CoIR constructs a StackOverflow QA retrieval task from Stack Overflow data. Developer questions are paired with their answers, and the retrieval model must find the answer that corresponds to the question. The metadata records no confirmed standalone task paper beyond CoIR construction details and the source dataset card.

The original task measures question-to-answer retrieval for programming help. Relevance depends on whether the answer solves or explains the user's issue. Queries may include noisy prose, partial code, error traces, and environment-specific details.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 200 positive qrels. Each query has exactly one positive answer. Queries average 1,361.81 characters, and documents average 1,218.06 characters. Both sides are long enough to contain a mix of natural language and code.

Observed examples involve WinForms click blocking, Angular `$resource` parameters, source-map configuration, MongoDB aggregation, and Inno Setup message behavior. Positive answers often include concrete fixes, corrected code, configuration details, or explanations of why the observed behavior occurs.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.7482, hit@10 of 0.8300, and recall@100 of 0.9250 using a top-500 candidate pool. Exact overlap from framework names, API names, error messages, configuration keys, and code snippets gives lexical retrieval useful anchors.

However, BM25 is not the strongest profile. StackOverflow answers often paraphrase the diagnosis, omit parts of the question text, or focus on the decisive fix rather than every error token. BM25 can also retrieve answers from the same tag or framework that share many words but solve a different issue.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by top-rank metrics, with nDCG@10 of 0.8836, hit@10 of 0.9300, and recall@100 of 0.9400. Dense retrieval improves over BM25 by connecting the developer problem to the answer's explanatory content and fix.

Dense similarity is useful when the question contains a long narrative but the relevant answer focuses on a small conceptual correction. It can recognize that a source-map problem is about path fields, or that an Angular resource issue is about parameter construction, even when the exact wording differs. The remaining errors likely involve several plausible answers from the same technology area.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.8328, hit@10 of 0.8850, and recall@100 of 0.9900. It uses top-100 candidates with optional rank-101 safeguards; two rows contain 101 candidates and two safeguard-positive rows are recorded. Hybrid retrieval has the best top-100 coverage but is below dense retrieval for top-10 ranking.

This pattern is useful for reranking pipelines. BM25 contributes exact diagnostic tokens and code identifiers, while dense retrieval contributes semantic diagnosis. Together they nearly always include the positive in the top 100. A final ranker then needs to choose the answer that actually resolves the user's problem.

### Metric Interpretation for Model Researchers

NanoStackOverflowQA is a high-signal hybrid developer-help task. BM25 is strong because programming questions include exact terms, but dense retrieval is stronger because answers are explanatory and often paraphrase the solution. Reranking_hybrid is best for candidate coverage.

For researchers, the task distinguishes three capabilities: lexical matching of error and API tokens, semantic matching of problem and fix, and final ranking among same-tag answers. nDCG@10 is the main top-rank diagnostic, while recall@100 indicates whether downstream reranking has access to the correct answer.

### Query and Relevance Type Tendencies

Queries are real-world programming questions. They may contain titles, code, error output, framework versions, configuration snippets, or partial attempts. Documents are developer answers that mix prose, code, and corrective guidance.

Relevance is answer usefulness. The positive answer should solve, explain, or correctly diagnose the specific issue in the question. A candidate from the same framework is not enough if it addresses a different error or a different API behavior.

### Representative Failure Modes

BM25 may retrieve answers from the same framework tag because of shared API names or stack-trace tokens. Dense retrieval may retrieve an answer that is conceptually close but not the accepted or intended fix. Hybrid retrieval can include the correct answer in the pool but rank a more lexically similar answer above it.

Another failure mode is over-focusing on code snippets while missing the user's actual question. The decisive evidence may be in prose around the code, such as a version mismatch, a configuration path, or a misunderstanding of an API parameter.

### Training Data That May Help

Useful training data includes StackOverflow question-answer retrieval, code troubleshooting pairs, error-message matching, and framework-tag hard negatives. Strong negatives should come from the same language or framework and share visible tokens while solving a different problem.

Leakage filtering is required. The Nano split is derived from CoIR StackOverflow QA test-side data. Training should exclude NanoStackOverflowQA question-answer pairs and avoid StackOverflow QA test-derived rows. Filters should cover normalized title, body, answer text, code snippets, URL or ID, and token fingerprints.

### Model Improvement Notes

Improving this task requires models that can represent both code tokens and explanatory diagnosis. Error messages, API names, and configuration keys should remain visible, but the model also needs to understand why a specific answer resolves the question.

For reranking, the most useful signals are answer specificity, correspondence to the reported failure, and handling of the exact framework or configuration context. Same-tag hard negatives are essential for measuring real progress.

## Example Data

| Query | Positive document |
| --- | --- |
| How to block mouse click events from another form I have a winforms single form application that use... [100 / 1,644 chars] | I'm glad to announce that the problem is finally solved. After spending a few days attempting to recreate this bug in a new application, re-constructing the main form in the application, comment out p... [200 / 916 chars] |
| Passing a parameter to a $resource? I have a controller that that looks like this: (function() { ang... [100 / 1,406 chars] | Create the $resource object with: function branchResource($resource){ ̶r̶e̶t̶u̶r̶n̶ ̶$̶r̶e̶s̶o̶u̶r̶c̶e̶(̶"̶/̶a̶p̶i̶/̶u̶s̶e̶r̶/̶G̶e̶t̶A̶l̶l̶U̶s̶e̶r̶B̶r̶a̶n̶c̶h̶e̶s̶?̶f̶e̶d̶e̶r̶a̶t̶e̶d̶U̶s̶e̶r̶N̶a̶m̶e̶=... [200 / 991 chars] |
| Chrome doesn’t show un-minified code in spite of source map present I’m using Grunt and UglifyJS to... [100 / 910 chars] | "sources":["customDomain.js"] should be relative to the customDomain.map.js file. Make sure they are in the same directory on your server if this is the case for you. "file":"customDomain.js" should b... [200 / 641 chars] |
| Get looked up array count for a document i have 2 collections : words and phrases Each word document... [100 / 2,051 chars] | db.words.aggregate([ { "$unwind" : "$phrases"}, { "$lookup": { "from": "phrases", "localField": "phrases", "foreignField": "id", "as": "phrases_data" } }, { "$match" : { "phrases_data.active" : 1} },... [200 / 683 chars] |
| Inno Setup Remove version number from "Setup has detected that ... is currently running" I've added... [100 / 694 chars] | You are wrong. The message is: SetupAppRunningError=Setup has detected that %1 is currently running.%n%nPlease close all instances of it now, then click OK to continue, or Cancel to exit. Where the %1... [200 / 858 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883) | Benchmark paper defining the retrieval adaptation. |
| [CoIR-Retrieval/stackoverflow-qa](https://huggingface.co/datasets/CoIR-Retrieval/stackoverflow-qa) | Public source dataset card for the retrieval task. |
| [Stack Overflow Data on Kaggle](https://www.kaggle.com/datasets/stackoverflow/stacksample/data) | Public source data page. |
| [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A WinForms question about blocking mouse-click events behind a modal overlay. | The answer reports the eventual fix and explains what caused the form interaction issue. |
| An Angular `$resource` question about passing a parameter to an API endpoint. | The answer shows how to construct the resource with a parameterized route. |
| A source-map question where Chrome does not show unminified code. | The answer explains how the source-map path fields should be relative to the map file. |
| A MongoDB question about counting active looked-up array items. | The answer uses aggregation stages such as unwind, lookup, match, and group. |
| An Inno Setup question about an application-running message containing a version number. | The answer explains which message placeholder is used and where the displayed name comes from. |
