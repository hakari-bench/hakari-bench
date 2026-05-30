# NanoMTEB-Dutch / open_tender

## Overview

`open_tender` is a Dutch public-procurement retrieval task from MTEB-NL.
Queries are tender titles or short procurement descriptions, and documents are
tender call descriptions from Belgian and Dutch public procurement records. The
Nano split contains 199 queries, 10,000 documents, and 199 positive qrel rows,
with exactly one positive document per query. It evaluates retrieval over
administrative, contractual, supplier, service, construction, insurance, and
public-sector procurement language.

The task is a title-to-description retrieval problem with formal domain
vocabulary. BM25 is the strongest nDCG@10 source, dense retrieval is weaker,
and `reranking_hybrid` gives the highest hit@10 and recall@100. This indicates
that procurement titles often share important terms with the correct notice,
but hybrid search improves coverage by adding semantically related candidates.
The task is useful for evaluating whether retrieval systems can handle precise
public-sector descriptions and same-category hard negatives.

## Details

### What the Original Data Measures

[MTEB-NL and E5-NL](https://arxiv.org/abs/2509.12340) includes
OpenTenderRetrieval as a Dutch retrieval task based on Belgian and Dutch tender
calls. The retrieval framing matches tender titles or short title-like queries
to tender descriptions. No standalone paper for this exact retrieval dataset
was confirmed; interpretation relies on the MTEB-NL paper, the Hugging Face
source dataset card, MTEB metadata, and observed Nano examples.

This task adds a procurement domain that differs from news, QA, and fact
verification. The language is formal and administrative, often containing
terms such as framework agreement, European tender, service delivery,
maintenance, insurance, access control, construction, and public buyer names.

### Observed Data Profile

The split contains 199 queries over 10,000 documents. Queries average 62.19
characters, while documents average 442.03 characters. Documents can be very
short title-like notices or longer descriptions that explain contract scope,
buyer identity, procedure type, and deliverables.

Representative examples include thermal imaging cameras, construction of a
new service and administrative building, access-control systems, railway
infrastructure conversion under a framework agreement, and fire insurance for a
public safety region. The positive is usually the procurement notice matching
the title, but same-sector notices can be lexically close.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.6712, hit@10 = 0.7136, and recall@100 = 0.8090 over
top-500 candidate lists. BM25 is strong because tender titles and descriptions
often repeat exact procurement nouns, buyer names, procedure labels, and sector
terms. In this domain, lexical overlap is a meaningful signal rather than a
weak baseline.

The remaining errors come from administrative paraphrase and same-category
ambiguity. A title may be concise while the description uses a formal contract
scope. Many procurement notices share terms such as maintenance, delivery,
framework agreement, insurance, construction, or services. BM25 can retrieve
nearby notices while missing the exact tender.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.6044, hit@10 =
0.6734, and recall@100 = 0.8090. Dense retrieval ties BM25 in recall@100 but is
weaker in top-10 ranking. This suggests that dense similarity captures the
general procurement category but loses some exact title-description precision.

Dense retrieval may help when the tender title and description use different
administrative wording, but it can also overgeneralize among same-sector
notices. Public procurement data has many semantically similar records, so
exact identifiers and contract wording remain important.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.6556, hit@10 =
0.7286, and recall@100 = 0.8543, with 100 to 101 candidates per query and 29
rank-101 safeguard rows. It has the best hit@10 and recall@100, while BM25 has
the best nDCG@10. Hybrid retrieval therefore improves candidate coverage but
does not fully beat the sparse top order.

This pattern is typical for formal title matching. BM25 ranks many exact-title
or exact-scope matches well. Dense retrieval adds semantically related notices
that improve recall. A reranker can use the hybrid pool to decide which
same-sector candidate is the exact procurement notice.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 directly reflects the rank of the
matching tender notice. Hit@10 measures whether the correct notice is in a
short result list, and recall@100 measures reranking candidate coverage. BM25's
high nDCG@10 means exact procurement vocabulary is central to the benchmark.

Hybrid search is still useful because it increases the chance that the correct
notice is in the top-100 pool. The best system design is likely sparse-strong
candidate generation plus semantic reranking over same-category notices.

### Query and Relevance Type Tendencies

Queries are formal tender titles or short procurement descriptions. They often
name goods, services, infrastructure work, buyer organizations, or procedure
types. Relevant documents are procurement notices that describe the same
contract.

Relevance is notice identity. A document from the same sector or buyer is not
enough; it must correspond to the same tender title and contract scope.

### Representative Failure Modes

BM25 can fail when the query title and notice description use different
administrative wording or abbreviations. Dense retrieval can fail by retrieving
a same-sector procurement notice that is semantically similar but not the exact
contract. Hybrid retrieval can still rank broad category matches above the
true positive.

Hard negatives should be notices from the same municipality, buyer, sector,
procedure type, or contract category. These are more informative than random
procurement records.

### Training Data That May Help

Useful training data includes non-overlapping Dutch tender title-description
pairs, public procurement notices with category metadata, procurement search
logs and clicked tender records, and same-category hard negatives from tender
corpora. Training should exclude overlapping OpenTender titles, descriptions,
qrels, and evaluation rows.

Synthetic data can be generated from procurement notices outside the evaluation
set. Create Dutch tender descriptions with buyer, scope, procedure, and
contract details, then generate concise title-like queries. Hard negatives
should share the sector or procedure type but refer to a different contract.

### Model Improvement Notes

Improving this task requires exact title-scope matching. Sparse terms, buyer
names, and procurement vocabulary should be preserved. Dense models should be
trained with same-category hard negatives so that they do not rank every
similar service or construction notice as relevant.

For rerankers, the critical behavior is contract-identity matching: does the
candidate describe the same tender as the query, or merely a similar public
procurement item?

## Example Data

### Public Sources

- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.
- [clips/mteb-nl-opentender-ret](https://huggingface.co/datasets/clips/mteb-nl-opentender-ret), source dataset card.
- [MTEB project repository](https://github.com/embeddings-benchmark/mteb).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |
| clips/mteb-nl-opentender-ret |  | dataset card | https://huggingface.co/datasets/clips/mteb-nl-opentender-ret |
| MTEB project repository |  | repository | https://github.com/embeddings-benchmark/mteb |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Warmtebeeldcamera's | A Dutch procurement notice describes thermal imaging cameras for several safety regions. |
| Nieuwbouw van een vrijstaand gebouw voor dienstverlenende en administratieve functies | A Dutch tender lot describes elevators for new construction supporting mental-health services and administration. |
| Toegangscontrolesysteem | A Dutch notice describes delivery and installation of online wireless access-control systems. |
| Area North-West - Omvorming van spoorinfrastructuur - Raamovereenkomst | A Dutch tender description lists renewal and replacement work for rails, sleepers, ballast, and track equipment. |
| Europese aanbesteding brandverzekering Veiligheidsregio Zeeland | A Dutch notice describes a public European tender for fire-insurance agreements for a safety region. |
