# MNanoBEIR / NanoBEIR-pt / NanoTouche2020

## Overview

NanoBEIR-pt NanoTouche2020 is a Portuguese argument retrieval task derived
from the Touché 2020 argument retrieval benchmark. Queries are translated
controversial questions, and documents are translated debate-style argument
passages. The task is useful because relevance is not simple question
answering: a relevant document should provide a substantive argument about the
controversial issue. Since each query has many positives, the benchmark tests
both first-page success and broad coverage of relevant argumentative material.

## Details

### What the Original Data Measures

Touché 2020 evaluates argument retrieval for conversational and controversial
information needs. BEIR includes it as an argument retrieval task, and the
MNanoBEIR Portuguese version keeps that task shape after translation. It
measures whether retrieval models can map short controversial questions to
long argument passages that discuss the issue in a useful way, including pro
and con positions, examples, and policy reasoning.

### Observed Data Profile

This Nano subset contains 49 queries, 5,745 documents, and 932 positive qrels.
Every query has multiple positives. The average is 19.02 positives per query,
with a minimum of 6, median of 19.00, and maximum of 32. Queries average 49.14
characters, while documents are long argument texts averaging 2,264.92
characters. This creates a broad argument retrieval setting: a model should
retrieve many relevant arguments for a topic, not only a single passage that
mentions the same terms.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.5366,
hit@10 0.9796, and recall@100 0.7318. Lexical matching is very strong for this
task because controversial questions contain clear topic terms, and debate
passages often repeat those terms. The high hit@10 shows that BM25 almost
always finds at least one relevant argument early. The remaining challenge is
coverage and ordering: many passages discuss the same topic, but the best
results should contain substantive arguments, not just topical mentions.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.4496, hit@10 0.9592, and recall@100 0.7682. Dense retrieval
improves recall@100 over BM25 but is weaker in nDCG@10 and hit@10. This
suggests that semantic matching broadens the set of relevant arguments,
including passages that use different wording, but the dense order may bring
in broad same-topic arguments that are less useful at the top. For Portuguese
Touché, lexical topic anchors are unusually strong for early ranking.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.5371, hit@10 1.0000, and
recall@100 0.7994, making it the strongest overall profile. The hybrid result
combines BM25's precise topic anchoring with dense retrieval's broader
semantic coverage. This is a clear case where hybrid search captures the best
of both sides: it preserves top-rank quality and increases the share of
positive argument passages available in the candidate pool.

### Metric Interpretation for Model Researchers

Because every query has many positives, hit@10 is easy to saturate and should
not be treated as complete success. Recall@100 is crucial for judging argument
coverage, while nDCG@10 shows whether relevant arguments are ranked early. The
hybrid profile is strongest in both early ordering and coverage, while dense
retrieval mainly contributes additional recall. Researchers should evaluate
whether a model retrieves diverse, substantive arguments rather than repeated
topical passages.

### Query and Relevance Type Tendencies

Queries are short controversial questions about homework, prescription drug
advertising, childhood vaccines, abortion, standardized testing, and similar
debate topics. Relevant documents are long argument passages that may support,
oppose, or contextualize the issue. The retrieval target is argumentative
usefulness: a passage should provide a reason, claim, or example that answers
the debate question. This favors models that preserve topic, stance, and
argument quality.

### Representative Failure Modes

BM25 may retrieve documents that repeat the topic but contain weak or partial
argumentation. Dense models may retrieve broadly related debate text that does
not address the specific question or stance. Hybrid retrieval improves both
coverage and top ranking but still needs reranking to diversify pro and con
evidence and avoid near-duplicate topical passages. Translation can also blur
stance markers or rhetorical details in long arguments.

### Training Data That May Help

Helpful training data includes non-overlapping argument retrieval, debate
passages, stance-aware ranking, pro/con argument pairs, Portuguese
controversial-question retrieval, and argument quality data. Hard negatives
should discuss the same debate topic but not answer the specific stance or
aspect requested by the query. Training should exclude Touché, BEIR,
NanoBEIR, and translated evaluation arguments.

### Model Improvement Notes

NanoTouche2020-pt is a strong benchmark for hybrid retrieval and argument
reranking. BM25 is already strong for top-rank topic matching, dense retrieval
adds broader argument coverage, and reranking hybrid performs best overall.
Improvements should focus on stance-sensitive representations, argument
quality, diversity across relevant arguments, and rerankers that distinguish
substantive debate content from topical mentions.

## Example Data

| Query | Positive document |
| --- | --- |
| Os deveres de casa são benéficos? | Existem três argumentos para justificar por que a lição de casa é excelente e deve continuar nas escolas modernas... |
| Os medicamentos de prescrição devem ser anunciados diretamente aos consumidores? | Muitos anúncios não incluem informações suficientes sobre a eficácia dos medicamentos. Por exemplo, o Lunesta é anunciado por uma mariposa... |
| Quais vacinas as crianças devem tomar? | Os governos não devem ter o direito de intervir nas decisões de saúde que os pais tomam para seus filhos... |
| O aborto deve ser legalizado? | Os abortos devem ser legais, pois a personalidade jurídica começa após o feto se tornar viável ou após o nascimento... |
| Os testes padronizados melhoram a educação? | O SAT, o ACT e outros testes padronizados fornecem mais insights sobre a preparação de estudantes para universidades de elite... |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | task paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
