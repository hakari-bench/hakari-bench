# MNanoBEIR / NanoBEIR-no / NanoFEVER

## Overview

NanoBEIR-no NanoFEVER is a Norwegian fact-verification evidence retrieval task
derived from FEVER. Queries are short translated claims, and documents are
translated Wikipedia evidence passages. The retrieval problem is to find the
passage that can support, refute, or otherwise verify the claim before any
classification step. Compared with climate-specific fact checking, this task
has broader encyclopedic coverage: people, media works, places, organizations,
and historical facts all appear. It is therefore a useful benchmark for
short-claim retrieval over long evidence documents in a multilingual setting.

## Details

### What the Original Data Measures

FEVER introduced a large-scale dataset for fact extraction and verification
using claims paired with Wikipedia evidence. BEIR uses the evidence retrieval
stage as an information retrieval benchmark, separating the task of finding
evidence from the later decision about whether a claim is supported or refuted.
The MNanoBEIR Norwegian version keeps this claim-to-evidence structure while
using a compact translated subset. It measures whether a model can connect a
brief Norwegian claim to the right Wikipedia passage, often through entity
names, paraphrases, and factual attributes.

### Observed Data Profile

This Nano subset contains 50 queries, 4,996 documents, and 57 positive qrels.
Most queries have one positive document, with an average of 1.14 positives per
query, a minimum of 1, median of 1.00, and maximum of 3. Six queries have
multiple positives, representing 12.0% of the task. Queries are short at 46.02
characters on average, while evidence documents are much longer at 1,166.53
characters. This creates a high-precision retrieval task: the model must use a
small claim to identify a specific evidence-bearing passage within a larger
encyclopedic corpus.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.7396,
hit@10 0.9000, and recall@100 0.9649. This is a strong lexical profile. Many
FEVER claims contain entity names, titles, or compact factual phrases that are
also present in the evidence passages, so term matching is often enough to
retrieve the right page or paragraph. The remaining difficulty comes from
translated paraphrases and from claims where the evidence passage contains the
answer indirectly. BM25 is therefore not merely a weak baseline here; it is a
high-quality candidate generator whose errors mark cases where exact wording
and entity overlap are insufficient.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
achieves nDCG@10 0.8416, hit@10 0.9400, and recall@100 0.9474. Dense retrieval
has the best nDCG@10 and improves hit@10 over BM25, indicating better early
ordering for short claims and long Wikipedia passages. Its recall@100 is
slightly lower than BM25, however, which suggests that lexical exact matches
still recover some positives that dense similarity does not rank as broadly.
This is a typical FEVER pattern: entity-level surface cues are valuable for
coverage, while semantic matching helps put the most useful evidence closer to
the top.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.02 and 1 safeguard row. It scores nDCG@10 0.7934, hit@10 0.9400,
and recall@100 0.9649. The hybrid candidate pool matches BM25 recall and dense
hit@10, but its nDCG@10 falls between them. This makes it a strong reranking
input: it combines the lexical coverage needed for entity-heavy claims with
the semantic coverage needed for paraphrased evidence. The top ordering is not
as strong as dense alone, so a downstream reranker must exploit the broader
pool rather than assuming the candidate order is already optimal.

### Metric Interpretation for Model Researchers

Because almost all queries have one positive, hit@10 is close to a query-level
success measure and recall@100 shows whether the evidence is available to a
reranker. nDCG@10 is the best indicator of whether the positive appears near
the top rather than merely somewhere in the first page. The observed scores
show a useful tradeoff: BM25 and hybrid provide excellent candidate coverage,
while dense retrieval gives the strongest early ranking. For evaluating
retrieval models, this task helps separate entity recall from semantic evidence
ranking. A strong model should preserve BM25-style exact entity sensitivity
while improving dense-style paraphrase handling.

### Query and Relevance Type Tendencies

Queries are short factual claims, often centered on a named entity, title, or
simple relation. Relevant documents are Wikipedia-derived passages that contain
the information needed to evaluate the claim. Examples include claims about a
musician, a television series, a city associated with advanced aircraft, a
Roman emperor, and a film's nationality. The task rewards models that can map
brief claims to longer passages, recognize aliases and translated names, and
match factual predicates such as occupation, genre, location, membership, or
national origin.

### Representative Failure Modes

BM25 can fail when the evidence uses a paraphrase, alternate title, or broader
description rather than the exact claim wording. Dense models can fail by
retrieving semantically related entity pages that do not contain the specific
fact needed for verification. Hybrid retrieval can include both the right
entity and many nearby entities, leaving final disambiguation to the reranker.
Translation can add ambiguity when names are preserved but surrounding
relations are phrased differently from the original English source.

### Training Data That May Help

Helpful training data includes non-overlapping FEVER-style claim-evidence
pairs, Wikipedia passage retrieval, multilingual fact-checking datasets,
entity-centric QA, and hard-negative evidence selection. Hard negatives should
come from the same entity page, related entities, or passages that share key
names but do not verify the claim. Training should avoid FEVER, BEIR,
NanoBEIR, and overlapping translated Wikipedia evidence.

### Model Improvement Notes

NanoFEVER-no is a good test for models that must balance exact entity matching
with semantic claim-evidence alignment. Dense retrieval is strongest for
ranking the positive near the top, but BM25 and reranking hybrid have the
highest recall@100. A robust system should therefore use lexical evidence as a
coverage layer and semantic scoring as an ordering layer. Further improvements
should focus on entity disambiguation, alias handling, relation matching, and
claim-specific reranking over long evidence passages.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux kjente Grateful Dead. [36 chars] | The Grateful Dead var et amerikansk rockeband som ble dannet i 1965 i Palo Alto, California. Bandet, som besto av fem til syv medlemmer, er kjent for sin unike og eklektiske stil, som kombinerte eleme... [200 / 2,873 chars] |
| Taarak Mehta Ka Ooltah Chashmah er en situasjonskomedie. [56 chars] | Taarak Mehta Ka Ooltah Chashmah (norsk: Taarak Mehtas forskjellige perspektiver) er Indias lengst løpende sitcom-serie, produsert av Neela Tele Films Private Limited. Serien ble sendt på lufta 28. jul... [200 / 575 chars] |
| Hemmelige og teknologisk avanserte fly ble bygget i Burbank, California. [72 chars] | Burbank er en by i Los Angeles County i Sør-California, USA, 12 mil nordvest for sentrum av Los Angeles. Ved folketellingen i 2010 var befolkningen 103 340. Kjent som 'Verdens mediehovedstad' og bare... [200 / 1,248 chars] |
| Nero er en person. [18 chars] | Julio-Claudiske dynasti refererer til de første fem romerske keiserne – Augustus, Tiberius, Caligula, Claudius og Nero – eller familien de tilhørte. De styrte Det romerske riket fra dets dannelse unde... [200 / 1,988 chars] |
| Scream 2 er kun en tysk film. [29 chars] | Scream 2 er en amerikansk slasherfilm fra 1997, regissert av Wes Craven og skrevet av Kevin Williamson. Filmen har David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Jamie Kennedy, L... [200 / 2,419 chars] |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
