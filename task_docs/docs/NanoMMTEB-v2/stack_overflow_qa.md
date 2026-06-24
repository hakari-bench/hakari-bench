# NanoMMTEB-v2 / stack_overflow_qa

## Overview

`NanoMMTEB-v2 / stack_overflow_qa` is an English developer-question retrieval
task. Queries are Stack Overflow questions that may include code snippets, error
messages, framework details, and attempted solutions. Documents are answer
posts. The Nano split has 200 queries, 10,000 documents, and 200 positive qrel
rows, with exactly one positive answer per query. Current diagnostics show
dense retrieval as the strongest top-rank profile, `reranking_hybrid` as the
strongest recall@100 profile, and BM25 as strong but weaker because resolving a
developer issue often requires semantic troubleshooting beyond token overlap.

## Details

### What the Original Data Measures

CoIR describes StackOverflow QA as a single-turn code question-answer retrieval
task based on Stack Overflow questions and answers. It is important for code
information retrieval because developer search mixes natural language, code
identifiers, API names, versions, snippets, error strings, and debugging
context.

The task measures whether a retriever can find the answer that resolves the
stated developer problem. Relevance depends on the fix or explanation, not
merely on shared API names.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has exactly one positive document. Queries average 1,361.81
characters, while documents average 1,218.06 characters.

Queries can be long posts with code snippets, stack traces, setup details, and
failed attempts. Documents are answer posts containing explanations, API usage,
commands, database queries, code changes, or configuration advice.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7970, hit@10 = 0.8700, and recall@100 = 0.9250. BM25 is
strong because exact API names, method names, error messages, framework terms,
and code tokens often repeat between the question and answer.

Its weakness is troubleshooting semantics. The correct answer may explain a
cause, propose a refactor, or identify a configuration issue without repeating
all details from the question. Same-API negatives can share many terms while
solving a different problem.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.8886, hit@10 = 0.9350, and recall@100 = 0.9450.
Dense retrieval is the strongest observed top-rank profile.

This shows the value of semantic matching for developer support retrieval. A
dense model can connect a question about symptoms, attempted code, or expected
behavior to an answer that explains the underlying cause, even when the answer
uses different wording.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.8457, hit@10 = 0.8900, and recall@100 = 0.9900. Hybrid retrieval has the best
recall@100 but is below dense retrieval for top-rank quality.

This profile suggests that hybrid search is a strong candidate generator for
reranking. It combines code-token coverage from BM25 with semantic matching
from dense retrieval, but a reranker is needed to rank the answer that actually
resolves the issue above same-API distractors.

### Metric Interpretation for Model Researchers

This task is single-positive: each question has one annotated answer. Hit@10
measures whether that answer appears near the top. nDCG@10 is sensitive to its
rank, and recall@100 measures whether it is available for reranking.

The high dense score indicates that generic lexical overlap is not enough to
capture developer intent. Good retrieval should understand the error, API,
configuration, and attempted solution well enough to distinguish fixes from
topically similar answers.

### Query and Relevance Type Tendencies

Queries are long developer questions about WinForms, Angular resources, source
maps, MongoDB aggregation, Inno Setup messages, APIs, frameworks, build tools,
and runtime behavior. Relevant documents are answer posts with concrete fixes,
code snippets, explanations, or configuration corrections.

The task rewards code-aware natural-language retrieval, identifier matching,
error-message handling, and troubleshooting semantics.

### Representative Failure Modes

BM25 can retrieve an answer with the same API names or error strings but the
wrong failure mode. Dense retrieval can retrieve a conceptually similar answer
that does not fit the exact version, framework, or code context. Hybrid
retrieval can improve coverage while still ranking same-library distractors
above the true fix.

Rerankers should check whether the candidate answer resolves the stated problem
and is compatible with the language, library, version, and code path in the
query.

### Training Data That May Help

Useful training data includes Stack Overflow question-answer pairs,
documentation retrieval pairs, API example retrieval, issue-to-fix pairs, and
error-message retrieval data. The Nano split's Stack Overflow questions, qrels,
and answer posts should be excluded from training, especially exact duplicates
from public dumps.

Synthetic data can generate realistic developer questions with language,
library, version, error, and minimal code context. Answers should include
concrete fixes or explanations. Hard negatives should mention the same API or
error family but solve a different failure mode.

### Model Improvement Notes

Dense retrievers should encode code identifiers, natural-language intent, and
debugging context together. Sparse systems should preserve exact error strings
and API tokens. Rerankers should compare code snippets and constraints, not
only topical similarity.

For hybrid systems, `NanoMMTEB-v2 / stack_overflow_qa` is a strong candidate
generation case: `reranking_hybrid` has the best recall@100. Dense retrieval
currently gives the best first-stage top-rank ordering, so the main opportunity
is reranking hybrid candidates with code-aware evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| How to block mouse click events from another form I have a winforms single form application that uses a "Thickbox" I've created whenever the loads a new view into the application form. The "Thickbox" shows another form in front of the application's form that is semi-transparent and has a user control that is the box itself. This thickbox can be shown a modal dialog and in that case I have no problems at all, but it can also be shown as a non modal, for instance, when the user switches views in t... [500 / 1,644 chars] | I'm glad to announce that the problem is finally solved. After spending a few days attempting to recreate this bug in a new application, re-constructing the main form in the application, comment out parts of the code in the main application, and generally just shooting all over to try and find a lead, It finally hit me. The application behaved as if the clicks on the thickbox was queued somehow and only activated when the thickbox was closed. This morning, after fixing some other bugs, The penny finally dropped - all I was missing was a single line of code right before closing the thickbox's form: Application.DoEvents(); The annoying thing is that it's not something that's new to me, I've used it many times before including in the main application and in the thickbox code itself... I guess I just had to let if go for a while to enable my mind to understand what was so painfully obvious in hindsight... [916 chars] |
| Passing a parameter to a $resource? I have a controller that that looks like this: (function() { angular .module("main") .controller("HomeCtrl", ["branchResource", "adalAuthenticationService", HomeCtrl]); function HomeCtrl(branchResource, adalService){ var vm = this; vm.copyrightDate = new Date(); vm.user = adalService.userInfo.userName; // right here, can I insert the vm.user from above // as a parameter to the resource's query? branchResource.query(function (data) { vm.branches = data; }); }}(... [500 / 1,406 chars] | Create the $resource object with: function branchResource($resource){ ̶r̶e̶t̶u̶r̶n̶ ̶$̶r̶e̶s̶o̶u̶r̶c̶e̶(̶"̶/̶a̶p̶i̶/̶u̶s̶e̶r̶/̶G̶e̶t̶A̶l̶l̶U̶s̶e̶r̶B̶r̶a̶n̶c̶h̶e̶s̶?̶f̶e̶d̶e̶r̶a̶t̶e̶d̶U̶s̶e̶r̶N̶a̶m̶e̶=̶:̶u̶s̶e̶r̶"̶)̶ ̶ return $resource("/api/user/GetAllUserBranches") }} Call the $resource object with: branchResource.query({"federatedUserName": vm.user}, function (data) { vm.branches = data; }); //OR vm.branches = branchResource.query({"federatedUserName": vm.user}); It is important to realize that invoking a $resource object method immediately returns an empty reference (object or array depending on isArray). Once the data is returned from the server the existing reference is populated with the actual data. Each key value in the parameter object is first bound to url template if present and then any excess keys are appended to the url search query after the ?. For more information, see AngularJS ngResource $resource API Reference. [991 chars] |
| Chrome doesn’t show un-minified code in spite of source map present I’m using Grunt and UglifyJS to generate source maps for my AngularJS app. It produces a file customDomain.js and customDomain.js.map. JS file Last line of customDomain.js looks like this: //# sourceMappingURL=customDomain.js.map Map file I find two references to customDomain.js inside of customDomain.js.map, one at the beginning: "sources":["../../../.tmp/concat/scripts/customDomain.js"] I think this looks weird so I trim it to... [500 / 910 chars] | "sources":["customDomain.js"] should be relative to the customDomain.map.js file. Make sure they are in the same directory on your server if this is the case for you. "file":"customDomain.js" should be changed to the name of the map file, in your case this would be "file":"customDomain.map.js". Here's a map file example taken from treehouse (sourceRoot may be unnecessary in your case): { version: 3, file: "script.js.map", sources: [ "app.js", "content.js", "widget.js" ], sourceRoot: "/", names: ["slideUp", "slideDown", "save"], mappings: "AAA0B,kBAAhBA,QAAOC,SACjBD,OAAOC,OAAO..." } [641 chars] |

### Public Sources

- [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883),
  2025.
- [mteb/StackOverflowQA](https://huggingface.co/datasets/mteb/StackOverflowQA).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | [https://arxiv.org/abs/2407.02883](https://arxiv.org/abs/2407.02883) |
| mteb/StackOverflowQA | 2024 | dataset card | [https://huggingface.co/datasets/mteb/StackOverflowQA](https://huggingface.co/datasets/mteb/StackOverflowQA) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A WinForms question about blocking mouse clicks from another form. | An answer explaining the bug investigation and final fix. |
| An Angular question about passing a parameter to `$resource`. | An answer showing the correct `$resource` object construction. |
| A Grunt/UglifyJS question about Chrome source maps. | An answer explaining relative source-map paths and file naming. |
| A MongoDB question about counting active looked-up array entries. | An aggregation-pipeline answer using unwind, lookup, match, and group. |
| An Inno Setup question about a running-app message. | An answer explaining the `%1` substitution in the setup message. |
