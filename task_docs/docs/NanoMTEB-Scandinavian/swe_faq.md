# NanoMTEB-Scandinavian / swe_faq

## Overview

`swe_faq` is the Swedish NanoMTEB-Scandinavian retrieval adaptation of SweFAQ, a dataset described in the SuperLim Swedish language understanding benchmark. SweFAQ contains frequently asked questions and answers from Swedish public-authority websites, including practical administrative domains such as social insurance, taxes, child support, parental benefits, disability support, and public services. In this retrieval task, a Swedish user question must retrieve the corresponding government-style answer.

The Nano split contains 200 queries, 511 documents, and exactly 200 positive relevance judgments. Each query has one positive answer. Queries average about 73 characters, while answer documents average about 320 characters. The observed questions involve `Försäkringskassan`, `underhållsbidrag`, `föräldrapenning`, `bilstöd`, work injury compensation, child benefits across EU/EES borders, and LSS. The task rewards matching a citizen's situation to the exact administrative answer.

## Details

### What the Original Data Measures

SuperLim describes SweFAQ as a Swedish FAQ dataset from public authorities. The retrieval adaptation uses the question as the query and the corresponding answer as the relevant document. This is practical QA retrieval: the answer should directly resolve the user's administrative question.

Relevance depends on more than benefit-category overlap. Two questions can both discuss child benefit or parental leave but differ in eligibility, country coordination, timing, payment, or exceptions. The model must identify the exact policy scenario being asked about.

### Observed Data Profile

The corpus is small, but the answer documents contain dense policy language. Queries are usually full user questions with personal conditions, such as working in Sweden while family lives in another EU/EES country, or asking whether another parent abroad can receive parental benefit. Answers often include legal conditions, exceptions, or procedural constraints.

Each query has a single positive, so precise top ranking matters. Many candidates may discuss the same authority or benefit, but only one answer directly fits the question.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5449, hit@10 of 0.7500, and recall@100 of 0.9050. Lexical matching is useful because Swedish administrative terms are specific. Words such as `Försäkringskassan`, `vårdbidrag`, `barnbidrag`, `föräldrapenning`, `LSS`, and `arbetsskada` often appear in both the question and answer.

The limitation is scenario matching. A question may use everyday wording while the answer uses formal policy language. Multiple answers can share the same benefit term but address different conditions. BM25 retrieves many positives within the top 100, but it is less reliable at placing the exact answer first.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest at top ranks, with nDCG@10 of 0.6488, hit@10 of 0.8100, and recall@100 of 0.9400. Dense retrieval improves because it can represent the user's situation and the answer's administrative condition as semantically related, even when wording differs.

This is important for public-sector FAQ retrieval. Users may phrase questions in practical terms, while authority answers use standardized legal or procedural language. Dense similarity better bridges that style gap than term overlap alone.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.6395, hit@10 of 0.8000, and recall@100 of 0.9650. Candidate lists contain 100 to 101 items, and 7 rows use the positive safeguard. Hybrid retrieval has the best recall@100, while dense retrieval has slightly better top-10 ranking.

This pattern suggests that lexical administrative terms and semantic scenario matching are complementary. Hybrid search is attractive for candidate generation because it keeps more correct answers available. Dense retrieval remains the stronger direct ranking profile by a small margin.

### Metric Interpretation for Model Researchers

This split is dense-favorable for direct answer ranking and hybrid-favorable for candidate recall. BM25 is moderately strong because authority terms are repeated, but it cannot fully resolve eligibility scenarios and policy exceptions. Dense retrieval's top-rank advantage shows the value of semantic question-answer matching.

Because each query has one positive, nDCG@10 directly reflects whether the correct answer is placed high. Recall@100 is useful for reranking pipelines, where hybrid search provides the broadest candidate coverage.

### Query and Relevance Type Tendencies

Representative queries ask whether the Social Insurance Agency can investigate a work injury for AFA insurance, why a care allowance decision must be followed up, whether a worker in Sweden can receive child benefit when the family lives in another EU/EES country, whether another parent abroad can receive parental benefit from Sweden, and what LSS means.

Relevant answers often begin with direct yes/no or definition-like language, followed by conditions. The model should match the user's concrete situation to the correct policy answer, not merely retrieve any answer about the same benefit.

### Representative Failure Modes

BM25 may over-rank answers sharing the same benefit term but addressing a different condition. Dense retrieval may retrieve a semantically related policy answer that is not the exact scenario. Hybrid retrieval can preserve more positives but still rank same-benefit distractors high.

Another failure mode is missing cross-border or exception conditions. Questions involving EU/EES, Switzerland, work status, or which parent is insured require precise interpretation of the administrative situation.

### Training Data That May Help

Useful training data includes non-overlapping Swedish FAQ question-answer pairs, public-sector help-center retrieval data, same-benefit hard negatives, and Swedish administrative QA paraphrases. Training should exclude SweFAQ or SuperLim test examples, Nano qrels, and answer documents from this split.

Hard negatives should be answers about the same authority and benefit but different eligibility, timing, or procedure. These are more useful than random negatives because they teach the model to identify exact policy fit.

### Model Improvement Notes

Dense models can improve by representing administrative scenarios, benefit names, and exception conditions in Swedish. Sparse systems can improve through domain vocabulary and compound handling, but exact matching alone will confuse same-benefit answers. Hybrid retrieval is useful for first-stage recall, especially when followed by a reranker trained on FAQ answer selection.

For deployment-like evaluation, this task is a practical test of public-service search. The best model should retrieve the answer that a citizen can actually use, not merely a related policy page.

## Example Data

### Public Sources

- Scandinavian Embedding Benchmarks paper: https://arxiv.org/abs/2406.02396
- SuperLim paper: https://aclanthology.org/2023.emnlp-main.506/
- Source task dataset card: https://huggingface.co/datasets/mteb/SweFaqRetrieval

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Scandinavian Embedding Benchmarks | Retrieval benchmark framing. |
| SuperLim paper | Original Swedish benchmark and SweFAQ context. |
| MTEB task card | Retrieval packaging of SweFAQ. |

### Representative Snippets

- A query asks whether `Försäkringskassan` can investigate a work injury for AFA insurance; the answer says no and explains the legal condition.
- A query asks why a care allowance decision must be followed up; the answer states that it is reviewed at least every two years unless conditions justify otherwise.
- A query asks whether a worker in Sweden can receive child benefit when the family lives in another EU/EES country; the answer explains coordination between member states.
- A query asks whether another parent abroad can receive parental benefit from Sweden; the answer says an insurance-status investigation is needed.
- A query asks what LSS is; the answer expands the acronym and defines the law's purpose.
