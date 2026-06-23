# MNanoBEIR / NanoBEIR-fr / NanoHotpotQA

## Overview

This task is the French NanoBEIR version of HotpotQA, a multi-hop question answering retrieval benchmark built from Wikipedia. The original HotpotQA dataset was designed to require reasoning over multiple supporting documents, including bridge questions and comparison questions. In this NanoBEIR slice, French translated multi-hop questions must retrieve French translated supporting Wikipedia passages from 5,090 candidates. The task contains 50 queries and 100 positive relevance judgments, with exactly two positives for every query. It is a compact diagnostic for evidence-chain retrieval: models must retrieve both supporting passages needed for reasoning, not only the most obvious entity page.

## Details

### What the Original Data Measures

HotpotQA measures explainable multi-hop QA. In retrieval form, the goal is to surface the two evidence passages that make the reasoning path possible. One passage may mention the query entity, while the other contains the bridge or comparison evidence needed to answer. This differs from single-hop QA because retrieving only one relevant passage can leave the downstream reader without enough evidence.

### Observed Data Profile

The French Nano task has 50 queries, 5,090 documents, and 100 positives. Every query has exactly two relevant passages. Query length averages about 99 characters, and documents average about 389 characters. Example questions involve Penny Rae Bridges, Kaganoi Shigemochi, Joby Harold and Samuel Sim, a Clemson football game, and Supersuckers. The documents are short translated Wikipedia-style entity and event descriptions.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.726, Hit@10 of 0.940, and Recall@100 of 0.920. This reflects the entity-heavy structure of the task: names, titles, locations, and dates often appear directly in one or both supporting passages. Sparse retrieval is good at finding the obvious page. The main challenge is recovering both supports, especially the bridge passage that may not share as many query terms.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline improves on BM25, with nDCG@10 of 0.756, Hit@10 of 0.960, and Recall@100 of 0.930. Dense retrieval helps connect bridge relations and comparison context when the wording differs from the question. It still depends on correct entity grounding, but the results show that semantic similarity contributes useful ranking signal beyond exact names and titles.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest, with nDCG@10 of 0.783, Hit@10 of 1.000, and Recall@100 of 0.950. This is a clear hybrid-search case. BM25 anchors exact entity names and rare terms, while dense retrieval helps identify the semantically connected supporting passage. The hybrid result improves both first-page inclusion and candidate coverage, which is important because the task requires a complete two-document evidence chain.

### Metric Interpretation for Model Researchers

Hit@10 can be misleading because a query is counted as hit when at least one positive appears, even though both positives are needed for multi-hop reasoning. nDCG@10 and Recall@100 are more informative. Recall@100 measures whether both evidence documents are available for a downstream reader or reranker. The hybrid profile's gains show that combining sparse and dense candidates is useful for complete evidence recovery.

### Query and Relevance Type Tendencies

Queries are French natural-language multi-hop questions involving people, films, sports, music, and historical entities. Relevant documents are paired supporting passages. One support is often lexically obvious, while the other may be connected through a creator, actor, composer, event, date, or comparison relation. The task rewards entity linking, alias handling, and relation-aware retrieval.

### Representative Failure Modes

BM25 can retrieve the direct entity page but miss the second support. Dense retrieval can retrieve semantically related pages that are not part of the annotated evidence path. Hybrid retrieval improves coverage but can still rank one support much higher than the other. Failure analysis should check whether both positives are present and whether they jointly support the answer.

### Training and Leakage Considerations

Training should exclude HotpotQA, BEIR, NanoBEIR, and translated records likely to overlap with these questions or supporting pages. Useful non-overlapping data includes multi-hop QA retrieval pairs, Wikipedia hyperlink graph supervision, French or multilingual question-to-multiple-document data, and bridge/comparison question generation. Multi-positive training is required because every query has two supporting documents.

### Model Improvement Signals

Strong models should improve second-support retrieval without sacrificing exact entity recall. Useful signals include paired evidence training, bridge-entity hard negatives, comparison questions, and relation-aware dense retrieval. Hybrid systems should preserve names and titles through BM25 while using dense retrieval to recover semantically linked supports.

## Example Data

| Query | Positive document |
| --- | --- |
| Avec quel autre acteur Penny Rae Bridges a-t-elle joué dans une sitcom ? [72 chars] | Penny Rae Bridges (née le 29 juillet 1990) est une actrice américaine. Elle a joué dans les séries "For Your Love", "Family Law", "Boy Meets World" et "The Parent 'Hood". Elle est surtout connue pour son rôle dans "Half & Half", celui de la jeune Mona. [252 chars] |
| Qui a donné à Kaganoi Shigemochi une lame forgée par Masamune, le fondateur de l'école Muramasa ? [97 chars] | Kaganoi Shigemochi (加賀井 重望, 1561 – 27 août 1600) était un samouraï japonais de la période Azuchi-Momoyama, au service du clan Oda. Il gouvernait le château de Kaganoi. Lors de la bataille de Komaki et Nagakute, Shigemochi combattait sous les ordres de son père, Shigemune, qui était rattaché aux forces d'Oda Nobukatsu. Peu après, le château de Kaganoi fut encerclé par les troupes de Toyotomi Hideyoshi ; Shigemune se rendit, et Shigemochi fut employé par Hideyoshi comme messager, recevant une rente de 10 000 "koku". Il possédait également une lame forgée par Muramasa, que Hideyoshi lui offrit en 1598. [606 chars] |
| Quel film a été écrit et réalisé par Joby Harold avec la musique de Samuel Sim ? [80 chars] | Samuel Sim est un compositeur de films et de séries télévisées. Il a acquis une notoriété avec sa bande originale récompensée pour la série dramatique de la BBC "Dunkirk". Depuis, il a composé la musique pour une grande variété de productions cinématographiques et télévisuelles. Récemment, il a signé la bande originale du film "Awake" pour The Weinstein Company et de la série dramatique BBC/HBO "House of Saddam". Sa musique la plus récemment acclamée est la bande originale de "Home Fires". "Home Fires (Bande originale de la série télévisée)" est sorti le 6 mai 2016 chez Sony Classical Records. [600 chars] |

## Public Sources

- [HotpotQA paper](https://arxiv.org/abs/1809.09600)
- [HotpotQA official site](https://hotpotqa.github.io/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| HotpotQA paper (https://arxiv.org/abs/1809.09600) |
| HotpotQA official site (https://hotpotqa.github.io/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
