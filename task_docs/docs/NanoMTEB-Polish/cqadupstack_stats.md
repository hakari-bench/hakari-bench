# NanoMTEB-Polish / cqadupstack_stats

## Overview

`cqadupstack_stats` is the Polish NanoMTEB version of the Statistics subset from CQADupStack. The source data comes from duplicate-question links in statistics-oriented community QA, so the task is to retrieve documents that ask the same statistical modeling, inference, or interpretation question as a short Polish query. The observed examples cover variance estimation, type II error and power, distance matrices, PCA, missing values, linear-model output, logistic regression, ANOVA interactions, correlated random variables, learning-to-rank, and Gaussian densities.

The Nano split contains 200 queries, 10,000 documents, and 373 positive relevance judgments. Queries average about 61 characters, while documents average about 1,017 characters. The average number of positives per query is 1.865, and 58 queries have more than one positive. Most information needs are therefore relatively narrow, but a nontrivial portion of the task contains duplicate clusters around common statistical questions.

## Details

### What the Original Data Measures

CQADupStack evaluates duplicate-question retrieval in community question answering. In the Statistics subset, relevance means that two posts ask the same statistical question, not simply that they mention the same method or distribution. A query about PCA with missing values should retrieve posts about that same analysis issue, not every PCA-related document. A question about variance estimates from an iid sample should retrieve explanations of the same denominator or estimator issue, not every question containing variance.

This makes the task useful for studying retrieval over technical natural language. Statistical terminology gives strong lexical clues, but true relevance depends on the inferential problem, model assumption, data condition, or interpretation question.

### Observed Data Profile

The documents are long and often include examples, formulas, software output, variable descriptions, or partial data-analysis scenarios. The Polish translation wraps statistical terms and notation in Polish prose, while method names such as PCA, ANOVA, R, logistic regression, and Gaussian often remain recognizable. Models must combine lexical anchors with the meaning of the statistical setup.

The relevance distribution is less clustered than TeX or Programmers, but not purely single-positive. The median positives per query is 1, while the maximum is 18. This means many queries reward precise ranking of a single duplicate, while others require broader recovery of repeated statistical questions.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2662, hit@10 of 0.3800, and recall@100 of 0.4370. It benefits from exact method names and statistical vocabulary. Queries containing PCA, ANOVA, Gaussian, variance, or linear model terms often have enough lexical signal to find related documents.

The limitation is that method-name overlap is not the same as duplicate relevance. Many posts can mention PCA while asking about dimensionality, visualization, missing values, or interpretation. Similarly, linear-model output can be discussed for coefficients, residuals, diagnostics, or hypothesis tests. BM25 tends to retrieve same-topic documents but cannot reliably identify the same inferential issue.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run improves to nDCG@10 of 0.3375, hit@10 of 0.4850, and recall@100 of 0.5255. Dense retrieval is better at connecting different formulations of the same statistical question. It can use the semantic structure of the problem, such as "why divide by n-1", "how to handle missing values before PCA", or "how to interpret R `lm()` output", even when the exact phrasing differs.

This profile shows that the task is strongly semantic. Dense retrieval is the best direct top-10 ranking among the three methods, although its recall is narrowly below `reranking_hybrid`. The gain over BM25 is substantial enough to indicate that statistical duplicate retrieval cannot be solved by keyword overlap alone.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.3314, hit@10 of 0.4650, and recall@100 of 0.5308. Candidate lists contain 100 to 101 items, and 55 rows use the positive safeguard. The hybrid profile has the best recall@100 but slightly lower top-10 metrics than dense retrieval.

For reranking pipelines, this is a useful distinction. The hybrid candidate pool preserves a slightly larger fraction of positives by combining exact statistical terms with dense semantic matches. But for direct first-stage ranking, dense retrieval orders the top results slightly better. A strong reranker should be able to exploit the hybrid pool while improving the top-10 order.

### Metric Interpretation for Model Researchers

This split is dense-favorable for top-ranked search and hybrid-favorable for candidate recall. BM25 is useful for identifying broad statistical topics, but it is not enough for duplicate-question retrieval. Dense retrieval's higher nDCG@10 and hit@10 indicate that embedding similarity captures inferential intent better than term frequency.

The narrow hybrid recall advantage matters when the retrieval stage feeds a reranker. Researchers should evaluate both use cases separately: direct retrieval quality is best represented by nDCG@10, while candidate-generation quality is better represented by recall@100.

### Query and Relevance Type Tendencies

Representative queries include variance estimates from iid samples, graphical display of type II error and power, representing a distance matrix in a plane, interpreting R linear-model output, and handling missing values for PCA. These examples show that the task frequently centers on statistical reasoning rather than named entities.

Relevant documents may include different notation, different software examples, or different datasets. A model should identify the same statistical assumption or inferential question beneath the surface form. It should also avoid confusing related methods with the exact duplicate relation.

### Representative Failure Modes

BM25 may over-rank documents that share method names but ask different questions. A PCA query can retrieve documents about PCA visualization rather than missing-value handling. A linear-model query can retrieve documents about regression in general rather than interpretation of a particular output. Dense retrieval can make the opposite error by retrieving conceptually adjacent statistics discussions that are educationally similar but not duplicates.

Another failure mode is losing the role of mathematical notation or software output. A short query may be matched to a long document where the relevant issue appears in a formula, an R function call, or an example table. Models that treat these as peripheral text can miss the duplicate.

### Training Data That May Help

Useful training data includes Cross Validated duplicate pairs, Polish statistics QA, translated textbook-style question pairs, and hard negatives that share a method name but differ in the inferential question. Data with formulas, software output, and short-to-long query-document pairs would be especially relevant.

Hard negatives should include near misses such as multiple PCA questions, multiple regression-output questions, or multiple power-analysis questions that require different answers. These examples help a model distinguish topical similarity from duplicate relevance.

### Model Improvement Notes

Dense models can improve by representing statistical assumptions, inferential goals, and software-context clues. Sparse systems can improve through normalization of Polish technical terminology and method abbreviations, but exact matching alone is not sufficient. Hybrid systems are useful for candidate generation, especially when followed by a reranker that can reason over the actual statistical question.

Researchers should track whether improvements come from better top-10 ordering or better recall@100. This split makes the distinction visible because dense is slightly better at the top while hybrid preserves slightly more positives.

## Example Data

### Public Sources

- CQADupStack original paper: https://ir.webis.de/anthology/2015.adcs_conference-2015.3/
- MTEB benchmark paper: https://arxiv.org/abs/2210.07316
- CLARIN-KNEXT Polish dataset card: https://huggingface.co/datasets/clarin-knext/cqadupstack-stats-pl
- Source task dataset card: https://huggingface.co/datasets/mteb/CQADupstack-Stats-PL

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original duplicate-question retrieval construction. |
| MTEB paper | Benchmark context for retrieval evaluation. |
| CLARIN-KNEXT dataset card | Polish translated Statistics subset. |
| MTEB task card | Task packaging and retrieval interface. |

### Representative Snippets

- A query asks about variance estimates from an iid sample; relevant posts explain the `n-1` denominator in sample standard deviation.
- A query asks how to display type II error, power, and sample size graphically; relevant documents discuss practical power-function examples.
- A query asks how to represent a distance matrix in a plane; relevant posts compare PCA and multidimensional scaling.
- A query asks for help interpreting R linear-model output; relevant documents walk through `lm()` summary fields.
- A query asks how to handle missing values for PCA; relevant posts discuss replacing `NA` values before using PCA functions.
