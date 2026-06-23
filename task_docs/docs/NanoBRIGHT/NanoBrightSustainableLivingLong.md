# NanoBRIGHT / NanoBrightSustainableLivingLong

## Overview

NanoBrightSustainableLivingLong is the long-document Sustainable Living StackExchange slice of NanoBRIGHT. Queries are practical sustainability questions, and relevant documents are full cited pages, reports, official guidance pages, or long environmental references. The task measures whether a retriever can identify the source page containing evidence for a specific environmental decision, even when the answer-bearing section is embedded inside a long document.

## Details

### What the Original Data Measures

BRIGHT's long-document variants retrieve full source pages rather than split passages. In Sustainable Living, those pages can be environmental reports, product guidance, government pages, energy-program documentation, encyclopedia pages, or practical sustainability articles.

The task retains the practical reasoning nature of the passage-level slice: the model must find evidence for a decision about reuse, energy, carbon, materials, recycling, or environmental risk. Long documents add extra difficulty because pages often cover many related topics and include navigation, legal context, examples, and caveats.

### Observed Data Profile

The task contains 108 queries, 551 documents, and 129 relevance judgments. It is mostly single-positive: there are 1.19 positives per query on average, a minimum of 1, a median of 1.0, a maximum of 5, and 15 multi-positive queries, or 13.89% of the set.

Queries average 682.84 characters, while documents average 38,204.30 characters. The corpus has far fewer documents than the passage version, but each candidate may include several sections and broad sustainability vocabulary.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3277, hit@10 of 0.5000, and recall@100 of 0.8992 using the top-500 BM25 candidate subset. Sparse retrieval has strong recall because long environmental pages contain many query terms, product names, materials, and policy expressions.

The top-rank quality is much weaker than recall. A long page can mention carbon, recycling, energy, pesticides, or water while not containing the evidence needed for the user's specific decision. BM25 is useful for candidate coverage but struggles to order the most supportive source pages first.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5501, hit@10 of 0.7870, and recall@100 of 0.9690. Dense retrieval is the strongest top-ranking profile in this task and greatly improves over BM25 for nDCG@10 and hit@10.

This indicates that semantic matching is highly valuable for long sustainability sources. Dense retrieval can connect a practical question to the page whose overall content supports the relevant decision, even when the page does not repeat the query wording exactly.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4436, hit@10 of 0.6852, and recall@100 of 0.9845. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 2 safeguard rows, candidate counts from 100 to 101, and a mean of 100.02 candidates.

The hybrid profile has the best recall@100 but does not beat dense retrieval at the top of the ranking. This means the fused pool is excellent for downstream reranking, while dense retrieval alone provides the strongest first-page ordering for this long-document slice.

### Metric Interpretation for Model Researchers

This task separates top-rank semantic quality from candidate coverage. BM25 has strong recall because long source pages contain many environmental terms. Dense retrieval is best for nDCG@10 and hit@10 because it captures the practical decision intent. Reranking_hybrid is best for recall@100 and is therefore attractive as a reranker input pool.

Researchers should evaluate whether systems retrieve the page that actually contains evidence for the environmental decision. A page can be about sustainability and still fail to answer the specific question. Long-document models should ideally combine source-page retrieval with section-level evidence extraction.

### Query and Relevance Type Tendencies

Queries ask about reusing bacon grease, carbon-reduction upgrades, solar water circulation, neonicotinoid recognition, deposit-label rules, product lifecycle impacts, and household environmental decisions. Positive long documents may be government pages, energy-lab documents, practical guides, encyclopedia pages, or product and program references.

The relevance relation is source-level evidence support. The document is positive because it contains the necessary environmental, technical, or regulatory evidence, not because every section is relevant.

### Representative Failure Modes

Likely failures include retrieving a long environmental page with broad vocabulary but no decision evidence, over-ranking a product page that lacks lifecycle or regulatory detail, missing official guidance because the query uses everyday wording, and confusing adjacent impact categories such as energy use, emissions, waste, and toxicity.

BM25 is exposed to long-page term dilution. Dense retrieval can still prefer a semantically plausible source with insufficient evidence. Hybrid retrieval improves coverage but needs reranking to recover dense-like top precision.

### Training Data That May Help

Useful training data includes long environmental report retrieval, document-level sustainability QA, cited-source retrieval from environmental forums, and passage-to-full-page supervision that maps evidence spans to source documents.

Synthetic data should generate long environmental pages about products, materials, energy, lifecycle impacts, and policy caveats. Questions should ask practical comparisons or decision criteria. Hard negatives should cover the same product or impact category but fail to answer the exact question.

### Model Improvement Notes

Strong systems should combine practical decision understanding with source-page evidence retrieval. Dense retrieval is the best observed first-stage ranker, while reranking_hybrid gives the broadest candidate coverage. A useful production system would retrieve with a hybrid pool and rerank or extract the section that directly supports the decision.

The task is a good probe for whether retrieval models can support environmental advice with evidence rather than merely matching green-living vocabulary.

## Example Data

| Query | Positive document |
| --- | --- |
| More uses for bacon grease We (my family) consume good amounts of bacon which produce a lot of bacon grease. I don't like wasting anything that I could reuse or repurpose, including this. I use this byproduct in many different ways, including: cooking. Filtered it can be used in cooking other foods or greasing the pans. pet food. Mixed with other foods, it is a good addition to the animals' diet. lubricant. Good for certain tools, or snow sleds. candles. Good source of light while camping or in... [500 / 604 chars] | [ ![Mother Earth News](https://ogden_images.s3.amazonaws.com/www.motherearthnews.com/images/2022/03/04200002/men_logo.svg) ](https://www.motherearthnews.com) * [ Organic Gardening ](https://www.motherearthnews.com/organic-gardening/) * [ Fruits ](https://www.motherearthnews.com/organic-gardening/fruits/) * [ Garden Planning ](https://www.motherearthnews.com/organic-gardening/garden-planning/) * [ Garden Tools ](https://www.motherearthnews.com/organic-gardening/garden-tools/) * [ Gardening Techniques ](https://www.motherearthnews.com/organic-gardening/gardening-techniques/) * [ Herbs ](https://www.motherearthnews.com/organic-gardening/herbs/) * [ Ornamentals ](https://www.motherearthnews.com/organic-gardening/ornamentals/) * [ Pest Control ](https://www.motherearthnews.com/organic-gardening/pest-control/) * [ Vegetables ](https://www.motherearthnews.com/organic-gardening/vegetables/) * [ Homesteading & Livestock ](https://www.motherearthnews.com/homesteading-and-livestock/) * [ Livestoc... [1,000 / 35,063 chars] |
| Determining carbon reduction vs cost of various home upgrades I've done some amount of upgrades to my house to reduce my overall carbon emissions, and reading online there are all kinds of suggestions for doing even more: Replace my natural gas water heater with electric Put solar panels on the roof Buy wind energy credits Other kinds of carbon offsets Geothermal Don't replace my electric oven with gas (which I had been thinking about, since I hear how great they are for cooking) And of course I... [500 / 2,158 chars] | Skip to main content [ ![National Renewable Energy Laboratory](/assets/images/nrel-logo-web.svg) ](/) Toggle Search Search NREL.gov Search [ Buildings ](/buildings/) Menu * Research * [ Research __ ](/buildings/research.html) * [ Building Energy Modeling ](/buildings/building-energy-modeling.html) * [ Communities & Urban Districts ](/buildings/communities.html) * [ Extreme Climates ](/buildings/extreme-climates.html) * [ Industrialized Construction ](/buildings/industrialized-construction.html) * [ Lighting ](/buildings/lighting.html) * [ Resilient Buildings ](/buildings/resilient-buildings.html) * [ Sensors & Controls ](/buildings/sensors-controls.html) * [ Systems Technologies ](/buildings/systems-technologies.html) * [ Thermal Energy Storage ](/buildings/storage.html) * [ Windows ](/buildings/windows.html) * [ Workforce Development ](/buildings/workforce-development.html) * [ Staff ](/buildings/staff.html) * Publications * [ Publications __ ](/buildings/publications.html) * [ Newsle... [1,000 / 17,158 chars] |
| Forcing water circulation in solar hot water installation I'm planning an installation for heating water using solar "exchanger" panels (solar used to heat water directly, not through electricity). I don't want to bind the reservoir, panel and tap locations to the natural circulation cycle though (hot water traveling up etc). So, in order for this to work, I'd have to force some very slow water circulation between the reservoir and the panels; a pump that takes very little power and provides ver... [500 / 1,071 chars] | Skip to content [ ](https://www.firespeaking.com/wp- login.php?redirect_to=https%3A%2F%2Fwww.firespeaking.com%2Fmasonry- heaters%2Fheat-water%2Fdetails-of-plumbing) Username or Email Address Password Remember Me [ Lost your password? ](https://www.firespeaking.com/my-account/lost- password/) Search for: Search _ _ Search [ Cart _ _ ](https://www.firespeaking.com/cart/) [ ![Firespeaking logo](https://www.firespeaking.com/wp- content/uploads/2022/04/Firespeaking_Logo-type-header-360x50.png) ](https://www.firespeaking.com/) * [ Hardware ](https://www.firespeaking.com/product-category/masonry-heater-hardware/) Menu Toggle * [ Whole Heater Packages ](https://www.firespeaking.com/product-category/masonry-heater-hardware/bundles/) * [ Firebox Doors ](https://www.firespeaking.com/product-category/masonry-heater-hardware/firebox-doors/) * [ Oven Doors ](https://www.firespeaking.com/product-category/masonry-heater-hardware/oven-doors/) * [ Cleanout Doors & Ash Doors ](https://www.firespeaking.co... [1,000 / 19,918 chars] |

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
| What are additional uses for bacon grease instead of wasting it? | A long practical living article discusses reuse of rendered fats and related household applications. |
| Which home upgrades reduce carbon most cost-effectively? | A long NREL-style page describes building energy optimization and efficiency package evaluation. |
| How should water circulate in a solar hot water installation? | A long plumbing guide discusses thermosiphon loop and solar hot water details. |
| How can products containing neonicotinoid pesticides be recognized? | A long reference page explains neonicotinoid products, markets, and pesticide context. |
| Why do some sparkling or mineral water cans not carry deposit labels? | A government environmental page lists beverage deposit categories and exclusions. |
