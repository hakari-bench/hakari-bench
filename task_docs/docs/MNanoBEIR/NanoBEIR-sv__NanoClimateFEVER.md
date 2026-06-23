# MNanoBEIR / NanoBEIR-sv / NanoClimateFEVER

## Overview

NanoClimateFEVER in the Swedish NanoBEIR slice is an evidence retrieval task derived from CLIMATE-FEVER. The queries are Swedish translated climate-related claims, and the corpus contains Swedish translated evidence passages. The retrieval goal is to find passages that can verify or contextualize a claim about climate science, climate change, or related public claims. This makes the task a compact diagnostic for scientific fact-checking retrieval in a multilingual setting, where the model must combine topical climate vocabulary with evidence-sensitive matching.

## Details

### What the Original Data Measures

CLIMATE-FEVER evaluates whether systems can retrieve evidence for real-world climate claims. In retrieval form, a query is a claim and relevant documents are passages that contain evidence needed to assess it. The task is more specific than broad climate-topic search: a passage about sea level, temperature, hurricanes, or solar cycles is not automatically relevant unless it bears on the particular claim.

The Swedish translated version adds multilingual issues around scientific terminology, long factual statements, and translated named phenomena. Many claims contain quantities, dates, causal language, or scientific qualifiers. A strong retriever must preserve these details while also recognizing evidence passages that express the same scientific issue with different wording.

### Observed Data Profile

The task contains 50 queries, 3,408 documents, and 148 relevance judgments. Most queries have multiple positives, with an average of 2.96 positives per query. The minimum is 1, the median is 3.0, the maximum is 5, and 44 queries are multi-positive, or 88.0% of the query set. This makes the task a multi-evidence benchmark rather than a single-document lookup.

Queries average 132.16 characters, and documents average 1,538.72 characters. The claims are longer than many search queries because they often encode a full assertion. The evidence passages are much longer and may include background explanation, definitions, or scientific context. This length asymmetry makes ranking difficult: the relevant evidence may be a small part of a long passage.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2388, hit@10 of 0.5800, and recall@100 of 0.4595 using the top-500 BM25 candidate subset. This is a weak-to-moderate lexical profile. Climate claims often contain recognizable terms, but the exact claim wording and the evidence wording can differ substantially, and long passages can dilute the most important evidence terms.

The BM25 result suggests that lexical overlap alone often struggles to retrieve the full evidence set. It may find passages that share visible climate vocabulary but miss evidence expressed through paraphrase, definitions, or broader scientific context. The low recall@100 is especially important because most queries have multiple positives; missing candidates limits what any later reranker can recover.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2633, hit@10 of 0.6800, and recall@100 of 0.5811. Dense retrieval improves over BM25 on all three metrics. This indicates that embedding similarity helps connect claims to evidence passages even when they do not share exact wording.

The improvement is meaningful but still leaves the task difficult. Climate evidence retrieval requires matching not only the broad topic but also the direction and specificity of the claim. A dense model can retrieve passages about global warming, sea level, or solar activity, but may still rank topically related background above the passage that verifies the claim. The task therefore exposes the limits of general semantic similarity for scientific fact-checking.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3202, hit@10 of 0.7800, and recall@100 of 0.5946. It uses a top-100 candidate range with an optional rank-101 safeguard; the observed candidate count ranges from 100 to 101, with 4 safeguard rows and a mean of 100.08 candidates. This is the strongest profile among the three search modes.

The hybrid result shows that this task benefits from combining lexical climate anchors with dense semantic evidence matching. BM25 contributes precise terms such as named phenomena, dates, and scientific labels, while dense retrieval captures paraphrased evidence and broader context. The gains in nDCG@10 and hit@10 indicate that the combined signal improves first-page quality, not only candidate coverage.

### Metric Interpretation for Model Researchers

nDCG@10 measures whether the first results contain useful evidence passages, while hit@10 measures whether at least one evidence passage is visible in the practical top ranks. recall@100 is important because most queries have several positives; a system that finds only one evidence passage may not support robust verification. The gap between the current recall values and a complete evidence set shows that this benchmark remains challenging for candidate generation.

The method comparison is clear. BM25 is limited by exact wording. Dense retrieval improves both semantic coverage and top-rank access. reranking_hybrid is strongest overall, suggesting that Swedish climate claim retrieval needs both terminology precision and semantic paraphrase handling. This makes the task useful for evaluating hybrid search design and evidence reranking.

### Query and Relevance Type Tendencies

Queries are full climate claims, often involving time ranges, statistical significance, sea-level variation, hurricanes, global warming attribution, or cosmic rays. Relevant passages are evidence-bearing explanatory texts. They may describe scientific definitions, climate mechanisms, measurement records, or attribution arguments.

The task rewards models that handle qualifiers. Words such as "downward," "not statistically significant," "local and regional," or "required to blame" change what evidence is relevant. A model that retrieves only broadly climate-related passages may miss the central verification need.

### Representative Failure Modes

Likely failures include retrieving passages that mention the same climate topic but do not verify the claim, missing evidence because the claim and passage use different phrasing, over-ranking broad global warming explanations for specific claims, and failing to distinguish statistical or causal qualifiers. BM25 is vulnerable to vocabulary mismatch, while dense models may overgeneralize to topically similar but evidentially weak passages.

### Training Data That May Help

Useful training data includes climate claim verification, scientific evidence retrieval, multilingual fact-checking, climate QA, and hard negatives that share climate terms but fail to verify the claim. Swedish scientific and public-policy text can help with local phrasing, while English climate evidence data can help if multilingual transfer is strong. For rerankers, near-topic non-evidence passages are especially valuable.

### Model Improvement Notes

A model targeting this task should improve evidence specificity. Sparse systems need better term normalization and expansion for climate terminology. Dense systems need stronger handling of numerical, causal, and negation-like qualifiers. Hybrid systems are well suited to the benchmark, but further gains likely require a reranker that reads the claim-passage relation rather than only scoring broad semantic similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Från 1970 till 1998 fanns det en uppvärmningsperiod som höjde temperaturerna med cirka 0,7 Fahrenhei... [100 / 164 chars] | Paleocen (uttalas /ˈpæliəˌsiːn/ eller /ˈpæ - , - lioʊ - /) eller Paleocen, den "gamla nya", är en geologisk epok som varade från cirka . Det är den första epoken i Paleogenperioden under den moderna C... [200 / 1,004 chars] |
| I själva verket är trenden nedåtgående, även om det inte är statistiskt signifikant. [84 chars] | Solarcykeln eller solaktivitetscykeln är den nästan periodiska 11-årsförändringen i solens aktivitet (inklusive förändringar i nivåerna av solstrålning och utsändning av solmaterial) och utseende (för... [200 / 607 chars] |
| Lokala och regionala havsnivåer fortsätter visa den vanliga naturliga variationen, stiger på vissa s... [100 / 128 chars] | Medelhavsnivå (MSL) (förkortat havsnivå) är en genomsnittlig nivå av jordens havsytor, från vilken höjder som höjder kan mätas. MSL är en typ av vertikal datum, en standardiserad geodetisk referenspun... [200 / 867 chars] |
| Klimatforskare säger att i fallet med Orkanen Harvey tyder det på att global uppvärmning förvärrar e... [100 / 124 chars] | De globala uppvärmningens effekter är de miljö- och samhällsförändringar som orsakas (direkt eller indirekt) av människans utsläpp av växthusgaser. Det finns en vetenskaplig konsensus om att klimatför... [200 / 1,368 chars] |
| CERN:s CLOUD-experiment testade endast en tredjedel av ett av fyra krav som krävs för att skylla på... [100 / 197 chars] | Tillskrivning av den senaste klimatförändringen är ansträngningen att vetenskapligt fastställa mekanismer som är ansvariga för de senaste klimatförändringarna på jorden, vanligtvis kända som `global u... [200 / 2,098 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Från 1970 till 1998 fanns det en uppvärmningsperiod som höjde temperaturerna med cirka 0,7 Fahrenheit... | Paleocen eller Paleocen, den "gamla nya", är en geologisk epok som varade från cirka... |
| I själva verket är trenden nedåtgående, även om det inte är statistiskt signifikant. | Solarcykeln eller solaktivitetscykeln är den nästan periodiska 11-årsförändringen i solens aktivitet... |
| Lokala och regionala havsnivåer fortsätter visa den vanliga naturliga variationen, stiger på vissa ställen och sjunker på andra. | Medelhavsnivå (MSL) är en genomsnittlig nivå av jordens havsytor... |
| Klimatforskare säger att i fallet med Orkanen Harvey tyder det på att global uppvärmning förvärrar en redan dålig situation. | De globala uppvärmningens effekter är de miljö- och samhällsförändringar som orsakas av människans utsläpp... |
| CERN:s CLOUD-experiment testade endast en tredjedel av ett av fyra krav som krävs för att skylla på kosmiska strålar... | Tillskrivning av den senaste klimatförändringen är ansträngningen att vetenskapligt fastställa mekanismer... |
