# NanoMTEB-Dutch / cqadupstack_stats

## Overview

`cqadupstack_stats` is the Dutch-translated Cross Validated, or statistics,
subforum split of CQADupStack. Queries are statistics and probability questions,
and relevant documents are older questions marked as duplicates. The Nano split
contains 200 queries, 10,000 documents, and 200 positive qrel rows, with one
positive duplicate per query. It evaluates retrieval over variance, sampling,
linear models, PCA, probability, hypothesis testing, R code, formulas, and
statistical interpretation.

The task sits between technical lexical retrieval and conceptual STEM
retrieval. BM25 can use terms such as variance, PCA, Bernoulli, p-value, and R
function names, but duplicates often use different examples or notation to ask
about the same statistical idea. Dense retrieval improves on BM25, and
`reranking_hybrid` is strongest across the reported metrics. This makes the
split useful for evaluating hybrid retrieval over translated, formula-aware
statistics questions.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
uses Stack Exchange duplicate links to construct retrieval tasks for community
question answering. In the Cross Validated split, a query is a later statistics
question and the system must retrieve an older duplicate. The domain is
conceptually focused but still difficult because the same statistical issue can
be illustrated through different examples, formulas, or software outputs.

BEIR includes CQADupStack as a zero-shot retrieval dataset, and BEIR-NL
translates the public BEIR data into Dutch. This Nano task therefore uses
Dutch-translated statistical questions while preserving many formulas, symbols,
and code fragments. Retrieval models must combine Dutch semantic matching with
notation-aware reasoning.

### Observed Data Profile

The split has 200 queries and 10,000 documents. Queries average 64.27
characters, while documents average 1,097.65 characters. Documents may contain
R code, formulas, mathematical notation, textbook-style explanations, and
worked examples. The positive duplicate can be a different example of the same
statistical concept rather than a near-copy of the query.

Representative questions ask about variance estimates from an iid sample,
graphing type-II error and power, representing a distance matrix in a plane,
interpreting an R linear model, and handling missing values for PCA. These
examples show why exact lexical overlap is not enough: the same concept can
appear under different statistical language and applied examples.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2827, hit@10 = 0.3850, and recall@100 = 0.5700 over
top-500 candidate lists. Sparse retrieval benefits from technical terms,
symbols, and code tokens. A query containing PCA, variance, `summary(lm(...))`,
or `prcomp()` has useful exact-match anchors, and many positive documents share
domain terminology.

The limitation is conceptual paraphrase. A duplicate may discuss dividing by
`n - 1` without using the same title wording about variance estimates, or it
may explain a distance-matrix method through PCA and multidimensional scaling.
BM25 also struggles when different examples instantiate the same statistical
principle. It retrieves same-topic candidates, but not always the true
duplicate.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.3224, hit@10 =
0.4300, and recall@100 = 0.6550. It improves over BM25 across the reported
metrics, which indicates that embedding similarity captures some conceptual
equivalence among statistical questions. Dense retrieval is especially useful
when the query and positive document use different examples for the same
underlying idea.

The score remains moderate because statistics questions create hard negatives.
Many candidates can share terms such as variance, regression, PCA, likelihood,
or probability while asking a different question. Dense models need to
distinguish the requested statistical interpretation or method, not just the
general topic.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3337, hit@10 =
0.4450, and recall@100 = 0.6800, with 100 to 101 candidates per query and 64
rank-101 safeguard rows. It is the strongest candidate profile for this task.
The hybrid signal appears to combine exact statistical notation and code terms
from BM25 with semantic concept matching from dense retrieval.

This pattern is encouraging for reranking. The hybrid pool has better top-100
coverage and slightly better top-10 ranking than either individual candidate
source. A reranker can then focus on deciding whether two questions ask the
same statistical concept or merely share notation and software context.

### Metric Interpretation for Model Researchers

With a single positive per query, nDCG@10 measures how high the duplicate
question is ranked. Hit@10 measures whether the duplicate appears in the short
result list, while recall@100 measures candidate-pool suitability for a
reranker. The progression from BM25 to dense to hybrid shows that both sparse
and dense signals contribute useful evidence.

The task is a good diagnostic for formula-aware retrieval. A model that ignores
symbols and R code loses important anchors, but a model that relies too heavily
on them can confuse notation-near negatives. Strong performance requires
matching the statistical problem itself.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated statistics questions. They often contain a
concept name, formula, model type, R function, or applied statistical task.
Relevant documents are older questions marked as duplicates, usually longer and
more detailed than the query.

Relevance is based on duplicate statistical intent. Two posts about PCA are not
duplicates unless they ask the same methodological question. Two posts with
different examples may be duplicates if they ask about the same estimator,
model interpretation, or probability concept.

### Representative Failure Modes

BM25 can fail when the same concept is expressed with different examples or
terminology. It can also over-rank documents that share R functions or formulas
but ask a different statistical question. Dense retrieval can fail when
semantic similarity groups together related concepts such as PCA and MDS,
variance and standard deviation, or power and type-II error without preserving
the exact question.

Hybrid failures tend to involve notation-near or method-near hard negatives. A
candidate may look plausible because it shares code or symbols, but the
duplicate relation depends on the same statistical interpretation.

### Training Data That May Help

Useful training data includes non-overlapping Cross Validated duplicate pairs,
Dutch-translated statistics QA pairs, formula-aware STEM duplicate retrieval
data, and multilingual statistical paraphrase data with overlap removed.
Training should exclude the translated Statistics test queries and duplicate
positives used by this Nano split.

Synthetic data can be generated from statistics forum questions outside the
evaluation set. Preserve formulas and R code, but create Dutch paraphrases that
use different examples for the same concept. Hard negatives should share
notation, variables, or model names while asking a different statistical
question.

### Model Improvement Notes

Improving this task requires concept-level statistical retrieval. Dense models
should learn from duplicate pairs where the same principle is expressed through
different examples. Rerankers should compare the statistical operation, target
quantity, and interpretation requested by the query and candidate.

Hybrid systems are a strong fit. BM25 protects exact formulas and software
tokens, dense retrieval supplies paraphrase matching, and reranking can decide
whether the shared notation actually implies duplicate intent.

## Example Data

| Query | Positive document |
| --- | --- |
| Schattingen van variantie uit een iid steekproef [48 chars] | Intuïtieve uitleg voor delen door (n-1) bij het berekenen van de standaarddeviatie? Vandaag kreeg ik in de klas de vraag waarom je de som van de gekwadrateerde afwijkingen deelt door $(n-1)$ in plaats van door $n$ bij het berekenen van de standaarddeviatie. Ik zei dat ik dat in de klas niet zou beantwoorden (omdat ik niet over zuivere schatters wilde beginnen), maar later vroeg ik me af - **is er** een intuïtieve uitleg hiervoor?! [435 chars] |
| Hoe kan ik type II (bèta) fout, power en steekproefomvang het beste grafisch weergeven? [87 chars] | Reëel gebaseerd op machtsfunctie Probleem: Wat is een voorbeeld uit het echte leven van een machtsfunctie? Ik heb erover nagedacht, maar ik ben er niet uitgekomen. Weet iemand het? [181 chars] |
| Het weergeven van een afstandsmatrix in het vlak [48 chars] | Wat is het verschil tussen principale componentenanalyse en multidimensionale schaalverdeling? Hoe verschillen PCA en klassieke MDS? En MDS versus niet-metrische MDS? Is er een situatie waarin je de voorkeur aan de een boven de ander zou geven? Hoe verschillen de interpretaties? [280 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | [https://doi.org/10.1145/2838931.2838934](https://doi.org/10.1145/2838931.2838934) |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | [https://aclanthology.org/2025.bucc-1.5/](https://aclanthology.org/2025.bucc-1.5/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| clips/beir-nl-cqadupstack |  | dataset card | [https://huggingface.co/datasets/clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Schattingen van variantie uit een iid steekproef | A translated duplicate asks for an intuitive explanation of dividing by `n - 1` when calculating standard deviation. |
| Hoe kan ik type II fout, power en steekproefomvang grafisch weergeven? | A translated post asks for a real-world example of a power function and how it can be understood. |
| Het weergeven van een afstandsmatrix in het vlak | A translated duplicate compares PCA, classical MDS, and non-metric MDS for representing distances. |
| Hulp bij het interpreteren van een R lineair model | A translated question asks how to interpret `summary(lm(...))` output in R, including intercept p-values. |
| Hoe om te gaan met ontbrekende waarden voor PCA? | A translated post asks about replacing missing values before PCA analysis in R with `prcomp()`. |
