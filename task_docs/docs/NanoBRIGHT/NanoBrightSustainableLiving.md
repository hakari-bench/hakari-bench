# NanoBRIGHT / NanoBrightSustainableLiving

## Overview

NanoBrightSustainableLiving is the Sustainable Living StackExchange slice of NanoBRIGHT. Queries are practical questions about environmental impact, energy use, waste, recycling, materials, food, household upgrades, and everyday sustainability decisions. Relevant documents are cited passages that provide evidence for an environmental comparison or decision. The task is useful for evaluating retrieval systems on practical, evidence-backed sustainability reasoning rather than simple topic lookup.

## Details

### What the Original Data Measures

BRIGHT's StackExchange tasks use real questions and cited or validated sources as positives. In Sustainable Living, a query may ask whether a household product can be reused, which upgrade reduces carbon most cost-effectively, how a solar water system should circulate, or what regulations apply to recycling and deposits.

The task measures whether a retriever can find evidence that supports a practical environmental judgment. Relevance is often comparative: a useful passage may provide lifecycle data, regulatory scope, energy modeling, product chemistry, or environmental risk evidence.

### Observed Data Profile

The task contains 108 queries, 10,000 documents, and 575 relevance judgments. It is moderately multi-positive: there are 5.32 positives per query on average, a minimum of 1, a median of 3.0, a maximum of 55, and 76 multi-positive queries, or 70.37% of the set.

Queries average 682.84 characters, and documents average 733.62 characters. Queries often include a concrete situation and ask for guidance, while documents are short passages from reports, articles, environmental references, practical guides, or official policy pages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4189, hit@10 of 0.7130, and recall@100 of 0.5948 using the top-500 BM25 candidate subset. Lexical retrieval is fairly strong because many questions contain distinctive terms such as bacon grease, carbon reduction, solar hot water, neonicotinoid, deposit label, lifecycle assessment, or building energy.

The limitation is that sustainability questions often require evidence for a decision rather than a same-topic passage. BM25 can retrieve pages that mention recycling, carbon, energy, or water, but the useful passage must address the specific comparison, regulation, or impact pathway.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5338, hit@10 of 0.7963, and recall@100 of 0.7774. Dense retrieval is the strongest profile for nDCG@10 and recall@100, and it ties reranking_hybrid for hit@10.

This suggests that embedding similarity captures the practical intent of sustainability questions better than term frequency alone. Dense retrieval can link a household scenario to evidence about lifecycle impact, product reuse, energy efficiency, or environmental regulation even when the source uses different wording.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5198, hit@10 of 0.7963, and recall@100 of 0.7617. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 7 safeguard rows, candidate counts from 100 to 101, and a mean of 100.06 candidates.

Hybrid retrieval is very close to dense retrieval and ties hit@10, but dense remains slightly better for nDCG@10 and recall@100. This indicates that sparse anchors help for named products and regulations, while semantic matching drives most of the ranking quality.

### Metric Interpretation for Model Researchers

This task is dense-favorable but not sparse-free. BM25 already performs well because many environmental questions contain distinctive named objects and policy terms. Dense retrieval improves by matching the practical question to the kind of evidence needed for the decision. Reranking_hybrid is competitive and useful for robust candidate generation, but it does not surpass dense in this passage-level slice.

Researchers should evaluate whether retrieved passages support the environmental decision, not just the broad sustainability topic. The difference between a plausible green-living article and an evidence-bearing passage is often the key relevance boundary.

### Query and Relevance Type Tendencies

Queries ask about uses for bacon grease, cost-effective carbon reductions from home upgrades, solar water circulation, recognizing neonicotinoid products, mineral water deposit labels, recycling rules, product impacts, and energy efficiency. Positive passages may be practical guides, official program pages, environmental reports, or reference explanations.

The relevance relation is usually evidence support for a practical choice. A passage may be relevant because it provides a regulatory category, lifecycle comparison, technical constraint, or environmental mechanism.

### Representative Failure Modes

Likely failures include retrieving same-topic sustainability advice that lacks evidence, confusing broad carbon-reduction recommendations with the specific upgrade question, missing official regulatory pages, and over-ranking pages that mention the product but not the environmental decision.

BM25 is vulnerable to topical overlap. Dense retrieval can over-match broad environmental intent without enough detail. Hybrid retrieval helps when named materials, policies, or products are decisive.

### Training Data That May Help

Useful training data includes non-overlapping Sustainable Living StackExchange posts with cited sources, environmental QA with references, lifecycle-assessment document retrieval, and hard negatives on the same product or resource but a different impact pathway.

Synthetic data should generate sustainability questions comparing materials, energy use, carbon intensity, waste treatment, or lifecycle impacts. Positives should contain evidence for the specific comparison. Hard negatives should be plausible environmental pages that do not answer the exact decision.

### Model Improvement Notes

Strong systems should connect practical scenarios to evidence categories such as lifecycle analysis, regulation, energy modeling, toxicity, and reuse constraints. Dense retrieval is the strongest observed first-stage method, but sparse features remain important for named chemicals, legal categories, and product terms.

The task is a useful benchmark for retrieval models that must support advice with evidence. Rerankers should prioritize passages that answer the comparative or decision-oriented part of the query.

## Example Data

| Query | Positive document |
| --- | --- |
| More uses for bacon grease We (my family) consume good amounts of bacon which produce a lot of bacon... [100 / 604 chars] | Tallow, or rendered beef fat, can be used to make soap. It went against my grain to throw out the tallow from a side of beef we bought, so I called our County Agent to see if he had any directions for... [200 / 2,693 chars] |
| Determining carbon reduction vs cost of various home upgrades I've done some amount of upgrades to m... [100 / 2,158 chars] | BEopt: Building Energy Optimization Tool The BEopt™ (Building Energy Optimization Tool) software provides capabilities to evaluate residential building designs and identify cost-optimal efficiency pac... [200 / 1,457 chars] |
| Forcing water circulation in solar hot water installation I'm planning an installation for heating w... [100 / 1,071 chars] | Here you can see the array of pipe going between the coil, the tank, and the domestic hot water plumbing. Alan transitioned to a flexible, pre-insulated stainless steel pipe to complete the thermosiph... [200 / 493 chars] |
| How to recognize products with neonicotinoid pesticides in them? Recently, the EU has temporarily ba... [100 / 561 chars] | Market [ [ edit ](/w/index.php?title=Neonicotinoid&action=edit&section=2 "Edit section: Market") ] ![](//upload.wikimedia.org/wikipedia/commons/thumb/9/98/Ambox_current_red.svg/42px- Ambox_current_red... [200 / 1,911 chars] |
| Why don't mineral water cans carry a deposit label? I've been putting in the recycling bin all our "... [100 / 443 chars] | What beverages are covered by NY's Bottle Bill? Carbonated Soft Drinks Including Sparkling Water Carbonated Energy Drinks Carbonated Juice (anything less than 100% juice, containing added sugar or wat... [200 / 444 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| What are additional uses for bacon grease instead of wasting it? | A practical source discusses rendered animal fat and soap-making reuse. |
| Which home upgrades reduce carbon most cost-effectively? | A building-energy optimization passage describes evaluating residential efficiency packages. |
| How should water circulate in a solar hot water installation? | A source describes plumbing and thermosiphon loop details for heated water. |
| How can products containing neonicotinoid pesticides be recognized? | A reference passage discusses neonicotinoids and market information. |
| Why do some sparkling or mineral water cans not carry deposit labels? | An official bottle-bill passage lists beverage categories covered by deposit rules. |
