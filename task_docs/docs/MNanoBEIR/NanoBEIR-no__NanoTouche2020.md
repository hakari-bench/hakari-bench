# MNanoBEIR / NanoBEIR-no / NanoTouche2020

## Overview

NanoBEIR-no NanoTouche2020 is a Norwegian argument retrieval task derived from
the Touché 2020 argument retrieval benchmark. Queries are translated
controversial questions, and documents are translated debate-style arguments.
The task differs from ordinary question answering because relevant documents do
not simply answer a fact; they provide arguments for or against a controversial
issue. It is useful for evaluating whether retrieval models can combine topic
matching, argumentative content, and broad coverage of multiple relevant
positions in a multilingual setting.

## Details

### What the Original Data Measures

Touché 2020 focused on argument retrieval for controversial questions. Systems
are expected to retrieve arguments that are relevant to a debated topic, often
with attention to stance, argumentative quality, and topical usefulness. BEIR
includes Touché 2020 as an argument retrieval task, and MNanoBEIR provides a
Norwegian translated Nano subset. This version measures whether models can map
short controversial questions to long debate passages that contain substantive
argumentation rather than surface topic mentions alone.

### Observed Data Profile

This Nano subset contains 49 queries, 5,745 documents, and 932 positive qrels.
Every query is multi-positive. The average is 19.02 positives per query, with a
minimum of 6, median of 19.00, and maximum of 32. Queries are short,
averaging 39.84 characters, while documents are long debate arguments averaging
2,114.42 characters. This creates a broad argument retrieval setting: a system
should retrieve several relevant pro and con arguments for each controversial
question, not just one matching passage.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.4586,
hit@10 0.9796, and recall@100 0.6556. The very high hit@10 shows that lexical
topic matching is usually enough to place at least one relevant argument on the
first page. Controversial questions contain strong topic terms such as
homework, vaccines, abortion, advertising, or standardized testing, and those
terms often appear in debate documents. The harder part is ranking: many
passages mention the same topic, but relevance depends on whether they present
a substantive argument. BM25 is therefore strong for first-hit success but
less complete for broad argument coverage.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.4613, hit@10 0.9592, and recall@100 0.7296. Dense retrieval
has slightly better nDCG@10 and substantially better recall@100 than BM25, but
slightly lower hit@10. This suggests that embedding similarity is better at
covering a wider set of relevant arguments, including passages that use
different wording from the question. However, lexical topic cues remain strong
enough that BM25 is more reliable for finding at least one argument early.
Dense retrieval is especially useful when arguments discuss the issue through
examples, consequences, or stance-specific reasoning rather than repeating the
query exactly.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.5021, hit@10 1.0000, and
recall@100 0.7371, making it the strongest profile for this Norwegian subset.
The hybrid result matches the task's structure: BM25 contributes reliable
topic-term matches, while dense retrieval contributes semantic and stance-aware
coverage. The combined pool gives both perfect first-page query coverage and
the best top-100 positive coverage. This is a clear case where hybrid search
captures useful behavior from both lexical and dense retrieval.

### Metric Interpretation for Model Researchers

Because every query has many positives, hit@10 is easy to saturate and should
not be treated as full task success. Recall@100 is more informative for
argument coverage, and nDCG@10 shows whether high-quality relevant arguments
are ranked early. The hybrid profile is strongest across the practical ranking
signals, indicating that argument retrieval benefits from combining lexical
topic anchors with dense semantic matching. Researchers should evaluate
whether a model retrieves diverse relevant arguments across a topic, not only
whether it finds a single passage that mentions the issue.

### Query and Relevance Type Tendencies

Queries are short controversial questions such as whether homework is useful,
whether prescription drugs should be advertised directly to consumers, whether
children should receive vaccines, whether abortion should be allowed, or
whether standardized tests improve education. Relevant documents are long
debate arguments that may support, oppose, or contextualize the issue. The
task favors models that represent topic, stance, argumentative content, and
document substance. It also rewards broad retrieval because many arguments may
be relevant for the same question.

### Representative Failure Modes

BM25 may retrieve passages that repeatedly mention the topic but contain weak,
off-topic, or incomplete argumentation. Dense models may retrieve semantically
related debate passages that discuss a nearby issue or general value judgment
without answering the exact controversial question. Hybrid systems improve
coverage but still require a reranker to prioritize strong arguments and avoid
near-topic distractors. Translation can blur stance or argumentative nuance,
especially in long debate passages with examples and rhetorical structure.

### Training Data That May Help

Helpful training data includes non-overlapping argument retrieval, debate
portal data, pro/con argument collections, stance-aware retrieval, argument
quality ranking, and multilingual controversial-question retrieval. Hard
negatives should share topic terms but fail to provide a substantive argument
for the question. Training should exclude Touché 2020, BEIR, NanoBEIR, and
overlapping translated argument passages.

### Model Improvement Notes

NanoTouche2020-no is a strong benchmark for hybrid retrieval and reranking.
Unlike many QA tasks, BM25 already gives excellent first-hit behavior, but
dense and hybrid retrieval improve broader argument coverage. The best
systems should combine exact controversial-topic matching with semantic and
stance-sensitive ranking. Rerankers should be trained to distinguish argument
quality, topical relevance, and stance coverage so that the top results contain
useful and diverse debate evidence rather than repeated topical mentions.

## Example Data

| Query | Positive document |
| --- | --- |
| Er leksene nyttige? [19 chars] | Først, er det tre argumenter for hvorfor leksene er utmerket og bør fortsette i moderne skoler. 1. Leksene hjelper gjerningslærere. Det er generelt akseptert at det finnes tre typer lærere: de som lær av å høre, de som lær av å se, og de som lær av å gjøre. Mens mange er fornøyd med å høre eller se instruksjoner om et gitt emne, trenger noen å faktisk gjøre det. Derfor er leksene gunstig for denne siste gruppen fordi instruksjonen lær gjennom handling. 2. Leksene styrker instruksjonen. Selv om mange kanskje ville være fornøyd med å ikke ha leksene, ville kvaliteten på den utdanningen de får sikkert lide hvis den ble fjernet. Uansett om leksene er tildelte lesninger, oppgaver, etc., er alt av det designet for å styrke instruksjonen i studentenes sinn. Til slutt, de som gjør leksene er mer akademisk suksessrike enn de som ikke gjør det. Jeg mener at dette er en selvinnlysende sannhet, men jeg vil la Pro overbevise deg om det motsatte. 3. Leksene speiler virkelige krav. Etter videregående... [1,000 / 3,544 chars] |
| Bør reseptbelagte legemidler reklameres direkte til forbrukere? [63 chars] | Mange reklamer inneholder ikke nok informasjon om hvordan medisiner virker. For eksempel reklameres Lunesta med en sommerfugl som flyr inn gjennom et soveromsvindu over en person som sover fredelig. Faktisk hjelper Lunesta pasienter til å sovne 15 minutter raskere etter seks måneders behandling og gir 37 minutter mer søvn per natt. Flertallet av reklamene er basert på følelsesmessige appell, men få inkluderer årsaker til tilstanden, risikofaktorer eller viktige livsstilsendringer. I en studie av 38 farmasøytiske reklamer fant forskerne at 82 prosent gjorde en faktisk påstand og 86 prosent fremmet rasjonelle argumenter for produktbruk. Bare 26 prosent beskrev årsaker til tilstanden, risikofaktorer eller forekomst. Dette gir ikke pasientene balansert informasjon som ville gjøre dem oppmerksomme på at å ta en av pillene ikke er en magisk løsning på deres problem. Faktisk, ifølge en studie utført i USA og New Zealand, ba pasienter om resept i 12 prosent av de undersøkte besøkene. Av disse... [1,000 / 1,726 chars] |
| Skal barn få noen vaksiner? [27 chars] | Ikke et fullstendig tilfelle ennå... Bare noen små punkter jeg har satt sammen... Regjeringer bør ikke ha rett til å gripe inn i helsebeslutninger som foreldre tar for sine barn. Ifølge en undersøkelse fra University of Michigan i 2010, mener 31% av foreldrene at de bør ha rett til å nekte påbudte skoleinngangsvaksinasjoner for sine barn. Mange foreldre har religiøse overbevisninger mot vaksinasjoner. Å tvinge slike foreldre til å vaksinere sine barn ville stride mot 1. tillegget, som garanterer borgernes rett til å utøve sin religion fritt. Vaksiner er ofte unødvendige i mange tilfeller der trusselen om dødsfall fra sykdom er liten. På begynnelsen av 1800-tallet falt dødeligheten for barndomsykdommer som kikhoste, meslinger og skarlagensfeber drastisk før immunisering ble tilgjengelig. Denne nedgangen i dødelighet er blitt tilskrevet forbedret personlig hygiene, vannrensing, effektiv avløpshåndtering og bedre mat- og næringshygiene. Vaksiner forstyrrer naturlovene og Guds plan for men... [1,000 / 4,271 chars] |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | [https://doi.org/10.1007/978-3-030-58219-7_26](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | [https://doi.org/10.5281/zenodo.6862281](https://doi.org/10.5281/zenodo.6862281) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
