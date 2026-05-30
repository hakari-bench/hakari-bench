# NanoLaw / NanoLegalSummarization

## Overview

`NanoLaw / NanoLegalSummarization` is an English contract-summary retrieval task.
Queries are plain-English summaries of contract or terms-of-service clauses,
and documents are the corresponding legal text snippets. The task reverses a
summarization resource into retrieval: given a simplified user-facing statement,
find the legal clause that entails it. The Nano split has 200 queries, 438
documents, and 345 positive qrel rows. It is moderately multi-positive, with 56
queries having more than one relevant clause. Current diagnostics show
`reranking_hybrid` as the strongest observed profile, dense retrieval slightly
above BM25, and BM25 still useful when summaries reuse legal or product terms.

## Details

### What the Original Data Measures

The Plain English Summarization of Contracts paper introduces a dataset of legal
text snippets paired with plain-English summaries, built from resources such as
TL;DRLegal and TOS;DR and manually checked for quality. The paper emphasizes
heavy abstraction, compression, and simplification: summaries often use words
that do not appear directly in the original legal text.

The MTEB legal summarization card frames the resource as contract-summary pairs.
In the Nano retrieval version, the query is the plain-English summary and the
target document is the original clause or legal snippet. The task therefore
measures clause retrieval under paraphrase and simplification.

### Observed Data Profile

The Nano split contains 200 queries, 438 documents, and 345 positive qrel rows.
Positives per query average 1.725, with a minimum of 1, a median of 1, and a
maximum of 11. Multi-positive queries account for 28.0 percent of the split.
Queries average 103.06 characters, while documents average 606.16 characters.

Representative summaries discuss location data collection, game modification
rules, deletion of virtual goods, unilateral changes to terms, and provider
access to uploaded content. The documents are contract clauses or short
terms-of-service snippets written in more formal legal language.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 438-document corpus and
achieves nDCG@10 = 0.5678, hit@10 = 0.7800, and recall@100 = 0.8667. BM25 is
helpful when the plain-English summary shares words with the clause, such as
`spam`, `real name`, `location`, `age`, `delete`, or `content`. Exact product
terms and user-rights vocabulary can be strong anchors.

BM25 is limited by the dataset's core abstraction. A summary may say that a
service can access, scan, or duplicate content, while the clause expresses that
right through broader license language. Sparse matching can also confuse
clauses that mention the same topic but differ in permission, obligation,
scope, or exception.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset covers 438 documents per query
and achieves nDCG@10 = 0.5861, hit@10 = 0.7850, and recall@100 = 0.9159. Dense
retrieval slightly improves over BM25 across the reported metrics. This fits
the task: the query is simplified language and the document is legalistic
language, so semantic paraphrase matching is valuable.

Dense retrieval still leaves room for improvement. Contract clauses can be
semantically close while differing in legal effect. A model may retrieve a
clause about account termination when the summary is specifically about virtual
goods, or retrieve a broad data-use clause when the positive is about location
data. The challenge is legal entailment, not just topical similarity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 13 safeguard positive rows and a mean of 100.065 candidates. It
achieves nDCG@10 = 0.6085, hit@10 = 0.8100, and recall@100 = 0.9246. This is
the strongest observed profile across all three metrics.

The hybrid result is intuitive. BM25 preserves exact terms, service names, and
clause vocabulary, while dense retrieval connects simplified summaries to
legal-language paraphrases. The combination is especially useful when the
summary is abstract but still contains a few decisive words. For reranking,
this is a good candidate pool because it balances lexical and semantic evidence.

### Metric Interpretation for Model Researchers

This task has both single-positive and multi-positive queries. Hit@10 measures
whether at least one relevant clause appears in the first ten results. nDCG@10
rewards ranking relevant clauses high, including cases where multiple clauses
can support the same summary. Recall@100 measures how much of the positive set
is available for reranking.

The current values show that plain-English contract summary retrieval is not
purely lexical and not purely semantic. Dense beats BM25 slightly, but hybrid
does best. The task is useful for evaluating whether a retrieval system can
connect simplified user-facing descriptions to formal legal clauses.

### Query and Relevance Type Tendencies

Queries are short, simplified summaries of rights, restrictions, data practices,
account rules, or user obligations. Documents are legal snippets that may use
formal and conditional language. The positive document must entail the summary,
not merely share a topic.

The task rewards models that understand contractual permissions, restrictions,
exceptions, and scope. It also requires handling colloquial or simplified
phrasing, such as "we can delete your virtual goods" or "you may mod the game",
and connecting it to legal text.

### Representative Failure Modes

BM25 can fail when the summary paraphrases the clause without shared wording.
Dense retrieval can fail when two clauses are semantically close but differ in
legal effect, such as permission versus prohibition or provider right versus
user obligation. Hybrid retrieval can still rank adjacent clauses high when
they share both topic and vocabulary but do not entail the summary.

Multi-positive cases add another issue: several clauses can support the same
summary, and ranking only one may not capture the full relevance set.

### Training Data That May Help

Useful training data includes contract-summary pairs, terms-of-service
simplification, clause-to-description retrieval, contract entailment, and hard
negatives from adjacent clauses about nearby user rights. Training should
preserve distinctions in permission, obligation, exception, and scope.

For comparable evaluation, training should exclude NanoLegalSummarization
summaries, qrels, and positive clauses. Synthetic data can help when it
generates legalistic clauses and plain-English summaries that remain entailed
but do not copy clause wording.

### Model Improvement Notes

Dense retrievers can improve by learning legal simplification and entailment,
not only topical similarity. Sparse systems benefit from service names, rights
terms, and obligation vocabulary, but should be paired with semantic matching.
Rerankers should check whether the clause actually entails the summary and
whether exceptions or limitations change the legal effect.

For hybrid systems, `NanoLegalSummarization` is a strong fit: lexical signals
and embedding similarity each recover different positives, and the observed
`reranking_hybrid` profile is best overall.

## Example Data

Representative summaries say that a service may collect and share location
data, that users may modify a game but should not distribute hacked clients,
that virtual goods can be deleted, that terms may change without user
involvement, and that Dropbox and third parties may access or process uploaded
content. Positive documents are the corresponding contract clauses.

### Public Sources

- [Plain English Summarization of Contracts](https://arxiv.org/abs/1906.00424),
  2019.
- [legal_summarization GitHub repository](https://github.com/lauramanor/legal_summarization),
  source repository.
- [mteb/legal_summarization](https://huggingface.co/datasets/mteb/legal_summarization),
  source task dataset.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Plain English Summarization of Contracts | 2019 | arXiv paper | https://arxiv.org/abs/1906.00424 |
| legal_summarization | 2019 | GitHub repository | https://github.com/lauramanor/legal_summarization |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A plain summary saying the service may collect, use, and share location data. | A clause allowing Apple and partners to collect, use, and share precise location data. |
| A summary saying users may modify a game but should not distribute hacked clients. | A clause permitting mods or plugins while restricting distribution of changed software. |
| A summary saying virtual goods can be deleted or discontinued. | A clause allowing account termination or cancellation of virtual money and goods. |
| A summary saying the service can make critical changes to terms without user involvement. | A clause reserving the right to modify or replace terms at the provider's discretion. |
| A summary saying Dropbox and third parties may access or process uploaded content. | A clause granting limited rights needed to provide services involving user files and content. |
