# NanoRARb / NanoTempReasonL2Fact

## Overview

`NanoTempReasonL2Fact` is an English temporal reasoning retrieval task from NanoRARb. The query includes a temporal question plus a compact set of supporting dated facts, and the relevant document is the correct entity or role active at the queried time. Each query has one positive answer. Compared with the long-context variant, the fact setting gives more focused evidence, but the answer still requires interval selection. Dense retrieval is the strongest top-rank profile, while `reranking_hybrid` gives the best recall@100.

## Details

### What the Original Data Measures

RAR-b converts TempReason temporal reasoning tasks into answer retrieval. The underlying TempReason benchmark tests whether systems can reason over temporal facts, including which entity, position, or relation is valid at a specified date.

The fact variant provides the relevant temporal facts directly in the query rather than burying them in a much larger context. The retriever must still select the answer string that corresponds to the interval containing the queried date.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has one positive. Queries average 1,744.39 characters, and answer documents average 19.91 characters.

Examples ask for the office held by Patricia de Lille, the parliamentary role held by Lord Douglas Gordon-Hallyburton, the head of Russia at a given date, Glynn Snodin's team at a specific time, and the head of Romania in May 1935. The positive documents are short names or role strings.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0615, hit@10 of 0.1350, and recall@100 of 0.7200. BM25 has decent recall because the answer string often appears inside the fact list, but it is poor at top-rank ordering.

The reason is that lexical overlap cannot determine which fact is temporally valid. A fact about the same person or country may share many words while covering a different interval.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3005, hit@10 of 0.5250, and recall@100 of 0.8950. Dense retrieval is much stronger than BM25 for early ranking and broad coverage.

The focused fact set makes semantic matching more effective than in the long-context setting. Dense retrieval can often connect the question to the relevant answer string, but exact interval arithmetic is still needed for the hardest cases.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 15 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.2513, hit@10 of 0.5150, and recall@100 of 0.9250. Hybrid retrieval has the highest recall@100 but lower nDCG@10 than dense retrieval.

This indicates that sparse evidence helps recover answer strings in the candidate pool, while dense retrieval orders the most likely temporal answer better. A reranker should benefit from the hybrid pool if it can perform interval selection.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures early placement of the exact answer, hit@10 measures whether the answer is in the first ten candidates, and recall@100 measures reranking availability.

For TempReasonL2Fact, dense retrieval is the top-rank baseline and hybrid retrieval is the coverage baseline. A strong system should use the provided facts to compute which interval covers the target date.

### Query and Relevance Type Tendencies

Queries contain a temporal question and several dated facts. Relevant documents are short answer strings, usually entity names, political offices, sports teams, or roles. The answer must match the fact whose start and end dates contain the target date.

Relevance is exact temporal selection. A candidate with the same entity but a wrong time span is not relevant.

### Representative Failure Modes

Common failures include choosing an entity from an adjacent interval, selecting a role associated with the same person but not the target date, ranking a fact with greater lexical overlap above the valid fact, and confusing open or overlapping date ranges. BM25 recovers strings but does not reason over time; dense retrieval can approximate but not guarantee interval correctness.

### Training Data That May Help

Useful training data includes temporal QA with supporting facts, interval reasoning tasks, entity-time retrieval, and date containment examples. Evaluation queries, facts, answers, and qrels should be excluded.

### Model Improvement Notes

Models should learn to parse date intervals and compare them to target dates. Hard negatives should use the same relation or entity with nearby dates outside the correct interval. Hybrid candidate pools are useful when paired with rerankers that explicitly check temporal validity.

## Example Data

| Query | Positive document |
| --- | --- |
| Question: Which position did Patricia de Lille hold in Sep, 2015? Facts: Patricia de Lille holds the position of Member of Provincial Parliament of Western Cape from Sep, 2010 to May, 2011. Patricia de Lille holds the position of mayor of Cape Town from Jun, 2011 to Oct, 2018. Patricia de Lille holds the position of member of the National Assembly of South Africa from May, 2019 to Dec, 2022. [398 chars] | mayor of Cape Town [18 chars] |
| Question: Which position did Lord Douglas Gordon-Hallyburton hold in Oct, 1833? Facts: Lord Douglas Gordon-Hallyburton holds the position of Member of the 13th Parliament of the United Kingdom from Jul, 1837 to Jun, 1841. Lord Douglas Gordon-Hallyburton holds the position of Member of the 11th Parliament of the United Kingdom from Dec, 1832 to Dec, 1834. Lord Douglas Gordon-Hallyburton holds the position of Member of the 10th Parliament of the United Kingdom from Jan, 1832 to Dec, 1832. Lord Dou... [500 / 632 chars] | Member of the 11th Parliament of the United Kingdom [51 chars] |
| Question: Who was the head of Russia in Jul, 1999? Facts: Mikhail Kasyanov is the head of the government of Russia from May, 2000 to Feb, 2004. Viktor Khristenko is the head of the government of Russia from Feb, 2004 to Mar, 2004. Sergey Kiriyenko is the head of the government of Russia from Mar, 1998 to Aug, 1998. Yegor Gaidar is the head of the government of Russia from Jun, 1992 to Dec, 1992. Dmitry Medvedev is the head of the government of Russia from May, 2012 to Jan, 2020. Viktor Zubkov is... [500 / 1,190 chars] | Sergei Stepashin [16 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which position did Patricia de Lille hold in Sep, 2015, given a compact list of office intervals? | Mayor of Cape Town. |
| Which position did Lord Douglas Gordon-Hallyburton hold in Oct, 1833? | Member of the 11th Parliament of the United Kingdom. |
| Who was the head of Russia in Jul, 1999? | Sergei Stepashin. |
| Which team did Glynn Snodin play for in Jan, 1992? | Leeds United F.C. |
| Who was the head of Romania in May, 1935? | Gheorghe Tatarescu. |
