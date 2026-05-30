# MNanoBEIR / NanoBEIR-it / NanoSciFact

## Overview

`NanoBEIR-it__NanoSciFact` is the Italian NanoBEIR version of SciFact, a
scientific claim verification retrieval benchmark. The task uses Italian
translated scientific claims as queries and asks a retriever to rank Italian
translated abstracts that provide evidence for or against each claim. The Nano
split contains 50 queries, 2,919 documents, and 56 positive qrels. Most queries
have one positive, while 4 queries have multiple positives. Unlike SCIDOCS,
which emphasizes related paper retrieval, SciFact is closer to claim-to-evidence
search: the model must find abstracts whose experimental finding or conclusion
is relevant to a specific scientific assertion.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduced SciFact as a dataset of expert-written scientific claims paired with
evidence abstracts, support/refute labels, and rationales. BEIR uses SciFact as
a fact-checking retrieval task: the first-stage retriever must find the abstract
that can verify the claim before any entailment or stance model can decide
support versus refutation. The Italian NanoBEIR version evaluates that retrieval
step in translated scientific and biomedical prose.

### Observed Data Profile

The task contains 50 queries and 2,919 documents. It has 56 positive qrels, with
1.12 positives per query on average. The positives-per-query distribution is 1
minimum, 1.00 median, and 4 maximum, and only 8.0% of queries are multi-positive.
Queries average 113.72 characters, reflecting full scientific claims rather than
short keyword searches. Documents are long abstracts averaging 1,631.49
characters. This profile requires matching a specific claim to an evidence-
bearing abstract, often through biomedical terminology, experimental context,
and causal or comparative phrasing.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.6714, hit@10 = 0.7800, and
Recall@100 = 0.8929. This is a strong lexical result. Scientific claims often
repeat distinctive biomedical entities, genes, proteins, diseases, interventions,
or outcome phrases that also appear in the evidence abstract. BM25 can therefore
anchor retrieval effectively. Its limitation is that verification evidence may
use abbreviations, different clause structure, or a broader experimental
description than the claim text, which can prevent exact matching from always
placing the evidence abstract at the very top.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.6381, hit@10 =
0.7600, and Recall@100 = 0.8929. Dense retrieval matches BM25 on top-100
coverage but is slightly weaker on top-10 ranking. This suggests that semantic
similarity is able to find the same evidence abstracts in the candidate pool,
but exact scientific terminology remains highly predictive for early ranking.
For this task, embedding similarity helps with paraphrase and context, yet a
general dense model may not always preserve the fine biomedical distinctions
needed to rank the correct abstract over related ones.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.6766, hit@10 = 0.8200, and Recall@100 = 0.9286. Four queries use
the rank-101 safeguard. Hybrid retrieval is the strongest profile across the
main metrics. It combines BM25's exact scientific term anchors with dense
retrieval's ability to recover semantically related evidence. The gain is not
large in nDCG@10, but it is consistent with the task: claim verification
benefits from keeping precise entities and measurements while also allowing
variation in how findings are described.

### Metric Interpretation for Model Researchers

SciFact is a case where BM25 is already strong, dense retrieval is competitive,
and hybrid retrieval provides the best overall behavior. The task should not be
read as a generic semantic similarity benchmark. It is a claim-evidence matching
benchmark where biomedical terms and claim structure carry strong signal. A
model that improves on this task should preserve exact entity and outcome
matching while also handling paraphrased claims, abbreviations, and experimental
descriptions. Since most queries have one positive, top-rank ordering has a
large effect on nDCG@10.

### Query and Relevance Type Tendencies

The examples include claims about neutrophil migration, antiretroviral therapy
and tuberculosis, interferon-induced genes, cervical cancer screening, and
TDP-43 interactions. Relevant documents are long scientific abstracts that
usually contain the claim's key entities plus methods, background, and results.
The retriever must identify the abstract that bears on the claim, not merely an
abstract from the same biomedical area. This makes near-miss related abstracts a
central source of difficulty.

### Representative Failure Modes

BM25 can over-rank abstracts with matching biomedical terms that do not verify
the claim. Dense retrieval can over-rank semantically related abstracts that
discuss the same disease, protein, or intervention but support a different
finding. Hybrid retrieval can still fail when lexical and dense signals both
favor the same topical distractor. Because the task is used for verification,
retrieval errors are especially costly: if the evidence abstract is missing, a
downstream verifier cannot recover the correct support or refute decision.

### Training Data That May Help

Useful training data includes non-overlapping scientific fact verification,
claim-evidence retrieval, biomedical abstract retrieval, and multilingual
scientific NLI. Hard negatives should share entities, interventions, or outcome
terms with the claim while differing in the actual finding. Training should
exclude SciFact, BEIR, NanoBEIR, and overlapping translated abstracts or claim
pairs from this benchmark.

### Model Improvement Notes

Strong systems should model claim specificity. Entity matching is necessary but
not sufficient; the ranker must also attend to relation words, directionality,
comparative outcomes, and experimental context. Hybrid candidate generation is a
good fit because it preserves both exact biomedical anchors and semantic
evidence variation, but final ranking should distinguish evidence-bearing
abstracts from merely related scientific literature.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q regola la migrazione dei neutrofili verso i siti di infiammazione modulando le funzioni dei raft di membrana. | Neutrofili subiscono rapidamente una polarizzazione e un movimento direzionale per infiltrarsi nei siti di infezione e infiammazione. Qui mostriamo che un recettore MHC I inibitorio... |
| La terapia antiretrovirale riduce l'incidenza di tubercolosi in un ampio spettro di livelli di CD4. | CONTESTO L'infezione da virus dell'immunodeficienza umana (HIV) è il principale fattore di rischio per lo sviluppo della tubercolosi... |
| La regolazione rapida verso l'alto e l'espressione basale più elevata dei geni indotti da interferone riducono la sopravvivenza dei neuroni a granulo infetti dal virus del Nilo occidentale. | La suscettibilità dei neuroni del cervello all'infezione microbica è un determinante principale dell'esito clinico. Poco si sa riguardo ai fattori molecolari... |
| Lo screening primario per il cancro cervicale con rilevazione dell'HPV ha una maggiore sensibilità nel tempo rispetto alla citologia convenzionale per rilevare la neoplasia intraepiteliale cervicale di grado 2. | CONTESTO Lo screening per il cancro cervicale basato sul test per il papillomavirus umano (HPV) aumenta la sensibilità nella rilevazione della neoplasia intraepiteliale... |
| Inibire l'interazione tra TDP-43 e le proteine del complesso respiratorio I ND3 e ND6 provoca un aumento della perdita neuronale indotta da TDP-43. | Le mutazioni genetiche nella proteina TAR DNA-binding protein 43 (TARDBP, nota anche come TDP-43) causano la sclerosi laterale amiotrofica... |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
| SciFact repository |  | project page | https://github.com/allenai/scifact |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
