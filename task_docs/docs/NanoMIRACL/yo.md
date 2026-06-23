# NanoMIRACL / yo

## Overview

`NanoMIRACL / yo` is the Yoruba-centered split of the MIRACL-style retrieval
benchmark. It is intended as same-language Yoruba Wikipedia passage retrieval,
but repository metadata labels the split as multilingual and notes Yoruba,
English, and Swahili signals. The Nano split has 119 queries, 10,000 documents,
and 144 positive qrel rows. It is small, mostly single-positive, and contains
orthographic variation such as diacritic-rich and plain forms. Current
diagnostics show dense retrieval as the strongest top-rank profile,
`reranking_hybrid` as the strongest recall profile, and BM25 as a useful but
template-sensitive lexical baseline.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual for each language: Yoruba queries
retrieve Yoruba passages. The benchmark emphasizes native-language questions,
passage-level evidence, and human relevance judgments.

Yoruba has a special MIRACL role as a WSDM Cup surprise language with
development and test data but no original training split. This matters for
research use: Yoruba results should be interpreted as retrieval under limited
language-specific supervision. The relevant item is a passage containing the
answer evidence, not a short answer string.

### Observed Data Profile

The Nano split contains 119 queries, 10,000 documents, and 144 positive qrel
rows. Positives per query average 1.21, with a minimum of 1, a median of 1, and
a maximum of 4. There are 18 multi-positive queries, representing 15.13 percent
of the split. Queries average 37.69 characters, while documents average 176.69
characters.

The examples are short Yoruba factual questions with forms such as `Ki ni`,
`Kí ni`, `Ta ni`, `Ilu wo`, `Orile ede wo`, `Ọmọ orile ede wo`, `odun wo`,
`Oṣù wo`, and `nibo`. The data includes diacritic variation, English names,
country names, code-mixed text, and plain ASCII-like spellings. Topics include
countries, capitals, years, Nigerian history, people, food, states,
institutions, biographies, and cultural topics.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5816, hit@10 = 0.8151, and recall@100 = 0.9167. BM25 works
when exact entity names, country names, capital names, or short factual phrases
match between query and passage.

The sparse profile is limited by template-like wording and orthographic
variation. Many questions share forms such as `oluilu orile-ede`, `Omo orile
ede`, or `Orile ede wo`, so lexical matching can retrieve a page with the same
question pattern but the wrong entity. Diacritic differences and code-mixed
English names add another source of mismatch.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.8416, hit@10 = 0.9496, and recall@100 = 0.9653.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
substantially improves over BM25 by matching the entity-relation intent of short
Yoruba questions.

This is especially important because many queries are formulaic. Dense retrieval
helps distinguish whether the question asks for a capital, country, nationality,
year, month, school, or definition, rather than only matching the shared Yoruba
template.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.7651, hit@10 = 0.9412,
and recall@100 = 1.0000. Hybrid retrieval is below dense retrieval by top-rank
quality, but it preserves every judged positive in the observed top-100
candidate set.

This profile makes hybrid search valuable for Yoruba candidate generation. BM25
contributes exact titles, names, and country strings, while dense retrieval
contributes semantic relation matching. The combined candidate pool is ideal for
reranking, especially in a low-resource split where exact surface evidence
should not be discarded.

### Metric Interpretation for Model Researchers

This task is mostly single-positive: only 15.13 percent of queries have more
than one positive passage. Hit@10 measures whether the relevant passage appears
near the top. nDCG@10 is sensitive to exact rank because most queries have one
main target. recall@100 measures whether that target survives for reranking.

The Yoruba pattern is clear: dense retrieval is best for direct top-rank
ranking, while `reranking_hybrid` is best for full candidate coverage. BM25 is
not enough by itself, but it supplies useful lexical anchors for names,
countries, and capitals.

### Query and Relevance Type Tendencies

Queries ask about capitals, countries, years, nationalities, institutions,
historical events, food, biographies, and cultural facts. Many are short and
template-like, so the model must identify the entity and requested attribute
together.

Relevant documents are Yoruba-centered Wikipedia passages with title context and
answer-bearing prose. The task rewards diacritic robustness, entity matching,
code-mixed name handling, and relation selection among template-like
distractors.

### Representative Failure Modes

BM25 can retrieve other capital pages before Port-au-Prince for a question about
Haiti's capital because the shared `oluilu orile-ede` pattern dominates. A
question asking Kamaru Usman's nationality can retrieve pages about other
Nigerian people. A question asking which country Ghadames is in can retrieve
generic country or capital pages. A Christmas month query can retrieve passages
with month names in unrelated contexts.

Dense retrieval can still miss exact low-resource entities or overgeneralize to
a semantically related page. Hybrid retrieval reduces missing positives but
still requires reranking when several template-matched passages are present.

### Training Data That May Help

Yoruba MIRACL has no original training split. Useful training data should come
from non-overlapping external or synthetic sources, such as Yoruba Wikipedia
question-to-passage pairs from non-evaluation pages, Yoruba open-domain QA
evidence retrieval datasets, Nigerian geography and biography retrieval data
with Yoruba evidence passages, and multilingual African-language retrieval data
with Yoruba evidence passages.

Synthetic data can help when it creates Yoruba Wikipedia-style passages with
titles, capitals, countries, years, biographies, institutions, food
descriptions, and Nigerian history facts. Generated questions should use `Ki
ni`, `Ta ni`, `Ilu wo`, `Orile ede wo`, `Omo orile ede wo`, `odun wo`, `Osu
wo`, and `nibo` forms with both diacritic-rich and plain variants. Comparable
evaluation must avoid NanoMIRACL evaluation queries and positive passages.

### Model Improvement Notes

Dense retrievers should preserve strong top-rank semantic matching while
improving exact low-resource entity handling. Sparse systems benefit from
diacritic normalization, robust tokenization, and better weighting of entity
names relative to generic templates. Rerankers should choose the passage that
answers the exact capital, country, year, nationality, or institution relation.

For hybrid systems, `NanoMIRACL / yo` supports `reranking_hybrid` as a complete
coverage candidate stage. Dense retrieval sets the top-rank quality target;
hybrid retrieval keeps all judged positives available for reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| ilé iṣẹ iroyin wo ni Eugenia Abu bá ṣiṣe? [41 chars] | Eugenia Abu Eugenia Abu (bíi ni ọjọ́ mọ́kàndinlógún oṣù kẹwàá ọdún 1961) jẹ́ oniroyin, agbóhùnsáfẹ́fẹ́, akọ̀wé àti akéwì. Òun ni atọkun ètò ìròyìn tẹ́lẹ̀ fún Nigerian Television Authority (NTA) . Ó ṣe atọkun ètò lórí NTA fún ọdún mẹ́tàdínlọgbọn. [246 chars] |
| Awon orile ede wo lo yika Austria? [34 chars] | Austríà Austríà ( tabi ; ), lonibise bi Orileominira ile Austria (German: "Republik Österreich"), je orile-ede atimo ile to ni awon eniyan bi egbegberun 8.8 to wa ni Aringbongan Europe. O ni bode mo Orileominira Tseki ati Jemani ni ariawa, Slofakia ati Hungari ni ilaorun, Slofenia ati Italia ni gusu, ati Switsalandi ati Likstenstein ni iwoorun. Gbogbo agbegbe ile Austríà je be sini ojuojo ibe je onitutu ati alpini. Ori ile Austríà je oloke gan nitori pe awon Alpi po nibe; 32% ibe nikan ni won wa ni abe , be sin oke re togajulo je . Opo awon iyeolubugbe unso ede Jemani, to tun je ede onibise orile-ede ohun. Awon ede ibile onibise miran tun ni ede Kroatia, Hungari ati Slofenia. [685 chars] |
| ẹgbẹ wo ni Huey Newton da silẹ? [31 chars] | Huey P. Newton Huey Percy Newton (February 17, 1942 – August 22, 1989) je omo ile Amerika. Newton je oludasile ati olori egbe oselu Black Panther Party. [153 chars] |

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
| A Yoruba question asking which news organization Eugenia Abu worked with. | A biographical passage about Eugenia Abu and Nigerian Television Authority. |
| A question asking which countries border Austria. | A passage about Austria and neighboring countries. |
| A question asking which group Huey Newton founded. | A passage about Huey P. Newton and the Black Panther Party. |
| A question asking what year Stella Obasanjo died. | A biographical passage with her death date. |
| A question asking what Botswana was called before its name changed. | A passage about Botswana history and earlier naming. |
