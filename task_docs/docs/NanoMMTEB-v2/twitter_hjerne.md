# NanoMMTEB-v2 / twitter_hjerne

## Overview

`NanoMMTEB-v2 / twitter_hjerne` is a Danish social-media answer retrieval task.
Queries are Danish #Twitterhjerne help-seeking tweets, and documents are human
reply tweets. The Nano split has 77 queries, 262 documents, and 262 positive
qrel rows. It is strongly multi-positive, averaging 3.40 useful replies per
query. Current diagnostics show dense retrieval as much stronger than BM25,
`reranking_hybrid` as second, and BM25 as limited because useful replies often
introduce new advice or recommendations rather than repeating the question
wording.

## Details

### What the Original Data Measures

The upstream Danish #Twitterhjerne dataset contains questions asked on
Twitter/X with the `#Twitterhjerne` hashtag and their answers. The Scandinavian
Embedding Benchmarks include it as a Danish retrieval task where social-media
questions are matched to relevant replies.

The task measures informal answer retrieval in Danish. A model must connect a
help-seeking tweet to replies that solve, recommend, clarify, or advise, even
when the reply uses short informal wording.

### Observed Data Profile

The Nano split contains 77 queries, 262 documents, and 262 positive qrel rows.
Almost every query has multiple positives: average positives per query is 3.40,
with a minimum of 1, median of 3, and maximum of 6. The metadata records 97.40%
of queries as multi-positive. Queries average 165.75 characters, while reply
documents average 128.77 characters.

The text is informal Danish with hashtags, URLs, emojis, product names, places,
recommendations, and troubleshooting advice. Examples include questions about
non-Danish potatoes, media monitoring services, PS5 controller charging, heavy
cream, and family photo sharing.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains all 262 documents per query
and achieves nDCG@10 = 0.2395, hit@10 = 0.6104, and recall@100 = 0.6527. BM25
is useful when queries and replies share product names, places, brands, or
specific hashtags.

However, BM25 is clearly weaker than dense retrieval. Replies often answer by
introducing a recommendation, short advice, or new term that does not appear in
the question. Social-media spelling, abbreviations, and conversational tone
also reduce exact lexical overlap.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains all 262 documents per
query and achieves nDCG@10 = 0.6243, hit@10 = 0.9221, and recall@100 = 0.9046.
Dense retrieval is the strongest observed profile.

This indicates that semantic matching is central. A dense model can connect a
question about where to buy an item, how to fix a device, or which service to
use with a short reply that gives the answer without repeating much of the
question.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.4402, hit@10 = 0.8182, and recall@100 = 0.8702. Hybrid retrieval improves
substantially over BM25 but remains below dense retrieval.

The hybrid profile suggests that sparse matching adds some useful named-entity
anchors, but the task is dense-first. Lexical signal can also emphasize words
that are incidental rather than answer-bearing in informal replies.

### Metric Interpretation for Model Researchers

This is a multi-positive task. nDCG@10 rewards ranking several useful replies
early, while hit@10 only checks whether at least one useful reply appears near
the top. Recall@100 measures whether useful replies remain available to a
reranker.

Because nearly every query has multiple valid replies, training and evaluation
should preserve the multi-answer structure. Collapsing the task to one canonical
reply would underrepresent the social-media answer setting.

### Query and Relevance Type Tendencies

Queries are Danish help-seeking tweets about recommendations, shopping,
troubleshooting, food substitutions, services, technology, travel, and household
problems. Relevant documents are short Danish reply tweets that give advice,
recommendations, or direct answers.

The task rewards informal Danish understanding, recommendation matching, and
short-answer semantics. It penalizes models that rely only on repeated
keywords.

### Representative Failure Modes

BM25 can miss replies that are useful but lexically short or introduce new
terms. Dense retrieval can rank generally plausible advice that does not answer
the specific need. Hybrid retrieval can overvalue shared brand or topic words
while missing the best practical recommendation.

Rerankers should check whether the reply actually addresses the user need and
whether it is a recommendation, troubleshooting step, clarification, or direct
answer.

### Training Data That May Help

Useful training data includes Danish social-media QA pairs, Danish forum
question-reply data, community-support and recommendation threads, and
multi-positive answer retrieval data. The Nano split's question tweets, reply
tweets, and qrels should be excluded from training.

Synthetic data can generate informal Danish questions asking for
recommendations, troubleshooting, shopping advice, travel tips, or household
help. Several plausible reply tweets should be generated for each question.
Negatives should be plausible replies to adjacent topics but not useful for the
specific query.

### Model Improvement Notes

Dense retrievers should improve informal Danish semantics and short-reply
matching. Sparse systems should preserve product names and hashtags but need
semantic expansion. Rerankers should be trained with multi-positive objectives
and same-topic but unhelpful replies.

For hybrid systems, `NanoMMTEB-v2 / twitter_hjerne` shows that dense retrieval
is the dominant signal. Hybrid search may help coverage, but top-rank quality
requires modeling conversational usefulness.

## Example Data

| Query | Positive document |
| --- | --- |
| Hej #Twitterhjerne & twitterfolkens (- eller X'ere, whatever 😊) Er der nogen der kan fortælle mig hvor jeg kan købe IKKE-danske kartofler? Hverken Rema1000, Netto, Kvickly ell SuperBrugsen sælger andet end danske. (Jeg ønsker ikke at spise det hjerneskadende pesticid Reglone) [278 chars] | Økologiske er vel ok? [21 chars] |
| Hvis I betaler for medieovervågning på arbejdet - hvem bruger I så, og er I tilfredse? #dkmedier #dkbiz #twitterhjerne [118 chars] | Infomedia - og mnjah [20 chars] |
| Er der andre der døjer med samme problem som mig, min controller til ps5 lader maks 1 streg om natten. Hver gang jeg sidder og spiller disconneter den hele tiden, jeg har ikke gjort noget ved den. Den havde det allerede 1 uge efter jeg fik konsollen. [250 chars] | Du skal bare indlevere den, hvor du har købt, så får du en ny [61 chars] |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396),
  2024.
- [sorenmulli/da-hashtag-twitterhjerne](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne).
- [mteb/TwitterHjerneRetrieval](https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | benchmark paper | [https://arxiv.org/abs/2406.02396](https://arxiv.org/abs/2406.02396) |
| sorenmulli/da-hashtag-twitterhjerne | 2024 | dataset card | [https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne](https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne) |
| mteb/TwitterHjerneRetrieval | 2024 | dataset card | [https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval](https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Danish tweet asking where to buy non-Danish potatoes. | A short reply suggesting organic potatoes may be acceptable. |
| A question asking which media monitoring service people use. | A reply naming Infomedia with a brief evaluation. |
| A PS5 controller troubleshooting tweet. | A reply advising returning it to the seller for replacement. |
| A food question asking whether heavy cream equals whipping cream. | A reply discussing heavy cream's fat percentage. |
| A question asking how to share family photos without Google Photos or iCloud. | A reply recommending OneDrive and describing backup use. |
