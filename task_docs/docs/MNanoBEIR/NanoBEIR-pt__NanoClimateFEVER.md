# MNanoBEIR / NanoBEIR-pt / NanoClimateFEVER

## Overview

NanoBEIR-pt NanoClimateFEVER is a Portuguese climate claim evidence retrieval
task derived from CLIMATE-FEVER. Queries are translated climate-related claims,
and documents are translated evidence passages. The task combines short claims
with long scientific or encyclopedic documents, making it useful for evaluating
whether multilingual retrieval systems can connect a compact assertion to the
evidence needed to support, refute, or contextualize it. It also stresses
domain-specific climate terminology, paraphrase, and multi-positive evidence
coverage.

## Details

### What the Original Data Measures

CLIMATE-FEVER extends fact-checking to real-world climate claims and evidence.
In BEIR, it is evaluated as claim-evidence retrieval: the retriever must find
documents relevant to a climate claim before any verification label can be
assigned. The MNanoBEIR Portuguese version preserves this retrieval structure
after translation. It measures whether a model can map Portuguese claims about
warming, sea level, storms, cosmic rays, or climate attribution to passages
that contain the appropriate scientific context.

### Observed Data Profile

This Nano subset contains 50 queries, 3,408 documents, and 148 positive qrels.
Most queries have multiple positives: the average is 2.96 positives per query,
with a minimum of 1, median of 3.00, and maximum of 5. There are 44
multi-positive queries, covering 88.0% of the task. Queries average 147.80
characters, while documents are much longer at 1,680.20 characters on average.
This creates a short-claim to long-evidence retrieval task where complete
coverage may require retrieving several acceptable documents for one claim.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2631,
hit@10 0.6400, and recall@100 0.5676. Lexical matching is moderately useful:
climate claims often contain distinctive terms such as sea level, global
warming, storms, cosmic rays, or specific experiments, and those terms can
anchor retrieval. However, the low nDCG and moderate recall show that exact
term overlap does not fully solve the task. Evidence passages may explain a
claim through broader scientific context, while many non-relevant documents
share the same climate vocabulary.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.2508, hit@10 0.6000, and recall@100 0.5878. Dense retrieval
slightly improves recall@100 over BM25 but trails BM25 in early ranking. This
suggests that embedding similarity expands evidence coverage by finding
semantically related climate passages, but it also brings in broad same-domain
distractors that are not the best evidence for the specific claim. For this
Portuguese subset, dense semantic matching is useful but not sufficient for
precise top-rank claim verification retrieval.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.04 and 2 safeguard rows. It reaches nDCG@10 0.2958, hit@10 0.7200,
and recall@100 0.6622, making it the strongest profile across the reported
metrics. The result indicates that Portuguese Climate-FEVER benefits from
combining lexical climate terminology with dense semantic evidence matching.
Hybrid retrieval gives better first-page success and broader evidence coverage
than either BM25 or dense alone.

### Metric Interpretation for Model Researchers

Because most queries have several positives, hit@10 only shows whether at least
one evidence passage reached the first page. Recall@100 reflects coverage of
the evidence set, and nDCG@10 measures whether relevant evidence is ranked
early. The hybrid profile is strongest, showing that neither lexical frequency
nor embedding similarity alone dominates this task. For model research, this
is a useful case where hybrid retrieval is not just a safety net but the best
observed candidate strategy for both coverage and early ranking.

### Query and Relevance Type Tendencies

Queries are Portuguese climate claims, often making assertions about trends,
causal mechanisms, or scientific interpretation. Relevant documents are longer
passages that provide definitions, background evidence, measurement context, or
attribution discussion. Examples include claims about warming periods, solar
activity, regional sea levels, Hurricane Harvey, and the CERN CLOUD experiment.
The task favors models that can preserve claim intent and scientific meaning
while handling technical vocabulary and long explanatory evidence.

### Representative Failure Modes

BM25 may retrieve climate documents that repeat the right terms but do not
verify the exact claim. Dense models may retrieve semantically broad passages
about climate change that are relevant to the topic but insufficient as
evidence. Hybrid retrieval improves both coverage and ranking but can still
include many same-domain distractors. Translation can also create mismatches
when a Portuguese claim and the evidence passage use different formulations for
the same scientific concept.

### Training Data That May Help

Helpful training data includes non-overlapping climate fact-checking,
scientific claim-evidence retrieval, multilingual fact verification,
Portuguese environmental QA, and climate-domain hard negatives. Hard negatives
should share climate terms but fail to support, refute, or explain the exact
claim. Training should exclude CLIMATE-FEVER, BEIR, NanoBEIR, and translated
records that overlap this evaluation split.

### Model Improvement Notes

NanoClimateFEVER-pt is a useful benchmark for claim-evidence retrieval in a
technical domain. The hybrid profile is strongest, so improvements should
preserve both lexical climate-term sensitivity and semantic claim-evidence
matching. Dense models may need climate-domain adaptation or reranking support
to avoid broad same-topic errors. A practical system would use hybrid
candidate generation followed by a verifier-oriented reranker trained to
distinguish true evidence from general climate-related text.

## Example Data

| Query | Positive document |
| --- | --- |
| De 1970 até 1998 houve um período de aquecimento que elevou as temperaturas em cerca de 0,39°C, o que contribuiu para o surgimento do movimento alarmista do aquecimento global. [176 chars] | O Paleoceno (pronunciado /paleoˈsɛnu/), ou Paleoceno, o "recentemente antigo", é uma época geológica que durou aproximadamente de 66 a 56 milhões de anos atrás. É a primeira época do Período Paleogeno na Era Cenozoica moderna. Assim como muitos períodos geológicos, as camadas que definem o início e o fim da época estão bem identificadas, mas as idades exatas permanecem incertas. A Época do Paleoceno abrange dois eventos principais na história da Terra. Começou com o evento de extinção em massa no final do Cretáceo, conhecido como a fronteira Cretáceo-Paleogeno (K-Pg). Este foi um período marcado pelo desaparecimento dos dinossauros não avianos, répteis marinhos gigantes e de muita outra fauna e flora. A extinção dos dinossauros deixou nichos ecológicos vazios em todo o mundo. O Paleoceno terminou com o Máximo Térmico do Paleoceno-Eoceno, um intervalo geologicamente breve (cerca de 0,2 milhão de anos) caracterizado por mudanças extremas no clima e no ciclo do carbono. O nome "Paleoceno"... [1,000 / 1,128 chars] |
| De fato, a tendência, embora não seja estatisticamente significativa, é de queda. [81 chars] | O ciclo solar, ou ciclo de atividade magnética solar, é a mudança quase periódica de 11 anos na atividade do Sol, que inclui variações nos níveis de radiação solar e na ejeção de material solar, bem como alterações na sua aparência (como o número e tamanho de manchas solares, fulgurações e outras manifestações). Essas mudanças têm sido observadas há séculos, tanto pelas alterações na aparência do Sol quanto pelos fenômenos observados na Terra, como as auroras. As mudanças no Sol causam efeitos no espaço, na atmosfera e na superfície terrestre. Embora seja a variável dominante na atividade solar, também ocorrem flutuações aperiódicas. [641 chars] |
| Os níveis do mar locais e regionais continuam a apresentar a variabilidade natural esperada, subindo em algumas regiões e descendo em outras. [141 chars] | O nível médio do mar (NMM) (abreviado simplesmente como nível do mar) é o nível médio da superfície de um ou mais dos oceanos da Terra, a partir do qual se podem medir alturas, como elevações. O NMM é um tipo de datum vertical, um ponto de referência geodésico padronizado, utilizado, por exemplo, como datum de carta em cartografia e navegação marítima, ou, na aviação, como o nível do mar padrão no qual a pressão atmosférica é medida para calibrar a altitude e, consequentemente, os níveis de voo das aeronaves. Um padrão comum e relativamente simples de nível médio do mar é o ponto médio entre a maré baixa média e a maré alta média em um local específico. Os níveis do mar podem ser afetados por muitos fatores e são conhecidos por terem variado bastante ao longo de escalas de tempo geológicas. A medição cuidadosa das variações no NMM pode fornecer insights sobre a mudança climática em curso, e o aumento do nível do mar tem sido amplamente citado como evidência do aquecimento global em and... [1,000 / 1,098 chars] |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | task paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
