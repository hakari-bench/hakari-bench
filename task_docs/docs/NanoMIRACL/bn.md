# NanoMIRACL / bn

## Overview

`NanoMIRACL / bn` is the Bengali split of the MIRACL-style multilingual
monolingual retrieval benchmark. Bengali queries retrieve Bengali Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 407 positive qrel rows. More than half of the queries have
multiple positives, so the task measures retrieval of a small answer-bearing
passage set rather than a single canonical passage. Current diagnostics show
dense retrieval as the strongest top-rank profile, `reranking_hybrid` as the
strongest recall profile, and BM25 as a useful but more brittle Bengali lexical
baseline.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark across many
languages. Its design is monolingual: Bengali queries retrieve Bengali passages
from Bengali Wikipedia. The benchmark emphasizes native-language queries,
Wikipedia passage evidence, and manual relevance judgments.

For Bengali, this means the model must handle native Bengali question wording,
named entities, inflected forms, compound expressions, and encyclopedic passage
structure. The retrieval unit is a passage rather than a full article, so a
system must choose the passage that contains the requested definition, count,
date, location, person relation, country fact, or other answer evidence.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 407 positive qrel
rows. Positives per query average 2.04, with a minimum of 1, a median of 2, and
a maximum of 8. There are 110 multi-positive queries, representing 55.0 percent
of the split. Queries average 47.23 characters, while documents average 446.23
characters.

The examples are Bengali fact questions, often entity-first rather than
question-word-first. Many queries introduce the topic or entity and then ask
for `কী`, `কোথায়`, `কত`, `কোন`, or `কবে`. Observed topics include religious
concepts, Bangladeshi and Indian public figures, rivers, prisons, country
statistics, software support, literary works, films, sports organizations, and
historical entities.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5033, hit@10 = 0.7800, and recall@100 = 0.9582. BM25 is
useful because many Bengali queries contain distinctive names, titles,
locations, or rare terms that also appear in relevant Wikipedia passages.
Examples include entity names, river names, book or film titles, and software
or organization names.

The sparse profile is substantially weaker than dense retrieval at the top of
the ranking. A common difficulty is entity-neighbor confusion: a query may
contain a person, place, or concept name that appears in many related passages,
but only one passage states the requested attribute. BM25 can also over-rank a
specific article about a related subtopic when the correct answer requires a
broader passage, such as a general article passage containing a count or
definition.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7661, hit@10 = 0.9450, and recall@100 = 0.9484.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
appears to handle Bengali question intent more effectively than BM25,
especially when the wording of the passage does not exactly repeat the query.

This is an important Bengali MIRACL pattern. Many questions are short but
relation-heavy: they ask for an attribute of an entity, not just any passage
that mentions the entity. Dense retrieval helps connect the semantic intent of
the question to answer-bearing passages about locations, dates, counts, roles,
definitions, or biographical facts. Its recall@100 is slightly lower than BM25
and hybrid retrieval, so the main strength is top-rank ordering rather than
complete positive-set coverage.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.6537, hit@10 = 0.9350,
and recall@100 = 0.9975. Hybrid retrieval is not the best top-10 ranking
profile, but it is the strongest candidate-generation profile by recall@100.

This profile emulates the benefit of combining lexical and dense retrieval.
BM25 contributes exact Bengali names and rare surface terms, while dense
retrieval contributes semantic matching for answer relations. The combined
candidate set preserves almost all judged positives for downstream reranking,
but dense retrieval alone ranks the best evidence passages higher in the
observed top-10 metrics.

### Metric Interpretation for Model Researchers

This task is multi-positive for more than half of the queries. Hit@10 measures
whether at least one relevant passage appears near the top. nDCG@10 rewards
placing relevant passages high, and recall@100 measures how much of the judged
positive set remains available for reranking.

The metric pattern is therefore diagnostic. Dense retrieval is currently best
for top-rank quality, `reranking_hybrid` is best for positive coverage, and
BM25 remains useful for exact Bengali lexical anchors. A strong Bengali retriever
should ideally combine dense semantic intent matching with preservation of rare
names, titles, and numeric or location-bearing passages.

### Query and Relevance Type Tendencies

Queries tend to be compact Bengali information needs about people, places,
religion, history, geography, organizations, software, and cultural works.
They often place the entity before the interrogative expression, so models must
parse the relation requested by the later part of the question.

Relevant documents are Bengali Wikipedia passages with article-title context
and answer-bearing prose. The task rewards systems that can distinguish a
passage that merely mentions the entity from a passage that states the queried
attribute, such as a birthplace, father name, location, number, definition,
religious classification, or historical date.

### Representative Failure Modes

BM25 can retrieve the wrong member of an entity family when the surface form is
shared by several passages. For example, a question about the father of a person
can retrieve passages about other people with overlapping names. A question
about the location of Lalon's akhra can retrieve passages about related singers,
films, or cultural works before the location-bearing passage. A question about
the number of suras in the Qur'an can retrieve individual sura pages above a
general Qur'an passage.

Dense retrieval can fail by choosing a semantically related passage that lacks
the exact requested attribute. Hybrid retrieval reduces missing positives but
still depends on a reranker to choose the passage with the best answer evidence.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Bengali training data,
native Bengali Wikipedia question-to-passage pairs, Bengali entity-attribute QA
evidence retrieval, and hard negatives from related Bengali Wikipedia pages.
Synthetic data can also help when it produces Bengali Wikipedia-style passages
and fact questions with both topic-first and question-word-first forms.

Comparable evaluation should avoid upstream development or test data, or other
MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions
and passages.

### Model Improvement Notes

Dense retrievers should improve Bengali relation matching while preserving exact
entity, title, and numeric signals. Sparse systems benefit from better Bengali
tokenization and normalization, especially for compound forms and variant
surface expressions. Rerankers should explicitly combine exact-entity evidence
with semantic answer relation matching.

For hybrid systems, `NanoMIRACL / bn` supports using `reranking_hybrid` as a
high-recall candidate stage followed by a stronger reranker. The dense baseline
shows that Bengali semantic matching can be very effective at top ranks, while
the hybrid profile shows that lexical evidence remains important for complete
candidate coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| শ্রীনিবাস রামানুজনের বাবার নাম কি ছিল ? [39 chars] | শ্রীনিবাস রামানুজন রামানুজন ১৮৮৭ খ্রিস্টাব্দের ২২ ডিসেম্বর প্রাচীন ভারতের মাদ্রাজ প্রদেশের তাঞ্জোর জেলার ইরেভদ শহরের এক দরিদ্র ব্রাহ্মণ পরিবারে জন্মগ্রহণ করেন। তাঁর পিতা "কে শ্রীনিবাস ইয়েঙ্গার" ছিলেন... [200 / 589 chars] |
| জে কে রাউলিং রচিত হ্যারি পটার উপন্যাসের প্রকাশক কে ? [52 chars] | হ্যারি পটার এই বইয়ের সাফল্য রাউলিংকে ইতিহাসে সবচেয়ে বেশী উপার্জন করা লেখকের তালিকায় শীর্ষস্থান দিয়েছে। বইগুলোর ইংরেজি সংস্করণণ প্রকাশ করে ব্লুমসবারি যুক্তরাজ্যে, স্কলাস্টিক প্রেস যুক্তরাষ্ট্রে, অ্... [200 / 256 chars] |
| খেজুর গাছে খেজুর ফল আসতে কতদিন সময় লাগে ? [41 chars] | খেজুর গাছে ফল উৎপাদনের জন্য সচরাচর ৪ থেকে ৮ বছর পর্যন্ত অপেক্ষা করতে হয়। তবে বাণিজ্যিকভাবে ফসল উৎপাদন উপযোগী খেজুর গাছে ফল আসতে ৭ থেকে ১০ বছর সময় লেগে যায়। পূর্ণাঙ্গ খেজুর গাছে প্রতি মৌসুমে গড়ে ৮০... [200 / 417 chars] |
| ওড়িশার কোন শহরে জগন্নাথের প্রধান মন্দিরটি অবস্থিত ? [51 chars] | জগন্নাথ জগন্নাথের মূর্তি সাধারণত কাঠে তৈরি করা হয়। এই মূর্তির চোখদুটি বড়ো বড়ো ও গোলাকার। হাত অসম্পূর্ণ। মূর্তিতে কোনো পা দেখা যায় না। জগন্নাথের পূজাপদ্ধতিও অন্যান্য হিন্দু দেবতাদের পূজাপদ্ধতির চেয... [200 / 310 chars] |
| সাদ্দাম হোসেন আবদুল মাজিদ আল তিকরিতি কবে নিহত হন ? [50 chars] | সাদ্দাম হুসাইন প্রথমে সাদ্দাম হোসেন জেনারেল আহমেদ হাসান আল বকরের উপ-রাষ্ট্রপতি ছিলেন। সেই সময় সাদ্দাম দৃঃঢ় ভাবে সরকার ও সামরিক বাহিনীর মধ্যকার বিরোধের অবসান ঘটান। এই উদ্দেশ্যে তিনি নিরাপত্তা বাহিনী... [200 / 1,237 chars] |

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
| A Bengali question asking for a person's father name. | A Bengali Wikipedia biographical passage with the requested family relation. |
| A question asking where Lalon's akhra was located. | A passage about Lalon, his akhra, and the relevant place. |
| A question asking how many suras the Qur'an contains. | A general passage about the Qur'an and its structure. |
| A question asking for a river, country, or institution attribute. | A passage with the requested geographic or institutional fact. |
| A question about a Bengali literary work, film, software product, or sports body. | A passage from the relevant Bengali Wikipedia article containing answer evidence. |
