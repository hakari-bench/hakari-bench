# MNanoBEIR / NanoBEIR-no / NanoSciFact

## Overview

NanoBEIR-no NanoSciFact is a Norwegian scientific claim verification retrieval
task derived from SciFact. Queries are translated scientific claims, and
documents are translated scientific abstracts that provide evidence supporting
or refuting those claims. The task differs from general scientific related-paper
retrieval because relevance depends on whether the abstract contains evidence
for a specific claim. It is therefore a compact benchmark for scientific
evidence retrieval, biomedical terminology, and claim-to-abstract matching in a
multilingual setting.

## Details

### What the Original Data Measures

SciFact was introduced for verifying expert-written scientific claims against
evidence abstracts, with support and refute labels plus rationales. In BEIR,
SciFact is evaluated as a retrieval task: the system must first retrieve the
abstracts that contain the evidence needed for verification. The MNanoBEIR
Norwegian version keeps that claim-to-evidence structure after translation. It
measures whether models can connect precise scientific assertions to abstracts
that report the relevant findings, mechanisms, or experimental outcomes.

### Observed Data Profile

This Nano subset contains 50 queries, 2,919 documents, and 56 positive qrels.
Most queries have one positive, while 4 queries have multiple positives. The
average is 1.12 positives per query, with a minimum of 1, median of 1.00, and
maximum of 4. Queries average 96.18 characters and are often technical
scientific claims. Documents are long abstracts averaging 1,424.51 characters.
The task therefore requires matching a compact claim to a long abstract that
contains the correct scientific evidence.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.5652,
hit@10 0.7200, and recall@100 0.8571. This is a strong lexical profile for a
scientific task. Claims and abstracts often share biomedical entities,
abbreviations, proteins, diseases, or technical terms, giving BM25 useful
anchors. However, evidence retrieval still requires more than term matching:
abstracts may share terminology while reporting different findings, and a
claim may be expressed as a paraphrase of the evidence. BM25 is a reliable
candidate generator but can confuse same-domain abstracts with true evidence.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.6217, hit@10 0.7600, and recall@100 0.9107, improving over
BM25 on every metric. Dense retrieval helps because scientific claims often
express a conclusion, while the evidence abstract may describe the experiment,
mechanism, or result in different words. Embedding similarity can connect those
forms of meaning better than exact lexical overlap alone. The remaining errors
likely come from highly technical distinctions, negation, and abstracts that
share entities but support different findings.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.08 and 4 safeguard rows. It reaches nDCG@10 0.6137, hit@10 0.7600,
and recall@100 0.9286. The hybrid pool has the best recall and matches dense
hit@10, while dense has a slightly higher nDCG@10. This is a strong example of
hybrid search behaving as complementary evidence collection: BM25 contributes
technical term coverage, dense retrieval contributes semantic claim-evidence
matching, and the combined pool gives a reranker access to more positives.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 is close to a query-level
success signal, while recall@100 indicates whether the evidence abstract is
available for reranking. nDCG@10 matters because downstream verification needs
the evidence near the top, not buried in a long candidate list. The observed
scores show that dense retrieval is best for early ordering, while reranking
hybrid is best for coverage. For research, this task is useful for separating
scientific semantic understanding from exact terminology matching.

### Query and Relevance Type Tendencies

Queries are atomic scientific claims, often about biological mechanisms,
clinical interventions, gene expression, screening methods, or disease-related
findings. Relevant documents are abstracts that contain evidence for or against
the claim. The relation is evidence-specific: a document about the same protein,
disease, or intervention is not enough unless it reports the relevant result.
This favors models that can represent scientific predicates, experimental
context, and the direction of a claim.

### Representative Failure Modes

BM25 may retrieve abstracts that share rare biomedical terms but do not verify
the claim. Dense systems may retrieve semantically related abstracts that are
too broad or that discuss the same pathway without the specific finding.
Hybrid systems improve coverage but can still mix true evidence with
same-domain distractors. Translation may introduce additional difficulty for
abbreviations, technical names, and nuanced scientific phrasing, especially
where negation or causality is important.

### Training Data That May Help

Helpful training data includes non-overlapping scientific fact verification,
claim-evidence retrieval, biomedical abstract retrieval, scientific NLI,
clinical trial evidence selection, and multilingual scientific retrieval.
Hard negatives should come from the same discipline and share key terms while
lacking the claim's specific finding. Training should exclude SciFact, BEIR,
NanoBEIR, and overlapping translated abstracts.

### Model Improvement Notes

NanoSciFact-no is a compact test of scientific evidence retrieval. Dense
retrieval is strongest for ranking, while reranking hybrid provides the best
top-100 evidence coverage. Improvements should focus on biomedical and
scientific-domain embeddings, claim predicate modeling, negation and causal
relation handling, and rerankers that compare a claim against abstract-level
evidence. A strong retrieval system should combine exact technical term
sensitivity with semantic evidence matching.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q styrer organiseringen av neutrofilmigrering til betennelsesområder ved å regulere membranraftf... [100 / 110 chars] | Neutrofiler gjennomgår rask polarisering og rettet bevegelse for å trenge inn i infeksjons- og betennelsesområder. Her viser vi at en inhiberende MHC I-reseptor, Ly49Q, var avgjørende for rask polaris... [200 / 969 chars] |
| Antiretroviral behandling reduserer forekomsten av tuberkulose i ulike CD4-nivåer. [82 chars] | BAKGRUNN Humant immunsviktvirus (HIV) infeksjon er den sterkeste risikofaktoren for å utvikle tuberkulose og har bidratt til en økning i forekomsten, spesielt i sub-Sahara-Afrika. I 2010 var det anslå... [200 / 2,211 chars] |
| Rask oppregulering og høyere basal ekspresjon av interferon-induserte gener reduserer overlevelsen a... [100 / 164 chars] | Selv om neuroners følsomhet for mikrobiell infeksjon i hjernen er en viktig faktor for klinisk utfall, er det lite kjent om de molekylære faktorer som styrer denne sårbarheten. Her viser vi at to type... [200 / 1,072 chars] |
| Primær screening for livmorhalskreft med HPV-detektering har høyere langtidssensitivitet enn konvens... [100 / 165 chars] | BAKGRUNN Screening for livmorhalskreft basert på testing for humant papillomavirus (HPV) øker følsomheten for å oppdage høygradig (grad 2 eller 3) livmorhalskreft forstadier, men om denne økningen rep... [200 / 2,218 chars] |
| Å blokkere interaksjonen mellom TDP-43 og respiratorisk kompleks I-proteiner ND3 og ND6 fører til øk... [100 / 134 chars] | Genetiske mutasjoner i TAR DNA-binding protein 43 (TARDBP, også kjent som TDP-43) fører til amyotrofisk lateralsklerose (ALS). Økt tilstedeværelse av TDP-43 (kodet av TARDBP) i cytoplasma er et fremtr... [200 / 1,254 chars] |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | [https://arxiv.org/abs/2004.14974](https://arxiv.org/abs/2004.14974) |
| SciFact repository |  | project page | [https://github.com/allenai/scifact](https://github.com/allenai/scifact) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
