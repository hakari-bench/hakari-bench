# NanoMTEB-Dutch / cqadupstack_mathematica

## Overview

`cqadupstack_mathematica` is the Dutch-translated Mathematica subforum split of
CQADupStack. Queries are Wolfram Language and Mathematica support questions,
and relevant documents are older questions marked as duplicates. The Nano split
contains 200 queries, 10,000 documents, and 200 positive qrel rows, with one
positive duplicate per query. It measures duplicate-question retrieval for
symbolic computation, notebook behavior, plotting, interpolation, functional
programming constructs, and code snippets in translated technical forum text.

This is one of the harder Dutch CQADupStack profiles. Documents are long,
averaging 1,166.66 characters, and the data mixes Dutch-translated prose with
untranslated code tokens and mathematical notation. BM25 is weak, dense
retrieval is only slightly stronger, and `reranking_hybrid` has the best
overall profile but remains moderate. The task is a useful stress test for
retrieval models that must understand code-adjacent duplicate intent rather
than merely match function names.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) was created from
Stack Exchange duplicate links and defines retrieval splits where newer
questions must retrieve older duplicates. The Mathematica subforum contributes
code-heavy support questions about the Wolfram Language, symbolic and numeric
computation, plotting, notebook interfaces, and expression manipulation.

BEIR packaged CQADupStack into a common retrieval benchmark, and BEIR-NL
translated the public BEIR tasks into Dutch. In this split, ordinary prose is
Dutch-translated, while many code tokens, function names, mathematical
expressions, and TeX fragments remain close to the original. The retrieval
problem is therefore mixed-language and mixed-format: models must combine
natural-language semantics with programming and mathematical cues.

### Observed Data Profile

The task has 200 short queries over 10,000 documents. Queries average 55.30
characters, while documents average 1,166.66 characters. The long document
length reflects forum posts that include code examples, attempted solutions,
error messages, mathematical expressions, and explanatory text.

Representative questions ask why `DeleteDuplicatesBy` does not behave as
expected, whether plot colors can be changed after `Show`, how to obtain a
polynomial interpolation formula, how to pass a function or formula as an
argument, and how to use `ToExpression` and `TeXForm`. These examples show that
the positive duplicate may share a function name, but the real match is the
same computational operation or programming problem.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.1826, hit@10 = 0.2750, and recall@100 = 0.4350 over
top-500 candidate lists. Sparse retrieval can use exact code tokens such as
`DeleteDuplicatesBy`, `Show`, `Plot`, `ToExpression`, and `TeXForm`, and it can
match mathematical symbols or quoted snippets when they are preserved. These
anchors are helpful, but not enough.

The weak BM25 profile reflects several difficulties. Queries are short,
documents are long, and many posts contain multiple function names that are not
central to the duplicate relation. Different users may describe the same
operation with different code, or use the same function in unrelated contexts.
Translation also changes the explanatory prose around otherwise identical code
tokens. BM25 therefore finds some code-near candidates but often misses the
true duplicate.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.1992, hit@10 =
0.3050, and recall@100 = 0.5250. Dense retrieval improves over BM25, especially
in recall, but the improvement is modest. This suggests that the model captures
some semantic similarity between paraphrased Mathematica questions, but still
struggles with code-specific intent.

The difficulty is that natural-language embedding similarity may treat many
Mathematica questions as close if they concern plotting, lists, functions, or
symbolic expressions. A true duplicate can depend on a precise operation:
removing duplicates, changing plot properties after creation, passing functions
as arguments, or converting TeX input. Dense models need code-aware and math-
aware representations to distinguish these fine-grained tasks.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.2181, hit@10 =
0.3150, and recall@100 = 0.5750, with 100 to 101 candidates per query and 85
rank-101 safeguard rows. It is the best of the three candidate profiles, but
the absolute scores remain low. The high number of safeguard rows indicates
that many positives are recovered only at the edge of the hybrid candidate
pool.

Hybrid retrieval helps because exact code tokens and dense semantic similarity
cover different parts of the task. BM25 can preserve rare function names, while
dense retrieval can connect paraphrased descriptions of the same operation. The
reranking challenge is substantial: the pool contains many candidates sharing
the same function or broad concept but requiring different Mathematica behavior.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how high the duplicate is ranked,
and recall@100 measures whether candidate generation is adequate for reranking.
The metric pattern shows that all first-stage methods are under stress. Dense
retrieval improves recall, and hybrid search improves it further, but top-10
ranking remains difficult.

This makes the split valuable for evaluating code-adjacent retrieval rather
than general Dutch semantic retrieval. A model that performs well here likely
handles exact code tokens, translated explanatory text, and fine-grained
programming intent. A weak model may retrieve posts about the same function
without retrieving the duplicate question.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated Mathematica questions, often containing
function names, code snippets, mathematical terms, or interface vocabulary.
Relevant documents are longer prior questions that duplicate the user's
problem. The duplicate may be expressed with different code or a broader title.

Relevance depends on operation identity. Two documents can both mention
`Plot`, `Interpolation`, or `ToExpression` while solving different problems.
The model must identify whether the same computational issue is being asked,
not just whether the same function appears.

### Representative Failure Modes

BM25 can fail when the positive uses different code tokens or when long
documents contain many incidental function names. It can also over-rank posts
with the same function but a different question. Dense retrieval can fail when
it captures general Mathematica topic similarity but misses the precise code
behavior or mathematical transformation being requested.

Hybrid failures often occur in code-near hard negatives. A candidate may share
`Plot`, `Show`, or a TeX conversion function with the query but address a
different workflow. Rerankers must compare the intended operation and the role
of the code token, not only its presence.

### Training Data That May Help

Useful training data includes non-overlapping CQADupStack Mathematica duplicate
question pairs, Wolfram Language forum QA with duplicate links, and code-
question paraphrase data with overlap removed. Training should exclude the
translated Mathematica test queries and duplicate positives used by this Nano
split.

Synthetic data can be generated from Mathematica support posts outside the
evaluation set, preserving original code tokens while writing Dutch
paraphrases. Good hard negatives should share functions or mathematical objects
but require a different operation, such as plotting versus post-processing a
plot, or interpolation versus solving an equation.

### Model Improvement Notes

Improving this task likely requires code-aware dense training and strong
reranking. The model should represent both the natural-language problem and the
specific function or expression involved. Contrastive training with same-
function non-duplicates would be more useful than random negatives.

For rerankers, the central behavior is to verify duplicate intent at the
operation level. A good reranker should ask whether the candidate question
would lead to the same answer or solution pattern, even when its code example
or translated wording differs from the query.

## Example Data

| Query | Positive document |
| --- | --- |
| DeleteDuplicatesBy werkt niet zoals ik had gehoopt. Mis ik iets? [64 chars] | Dubbele elementen uit een lijst verwijderen Als een lijst dubbele elementen bevat, bijvoorbeeld list = {a, 1, 5, 3, 5, x^2, x^2}, hoe kunnen de dubbele elementen worden verwijderd? Het resultaat zou zijn uniqueElements = {a, 1, 5, 3, x^2} [274 chars] |
| Is het mogelijk om de kleur van de plot in Show te veranderen? [62 chars] | Plot bewerken na aanmaak Ik probeer een manier te vinden om een plot te manipuleren die ik eerder heb gemaakt. (voor de volledige code, neem de functie x[t_]:=Sin[2t] ) Stel dat ik een plot heb: plot1 = Plot[x[t], {t, 0, 10}, PlotStyle -> Purple, ImagePadding -> 55, Frame -> {True, True, True, False}, FrameStyle -> {Automatic, Purple, Automatic, Automatic}, FrameLabel -> {None, "Signaal", None, None}, LabelStyle -> {16}, ImageSize -> 600]; En later wil ik dezelfde plot gebruiken met een punt op de lijn. De complete code zou zijn: plot1 = Plot[x[t], {t, 0, 10}, PlotStyle -> Purple, ImagePadding -> 55, Frame -> {True, True, True, False}, FrameStyle -> {Automatic, Purple, Automatic, Automatic}, FrameLabel -> {None, "Signaal", None, None}, LabelStyle -> {16}, ImageSize -> 600, Epilog -> {Directive[{Purple}], PointSize -> Large, Point[{2, x[2]}]}]; Maar is er een andere manier? Zoiets als SetOptions[plot1,Epilog -> {Directive[{Purple}], PointSize -> Large, Point[{2, x[2]}]}] En wat als ik d... [1,000 / 1,150 chars] |
| Krijg polynomiale interpolatieformule [37 chars] | Functies Bepalen Gegeven Datapunten Kan Mathematica f(x,y) = 0 oplossen zodanig dat {x,y} bevat `{{0,0.5}, {1,0.5}, {0.6,0.8}, {0.4,0.2}}`? Moeten we f(x,y) eerst specificeren? Dank u. [186 chars] |

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
| DeleteDuplicatesBy werkt niet zoals ik had gehoopt. Mis ik iets? | A translated duplicate asks how to remove duplicate elements from a Mathematica list and keep only unique elements. |
| Is het mogelijk om de kleur van de plot in Show te veranderen? | A translated Mathematica question asks how to edit or manipulate a plot after it has already been created. |
| Krijg polynomiale interpolatieformule | A translated question asks whether Mathematica can determine a function from a set of data points. |
| Functie of formule als functieparameter doorgeven | A translated duplicate asks how to pass a function as an argument to another Mathematica function. |
| Hoe typ ik een hoofdletter E in Mathematica 9 met behulp van ToExpression en TeXForm? | A translated post reports that TeX input conversion with `ToExpression` and `TeXForm` fails. |
