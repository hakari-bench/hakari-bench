# NanoLaw / NanoAILACasedocs

## Overview

`NanoLaw / NanoAILACasedocs` is an English legal precedent-retrieval task based
on the AILA 2019 Artificial Intelligence for Legal Assistance track. Each query
is a long factual legal scenario, and the corpus consists of Indian Supreme
Court case documents. The retrieval goal is to find prior cases that are
relevant as precedents, not merely documents that share the same words. The Nano
split has 50 queries, 186 documents, and 195 positive qrel rows. Most queries
have multiple positives: 40 of 50 queries have more than one relevant case.
Current diagnostics show dense retrieval as the strongest nDCG@10 profile,
`reranking_hybrid` as the best hit@10 and recall@100 profile, and BM25 as a
useful but weaker legal lexical baseline.

## Details

### What the Original Data Measures

The FIRE 2019 AILA overview defines legal assistance retrieval tasks for Indian
law, including prior-case retrieval and statute retrieval. In the prior-case
task, systems receive a natural-language factual scenario and must identify
relevant prior cases from Indian Supreme Court case documents. The paper
describes the gold labels as based on cases cited by lawyers in the original
documents, while noting limitations of the available gold standard.

The MTEB `AILA_casedocs` card follows this precedent-retrieval framing. The
task is not a general web search problem and not ordinary passage QA. It
measures whether a model can connect a long case scenario to legally analogous
case documents, including procedural posture, charges, statutory issues,
material facts, and legal reasoning.

### Observed Data Profile

The Nano split contains 50 queries, 186 documents, and 195 positive qrel rows.
There are 3.90 positives per query on average, with a minimum of 1, a median of
3, and a maximum of 22. Multi-positive queries account for 80.0 percent of the
task. Queries are long, averaging 3,038.42 characters. Documents are full or
near-full judgments averaging 26,947.34 characters.

The sampled scenarios include criminal appeals, procedural questions, sanction
requirements, partnership dissolution, constitutional or public-law questions,
and land or property disputes. Both query and document text include formal
legal language, citations, party roles, procedural history, and long narrative
facts. The task therefore tests legal-relevance matching across long documents,
not short keyword lookup.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset effectively covers the 186-document
corpus for each query and achieves nDCG@10 = 0.2805, hit@10 = 0.6200, and
recall@100 = 0.9128. BM25 is useful because legal texts repeat charge labels,
statutory terms, court names, procedural phrases, and party-role vocabulary.
When the scenario and precedent share those surface markers, sparse retrieval
can keep relevant cases available.

However, BM25 is clearly weaker than dense retrieval in top-10 rank quality.
Precedent relevance often depends on legal analogy rather than direct term
frequency. Two cases can share offences or statutes while differing in the
decisive legal issue, and two legally analogous cases may use different factual
phrasing. BM25 therefore provides a baseline for lexical overlap, not a full
model of precedent relevance.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset also covers the 186-document
corpus for each query. It achieves nDCG@10 = 0.4003, hit@10 = 0.6800, and
recall@100 = 0.9026. Dense retrieval is the strongest observed profile by
nDCG@10, suggesting that semantic similarity helps rank legally relevant cases
above cases that merely share surface terms.

The dense advantage fits the task's nature. A query may describe a factual and
procedural situation whose relevant precedents turn on analogous reasoning,
sanction requirements, evidentiary posture, or partnership-law consequences.
Dense retrieval can capture broader scenario similarity and legal-topic
alignment. Its slightly lower recall@100 than BM25 and hybrid also shows that
exact legal terminology remains important for candidate coverage.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 2 safeguard positive rows and a mean of 100.04 candidates. It
achieves nDCG@10 = 0.3667, hit@10 = 0.7000, and recall@100 = 0.9436. The hybrid
profile has the best observed hit@10 and recall@100, while dense retrieval has
the best nDCG@10.

This split illustrates why legal search often benefits from hybrid retrieval.
BM25 contributes exact legal anchors such as statute names, offences, citation
language, and procedural phrases. Dense retrieval contributes analogical
matching across long fact patterns and legal reasoning. Hybrid retrieval keeps
more positives available and finds at least one relevant case for more queries,
but its ordering of the first ten results still needs a reranker that can rank
the most legally useful precedents first.

### Metric Interpretation for Model Researchers

This task is multi-positive, so metrics should be interpreted as precedent-set
retrieval rather than single-answer retrieval. Hit@10 measures whether at least
one relevant prior case appears in the top ten. nDCG@10 rewards ranking multiple
relevant precedents high, and is sensitive to whether the best results are all
legally useful. Recall@100 measures how much of the cited precedent set remains
available for reranking.

The current pattern is nuanced: dense is best for ranking quality, hybrid is
best for finding at least one relevant precedent and retaining positives, and
BM25 is weaker but still valuable. A strong legal retrieval system should be
evaluated on both early precision and coverage of the broader precedent set.

### Query and Relevance Type Tendencies

Queries are long factual scenarios written in formal legal English. They often
include procedural background, statutory questions, appeal posture, factual
allegations, and a summary of the issue before the court. Relevant documents are
prior case judgments. Relevance is legal and precedential: a case can be
relevant because it was cited or because it resolves a materially similar issue,
not because it contains the same sentence as the query.

This task rewards models that can handle long legal narratives, distinguish
material facts from background details, and identify legal analogies across
cases. It is also sensitive to citation-style vocabulary and jurisdiction-
specific terminology from Indian law.

### Representative Failure Modes

BM25 can fail by ranking cases that share charges, statutes, or procedural
phrases but do not address the same legal issue. Dense retrieval can fail by
ranking factually similar cases that are not cited precedents, or by smoothing
over crucial distinctions in procedural posture. Hybrid retrieval can preserve
more candidate positives but still needs final ranking that understands legal
materiality.

Long documents introduce additional difficulty. A judgment may contain many
issues, facts, and citations, only some of which are relevant to the query. A
model that represents the full document too coarsely may match the wrong part
of the case.

### Training Data That May Help

Useful training data includes non-overlapping legal precedent retrieval pairs,
case-citation prediction, Indian legal case retrieval corpora, and hard
negatives from cases sharing statutes or charges but not legal reasoning.
Training should preserve long factual scenarios and full judgment documents
rather than converting the task into short keyword search.

For comparable evaluation, training should exclude the NanoAILACasedocs queries,
qrels, and cited precedent documents. Multi-positive training is important
because most queries in this split have several relevant prior cases.

### Model Improvement Notes

Dense retrievers can improve by learning legal issue similarity and citation-
style precedent relationships, not just topical similarity. Sparse systems
benefit from legal-aware tokenization and weighting of statutes, charges,
sections, and citation terms. Rerankers should compare the query's material
facts and issue posture against the candidate judgment's holding and reasoning.

For hybrid legal retrieval, this task supports a design where sparse retrieval
protects legal terminology coverage, dense retrieval adds analogical scenario
matching, and the reranker resolves which cases are truly precedential.

## Example Data

Representative queries include long criminal appeal scenarios, questions about
sanction requirements for criminal proceedings, appeals involving conviction
and sentence confirmation, witness or contempt-related procedural issues, and
questions about whether distribution of partnership assets requires
registration. Positive documents are Indian Supreme Court case judgments such as
prior criminal appeals, sanction cases, and partnership-law precedents.

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf),
  2019.
- [AILA 2019 Precedent & Statute Retrieval Task](https://doi.org/10.5281/zenodo.4063986),
  Zenodo dataset release.
- [mteb/AILA_casedocs](https://huggingface.co/datasets/mteb/AILA_casedocs),
  MTEB source dataset.
- [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | CEUR paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | Zenodo dataset | https://doi.org/10.5281/zenodo.4063986 |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A long criminal appeal scenario challenging conviction and life sentence. | A prior Supreme Court criminal appeal judgment relevant to conviction, sentence, and appellate review. |
| A scenario involving appeal from a High Court order confirming conviction. | A Supreme Court criminal appeal precedent with comparable procedural posture. |
| A scenario about a witness and later proceedings connected to a criminal trial. | A prior case discussing procedural and evidentiary issues around the proceeding. |
| A question about whether sanction is required before initiating criminal proceedings. | A precedent addressing sanction requirements and official-duty related criminal proceedings. |
| A question about distribution of partnership assets on dissolution and registration. | A Supreme Court precedent addressing partnership dissolution and registration of an award. |
