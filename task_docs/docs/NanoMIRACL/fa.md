# NanoMIRACL / fa

## Overview

`NanoMIRACL / fa` is the Persian split of the MIRACL-style multilingual
monolingual retrieval benchmark. Persian queries retrieve Persian Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 427 positive qrel rows. The task combines compact Persian fact
questions, native script, entity-heavy topics, and passage-level evidence
selection. Current diagnostics show dense retrieval as the strongest nDCG@10
profile, `reranking_hybrid` as the strongest hit and recall profile, and BM25
as a useful lexical baseline with sensitivity to spelling, spacing, and
near-title ambiguity.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Persian queries retrieve Persian
passages from Persian Wikipedia. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Persian is one of the MIRACL languages created beyond the older Mr. TyDi/TyDi
QA sources. The task should therefore be read as MIRACL-style Persian Wikipedia
retrieval, not as translated English retrieval. The relevant item is a Persian
passage containing the requested evidence, not a direct answer string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 427 positive qrel
rows. Positives per query average 2.14, with a minimum of 1, a median of 2, and
a maximum of 8. There are 105 multi-positive queries, representing 52.5 percent
of the split. Queries average 39.99 characters, while documents average 310.75
characters.

The examples are compact Persian questions or entity-first information needs.
Common forms include `چه`, `کدام`, `چند`, `در چه سالی`, `در کجا`, `علت`, and
`چه کسی`. Topics include universities, government offices, religion,
infrastructure, wars, geography, sports, caves, lakes, calligraphy, political
leaders, tax exemptions, and definitions.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5788, hit@10 = 0.9100, and recall@100 = 0.9602. BM25 is
strong when the query contains distinctive Persian names, titles, places, or
historical terms. Exact matches for universities, wars, caves, government
ministries, and geographic entities often provide useful lexical anchors.

The sparse profile is limited by Persian script and passage disambiguation.
Spacing, half-spaces, affixes, Arabic/Persian letter variants, and compact forms
can affect token matching. BM25 can also prefer the more familiar article title
or near-name passage when the labeled positive is a different passage that
contains the requested relation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6476, hit@10 = 0.8750, and recall@100 = 0.9016.
Dense retrieval is the strongest observed profile by nDCG@10. It ranks the
evidence it finds better than BM25 by using semantic question-passage matching
for facts such as country, year, founder, location, number, reason, and office.

The tradeoff is coverage. Dense retrieval has lower hit@10 and recall@100 than
BM25 and hybrid retrieval, so it is less complete as a candidate generator. This
means the Persian split separates semantic ordering quality from the ability to
retain all relevant Persian passages in a top-100 pool.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with one query using a rank-101 safeguard row. It achieves nDCG@10 =
0.6334, hit@10 = 0.9350, and recall@100 = 0.9930. Hybrid retrieval is slightly
below dense retrieval by nDCG@10, but it has the best hit@10 and top-100
coverage.

This profile emulates the benefit of combining lexical and dense search. BM25
contributes exact Persian names, titles, measurements, and surface forms, while
dense retrieval contributes semantic matching for answer relations. The combined
candidate set is therefore a stronger input for reranking than either method
alone when coverage matters.

### Metric Interpretation for Model Researchers

This task is multi-positive for 52.5 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The observed pattern is balanced. Dense retrieval is best for top-rank quality,
BM25 is better for preserving positives, and `reranking_hybrid` gives the
strongest coverage and hit rate. Persian retrieval models should therefore be
evaluated both for relation-sensitive top ranking and for robust handling of
script-normalized lexical anchors.

### Query and Relevance Type Tendencies

Queries are short Persian information needs about entities, places, government
roles, years, causes, counts, definitions, and religious or historical facts.
Many begin with an entity rather than a question word, so the model must bind
the later question intent to the correct passage.

Relevant documents are Persian Wikipedia passages with title context and
answer-bearing prose. The task rewards script normalization, entity
disambiguation, and semantic passage selection. It also tests whether a model
can avoid treating the most obvious title match as relevant when another passage
contains the requested fact.

### Representative Failure Modes

BM25 can retrieve a near-title passage instead of the labeled evidence passage.
Questions about Nader Shah memorials, Lake Van or similar lake names, and
World War events can pull in close but non-answering pages. A question about
types of writing style can retrieve general scientific-writing or calligraphy
passages before the passage that lists literary styles.

Dense retrieval can fail by choosing a semantically related Persian passage that
lacks the exact requested attribute. Hybrid retrieval reduces missing positives,
but a downstream reranker still has to decide which candidate directly states
the answer relation.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Persian training data,
Persian Wikipedia question-to-passage retrieval pairs, Persian entity-attribute
QA evidence retrieval pairs, and hard negatives from related Persian Wikipedia
pages. Training should include spelling and spacing variants, near-title
distractors, and questions grounded in dates, places, offices, measurements,
definitions, and reasons.

Synthetic data can help when it creates Persian Wikipedia-style passages with
titles, aliases, dates, places, offices, measurements, definitions, and factual
evidence. Generated questions should use varied `چه`, `کدام`, `چند`, `در چه
سالی`, `در کجا`, `علت`, and `چه کسی` forms. Comparable evaluation should
exclude upstream development/test data or other MIRACL-derived examples likely
to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should improve Persian semantic relation matching while
recovering more of BM25's recall. Sparse systems benefit from Persian
normalization, half-space handling, affix-aware tokenization, and careful
weighting of entity names versus generic question words. Rerankers should
combine exact title/entity evidence with relation-level answer matching.

For hybrid systems, `NanoMIRACL / fa` supports using `reranking_hybrid` as a
high-coverage candidate stage. The dense baseline shows useful semantic ranking
strength, but the hybrid profile shows that lexical Persian evidence remains
important for robust candidate generation.

## Example Data

| Query | Positive document |
| --- | --- |
| اسرائیل با چه کشورهایی روابط دوستانه دارد؟ [42 chars] | وزارت امور خارجه اسرائیل پیش از پیروزی انقلاب ۱۳۵۷ و به قدرت رسیدن نظام جمهوری اسلامی، ایران با کشور اسرائیل روابط دوستانه و حسنه‌ای را داشت و ایران اولین کشور اسلامی در منطقه خاورمیانه بود که کشور اسرائیل را به رسمیت شناخت. در آن زمان دو کشور ایران و اسرائیل سفارتخانه‌هایی را در پایتخت دو کشور جهت تحکیم روابط برقرار کردند و روابط دوستانه ایران و اسرائیل تا به قدرت رسیدن روح الله خمینی در ایران ادامه داشت. [410 chars] |
| وزیر کنونی فرهنگ و ارشاد اسلامی ایران چه کسی است؟ [49 chars] | محمدمهدی اسماعیلی محمدمهدی اسماعیلی (متولد ۱۳۵۴ در کبودرآهنگ) سیاستمدار ایرانی و وزیر فرهنگ و ارشاد اسلامی است. او دانش‌آموخته دکتری علوم سیاسی از پژوهشگاه علوم انسانی و مطالعات فرهنگی و عضو هیأت علمی دانشگاه تهران است. تحصیلات حوزوی را نیز تا پایان دوره سطح ادامه داده است. وی همچنین در ۲۰ مرداد ۱۴۰۰ به عنوان وزیر فرهنگ و ارشاد اسلامی پیشنهادی دولت سیزدهم توسط سید ابراهیم رئیسی به مجلس معرفی شد. [399 chars] |
| مثلث برمودا در کجا قرار دارد؟ [29 chars] | مثلث برمودا مثلث برمودا ، همچنین به عنوان مثلث شیطان شناخته می‌شود. منطقه‌ای است در ناحیه غربی اقیانوس اطلس شمالی که گفته می‌شود تعدادی هواپیما و کشتی تحت شرایط مرموز در آن ناپدید شده‌اند. [189 chars] |

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
| A Persian question asking which countries had friendly relations with Israel. | A passage about Israeli foreign relations and recognition in the region. |
| A question asking who holds an Iranian government office. | A biographical or ministry-related passage naming the office holder. |
| A question asking where the Bermuda Triangle is located. | A passage describing the region in the western North Atlantic. |
| A question asking which city is the capital of Nova Scotia. | A passage about Nova Scotia and Halifax. |
| A question asking which genus a plant or fossil plant belongs to. | A passage defining the genus and its plant characteristics. |
