# NanoMTEB-Dutch / sci_fact_nl

## Overview

`sci_fact_nl` is the Dutch SciFact retrieval task from BEIR-NL. Queries are
Dutch translations of scientific claims, and documents are translated
scientific-paper abstracts. The Nano split contains 200 queries, 5,183
documents, and 226 positive qrel rows. Most claims have one positive abstract,
but 16 queries have multiple positives, with at most five positives for one
query. It evaluates scientific evidence retrieval for claim verification.

The task is harder than ordinary entity retrieval because relevance depends on
whether an abstract supports or refutes a precise claim. BM25 is a useful
baseline because gene names, diseases, interventions, and technical phrases
often overlap. Dense retrieval with `harrier_oss_v1_270m` has the strongest
nDCG@10 and hit@10, while `reranking_hybrid` has the highest recall@100. This
is a strong example of dense retrieval helping with scientific relation
matching, with hybrid search providing broader reranking coverage.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduced SciFact as a scientific claim-verification dataset with
expert-written claims, evidence abstracts, support/refute labels, and evidence
rationales. BEIR uses SciFact as a retrieval task: given a scientific claim,
retrieve abstracts that provide evidence for or against it.

BEIR-NL translates public BEIR datasets into Dutch. This split is therefore
Dutch-translated scientific evidence retrieval, not a natively authored Dutch
scientific-claim corpus. Scientific terminology, names, abbreviations, and
measurement expressions often remain important even after translation.

### Observed Data Profile

The split contains 200 claims and 5,183 abstracts. Queries average 100.13
characters, much longer than ordinary web questions, and documents average
1,640.32 characters. Abstracts include titles, methods, measurements,
interventions, populations, and findings. The claim usually states a specific
scientific relation or result.

Representative claims concern metastatic colorectal cancer treatment, CRP as a
predictor after coronary bypass surgery, the role of arginine 90 in p150
interaction with EB1, whether obesity is determined only by environmental
factors, and the effect of febrile seizures on later epilepsy. These are
precise claim-evidence relationships, not broad topic searches.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.6160, hit@10 = 0.7900, and recall@100 = 0.8363 over
top-500 candidate lists. Sparse retrieval works reasonably well because claims
and abstracts often share technical terms, disease names, genes, interventions,
or outcome measures. Exact terminology is a real signal in scientific
retrieval.

BM25's limitation is relation specificity. An abstract can share the same
entities but report a different outcome, study design, or conclusion. A claim
about increased risk, reduced effectiveness, or molecular interaction requires
matching the finding, not just the vocabulary.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.6758, hit@10 =
0.8300, and recall@100 = 0.9336. Dense retrieval is the strongest top-ranked
candidate source. It appears to capture scientific claim-to-abstract semantics
better than BM25, especially when the evidence is phrased differently from the
claim.

The remaining dense errors are likely terminology-sharing hard negatives.
Scientific abstracts can be close in embedding space because they mention the
same disease, gene, or method while supporting a different conclusion. A strong
model must preserve directionality, measurement, and evidence relation.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.6709, hit@10 =
0.8200, and recall@100 = 0.9558, with 100 to 101 candidates per query and 10
rank-101 safeguard rows. It has the highest recall@100, while dense retrieval
has slightly better top-10 ranking. This makes hybrid search the best reranking
candidate pool.

Hybrid retrieval combines BM25's exact scientific terminology with dense
semantic evidence matching. A reranker can then decide whether the candidate
abstract actually supports or refutes the claim, rather than merely sharing
scientific vocabulary.

### Metric Interpretation for Model Researchers

The task has 226 positives for 200 queries, so it is mostly single-positive but
not entirely. nDCG@10 and hit@10 are useful for first-stage ranking, while
recall@100 measures candidate availability for a reranker. Dense retrieval is
the best top-rank signal; hybrid retrieval gives broader coverage.

The important comparison is not only sparse versus dense. It is whether the
system can retrieve evidence that matches the claim's scientific relation.
Entity overlap alone is not enough.

### Query and Relevance Type Tendencies

Queries are precise scientific claims. They often contain biomedical entities,
interventions, outcomes, molecular relations, or statistical conclusions.
Relevant documents are abstracts that support or refute the claim.

Relevance is evidence bearing. A document about the same disease or gene is not
necessarily relevant unless it contains the finding needed to verify the claim.

### Representative Failure Modes

BM25 can fail by retrieving abstracts with shared terminology but incompatible
findings. Dense retrieval can fail by overgeneralizing among abstracts about
the same topic. Hybrid retrieval can include both the right evidence and
terminology-sharing distractors, so reranking remains important.

Hard negatives should share diseases, genes, methods, or interventions while
changing the result or relation. These negatives are critical for claim
verification retrieval.

### Training Data That May Help

Useful training data includes official SciFact training data with overlap
removed, scientific claim-verification retrieval datasets, biomedical abstract
retrieval pairs, and Dutch or multilingual scientific evidence pairs. Training
should exclude translated SciFact test claims, qrels, and evidence abstracts
used by this Nano split.

Synthetic data can be generated from non-evaluation scientific abstracts.
Create precise Dutch claims that are supported or refuted by explicit findings.
Hard negatives should share terminology but imply a different result or
relation.

### Model Improvement Notes

Improving this task requires scientific relation modeling. Dense encoders
should capture claim direction, entity roles, and outcome wording. Rerankers
should compare the claim to the abstract's findings and not stop at keyword or
topic overlap.

Hybrid retrieval is useful as a high-recall source, but final quality depends
on evidence-aware ranking.

## Example Data

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974), 2020.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [clips/beir-nl-scifact](https://huggingface.co/datasets/clips/beir-nl-scifact), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | arXiv paper | https://arxiv.org/abs/2004.14974 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | ACL paper | https://aclanthology.org/2025.bucc-1.5/ |
| clips/beir-nl-scifact |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-scifact |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Metastatische colorectale kanker behandeld met enkelvoudige fluoropyrimidinen resulteerde in lagere werkzaamheid dan oxaliplatine-gebaseerde chemotherapie. | A translated clinical-trial abstract compares chemotherapy options for older or frail patients with metastatic colorectal cancer. |
| CRP is geen voorspeller van postoperatieve mortaliteit na CABG-operatie. | A translated abstract discusses prognostic biomarkers and cost-effectiveness for patients awaiting coronary bypass surgery. |
| Arginine 90 in p150 is belangrijk voor interactie met EB1. | A translated abstract describes the structural basis for microtubule assembly activation by the EB1 and p150Glued complex. |
| Obesitas wordt uitsluitend bepaald door omgevingsfactoren. | A translated study about adult adoptees and biological siblings discusses genetic effects on obesity. |
| Koortsstuipen verhogen de drempel voor het ontwikkelen van epilepsie. | A translated abstract describes lasting changes in neuronal excitability after febrile seizures in the developing brain. |
