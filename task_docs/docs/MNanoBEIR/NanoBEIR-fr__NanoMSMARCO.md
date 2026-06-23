# MNanoBEIR / NanoBEIR-fr / NanoMSMARCO

## Overview

This task is the French NanoBEIR version of MS MARCO, a web question answering and passage ranking benchmark built from real search-engine queries. The original MS MARCO dataset contains anonymized user questions paired with answer-bearing web passages, so the questions are often short, practical, and underspecified. In this NanoBEIR slice, French translated web-search style questions must retrieve French translated answer passages from 5,043 candidate documents. The task contains 50 queries and 50 positive relevance judgments, with exactly one positive passage per query. It is a compact diagnostic for short-query answer retrieval across everyday information needs, definitions, media questions, consumer topics, and practical web search phrasing.

## Details

### What the Original Data Measures

MS MARCO measures retrieval for real user information needs rather than questions written to match a known paragraph. In retrieval form, the relevant document is the passage that directly answers the question. This often requires connecting a short query to explanatory wording in an answer passage. A page that repeats a term but does not resolve the user's intent is not sufficient.

### Observed Data Profile

The French Nano task has 50 queries, 5,043 documents, and 50 positives. Every query has one positive passage. Query length averages about 45 characters, and documents average about 374 characters. Example questions ask what rumination syndrome is, who sang "Here I Go Again", what role Cameron Boyce plays in Liv and Maddie, where most large deserts are located, and what a policing slang term means. Documents are concise French translated web answer passages.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.461, Hit@10 of 0.620, and Recall@100 of 0.880. Sparse retrieval gives useful coverage because many questions contain distinctive names, titles, or terms. However, it does not always rank the answer passage high because web questions often need answerability rather than surface repetition. BM25 can retrieve passages sharing an entity or term while missing the passage that actually answers the question.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is strongest by top-10 ranking, with nDCG@10 of 0.575, Hit@10 of 0.720, and Recall@100 of 0.940. This shows that semantic answer matching is central for this French MS MARCO slice. Dense retrieval can connect short questions to answer passages that explain, define, or resolve the intent using different wording. It also improves candidate coverage over BM25 in this sample.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.531, Hit@10 of 0.700, and Recall@100 of 0.940, with three safeguard rows at 101 candidates. It matches dense Recall@100 but trails dense top-10 ranking. This suggests that hybrid search is useful as a robust candidate generator, while dense ranking is better at ordering the single answer passage near the top. BM25 still contributes exact names and terms, especially for entity-heavy queries.

### Metric Interpretation for Model Researchers

Because each query has one positive, Hit@10 and Recall@100 are direct evidence-finding measures. nDCG@10 is the clearest signal for first-page quality. The contrast between dense and hybrid is useful: both have high recall, but dense places positives higher. For reranking pipelines, hybrid candidates may be sufficient; for direct retrieval, dense ordering is stronger.

### Query and Relevance Type Tendencies

Queries are short French user questions or search prompts. Relevant documents are concise answer-bearing passages. Some queries are definition requests, some ask about media or names, and others ask practical facts. Hard negatives may mention the same entity or topic but answer a different question. The task rewards answerability, paraphrase handling, and precise entity matching.

### Representative Failure Modes

BM25 can over-rank passages with repeated query terms but no answer. Dense retrieval can retrieve passages that answer a nearby but different question. Hybrid retrieval improves coverage but may still put a lexical distractor ahead of the answer. Failure analysis should check whether the retrieved passage directly satisfies the query.

### Training and Leakage Considerations

Training should exclude MS MARCO, BEIR, NanoBEIR, and translated records likely to overlap with these queries or passages. Useful non-overlapping data includes MS MARCO-style passage-ranking pairs, French or multilingual web QA retrieval data, search-query-to-answer-passage pairs, and noisy real user-question datasets. Synthetic data should generate short French questions from concise non-evaluation web answer passages.

### Model Improvement Signals

Strong models should improve answerability ranking while preserving exact entity recall. Useful training signals include short-query paraphrases, definition questions, same-entity hard negatives, and multilingual web QA examples. Hybrid systems should use sparse matching for names and rare terms while dense retrieval handles explanatory answer wording.

## Example Data

| Query | Positive document |
| --- | --- |
| Qu'est-ce que le syndrome de rumination ? [41 chars] | Syndrome de rumination. Le syndrome de rumination, également appelé merycisme, est un trouble alimentaire non spécifié qui provoque la régurgitation des aliments. Bien qu'il ne soit pas identifié comm... [200 / 316 chars] |
| Qui a chanté "Here I Go Again" ? [32 chars] | Pour d'autres usages, voir Here I Go Again (homonymie). "Here I Go Again" est une chanson du groupe de rock britannique Whitesnake. Parue à l'origine sur leur album de 1982, Saints & Sinners, la chans... [200 / 359 chars] |
| Quel rôle joue Cameron Boyce dans la série Liv et Maddie ? [58 chars] | Préparez-vous à bien rire, les amis. Dans un EXCLUSIF avant-première de l'épisode du 19 avril de Liv & Maddie intitulé “Prom-A-Rooney.” Évidemment. Dans cet extra hilarant, on voit l'acteur de Jessie,... [200 / 334 chars] |
| Où se situent la plupart des grands déserts de la Terre ? [57 chars] | Les autres déserts de la Terre se situent en dehors des régions polaires. Le plus grand est le désert du Sahara, un désert subtropical situé en Afrique du Nord. [160 chars] |
| Que signifie le mot "flic" ? [28 chars] | Selon les résultats actuels, il semble que le terme « copper » (un policier, littéralement « celui qui arrête ») soit antérieur à « cop » (utilisé soit verbalement pour signifier « arrêter » ou comme... [200 / 412 chars] |

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
