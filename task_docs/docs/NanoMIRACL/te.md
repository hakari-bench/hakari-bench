# NanoMIRACL / te

## Overview

`NanoMIRACL / te` is the Telugu split of the MIRACL-style multilingual
monolingual retrieval benchmark. Telugu queries retrieve Telugu Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 211 positive qrel rows. Unlike many other MIRACL Nano splits, it
is almost single-positive, and many questions are entity- and census-oriented.
Current diagnostics show dense retrieval as the strongest top-rank profile by a
large margin, `reranking_hybrid` as the strongest recall profile, and BM25 as a
weaker lexical baseline for this highly repetitive passage setting.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Telugu queries retrieve Telugu
passages from Telugu Wikipedia. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Telugu is one of the MIRACL languages connected to the TyDi/Mr. TyDi lineage.
The MIRACL framing adds passage-level relevance judgments over a segmented
Wikipedia corpus. For this split, the relevant item is a Telugu passage that
contains answer evidence, not a translated English passage or a short answer.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 211 positive qrel
rows. Positives per query average 1.05, with a minimum of 1, a median of 1, and
a maximum of 3. There are only 9 multi-positive queries, representing 4.5
percent of the split. Queries average 38.41 characters, while documents average
409.03 characters.

The examples are strongly entity- and attribute-oriented. Many ask about 2011
census values, village area, male population, number of houses, pin codes,
birthplaces, founders, scientific names, religious sites, institutions, and
definitions. Telugu village pages often repeat similar census-style prose, so
the task requires exact entity disambiguation as well as attribute matching.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5292, hit@10 = 0.6400, and recall@100 = 0.8768. BM25 is
useful when the exact village name, entity name, or attribute phrase appears in
both query and passage. It can exploit repeated Telugu terms for area,
population, pin code, and scientific name.

The sparse profile is weak because many candidate passages are near-duplicates
in structure. Village pages can share the same census phrases, distances,
population formulas, caste-count language, and pin-code patterns. BM25 may rank
a passage with the right attribute words above the exact village or entity page.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.8720, hit@10 = 0.9150, and recall@100 = 0.9194.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
greatly improves top-rank ordering by connecting the query's entity and
attribute to the answer-bearing passage.

This is a clear dense-retrieval advantage. The model must distinguish whether a
question asks for area, population, male count, number of houses, pin code,
founder, birthplace, or scientific name, even when many passages share the same
template. Dense retrieval ranks the exact evidence much better than BM25.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with three queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.6953, hit@10 = 0.8650, and recall@100 = 0.9810. Hybrid retrieval is below
dense retrieval in top-rank quality, but it has the best positive coverage.

This means hybrid search is useful primarily as a candidate generator for this
Telugu split. BM25 contributes exact entity and attribute phrases, while dense
retrieval contributes semantic and structural matching. The hybrid candidate
pool retains more positives for reranking, but dense retrieval alone ranks the
top evidence more accurately.

### Metric Interpretation for Model Researchers

This task is close to single-positive: only 4.5 percent of queries have more
than one positive passage. Hit@10 measures whether the labeled passage appears
near the top. nDCG@10 is especially sensitive to rank position because most
queries have one relevant target. recall@100 measures whether the target
survives for reranking.

The Telugu pattern is diagnostic. Dense retrieval is the best top-rank model,
BM25 struggles with repeated templates, and `reranking_hybrid` is the best
coverage source. Researchers should evaluate exact entity disambiguation and
attribute binding, not only general semantic similarity.

### Query and Relevance Type Tendencies

Queries frequently ask about village statistics and local attributes: area,
population, male count, number of houses, pin code, census values, and
location. Other questions cover scientific names, religious or institutional
facts, authorship, birthplaces, founders, and historical definitions.

Relevant documents are Telugu Wikipedia passages with title context and
answer-bearing prose. The task rewards exact Telugu-script entity preservation,
template-aware passage selection, and relation matching between the query
attribute and the passage field.

### Representative Failure Modes

BM25 can retrieve the wrong village page because many passages share the same
`గ్రామ విస్తీర్ణం`, census, population, or pin-code wording. A pumpkin
scientific-name query can retrieve other plant pages with `శాస్త్రీయ నామం`
before the pumpkin passage. Pin-code questions can retrieve nearby or similarly
formatted village pages. Organization or authorship questions can retrieve
related cultural or institutional pages that share terms but lack the answer.

Dense retrieval can still miss an exact entity when similar village templates
are very close semantically. Hybrid retrieval improves recall but still requires
reranking to select the precise village or attribute-bearing passage.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Telugu training data,
Telugu Wikipedia question-to-passage retrieval pairs, Telugu open-domain QA
evidence retrieval datasets, and synthetic village-statistic retrieval pairs
from non-evaluation Telugu pages. Hard negatives should include near-duplicate
village pages that differ only by name, area, population, pin code, or census
line.

Synthetic data can help when it creates Telugu Wikipedia-style passages with
titles, aliases, census prose, areas, population counts, pin codes, founders,
birthplaces, scientific names, and institutional descriptions. Generated
questions should include `2011` census, village area, male count, number of
houses, pin code, who, where, and scientific-name forms with exact entity names.
Comparable evaluation should exclude upstream development/test data or other
MIRACL-derived examples likely to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their strong top-rank advantage while
improving coverage toward the hybrid profile. Sparse systems need better
Telugu tokenization and entity weighting for repeated census templates.
Rerankers should explicitly bind village name and requested attribute, rather
than rewarding shared boilerplate.

For hybrid systems, `NanoMIRACL / te` supports `reranking_hybrid` as a high-
recall candidate stage, followed by a reranker specialized for exact entity and
field matching. Dense retrieval sets a strong top-rank target for this split.

## Example Data

| Query | Positive document |
| --- | --- |
| కామేపల్లి గ్రామ విస్తీర్ణం ఎంత? [31 chars] | కామేపల్లి (ఖమ్మం జిల్లా) గ్రామ జనాభా: 2011 భారత జనగణన గణాంకాల ప్రకారం ఈ గ్రామం 1496 ఇళ్లతో, 5464 జనాభాతో 1380 హెక్టార్లలో విస్తరించి ఉంది. గ్రామంలో మగవారి సంఖ్య 2563, ఆడవారి సంఖ్య 2901. షెడ్యూల్డ్ కులాల సంఖ్య 1087 కాగా షెడ్యూల్డ్ తెగల సంఖ్య 2105. గ్రామం యొక్క జనగణన లొకేషన్ కోడ్ 579469.. పిన్ కోడ్: 507182. [307 chars] |
| ఫలక్‌నుమా ప్యాలెస్ ను ఎవరు నిర్మించారు? [39 chars] | ఫలక్‌నుమా ప్యాలెస్ ఫలక్ నూమా ప్యాలెస్ కు ఆంగ్లేయ ఆర్కిటెక్టర్ నిర్మాణాకృతినిచ్చారు. మార్చి3, 1884లో ఈ నిర్మాణానికి సర్ వికార్ శంకు స్థాపన చేయగా అన్ని హంగులతో నిర్మాణం పూర్తి కావడానికి తొమ్మిదేళ్లు పట్టింది. ఫలక్ నుమా ప్యాలెస్ లోని 93,971 చదరపు మీటర్ల విస్తీర్ణం గల మర్దనా భాగాన్ని ఇటలీ నుంచి తెప్పించిన ప్రత్యేకమైన పాలరాళ్లతో పరిచారు. తేలు ఆకృతిలో నిర్మించిన ఈ ప్యాలెస్ మధ్య భాగంలో ప్రధాన భవనం, వంటగది, గోల్ బంగ్లా, జెన్నా మహల్ తో పాటు దక్షిణ భాగంలో పట్టపు రాణులు, చెలికత్తెల కోసం క్వార్టర్లను నిర్మించారు. ఫలక్ నుమా ప్యాలెస్ మొత్తం అరుదైన ఇటాలియన్, టుడూర్ ఆర్కిటెక్చర్ కనిపిస్తుంది. ఇందులోని కిటికీలకు ఉపయోగించిన రంగు రంగుల అద్దాల పట్టకాల నుంచి వచ్చే కాంతి గదులకు ప్రత్యేక ఆకర్షణ కలిగిస్తాయి. 1897-98 వరకు సర్ వికార్ తన వ్యక్తిగత నివాసంగా ఫలక్ నుమా ప్యాలెస్ ను ఉపయోగించుకున్నాడు. ఆ తర్వాత దీని యాజమాన్య బాధ్యతలను హైదరాబాద్ రాజైన 6వ నిజాంకు అప్పగించారు. ఫలక్ నుమా ప్యాలెస్ చాలా ఖరీదైన కట్టడం. దీని కోసం చేసిన అప్పులు తీర్చేందుకు వికార్ కు చాలా కాలం పట్టిందట. ఆయ భార్య వికారుల్ ఉమ్రా ఇచ్చిన సలహా మేరకు... [1,000 / 1,238 chars] |
| మదర్ థెరీసా ఎప్పుడు మరణించింది? [31 chars] | మదర్ థెరీసా ఏప్రిల్ 1996,లో మదర్ థెరీసా క్రిందపడటం వలన ఆమె మెడ ఎముక విరిగింది.ఆగస్టులో ఆమె మలేరియాతో బాధ పడటంతో పాటు గుండె ఎడమభాగంలోని జఠరిక(గుండె) పనిచేయడం మానివేసింది.ఆమెకు గుండె శస్త్రచికిత్సజరిగింది, కానీ ఆమె ఆరోగ్యం క్షీణిస్తున్న విషయం వెల్లడైంది. తాను అనారోగ్యం పాలైనపుడు తన వైద్యశాలలలో ఏదో ఒక దానిలో చికిత్స పొందకుండా, కాలిఫోర్నియాలో అన్ని హంగులతో కూడిన వైద్యశాలను ఎంచుకొనడం వివాదాలకు దారితీసింది. మార్చి 13, 1997 న ఆమె మిషనరీస్ అఫ్ ఛారిటీ అధినేత పదవి నుండి వైదొలిగారు, 1997 సెప్టెంబర్ 5 న మరణించారు. [508 chars] |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984),
  2022.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/),
  2023.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus),
  source corpus dataset.
- [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | [https://aclanthology.org/2023.tacl-1.63/](https://aclanthology.org/2023.tacl-1.63/) |
| MIRACL GitHub repository |  | project repository | [https://github.com/project-miracl/miracl](https://github.com/project-miracl/miracl) |
| miracl/miracl-corpus |  | dataset card | [https://huggingface.co/datasets/miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Telugu question asking for a village's area. | A Telugu village passage with area and census prose. |
| A question asking for another village's extent or pin code. | A similarly structured village page with the exact village name. |
| A question asking for the scientific name of pumpkin. | A passage about pumpkin or gourd with the scientific name. |
| A question asking what the first war in India was. | A passage about the First War of Indian Independence. |
| A question asking a biographical family detail. | A passage about the person containing the requested relation. |
