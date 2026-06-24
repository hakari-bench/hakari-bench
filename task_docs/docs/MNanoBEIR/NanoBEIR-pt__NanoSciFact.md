# MNanoBEIR / NanoBEIR-pt / NanoSciFact

## Overview

NanoBEIR-pt NanoSciFact is a Portuguese scientific claim evidence retrieval
task derived from SciFact. Queries are translated scientific claims, and
documents are translated abstracts that provide evidence. The task is a
claim-to-abstract retrieval problem: the relevant document should contain the
scientific result, mechanism, or experimental context needed to verify the
claim. It is useful for evaluating whether multilingual retrieval models can
combine technical term matching with evidence-specific semantic matching in
scientific and biomedical prose.

## Details

### What the Original Data Measures

SciFact evaluates scientific claim verification using abstracts as evidence.
In BEIR, the retrieval portion is evaluated: a system must find abstracts that
support or refute a claim before verification can occur. The MNanoBEIR
Portuguese version preserves this structure after translation. It measures
whether a model can map Portuguese scientific claims to the correct evidence
abstracts, including cases involving biomedical entities, interventions,
screening methods, or molecular mechanisms.

### Observed Data Profile

This Nano subset contains 50 queries, 2,919 documents, and 56 positive qrels.
Most queries have one positive, with a small multi-positive tail. The average
is 1.12 positives per query, with a minimum of 1, median of 1.00, and maximum
of 4. Four queries are multi-positive, covering 8.0% of the task. Queries
average 105.86 characters, and documents are long scientific abstracts
averaging 1,562.73 characters. The task requires matching a compact claim to a
long abstract that contains the specific evidence relation.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.6827,
hit@10 0.8400, and recall@100 0.9107. This is a strong lexical profile.
Scientific claims often repeat distinctive proteins, diseases, interventions,
or technical phrases from the abstract, so BM25 can find evidence candidates
reliably. The limitation is evidence discrimination: abstracts can share the
same entities or methods while reporting different findings. BM25 can retrieve
same-domain scientific text that is not the actual verification evidence.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.6801, hit@10 0.8000, and recall@100 0.8571. Dense retrieval
is close to BM25 in nDCG@10 but lower in hit@10 and recall@100. For this
Portuguese subset, exact technical terminology appears to be especially
important for candidate coverage. Dense similarity still helps connect claim
meaning to evidence context, but generic embeddings may blur fine-grained
scientific distinctions such as directionality, intervention effect, or
experimental condition.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.08 and 4 safeguard rows. It reaches nDCG@10 0.7118, hit@10 0.8400,
and recall@100 0.9286, making it the strongest profile overall. The result
shows that claim-evidence retrieval benefits from combining BM25's exact
scientific terminology with dense semantic matching. Hybrid retrieval gives
the best coverage and top-rank quality, which makes it a strong candidate pool
for verification-oriented reranking.

### Metric Interpretation for Model Researchers

Because most queries have a single positive, hit@10 and recall@100 are direct
signals of whether the evidence can be found and passed downstream. nDCG@10
captures whether evidence is placed early enough for verification. The hybrid
profile is strongest, while BM25 is unusually competitive with dense retrieval
because of technical term overlap. Researchers should use this task to test
whether a model preserves scientific terminology while still understanding
claim-level evidence relations.

### Query and Relevance Type Tendencies

Queries are atomic scientific claims about neutrophil migration, antiretroviral
therapy, interferon-induced genes, HPV screening, and TDP-43 interactions.
Relevant documents are abstracts that report the necessary evidence. The
relation is claim-specific: a document about the same protein, disease, or
screening method is not enough unless it addresses the exact finding. This
favors models that represent scientific predicates, causal direction, and
experimental context.

### Representative Failure Modes

BM25 may over-rank abstracts sharing rare biomedical terms but reporting a
different result. Dense models may retrieve broadly related biomedical
abstracts that are semantically close but not evidentially correct. Hybrid
retrieval improves both coverage and ranking, but a final verifier-oriented
reranker is still needed for claims involving negation, causality, or specific
experimental outcomes. Translation can add difficulty for abbreviations and
technical names.

### Training Data That May Help

Helpful training data includes non-overlapping scientific claim verification,
biomedical abstract retrieval, scientific NLI, Portuguese scientific QA, and
multilingual evidence retrieval. Hard negatives should share entities,
interventions, or methods while failing to provide the needed evidence.
Training should exclude SciFact, BEIR, NanoBEIR, and translated claim-evidence
pairs from the evaluation split.

### Model Improvement Notes

NanoSciFact-pt is a strong diagnostic for scientific evidence retrieval.
Reranking hybrid is the best candidate profile, and BM25 remains strong due to
technical overlap. Improvements should focus on scientific-domain embeddings,
claim predicate modeling, terminology preservation, and rerankers that compare
the claim against abstract-level evidence. The most useful models will combine
exact biomedical matching with semantic evidence reasoning.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q controla a migração de neutrófilos para locais de inflamação regulando as funções das rafts de membrana. [110 chars] | Neutrófilos sofrem polarização e movimento direcionado rapidamente para infiltrar os locais de infecção e inflamação. Aqui, mostramos que um receptor inibitório MHC I, Ly49Q, foi essencial para a polarização rápida e a infiltração tecidual dos neutrófilos. Durante o estado de equilíbrio, Ly49Q inibiu a adesão dos neutrófilos impedindo a formação de complexos focais, provavelmente inibindo as quinases Src e PI3. No entanto, na presença de estímulos inflamatórios, Ly49Q mediou a polarização rápida e a infiltração tecidual dos neutrófilos de maneira dependente do domínio ITIM. Essas funções opostas parecem ser mediadas pelo uso distinto das fosfatases efetoras SHP-1 e SHP-2. A polarização e a migração dependentes de Ly49Q foram afetadas pela regulação das funções dos rafts de membrana por Ly49Q. Proponemos que Ly49Q é crucial para a transição dos neutrófilos para sua morfologia polarizada e migração rápida durante a inflamação, através da regulação espaço-temporal dos rafts de membrana e... [1,000 / 1,050 chars] |
| Terapia antirretroviral reduz as taxas de tuberculose em diferentes níveis de contagem de CD4. [94 chars] | CONTEXTO A infecção pelo vírus da imunodeficiência humana (HIV) é o principal fator de risco para o desenvolvimento da tuberculose e tem impulsionado seu ressurgimento, especialmente na África subsaariana. Em 2010, estimava-se que havia 1,1 milhão de novos casos de tuberculose entre os 34 milhões de pessoas vivendo com HIV no mundo. A terapia antirretroviral tem um potencial significativo para prevenir a tuberculose associada ao HIV. Realizamos uma revisão sistemática de estudos que analisaram o impacto da terapia antirretroviral na incidência de tuberculose em adultos com infecção por HIV. MÉTODOS E RESULTADOS Foram realizadas buscas sistemáticas nas bases de dados PubMed, Embase, African Index Medicus, LILACS e registros de ensaios clínicos. Foram incluídos ensaios clínicos randomizados, estudos de coorte prospectivos e estudos de coorte retrospectivos que compararam a incidência de tuberculose pelo status de terapia antirretroviral em adultos infectados pelo HIV por um período media... [1,000 / 2,345 chars] |
| Aumento rápido e expressão basal aumentada de genes induzidos por interferon reduzem a sobrevivência de neurônios de células granulares infectados pelo vírus do Nilo Ocidental. [176 chars] | Embora a suscetibilidade dos neurônios do cérebro à infecção microbiana seja um grande determinante do resultado clínico, pouco se sabe sobre os fatores moleculares que governam essa vulnerabilidade. Aqui, mostramos que dois tipos de neurônios de diferentes regiões cerebrais apresentaram permissividade diferencial à replicação de vários vírus de RNA de fita positiva. Neurônios de células granulares do cerebelo e neurônios corticais do córtex cerebral possuem programas imunológicos inatos únicos que conferem suscetibilidade diferencial à infecção viral ex vivo e in vivo. Ao transduzir neurônios corticais com genes que eram expressos mais altamente em neurônios de células granulares, identificamos três genes estimulados por interferon (ISGs; Ifi27, Irg1 e Rsad2 (também conhecido como Viperin)) que mediaram os efeitos antivirais contra diferentes vírus neurotrópicos. Além disso, descobrimos que o estado epigenético e a regulação mediada por microRNA (miRNA) dos ISGs correlacionam-se com u... [1,000 / 1,256 chars] |

### Public Sources

- [SciFact: Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SciFact: Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | [https://arxiv.org/abs/2004.14974](https://arxiv.org/abs/2004.14974) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
