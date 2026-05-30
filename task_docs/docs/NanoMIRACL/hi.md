# NanoMIRACL / hi

## Overview

`NanoMIRACL / hi` is the Hindi split of the MIRACL-style multilingual
monolingual retrieval benchmark. Hindi queries retrieve Hindi Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 410 positive qrel rows. Queries are relatively long and often
entity-heavy, with question intent expressed through forms such as `किस`,
`कौन`, `किसने`, `कितनी`, `कहाँ`, `कब`, and `क्या`. Current diagnostics show
dense retrieval as the strongest top-rank profile, `reranking_hybrid` as the
strongest recall profile, and BM25 as a weak lexical baseline on this split.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Hindi queries retrieve Hindi
passages from Hindi Wikipedia. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Hindi is one of the MIRACL languages created beyond the earlier Mr. TyDi/TyDi
QA sources. The split should therefore be read as MIRACL-style Hindi Wikipedia
retrieval, not as translated English retrieval. The relevant item is a Hindi
passage that contains answer evidence, not a short answer string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 410 positive qrel
rows. Positives per query average 2.05, with a minimum of 1, a median of 2, and
a maximum of 9. There are 105 multi-positive queries, representing 52.5 percent
of the split. Queries average 54.75 characters, while documents average 419.30
characters.

Observed queries often begin with topical entities such as `भारत`, `भारतीय`, or
`विश्व`, while the actual question relation appears later. Topics include Indian
administration, Pakistani constitutional history, dams, reefs, earthquakes,
Mysore wars, technical terminology, animal instruments, media institutions,
countries, languages, U.S. presidents, rural development, Jain history, and
legal or political procedures.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.3037, hit@10 = 0.5200, and recall@100 = 0.7049. BM25 is
substantially weaker here than on many other MIRACL Nano splits. It can still
help when distinctive Devanagari names, technical terms, or transliterated
entities appear, but lexical overlap alone misses many relevant passages.

The weak sparse profile reflects relation and normalization difficulties.
Hindi queries can be entity-first and longer, so repeated topical words do not
guarantee relevance. Morphology, postpositions, spelling variation, English
loanwords, and transliterated names can all affect matching. BM25 often finds a
related administrative, historical, or technical page but not the passage that
states the requested fact.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6847, hit@10 = 0.9100, and recall@100 = 0.9220.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
substantially improves over BM25 by matching the semantic relation expressed in
the Hindi question.

This is a central Hindi pattern. The model must connect a topic-heavy query to
evidence about who administers a territory, which river a dam is on, what a
technical term means, which treaty ended a war, or what an instrument is used
for. Dense retrieval better captures these relations and retrieves answer-
bearing passages even when exact surface overlap is weak.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with seven queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.5174, hit@10 = 0.8200, and recall@100 = 0.9634. Hybrid retrieval is below
dense retrieval at the top of the ranking, but it has the strongest positive
coverage.

This means hybrid search is primarily valuable as a candidate generator for
Hindi. BM25 contributes exact names, transliterated terms, and rare surface
forms, while dense retrieval contributes semantic relation matching. The hybrid
candidate set preserves more positives than dense retrieval alone, but it needs
a reranker to recover dense-level top-rank quality.

### Metric Interpretation for Model Researchers

This task is multi-positive for 52.5 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The Hindi metric pattern is sharp: BM25 is weak, dense retrieval is best for
top-rank evidence selection, and `reranking_hybrid` is best for coverage. A
Hindi retriever should therefore be judged both on semantic answer matching and
on whether it can preserve rare lexical anchors for downstream reranking.

### Query and Relevance Type Tendencies

Queries ask about administration, history, geography, science, religion, law,
sports, technology, definitions, and institutions. Many are not keyword queries:
they contain a topic, a relation, and sometimes numbers or administrative
phrases that must be interpreted together.

Relevant documents are Hindi Wikipedia passages with title context and
answer-bearing prose. The task rewards Devanagari handling, entity recognition,
transliteration robustness, and relation-sensitive passage retrieval. Topic
overlap is especially insufficient for administrative and historical questions.

### Representative Failure Modes

BM25 can retrieve broad government or ministry pages for administrative
questions while missing the passage that states the specific authority or role.
For a question about the treaty ending the Third Anglo-Mysore War, lexical
matching can retrieve Tipu Sultan and Mysore-war pages before the passage with
the relevant treaty context. Temperature and altitude questions can retrieve
passages containing temperature words but miss lapse-rate evidence. A question
about a Burdizzo instrument can retrieve survey or generic instrument pages
before the animal-castration passage.

Dense retrieval can still fail by selecting a semantically related Hindi
passage that lacks the exact requested attribute. Hybrid retrieval reduces
missing positives but still requires reranking to choose direct evidence.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Hindi training data, Hindi
Wikipedia question-to-passage retrieval pairs, Hindi open-domain QA evidence
retrieval datasets, and entity-attribute supervision for Indian administration,
history, geography, religion, law, science, and technology. Hard negatives
should include related Hindi Wikipedia passages around the same entity or
administrative topic.

Synthetic data can help when it creates Hindi Wikipedia-style passages with
titles, aliases, dates, places, administrative roles, measurements, technical
terms, and factual evidence. Generated questions should use varied `किस`,
`कौन`, `किसने`, `कितनी`, `कहाँ`, `कब`, `क्या`, and `किसके द्वारा` forms.
Comparable evaluation should exclude upstream development/test data or other
MIRACL-derived examples likely to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their strong Hindi semantic gains while
recovering more hybrid-style coverage. Sparse systems need better Hindi
tokenization, normalization, transliteration handling, and weighting of rare
entity terms against generic question material. Rerankers should explicitly
select passages that state the requested administrative, historical, or
technical relation.

For hybrid systems, `NanoMIRACL / hi` supports using `reranking_hybrid` as a
recall-oriented candidate stage, followed by a stronger reranker. Dense
retrieval sets the top-rank quality target; hybrid retrieval supplies broader
positive coverage.

## Example Data

Representative queries ask what kind of waves radar uses, on which date India's
Republic Day falls, who leads the Congress party, whether vehicle fuel
combustion pollutes air, or which factories in India were established by the
Portuguese. Positive documents are Hindi Wikipedia passages containing the
requested technical, date, leadership, pollution, or historical evidence.

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
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus |  | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Hindi question asking what kind of waves radar uses. | A passage defining radar and its use of microwaves. |
| A question asking when India's Republic Day occurs. | A passage about Republic Day and the date January 26. |
| A question asking who leads a political party. | A passage about the party and its prominent leaders. |
| A question asking whether petrol combustion pollutes air. | A passage about motor vehicles, combustion, and air pollution. |
| A question asking which Indian factories were established by the Portuguese. | A passage about European arrival in India and Portuguese trading posts. |
