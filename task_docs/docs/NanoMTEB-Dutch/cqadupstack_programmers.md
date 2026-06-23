# NanoMTEB-Dutch / cqadupstack_programmers

## Overview

`cqadupstack_programmers` is the Dutch-translated Programmers, or Software
Engineering, subforum split of CQADupStack. Queries are conceptual programming
and software-engineering questions, and relevant documents are older forum
questions marked as duplicates. The Nano split contains 200 queries, 10,000
documents, and 200 positive qrel rows, with one positive duplicate per query.
It evaluates retrieval over design tradeoffs, programming practice, licensing,
learning frameworks, pointers, refactoring, interfaces, and professional
software-development process.

Unlike code-heavy splits, this task is mostly conceptual discussion retrieval.
BM25 can use terms such as algorithms, Django, licensing, .NET, pointers, class,
or interface, but duplicate identity often depends on the same design or
practice question being framed differently. Dense retrieval with
`harrier_oss_v1_270m` is strongest in top-10 ranking and ties
`reranking_hybrid` in recall@100. The split is useful for evaluating semantic
retrieval over developer questions that are long, translated, and often
opinion-like.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) uses Stack Exchange
duplicate links to define a retrieval task: given a later question, retrieve
the earlier question that duplicates it. The Programmers subforum differs from
more concrete technical support domains because many questions are about
software design principles, professional practice, methodology, and tradeoffs
rather than a specific error message or code snippet.

BEIR included CQADupStack in a common retrieval benchmark, and BEIR-NL
translated public BEIR datasets into Dutch. This task therefore keeps the
original duplicate relations while presenting Dutch-translated software-
engineering discussion posts. The retrieval challenge is to recognize
conceptual equivalence through translated prose.

### Observed Data Profile

The split contains 200 queries over 10,000 documents. Queries average 61.25
characters, while documents average 1,142.35 characters. Documents are often
long discussion posts containing background, motivation, constraints, and
several possible interpretations of a software-engineering issue.

Representative questions ask whether to keep investing in data structures and
algorithms, how to learn Django from examples, how to validate software
licenses through a home server, whether using the .NET Framework requires
payment to Microsoft, and how to explain pointers. These examples have some
technical anchors, but the positive relation is often a shared conceptual
question rather than the same wording.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2991, hit@10 = 0.4150, and recall@100 = 0.6050 over
top-500 candidate lists. Sparse retrieval can benefit from specific technology
and topic words such as Django, .NET, C#, license, pointer, interface, class,
algorithm, or Agile. When a duplicate question reuses these terms, BM25 can
rank it reasonably well.

BM25 is limited because many software-engineering duplicates are framed as
different practical concerns. A question about learning algorithms may be a
duplicate of one about becoming a stronger programmer; a licensing question may
use different legal or commercial language; a design-principle question may
share few exact terms. Term frequency captures the topic, but not always the
same tradeoff or professional concern.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.3906, hit@10 =
0.5600, and recall@100 = 0.7600. This is the strongest top-10 profile. The
large improvement over BM25 shows that embedding similarity is better suited to
conceptual programming duplicates, where paraphrase and intent matter more than
exact tokens.

Dense retrieval can connect questions about the same design issue even when
the wording changes. It can also match broad developer concepts such as
learning strategy, licensing validation, pointer explanation, or best-practice
tradeoffs. Its main risk is overgeneralization: many software-engineering posts
share a broad topic but ask different questions or take different perspectives.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3638, hit@10 =
0.5250, and recall@100 = 0.7600, with 100 to 101 candidates per query and 48
rank-101 safeguard rows. It ties dense retrieval in recall@100 but has weaker
top-10 ordering. This suggests that sparse evidence adds useful candidate
coverage without improving the initial ranking beyond dense retrieval.

The hybrid pool is still valuable for reranking. It preserves exact technical
terms that dense retrieval might underweight, while dense retrieval supplies
semantic candidates for paraphrased conceptual questions. A reranker should
learn when a shared technology name is central to the duplicate relation and
when it is merely a broad topic marker.

### Metric Interpretation for Model Researchers

Each query has one positive duplicate, so nDCG@10 reflects how highly the
duplicate is ranked. Hit@10 reflects user-visible retrieval, and recall@100
reflects whether a reranker can access the positive. Dense retrieval is the
best first-stage ordering here, while hybrid retrieval is a comparable
candidate source for downstream reranking.

This metric profile is typical of conceptual duplicate-question retrieval.
BM25 is helpful but not enough. Dense models capture more duplicate intent, but
reranking is needed to separate true duplicates from same-topic software-
engineering discussions.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated developer questions. They often ask whether
a practice is worthwhile, how to learn a tool, how licensing works, how to
explain a programming concept, or whether a design pattern is appropriate.
Relevant documents are longer prior questions that ask the same underlying
tradeoff or practice question.

The relevance type is conceptual duplicate identity. Two posts about Django,
licensing, or pointers are not automatically duplicates. A model must identify
whether the user's underlying decision or confusion is the same.

### Representative Failure Modes

BM25 can fail when duplicates use different professional vocabulary or when a
long document contains many incidental software terms. It can also over-rank
same-technology posts that ask a different question. Dense retrieval can fail
when it retrieves a broadly related software-engineering discussion that does
not duplicate the query's precise concern.

Hybrid failures occur when lexical and dense evidence both point to plausible
same-topic documents. A candidate can mention the same framework or concept but
answer a different tradeoff. Rerankers should compare the actual decision,
practice, or conceptual confusion expressed by the query and candidate.

### Training Data That May Help

Useful training data includes non-overlapping Software Engineering Stack
Exchange duplicate-question pairs, Dutch-translated developer discussion QA,
and conceptual programming duplicate-question data with overlap removed.
Training should exclude the translated Programmers test queries and duplicate
positives used by this Nano split.

Synthetic data can be generated from software-engineering discussion posts
outside the evaluation set. Create Dutch paraphrases that ask the same design,
process, or learning question from a different angle. Hard negatives should
share the technology or broad topic but ask about a different tradeoff.

### Model Improvement Notes

Improving this task requires semantic modeling of developer intent. Dense
models should be trained with conceptual duplicates and same-topic hard
negatives, not just code or documentation pairs. Topic labels such as Django or
.NET should be treated as helpful context but not as the relevance decision.

For rerankers, the most important behavior is deciding whether two questions
would reasonably share the same answer thread. Long translated documents should
be compared at the level of professional problem, design tradeoff, and
underlying confusion.

## Example Data

| Query | Positive document |
| --- | --- |
| Moet ik blijven investeren in datastructuren en algoritmes? [59 chars] | Hoe belangrijk is het leren van algoritmes voor programmeurs van hogere programmeertalen? **Mogelijk duplicaat:** > Hoe belangrijk is het bestuderen van algoritmes en theorie om een geweldige > programmeur te worden? Vandaag leerde ik het quicksort-algoritme. Ik betwijfel of ik ooit mijn eigen versie zal implementeren, aangezien C# zijn eigen ingebouwde sorteermethode heeft voor lijsten en arrays. Hoe belangrijk is het leren van algoritmes voor programmeurs van hogere programmeertalen? In mijn voorbeeld had ik geen voordeel van het kennen van het algoritme, maar was mijn voorbeeld misschien te triviaal om accuraat te zijn? [632 chars] |
| Django leren aan de hand van voorbeelden [40 chars] | Hoe begrijp ik het Django framework goed? Ik heb redelijke kennis van PHP, d.w.z. ik kan een framework pakken, de code lezen en als de documentatie adequaat is, begrijpen wat het doet. De belangrijkste reden hiervoor is dat PHP eigenlijk een zeer eenvoudige taal is die letterlijk gemaakt is voor webontwikkeling. Ik probeer nu een week Django te leren, ik kan er een basisapplicatie mee maken, maar er zijn gewoon te veel dingen die boven mijn pet gaan, d.w.z. die als magie lijken. De reden hiervoor is, denk ik, dat de hele interactie met de server onderdeel is van Django, terwijl dat in PHP allemaal door je server wordt afgehandeld. Ik wil meer lezen over dit onderdeel, d.w.z. welke onderwerpen moet ik behandelen om dit te 'begrijpen'. Suggesties voor boeken zijn ook welkom. [786 chars] |
| Licentieverificatie en contact opnemen met de thuisserver [57 chars] | Softwarelicentie veilig valideren Ik ontwikkel momenteel een product (in C#) dat gratis te downloaden is, maar een maandelijks abonnement vereist om na een specifieke proefperiode te kunnen gebruiken. Mijn bedoeling is dat de gebruiker een account registreert op onze website en deze opwaardeert met tegoed om de applicatie te gebruiken. Echter, ik loop als nieuwkomer in het licentievak tegen een aantal problemen aan: * Hoe wordt deze logica meestal geïmplementeerd? * Hoe verbind ik mijn C#-applicatie met de database van mijn website en haal ik de benodigde gegevens op (is de proefperiode verlopen, zo ja, heeft de gebruiker voldoende tegoed)? * Hoe zorg ik ervoor dat ik minstens 80% (of zo) beveiligd ben tegen aanvallers die een MITM-aanval zouden kunnen starten om de ontvangen pakketten te wijzigen en ongeautoriseerde toegang tot mijn programma te krijgen? * Zoals ik al gehoord heb, kan SSL garanderen dat mijn applicatie verbinding maakt met het juiste adres. Maar hoe maak ik zo'n verbi... [1,000 / 1,674 chars] |

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
| Moet ik blijven investeren in datastructuren en algoritmes? | A translated duplicate asks how important learning algorithms and theory is for becoming a strong programmer. |
| Django leren aan de hand van voorbeelden | A translated question asks how to understand the Django framework well by reading code and documentation. |
| Licentieverificatie en contact opnemen met de thuisserver | A translated post asks how to validate a software license securely for a subscription product. |
| Als ik .NET Framework gebruik voor mijn applicatie, moet ik dan iets aan Microsoft betalen? | A translated duplicate asks about selling a C# desktop application and whether .NET licensing creates payment obligations. |
| Wat is een goede uitleg voor pointers? | A translated question asks for a precise conceptual definition of a pointer in programming languages. |
