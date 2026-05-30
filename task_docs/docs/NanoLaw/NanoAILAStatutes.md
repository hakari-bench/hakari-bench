# NanoLaw / NanoAILAStatutes

## Overview

`NanoLaw / NanoAILAStatutes` is an English legal statute-retrieval task based on
the AILA 2019 Artificial Intelligence for Legal Assistance track. Each query is
a long Indian legal factual scenario, and the corpus contains statutory
provisions with titles and descriptive legal text. The task is multi-label: a
single scenario can require several applicable statutes. The Nano split has 50
queries, 82 documents, and 217 positive qrel rows. Every query has multiple
positive statutes. Current diagnostics show that all candidate profiles have
full recall@100 because the corpus is small, while dense retrieval provides the
best top-10 ranking, `reranking_hybrid` is second, and BM25 is the weakest
top-10 profile.

## Details

### What the Original Data Measures

The FIRE 2019 AILA overview describes a statute retrieval task in which systems
receive 50 factual legal scenarios and identify the most relevant statutes. The
paper reports that the statute pool was built from frequently cited Indian
legal sections, reduced after removing repealed entries, and represented with
titles and descriptions. The MTEB `AILA_statutes` card follows the same task
framing: given a situation, retrieve applicable statutory provisions.

This task measures fact-to-statute mapping. It differs from precedent retrieval
because the target documents are not case judgments but statutory provisions.
The model must identify governing legal rules from long factual narratives,
often where the scenario implies the statute rather than naming it directly.

### Observed Data Profile

The Nano split contains 50 queries, 82 statute documents, and 217 positive qrel
rows. Every query is multi-positive. Positives per query average 4.34, with a
minimum of 2, a median of 4.5, and a maximum of 5. Queries average 3,038.42
characters, while statute documents average 1,972.63 characters.

The same long legal scenarios used in the AILA precedent task appear here, but
the relevance target changes. Instead of finding analogous cases, the model
must identify provisions such as attempt to murder, dowry death, criminal
conspiracy, compulsory registration of documents, or other applicable statutory
sections. The documents are shorter than judgments, but their wording is formal
and provision-specific.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset covers all 82 statutes for each
query and achieves nDCG@10 = 0.2070, hit@10 = 0.6600, and recall@100 = 1.0000.
BM25 has perfect top-100 coverage because the corpus is smaller than the
candidate limit, but its top-10 ordering is weak. Long factual narratives often
describe conduct, procedure, or legal consequences without repeating the exact
title or wording of the relevant statute.

Sparse matching helps when the scenario explicitly names an offence, procedure,
or legal term that also appears in the statute. It struggles when applicability
depends on legal classification: the model must infer that facts about injury,
dowry, conspiracy, registration, public duty, or evidence correspond to a
specific statutory provision. This makes BM25 a coverage baseline rather than a
strong final ranker.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset also covers all 82 statutes per
query. It achieves nDCG@10 = 0.2711, hit@10 = 0.7600, and recall@100 = 1.0000,
making it the strongest observed profile by top-10 ranking. Dense retrieval is
better suited to mapping long fact patterns to short legal provisions because
it can use semantic similarity between the scenario and statutory concepts.

The absolute nDCG@10 remains modest, which reflects the task's difficulty. A
scenario can activate multiple provisions, and many statutes are conceptually
near one another. The model must rank a set of applicable sections above
neighboring but non-governing provisions. Dense retrieval helps, but legal
entailment and issue spotting are still harder than generic semantic matching.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains all 82 documents per query,
with no safeguard rows. It achieves nDCG@10 = 0.2564, hit@10 = 0.7400, and
recall@100 = 1.0000. Hybrid retrieval improves over BM25 and approaches dense
retrieval, but it does not surpass dense in top-10 rank quality.

This pattern suggests that lexical statute names and semantic applicability
both matter, but dense evidence is more helpful for final ranking in this
particular split. Since every method sees the full corpus in the candidate
pool, the main question is ordering rather than recall. A reranker trained for
legal issue spotting could plausibly improve substantially over all three
candidate profiles.

### Metric Interpretation for Model Researchers

This is a multi-positive statute retrieval task. Hit@10 measures whether at
least one applicable statute appears in the first ten results. nDCG@10 rewards
ranking several applicable provisions high, which is important because every
query has between two and five positives. Recall@100 is saturated for all three
profiles because the 82-document corpus fits inside the top-100 candidate pool.

The metric pattern should therefore be read as a ranking-quality comparison,
not a candidate-coverage comparison. Dense retrieval ranks applicable statutes
best, hybrid follows, and BM25 has the weakest ordering despite full coverage.

### Query and Relevance Type Tendencies

Queries are long legal fact patterns with procedural history, allegations,
charges, and legal questions. Relevant documents are statutory provisions with
titles and descriptive clause text. A positive statute is one that governs the
scenario or is legally applicable to one of its issues.

The task rewards models that perform legal issue spotting: mapping facts to
offence categories, procedural requirements, evidence rules, registration
rules, or other statutory concepts. It is not enough to match shared words; the
system must identify which provisions the facts legally trigger.

### Representative Failure Modes

BM25 can miss high ranking when the scenario implies a statute without naming
it, or when multiple statutes share common legal vocabulary. Dense retrieval can
confuse neighboring legal provisions that are semantically similar but apply to
different factual elements. Hybrid retrieval can still rank a related statute
above the governing one if exact terms and semantic concepts point in different
directions.

Multi-positive relevance adds another issue: retrieving one applicable statute
does not mean the statutory set is complete. Systems that only optimize for one
best provision may underperform on nDCG when several provisions should be
ranked high.

### Training Data That May Help

Helpful training data includes fact-to-statute retrieval pairs, statutory legal
entailment examples, Indian penal and procedure statute hard negatives, and
multi-label legal issue spotting data. Training should preserve the long
scenario format and the multi-positive nature of the task.

For comparable evaluation, training should exclude NanoAILAStatutes scenarios,
qrels, and positive statute mappings. Synthetic data can help when it generates
case-like factual narratives that require several applicable statutes and
includes hard negatives from neighboring provisions.

### Model Improvement Notes

Dense retrievers should learn the relationship between factual elements and
statutory requirements, especially where the statute title is not stated in the
scenario. Sparse systems can improve with legal-aware term weighting for
offence names, procedure words, and statutory section language. Rerankers should
act more like legal issue spotters, checking whether each element of a statute
is supported by the scenario.

For hybrid systems, this task suggests that sparse evidence is useful but
should not dominate. Since coverage is already complete, the main improvement
target is ranking the governing provisions ahead of merely related provisions.

## Example Data

Representative queries include long appeal scenarios involving conviction,
dowry death allegations, sanction requirements for criminal proceedings,
criminal conspiracy, and partnership or property-registration questions.
Positive documents are statute provisions such as attempt to murder, dowry
death, punishment of criminal conspiracy, and compulsory registration of
documents.

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf),
  2019.
- [AILA 2019 Precedent & Statute Retrieval Task](https://doi.org/10.5281/zenodo.4063986),
  Zenodo dataset release.
- [mteb/AILA_statutes](https://huggingface.co/datasets/mteb/AILA_statutes),
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
| A long criminal appeal scenario involving legality of conviction and life sentence. | A statute provision titled "Attempt to murder" with clause text describing intention, knowledge, and punishment. |
| A scenario involving a conviction appeal and allegations connected to a woman's death. | A statute provision titled "Dowry death" with conditions about death within seven years of marriage. |
| A scenario involving criminal proceedings and official-duty questions. | A statute provision connected to criminal conspiracy or related procedural liability. |
| A question about whether sanction is required before criminal proceedings. | A governing statutory provision relevant to criminal liability or procedural authorization. |
| A partnership dissolution scenario about whether an award requires registration. | A statute provision titled "Documents of which registration is compulsory." |
