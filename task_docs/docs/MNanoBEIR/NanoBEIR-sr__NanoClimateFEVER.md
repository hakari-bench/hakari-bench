# MNanoBEIR / NanoBEIR-sr / NanoClimateFEVER

## Overview

NanoBEIR-sr NanoClimateFEVER is a Serbian climate claim evidence retrieval
task derived from CLIMATE-FEVER. Queries are translated climate-related claims,
and documents are translated evidence passages. The task combines short claims
with long scientific or encyclopedic documents, and most queries have several
acceptable evidence passages. It is useful for evaluating whether multilingual
retrieval models can connect Serbian claims about climate science to evidence
that supports, refutes, or contextualizes them.

## Details

### What the Original Data Measures

CLIMATE-FEVER extends fact-checking to real-world climate claims and evidence
documents. In BEIR, it is evaluated as claim-evidence retrieval: the system
must find evidence before any verification label can be assigned. The
MNanoBEIR Serbian version preserves that structure after translation. It
measures whether retrievers can connect claims about warming trends, sea level,
storms, cosmic rays, or climate attribution to passages that contain relevant
scientific context.

### Observed Data Profile

This Nano subset contains 50 queries, 3,408 documents, and 148 positive qrels.
Most queries have multiple positives, averaging 2.96 positives per query, with
a minimum of 1, median of 3.00, and maximum of 5. There are 44 multi-positive
queries, covering 88.0% of the task. Queries average 135.24 characters, while
documents average 1,552.34 characters. This short-claim to long-evidence shape
requires both finding at least one useful passage and covering multiple
acceptable evidence documents where they exist.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2389,
hit@10 0.6400, and recall@100 0.5473. Lexical matching often finds some
evidence because climate claims contain distinctive terms, measurements,
events, and scientific phrases. However, the top ranking and evidence coverage
remain difficult. Many passages share climate vocabulary while not verifying
the exact claim, and relevant evidence may express the same scientific concept
with different wording. BM25 is useful for climate-term anchoring but not
sufficient for precise evidence ranking.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.2946, hit@10 0.6800, and recall@100 0.5473. Dense retrieval
improves early ranking and first-page success over BM25, but it does not
improve recall@100. This suggests that embeddings help rank some claim-evidence
matches higher, while the broader candidate coverage remains constrained by
domain difficulty and same-topic distractors. Dense similarity can connect
paraphrased scientific context, but it may still retrieve broad climate
passages that are not evidence for the exact claim.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.04 and 2 safeguard rows. It reaches nDCG@10 0.3266, hit@10 0.7400,
and recall@100 0.6149, making it the strongest profile across the reported
metrics. Hybrid retrieval improves both early ranking and evidence coverage by
combining lexical climate terminology with dense semantic matching. This is a
case where neither BM25 nor dense alone dominates; the mixed candidate pool is
the most useful starting point for reranking.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, hit@10 only indicates whether at
least one relevant evidence passage appears early. Recall@100 is important for
evidence-set coverage, and nDCG@10 captures early ordering quality. The hybrid
profile is strongest, showing that Serbian Climate-FEVER benefits from both
word-level climate cues and semantic claim-evidence matching. Researchers
should evaluate whether a model retrieves enough evidence for verification,
not only whether it finds one topically related passage.

### Query and Relevance Type Tendencies

Queries are Serbian climate claims about warming periods, solar cycles,
regional sea level, Hurricane Harvey, and the CERN CLOUD experiment. Relevant
documents are longer passages that define scientific concepts, summarize
observations, or provide attribution context. The relation is evidence-based:
a document can be on the same climate topic and still be irrelevant if it does
not address the exact assertion. Models need to represent both technical terms
and claim meaning.

### Representative Failure Modes

BM25 may retrieve passages that repeat terms such as global warming, sea level,
or climate change without verifying the claim. Dense models may retrieve broad
climate science passages that are semantically related but not evidentially
specific. Hybrid retrieval improves both ranking and coverage but can still
include many same-domain distractors. Translation can also introduce variation
in scientific terminology across claims and documents.

### Training Data That May Help

Helpful training data includes non-overlapping climate claim verification,
Serbian scientific and policy evidence retrieval, multilingual fact-checking,
claim-evidence pairs, and climate-domain hard negatives. Hard negatives should
share climate terms but not contain verifying evidence. Training should
exclude CLIMATE-FEVER, BEIR, NanoBEIR, and overlapping translations.

### Model Improvement Notes

NanoClimateFEVER-sr is a compact benchmark for climate-domain evidence
retrieval. Reranking hybrid is the strongest observed profile, so improvements
should preserve both lexical terminology and semantic evidence matching.
Models should be evaluated on coverage of multiple evidence passages and on
their ability to rank evidence above same-topic climate text. A practical
system would use hybrid candidate generation followed by a claim-evidence
reranker.

## Example Data

| Query | Positive document |
| --- | --- |
| Od 1970. do 1998. godine postojao je period zagrevanja koji je podigao temperature za oko 0,7 stepeni Farenhajta... | Paleocen, što znači "stari novi", je geološka epoha koja je trajala od oko 66 do 56 miliona godina... |
| Zapravo, trend je, iako nije statistički značajan, opadajući. | Solarni ciklus ili ciklus solarne magnetne aktivnosti predstavlja gotovo periodičnu 11-godišnju promenu u aktivnosti Sunca... |
| Lokalni i regionalni nivoi mora i dalje pokazuju tipičnu prirodnu varijabilnost na nekim mestima se podižu, a na drugim spuštaju. | Srednji nivo mora je prosečan nivo površine jednog ili više Zemljinih okeana od koga se mogu meriti nadmorske visine... |
| Klimatolozi kažu da pojedini aspekti slučaja uragana Harvey ukazuju da globalno zagrevanje pogoršava već lošu situaciju. | Posledice globalnog zagrevanja su ekološke i društvene promene uzrokovane ljudskim emisijama gasova staklene bašte... |
| Eksperiment CERN CLOUD testirao je samo jednu trećinu jednog od četiri uslova potrebnih da se globalno zagrevanje okrivi na kosmičke zrake... | Pripisivanje nedavnih klimatskih promena predstavlja naučni pokušaj da se utvrde mehanizmi odgovorni za nedavne klimatske promene na Zemlji... |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
