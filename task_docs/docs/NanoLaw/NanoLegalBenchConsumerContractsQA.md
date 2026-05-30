# NanoLaw / NanoLegalBenchConsumerContractsQA

## Overview

`NanoLaw / NanoLegalBenchConsumerContractsQA` is an English legal retrieval task
derived from LegalBench's consumer contract question answering task. Queries
are yes/no consumer questions about online terms of service, and documents are
contract clauses or sections that contain the answer. The task tests whether a
retrieval model can find the relevant clause for questions about permissions,
fees, parental consent, scraping, data sharing, account transfer, intellectual
property, liability, and dispute terms. The Nano split has 200 queries, 153
documents, and one positive clause per query. Current diagnostics show
`reranking_hybrid` as the strongest observed profile, with BM25 and dense
retrieval both strong but each missing different cases.

## Details

### What the Original Data Measures

LegalBench describes `consumer_contracts_qa` as an interpretation task for
legal reasoning over consumer contracts, especially terms of service. The task
contains yes/no questions and alternative wordings about online services,
rights, obligations, eligibility, payments, intellectual property, liability,
and dispute resolution. The LegalBench task page identifies it as yes/no QA and
points to the consumer-contract dataset work by Noam Kolt.

In the retrieval formulation, the question is the query and the relevant
document is the contract section needed to answer it. This turns a legal QA
task into clause retrieval. The model is not expected to produce the yes/no
answer directly; it must identify the clause that supports the answer.

### Observed Data Profile

The Nano split contains 200 queries, 153 documents, and 200 positive qrel rows.
Every query has exactly one positive document, with no multi-positive queries.
Queries average 97.22 characters. Documents average 2,743.33 characters and are
terms-of-service sections from services such as Instagram, Facebook, YouTube,
Yahoo, eBay, Reddit, Google, Verizon, and Disney.

Representative questions ask whether Instagram and Facebook share user data,
whether a user may have to pay for services, whether minors need parental
permission for YouTube, whether automated scraping of YouTube video data is
allowed, and whether eBay prohibits account transfers. The positives are
service-specific clauses that may answer the question directly or require
interpreting a permission, prohibition, exception, or obligation.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 153-document corpus and
achieves nDCG@10 = 0.7556, hit@10 = 0.9100, and recall@100 = 0.9900. BM25 is
strong because questions often reuse provider names, product names, and legal
concepts from the relevant clauses. Terms such as fees, parental permission,
data sharing, scraping, accounts, copyright, and services are highly useful
lexical anchors.

BM25 is not perfect because contract interpretation often depends on wording
that is semantically related but not identical to the consumer question. A
clause may express a prohibition through a list of restricted uses, or state a
permission as part of a broader license. Sparse retrieval can also be distracted
by same-provider clauses that share the service name but address a different
right or obligation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset also covers the 153-document
corpus and achieves nDCG@10 = 0.7785, hit@10 = 0.9050, and recall@100 = 0.9650.
Dense retrieval slightly improves nDCG@10 over BM25, indicating that semantic
question-clause alignment helps. It can connect a consumer-facing question to a
contractual formulation that uses different wording.

Dense retrieval's hit@10 and recall@100 are slightly lower than BM25's. This
suggests that exact provider names and contractual terms remain important.
Because many clauses from the same service are present, dense retrieval may
rank a semantically related but legally different section above the exact
answering clause.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.8054, hit@10 = 0.9350,
and recall@100 = 1.0000. This is the strongest observed profile across the main
metrics.

The hybrid result fits the task well. BM25 contributes provider names and exact
contract vocabulary, while dense retrieval contributes semantic matching
between consumer questions and clause language. Combining both is especially
useful for questions that are phrased plainly while the contract uses legal or
policy language. For reranking, the hybrid candidate pool gives full positive
coverage and the best top-10 starting point.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. Hit@10 measures whether the answering
clause appears in the first ten results, while nDCG@10 rewards ranking it near
the top. Recall@100 measures whether candidate generation keeps the clause
available for reranking.

The metric pattern shows a balanced legal-clause retrieval task: BM25 is strong,
dense is slightly better by nDCG, and hybrid is clearly best overall. This
makes the task a useful diagnostic for whether a retrieval system can combine
exact terms-of-service anchors with semantic interpretation of rights and
obligations.

### Query and Relevance Type Tendencies

Queries are plain-English yes/no questions a consumer might ask about a service
contract. Relevant documents are contract sections, often longer than the
question and written in formal policy language. The positive clause contains
the information required to answer the question, even if the answer is embedded
inside a broader list of terms.

The task rewards models that understand provider-specific context, contractual
permissions and prohibitions, obligation language, exceptions, and cross-service
data or account rules. It is not enough to retrieve any clause from the same
provider.

### Representative Failure Modes

BM25 can fail by overmatching provider names while choosing the wrong clause.
Dense retrieval can fail by choosing a semantically related policy section that
does not answer the precise legal question. Hybrid retrieval reduces these
risks but still requires a reranker to distinguish permissions from
prohibitions, default rules from exceptions, and user obligations from service
rights.

Another common error is confusing different topics within the same contract,
such as content licenses, account restrictions, payment terms, privacy/data
sharing, or dispute resolution.

### Training Data That May Help

Useful training data includes consumer-contract QA, terms-of-service clause
retrieval, contract entailment over rights and obligations, and hard negatives
from the same provider or same topic. Training should include plain-language
questions paired with formal clauses and should preserve legal distinctions
such as may, must, may not, except, and unless.

For comparable evaluation, training should exclude NanoLegalBenchConsumerContractsQA
questions, qrels, and positive contract clauses. Synthetic data can help when
it generates realistic terms-of-service clauses with permissions, duties,
exceptions, remedies, and yes/no consumer questions.

### Model Improvement Notes

Dense retrievers can improve by learning contract entailment and consumer-to-
legal language paraphrase. Sparse systems benefit from preserving provider
names and contractual terms, but should avoid relying only on service names.
Rerankers should evaluate whether a clause actually answers the yes/no question
and whether the clause states a permission, prohibition, requirement, or
exception.

For hybrid systems, this task is a good fit: exact contractual vocabulary and
semantic interpretation both matter, and the observed `reranking_hybrid`
profile is the strongest of the three.

## Example Data

Representative queries ask whether Instagram and Facebook share user data,
whether a user might have to pay for services, whether minors need parental
permission for YouTube, whether automated scraping of YouTube data is allowed,
and whether eBay prohibits account transfers. Positive documents are the
specific terms-of-service sections that answer those questions.

### Public Sources

- [LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models](https://arxiv.org/abs/2308.11462),
  2023.
- [consumer_contracts_qa LegalBench task page](https://hazyresearch.stanford.edu/legalbench/tasks/consumer_contracts_qa.html).
- [Predicting Consumer Contracts](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3844988),
  2022.
- [mteb/legalbench_consumer_contracts_qa](https://huggingface.co/datasets/mteb/legalbench_consumer_contracts_qa),
  source task dataset.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models | 2023 | arXiv paper | https://arxiv.org/abs/2308.11462 |
| consumer_contracts_qa | 2023 | LegalBench task page | https://hazyresearch.stanford.edu/legalbench/tasks/consumer_contracts_qa.html |
| Predicting Consumer Contracts | 2022 | law review article | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3844988 |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A question asking whether Instagram and Facebook share user data. | An Instagram terms section describing the Instagram service and relationship with Facebook products. |
| A question asking whether the user may have to pay money for services. | A services clause addressing authority, use, and possible paid services or charges. |
| A question asking whether minors require parental permission for YouTube. | A YouTube introduction or service terms section describing eligibility and use by minors. |
| A question asking whether automated scraping of YouTube video data is allowed. | A YouTube content or service-use clause restricting automated access or scraping. |
| A question asking whether eBay prohibits transfer of eBay accounts. | An eBay services clause listing prohibited conduct, including account-transfer restrictions. |
