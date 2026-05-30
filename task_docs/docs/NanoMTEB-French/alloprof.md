# NanoMTEB-French / alloprof

## Overview

`alloprof` is a French educational retrieval task based on Alloprof, a Quebec
school-help resource. Queries are student questions in French, and documents
are long lesson-style educational explanations. The Nano split contains 200
queries, 2,556 documents, and 200 positive qrel rows, with exactly one positive
lesson per query. It evaluates whether a retrieval model can connect informal
student questions to the appropriate pedagogical resource.

This task is difficult for simple keyword matching because queries are often
long, noisy, and student-written, while documents are long structured lessons.
BM25 is moderate, dense retrieval with `harrier_oss_v1_270m` is much stronger,
and `reranking_hybrid` is strongest overall in the reported metrics. The task
is useful for evaluating French educational retrieval where spelling variation,
partial attempts, school vocabulary, and concept-level matching all matter.

## Details

### What the Original Data Measures

[MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468)
includes AlloprofRetrieval as a French retrieval task. Alloprof is a Quebec
educational help platform with resources and forum-style support for students.
No standalone retrieval paper was confirmed for this task, so interpretation
uses MTEB-French, public dataset cards, and the observed Nano examples.

In retrieval form, the student question is the query and the target is the
lesson or educational resource that answers it. The task covers mathematics,
grammar, history, science, writing, and other school subjects.

### Observed Data Profile

Queries average 179.29 characters, much longer than typical web-search queries.
Some are concise concept questions, but many are student messages with
greetings, spelling mistakes, grade-level context, and partial understanding.
Documents average 3,504.53 characters and often include definitions, examples,
formulas, and explanatory sections.

Representative questions ask about the simple past versus past progressive,
irreducible and equivalent fractions, electrical resistors, litmus paper and
pH, and the meaning of a sum. The positive document is usually a lesson that
explains the concept rather than a short direct answer.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.3447, hit@10 = 0.4850, and recall@100 = 0.7900 over
top-500 candidate lists. Sparse retrieval works when the student uses a
distinct subject term such as probability, fraction, resistor, pH, or a
historical name. It struggles when the query contains conversational text,
misspellings, or vague descriptions of a school concept.

Long lesson documents also dilute lexical evidence. A relevant document may
contain the needed concept but not repeat the exact student wording. BM25 is
therefore a useful first signal but not sufficient for robust educational
retrieval.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.5139, hit@10 =
0.6750, and recall@100 = 0.8950. Dense retrieval substantially improves over
BM25 because it can map informal student wording to lesson concepts. It is
better at connecting a partial question to the underlying curriculum topic.

The remaining dense errors likely involve closely related school concepts:
several lessons can be about fractions, electricity, grammar tenses, or
writing structure, but only one explains the student's exact need. Dense
models must preserve concept specificity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.5214, hit@10 =
0.7000, and recall@100 = 0.9150, with 100 to 101 candidates per query and 17
rank-101 safeguard rows. It is the strongest candidate profile. Hybrid search
adds lexical school-subject anchors to dense concept matching and improves
both top-10 success and top-100 coverage.

For reranking, this pool is attractive because it contains semantic matches
and exact-topic matches. A reranker should decide which long lesson actually
answers the student's question, not merely which lesson shares a school subject.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 measures the rank of the target
lesson. Hit@10 measures whether a student would see the correct resource
quickly, and recall@100 measures reranking coverage. The clear improvement from
BM25 to dense and hybrid shows that educational semantic matching is central.

Because documents are long, top-ranked retrieval quality depends on concept
selection rather than isolated term overlap. Rerankers should be evaluated for
whether they can identify answerability inside long pedagogical text.

### Query and Relevance Type Tendencies

Queries are student-authored French questions, sometimes with informal tone,
misspellings, or contextual statements. Relevant documents are lesson-style
resources that explain a concept or procedure.

Relevance is pedagogical answerability. A lesson from the same subject is not
enough unless it directly explains the student's problem.

### Representative Failure Modes

BM25 can fail on spelling variation, conversational filler, or mismatched
terminology. Dense retrieval can fail by retrieving a related lesson that
covers the same broad subject but not the exact concept. Hybrid retrieval can
still include several same-subject lessons that require reranking.

Hard negatives should be lessons from the same school subject and grade level
but covering a different concept.

### Training Data That May Help

Useful training data includes French educational forum question-resource
pairs, Quebec school-subject QA and lesson retrieval data, French pedagogical
explanations with student questions, and hard negatives from the same school
subject. Training should exclude Alloprof test examples, Nano queries, qrels,
and positive lesson documents likely to overlap with this evaluation.

Synthetic data can be generated by writing French lesson-style documents for
mathematics, grammar, history, science, and writing, then creating realistic
student questions with spelling variation and partial attempts. Each positive
lesson should directly explain the needed concept or procedure.

### Model Improvement Notes

Improving this task requires robust French educational semantics. Dense models
should learn to map informal learner language to curriculum concepts. Rerankers
should inspect long lessons and identify whether the explanation actually
answers the student question.

Hybrid retrieval is currently the strongest setup because it keeps exact
school terms while adding semantic concept matching.

## Example Data

### Public Sources

- [MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468), 2024.
- [mteb/AlloprofRetrieval](https://huggingface.co/datasets/mteb/AlloprofRetrieval), source dataset card.
- [antoinelb7/alloprof](https://huggingface.co/datasets/antoinelb7/alloprof), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis | 2024 | arXiv paper | https://arxiv.org/abs/2405.20468 |
| mteb/AlloprofRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/AlloprofRetrieval |
| antoinelb7/alloprof |  | dataset card | https://huggingface.co/datasets/antoinelb7/alloprof |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Bonjour, j'ai de la difficulté à comprendre les différences entre le simple past et le past progressive. | A lesson explains how the past continuous describes actions happening in the past and contrasts it with other past-tense uses. |
| Je voudrais des trucs pour mémoriser les fractions irréductible et équivalente. | A lesson explains equivalent fractions and how multiplying or dividing by a unit fraction gives an equivalent value. |
| A quoi servent les résistances dans un circuit électrique? | A lesson explains electrical resistance as a property that limits current in a circuit. |
| L'eau est un pH 7, alors le papier tournesol rouge et bleu ne réagit pas? | A lesson explains litmus paper and how indicators determine whether a substance is acidic, basic, or neutral. |
| C'est quoi une somme? | A lesson explains addition, terms, and the sum as the result of the operation. |
