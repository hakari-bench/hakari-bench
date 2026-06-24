# NanoMTEB-Polish / cqadupstack_physics

## Overview

`cqadupstack_physics` is the Polish NanoMTEB version of the Physics subset from CQADupStack. The task evaluates duplicate-question retrieval for translated physics forum posts: a short Polish query must retrieve longer candidate questions that ask the same physical concept, calculation, or explanation. The data covers topics such as quantum mechanics, gravity, relativistic mass, active noise cancellation, discrete and continuous models, superconductivity, cosmology, inertial frames, and heat transfer.

The Nano split contains 200 queries, 10,000 documents, and 621 positive relevance judgments. Queries average about 59 characters, while documents average about 815 characters. The task has substantial duplicate clustering: 83 queries have multiple positives, the average positives per query is 3.105, and the largest cluster has 72 positives. This makes it a useful benchmark for testing whether a model can recover many formulations of the same physics question, from informal intuition to equation-heavy explanation.

## Details

### What the Original Data Measures

CQADupStack defines relevance through duplicate links in community question answering. In the Physics subset, two posts are relevant when they ask the same physics problem, not merely when they share a topic such as gravity, quantum mechanics, or relativity. The same concept may appear in colloquial language, in mathematical notation, or in a more formal theoretical framing.

This is a good retrieval task for studying semantic abstraction. A query such as "gravity from energy" may be equivalent to a longer post about whether non-mass energy generates a gravitational field. A query about the Schrödinger equation being a wave equation may map to a detailed explanation using differential equations. Models must connect physical meaning across differences in wording, notation, and level of formality.

### Observed Data Profile

The documents are moderately long and often contain explanations, equations, diagrams, or context about the physical setup. The Polish translation keeps the conceptual question in Polish while preserving names, equations, and symbols. This makes both language understanding and mathematical-scientific terminology important.

The relevance distribution is mixed. Many queries have a single positive, but the multi-positive rate is 41.5%, and some common physics questions have large duplicate clusters. A model that retrieves one good explanation may still miss many relevant duplicates if it does not recognize alternative formulations of the same concept.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3359, hit@10 of 0.5450, and recall@100 of 0.4364. This is a stronger lexical baseline than in some other CQADupStack splits because physics questions often contain distinctive terms: Schrödinger, Hubble, gravitational, relativistic, superconductivity, energy, wave equation, and similar anchors.

The limitation is that duplicate physics questions often use different conceptual language. A colloquial question about mass increasing near light speed may correspond to a formal discussion of relativistic momentum. A question about energy and gravity may use stress-energy terminology in the relevant document. BM25 can find shared technical vocabulary, but it does not reliably bridge informal and formal statements of the same physical idea.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is strongest at the top of the ranking, with nDCG@10 of 0.4306, hit@10 of 0.6750, and recall@100 of 0.5475. The large gain over BM25 shows that embedding similarity captures many conceptual equivalences that lexical matching misses. Dense retrieval is particularly useful when the same principle is described through different examples, levels of mathematical detail, or explanatory style.

This profile indicates that the task rewards semantic understanding of physics questions more than exact term frequency. Dense retrieval can connect "non-mass energy generating gravity" with stress-energy explanations, or a short query about the Schrödinger equation with a longer wave-equation discussion. It is therefore the best direct first-stage ranking among the three profiles for top-10 quality.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.4024, hit@10 of 0.6100, and recall@100 of 0.5491. Candidate lists contain 100 to 101 items, and 27 rows use the positive safeguard. Hybrid recall is slightly higher than dense recall, but top-10 ranking is lower than the dense run.

This result shows that hybrid candidate construction is useful for preserving relevant documents, but dense retrieval is better as a direct ranked output for this split. The hybrid candidate pool still matters for reranking experiments because it combines exact scientific terms with semantic matches. A strong reranker may be able to use the broader hybrid pool while restoring dense-like or better top-rank ordering.

### Metric Interpretation for Model Researchers

This task is dense-favorable at top 10 and hybrid-favorable only by a narrow margin in recall@100. BM25 is a useful baseline because physics terminology is distinctive, but it misses many conceptual duplicates. Dense retrieval's higher nDCG@10 and hit@10 indicate that semantic similarity is central to the task.

Researchers should separate direct retrieval from candidate generation. If the goal is to return the best answers immediately, dense retrieval is the stronger reference profile. If the goal is to create a candidate set for a reranker, `reranking_hybrid` may be preferable because it preserves a slightly larger fraction of positives at top 100.

### Query and Relevance Type Tendencies

Representative queries ask how the Schrödinger equation is a wave equation, how active noise reduction can be measured, whether continuous mathematical models are awkward for discrete physical phenomena, whether energy without rest mass generates gravity, and why relativistic mass is said to increase near light speed. These examples show the range of the task: conceptual clarification, mathematical formulation, experimental setup, and terminology debates.

Relevant documents may be written at different levels. Some are intuitive questions; others include equations or formal definitions. A strong retrieval model should recognize the shared physical principle even when the query and document use different explanatory registers.

### Representative Failure Modes

BM25-style systems may retrieve documents that share scientific terms but ask a different principle. Many posts can mention gravity, energy, or relativity without being duplicates. Dense systems may retrieve conceptually adjacent physics questions that are educationally similar but not equivalent. This is especially likely in broad areas such as quantum mechanics or cosmology.

Another failure mode is mishandling notation. Equations and symbols can be central to relevance, but they may appear alongside translated prose. A model that ignores notation may miss a duplicate; a model that overweights notation may retrieve a mathematically similar but conceptually different question.

### Training Data That May Help

Useful training data includes Physics Stack Exchange duplicate pairs, Polish science QA, translated educational physics explanations, and hard negatives sharing entities or formulas but asking different principles. Data should include both informal questions and formal explanations to teach models the mapping between intuitive and technical formulations.

Hard negatives should include near-topic questions about the same phenomenon but different conceptual focus, such as gravity from mass versus gravity from energy, or several relativity questions that differ in whether they ask about mass, momentum, or measurement.

### Model Improvement Notes

Dense models can improve by better representing scientific concepts, equations, and explanatory paraphrases across Polish text. Sparse systems can improve through normalization of Polish scientific terms and named equations, but exact matching alone is unlikely to beat dense retrieval. Hybrid systems are useful for candidate generation, especially when a reranker can resolve conceptual equivalence.

For evaluation, nDCG@10 should be used to judge direct search quality, while recall@100 should be used to judge first-stage usefulness for reranking. This split makes that distinction visible because dense is best at the top, while hybrid narrowly leads in candidate coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| Jak równanie Schroedingera jest równaniem falowym? [50 chars] | związek między równaniem Schrodingera a równaniem falowym Zawsze byłem zdezorientowany związkiem między równaniem Schrödingera a równaniem falowym. $$ i\hbar \frac{\partial \psi}{\partial t} = - \frac{\hbar^2}{2m} \nabla^2+ U \psi \hspace{0.25in}\text{-vs -}\hspace{0.25in}\nabla^2 E = \frac{1}{c^2}\frac{\partial^2 E}{\partial^2 t} $$ Ze względu na pierwszą pochodną Schrödingera równanie wygląda bardziej jak równanie ciepła. Niektóre wyprowadzenia równania Schrodingera zaczynają się od dualizmu falowo-cząsteczkowego dla światła i dowodzą, że materia również powinna wykazywać to zjawisko. W niektórych notatkach Fermiego została ona wyprowadzona przez porównanie zasady najmniejszego czasu Fermata $\delta \int n \;ds = 0 $ i zasady najmniejszego działania Maupertuisa $\delta \int 2T(t) \; dt = 0 zł. Czy to kiedykolwiek zostało wyjaśnione? Jak możemy bardziej ilościowo zobaczyć ideę fali materii? * * * Podsumowując, próbuję zrozumieć, dlaczego równanie fal elektromagnetycznych jest hiperbol... [1,000 / 1,059 chars] |
| Pomiary technologii aktywnej redukcji szumów [44 chars] | Maksymalne opóźnienie efektywnej aktywnej redukcji szumów? Aktywna redukcja szumów redukuje niechciany dźwięk, wysyłając odwróconą fazę oryginalnej fazy: ![Aktywna redukcja szumów](http://i.stack.imgur.com/0jSp8.png) (Źródło: Wikipedia) Teoretycznie wydaje się to logiczne ja. Jednak w rzeczywistości eliminacja szumów musi być tworzona przez jakiś system sprzętowy lub programowy (np. słuchawki z aktywną redukcją szumów), co wymaga czasu. Zakładam więc, że anty-hałas jest zawsze opóźniony do oryginalnego dźwięku: ![Aktywna redukcja szumów z opóźnieniem](http://i.stack.imgur.com/XBMyk.png) Moje pytania: * Ile (w milisekundach) lub cokolwiek) jest _maksymalnym_ opóźnieniem, które jest „dozwolone” dla aktywnej redukcji szumów, tak aby słuchacz hałasu + antyhałas nadal zauważał efekt? * Czy „dozwolone” opóźnienie zależy od tego, jaki hałas ma zostać skasowany (np. jazda samochodem, ludzie mówiący, muzyka)? [913 chars] |
| Czy ciągłe modele matematyczne dyskretnych zjawisk fizycznych są bałaganiarskie z powodu rozłączenia między „ciągłym” i „nieciągłym”? [133 chars] | Jaki jest „dyskretny” odpowiednik mechaniki „ciągłej”? Gdybym chciał zbadać podejście matematyki dyskretnej do mechaniki kontinuum, do jakich podręczników powinienem się zajrzeć? Przypuszczam, że gotową odpowiedzią na to pytanie może być: „obliczeniowa mechanika kontinuum”, ale zwykle podręczniki poruszające taki temat koncentrują się zwykle na zastosowaniu analizy numerycznej do teorii ciągłych (tj. baza jest ciągła), natomiast chciałbym wiedzieć, czy istnieje traktowanie tematu, które buduje się z podstawy, która jest dyskretna. [536 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original duplicate-question retrieval construction. |
| MTEB paper | Benchmark framing for retrieval tasks. |
| CLARIN-KNEXT dataset card | Polish translated Physics subset. |
| MTEB task card | Task packaging and retrieval interface. |

### Representative Snippets

- A query asks how the Schrödinger equation is a wave equation; relevant posts discuss its relation to wave-equation forms.
- A query asks about measuring active noise reduction; relevant documents describe phase inversion and cancellation limits.
- A query asks whether continuous models are awkward for discrete physical phenomena; relevant posts discuss discrete analogues of continuum mechanics.
- A query asks whether non-mass energy generates gravity; relevant documents discuss stress-energy and gravitational fields.
- A query asks why relativistic mass increases near light speed; relevant posts compare relativistic mass and momentum.
