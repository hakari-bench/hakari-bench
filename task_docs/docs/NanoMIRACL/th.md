# NanoMIRACL / th

## Overview

`NanoMIRACL / th` is the Thai split of the MIRACL-style multilingual
monolingual retrieval benchmark. Thai queries retrieve Thai Wikipedia passages,
not translated evidence. The Nano split has 200 queries, 10,000 documents, and
343 positive qrel rows. Questions ask for years, spouses, founders, places,
definitions, statement verification, and other factual attributes. Current
diagnostics show dense retrieval as the strongest nDCG@10 and hit@10 profile,
`reranking_hybrid` as the strongest recall profile, and BM25 as a strong but
less relation-aware lexical baseline.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Thai queries retrieve Thai
passages from Thai Wikipedia. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Thai is one of the MIRACL languages connected to the TyDi/Mr. TyDi lineage. The
MIRACL framing adds passage-level relevance judgments over a segmented Wikipedia
corpus. For this split, the relevant item is a Thai passage that contains the
requested evidence, not a translated English passage or a short answer.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 343 positive qrel
rows. Positives per query average 1.72, with a minimum of 1, a median of 1, and
a maximum of 7. There are 86 multi-positive queries, representing 43.0 percent
of the split. Queries average 43.59 characters, while documents average 409.88
characters.

The examples include Thai questions about media, sports, biology, history,
politics, technology, countries, religion, anatomical terms, cultural works, and
named people. Thai year expressions such as `พ.ศ.` appear often, and many
queries require binding a named entity to a specific attribute such as release
year, number of teams, anatomical location, birth date, relationship, country
area, first use, office holder, or place of death.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6229, hit@10 = 0.9000, and recall@100 = 0.9679. BM25 is
strong when exact Thai entity names, years, competition names, country names, or
technical terms appear in both query and passage. It also retains many positives
within the top-100 pool.

The sparse profile is limited by Thai word segmentation and passage selection.
Several candidates can share the same article family, competition name,
country, year, or technical phrase. BM25 can find the right topic but rank a
neighboring section above the passage that states the requested number, date,
relationship, or location.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.8101, hit@10 = 0.9500, and recall@100 = 0.9504.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
improves top-rank evidence selection by matching the question's semantic
relation rather than relying only on repeated Thai surface forms.

The tradeoff is that dense recall@100 is lower than BM25 and hybrid retrieval.
Dense retrieval is the best top-rank model, while lexical and hybrid signals are
still valuable for preserving a broader positive set for reranking.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with one query using a rank-101 safeguard row. It achieves nDCG@10 =
0.7296, hit@10 = 0.9300, and recall@100 = 0.9971. Hybrid retrieval is below
dense retrieval at top ranks but nearly complete in positive coverage.

This profile shows the complementary value of BM25 and dense retrieval. BM25
contributes exact Thai terms, years, and names, while dense retrieval
contributes relation-sensitive evidence matching. The combined pool is best for
candidate generation, especially when a reranker can choose the direct evidence
passage.

### Metric Interpretation for Model Researchers

This task is multi-positive for 43.0 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The Thai profile separates top-rank accuracy from coverage. Dense retrieval is
best at selecting answer-bearing passages near the top, while
`reranking_hybrid` is best at retaining positives. BM25 remains informative
because exact Thai names and year expressions are important anchors.

### Query and Relevance Type Tendencies

Queries ask about years, counts, locations, founders, spouses, definitions,
competitions, anatomical terms, political offices, countries, technologies, and
cultural works. Some questions are statement-like or yes/no-style rather than
simple wh-questions.

Relevant documents are Thai Wikipedia passages with title context and
answer-bearing prose. The task rewards Thai segmentation robustness, exact
entity handling, date normalization across Buddhist-era and Common Era mentions,
and passage-level relation selection inside same-topic articles.

### Representative Failure Modes

BM25 can retrieve the right broad article family but not the specific passage.
For a UEFA Europa League 2018-19 query, it can rank season or group-stage pages
above the qualifying/playoff passage that states the number of participating
clubs. A query about China's area can retrieve related administrative pages
before the country passage with the area statement. A stainless-steel first-use
question can retrieve other stainless-steel sections before the passage about
commercial adoption. Long royal biography questions can be distracted by
nearby sections from related articles.

Dense retrieval can fail when a semantically close Thai passage lacks the exact
attribute. Hybrid retrieval reduces missing positives but still depends on
reranking to choose the most direct evidence passage.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Thai training data, Thai
Wikipedia question-to-passage retrieval pairs, Thai open-domain QA evidence
retrieval datasets, and same-article Thai Wikipedia hard negatives. Training
should cover Thai dates, competition structure, offices, locations, definitions,
and statement-verification forms.

Synthetic data can help when it creates Thai Wikipedia-style passages with
titles, aliases, dates, locations, competitions, anatomical terms, cultural
works, and political offices. Generated questions should include who, when,
which year, how many, where, what-is, and yes/no statement forms with Buddhist-
era and Common Era date variants. Comparable evaluation should exclude upstream
development/test data or other MIRACL-derived examples likely to overlap with
this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their Thai top-rank advantage while improving
coverage toward the hybrid profile. Sparse systems benefit from Thai word
segmentation, better date/entity weighting, and ranking logic that distinguishes
same-article sections. Rerankers should prioritize the passage that states the
requested number, date, location, or relation.

For hybrid systems, `NanoMIRACL / th` supports using `reranking_hybrid` as a
high-recall candidate stage. Dense retrieval sets the top-rank target, while the
hybrid candidate set keeps more positives available for reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| ชาวนอร์มันหมายถึงอะไร? [22 chars] | นอร์มัน นอร์มัน () คือกลุ่มชนผู้ให้นามแก่ดินแดนนอร์ม็องดีซึ่งเป็นบริเวณทางตอนเหนือของฝรั่งเศส ชนนอร์มันสืบเชื้อสายมาจากไวกิงผู้ได้รับชัยชนะต่อผู้ตั้งถิ่นฐานอยู่แต่เดิมที่เป็นชนแฟรงค์ (Franks) และกอลล์-โรมัน (Gallo-Roman) ความเป็น “ชนนอร์มัน” เริ่มเป็นที่รู้จักกันเป็นครั้งแรกราวครึ่งแรกของคริสต์ศตวรรษที่ 10 และค่อยๆ วิวัฒนาการเรื่อยมาในคริสต์ศตวรรษต่อๆ มาจนกระทั่งสูญหายไปจากการเป็นกลุ่มชนที่เป็นเอกลักษณ์ของตนเองในต้นคริสต์ศตวรรษที่ 13 คำว่า “นอร์มัน” มาจากคำว่า “นอร์สเม็น” หรือ “นอร์ธเม็น” (Norsemen หรือ Northmen) ตามชื่อไวกิงจากสแกนดิเนเวียผู้ก่อตั้งนอร์ม็องดี หรือ “นอร์ธมานเนีย” เดิมในภาษาละติน [603 chars] |
| สัตว์ประจำชาติสหรัฐอเมริกาคืออะไร? [34 chars] | สหรัฐ นิเวศวิทยาของสหรัฐนั้นหลากหลายมาก (megadiverse) โดยมีพืชมีท่อลำเลียงประมาณ 17,000 ชนิดในสหรัฐแผ่นดินใหญ่และรัฐอะแลสกา และพบพืชดอกกว่า 1,800 ชนิดในรัฐฮาวาย ซึ่งมีจำนวนน้อยที่พบในแผ่นดินใหญ่ สหรัฐเป็นถิ่นที่อยู่ของสัตว์เลี้ยงลูกด้วยนม 428 ชนิด นก 784 ชนิด สัตว์เลื้อยคลาน 311 ชนิดและสัตว์สะเทินน้ำสะเทินบก 295 ชนิด มีการพบแมลงประมาณ 91,000 ชนิด อินทรีหัวขาวเป็นนกประจำชาติและสัตว์ประจำชาติของสหรัฐ และเป็นสัญลักษณ์ของประเทศเสมอมา [434 chars] |
| สไปรูไลนามีโปรตีนอยู่ราวเท่าไหร่? [33 chars] | สไปรูลินา (ผลิตภัณฑ์เสริมอาหาร) สไปรูไลนามีโปรตีนอยู่ราว 60% (51-71%) ในสไปรูไลนามีโปรตีนที่มีกรดอะมิโนจำเป็นทุกชนิด แม้ว่าจะมีปริมาณเมไทโอนีน ซีสเตอีนและไลซีนเมื่อเทียบกับโปรตีนที่ได้จากเนื้อสัตว์ ไข่และนม อย่างไรก็ตาม สไปรูไลนาเหนือกว่าโปรตีนพืชตัวอย่าง อย่างเช่นที่ได้จากพืชตระกูลถั่ว (legume) ในภาพรวม ขณะที่สไปรูไลนามักถูกโฆษณาว่าเป็นแหล่งโปรตีนที่ยอดเยี่ยม แต่มันก็ไม่ได้ดีไปกว่านมหรือเนื้อสัตว์ (เว้นเสียแต่มันมีโปรตีนที่มีกรดอะมิโนจำเป็นครบ) และเป็นโปรตีนที่ราคาต่อกรัมแพงกว่าโปรตีนแหล่งอื่นอย่างน้อย 30 เท่า [517 chars] |

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
| A Thai question asking what the Normans mean. | A passage defining the Normans and their origin. |
| A question asking what fluid fills the cochlea. | A passage about the cochlea and perilymph. |
| A question asking how much protein spirulina contains. | A passage about spirulina nutritional composition. |
| A question asking when a palace was built. | A passage about the palace, location, and construction context. |
| A question asking how many clubs competed in a football competition stage. | A passage about the competition qualifying and playoff structure. |
