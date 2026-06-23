# NanoMTEB-Dutch / cqadupstack_physics

## Overview

`cqadupstack_physics` is the Dutch-translated Physics subforum split of
CQADupStack. Queries are physics questions, and relevant documents are older
questions from the same Stack Exchange domain marked as duplicates. The Nano
split contains 200 queries, 10,000 documents, and 200 positive qrel rows, with
one positive duplicate per query. It evaluates retrieval over mechanics,
relativity, acoustics, thermodynamics, quantum mechanics, mathematical models,
constants, and scientific notation.

The task has a clearer conceptual structure than many general forum datasets,
but it is still difficult because duplicate physics questions can be phrased at
different levels of abstraction. BM25 benefits from formulas, named concepts,
and technical terms. Dense retrieval with `harrier_oss_v1_270m` is strongest in
top-10 ranking, while `reranking_hybrid` has slightly higher recall@100 but a
weaker top order. The task is useful for testing whether a model understands
physics-question intent rather than only matching symbols or broad scientific
topics.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) defines a duplicate-
question retrieval benchmark from Stack Exchange data. A query is a later
question, and the system must retrieve the older question that was marked as a
duplicate. Physics is a domain where duplicate questions often ask about the
same concept, equation, or apparent paradox using different examples and
levels of mathematical detail.

BEIR included CQADupStack as part of a broad zero-shot retrieval benchmark, and
BEIR-NL translated the public BEIR datasets into Dutch. In this split, the
prose is Dutch-translated, while variables, equations, constants, and many
scientific names remain recognizable. The benchmark therefore mixes natural
language semantic retrieval with formula-aware and concept-aware matching.

### Observed Data Profile

The split has 200 queries over 10,000 documents. Queries average 62.09
characters, and documents average 870.44 characters. Documents often contain
equations, variables, images, derivations, or long conceptual setup. The
positive duplicate may be a broader or narrower version of the same physics
question.

Representative questions ask how the Schrodinger equation is a wave equation,
how active noise-cancellation technology is measured, whether continuous
mathematical models create problems for discrete phenomena, whether energy can
gravitate, and why relativistic mass increases near light speed. These examples
show that the target is a shared physical concept or confusion, not merely the
same words.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.3269, hit@10 = 0.4250, and recall@100 = 0.6250 over
top-500 candidate lists. This is a useful sparse baseline because physics
questions often contain distinctive terms, formulas, symbols, constants, or
named equations. Exact words such as Schrodinger, relativity, mass, wave, or
noise cancellation can be strong retrieval anchors.

BM25 still misses many duplicates. The same physics issue can be described with
different terminology, such as a question about relativistic mass versus a
question about energy and black holes. Formula overlap can also be misleading
when two posts share variables but ask different conceptual questions. BM25 is
therefore good at finding nearby physics material, but less reliable for
identifying the exact duplicate question.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.4020, hit@10 =
0.5450, and recall@100 = 0.7500. It is the strongest top-10 candidate profile.
Dense retrieval improves over BM25 because it can connect paraphrased
conceptual questions and capture that two posts are asking about the same
underlying physical principle.

The remaining errors likely come from concept-adjacent hard negatives. Physics
has many questions that are semantically close but not duplicates: two posts may
both mention waves, mass, energy, or quantum mechanics while asking about
different derivations or interpretations. Strong dense retrieval must preserve
the exact conceptual relation requested by the query, not only the topic area.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3756, hit@10 =
0.5050, and recall@100 = 0.7550, with 100 to 101 candidates per query and 49
rank-101 safeguard rows. It has the best top-100 coverage, but dense retrieval
has the better top-10 order. This indicates that adding sparse evidence helps
recover a few more positives, while also introducing lexical or formula-near
distractors into the top ranks.

For a reranking system, this is a useful setup. The hybrid pool usually
contains the positive by top 100, but the initial order can be noisy. A reranker
must decide whether shared symbols or terms correspond to the same physics
question, or whether a dense semantic match better captures the duplicate
intent.

### Metric Interpretation for Model Researchers

Because there is one positive duplicate per query, nDCG@10 measures the rank of
that duplicate, hit@10 measures short-list visibility, and recall@100 measures
candidate-pool coverage. Dense retrieval is the best first-stage ranker, while
hybrid retrieval gives slightly broader coverage for reranking.

This metric pattern suggests that physics duplicate retrieval benefits from
semantic modeling, but exact symbols and named concepts still matter. A
production-style system might use hybrid candidate generation, then apply a
reranker trained to distinguish true conceptual duplicates from same-topic
physics neighbors.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated physics questions. They often contain a
named concept, physical quantity, equation name, or conceptual contradiction.
Relevant documents are longer prior questions that duplicate the same physical
problem or confusion, sometimes with more mathematical detail.

The relevance relation is concept identity. Two candidates can both discuss
relativity or quantum mechanics but differ in the actual question. Conversely,
a true duplicate can use different examples if the same principle is being
asked about.

### Representative Failure Modes

BM25 can fail when different terminology points to the same concept, or when
shared equations appear in non-duplicate contexts. Dense retrieval can fail by
ranking a concept-adjacent question highly even though it asks about a different
derivation, interpretation, or physical regime.

Hybrid failures often involve equation-near candidates. A candidate may share a
formula, symbol, or named phenomenon but answer a different conceptual
question. Rerankers need to compare the role of the concept in the query and in
the candidate document.

### Training Data That May Help

Useful training data includes non-overlapping Physics Stack Exchange duplicate
pairs, Dutch-translated scientific QA pairs, formula-aware STEM duplicate
retrieval data, and multilingual physics paraphrase data with overlap removed.
Training should exclude the translated Physics test queries and duplicate
positives used by this Nano split.

Synthetic data can use physics forum questions outside the evaluation set.
Preserve equations and variables, but generate Dutch paraphrases that ask the
same conceptual question in different words. Hard negatives should share
variables, equations, or topics while asking about a different physical
principle.

### Model Improvement Notes

Improving this task requires concept-aware retrieval. Dense models should be
trained to align paraphrased scientific questions while separating nearby
concepts. Symbol-aware reranking can help when formulas are important, but the
model must not treat every shared equation as a duplicate signal.

The strongest systems should combine formula and terminology awareness with
semantic reasoning over the question's physical intent. That is especially
important for relativity, quantum mechanics, and thermodynamics examples where
surface terms repeat across many non-duplicate questions.

## Example Data

| Query | Positive document |
| --- | --- |
| Hoe is de Schrödingervergelijking een golffvergelijking? [56 chars] | Relatie tussen de Schrödingervergelijking en de golfvergelijking Ik ben altijd in de war geweest over de relatie tussen de Schrödingervergelijking en de golfvergelijking. $$ i\hbar \frac{\partial \psi}{\partial t} = - \frac{\hbar^2}{2m} \nabla^2+ U \psi \hspace{0.25in}\text{-vs-}\hspace{0.25in}\nabla^2 E = \frac{1}{c^2}\frac{\partial^2 E}{\partial^2 t} $$ Vanwege de eerste afgeleide lijkt de Schrödingervergelijking meer op de warmtevergelijking. Sommige afleidingen van de Schrödingervergelijking beginnen met golf-deeltjes dualiteit voor licht en betogen dat materie dit fenomeen ook zou moeten vertonen. In sommige aantekeningen van Fermi werd deze afgeleid door het Fermat principe van de kortste tijd $\delta \int n \;ds = 0 $ en het Maupertuis principe van de kleinste actie $\delta \int 2T(t) \; dt = 0 $ te vergelijken. Is dit ooit verduidelijkt? Hoe kunnen we het idee van een materiegolf kwantitatiever bekijken? * * * Samengevat, ik probeer te begrijpen waarom de elektromagnetische gol... [1,000 / 1,081 chars] |
| Metingen van actieve ruisonderdrukkingstechnologie [50 chars] | Maximale vertraging voor effectieve actieve ruisonderdrukking? Actieve ruisonderdrukking vermindert ongewenste geluiden door de omgekeerde fase van de originele fase te verzenden: ![Actieve ruisonderdrukking](http://i.stack.imgur.com/0jSp8.png) (Bron: Wikipedia) Theoretisch lijkt dit logisch. In de praktijk moet het antigeluid echter worden gegenereerd door een hardware- of softwaresysteem (zoals actieve ruisonderdrukkende hoofdtelefoons), wat tijd kost. Ik neem daarom aan dat het antigeluid altijd vertraagd is ten opzichte van het originele geluid: ![Actieve ruisonderdrukking met vertraging](http://i.stack.imgur.com/XBMyk.png) Mijn vragen: * Hoeveel (in milliseconden of wat dan ook) is de _maximale_ vertraging die "toegestaan" is voor actieve ruisonderdrukking zodat de luisteraar van het geluid+antigeluid het effect nog steeds merkt? * Hangt de "toegestane" vertraging af van welk geluid er moet worden onderdrukt (bijv. een rijdende auto, mensen die praten, muziek)? [985 chars] |
| Zijn continue wiskundige modellen van discrete fysische verschijnselen rommelig vanwege een discrepantie tussen "continu" en "discontinu"? [138 chars] | Wat is het "discrete" analogon van de "continuüm" mechanica? Als ik een discrete wiskundige benadering van de continuümmechanica wil verkennen, welke leerboeken moet ik dan raadplegen? Een kant-en-klaar antwoord op de vraag zou kunnen zijn: "computationele continuümmechanica", maar leerboeken die dit onderwerp behandelen, zijn meestal gericht op het toepassen van numerieke analyse op continue theorieën (d.w.z. de basis is continu), terwijl ik wil weten of er een behandeling van het onderwerp bestaat die opgebouwd is vanuit een discrete basis. [549 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | [https://doi.org/10.1145/2838931.2838934](https://doi.org/10.1145/2838931.2838934) |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | [https://aclanthology.org/2025.bucc-1.5/](https://aclanthology.org/2025.bucc-1.5/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| clips/beir-nl-cqadupstack |  | dataset card | [https://huggingface.co/datasets/clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Hoe is de Schrodingervergelijking een golfvergelijking? | A translated duplicate asks about the relation between the Schrodinger equation and the classical wave equation, including mathematical notation. |
| Metingen van actieve ruisonderdrukkingstechnologie | A translated question discusses maximum delay for effective active noise cancellation and phase inversion. |
| Zijn continue wiskundige modellen van discrete fysische verschijnselen rommelig? | A translated post asks about the discrete analogue of continuum mechanics and relevant references. |
| Gravitatie van energie | A translated duplicate asks whether a black hole could form through Lorentz contraction or high-speed mass-energy effects. |
| Waarom neemt relativistische massa toe naarmate snelheid de lichtsnelheid benadert? | A translated question discusses confusion about relativistic mass depending on velocity and reference frame. |
