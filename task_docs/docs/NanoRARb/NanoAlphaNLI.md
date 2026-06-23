# NanoRARb / NanoAlphaNLI

## Overview

`NanoAlphaNLI` is an English reasoning-as-retrieval task from NanoRARb. It recasts AlphaNLI abductive commonsense reasoning as retrieval: the query contains the beginning and ending observations of a short story, and the retriever must find the missing explanatory event from a large answer pool. Each query has one positive answer. Dense retrieval is much stronger than BM25 because the correct hypothesis is often causally plausible rather than lexically obvious, while the hybrid pool improves coverage but trails dense top-rank quality.

## Details

### What the Original Data Measures

RAR-b converts reasoning tasks into full answer retrieval. AlphaNLI originates from the Abductive Commonsense Reasoning task, where a system selects the most plausible hypothesis connecting two observations. The retrieval version tests whether that missing event can be found among many short candidate explanations.

The task measures narrative and causal plausibility. A relevant document is not a source passage; it is the best explanatory bridge between a story's start and end.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 103.79 characters, and candidate explanations average 43.84 characters.

Queries are formatted with `Start:` and `End:` fields. Examples include moving away from New York, tripping over untied shoelaces, wanting a game at Target, disliking karate class, and winning a spelling bee after practice. Candidate documents are short story middle events.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3288, hit@10 of 0.4650, and recall@100 of 0.6750. BM25 is moderately useful because the correct hypothesis may repeat characters, places, or objects from the observations.

However, lexical overlap is not enough. Many wrong candidates mention the same people or objects but do not explain the ending. The task requires identifying the event that makes the transition plausible.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.5898, hit@10 of 0.7900, and recall@100 of 0.9150. Dense retrieval is much stronger than BM25 across all metrics. Embedding similarity captures narrative continuity and causal relationships better than exact word matching.

This is the strongest standalone profile. It suggests that AlphaNLI is well suited to semantic retrieval, although ranking the single best explanation among many plausible short events remains nontrivial.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 21 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.4777, hit@10 of 0.6500, and recall@100 of 0.8950. Hybrid retrieval improves over BM25 and nearly matches dense recall@100, but it is weaker than dense retrieval at top-rank ordering.

The pattern indicates that lexical overlap adds coverage but can pull in distractors that mention the same story entities. Dense retrieval remains the better first-stage ranker, while hybrid retrieval can be useful for reranking coverage.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 reflects how early the correct missing event appears, hit@10 measures whether it is in the first ten candidates, and recall@100 measures whether a reranker can access it.

For AlphaNLI, dense retrieval is the baseline to beat. Improvements should focus on abductive plausibility and causal story coherence, not only entity overlap.

### Query and Relevance Type Tendencies

Queries provide two observations: a starting situation and an ending outcome. Relevant documents are short hypotheses that explain the transition. They often involve a decision, accident, emotional response, preparation, or discovery.

Relevance is explanatory. A candidate can share a character or object with the query and still be wrong if it does not make the ending plausible.

### Representative Failure Modes

Common failures include choosing an event that repeats query entities but does not explain the end, selecting a plausible event with the wrong emotional consequence, failing to infer a causal accident, and confusing preparation with outcome. BM25 overweights repeated names; dense retrieval can rank generic plausible events above the exact story bridge.

### Training Data That May Help

Useful training data includes abductive commonsense QA, story cloze tasks, narrative continuation, retrieval-formatted hypothesis selection, and hard negatives that mention the same people or objects but fail the causal bridge. Evaluation questions and candidate answers should be excluded.

### Model Improvement Notes

Models should learn query-to-hypothesis coherence over short text. Hard negatives should be fluent and lexically similar but causally wrong. Because the documents are short hypotheses, training should emphasize narrative entailment and abductive reasoning rather than passage-level semantic similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Start: Scott has felt increasingly unhappy in his last few Year's in New York. End: Driving out of New York, Scott feels both relieved and nostalgic. [149 chars] | The daily grind, extreme traffic and rude city dwellers left Scott longing for small town living. [97 chars] |
| Start: Joe's mother bugged him constantly to tie his shoelaces. End: As he lay at the bottom of the stairs he wished he'd listened. [131 chars] | Joe tripped down the stairs with his shoes untied. [50 chars] |
| Start: Alex was at target with his mom. End: He begged his mother to buy it until she gave in. [94 chars] | Alex saw a game he really wanted. [33 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Abductive Commonsense Reasoning | 2019 | arXiv paper | [https://arxiv.org/abs/1908.05739](https://arxiv.org/abs/1908.05739) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Start: Scott is unhappy in New York. End: Leaving New York, he feels relieved and nostalgic. | The daily grind, traffic, and rude city dwellers left him wanting small-town life. |
| Start: Joe's mother told him to tie his shoelaces. End: At the bottom of the stairs, he wished he had listened. | Joe tripped down the stairs with his shoes untied. |
| Start: Alex was at Target with his mother. End: He begged until she bought it. | Alex saw a game he really wanted. |
| Start: Ali's mother enrolled her in karate. End: Ali was embarrassed and told no friends. | Ali did not want to take karate. |
| Start: Mia could spell well. End: She won the spelling bee and felt more confident. | She studied hard because she wanted to spell. |
