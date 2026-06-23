# NanoMTEB-Polish / cqadupstack_mathematica

## Overview

`cqadupstack_mathematica` is the Polish NanoMTEB version of the Mathematica subset from CQADupStack. The task evaluates duplicate-question retrieval for Wolfram Language and Mathematica community posts. A short Polish query must retrieve longer candidate documents that ask the same computational, symbolic, notebook, plotting, or code-behavior question. This is a technical retrieval task with a mixture of natural language, translated Polish prose, function names, code snippets, and mathematical notation.

The Nano split contains 200 queries, 10,000 documents, and 506 positive relevance judgments. Queries average about 50 characters, while documents average about 1,089 characters, making the candidate posts among the longer Polish CQADupStack documents. The average number of positives per query is 2.53, 80 queries have multiple positives, and the largest duplicate cluster has 56 positives. The task therefore combines narrow code-specific duplicates with broader recurring Mathematica usage questions.

## Details

### What the Original Data Measures

CQADupStack measures whether retrieval systems can find duplicate community QA posts. In the Mathematica subset, relevance means that two questions ask the same Wolfram Language problem, not merely that they mention the same function name. A post about `DeleteDuplicatesBy`, `Plot`, `Dynamic`, `TeXForm`, interpolation, or function arguments is relevant only when the underlying computational issue is equivalent.

This makes the benchmark useful for testing code-adjacent retrieval. The text is not pure source code, but code identifiers and examples are central to relevance. A model must read the surrounding explanation, understand the intended operation, and avoid treating shared identifiers as sufficient evidence.

### Observed Data Profile

The documents are long because Mathematica questions often include code blocks, attempted expressions, graphical output descriptions, errors, or notebook behavior. The Polish translation covers the explanatory text, while many Wolfram Language identifiers remain unchanged. This creates mixed text where exact symbols, function names, and Polish descriptions all matter.

Examples include questions about `DeleteDuplicatesBy`, editing plot colors after drawing, interpolation formulas, passing a function as an argument, and converting TeX input with `ToExpression` and `TeXForm`. These cases require models to preserve small technical distinctions. Two posts may both mention `Plot`, but one may concern styling, another evaluation order, and another export behavior.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2129, hit@10 of 0.3550, and recall@100 of 0.3024. This relatively low lexical profile shows that exact function-name overlap alone is not enough. Mathematica identifiers provide strong anchors, but they also appear in many non-duplicate posts. Long candidate documents can contain several shared tokens without asking the same question.

BM25 is most useful when the query contains a rare function, option, or notation that is central to the duplicate relation. It struggles when the same computational intent is expressed with different code structure, different examples, or different explanatory language. Polish morphology affects the surrounding prose, but the larger limitation is that code-like terms are ambiguous across tasks.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run is slightly stronger, with nDCG@10 of 0.2171, hit@10 of 0.3750, and recall@100 of 0.3498. Dense retrieval improves recall more than top-rank quality. This suggests that embeddings can find more semantically related Mathematica posts, but the final ranking still has difficulty separating true duplicates from nearby programming topics.

The modest dense gain is itself informative. In code-adjacent mathematical software tasks, embedding similarity can capture broad intent such as "pass a function as an argument" or "change plot styling after construction." However, precise relevance often depends on exact syntax, evaluation semantics, or a specific function behavior. Dense retrieval helps, but it does not fully solve the task.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest, with nDCG@10 of 0.2411, hit@10 of 0.3950, and recall@100 of 0.3874. Candidate lists contain 100 to 101 items, and 75 rows use the positive safeguard. The hybrid result shows that BM25 and dense retrieval contribute complementary evidence: BM25 preserves rare identifiers and expressions, while dense retrieval broadens the pool toward semantically similar computational goals.

This pattern is important for reranking. Mathematica duplicate detection often needs exact token evidence and semantic interpretation at the same time. A hybrid candidate pool is better positioned to include the correct posts, while a downstream reranker can decide whether the shared function name really corresponds to the same problem.

### Metric Interpretation for Model Researchers

This task is hybrid-favorable, but all scores are moderate. That indicates a difficult retrieval setting with long documents, code-like identifiers, and fine-grained duplicate definitions. BM25 alone is too literal; dense retrieval alone is not precise enough at the top; `reranking_hybrid` provides the best compromise.

Researchers should read recall@100 carefully. The dense and hybrid improvements over BM25 show that many positives can be recovered by adding semantic candidates, but nDCG@10 remains limited. A strong reranker or code-aware retriever should aim to improve the top-10 ordering by distinguishing syntactic similarity, semantic equivalence, and merely shared Mathematica vocabulary.

### Query and Relevance Type Tendencies

Representative queries ask why `DeleteDuplicatesBy` does not behave as expected, whether a plot color can be changed after using `Show`, how to obtain an interpolation formula, how to pass a function or formula as a function parameter, or how to enter a capital `E` through `ToExpression` and `TeXForm`. These questions mix code syntax, notebook interface expectations, symbolic math, and plotting behavior.

Relevant documents often include longer examples than the query. They may describe a failed expression, a performance concern, a graphics object, or a desired transformation. Matching requires identifying the computational goal rather than simply matching the surface code.

### Representative Failure Modes

Lexical systems may over-rank documents that share function names such as `Plot`, `Dynamic`, or `DeleteDuplicates` but solve a different problem. Dense systems may retrieve conceptually adjacent Mathematica questions, such as several plotting or list-processing posts, while missing the specific duplicate relation. Both errors are likely when documents contain long code snippets and many related identifiers.

Another failure mode is ignoring executable semantics. Two snippets can look similar but behave differently because of evaluation order, scoping, attributes, or expression structure. Conversely, two snippets can look different while asking the same underlying operation. General-purpose text embeddings may not capture these distinctions consistently.

### Training Data That May Help

Useful training data includes Mathematica Stack Exchange duplicate pairs, code-question paraphrases, symbolic-computation QA, Polish translated technical posts, and hard negatives that share function names but differ in computational goal. Examples should include both short titles and longer posts with code context.

Hard negatives are essential. Pairs that both mention `Plot` but ask about different graphics operations, or both mention list deduplication but differ in the criterion, help teach the model to avoid identifier-only matching. Code-aware reranking data may be especially useful.

### Model Improvement Notes

Dense models can improve by representing code identifiers together with surrounding natural-language intent. Sparse systems can improve through careful tokenization of symbols, camel-case identifiers, and code fragments, but lexical overlap alone is unlikely to dominate. Hybrid systems are the most promising first-stage approach for this split because they preserve exact code anchors while expanding to semantic neighbors.

For reranker development, this task rewards models that can compare short queries against long technical posts and decide whether the same Mathematica behavior is being asked about. Improvements should be evaluated through both nDCG@10 and recall@100 to separate better ranking from better candidate preservation.

## Example Data

| Query | Positive document |
| --- | --- |
| DeleteDuplicatesBy nie działa tak, jak się spodziewałem. Czy czegoś mi brakuje? [79 chars] | Szybsza alternatywa dla DeleteDuplicates do usuwania elementów z listy Mam listę w tym stylu data={{a1,b1,c1,d1,e1,f1}, {a2,b2,c2,d2,e2,f2}} Muszę usunąć wszystkie elementy, w których znajduje się `b1... [200 / 621 chars] |
| Czy można zmienić kolor fabuły w programie Show? [48 chars] | Edytuj wykres/grafikę po narysowaniu. Czasami wpadam w sytuację, gdy istnieją obiekty graficzne (głównie wykresy), których rysowanie zajmuje trochę czasu. Dobra praktyka sugerowałaby, że całą ocenę pr... [200 / 545 chars] |
| Uzyskaj wzór na interpolację wielomianową [41 chars] | Określ funkcje na podstawie punktów danych Czy Mathematica może rozwiązać dla f(x,y) = 0 takie, że {x,y} zawiera `{{0,0.5}, {1,0.5}, {0.6,0.8}, {0.4,0.2}} `? Czy musimy najpierw określić f(x,y) ? Dzię... [200 / 207 chars] |
| Przekaż funkcję lub formułę jako parametr funkcji [49 chars] | Przekazywanie funkcji jako argumentu innej funkcji > **Możliwe duplikowanie:** > Przekaż funkcję lub formułę jako parametr funkcji Próbuję zaimplementować prostą funkcję podobną do wykresu [], z tym s... [200 / 892 chars] |
| Jak wpisać duże „E” w Mathematica 9 za pomocą „ToExpression” i „TeXForm”? [73 chars] | Nie można przekonwertować danych wejściowych $\TeX$ na matematykę Wejście ToExpression["\\sqrt{x y}", TeXForm] daje mi wynik `$Failed`. Może mój bardzo stary komputer jest problemem, ale to jedyne pol... [200 / 278 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original duplicate-question retrieval benchmark design. |
| MTEB paper | Benchmark framing for retrieval tasks. |
| CLARIN-KNEXT dataset card | Polish translated Mathematica subset. |
| MTEB task card | Task packaging and retrieval interface. |

### Representative Snippets

- A query asks why `DeleteDuplicatesBy` does not work as expected; relevant documents discuss removing duplicate list elements by a selected criterion.
- A query asks whether plot color can be changed after `Show`; relevant posts discuss editing graphics objects after drawing.
- A query asks how to obtain an interpolation formula; relevant documents discuss deriving functions from points.
- A query asks how to pass a function or formula as a parameter; relevant posts describe function arguments and delayed evaluation patterns.
- A query asks how to enter a capital `E` using `ToExpression` and `TeXForm`; relevant documents discuss converting TeX-style input into Mathematica expressions.
