# NanoBuiltBench / NanoBuiltBench

## Overview

NanoBuiltBench is an English built-asset information retrieval task. Queries are compact IFC-derived descriptions of building, infrastructure, equipment, and facility-management entities, while documents are Uniclass product descriptions. The task measures whether retrieval systems can align terminology across built-environment classification systems, such as mapping an IFC entity definition to relevant Uniclass product classes.

## Details

### What the Original Data Measures

BuiltBench was introduced to evaluate text embedding models for aligning built asset information across taxonomies and classification systems. The underlying benchmark uses authoritative built-environment vocabularies, including IFC product descriptions and Uniclass product records, and tests whether models can map a source entity to corresponding target classes.

This is a terminology and taxonomy alignment problem, not general web search. The query may be a short definition such as a water boiler or a covering moulding, while the relevant document may be a Uniclass product description with hierarchy, function, and product-family context. Relevance depends on functional and classification equivalence.

### Observed Data Profile

The task contains 200 queries, 2,761 documents, and 1,480 relevance judgments. It is strongly multi-positive: there are 7.40 positives per query on average, a minimum of 1, a median of 3.0, a maximum of 93, and 133 multi-positive queries, or 66.50% of the set.

Queries average 102.12 characters, and documents average 341.69 characters. Queries are short technical definitions, while documents are richer product-class descriptions. Broad IFC concepts can map to many Uniclass products, producing the long positive tail.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5235, hit@10 of 0.7400, and recall@100 of 0.6642 using the top-500 BM25 candidate subset. This is a strong lexical baseline because many built-asset terms overlap directly across IFC and Uniclass descriptions: boiler, cooling coil, moulding, bollard, refrigerator, or fastener-like terms.

The remaining difficulty comes from near-neighbor product classes. BM25 can confuse products with the same material, system, or construction context but different function. A strong model must distinguish classification intent, not merely shared product vocabulary.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6209, hit@10 of 0.8400, and recall@100 of 0.7649. Dense retrieval is the strongest profile for the top ranking and slightly best for recall@100. It improves over BM25 by capturing functional similarity and hierarchy-aware descriptions beyond exact terms.

This result indicates that embedding similarity is well suited to IFC-to-Uniclass alignment when the document descriptions contain enough functional context. Dense retrieval can connect concise entity definitions to product classes that use different wording but share the same built-asset role.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5751, hit@10 of 0.8000, and recall@100 of 0.7642. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 9 safeguard rows, candidate counts from 100 to 101, and a mean of 100.05 candidates.

Hybrid retrieval improves over BM25 and nearly matches dense recall@100, but dense remains better for nDCG@10 and hit@10. The practical reading is that sparse signals are useful for exact product names, while dense retrieval gives better ordering among taxonomy neighbors.

### Metric Interpretation for Model Researchers

This task is a dense-favorable domain alignment benchmark with a strong BM25 baseline. BM25 performs well when terms transfer directly across classification systems, but dense retrieval is better at function-level mapping. Reranking_hybrid is a useful robust candidate pool, though it does not surpass dense in the reported top-rank metrics.

Researchers should look beyond hit@10. Because many queries have multiple positives, nDCG@10 measures whether the ranking surfaces several good mappings early, and recall@100 reflects whether downstream expert review or reranking can see enough valid alternatives.

### Query and Relevance Type Tendencies

Queries describe built assets such as mooring posts, mouldings, cooling coils, boilers, electrical appliances, fasteners, vents, and facility-management products. Positive documents are Uniclass descriptions that include product names, parent classes, broader category labels, and short functional definitions.

The relevance relation is cross-classification equivalence. A document is relevant when its Uniclass product class corresponds to the IFC-derived entity or definition. Product hierarchy and function are often more important than exact wording.

### Representative Failure Modes

Likely failures include retrieving a nearby product with the same material but different function, confusing parent and child product classes, over-ranking generic service-system descriptions, and missing broad classes with many valid product mappings.

BM25 is vulnerable to shared terms among neighboring classes. Dense retrieval can over-generalize within a product family. Hybrid retrieval improves robustness, but final ranking should respect hierarchy and intended asset function.

### Training Data That May Help

Useful training data includes non-overlapping IFC-to-Uniclass mappings, buildingSMART Data Dictionary definitions, Uniclass product descriptions, BIM object catalogs, construction specification classification pairs, and hard negatives from neighboring product categories.

Synthetic data should generate non-evaluation built asset product-class descriptions with hierarchy and function details, then create concise IFC-like definitions grounded in those descriptions. Hard negatives should share material, service system, or product family but differ in class or function.

### Model Improvement Notes

Strong systems should combine domain terminology, product hierarchy, and functional semantics. Dense retrieval is the best observed first-stage method, but sparse features remain valuable for exact product names and standard classification terms. Multi-positive training is important because broad IFC classes may map to many products.

The task is a useful benchmark for BIM, construction, and asset-information search systems where expert review depends on ranking plausible taxonomy matches, not answering natural-language questions.

## Example Data

| Query | Positive document |
| --- | --- |
| a short, thick post on the deck of a ship or a quay side, to which ship's rope may be secured. not t... [100 / 136 chars] | Capstan Capstan: This product is associated with equipment used for mooring, docking, and flotation, categorized under 'equipment' in the broader context of signage, sanitary fittings, and furnishings... [200 / 315 chars] |
| The covering is used to represent a molding being a strip of material to cover the transition of sur... [100 / 148 chars] | Fibrous plaster mouldings Fibrous plaster mouldings are trim products used for interior wall and ceiling detailing, categorized under coverings and finishes. These mouldings add both functional and ae... [200 / 232 chars] |
| Cooling coil using a refrigerant to cool the air stream directly. [65 chars] | Refrigerant cooling coils Refrigerant cooling coils are components associated with heating and cooling coils, classified under air and fume source products, which are part of the larger group of servi... [200 / 314 chars] |
| Water boiler. [13 chars] | Biomass boilers Biomass boilers are a type of boiler system classified under heating and cooling source products, which are part of the larger group of services and process source products. These boil... [200 / 255 chars] |
| An electrical appliance that has the primary function of storing food at low temperature but above t... [100 / 127 chars] | Drink chillers Drink chillers are a type of equipment categorized under commercial display and service catering products, which are part of the broader classification of signage, sanitary fittings, an... [200 / 320 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| arXiv paper | [Benchmarking pre-trained text embedding models in aligning built asset information](https://arxiv.org/abs/2411.12056) |
| Journal article | [Scientific Reports version](https://www.nature.com/articles/s41598-025-09052-5) |
| Source repository | [BuiltBench GitHub](https://github.com/mehrzadshm/built-bench-paper) |
| Source dataset | [MTEB BuiltBenchRetrieval](https://huggingface.co/datasets/mteb/BuiltBenchRetrieval) |
| NanoBuiltBench dataset | [hakari-bench/NanoBuiltBench](https://huggingface.co/datasets/hakari-bench/NanoBuiltBench) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| A short, thick post on a ship deck or quay side for securing rope. | A Uniclass product description for capstans associates the class with mooring and docking equipment. |
| A strip used to cover transitions between wall cladding and ceiling. | A fibrous plaster mouldings description identifies interior wall and ceiling trim products. |
| A cooling coil using refrigerant to cool air directly. | A refrigerant cooling coils description places the product under heating and cooling source products. |
| Water boiler. | A boiler product description maps the query to heating and cooling source products. |
| An appliance for storing food at low temperature above freezing. | A chiller product description connects refrigeration function to commercial display or catering equipment. |
