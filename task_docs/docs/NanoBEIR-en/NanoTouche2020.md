# NanoBEIR-en / NanoTouche2020

## Overview

NanoTouche2020 is the compact English NanoBEIR version of Touche 2020 argument retrieval for controversial questions. Queries are short debate-style questions, and the corpus contains long argumentative passages from online debate sources. The retrieval goal is to find passages that substantively address the controversial issue, often from either side of the debate. This makes the task useful for evaluating argument retrieval, stance-diverse topical coverage, and ranking over long noisy debate text.

## Details

### What the Original Data Measures

Touche 2020 evaluates argument retrieval for controversial and decision-oriented information needs. In the controversial-question setting, systems retrieve argumentative texts from debate-oriented sources. A relevant document is not a factual answer snippet; it is an argument that addresses the topic, supplies reasons, or engages with the issue.

The BEIR version treats Touche 2020 as argument retrieval, and the NanoBEIR version keeps the short-query, long-document structure. The original task uses graded relevance, while this Nano task exposes binary positive qrels. A strong retriever should rank multiple useful arguments, not only one passage that repeats the query words.

### Observed Data Profile

The task contains 49 queries, 5,745 documents, and 932 relevance judgments. Every query is multi-positive, with an average of 19.02 positives per query. The minimum is 6, the median is 19.0, the maximum is 32, and all 49 queries are multi-positive.

Queries average 43.43 characters, while documents average 2,142.57 characters. Queries are short controversial questions, and documents are long debate passages containing claims, evidence, rebuttals, informal wording, and sometimes several argument points. The task is therefore about ranking a diverse argument set for each topic.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6648, hit@10 of 1.0000, and recall@100 of 0.8176 using the top-500 BM25 candidate subset. This is a strong lexical profile. Controversial questions often contain topic terms such as abortion, homework, vaccines, minimum wage, or standardized tests, and relevant arguments repeat those terms.

The high hit@10 should not be overread. Since each query has many positives, finding one argument is relatively easy. The harder problem is ranking a broad set of relevant arguments near the top and not over-focusing on one stance or phrasing pattern.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5407, hit@10 of 1.0000, and recall@100 of 0.8079. Dense retrieval also finds at least one positive for every query, but it is weaker than BM25 in nDCG@10 and slightly weaker in recall@100.

This suggests that the task remains strongly lexical in this English slice. Long debate documents repeat topic vocabulary, and general embedding similarity can blur distinct argumentative aspects. Dense retrieval may retrieve passages that are broadly about the same issue but less directly useful under the topic narrative.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6184, hit@10 of 1.0000, and recall@100 of 0.8391. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile has the best recall@100, while BM25 has the best nDCG@10.

This makes hybrid retrieval a strong candidate pool for downstream reranking. BM25 contributes precise controversial-topic anchors, while dense retrieval broadens coverage to arguments phrased differently. A reranker can then focus on argument relevance, stance diversity, and quality.

### Metric Interpretation for Model Researchers

Because every query has many positives, hit@10 is too forgiving: all three methods reach 1.0000. nDCG@10 measures whether the top list is rich in relevant arguments, and recall@100 measures whether a reranker can access enough of the positive argument set.

The comparison shows that BM25 is strongest for direct top ranking, dense retrieval is weaker on these long debate passages, and reranking_hybrid gives the best candidate coverage. This task is useful for testing argument retrieval beyond simple first-hit success.

### Query and Relevance Type Tendencies

Queries include questions such as whether homework is beneficial, whether prescription drugs should be advertised directly to consumers, whether vaccines should be required for children, whether abortion should be legal, and whether standardized tests improve education. Relevant documents are long passages making pro or con arguments.

The task rewards topical argument relevance and diversity. A relevant passage should address the controversial issue with a substantive argumentative move. It need not share the query's stance, and in many cases useful retrieval should expose both sides.

### Representative Failure Modes

Likely failures include retrieving passages that mention the topic but do not make a useful argument, over-ranking one stance while missing other relevant arguments, matching repeated terms without considering the topic narrative, and missing informal or noisy debate passages. BM25 may be too topic-term driven, while dense retrieval may be too broad.

### Training Data That May Help

Useful training data includes non-overlapping debate-portal argument relevance judgments, args.me-style query-to-argument supervision, pro/con topic retrieval data, stance-labeled arguments, and multi-positive argument retrieval sets. Hard negatives should discuss the same issue but fail the specific topic or argument relevance criterion.

### Model Improvement Notes

A model targeting this task should optimize for multi-positive argument ranking rather than single-answer retrieval. Sparse systems need long-document handling and phrase normalization. Dense systems need argument-specific training that distinguishes substantive arguments from broad topical similarity. Hybrid systems are promising reranking inputs because they provide the broadest candidate coverage.

## Example Data

### Public Sources

The original task is based on Touche 2020, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact English dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original task paper | [Overview of Touche 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Open PDF | [Overview of Touche 2020 PDF](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf) |
| Dataset record | [Touche20 Argument Retrieval](https://doi.org/10.5281/zenodo.6862281) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Source dataset card | [mteb/touche2020](https://huggingface.co/datasets/mteb/touche2020) |

Representative query and positive argument snippets:

| Query | Positive document snippet |
| --- | --- |
| Is homework beneficial? | Homework aids doer-learners and should continue in modern schools. |
| Should prescription drugs be advertised directly to consumers? | Many ads do not include enough information on how well drugs work. |
| Should any vaccines be required for children? | Governments should not have the right to intervene in health decisions parents make for their children. |
| Should abortion be legal? | Abortions should be legal because personhood begins after viability or birth. |
| Do standardized tests improve education? | Standardized tests can provide insight into student preparedness beyond high school GPA. |
