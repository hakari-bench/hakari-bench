# NanoMTEB-French / bsard

## Overview

`bsard` is the Belgian Statutory Article Retrieval Dataset in French. Queries
are lay legal questions, and documents are Belgian statutory articles. The Nano
split contains 200 queries, 10,000 documents, and 200 positive qrel rows, with
exactly one positive article per query. It evaluates whether a retrieval model
can map ordinary legal problems to the statutory article that grounds the
answer.

This is a hard legal retrieval task because citizen language and statutory
language often diverge. BM25 is weak, dense retrieval with
`harrier_oss_v1_270m` is substantially stronger, and `reranking_hybrid` has the
highest nDCG@10 but lower hit@10 and recall@100 than dense. The task is useful
for testing French legal semantic retrieval, especially the ability to connect
plain-language questions about debt, tenancy, inheritance, legal aid, and
procedure to formal Belgian law articles.

## Details

### What the Original Data Measures

[A Statutory Article Retrieval Dataset in French](https://arxiv.org/abs/2108.11792)
introduces BSARD as a French legal retrieval dataset with questions labeled by
jurists against Belgian statutory articles. The paper emphasizes the mismatch
between non-expert legal questions and formal law text, as well as the
hierarchical structure of legal codes.

In this Nano version, the query is a lay legal question and the relevant
document is a statute article. The task is not general legal FAQ retrieval; it
requires article-level statutory grounding.

### Observed Data Profile

Queries average 144.97 characters and often include both a natural question
and category-like legal context. Documents average 793.01 characters and are
formal statutory text with article sections, legal clauses, and enumerated
conditions. The split has one positive article per query.

Examples cover annual campsite caravan rental in Brussels, modifying a
testament, court costs after contesting a social-security decision, repairs
that a landlord does not perform, and understanding a water bill in Wallonia.
The positive article may not use the same words as the lay question.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.1943, hit@10 = 0.3350, and recall@100 = 0.5500 over
top-500 candidate lists. This weak sparse profile reflects the lay-to-law
vocabulary gap. A query may mention a practical problem, while the statute uses
formal legal categories and article language.

BM25 succeeds when the query contains exact terms from the code, such as a law
name, legal procedure, or distinctive phrase. It fails when the user describes
the situation in ordinary language or when many articles share similar legal
terms.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.3023, hit@10 =
0.4550, and recall@100 = 0.7250. Dense retrieval is much stronger than BM25
because it better connects lay legal intent with formal statutory concepts. It
is the best source for hit@10 and recall@100.

Dense retrieval still leaves many failures because legal articles are precise.
Several provisions can concern the same procedure or right while differing in
jurisdiction, condition, or exception. A dense model must distinguish statutory
scope, not only legal topic.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3048, hit@10 =
0.4350, and recall@100 = 0.6750, with 100 to 101 candidates per query and 65
rank-101 safeguard rows. It has the highest nDCG@10 but lower hit and recall
than dense retrieval. This suggests that hybrid search can rank some positives
slightly higher when sparse legal terms help, but the restricted hybrid pool
misses more positives than dense top-500.

For reranking, the hybrid candidate set is useful but should be monitored for
coverage. Dense retrieval appears to supply broader access to the correct law
articles, while hybrid order can help when exact code terms are present.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 measures the rank of the one target
statutory article. Hit@10 measures practical legal-search visibility, and
recall@100 measures whether a reranker can access the correct provision.

The central observation is that sparse legal terms alone are not enough. Dense
semantic matching is critical, but final ranking still requires legal scope
discrimination.

### Query and Relevance Type Tendencies

Queries are French lay legal questions about tenancy, debt, social-security
procedure, legal aid, family matters, wills, and administrative benefits.
Relevant documents are formal Belgian statutory articles.

Relevance is statutory basis. A document about the same legal topic is not
sufficient unless it provides the article needed to address the question.

### Representative Failure Modes

BM25 can fail when the query uses everyday language instead of statute
terminology. Dense retrieval can fail when it retrieves the right legal topic
but the wrong article or jurisdiction. Hybrid retrieval can over-rank articles
that share legal terms but do not answer the specific question.

Hard negatives should come from the same Belgian code, legal topic, or
procedure, because those are the realistic confusions.

### Training Data That May Help

Useful training data includes non-overlapping BSARD train examples, French
legal question-to-statute retrieval pairs, legal FAQ to code article mappings,
and hard negatives from the same Belgian code or legal topic. Training should
exclude BSARD test questions, Nano queries, qrels, and positive Belgian law
articles likely to overlap with this evaluation.

Synthetic data can pair formal French Belgian-style statutory articles with
lay French legal questions about debt, rental law, family law, legal aid,
procedure, and benefits. Each positive article should provide the statutory
basis needed to address the lay question.

### Model Improvement Notes

Improving this task requires legal semantic alignment and article-level
precision. Dense encoders should be trained on lay-question-to-statute pairs
with same-code hard negatives. Rerankers should compare the user's situation
against legal conditions, exceptions, and jurisdiction.

The task is a strong diagnostic for French legal retrieval because it exposes
both vocabulary mismatch and statutory-scope errors.

## Example Data

### Public Sources

- [A Statutory Article Retrieval Dataset in French](https://arxiv.org/abs/2108.11792), 2022.
- [mteb/BSARDRetrieval](https://huggingface.co/datasets/mteb/BSARDRetrieval), source dataset card.
- [MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468), 2024.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Statutory Article Retrieval Dataset in French | 2022 | arXiv paper | https://arxiv.org/abs/2108.11792 |
| MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis | 2024 | arXiv paper | https://arxiv.org/abs/2405.20468 |
| mteb/BSARDRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/BSARDRetrieval |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Je loue une caravane dans un camping à l'année. Quelles règles s'appliquent à mon bail à Bruxelles? | A Belgian statutory article describes when tenancy provisions apply to housing used as the tenant's principal residence. |
| J'ai fait un testament. Puis-je le modifier? | A statutory passage describes a testament received by a notary in the presence of witnesses or by two notaries. |
| Dois-je payer les frais de justice si je conteste une décision d'un organisme de sécurité sociale? | A legal article describes procedural indemnity and fixed intervention in lawyer fees for the winning party. |
| Mon propriétaire ne fait pas les réparations nécessaires, puis-je faire les réparations à sa place à Bruxelles? | A statutory article discusses tenant obligations for rental repairs and maintenance, with exceptions. |
| Comment lire et comprendre ma facture d'eau en Wallonie? | A legal article describes annual water bills and intermediate invoices issued by the distributor. |
