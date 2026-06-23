# NanoRuMTEB / ria_news

## Overview

`ria_news` is a Russian headline-to-article retrieval task from NanoRuMTEB. The query is a compact Russian news headline, and the relevant document is the corresponding RIA news article body. Each query has one positive article among 10,000 documents. All retrieval profiles are strong because headlines and articles often share named entities, locations, and event phrases. Dense retrieval has the best nDCG@10 and hit@10, while `reranking_hybrid` has the best recall@100.

## Details

### What the Original Data Measures

ruMTEB includes RiaNewsRetrieval as a Russian retrieval task built from RIA news data. The underlying RIA corpus was originally used for headline generation, with Russian news articles and their titles from the Rossiya Segodnya news collection.

In retrieval form, the task reverses headline generation: given a headline, the system must retrieve the article body it describes. This tests asymmetric news retrieval, where a short summary-like query must match a longer event report.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 61.99 characters, while article bodies average 1,145.34 characters.

Example headlines mention temporary accommodation points in the Russian Far East, Taliban leaders receiving Afghan passports, Tatneft work outside Tatarstan, RTS and MICEX index changes, and a football transfer involving Zenit.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.9135, hit@10 of 0.9500, and recall@100 of 0.9750. BM25 is very strong because the headline usually repeats the central entities, places, and event words that appear in the article.

The remaining difficulty is event disambiguation. News corpora contain many near-duplicate stories about the same officials, locations, market indicators, disasters, or sports teams, so exact overlap can retrieve a related but different event.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.9478, hit@10 of 0.9700, and recall@100 of 0.9750. Dense retrieval is the strongest direct ranker.

This shows that semantic similarity helps align compact headlines with longer article bodies, especially when the article elaborates the event using quotes, paraphrases, or additional context.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 2 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.9272, hit@10 of 0.9450, and recall@100 of 0.9900. Hybrid retrieval has the best broad coverage but slightly weaker early ranking than dense retrieval.

This suggests that sparse event anchors improve candidate coverage, while dense retrieval orders the exact article better among same-topic news items.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the corresponding article appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `ria_news`, the metrics are high enough that residual errors likely reflect near-duplicate event confusion, short or noisy headlines, and article-body variants rather than general topical failure.

### Query and Relevance Type Tendencies

Queries are short lowercase Russian headlines. Documents are longer Russian news bodies with agency style, quotes, dates, named entities, and event details.

Relevance is article-level identity. A topically similar article about the same actor or event category is wrong if it is not the article paired with the headline.

### Representative Failure Modes

Common failures include retrieving another article about the same location, official, team, market index, or disaster; overmatching repeated news vocabulary; and missing terse headlines with little context. BM25 is strong but can be distracted by shared event terms; dense retrieval can still confuse related articles.

### Training Data That May Help

Useful training data includes non-overlapping Russian headline-to-article pairs, Russian news summarization pairs converted to retrieval, same-topic hard-negative clusters, and Russian news search or click data with overlap removed. Evaluation headlines, articles, and qrels should be excluded.

### Model Improvement Notes

Models should preserve named entities and dates while learning event-level paraphrase between headline and body. Hard negatives should be same-day or same-topic articles with overlapping actors and locations. Dense retrieval is the best direct ranker, while hybrid retrieval is useful for recall-oriented reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| около 1 тыс человек остаются в пунктах временного содержания в дфо [66 chars] | глава мчс россии владимир пучков заявил, что около тысячи человек, пострадавших от наводнения на дальнем востоке, смогут находиться в пунктах временного размещения, пока не будут решены их жилищные пр... [200 / 1,563 chars] |
| афганистан выдал паспорта освобожденным в пакистане главам "талибан" [68 chars] | консульство афганистана в пакистанском городе пешавар выдало афганские паспорта деятелям радикального движения "талибан", которые были на днях освобождены пакистанскими властями из тюрем по просьбе аф... [200 / 1,537 chars] |
| минниханов не против работы "татнефти" за пределами татарстана [62 chars] | оао "татнефть" продолжит работу над существующими проектами за пределами татарстана и будет принимать участие в новых интересных проектах, если такие появятся, заявил агентству "прайм" президент тата... [200 / 1,607 chars] |
| индекс ртс на открытии упал на 1,66%, ммвб - на 0,84% [53 chars] | индекс ртс к 10.01 мск пятницы упал на 1,66% - до 1364,83 пункта, индекс ммвб упал на 0,84% - до 1377,74 пункта, свидетельствуют данные бирж. аналитики предсказывали негативное начало торгов при смеша... [200 / 218 chars] |
| кришито присоединится к фк "зенит" в начале июля - источник в "дженоа" [70 chars] | футболист доменико кришито, официальное объявление о переходе которого из "дженоа" в "зенит" может быть сделано уже через несколько дней, присоединится к санкт-петербургскому клубу в начале июля, соо... [200 / 1,520 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design | 2025 | arXiv paper | [https://arxiv.org/abs/2408.12503](https://arxiv.org/abs/2408.12503) |
| Self-Attentive Model for Headline Generation | 2019 | arXiv paper | [https://arxiv.org/abs/1901.07786](https://arxiv.org/abs/1901.07786) |
| mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2 | 2025 | dataset card | [https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| около 1 тыс человек остаются в пунктах временного содержания в дфо | Article about flood victims in the Far East staying in temporary accommodation points. |
| афганистан выдал паспорта освобожденным в пакистане главам "талибан" | Article about Afghan passports issued to Taliban figures released in Pakistan. |
| минниханов не против работы "татнефти" за пределами татарстана | Article about Tatneft projects outside Tatarstan. |
| индекс ртс на открытии упал на 1,66%, ммвб - на 0,84% | Article giving RTS and MICEX opening index movements. |
| кришито присоединится к фк "зенит" в начале июля | Article about Domenico Criscito joining Zenit in early July. |
