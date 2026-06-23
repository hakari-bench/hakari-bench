# NanoMTEB-Dutch / cqadupstack_english

## Overview

`cqadupstack_english` is the Dutch-translated English Language and Usage
subforum split of CQADupStack. The original topic is English grammar, wording,
idioms, punctuation, and usage, but the benchmark text presented to the
retriever is Dutch translation of those forum questions. The Nano split
contains 200 queries, 10,000 documents, and 200 positive duplicate links, with
one positive per query. It tests whether a retrieval model can identify older
duplicate questions about language usage when Dutch explanatory text contains
embedded English expressions.

The evaluation profile shows that dense retrieval is the strongest top-10
signal, BM25 is useful but limited, and `reranking_hybrid` gives the highest
top-100 coverage while ranking below dense at the top. This is a distinctive
duplicate-question task: exact quoted English phrases can be powerful lexical
anchors, but the true duplicate relation often depends on grammatical intent
rather than phrase reuse. Models must handle mixed-language text, translated
forum wording, and fine distinctions between similar English-usage questions.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
defines a duplicate-question retrieval benchmark from Stack Exchange subforums.
The retrieval task asks a system to find an older question that was marked as a
duplicate of a newer one. The English Language and Usage subset focuses on
questions about grammar, punctuation, word choice, idioms, and phrase meaning.

BEIR later included CQADupStack as part of a heterogeneous zero-shot retrieval
benchmark, and BEIR-NL translated public BEIR datasets into Dutch. This means
that `cqadupstack_english` is not a native Dutch grammar forum. It is a Dutch
translation of a forum about English usage, preserving quoted English examples
inside Dutch question text. The result is a retrieval problem with both Dutch
semantic context and English surface strings.

### Observed Data Profile

The split contains 200 short queries over 10,000 documents. Queries average
49.65 characters, and documents average 521.67 characters. Documents often
include a translated title, duplicate marker, quoted English expression, and a
body that explains the user's grammar or usage doubt. The short query may be
only a phrase such as "Het algemene 'het'" or a concise question about a dash,
capitalization, or preposition.

Representative examples ask what "it" refers to in a sentence, how to
punctuate a numeric range with a hyphen, where a preposition should stand, how
to capitalize "the" in proper names, and how to distinguish "part of" from "a
part of." These examples show why retrieval cannot be reduced to topic
matching. Many candidates can discuss articles, punctuation, or prepositions,
but only one is the known duplicate of the query.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2769, hit@10 = 0.3550, and recall@100 = 0.4950 over
top-500 candidate lists. Sparse retrieval has useful hooks in this task:
quoted English strings, punctuation symbols, grammar terms, and short phrases
can match directly between the query and positive document. When a duplicate
shares the same expression, BM25 can rank it well.

The limitation is that many duplicate questions are paraphrased. Two users may
ask the same grammar question with different examples, different Dutch
translation choices, or different levels of technical terminology. BM25 can
also overvalue a shared quoted word while missing that the grammatical issue is
different. The sparse profile therefore captures surface phrase overlap, but it
does not reliably capture the duplicate relation behind the usage question.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.3587, hit@10 =
0.5150, and recall@100 = 0.6500. This is the strongest top-10 ranking among the
three candidate sources. Dense retrieval is better suited to connecting
paraphrased grammar questions, such as different ways of asking about article
usage, punctuation functions, or preposition placement.

The score is still moderate rather than high. English Language and Usage
duplicates are often fine-grained: a question about one quoted expression may
look semantically close to another question about a different expression with a
similar grammatical structure. A dense model that captures only broad grammar
topic similarity can retrieve plausible but non-duplicate candidates. Strong
performance requires preserving the exact linguistic phenomenon under
discussion.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3248, hit@10 =
0.4250, and recall@100 = 0.6850, with 100 to 101 candidates per query and 63
rank-101 safeguard rows. Its top-10 ranking is lower than dense retrieval, but
its top-100 recall is higher. This shows the value of adding sparse candidates
when quoted English phrases or punctuation marks are crucial, even if the
initial hybrid order is noisier.

For reranking, this is an attractive candidate pool. It contains more positives
within the top 100 than either BM25 or dense alone, but it also contains many
same-phrase or same-topic distractors. A reranker should use both the quoted
English material and the Dutch question context to identify whether two posts
ask the same underlying grammar or usage question.

### Metric Interpretation for Model Researchers

With a single positive per query, nDCG@10 mostly reflects the rank assigned to
the known duplicate. Hit@10 reflects whether the duplicate appears in a user-
visible short list. Recall@100 is best read as reranking candidate coverage.
The metric pattern here says that dense retrieval is better for immediate
ranking, while the hybrid pool is better for making the positive available to a
second stage.

This split is therefore useful for testing a design choice. A dense-only system
may produce better first-stage ranking. A hybrid two-stage system may expose
more positives to a reranker, especially when exact quoted expressions matter.
The right conclusion depends on whether the downstream model can distinguish
true duplicate usage questions from merely similar grammar discussions.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated forum titles or questions about English
usage. They often include quoted English words, punctuation symbols, idiomatic
phrases, or grammatical labels. Relevant documents are prior forum questions
that duplicate the query's intent, not necessarily documents with identical
wording.

The task rewards models that understand the difference between surface form and
linguistic issue. A shared word such as "the", "part", or a dash mark can be
important, but the retrieval target is the matching grammatical question.

### Representative Failure Modes

BM25 can fail when a duplicate uses a different example phrase or when
translation changes the Dutch context around a quoted English expression. It
can also retrieve posts with the same quoted token but a different usage issue.
Dense retrieval can fail when two grammar questions are semantically close but
not duplicates, such as questions about related punctuation marks or similar
prepositional constructions.

Hybrid failures often combine these two effects. The pool may include a true
duplicate recovered by dense similarity and several lexical matches recovered by
quoted phrases. If the initial order overweights phrase overlap, the positive
can be pushed below same-surface distractors.

### Training Data That May Help

Useful training data includes non-overlapping CQADupStack English duplicate
question pairs, Dutch-translated grammar and usage duplicate questions, and
multilingual duplicate-question retrieval data where quoted phrases are
preserved. Training should exclude the translated English subforum test queries
and duplicate positives used by this Nano split.

Synthetic data can be built from non-evaluation English-usage forum questions
translated or written in Dutch. Generate pairs of paraphrased questions that ask
about the same grammatical phenomenon while changing the title wording, quoted
example, or explanatory context. Hard negatives should discuss a nearby
grammar topic or share a quoted token without being a duplicate.

### Model Improvement Notes

Improving this task requires mixed-language robustness. The model must encode
Dutch explanatory text while treating quoted English expressions as meaningful
retrieval evidence. Dense training should emphasize fine-grained linguistic
intent, and sparse-aware reranking should avoid treating every shared quoted
word as a duplicate signal.

For rerankers, the best improvement target is pairwise duplicate verification:
does the candidate question ask the same grammar or usage question as the
query? Models that can compare the quoted examples and the surrounding Dutch
explanation should benefit most from the high-recall hybrid pool.

## Example Data

| Query | Positive document |
| --- | --- |
| Het algemene 'het [17 chars] | Waar verwijst 'het' naar in dit voorbeeld? **Mogelijk duplicaat:** > Het regent. Wat dan? 'Het regent.' Waar verwijst 'het' naar? Ik weet dat sommige mensen 'het weer' zouden zeggen, maar je zou niet zeggen: 'Het weer regent.' Maar je zou wel zeggen: Hoe is het weer? Het regent.' Beetje verwarrend. [301 chars] |
| Hoe moet je een bereik van getallen met een koppelteken interpunctiëren? [72 chars] | Wat is het verschil tussen - en -- in een zin? **Mogelijke dubbel:** > Wanneer moet ik een em-dash, een en-dash en een koppelteken gebruiken? Wanneer plaats ik een - in een zin? Is het een sterkere komma? Met een langere pauze? [229 chars] |
| Kiezen tussen "experimenteren met" en "waarmee te experimenteren [64 chars] | Waar moet het voorzetsel van "goedkeuren" staan? **Mogelijke dubbel:** > Wanneer is het gepast om een zin met een voorzetsel te eindigen? In dit antwoord schreef ik > [Je kunt het gebruiken] om foto's te maken van een film in een bioscoop, waarvan > de bioscoopmedewerkers waarschijnlijk geen goedkeuring zouden geven. maar ik weet niet zeker of het beter zou zijn > [Je kunt het gebruiken] om foto's te maken van een film in een bioscoop, waaraan de bioscoopmedewerkers waarschijnlijk geen goedkeuring zouden geven. Ik vond deze pagina, maar ik kan nog steeds niet vinden op welk voorbeeld het betrekking heeft. (... op welk voorbeeld het betrekking heeft?) [660 chars] |

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
| Het algemene "het" | A translated duplicate asks what "it" refers to in a sentence such as "It is raining" and discusses whether it points to the weather. |
| Hoe moet je een bereik van getallen met een koppelteken interpunctieren? | A translated duplicate compares a hyphen, en dash, and em dash, asking when each mark should be used in a sentence. |
| Kiezen tussen "experimenteren met" en "waarmee te experimenteren" | A translated duplicate asks where a preposition should stand and whether ending a sentence with a preposition is appropriate. |
| Hoofdletterregels voor "the" | A translated post discusses capitalization of definite articles in names of people, places, and things. |
| Wat is het verschil tussen "part of" en "a part of"? | A translated duplicate asks about the difference between "part" and "a part" and why the article changes the meaning. |
