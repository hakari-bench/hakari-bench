# NanoMTEB-Dutch / cqadupstack_tex

## Overview

`cqadupstack_tex` is the Dutch-translated TeX and LaTeX subforum split of
CQADupStack. Queries are typesetting and LaTeX workflow questions, and
relevant documents are older questions marked as duplicates. The Nano split
contains 200 queries, 10,000 documents, and 200 positive qrel rows, with one
positive duplicate per query. It evaluates retrieval over BibLaTeX, graphics,
alignment environments, tables, Beamer, TeXstudio, TikZ, fonts, packages, and
compilation behavior.

This split has the longest average document length among the inspected Dutch
CQADupStack tasks, at 1,211.75 characters. Many documents include code,
commands, package names, minimal examples, error descriptions, and translated
prose. BM25 is weak as a final ranker, dense retrieval improves top-10 quality,
and `reranking_hybrid` is strongest across the reported metrics. The task is a
good diagnostic for code-aware hybrid retrieval over long translated support
posts.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) defines duplicate-
question retrieval from Stack Exchange duplicate links. The TeX subforum
contains practical questions about producing a desired document layout,
compiling source, configuring packages, and resolving LaTeX errors. The
retrieval task is to find the earlier question that addresses the same
typesetting or compilation problem.

BEIR standardizes CQADupStack for zero-shot retrieval, and BEIR-NL translates
the public BEIR datasets into Dutch. In this split, explanatory text is
translated, while LaTeX commands, package names, code fragments, and many error
strings remain close to the original. Retrieval therefore needs both natural-
language semantic matching and exact technical token awareness.

### Observed Data Profile

The split has 200 queries over 10,000 documents. Queries average 53.53
characters, while documents average 1,211.75 characters. The document side is
long because TeX questions often include minimal working examples, package
lists, error messages, screenshots, and explanations of desired output.

Representative questions ask about primary and secondary BibLaTeX
bibliographies, speeding compilation of documents with many images, blank lines
inside an `align` environment, alternatives to `slashbox`, and placing
different images in page corners. These examples show that the positive
duplicate is often tied to a specific rendering or compilation behavior rather
than a broad package topic.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2106, hit@10 = 0.2850, and recall@100 = 0.5650 over
top-500 candidate lists. Sparse retrieval has access to valuable exact tokens:
package names, LaTeX commands, environment names, and error strings. When a
query and positive document share `align`, `BibLaTeX`, `includegraphics`,
`TikZ`, or a specific package, BM25 can recover the relevant area.

The top-10 score is low because exact package overlap is not the same as
duplicate intent. Long documents contain many incidental commands, and many TeX
questions use the same packages for different output goals. A candidate can
share `beamer` or `tikz` while solving a different layout problem. BM25 is
therefore a useful recall source, but not a reliable final ranker.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.2611, hit@10 =
0.3800, and recall@100 = 0.6400. Dense retrieval improves over BM25 by
capturing paraphrased descriptions of the same desired rendering or workflow.
It can connect questions about suppressing image processing, bibliography
separation, table layout, or document preview even when exact command overlap
is incomplete.

Dense retrieval is still challenged by the code-like nature of the task. Many
TeX posts are semantically similar because they involve formatting, packages,
or compilation, but the duplicate relation depends on a precise command,
environment, or output behavior. General embedding similarity can retrieve
nearby LaTeX problems that are not true duplicates.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.2926, hit@10 =
0.4100, and recall@100 = 0.6750, with 100 to 101 candidates per query and 65
rank-101 safeguard rows. It is the strongest candidate profile for this split.
The hybrid result indicates that sparse command/package evidence and dense
semantic evidence are complementary in TeX duplicate retrieval.

The high number of safeguard rows also shows that many positives sit near the
edge of the candidate pool. A reranker using this pool must distinguish true
duplicate rendering or compilation issues from package-near hard negatives.
Hybrid search gives the reranker a better chance than BM25 or dense alone, but
the top order still leaves significant room for improvement.

### Metric Interpretation for Model Researchers

Because each query has one positive duplicate, nDCG@10 is a direct measure of
where that duplicate is ranked. Hit@10 estimates whether a user sees it quickly,
and recall@100 measures candidate coverage for reranking. The metric pattern
shows a clear hybrid advantage: exact commands matter, but semantic duplicate
intent matters too.

This split is useful for testing code-aware and markup-aware retrieval. A model
that treats LaTeX commands as ordinary rare words will miss their importance,
while a model that treats every shared command as relevance will over-rank
package-near distractors.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated TeX support questions. They often include a
package, command, environment, or desired output behavior. Relevant documents
are longer prior questions with the same rendering or compilation problem,
often including source snippets and explanatory body text.

Relevance is based on duplicate user need. Two posts about bibliographies,
images, or tables may not be duplicates unless they seek the same behavior.
Conversely, two duplicates may use different packages if they express the same
typesetting goal.

### Representative Failure Modes

BM25 can fail by over-ranking documents that share a package or command but
solve a different problem. It can also miss duplicates when the query uses a
short natural-language description and the positive uses code. Dense retrieval
can fail by grouping related formatting problems together without identifying
the exact desired output.

Hybrid failures usually involve package-near hard negatives. The positive may
be available by top 100, but candidates with stronger command overlap can rank
above it. Rerankers should compare the requested rendering behavior, source
context, and compilation issue.

### Training Data That May Help

Useful training data includes non-overlapping TeX Stack Exchange duplicate
question pairs, LaTeX support QA pairs, code-aware technical duplicate
retrieval data, and Dutch-translated technical forum pairs. Training should
exclude the translated TeX test queries and duplicate positives used by this
Nano split.

Synthetic data can be generated from LaTeX support posts outside the evaluation
set. Preserve commands, package names, and minimal examples, then create Dutch
paraphrases that ask for the same output or compilation behavior. Hard
negatives should share packages or commands but require a different fix.

### Model Improvement Notes

Improving this task requires markup-aware retrieval. Dense models should learn
that commands and package names are not just tokens but constraints on the
problem. Rerankers should compare code context and desired output, especially
when long documents contain many incidental LaTeX commands.

Hybrid retrieval is the most promising first stage for this split. BM25 keeps
rare TeX tokens in the pool, dense retrieval captures paraphrased user needs,
and reranking can make the final duplicate-intent decision.

## Example Data

| Query | Positive document |
| --- | --- |
| BibLaTeX: primaire en secundaire bibliografieën [47 chars] | Bibliografie met verschillende namen en gesorteerd op naam Ik wil graag twee bibliografieën maken met twee verschillende namen. Mijn twee bibliografieën zijn books.bib en articles.bib. Door \renewcommand{\refname}{Referenties uit Boeken} na `\begin{document}` te plaatsen en vervolgens de bibliografie in te voeren met: \nocite* \bibliographystyle{plain} \bibliography{books} % werkt dit voor books.bib. Ik wil hetzelfde doen met articles.bib en de titel "Referenties uit artikelen". Bovendien moeten de items in beide gevallen alfabetisch geordend worden. [559 chars] |
| Hoe kan ik het compileren van een document met meerdere afbeeldingen versnellen? [80 chars] | Het verwerken van alle afbeeldingen onderdrukken Ik probeer een concept te maken door LaTeX te dwingen alle afbeeldingen te negeren. Hoe kan ik LaTeX vertellen alle afbeeldingsbestandsnamen (in de `\includegraphics`-opdracht) te onderdrukken en gewoon een leeg vakje in te voegen? Het probleem met de `[draft]`-optie is dat het nog steeds vereist dat ik alle afbeeldingen in de map heb waar mijn `.tex`-bestanden staan. [420 chars] |
| Lege regels in align-omgeving [29 chars] | Waarom geeft een extra regel witruimte voor \end{align} een foutmelding? Ik voeg vaak extra witruimte toe aan mijn TeX-bestand voor betere leesbaarheid, en ik krijg deze foutmelding steeds wanneer er een lege regel voor `\end{align}` staat. Wat is de oorzaak van de fout en is er een manier om dit te verhelpen? [312 chars] |

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
| BibLaTeX: primaire en secundaire bibliografieen | A translated question asks how to create two bibliographies with different names and sorting behavior. |
| Hoe kan ik het compileren van een document met meerdere afbeeldingen versnellen? | A translated duplicate asks how to force LaTeX to ignore image files while compiling a draft. |
| Lege regels in align-omgeving | A translated post asks why an extra blank line before `\end{align}` causes an error. |
| alternatief voor slashbox | A translated question asks how to create advanced table layouts like a diagonal header cell. |
| Een ander plaatje plaatsen in elke paginahoek | A translated document-layout question asks how to place changing images in page corners for a flipbook-like effect. |
