# NanoMTEB-v2 / cqadupstack_gaming

## Overview

`NanoMTEB-v2 / cqadupstack_gaming` is the Gaming slice of CQADupStack duplicate-question retrieval. Short Gaming StackExchange question titles are used as queries, and candidate documents are longer posts that may ask the same or near-duplicate question. The original CQADupStack benchmark was built from StackExchange duplicate links for community question-answering research. In this slice, the retrieval problem is player-intent matching: a model must recognize that two questions concern the same game mechanic, platform constraint, quest issue, or resource rule, even when the wording differs. The Nano split contains 200 queries over 10,000 documents and includes many multi-positive queries.

## Details

### What the Original Data Measures

CQADupStack measures duplicate-question retrieval across StackExchange subforums. The positive document is a question judged to be a duplicate or near duplicate of the query. This is not answer passage retrieval: the model is matching two questions.

The Gaming subset focuses on game-specific problems, including mechanics, co-op setup, buildings, resources, creature forms, platforms, and game versions. Relevance depends on shared intent, not just shared game names.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 415 positive qrel rows. Queries have 2.075 positives on average, with a median of 1 and a maximum of 22. There are 65 multi-positive queries, or 32.5% of the query set. Queries average 47.62 characters, while documents average 481.08 characters.

The examples are short titles paired with longer StackExchange posts. Documents may include duplicate markers, quoted text, game names, tags, and explanatory body content. Some questions are highly lexical because game names repeat; others require recognizing paraphrased gameplay intent.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.5073, hit@10 of 0.6850, and recall@100 of 0.7759. BM25 is a useful baseline because titles and duplicate posts often share game names, item names, or mechanic terms.

Its limitations appear when a duplicate question phrases the same issue differently. BM25 may rank another post from the same game, or a post with the same mechanic word, above the true duplicate. The task therefore tests whether lexical matching can separate same-game topical similarity from actual duplicate intent.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.6375, hit@10 of 0.7900, and recall@100 of 0.8506. Dense retrieval is clearly stronger than BM25 across all reported metrics. This suggests that embedding similarity captures gameplay intent and question paraphrase better than term overlap alone.

Dense retrieval is still challenged by domain-specific names and mechanics. If a model lacks gaming knowledge or treats a rare game term as noise, it may miss a duplicate that BM25 can surface. The best systems need both semantic paraphrase matching and sensitivity to exact game-specific terminology.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 10 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.5970, hit@10 of 0.7800, and recall@100 of 0.8771. Hybrid retrieval provides the best recall@100, while dense retrieval remains strongest in top-rank quality.

This indicates that sparse retrieval adds complementary game-name and keyword coverage, but dense retrieval better orders the most relevant duplicates. A reranker should benefit from the hybrid pool if it can compare detailed question intent across same-game hard negatives.

### Metric Interpretation for Model Researchers

The multi-positive structure matters: some query titles have many duplicate posts, while most have only one. nDCG@10 rewards ranking any accepted duplicate highly, but recall@100 shows whether the candidate pool is broad enough for multi-positive queries.

Dense retrieval is the main first-stage baseline to beat. Hybrid retrieval is a stronger reranking pool because it captures both exact game terms and paraphrased duplicates.

### Query and Relevance Type Tendencies

Queries are short gaming question titles. Relevant documents are longer duplicate questions from Gaming StackExchange. They may discuss the same mechanic using different examples, versions, or platforms.

The relevance relation is duplicate-question equivalence. A post about the same game is not relevant unless it asks the same or near-same player question.

### Representative Failure Modes

Common failures include retrieving another question about the same game but a different mechanic, confusing platform-specific setup with general setup, over-matching popular game titles, and missing paraphrases that describe the same gameplay problem in different words. Dense systems can miss rare item or quest names; sparse systems can over-rank title overlap.

### Training Data That May Help

Useful training data includes StackExchange duplicate-question pairs, gaming forum duplicate questions, gaming FAQ pairs, and hard negatives from the same game or tag. Multi-positive training is recommended because duplicate clusters can contain many accepted variants.

### Model Improvement Notes

Models should learn duplicate intent at the question level. Hard negatives should share game names and mechanics but ask different questions. Rerankers should compare the full post body, not only the title, because duplicate evidence is often in setup details or constraints.

## Example Data

| Query | Positive document |
| --- | --- |
| How can a monk tank effectively for a group? [44 chars] | Monk skills suited for CC and tanking > **Possible Duplicate:** > How can a monk tank effectively for a group? When playing with my friends (who play ranged classes), I mostly end up tanking / crowd c... [200 / 298 chars] |
| Portal 2 Offline Co-op on Mac [29 chars] | Can we play Portal 2 co-op on one PC or Mac? Is there a way to play Portal 2 co-op on a single PC or Mac? If so, do we need two keyboards, or two mice, or what? Do we need to buy two copies of the gam... [200 / 389 chars] |
| What type of buildings offer what level of jobs? [48 chars] | Who works in medium value commercial properties? I have some §§ (medium-wealth) buildings that are closed or closing due to a lack of workers. Yet, of my 10,652 §§ workers, 3,205 are unemployed and 15... [200 / 305 chars] |
| At what rate do players and commanders receive resources per resource node? [75 chars] | How are resources gained, distributed, and spent? > **Possible Duplicate:** > At what rate do players and commanders receive resources per resource node? I'm unclear on how resources gained by aliens... [200 / 1,478 chars] |
| How many forms of Vivilion are there? [37 chars] | Vivillon's Pattern 3DS Locations - Who do I need to trade with? According to Vivillon's Pokedex Entry, they have different wing patterns depending on their original location in the world: > Vivillon w... [200 / 765 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | [https://eltimster.github.io/www/pubs/adcs2015.pdf](https://eltimster.github.io/www/pubs/adcs2015.pdf) |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| mteb/cqadupstack-gaming |  | dataset card | [https://huggingface.co/datasets/mteb/cqadupstack-gaming](https://huggingface.co/datasets/mteb/cqadupstack-gaming) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| How can a monk tank effectively for a group? | A Gaming StackExchange post about monk skills for crowd control and tanking, explicitly marked as a possible duplicate of the query. |
| Portal 2 Offline Co-op on Mac | A post asking whether Portal 2 co-op can be played on a single PC or Mac and what input devices or copies are required. |
| What type of buildings offer what level of jobs? | A city-building question about medium-wealth commercial properties and worker availability. |
| At what rate do players and commanders receive resources per resource node? | A post asking how alien and marine resources are gained, distributed, and spent. |
| How many forms of Vivilion are there? | A post about Vivillon wing patterns and 3DS locations for trading. |
