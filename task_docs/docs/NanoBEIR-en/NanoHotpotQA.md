# NanoBEIR-en / NanoHotpotQA

## Overview

NanoHotpotQA is the compact English NanoBEIR version of HotpotQA, a multi-hop question answering retrieval task built from Wikipedia. Each query is a question whose answer depends on evidence from two supporting documents. The retrieval goal is to surface both documents needed for the reasoning path, not merely one answer-bearing page. This makes the task useful for evaluating bridge-entity retrieval, comparison questions, multi-positive ranking, and evidence completeness for explainable QA.

## Details

### What the Original Data Measures

HotpotQA was designed to require reasoning over multiple Wikipedia documents. The original dataset includes bridge questions, where one page points to another through an intermediate entity, and comparison questions, where two entities must be compared on a shared property. Supporting facts make the evidence path explicit.

The BEIR version frames this as a retrieval task: the question is the query, and the retriever must rank the supporting documents. The NanoBEIR version keeps the two-positive structure. A strong model should retrieve the complete evidence pair, because downstream QA may fail if only the easiest entity page is present.

### Observed Data Profile

The task contains 50 queries, 5,090 documents, and 100 relevance judgments. Every query has exactly 2 positives, so the average is 2.0, the minimum is 2, the median is 2.0, the maximum is 2, and all 50 queries are multi-positive.

Queries average 88.34 characters, while documents average 349.63 characters. Queries are longer and more compositional than ordinary factoid search. Documents are short Wikipedia-style entity descriptions, and positives usually form a bridge chain or a pair of compared entities.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8270, hit@10 of 1.0000, and recall@100 of 0.9600 using the top-500 BM25 candidate subset. This is a very strong lexical profile. Many HotpotQA questions contain explicit entity names, titles, dates, or other anchors that appear in at least one supporting document.

The key caveat is that hit@10 can be satisfied by only one of the two required positives. BM25 often retrieves the most obvious entity page quickly, but the task also requires the bridge or comparison partner. nDCG@10 and recall@100 are therefore more informative than hit@10 alone.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8043, hit@10 of 0.9400, and recall@100 of 0.9100. Dense retrieval is strong, but it is weaker than BM25 on this English slice. This suggests that exact entity and title matching remain highly valuable for HotpotQA-style retrieval.

Dense retrieval still contributes useful semantic matching for bridge relations and comparison framing. It can help when the supporting page does not repeat the most visible query terms. However, if the model underweights exact entity anchors, it may miss one of the required support pages.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.8325, hit@10 of 0.9600, and recall@100 of 0.9700. It uses exactly 100 candidates per query, with no safeguard rows. This is the strongest profile by nDCG@10 and recall@100, while BM25 has the highest hit@10.

The hybrid result shows that multi-hop retrieval benefits from combining lexical entity capture with semantic relation coverage. BM25 finds obvious names and titles, while dense retrieval helps recover less explicit bridge pages. The hybrid pool is the best observed candidate set for downstream multi-hop reranking.

### Metric Interpretation for Model Researchers

Because every query has two positives, hit@10 is not enough to judge task success. It only shows that at least one supporting document appears. nDCG@10 better reflects whether both positives are ranked near the top, and recall@100 measures whether a reranker can access the complete evidence pair.

The comparison shows that BM25 is extremely strong for entity anchoring, dense retrieval is slightly weaker as a direct ranker, and reranking_hybrid gives the best multi-positive candidate profile. This task is useful for testing whether retrieval models support complete reasoning paths.

### Query and Relevance Type Tendencies

Queries ask questions such as which actor appeared in a sitcom with Penny Rae Bridges, who gave Kaganoi Shigemochi a blade, which film was written and directed by Joby Harold with music by Samuel Sim, the date of a specific Clemson-Oklahoma football game, and what name Supersuckers used for country shows. Relevant documents usually include one page that identifies an intermediate entity and another that supplies the final attribute.

The task rewards entity tracking, bridge resolution, and comparison handling. A model that retrieves only the page named in the query may still miss the page that completes the reasoning chain.

### Representative Failure Modes

Likely failures include retrieving only one of the two supporting documents, over-ranking pages about a mentioned entity that lack the needed bridge fact, missing the less lexical comparison partner, and confusing similarly titled works or people. BM25 may over-focus on obvious names, while dense retrieval may miss exact anchors.

### Training Data That May Help

Useful training data includes non-overlapping HotpotQA examples with supporting facts, multi-hop QA retrieval datasets, Wikipedia hyperlink graph retrieval pairs, and question-to-multiple-document supervision. Single-hop QA data can help entity matching but does not fully teach evidence-pair retrieval.

### Model Improvement Notes

A model targeting this task should optimize for complete support coverage, not just first-positive visibility. Sparse systems need robust title and entity indexing. Dense systems need multi-hop positives and bridge hard negatives. Hybrid systems are promising because the observed profile best preserves both entity anchors and semantic bridge coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Penny Rae Bridges starred in a television sitcom with what other actor? [71 chars] | Penny Rae Bridges (born July 29, 1990) is an American actress. Her television work has included roles in "For Your Love", "Family Law", "Boy Meets World" and "The Parent 'Hood". She is best known for her role in "Half & Half", as the young Mona. [245 chars] |
| Who bestowed Kaganoi Shigemochi with a blade made by the person that founded the Muramasa school? [97 chars] | Kaganoi Shigemochi (加賀井 重望 , 1561 – August 27, 1600) was a Japanese samurai of the Azuchi-Momoyama period, who served the Oda clan. He ruled Kaganoi Castle. During the Battle of Komaki and Nagakute, Shigemochi fought under his father Shigemune, who was attached to the forces of Oda Nobukatsu. Soon after, Kaganoi Castle was surrounded by the forces of Toyotomi Hideyoshi; Shigemune surrendered, and Shigemochi was employed by Hideyoshi as a messenger, receiving a stipend of 10,000 "koku". He also possessed a blade made by Muramasa, which Hideyoshi bestowed on him in 1598. [575 chars] |
| What film was written and directed by Joby Harold with music written by Samuel Sim? [83 chars] | Samuel Sim is a film and television composer. He first gained recognition with his award winning score for the BBC drama series "Dunkirk". Since then he has written the music for a wide variety of film and television productions, most recently scoring the film "Awake" for The Weinstein Company and the BBC/HBO drama series "House of Saddam". His most recent acclaimed music is the soundtrack for Home Fires. Home Fires (Music from the Television Series) released May 6, 2016 by Sony Classical Records. [502 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset paper | [HotpotQA](https://arxiv.org/abs/1809.09600) |
| Project site | [HotpotQA official site](https://hotpotqa.github.io/) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive evidence snippets:

| Query | Positive document snippet |
| --- | --- |
| Penny Rae Bridges starred in a television sitcom with what other actor? | Penny Rae Bridges is an American actress with television roles including For Your Love and Family Law. |
| Who bestowed Kaganoi Shigemochi with a blade made by the person that founded the Muramasa school? | Kaganoi Shigemochi was a Japanese samurai of the Azuchi-Momoyama period. |
| What film was written and directed by Joby Harold with music written by Samuel Sim? | Samuel Sim is a film and television composer known for scores across film and television. |
| What is the date played of this college football game at Sun Life Stadium? | The 2015 Clemson Tigers football team represented Clemson University in the 2015 season. |
| Devil's Food is a singles compilation by an American rock and roll band that also played country shows under what name? | Devil's Food is a singles compilation by the American rock and roll band Supersuckers. |
