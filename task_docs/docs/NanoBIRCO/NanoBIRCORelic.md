# NanoBIRCO / NanoBIRCORelic

## Overview

NanoBIRCORelic is a compact Nano task derived from BIRCO's RELIC literary evidence retrieval setting. Each query is a paragraph-length literary analysis passage where one quotation has been masked, and the corpus contains candidate literary passages. The retrieval goal is to recover the source passage that supports the surrounding analysis. This makes the task useful for evaluating discourse-level evidence retrieval, quotation recovery, literary interpretation, and low-overlap matching between criticism and source prose.

## Details

### What the Original Data Measures

BIRCO frames RELIC as a complex-objective retrieval task over literary analysis. The query contains scholarly or critical prose with one or more masked quotations. The relevant passage is the original literary sentence or passage that makes the surrounding analysis coherent.

This is not ordinary semantic similarity. The query is written in analytical language, while the positive document is literary prose. The model must infer tone, imagery, character relation, narrative function, or thematic evidence from the critic's context and match it to the source text.

### Observed Data Profile

The task contains 100 queries, 5,023 documents, and 100 relevance judgments. Each query has exactly one positive passage, so the positives-per-query average is 1.0, with minimum 1, median 1.0, maximum 1, and no multi-positive queries.

Queries average 1,016.31 characters, while documents average 477.34 characters. Queries are long criticism-style contexts; documents are shorter literary passages, often from classic novels. The task is difficult because the query and the positive may share few words despite being tightly related.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1314, hit@10 of 0.2300, and recall@100 of 0.5900 using the top-500 BM25 candidate subset. This is a weak lexical profile. BM25 can sometimes exploit character names, work titles, or repeated thematic words, but those signals rarely identify the exact quotation.

The core problem is that critical prose and source prose use different registers. A query may discuss symbolism, irony, social knowledge, sublimity, or narrative contrast, while the positive passage expresses those ideas through scene description. Lexical matching is therefore a poor proxy for evidence fit.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.0725, hit@10 of 0.1300, and recall@100 of 0.6600. Dense retrieval improves recall@100 over BM25 but is weaker in the top 10. This suggests that embedding similarity can broaden the candidate pool, but it does not reliably rank the exact quotation near the top.

The task is unusually hard for general dense retrieval because the relevance relation is indirect. The positive passage supports an interpretive claim rather than paraphrasing it. Literary style, metaphor, and narrative context can be difficult to compress into ordinary embedding similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.1276, hit@10 of 0.2200, and recall@100 of 0.6900. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 31 safeguard rows, candidate counts from 100 to 101, and a mean of 100.31 candidates. Hybrid has the best recall@100, while BM25 is slightly stronger in top-10 ranking.

This indicates that hybrid retrieval is useful as a candidate pool even when top-10 ranking remains weak. Sparse signals capture names and textual echoes, while dense signals add broader interpretive relatedness. A specialized reranker would still be needed to identify the exact supporting quotation.

### Metric Interpretation for Model Researchers

Because every query has one positive, hit@10 directly measures whether the missing quotation is visible. nDCG@10 reflects how early it appears, and recall@100 measures whether a later reranker has a chance. The low top-10 scores show that this is one of the harder complex-objective retrieval tasks.

The comparison shows that BM25 is slightly better for direct top ranking, dense retrieval helps coverage, and reranking_hybrid gives the best candidate completeness. This task is useful for evaluating retrieval beyond paraphrase and topical similarity.

### Query and Relevance Type Tendencies

Queries discuss classic literature and criticism involving authors or works such as D. H. Lawrence, Orwell, Dreiser, Dickens, Austen, Melville, and Shelley. Positives are literary passages that provide the missing textual evidence for a claim about tone, character, narrative pattern, or theme.

The task rewards inference from analysis to source evidence. A candidate can mention the same character or work but fail to support the specific interpretive point. Same-work passages are strong hard negatives.

### Representative Failure Modes

Likely failures include retrieving passages with the same character names but wrong scene, matching broad themes without fitting the masked context, missing metaphorical or tonal evidence, and ranking adjacent or topically related passages above the precise quotation. BM25 may be too literal, while dense retrieval may miss the exact support relation.

### Training Data That May Help

Useful training data includes non-overlapping literary evidence retrieval pairs, quotation recovery tasks, literary analysis paired with supporting passages, and same-work hard negatives that share characters or themes but do not support the claim. Training should avoid memorized quotation lookup and focus on analysis-to-evidence matching.

### Model Improvement Notes

A model targeting this task should represent discourse function and literary evidence, not just topic. Sparse systems need character and work cues but cannot rely on them. Dense systems need literary analysis supervision and same-work negatives. Hybrid systems are useful for recall, but the observed top-10 profile calls for a specialized reranker.

## Example Data

### Public Sources

The original task is based on BIRCO's complex-objective retrieval benchmark, with NanoBIRCO providing the compact dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BIRCO](https://arxiv.org/abs/2402.14151) |
| Project repository | [BIRCO GitHub repository](https://github.com/BIRCO-benchmark/BIRCO) |
| NanoBIRCO dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |

Representative query and positive passage snippets:

| Query | Positive document snippet |
| --- | --- |
| A literary analysis comparing Moby Dick with Euripides and a masked passage about divine fire. | thou clear spirit of clear fire, whom on these seas I as Persian once did worship... |
| A discussion of Lawrence's The Rainbow and generations of the Brangwen family. | But heaven and earth was teeming around them, and how should this cease? |
| A criticism passage comparing mass spectacle and fascist rallies. | Round they went, a circular procession of dancers, each with hands on the hips of the dancer preceding... |
| A Shelley analysis about the monster, loneliness, homelessness, and sublimity. | Delighted and surprised, I embraced her, but her features appeared to change... |
| A passage about feminine intuition and sorrowful peace. | But on other moonlight nights, when the sadness and the silence have touched me... |
