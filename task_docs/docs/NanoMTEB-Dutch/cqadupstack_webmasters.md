# NanoMTEB-Dutch / cqadupstack_webmasters

## Overview

`cqadupstack_webmasters` is the Dutch-translated Webmasters subforum split of
CQADupStack. Queries ask about SEO, indexing, URLs, malware, spam prevention,
rich snippets, cross-linking, and web publishing, and relevant documents are
older Stack Exchange questions marked as duplicates. The Nano split contains
200 queries, 10,000 documents, and 200 positive qrel rows, with one positive
duplicate per query.

This task evaluates duplicate retrieval in a broad site-administration domain.
BM25 can use terms such as SEO, WordPress, malware, robots, `rel`, URLs, and
Google, but those terms often identify only the webmaster topic, not the exact
duplicate. Dense retrieval with `harrier_oss_v1_270m` is much stronger at
top-10 hit rate, while `reranking_hybrid` gives the highest nDCG@10 and
recall@100 but a slightly lower hit@10 than dense. The result is a useful
example of hybrid search improving candidate coverage while still requiring a
reranker to sort same-topic web-management questions.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) defines duplicate-
question retrieval tasks from Stack Exchange duplicate links. A later question
is used as the query, and the system must retrieve the older question that was
marked as its duplicate. The Webmasters subforum covers operational and SEO
questions rather than a single programming API, so duplicate links often connect
posts that describe the same site-management concern in different language.

BEIR included CQADupStack in a common zero-shot retrieval benchmark, and
BEIR-NL translated public BEIR datasets into Dutch. This split therefore keeps
the original duplicate relation but presents translated Dutch webmaster
questions. Markup snippets, URLs, and search-engine terms often remain
recognizable, while explanatory text and user framing are translated.

### Observed Data Profile

The split has 200 queries over 10,000 documents. Queries average 58.83
characters, and documents average 761.20 characters. Documents often include
URLs, quoted markup, SEO terminology, webmaster configuration details, and
context about search-engine behavior or site security.

Representative questions ask about SEO effects of a paginated homepage URL,
preventing robots from crawling a page section, whether `www` and non-`www`
domains rank differently, what double slashes in URLs mean, and why Google Rich
Snippets work for one author but not another. These examples have useful
lexical anchors, but the duplicate relation depends on the same operational
question, not just a shared SEO or URL term.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2307, hit@10 = 0.2850, and recall@100 = 0.5550 over
top-500 candidate lists. Sparse retrieval benefits from exact strings such as
`rel="next"`, `rel="prev"`, `robots`, `www`, URL fragments, rich snippets,
malware, and WordPress. These tokens can recover a relevant topic area and
sometimes a true duplicate.

The weakness is that webmaster terminology is broad and repeated. Many
questions mention SEO or Google but ask different questions. Translation can
also vary the Dutch framing around otherwise similar site-administration
issues. BM25 therefore often finds same-topic neighbors without ranking the
true duplicate high enough.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.2947, hit@10 =
0.4450, and recall@100 = 0.6700. Dense retrieval improves strongly over BM25,
especially in hit@10. This indicates that semantic similarity helps connect
paraphrased webmaster questions, such as different ways of asking about
canonical domains, crawling exclusions, spam prevention, or rich-snippet
behavior.

Dense retrieval still faces many hard negatives. A site-administration post can
be semantically close because it discusses the same SEO mechanism or web
platform while not duplicating the exact user need. The model must identify the
same operational intent rather than broad webmaster topic similarity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.2968, hit@10 =
0.4200, and recall@100 = 0.7250, with 100 to 101 candidates per query and 55
rank-101 safeguard rows. Hybrid retrieval has the best top-100 coverage and a
slightly higher nDCG@10 than dense retrieval, although dense has the higher
hit@10. This means the hybrid pool recovers more positives but also changes the
top-10 ordering in a way that sometimes moves positives below rank 10.

For reranking, the hybrid pool is attractive. BM25 contributes exact URL,
markup, CMS, and SEO terms, while dense retrieval contributes paraphrased
intent. A reranker must then decide whether the shared term indicates the same
webmaster problem or merely a related site-management topic.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 reflects how high the duplicate is ranked,
hit@10 reflects user-visible retrieval, and recall@100 reflects whether a
downstream reranker can access the positive. The metric pattern shows that BM25
is not enough, dense retrieval is a better first-stage ranker, and hybrid
retrieval offers the broadest candidate pool.

This split is useful for evaluating search systems that must balance exact
technical strings with semantic duplicate intent. Strong systems should exploit
URLs and markup without over-trusting them.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated webmaster questions. They often mention SEO,
indexing, robots, URL structure, Google features, spam, malware, or CMS
configuration. Relevant documents are prior duplicate questions, sometimes with
longer background or examples.

The relevance type is operational duplicate identity. A shared term such as SEO
or Google is not enough; the candidate must address the same site-management
decision or troubleshooting problem.

### Representative Failure Modes

BM25 can fail by over-ranking same-keyword questions about a different SEO or
site-administration issue. Dense retrieval can fail by retrieving a semantically
near post about the same web concept but a different implementation detail.
Hybrid retrieval can include both kinds of distractors.

Common hard negatives are same-platform, same-search-engine, or same-URL
questions that do not duplicate the query. Rerankers should compare the exact
site behavior, desired policy, and webmaster decision involved.

### Training Data That May Help

Useful training data includes non-overlapping Webmasters Stack Exchange
duplicate-question pairs, Dutch web-administration support QA, and SEO or CMS
duplicate-question pairs with overlap removed. Training should exclude the
translated Webmasters test queries and duplicate positives used by this Nano
split.

Synthetic data can be generated from webmaster support posts outside the
evaluation set. Create Dutch paraphrases for duplicate SEO tags, indexing,
malware warnings, form spam, URL normalization, and CMS configuration issues.
Hard negatives should share the same broad site-management topic while asking a
different operational question.

### Model Improvement Notes

Improving this task requires intent-level webmaster retrieval. Dense models
should learn from duplicate pairs where the same site-administration problem is
described with different terminology. Hybrid rerankers should preserve exact
technical strings such as URLs and markup but verify whether they support the
same duplicate relation.

The strongest systems should treat SEO and web-platform terms as candidate
signals, then use reranking to decide whether the candidate would answer the
same user question.

## Example Data

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| vind-nieuwe/berichten&recent=1 als homepage: wat met SEO? | A translated duplicate asks about best-practice URL structures for pagination and SEO considerations. |
| Het voorkomen dat robots een specifiek gedeelte van een pagina crawlen | A translated post asks how to prevent search engines from indexing specific content on a site. |
| SEO-voorkeur voor WWW of HTTP protocolredirectie? | A translated duplicate asks about choosing a canonical domain between `www.example.com` and `example.com`. |
| Wat betekenen dubbele slashes in URL's? | A translated question asks whether using two slashes in the middle of a URL is a problem. |
| Waarom werken Google Rich Snippets voor de ene site-auteur wel en voor de andere niet? | A translated post discusses Google ignoring rich-snippet microdata for some authors. |
