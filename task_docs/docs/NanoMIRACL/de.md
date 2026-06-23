# NanoMIRACL / de

## Overview

`NanoMIRACL / de` is the German split of the MIRACL-style multilingual
monolingual retrieval benchmark. German queries retrieve German Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 538 positive qrel rows. German is a high-resource language, but
this split remains challenging because many questions ask for a precise
relation or attribute of a familiar entity. Current diagnostics show dense
retrieval as the strongest top-rank profile, `reranking_hybrid` as the strongest
coverage profile, and BM25 as a useful lexical baseline that is vulnerable to
common German question templates and related-entity passages.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: German queries retrieve German
passages from German Wikipedia. The benchmark emphasizes native-language
queries, passage-level evidence, and human relevance judgments.

German has a notable role in MIRACL because it was one of the WSDM Cup surprise
languages. The MIRACL paper describes these languages as having development and
test data but no training split, so they probe retrieval under limited
language-specific supervision. For this Nano split, the relevant item is an
evidence-bearing German Wikipedia passage, not a direct answer string or a
translated English passage.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 538 positive qrel
rows. Positives per query average 2.69, with a minimum of 1, a median of 2, and
a maximum of 10. There are 142 multi-positive queries, representing 71.0 percent
of the split. Queries average 45.38 characters, while documents average 457.20
characters.

The examples are ordinary German fact questions, commonly using forms such as
`Wie`, `Wann`, `Welche`, `Was`, `Wo`, `Wer`, `Warum`, and `Wozu`. Topics include
pop music, public broadcasters, football clubs, castles, Indigenous peoples,
geography, government institutions, inventions, universities, films, sports,
software, and organizations. Many questions ask for an exact attribute: a chart
position, acronym expansion, headquarters, inventor, builder, province count,
founding date, or location.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5172, hit@10 = 0.8550, and recall@100 = 0.9126. BM25 is
useful because German questions often contain distinctive entity names,
abbreviations, locations, titles, and numeric clues that recur in relevant
Wikipedia passages.

The lexical profile is nevertheless well below dense retrieval at the top of
the ranking. German questions often share generic templates such as `Wer hat`,
`Was ist`, or `Wie viele`, and these common tokens can pull in unrelated
passages with similar question-like phrasing or broad topical overlap. BM25 can
also retrieve the right entity family while missing the passage that states the
requested relation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7389, hit@10 = 0.9550, and recall@100 = 0.9387.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
appears to connect German question intent to answer-bearing passages more
reliably than exact lexical matching alone.

This split rewards semantic relation matching. The model must distinguish a
passage that merely mentions `Neuschwanstein`, `FC Liverpool`, `ZDF`, or a
country name from the passage that answers who built it, where it is located,
what an acronym means, or how many units exist. Dense retrieval improves this
top-rank ordering, though its recall@100 remains below the hybrid candidate
set.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with one query using a rank-101 safeguard row. It achieves nDCG@10 =
0.6418, hit@10 = 0.9350, and recall@100 = 0.9796. Hybrid retrieval is not the
best top-10 ranking profile, but it is the strongest candidate-generation
profile by positive coverage.

This pattern is useful for reranking systems. BM25 contributes exact German
names, abbreviations, compounds, and rare surface forms, while dense retrieval
contributes semantic evidence matching. The combined candidate set preserves
more of the judged positive set for downstream reranking, even though dense
retrieval alone places the best evidence passages higher in the observed top-10
metrics.

### Metric Interpretation for Model Researchers

This task is heavily multi-positive: 71.0 percent of queries have more than one
positive passage. Hit@10 measures whether at least one relevant passage appears
near the top. nDCG@10 rewards ranking relevant passages high, and recall@100
measures how much of the judged positive set survives for reranking.

The metric pattern separates two retrieval qualities. Dense retrieval is the
current best top-rank answer-evidence model, while `reranking_hybrid` is the
best high-recall candidate source. BM25 is informative as a German lexical
anchor baseline, but strong models need to go beyond repeated entities and
question templates.

### Query and Relevance Type Tendencies

Queries are concise German information needs about entities, dates, counts,
locations, organizations, inventions, media works, institutions, and geographic
facts. German compounding and inflection matter, but the main difficulty is
often relational: which passage states the requested fact rather than simply
mentioning the topic.

Relevant documents are German Wikipedia passages with article-title context and
answer-bearing prose. The task rewards entity-aware semantic retrieval,
compound-sensitive lexical handling, and passage selection that recognizes
definition, inventor, builder, location, membership, count, or founding-date
relations.

### Representative Failure Modes

BM25 can be distracted by common German question templates. A query such as
`Wer hat Neuschwanstein gebaut?` can retrieve passages that share `Wer hat`
phrasing or broad cultural terms before the passage about Ludwig II. Similar
risks appear in invention questions such as `Wer hat das Mikroskop erfunden?`
or `Wer hat das Musical erfunden?`.

Count and list questions create another failure mode. A query about how many
provinces Turkey has may retrieve a passage that mentions the same number in a
different context before the direct list or country-structure passage. Dense
retrieval can fail in the opposite direction by choosing a semantically related
entity page that lacks the exact requested fact. Hybrid retrieval mitigates
missing positives but still needs reranking to choose the best evidence passage.

### Training Data That May Help

Because MIRACL German was introduced as a surprise language without an original
training split, useful training data should come from non-overlapping German
retrieval sources. Good candidates include German Wikipedia question-to-passage
pairs, German QA evidence retrieval datasets, German entity-attribute retrieval
supervision, and hard negatives from related German Wikipedia pages.

Synthetic data can help when it creates German Wikipedia-style passages with
titles, aliases, dates, locations, counts, abbreviations, organizations, and
explicit factual evidence. Generated questions should vary `Wer`, `Was`,
`Wann`, `Wo`, `Wie viele`, `Welche`, and `Wozu` forms while keeping the answer
grounded in the selected passage. Comparable evaluation should exclude MIRACL
German development or test data likely to overlap with the Nano split.

### Model Improvement Notes

Dense retrievers should improve German relation matching while preserving exact
entity names, abbreviations, compounds, and numeric clues. Sparse systems
benefit from compound-aware tokenization, normalization, and weighting that
reduces the influence of generic question stems. Rerankers should combine exact
entity evidence with semantic relation recognition.

For hybrid systems, `NanoMIRACL / de` supports a two-stage design: use
`reranking_hybrid` to retain a broad positive set, then apply a stronger
reranker to select the passage that actually answers the German question. The
dense baseline indicates that top-rank quality is achievable, while the hybrid
profile shows that lexical evidence still improves candidate coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Welche Mechanismen helfen Computern, menschliche Sprache zu verstehen? [70 chars] | Wissen Ein anderes Anwendungsfeld sind Dialogsysteme, die in der Mensch-Computer-Interaktion eingesetzt werden und die Kommunikation eines Menschen mit einem Computer mittels natürlicher Sprache ermög... [200 / 1,585 chars] |
| In welchem Jahr wurde TikTok gegründet? [39 chars] | TikTok "Douyin" wurde im September 2016 von Zhang Yiming, dem Gründer von ByteDance, ins Leben gerufen. Im Januar 2017 erhielt das Unternehmen mehrere Millionen Renminbi von der Toutiao-Gruppe, um die... [200 / 298 chars] |
| Was macht Südostasien attraktiv für Touristen? [46 chars] | Krabi (Stadt) Krabi ist eines der attraktivsten Reiseziele in Süd-Thailand. Die Andamanensee im Westen, an der zahllose natürliche Attraktionen liegen, ist beeindruckend. Dazu gehören die weißen Sands... [200 / 350 chars] |
| Was ist das kleinste Teilchen im Universum? [43 chars] | Elementarteilchen Elementarteilchen sind unteilbare subatomare Teilchen und die kleinsten bekannten Bausteine der Materie. Aus der Sicht der theoretischen Physik sind sie die geringsten Anregungsstufe... [200 / 731 chars] |
| Wann wurde die erste Brücke über eine Autobahn gebaut? [54 chars] | Brückenlandschaft Ruhraue Die erste Autobahnbrücke an dieser Stelle wurde im Rahmen des Reichsautobahnsprogrammes geplant und am 12. Dezember 1936 eröffnet, damals noch als einfache, vierstreifige Str... [200 / 287 chars] |

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
| A German question asking what helps computers understand human language. | A passage about dialog systems or natural-language human-computer interaction. |
| A question asking when TikTok was founded. | A passage about TikTok, Douyin, ByteDance, and the founding date. |
| A question asking what makes a travel region attractive. | A passage describing geographic or tourist features of the relevant place. |
| A question asking who built or invented a known object. | A passage about the person or historical development that states the relation. |
| A question asking how many provinces, members, or units exist. | A passage with the explicit count and the relevant administrative or institutional context. |
