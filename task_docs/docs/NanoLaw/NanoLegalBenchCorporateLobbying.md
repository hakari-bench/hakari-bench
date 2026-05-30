# NanoLaw / NanoLegalBenchCorporateLobbying

## Overview

`NanoLaw / NanoLegalBenchCorporateLobbying` is an English legislative retrieval
task derived from the LegalBench corporate lobbying task. In its original
LegalBench setting, the task asks whether a proposed congressional bill may be
relevant to a company based on the bill and the company's SEC 10-K description.
In this retrieval version, queries are bill titles or formal bill descriptions,
and documents are bill titles plus concise summaries. The Nano split has 200
queries, 319 documents, and one positive bill summary per query. Current
diagnostics are high across all methods: dense retrieval has the best nDCG@10,
BM25 has perfect recall@100 and very high hit@10, and `reranking_hybrid` is
close to dense while also preserving full top-100 coverage.

## Details

### What the Original Data Measures

LegalBench describes `corporate_lobbying` as an issue-spotting task. The
original question is whether a proposed congressional bill could be relevant to
a company, requiring reasoning about the legal consequences of the bill and
whether those consequences matter to the company's business model, structure,
or activities. The LegalBench task page lists it as a manually labeled
corporate lobbying task.

The retrieval formulation used here focuses on the bill side. A query is a
formal bill objective or title-like description, and the positive document is
the matching bill title and summary. This makes the Nano task closer to
legislative search than corporate impact analysis: it evaluates whether a model
can match a formal bill description to the correct summarized bill.

### Observed Data Profile

The Nano split contains 200 queries, 319 documents, and 200 positive qrel rows.
Each query has one positive document, with no multi-positive queries. Queries
average 179.67 characters. Documents average 1,157.21 characters and typically
contain a bill title followed by a compact summary of provisions.

Representative examples cover secure 5G infrastructure, Native American
business incubators, worker classification under the tax code, Middle East
security assistance, and carbon dioxide utilization or capture. The text is
formal legislative English, but much shorter and more structured than legal
case-law tasks.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers the 319-document corpus and
achieves nDCG@10 = 0.8955, hit@10 = 0.9800, and recall@100 = 1.0000. BM25 is
very strong because bill descriptions and summaries often share distinctive
policy terms, agency names, program names, statutes, or bill-specific phrases.
Formal legislative language is repetitive enough for exact matching to work
well.

BM25's small weakness is top-rank precision. Bills in the same policy area can
share many terms, such as security assistance, carbon capture, retirement
plans, or tax-code amendments. Sparse retrieval can keep the correct bill in
the candidate pool while ranking a closely related bill above it.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset covers the same 319 documents
and achieves nDCG@10 = 0.9108, hit@10 = 0.9750, and recall@100 = 0.9800. Dense
retrieval has the best nDCG@10, indicating that semantic matching helps order
closely related legislative summaries. It can connect a formal objective to a
summary even when wording differs.

The slight recall disadvantage shows that exact bill vocabulary still matters.
Dense retrieval may rank semantically related bills highly but miss a few
positives within the first 100. In this task, dense evidence is valuable for
ordering, while sparse evidence is valuable for exhaustive coverage.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.9068, hit@10 = 0.9700,
and recall@100 = 1.0000. Hybrid retrieval is very close to dense retrieval by
nDCG@10 and matches BM25's full top-100 coverage.

This profile reflects the task's mixed nature. Exact legislative terms,
acronyms, agency names, and statutes are strong signals, but semantic policy
matching helps when bill summaries paraphrase the query. Hybrid search gives a
robust candidate pool, although dense retrieval slightly edges it in top-rank
ordering for this split.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. Hit@10 measures whether the matching
bill summary appears in the top ten, nDCG@10 rewards ranking it near the top,
and recall@100 measures whether candidate generation keeps it available.

Because all scores are high, the task is mainly useful for fine-grained
legislative matching and regression testing. Dense retrieval's nDCG advantage
suggests that semantic policy alignment matters, while BM25 and hybrid recall
show that exact legislative phrasing remains important.

### Query and Relevance Type Tendencies

Queries are formal bill descriptions or titles, often beginning with "To
require", "To establish", or "To amend". Relevant documents are bill titles
plus summaries of the bill's requirements, authorizations, amendments, or
programs. The relevance relation is exact bill identity, not broad topic
similarity.

The task rewards models that recognize legislative objectives, agencies,
statutes, policy domains, and bill-specific acronyms. It also tests the ability
to distinguish bills in the same policy area that share surface vocabulary but
have different legal effects.

### Representative Failure Modes

BM25 can fail by ranking another bill from the same policy domain because it
shares agencies, statutes, or industry terms. Dense retrieval can fail by
ranking a semantically similar policy proposal that is not the same bill.
Hybrid retrieval can include both and still need final discrimination based on
bill-specific provisions.

Other likely errors include confusing authorization bills with appropriations,
mixing adjacent defense or energy bills, or overmatching broad policy terms
while missing the exact program or amendment described in the query.

### Training Data That May Help

Helpful training data includes bill-title to bill-summary retrieval,
legislative search data, corporate lobbying issue-spotting data, policy-domain
hard negatives, and summaries from the same committee or topic area. Training
should include same-policy negatives because most errors are likely among
closely related bills.

For comparable evaluation, training should exclude NanoLegalBenchCorporateLobbying
queries, qrels, and positive bill summaries. Synthetic data can help when it
generates formal bill descriptions and matching summaries with hard negatives
that share agencies or statutes but differ in policy effect.

### Model Improvement Notes

Dense retrievers can improve by representing exact legislative intent while
preserving bill-specific identifiers and policy details. Sparse systems already
perform very well, but should handle acronyms, agency names, statute names, and
formal title phrasing carefully. Rerankers should compare whether the summary
describes the same legislative proposal, not just the same policy domain.

For hybrid systems, this task is a calibration benchmark: both lexical and
semantic signals are strong, and the main ranking challenge is among near-
duplicate policy proposals.

## Example Data

Representative queries include descriptions of secure 5G strategy, a Native
American business incubator program, worker-classification safe harbors, Middle
East security assistance, and carbon capture or utilization research. Positive
documents are the corresponding bill titles and summaries.

### Public Sources

- [LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models](https://arxiv.org/abs/2308.11462),
  2023.
- [corporate_lobbying LegalBench task page](https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html).
- [mteb/legalbench_corporate_lobbying](https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying),
  source task dataset.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models | 2023 | arXiv paper | https://arxiv.org/abs/2308.11462 |
| corporate_lobbying | 2023 | LegalBench task page | https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A formal description requiring a strategy to secure next-generation mobile telecommunications infrastructure. | The Secure 5G and Beyond Act summary describing federal strategy for 5G and future systems. |
| A description establishing business incubators in Indian reservation communities. | The Native American Business Incubators Program Act summary. |
| A description amending the Internal Revenue Code for worker classification safe harbor. | A bill summary for the NEW GIG Act and independent-contractor classification. |
| A description authorizing security assistance to Israel and cooperation with Jordan. | A summary for a Middle East security assistance bill. |
| A description supporting carbon dioxide utilization and direct air capture research. | The USE IT Act summary addressing carbon capture, utilization, and sequestration. |
