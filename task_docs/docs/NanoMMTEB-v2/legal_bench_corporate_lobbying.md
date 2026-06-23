# NanoMMTEB-v2 / legal_bench_corporate_lobbying

## Overview

`NanoMMTEB-v2 / legal_bench_corporate_lobbying` is an English legal-policy
retrieval task derived from LegalBench. Queries are bill titles or short policy
descriptions, and documents are bill records with structured legislative
summaries. The Nano split has 200 queries, 319 documents, and 200 positive qrel
rows, with exactly one positive document per query. Current diagnostics show
dense retrieval as the strongest nDCG@10 profile, BM25 as strongest on hit@10,
and `reranking_hybrid` as nearly tied with dense while matching BM25 recall.

## Details

### What the Original Data Measures

LEGALBENCH is a collaboratively built benchmark for legal reasoning. Its
`corporate_lobbying` task is an issue-spotting style task about whether a
proposed Congressional bill may implicate company or issue interests. The MTEB
retrieval version turns this into a bill retrieval task that matches policy
descriptions to bill records.

The task measures legislative and policy-issue retrieval. A model must connect
a bill objective, regulated activity, agency, population, or policy area to the
matching bill summary.

### Observed Data Profile

The Nano split contains 200 queries, 319 documents, and 200 positive qrel rows.
Every query has exactly one positive document. Queries average 179.67
characters, while documents average 1,157.21 characters.

Queries usually describe a bill objective, such as securing 5G infrastructure,
creating Native American business incubators, clarifying worker classification,
authorizing Middle East security assistance, or supporting carbon capture and
utilization. Documents contain bill names and structured summaries.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains all 319 documents per query
and achieves nDCG@10 = 0.8955, hit@10 = 0.9800, and recall@100 = 1.0000. BM25
is very strong because bill objectives and bill summaries often reuse
distinctive policy terms, agency names, program names, and regulated
technologies.

Lexical retrieval is especially effective when the query contains bill-specific
phrasing such as 5G security, Indian reservation business incubators, worker
classification, Israel assistance, or carbon dioxide utilization. The remaining
difficulty is broader policy paraphrase and same-policy-area hard negatives.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains all 319 documents per
query and achieves nDCG@10 = 0.9110, hit@10 = 0.9700, and recall@100 = 0.9800.
Dense retrieval has the best nDCG@10, though BM25 has slightly better hit@10
and recall@100.

This suggests that semantic matching helps when the query describes a policy
intent rather than repeating the exact bill summary. Dense retrieval can connect
objectives, affected actors, agencies, and remedies even when the wording
differs.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 candidates per query and
achieves nDCG@10 = 0.9080, hit@10 = 0.9700, and recall@100 = 1.0000. Hybrid
retrieval is nearly tied with dense retrieval on nDCG@10 and matches BM25 on
recall@100.

This is a strong hybrid-search profile. Sparse evidence preserves bill-specific
terms, while dense evidence helps with policy paraphrase. The small gap between
the profiles means errors are likely concentrated among same-domain bills with
similar regulated activity but different remedies or agencies.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has one matching bill record. Hit@10
measures whether that record appears near the top. nDCG@10 is sensitive to its
exact rank, and recall@100 measures whether it remains available to rerankers.

Because the corpus has only 319 documents, candidate coverage is relatively
easy. The meaningful signal is ranking quality among bills that share the same
policy area, agency, industry, or legal mechanism.

### Query and Relevance Type Tendencies

Queries are English bill objectives or short policy descriptions. They mention
legislative goals, regulated industries, federal agencies, appropriations,
programs, or affected populations. Relevant documents are bill records with
official titles and summaries.

The task rewards both exact policy-term matching and semantic issue spotting.
Good retrieval distinguishes bills that share a domain, such as health care,
telecommunications, firearms, defense, labor, or environmental regulation, but
implement different actions.

### Representative Failure Modes

BM25 can over-rank a bill with overlapping policy terms but the wrong remedy,
agency, or regulated activity. Dense retrieval can retrieve a semantically
similar bill in the same policy area while missing the specific title or
program named by the query. Hybrid retrieval can still confuse bills with
parallel legislative structure.

Rerankers should compare the bill's objective, affected actor, agency,
appropriation, and policy mechanism against the query.

### Training Data That May Help

Useful training data includes legislative title-to-summary retrieval, bill
classification and policy issue spotting data, same-policy-area bill hard
negatives, and legal or regulatory document search data. The Nano split's bill
queries, qrels, and positive bill summaries should be excluded from training.

Synthetic data can generate realistic Congressional bill titles and structured
summaries with policy scope, agencies, affected actors, exceptions, and
remedies. Queries should describe bill objectives or short policy scenarios.
Negatives should be same-domain bills that differ in remedy, agency, or
regulated activity.

### Model Improvement Notes

Sparse systems should preserve bill-specific phrases, acronyms, agency names,
and statutory program names. Dense retrievers should improve policy-intent
matching and same-domain discrimination. Rerankers should map query objectives
to bill summaries at the level of actor, action, and legal mechanism.

For hybrid systems, `NanoMMTEB-v2 / legal_bench_corporate_lobbying` is a
near-ceiling but still useful legislative retrieval test. Dense and hybrid
profiles are slightly stronger by nDCG@10, while BM25 remains a strong lexical
baseline.

## Example Data

| Query | Positive document |
| --- | --- |
| To require the President to develop a strategy to ensure the security of next generation mobile tele... [100 / 341 chars] | Secure 5G and Beyond Act of 2020 This bill requires the President, in consultation with relevant federal agencies, to develop (1) a strategy to secure and protect U.S. fifth and future generations (5G... [200 / 685 chars] |
| To establish a business incubators program within the Department of the Interior to promote economic... [100 / 147 chars] | Native American Business Incubators Program Act This bill requires the Department of the Interior to establish a grant program in the Office of Indian Energy and Economic Development for establishing... [200 / 826 chars] |
| To amend the Internal Revenue Code of 1986 to provide a safe harbor for determinations of worker cla... [100 / 168 chars] | New Economy Works to Guarantee Independence and Growth Act of 2019 or the NEW GIG Act of 2019 This bill establishes a test for determining if a service provider should be classified as an independent... [200 / 1,572 chars] |
| To make improvements to certain defense and security assistance provisions and to authorize theappro... [100 / 283 chars] | Strengthening America's Security in the Middle East Act of 2019 This bill authorizes assistance and weapons transfers to Israel, and extends defense cooperation with Jordan. It establishes additional... [200 / 1,724 chars] |
| To support carbon dioxide utilization and direct air capture research, to facilitate the permitting... [100 / 228 chars] | Utilizing Significant Emissions with Innovative Technologies Act or the USE IT Act This bill addresses the capture, utilization, and sequestration of carbon dioxide. The Environmental Protection Agenc... [200 / 1,562 chars] |

### Public Sources

- [LEGALBENCH: A Collaboratively Built Benchmark](https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf),
  2023.
- [LegalBench corporate_lobbying task page](https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html).
- [mteb/legalbench_corporate_lobbying](https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LEGALBENCH: A Collaboratively Built Benchmark | 2023 | benchmark paper | [https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf](https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf) |
| LegalBench corporate_lobbying task page | 2023 | task page | [https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html](https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html) |
| mteb/legalbench_corporate_lobbying | 2024 | dataset card | [https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying](https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A bill objective requiring a strategy for secure next-generation mobile telecommunications. | A bill record for the Secure 5G and Beyond Act of 2020. |
| A query about business incubators in Indian reservation communities. | A bill record for the Native American Business Incubators Program Act. |
| A query about safe harbor for worker classification. | A bill record for the NEW GIG Act of 2019. |
| A query about defense assistance for Israel and cooperation with Jordan. | A bill record for strengthening U.S. security in the Middle East. |
| A query about carbon dioxide utilization and direct air capture research. | A bill record for the USE IT Act. |
