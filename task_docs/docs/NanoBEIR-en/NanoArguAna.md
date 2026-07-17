# NanoBEIR-en / NanoArguAna

## Overview

NanoArguAna is the compact English NanoBEIR version of ArguAna, an argument retrieval task where each query is a long debate argument and the relevant document is its best counterargument. The retrieval target is not a duplicate, summary, or supporting passage. It is an opposing argument that addresses the same topic and aspects while challenging the query's claim, premise, consequence, or policy framing. This makes the task useful for evaluating stance-aware retrieval, long argumentative text matching, and counterargument selection.

## Details

### What the Original Data Measures

ArguAna was introduced for retrieving the best counterargument without prior topic knowledge. The original formulation assumes that a good counterargument should be related to the same debate issue but should oppose the query argument's stance or reasoning. This makes the task different from ordinary semantic similarity, because a passage that is too similar in stance may be a bad result.

The BEIR version frames ArguAna as argument retrieval, and the NanoBEIR version keeps the long-form debate structure in a compact sample. A model must read enough of each passage to identify the claim, premises, examples, and argumentative target. Simple topical matching is often necessary but not sufficient.

### Observed Data Profile

The task contains 50 queries, 3,635 documents, and 50 relevance judgments. Each query has exactly one positive counterargument, so the positives-per-query average is 1.0, with minimum 1, median 1.0, maximum 1, and no multi-positive queries.

The text is much longer than most NanoBEIR tasks. Queries average 1,201.78 characters, and documents average 1,011.79 characters. Both sides often contain titles, claims, evidence, examples, citations, and policy implications. The retrieval problem is therefore long-passage argument matching rather than short query search.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4650, hit@10 of 0.7600, and recall@100 of 1.0000 using the top-500 BM25 candidate subset. The perfect recall@100 shows that lexical matching is very effective at candidate generation. Debate pairs usually share topic vocabulary, named entities, policy terms, and issue-specific phrases.

The weaker nDCG@10 shows the core difficulty. BM25 can find the right topic but may rank same-side arguments, broad topical discussions, or near-duplicates above the actual counterargument. The task requires recognizing an opposing move, not merely repeated words.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5787, hit@10 of 0.9200, and recall@100 of 0.9400. Dense retrieval is the strongest direct top-rank profile. It substantially improves hit@10 and nDCG@10 over BM25, which suggests that embedding similarity helps capture argumentative relatedness beyond exact term overlap.

The recall@100 drop relative to BM25 is still important. Dense retrieval is better at placing good counterarguments near the top when it finds them, but it misses some positives from the top-100 candidate window. This is a typical tradeoff for long argumentative text: semantic matching improves ordering, while sparse matching preserves exact topical coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5422, hit@10 of 0.8800, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard rows. The hybrid profile restores BM25's complete recall@100 while retaining much of the dense top-10 improvement.

This makes reranking_hybrid the most attractive candidate pool for downstream counterargument reranking. BM25 contributes reliable topic and phrase coverage, while dense retrieval contributes broader argument similarity. A second-stage model trained for stance and attack relations should benefit from the complete candidate coverage.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is easy to interpret: the intended counterargument is either visible or not. nDCG@10 captures how early it appears, which matters for practical argument search. recall@100 indicates whether a reranker has access to the positive.

The comparison shows that BM25 is best for candidate completeness, dense retrieval is best for direct top-rank ordering, and reranking_hybrid combines complete recall with stronger top-rank behavior than BM25. This task is useful for testing whether a model can retrieve opposition, not just semantic similarity.

### Query and Relevance Type Tendencies

Queries cover debates about constitutional reform, airport expansion, consumer choice, cyber attacks, religious speech, health policy, education, and international affairs. The positive document usually addresses the same debate issue while challenging a premise, feasibility claim, value judgment, or predicted consequence.

The task rewards recognizing argumentative structure. A relevant passage may repeat many query terms, but it must function as a counterargument. Same-topic same-stance passages are especially dangerous negatives.

### Representative Failure Modes

Likely failures include retrieving support arguments instead of counterarguments, over-ranking the query-side position, matching on topic vocabulary while missing stance, and failing to process long passages where the decisive counterpoint appears late. BM25 may be too lexical, while dense retrieval may treat related support and opposition as similarly relevant.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs, debate portal pro/con responses, argument attack and support relation datasets, stance-classified arguments, and hard negatives from same-topic same-stance passages. Training data should avoid upstream ArguAna or idebate pairs that overlap the evaluation material.

### Model Improvement Notes

A model targeting this task should combine long-document topical recall with explicit stance and attack-relation awareness. Sparse systems need robust long-passage term handling. Dense systems need counterargument-specific positives and same-topic support negatives. Hybrid systems are promising because the observed candidate pool keeps full recall while improving over pure lexical ranking.

## Example Data

| Query | Positive document |
| --- | --- |
| The public is apathetic to reform. Whether or not reform of the House of Lords should be a top priority in the current economic climate is debateable, let alone whether or not a coalition government would be able to initiate and drive through such measures. Attempts to reform the House of Lords have been delayed time and time again, demonstrating the House of Commons’ reservations on change. [1] A feeling that is no doubt echoed in popular British opinion – as demonstrated by the recent outcome... [500 / 799 chars] | The AV campaign cannot be compared to reform to the House of Lords, furthermore one should not mistake a misinformed public due to political spin, with apathy. Often voters express that they are apathetic because they feel that they can’t change anything, that there vote won’t count: reform that ensures the people running the country are directly elected by the people would help to counter these feelings. [408 chars] |
| The expansion of Heathrow is vital for the economy Expanding Heathrow would ensure many current jobs as well as creating new ones. Currently, Heathrow supports around 250,000 jobs. [1] Added to this many hundreds of thousands more are dependent upon the tourist trade in London which relies on good transport links like Heathrow. Loosing competitiveness in front of other European airports not only could imply wasting the possibility to create new jobs, but lose some of those that already exist. Ex... [500 / 1,421 chars] | The business community is far from united in its supposed support of a third run-way. Surveys suggest that many influential businesses in fact do not support expansion. A letter expressing concern was signed by Justin King the Chief Executive of J Sainsbury and BskyB’s James Murdoch. [1] Therefore to conflate the business community as one voice calling for expansion is misguided. We should also remember, when considering the alternatives to Heathrow’s new run-way such as a new runway at another London airport or a completely new airport, that these would likely have a similar economic impact as the Heathrow expansion would. If it is the connections that matter to bring in business and tourists then so long as the connection is with London it does not matter which airport the connection is from. There may even be less need for the airport to be a hub airport if we are focused on benefits to London as Bob Ayling, former British Airways Chief Executive stated Heathrow should be focused on... [1,000 / 1,330 chars] |
| People are given too much choice, which makes them less happy. Advertising leads to many people being overwhelmed by the endless need to decide between competing demands on their attention – this is known as the tyranny of choice or choice overload. Recent research suggests that people are on average less happy than they were 30 years ago - despite being better off and having much more choice of things to spend their money on1. The claims of adverts crowd in on people, raising expectations about... [500 / 1,031 chars] | People are unhappy because they can't have everything, not because they are given too much choice and find it stressful. In fact, advertisements play a crucial role in ensuring that what money people have, they spend on the most appropriate product for themselves. If advertisements were not permitted, people would waste money on an initial product when, given the choice, they clearly would go for another. A meta-analysis incorporating research from 50 independent studies found no meaningful connection between choice and anxiety, but speculated that the variance in the studies left open the possibility that choice overload could be tied to certain highly specific and as yet poorly understood pre-conditions1. 1 ^ Scheibehenne, Benjamin; Greifeneder, R. &amp; Todd, P. M. (2010). "Can There Ever be Too Many Options? A Meta-Analytic Review of Choice Overload" . Journal of Consumer Research 37: 409-425. [912 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Source dataset card | [mteb/arguana](https://huggingface.co/datasets/mteb/arguana) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and counterargument snippets:

| Query | Positive document snippet |
| --- | --- |
| The public is apathetic to reform of the House of Lords. | The AV campaign cannot be compared to reform to the House of Lords, and political spin should not be mistaken for apathy. |
| The expansion of Heathrow is vital for the economy. | The business community is far from united in its support of a third runway. |
| People are given too much choice, which makes them less happy. | People are unhappy because they cannot have everything, not because choice itself is stressful. |
| Cyber attacks are often carried out by non-state actors. | In cases involving non-state actors, a state may still retaliate if another state is unwilling or unable to act. |
| Religious certainty can justify hatred, so free speech must come second. | Nobody is forced to commit violence by another person's words, and responsibility remains with the actor. |
