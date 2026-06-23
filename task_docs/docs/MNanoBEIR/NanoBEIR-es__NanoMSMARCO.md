# MNanoBEIR / NanoBEIR-es / NanoMSMARCO

## Overview

This task is the Spanish NanoBEIR version of MS MARCO, a web question answering and passage ranking benchmark built from real search-engine queries. The original MS MARCO dataset contains anonymized user questions paired with web passages and human-generated answers, making it noisy and practical rather than curated around a known paragraph. In this NanoBEIR slice, short Spanish translated web-search style questions must retrieve Spanish translated answer-bearing passages from 5,043 documents. The task contains 50 queries and 50 positive relevance judgments, with exactly one positive passage per query. It is a compact test of short-query answer retrieval across everyday topics, definitions, names, consumer questions, and underspecified search intents.

## Details

### What the Original Data Measures

MS MARCO measures passage retrieval for real user information needs. Questions are often short and may not contain the same wording as the answer passage. The retrieval task is to find the passage that directly answers the user's need, not simply a passage on the same topic. This makes answerability, paraphrase, and practical context important, especially when the query is a fragment or a definition request.

### Observed Data Profile

The Spanish Nano task has 50 queries, 5,043 documents, and 50 positives. Every query has one relevant passage. Query length averages about 42 characters, and documents average about 360 characters. Example questions ask what rumination syndrome is, who sang "Here I Go Again", who Cameron Boyce plays in Liv and Maddie, where most large deserts are located, and what "copper" means in a policing context. The positive passages are concise web answer passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.404, Hit@10 of 0.600, and Recall@100 of 0.900. Sparse retrieval gives good candidate coverage because many questions contain distinctive terms, entities, or titles. However, it is weaker at ranking the answer passage in the first page. Short queries often express an information need while the answer uses explanatory wording, and BM25 may over-rank passages that repeat a term without answering the question.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline gives the best top-10 ranking, with nDCG@10 of 0.499, Hit@10 of 0.660, and Recall@100 of 0.880. This indicates that semantic answerability is central for Spanish MS MARCO-style retrieval. Dense retrieval can connect a short question to a passage that defines, explains, or answers it in different wording. Its slightly lower Recall@100 than BM25 shows that exact terms still matter for broad candidate discovery, but dense similarity is better for early ordering.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.452, Hit@10 of 0.640, and Recall@100 of 0.940, with three safeguard rows at 101 candidates. It gives the best Recall@100 but does not beat dense retrieval on nDCG@10. This suggests that hybrid search is the best first-stage candidate generator, while dense ranking alone is better at placing the single answer passage highest. For a reranking pipeline, the hybrid candidate set is valuable because it misses fewer positives.

### Metric Interpretation for Model Researchers

Because every query has one positive, Hit@10 and Recall@100 are direct measures of whether the answer passage was found. nDCG@10 is the clearest top-rank signal. The pattern here separates candidate coverage from final ordering: BM25 and hybrid retrieve many positives into the top 100, while dense retrieval ranks positives better near the top. Researchers should decide whether they are optimizing first-stage recall or direct top-10 retrieval quality.

### Query and Relevance Type Tendencies

Queries are short Spanish web questions and often omit context. Relevant documents are direct answer passages, not general topic pages. Hard negatives may share a named entity, media title, or definition term but fail to answer the question. The task rewards semantic answer matching, entity precision, and robustness to translated web phrasing.

### Representative Failure Modes

BM25 can retrieve passages with repeated keywords but no answer. Dense retrieval can retrieve semantically plausible passages that answer a related question but not the exact one. Hybrid retrieval improves candidate coverage but may still order a lexical distractor above the positive. Failure analysis should ask whether the passage directly satisfies the query's information need.

### Training and Leakage Considerations

Training should exclude MS MARCO, BEIR, NanoBEIR, and translated records likely to overlap with these evaluation queries or passages. Useful non-overlapping data includes MS MARCO-style passage-ranking pairs, Spanish or multilingual web QA data, search-query-to-answer-passage pairs, and noisy user-question corpora. Synthetic data should generate realistic short Spanish questions from concise web answer passages.

### Model Improvement Signals

Strong models should improve answerability ranking without losing exact-term recall. Useful signals include short-query paraphrase training, hard negatives that share entities but answer different questions, and multilingual web QA supervision. Hybrid systems should use lexical matching for names and titles while dense retrieval handles definitions and explanatory answer passages.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Qué es el síndrome de rumiación? [33 chars] | Síndrome de rumiación. El síndrome de rumiación, también conocido como mericismo, es un tipo de trastorno de la alimentación no especificado de otra manera que provoca la regurgitación de alimentos. A... [200 / 354 chars] |
| ¿Quién canta "Here I Go Again"? [31 chars] | Para otros usos, consulte Aquí Voy Otra Vez (desambiguación). Aquí Voy Otra Vez es una canción de la banda de rock británica Whitesnake. La canción fue lanzada originalmente en su álbum de 1982, Santo... [200 / 355 chars] |
| ¿Quién interpreta Cameron Boyce en Liv y Maddie? [48 chars] | Prepárense para reírse a carcajadas, chicos. En un adelanto EXCLUSIVO del episodio del 19 de abril de 'Liv & Maddie' titulado 'Prom-A-Rooney.' ¡Obviamente! En el divertido clip, vemos a Cameron Boyce,... [200 / 347 chars] |
| ¿Dónde se encuentran la mayoría de los grandes desiertos del mundo? [67 chars] | Los demás desiertos del planeta se encuentran fuera de las regiones polares. El más extenso es el desierto del Sahara, un desierto subtropical en el norte de África. [165 chars] |
| ¿Qué significa "copper" en el contexto de la policía? [53 chars] | Según los hallazgos actuales parece que "copper" (un policía, literalmente 'el que detiene') precede a "cop" (tanto como verbo, que significa detener, como sustantivo, que significa policía). Es posib... [200 / 382 chars] |

## Public Sources

- [MS MARCO paper](https://arxiv.org/abs/1611.09268)
- [MS MARCO dataset site](https://microsoft.github.io/msmarco/Datasets.html)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| MS MARCO paper (https://arxiv.org/abs/1611.09268) |
| MS MARCO dataset site (https://microsoft.github.io/msmarco/Datasets.html) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
