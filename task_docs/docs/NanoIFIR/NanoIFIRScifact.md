# NanoIFIR / NanoIFIRScifact

## Overview

`NanoIFIRScifact` is an English scientific literature retrieval task in NanoIFIR. The queries are scientific claims, and the documents are scientific article titles and abstracts.

This task evaluates evidence retrieval for scientific claim verification. The retriever must find abstracts that support, refute, or otherwise provide evidence for the claim under the instruction-following setting. It is lexically favorable compared with many other IFIR tasks because claims often include distinctive scientific terms that appear in relevant abstracts.

## Details

### What the Original Data Measures

IFIR uses SciFact-open for the scientific literature domain. It turns claim-evidence retrieval into instruction-following retrieval by adding requirements such as finding supporting evidence, refuting evidence, or research-objective-specific passages.

SciFact is a scientific claim verification benchmark. It asks systems to select abstracts from the research literature that support or refute a scientific claim and to identify rationales. In NanoIFIR, this becomes a retrieval-focused task over scientific abstracts.

### Observed Data Profile

This Nano split contains 43 queries, 10,000 documents, and 255 positive qrels. Every query is multi-positive. Queries have 5.93 positives on average, with a minimum of 3, a median of 5.0, and a maximum of 24. Queries average 73.63 characters, and documents average 1,452.61 characters.

Observed claims cover obesity genetics, teaching versus non-teaching hospital outcomes, risedronate fracture reduction, bariatric surgery and diabetes, BRCA mutation location and cancer risk, biomedical mechanisms, receptors, stem cells, and gene expression. Documents are article titles and abstracts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8682, hit@10 of 1.0000, and recall@100 of 0.9765 with a top-500 candidate pool. This is an extremely strong lexical profile.

Scientific claims often reuse technical terms, disease names, drug names, gene names, or intervention phrases found in evidence abstracts. BM25 can therefore retrieve relevant evidence reliably. Remaining ranking errors are likely cases where several abstracts share the same entities but differ in evidence relation or polarity.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.8516, hit@10 of 0.9767, and recall@100 of 0.9686. Dense retrieval is also very strong, but slightly below BM25.

This suggests that exact scientific terminology is particularly valuable in this split. Dense retrieval captures semantic relatedness, but may blur fine distinctions between evidence-bearing abstracts and related scientific background.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.9055, hit@10 of 1.0000, and recall@100 of 0.9922. It uses exactly 100 candidates per query and has no safeguard-positive rows.

Hybrid retrieval is the strongest profile. It preserves BM25's terminology precision while adding semantic evidence coverage, producing the best nDCG@10 and recall@100. This is a high-quality reranking pool with little candidate-miss pressure.

### Metric Interpretation for Model Researchers

`NanoIFIRScifact` is a high-scoring scientific evidence retrieval task. BM25 is already near ceiling for hit and recall, so improvements should be judged mainly through nDCG@10 and evidence-ordering quality.

Because every query has multiple positives, recall@100 remains meaningful. The hybrid profile shows that combining lexical and dense signals can improve the ordering of evidence abstracts even when lexical retrieval is already strong.

### Query and Relevance Type Tendencies

Queries are concise scientific claims. Documents are scientific abstracts with titles, background, methods, and findings. The topics are heavily biomedical but include general scientific and healthcare outcome claims.

The relevance relation is evidence-bearing relevance. A positive abstract should contain information useful for supporting, refuting, or evaluating the claim, not merely mention the same entity.

### Representative Failure Modes

BM25 may retrieve abstracts with the same technical terms but a different finding or evidence polarity. Dense retrieval may retrieve related literature that lacks the specific outcome or claim relation. Hybrid retrieval reduces both failure modes but still needs reranking to handle support versus refute distinctions.

Negation and comparative claims are especially sensitive. A passage can share all major entities while contradicting the claim or addressing a different endpoint.

### Training Data That May Help

Useful training data includes non-overlapping SciFact claim-evidence pairs, scientific abstract retrieval pairs, citation intent and evidence retrieval data, and same-entity scientific hard negatives.

Training should distinguish evidence retrieval from truth classification, preserve multiple evidence abstracts, and exclude `NanoIFIRScifact` claims, qrels, and positive evidence abstracts.

### Model Improvement Notes

Improving this task requires evidence-level scientific matching. Models should preserve named entities and interventions while representing finding direction, comparison, causality, and evidence polarity.

For reranking, the core question is whether the abstract provides usable evidence for the claim. A strong reranker should not treat topical similarity as sufficient when the claim relation differs.

## Example Data

| Query | Positive document |
| --- | --- |
| Obesity is determined in part by genetic factors. [49 chars] | Genetics of obesity in adult adoptees and their biological siblings. An adoption study of genetic effects on obesity in adulthood was carried out in which adoptees separated from their natural parents very early in life were compared with their biological full and half siblings reared by their natural parents. The adoptees represented four groups who by sampling from a larger population were categorised as either thin, medium weight, overweight, or obese. Weight and height were obtained for 115 full siblings of 57 adoptees and for 850 half siblings of 341 adoptees. In full siblings body mass index (kg/m2) significantly increased with weight of the adoptees. Body mass index of the half siblings showed a steady but weaker increase across the four weight groups of adoptees. There were no significant interactions with sex of the adoptees, sex of the siblings, or (for the half siblings) sex of the common parent. In contrast with the findings in half siblings and (previously) the natural par... [1,000 / 1,319 chars] |
| Teaching hospitals provide better care than non-teaching hospitals. [67 chars] | Patient Outcomes with Teaching Versus Nonteaching Healthcare: A Systematic Review Background Extensive debate exists in the healthcare community over whether outcomes of medical care at teaching hospitals and other healthcare units are better or worse than those at the respective nonteaching ones. Thus, our goal was to systematically evaluate the evidence pertaining to this question. Methods and Findings We reviewed all studies that compared teaching versus nonteaching healthcare structures for mortality or any other patient outcome, regardless of health condition. Studies were retrieved from PubMed, contact with experts, and literature cross-referencing. Data were extracted on setting, patients, data sources, author affiliations, definition of compared groups, types of diagnoses considered, adjusting covariates, and estimates of effect for mortality and for each other outcome. Overall, 132 eligible studies were identified, including 93 on mortality and 61 on other eligible outcomes (2... [1,000 / 2,347 chars] |
| Risedronate reduces risk of vertebral and non-vertebral fractures. [66 chars] | Effects of risedronate treatment on vertebral and nonvertebral fractures in women with postmenopausal osteoporosis: a randomized controlled trial. Vertebral Efficacy With Risedronate Therapy (VERT) Study Group. CONTEXT Risedronate, a potent bisphosphonate, has been shown to be effective in the treatment of Paget disease of bone and other metabolic bone diseases but, to our knowledge, it has not been evaluated in the treatment of established postmenopausal osteoporosis. OBJECTIVE To test the efficacy and safety of daily treatment with risedronate to reduce the risk of vertebral and other fractures in postmenopausal women with established osteoporosis. DESIGN, SETTING, AND PARTICIPANTS Randomized, double-blind, placebo-controlled trial of 2458 ambulatory postmenopausal women younger than 85 years with at least 1 vertebral fracture at baseline who were enrolled at 1 of 110 centers in North America conducted between December 1993 and January 1998. INTERVENTIONS Subjects were randomly assig... [1,000 / 2,739 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [SciFact: A Dataset and Benchmark for Scientific Claim Verification](https://aclanthology.org/2020.emnlp-main.609/) | Original scientific claim verification paper. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A claim that obesity is partly determined by genetic factors. | An abstract about genetics of obesity in adoptees and biological siblings. |
| A claim that teaching hospitals provide better care than non-teaching hospitals. | A systematic review comparing patient outcomes in teaching and non-teaching healthcare. |
| A claim that risedronate reduces vertebral and non-vertebral fracture risk. | A randomized controlled trial abstract about risedronate treatment in postmenopausal osteoporosis. |
| A claim about bariatric surgery and diabetes resolution. | A cohort-study abstract about bariatric surgery outcomes and weight-loss effects. |
| A claim about BRCA mutation location and breast or ovarian cancer risk. | An abstract analyzing the association between BRCA1/BRCA2 mutation type or location and cancer risk. |
