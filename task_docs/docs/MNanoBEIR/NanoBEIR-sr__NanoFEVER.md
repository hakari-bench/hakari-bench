# MNanoBEIR / NanoBEIR-sr / NanoFEVER

## Overview

NanoBEIR-sr NanoFEVER is a Serbian factual-claim evidence retrieval task
derived from FEVER. Queries are short translated claims, and documents are
translated Wikipedia-style evidence passages. The retrieval goal is to find
the passage that can verify the claim before any support or refute decision.
The task is useful for evaluating multilingual retrieval systems that must
combine named-entity matching, semantic evidence matching, and precise
claim-passage alignment in Serbian.

## Details

### What the Original Data Measures

FEVER was built for fact extraction and verification over Wikipedia, where
systems retrieve evidence for claims before assigning verification labels. In
BEIR, the evidence retrieval step is evaluated independently. The MNanoBEIR
Serbian version keeps that structure after translation. It measures whether a
retriever can connect a compact Serbian claim to the Wikipedia passage that
contains the evidence needed for verification.

### Observed Data Profile

This Nano subset contains 50 queries, 4,996 documents, and 57 positive qrels.
Most queries have one positive, with a small multi-positive tail. The average
is 1.14 positives per query, with a minimum of 1, median of 1.00, and maximum
of 3. Six queries are multi-positive, covering 12.0% of the task. Queries
average 46.14 characters, while documents average 1,184.60 characters. This
creates a short-claim to long-evidence retrieval setting where early ranking
of the correct passage is important.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.6486,
hit@10 0.7800, and recall@100 0.8596. BM25 benefits from named entities,
titles, and factual terms that appear in both claims and evidence passages.
However, Serbian translated claims still require more than exact overlap in
some cases. A passage can mention the right entity while lacking the specific
fact, and title transliteration or paraphrase can reduce lexical matching.
BM25 is a useful candidate generator but leaves room for semantic evidence
ranking.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.7611, hit@10 0.9000, and recall@100 0.8947, outperforming
BM25 across all three reported metrics. Dense retrieval is better at connecting
claim meaning to evidence context, especially when the passage contains the
answer through paraphrase, description, or a longer explanation. This profile
shows that Serbian FEVER-style retrieval benefits strongly from embedding
similarity, while still retaining value from exact entity cues.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.04 and 2 safeguard rows. It reaches nDCG@10 0.7191, hit@10 0.8600,
and recall@100 0.9474. Hybrid retrieval has the best top-100 coverage but
does not match dense early ranking. This makes it a strong reranking input:
the pool contains more positives, while the final ordering needs a model that
can identify which passage actually verifies the claim.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 is close to a query-level
first-page success signal, and recall@100 indicates whether the evidence is
available to a reranker. nDCG@10 is the key early-ranking measure. Dense
retrieval is strongest for ranking, while reranking hybrid is strongest for
coverage. Researchers can use this task to study the tradeoff between semantic
claim-evidence ranking and candidate recall in an entity-heavy fact-checking
setting.

### Query and Relevance Type Tendencies

Queries are short factual claims about people, media works, locations,
historical figures, and films. Relevant documents are Wikipedia passages that
contain the verification evidence. Examples include claims about Keith
Godchaux and the Grateful Dead, a sitcom, advanced aircraft in Burbank, Nero,
and the film Scream 2. The task favors models that preserve entity identity,
title matching, and relation-specific evidence.

### Representative Failure Modes

BM25 may retrieve the right entity page but not the passage that verifies the
claim. Dense models may retrieve semantically related passages about the same
entity or work while missing the requested fact. Hybrid retrieval improves
candidate coverage but can include both lexical and semantic distractors.
Serbian translation and transliteration can also create variants of names and
titles that affect matching.

### Training Data That May Help

Helpful training data includes non-overlapping claim-evidence retrieval,
Serbian Wikipedia evidence mining, multilingual fact-checking, entity-centric
QA, and hard-negative evidence selection. Hard negatives should come from
related entities or neighboring events that share terms but fail to verify the
claim. Training should exclude FEVER, BEIR, NanoBEIR, and direct translations
of evaluation claims or evidence pages.

### Model Improvement Notes

NanoFEVER-sr is a strong benchmark for answer and evidence-aware retrieval.
Dense retrieval gives the best early ordering, while reranking hybrid gives
the best evidence coverage. Improvements should focus on entity
disambiguation, alias and transliteration handling, relation matching, and
rerankers that check whether the passage actually verifies the claim. A
practical system would use hybrid candidates for recall and a claim-evidence
reranker for final ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| Kith Godčo je poznavao Grateful Dead. [37 chars] | Grateful Dead je bila američka rok grupa osnovana 1965. godine u Palo Altu u Kaliforniji. Sa sastavom koji je varirao od kvinteta do septeta, bend je poznat po svom jedinstvenom i eklektičnom stilu, k... [200 / 2,888 chars] |
| "Taarak Mehta Ka Ooltah Chashmah" je sitkom. [44 chars] | "Taarak Mehta Ka Ooltah Chashmah" (na engleskom: "Taarak Mehta's Different Perspective") je najduže trajuća indijska sitkom serija koju proizvodi Neela Tele Films Private Limited. Serija je počela sa... [200 / 590 chars] |
| Tajni i tehnološki napredni avioni proizvođeni su u Burbanku u Kaliforniji. [75 chars] | Burbank je grad u okrugu Los Anđeles u južnoj Kaliforniji, Sjedinjene Države, 19 km severozapadno od centra Los Anđelesa. Prema popisu iz 2010. godine, stanovništvo je iznosilo 103.340. Poznat kao "Me... [200 / 1,321 chars] |
| Nero je osoba. [14 chars] | Termin Julijevsko-Klaudijevska dinastija odnosi se na prvih pet rimskih careva — Avgusta, Tiberija, Kaligulu, Klaudija i Nerona — ili na porodicu kojoj su pripadali. Oni su vladali Rimskim Carstvom od... [200 / 2,025 chars] |
| "Scream 2" je isključivo nemački film. [38 chars] | Scream 2 je američki slasher film iz 1997. godine koji je režirao Wes Craven, a scenario napisao Kevin Williamson. U filmu glume David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Ja... [200 / 2,427 chars] |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
