# NanoMTEB-French

## Overview

NanoMTEB-French is a compact French retrieval group drawn from MTEB-French and
related MTEB tasks. It combines educational resource retrieval, Belgian
statutory article retrieval, French Wikipedia QA passage retrieval, French
Mintaka answer retrieval, Syntec collective-agreement retrieval, and
French-English product question answering. The group tests monolingual French
retrieval and cross-lingual product QA in one small suite.

The source tasks differ more than their French surface suggests. Alloprof and
BSARD map user-facing questions to long educational or legal documents. FQuAD
retrieves answer-bearing passages. Mintaka retrieves short entity-like answers.
Syntec retrieves labor-agreement clauses. xPQA tests product answerability
across French and English directions. BM25 exposes exact wording and named
entities; dense retrieval tests French paraphrase and cross-lingual matching;
`reranking_hybrid` shows where both signals are useful.

## What This Group Measures

NanoMTEB-French follows MTEB-French retrieval coverage and includes xPQA
directions that involve French. The group measures whether a model can retrieve
the correct French or French-English answer source across education, law,
Wikipedia QA, entity answers, labor agreements, and product QA.

The shared challenge is not only French language handling. Each task has its
own relevance definition: an educational lesson should answer a student
question, a statute should satisfy a legal need, a product snippet should
answer compatibility or specification questions, and a Mintaka answer may be a
very short label.

## Task Families

- **Educational retrieval:** `alloprof` retrieves French educational resources
  for student questions.
- **Legal and workplace retrieval:** `bsard` and `syntec` retrieve Belgian
  statutes or collective-agreement clauses.
- **French QA retrieval:** `fquad` retrieves French Wikipedia evidence passages.
- **Answer-label retrieval:** `mintaka_fr` retrieves short canonical answer
  strings.
- **Product QA retrieval:** `xpqa_eng_fra`, `xpqa_fra_eng`, and `xpqa_fra_fra`
  retrieve product answer snippets across French-English directions.

## Dataset Shape

NanoMTEB-French contains 8 task pages, 1,500 queries, 19,397 split-local
documents, and 2,212 positive qrel rows. Most tasks are single-positive. The
three xPQA tasks are multi-positive, with roughly two positive snippets per
query on average.

Document formats vary widely. Alloprof lessons are long educational documents,
BSARD statutes are formal legal articles, FQuAD passages are compact evidence
paragraphs, Mintaka targets are short answer strings, and xPQA documents are
short product answer snippets. The group should therefore be read by target
type rather than as one generic French retrieval benchmark.

## Retrieval Behavior

### BM25 Profile

BM25 is strongest on `fquad`, `syntec`, and monolingual `xpqa_fra_fra`. These
tasks often preserve names, article terms, product specifications, or agreement
language. FQuAD in particular has strong lexical overlap between question and
Wikipedia evidence.

BM25 is weakest on cross-lingual xPQA and BSARD. French-to-English or
English-to-French product QA has limited lexical bridge beyond product names,
numbers, and units. BSARD is difficult because lay legal questions often use
different wording from statutory articles.

### Dense Profile

Dense retrieval is the best profile for most NanoMTEB-French tasks. It improves
Alloprof, BSARD, Mintaka, Syntec, and all xPQA directions by matching semantic
answerability and cross-lingual product information beyond exact terms.

Dense retrieval is not universally best: FQuAD remains BM25-led because
answer-bearing passages share strong lexical cues with questions. This contrast
makes the group useful for separating French semantic matching from exact
evidence-word matching.

### Reranking Hybrid Profile

`reranking_hybrid` is best on Alloprof and BSARD in the current metadata, and
competitive on FQuAD, Syntec, and monolingual xPQA. These tasks benefit from
both exact French terms and semantic matching. In cross-lingual xPQA, dense is
much stronger than hybrid, suggesting that sparse retrieval contributes less
when the language bridge is weak.

For reranker experiments, xPQA should be read as a multi-positive answer
ranking task. Several snippets can answer the same product question, so
candidate coverage matters.

## Task Summary

| Task | Retrieval focus | Lang | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [alloprof](alloprof.md) | student question to lesson resource | `fr` | 200 | 2,556 | 200 | 0.3447 | 0.5139 | 0.5214 | Reranking hybrid |
| [bsard](bsard.md) | lay legal question to statute | `fr` | 200 | 10,000 | 200 | 0.1943 | 0.3023 | 0.3048 | Reranking hybrid |
| [fquad](fquad.md) | French QA question to evidence passage | `fr` | 200 | 269 | 200 | 0.8899 | 0.8102 | 0.8666 | BM25 |
| [mintaka_fr](mintaka_fr.md) | complex question to answer label | `multilingual` | 200 | 1,714 | 200 | 0.2995 | 0.3676 | 0.3400 | Dense |
| [syntec](syntec.md) | labor question to agreement clause | `fr` | 100 | 90 | 100 | 0.7180 | 0.8660 | 0.8463 | Dense |
| [xpqa_eng_fra](xpqa_eng_fra.md) | English product question to French answer | `multilingual` | 200 | 1,674 | 451 | 0.1061 | 0.3639 | 0.1775 | Dense |
| [xpqa_fra_eng](xpqa_fra_eng.md) | French product question to English answer | `multilingual` | 200 | 1,547 | 437 | 0.2918 | 0.6479 | 0.3724 | Dense |
| [xpqa_fra_fra](xpqa_fra_fra.md) | French product question to French answer | `fr` | 200 | 1,547 | 424 | 0.5644 | 0.6400 | 0.6208 | Dense |

## Interpretation Notes for Model Researchers

NanoMTEB-French should be read by retrieval relation. FQuAD and Syntec have
strong exact-language cues. BSARD and Alloprof require mapping user questions
to formal or explanatory documents. xPQA tests product answerability and
cross-lingual matching. Mintaka tests short answer labels, where document text
may be too short for ordinary passage retrieval assumptions.

Dense-led cross-lingual xPQA rows are especially informative for multilingual
embedding models. BM25-led FQuAD is a reminder that exact French entity and
answer wording remains valuable.

## Training and Leakage Notes

Useful training data includes French educational QA, statute retrieval, labor
agreement QA, French Wikipedia QA, Mintaka-style entity QA, and product QA
ranking in French and English. For xPQA, preserve multiple valid answer snippets
per question.

Exclude NanoMTEB-French evaluation queries, positives, qrels, answer strings,
statutes, lesson resources, agreement clauses, and product snippets. Cross-
lingual examples should avoid direct translations of evaluation queries as
synthetic seeds.

## Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2022.
- [FQuAD: French Question Answering Dataset](https://aclanthology.org/2020.findings-emnlp.107/), 2020.
- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://aclanthology.org/2022.coling-1.138/), 2022.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2022 | paper | [https://arxiv.org/abs/2210.07316](https://arxiv.org/abs/2210.07316) |
| FQuAD: French Question Answering Dataset | 2020 | paper | [https://aclanthology.org/2020.findings-emnlp.107/](https://aclanthology.org/2020.findings-emnlp.107/) |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | paper | [https://aclanthology.org/2022.coling-1.138/](https://aclanthology.org/2022.coling-1.138/) |
