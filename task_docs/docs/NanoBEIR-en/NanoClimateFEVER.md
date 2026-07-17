# NanoBEIR-en / NanoClimateFEVER

## Overview

NanoClimateFEVER is the compact English NanoBEIR version of Climate-FEVER, a climate-change claim evidence retrieval task. Each query is a real-world climate-related claim, and the system must retrieve Wikipedia evidence passages that support, refute, or otherwise address the claim. The task is useful for evaluating claim-to-evidence retrieval, climate-domain terminology, numeric and temporal grounding, and retrieval under misinformation-style wording.

## Details

### What the Original Data Measures

Climate-FEVER was created for verification of real-world climate claims. Unlike synthetic fact-checking claims, many Climate-FEVER claims come from public discourse and can contain hedging, partial truths, misleading framing, quantities, dates, or references to institutions. The retrieval step asks whether a system can surface evidence that a verifier could use.

The BEIR version evaluates retrieval of evidence documents or passages rather than final entailment labels. The NanoBEIR version keeps this claim-evidence structure in a smaller English sample. A strong retriever must understand the claim's climate subtopic and evidential target, not just retrieve broadly climate-related pages.

### Observed Data Profile

The task contains 50 queries, 3,408 documents, and 148 relevance judgments. It is strongly multi-positive, with an average of 2.96 positives per query. The minimum is 1, the median is 3.0, the maximum is 5, and 44 queries are multi-positive, or 88.0% of the set.

Queries average 128.40 characters, while documents average 1,619.53 characters. The queries are long declarative claims rather than short questions. Documents are Wikipedia-style evidence passages that may discuss climate indicators, temperature records, sea level, greenhouse gases, attribution, ice sheets, or climate change denial.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3266, hit@10 of 0.7200, and recall@100 of 0.5743 using the top-500 BM25 candidate subset. Lexical matching helps when claims contain distinctive entities, numbers, or phrases such as NASA, NOAA, sea level, solar activity, or specific time spans.

The low recall@100 shows that climate evidence retrieval is not solved by term overlap. Evidence may use different wording from the claim, and misleading claims can contain terms that pull BM25 toward topically related but non-evidential pages. BM25 often finds the climate topic but not enough of the evidence set.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2811, hit@10 of 0.6800, and recall@100 of 0.6757. Dense retrieval improves recall@100 over BM25 but is weaker in top-10 ranking. This suggests that embedding similarity broadens the candidate pool but can rank broad climate context above the most directly evidential passages.

This profile is important for climate claim retrieval. Dense similarity can connect paraphrased claims to related evidence, but the task often depends on exact quantities, time periods, or scientific subtopics. A general dense model may retrieve semantically plausible climate passages that do not verify the specific claim.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.3419, hit@10 of 0.7600, and recall@100 of 0.7027. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.02 candidates. It is the strongest profile across the reported metrics.

The hybrid result shows that Climate-FEVER benefits from combining exact climate anchors with dense semantic coverage. BM25 contributes names, numbers, dates, and key climate terms, while dense retrieval adds evidence passages that use different wording. The combined candidate pool is the best observed starting point for a verifier or reranker.

### Metric Interpretation for Model Researchers

Because most queries have several positives, nDCG@10 rewards systems that rank multiple evidence passages well, while hit@10 only measures whether at least one useful passage is visible. recall@100 is important because fact-checking pipelines often depend on a downstream verifier or reranker.

The comparison shows that BM25 is useful but coverage-limited, dense retrieval increases candidate coverage but weakens top ranking, and reranking_hybrid gives the best balance. This task is useful for testing whether retrieval models can combine climate-domain lexical cues with claim-level semantic evidence matching.

### Query and Relevance Type Tendencies

Queries include claims about warming periods, statistically insignificant trends, regional sea-level variability, Hurricane Harvey and global warming, and cosmic rays as an explanation for climate change. The relevant documents include pages or passages about temperature records, sea level, solar cycles, attribution of climate change, greenhouse gases, and effects of global warming.

The task rewards precise evidence targeting. A passage can mention the same climate topic yet fail to address the specific claim. Claims with numbers, dates, and causal language are especially sensitive to evidence mismatch.

### Representative Failure Modes

Likely failures include retrieving generic climate pages for specific claims, missing evidence because the claim uses misleading wording, over-ranking passages that share a number or entity but address another issue, and failing to distinguish support, refutation, and qualification. BM25 may be distracted by surface terms, while dense retrieval may be too broad.

### Training Data That May Help

Useful training data includes non-overlapping climate claim-evidence retrieval pairs, FEVER-style fact verification data, scientific claim verification, climate FAQ evidence retrieval, and hard negatives that share the same climate topic but do not address the claim. Climate-FEVER and BEIR-derived evaluation examples should be audited carefully for overlap.

### Model Improvement Notes

A model targeting this task should improve claim-specific evidence ranking while preserving climate-domain anchors. Sparse systems need expansion for climate terminology and careful handling of numbers and dates. Dense systems need training on claim-to-evidence pairs rather than only topical similarity. Hybrid systems are promising because the observed profile is strongest when lexical and semantic signals are combined.

## Example Data

| Query | Positive document |
| --- | --- |
| From 1970 until 1998 there was a warming period that raised temperatures by about 0.7 F that helped spawn the global warming alarmist movement. [143 chars] | The Paleocene ( -LSB- pronˈpæliəˌsiːn , _ ˈpæ - , _ - lioʊ - -RSB- ) or Palaeocene , the `` old recent '' , is a geologic epoch that lasted from about . It is the first epoch of the Paleogene Period in the modern Cenozoic Era . As with many geologic periods , the strata that define the epoch 's beginning and end are well identified , but the exact ages remain uncertain . The Paleocene Epoch brackets two major events in Earth 's history . It started with the mass extinction event at the end of the Cretaceous , known as the Cretaceous -- Paleogene ( K -- Pg ) boundary . This was a time marked by the demise of non-avian dinosaurs , giant marine reptiles and much other fauna and flora . The die-off of the dinosaurs left unfilled ecological niches worldwide . The Paleocene ended with the Paleocene -- Eocene Thermal Maximum , a geologically brief ( ~ 0.2 million year ) interval characterized by extreme changes in climate and carbon cycling . The name `` Paleocene '' comes from Ancient Greek... [1,000 / 1,126 chars] |
| In fact, the trend, while not statistically significant, is downward.” [70 chars] | The solar cycle or solar magnetic activity cycle is the nearly periodic 11-year change in the Sun 's activity ( including changes in the levels of solar radiation and ejection of solar material ) and appearance ( changes in the number and size of sunspots , flares , and other manifestations ) . They have been observed ( by changes in the sun 's appearance and by changes seen on Earth , such as auroras ) for centuries . The changes on the sun cause effects in space , in the atmosphere , and on Earth 's surface . While it is the dominant variable in solar activity , aperiodic fluctuations also occur . [610 chars] |
| Local and regional sea levels continue to exhibit typical natural variability—in some places rising and in others falling. [122 chars] | Mean sea level ( MSL ) ( abbreviated simply sea level ) is an average level of the surface of one or more of Earth 's oceans from which heights such as elevations may be measured . MSL is a type of vertical datuma standardised geodetic reference pointthat is used , for example , as a chart datum in cartography and marine navigation , or , in aviation , as the standard sea level at which atmospheric pressure is measured in order to calibrate altitude and , consequently , aircraft flight levels . A common and relatively straightforward mean sea-level standard is the midpoint between a mean low and mean high tide at a particular location . Sea levels can be affected by many factors and are known to have varied greatly over geological time scales . The careful measurement of variations in MSL can offer insights into ongoing climate change , and sea level rise has been widely quoted as evidence of ongoing global warming . The term above sea level generally refers to above mean sea level ( A... [1,000 / 1,011 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Project site | [Climate-FEVER project site](http://climatefever.ai) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| From 1970 until 1998 there was a warming period that raised temperatures by about 0.7 F. | A geologic or climate-history passage providing context for temperature periods and climate interpretation. |
| In fact, the trend, while not statistically significant, is downward. | A solar-cycle or climate-indicator passage discussing periodic activity and trend interpretation. |
| Local and regional sea levels continue to exhibit natural variability. | A mean sea-level passage explaining measurement and regional variation. |
| Climate scientists say Hurricane Harvey suggests global warming is making a bad situation worse. | A passage on the effects of global warming and climate-related environmental changes. |
| The CERN CLOUD experiment only tested part of the requirements needed to blame global warming on cosmic rays. | A passage on attribution of recent climate change and mechanisms responsible for global warming. |
