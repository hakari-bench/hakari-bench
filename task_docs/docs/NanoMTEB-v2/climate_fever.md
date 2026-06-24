# NanoMTEB-v2 / climate_fever

## Overview

`NanoMTEB-v2 / climate_fever` is a Climate-FEVER hard-negative retrieval task. Queries are real-world climate claims, and documents are Wikipedia evidence passages. The original CLIMATE-FEVER dataset adapts FEVER-style evidence verification to climate-change claims gathered from the web, requiring systems to retrieve evidence that can support, refute, or otherwise bear on those claims. This Nano split contains 200 claims over 10,000 documents and is strongly multi-positive: most claims have several evidence passages. It is useful for studying scientific evidence retrieval, claim wording, and the limits of lexical matching when claims use public talking-point language but evidence is distributed across broader encyclopedia passages.

## Details

### What the Original Data Measures

CLIMATE-FEVER measures evidence retrieval and verification for climate-related claims. The retrieval component asks whether a system can find passages that are evidentially relevant to the claim, not merely passages that mention climate in general. Evidence may support or refute a claim, and the source passages often come from Wikipedia articles about climate science, weather, ecology, energy, or related topics.

The MTEB hard-negative version increases difficulty by using candidate passages that are plausible but not necessarily evidential. This Nano task preserves that claim-to-evidence retrieval setting.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 621 positive qrel rows. Queries have 3.105 positives on average, with a median of 3 and a maximum of 5. There are 181 multi-positive queries, or 90.5% of the query set. Queries average 114.97 characters, while documents average 1,115.93 characters.

The examples include claims about sea-level rise, water vapor, model predictions, sunspot activity, and U.S. flooding trends. Relevant documents are often broad Wikipedia passages, so the evidence may be embedded in a larger scientific or historical explanation.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1719, hit@10 of 0.4550, and recall@100 of 0.5250. BM25 struggles because climate claims often use concise public-argument phrasing, while the evidence passages use encyclopedia language, article titles, or broader scientific context.

Lexical overlap helps on claims with distinctive terms such as `greenhouse gas`, `sunspot`, or `sea-level`, but it is not sufficient for evidential relevance. BM25 may retrieve passages that share climate vocabulary without containing the specific evidence needed for the claim.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3276, hit@10 of 0.7300, and recall@100 of 0.6522. Dense retrieval is much stronger than BM25 in both top-rank quality and recall, showing that semantic matching is critical for climate evidence retrieval.

This profile suggests that embeddings can bridge claim wording and evidence phrasing more effectively than sparse term overlap. However, the task remains difficult: a semantically related passage about climate is not always evidence for the specific claim, especially when the claim contains quantities, causal relations, or negated framing.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 17 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.2794, hit@10 of 0.6600, and recall@100 of 0.6747. The hybrid candidate pool has the best recall@100, but dense retrieval remains stronger at nDCG@10 and hit@10.

This indicates that BM25 adds some complementary evidence candidates, but it also brings many lexical climate negatives into the top candidate window. A reranker can benefit from the hybrid pool if it learns evidential relevance rather than broad climate topicality.

### Metric Interpretation for Model Researchers

The high multi-positive rate changes how metrics should be read. A system can improve recall by finding any of several evidence passages, but nDCG@10 still measures whether the most useful evidence appears early. Because many queries have multiple positives, recall@100 is a meaningful coverage metric for downstream verification systems.

Dense retrieval is the strongest first-stage ranking signal, while hybrid retrieval is strongest for exposing positives to a reranker. This makes the task a good testbed for claim-evidence reranking, especially with hard negatives that share climate vocabulary.

### Query and Relevance Type Tendencies

Queries are English climate claims, often written as declarative statements rather than questions. They may include numbers, temporal comparisons, causal claims, attribution, or skeptical framing. Relevant documents are Wikipedia passages that provide evidence related to the claim.

The relevance relation is evidential. A passage about the same climate topic is not enough unless it can support, refute, or contextualize the specific claim.

### Representative Failure Modes

Common failures include retrieving a general climate-change page for a specific claim, matching a keyword such as `temperature` or `emissions` without finding the relevant evidence, missing negation or causal framing, and confusing related phenomena such as weather variability, sea level, ice loss, and greenhouse gases. Dense systems may over-rank broad semantic matches; sparse systems may over-rank passages with repeated climate terms.

### Training Data That May Help

Useful training data includes climate claim-evidence retrieval pairs, FEVER-style evidence retrieval, scientific fact-checking datasets, and hard negatives with overlapping climate vocabulary. Multi-positive training is recommended because many claims can be evidenced by several passages.

### Model Improvement Notes

Models should learn evidence specificity, not only topic similarity. Training should include claims with numbers, dates, causal statements, and negation, as well as hard negatives from the same climate subtopic. Rerankers should be evaluated on whether they lift genuinely evidence-bearing passages above broad topical matches.

## Example Data

| Query | Positive document |
| --- | --- |
| Currently, sea-level rise does not seem to depend on ocean temperature, and certainly not on CO2. [97 chars] | Paleocene–Eocene Thermal Maximum The Paleocene -- Eocene Thermal Maximum ( PETM ) , alternatively ( ETM1 ) , and formerly known as the `` Initial Eocene '' or '' '' was a time period with more than 8 ° C warmer global average temperature than today . This climate event began at the time boundary between the Paleocene and Eocene geological epochs . The exact age and duration of the event is uncertain but it is estimated to have occurred around 55.5 million years ago . The associated period of massive carbon injection into the atmosphere has been estimated to have lasted no longer than 20,000 years . The entire warm period lasted for about 200,000 years . Global temperatures increased by 5 -- 8 ° C . The carbon dioxide was likely released in two pulses , the first lasting less than 2,000 years . Such a repeated carbon release is in line with current global warming . A main difference is that during the Paleocene -- Eocene Thermal Maximum , the planet was essentially ice-free . The onset... [1,000 / 2,549 chars] |
| The main greenhouse gas is water vapour[…] [42 chars] | Greenhouse gas A greenhouse gas ( abbrev . GHG ) is a gas in an atmosphere that absorbs and emits radiation within the thermal infrared range . This process is the fundamental cause of the greenhouse effect . The primary greenhouse gases in Earth 's atmosphere are water vapor , carbon dioxide , methane , nitrous oxide , and ozone . Without greenhouse gases , the average temperature of Earth 's surface would be about -18 ° C , rather than the present average of 15 ° C . In the Solar System , the atmospheres of Venus , Mars and Titan also contain gases that cause a greenhouse effect . Human activities since the beginning of the Industrial Revolution ( taken as the year 1750 ) have produced a 40 % increase in the atmospheric concentration of carbon dioxide , from 280 ppm in 1750 to 406 ppm in early 2017 . This increase has occurred despite the uptake of a large portion of the emissions by various natural `` sinks '' involved in the carbon cycle . Anthropogenic carbon dioxide emissions ( i... [1,000 / 1,706 chars] |
| the warming is not nearly as great as the climate change computer models have predicted. [88 chars] | Deforestation Deforestation , clearance or clearing is the removal of a forest or stand of trees where the land is thereafter converted to a non-forest use . Examples of deforestation include conversion of forestland to farms , ranches , or urban use . The most concentrated deforestation occurs in tropical rainforests . About 30 % of Earth 's land surface is covered by forests . Deforestation occurs for multiple reasons : trees are cut down to be used for building or sold as fuel , ( sometimes in the form of charcoal or timber ) , while cleared land is used as pasture for livestock and plantation . The removal of trees without sufficient reforestation has resulted in damage to habitat , biodiversity loss and aridity . It has adverse impacts on biosequestration of atmospheric carbon dioxide . Deforestation has also been used in war to deprive the enemy of vital resources and cover for its forces . Modern examples of this were the use of Agent Orange by the British military in Malaya dur... [1,000 / 2,080 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | source task paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/ClimateFEVER_test_top_250_only_w_correct-v2 |  | dataset card | [https://huggingface.co/datasets/mteb/ClimateFEVER_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/ClimateFEVER_test_top_250_only_w_correct-v2) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Currently, sea-level rise does not seem to depend on ocean temperature, and certainly not on CO2. | A Wikipedia passage about the Paleocene-Eocene Thermal Maximum and a period of much warmer global average temperature. |
| The main greenhouse gas is water vapour. | A passage defining greenhouse gases and explaining their role in the greenhouse effect. |
| the warming is not nearly as great as the climate change computer models have predicted. | A passage connected to climate-change effects and environmental change, used as evidence for the claim. |
| [S]unspot activity on the surface of our star has dropped to a new low. | A passage about the Sun, solar plasma, and magnetic activity. |
| Since 1965, more parts of the U.S. have seen a decrease in flooding than have seen an increase. | A passage about effects of global warming and environmental changes linked to greenhouse-gas emissions. |
