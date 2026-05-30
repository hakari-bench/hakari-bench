# MNanoBEIR / NanoBEIR-sr / NanoTouche2020

## Overview

NanoTouche2020 in the Serbian NanoBEIR slice is an argument retrieval task derived from the Touché 2020 shared task. The queries are Serbian translated controversial questions, and the corpus contains Serbian translated argumentative passages. The retrieval goal is to find passages that provide relevant arguments for the debate topic, not merely documents that mention the same issue. This makes the task a compact benchmark for argumentative search, stance-aware retrieval, and broad multi-positive ranking in a multilingual setting.

## Details

### What the Original Data Measures

Touché 2020 evaluates retrieval for controversial questions where users need arguments, evidence, and perspectives. Relevance is tied to whether a passage contributes to the debate, often by supporting or opposing a position or by addressing a particular aspect of the issue. The task is therefore different from fact lookup: many passages can be relevant, and they may differ in stance, scope, and argumentative quality.

The Serbian translated version tests whether a retriever can handle debate questions and long translated argument passages. Some queries are simple questions, but the relevant documents are much longer and often contain lists, examples, claims, and supporting explanations. A useful model must connect the debate topic to argumentative content while avoiding passages that are merely topically adjacent.

### Observed Data Profile

The task contains 49 queries, 5,745 documents, and 932 relevance judgments. Every query is multi-positive, with an average of 19.02 positives per query. The minimum number of positives is 6, the median is 19.0, and the maximum is 32. This is one of the broadest relevant-set profiles among the NanoBEIR-style tasks.

Queries average 55.06 characters, while documents average 2,095.78 characters. The short query and long document contrast is important. The query usually names a debate topic, but a relevant passage may discuss only one side, one example, or one sub-argument. This makes recall and ranking diversity central to the task.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4741, hit@10 of 1.0000, and recall@100 of 0.6695 using the top-500 BM25 candidate subset. The perfect hit@10 shows that lexical matching reliably finds at least one relevant argument for every query. Controversial questions often contain distinctive topic words, and long argument passages tend to repeat those topic terms.

The lower recall@100 relative to the number of positives shows the limitation. BM25 can find an obvious argument, but it may not cover the full range of relevant passages, especially when arguments use alternative wording or focus on a sub-aspect of the debate. For research use, this task separates "find one argument" from "rank many relevant arguments well."

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.4605, hit@10 of 0.9796, and recall@100 of 0.8004. Dense retrieval improves recall@100 substantially over BM25, indicating that embedding similarity captures argumentative and topical variants that lexical matching misses. It is especially helpful when relevant passages discuss the same debate without repeating the exact query wording.

At the same time, dense retrieval is slightly weaker than BM25 on nDCG@10 and hit@10. This suggests that broad semantic similarity can retrieve a wider set of relevant arguments, but may place some less direct or less focused passages above the strongest matches. In debate retrieval, semantic breadth is valuable, but the top ranks still need tight alignment with the question.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5246, hit@10 of 0.9796, and recall@100 of 0.7650. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. This is the strongest top-rank profile among the three modes, although dense retrieval has the highest recall@100.

The result shows that hybrid search is well aligned with NanoTouche2020-sr. BM25 contributes precise topic anchoring, while dense retrieval broadens the argumentative space. The hybrid ordering places more relevant material near the top than either individual source, even though it does not recover quite as many positives at rank 100 as dense retrieval. For practical argumentative search, that top-rank improvement is important.

### Metric Interpretation for Model Researchers

Because every query has many positives, recall@100 is a key signal for candidate generation. A model with perfect hit@10 can still be weak if it retrieves only one obvious passage and misses many other relevant arguments. nDCG@10 measures whether the first page is densely populated with relevant arguments, which is important for debate exploration and downstream reranking.

The three profiles show different strengths. BM25 is excellent at finding at least one relevant passage through topic words. Dense retrieval gives the broadest relevant-set coverage. reranking_hybrid produces the best top-10 ranking. Researchers should choose the metric emphasis according to the intended system: high-recall argument discovery, first-page search quality, or second-stage reranking.

### Query and Relevance Type Tendencies

Queries ask controversial questions such as whether homework is useful, whether prescription drug advertising should target consumers, whether vaccines should be mandatory for children, whether abortion should be legal, and whether standardized tests improve education. Relevant passages are long arguments, often containing claims, examples, and explicit reasons.

The benchmark rewards models that identify debate topic, stance, and aspect. A passage can be relevant even if it argues from a different side than another positive passage. Conversely, a passage can mention the same topic but fail to address the specific argumentative need. This makes the task richer than simple topical retrieval.

### Representative Failure Modes

Likely failures include retrieving generic informational passages instead of arguments, over-ranking documents that repeat the debate topic without providing a clear claim, missing counterarguments that use different terminology, and failing to diversify across the many relevant passages. Dense models may retrieve broadly related opinion text that is not focused enough, while BM25 may miss arguments framed with synonyms or indirect language.

### Training Data That May Help

Useful training data includes argument retrieval, debate passage ranking, stance-aware retrieval, controversial question answering, and hard negatives from the same topic with weak or unrelated argumentative content. Serbian debate and opinion data can help with translated discourse markers and stance phrasing. For rerankers, pairs of same-topic arguments with different relevance or stance quality are valuable.

### Model Improvement Notes

A model targeting this task should balance topic anchoring with argumentative relevance. Sparse retrieval can be strong for initial candidate discovery, but needs expansion or normalization to improve recall over varied arguments. Dense retrieval should be tuned to keep semantic breadth while improving top-rank focus. Hybrid systems are particularly promising here because they combine the strengths of lexical topic matching and dense argument similarity.

## Example Data

### Public Sources

The original task is based on Touché 2020 argument retrieval, with BEIR providing the retrieval benchmark framing and NanoBEIR providing the compact multilingual dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original task | [Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sr dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |

Representative query and positive argument snippets:

| Query | Positive document snippet |
| --- | --- |
| Da li je domaći zadatak koristan? | Prvo, postoje tri argumenta zašto je domaći zadatak odličan i trebalo bi da se nastavi u modernim školama... |
| Treba li se reklamni lekovi na recept direktno usmeravati potrošačima? | Mnogi oglasi ne sadrže dovoljno informacija o tome koliko lekovi delotvorno deluju... |
| Da li bi neke vakcine trebalo da budu obavezne za decu? | Još uvek nije u potpunosti razrađeno... Vlade ne bi trebalo da imaju pravo da se mešaju... |
| Da li abortus treba da bude legalan? | Pobačaji bi trebalo da budu legalni jer ličnost počinje nakon što fetus postane sposoban za život... |
| Da li standardizovani testovi poboljšavaju obrazovanje? | Rezolucija: SAT, ACT i drugi standardizovani testovi pružaju bolji uvid u spremnost srednjoškolca... |
