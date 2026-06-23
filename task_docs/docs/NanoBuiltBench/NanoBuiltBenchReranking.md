# NanoBuiltBench / NanoBuiltBenchReranking

## Overview

NanoBuiltBenchReranking is an English built-asset reranking task. Queries are IFC-style entity names and definitions, and documents are candidate Uniclass product descriptions. The task focuses on ordering a candidate set that contains multiple relevant product classes and close hard negatives. It measures whether a model can prioritize the most relevant built asset classes for expert review or downstream taxonomy alignment.

## Details

### What the Original Data Measures

BuiltBench includes reranking settings for built asset information alignment. The benchmark addresses the practical problem of reducing domain-expert verification effort: given a source IFC-like entity and a candidate set of Uniclass descriptions, the model should rank the best cross-classification matches first.

This differs from broad retrieval because the candidate set is already narrow and often contains close alternatives. The model must distinguish products that share material, service system, installation context, or parent hierarchy but differ in function or classification.

### Observed Data Profile

The task contains 82 queries, 2,898 documents, and 574 relevance judgments. Every query has exactly 7 positives, so the task is uniformly multi-positive: the average, minimum, median, and maximum positives per query are all 7.0, and 100.00% of queries are multi-positive.

Queries average 138.28 characters and often include an IFC entity label plus a parent type, such as a mechanical fastener or electric appliance. Documents average 309.04 characters and describe Uniclass product classes with hierarchy and function.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2681, hit@10 of 0.8171, and recall@100 of 0.8397 using the top-500 BM25 candidate subset. The high hit@10 shows that exact product and material terms often bring at least one positive near the top.

The lower nDCG@10 indicates weak ordering among multiple positives and close negatives. BM25 may find a nail-like product for a nail query but still rank nearby fasteners incorrectly, or it may match pipe, grille, cooker, or joint terms without fully respecting the intended product class.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.3650, hit@10 of 0.9024, and recall@100 of 0.8937. Dense retrieval is the strongest top-ranking profile in this task, improving clearly over BM25 for both nDCG@10 and hit@10.

This suggests that embedding similarity captures function and taxonomy context better than term frequency alone. Dense retrieval is better at distinguishing nearby construction product classes when the descriptions include functional context.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3277, hit@10 of 0.8659, and recall@100 of 0.8955. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.01 candidates.

Hybrid retrieval has the best recall@100 by a very small margin, while dense retrieval has better top-rank ordering. This means the hybrid pool is useful for coverage, but dense is the stronger ranker for prioritizing candidates in the first page.

### Metric Interpretation for Model Researchers

This reranking task is precision-oriented. Hit@10 is high for all methods because every query has seven positives and product terminology is informative. nDCG@10 is more important because it measures whether the ranking places multiple relevant classes above hard negatives.

The observed pattern favors dense retrieval for ordering, with reranking_hybrid nearly tied for candidate coverage. BM25 is a useful baseline but insufficient for ranking close taxonomy neighbors.

### Query and Relevance Type Tendencies

Queries describe IFC-style product entities such as nails, electric cookers, expansion joint devices, kitchen machines, and grilles. Positive documents are Uniclass descriptions of specific product classes such as corrugated fasteners, commercial electric grills, expansion joints, food mixers, or gas venting grilles.

The relevance relation is candidate-set crosswalk ranking. A document is relevant when it belongs to the mapped product class family for the source entity. Multiple positives are expected and should be surfaced early.

### Representative Failure Modes

Likely failures include ranking a product with the same material but wrong function, confusing broader and narrower product hierarchy levels, over-weighting shared service-system terms, and failing to group all seven positives ahead of close negatives.

BM25 is vulnerable to exact-term distractors. Dense retrieval can over-generalize within a product family. Hybrid retrieval gives slightly broader recall but still needs listwise or multi-positive ranking objectives to improve nDCG.

### Training Data That May Help

Useful training data includes non-overlapping IFC-to-Uniclass reranking sets, BIM product catalog matching pairs, construction taxonomy crosswalks, and hard negatives from neighboring product classes.

Synthetic data should create candidate product-class descriptions with hierarchy, material, function, and system context, then generate concise IFC-style labels and definitions. Candidate sets should include several positives and hard negatives sharing material or service context but differing in function.

### Model Improvement Notes

Strong systems should optimize for multi-positive ranking, not single-positive classification. Dense retrieval is the best observed ordering method, while reranking_hybrid is slightly better for recall@100. A domain reranker should use product hierarchy, parent type, function, material, and intended use.

This task is useful for evaluating whether a model can reduce expert review effort by ranking plausible taxonomy mappings in the right order.

## Example Data

| Query | Positive document |
| --- | --- |
| Nail (Mechanical Fastener type). A thin pointed piece of metal that is hammered into materials as a... [100 / 109 chars] | Corrugated fasteners are a type of nail-like product that belong to the fastener category, which is part of the larger group of structural and general products. These fasteners are specifically design... [200 / 270 chars] |
| Electric Cooker (Electric Appliance Type). An electrical appliance that has the primary function of... [100 / 142 chars] | Commercial electric grills are a type of commercial cooking device categorized as equipment. They are part of the wider array of products that include signage, sanitary fittings, and other furnishings... [200 / 287 chars] |
| Expansion Joint Device (Discrete Accessory Type). Assembly connection element between construction e... [100 / 153 chars] | Chloroprene and copper expansion joints are components that belong to the trim products category, specifically within the wider group of covering and finishing products. These expansion joints are des... [200 / 366 chars] |
| Kitchen Machine (Electric Appliance Type). A specialized appliance used in commercial kitchens such... [100 / 111 chars] | Commercial food mixers are categorized as preparation catering equipment, falling within the equipment segment of the broader signage, sanitary fittings, and furnishings and equipment (FF&E) product c... [200 / 336 chars] |
| Grille (Air Terminal type). A covering for any area through which air passes. [77 chars] | Gas venting grilles are components associated with wall venting solutions, categorized under openings and components of openings within the wider classification of products designed for openings. Thes... [200 / 262 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| arXiv paper | [Benchmarking pre-trained text embedding models in aligning built asset information](https://arxiv.org/abs/2411.12056) |
| Journal article | [Scientific Reports version](https://www.nature.com/articles/s41598-025-09052-5) |
| Source repository | [BuiltBench GitHub](https://github.com/mehrzadshm/built-bench-paper) |
| Source dataset | [MTEB BuiltBenchReranking](https://huggingface.co/datasets/mteb/BuiltBenchReranking) |
| NanoBuiltBench dataset | [hakari-bench/NanoBuiltBench](https://huggingface.co/datasets/hakari-bench/NanoBuiltBench) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| Nail, a thin pointed metal piece used as a mechanical fastener. | A corrugated fasteners description identifies a nail-like fastener class. |
| Electric cooker, an appliance for cooking food. | A commercial electric grills description maps the appliance to cooking equipment. |
| Expansion joint device for thermic differential expansion. | An expansion-joint description covers movement accommodation between construction elements. |
| Kitchen machine, a commercial appliance such as a mixer. | A commercial food mixers description maps the entity to preparation catering equipment. |
| Grille, a covering for an area through which air passes. | A gas venting grilles description maps the entity to opening and venting products. |
