# NanoMIRACL

## Overview

NanoMIRACL is a language-specific Nano benchmark for MIRACL, a multilingual ad
hoc retrieval benchmark built around Wikipedia passage retrieval. The original
MIRACL work covers eighteen languages and asks a monolingual retrieval question
in each split: an Arabic query retrieves Arabic passages, a Japanese query
retrieves Japanese passages, and so on. This group keeps that retrieval setting
while making the task small enough to inspect one language at a time.

The group is valuable because it holds the high-level task constant while
changing script, morphology, tokenization behavior, resource level, and
Wikipedia coverage. The model is not translating and is not answering from a
fixed article. It must rank the passage that contains the answer-bearing
evidence for a short natural-language question. In the current Nano metadata,
BM25 is often a strong lexical anchor, dense retrieval from
`harrier_oss_v1_270m` is usually the best top-rank signal, and
`reranking_hybrid` gives the broadest top-100 candidate coverage.

## What This Group Measures

[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/)
and its arXiv version, [Making a MIRACL](https://arxiv.org/abs/2210.09984),
describe MIRACL as a multilingual retrieval benchmark with native-language
queries, Wikipedia passages, and relevance judgments. NanoMIRACL should be read
as a compact monolingual passage-retrieval suite derived from that benchmark.

The shared relevance relation is evidence retrieval: the positive passage should
answer or directly support the query. The task is therefore different from
generic semantic similarity. A high-scoring retriever must keep exact entity
names, dates, and article-title clues when they matter, while also recognizing
the relation asked by the question. This is especially important in languages
where segmentation, inflection, named-entity spelling, or short query length can
change sparse and dense behavior.

## Task Families

- **Wikipedia evidence retrieval:** all 18 tasks use monolingual factual
  question-to-passage retrieval over Wikipedia-style passages.
- **Short-query entity retrieval pressure:** Japanese, Chinese, Korean, Thai,
  Arabic, Persian, and several European-language splits often depend on short
  entity-heavy questions.
- **Multi-positive passage ranking:** most splits have more positive qrels than
  queries, so models are rewarded for ranking several acceptable passages, not
  only for finding one exact page.
- **Low-resource and script-diverse evaluation:** Bengali, Telugu, Swahili,
  Yoruba, Thai, and Persian expose failure modes that may be hidden by
  English-centric retrieval tuning.

## Dataset Shape

NanoMIRACL contains 18 task pages, 3,519 queries, 180,000 split-local documents,
and 8,071 positive qrel rows. Each split has 10,000 documents in the current
metadata; this is a sum over language-local candidate pools, not a deduplicated
corpus size. Most languages have 200 queries, while Yoruba has 119. Positive
density differs substantially: Telugu averages close to one positive per query,
while Spanish averages more than four.

Queries are short, with a query-weighted mean around 37.6 characters. Documents
are compact passages, with a document-weighted mean around 353 characters. CJK
splits have much shorter character counts than European-language splits, so raw
character length should not be compared as if it were token length. The group is
best interpreted as eighteen parallel retrieval conditions rather than one
large multilingual pool.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest when the query contains rare words, entity names, article
titles, dates, or other exact anchors that survive tokenization. Finnish,
Spanish, English, Indonesian, and Japanese are among the stronger sparse
profiles in the current metadata. BM25 is less reliable when the relevant
passage shares many terms with non-answering neighbors or when segmentation and
morphology make exact matching brittle.

At the group level, BM25 is not merely a weak baseline. It provides high
top-100 coverage and identifies tasks where lexical memorization or exact
surface-form handling is still central. For model researchers, BM25-led or
BM25-competitive splits should be treated as warnings that dense-only retrieval
may be discarding useful exact-match evidence.

### Dense Profile

Dense retrieval with `harrier_oss_v1_270m` is the best nDCG@10 profile for most
NanoMIRACL languages. It is especially useful when the query and passage express
the same answer relation with different wording, or when the relevant passage is
not the one with the highest exact lexical overlap. Dense retrieval improves the
interpretation of short questions because it can rank evidence passages by
answerability rather than by surface-term count alone.

The dense profile is still not a full replacement for sparse retrieval. Rare
names, spellings, and transliterated entities can be smoothed away by embedding
similarity. The most useful comparison is therefore not simply BM25 versus
dense, but which languages are dense-led, which are sparse-competitive, and
which lose top-100 coverage under dense retrieval.

### Reranking Hybrid Profile

`reranking_hybrid` combines the retrieval strengths needed for top-100 reranker
candidate generation. It is not always the best nDCG@10 sorter, but it often
has the safest Recall@100 because it can keep positives found by either lexical
or dense retrieval. Indonesian and Korean are examples where the hybrid profile
is best by nDCG@10 in the current metadata.

For reranker experiments, this profile should be read as the practical candidate
pool. If dense has the best nDCG@10 but hybrid has better recall, the task is
telling a clear story: first-stage dense ranking is good, but a reranker benefits
from candidates recovered by both sparse and dense retrieval.

## Language Summary

| Language | Task | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Arabic | [ar](ar.md) | 200 | 10,000 | 386 | 0.6352 | 0.8223 | 0.7514 | Dense |
| Bengali | [bn](bn.md) | 200 | 10,000 | 407 | 0.5033 | 0.7661 | 0.6537 | Dense |
| German | [de](de.md) | 200 | 10,000 | 538 | 0.5172 | 0.7389 | 0.6418 | Dense |
| English | [en](en.md) | 200 | 10,000 | 560 | 0.6774 | 0.7721 | 0.7474 | Dense |
| Spanish | [es](es.md) | 200 | 10,000 | 934 | 0.6861 | 0.7793 | 0.7478 | Dense |
| Persian | [fa](fa.md) | 200 | 10,000 | 427 | 0.5788 | 0.6476 | 0.6334 | Dense |
| Finnish | [fi](fi.md) | 200 | 10,000 | 328 | 0.7734 | 0.8634 | 0.8332 | Dense |
| French | [fr](fr.md) | 200 | 10,000 | 417 | 0.4658 | 0.6828 | 0.5896 | Dense |
| Hindi | [hi](hi.md) | 200 | 10,000 | 410 | 0.3037 | 0.6847 | 0.5174 | Dense |
| Indonesian | [id](id.md) | 200 | 10,000 | 654 | 0.6773 | 0.7076 | 0.7171 | Reranking hybrid |
| Japanese | [ja](ja.md) | 200 | 10,000 | 373 | 0.6601 | 0.7745 | 0.7223 | Dense |
| Korean | [ko](ko.md) | 200 | 10,000 | 508 | 0.4994 | 0.6910 | 0.7026 | Reranking hybrid |
| Russian | [ru](ru.md) | 200 | 10,000 | 555 | 0.5887 | 0.7693 | 0.6816 | Dense |
| Swahili | [sw](sw.md) | 200 | 10,000 | 405 | 0.5852 | 0.7872 | 0.7292 | Dense |
| Telugu | [te](te.md) | 200 | 10,000 | 211 | 0.5292 | 0.8720 | 0.6953 | Dense |
| Thai | [th](th.md) | 200 | 10,000 | 343 | 0.6229 | 0.8101 | 0.7296 | Dense |
| Yoruba | [yo](yo.md) | 119 | 10,000 | 144 | 0.5816 | 0.8416 | 0.7651 | Dense |
| Chinese | [zh](zh.md) | 200 | 10,000 | 471 | 0.4022 | 0.7191 | 0.5619 | Dense |

## Interpretation Notes for Model Researchers

Read NanoMIRACL as a controlled multilingual retrieval comparison. The task
family is stable, but the tokenizer, script, entity distribution, and Wikipedia
coverage change by language. A model that improves only English, Spanish, or
French may be learning resource-rich Wikipedia retrieval rather than robust
multilingual passage retrieval. Conversely, gains on Japanese, Chinese, Korean,
Thai, Bengali, Telugu, Swahili, or Yoruba may reveal improvements in
segmentation, multilingual representation, or low-resource transfer.

The most informative comparisons are the profile switches. Dense-led languages
show where semantic answerability helps. BM25-competitive languages show where
surface forms remain essential. Hybrid-led languages suggest complementarity
between exact anchors and embedding similarity. Because many queries have
multiple positives, nDCG@10 and Recall@100 should be inspected together: a model
can find one acceptable passage while still ranking the broader positive set
poorly.

## Training and Leakage Notes

Useful training data includes non-overlapping MIRACL training data,
language-matched Wikipedia question-to-passage pairs, open-domain QA evidence
retrieval data, and hard negatives drawn from same-article or same-entity
passages. Training should preserve the monolingual design: the query and
document should stay in the same language unless a separate cross-lingual
experiment is being run.

Leakage control is important. Exclude NanoMIRACL evaluation queries, qrels,
positive passages, and direct translations of evaluation examples. Upstream
MIRACL development or test rows should be checked for overlap before use.
Synthetic data should preserve named entities, dates, numerals, aliases,
orthography, and article-title conventions, and should include hard negatives
that share surface terms but do not answer the specific relation.

## Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984), 2022.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/), 2023.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [MIRACL corpus dataset](https://huggingface.co/datasets/miracl/miracl-corpus).
- [MIRACL source queries and qrels](https://huggingface.co/datasets/miracl/miracl).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project | https://github.com/project-miracl/miracl |
| MIRACL corpus dataset |  | dataset | https://huggingface.co/datasets/miracl/miracl-corpus |
| MIRACL source queries and qrels |  | dataset | https://huggingface.co/datasets/miracl/miracl |
