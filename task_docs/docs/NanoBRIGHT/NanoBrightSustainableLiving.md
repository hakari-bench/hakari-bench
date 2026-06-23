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
| More uses for bacon grease We (my family) consume good amounts of bacon which produce a lot of bacon grease. I don't like wasting anything that I could reuse or repurpose, including this. I use this byproduct in many different ways, including: cooking. Filtered it can be used in cooking other foods or greasing the pans. pet food. Mixed with other foods, it is a good addition to the animals' diet. lubricant. Good for certain tools, or snow sleds. candles. Good source of light while camping or in... [500 / 604 chars] | Tallow, or rendered beef fat, can be used to make soap. It went against my grain to throw out the tallow from a side of beef we bought, so I called our County Agent to see if he had any directions for making soap. To my surprise, he did; to my further surprise, they were easy. I rendered the first batch of tallow by cutting it into chunks, filling the pan about one-third full of water and occasionally stirring the fat while it cooked at moderate heat. The stirring was a bit sloppy and the fat took quite a while to melt, so I ground subsequent batches of tallow in the meat grinder. This sped up the process considerably because I could then get more in the pan, it was easier to stir and the fat melted more rapidly. The melted tallow and water was sieved and cooled. When the fat had solidified, I lifted it off the top of the water — and it was ready for soap. While I was heating 6 pounds of the rendered fat (13-1/2 cups) to 120-130 degrees, I stirred together a 13 oz. can of lye and 5 cup... [1,000 / 2,693 chars] |
| Determining carbon reduction vs cost of various home upgrades I've done some amount of upgrades to my house to reduce my overall carbon emissions, and reading online there are all kinds of suggestions for doing even more: Replace my natural gas water heater with electric Put solar panels on the roof Buy wind energy credits Other kinds of carbon offsets Geothermal Don't replace my electric oven with gas (which I had been thinking about, since I hear how great they are for cooking) And of course I... [500 / 2,158 chars] | BEopt: Building Energy Optimization Tool The BEopt™ (Building Energy Optimization Tool) software provides capabilities to evaluate residential building designs and identify cost-optimal efficiency packages at various levels of whole-house energy savings along the path to zero net energy. BEopt can be used to analyze both new construction and existing home retrofits, as well as single-family detached and multi-family buildings, through evaluation of single building designs, parametric sweeps, and cost- based optimizations. BEopt provides detailed simulation-based analysis based on specific house characteristics, such as size, architecture, occupancy, vintage, location, and utility rates. Discrete envelope and equipment options, reflecting realistic construction materials and practices, are evaluated. BEopt uses [ EnergyPlus ](https://energyplus.net/) , the Department of Energy's flagship simulation engine. Simulation assumptions are based on [ ANSI/RESNET/ICC Standards ](https://www.res... [1,000 / 1,457 chars] |
| Forcing water circulation in solar hot water installation I'm planning an installation for heating water using solar "exchanger" panels (solar used to heat water directly, not through electricity). I don't want to bind the reservoir, panel and tap locations to the natural circulation cycle though (hot water traveling up etc). So, in order for this to work, I'd have to force some very slow water circulation between the reservoir and the panels; a pump that takes very little power and provides ver... [500 / 1,071 chars] | Here you can see the array of pipe going between the coil, the tank, and the domestic hot water plumbing. Alan transitioned to a flexible, pre-insulated stainless steel pipe to complete the thermosiphon loop (black-covered pipes in the background). In the foreground, you see the cold water “in” and the hot water “out” as well as the pvc drain which services the pressure/temperature valve and the pan beneath the hot water tank. Note: all pipes excluding cold water “in” should be insulated. [493 chars] |

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
