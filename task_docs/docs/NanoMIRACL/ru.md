# NanoMIRACL / ru

## Overview

`NanoMIRACL / ru` is the Russian split of the MIRACL-style multilingual
monolingual retrieval benchmark. Russian queries retrieve Russian Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 555 positive qrel rows. The task focuses on Russian fact
questions about history, geography, rulers, law, technology, religion,
biography, infrastructure, and definitions. Current diagnostics show dense
retrieval as the strongest top-rank profile, `reranking_hybrid` as the strongest
recall profile, and BM25 as a useful but lower-ranking lexical baseline.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Russian queries retrieve Russian
passages from Russian Wikipedia. The benchmark emphasizes natural questions,
passage-level evidence, and human relevance judgments.

Russian is one of the MIRACL languages connected to the TyDi/Mr. TyDi lineage.
The MIRACL framing adds dense passage-level judgments over a segmented
Wikipedia corpus. For this split, the relevant item is a Russian passage that
contains answer evidence, not a translated English passage or short answer.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 555 positive qrel
rows. Positives per query average 2.78, with a minimum of 1, a median of 2, and
a maximum of 9. There are 134 multi-positive queries, representing 67.0 percent
of the split. Queries average 45.54 characters, while documents average 423.34
characters.

The examples are Russian fact questions using forms such as `Когда`, `Кто`,
`Где`, `Сколько`, `Какой`, `Какая`, `Что`, `В каком году`, and `При каком`.
Topics include Moldavian religious history, spaceflight, the Colosseum,
Khrushchevka housing, Sapsan trains, capital punishment, Olga of Kiev, Anna
Ioannovna, Cappadocia, Soviet tanks, Herod the Great, Istanbul, coming out,
Kaluga rivers, Kadyrov, women's suffrage, and Marilyn Monroe.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5887, hit@10 = 0.8650, and recall@100 = 0.9333. BM25 is
useful when a query contains distinctive Russian names, places, legal terms,
train names, rulers, or historical events. Exact lexical anchors often retrieve
the right topical neighborhood.

The limitation is relation-aware ranking. Russian inflection and long noun
phrases can separate query and passage forms, while near-topic pages share many
surface terms. BM25 can retrieve passages about a related country, law, ruler,
or event before the passage that states the requested date, name, legal status,
or historical relation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7693, hit@10 = 0.9250, and recall@100 = 0.9495.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10. It
improves top-rank evidence selection by matching the semantic relation asked in
the Russian question.

Dense retrieval is also slightly stronger than BM25 by recall@100, but it still
falls below the hybrid candidate set. This means it is the best single retrieval
profile for top evidence ranking, while hybrid retrieval remains more complete
for downstream reranking.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with three queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.6816, hit@10 = 0.9100, and recall@100 = 0.9928. Hybrid retrieval is not the
best top-10 ranking profile, but it has the strongest positive coverage.

This profile shows that Russian retrieval benefits from combining lexical and
dense signals. BM25 contributes exact names, dates, legal terms, and event
surface forms, while dense retrieval contributes relation-sensitive evidence
matching. The combined pool is a better candidate generator than either
individual method, even though dense retrieval ranks the top evidence more
strongly.

### Metric Interpretation for Model Researchers

This task is multi-positive for 67.0 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The Russian pattern separates semantic ranking from candidate retention. Dense
retrieval is the best top-rank model, while `reranking_hybrid` is the best
coverage source. BM25 remains valuable for exact lexical evidence, but by
itself it under-ranks many answer-bearing passages.

### Query and Relevance Type Tendencies

Queries are Russian information needs about dates, rulers, laws, places,
religious history, institutions, technology, and biographical facts. Many ask
for a precise temporal or legal relation, such as when an event occurred, what
name was used, who held an office, or where something was built.

Relevant documents are Russian Wikipedia passages with title context and
answer-bearing prose. The task rewards inflection-aware matching, named-entity
recognition, and passage selection that distinguishes direct evidence from
near-topic material.

### Representative Failure Modes

BM25 can retrieve related international or historical pages that share terms but
answer a different question. A query about when capital punishment was abolished
in the Russian Federation can retrieve pages about capital punishment in Norway
or Germany before the Russian legal passage. A question about Olga of Kiev's
baptismal name can retrieve Byzantine or church-history pages before the Olga
passage. A question about when Constantinople became Istanbul can retrieve
Mehmed II or Istanbul-history passages before the passage about the name. A
question about women's suffrage in Russia can retrieve generic suffrage pages
or other countries before the Russia-specific claim.

Dense retrieval can fail by selecting a semantically plausible passage that
lacks the exact date or legal relation. Hybrid retrieval reduces missing
positives but still needs reranking for direct evidence selection.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Russian training data,
Russian Wikipedia question-to-passage retrieval pairs, Russian open-domain QA
evidence retrieval datasets, and entity-attribute supervision for rulers,
places, dates, laws, historical events, and definitions. Hard negatives should
include same-country, same-ruler, same-law, and same-event distractors.

Synthetic data can help when it creates Russian Wikipedia-style passages with
titles, aliases, dates, offices, laws, locations, definitions, and factual
evidence. Generated questions should use varied `Когда`, `Кто`, `Где`,
`Сколько`, `Какой`, `Какая`, `Что`, `В каком году`, and `При каком` forms with
realistic inflection. Comparable evaluation should exclude upstream
development/test data or other MIRACL-derived examples likely to overlap with
this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their strong Russian top-rank quality while
improving recall toward the hybrid profile. Sparse systems benefit from Russian
morphology and inflection handling, plus better weighting of exact names versus
generic historical or legal terms. Rerankers should prioritize passages that
state the requested date, role, law, or name over merely related articles.

For hybrid systems, `NanoMIRACL / ru` supports `reranking_hybrid` as a
high-recall candidate stage followed by a stronger semantic reranker. Dense
retrieval sets the top-rank target; hybrid retrieval supplies broader positive
coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| В честь кого назван ЭВС «Сапсан»? [33 chars] | Сапсан (электропоезд) ЭВС «Сапсан» ("Velaro RUS") — высокоскоростные электропоезда из семейства электропоездов Velaro производства компании Siemens, приобретённые ОАО «РЖД» для эксплуатации на российских скоростных железных дорогах. Брендовое название получили в честь сокола-сапсана "(Falco peregrinus)". Электропоезда серии ЭВС1 — постоянного тока, ЭВС2 — двойного питания. Разработаны компанией Siemens специально для России. [429 chars] |
| Когда Тимофе́й Па́влович Мозго́в стал игроком команды НБА «Орландо Мэджик»? [75 chars] | Мозгов, Тимофей Павлович Тимофе́й Па́влович Мозго́в (16 июля 1986, Ленинград) — российский профессиональный баскетболист, выступающий за команду НБА «Орландо Мэджик». Играет на позиции центрового. Первые шаги в баскетболе Мозгов сделал в Санкт-Петербурге, затем в связи с переездом семьи продолжил заниматься баскетболом на юге России. Первым профессиональным клубом Тимофея был подмосковный «Химки». В 2010 году начал свою карьеру в НБА. В сезоне 2015/2016 в составе «Кливленд Кавальерс», вместе с одноклубником Александром Кауном, стал первым россиянином — чемпионом НБА. [574 chars] |
| Вавилон был центром держави Александра Македонского? [52 chars] | История Вавилона В октябре 331 г до н. э. Александр Македонский торжественно вступил в Вавилон, принёс жертву Белу и был провозглашён "«царём Вавилона и четырёх сторон света»". Македонское войско пребывало в городе около месяца, после чего продолжило продвижение на восток. Александр распорядился начать работы по восстановлению местных храмов; в частности, было принято решение о реставрации Эсагилы. По приказу царя, верхняя часть зиккурата Этеменанки были снесена, и легендарная башня начала перестраиваться. Стремясь подчеркнуть особую роль города, царь разрешил чеканить здесь серебряную монету. Мазей сохранил должность сатрапа; после его смерти в 328 г. до н. э. сатрапом стал Стамен (Дитамен). Окончательно разгромив Персидскую державу и подчинив ахеменидские владения в Средней Азии, македоняне совершили поход в Северо-Восточную Индию; в 323 г. до н. э. Александр вернулся в Вавилон, который он решил сделать своей столицей. С целью подготовки кампании по завоеванию Аравии, возле города бы... [1,000 / 1,161 chars] |

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
| A Russian question asking whom the Sapsan train is named after. | A passage about the Sapsan electric train and its naming. |
| A question asking when a basketball player joined a team. | A biographical passage about the player and the team. |
| A question asking whether Babylon was central to Alexander's empire. | A passage about Babylon and Alexander's entry into the city. |
| A question asking how Nicholas II died. | A passage about Nicholas II, abdication, arrest, and execution context. |
| A question asking where the first brick church was built. | A passage about the settlement or church construction history. |
