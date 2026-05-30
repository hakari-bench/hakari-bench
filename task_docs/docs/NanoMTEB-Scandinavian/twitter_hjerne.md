# NanoMTEB-Scandinavian / twitter_hjerne

## Overview

`twitter_hjerne` is the Danish NanoMTEB-Scandinavian retrieval adaptation of the `#Twitterhjerne` social-media question-answer dataset. The source data consists of Danish help-seeking question tweets and human reply tweets. In retrieval form, the query is a question tweet and the relevant documents are reply tweets that attempt to answer it. This makes the task informal, multi-positive Danish answer retrieval.

The Nano split contains 77 queries, 262 documents, and 262 positive relevance judgments. Queries average about 166 characters, while reply documents average about 129 characters. Almost every query is multi-positive: 75 of 77 queries have more than one positive, the median is 3 positives, and the maximum is 6. The task covers technology help, shopping, workplace tools, food substitutions, family photo sharing, travel, children's activities, household problems, and recommendations.

## Details

### What the Original Data Measures

The source dataset collects Danish questions posted with the `#Twitterhjerne` hashtag and their human answers. The thesis and dataset card describe the data as small, informal Danish help or input requests, filtered to have clear questions, no required attached image, no personal information, and multiple relevant replies. The retrieval adaptation preserves that structure: multiple replies can be valid positives for the same query.

This differs from factoid QA and duplicate-question retrieval. A relevant answer may be short, subjective, partial, advisory, or recommendation-oriented. The model must retrieve useful replies, not a single canonical answer.

### Observed Data Profile

The data is small and informal. Tweets may include hashtags, URLs, abbreviations, platform names, spelling variation, and conversational wording. Queries are often longer than replies because the question includes context, constraints, and social framing. Replies may be terse, such as a product name, a recommendation, or a short suggestion.

The multi-positive structure is central. A question can have several acceptable answers, especially for recommendations or practical advice. Evaluation should therefore reward models that retrieve a set of useful replies rather than only one best answer.

### BM25 Evaluation Profile

BM25 is weak to moderate, with nDCG@10 of 0.2395, hit@10 of 0.6104, and recall@100 of 0.6527. It can retrieve answers when the reply repeats a product name, platform name, or key term from the question. For example, a question about media monitoring may retrieve a reply naming a service if vocabulary overlaps.

However, many useful replies do not repeat the question wording. A question about a PS5 controller can be answered with advice to return it to the store. A question about photo sharing can be answered with `OneDrive`. A question about heavy cream can be answered by explaining fat percentage. BM25 misses many of these because the answer is semantically useful but lexically sparse.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is clearly strongest, with nDCG@10 of 0.6211, hit@10 of 0.9091, and recall@100 of 0.9008. Dense retrieval is well suited to this task because it can map a help-seeking question to an advisory reply even when the words differ. It can represent recommendation, troubleshooting, and substitution relations that are difficult for lexical matching.

This is one of the strongest dense-favorable profiles in the Scandinavian set. The gap from BM25 shows that informal social QA depends heavily on semantic answer usefulness rather than term overlap.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.4480, hit@10 of 0.8182, and recall@100 of 0.8664. Candidate lists contain 100 to 101 items, and 2 rows use the positive safeguard. Hybrid retrieval improves substantially over BM25 but remains below dense retrieval across the reported metrics.

This suggests that lexical candidates add some value but also introduce conversational or topical distractors. Dense retrieval alone is better at ranking useful replies near the top. Hybrid retrieval can still be useful as a candidate pool, but it is not the strongest final ranking for this task.

### Metric Interpretation for Model Researchers

This split is strongly dense-favorable. BM25 underperforms because question tweets and answer tweets often have different vocabulary. `reranking_hybrid` narrows the gap but does not exceed dense retrieval. A model that performs well here likely captures pragmatic answer relations: recommendation, troubleshooting, substitution, and short advice.

Because almost all queries have multiple positives, recall@100 and nDCG@10 both matter. The task does not require selecting one canonical answer. It rewards retrieving several useful replies. Hit@10 alone can hide whether the model retrieves a broad set of relevant responses.

### Query and Relevance Type Tendencies

Representative queries ask where to buy non-Danish potatoes, which media-monitoring service people use at work, how to handle a PS5 controller that barely charges, whether English `heavy cream` corresponds to Danish whipping cream, and how to share family photos without Google Photos or iCloud. Relevant replies are often short suggestions, service names, or practical advice.

The task includes subjective and contextual answers. A recommendation can be valid even if it does not repeat the question's constraints. A troubleshooting reply can be useful with only a few words. Models must infer the usefulness relation.

### Representative Failure Modes

BM25 may retrieve replies that repeat a word from the question but do not answer it. Dense retrieval may retrieve plausible advice for a nearby topic but not the specific constraint. Hybrid retrieval can include both lexical false positives and broad semantic neighbors.

Another failure mode is ignoring constraints. A query may exclude Google Photos or iCloud, ask for non-Danish potatoes, or specify a workplace context. A relevant answer must respect those constraints. Short reply tweets can make this difficult.

### Training Data That May Help

Useful training data includes Danish forum question-reply pairs, Danish social-media QA pairs, community-support and recommendation threads, and multi-positive answer retrieval examples. Training should preserve multiple human replies as positives rather than collapsing them into one answer.

Hard negatives should be plausible replies to nearby topics but not useful for the specific question. For example, a photo-sharing recommendation that violates the user's constraints is a stronger negative than an unrelated tweet.

### Model Improvement Notes

Dense models can improve by representing informal Danish, hashtags, abbreviations, and pragmatic answer relations. Sparse systems have limited upside unless replies repeat question terms. Hybrid systems may help candidate recall, but final ranking benefits most from semantic answer matching.

For reranking, this task rewards models that can judge whether a short reply actually helps with the query. Multi-positive training and evaluation are important because several different replies can all be relevant.

## Example Data

### Public Sources

- Scandinavian Embedding Benchmarks paper: https://arxiv.org/abs/2406.02396
- Are GLLMs Danoliterate? thesis: https://sorenmulli.github.io/thesis/thesis.pdf
- Source dataset card: https://huggingface.co/datasets/sorenmulli/da-hashtag-twitterhjerne
- MTEB task dataset card: https://huggingface.co/datasets/mteb/TwitterHjerneRetrieval

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| Scandinavian Embedding Benchmarks | Retrieval benchmark adaptation. |
| Danoliterate thesis | Danish dataset context and filtering description. |
| Source dataset card | `#Twitterhjerne` question and answer tweet data. |
| MTEB task card | Retrieval task packaging. |

### Representative Snippets

- A query asks where to buy non-Danish potatoes; a relevant reply suggests organic ones may be acceptable.
- A query asks which media-monitoring provider people use at work; a relevant reply names Infomedia with a qualified opinion.
- A query asks about a PS5 controller that barely charges and disconnects; a relevant reply advises returning it to the store for replacement.
- A query asks whether English `heavy cream` corresponds to Danish whipping cream; a relevant reply discusses fat percentage.
- A query asks for family photo sharing without Google Photos or iCloud; a relevant reply recommends OneDrive and mentions Jottacloud for backup.
