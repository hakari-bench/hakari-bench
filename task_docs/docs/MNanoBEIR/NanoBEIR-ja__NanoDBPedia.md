# MNanoBEIR / NanoBEIR-ja / NanoDBPedia

## Overview

`NanoBEIR-ja__NanoDBPedia` is the Japanese NanoBEIR version of DBpedia-Entity,
an entity retrieval benchmark. The task uses Japanese translated entity-style
queries and asks a retriever to rank Japanese translated DBpedia entity
descriptions. The Nano split contains 50 queries, 6,045 documents, and 1,158
positive qrels. It is strongly multi-positive, with 23.16 positives per query
on average and 48 of 50 queries having more than one positive. This makes it a
short-query entity search task where exact names are useful, but category-level
and description-level matching are also important.

## Details

### What the Original Data Measures

[DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751) evaluates entity
search over DBpedia descriptions. BEIR includes it as an entity retrieval task,
and this Japanese NanoBEIR version evaluates the same setting through translated
queries and translated entity descriptions. Queries may contain an exact entity
name, a partial entity reference, or a category-style information need such as
films shot in a location or entities related to a historical region. The
retriever must rank compact entity descriptions that satisfy that entity need.

### Observed Data Profile

The task has 50 queries and 6,045 documents. It contains 1,158 positive qrels,
with positives per query ranging from 1 to 81 and a median of 18.00. Queries are
short, averaging 28.16 characters, while documents are compact descriptions
averaging 174.64 characters. The large number of positives means that many
queries represent categories or sets of entities rather than one exact answer.
This makes both early precision and result coverage important: a model should
surface representative relevant entities near the top and cover many valid
entities in the top 100.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5843, hit@10 = 0.9200, and
Recall@100 = 0.6788. BM25 is strong because entity retrieval often preserves
names, locations, titles, and category words. Exact Japanese surface forms,
transliterations, and distinctive DBpedia labels can anchor retrieval well.
However, BM25 is weaker than dense and hybrid retrieval on every reported
metric. Category-style queries can match many descriptions that do not reuse the
same wording, and short queries provide limited lexical context.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.6098, hit@10 =
0.9400, and Recall@100 = 0.7090. Dense retrieval improves both top-10 ranking
and top-100 coverage over BM25. This suggests that embedding similarity helps
with category and description matching, where a relevant entity can be described
through attributes rather than the exact query words. Dense retrieval is
especially useful when the query expresses a class of entities, a relation, or a
property that is only indirectly stated in the entity description.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.6081, hit@10 = 0.9600, and Recall@100 = 0.7263, with no rank-101
safeguard rows. Hybrid retrieval has the best hit@10 and Recall@100, while dense
retrieval is very slightly higher on nDCG@10. This is a balanced hybrid pattern:
lexical search protects exact entity-name matches, dense search adds category
and semantic matches, and the combined candidate pool gives the broadest
coverage of relevant entities.

### Metric Interpretation for Model Researchers

This task is not a simple exact-name lookup benchmark. BM25 performs well, but
the dense and hybrid profiles show that entity search also depends on semantic
description matching. Dense retrieval is best for fine top-10 ranking quality,
while hybrid retrieval is best for finding at least one relevant entity and for
covering more positives in the top 100. Researchers should inspect whether model
gains come from exact entity label handling, category matching, or broad
multi-positive coverage.

### Query and Relevance Type Tendencies

The examples include a dealership and location, a short story collection and
author relation, Gallo-Roman architecture in Paris, former Yugoslav republics,
and films shot in Venice. Some queries include enough unique terms for lexical
retrieval, while others represent classes of entities where many descriptions
can be relevant. Relevant documents are short DBpedia-style summaries, so rank
errors often come from confusing related entities within the same category.

### Representative Failure Modes

BM25 can over-rank exact word matches that do not satisfy the entity relation or
category. Dense retrieval can retrieve semantically adjacent entities that are
plausible but not judged relevant. Hybrid retrieval can improve coverage but may
still miss less obvious positives when a query has dozens of valid entities.
For Japanese translation, transliteration variants and translated entity titles
can also affect both lexical and dense matching.

### Training Data That May Help

Useful training data includes non-overlapping entity search, Wikipedia or
DBpedia entity linking, multilingual entity retrieval, and short-query passage
retrieval. Hard negatives should be related entities from the same category,
location, or time period that fail the specific query relation. Training should
exclude DBpedia-Entity, BEIR, NanoBEIR, and translated entity records likely to
overlap with this benchmark.

### Model Improvement Notes

Strong systems should combine exact entity-name recall with semantic
description matching. For category-heavy queries, training should encourage
result diversity and broad positive coverage. For exact-name queries, the model
must preserve rare names and transliterations. Hybrid candidate generation is a
natural fit, with a reranker used to separate truly relevant entities from
related but incorrect DBpedia entries.

## Example Data

| Query | Positive document |
| --- | --- |
| フィッツジェラルド・オートモール チャンバーズバーグ ペンシルベニア州 [35 chars] | フィッツジェラルド・オートモールは1966年に創業された家族経営の自動車販売会社であり、最初の店舗はメリーランド州ベセスダにオープンしました。2014年時点で、フィッツジェラルド・オートモールは『オートモーティブニュース』が毎年発表する米国「トップ125ディーラーグループ」ランキングで59位にランクインしています。また、フィッツジェラルドのディーラー店舗は、2013年のワーズオートe-ディーラー100に第8位、第25位、第30位、第43位、第98位の5店舗で掲載されています。 [240 chars] |
| 1994年の短編小説集『アリス・マーローはオープン』 [26 chars] | アリス・アーン・マンロー（/ˈælɨs ˌæn mʌnˈroʊ/、旧姓レイドロウ /ˈleɪdlɔː/、1931年7月10日生まれ）はカナダの作家である。マンローの作品は、特に時間の前後を行き来する傾向を持つことから、短編小説の構造を革新したと評されている。彼女の物語は「示すよりも内に秘め、誇示するよりも深く明らかにする」と言われている。マンローのフィクションの舞台は、多くの場合、彼女の故郷であるオンタリオ州南西部のヒューロン郡に設定されている。彼女の物語は、簡潔な散文スタイルで人間の複雑さを探求している。 [256 chars] |
| パリのガロ＝ローマ建築 [11 chars] | パリの芸術は、フランスの首都であるパリにおける芸術文化と歴史に関する記事である。何世紀にもわたり、パリは世界中から芸術家たちを惹きつけてきた。彼らはこの街に訪れ、芸術的な資源や美術館からインスピレーションを得るとともに、研鑽を積んできた。その結果、パリは「芸術の都」という名声を獲得した。 [144 chars] |

### Public Sources

- [DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2 | 2017 | task paper | [https://doi.org/10.1145/3077136.3080751](https://doi.org/10.1145/3077136.3080751) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
