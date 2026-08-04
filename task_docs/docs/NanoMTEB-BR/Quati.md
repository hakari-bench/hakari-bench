# NanoMTEB-BR / Quati

## Overview

Quati is a general-domain passage-retrieval task created directly for Brazilian
Portuguese. Native speakers supplied queries, source documents came from
frequently accessed Brazilian websites, and relevance judgments were produced
with a large-language-model annotation process evaluated against human
agreement. The collection was designed to avoid relying on translated English
benchmarks and to represent information needs and web language that occur in
Brazil. NanoMTEB-BR evaluates a compact query sample against a 10,000-document
pool with hard negatives, so many candidates remain topically plausible. Some
queries have multiple relevant passages, making both early precision and
coverage important. Compared with the suite's institutional and specialist
tasks, Quati provides a broader test of everyday semantic retrieval across
topics. It reveals whether a model's Brazilian Portuguese quality generalizes
beyond legal, financial, educational, or medical terminology.

## Details

### What the Task Measures

The task measures native-language web passage retrieval under same-topic hard
negatives. A strong model must represent the requested relation or fact, not
only broad topic words, and should retrieve multiple useful passages when the
judgments support them.

### Metric Interpretation

`nDCG@10` rewards ordering judged relevant passages near the top and reflects
multi-positive coverage. `Hit@10` checks whether at least one relevant passage
appears in the first ten. Strong hit rate but weaker nDCG may indicate topical
success without consistent ordering of all useful passages.

### Training and Leakage Notes

Useful supervision includes non-overlapping Brazilian web search and passage
retrieval data with hard negatives. Exclude Nano queries, qrels, positive
passages, and upstream Quati evaluation records. Since web text is easily
republished, audit normalized and semantic near-duplicates across training and
evaluation sources.

## Public Sources

- [Quati paper](https://aclanthology.org/2024.stil-1.19/).
- [Quati source dataset](https://huggingface.co/datasets/MTEB-BR/quati-50k).
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
