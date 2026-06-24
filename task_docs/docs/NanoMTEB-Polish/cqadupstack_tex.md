# NanoMTEB-Polish / cqadupstack_tex

## Overview

`cqadupstack_tex` is the Polish NanoMTEB version of the TeX subset from CQADupStack. The task evaluates duplicate-question retrieval for LaTeX and TeX troubleshooting posts. A short Polish query must retrieve longer candidate documents that ask the same formatting, compilation, macro, package, layout, bibliography, table, figure, or PDF-link question. The task is technical and code-adjacent: natural-language descriptions are mixed with commands, package names, document classes, and rendered-output symptoms.

The Nano split contains 200 queries, 10,000 documents, and 843 positive relevance judgments. Queries average about 50 characters, while documents average about 1,106 characters. Duplicate clusters are common: 94 queries have more than one positive, the average positives per query is 4.215, and one cluster has 100 positives. This makes the split a strong test of whether retrieval models can recover many formulations of common LaTeX problems.

## Details

### What the Original Data Measures

CQADupStack uses community QA duplicate links as relevance judgments. In the TeX subset, two posts are relevant when they ask the same LaTeX or TeX problem, not merely when they mention the same command or package. A query about `biblatex` bibliography separation should retrieve posts about the same bibliography structure, while a query about blank lines in an aligned environment should retrieve posts about that specific alignment error.

This task is useful for studying retrieval where relevance depends on both literal command names and visual or compilation behavior. Two posts may use different packages to describe the same rendered effect, or the same command may appear in unrelated formatting questions. Models must connect the requested output or error symptom to the right duplicate thread.

### Observed Data Profile

The documents are long because TeX questions often include minimal examples, preambles, package lists, error messages, and desired-output descriptions. The Polish translation covers the prose, while LaTeX commands such as `\includegraphics`, `biblatex`, and alignment environments remain as exact technical tokens. This mixed representation makes both lexical and semantic retrieval important.

The task has many recurring problems, which explains the high duplicate clustering. Common issues include separate bibliographies, image compilation speed, blank lines in equation environments, slashbox-style table headers, page-corner images, table of contents behavior, clickable PDF links, and package interactions.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2555, hit@10 of 0.4300, and recall@100 of 0.3405. Exact matching is useful when package names, commands, or environment names are central. Queries containing `biblatex`, `\includegraphics`, table environments, or alignment terms can benefit from lexical overlap.

However, BM25 is limited because duplicate TeX problems can be described by output symptoms rather than identical commands. A user may ask for "a diagonal table header" without naming `slashbox`, or describe "separate bibliographies" through different package options. Long candidate posts also contain many incidental commands, which can create false lexical matches.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run improves to nDCG@10 of 0.2805, hit@10 of 0.4800, and recall@100 of 0.4033. Dense retrieval helps connect visual or functional intent across different wording. It can relate a query about speeding compilation with many images to documents about skipping image processing, even when the exact command usage differs.

The dense gain shows that semantic similarity matters, but the task is still difficult. TeX relevance often depends on exact package behavior, command scope, or document-structure details. Dense retrieval can find more conceptually related posts, but it may also retrieve visually similar formatting issues that are not true duplicates.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest, with nDCG@10 of 0.3147, hit@10 of 0.5450, and recall@100 of 0.4282. Candidate lists contain 100 to 101 items, and 50 rows use the positive safeguard. The hybrid result indicates that BM25 and dense retrieval are complementary: commands and package names must be preserved, but semantic descriptions of desired rendering also matter.

This is the expected profile for TeX troubleshooting. Exact tokens such as package names are highly informative, but many duplicates are phrased around output symptoms or document goals. Hybrid candidate construction gives a downstream reranker a better pool than either lexical or dense retrieval alone.

### Metric Interpretation for Model Researchers

This split is clearly hybrid-favorable. BM25 supplies technical anchors, dense retrieval expands toward semantic descriptions of the same output or error, and `reranking_hybrid` improves both top-10 quality and recall@100. A model that performs well here likely handles code-like tokens, natural-language symptoms, and long technical documents together.

The high number of duplicate clusters makes recall@100 important. A direct search system needs good nDCG@10, but a reranking pipeline needs to preserve enough candidate duplicates from large common-problem clusters. Hybrid retrieval is the strongest baseline for that use case in this split.

### Query and Relevance Type Tendencies

Representative queries ask about main and secondary bibliographies in `biblatex`, speeding compilation of documents with many images, blank lines in aligned environments, alternatives to `slashbox`, and placing different images in each page corner. These are practical TeX troubleshooting questions centered on either a desired visual effect or a compilation/document-structure problem.

Relevant documents may use a different package, a different document class, or a longer minimal example. The retrieval model must identify the same rendered outcome or error condition, not only the same command string. It must also preserve exact package constraints when they define the solution space.

### Representative Failure Modes

BM25 may retrieve documents that share a command or package but solve a different issue. Many TeX posts mention `\includegraphics`, `biblatex`, or table environments for unrelated reasons. Dense retrieval may retrieve documents with similar visual goals, such as several table-formatting questions, even when the actual package behavior differs.

Another failure mode is ignoring the minimal example structure. In TeX questions, the duplicate relation can depend on where a command appears, which package is loaded, or which environment is nested. A general-purpose text model may miss these details unless it represents code-like context.

### Training Data That May Help

Useful training data includes TeX Stack Exchange duplicate pairs, Polish LaTeX help questions, documentation-style retrieval pairs, and hard negatives that share a package or command but differ in rendered effect. Examples with minimal working examples and output descriptions are particularly valuable.

Hard negatives should include near misses such as multiple `biblatex` questions about different bibliography structures, multiple table-header questions using different packages, or multiple image-layout questions with different placement constraints.

### Model Improvement Notes

Dense models can improve by representing commands, package names, and visual-output intent together. Sparse systems can improve by careful tokenization of backslash commands and braces, but exact matching alone will miss symptom-based duplicates. Hybrid systems are best suited to this split because they combine command-level precision with semantic matching of desired formatting behavior.

For reranker development, this task rewards models that compare a short problem statement with a long minimal example and decide whether the same TeX behavior is being asked about. Improvements should be measured through both nDCG@10 and recall@100.

## Example Data

| Query | Positive document |
| --- | --- |
| BibLaTeX: bibliografia główna i drugorzędna [43 chars] | biblatex: drukowanie oddzielnych bibliografii Używam `biblatex` i mam to ustawione tak: W moim pliku bib mam 3 rodzaje wpisów, online, broszura i książka. A w mojej pracy dyplomowej chcę je wydrukować osobno w następujący sposób: \printbibliography[heading=subbibliography,title={Książki},type=book, nottype=url, nottype=booklet, nottype=online] \printbibliography[heading=subbibliography,title= {Strony internetowe},type=online, nottype=book, nottype=booklet, nottype=url] \printbibliography[heading=subbibliography,title={Różne},type=booklet] Z jakiegoś powodu to nie zadziała, nadal umieszcza strony internetowe, na których powinny być książki. I wzajemnie. Broszura jednak działa, pokazuje tam tylko moje wpisy do broszury. Niedawno zacząłem używać `biblatex`, więc to może być głupie pytanie. [797 chars] |
| Jak mogę przyspieszyć kompilację dokumentu z wieloma obrazami? [62 chars] | Pomiń przetwarzanie wszystkich obrazów Próbuję zrobić szkic, zmuszając LaTeX do ignorowania wszystkich obrazów. Jak mam powiedzieć LaTeX, aby pominął wszystkie nazwy plików obrazów (w poleceniu `\includegraphics`) i po prostu wstawił puste pole? Problem z opcjami `[draft]` polega na tym, że nadal wymaga to, abym wszystkie obrazy znajdowały się w folderze, w którym znajdują się moje pliki `.tex`. [398 chars] |
| Puste linie w wyrównanym środowisku [35 chars] | Błąd w wyrównaniu środowiska - niekontrolowany argument? > **Possible Duplicate:** > Puste linie w środowisku wyrównania \documentclass[12pt,a4paper]{article} \usepackage[wersja=3]{mhchem} \usepackage{siunitx} \begin{document} \begin{align*} \ce{K_a} & = \frac{\ce{[H3O+][A^-]}}{\ce{[HA]}} \\ \end{align*} \end{document} podaje argument Runaway? \ce {K_a} & = \frac {\ce {[H3O+][A^-]}}{\ce {[HA]}} \\ ! Akapit zakończył się przed ukończeniem \align*. <do przeczytania ponownie> \par l.8 ? [488 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original duplicate-question retrieval construction. |
| MTEB paper | Benchmark context for retrieval tasks. |
| CLARIN-KNEXT dataset card | Polish translated TeX subset. |
| MTEB task card | Task packaging and retrieval interface. |

### Representative Snippets

- A query asks about a main and secondary bibliography in `biblatex`; relevant documents describe printing separate bibliographies.
- A query asks how to speed compilation with many images; relevant posts discuss skipping image processing in draft workflows.
- A query asks about blank lines in an aligned environment; relevant documents describe alignment-environment errors caused by blank lines.
- A query asks for an alternative to `slashbox`; relevant posts discuss creating diagonal table headers.
- A query asks about placing different images in page corners; relevant documents describe page-corner or flipbook-style layout effects.
