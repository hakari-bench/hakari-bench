# NanoRuMTEB / miracl_ru

## Overview

`miracl_ru` is a Russian factual passage retrieval task from NanoRuMTEB. The queries are short Russian natural-language questions, and the documents are Russian Wikipedia passages. Many queries have multiple relevant passages, often from the same entity or topic. The task measures native Russian ad hoc retrieval rather than translation or English-centered search. Dense retrieval is the strongest top-rank profile, `reranking_hybrid` has the best recall@100, and BM25 remains a strong lexical baseline because entity names and titles often overlap directly.

## Details

### What the Original Data Measures

MIRACL is a multilingual retrieval benchmark covering 18 languages, including Russian. It uses Wikipedia passages, native-language queries, and relevance judgments created for multilingual information retrieval.

ruMTEB includes MIRACL retrieval as a Russian benchmark task. The Nano version uses the MIRACL Russian hard-negative setting, where candidates are drawn from retrieval pools and the evaluation focuses on ranking answer-bearing passages.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 579 positive qrel rows. Queries average 45.37 characters, while documents average 517.26 characters. Positives per query average 2.90, with a minimum of 1, a median of 2, and a maximum of 10. There are 136 multi-positive queries, 68.0% of the split.

Example queries ask whether "Agents of S.H.I.E.L.D." is a drama series, whether China is a socialist state, whether the Cipher Bureau worked on breaking Enigma, how long Tolstoy wrote "War and Peace", and how many days Euromaidan lasted in Ukraine.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.5154, hit@10 of 0.8250, and recall@100 of 0.9326. BM25 is a strong baseline because many Russian questions contain entity names, titles, or distinctive factual terms that appear in relevant Wikipedia passages.

Its limitation is passage selection. BM25 may retrieve the correct article but not the answer-bearing passage, or overrank a prominent entity passage that shares surface terms but does not answer the question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7938, hit@10 of 0.9550, and recall@100 of 0.9585. Dense retrieval is the strongest profile for early ranking.

This suggests that embedding similarity captures Russian question-passage semantics beyond direct word overlap. It helps with paraphrase, inflectional variation, and cases where the answer is expressed in a later explanatory passage.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 1 row receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.6646, hit@10 of 0.9050, and recall@100 of 0.9948. Hybrid retrieval has the best recall@100 but lower top-rank quality than dense retrieval.

The pattern shows that sparse and dense signals are complementary for candidate coverage. BM25 contributes exact entity and title matching, while dense retrieval is better at ordering answer-bearing passages near the top.

### Metric Interpretation for Model Researchers

Because many queries have multiple positives, nDCG@10 measures whether several relevant passages are ranked early, hit@10 measures whether at least one positive appears in the first ten, and recall@100 measures how much relevant material is available for reranking.

For `miracl_ru`, dense nDCG@10 is the main first-stage quality signal. Hybrid recall@100 is valuable when a reranker can distinguish answer-bearing passages from related passages.

### Query and Relevance Type Tendencies

Queries are short Russian fact, definition, and yes/no questions. Relevant documents are Russian Wikipedia passages, often with named entities, dates, titles, and explanatory facts.

Relevance is answer-bearing passage relevance. A passage from the correct article is not necessarily relevant if it does not contain the fact needed by the question.

### Representative Failure Modes

Common failures include retrieving the right entity but wrong passage, overmatching quoted titles, missing inflected or paraphrased Russian wording, and confusing closely related people, works, or events. BM25 is sensitive to exact terms; dense retrieval can still overrank topically related passages without the answer.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Russian train pairs, Russian Wikipedia question-passage retrieval, native Russian factual QA retrieval, and same-language multilingual retrieval data with overlap removed. Evaluation queries, positive passages, and qrels should be excluded.

### Model Improvement Notes

Models should handle Russian morphology, entity aliases, title variants, and passage-level answer grounding. Hard negatives should come from the same article or nearby entity pages. Dense retrieval is the best direct ranker, while hybrid retrieval is useful for high-recall reranking pools.

## Example Data

| Query | Positive document |
| --- | --- |
| «Агенты "Щ.И.Т."» - это драматический сериал? [45 chars] | Агенты «Щ.И.Т.» «Аге́нты „Щ.И.Т.“» () — американский супергеройский телесериал, созданный Джоссом Уидоном и основанный на одноимённом комиксе компании Marvel о вымышленной организации по борьбе с прес... [200 / 420 chars] |
| Китай социалистическое государство? [35 chars] | Китай Официально, Китайская Народная Республика — унитарная республика, социалистическое государство демократической диктатуры народа. Основным законом государства является конституция, принятая в 198... [200 / 574 chars] |
| Занималось Бюро шифров взломом шифров немецкой Энигмы? [54 chars] | Бюро шифров Главным ведомством Бюро и отделением, ответственным за криптоанализ немецких систем шифрования, стало BS4, позже основной задачей отделения стал взлом немецкой шифровальной машины «Энигма»... [200 / 677 chars] |
| Сколько лет Лев Николаевич Толстой писал роман «Война́ и мир»? [62 chars] | Война и мир Толстой писал роман на протяжении 6 лет, с 1863 по 1869 годы. По историческим сведениям, он вручную переписал его 8 раз, а отдельные эпизоды писатель переписывал более 26 раз. Исследовател... [200 / 307 chars] |
| Сколько дней длился Евромайдан в Украине? [41 chars] | Евромайдан События в период с 21 ноября 2013 года по 22 февраля 2014 года после смены власти на Украине в украинском праве официально назывались «массовые акции гражданского протеста в Украине с 21 но... [200 / 280 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | arXiv paper | [https://arxiv.org/abs/2210.09984](https://arxiv.org/abs/2210.09984) |
| The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design | 2025 | arXiv paper | [https://arxiv.org/abs/2408.12503](https://arxiv.org/abs/2408.12503) |
| MIRACL project page | 2023 | project page | [http://miracl.ai/](http://miracl.ai/) |
| mteb/MIRACLRetrievalHardNegatives | 2025 | dataset card | [https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| «Агенты "Щ.И.Т."» - это драматический сериал? | Passage describing the American superhero television series. |
| Китай социалистическое государство? | Passage stating that the People's Republic of China is a socialist state. |
| Занималось Бюро шифров взломом шифров немецкой Энигмы? | Passage about the Cipher Bureau and work on German Enigma systems. |
| Сколько лет Лев Николаевич Толстой писал роман «Война и мир»? | Passage stating that Tolstoy wrote the novel over six years. |
| Сколько дней длился Евромайдан в Украине? | Passage describing the protest dates from November 2013 to February 2014. |
