# NanoMTEB-Polish / cqadupstack_webmasters

## Overview

`cqadupstack_webmasters` is the Polish NanoMTEB version of the Webmasters subset from CQADupStack. The task evaluates duplicate-question retrieval for website operation and search-visibility questions. Queries ask about SEO, redirects, URL structure, favicons, robots behavior, indexing, rich snippets, DNS, canonical hostnames, and site-management policies. Relevant documents are community QA posts that ask the same website-management problem, not just posts that mention the same search engine or web term.

The Nano split contains 200 queries, 10,000 documents, and 882 positive relevance judgments. Queries average about 60 characters, while documents average about 739 characters. Duplicate clustering is important: 77 queries have multiple positives, the average number of positives per query is 4.41, and one cluster has 100 positives. The task therefore tests both precise matching for narrow webmaster problems and recovery of broad recurring SEO or indexing questions.

## Details

### What the Original Data Measures

CQADupStack defines duplicate-question retrieval through community QA duplicate links. In the Webmasters subset, relevance means operational equivalence. A post about `www` versus non-`www` hostnames is relevant to another post asking the same canonical-hostname SEO question, but not to every document mentioning redirects or SEO. A query about blocking indexing of part of a page is relevant to posts about the same indexing-control problem, not every robots-related question.

This task is useful because website-management questions combine exact terminology with practical outcomes. A model must understand whether the user is asking about search ranking, crawl policy, URL syntax, DNS behavior, or metadata interpretation. The same words can appear in many different operational contexts.

### Observed Data Profile

The documents are shorter than some code-heavy CQADupStack splits, but they often include URLs, configuration examples, platform names, and search-engine terminology. The Polish translation preserves many English web terms and URL fragments. Queries may contain mixed strings such as `find-new/posts&recent=1`, `HTTP://`, `www`, or rich-snippet terminology.

Because the task has large duplicate clusters, common webmaster concerns appear repeatedly. At the same time, many queries have only one positive. A strong model must handle both one-off operational questions and broad duplicate families around SEO, indexing, redirects, and URL design.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2440, hit@10 of 0.3900, and recall@100 of 0.3118. Exact web terms and URL fragments help BM25. Queries containing `www`, `HTTP`, robots, Google, favicon, noindex, or URL structure can retrieve topically related documents through lexical overlap.

The problem is that web-administration vocabulary is highly reused. Many posts mention Google, SEO, redirects, or URLs while asking different operational questions. BM25 therefore retrieves same-topic results but often fails to distinguish the actual duplicate intent, such as whether the issue is canonicalization, query-string SEO, crawler blocking, or rich-snippet display.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run improves to nDCG@10 of 0.3045, hit@10 of 0.4900, and recall@100 of 0.4796. Dense retrieval is much better at finding semantically equivalent webmaster problems. It can connect differently phrased questions about search visibility, indexing behavior, or redirect preference even when exact tokens differ.

The dense recall gain is large, which suggests that many positives are not easily found by lexical matching alone. Website-management questions often describe an observed state and desired outcome rather than a fixed technical term. Embedding similarity helps recover those equivalent operational descriptions.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` reports nDCG@10 of 0.3162, hit@10 of 0.5100, and recall@100 of 0.4683. Candidate lists contain 100 to 101 items, and 42 rows use the positive safeguard. Hybrid ranking is best at the top, while dense retrieval has slightly higher recall@100.

This split therefore shows a nuanced hybrid profile. The fusion of lexical and dense evidence improves top-10 ordering because exact URLs, search-engine terms, and policy words help disambiguate dense matches. But the dense candidate set preserves slightly more positives overall. For a reranking pipeline, both profiles are worth inspecting: hybrid gives better initial ordering, while dense may contribute additional candidates.

### Metric Interpretation for Model Researchers

This task is dense-and-hybrid favorable, with BM25 clearly behind. Dense retrieval supplies the largest recall gain, while `reranking_hybrid` gives the best nDCG@10 and hit@10. A strong model should combine semantic understanding of website operations with exact handling of URLs, directives, and search-engine terminology.

The metrics also show that candidate coverage and final order can diverge. Dense recall@100 is higher, but hybrid top-10 ranking is better. Researchers should decide whether the evaluation target is first-stage candidate generation or direct search results before drawing conclusions.

### Query and Relevance Type Tendencies

Representative queries ask whether a query-string URL used as a home page affects SEO, how to prevent robots from indexing part of a page, whether `www` or non-`www` hostnames are preferable, what a double slash means in a URL, and why Google rich snippets work for one site author but not another. These examples involve operational states and search-engine interpretation.

Relevant documents often describe the same issue with different domain names, platforms, or site configurations. A model should abstract away incidental domain details while preserving the actual action or policy being asked about.

### Representative Failure Modes

BM25 may retrieve any post containing SEO, Google, URL, or redirect terms even when the desired action differs. Dense retrieval may retrieve operationally similar but non-duplicate posts, such as several Google-indexing questions with different mechanisms. Hybrid retrieval can still fail when lexical anchors point to the wrong subproblem.

Another failure mode is mishandling URL syntax. Small differences between query strings, double slashes, protocols, hostnames, and paths can determine relevance. A model that treats URLs as ordinary text may miss these distinctions.

### Training Data That May Help

Useful training data includes webmaster QA duplicate pairs, Polish SEO and site-administration questions, DNS and redirect support pairs, and hard negatives sharing search-engine or URL terminology but asking different actions. Examples with actual URLs, directives, and platform-specific details would be useful.

Hard negatives should include multiple SEO questions that differ in cause, multiple redirect questions with different desired outcomes, and multiple indexing questions involving different crawler controls. These help the model distinguish broad topic overlap from duplicate relevance.

### Model Improvement Notes

Dense models can improve by representing website states, desired outcomes, and search-engine policy language. Sparse systems can improve through tokenization of URLs and directives, but exact matching alone is weak. Hybrid systems are promising for top-rank quality because they combine semantic interpretation with precise URL and web-policy terms.

For reranker research, this split rewards models that can read a short operational query and a longer post, identify the central website-management issue, and ignore incidental domain or platform details.

## Example Data

| Query | Positive document |
| --- | --- |
| find-new/posts&recent=1 jako strona główna: co z SEO? [53 chars] | Czy adres URL z ciągiem zapytania jest lepszy lub gorszy dla SEO niż adres bez niego? Chcę wiedzieć, czy istnieje ogromna różnica pod względem SEO między tymi adresami URL: > mysite.com/ontario/toronto/listings > > lub > > mysite.com/listings.php?p=ontario&c=toronto wyższy niż inny? Czy jest tu duża różnica? [309 chars] |
| Uniemożliwianie robotom indeksowania określonej części strony [61 chars] | Jak poprosić Google o nieindeksowanie niektórych części mojej strony? > **Możliwy duplikat:** > Uniemożliwianie robotom indeksowania określonej części strony Szukałem dzisiaj starej recenzji w mojej witrynie i zauważyłem, że Google indeksuje tekst nagłówka z mojej najnowszej listy artykułów na każdej stronie, która się pojawia , oczywiście tak sądzę. Problem polega na tym, że wyszukuję moją recenzję Dragon's Lair konkretnie w mojej witrynie, tak jak ta http://www.google.co.za/search?sugexp=chrome,mod=9&sourceid=chrome&ie=UTF-8&q=site%3Alazygamer.net +smoki+lair+recenzja Następnie zwraca mnóstwo stron, które są nieodpowiednie, ponieważ w ogóle nie są związane z recenzją. Powodem, dla którego mnie to obchodzi, jest to, że mam drugą recenzję Dragon's Lair, która została opublikowana lata temu, a teraz nie mogę jej znaleźć. Czy istnieje sposób, aby wskazać Google, że określony tekst nie ma związku z rzeczywistą zawartością strony? czy to okropny pomysł? [963 chars] |
| Preferencje SEO dla przekierowania protokołu WWW lub HTTP://? Czy strony www mają wyższą pozycję niż strony bez www? [116 chars] | Z www czy bez www? Którego lepiej użyć Właśnie kupiłem nową domenę `www.reversehacking.com` .... Co jest lepsze dla SEO: `http://reversehacking.com` lub `http://www.reversehacking.com` Myślę, że ludzie zrobią więcej linków zaczynających się na www i będzie miało więcej linków zwrotnych do www. Proszę o sugestie, a muszę jak najszybciej uruchomić stronę. [355 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original duplicate-question retrieval construction. |
| MTEB paper | Benchmark context for retrieval tasks. |
| CLARIN-KNEXT dataset card | Polish translated Webmasters subset. |
| MTEB task card | Task packaging and retrieval interface. |

### Representative Snippets

- A query asks whether using `find-new/posts&recent=1` as a home page affects SEO; relevant documents discuss SEO consequences of query-string URLs.
- A query asks how to stop robots from indexing part of a page; relevant posts discuss asking Google not to index selected page sections.
- A query asks whether `www` or non-`www` protocol redirects are better for SEO; relevant documents discuss canonical hostname choices.
- A query asks what a double slash in a URL means; relevant posts discuss problems caused by two slashes in the middle of a URL.
- A query asks why Google rich snippets work for one author but not another; relevant documents describe rich-snippet recognition problems.
