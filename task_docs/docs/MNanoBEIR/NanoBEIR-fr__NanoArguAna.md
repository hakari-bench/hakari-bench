# MNanoBEIR / NanoBEIR-fr / NanoArguAna

## Overview

This task is the French NanoBEIR version of ArguAna, an argument retrieval benchmark where the query is a long argument and the relevant document is its counterargument. The original ArguAna task studies retrieval of the best counterargument without assuming prior topic knowledge, using debate-portal pairs where good counterarguments usually address the same issue while reversing stance. In this NanoBEIR slice, French translated arguments must retrieve French translated counterarguments from 3,635 candidate documents. The task contains 50 queries and 50 positive relevance judgments, with exactly one positive per query. It is a compact diagnostic for stance-aware long-document retrieval, where topic similarity is necessary but insufficient because same-side arguments can look lexically and semantically close while being irrelevant.

## Details

### What the Original Data Measures

ArguAna measures counterargument retrieval. A relevant document should rebut the query argument by targeting the same issue, premise, or aspect from an opposing stance. This differs from ordinary topical search: a document can share many words and still be wrong if it supports the query's claim instead of challenging it. The task therefore tests long-passage argument understanding, stance reversal, premise matching, and the ability to reject same-topic support.

### Observed Data Profile

The French Nano task has 50 queries, 3,635 documents, and 50 positives. Every query has one positive counterargument. Queries are long, averaging about 1,271 characters, and documents average about 1,157 characters. The examples cover political reform, Heathrow expansion, excessive consumer choice, cyberattacks by non-state actors, and religiously motivated speech. Both query and document passages contain premises, conclusions, examples, and cited evidence.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.395, Hit@10 of 0.660, and Recall@100 of 0.900. Sparse retrieval is useful because counterarguments discuss the same topic and often repeat names, policies, institutions, or issue-specific terms. However, BM25 is limited at top ranking because lexical overlap does not distinguish rebuttal from agreement. A same-topic supporting argument can receive a strong sparse score even when the only positive is the opposing argument.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline performs best by top-10 ranking, with nDCG@10 of 0.520, Hit@10 of 0.840, and Recall@100 of 0.980. This indicates that embedding similarity is better at capturing argumentative fit and long-passage semantic relation in this French sample. Dense retrieval can connect rebuttals that use different wording while still addressing the same premise. It also improves candidate coverage over BM25, suggesting that lexical matching alone misses some counterarguments.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.461, Hit@10 of 0.780, and Recall@100 of 1.000. It gives complete top-100 coverage but does not beat dense retrieval in top-10 ordering. This is a useful pipeline pattern: hybrid search is excellent for candidate generation because it combines exact issue terms with semantic relation, but dense scoring is stronger for deciding which candidate is the best counterargument. A stance-aware reranker could benefit from the hybrid pool.

### Metric Interpretation for Model Researchers

Because each query has exactly one positive, Recall@100 measures whether the counterargument is available for a downstream reranker. nDCG@10 and Hit@10 measure whether the retriever itself places the counterargument early enough to be useful. The dense and hybrid split is important: dense is the better direct ranker, while hybrid gives the safest candidate coverage.

### Query and Relevance Type Tendencies

Queries are long French arguments about controversial policy or social topics. Relevant documents are counterarguments, not general answers or supporting evidence. Hard negatives are likely to share the same topic and vocabulary but take the same stance or attack a different premise. The task rewards stance awareness and premise-level alignment.

### Representative Failure Modes

BM25 can retrieve same-topic support because it shares issue vocabulary. Dense retrieval can retrieve a semantically close argument that does not actually rebut the query. Hybrid retrieval can include the positive but still rank a lexical distractor above it. Failure analysis should ask whether the retrieved document challenges the query's central claim or merely discusses the same issue.

### Training and Leakage Considerations

Training should exclude ArguAna, BEIR, NanoBEIR, and translated debate records likely to overlap with this evaluation slice. Useful non-overlapping data includes argument-counterargument pairs, stance-aware retrieval datasets, debate portal argument pairs, claim rebuttal data, and French or multilingual argument mining corpora. Synthetic data should create paired pro and con arguments for the same issue with explicit stance reversal and same-topic hard negatives.

### Model Improvement Signals

Strong models should improve stance-sensitive ranking while preserving topic coverage. Useful signals include long-passage contrastive training, premise-targeted rebuttals, same-topic same-stance hard negatives, and multilingual argument mining supervision. Hybrid systems should use sparse matching for issue anchoring and dense or cross-encoder scoring for rebuttal relation.

## Example Data

| Query | Positive document |
| --- | --- |
| Le public est indifférent à la réforme. Il est discutable que la réforme de la Chambre des Lords soi... [100 / 646 chars] | La campagne pour le vote alternatif ne peut pas être comparée à une réforme de la Chambre des Lords. De plus, il ne faut pas confondre un public mal informé par la propagande politique avec de l'apath... [200 / 471 chars] |
| L'expansion de Heathrow est cruciale pour l'économie. L'expansion de Heathrow permettrait de mainten... [100 / 1,372 chars] | La communauté des affaires est loin d'être unie dans son supposé soutien à une troisième piste. Des enquêtes suggèrent que de nombreuses entreprises influentes ne soutiennent en réalité pas l'expansio... [200 / 1,519 chars] |
| Les gens sont submergés par trop de choix, ce qui les rend moins heureux. La publicité submerge beau... [100 / 1,054 chars] | Les gens sont mécontents parce qu'ils ne peuvent pas tout avoir, et non parce qu'ils ont trop de choix et que cela les stresse. En réalité, les publicités jouent un rôle crucial en s'assurant que l'ar... [200 / 988 chars] |
| Les cyberattaques sont souvent menées par des acteurs non étatiques, tels que des cyberterroristes o... [100 / 1,072 chars] | En cas d'attaques par des acteurs non étatiques, de nombreux experts en droit international s'accordent à dire que l'État peut encore riposter en légitime défense si un autre État est 'incapable ou ré... [200 / 607 chars] |
| Parce que la religion favorise la certitude des croyances, la haine inspirée par le divin est facile... [100 / 1,319 chars] | Personne n'est forcé de commettre des actes de violence par les paroles d'autrui; c'est leur choix de le faire. De même, il y a beaucoup de gens qui pourraient avoir des opinions considérées comme hom... [200 / 695 chars] |

## Public Sources

- [ArguAna paper](https://aclanthology.org/P18-1023/)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| ArguAna paper (https://aclanthology.org/P18-1023/) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
