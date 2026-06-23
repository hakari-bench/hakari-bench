# NanoMTEB-Dutch / web_faq_nld

## Overview

`web_faq_nld` is the Dutch subset of WebFAQRetrieval from MTEB-NL. Queries are
natural FAQ-style questions or short web search prompts, and documents are FAQ
answer snippets from web pages. The Nano split contains 200 queries, 10,000
documents, and 200 positive qrel rows, with exactly one positive answer per
query. It evaluates broad-coverage Dutch question-answer retrieval over
practical web language.

This task is a single-positive FAQ retrieval benchmark with moderately short
answers. BM25 is strong because FAQ questions and answers often share important
terms. Dense retrieval with `harrier_oss_v1_270m` is strongest in nDCG@10 and
hit@10, while `reranking_hybrid` has perfect recall@100 in this Nano split. The
task is useful for evaluating realistic web FAQ retrieval, including noisy
commercial phrasing, service information, consumer advice, and occasional
language-mixing artifacts.

## Details

### What the Original Data Measures

[WebFAQ: A Multilingual Collection of Natural Q&A Datasets for Dense Retrieval](https://arxiv.org/abs/2502.20936)
describes a large multilingual collection of natural question-answer pairs
derived from FAQ-style schema.org annotations in Common Crawl. The collection
is intended for dense retrieval and includes broad domain coverage across many
languages.

MTEB-NL uses the Dutch subset of WebFAQRetrieval. This means the task is not a
curated single-domain QA benchmark. It reflects the variety of web FAQ pages:
service instructions, product advice, travel policies, civic information,
technical help, and commercial support text.

### Observed Data Profile

The split has 200 queries over 10,000 documents. Queries average 50.45
characters, and documents average 322.18 characters. The positive answer is
usually short enough to directly resolve the question, but answers may contain
web-template language or commercial context.

Representative questions ask what is important when giving advice, the
difference between 2D and 3D kitchen-design drawings, how to program NFC tags,
whether a visa is needed for Japan, and what type of photos can be used for a
card-making service. The data is broad and practical rather than encyclopedic.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.7698, hit@10 = 0.8450, and recall@100 = 0.9050 over
top-500 candidate lists. This is a strong sparse baseline because many FAQ
answers repeat the product, service, or action named in the question. Exact
terms such as visa, NFC, design drawing, photos, and product names are useful.

BM25's errors are likely caused by short or underspecified questions,
paraphrased answers, same-site hard negatives, and noisy web phrasing. An answer
can resolve a question without repeating all its words, especially when the
answer is policy-like or instructional.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.8776, hit@10 =
0.9150, and recall@100 = 0.9550. It is the strongest top-ranked candidate
source. Dense retrieval improves over BM25 by matching question intent to
answer content, even when the answer uses a different wording or gives a direct
policy response.

The remaining dense errors likely involve same-domain FAQ answers that are
semantically close but answer a different question. For example, several
answers from one website may discuss the same product or service but only one
answers the query.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.8442, hit@10 =
0.9100, and recall@100 = 1.0000, with exactly 100 candidates per query and no
safeguard rows. It recovers every positive answer in the top-100 pool, while
dense retrieval has the best top-10 ordering.

This makes hybrid search a strong reranking input. BM25 contributes exact
product or service terms, and dense retrieval contributes semantic answer
matching. A reranker can then separate the exact answer from same-site or
same-domain FAQ negatives.

### Metric Interpretation for Model Researchers

This is a single-positive task, so nDCG@10 measures the rank of the one answer
snippet. Hit@10 measures whether a user would see the correct answer quickly,
and recall@100 measures whether a reranker has access to it. Dense retrieval
is the best first-stage ranker; hybrid retrieval is the safest candidate pool.

Because recall@100 is perfect for hybrid search, reranking experiments can
focus on ordering quality rather than missing positives.

### Query and Relevance Type Tendencies

Queries are Dutch FAQ questions from many domains. They are often direct,
practical, and user-oriented. Documents are answer snippets that may include
instructions, policy details, requirements, or short explanations.

Relevance is answerability. A same-domain answer is not sufficient unless it
answers the question explicitly.

### Representative Failure Modes

BM25 can fail when answer wording does not repeat the query or when a web page
contains several similar FAQ answers. Dense retrieval can fail when a nearby
answer from the same product or service appears semantically close. Hybrid
retrieval can include many same-site candidates that require reranking.

Hard negatives should come from the same website, product, or FAQ category.

### Training Data That May Help

Useful training data includes non-overlapping Dutch FAQ question-answer pairs,
multilingual FAQ retrieval pairs with Dutch coverage, customer-support and
website FAQ retrieval data, and same-site or same-product hard negatives.
Training should exclude Dutch WebFAQ test questions, answers, and qrels used by
this Nano split.

Synthetic data can be generated from non-evaluation Dutch FAQ answers. Create
natural FAQ-style questions answerable from the selected answer, with hard
negatives from the same service or product domain.

### Model Improvement Notes

Improving this task requires robust question-answer matching over noisy web
language. Dense models should learn practical answerability, not just topic
similarity. Rerankers should compare the query with answer snippets directly
and handle short, policy-like, or commercial text.

Hybrid retrieval is especially useful for complete candidate coverage, while
dense retrieval gives the strongest initial ranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Wat is belangrijk bij adviseren? [32 chars] | Zorg ervoor dat je weet hoe degene aan wie je advies geeft in elkaar steekt, zodat je je advies op de persoon of situatie kunt aanpassen. Ook is het belangrijk om je eigen mening op de achtergrond te houden. [207 chars] |
| Wat is verschil tussen 2D-tekening en 3D-tekening van keukenontwerp? [68 chars] | Een 2D-tekening is in feite een plattegrond. Met deze 2D tekening kan je goed kijken of je alle ruimte optimaal benut. Ook krijg je een duidelijk beeld van de indeling. Als je tevreden bent met het 2D keukenontwerp wordt er een 3D tekening gemaakt met behulp van ontwerpsoftware. Een 3D keukenontwerp is ontzettend realistisch en geeft echt een kijkje in de keuken. [365 chars] |
| Hoe programmeer ik NFC-tags? [28 chars] | Dit doe je gemakkelijk met software op je NFC ondersteunende telefoon. Hier vind je meer informatie. [100 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WebFAQ: A Multilingual Collection of Natural Q&A Datasets for Dense Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2502.20936](https://arxiv.org/abs/2502.20936) |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | [https://arxiv.org/abs/2509.12340](https://arxiv.org/abs/2509.12340) |
| mteb/WebFAQRetrieval |  | dataset card | [https://huggingface.co/datasets/mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval) |
| PaDaS Lab Hugging Face organization |  | project page | [https://huggingface.co/PaDaS-Lab](https://huggingface.co/PaDaS-Lab) |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Wat is belangrijk bij adviseren? | A Dutch answer explains that advice should be adapted to the person or situation and that one's own opinion should stay in the background. |
| Wat is verschil tussen 2D-tekening en 3D-tekening van keukenontwerp? | A Dutch answer explains that a 2D drawing is a floor plan and that a 3D design follows after the layout is satisfactory. |
| Hoe programmeer ik NFC-tags? | A short Dutch answer says this can be done with software on an NFC-capable phone. |
| Heb je voor Japan een visum nodig? | A Dutch answer says no visa is needed for stays up to 90 days, with a visa required for longer stays. |
| Met welk type foto's kan ik MijnKaart maken? | A Dutch answer says recent digital-camera photos can be used and explains how upload indicators show whether resolution is sufficient. |
