# NanoBRIGHT / NanoBrightEarthScienceLong

## Overview

NanoBrightEarthScienceLong is the long-document NanoBRIGHT slice for Earth Science StackExchange retrieval. Queries are technical Earth science questions, while candidate documents are long cited web pages rather than compact passage chunks. The task measures whether a retriever can identify a source page that contains the evidence needed for scientific reasoning, even when the matching section is embedded inside a much longer article, report, or documentation page.

## Details

### What the Original Data Measures

BRIGHT's long-document variants keep the reasoning-intensive StackExchange retrieval setting but replace passage-level retrieval with full or long source pages. For Earth Science, this means a query about geology, climate data, meteorology, planetary soil, atmospheric chemistry, or environmental measurement may map to a long NASA page, Wikipedia article, science report, or specialist explanatory source.

The key difficulty is evidence localization through retrieval. A relevant document may contain the answer-bearing section, but the page can also include navigation text, unrelated sections, background material, references, or broad topical coverage. Systems therefore need both scientific intent matching and enough robustness to long-document dilution.

### Observed Data Profile

The task contains 116 queries, 587 documents, and 186 relevance judgments. It has an average of 1.60 positives per query, with a minimum of 1, a median of 1.0, a maximum of 4, and 53 multi-positive queries, or 45.69% of the set.

Queries average 476.71 characters, matching the compact Earth Science slice. Documents average 70,649.63 characters, which makes this a very different retrieval problem from passage search. The corpus is small in document count, but each candidate can contain many possible topical sections.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3526, hit@10 of 0.6121, and recall@100 of 0.8172 using the top-500 BM25 candidate subset. The recall is relatively high, showing that exact Earth science terminology can still bring many positives into the candidate pool. Named concepts, datasets, substances, and technical phrases remain useful anchors.

The ranking quality is weaker than the recall profile. In long pages, the terms that match the query may appear in navigation, references, introductory sections, or adjacent topics rather than in the evidence-bearing portion. BM25 can therefore retrieve a plausible page but struggle to rank the truly useful source near the top.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5786, hit@10 of 0.8621, and recall@100 of 0.9032. This is the strongest nDCG@10 and hit@10 profile among the reported candidate subsets. Dense retrieval appears much better at connecting long contextual questions to pages whose overall semantic content supports the requested scientific explanation.

This pattern suggests that the long Earth Science task rewards embedding similarity more than exact term frequency. Queries often describe a phenomenon or practical problem in paragraph form, while relevant documents may express the evidence through broader scientific exposition. Dense retrieval is better suited to this semantic bridge.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.4971, hit@10 of 0.7845, and recall@100 of 0.9409. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 3 safeguard rows, candidate counts from 100 to 101, and a mean of 100.03 candidates.

The hybrid profile gives the best recall@100 but does not beat dense retrieval at the top of the ranking. This is an important diagnostic: combining sparse and dense candidates improves coverage, but the fused ordering can place some long-page positives below dense-only candidates. For downstream reranking, reranking_hybrid is attractive because it exposes the most positives within a smaller candidate pool.

### Metric Interpretation for Model Researchers

The contrast among metrics is central to this task. BM25 is useful for candidate coverage because technical terms survive long-document noise, but its top-10 ranking is limited. Dense retrieval is the best first-stage ranker at nDCG@10 and hit@10. Reranking_hybrid is the best pool for recall@100 and therefore the best diagnostic for reranker input coverage.

Researchers should avoid treating this as a simple lexical benchmark. The long-document setting tests whether a retriever can score a whole page as relevant when only a fraction of that page may answer the query. Models with strong long-context representations, section-aware pooling, or passage aggregation may have an advantage.

### Query and Relevance Type Tendencies

Queries ask about continental drift monitoring, weather forecasting statistics, oxygen production by plants, Martian soil simulants, ozone layer thickness, optical phenomena, and other scientific explanations. Relevant documents may be broad pages about paleomagnetism, algae, Mars soil, ozone chemistry, government science resources, or educational material.

The relevance relation is usually source-support rather than short-answer matching. A page may be relevant because it contains the evidence, definitions, measurements, or mechanism needed to answer the StackExchange question. Same-topic pages without the needed section are difficult negatives.

### Representative Failure Modes

Common failures include over-ranking a long page because it repeats query terms in a non-answering section, missing a source page whose useful section uses different wording, confusing broad topical similarity with answer support, and losing positives when document representations average away small but decisive evidence spans.

BM25 is exposed to term-frequency dilution and boilerplate. Dense retrieval is exposed to broad semantic false positives. Hybrid retrieval improves coverage but may still need a strong reranker or passage-level evidence extractor to order long documents effectively.

### Training Data That May Help

Useful training data includes long Earth science pages aligned with technical questions, scientific report retrieval pairs, climate and geoscience documentation search pairs, and source-backed QA where the positive is a full page rather than a pre-trimmed passage.

Synthetic data can help if it preserves long-document structure: generate multi-section science pages, write technical questions answerable by one section, and include hard negatives from pages on the same broad topic that omit the required evidence.

### Model Improvement Notes

For this task, dense document representations should preserve localized evidence rather than only global topic. Sparse systems need robust handling of technical terminology, units, and named datasets, but also mechanisms to reduce boilerplate impact. Hybrid systems should treat reranking_hybrid as a high-recall pool and rely on downstream models to recover top-rank precision.

Long-document retrievers may benefit from hierarchical encoding, passage aggregation, late interaction, or reranking that can inspect specific sections. The observed scores show that top-rank quality and candidate coverage are separated: dense is best for initial top-10 ranking, while reranking_hybrid is best for giving a reranker access to positives.

## Example Data

| Query | Positive document |
| --- | --- |
| How is/was continental drift monitored? I am curious about current technology but I am particularly interested in what techniques were employed prior to the advent of satellite technology. [189 chars] | Paleomagnetism - Wikipedia Jump to content Main menu Main menu move to sidebar hide Navigation Main pageContentsCurrent eventsRandom articleAbout WikipediaContact usDonate Contribute HelpLearn to editCommunity portalRecent changesUpload file Search Search Create account Log in Personal tools Create account Log in Pages for logged out editors learn more ContributionsTalk Contents move to sidebar hide (Top) 1History 2Fields 3Principles Toggle Principles subsection 3.1Thermoremanent magnetization 3.2Detrital remanent magnetization 3.3Chemical remanent magnetization 3.4Isothermal remanent magnetization 3.5Viscous remanent magnetization 4Sampling 5Applications 6See also 7Notes 8References 9Further reading 10External links Toggle the table of contents Paleomagnetism 42 languages AfrikaansالعربيةAzərbaycancaBosanskiCatalàČeštinaDeutschEspañolEuskaraفارسیFrançaisGaeilgeGalego한국어Հայերենहिन्दीHrvatskiBahasa IndonesiaItalianoעבריתҚазақшаMagyarमराठीBahasa MelayuNederlands日本語Norsk bokmålNorsk nynor... [1,000 / 21,493 chars] |
| I am a lay person in meteorology, maybe this is not the right place for my question, but I would like to ask then. My question is simple: is there a website or institute that has integrated statistics on forecasting the occurrence of rainbows in different countries around the world? [284 chars] | How Rainbows Form - Overview How Rainbows Form Overview Steps Involved Overview Copyright 1999 Rebecca McDowell. Figure 1: Basic diagram showing formation of rainbow. Note: Angles not to scale. The formation of a rainbow involves a series of physical phenomena - reflection, refraction, dispersion and total internal reflection. The occurence of each of these is due to the interaction of light with air and water and the boundaries between them. Enlarged view of diagram. The Steps Involed in the Process Figure 2: Ray digram - light through raindrop Copyright 1999 Rebecca McDowell. 1. Light from Sun strikes raindrop 2. Some of the light is reflected 3. The rest of the light is refracted 4. Light splits into component colours 5. Reflected at rear of raindrop (TIR) 6. Refracted again as it leaves raindrop 7. Colours are further dispersed Click on the links above for more detail on ech step. 1. Light from sun strikes raindrop. White light from the Sun has to hit the raindrops at a certain ang... [1,000 / 3,583 chars] |
| Which plant is the most efficient in making oxygen for it's weight? I want to think it is the greenest plant with more leaves and least trunk in full sun? [154 chars] | Algae - Rocky Mountain National Park (U.S. National Park Service) Skip to global NPS navigation Skip to this park navigation Skip to the main content Skip to this park information section Skip to the footer section National Park Service Search Search This Site All NPS Open Menu Close Menu Explore This Park Explore the National Park Service Exiting nps.gov Cancel Rocky Mountain National Park Colorado Info Alerts Maps Calendar Fees Loading alerts Alerts In Effect Dismiss more information on current conditions... Dismiss View all alerts Contact Us Algae While some plants decorate the landscape and are very visible at Rocky Mountain National Park, others are seldom seen. Tiny floating plants, called algae, live in lakes, wetlands, and ponds. Individual algae are virtually invisible, but when they congregate, they turn into the green 'slime' on stream rocks. Algae are important because they produce oxygen, provide food for themselves (photosynthesis) as well as food for larger aquatic (wate... [1,000 / 6,419 chars] |

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
| How was continental drift monitored before satellite technology? | A long reference article discusses paleomagnetism and other evidence related to continental movement. |
| Where can a non-specialist find integrated statistics on weather forecast occurrence? | A long educational page explains optical and atmospheric phenomena with supporting diagrams and context. |
| Which plant is most efficient at producing oxygen for its weight? | A source page discusses algae and plant-like organisms in a broader environmental context. |
| How can a student approximate Martian soil for a science project? | A long article describes a Mars simulation experiment and the materials used to create a soil-like environment. |
| How should ozone layer thickness in Dobson units be understood? | A broad chemistry page covers halogenated compounds and atmospheric effects relevant to ozone depletion. |
