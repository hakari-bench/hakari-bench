# NanoBEIR-en / NanoMSMARCO

## Overview

NanoMSMARCO is the compact English NanoBEIR version of MS MARCO passage retrieval. Each query is a short real-world web question or search fragment, and the corpus contains concise answer-bearing web passages. The retrieval goal is to find the passage that directly answers the user's information need. This makes the task useful for evaluating open-domain web QA retrieval, noisy query handling, and answer-oriented passage ranking.

## Details

### What the Original Data Measures

MS MARCO was built from anonymized Bing search queries and web passages. Unlike datasets whose questions are written from a supplied paragraph, MS MARCO reflects real user information needs, including lowercase fragments, abbreviations, typos, ambiguous wording, and missing context. The passage-ranking task asks systems to rank answer-bearing passages for those queries.

The BEIR version includes MS MARCO as a question answering retrieval benchmark, and NanoBEIR keeps a compact English passage retrieval slice. The task is broad rather than domain-specific: questions can involve definitions, entertainment, medical terms, law, consumer advice, weather, and everyday factual lookup.

### Observed Data Profile

The task contains 50 queries, 5,043 documents, and 50 relevance judgments. Every query has one positive passage, so the positives-per-query average is 1.0, with minimum 1, median 1.0, maximum 1, and no multi-positive queries.

Queries average 32.22 characters, while documents average 330.16 characters. This is a short-query, short-passage task. Queries often contain only a few words, and the model must infer whether the user wants a definition, a factual answer, a substitution, a person, a place, or a short explanation.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5217, hit@10 of 0.7200, and recall@100 of 1.0000 using the top-500 BM25 candidate subset. The perfect recall@100 shows that lexical matching can usually place the positive passage somewhere in the candidate pool. Query terms often appear directly in the answer passage.

The lower hit@10 and nDCG@10 show that top-rank ordering is harder. BM25 can be distracted by common words, ambiguous terms, or passages that mention the query phrase without answering it. It is a strong candidate generator but not the best first-stage ranker for answer intent.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6188, hit@10 of 0.8400, and recall@100 of 1.0000. Dense retrieval is the strongest direct profile on this task by nDCG@10 and hit@10. It preserves full recall@100 while placing answer-bearing passages higher.

This is consistent with MS MARCO-style retrieval. The model must connect short user wording to passages that answer the implied question, not just share query words. Dense retrieval is better at matching definitions, paraphrases, and answer types under noisy web query phrasing.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.6170, hit@10 of 0.7600, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile nearly matches dense nDCG@10 and preserves full recall, but its hit@10 is closer to BM25.

This suggests that the hybrid candidate pool is robust for reranking, though dense retrieval is the best direct first-stage ranker. BM25 contributes exact wording and rare-term matches, while dense retrieval contributes answer-intent matching. A downstream reranker should have complete candidate access under all three profiles.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is a direct measure of whether the answer passage is visible. nDCG@10 captures how early it appears, which matters for search and RAG systems. recall@100 shows that candidate generation is not the bottleneck in this slice; ranking quality is.

The comparison shows that BM25 retrieves the answer somewhere, dense retrieval ranks it best, and reranking_hybrid provides a high-quality pool with full recall. This task is useful for testing short-query semantic answer retrieval rather than multi-positive coverage.

### Query and Relevance Type Tendencies

Queries include questions such as what rumination syndrome is, who sang "Here I Go Again", who Cameron Boyce plays in Liv and Maddie, where most of Earth's large deserts occur, and the meaning of copper as police slang. Positive passages are short web snippets that usually answer directly.

The task rewards answer-type inference and noise tolerance. Some queries are clean questions, while others are fragmentary or ambiguous. A relevant passage should resolve the user's intent, not merely repeat the query words.

### Representative Failure Modes

Likely failures include retrieving dictionary pages for the wrong sense, ranking passages that share a title but not the answer, mishandling misspellings or abbreviations, and over-valuing common query words. BM25 may be too literal, while dense retrieval may occasionally retrieve a semantically related passage that does not contain the exact answer.

### Training Data That May Help

Useful training data includes non-overlapping MS MARCO passage-ranking pairs, web QA retrieval data, search-query-to-answer-passage pairs, and noisy real user question datasets. Synthetic data should include search fragments, spelling variants, abbreviations, and everyday answer types.

### Model Improvement Notes

A model targeting this task should improve answer-bearing passage ranking for short noisy queries. Sparse systems need query expansion and robust token handling. Dense systems are the strongest direct baseline and should be trained on passage-ranking objectives. Hybrid systems are useful as reranking pools because they retain exact-match coverage while adding semantic answer matching.

## Example Data

| Query | Positive document |
| --- | --- |
| what is rumination syndrome [27 chars] | Rumination Syndrome. Rumination syndrome, also called Merycism, is a type of eating disorder not otherwise specified that causes the regurgitation of food. Even though it is not identified as a specific eating disorder in the DSM-IV, certain parameters have been outlined for diagnosing the disorder. [300 chars] |
| who sang here i go again [24 chars] | For other uses, see Here I Go Again (disambiguation). Here I Go Again is a song by British rock band Whitesnake. Originally released on their 1982 album, Saints & Sinners, the song was re-recorded for their eponymous 1987 album Whitesnake. The song was re-recorded again that year in a new radio-mix version. [308 chars] |
| who does cameron boyce play in liv and maddie [45 chars] | Get ready for some serious LOLs, you guys. In an EXCLUSIVE sneak peek at the Apr. 19 episode of Liv & Maddie called “Prom-A-Rooney.” Obviously. In the hilarious clip, we see Jessie star Cameron Boyce hop over to a different Disney show to meet Maddie (Shelby Wulfert). His character is, um, eccentric! [301 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [MS MARCO](https://arxiv.org/abs/1611.09268) |
| Dataset site | [MS MARCO dataset site](https://microsoft.github.io/msmarco/Datasets.html) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive answer snippets:

| Query | Positive document snippet |
| --- | --- |
| what is rumination syndrome | Rumination syndrome, also called Merycism, is a disorder that causes regurgitation of food. |
| who sang here i go again | Here I Go Again is a song by British rock band Whitesnake. |
| who does cameron boyce play in liv and maddie | A preview of Liv & Maddie shows Cameron Boyce appearing in the episode Prom-A-Rooney. |
| where do most of earth's large deserts occur | The rest of Earth's deserts are outside the polar areas, with the Sahara as the largest. |
| meaning of copper for a policeman | Copper, meaning a policeman, appears to predate cop in current findings. |
