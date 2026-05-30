# NanoMTEB-Scandinavian

## Overview

NanoMTEB-Scandinavian is a compact retrieval group for Danish, Norwegian, and
Swedish tasks from the Scandinavian Embedding Benchmark ecosystem. It covers
fact verification, extractive QA answer selection, encyclopedia article lookup,
FAQ retrieval, news retrieval, and informal social question answering. The group
is small in task count, but it is not a single-domain benchmark: it moves from
highly lexical title or evidence retrieval to conversational answer retrieval
where lexical overlap is much weaker.

The group contains 1,273 queries, 9,737 task-local documents, and 1,753 positive
qrel rows. Most tasks are monolingual within one Scandinavian language, while
the group as a whole is multilingual because it spans Danish, Norwegian, and
Swedish. Its value is that it tests whether a model can handle closely related
North Germanic languages while preserving different source-task relevance
relations.

## What This Group Measures

The benchmark measures retrieval after several non-retrieval datasets have been
adapted into query-document ranking tasks. `dan_fever` retrieves Danish evidence
snippets for factual claims. `nor_quad` retrieves short Norwegian answer
strings for questions. `snl` retrieves Store norske leksikon article text from
Norwegian headwords. `swe_faq` retrieves Swedish authority FAQ answers. `swedn`
and `tv2_nordretrieval` retrieve news summaries or articles from headlines or
short summaries. `twitter_hjerne` retrieves Danish answer tweets for informal
question tweets.

The group is therefore useful for separating lexical retrieval from semantic
answer retrieval. Some tasks expose strong named entities, titles, places, or
dates. Others require matching a question to a concise answer or an informal
reply that does not repeat the same words. This creates a clear diagnostic
contrast between BM25, dense retrieval, and hybrid candidate generation.

## Task Families

- **Fact verification:** `dan_fever` retrieves Danish evidence for factual
  claims.
- **Answer selection:** `nor_quad`, `swe_faq`, and `twitter_hjerne` retrieve
  answer strings, FAQ answers, or social-media replies.
- **Encyclopedia retrieval:** `snl` retrieves Norwegian encyclopedia articles
  from short headwords.
- **News retrieval:** `swedn` and `tv2_nordretrieval` retrieve Swedish and
  Danish news documents from headlines or summaries.
- **Multi-positive retrieval:** `nor_quad`, `swedn`, and `twitter_hjerne`
  include more than one relevant document for some queries.

## Dataset Shape

The group has seven task pages. `dan_fever`, `snl`, `swe_faq`, and
`tv2_nordretrieval` are single-positive in the Nano split. `nor_quad` averages
1.48 positives per query, `swedn` has exactly two positives per query, and
`twitter_hjerne` averages 3.40 positives per query. The document pools are
small compared with many Nano sets, ranging from 262 documents for
`twitter_hjerne` to 2,522 for `dan_fever`.

Text length differs by source. `snl` has very short title-like queries and long
encyclopedia articles. `nor_quad` has compact questions and short answer
documents. `twitter_hjerne` has long informal question tweets and shorter answer
tweets. The news tasks retrieve longer article-style documents, while `swe_faq`
uses public-sector answer text. These differences should be kept visible when
comparing model behavior.

## Retrieval Behavior

### BM25 Profile

BM25 is the best nDCG@10 profile only for `dan_fever`, but it is highly
competitive on several lexical tasks. `dan_fever` reaches 0.8856 nDCG@10,
`snl` reaches 0.8781, and `tv2_nordretrieval` reaches 0.8957. These tasks expose
strong surface evidence: claims, article headwords, local place names, dates,
and news-specific entities.

BM25 is much weaker on answer-selection tasks. `nor_quad` scores only 0.1118
nDCG@10 because the positive document is often a short answer string that does
not repeat the question wording. `twitter_hjerne` also challenges BM25 because
informal replies can be useful without sharing many tokens with the question
tweet. This makes the group a good reminder that strong Scandinavian lexical
matching does not imply strong answer retrieval.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the best profile for five tasks:
`nor_quad`, `snl`, `swe_faq`, `swedn`, and `tv2_nordretrieval`. Its largest gains
are on answer and social retrieval. `nor_quad` rises from 0.1118 BM25 nDCG@10
to 0.2378 dense nDCG@10, and `twitter_hjerne` rises from 0.2395 to 0.6211 even
though hybrid remains below dense. Dense also improves `swe_faq`, where FAQ
answers can express policy or advice without repeating the user's wording.

Dense is not a replacement for lexical retrieval in every case. `dan_fever`
slightly favors BM25, indicating that claim-evidence overlap remains valuable.
Still, dense retrieval has the strongest query-weighted nDCG@10 for the group
at 0.7278, making it the most important single profile for this Nano slice.

### Reranking Hybrid Profile

The reranking hybrid profile is best only for no individual task in this group,
but it has the strongest recall@100 at 0.8878. It stays close to the best
profile on `dan_fever`, `snl`, `swe_faq`, `swedn`, and `tv2_nordretrieval`,
which means the combined candidate set is often good even when the top-10 order
is not optimal.

The weak spot is answer selection. Hybrid trails dense on `nor_quad` and
`twitter_hjerne`, suggesting that sparse evidence can dilute dense semantic
signals when the relevant answer or reply shares little vocabulary with the
query. For Scandinavian retrieval systems, this group supports hybrid candidate
generation, but it also argues for task-aware reranking or fusion when the
target is a short answer rather than a passage with lexical anchors.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [dan_fever](dan_fever.md) | Fact verification | `da` | 200 | 2,522 | 200 | 1.00 | 0.8856 | 0.8630 | 0.8832 | BM25 |
| [nor_quad](nor_quad.md) | Answer selection | `no` | 196 | 1,048 | 291 | 1.48 | 0.1118 | 0.2378 | 0.1301 | Dense |
| [snl](snl.md) | Encyclopedia retrieval | `no` | 200 | 1,300 | 200 | 1.00 | 0.8781 | 0.9599 | 0.9024 | Dense |
| [swe_faq](swe_faq.md) | FAQ answer retrieval | `sv` | 200 | 511 | 200 | 1.00 | 0.5449 | 0.6488 | 0.6395 | Dense |
| [swedn](swedn.md) | News retrieval | `sv` | 200 | 2,046 | 400 | 2.00 | 0.7081 | 0.7757 | 0.7398 | Dense |
| [tv2_nordretrieval](tv2_nordretrieval.md) | News retrieval | `da` | 200 | 2,048 | 200 | 1.00 | 0.8957 | 0.9127 | 0.8998 | Dense |
| [twitter_hjerne](twitter_hjerne.md) | Social QA retrieval | `da` | 77 | 262 | 262 | 3.40 | 0.2395 | 0.6211 | 0.4480 | Dense |

## Interpretation Notes for Model Researchers

NanoMTEB-Scandinavian is strongest as a contrast set. High BM25 performance on
`dan_fever`, `snl`, and `tv2_nordretrieval` reflects tasks with entities,
titles, claims, and news terms. Dense gains on `nor_quad`, `swe_faq`, and
`twitter_hjerne` reflect answerability and intent matching. A model that only
does well on lexical tasks may not be useful for Scandinavian FAQ or social QA.

The group also tests related-language coverage. Danish, Norwegian, and Swedish
share vocabulary and morphology, but the retrieval sources differ enough that a
single language-level conclusion can be misleading. Researchers should compare
fact verification, answer selection, encyclopedia, and news subtasks separately
before interpreting the aggregate score.

## Training and Leakage Notes

Useful training data includes Danish claim-evidence pairs, Norwegian extractive
QA and answer-selection pairs, Store norske leksikon title/article data, Swedish
FAQ and public-sector help-center pairs, Danish and Swedish headline-to-article
pairs, and Danish social QA threads. For `swedn` and `twitter_hjerne`,
multi-positive training should be preserved instead of forcing one canonical
answer.

Leakage control should exclude Nano evaluation queries, qrels, positives, tweet
threads, news article pairs, and near duplicates from SEB-related sources. Hard
negatives should be close within the same genre: nearby encyclopedia articles,
same-event news stories, related claims with changed entities or dates, similar
FAQ answers, or answer tweets from adjacent topics.

## Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396), 2024.
- [DanFEVER: claim verification dataset for Danish](https://aclanthology.org/2021.nodalida-main.47/), 2021.
- [NorQuAD: Norwegian Question Answering Dataset](https://aclanthology.org/2023.nodalida-1.17/), 2023.
- [Superlim: A Swedish Language Understanding Evaluation Benchmark](https://aclanthology.org/2023.emnlp-main.506/), 2023.
- [SweDN resource page](https://spraakbanken.gu.se/en/resources/swedn).
- [Nordjylland News datasheet](https://www.foundationmodels.dk/data/nordjyllandnews/nordjyllandnews.html).
- [#Twitterhjerne dataset card](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne).
- [strombergnlp/danfever](https://huggingface.co/datasets/strombergnlp/danfever).
- [mteb/norquad_retrieval](https://huggingface.co/datasets/mteb/norquad_retrieval).
- [mteb/SweFaqRetrieval](https://huggingface.co/datasets/mteb/SweFaqRetrieval).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | benchmark paper | https://arxiv.org/abs/2406.02396 |
| DanFEVER: claim verification dataset for Danish | 2021 | source task paper | https://aclanthology.org/2021.nodalida-main.47/ |
| NorQuAD: Norwegian Question Answering Dataset | 2023 | source task paper | https://aclanthology.org/2023.nodalida-1.17/ |
| Superlim: A Swedish Language Understanding Evaluation Benchmark | 2023 | benchmark paper | https://aclanthology.org/2023.emnlp-main.506/ |
| SweDN resource page |  | dataset page | https://spraakbanken.gu.se/en/resources/swedn |
| Nordjylland News datasheet |  | dataset page | https://www.foundationmodels.dk/data/nordjyllandnews/nordjyllandnews.html |
| #Twitterhjerne dataset card |  | dataset card | https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne |
| strombergnlp/danfever |  | dataset card | https://huggingface.co/datasets/strombergnlp/danfever |
| mteb/norquad_retrieval |  | dataset card | https://huggingface.co/datasets/mteb/norquad_retrieval |
| mteb/SweFaqRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/SweFaqRetrieval |
