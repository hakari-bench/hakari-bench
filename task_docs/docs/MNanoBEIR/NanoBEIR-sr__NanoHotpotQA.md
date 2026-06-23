# MNanoBEIR / NanoBEIR-sr / NanoHotpotQA

## Overview

NanoBEIR-sr NanoHotpotQA is a Serbian multi-hop question answering retrieval
task derived from HotpotQA. Queries are translated questions, and documents are
translated Wikipedia supporting passages. Every query in this Nano subset has
two positive documents, so the retrieval problem is not just finding one
obvious page. A good system should recover both pieces of evidence needed for
the multi-hop answer. The task is useful for evaluating bridge-entity
retrieval, multi-positive evidence coverage, and answer-oriented ranking in
Serbian.

## Details

### What the Original Data Measures

HotpotQA was designed for explainable multi-hop question answering with
supporting facts. In BEIR, the task evaluates retrieval of the supporting
passages before answer extraction. The MNanoBEIR Serbian version preserves
this structure after translation. It measures whether retrieval models can
follow a question across linked entities, retrieve the bridge evidence, and
also retrieve the answer-bearing passage.

### Observed Data Profile

This Nano subset contains 50 queries, 5,090 documents, and 100 positive qrels.
Every query has exactly two positives, so the average, median, minimum, and
maximum positives per query are all 2.00. All queries are multi-positive.
Queries average 86.54 characters, and documents average 353.56 characters.
This fixed two-positive design makes evidence-set coverage important: a system
that retrieves only one supporting document may still fail the multi-hop task.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.6327,
hit@10 0.9000, and recall@100 0.8700. Lexical matching is useful because
HotpotQA questions often include named entities, titles, dates, or places that
appear directly in one supporting passage. The limitation is two-hop coverage.
BM25 may find the most explicit entity but miss the bridge or complementary
supporting document. It is therefore a reasonable candidate generator but less
effective than dense or hybrid retrieval for complete evidence retrieval.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.7516, hit@10 0.9600, and recall@100 0.9500, outperforming
BM25 across all reported metrics. Dense retrieval helps connect the question's
semantic relation to supporting passages even when exact word overlap is not
strong. It is better at retrieving bridge passages and paraphrased evidence,
though it may still confuse same-entity or same-topic passages that answer
only part of the question.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.7414, hit@10 0.9400, and
recall@100 0.9600. The hybrid profile has the best evidence coverage, while
dense retrieval has slightly better early ranking and first-page success. This
is a useful reranking setup: the hybrid pool combines BM25 entity anchors with
dense semantic links and gives a downstream model access to more supporting
passages, but final ordering still needs multi-hop evidence awareness.

### Metric Interpretation for Model Researchers

Because every query has two positives, hit@10 is not enough to determine task
success. It only shows that at least one supporting passage was found. Recall@100
is more important for whether both pieces of evidence can reach a reranker,
and nDCG@10 measures whether they appear early. The dense profile is best for
top ranking, while reranking hybrid is best for coverage. Researchers should
evaluate whether a model retrieves complementary support passages rather than
repeated variants of the same hop.

### Query and Relevance Type Tendencies

Queries are Serbian multi-hop questions about actors, historical figures,
films, college football games, and music. Relevant documents are short
Wikipedia passages that each provide part of the evidence chain. Examples
include a question linking Penny Rae Bridges to another actor, a sword made by
the founder of a school, a film involving Joby Harold and Samuel Sim, and a
game at Sun Life Stadium. The task favors models that preserve entity identity
and relation constraints.

### Representative Failure Modes

BM25 may retrieve the paragraph with the most explicit entity overlap while
missing the second support. Dense models may retrieve semantically related
paragraphs about the same entity cluster but not the bridge fact. Hybrid
retrieval improves coverage but still requires reranking that values
complementary evidence. Serbian translation and transliteration can create
name variants that affect both lexical and semantic matching.

### Training Data That May Help

Helpful training data includes non-overlapping multi-hop QA retrieval, Serbian
Wikipedia question generation, bridge-entity retrieval, comparison questions,
and multi-positive passage ranking. Hard negatives should mention one entity
from the question but omit the bridge fact or final answer. Training should
exclude HotpotQA, BEIR, NanoBEIR, and translated evaluation questions or
support passages.

### Model Improvement Notes

NanoHotpotQA-sr is a compact benchmark for multi-hop evidence retrieval. Dense
retrieval is strongest for early ranking, while reranking hybrid provides the
best coverage. Improvements should focus on preserving bridge constraints,
retrieving complementary evidence, and reranking for full support-set
coverage. For downstream QA, the key behavior is whether both supporting
passages are available and ranked high enough to be used together.

## Example Data

| Query | Positive document |
| --- | --- |
| Peni Rej Bridžes je glumila u televizijskoj sitkom seriji uz kojeg drugog glumca? [81 chars] | Penny Rae Bridges (rođena 29. jula 1990) je američka glumica. Njen televizijski rad obuhvata uloge u serijama "For Your Love", "Family Law", "Boy Meets World" i "The Parent 'Hood". Najpoznatija je po... [200 / 240 chars] |
| Ko je dao Kaganoiju Šigemočiju oštricu koju je napravila osoba koja je osnovala Muramasa školu? [95 chars] | Kaganoi Shigemochi (加賀井 重望, 1561 – 27. avgust 1600) bio je japanski samuraj iz perioda Azuči-Momojama, koji je služio klanu Oda. Vladao je dvorcem Kaganoi. Tokom Bitke kod Komakija i Nagakutea, Shigem... [200 / 584 chars] |
| Koji film je napisao i režirao Joby Harold, a muziku komponovao Samuel Sim? [75 chars] | Samuel Sim je kompozitor za film i televiziju. Prvi put je stekao priznanje sa svojom nagrađivanom muzikom za dramsku seriju BBC-ja "Dunkirk". Od tada je napisao muziku za širok spektar filmskih i tel... [200 / 521 chars] |
| Koji je datum odigravanja ove koledž fudbalske utakmice na Sun Life Stadium u Miami Gardens, Florida... [100 / 182 chars] | Fudbalska ekipa Clemson Tigers iz 2015. godine predstavljala je Univerzitet Clemson u sezoni 2015. NCAA Division I FBS. Tigrove je vodio glavni trener Dabo Swinney u svojoj sedmoj punoj godini i osmoj... [200 / 1,070 chars] |
| "Devil's Food" je kompilacija singlova američke rok and rol grupe koja je takođe poznata po sviranju... [100 / 133 chars] | "Devil's Food" je kompilacija singlova američke rok and rol grupe Supersuckers, objavljena u aprilu 2005. godine za izdavačku kuću Mid-Fi. [138 chars] |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | [https://arxiv.org/abs/1809.09600](https://arxiv.org/abs/1809.09600) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
